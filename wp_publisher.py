#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小二郎资源网 - 文章发布脚本
通过数据库直接插入文章
"""

import paramiko
import pymysql
import re
from datetime import datetime

# 服务器配置
SERVER = {
    'host': '43.103.5.46',
    'user': 'root',
    'password': 'Langlang0.'
}

# 数据库配置
DB = {
    'host': 'localhost',
    'user': 'wpuser',
    'password': 'WpPass2024!',
    'database': 'wp_skillxm',
    'charset': 'utf8mb4'
}

# 分类映射
CATEGORIES = {
    'AI知识': 1,
    'ai': 1,
    'aigc': 1,
    '书籍资料': 2,
    '跨境电商': 3,
    '自媒体运营': 4,
    '自媒体': 4,
    '教育资源': 5,
    '工具合集': 6,
    '工具': 6,
    '影视娱乐': 7,
    '影视': 7,
    '健康养生': 8,
    '健康': 8,
    '影视在线': 9,
    '课程资料': 10,
    '课程': 10,
    '传统文化': 11,
    '自动化工具': 12,
    '自动化': 12,
}

def generate_article(title, description, download_link, category_name=None):
    """生成文章内容"""
    content = f"""<!-- wp:paragraph -->
<p><strong>一份资料，助你快速上手！</strong></p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>📦 资源内容包括：</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{description}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>👥 适合谁：</h3>
<!-- /wp:heading -->

<!-- wp:list -->
<ul>
<li>想系统学习相关技能的新手</li>
<li>想提升工作效率的打工人</li>
<li>想通过技能变现的自由职业者</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
<h3>📥 下载链接：</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>夸克网盘：</strong> <a href="{download_link}">{download_link}</a></p>
<!-- /wp:paragraph -->

<!-- wp:quote -->
<blockquote class="wp-block-quote"><p>💡 提示：建议使用夸克网盘APP保存，速度更快</p></blockquote>
<!-- /wp:quote -->
"""
    return content

def get_category_id(category_name):
    """获取分类ID"""
    if not category_name:
        return 1  # 默认分类
    
    category_name = category_name.lower().strip()
    for key, cat_id in CATEGORIES.items():
        if key.lower() in category_name or category_name in key.lower():
            return cat_id
    return 1

def publish_post(title, content, category_id=1):
    """发布文章到数据库"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER['host'], username=SERVER['user'], password=SERVER['password'])
    
    # 转义单引号
    title_escaped = title.replace("'", "''")
    content_escaped = content.replace("'", "''").replace("\\", "\\\\")
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post_name = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]+', '-', title)[:50].strip('-')
    
    sql = f"""
    INSERT INTO wp_posts (
        post_author, post_date, post_date_gmt, post_content, post_title,
        post_excerpt, post_status, comment_status, ping_status,
        post_password, post_name, to_ping, pinged, post_modified,
        post_modified_gmt, post_content_filtered, post_parent, guid,
        menu_order, post_type, post_mime_type, comment_count
    ) VALUES (
        1, '{now}', '{now}', '{content_escaped}', '{title_escaped}',
        '', 'publish', 'open', 'open',
        '', '{post_name}', '', '', '{now}',
        '{now}', '', 0, '',
        0, 'post', '', 0
    );
    """
    
    # 通过 SSH 执行 MySQL 命令
    mysql_cmd = f"""mysql -u{DB['user']} -p{DB['password']} {DB['database']} -e "{sql}" """
    
    stdin, stdout, stderr = ssh.exec_command(mysql_cmd)
    err = stderr.read().decode()
    
    if err and 'error' in err.lower():
        print(f"❌ 发布失败: {err}")
        ssh.close()
        return False
    
    # 获取刚插入的文章ID
    stdin, stdout, stderr = ssh.exec_command(
        f"mysql -u{DB['user']} -p{DB['password']} {DB['database']} -e \"SELECT MAX(ID) FROM wp_posts WHERE post_type='post';\""
    )
    result = stdout.read().decode()
    post_id = result.strip().split('\n')[-1] if result else '0'
    
    # 设置分类关系
    if category_id and post_id != '0':
        term_sql = f"""
        INSERT INTO wp_term_relationships (object_id, term_taxonomy_id, term_order)
        VALUES ({post_id}, {category_id}, 0);
        """
        stdin, stdout, stderr = ssh.exec_command(
            f"mysql -u{DB['user']} -p{DB['password']} {DB['database']} -e \"{term_sql}\""
        )
    
    ssh.close()
    print(f"✅ 发布成功！文章ID: {post_id}")
    print(f"   查看地址: https://skillxm.cn/?p={post_id}")
    return True

def main():
    print("=" * 50)
    print("小二郎资源网 - 文章发布工具")
    print("=" * 50)
    
    # 交互式输入
    print("\n请输入资源信息（输入 q 退出）：\n")
    
    while True:
        print("-" * 40)
        title = input("📌 标题: ").strip()
        if title.lower() == 'q':
            break
        if not title:
            print("标题不能为空！")
            continue
            
        description = input("📝 资源描述: ").strip()
        download_link = input("🔗 下载链接: ").strip()
        category = input("📁 分类 (可选，默认AI知识): ").strip() or "AI知识"
        
        # 生成文章内容
        content = generate_article(title, description, download_link, category)
        category_id = get_category_id(category)
        
        print(f"\n📋 文章预览:")
        print(f"   标题: {title}")
        print(f"   分类: {category} (ID: {category_id})")
        print(f"   链接: {download_link}")
        
        confirm = input("\n确认发布? (y/n): ").strip().lower()
        if confirm == 'y':
            publish_post(title, content, category_id)
        else:
            print("已取消")

if __name__ == '__main__':
    main()
