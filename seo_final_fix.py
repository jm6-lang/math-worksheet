import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Fix 1: Switch to correct nginx config
cmds = [
    # Remove old symlink, create new one
    "rm -f /etc/nginx/sites-enabled/resource_site.conf",
    "ln -sf /etc/nginx/sites-available/skillxm.cn.conf /etc/nginx/sites-enabled/skillxm.cn.conf",
    
    # Verify symlink
    "ls -la /etc/nginx/sites-enabled/",
    
    # Test nginx config
    "nginx -t 2>&1",
    
    # Reload nginx
    "systemctl reload nginx 2>&1",
    
    # Verify sitemap now works
    "curl -s https://skillxm.cn/sitemap_index.xml -o /dev/null -w '%{http_code}' 2>/dev/null",
    "curl -s https://skillxm.cn/post-sitemap.xml -o /dev/null -w '%{http_code}' 2>/dev/null",
    "curl -s https://skillxm.cn/robots.txt 2>/dev/null | head -8",
]
for c in cmds:
    print(">> " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out:
        print(out, flush=True)
    print(flush=True)

# Fix 2: Upload JSON-LD mu-plugin
jsonld = '''<?php
// SEO: JSON-LD structured data for all posts
add_action('wp_head', function() {
    if (is_singular('post')) {
        global $post;
        $title = get_the_title();
        $permalink = get_permalink();
        $date = get_the_date('c');
        $modified = get_the_modified_date('c');
        $categories = get_the_category();
        $section = !empty($categories) ? $categories[0]->name : '';
        
        $schema = array(
            '@context' => 'https://schema.org',
            '@type' => 'Article',
            'headline' => $title,
            'url' => $permalink,
            'datePublished' => $date,
            'dateModified' => $modified,
            'author' => array('@type' => 'Organization', 'name' => 'AI\u77e5\u8bc6\u8d44\u6e90\u7f51'),
            'publisher' => array(
                '@type' => 'Organization',
                'name' => 'AI\u77e5\u8bc6\u8d44\u6e90\u7f51',
            ),
            'mainEntityOfPage' => array('@type' => 'WebPage', '@id' => $permalink),
            'articleSection' => $section,
        );
        
        echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_UNICODE) . '</script>' . "\\n";
        
        // Breadcrumb
        $crumb = array(
            '@context' => 'https://schema.org',
            '@type' => 'BreadcrumbList',
            'itemListElement' => array(
                array('@type' => 'ListItem', 'position' => 1, 'name' => '\u9996\u9875', 'item' => 'https://skillxm.cn'),
                array('@type' => 'ListItem', 'position' => 2, 'name' => $section),
                array('@type' => 'ListItem', 'position' => 3, 'name' => $title),
            ),
        );
        echo '<script type="application/ld+json">' . wp_json_encode($crumb, JSON_UNESCAPED_UNICODE) . '</script>' . "\\n";
    }
    
    if (is_front_page() || is_home()) {
        $site = array(
            '@context' => 'https://schema.org',
            '@type' => 'WebSite',
            'name' => 'AI\u77e5\u8bc6\u8d44\u6e90\u7f51',
            'url' => 'https://skillxm.cn',
            'description' => '\u6c47\u96c6AI\u6559\u7a0b\u3001\u8bbe\u8ba1\u8f6f\u4ef6\u3001\u5f71\u89c6\u8d44\u6e90\u3001\u8de8\u5883\u7535\u5546\u3001\u81ea\u5a92\u4f53\u8fd0\u8425\u7b49\u9ad8\u8d28\u91cf\u514d\u8d39\u5b66\u4e60\u8d44\u6e90\uff0c\u6bcf\u65e5\u66f4\u65b0\u3002',
            'potentialAction' => array(
                '@type' => 'SearchAction',
                'target' => 'https://skillxm.cn/?s={search_term_string}',
                'query-input' => 'required name=search_term_string',
            ),
        );
        echo '<script type="application/ld+json">' . wp_json_encode($site, JSON_UNESCAPED_UNICODE) . '</script>' . "\\n";
    }
});
'''

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/skillxm.cn/public/wp-content/mu-plugins/seo-jsonld.php', 'w') as f:
    f.write(jsonld)
sftp.close()
print("JSON-LD mu-plugin installed!", flush=True)

ssh.close()
