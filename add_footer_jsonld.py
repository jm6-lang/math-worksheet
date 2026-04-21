import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Add sitemap link to footer.php before </body> tag
sed_cmd = "sed -i 's|<?php wp_footer(); ?>|<div style=\"text-align:center;padding:10px;background:#222;color:#888;font-size:12px;\"><a href=\"https://skillxm.cn/sitemap_index.xml\" style=\"color:#aaa;margin:0 8px;\">Sitemap</a><a href=\"https://skillxm.cn/robots.txt\" style=\"color:#aaa;margin:0 8px;\">Robots</a></div>\\n<?php wp_footer(); ?>|' /www/wwwroot/resource_site/wp-content/themes/yymarket/footer.php"

stdin, stdout, stderr = ssh.exec_command(sed_cmd)
err = stderr.read().decode('utf-8', errors='replace').strip()
if err: print("ERR: " + err)

# Verify
stdin, stdout, stderr = ssh.exec_command("grep -n 'sitemap' /www/wwwroot/resource_site/wp-content/themes/yymarket/footer.php")
print("Footer grep: " + stdout.read().decode('utf-8', errors='replace').strip())

# Also add JSON-LD mu-plugin to resource_site
jsonld = '''<?php
// JSON-LD structured data
add_action('wp_head', function() {
    if (is_singular('post')) {
        global $post;
        $schema = array(
            '@context' => 'https://schema.org',
            '@type' => 'Article',
            'headline' => get_the_title(),
            'url' => get_permalink(),
            'datePublished' => get_the_date('c'),
            'dateModified' => get_the_modified_date('c'),
            'author' => array('@type' => 'Organization', 'name' => get_bloginfo('name')),
            'mainEntityOfPage' => array('@type' => 'WebPage', '@id' => get_permalink()),
        );
        echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_UNICODE) . '</script>' . "\\n";
    }
});
'''

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/wp-content/mu-plugins/seo-jsonld.php', 'w') as f:
    f.write(jsonld)
sftp.close()

import time
time.sleep(2)

# Test
stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?v=10' 2>/dev/null | grep -c 'sitemap_index'")
print("Footer sitemap link: " + stdout.read().decode().strip())

stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/sitemap_index.xml' 2>/dev/null | head -10")
print("Sitemap:\n" + stdout.read().decode('utf-8', errors='replace').strip())

# Test JSON-LD on article
stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?p=800' 2>/dev/null | grep -c 'ld+json'")
print("JSON-LD on article: " + stdout.read().decode().strip())

ssh.close()
print("Done!")
