import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Add sitemap link + SEO footer via mu-plugin
footer_code = '''<?php
// Add sitemap and SEO links to footer
add_action('wp_footer', function() {
    echo '<div style="text-align:center;padding:20px 0;font-size:13px;color:#999;background:#f5f5f5;border-top:1px solid #eee;">';
    echo '<a href="https://skillxm.cn/sitemap_index.xml" style="color:#666;margin:0 10px;">站点地图</a>';
    echo '<a href="https://skillxm.cn/robots.txt" style="color:#666;margin:0 10px;">Robots</a>';
    echo '&copy; ' . date('Y') . ' AI知识资源网 - 汇集AI教程/设计软件/影视资源/跨境电商/自媒体运营等高质量免费学习资源';
    echo '</div>';
});

// Add canonical and alternate links
add_action('wp_head', function() {
    // Ensure canonical URL is set
    if (is_singular()) {
        echo '<link rel="canonical" href="' . get_permalink() . '" />' . "\\n";
    }
    
    // Add preconnect for performance
    echo '<link rel="dns-prefetch" href="//www.baidu.com" />' . "\\n";
});
'''

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/skillxm.cn/public/wp-content/mu-plugins/seo-footer.php', 'w') as f:
    f.write(footer_code)
sftp.close()

# Verify both mu-plugins exist
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/skillxm.cn/public/wp-content/mu-plugins/")
print(stdout.read().decode('utf-8', errors='replace'))

# Verify footer shows
stdin, stdout, stderr = ssh.exec_command("curl -s https://skillxm.cn/ 2>/dev/null | grep -i 'sitemap' | head -3")
out = stdout.read().decode('utf-8', errors='replace').strip()
print("Footer sitemap link: " + (out if out else "checking..."))

# Also check an article page
stdin, stdout, stderr = ssh.exec_command("curl -s https://skillxm.cn/?p=800 2>/dev/null | grep -i '站点地图\\|sitemap\\|canonical' | head -5")
out = stdout.read().decode('utf-8', errors='replace').strip()
print("Article SEO elements: " + (out if out else "not found"))

ssh.close()
print("Done!")
