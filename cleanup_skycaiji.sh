#!/bin/bash
# 清理蓝天采集器脚本
# 运行方式: bash cleanup_skycaiji.sh

echo "=== 开始清理蓝天采集器 ==="

# 1. 停止相关定时任务
echo "[1/5] 清理定时任务..."
# 移除蓝天采集器的crontab任务
crontab -l 2>/dev/null | grep -v "skycaiji" | grep -v "caiji" | crontab -

# 2. 删除蓝天采集器目录
echo "[2/5] 删除程序目录..."
rm -rf /www/wwwroot/skycaiji

# 3. 删除数据库(可选)
echo "[3/5] 清理数据库(可选)..."
read -p "是否删除蓝天采集器数据库? (y/n): " confirm
if [ "$confirm" = "y" ]; then
    mysql -u root -p -e "DROP DATABASE IF EXISTS skycaiji;"
    mysql -u root -p -e "DROP USER IF EXISTS 'skycaiji'@'localhost';"
    echo "数据库已删除"
else
    echo "跳过数据库删除"
fi

# 4. 清理nginx配置
echo "[4/5] 清理nginx配置..."
rm -f /etc/nginx/sites-enabled/caiji.skillxm.cn.conf 2>/dev/null
rm -f /etc/nginx/sites-available/caiji.skillxm.cn.conf 2>/dev/null

# 5. 重载nginx
echo "[5/5] 重载nginx..."
nginx -s reload

echo "=== 蓝天采集器清理完成 ==="
