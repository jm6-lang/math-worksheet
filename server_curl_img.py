#!/usr/bin/env python3
"""
WordPress Auto Featured Image - 使用curl下载图片（服务器上更可靠）
"""
import os, re, time, random, sys
import subprocess
from datetime import datetime

SITE_URL     = "https://skillxm.cn"
API_TOKEN    = "s6eW 2kHy 8yqu XNuY JjoK HHOR"
WP_USER      = "admin"

# 服务器可访问的图源（curl测试通过）
IMG_CONFIGS = [
    # httpbin - 固定测试图
    {"url": "https://httpbin.org/image/jpeg", "ext": "jpg"},
    # placehold - 生成文字占位图
    {"url": "https://placehold.co/800x600.png?text={kw}", "ext": "png"},
    # picsum - 需要-L跟随重定向
    {"url": "https://picsum.photos/seed/{kw}{r}/800/600.jpg", "ext": "jpg", "curl_L": True},
]

def get_image_url(kw):
    kw_safe = re.sub(r'[^\w]', '', kw.replace(' ', '')[:15])
    r = random.randint(1,9999)
    
    # Try httpbin first
    cfg = IMG_CONFIGS[0]
    url = cfg["url"]
    return url, cfg["ext"], cfg.get("curl_L", False), kw_safe, r

def download_image_curl(kw, r):
    kw_safe = re.sub(r'[^\w]', '', kw.replace(' ', '')[:15])
    tmp_path = f"/tmp/feature_img_{os.getpid()}.jpg"
    
    # Try placehold (generates proper images)
    cmd = f'curl -s -o {tmp_path} "https://placehold.co/800x600.png?text={kw_safe}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, timeout=15)
    
    if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 1000:
        return tmp_path, "image/png"
    
    # Fallback to httpbin
    cmd2 = f'curl -s -o {tmp_path} https://httpbin.org/image/jpeg'
    result2 = subprocess.run(cmd2, shell=True, capture_output=True, timeout=15)
    
    if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 1000:
        return tmp_path, "image/jpeg"
    
    return None, None

def upload_to_wp(file_path, content_type, filename, post_id):
    try:
        import base64
        # 读取文件
        with open(file_path, 'rb') as f:
            data = f.read()
        
        auth = base64.b64encode(f'{WP_USER}:{API_TOKEN}'.encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": content_type,
        }
        import requests
        r = requests.post(f"{SITE_URL}/wp-json/wp/v2/media",
                         headers=headers, data=data, timeout=25)
        if r.status_code not in [200, 201]:
            return None
        media = r.json()
        media_id = media["id"]
        
        # 设为特色图
        r2 = requests.post(f"{SITE_URL}/wp-json/wp/v2/posts/{post_id}",
                          headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"},
                          json={"featured_media": media_id}, timeout=10)
        return media_id if r2.status_code < 400 else None
    except Exception as e:
        return None

def get_cat_kw(cat_id):
    mapping = {
        53: "business", 80: "ai", 81: "book", 82: "shop", 83: "social",
        84: "course", 85: "tool", 86: "movie", 87: "health", 88: "video",
        89: "learning", 90: "culture", 91: "resource", 92: "tech", 93: "marketing",
    }
    return mapping.get(cat_id, "business")

def process_batch(offset=0, limit=30, delay=2):
    import requests, base64
    auth = base64.b64encode(f'{WP_USER}:{API_TOKEN}'.encode()).decode()
    headers = {"Authorization": f"Basic {auth}", "Content-Type": "application/json; charset=utf-8"}
    
    # 获取需要图片的文章
    r = requests.get(
        f"{SITE_URL}/wp-json/wp/v2/posts",
        params={"per_page": limit, "offset": offset, "status": "publish",
                "_fields": "id,title.rendered,categories,featured_media"},
        headers=headers, timeout=15,
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

        # 下载图片
        file_path, ct = download_image_curl(cat_kw, random.randint(1,9999))
        if not file_path:
            print("-> download failed")
            time.sleep(delay)
            continue

        # 上传
        safe_title = re.sub(r"[^\w\u4e00-\u9fff]", "_", title_plain)[:20]
        ext = "png" if ct == "image/png" else "jpg"
        filename = f"{safe_title}_{pid}.{ext}"

        media_id = upload_to_wp(file_path, ct, filename, pid)
        if media_id:
            print(f"-> OK (media={media_id})")
            success += 1
        else:
            print("-> upload failed")

        # 清理临时文件
        try:
            os.remove(file_path)
        except:
            pass

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