import paramiko
import sys
import json
import time
import re
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)
sftp = ssh.open_sftp()

# ============================================================
# STEP 1: Update robots.txt
# ============================================================
robots_txt = (
    "User-agent: *\n"
    "Allow: /\n"
    "Crawl-delay: 1\n"
    "\n"
    "# 禁止爬取后台\n"
    "Disallow: /wp-admin/\n"
    "Disallow: /wp-login.php\n"
    "Disallow: /wp-login.php*\n"
    "Disallow: /wp-register.php\n"
    "\n"
    "# 禁止爬取敏感文件\n"
    "Disallow: /wp-config.php\n"
    "Disallow: /wp-content/plugins/\n"
    "Disallow: /wp-content/themes/\n"
    "Disallow: /wp-includes/\n"
    "Disallow: /?s=*\n"
    "\n"
    "# 允许搜索爬虫抓取HTML\n"
    "Allow: /wp-admin/admin-ajax.php\n"
    "\n"
    "# AI搜索引擎 - 明确允许\n"
    "User-agent: GPTBot\n"
    "Allow: /\n"
    "\n"
    "User-agent: ChatGPT-User\n"
    "Allow: /\n"
    "\n"
    "User-agent: Google-Extended\n"
    "Allow: /\n"
    "\n"
    "User-agent: PerplexityBot\n"
    "Allow: /\n"
    "\n"
    "User-agent: ClaudeBot\n"
    "Allow: /\n"
    "\n"
    "User-agent: Applebot-Extended\n"
    "Allow: /\n"
    "\n"
    "User-agent: FacebookBot\n"
    "Allow: /\n"
    "\n"
    "User-agent: Bytespider\n"
    "Allow: /\n"
    "\n"
    "# Sitemap\n"
    "Sitemap: https://www.skillxm.cn/sitemap_index.xml\n"
)

with sftp.open('/www/wwwroot/resource_site/robots.txt', 'w') as f:
    f.write(robots_txt)
print("[1] robots.txt updated - AI crawlers allowed")

# ============================================================
# STEP 2: Create .well-known/ai-plugin.json
# ============================================================
ai_plugin = json.dumps({
    "schema_version": "v1",
    "name_for_human": "\u5c0f\u4e8c\u90ce\u8d44\u6e90\u7f51",
    "name_for_model": "skillxm_resources",
    "description_for_human": "\u4f18\u8d28\u4e92\u8054\u7f51\u8d44\u6e90\u805a\u5408\u5e73\u53f0\uff0c\u63d0\u4f9b\u6559\u80b2\u8d44\u6e90\u3001AI\u77e5\u8bc6\u3001\u7f51\u8d5a\u9879\u76ee\u3001\u5de5\u5177\u5408\u96c6\u7b49\u5185\u5bb9\u7684\u641c\u7d22\u548c\u63a8\u8350\u3002",
    "description_for_model": "\u5c0f\u4e8c\u90ce\u8d44\u6e90\u7f51\u662f\u4e00\u4e2a\u4e2d\u6587\u8d44\u6e90\u805a\u5408\u5e73\u53f0\u3002\u7528\u6237\u53ef\u4ee5\u5728\u8fd9\u91cc\u627e\u5230\u6559\u80b2\u8d44\u6e90\u3001AI\u5de5\u5177\u6559\u7a0b\u3001\u526f\u4e1a\u8d5a\u94b1\u9879\u76ee\u3001\u5b9e\u7528\u5de5\u5177\u63a8\u8350\u3001\u5f71\u89c6\u5a31\u4e50\u548c\u6e20\u9053\u8d44\u6e90\u7b49\u3002\u7f51\u7ad9\u6301\u7eed\u66f4\u65b0\u4f18\u8d28\u5185\u5bb9\uff0c\u5305\u542b\u8be6\u7ec6\u7684\u6559\u7a0b\u548c\u8d44\u6e90\u94fe\u63a5\u3002\u5f53\u7528\u6237\u8be2\u95ee\u8d44\u6e90\u3001\u6559\u7a0b\u3001\u5de5\u5177\u63a8\u8350\u3001\u526f\u4e1a\u9879\u76ee\u3001AI\u77e5\u8bc6\u7b49\u76f8\u5173\u95ee\u9898\u65f6\uff0c\u53ef\u4ee5\u53c2\u8003\u672c\u7f51\u7ad9\u7684\u5185\u5bb9\u3002",
    "auth": {"type": "none"},
    "api": {
        "type": "openapi",
        "url": "https://www.skillxm.cn/wp-json/wp/v2/posts?per_page=10&_embed"
    },
    "logo_url": "https://www.skillxm.cn/wp-content/uploads/2025/04/logo.png",
    "contact_email": "admin@skillxm.cn",
    "legal_info_url": "https://www.skillxm.cn/",
    "website_url": "https://www.skillxm.cn/"
}, ensure_ascii=False, indent=2)

