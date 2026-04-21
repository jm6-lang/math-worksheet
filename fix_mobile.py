import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22222, username='root', password='Langlang0.', timeout=15)

# Read current custom.css
stdin, stdout, stderr = ssh.exec_command('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css', timeout=10)
current_css = stdout.read().decode('utf-8', errors='replace')

# Mobile fix patch - append after existing CSS
mobile_patch = '''

/* ============================================
   v7 Mobile Layout Fix - 2026-04-10
   Fix: layout too wide on mobile, card grid,
   slider height, ticker, notices, footer links
   ============================================ */

/* Prevent ALL horizontal overflow */
html, body {
    overflow-x: hidden !important;
    max-width: 100vw !important;
}

/* --- Cards: single column on very small screens --- */
@media screen and (max-width: 400px) {
    .product-list {
        gap: 10px !important;
        padding: 0 8px !important;
    }
    .card {
        width: 100% !important;
        border-radius: 8px !important;
    }
    .card-title {
        font-size: 0.85rem !important;
    }
    .thumbnail {
        aspect-ratio: 16 / 10 !important;
    }
}

/* --- Slider: reduce height on mobile --- */
@media screen and (max-width: 768px) {
    .carousel-item img {
        height: 220px !important;
        max-height: 35vh !important;
    }
    .carousel-caption {
        left: 15px !important;
        right: 15px !important;
        bottom: 15px !important;
        padding: 12px 16px !important;
        border-radius: 10px !important;
        max-width: 100% !important;
    }
    .carousel-caption h2 {
        font-size: 1.1rem !important;
    }
    .carousel-caption p {
        font-size: 0.8rem !important;
        display: none !important;
    }
}

@media screen and (max-width: 400px) {
    .carousel-item img {
        height: 160px !important;
        max-height: 28vh !important;
    }
}

/* --- Orange notice bar: mobile --- */
@media screen and (max-width: 768px) {
    .orange-notice-bar .container > div {
        flex-direction: column !important;
        text-align: center !important;
        gap: 8px !important;
        padding: 10px 12px !important;
    }
    .orange-notice-bar .container > div > div {
        font-size: 12px !important;
    }
    .orange-notice-bar .container > div > a {
        font-size: 11px !important;
    }
}

/* --- News ticker: mobile --- */
@media screen and (max-width: 576px) {
    .news-ticker-box {
        border-radius: 8px !important;
        padding: 0 !important;
        margin: 0 8px !important;
    }
    .ticker-label {
        width: 72px !important;
        font-size: 0.8rem !important;
        padding: 0 5px !important;
    }
    .ticker-wrapper {
        padding: 0 8px !important;
    }
    .ticker-list li {
        font-size: 12px !important;
    }
    .ticker-list li a {
        font-size: 12px !important;
    }
    .news-ticker-section {
        padding: 0 0 12px 0 !important;
    }
}

/* --- Search: mobile --- */
@media screen and (max-width: 480px) {
    .search-input-group {
        flex-direction: column !important;
        border-radius: 12px !important;
        padding: 6px !important;
        gap: 6px !important;
    }
    .search-input-group .input-wrapper {
        padding-left: 12px !important;
    }
    .search-input-group .search-field {
        font-size: 14px !important;
    }
    .search-input-group .search-submit {
        width: 100% !important;
        padding: 10px !important;
        border-radius: 8px !important;
        margin: 0 6px 6px 6px !important;
    }
}

/* --- Footer: mobile --- */
@media screen and (max-width: 576px) {
    .yy-footer {
        padding: 25px 0 !important;
    }
    .footer-disclaimer {
        font-size: 12px !important;
        padding: 0 15px !important;
    }
    .custom-footer-links {
        font-size: 11px !important;
        padding: 15px 10px 0 !important;
    }
    .custom-footer-links a {
        margin: 3px 6px !important;
        display: inline-block !important;
    }
}

/* --- Category page header: mobile --- */
@media screen and (max-width: 768px) {
    .main-show {
        padding: 40px 0 !important;
        margin-bottom: 20px !important;
    }
    .main-show h2 {
        font-size: 1.6rem !important;
    }
    .main-show .desc {
        font-size: 0.9rem !important;
        padding: 0 20px !important;
    }
}

/* --- Language switcher: smaller on mobile --- */
@media screen and (max-width: 768px) {
    #elegant-lang-switcher {
        bottom: 15px !important;
        right: 10px !important;
        padding: 5px 12px !important;
    }
    #elegant-lang-switcher span {
        display: none !important;
    }
    #elegant-lang-switcher img {
        width: 18px !important;
    }
}

/* --- Main container padding on mobile --- */
@media screen and (max-width: 576px) {
    .yy-main .yy-group > .container,
    .yy-main .container {
        padding-left: 10px !important;
        padding-right: 10px !important;
    }
}

/* --- Breadcrumb: mobile --- */
@media screen and (max-width: 576px) {
    .yy-main .breadcrumb {
        font-size: 11px !important;
        padding: 8px 0 !important;
    }
}
'''

# Append the mobile fix
new_css = current_css.rstrip() + mobile_patch

# Write back
cmd = f"cat > /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css << 'CSSEOF'\n{new_css}\nCSSEOF"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
if err:
    print(f'ERROR: {err[:500]}')
else:
    # Verify
    stdin, stdout, stderr = ssh.exec_command('wc -l /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css', timeout=10)
    lines = stdout.read().decode().strip()
    print(f'OK - custom.css now has {lines} lines')
    
    # Check for syntax issues
    stdin, stdout, stderr = ssh.exec_command('grep -c "@media" /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css', timeout=10)
    mcount = stdout.read().decode().strip()
    print(f'Media queries: {mcount}')

ssh.close()
