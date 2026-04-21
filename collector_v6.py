#!/usr/bin/env python3
"""Auto collector v6 - Enhanced with better headers and retry logic"""
import json, os, re, sys, sqlite3, time, random, logging
from datetime import datetime
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
import feedparser

try:
    import trafilatura
    HAS_TRAF = True
except ImportError:
    HAS_TRAF = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
DB_PATH = os.path.join(BASE_DIR, "published.db")
LOCK_PATH = os.path.join(BASE_DIR, "collector.lock")
os.makedirs(LOG_DIR, exist_ok=True)

with open(os.path.join(BASE_DIR, "config.json"), "r", encoding="utf-8") as _f:
    CFG = json.load(_f)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "run_{}.log".format(datetime.now().strftime("%Y%m%d"))), encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ])
log = logging.getLogger(__name__)

# Realistic browser headers
UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

def init_db():
    c = sqlite3.connect(DB_PATH)
    c.execute("CREATE TABLE IF NOT EXISTS pub (id INTEGER PRIMARY KEY, url TEXT UNIQUE, title TEXT, post_id INTEGER, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, kw TEXT)")
    c.commit()
    return c

def is_done(c, url, title=None):
    if c.execute("SELECT 1 FROM pub WHERE url=?", (url,)).fetchone(): return True
    if title and c.execute("SELECT 1 FROM pub WHERE title=?", (title,)).fetchone(): return True
    return False

def is_blacklisted(url):
    domain = urlparse(url).netloc.lower()
    for bl in CFG.get("blacklisted_domains", []):
        if bl in domain: return True
    return False

def extract_content(url, session=None, retry=2):
    """Extract content with enhanced headers and retry"""
    for attempt in range(retry):
        try:
            headers = HEADERS.copy()
            headers["User-Agent"] = random.choice(UAS)
            
            s = session or requests
            r = s.get(url, headers=headers, timeout=20, allow_redirects=True)
            
            if r.status_code != 200:
                log.debug("Status {} for {}".format(r.status_code, url))
                time.sleep(2)
                continue
            
            html = r.text
            if len(html) < 3000:
                time.sleep(1)
                continue
            
            soup = BeautifulSoup(html, "lxml")
            
            # Remove unwanted
            for tag in soup(["script", "style", "nav", "header", "footer", "aside", "iframe", "noscript", "form", "button"]):
                tag.decompose()
            
            # Title
            title = ""
            for sel in ["h1.title", "h1.article-title", "article h1", ".post-title", "h1", "title"]:
                t = soup.select_one(sel)
                if t:
                    title = t.get_text(strip=True)
                    break
            if not title:
                t = soup.select_one("title")
                if t: title = t.get_text(strip=True)
            
            # Content selectors - Chinese sites
            content = ""
            selectors = [
                "article.article-content", "article.post-content", "article.entry-content",
                "div.article-content", "div.post-content", "div.entry-content",
                ".article-body", ".post-body", ".entry-content",
                "article", ".content-detail", ".article-detail",
                "[class*=content]", "[class*=article]", "[class*=post]",
            ]
            
            for sel in selectors:
                elem = soup.select_one(sel)
                if elem:
                    text = elem.get_text(separator="\n", strip=True)
                    if len(text) > 400:
                        content = text
                        break
            
            # Fallback: paragraphs
            if not content or len(content) < 400:
                paras = []
                for p in soup.find_all("p"):
                    t = p.get_text(strip=True)
                    if len(t) > 40:
                        paras.append(t)
                content = "\n".join(paras)
            
            # Images
            imgs = []
            for img in soup.select("article img, .content img, main img, .article img")[:5]:
                src = img.get("data-src") or img.get("data-original") or img.get("src") or ""
                if src and "http" in src and not src.startswith("data:") and "logo" not in src.lower():
                    if src.startswith("//"): src = "https:" + src
                    imgs.append(src)
            
            # Clean
            lines = [l.strip() for l in content.split("\n") if l.strip()]
            content = "\n".join(lines)
            
            min_len = CFG.get("min_content_length", 400)
            
            # Try trafilatura if short
            if len(content) < min_len and HAS_TRAF:
                try:
                    txt = trafilatura.extract(html, output_format="text")
                    if txt and len(txt) > min_len:
                        content = txt
                        # Also try to get images
                        for img in soup.select("img[src]")[:3]:
                            src = img.get("src") or ""
                            if src and "http" in src and "logo" not in src.lower():
                                if src.startswith("//"): src = "https:" + src
                                imgs.append(src)
                except: pass
            
            if title and len(title) > 5 and len(content) > 300:
                log.info("Extracted {} chars from {}".format(len(content), url[:50]))
                return {"title": title[:200], "html": content[:15000], "imgs": imgs[:5], "url": url}
            
            time.sleep(1)
            
        except Exception as e:
            log.debug("Extract err: {} - {}".format(url[:50], str(e)[:50]))
            time.sleep(2)
    
    return None

