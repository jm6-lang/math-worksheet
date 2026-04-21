import paramiko
import os

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Set site title and description
print("=== Setting site title ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp option update blogname "技能项目网" --allow-root 2>&1')
print(out.read().decode())

print("\n=== Setting site description ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp option update blogdescription "副业项目、创业项目、网创资源一站式平台" --allow-root 2>&1')
print(out.read().decode())

# Set permalink structure
print("\n=== Setting permalinks ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp rewrite structure "/%postname%/" --allow-root 2>&1')
print(out.read().decode())

print("\n=== Flush rewrite rules ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp rewrite flush --allow-root 2>&1')
print(out.read().decode())

c.close()
print("Done!")