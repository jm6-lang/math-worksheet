import paramiko, sys, time
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

BATCH_SIZE = 50
TOTAL = 685  # 预估总数（排除Hello world和去重后）
batches = (TOTAL + BATCH_SIZE - 1) // BATCH_SIZE  # 14批

print(f"总文章数: ~{TOTAL}, 每批: {BATCH_SIZE}, 共{batches}批")
print("开始全量重写...\n")

total_ok = 0
total_fail = 0

for b in range(batches):
    offset = b * BATCH_SIZE
    print(f"=== 第{b+1}/{batches}批 (offset={offset}) ===")
    
    stdin, stdout, stderr = ssh.exec_command(
        f"cd /www/wwwroot/resource_site && python3 auto_collect/rewrite_v2.py {offset} {BATCH_SIZE} 2>&1",
        timeout=120
    )
    output = stdout.read().decode('utf-8', errors='ignore')
    print(output)
    
    # 统计结果
    for line in output.split('\n'):
        if '[完成]' in line:
            parts = line.split('成功=')
            if len(parts) > 1:
                ok_fail = parts[1].split(' 失败=')
                total_ok += int(ok_fail[0].strip())
                total_fail += int(ok_fail[1].strip())
    
    # 如果这批返回0篇或出错了，可能已经处理完了
    if '没有更多文章' in output:
        print("所有文章已处理完毕！")
        break
    
    # 批次间暂停，让数据库喘口气
    if b < batches - 1:
        time.sleep(2)

print(f"\n{'='*40}")
print(f"全部完成！成功: {total_ok}, 失败: {total_fail}")

# 清除缓存让新内容生效
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp cache flush --allow-root 2>&1 && "
    "rm -rf /www/wwwroot/resource_site/wp-content/cache/wp-super-cache/* 2>/dev/null && "
    "echo '缓存已清除'",
    timeout=15
)
print("缓存: %s" % stdout.read().decode().strip())

ssh.close()
