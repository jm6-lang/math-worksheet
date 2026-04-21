#!/usr/bin/env python3
"""Auto collector v4 - RSS feeds + web search + fixed WP publishing"""
import json, os, re, sys, sqlite3, time, random, logging, traceback
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin, quote

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
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125.0 Safari/537.36",
]

# ===== DB =====
def init_db():
    c = sqlite3.connect(DB_PATH)
    c.execute("CREATE TABLE IF NOT EXISTS pub (id INTEGER PRIMARY KEY, url TEXT UNIQUE, title TEXT, post_id INTEGER, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, kw TEXT)")
    c.commit()
    return c

def is_done(c, url, title=None):
    if c.execute("SELECT 1 FROM pub WHERE url=?", (url,)).fetchone(): return True
    if title and c.execute("SELECT 1 FROM pub WHERE title=?", (title,)).fetchone(): return True
    return False

def save(c, url, title, pid, kw):
    try: c.execute("INSERT OR IGNORE INTO pub(url,title,post_id,kw) VALUES(?,?,?,?)", (url, title, pid, kw)); c.commit()
    except: pass

def mksess():
    s = requests.Session()
    s.headers["User-Agent"] = random.choice(UAS)
    s.headers["Accept-Language"] = "zh-CN,zh;q=0.9"
    return s

def is_blacklisted(url):
    domain = urlparse(url).netloc.lower()
    full = url.lower()
    for bl in CFG.get("blacklisted_domains", []):
        if bl.lower() in domain or bl.lower() in full:
            return True
    return False

# ===== RSS Feed Reader =====
def fetch_rss(sess, feed_url):
    """Fetch articles from an RSS feed"""
    try:
        r = sess.get(feed_url, timeout=20, headers={"User-Agent": random.choice(UAS)})
        if r.status_code != 200:
            log.debug("RSS feed error {}: {}".format(feed_url, r.status_code))
            return []

        feed = feedparser.parse(r.text)
        results = []
        for entry in feed.entries[:15]:
            link = entry.get("link", "")
            title = entry.get("title", "")
            if not link or not title:
                continue
            if is_blacklisted(link):
                continue
            # Check if published within last year
            published = entry.get("published_parsed") or entry.get("updated_parsed")
            if published:
                from time import mktime
                pub_ts = mktime(published)
                if time.time() - pub_ts > 365 * 86400:
                    continue

            results.append({
                "title": title,
                "url": link,
                "kw": "RSS:{}".format(urlparse(feed_url).netloc),
                "src": "rss",
                "summary": entry.get("summary", ""),
            })

        log.info("RSS {}: {} items".format(urlparse(feed_url).netloc, len(results)))
        return results
    except Exception as e:
        log.error("RSS err {}: {}".format(feed_url, e))
        return []

# ===== Web Search (backup) =====
def search_bing(sess, kw, pg=1):
    off = (pg - 1) * 10
    url = "https://cn.bing.com/search?q={}&count=10&offset={}&setlang=zh-Hans&cc=cn".format(quote(kw), off)
    try:
        r = sess.get(url, timeout=15)
        if r.status_code != 200: return []
        soup = BeautifulSoup(r.text, "lxml")
        res = []
        for li in soup.select("li.b_algo"):
            a = li.select_one("h2 a")
            if a and a.get("href"):
                href = a["href"]
                if is_blacklisted(href): continue
                title = a.get_text(strip=True)
                if len(title) > 8:
                    res.append({"title": title, "url": href, "kw": kw, "src": "bg"})
        log.info("Bing \"{}\": {} items".format(kw, len(res)))
        return res
    except Exception as e:
        log.error("Bing err: {}".format(e))
        return []

