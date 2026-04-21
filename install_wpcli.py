import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Install wp-cli
print("=== Install WP-CLI ===")
stdin, out, err = c.exec_command('curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar 2>&1 | tail -3')
print(out.read().decode()[:200])

stdin, out, err = c.exec_command('chmod +x wp-cli.phar && mv wp-cli.phar /usr/local/bin/wp')
print(out.read().decode())

# Test wp
print("\n=== Test WP-CLI ===")
stdin, out, err = c.exec_command('wp --info --allow-root')
print(out.read().decode()[:300])

c.close()