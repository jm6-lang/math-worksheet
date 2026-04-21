import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# 查询分类
cmd = "mysql -uwpuser -pWpPass2024! wp_skillxm -e \"SELECT t.term_id, t.name FROM wp_terms t JOIN wp_term_taxonomy tt ON t.term_id = tt.term_id WHERE tt.taxonomy='category';\""
stdin, stdout, stderr = ssh.exec_command(cmd)
print('=== 当前分类 ===')
print(stdout.read().decode())

ssh.close()
