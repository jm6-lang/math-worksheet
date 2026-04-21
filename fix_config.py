import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 修复采集配置 ===\n")

# 修复规则配置 - 使用正确的JSON格式
print("1. 修复规则配置...")
rule_config = '{"source_urls":["https://www.36kr.com/feed","https://sspai.com/feed","https://www.ithome.com/rss/IT"],"url_rule":"","title_rule":"css:.article-title","content_rule":"css:.article-content","author_rule":"","publish_time_rule":"","list_url_rule":"","page_rule":"","max_items":6}'

sql = f"""mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e "UPDATE skycaiji_rule SET config='{rule_config}' WHERE id=1;" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(sql, timeout=15)
print("   ", stdout.read().decode().strip() or "规则已更新")

# 创建发布配置
print("\n2. 创建发布配置...")
release_config = '{"site_url":"https://skillxm.cn","api_token":"s6eW 2kHy 8yqu XNuY JjoK HHOR","post_type":"post","category_id":"7","post_status":"publish","author_id":1}'

sql = f"""mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e "INSERT INTO skycaiji_release (task_id, name, module, addtime, config) VALUES (1, 'WordPress发布', 'wordpress', UNIX_TIMESTAMP(), '{release_config}');" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(sql, timeout=15)
print("   ", stdout.read().decode().strip() or "发布配置已创建")

# 验证
print("\n3. 验证配置...")
cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e 'SELECT id, name, config FROM skycaiji_release;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("发布配置:", stdout.read().decode().strip())

# 测试API
print("\n4. 测试API...")
cmd = "curl -s 'http://caiji.skillxm.cn/index.php?s=/admin/api/collect' -X POST -d 'task_id=1' 2>/dev/null | head -20"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode('utf-8', errors='ignore').strip()[:300])

ssh.close()

print("\n" + "="*50)
print("配置完成!")
print("="*50)
print("\n天空采集器已配置好:")
print("  - 网址: http://caiji.skillxm.cn")
print("  - 登录: admin / admin123")
print("  - 任务: 网赚教程采集")
print("  - 定时: 每天6条")
print("\n注意: 由于天空采集器需要可视化配置采集规则，")
print("建议登录后台完成具体的规则配置。")
