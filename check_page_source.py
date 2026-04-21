import urllib.request

url = "https://skillxm.cn"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        # Check for login modal
        if 'login-modal' in html:
            print("✓ login-modal HTML FOUND in page source")
            idx = html.find('login-modal')
            print(html[max(0,idx-100):idx+200])
        else:
            print("✗ login-modal NOT in page source")
        
        # Check for login-btn
        if 'login-btn' in html:
            print("\n✓ login-btn FOUND")
            count = html.count('login-btn')
            print(f"  Appears {count} times")
        else:
            print("✗ login-btn NOT in page source")
        
        # Check for jQuery
        if 'jquery' in html.lower():
            print("\n✓ jQuery FOUND")
        else:
            print("\n✗ jQuery NOT found")
        
        # Check for vessel login scripts
        if 'xenice_login' in html:
            print("\n✓ xenice_login scripts FOUND")
        else:
            print("\n✗ xenice_login scripts NOT found")
        
        print(f"\nTotal page size: {len(html)} bytes")
        
except Exception as e:
    print(f"Error: {e}")
