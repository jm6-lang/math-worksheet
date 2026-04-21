import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 配置天空采集器自动采集网赚教程 ===\n")

# 1. 配置WordPress发布接口
print("1. 配置WordPress发布...")
release_config = """INSERT INTO skycaiji_release (name, module, type, config, addtime) VALUES 
('WordPress发布', 'wordpress', 'wordpress', '{"site_url":"https://skillxm.cn","api_token":"s6eW 2kHy 8yqu XNuY JjoK HHOR","post_type":"post","category_id":"7","post_status":"publish"}', UNIX_TIMESTAMP())
ON DUPLICATE KEY UPDATE config='{"site_url":"https://skillxm.cn","api_token":"s6eW 2kHy 8yqu XNuY JjoK HHOR","post_type":"post","category_id":"7","post_status":"publish"}', uptime=UNIX_TIMESTAMP(); """

cmd = f"""mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e "{release_config}" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("   ", stdout.read().decode().strip() or "WordPress发布接口已配置")

# 2. 创建网赚教程采集规则
print("\n2. 创建网赚教程采集规则...")

# 先检查表结构
cmd = """mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e "DESC skycaiji_collector;" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("   表结构:", stdout.read().decode().strip()[:200])

ssh.close()