# ===== Content Extraction =====
def extract(sess, url, summary=""):
    if is_blacklisted(url): return None
    try:
        h = {"User-Agent": random.choice(UAS), "Accept-Language": "zh-CN,zh;q=0.9"}
        r = sess.get(url, timeout=20, headers=h, allow_redirects=True)
        r.raise_for_status()
        real_url = r.url
        html = r.text

        if len(html) < 2000: return None
        if is_blacklisted(real_url): return None

        title = ""
        content_html = ""
        imgs = []

        # trafilatura
        if HAS_TRAF:
            try:
                text = trafilatura.extract(html, output_format="html", include_images=True,
                                          include_links=False, favor_precision=True, include_formatting=True)
                clean = re.sub(r"<[^>]+>", "", text).strip() if text else ""
                min_len = CFG.get("min_content_length", 500)
                if text and len(clean) > min_len:
                    meta = trafilatura.extract_metadata(html)
                    title = meta.title if meta and meta.title else ""
                    soup = BeautifulSoup(html, "lxml")
                    if not title:
                        tt = soup.select_one("title")
                        title = tt.get_text(strip=True) if tt else ""
                    content_html = text
                    for img in soup.select("article img, .article-content img, .post-content img, .entry-content img, .content img, main img, .rich_media_content img, .post-body img")[:5]:
                        src = img.get("data-src") or img.get("data-original") or img.get("data-lazy-src") or img.get("src") or ""
                        if src and not src.startswith("data:") and ("http" in src or src.startswith("//")):
                            if src.startswith("//"): src = "https:" + src
                            imgs.append(src)
                    if title and len(title) > 6:
                        return {"title": title, "html": content_html, "imgs": imgs, "url": real_url}
            except Exception as e:
                log.debug("trafilatura err: {}".format(e))

        # Fallback: if we have an RSS summary, use it
        if summary and len(summary) > 200:
            soup = BeautifulSoup(html, "lxml")
            tt = soup.select_one("title")
            title = tt.get_text(strip=True) if tt else ""
            # Clean summary to HTML
            clean = BeautifulSoup(summary, "lxml").get_text(strip=True)
            if len(clean) > 100:
                ps = [p.strip() for p in clean.split('\n') if p.strip()]
                content_html = "".join("<p>{}</p>".format(p) for p in ps)
                if title and len(title) > 6:
                    return {"title": title, "html": content_html, "imgs": imgs, "url": real_url}

        return None
    except Exception as e:
        log.debug("Extract err {}: {}".format(url, e))
        return None

# ===== WordPress =====
class WP:
    def __init__(self):
        self.base = CFG["wp_url"].rstrip("/") + "/wp-json/wp/v2"
        self.s = requests.Session()
        self.s.headers["User-Agent"] = "AutoCollector/4.0"
        api_token = CFG.get("wp_api_token", "")
        if api_token:
            self.s.headers["X-Api-Token"] = api_token

    def _post(self, path, **kwargs):
        try:
            r = self.s.post(self.base + path, timeout=30, **kwargs)
            if r.status_code == 401:
                log.error("Auth FAILED (401)"); return None
            if r.status_code not in (200, 201):
                log.error("POST {} failed: {} {}".format(path, r.status_code, r.text[:200])); return None
            return r.json()
        except Exception as e:
            log.error("POST err: {}".format(e)); return None

    def tag_id(self, name):
        try:
            r = self.s.get(self.base + "/tags", params={"search": name}, timeout=10)
            if r.status_code == 200:
                for t in r.json():
                    if t["name"] == name: return t["id"]
            data = self._post("/tags", json={"name": name})
            if data and "id" in data: return data["id"]
        except: pass
        return None

    def upload_img(self, img_url):
        try:
            ir = requests.get(img_url, timeout=15, stream=True, headers={"User-Agent": random.choice(UAS)})
            if ir.status_code != 200: return None
            ct = ir.headers.get("Content-Type", "image/jpeg")
            if "image" not in ct: return None
            cl = int(ir.headers.get("Content-Length", 0))
            if cl > 5 * 1024 * 1024: return None
            ext = ct.split("/")[-1].replace("jpeg", "jpg")
            fn = "auto_{}_{}.{}".format(int(time.time()), random.randint(1000, 9999), ext)
            r = self.s.post(self.base + "/media", files={"file": (fn, ir.content)},
                           headers={"Content-Disposition": "attachment; filename=\"{}\"".format(fn)}, timeout=30)
            if r.status_code in (200, 201):
                d = r.json()
                log.info("Img OK: {} (ID:{})".format(fn, d.get("id")))
                return d.get("id"), d.get("source_url")
        except Exception as e:
            log.debug("Img err: {}".format(e))
        return None

    def post(self, title, content, feat_id=None, cat_id=None, tags=None):
        d = {"title": title, "content": content, "status": "publish", "comment_status": "open"}
        if feat_id: d["featured_media"] = feat_id
        if cat_id: d["categories"] = [cat_id]
        if tags: d["tags"] = [t for t in tags if t]
        data = self._post("/posts", json=d)
        if data and "id" in data:
            log.info("Published ID {}: {}".format(data["id"], title[:50]))
            return data["id"]
        return None

