import paramiko
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Add copyright filter to collector
filter_patterns = [
    r"未经.*许可.*禁止转载",
    r"未经作者许可.*禁止转载",
    r"未经授权.*转载",
    r"谢绝转载",
    r"严禁转载",
    r"版权所有",
    r"转载需.*授权",
    r"请点击.*联系",
]

# Read current collector
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/auto_collect/collector.py', 'r') as f:
    content = f.read().decode('utf-8')
sftp.close()

# Check if copyright filter already exists
if "COPYRIGHT_PATTERNS" in content:
    print("Copyright filter already exists")
else:
    # Add copyright filter after the is_relevant function
    filter_code = '''
COPYRIGHT_PATTERNS = [
    r"未经.*许可.*禁止转载",
    r"未经作者许可.*禁止转载", 
    r"未经授权.*转载",
    r"谢绝转载",
    r"严禁转载",
    r"版权所有",
    r"转载需.*授权",
]

def has_copyright_restriction(text):
    """Check if content has copyright/restriction notices"""
    if not text:
        return False
    for pattern in COPYRIGHT_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False
'''
    
    # Find the is_relevant function and add after it
    if "def is_relevant(title" in content:
        # Add after is_relevant function
        parts = content.split("def is_relevant(title")
        if len(parts) == 2:
            content = parts[0] + "def is_relevant(title" + parts[1]
            # Find end of is_relevant and insert after
            idx = content.find("def download_image(")
            if idx > 0:
                content = content[:idx] + filter_code + "\n" + content[idx:]
                
                sftp = ssh.open_sftp()
                with sftp.open('/www/wwwroot/resource_site/auto_collect/collector.py', 'w') as f:
                    f.write(content)
                sftp.close()
                print("Added copyright filter")
            else:
                print("Could not find download_image function")
        else:
            print("Split failed")
    else:
        print("is_relevant function not found")

# Now also update the filtering in main() - add copyright check
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'has_copyright' /www/wwwroot/resource_site/auto_collect/collector.py 2>/dev/null || echo 'NOT_FOUND'",
    timeout=10
)
result = stdout.read().decode('utf-8', errors='ignore').strip()

if result == "NOT_FOUND" or "has_copyright" not in result:
    # Need to add the check in the main loop
    cmd = '''sed -i 's/if not is_relevant(title, summary):/if not is_relevant(title, summary) or has_copyright_restriction(summary):/' /www/wwwroot/resource_site/auto_collect/collector.py'''
    ssh.exec_command(cmd, timeout=10)
    print("Added copyright check to main loop")
else:
    print("Copyright check already in place")

# Verify
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'copyright' /www/wwwroot/resource_site/auto_collect/collector.py | head -5",
    timeout=10
)
print("\nFilter status:")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
