import requests
import re

# Test Unsplash source API (free to use, no key needed for source URLs)
test_urls = [
    "https://source.unsplash.com/800x600/?ai,technology",
    "https://source.unsplash.com/800x600/?online,course",
    "https://source.unsplash.com/800x600/?business,money",
]

for url in test_urls:
    r = requests.head(url, timeout=10, allow_redirects=True)
    print(f"{url} -> {r.status_code} | {r.headers.get('Content-Type','?')}")
