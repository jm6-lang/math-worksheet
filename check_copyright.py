import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

cmd = """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e "SELECT ID, LEFT(post_title,40) as title, LEFT(post_content,200) as content FROM wp_posts WHERE ID IN (1812,1814,1816,1818,1820,1822) AND post_status='publish';" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
