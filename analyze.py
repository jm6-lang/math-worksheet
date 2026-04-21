import re

with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\daba\assets\style.css', encoding='utf-8', errors='ignore') as f:
    css = f.read()

with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\daba\assets\theme.js', encoding='utf-8', errors='ignore') as f:
    theme = f.read()

print('CSS size:', len(css))
print('Theme size:', len(theme))

# Find custom VP classes
vp_classes = set(re.findall(r'\.(VP[\w-]+)', css))
print('VP classes:', sorted(vp_classes)[:30])

# Look for custom classes (not in default VitePress)
# Extract background gradient styles
grads = re.findall(r'background:linear-gradient\([^;]+\)', css)
print('\nGradients:', grads[:5])

# Hero background
hero_bg = re.findall(r'\.VPHomeHero[^{]*\{[^}]+\}', css)
print('\nHero styles:', hero_bg[:3])

# Color scheme - find the primary color
primary = re.findall(r'#3451b2[^"]*', css)[:5]
print('\nPrimary blue:', primary)

# Find the homepage markdown that drives the layout
# The site is VitePress, so the config is in .vitepress/config.js or similar
# Let's check if there are any JSON configs in the index
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\daba\index.html', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Extract script tags content
scripts = re.findall(r'<script type="module"[^>]*src="([^"]+)"', html)
print('\nScript tags:', scripts)

# Look for theme config
config_refs = re.findall(r'/assets/index\.md[^"\']*', html)
print('Index MD:', config_refs)

# Check if there's a data file
data_refs = re.findall(r'"(/\w+\.\w+)"', html)
print('Asset refs:', data_refs[:20])
