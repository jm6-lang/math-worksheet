# -*- coding: utf-8 -*-
# Final SEO step: Add JSON-LD structured data and verify everything
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# ===== Step 7: Add JSON-LD structured data to header =====
# Check current header.php
commands = [
    "wp option get siteurl --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>/dev/null",
    "wp rewrite flush --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>&1",
    
    # Check if Yoast sitemap endpoint works
    "curl -s -o /dev/null -w '%{http_code}' https://skillxm.cn/sitemap_index.xml 2>/dev/null || echo 'curl-fail'",
    
    # Check current homepage head for meta tags
    "curl -s https://skillxm.cn/ 2>/dev/null | grep -i '<title>' | head -3 || echo 'no-title'",
    
    # Verify robots.txt accessible
    "curl -s https://skillxm.cn/robots.txt 2>/dev/null | head -5 || echo 'no-robots'",
]

for cmd in commands:
    print(">> {}".format(cmd), flush=True)
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out:
        print(out, flush=True)
    print(flush=True)

# ===== Step 8: Add JSON-LD to all posts via wp_head hook =====
jsonld_script = r'''<?php
// Add JSON-LD structured data to all posts
add_action('wp_head', function() {
    if (is_singular('post')) {
        global $post;
        setup_postdata($post);
        
        $title = get_the_title();
        $excerpt = get_the_excerpt();
        $permalink = get_permalink();
        $date = get_the_date('Y-m-d');
        $modified = get_the_modified_date('Y-m-d');
        $author = get_the_author();
        
        $categories = get_the_category();
        $cat_names = array();
        foreach ($categories as $cat) {
            $cat_names[] = $cat->name;
        }
        $section = implode(', ', $cat_names);
        
        $jsonld = array(
            '@context' => 'https://schema.org',
            '@type' => 'Article',
            'headline' => $title,
            'description' => wp_strip_all_tags($excerpt),
            'url' => $permalink,
            'datePublished' => $date . 'T00:00:00+08:00',
            'dateModified' => $modified . 'T00:00:00+08:00',
            'author' => array(
                '@type' => 'Organization',
                'name' => 'AI知识资源网'
            ),
            'publisher' => array(
                '@type' => 'Organization',
                'name' => 'AI知识资源网',
                'logo' => array(
                    '@type' => 'ImageObject',
                    'url' => 'https://skillxm.cn/wp-content/uploads/2024/logo.png'
                )
            ),
            'mainEntityOfPage' => array(
                '@type' => 'WebPage',
                '@id' => $permalink
            ),
            'articleSection' => $section
        );
        
        echo '<script type="application/ld+json">' . wp_json_encode($jsonld, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT) . '</script>' . "\n";
        
        // Also add BreadcrumbList
        $breadcrumb = array(
            '@context' => 'https://schema.org',
            '@type' => 'BreadcrumbList',
            'itemListElement' => array(
                array(
                    '@type' => 'ListItem',
                    'position' => 1,
                    'name' => '首页',
                    'item' => 'https://skillxm.cn'
                ),
                array(
                    '@type' => 'ListItem',
                    'position' => 2,
                    'name' => $section,
                    'item' => get_category_link($categories[0]->term_id) if !empty($categories) else ''
                ),
                array(
                    '@type' => 'ListItem',
                    'position' => 3,
                    'name' => $title
                )
            )
        );
        
        echo '<script type="application/ld+json">' . wp_json_encode($breadcrumb, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT) . '</script>' . "\n";
        
        wp_reset_postdata();
    }
    
    // Homepage WebSite schema
    if (is_front_page() || is_home()) {
        $website = array(
            '@context' => 'https://schema.org',
            '@type' => 'WebSite',
            'name' => 'AI知识资源网',
            'url' => 'https://skillxm.cn',
            'description' => '汇集AI教程、设计软件、影视资源、跨境电商、自媒体运营等高质量免费学习资源，每日更新。',
            'potentialAction' => array(
                '@type' => 'SearchAction',
                'target' => 'https://skillxm.cn/?s={search_term_string}',
                'query-input' => 'required name=search_term_string'
            )
        );
        echo '<script type="application/ld+json">' . wp_json_encode($website, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT) . '</script>' . "\n";
    }
});
'''

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/skillxm.cn/public/wp-content/mu-plugins/seo-jsonld.php', 'w') as f:
    f.write(jsonld_script)
sftp.close()
print("JSON-LD structured data added!", flush=True)

# Make sure mu-plugins dir exists (it should)
stdin, stdout, stderr = ssh.exec_command("ls /www/wwwroot/skillxm.cn/public/wp-content/mu-plugins/ 2>/dev/null || (mkdir -p /www/wwwroot/skillxm.cn/public/wp-content/mu-plugins/ && echo 'created')", timeout=10)
print(stdout.read().decode('utf-8', errors='replace').strip(), flush=True)

# Re-upload if needed
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/skillxm.cn/public/wp-content/mu-plugins/seo-jsonld.php 2>/dev/null", timeout=10)
check = stdout.read().decode('utf-8', errors='replace').strip()
print("mu-plugin check: {}".format(check), flush=True)

ssh.close()
print("\nSEO optimization complete!", flush=True)
