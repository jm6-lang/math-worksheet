import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 为首页设置SEO Meta
print("设置首页SEO Meta...")

# 首页ID通常是2（留言页）或最新页面）
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site && wp post list --post_type=page --posts_per_page=1 --orderby=ID --order=asc --fields=ID --allow-root", timeout=10)
home_id = stdout.read().decode().strip().split('\n')[-1].strip()
print(f"首页ID: {home_id}")

# 设置Meta Title
stdin, stdout, stderr = ssh.exec_command(
    f"cd /www/wwwroot/resource_site && wp post meta update {home_id} rank_math_title '小二郎资源网 - 免费资源分享平台' --allow-root",
    timeout=10
)
print("Meta Title设置:", stdout.read().decode().strip() or "成功")

# 设置Meta Description
stdin, stdout, stderr = ssh.exec_command(
    f"cd /www/wwwroot/resource_site && wp post meta update {home_id} rank_math_description '小二郎资源网提供各类免费资源下载，包括教育资源、工具软件、影视资源、网赚项目等，每日更新，欢迎收藏！' --allow-root",
    timeout=10
)
print("Meta Description设置:", stdout.read().decode().strip() or "成功")

# 刷新缓存
stdin, stdout, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site && wp cache flush --allow-root", timeout=10)

print("\n首页SEO设置完成！")
ssh.close()
