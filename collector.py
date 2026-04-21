#!/usr/bin/env python3
"""Auto collector for money-making tutorials"""
import json, os, re, sys, sqlite3, time, random, logging, hashlib
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin, quote

import requests
from bs4 import BeautifulSoup

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
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125.0 Safari/537.36",
]

def init_db():
    c = sqlite3.connect(DB_PATH)
    c.execute("CREATE TABLE IF NOT EXISTS pub (id INTEGER PRIMARY KEY, url TEXT UNIQUE, title TEXT, post_id INTEGER, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, kw TEXT)")
    c.commit()
    return c

def is_done(c, url, title=None):
    if c.execute("SELECT 1 FROM pub WHERE url=?", (url,)).fetchone():
        return True
    if title and c.execute("SELECT 1 FROM pub WHERE title=?", (title,)).fetchone():
        return True
    return False

def save(c, url, title, pid, kw):
    try:
        c.execute("INSERT OR IGNORE INTO pub(url,title,post_id,kw) VALUES(?,?,?,?)", (url, title, pid, kw))
        c.commit()
    except:
        pass

def mksess():
    s = requests.Session()
    s.headers["User-Agent"] = random.choice(UAS)
    s.headers["Accept-Language"] = "zh-CN,zh;q=0.9"
    return s

def search_baidu(sess, kw, pg=1):
    ts = int(time.time())
    ts0 = ts - 365 * 86400
    url = "https://www.baidu.com/s?wd={}&pn={}&rn=10&gpc=stf%3D{}%2C{}".format(quote(kw), (pg - 1) * 10, ts0, ts)
    try:
        r = sess.get(url, timeout=15)
        if r.status_code != 200:
            return []
        if "\u767e\u5ea6\u5b89\u5168\u9a8c\u8bc1" in r.text:
            return []
        soup = BeautifulSoup(r.text, "lxml")
        res = []
        for d in soup.select("#content_left > div"):
            cls = " ".join(d.get("class", []))
            if "result" not in cls and "c-container" not in cls:
                continue
            if d.select_one(".ec_wise_ad,.ec_youxuan"):
                continue
            a = d.select_one("h3 a, .t a, .c-title a")
            if a and a.get("href", "").startswith("http"):
                res.append({"title": a.get_text(strip=True), "url": a["href"], "kw": kw, "src": "bd"})
        log.info("Baidu {} p{}: {} items".format(kw, pg, len(res)))
        return res
    except Exception as e:
        log.error("Baidu err: {}".format(e))
        return []

def search_bing(sess, kw, pg=1):
    off = (pg - 1) * 10
    url = "https://cn.bing.com/search?q={}&count=10&offset={}&setlang=zh-Hans".format(quote(kw), off)
    try:
        r = sess.get(url, timeout=15)
        if r.status_code != 200:
            return []
        soup = BeautifulSoup(r.text, "lxml")
        res = []
        for li in soup.select("li.b_algo"):
            a = li.select_one("h2 a")
            if a and a.get("href"):
                res.append({"title": a.get_text(strip=True), "url": a["href"], "kw": kw, "src": "bg"})
        log.info("Bing {} p{}: {} items".format(kw, pg, len(res)))
        return res
    except Exception as e:
        log.error("Bing err: {}".format(e))
        return []

def resolve(sess, url):
    try:
        r = sess.head(url, allow_redirects=True, timeout=10)
        u = r.url
        if "baidu.com" in u:
            return None
        return u
    except:
        return None

