import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22222, username='root', password='Langlang0.', timeout=15)

# Read current custom.css
stdin, stdout, stderr = ssh.exec_command('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css', timeout=10)
css = stdout.read().decode('utf-8', errors='replace')

# v8 patch: pagination + AdSense optimization
v8_patch = '''

/* ============================================
   v8 Mobile Pagination + AdSense Optimization
   2026-04-10
   ============================================ */

/* --- Pagination: compact on mobile --- */
@media screen and (max-width: 768px) {
    .pagination {
        margin: 20px 0 15px 0 !important;
        gap: 4px !important;
        padding: 0 10px !important;
        flex-wrap: wrap !important;
    }
    .pagination .page-numbers {
        padding: 6px 10px !important;
        font-size: 13px !important;
        border-radius: 4px !important;
        min-width: 32px !important;
        text-align: center !important;
    }
}

@media screen and (max-width: 400px) {
    .pagination {
        margin: 15px 0 10px 0 !important;
        gap: 3px !important;
    }
    .pagination .page-numbers {
        padding: 5px 8px !important;
        font-size: 12px !important;
        min-width: 28px !important;
    }
}

/* --- AdSense: ad container styles --- */
.ad-container {
    text-align: center;
    margin: 15px auto;
    max-width: 100%;
    overflow: hidden;
}

.ad-container ins.adsbygoogle {
    background: transparent !important;
}

/* Mobile ad: between cards every 4 items */
.ad-mobile-inline {
    display: none;
}

@media screen and (max-width: 768px) {
    .ad-mobile-inline {
        display: block;
        margin: 10px auto;
        padding: 8px 0;
    }
}

/* Ad below search on mobile */
.ad-mobile-search {
    margin: 12px auto !important;
}

/* Ad in footer area */
.ad-footer {
    margin: 15px auto;
    padding: 10px 0;
    text-align: center;
}

@media screen and (max-width: 768px) {
    .ad-footer {
        margin: 10px auto;
    }
}

/* --- Card list: reduce vertical spacing on mobile --- */
@media screen and (max-width: 768px) {
    .product-list {
        gap: 10px !important;
        padding: 0 8px !important;
    }
    .card {
        margin-bottom: 0 !important;
    }
    .card .card-body {
        padding: 8px !important;
    }
    .thumbnail {
        aspect-ratio: 16 / 10 !important;
        border-radius: 6px !important;
        overflow: hidden !important;
    }
    .card-title {
        font-size: 13px !important;
        line-height: 1.4 !important;
        margin: 6px 0 4px 0 !important;
        display: -webkit-box !important;
        -webkit-line-clamp: 2 !important;
        -webkit-box-orient: vertical !important;
        overflow: hidden !important;
    }
    .bottom-data {
        font-size: 11px !important;
    }
}

@media screen and (max-width: 400px) {
    .product-list {
        gap: 8px !important;
        padding: 0 6px !important;
    }
    .card .card-body {
        padding: 6px !important;
    }
    .card-title {
        font-size: 12px !important;
    }
}

/* --- Reduce overall spacing on mobile --- */
@media screen and (max-width: 768px) {
    .yy-main {
        padding-top: 10px !important;
    }
    .yy-main > .yy-group {
        margin-bottom: 10px !important;
    }
    .yy-group > .container {
        padding-left: 10px !important;
        padding-right: 10px !important;
    }
    .search-section {
        margin-top: 15px !important;
        margin-bottom: 15px !important;
    }
}

/* --- Make single column on very small screens --- */
@media screen and (max-width: 400px) {
    .card {
        width: 100% !important;
    }
}
'''

new_css = css.rstrip() + v8_patch

# Write back
cmd = "cat > /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css << 'CSSEOF'\n" + new_css + "\nCSSEOF"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
err = stderr.read().decode('utf-8', errors='replace')
if err:
    print(f'ERROR: {err[:500]}')
else:
    # Verify braces
    stdin, stdout, stderr = ssh.exec_command(
        "o=$(grep -o '{' /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css | wc -l); c=$(grep -o '}' /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css | wc -l); echo \"open=$o close=$c\"", timeout=10)
    print('Braces:', stdout.read().decode().strip())
    
    # Count lines
    stdin, stdout, stderr = ssh.exec_command(
        "wc -l /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css", timeout=10)
    print('Lines:', stdout.read().decode().strip())

ssh.close()
