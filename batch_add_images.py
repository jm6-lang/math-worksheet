#!/usr/bin/env python3
"""
WordPress Auto Featured Image - 按文章标题/分类搜索免费图并设为特色图
支持: LoremFlickr(关键词随机图) + Wikimedia Commons
"""
import os, re, time, json, random, sys
import requests
from datetime import datetime

# ====== 配置 ======
SITE_URL     = "https://skillxm.cn"
API_TOKEN    = "s6eW 2kHy 8yqu XNuY JjoK HHOR"
WP_USER      = "admin"
BASE_DIR     = "/www/wwwroot/resource_site/auto_collect"

HEADERS = {
    "Authorization": f"Basic {__import__('base64').b64encode(f'{WP_USER}:{API_TOKEN}'.encode()).decode()}",
    "Content-Type": "application/json; charset=utf-8",
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
]

# ====== 图源 ======
def get_loremflickr_url(keyword, size=800):
    """LoremFlickr - 随机关键词图片，可靠"""
    kw = requests.utils.quote(keyword)
    return f"https://loremflickr.com/{size}/{size}/{kw}?random={random.randint(1,9999)}"

def search_wikimedia(keyword):
    """Wikimedia Commons 搜索，找一张可用图片URL"""
    url = (f"https://commons.wikimedia.org/w/api.php?action=query&list=search"
           f"&srsearch={requests.utils.quote(keyword)}&srnamespace=6&srlimit=8&format=json")
    try:
        r = requests.get(url, timeout=12, headers={"User-Agent": random.choice(USER_AGENTS)})
        data = r.json()
        results = data.get("query", {}).get("search", [])
        for item in results:
            raw_title = item["title"].replace("File:", "")
            # Wikimedia 直接文件URL
            safe_name = requests.utils.quote(raw_name := raw_title.replace(" ", "_"))
            direct = f"https://upload.wikimedia.org/wikipedia/commons/{safe_name}"
            # 试 .jpg/.jpeg/.png
            for ext in ["", ".jpg", ".jpeg", ".png", "-original"]:
                img_url = direct + ext if ext == "-original" or not ext else direct.replace("_", "%20") + ext
                try:
                    h = requests.head(img_url, timeout=6,
                                     headers={"User-Agent": random.choice(USER_AGENTS)})
                    ct = h.headers.get("Content-Type", "")
                    if h.status_code == 200 and "image" in ct:
                        return img_url, raw_title
                    if h.status_code == 429:
                        time.sleep(2)
                except:
                    pass
        return None, None
    except Exception as e:
        return None, None

# ====== 下载图片 ======
def download_image(url, timeout=15):
    for attempt in range(2):
        try:
            r = requests.get(url, timeout=timeout, headers={"User-Agent": random.choice(USER_AGENTS)},
                            allow_redirects=True)
            if r.status_code == 200 and len(r.content) > 5000:
                ct = r.headers.get("Content-Type", "image/jpeg")
                return r.content, ct
            if r.status_code == 429:
                time.sleep(3)
        except:
            pass
    return None, None

# ====== 上传到 WordPress ======
def upload_to_wp(image_data, content_type, filename, post_id):
    try:
        headers = {
            **HEADERS,
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": content_type,
        }
        r = requests.post(f"{SITE_URL}/wp-json/wp/v2/media",
                          headers=headers, data=image_data, timeout=30)
        if r.status_code not in [200, 201]:
            return None, None
        media = r.json()
        media_id = media["id"]
        media_url = media["source_url"]

        # 设为特色图
        r2 = requests.post(f"{SITE_URL}/wp-json/wp/v2/posts/{post_id}",
                           headers=HEADERS, json={"featured_media": media_id}, timeout=10)
        return media_id if r2.status_code < 400 else None, media_url
    except Exception as e:
        return None, None

