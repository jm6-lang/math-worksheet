import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Download Puock theme
print("=== Download Puock theme ===")
stdin, out, err = c.exec_command('cd /tmp && rm -f puock.zip && curl -L -o puock.zip "https://codeload.github.com/LyLme/puock-wordpress-theme/zip/refs/heads/master" 2>&1 | tail -5')
print(out.read().decode())

# Check file
print("\n=== Check zip file ===")
stdin, out, err = c.exec_command('ls -la /tmp/puock.zip')
print(out.read().decode())

c.close()