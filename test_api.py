import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Test API with better error handling
test_script = '''#!/usr/bin/env python3
import requests
import base64

WP_URL = "https://skillxm.cn"
WP_USER = "admin"
WP_APP_PASS = "s6eW 2kHy 8yqu XNuY JjoK HHOR"

# Create proper auth header
auth_str = WP_USER + ":" + WP_APP_PASS.replace(" ", "")
auth_bytes = auth_str.encode('utf-8')
auth_b64 = base64.b64encode(auth_bytes).decode('utf-8')

headers = {
    "Authorization": "Basic " + auth_b64
}

print("Testing API...")
print("Auth header: Basic " + auth_b64[:20] + "...")

# Test getting posts
r = requests.get(WP_URL + "/wp-json/wp/v2/posts?per_page=1", headers=headers, timeout=10)
print("GET posts status:", r.status_code)

# Test media upload with a small test
print("\nTesting media upload...")
test_data = b"\xff\xd8\xff\xe0\x00\x10JFIF" + b"\x00" * 100  # Minimal JPEG header
files = {"file": ("test.jpg", test_data, "image/jpeg")}
r = requests.post(WP_URL + "/wp-json/wp/v2/media", headers=headers, files=files, timeout=10)
print("Upload status:", r.status_code)
print("Response:", r.text[:200])
'''

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/test_api.py', 'w') as f:
    f.write(test_script)
sftp.close()

print("Test script created")

stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && python3 test_api.py 2>&1",
    timeout=30
)

print(stdout.read().decode())
print("Errors:", stderr.read().decode()[:200])

ssh.close()