def extract(sess, url):
    domain = urlparse(url).netloc
    for bl in CFG.get("blacklisted_domains", []):
        if bl in domain:
            return None
    try:
        h = {"User-Agent": random.choice(UAS), "Accept-Language": "zh-CN,zh;q=0.9"}
        r = sess.get(url, timeout=15, headers=h, allow_redirects=True)
        r.raise_for_status()
        real_url = r.url
        html = r.text
        if len(html) < 1000:
            return None
        title = ""
        content_html = ""
        imgs = []
        if HAS_TRAF:
            text = trafilatura.extract(html, output_format="html", include_images=True, include_links=False, favor_precision=True)
            if text and len(re.sub(r"<[^>]+>", "", text).strip()) > CFG.get("min_content_length", 500):
                meta = trafilatura.extract_metadata(html)
                title = meta.title if meta and meta.title else ""
                soup = BeautifulSoup(html, "lxml")
                if not title:
                    tt = soup.select_one("title")
                    title = tt.get_text(strip=True) if tt else ""
                content_html = text
                for img in soup.select("article img, .article-content img, .post-content img, .entry-content img, main img")[:5]:
                    src = img.get("data-src") or img.get("data-original") or img.get("src")
                    if src and not src.startswith("data:"):
                        imgs.append(urljoin(real_url, src))
                return {"title": title, "html": content_html, "imgs": imgs, "url": real_url}
        soup = BeautifulSoup(html, "lxml")
        tt = soup.select_one("title")
        title = tt.get_text(strip=True) if tt else ""
        for tag in soup.select("script,style,nav,header,footer,aside,.ad,.sidebar,.comment,#comments,.share,.related"):
            tag.decompose()
        art = (soup.select_one("article") or soup.select_one(".article-content") or
               soup.select_one(".post-content") or soup.select_one(".entry-content") or
               soup.select_one("main") or soup.select_one("body"))
        if not art:
            return None
        for img in art.select("img")[:5]:
            src = img.get("data-src") or img.get("data-original") or img.get("src")
            if src and not src.startswith("data:"):
                imgs.append(urljoin(real_url, src))
        txt = art.get_text(separator="\n", strip=True)
        if len(txt) < CFG.get("min_content_length", 500):
            return None
        ps = [p.strip() for p in txt.split("\n") if p.strip() and len(p.strip()) > 20]
        content_html = "".join("<p>{}</p>".format(p) for p in ps)
        return {"title": title, "html": content_html, "imgs": imgs, "url": real_url}
    except Exception as e:
        log.debug("Extract err {}: {}".format(url, e))
        return None

class WP:
    def __init__(self):
        self.base = CFG["wp_url"].rstrip("/") + "/wp-json/wp/v2"
        self.s = requests.Session()
        self.s.auth = (CFG["wp_user"], CFG["wp_app_password"])
        self.s.headers["User-Agent"] = "AutoCollector/1.0"

    def cat_id(self, name):
        try:
            r = self.s.get(self.base + "/categories", params={"search": name}, timeout=10)
            for c in r.json():
                if c["name"] == name:
                    return c["id"]
            r = self.s.post(self.base + "/categories", json={"name": name}, timeout=10)
            return r.json()["id"]
        except Exception as e:
            log.error("Cat err: {}".format(e))
        return 1

    def tag_id(self, name):
        try:
            r = self.s.get(self.base + "/tags", params={"search": name}, timeout=10)
            for t in r.json():
                if t["name"] == name:
                    return t["id"]
            r = self.s.post(self.base + "/tags", json={"name": name}, timeout=10)
            if r.status_code == 201:
                return r.json()["id"]
        except:
            pass
        return None

    def upload_img(self, img_url):
        try:
            ir = requests.get(img_url, timeout=15, stream=True, headers={"User-Agent": random.choice(UAS)})
            if ir.status_code != 200:
                return None
            ct = ir.headers.get("Content-Type", "image/jpeg")
            if "image" not in ct:
                return None
            ext = ct.split("/")[-1].replace("jpeg", "jpg")
            fn = "auto_{}_{}.{}".format(int(time.time()), random.randint(1000, 9999), ext)
            r = self.s.post(self.base + "/media", files={"file": (fn, ir.content)},
                           headers={"Content-Disposition": "attachment; filename=\"{}\"".format(fn)}, timeout=30)
            if r.status_code in (200, 201):
                d = r.json()
                log.info("Img uploaded: {} (ID:{})".format(fn, d.get("id")))
                return d.get("id"), d.get("source_url")
        except Exception as e:
            log.debug("Img err: {}".format(e))
        return None

    def post(self, title, content, feat_id=None, cat_id=None, tags=None):
        d = {"title": title, "content": content, "status": "publish", "comment_status": "open"}
        if feat_id:
            d["featured_media"] = feat_id
        if cat_id:
            d["categories"] = [cat_id]
        if tags:
            d["tags"] = [t for t in tags if t]
        try:
            r = self.s.post(self.base + "/posts", json=d, timeout=30)
            if r.status_code == 201:
                pid = r.json()["id"]
                log.info("Published ID {}: {}".format(pid, title[:50]))
                return pid
            log.error("Post fail ({}): {}".format(r.status_code, r.text[:200]))
        except Exception as e:
            log.error("Post err: {}".format(e))
        return None

