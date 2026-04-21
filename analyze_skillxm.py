import re

with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\skillxm_home.html', encoding='utf-8', errors='ignore') as f:
    html = f.read()

print('HTML size:', len(html))

# Extract article classes
articles = re.findall(r'<article[^>]*class="([^"]+)"', html)
print('\nArticle classes:', set(articles))

# Find card/post related classes
card_classes = re.findall(r'class="([^"]*(?:post|article|card|item|entry|list)[^"]*)"', html, re.I)
print('\nCard-related classes:', set(card_classes))

# Nav classes
nav_classes = re.findall(r'class="([^"]*(?:nav|menu|header)[^"]*)"', html, re.I)
print('\nNav classes:', set(nav_classes))

# Look for main content area classes
main_classes = re.findall(r'class="([^"]*(?:content|main|container|site-content)[^"]*)"', html, re.I)
print('\nMain/content classes:', set(main_classes))

# First article block
article_html = re.findall(r'<article[^>]*>.*?</article>', html, re.DOTALL)
if article_html:
    print('\nFirst article (first 500 chars):')
    print(article_html[0][:500])
