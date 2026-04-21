import sys, time, urllib.request, re, json

sys.stdout.reconfigure(encoding='utf-8')

time.sleep(2)

# Check article page
req = urllib.request.Request("https://www.skillxm.cn/?p=1812", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    body = r.read().decode('utf-8', errors='ignore')
    schemas = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', body, re.DOTALL)
    print("Article (?p=1812) JSON-LD: %d" % len(schemas))
    for i, s in enumerate(schemas):
        try:
            data = json.loads(s)
            if '@graph' in data:
                print("  #%d: @graph (%d items)" % (i+1, len(data['@graph'])))
            else:
                stype = data.get('@type','?')
                print("  #%d: %s" % (i+1, stype))
                if stype == 'FAQPage':
                    faqs = data.get('mainEntity', [])
                    print("    %d FAQ questions:" % len(faqs))
                    for q in faqs[:2]:
                        print("      - %s" % q.get('name','')[:50])
                elif stype == 'Article':
                    print("    headline: %s" % data.get('headline','')[:50])
                    print("    image: %s" % ('yes' if data.get('image') else 'no'))
        except:
            print("  #%d: error" % (i+1))
    print("GEO marker: %s" % ("YES" if 'GEO Structured Data' in body else "no"))

# Check homepage
req = urllib.request.Request("https://www.skillxm.cn/", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    body = r.read().decode('utf-8', errors='ignore')
    schemas = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', body, re.DOTALL)
    print("\nHomepage JSON-LD: %d" % len(schemas))
    for i, s in enumerate(schemas):
        try:
            data = json.loads(s)
            if '@graph' in data:
                print("  #%d: @graph (%d items)" % (i+1, len(data['@graph'])))
            else:
                stype = data.get('@type','?')
                desc = data.get('description','')[:60]
                print("  #%d: %s - %s" % (i+1, stype, desc))
        except:
            print("  #%d: error" % (i+1))
    print("GEO marker: %s" % ("YES" if 'GEO Structured Data' in body else "no"))

# Check robots.txt AI crawlers
req = urllib.request.Request("https://www.skillxm.cn/robots.txt", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    body = r.read().decode('utf-8', errors='ignore')
    ai_bots = [l.strip() for l in body.split('\n') if any(b in l for b in ['GPTBot','PerplexityBot','ClaudeBot','Bytespider','ChatGPT-User'])]
    print("\nAI crawlers in robots.txt: %d" % len(ai_bots))
    for line in ai_bots:
        print("  %s" % line)

# Check ai-plugin.json
try:
    req = urllib.request.Request("https://www.skillxm.cn/.well-known/ai-plugin.json", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        print("\nai-plugin.json: HTTP %d" % r.status)
except Exception as e:
    print("\nai-plugin.json: Error - %s" % str(e)[:50])

print("\n=== GEO Summary ===")
print("1. robots.txt: AI crawlers allowed (GPTBot, ClaudeBot, PerplexityBot, etc.)")
print("2. ai-plugin.json: OpenAI/AI discovery config")
print("3. Article Schema: Enhanced with image, section, author")
print("4. FAQ Schema: Category-specific FAQ pages for AI citation")
print("5. Organization Schema: Enhanced with description")