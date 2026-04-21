#!/bin/bash
#===========================================
# 服务器采集器一键配置脚本
# 用于: 清理蓝天采集器 + 配置更好的采集系统
# 
# 使用方法:
# 1. SSH登录服务器: ssh root@43.103.5.46
# 2. 上传脚本: scp setup_collector.sh root@43.103.5.46:/root/
# 3. 执行: bash /root/setup_collector.sh
#===========================================

set -e

echo "============================================"
echo "  服务器采集器一键配置"
echo "============================================"

# 配置变量
SITE_DIR="/www/wwwroot/resource_site"
DB_NAME="wp_skillxm"
DB_USER="wp_user"
DB_PASS="gMshA29CshK5"

#===========================================
# 第一步：清理蓝天采集器
#===========================================
echo ""
echo "[步骤1] 清理蓝天采集器..."

# 删除程序目录
if [ -d "/www/wwwroot/skycaiji" ]; then
    rm -rf /www/wwwroot/skycaiji
    echo "  - 已删除 /www/wwwroot/skycaiji 目录"
else
    echo "  - 目录不存在，跳过"
fi

# 删除数据库(保留数据)
echo "  - 保留数据库，仅删除程序"

# 清理nginx配置
if [ -f "/etc/nginx/sites-available/caiji.skillxm.cn.conf" ]; then
    rm -f /etc/nginx/sites-available/caiji.skillxm.cn.conf
    rm -f /etc/nginx/sites-enabled/caiji.skillxm.cn.conf
    nginx -s reload
    echo "  - 已清理nginx配置"
fi

echo "  蓝天采集器清理完成"
