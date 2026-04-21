#!/usr/bin/env python3
"""
WordPress Auto Featured Image - 按文章标题/分类搜索免费图并设为特色图
"""
import os
import re
import time
import json
import random
import requests
importwordpress
fromdatetimeimport datetime

# WordPress REST API
SITE_URL = "https://skillxm.cn"
API_TOKEN = "s6eW 2kHy 8yqu XNuY JjoK HHOR"
HEADERS = {
    "Authorization": f"Basic {__import__('base64').b64encode(f'admin:{API_TOKEN}'.encode()).decode()}",
    "Content-Type": "application/json",
}

# Image search configs
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Safari/537.36",
]

# Category keyword mapping
CAT_KEYWORDS = {
    53: ["网赚", "赚钱", "副业", "money", "business"],
    80: ["AI", "artificial intelligence", "机器学习"],
    81: ["book", "ebook", "pdf", "阅读", "书籍"],
    82: ["电商", "shop", "e-commerce", "跨境"],
    83: ["自媒体", "短视频", "social media", "运营"],
    84: ["course", "在线课程", "教育", "学习", "教程"],
    85: ["software", "工具", "app", "tool"],
    86: ["movie", "film", "video", "影视", "音乐"],
    87: ["健康", "health", "养生", "medical"],
    88: ["movie", "video", "film", "在线影视"],
    89: ["course", "课程", "education", "学习"],
    90: ["传统文化", "culture", "历史", "art"],
    91: ["资源", "resource", "分享"],
    92: ["AI", "chatgpt", "人工智能"],
    93: ["渠道", "推广", "channel"],
}

IMG_SOURCES = [
    # Pexels free images via search
    "https://api.pexels.com/v1/search?per_page=3&query={}",
    # Wikimedia Commons search
    "https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={}&srnamespace=6&srlimit=3&format=json",
]

def search_wikimedia(keyword):
    """从Wikimedia Commons搜索免费图片"""
    url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(keyword)}&srnamespace=6&srlimit=5&format=json"
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": random.choice(USER_AGENTS)})
        data = r.json()
        results = data.get("query", {}).get("search", [])
        for item in results:
            title = item["title"]
            # Get actual image URL
            img_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{requests.utils.quote(title.replace('File:', ''))}?width=800"
            # Verify it's an image
            try:
                head = requests.head(img_url, timeout=8, headers={"User-Agent": random.choice(USER_AGENTS)})
                ct = head.headers.get("Content-Type", "")
                if "image" in ct:
                    return img_url
            except:
                continue
    except Exception as e:
        pass
    return None

def search_bing_images(keyword):
    """通过Bing搜索免费图片"""
    try:
        url = f"https://www.bing.com/images/search?q={requests.utils.quote(keyword + ' free image site:wikimedia.org OR site:pexels.com OR site:pixabay.com')}"
        r = requests.get(url, timeout=10, headers={
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9",
        })
        # Extract image URLs from Bing results
        matches = re.findall(r'"murl":"([^"]+)"', r.text)
        for m in matches[:5]:
            if m and ("jpg" in m or "png" in m or "jpeg" in m) and not m.startswith("data:"):
                try:
                    head = requests.head(m, timeout=8, headers={"User-Agent": random.choice(USER_AGENTS)})
                    if head.status_code == 200 and "image" in head.headers.get("Content-Type", ""):
                        return m
                except:
                    continue
    except Exception as e:
        print(f"    Bing search error: {e}")
    return None

def get_post_image(post_id):
    """获取文章图片（优先特色图URL）"""
    r = requests.get(f"{SITE_URL}/wp-json/wp/v2/posts/{post_id}?_fields=featured_media_url,title, categories", 
                     headers=HEADERS, timeout=10)
    if r.status_code == 200:
        return r.json()
    return None

def upload_to_wordpress(image_url, post_id, filename):
    """下载图片并上传到WordPress"""
    try:
        # Download image
        img_data = requests.get(image_url, timeout=15, headers={"User-Agent": random.choice(USER_AGENTS)})
        if img_data.status_code != 200:
            return None
        
        # Upload to WordPress
        files = {
            "file": (filename, img_data.content, img_data.headers.get("Content-Type", "image/jpeg")),
        }
        data = {"action": "wp_handle_upload", "post_id": str(post_id)}
        r_upload = requests.post(
            f"{SITE_URL}/wp-json/wp/v2/media",
            headers={
                **HEADERS,
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": img_data.headers.get("Content-Type", "image/jpeg"),
            },
            data=img_data.content,
            timeout=20,
        )
        if r_upload.status_code in [200, 201]:
            media = r_upload.json()
            media_id = media["id"]
            media_url = media["source_url"]
            # Set as featured image
            r_featured = requests.post(
                f"{SITE_URL}/wp-json/wp/v2/posts/{post_id}",
                headers=HEADERS,
                json={"featured_media": media_id},
                timeout=10,
            )
            return media_id, media_url
    except Exception as e:
        print(f"    Upload error: {e}")
    return None

def get_posts_needing_image(limit=50, offset=0):
    """获取需要图片的文章"""
    # Try REST API first
    r = requests.get(
        f"{SITE_URL}/wp-json/wp/v2/posts",
        params={"per_page": limit, "offset": offset, "status": "publish", 
                "_fields": "id,title,categories,featured_media"},
        headers=HEADERS,
        timeout=15,
    )
    if r.status_code == 200:
        posts = r.json()
        need_image = [p for p in posts if p.get("featured_media") == 0]
        return need_image
    return []

def get_category_name(cat_id):
    return CAT_KEYWORDS.get(cat_id, ["image", "photo"])[0]

def process_batch(start=0, limit=50, delay=3):
    """处理一批文章"""
    posts = get_posts_needing_image(limit, start)
    if not posts:
        print("No posts need images!")
        return 0
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Found {len(posts)} posts needing images")
    success = 0
    
    for post in posts:
        post_id = post["id"]
        title = post.get("title", {}).get("rendered", "")
        title_plain = re.sub(r'<[^>]+>', '', title)  # strip HTML
        cats = post.get("categories", [])
        cat_kw = get_category_name(cats[0]) if cats else "technology"
        
        keywords = [title_plain[:15], cat_kw, "business", "online"]
        chosen_url = None
        
        for kw in keywords:
            if not kw:
                continue
            # Try Wikimedia first
            url = search_wikimedia(kw)
            if url:
                chosen_url = url
                break
            # Try Bing as fallback
            url = search_bing_images(kw)
            if url:
                chosen_url = url
                break
        
        if not chosen_url:
            print(f"  [{post_id}] No image found for: {title_plain[:40]}")
            time.sleep(delay)
            continue
        
        # Generate filename
        safe_title = re.sub(r'[^\w\u4e00-\u9fff]', '_', title_plain)[:30]
        ext = "jpg"
        if chosen_url.endswith(".png"):
            ext = "png"
        elif chosen_url.endswith(".gif"):
            ext = "gif"
        filename = f"{safe_title}_{post_id}.{ext}"
        
        print(f"  [{post_id}] '{title_plain[:40]}' -> {chosen_url[:80]}")
        result = upload_to_wordpress(chosen_url, post_id, filename)
        if result:
            print(f"    SUCCESS! Media ID: {result[0]}, URL: {result[1][:80]}")
            success += 1
        else:
            print(f"    FAILED")
        
        time.sleep(delay)
    
    print(f"\nBatch done: {success}/{len(posts)} images added")
    return success

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--delay", type=int, default=3)
    args = parser.parse_args()
    
    total = process_batch(args.start, args.limit, args.delay)
    print(f"\nTotal images added: {total}")
