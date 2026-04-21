#!/usr/bin/env python3
"""
WordPress Auto Featured Image - 全部使用curl（服务器上最可靠）
"""
import os, re, time, random, sys
import subprocess
import json
import base64
from datetime import datetime

SITE_URL     = "https://skillxm.cn"
API_TOKEN    = "s6eW 2kHy 8yqu XNuY JjoK HHOR"
WP_USER      = "admin"

auth = base64.b64encode(f'{WP_USER}:{API_TOKEN}'.encode()).decode()

def download_image_curl(kw):
    """使用curl下载图片"""
    kw_safe = re.sub(r'[^\w]', '', kw.replace(' ', '')[:15])
    tmp_path = f"/tmp/feature_{os.getpid()}.png"
    
    # 优先用 placehold.co
    cmd = f'curl -s -o {tmp_path} "https://placehold.co/800x600.png?text={kw_safe}"'
    subprocess.run(cmd, shell=True, capture_output=True, timeout=15)
    
    if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 1000:
        return tmp_path
    
    # 备用 httpbin
    cmd2 = f'curl -s -o {tmp_path} https://httpbin.org/image/jpeg'
    subprocess.run(cmd2, shell=True, capture_output=True, timeout=15)
    
    if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 1000:
        return tmp_path
    
    return None

def upload_curl(file_path, filename):
    """使用curl上传图片到WordPress"""
    # 通过stdin传递文件内容，避免命令行参数过长
    cmd = f'''curl -s -X POST \\
      -H "Authorization: Basic {auth}" \\
      -H "Content-Disposition: attachment; filename={filename}" \\
      -H "Content-Type: image/png" \\
      --data-binary @{file_path} \\
      {SITE_URL}/wp-json/wp/v2/media'''
    
    result = subprocess.run(cmd, shell=True, capture_output=True, timeout=25)
    try:
        data = json.loads(result.stdout.decode('utf-8', errors='replace'))
        if 'id' in data:
            return data['id'], data.get('source_url', '')
    except:
        pass
    return None, None

def set_featured_curl(post_id, media_id):
    """使用curl设置特色图"""
    cmd = f'''curl -s -X POST \\
      -H "Authorization: Basic {auth}" \\
      -H "Content-Type: application/json" \\
      -d '{{"featured_media": {media_id}}}' \\
      {SITE_URL}/wp-json/wp/v2/posts/{post_id}'''
    
    result = subprocess.run(cmd, shell=True, capture_output=True, timeout=15)
    return result.returncode == 0

def get_posts_needing_image(offset, limit):
    """获取需要图片的文章"""
    cmd = f'''curl -s -H "Authorization: Basic {auth}" \\
      "{SITE_URL}/wp-json/wp/v2/posts?per_page={limit}&offset={offset}&status=publish&_fields=id,title.rendered,categories,featured_media"'''
    
    result = subprocess.run(cmd, shell=True, capture_output=True, timeout=15)
    try:
        posts = json.loads(result.stdout.decode('utf-8', errors='replace'))
        return [p for p in posts if p.get('featured_media', 0) == 0]
    except:
        return []

def get_cat_kw(cat_id):
    mapping = {
        53: "business", 80: "ai", 81: "book", 82: "shop", 83: "social",
        84: "course", 85: "tool", 86: "movie", 87: "health", 88: "video",
        89: "learning", 90: "culture", 91: "resource", 92: "tech", 93: "marketing",
    }
    return mapping.get(cat_id, "business")

def process_batch(offset=0, limit=30, delay=2):
    need_img = get_posts_needing_image(offset, limit)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Need images: {len(need_img)}")
    
    if not need_img:
        print("All done!")
        return 0

    success = 0
    for post in need_img:
        pid = post['id']
        title_html = post.get('title', {}).get('rendered', '')
        title_plain = re.sub(r'<[^>]+>', '', title_html).strip()[:40]
        cats = post.get('categories', [])
        cat_kw = get_cat_kw(cats[0]) if cats else 'business'

        print(f"  [{pid}] {title_plain}", end=" ", flush=True)

        # 下载
        file_path = download_image_curl(cat_kw)
        if not file_path:
            print("-> download failed")
            time.sleep(delay)
            continue

        # 上传
        safe_title = re.sub(r'[^\w\u4e00-\u9fff]', '_', title_plain)[:20]
        filename = f"{safe_title}_{pid}.png"

        media_id, media_url = upload_curl(file_path, filename)
        if not media_id:
            print("-> upload failed")
            time.sleep(delay)
            continue

        # 设为特色图
        if set_featured_curl(pid, media_id):
            print(f"-> OK (media={media_id})")
            success += 1
        else:
            print("-> set featured failed")

        # 清理
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