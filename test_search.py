import requests, re, time

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'

# Test Wikimedia
keyword = 'online business education'
url = f'https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(keyword)}&srnamespace=6&srlimit=5&format=json'
r = requests.get(url, timeout=10, headers={'User-Agent': USER_AGENT})
data = r.json()
results = data.get('query', {}).get('search', [])
print(f'Wikimedia results for "{keyword}": {len(results)}')
for item in results[:3]:
    title = item['title'].replace('File:', '')
    img_url = f'https://commons.wikimedia.org/wiki/Special:FilePath/{requests.utils.quote(title)}?width=800'
    try:
        h = requests.head(img_url, timeout=8, headers={'User-Agent': USER_AGENT})
        ct = h.headers.get('Content-Type', '')
        print(f'  {title[:40]}: {h.status_code} {ct[:30]}')
    except Exception as e:
        print(f'  Error: {e}')

# Test Bing image search
print('\nBing image search:')
url2 = f'https://www.bing.com/images/search?q={requests.utils.quote("AI technology free image site:wikimedia.org")}'
r2 = requests.get(url2, timeout=10, headers={
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US,en;q=0.9',
})
matches = re.findall(r'"murl":"([^"]+)"', r2.text)
print(f'Found {len(matches)} image URLs')
for m in matches[:3]:
    print(f'  {m[:100]}')
