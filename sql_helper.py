import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 配置天空采集器 ===\n")

# 创建SQL文件
sql_content = """
-- 配置WordPress发布接口
INSERT INTO skycaiji_release (name, module, type, config, addtime, uptime) VALUES 
('WordPress发布', 'wordpress', 'wordpress', '{\"site_url\":\"https://skillxm.cn\",\"api_token\":\"s6eW 2kHy 8yqu XNuY JjoK HHOR\",\"post_type\":\"post\",\"category_id\":\"7\",\"post_status\":\"publish\"}', UNIX_TIMESTAMP(), UNIX_TIMESTAMP())
ON DUPLICATE KEY UPDATE config='{\"site_url\":\"https://skillxm.cn\",\"api_token\":\"s6eW 2kHy 8yqu XNuY JjoK HHOR\",\"post_type\":\"post\",\"category_id\":\"7\",\"post_status\":\"publish\"}', uptime=UNIX_TIMESTAMP();

-- 查看现有发布配置
SELECT * FROM skycaiji_release;
"""

sftp = ssh.open_sftp()
with sftp.open('/tmp/skycaiji_setup.sql', 'w') as f:
    f.write(sql_content)
sftp.close()
print("1. SQL文件已创建")

# 执行SQL
print("\n2. 执行SQL...")
cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji < /tmp/skycaiji_setup.sql 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
result = stdout.read().decode().strip()
print("   ", result[:500] if result else "执行成功")

# 检查发布配置
print("\n3. 检查发布配置...")
cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e 'SELECT id, name, type FROM skycaiji_release;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("   ", stdout.read().decode().strip())

ssh.close()
