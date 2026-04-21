import sys, time
sys.path.insert(0, r'E:\Qclaw\resources\openclaw\config\skills\browser-cdp\scripts')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from browser_launcher import BrowserLauncher, BrowserNeedsCDPError

launcher = BrowserLauncher()
try:
    cdp_url = launcher.launch(browser='chrome')
    print("CDP URL:", cdp_url)
except BrowserNeedsCDPError as e:
    print(f"NEED_CDP:{e}")
    sys.exit(1)
except Exception as e:
    print(f"LAUNCH_ERR:{e}")
    sys.exit(1)

from cdp_client import CDPClient
client = CDPClient(cdp_url)
client.connect()

tabs = client.list_tabs()
target = 'feishu.cn/docx/JnHDdKK3KoVyuQxQE1yc860znd0'
tab = None
for t in tabs:
    if target in t.get('url', ''):
        tab = t
        break

if tab:
    client.attach(tab['id'])
    print("Reused tab:", tab['id'])
else:
    tab = client.create_tab('https://kcnpawl2dqlx.feishu.cn/docx/JnHDdKK3KoVyuQxQE1yc860znd0')
    client.attach(tab['id'])
    print("New tab:", tab['id'])

from browser_actions import BrowserActions
from page_snapshot import PageSnapshot

actions = BrowserActions(client, PageSnapshot(client))
actions.wait_for_load()
time.sleep(5)

current_url = actions.get_url()
print("Current URL:", current_url)

# Check if login is needed
if 'login' in current_url.lower() or 'passport' in current_url.lower() or 'feishu.cn/docx' not in current_url:
    actions.screenshot(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\feishu_login.png')
    print("NEED_LOGIN")
else:
    # Get page content
    tree = PageSnapshot(client).accessibility_tree()
    with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\feishu_tree.txt', 'w', encoding='utf-8') as f:
        f.write(tree)
    print("Tree saved, length:", len(tree))
    actions.screenshot(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\feishu_page.png')
    print("Screenshot saved")
    # Also extract via JS
    text = actions.evaluate("document.querySelector('.doc-content, .suite-doc-content, [role=document], .render-unit-wrapper, .docx-container')?.innerText || document.body?.innerText || ''")
    with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\feishu_text.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Text saved, length:", len(text))