# ===== Main =====
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
        cat_id = CFG.get("category_id", 53)  # 赚钱教程
        log.info("Category ID: {}".format(cat_id))

        sess = mksess()
        cnt = 0
        mx = CFG.get("max_posts_per_run", 8)

        # ===== Phase 1: RSS Feeds (primary) =====
        log.info("\n=== Phase 1: RSS Feeds ===")
        for feed_url in CFG.get("rss_feeds", []):
            if cnt >= mx: break
            items = fetch_rss(sess, feed_url)
            for item in items:
                if cnt >= mx: break
                url = item["url"]
                title = item["title"]
                if is_done(db, url, title):
                    log.info("Skip (done): {}".format(title[:50]))
                    continue
                time.sleep(random.uniform(1, 3))
                art = extract(sess, url, summary=item.get("summary", ""))
                if not art:
                    log.info("Skip (no content): {}".format(url[:60]))
                    continue
                final_title = art["title"] or title
                if not final_title or len(final_title) < 8: continue

                src_netloc = urlparse(url).netloc
                wp_html = "<!-- src:{} -->\n".format(url)
                wp_html += "<p><em>\u672c\u6587\u6574\u7406\u81ea\u7f51\u7edc\uff0c\u4ec5\u4f9b\u53c2\u8003\u3002</em></p>\n"
                wp_html += art["html"]
                wp_html += "\n<p style=\"color:#888;font-size:12px\">\u6765\u6e90\uff1a<a href=\"{}\" target=\"_blank\" rel=\"nofollow\">{}</a></p>".format(url, src_netloc)

                fid = None
                for iu in art.get("imgs", []):
                    if is_blacklisted(iu): continue
                    result = wp.upload_img(iu)
                    if result:
                        mid, murl = result
                        fid = mid
                        wp_html = '<img src="{}" alt="{}" />\n'.format(murl, final_title[:30]) + wp_html
                        break

                tids = []
                kw_word = item.get("kw", "").split(":")[-1] if ":" in item.get("kw", "") else ""
                if kw_word:
                    tid = wp.tag_id(kw_word)
                    if tid: tids.append(tid)

                pid = wp.post(final_title, wp_html, fid, cat_id, tids)
                if pid:
                    save(db, url, final_title, pid, item.get("kw", ""))
                    cnt += 1
                    log.info("Done #{}/{}: {}".format(cnt, mx, final_title[:50]))
                else:
                    log.warning("Fail: {}".format(final_title[:50]))

        # ===== Phase 2: Web Search (backup, if we still need more) =====
        if cnt < mx:
            remaining = mx - cnt
            log.info("\n=== Phase 2: Web Search (need {} more) ===".format(remaining))
            kws = CFG.get("keywords", [])
            random.shuffle(kws)
            for kw in kws:
                if cnt >= mx: break
                items = search_bing(sess, kw)
                for item in items:
                    if cnt >= mx: break
                    url = item["url"]
                    if is_done(db, url, item.get("title")): continue
                    time.sleep(random.uniform(2, 4))
                    art = extract(sess, url)
                    if not art: continue
                    final_title = art["title"] or item["title"]
                    if not final_title or len(final_title) < 8: continue

                    src_netloc = urlparse(url).netloc
                    wp_html = "<!-- src:{} -->\n".format(url)
                    wp_html += "<p><em>\u672c\u6587\u6574\u7406\u81ea\u7f51\u7edc\uff0c\u4ec5\u4f9b\u53c2\u8003\u3002</em></p>\n"
                    wp_html += art["html"]
                    wp_html += "\n<p style=\"color:#888;font-size:12px\">\u6765\u6e90\uff1a<a href=\"{}\" target=\"_blank\" rel=\"nofollow\">{}</a></p>".format(url, src_netloc)

                    fid = None
                    for iu in art.get("imgs", []):
                        if is_blacklisted(iu): continue
                        result = wp.upload_img(iu)
                        if result:
                            mid, murl = result
                            fid = mid
                            wp_html = '<img src="{}" alt="{}" />\n'.format(murl, final_title[:30]) + wp_html
                            break

                    tids = []
                    tn = kw.split()[0]
                    if tn:
                        tid = wp.tag_id(tn)
                        if tid: tids.append(tid)

                    pid = wp.post(final_title, wp_html, fid, cat_id, tids)
                    if pid:
                        save(db, url, final_title, pid, kw)
                        cnt += 1
                        log.info("Done #{}/{}: {}".format(cnt, mx, final_title[:50]))

        db.close()
        log.info("Finished - {}/{} published".format(cnt, mx))
    finally:
        try: os.remove(LOCK_PATH)
        except: pass

if __name__ == "__main__":
    main()
