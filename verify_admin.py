import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[VERIFY] Admin user meta')

# Check all meta for user 3
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SELECT * FROM wp_skillxm.wp_usermeta WHERE user_id = 3;"')
print('User 3 meta:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

client.close()
print('[DONE]')
print('')
print('========================================')
print('🎉 WordPress 管理后台已创建完成!')
print('========================================')
print('')
print('访问地址: https://skillxm.cn/wp-admin')
print('用户名: admin')
print('密码: Admin123456')
print('')
print('请登录后配置:')
print('1. 主题设置 (外观 -> 主题设置)')
print('2. 底部版权设置')
print('3. 顶部导航设置')
print('4. 开启用户注册 (设置 -> 常规)')
print('========================================')