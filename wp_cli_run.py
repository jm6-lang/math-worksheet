import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Create script that uses WP-CLI instead of REST API
script = '''#!/usr/bin/env python3
import subprocess
import requests
import re
import time
import random

def get_posts():
    # Get posts via WP-CLI
    result = subprocess.run(
        ["wp", "post", "list", "--post_type=post", "--fields=ID,post_title", "--format=json", "--allow-root"],
        capture_output=True, text=True, cwd="/www/wwwroot/resource_site"
    )
    import json
    try:
        posts = json.loads(result.stdout)
        return [{"id": p["ID"], "title": p["post_title"]} for p in posts]
    except:
        return []

def download_image(url, save_path):
    try:
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(r.content)
            return True
    except Exception as e:
        print("    Download error:", e)
    return False

def import_image(file_path, title):
    # Use WP-CLI to import
    result = subprocess.run(
        ["wp", "media", "import", file_path, "--title=" + title, "--porcelain", "--allow-root"],
        capture_output=True, text=True, cwd="/www/wwwroot/resource_site"
    )
    output = result.stdout.strip()
    if output.isdigit():
        return int(output)
    return None

def set_thumbnail(post_id, img_id):
    # Use WP-CLI to set featured image
    result = subprocess.run(
        ["wp", "post", "meta", "update", str(post_id), "_thumbnail_id", str(img_id), "--allow-root"],
        capture_output=True, text=True, cwd="/www/wwwroot/resource_site"
    )
    return "Success" in result.stdout or "Updated" in result.stdout

print("Getting posts...")
posts = get_posts()
print("Found:", len(posts), "posts")

success = 0
fail = 0

for i, p in enumerate(posts[:50]):
    print("[" + str(i+1) + "/50] " + p["title"][:45])
    
    # Get random image from picsum
    img_id = random.randint(1, 1000)
    img_url = "https://picsum.photos/seed/" + str(img_id) + "/800/600"
    
    # Download to temp file
    temp_file = "/tmp/article_" + str(p["id"]) + ".jpg"
    
    if download_image(img_url, temp_file):
        print("    Downloaded")
        
        # Import to WP
        media_id = import_image(temp_file, p["title"][:50])
        if media_id:
            print("    Imported, ID:", media_id)
            
            # Set as thumbnail
            if set_thumbnail(p["id"], media_id):
                print("    SUCCESS")
                success += 1
            else:
                print("    FAIL: set thumbnail")
                fail += 1
        else:
            print("    FAIL: import")
            fail += 1
        
        # Clean up
        subprocess.run(["rm", "-f", temp_file])
    else:
        print("    FAIL: download")
        fail += 1
    
    time.sleep(1)

print("\n=== RESULTS ===")
print("Success:", success)
print("Failed:", fail)
'''

import base64
encoded = base64.b64encode(script.encode()).decode()

stdin, stdout, stderr = ssh.exec_command(
    f"echo '{encoded}' | base64 -d > /www/wwwroot/resource_site/wp_cli_fetcher.py",
    timeout=10
)
print("Script created")

# Run it
print("\nRunning WP-CLI fetcher (50 posts)...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && python3 wp_cli_fetcher.py 2>&1",
    timeout=300
)

print("Output:")
output = stdout.read().decode()
print(output[:3000])
if len(output) > 3000:
    print("... (truncated)")

err = stderr.read().decode()
if err:
    print("Errors:", err[:500])

ssh.close()