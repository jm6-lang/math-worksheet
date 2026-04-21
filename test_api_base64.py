import paramiko
import base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Test script
test_script = '''#!/usr/bin/env python3
import requests
import base64

WP_URL = "https://skillxm.cn"
WP_USER = "admin"
WP_APP_PASS = "s6eW2kHy8yquXNuYJjoKHHOR"

auth_str = WP_USER + ":" + WP_APP_PASS
auth_b64 = base64.b64encode(auth_str.encode()).decode()

headers = {"Authorization": "Basic " + auth_b64}

print("Testing API...")
r = requests.get(WP_URL + "/wp-json/wp/v2/posts?per_page=1", headers=headers, timeout=10)
print("GET status:", r.status_code)

print("Testing upload...")
test_data = b"fake_image_data"
files = {"file": ("test.jpg", test_data, "image/jpeg")}
r = requests.post(WP_URL + "/wp-json/wp/v2/media", headers=headers, files=files, timeout=10)
print("Upload status:", r.status_code)
print("Response:", r.text[:100])
'''

# Encode and write via base64
encoded = base64.b64encode(test_script.encode()).decode()
stdin, stdout, stderr = ssh.exec_command(
    f"echo '{encoded}' | base64 -d > /www/wwwroot/resource_site/test_api.py",
    timeout=10
)
print("Script written via base64")

# Run it
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && python3 test_api.py 2>&1",
    timeout=30
)
print("Output:")
print(stdout.read().decode())
print("Errors:", stderr.read().decode()[:200])

ssh.close()