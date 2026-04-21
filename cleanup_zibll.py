import paramiko, time, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

def connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)
    return client

def run_cmd(client, cmd, timeout=15):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace').strip()
        return out
    except:
        return '[TIMEOUT]'

client = connect()

# Write cleanup script to remote
script = """#!/bin/bash
echo "=========================================="
echo "  开始清理残留"
echo "=========================================="

# 1. Delete fake api.zibll.com
echo ""
echo "[1] 删除假API站点 api.zibll.com"
if [ -d /www/wwwroot/api.zibll.com ]; then
    rm -rf /www/wwwroot/api.zibll.com
    echo "  已删除 /www/wwwroot/api.zibll.com"
else
    echo "  不存在"
fi

# 2. Delete zibll-bypass mu-plugin
echo ""
echo "[2] 删除 zibll-bypass.php"
if [ -f /www/wwwroot/resource_site/wp-content/mu-plugins.disabled/zibll-bypass.php ]; then
    rm -f /www/wwwroot/resource_site/wp-content/mu-plugins.disabled/zibll-bypass.php
    echo "  已删除"
else
    echo "  不存在"
fi
# Clean empty mu-plugins.disabled dir
rmdir /www/wwwroot/resource_site/wp-content/mu-plugins.disabled 2>/dev/null
echo "  mu-plugins.disabled dir cleaned"

# 3. Clean /tmp zibll files
echo ""
echo "[3] 清理 /tmp 中的zibll相关文件"
rm -f /tmp/zibll-7.8.zip
rm -f /tmp/test_zibll.php
rm -f /tmp/zibll_safe_check.py
rm -f /tmp/zibll_functions_backup.php
rm -f /tmp/switch_zibll.sql
rm -f /tmp/zibll_opts.html
rm -f /tmp/del_zibll.sh
rm -f /tmp/fix_theme.sh
rm -f /tmp/debug_bash.sh
rm -f /tmp/check_db.sh
rm -f /tmp/del_zibll.sh
rm -f /tmp/q_test.php
rm -rf /tmp/zibll_backup_deleted
rm -f /tmp/zibll_backup_20260405_194507.tar.gz
echo "  /tmp 已清理"

# 4. Clean zibll database options
echo ""
echo "[4] 清理数据库中zibll相关选项"
mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e "
DELETE FROM wp_options WHERE option_name IN (
    'theme_mods_zibll',
    'widget_zib_bbs_widget_ui_plate_info',
    'widget_zib_bbs_widget_ui_plate_lists',
    'widget_zib_bbs_widget_ui_plate_moderator',
    'widget_zib_bbs_widget_ui_posts_lists',
    'widget_zib_bbs_widget_ui_topic_lists',
    'widget_zib_widget_ui_dplayer',
    'widget_zib_widget_ui_graphic_cover',
    'widget_zib_widget_ui_hot_posts',
    'widget_zib_widget_ui_icon_card',
    'widget_zib_widget_ui_icon_cover_card',
    'widget_zib_widget_ui_iframe',
    'widget_zib_widget_ui_posts_pay',
    'widget_zib_widget_ui_slider',
    'widget_zib_widget_ui_term_card',
    'widget_zib_widget_ui_term_lists_card',
    'widget_zib_widget_ui_user_ranking',
    'zibll_options'
);" 2>/dev/null
echo "  已删除18个zibll数据库选项"

# 5. Drop zibpay tables
echo ""
echo "[5] 清理zibpay数据表"
mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e "
DROP TABLE IF EXISTS wp_zibpay_card_pass;
DROP TABLE IF EXISTS wp_zibpay_income;
DROP TABLE IF EXISTS wp_zibpay_order;
" 2>/dev/null
echo "  已删除 wp_zibpay_card_pass, wp_zibpay_income, wp_zibpay_order"

# 6. Clean zibll usermeta
echo ""
echo "[6] 清理用户元数据中的zibll信息"
mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e "
DELETE FROM wp_usermeta WHERE meta_key LIKE '%zib%';
DELETE FROM wp_usermeta WHERE meta_key LIKE '%zibpay%';
" 2>/dev/null
COUNT=$(mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "SELECT COUNT(*) FROM wp_usermeta WHERE meta_key LIKE '%zib%';" 2>/dev/null)
echo "  清理完成 (剩余zib usermeta: $COUNT)"

# 7. Clean zibll postmeta
echo ""
echo "[7] 清理文章元数据中的zibll信息"
mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e "
DELETE FROM wp_postmeta WHERE meta_key LIKE '%zib%';
" 2>/dev/null
echo "  已清理zib postmeta"

# 8. Final verify
echo ""
echo "=========================================="
echo "  验证清理结果"
echo "=========================================="

echo ""
echo "--- 文件残留检查 ---"
FOUND=$(find /www/wwwroot -iname "*zibll*" 2>/dev/null | grep -v "/proc\\|/sys")
echo "$FOUND"
if [ -z "$FOUND" ]; then
    echo "  无残留文件"
fi

echo ""
echo "--- 数据库残留检查 ---"
mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "SELECT option_name FROM wp_options WHERE option_name LIKE '%zib%';" 2>/dev/null
COUNT=$(mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "SELECT COUNT(*) FROM wp_options WHERE option_name LIKE '%zib%';" 2>/dev/null)
echo "  数据库zib选项残留: $COUNT"

mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "SHOW TABLES LIKE '%zib%';" 2>/dev/null
echo "  zib相关表: (上面显示的就是剩余的)"

echo ""
echo "--- 站点测试 ---"
systemctl restart php8.1-fpm 2>/dev/null
sleep 1
HTTP_CODE=$(curl -s -k --max-time 10 -o /dev/null -w "%{http_code}" https://127.0.0.1/)
PAGE_SIZE=$(curl -s -k --max-time 10 https://127.0.0.1/ | wc -c)
TITLE=$(curl -s -k --max-time 10 https://127.0.0.1/ | grep -o "<title>[^<]*</title>" | head -1)
echo "  HTTP: $HTTP_CODE, Size: ${PAGE_SIZE}B"
echo "  $TITLE"

echo ""
echo "=========================================="
echo "  清理完成"
echo "=========================================="
"""

sftp = client.open_sftp()
with sftp.file('/tmp/cleanup_zibll.sh', 'w') as f:
    f.write(script)
sftp.close()

out = run_cmd(client, 'bash /tmp/cleanup_zibll.sh', timeout=30)
print(out)

client.close()
