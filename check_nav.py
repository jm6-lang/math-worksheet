import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmds = [
    # Check puock_nav_blur value
    "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT option_value FROM wp_options WHERE option_name='puock_nav_blur'\"",
    # Check all puock options
    "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT option_name, option_value FROM wp_options WHERE option_name LIKE 'puock%' LIMIT 20\"",
    # Check yymarket theme options (yy_get options)
    "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT option_name, LEFT(option_value,200) FROM wp_options WHERE option_name LIKE 'yy_%' LIMIT 20\"",
    # Check nav menu locations
    "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT option_value FROM wp_options WHERE option_name='theme_mods_yymarket'\"",
    # Check available menus
    "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT term_id, name FROM wp_terms WHERE term_id IN (SELECT term_id FROM wp_term_taxonomy WHERE taxonomy='nav_menu')\"",
]

for c in cmds:
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    print(f">>> {c[:70]}...")
    print(out[:500] if out else (err[:200] if err else '(empty)'))
    print("---")

ssh.close()
