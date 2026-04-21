import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== Check WordPress API ===\n")

# 测试API Token
print("1. 测试当前API Token...")
stdin, stdout, stderr = ssh.exec_command("""curl -s -X GET "https://skillxm.cn/wp-json/wp/v2/users/me" -H "Authorization: Bearer s6eW 2kHy 8yqu XNuY JjoK HHOR" 2>/dev/null | head -100""", timeout=30)
result = stdout.read().decode('utf-8', errors='ignore')
print(result[:500])

# 检查WordPress用户
print("\n2. 检查WordPress用户...")
stdin, stdout, stderr = ssh.exec_command("""curl -s "https://skillxm.cn/wp-json/wp/v2/users" -H "Authorization: Bearer s6eW 2kHy 8yqu XNuY JjoK HHOR" 2>/dev/null | head -100""", timeout=30)
result = stdout.read().decode('utf-8', errors='ignore')
print(result[:500])

ssh.close()
