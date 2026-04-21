import requests, re

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
results = {}

sources = {
    "LoremFlickr": "https://loremflickr.com/800/600/business?random=1",
    "LoremFlickr2": "https://loremflickr.com/800/600/technology?random=2",
    "HTTPBin": "https://httpbin.org/image/jpeg",
    "PlaceKitten": "https://placekitten.com/800/600",
    "PlaceDog": "https://place.dog/800/600.jpg",
    "UnsplashDirect": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&q=80",
    "Bing_thumb": "https://th.bing.com/th/id/OIP.test.jpg",
}

for name, url in sources.items():
    try:
        r = requests.head(url, timeout=8, allow_redirects=True)
        ct = r.headers.get('Content-Type', '')
        loc = r.headers.get('Location', '')[:80]
        results[name] = f"{r.status_code} | {ct[:30]} | {loc}"
    except Exception as e:
        results[name] = f"ERROR: {e}"

for k, v in results.items():
    print(f"{k}: {v}")