def main():
    try:
        open(LOCK_PATH, "x").close()
    except FileExistsError:
        log.warning("Already running, exit.")
        sys.exit(0)
    try:
        log.info("=" * 60)
        log.info("Started {}".format(datetime.now().strftime("%Y-%m-%d %H:%M")))
        log.info("=" * 60)
        db = init_db()
        wp = WP()
        cid = wp.cat_id(CFG.get("category", "\u8d5a\u94b1\u6559\u7a0b"))
        log.info("Category: {} (ID:{})".format(CFG.get("category"), cid))
        sess = mksess()
        cnt = 0
        mx = CFG.get("max_posts_per_run", 5)
        kws = CFG.get("keywords", [])
        random.shuffle(kws)
        for kw in kws:
            if cnt >= mx:
                break
            log.info("--- Keyword: {} ---".format(kw))
            items = search_baidu(sess, kw)
            if not items:
                items = search_bing(sess, kw)
            for it in items:
                if cnt >= mx:
                    break
                url = it["url"]
                if it["src"] == "bd":
                    url = resolve(sess, url)
                    if not url:
                        continue
                if is_done(db, url, it.get("title")):
                    log.info("Skip (done): {}".format(url[:60]))
                    continue
                time.sleep(random.uniform(1.5, 3.5))
                art = extract(sess, url)
                if not art:
                    log.info("Skip (no content): {}".format(url[:60]))
                    continue
                title = art["title"] or it.get("title", "")
                if not title:
                    continue
                src_line = "\u6765\u6e90\uff1a<a href=\"{}\" target=\"_blank\" rel=\"nofollow\">{}</a>".format(url, urlparse(url).netloc)
                wp_html = "<!-- src:{} -->\n<p><em>\u672c\u6587\u6574\u7406\u81ea\u7f51\u7edc\uff0c\u4ec5\u4f9b\u53c2\u8003\u3002</em></p>\n".format(url)
                wp_html += art["html"]
                wp_html += "\n<p style=\"color:#888;font-size:12px\">{}</p>".format(src_line)
                fid = None
                for iu in art.get("imgs", []):
                    mid, murl = wp.upload_img(iu)
                    if mid:
                        fid = mid
                        wp_html = "<img src=\"{}\" alt=\"{}\" />\n".format(murl, title) + wp_html
                        break
                tids = []
                tn = kw.split()[0]
                if tn:
                    tid = wp.tag_id(tn)
                    if tid:
                        tids.append(tid)
                pid = wp.post(title, wp_html, fid, cid, tids)
                if pid:
                    save(db, url, title, pid, kw)
                    cnt += 1
                    log.info("Done #{}/{}: {}".format(cnt, mx, title[:50]))
                else:
                    log.warning("Fail: {}".format(title[:50]))
        db.close()
        log.info("Finished - {}/{} published".format(cnt, mx))
    finally:
        try:
            os.remove(LOCK_PATH)
        except:
            pass

if __name__ == "__main__":
    main()
