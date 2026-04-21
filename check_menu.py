import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Get the nav/menu HTML section
cmds = [
    # Get menu HTML
    "curl -sk 'https://skillxm.cn/' 2>/dev/null | grep -A5 -B2 'nav\\|menu\\|header' | head -80",
    # Check theme customizer options
    "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT option_name FROM wp_options WHERE option_name LIKE '%nav%' OR option_name LIKE '%menu%' OR option_name LIKE '%header%' LIMIT 20\"",
    # Check if there are any widget areas with nav
    "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT option_name, LEFT(option_value,300) FROM wp_options WHERE option_name LIKE '%theme_mods_yymarket%' LIMIT 1\"",
]

for c in cmds:
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    print(f">>> {c[:80]}")
    print(out[:1000] if out else (err[:200] if err else '(empty)'))
    print("---")

ssh.close()
