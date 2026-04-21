#!/usr/bin/env python3
"""Auto collector v5 - Optimized for Chinese websites"""
import json, os, re, sys, sqlite3, time, random, logging, traceback
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

UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
]

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
        if bl in domain:
            return True
    return False

def extract_content(url, session=None):
    """Extract content using BeautifulSoup (optimized for Chinese sites)"""
    imgs = []
    try:
        headers = {
            "User-Agent": random.choice(UAS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        r = (session or requests).get(url, headers=headers, timeout=15)
        html = r.text
        
        if len(html) < 2000:
            return None
        
        try:
            soup = BeautifulSoup(html, "lxml")
        except:
            soup = BeautifulSoup(html, "html.parser")
        
        # Remove unwanted elements
        for tag in soup(["script", "style", "nav", "header", "footer", "aside", "iframe", "noscript"]):
            tag.decompose()
        
        # Get title
        title_tag = soup.select_one("title")
        title = title_tag.get_text(strip=True) if title_tag else ""
        
        # Find content - priority order for Chinese sites
        content_selectors = [
            "article",
            '[class*="article-content"]', '[class*="article_content"]',
            '[class*="post-content"]', '[class*="post_content"]',
            '[class*="entry-content"]', '[class*="entry_content"]',
            '[class*="content"]', '[class*="main-content"]',
            '[class*="detail"]', '[class*="article"]',
            '[id*="article"]', '[id*="content"]', '[id*="main"]',
            ".rich_media_content", ".article-body", ".post-body",
        ]
        
        content_text = ""
        for selector in content_selectors:
            elem = soup.select_one(selector)
            if elem:
                text = elem.get_text(separator="\n", strip=True)
                if len(text) > 300:
                    content_text = text
                    break
        
        # Fallback: collect all substantial paragraphs
        if not content_text:
            paragraphs = soup.find_all("p")
            parts = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 30]
            content_text = "\n".join(parts)
        
        # Extract images
        for img in soup.select("article img, .content img, main img, .article img, .post img")[:5]:
            src = img.get("data-src") or img.get("data-original") or img.get("src") or ""
            if src and "http" in src and not src.startswith("data:"):
                if src.startswith("//"): src = "https:" + src
                imgs.append(src)
        
        # Clean whitespace
        lines = [l.strip() for l in content_text.split("\n") if l.strip()]
        content_text = "\n".join(lines)
        
        min_len = CFG.get("min_content_length", 400)
        
        # Try trafilatura if content too short
        if len(content_text) < min_len and HAS_TRAF:
            try:
                text = trafilatura.extract(html, output_format="text")
                if text and len(text) > min_len:
                    content_text = text
            except: pass
        
        if title and len(title) > 3 and len(content_text) > 200:
            return {"title": title[:200], "html": content_text[:15000], "imgs": imgs[:5], "url": url}
        return None
    except Exception as e:
        log.debug("Extract err: {}".format(e))
        return None

class WP:
    def __init__(self):
        self.base = CFG["wp_url"].rstrip("/") + "/wp-json/wp/v2"
        self.s = requests.Session()
        self.s.headers["User-Agent"] = "AutoCollector/5.0"
        token = CFG.get("wp_api_token", "")
        if token:
            self.s.headers["Authorization"] = "Bearer " + token

    def _post(self, path, **kwargs):
        try:
            r = self.s.post(self.base + path, timeout=30, **kwargs)
            if r.status_code == 401:
                log.error("Auth FAILED (401)"); return None
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
                log.info("Img OK: ID {}".format(d.get("id")))
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
        log.info("Started {}".format(datetime.now().strftime("%Y-%m-%d %H:%M")))
        log.info("=" * 60)

        db = init_db()
        wp = WP()
        cat_id = CFG.get("category_id", 53)
        log.info("Category ID: {}".format(cat_id))

        cnt = 0
        mx = CFG.get("max_posts_per_run", 8)

        # Phase 1: RSS Feeds
        log.info("\n=== Phase 1: RSS Feeds ===")
        for feed_url in CFG.get("rss_feeds", []):
            try:
                feed = feedparser.parse(feed_url)
                log.info("RSS {}: {} items".format(feed_url.split("/")[2], len(feed.entries)))
                for entry in feed.entries[:15]:
                    if is_done(db, entry.link, entry.get("title")):
                        log.info("Skip (done): {}".format(entry.get("title", "")[:40]))
                        continue
                    result = extract_content(entry.link)
                    if result:
                        feat_id = None
                        if result["imgs"]:
                            feat_id, _ = wp.upload_img(result["imgs"][0])
                            time.sleep(1)
                        pid = wp.post(result["title"], result["html"], feat_id, cat_id)
                        if pid:
                            db.execute("INSERT INTO pub (url, title, post_id, kw) VALUES (?, ?, ?, ?)",
                                      (entry.link, result["title"], pid, "rss"))
                            db.commit()
                            cnt += 1
                            log.info("Published: {}".format(result["title"][:50]))
                            if cnt >= mx: break
                    else:
                        log.info("Skip (no content): {}".format(entry.link))
                    time.sleep(2)
                if cnt >= mx: break
            except Exception as e:
                log.error("RSS err {}: {}".format(feed_url, e))
        
        log.info("Finished - {}/{} published".format(cnt, mx))
        
    finally:
        try: os.remove(LOCK_PATH)
        except: pass

if __name__ == "__main__":
    main()