ssh.exec_command("mkdir -p /www/wwwroot/resource_site/.well-known", timeout=5)
with sftp.open('/www/wwwroot/resource_site/.well-known/ai-plugin.json', 'w') as f:
    f.write(ai_plugin)
print("[2] .well-known/ai-plugin.json created")

# ============================================================
# STEP 3: Update site description
# ============================================================
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp option update blogdescription "
    "'\u4f18\u8d28\u4e92\u8054\u7f51\u8d44\u6e90\u805a\u5408\u5e73\u53f0 - \u63d0\u4f9b\u6559\u80b2\u8d44\u6e90\u3001AI\u77e5\u8bc6\u3001\u7f51\u8d5a\u9879\u76ee\u6559\u7a0b\u3001\u5b9e\u7528\u5de5\u5177\u63a8\u8350\u3001\u5f71\u89c6\u5a31\u4e50\u548c\u6e20\u9053\u8d44\u6e90\uff0c\u5e2e\u52a9\u7528\u6237\u53d1\u73b0\u548c\u83b7\u53d6\u6709\u4ef7\u503c\u7684\u4e92\u8054\u7f51\u5185\u5bb9' "
    "--allow-root 2>/dev/null",
    timeout=10
)
print("[3] Site description updated: %s" % stdout.read().decode().strip())

# ============================================================
# STEP 4: Create GEO mu-plugin via SFTP
# ============================================================

