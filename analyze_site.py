import urllib.request, ssl, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://doc.869hr.uk/'

# Get full response with headers
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})

resp = urllib.request.urlopen(req, context=ctx, timeout=15)

print('=== Response Headers ===')
for k, v in resp.getheaders():
    print(f'{k}: {v}')

html = resp.read().decode('utf-8', errors='replace')

print('\n=== HTML Head (first 3000 chars) ===')
print(html[:3000])

# Check for common CMS/framework signatures
print('\n=== Tech Detection ===')

# WordPress
if 'wp-content' in html or 'wordpress' in html.lower():
    print('WordPress detected')

# Hexo
if 'hexo' in html.lower():
    print('Hexo detected')

# Hugo
if 'hugo' in html.lower():
    print('Hugo detected')

# Docsify
if 'docsify' in html.lower():
    print('Docsify detected')

# VuePress
if 'vuepress' in html.lower():
    print('VuePress detected')

# VitePress
if 'vitepress' in html.lower() or 'vite' in html.lower():
    print('VitePress/Vite detected')

# Check generator meta tag
gen_match = re.search(r'<meta[^>]+generator[^>]+content=["\']([^"\']+)["\']', html, re.I)
if gen_match:
    print(f'Generator: {gen_match.group(1)}')

# Check for theme
theme_match = re.search(r'theme["\']?\s*[:=]\s*["\']([^"\']+)["\']', html, re.I)
if theme_match:
    print(f'Theme: {theme_match.group(1)}')

# Check for static site generator files
if '/assets/' in html and '.js' in html:
    print('Likely a static site generator')