class WP:
    def __init__(self):
        self.base = CFG["wp_url"].rstrip("/") + "/wp-json/wp/v2"
        self.s = requests.Session()
        self.s.headers["User-Agent"] = "Mozilla/5.0 AutoCollector/6.0"
        token = CFG.get("wp_api_token", "")
        if token:
            self.s.headers["Authorization"] = "Bearer " + token

    def _post(self, path, **kwargs):
        try:
            r = self.s.post(self.base + path, timeout=30, **kwargs)
            if r.status_code == 401:
                log.error("Auth FAILED"); return None
            if r.status_code not in (200, 201):
                log.error("POST {} failed: {}".format(path, r.status_code)); return None
            return r.json()
        except Exception as e:
            log.error("POST err: {}".format(e)); return None

    def upload_img(self, img_url):
        try:
            ir = requests.get(img_url, timeout=15, stream=True, headers={"User-Agent": random.choice(UAS)})
            if ir.status_code != 200: return None
            ct = ir.headers.get("Content-Type", "image/jpeg")
            if "image" not in ct: return None
            ext = ct.split("/")[-1].replace("jpeg", "jpg")
            fn = "auto_{}_{}.{}".format(int(time.time()), random.randint(1000, 9999), ext)
            r = self.s.post(self.base + "/media", files={"file": (fn, ir.content)}, timeout=30)
            if r.status_code in (200, 201):
                d = r.json()
                return d.get("id"), d.get("source_url")
        except Exception as e:
            log.debug("Img err: {}".format(e))
        return None

    def post(self, title, content, feat_id=None, cat_id=None, tags=None):
        d = {"title": title, "content": content, "status": "publish", "comment_status": "open"}
        if feat_id: d["featured_media"] = feat_id
        if cat_id: d["categories"] = [cat_id]
        data = self._post("/posts", json=d)
        if data and "id" in data:
            log.info("Published ID {}: {}".format(data["id"], title[:50]))
            return data["id"]
        return None

def main():
    try:
        open(LOCK_PATH, "x").close()
    except FileExistsError:
        log.warning("Already running"); sys.exit(0)
    
    try:
        log.info("=" * 60)
        log.info("Started {} v6".format(datetime.now().strftime("%Y-%m-%d %H:%M")))
        log.info("=" * 60)

        db = init_db()
        wp = WP()
        cat_id = CFG.get("category_id", 53)
        
        cnt = 0
        mx = CFG.get("max_posts_per_run", 8)

        log.info("\n=== Phase 1: RSS Feeds ===")
        for feed_url in CFG.get("rss_feeds", []):
            if cnt >= mx: break
            try:
                feed = feedparser.parse(feed_url, request_headers={"User-Agent": random.choice(UAS)})
                source = feed_url.split("/")[2]
                log.info("RSS {}: {} items".format(source, len(feed.entries)))
                
                for entry in feed.entries[:15]:
                    if cnt >= mx: break
                    if is_done(db, entry.link, entry.get("title")):
                        log.info("Skip (done): {}".format(entry.get("title", "")[:40]))
                        continue
                    
                    result = extract_content(entry.link)
                    if result:
                        feat_id = None
                        if result["imgs"]:
                            feat_id, _ = wp.upload_img(result["imgs"][0])
                            time.sleep(1.5)
                        pid = wp.post(result["title"], result["html"], feat_id, cat_id)
                        if pid:
                            db.execute("INSERT INTO pub (url, title, post_id, kw) VALUES (?, ?, ?, ?)",
                                      (entry.link, result["title"], pid, "rss"))
                            db.commit()
                            cnt += 1
                            log.info("OK: {}".format(result["title"][:50]))
                    else:
                        log.info("Skip (no content): {}".format(entry.link))
                    time.sleep(2)
                    
            except Exception as e:
                log.error("RSS err {}: {}".format(feed_url[:50], e))
        
        log.info("\nFinished - {}/{} published".format(cnt, mx))
        
    finally:
        try: os.remove(LOCK_PATH)
        except: pass

if __name__ == "__main__":
    main()
