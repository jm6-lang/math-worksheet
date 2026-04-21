import paramiko, re

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Homepage footer HTML')

# Get homepage HTML
stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ 2>&1')
html = stdout.read().decode('utf-8', errors='ignore')

# Find footer section
footer_start = html.find('<footer')
if footer_start >= 0:
    footer_html = html[footer_start:footer_start+2000]
    with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\footer_html.txt', 'w', encoding='utf-8') as out:
        out.write(footer_html)
    print(f'Footer found at position {footer_start}')
    # Show first 500 chars
    print('Footer preview:', footer_html[:500])
else:
    print('No footer tag found')
    # Check for container-footer
    cf = html.find('container-footer')
    if cf >= 0:
        print(f'container-footer found at {cf}')
        with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\footer_html.txt', 'w', encoding='utf-8') as out:
            out.write(html[cf-100:cf+1000])

# Check all_footer widget
widget = html.find('all_footer')
print(f'all_footer widget: {widget}')

# Check for sidebar widgets
sidebar = html.find('sidebar')
print(f'sidebar found: {sidebar}')

client.close()