# ====== 搜索图片（多策略） ======
def find_image_for_post(title_plain, category_kw, cat_id):
    """返回 (图片URL, 来源标签) 或 None"""
    # 组合关键词
    keywords = [
        title_plain[:20] if title_plain else category_kw,
        category_kw,
        "online business",
        "technology",
    ]
    keywords = [k.strip() for k in keywords if k.strip()][:3]

    for kw in keywords:
        time.sleep(0.8)

        # 策略1: LoremFlickr (快速，可靠)
        try:
            lf_url = get_loremflickr_url(kw)
            h = requests.head(lf_url, timeout=10, allow_redirects=True,
                            headers={"User-Agent": random.choice(USER_AGENTS)})
            if h.status_code == 200 and "image" in h.headers.get("Content-Type", ""):
                return lf_url, "loremflickr"
        except:
            pass

        # 策略2: Wikimedia
        img_url, title = search_wikimedia(kw)
        if img_url:
            return img_url, f"wikimedia:{title[:30]}"

    return None, None

# ====== 主逻辑 ======
def process_posts(offset=0, limit=30, delay=3):
    """处理一批文章"""
    # 获取需要图片的文章（featured_media = 0）
    r = requests.get(
        f"{SITE_URL}/wp-json/wp/v2/posts",
        params={"per_page": limit, "offset": offset, "status": "publish",
                "_fields": "id,title.rendered,categories,featured_media"},
        headers=HEADERS, timeout=15,
    )
    if r.status_code != 200:
        print(f"Failed to fetch posts: {r.status_code} {r.text[:200]}")
        return 0

    posts = r.json()
    need_img = [p for p in posts if p.get("featured_media", 0) == 0]
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Offset {offset}: "
          f"{len(posts)} posts fetched, {len(need_img)} need images")
    if not need_img:
        return 0

    success = 0
    for post in need_img:
        pid = post["id"]
        title_html = post.get("title", {}).get("rendered", "")
        title_plain = re.sub(r"<[^>]+>", "", title_html).strip()
        cats = post.get("categories", [])
        cat_kw = get_cat_kw(cats[0]) if cats else "technology"

        print(f"  [{pid}] {title_plain[:45]} (kw={cat_kw})")

        img_url, source = find_image_for_post(title_plain, cat_kw, cats[0] if cats else None)
        if not img_url:
            print(f"    No image found")
            time.sleep(delay)
            continue

        print(f"    Found: {source} -> {img_url[:70]}")
        img_data, ct = download_image(img_url)
        if not img_data:
            print(f"    Download failed")
            time.sleep(delay)
            continue

        safe_title = re.sub(r"[^\w\u4e00-\u9fff]", "_", title_plain)[:25]
        ext = "jpg"
        if "png" in ct:
            ext = "png"
        elif "gif" in ct:
            ext = "gif"
        filename = f"{safe_title}_{pid}.{ext}"

        media_id, media_url = upload_to_wp(img_data, ct, filename, pid)
        if media_id:
            print(f"    SUCCESS media_id={media_id} {media_url[:70]}")
            success += 1
        else:
            print(f"    Upload failed")

        time.sleep(delay)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Done: {success}/{len(need_img)} added")
    return success

def get_cat_kw(cat_id):
    mapping = {
        53: "online business money",  # 网赚项目
        80: "artificial intelligence",  # AI知识
        81: "book education",           # 书籍资料
        82: "e-commerce shopping",      # 跨境电商
        83: "social media marketing",  # 自媒体运营
        84: "online course education learning",  # 教育资源/课程
        85: "software app tool",        # 工具合集
        86: "movie video entertainment", # 影视娱乐
        87: "health wellness",          # 健康养生
        88: "movie streaming video",    # 影视在线
        89: "course education",         # 课程资料
        90: "traditional culture art",  # 传统文化
        91: "resource download",        # 资源
        92: "AI chatbot technology",    # AI
        93: "marketing channel",        # 渠道资源
    }
    return mapping.get(cat_id, "business technology")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--delay", type=int, default=3)
    args = p.parse_args()
    process_posts(args.offset, args.limit, args.delay)
