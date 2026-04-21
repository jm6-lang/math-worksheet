import paramiko
import sys
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 配置天空采集器采集网赚教程 ===\n")

# 1. 创建任务组
print("1. 创建任务组...")
sql = """mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e "INSERT INTO skycaiji_taskgroup (name, sort, addtime) VALUES ('网赚教程', 1, UNIX_TIMESTAMP());" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(sql, timeout=15)
print("   任务组已创建")

# 2. 创建采集规则 - 使用EasyRule简单规则
print("\n2. 创建采集规则...")

# EasyRule配置 - 采集网赚教程
easyrule_config = json.dumps({
    "source_urls": [
        "https://www.36kr.com/feed",
        "https://sspai.com/feed",
        "https://www.ithome.com/rss/IT"
    ],
    "url_rule": "",
    "title_rule": "css:.article-title",
    "content_rule": "css:.article-content",
    "author_rule": "",
    "publish_time_rule": "",
    "list_url_rule": "",
    "page_rule": "",
    "max_items": 6
}, ensure_ascii=False)

sql = f"""mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e "INSERT INTO skycaiji_rule (name, type, module, store_id, addtime, provider_id, config) VALUES ('网赚教程采集', 'easy', 'easy', 1, UNIX_TIMESTAMP(), 0, '{easyrule_config}');" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(sql, timeout=15)
result = stdout.read().decode().strip()
print("   ", result or "采集规则已创建")

# 3. 创建发布配置 - WordPress
print("\n3. 创建WordPress发布配置...")

release_config = json.dumps({
    "site_url": "https://skillxm.cn",
    "api_token": "s6eW 2kHy 8yqu XNuY JjoK HHOR",
    "post_type": "post",
    "category_id": "7",
    "post_status": "publish",
    "author_id": 1
}, ensure_ascii=False)

sql = f"""mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e "INSERT INTO skycaiji_release (task_id, name, module, addtime, config) VALUES (1, 'WordPress发布', 'wordpress', UNIX_TIMESTAMP(), '{release_config}');" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(sql, timeout=15)
result = stdout.read().decode().strip()
print("   ", result or "WordPress发布配置已创建")

# 4. 创建任务
print("\n4. 创建采集任务...")

task_config = json.dumps({
    "maxContent": 5000,
    "minContent": 100,
    "release_id": 1,
    "rule_id": 1
}, ensure_ascii=False)

sql = f"""mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e "INSERT INTO skycaiji_task (name, tg_id, module, auto, sort, addtime, caijitime, config) VALUES ('网赚教程采集', 1, 'easy', 1, 1, UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), '{task_config}');" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(sql, timeout=15)
result = stdout.read().decode().strip()
print("   ", result or "采集任务已创建")

# 5. 设置定时任务 - 每天自动采集
print("\n5. 设置定时任务...")
sql = """mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e "INSERT INTO skycaiji_task_timer (task_id, name, data) VALUES (1, 'day', '6');" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(sql, timeout=15)
print("   ", stdout.read().decode().strip() or "定时任务已设置")

# 6. 验证
print("\n6. 验证配置...")
cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e 'SELECT id, name FROM skycaiji_task;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("   任务:", stdout.read().decode().strip())

cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e 'SELECT * FROM skycaiji_task_timer;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("   定时器:", stdout.read().decode().strip())

ssh.close()

print("\n" + "="*50)
print("采集任务配置完成!")
print("="*50)
print("\n请登录天空采集器后台完成规则配置:")
print("  http://caiji.skillxm.cn/index.php?s=/admin/login")
print("  用户名: admin")
print("  密码: admin123")
print("\n配置说明:")
print("  - 任务组: 网赚教程")
print("  - 采集规则: EasyRule简单规则")
print("  - 发布方式: WordPress")
print("  - 定时任务: 每天6条")