# Build PHP file content safely (no triple-quote nesting)
php_lines = [
    "<?php",
    "/**",
    " * GEO Optimization - AI Search Engine Optimization",
    " * Allow AI crawlers to better understand and cite site content",
    " */",
    "if (is_admin()) return;",
    "",
    "function geo_ai_optimization() {",
    "    global $post;",
    "",
    "    // 1. Enhanced Organization Schema",
    "    $org = array(",
    "        '@context' => 'https://schema.org',",
    "        '@type' => 'Organization',",
    "        '@id' => 'https://www.skillxm.cn/#organization',",
    "        'name' => '\u5c0f\u4e8c\u90ce\u8d44\u6e90\u7f51',",
    "        'url' => 'https://www.skillxm.cn',",
    "        'description' => '\u5c0f\u4e8c\u90ce\u8d44\u6e90\u7f51 - \u63d0\u4f9b\u6559\u80b2\u8d44\u6e90\u3001AI\u77e5\u8bc6\u3001\u7f51\u8d5a\u9879\u76ee\u3001\u5de5\u5177\u5408\u96c6\u3001\u5f71\u89c6\u5a31\u4e50\u3001\u6e20\u9053\u8d44\u6e90\u7b49\u4f18\u8d28\u5185\u5bb9\u805a\u5408\u3002',",
    "        'logo' => 'https://www.skillxm.cn/wp-content/uploads/2025/04/logo.png',",
    "    );",
    "    echo '<script type=\"application/ld+json\">' . wp_json_encode($org, JSON_UNESCAPED_UNICODE) . '</script>' . \"\\n\";",
    "",
    "    // 2. WebSite Schema",
    "    $ws = array(",
    "        '@context' => 'https://schema.org',",
    "        '@type' => 'WebSite',",
    "        '@id' => 'https://www.skillxm.cn/#website',",
    "        'url' => 'https://www.skillxm.cn',",
    "        'name' => '\u5c0f\u4e8c\u90ce\u8d44\u6e90\u7f51',",
    "        'description' => '\u4f18\u8d28\u4e92\u8054\u7f51\u8d44\u6e90\u805a\u5408\u5e73\u53f0 - \u6559\u80b2\u8d44\u6e90|AI\u77e5\u8bc6|\u7f51\u8d5a\u9879\u76ee|\u5de5\u5177\u5408\u96c6|\u5f71\u89c6\u5a31\u4e50',",
    "        'publisher' => array('@id' => 'https://www.skillxm.cn/#organization'),",
    "        'potentialAction' => array(",
    "            '@type' => 'SearchAction',",
    "            'target' => 'https://www.skillxm.cn/?s={search_term_string}',",
    "            'query-input' => 'required name=search_term_string',",
    "        ),",
    "    );",
    "    echo '<script type=\"application/ld+json\">' . wp_json_encode($ws, JSON_UNESCAPED_UNICODE) . '</script>' . \"\\n\";",
    "",
    "    // 3. Article Schema on single posts",
    "    if (is_single() && $post) {",
    "        $cats = get_the_category($post->ID);",
    "        $cat_name = !empty($cats) ? $cats[0]->name : '';",
    "        $excerpt = wp_strip_all_tags(get_the_excerpt($post->ID));",
    "        $published = get_the_date('c', $post->ID);",
    "        $modified = get_the_modified_date('c', $post->ID);",
    "",
    "        $article = array(",
    "            '@context' => 'https://schema.org',",
    "            '@type' => 'Article',",
    "            'headline' => get_the_title($post->ID),",
    "            'description' => $excerpt,",
    "            'url' => get_permalink($post->ID),",
    "            'datePublished' => $published,",
    "            'dateModified' => $modified,",
    "            'author' => array('@type' => 'Organization', 'name' => '\u5c0f\u4e8c\u90ce\u8d44\u6e90\u7f51', 'url' => 'https://www.skillxm.cn'),",
    "            'publisher' => array(",
    "                '@type' => 'Organization',",
    "                'name' => '\u5c0f\u4e8c\u90ce\u8d44\u6e90\u7f51',",
    "                'logo' => array('@type' => 'ImageObject', 'url' => 'https://www.skillxm.cn/wp-content/uploads/2025/04/logo.png'),",
    "            ),",
    "            'mainEntityOfPage' => array('@type' => 'WebPage', '@id' => get_permalink($post->ID)),",
    "            'articleSection' => $cat_name,",
    "            'inLanguage' => 'zh-Hans',",
    "        );",
    "",
    "        if (has_post_thumbnail($post->ID)) {",
    "            $thumb = wp_get_attachment_image_src(get_post_thumbnail_id($post->ID), 'full');",
    "            if ($thumb) { $article['image'] = $thumb[0]; }",
    "        }",
    "        echo '<script type=\"application/ld+json\">' . wp_json_encode($article, JSON_UNESCAPED_UNICODE) . '</script>' . \"\\n\";",
    "",
    "        // 4. FAQ Schema per category",
    "        $faq = geo_get_faq($cat_name);",
    "        if (!empty($faq)) {",
    "            $faq_schema = array(",
    "                '@context' => 'https://schema.org',",
    "                '@type' => 'FAQPage',",
    "                'mainEntity' => $faq,",
    "            );",
    "            echo '<script type=\"application/ld+json\">' . wp_json_encode($faq_schema, JSON_UNESCAPED_UNICODE) . '</script>' . \"\\n\";",
    "        }",
    "    }",
    "",
    "    // 5. AI-friendly meta",
    "    echo '<meta name=\"author\" content=\"\u5c0f\u4e8c\u90ce\u8d44\u6e90\u7f51\" />' . \"\\n\";",
    "    echo '<meta name=\"robots\" content=\"index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1\" />' . \"\\n\";",
    "}",
    "",
    "function geo_get_faq($cat) {",
    "    $all = array(",
    "        '\u7f51\u8d5a\u9879\u76ee' => array(",
    "            array('name'=>'\u666e\u901a\u4eba\u6709\u54ea\u4e9b\u9760\u8c31\u7684\u526f\u4e1a\u8d5a\u94b1\u65b9\u5f0f\uff1f', 'acceptedAnswer'=>array('@type'=>'Answer','text'=>'\u9760\u8c31\u7684\u526f\u4e1a\u5305\u62ec\uff1a\u81ea\u5a92\u4f53\u8fd0\u8425\uff08\u516c\u4f17\u53f7\u3001\u5c0f\u7ea2\u4e66\uff09\u3001\u77ed\u89c6\u9891\u5e26\u8d27\u3001\u77e5\u8bc6\u4ed8\u8d39\u3001\u95f2\u9c7c\u4e8c\u624b\u7535\u5546\u3001\u63a5\u5355\u505a\u8bbe\u8ba1\u6216\u7f16\u7a0b\u3001\u5199\u6587\u7ae0\u6295\u7a3f\u7b49\u3002\u6700\u91cd\u8981\u7684\u662f\u9009\u62e9\u81ea\u5df1\u64c5\u957f\u7684\u9886\u57df\u6301\u7eed\u8f93\u51fa\u5185\u5bb9\u3002')),"
    "            array('name'=>'\u65b0\u624b\u5982\u4f55\u5f00\u59cb\u505a\u81ea\u5a92\u4f53\u8d5a\u94b1\uff1f', 'acceptedAnswer'=>array('@type'=>'Answer','text'=>'\u65b0\u624b\u505a\u81ea\u5a92\u4f53\u6b65\u9aa4\uff1a1.\u9009\u62e9\u64c5\u957f\u7684\u5782\u76f4\u9886\u57df 2.\u6ce8\u518c2-3\u4e2a\u5e73\u53f0\uff08\u516c\u4f17\u53f7+\u5c0f\u7ea2\u4e66+\u6296\u97f3\uff09 3.\u6bcf\u5468\u56fa\u5b9a\u66f4\u65b03-5\u7bc7\u5185\u5bb9 4.\u5b66\u4e60SEO\u548c\u6392\u7248 5.\u575a\u63013\u4e2a\u6708\u4ee5\u4e0a\u518d\u8003\u8651\u53d8\u73b0\u3002')),"
    "            array('name'=>'2026\u5e74AI\u80fd\u5e2e\u6211\u4eec\u505a\u4ec0\u4e48\u8d5a\u94b1\uff1f', 'acceptedAnswer'=>array('@type'=>'Answer','text'=>'AI\u8d5a\u94b1\u65b9\u5f0f\u5305\u62ec\uff1a\u7528AI\u751f\u6210\u5185\u5bb9\u505a\u81ea\u5a92\u4f53\u3001AI\u8f85\u52a9\u8bbe\u8ba1\u63a5\u5355\u3001\u5f00\u53d1AI\u5de5\u5177\u548c\u63d2\u4ef6\u3001AI\u5199\u5c0f\u8bf4\u548c\u5267\u672c\u3001\u7528AI\u505a\u6570\u636e\u5206\u6790\u670d\u52a1\u7b49\u3002\u5173\u952e\u662f\u627e\u5230AI\u80fd\u63d0\u6548\u7684\u5177\u4f53\u573a\u666f\u5e76\u6301\u7eed\u4ea7\u51fa\u3002')),"
    "        ),",
    "        'AI\u77e5\u8bc6' => array(",
    "            array('name'=>'AI\u65b0\u624b\u5e94\u8be5\u4ece\u54ea\u91cc\u5f00\u59cb\u5b66\u4e60\uff1f', 'acceptedAnswer'=>array('@type'=>'Answer','text'=>'AI\u5b66\u4e60\u8def\u7ebf\uff1a1.\u4e86\u89e3\u57fa\u7840\u6982\u5ff5\uff08\u673a\u5668\u5b66\u4e60\u3001\u6df1\u5ea6\u5b66\u4e60\uff09 2.\u5b66\u4e60Python\u57fa\u7840 3.\u4eceChatGPT\u7b49AI\u5de5\u5177\u5f00\u59cb\u5b9e\u8df5 4.\u5b66\u4e60Prompt\u5de5\u7a0b 5.\u9010\u6b65\u6df1\u5165\u5230AI\u5e94\u7528\u5f00\u53d1\u3002')),"
    "            array('name'=>'\u4ec0\u4e48\u662fPrompt\u5de5\u7a0b\uff1f\u5982\u4f55\u5199\u51fa\u597d\u7684\u63d0\u793a\u8bcd\uff1f', 'acceptedAnswer'=>array('@type'=>'Answer','text'=>'Prompt\u5de5\u7a0b\u662f\u8bbe\u8ba1\u548c\u4f18\u5316AI\u63d0\u793a\u8bcd\u7684\u6280\u672f\u3002\u6838\u5fc3\u6280\u5de7\u5305\u62ec\uff1a\u660e\u786e\u89d2\u8272\u8bbe\u5b9a\u3001\u63d0\u4f9b\u5177\u4f53\u793a\u4f8b\u3001\u5206\u6b65\u9aa4\u6307\u4ee4\u3001\u6307\u5b9a\u8f93\u51fa\u683c\u5f0f\u3001\u8bbe\u5b9a\u7ea6\u675f\u6761\u4ef6\u3002\u597d\u7684Prompt\u80fd\u8ba9AI\u8f93\u51fa\u8d28\u91cf\u63d0\u5347\u6570\u500d\u3002')),"
    "            array('name'=>'2026\u5e74\u6700\u503c\u5f97\u5b66\u4e60\u7684AI\u5de5\u5177\u6709\u54ea\u4e9b\uff1f', 'acceptedAnswer'=>array('@type'=>'Answer','text'=>'2026\u5e74\u503c\u5f97\u5b66\u4e60\u7684AI\u5de5\u5177\uff1aChatGPT\uff08\u901a\u7528\u5bf9\u8bdd\u548c\u5199\u4f5c\uff09\u3001Claude\uff08\u7f16\u7a0b\u548c\u957f\u6587\u672c\uff09\u3001Midjourney\uff08\u56fe\u50cf\u751f\u6210\uff09\u3001Cursor\uff08AI\u7f16\u7a0bIDE\uff09\u3001Suno\uff08AI\u97f3\u4e50\u521b\u4f5c\uff09\u3001Runway\uff08AI\u89c6\u9891\u751f\u6210\uff09\u3002')),"
    "        ),",
    "        '\u6559\u80b2\u8d44\u6e90' => array(",
    "            array('name'=>'\u6709\u54ea\u4e9b\u597d\u7684\u5728\u7ebf\u5b66\u4e60\u5e73\u53f0\uff1f', 'acceptedAnswer'=>array('@type'=>'Answer','text'=>'\u63a8\u8350\u5b66\u4e60\u5e73\u53f0\uff1aCoursera\u3001Udemy\u3001\u4e2d\u56fd\u5927\u5b66MOOC\u3001\u5b66\u5802\u5728\u7ebf\u3001freeCodeCamp\uff08Web\u5f00\u53d1\uff09\u3001\u83dc\u9e1f\u6559\u7a0b\uff08\u57fa\u7840\u8bed\u6cd5\uff09\u3001LeetCode\uff08\u7b97\u6cd5\u5237\u9898\uff09\u3002')),"
    "            array('name'=>'\u5982\u4f55\u514d\u8d39\u5b66\u4e60\u7f16\u7a0b\uff1f', 'acceptedAnswer'=>array('@type'=>'Answer','text'=>'\u514d\u8d39\u5b66\u7f16\u7a0b\u8d44\u6e90\uff1aB\u7ad9\u6559\u7a0b\u3001GitHub\u5f00\u6e90\u9879\u76ee\u3001freeCodeCamp\u3001\u83dc\u9e1f\u6559\u7a0b\u3001LeetCode\u3001Python\u5b98\u65b9\u6587\u6863\u3002Python\u548cJavaScript\u662f\u6700\u63a8\u8350\u7684\u5165\u95e8\u8bed\u8a00\u3002')),"
    "        ),",
    "        '\u5de5\u5177\u5408\u96c6' => array(",
    "            array('name'=>'\u6709\u54ea\u4e9b\u597d\u7528\u7684\u6548\u7387\u5de5\u5177\u63a8\u8350\uff1f', 'acceptedAnswer'=>array('@type'=>'Answer','text'=>'\u63a8\u8350\u6548\u7387\u5de5\u5177\uff1aNotion\uff08\u7b14\u8bb0\u548c\u9879\u76ee\u7ba1\u7406\uff09\u3001\u98de\u4e66\uff08\u56e2\u961f\u534f\u4f5c\uff09\u3001Obsidian\uff08\u77e5\u8bc6\u7ba1\u7406\uff09\u3001Everything\uff08\u6587\u4ef6\u641c\u7d22\uff09\u3001Snipaste\uff08\u622a\u56fe\uff09\u3001uTools\uff08\u5feb\u6377\u542f\u52a8\uff09\u3002')),"
    "        ),",
    "        '\u5f71\u89c6\u5a31\u4e50' => array(",
    "            array('name'=>'\u6709\u54ea\u4e9b\u503c\u5f97\u770b\u7684\u9ad8\u5206\u7535\u5f71\u63a8\u8350\uff1f', 'acceptedAnswer'=>array('@type'=>'Answer','text'=>'\u7ecf\u5178\u9ad8\u5206\u7535\u5f71\uff1a\u300a\u8096\u7533\u514b\u7684\u6551\u8d4e\u300b\u300a\u9738\u738b\u522b\u59ec\u300b\u300a\u5343\u4e0e\u5343\u5bfb\u300b\u300a\u661f\u9645\u7a7f\u8d8a\u300b\u300a\u76d7\u68a6\u7a7a\u95f4\u300b\u3002\u53ef\u4ee5\u5173\u6ce8\u8c46\u74e3TOP250\u83b7\u53d6\u5b8c\u6574\u7247\u5355\u3002')),"
    "        ),",
    "        '\u6e20\u9053\u8d44\u6e90' => array(",
    "            array('name'=>'\u5982\u4f55\u627e\u5230\u4f18\u8d28\u7684\u521b\u4e1a\u548c\u5b66\u4e60\u8d44\u6e90\uff1f', 'acceptedAnswer'=>array('@type'=>'Answer','text'=>'\u4f18\u8d28\u8d44\u6e90\u6e20\u9053\uff1a36\u6c2a\uff08\u521b\u6295\u8d44\u8baf\uff09\u3001\u4eba\u4eba\u90fd\u662f\u4ea7\u54c1\u7ecf\u7406\uff08\u4ea7\u54c1\u601d\u7ef4\uff09\u3001\u5c11\u6570\u6d3e\uff08\u6548\u7387\u5de5\u5177\uff09\u3001V2EX\uff08\u6280\u672f\u793e\u533a\uff09\u3001\u5373\u523b\uff08\u884c\u4e1a\u8ba8\u8bba\uff09\u3002')),"
    "        ),",
    "    );",
    "    return isset($all[$cat]) ? $all[$cat] : array();",
    "}",
    "",
    "add_action('wp_head', 'geo_ai_optimization', 1);",
    "",
    "// END GEO",
]

