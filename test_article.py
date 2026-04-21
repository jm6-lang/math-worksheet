import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 测试新文章的最终URL和状态
cmd = "curl -sIL 'https://www.skillxm.cn/?p=1825' 2>&1 | head -20"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print("=== 测试文章1825重定向 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 测试文章详情页
cmd2 = "curl -s 'https://www.skillxm.cn/?p=1825' 2>&1 | head -50"
stdin, stdout, stderr = ssh.exec_command(cmd2, timeout=30)
print("\n=== 文章1825内容预览 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 检查WordPress固定链接设置
cmd3 = "mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e \"SELECT option_value FROM wp_options WHERE option_name='permalink_structure'\""
stdin, stdout, stderr = ssh.exec_command(cmd3, timeout=30)
print("\n=== 固定链接设置 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
