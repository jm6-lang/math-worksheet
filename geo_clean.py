import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)
sftp = ssh.open_sftp()

# Clean mu-plugin - use wp_footer instead of wp_head to avoid conflicts
# Inject JSON-LD directly into footer
php_content = """<?php
// GEO Optimization for AI Search Engines
add_action('wp_footer', 'geo_add_structured_data', 99);
function geo_add_structured_data() {
    if (is_admin()) return;
    global $post;
    echo '<!-- GEO Structured Data -->';
    
    // Enhanced Article Schema for single posts
    if (is_single() && $post) {
        $cats = get_the_category($post->ID);
        $cat_name = !empty($cats) ? $cats[0]->name : '';
        $excerpt = wp_strip_all_tags(get_the_excerpt($post->ID));
        if (strlen($excerpt) > 300) $excerpt = substr($excerpt, 0, 300) . '...';
        $published = get_the_date('c', $post->ID);
        $modified = get_the_modified_date('c', $post->ID);
        $thumb = '';
        if (has_post_thumbnail($post->ID)) {
            $t = wp_get_attachment_image_src(get_post_thumbnail_id($post->ID), 'full');
            if ($t) $thumb = $t[0];
        }
        
        $a = array();
        $a['@context'] = 'https://schema.org';
        $a['@type'] = 'Article';
        $a['headline'] = get_the_title($post->ID);
        $a['description'] = $excerpt;
        $a['url'] = get_permalink($post->ID);
        $a['datePublished'] = $published;
        $a['dateModified'] = $modified;
        $a['author'] = array('@type'=>'Organization','name'=>'小二郎资源网','url'=>'https://www.skillxm.cn');
        $a['publisher'] = array('@type'=>'Organization','name'=>'小二郎资源网','logo'=>array('@type'=>'ImageObject','url'=>'https://www.skillxm.cn/wp-content/uploads/2025/04/logo.png'));
        $a['mainEntityOfPage'] = array('@type'=>'WebPage','@id'=>get_permalink($post->ID));
        $a['articleSection'] = $cat_name;
        $a['inLanguage'] = 'zh-Hans';
        if ($thumb) $a['image'] = $thumb;
        
        echo '<script type="application/ld+json">' . wp_json_encode($a, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES) . '</script>';
        
        // FAQ Schema
        $faq = geo_faq($cat_name);
        if (!empty($faq)) {
            $f = array();
            $f['@context'] = 'https://schema.org';
            $f['@type'] = 'FAQPage';
            $f['mainEntity'] = $faq;
            echo '<script type="application/ld+json">' . wp_json_encode($f, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES) . '</script>';
        }
    }
    
    // Homepage: Enhanced Organization + WebSite
    if (is_front_page() || is_home()) {
        $org = array(
            '@context'=>'https://schema.org','@type'=>'Organization',
            '@id'=>'https://www.skillxm.cn/#organization',
            'name'=>'小二郎资源网','url'=>'https://www.skillxm.cn',
            'description'=>'优质互联网资源聚合平台 - 提供教育资源、AI知识、网赚项目教程、实用工具推荐、影视娱乐和渠道资源，帮助用户发现和获取有价值的互联网内容。',
            'logo'=>'https://www.skillxm.cn/wp-content/uploads/2025/04/logo.png',
        );
        echo '<script type="application/ld+json">' . wp_json_encode($org, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES) . '</script>';
    }
    
    echo '<!-- /GEO -->';
}

function geo_faq($cat) {
    $all = array(
        '网赚项目' => array(
            array('@type'=>'Question','name'=>'普通人有哪些靠谱的副业赚钱方式？','acceptedAnswer'=>array('@type'=>'Answer','text'=>'靠谱的副业包括：自媒体运营（公众号、小红书）、短视频带货、知识付费、闲鱼二手电商、接单做设计或编程、写文章投稿等。最重要的是选择自己擅长的领域持续输出内容。')),
            array('@type'=>'Question','name'=>'新手如何开始做自媒体赚钱？','acceptedAnswer'=>array('@type'=>'Answer','text'=>'新手做自媒体步骤：1.选择擅长的垂直领域 2.注册2-3个平台（公众号+小红书+抖音）3.每周固定更新3-5篇内容 4.学习SEO和排版 5.坚持3个月以上再考虑变现。')),
            array('@type'=>'Question','name'=>'2026年AI能帮我们做什么赚钱？','acceptedAnswer'=>array('@type'=>'Answer','text'=>'AI赚钱方式包括：用AI生成内容做自媒体、AI辅助设计接单、开发AI工具和插件、AI写小说和剧本、用AI做数据分析服务等。关键是找到AI能提效的具体场景并持续产出。')),
        ),
        'AI知识' => array(
            array('@type'=>'Question','name'=>'AI新手应该从哪里开始学习？','acceptedAnswer'=>array('@type'=>'Answer','text'=>'AI学习路线：1.了解基础概念（机器学习、深度学习）2.学习Python基础 3.从ChatGPT等AI工具开始实践 4.学习Prompt工程 5.逐步深入到AI应用开发。')),
            array('@type'=>'Question','name'=>'什么是Prompt工程？如何写出好的提示词？','acceptedAnswer'=>array('@type'=>'Answer','text'=>'Prompt工程是设计和优化AI提示词的技术。核心技巧包括：明确角色设定、提供具体示例、分步骤指令、指定输出格式、设定约束条件。好的Prompt能让AI输出质量提升数倍。')),
            array('@type'=>'Question','name'=>'2026年最值得学习的AI工具有哪些？','acceptedAnswer'=>array('@type'=>'Answer','text'=>'2026年值得学习的AI工具：ChatGPT（通用对话和写作）、Claude（编程和长文本）、Midjourney（图像生成）、Cursor（AI编程IDE）、Suno（AI音乐创作）、Runway（AI视频生成）。')),
        ),
        '教育资源' => array(
            array('@type'=>'Question','name'=>'有哪些好的在线学习平台？','acceptedAnswer'=>array('@type'=>'Answer','text'=>'推荐学习平台：Coursera、Udemy、中国大学MOOC、学堂在线、freeCodeCamp（Web开发）、菜鸟教程（基础语法）、LeetCode（算法刷题）。')),
            array('@type'=>'Question','name'=>'如何免费学习编程？','acceptedAnswer'=>array('@type'=>'Answer','text'=>'免费学编程资源：B站教程、GitHub开源项目、freeCodeCamp、菜鸟教程、LeetCode、Python官方文档。Python和JavaScript是最推荐的入门语言。')),
        ),
        '工具合集' => array(
            array('@type'=>'Question','name'=>'有哪些好用的效率工具推荐？','acceptedAnswer'=>array('@type'=>'Answer','text'=>'推荐效率工具：Notion（笔记和项目管理）、飞书（团队协作）、Obsidian（知识管理）、Everything（文件搜索）、Snipaste（截图）、uTools（快捷启动器）。')),
        ),
        '影视娱乐' => array(
            array('@type'=>'Question','name'=>'有哪些值得看的高分电影推荐？','acceptedAnswer'=>array('@type'=>'Answer','text'=>'经典高分电影：《肖申克的救赎》《霸王别姬》《千与千寻》《星际穿越》《盗梦空间》。可以关注豆瓣TOP250获取完整片单。')),
        ),
        '渠道资源' => array(
            array('@type'=>'Question','name'=>'如何找到优质的创业和学习资源？','acceptedAnswer'=>array('@type'=>'Answer','text'=>'优质资源渠道：36氪（创投资讯）、人人都是产品经理（产品思维）、少数派（效率工具）、V2EX（技术社区）、即刻（行业讨论）。')),
        ),
    );
    return isset($all[$cat]) ? $all[$cat] : array();
}
"""

# Remove .bak and write new clean file
ssh.exec_command("rm -f /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php.bak", timeout=5)
with sftp.open('/www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php', 'w') as f:
    f.write(php_content)
print("Clean mu-plugin installed")

# Verify PHP syntax
stdin, stdout, stderr = ssh.exec_command("php -l /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php 2>&1", timeout=10)
print("PHP syntax: %s" % stdout.read().decode().strip())

sftp.close()

# Verify page output
import time, urllib.request, re, json
time.sleep(1)

req = urllib.request.Request("https://www.skillxm.cn/?p=1812", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    body = r.read().decode('utf-8', errors='ignore')
    schemas = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', body, re.DOTALL)
    print("Article JSON-LD count: %d" % len(schemas))
    for i, s in enumerate(schemas):
        try:
            data = json.loads(s)
            if '@graph' in data:
                print("  #%d: @graph (%d items)" % (i+1, len(data['@graph'])))
            else:
                stype = data.get('@type','?')
                print("  #%d: %s" % (i+1, stype))
                if stype == 'FAQPage':
                    print("    FAQ: %d questions" % len(data.get('mainEntity', [])))
        except:
            print("  #%d: parse error" % (i+1))

ssh.close()
print("Done!")