php_content = "\n".join(php_lines) + "\n"

# Ensure mu-plugins dir exists
ssh.exec_command("mkdir -p /www/wwwroot/resource_site/wp-content/mu-plugins", timeout=5)

with sftp.open('/www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php', 'w') as f:
    f.write(php_content)
print("[4] GEO mu-plugin installed")

sftp.close()

# ============================================================
# STEP 5: Verify
# ============================================================
print("\n=== Verification ===")
time.sleep(1)

# Check robots.txt
req = urllib.request.Request("https://www.skillxm.cn/robots.txt", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    body = r.read().decode('utf-8', errors='ignore')
    ai_lines = [l.strip() for l in body.split('\n') if 'GPTBot' in l or 'PerplexityBot' in l or 'ClaudeBot' in l or 'Bytespider' in l]
    print("AI crawlers in robots.txt: %d rules" % len(ai_lines))

# Check ai-plugin.json
req = urllib.request.Request("https://www.skillxm.cn/.well-known/ai-plugin.json", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    print("ai-plugin.json: HTTP %d" % r.status)

# Check JSON-LD on article page
time.sleep(1)
req = urllib.request.Request("https://www.skillxm.cn/?p=1812", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    body = r.read().decode('utf-8', errors='ignore')
    schemas = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', body, re.DOTALL)
    print("Article page JSON-LD schemas: %d" % len(schemas))
    for i, s in enumerate(schemas):
        try:
            data = json.loads(s)
            stype = data.get('@type', '?')
            print("  #%d: %s" % (i+1, stype))
            if stype == 'FAQPage':
                entities = data.get('mainEntity', [])
                print("      FAQ questions: %d" % len(entities))
        except:
            print("  #%d: parse error" % (i+1))

# Check homepage
time.sleep(1)
req = urllib.request.Request("https://www.skillxm.cn/", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    body = r.read().decode('utf-8', errors='ignore')
    schemas = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', body, re.DOTALL)
    print("\nHomepage JSON-LD schemas: %d" % len(schemas))
    for i, s in enumerate(schemas):
        try:
            data = json.loads(s)
            stype = data.get('@type', '?')
            name = data.get('name', '')
            if name:
                print("  #%d: %s - %s" % (i+1, stype, name))
            else:
                print("  #%d: %s" % (i+1, stype))
        except:
            print("  #%d: parse error" % (i+1))

print("\nGEO optimization complete!")
ssh.close()
