import paramiko
import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 创建新应用密码 ===\n")

# 创建新应用密码
print("1. 创建新应用密码...")
cmd = """cd /www/wwwroot/resource_site && wp user application-password create admin "API-Post" --porcelain --allow-root 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
result = stdout.read().decode('utf-8', errors='ignore').strip()
print(f"结果: {result}")

# 检查是否是纯文本密码
if result and len(result) > 20 and '$' not in result:
    print(f"\n新Token: {result}")
    new_token = result
    
    # 测试API
    print("\n2. 测试API...")
    headers = {
        "Authorization": f"Bearer {new_token}",
        "Content-Type": "application/json"
    }
    
    test_post = {
        "title": "测试文章-自动采集",
        "content": "<p>这是一篇测试文章，验证API是否正常工作。</p>",
        "status": "publish",
        "categories": [7]
    }
    
    r = requests.post("https://skillxm.cn/wp-json/wp/v2/posts", headers=headers, json=test_post, timeout=30, verify=False)
    print(f"发布状态: {r.status_code}")
    if r.status_code in [200, 201]:
        print(f"发布成功!")
        data = r.json()
        print(f"文章链接: {data.get('link', '')}")
    else:
        print(f"失败: {r.text[:200]}")
else:
    print("需要手动查看或创建应用密码")

ssh.close()
