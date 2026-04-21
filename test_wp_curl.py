import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Test WordPress media upload directly via curl
# First ensure we have a test image
ssh.exec_command("curl -s -o /tmp/test_img.jpg https://httpbin.org/image/jpeg", timeout=15)

# Get base64 auth
import base64
token = base64.b64encode('admin:s6eW 2kHy 8yqu XNuY JjoK HHOR'.encode()).decode()

# Try upload with curl
cmd = f'''curl -s -w "\\nHTTP: %{{http_code}}\\n" -X POST \\
  -H "Authorization: Basic {token}" \\
  -H "Content-Disposition: attachment; filename=test.jpg" \\
  -H "Content-Type: image/jpeg" \\
  --data-binary @/tmp/test_img.jpg \\
  https://skillxm.cn/wp-json/wp/v2/media'''

stdin, stdout, stderr = ssh.exec_command(cmd, timeout=20)
out = stdout.read().decode('utf-8', errors='replace')
print("Curl upload result:")
print(out)

ssh.close()