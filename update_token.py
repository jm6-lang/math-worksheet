import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

cfg_path = '/www/wwwroot/resource_site/auto_collect/config.json'

# Read current config
stdin, stdout, stderr = ssh.exec_command(f"cat {cfg_path}", timeout=10)
config_content = stdout.read().decode('utf-8', errors='replace')
print("当前config:", config_content)

# Update with new password - need to set password in a way that preserves JSON
# The password has spaces, need to handle properly
new_token = "s6eW 2kHy 8yqu XNuY JjoK HHOR"

# Use sed to replace the token
cmd = f"sed -i 's|\"wp_api_token\": \".*\"|\"wp_api_token\": \"{new_token}\"|' {cfg_path}"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print("sed结果:", out, err)

# Verify
stdin, stdout, stderr = ssh.exec_command(f"cat {cfg_path}", timeout=10)
new_content = stdout.read().decode('utf-8', errors='replace')
print("更新后:", new_content)

ssh.close()
