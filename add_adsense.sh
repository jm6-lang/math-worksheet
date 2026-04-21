#!/bin/bash
# 添加Google AdSense代码到WordPress头部
# 运行: bash add_adsense.sh

ADSENSE_CODE='<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4710405779358793"
 crossorigin="anonymous"></script>'

HEADER_FILE="/www/wwwroot/resource_site/wp-content/themes/yymarket/header.php"

echo "=== 添加Google AdSense代码 ==="

# 检查是否已存在
if grep -q "ca-pub-4710405779358793" "$HEADER_FILE" 2>/dev/null; then
    echo "AdSense代码已存在，无需重复添加"
    exit 0
fi

# 备份
cp "$HEADER_FILE" "${HEADER_FILE}.bak.$(date +%Y%m%d%H%M%S)"

# 在</head>前插入AdSense代码
sed -i "s|</head>|${ADSENSE_CODE}\n</head>|" "$HEADER_FILE"

# 验证
if grep -q "ca-pub-4710405779358793" "$HEADER_FILE"; then
    echo "✅ AdSense代码添加成功"
    echo ""
    echo "已添加到: $HEADER_FILE"
else
    echo "❌ 添加失败"
fi
