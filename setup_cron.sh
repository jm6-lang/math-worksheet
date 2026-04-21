#!/bin/bash
# 自动采集定时任务设置脚本
# 运行: bash setup_cron.sh

echo "=== 配置自动采集定时任务 ==="

# 采集器路径
COLLECTOR_DIR="/www/wwwroot/resource_site/auto_collect"
COLLECTOR_SCRIPT="$COLLECTOR_DIR/collector_v2.py"

# 检查脚本是否存在
if [ ! -f "$COLLECTOR_SCRIPT" ]; then
    echo "错误: 采集脚本不存在: $COLLECTOR_SCRIPT"
    exit 1
fi

# 设置执行权限
chmod +x "$COLLECTOR_SCRIPT"

# 添加定时任务 - 每天9点和18点各运行一次
CRON_JOB="0 9,18 * * * cd $COLLECTOR_DIR && python3 collector_v2.py >> $COLLECTOR_DIR/collector.log 2>&1"

# 检查是否已有任务
if crontab -l 2>/dev/null | grep -q "collector"; then
    echo "已有采集任务，更新..."
    crontab -l 2>/dev/null | grep -v "collector" | crontab -
fi

# 添加新任务
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "定时任务已设置:"
echo "  每天 9:00 和 18:00 自动采集"
echo ""
echo "当前定时任务:"
crontab -l | grep -i collect

echo ""
echo "=== 配置完成 ==="