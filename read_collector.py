import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Read the full collector.py to understand image collection
stdin, stdout, stderr = ssh.exec_command(
    "cat /www/wwwroot/resource_site/auto_collect/collector.py",
    timeout=15
)
content = stdout.read().decode('utf-8', errors='replace')

# Save to local for analysis
with open('C:\\Users\\Administrator\\.qclaw\\workspace-agent-3bb7b585\\collector_full.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"File size: {len(content)} bytes")

# Check for image search functions
import re
img_funcs = re.findall(r'def\s+\w*img\w*\([^)]*\):', content)
print(f"\nImage-related functions: {img_funcs}")

# Check for search image functionality
if 'search' in content.lower() and 'image' in content.lower():
    print("\nFound image search references")

ssh.close()