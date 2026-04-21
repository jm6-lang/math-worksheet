#!/usr/bin/env python3
"""
WordPress Auto Featured Image - 使用服务器可访问的图源
"""
import os, re, time, json, random, sys
import requests
from datetime import datetime

SITE_URL     = "https://skillxm.cn"
API_TOKEN    = "s6eW 2kHy 8yqu XNuY JjoK HHOR"
WP_USER      = "admin"

HEADERS = {
    "Authorization": f"Basic {__import__('base64').b64encode(f'{WP_USER}:{API_TOKEN}'.encode()).decode()}",
    "Content-Type": "application/json; charset=utf-8",
}

# 服务器可访问的图源
IMG_SOURCES = [
    "https://picsum.photos/seed/{kw}{r}/800/600.jpg",
    "https://placehold.co/800x600.png?text={kw}",
    "https://httpbin.org/image/jpeg",
]

def get_image_url(kw, w=800, h=600):
    kw_safe = re.sub(r'[^\w]', '', kw.replace(' ', '')[:15])
    r = random.randint(1,9999)
    
    # Try picsum (returns actual images, not 302 anymore)
    url = f"https://picsum.photos/seed/{kw_safe}{r}/{w}/{h}.jpg"
    try:
        r1 = requests.head(url, timeout=6, allow_redirects=True)
        # Follow redirects manually to check final status
        if r1.status_code in [200, 302]:
            # 302 is redirect, need to get final URL
            final_url = r1.headers.get('Location', url)
            if final_url:
                return final_url
            return url
    except:
        pass
    
    # Fallback to placehold.co (always returns 200)
    url2 = f"https://placehold.co/{w}x{h}.png?text={kw_safe}"
    try:
        r2 = requests.head(url2, timeout=6)
        if r2.status_code == 200:
            return url2
    except:
        pass
    
    # Last resort: httpbin (fixed image)
    return "https://httpbin.org/image/jpeg"

def download_image(url, timeout=12):
    for attempt in range(2):
        try:
            r = requests.get(url, timeout=timeout, allow_redirects=True)
            if r.status_code == 200 and len(r.content) > 1000:
                ct = r.headers.get("Content-Type", "image/jpeg")
                return r.content, ct
        except:
            pass
    return None, None

def upload_to_wp(image_data, content_type, filename, post_id):
    try:
        headers = {
            **HEADERS,
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": content_type,
        }
        r = requests.post(f"{SITE_URL}/wp-json/wp/v2/media",
                          headers=headers, data=image_data, timeout=25)
        if r.status_code not in [200, 201]:
            return None, None
        media = r.json()
        media_id = media["id"]
        
        # 设为特色图
        r2 = requests.post(f"{SITE_URL}/wp-json/wp/v2/posts/{post_id}",
                           headers=HEADERS, json={"featured_media": media_id}, timeout=10)
        return media_id if r2.status_code < 400 else None, media["source_url"]
    except:
        return None, None

def get_cat_kw(cat_id):
    mapping = {
        53: "business", 80: "ai", 81: "book", 82: "shop", 83: "social",
        84: "course", 85: "tool", 86: "movie", 87: "health", 88: "video",
        89: "learning", 90: "culture", 91: "resource", 92: "tech", 93: "marketing",
    }
    return mapping.get(cat_id, "business")

def process_batch(offset=0, limit=30, delay=2):
    # 获取需要图片的文章
    r = requests.get(
        f"{SITE_URL}/wp-json/wp/v2/posts",
        params={"per_page": limit, "offset": offset, "status": "publish",
                "_fields": "id,title.rendered,categories,featured_media"},
        headers=HEADERS, timeout=15,
    )
    if r.status_code != 200:
        print(f"Failed: {r.status_code}")
        return 0

    posts = r.json()
    need_img = [p for p in posts if p.get("featured_media", 0) == 0]
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Posts: {len(posts)}, need img: {len(need_img)}")
    
    if not need_img:
        print("All done!")
        return 0

    success = 0
    for post in need_img:
        pid = post["id"]
        title_html = post.get("title", {}).get("rendered", "")
        title_plain = re.sub(r"<[^>]+>", "", title_html).strip()[:40]
        cats = post.get("categories", [])
        cat_kw = get_cat_kw(cats[0]) if cats else "business"

        print(f"  [{pid}] {title_plain}", end=" ", flush=True)

        # 找图
        img_url = get_image_url(cat_kw)
        if not img_url:
            print("-> no image URL")
            time.sleep(delay)
            continue

        # 下载
        img_data, ct = download_image(img_url)
        if not img_data:
            print("-> download failed")
            time.sleep(delay)
            continue

        # 上传
        safe_title = re.sub(r"[^\w\u4e00-\u9fff]", "_", title_plain)[:20]
        ext = "jpg"
        if "png" in ct:
            ext = "png"
        filename = f"{safe_title}_{pid}.{ext}"

        media_id, media_url = upload_to_wp(img_data, ct, filename, pid)
        if media_id:
            print(f"-> OK (media={media_id})")
            success += 1
        else:
            print("-> upload failed")

        time.sleep(delay)

    print(f"Done: {success}/{len(need_img)} images added")
    return success

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--delay", type=int, default=2)
    args = p.parse_args()
    process_batch(args.offset, args.limit, args.delay)