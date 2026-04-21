import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Create custom CSS file
css = '''/* Custom CSS for GeneratePress - Matching jichuanglm.cn style */
.site-header { background: #fff; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.main-navigation { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.main-nav ul li a { color: #fff; font-weight: 500; }
.hero-section { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 60px 20px; text-align: center; color: #fff; margin-bottom: 30px; }
.search-box { background: #fff; border-radius: 50px; padding: 15px 25px; max-width: 600px; margin: 20px auto; box-shadow: 0 5px 30px rgba(0,0,0,0.2); }
.posts-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; padding: 20px; }
.post-card { background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.08); transition: transform 0.3s, box-shadow 0.3s; }
.post-card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.15); }
.post-card .thumbnail { position: relative; padding-top: 60%; overflow: hidden; }
.post-card .thumbnail img { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; }
.post-card .content { padding: 15px; }
.post-card h2 { font-size: 16px; margin: 0 0 10px; line-height: 1.4; }
.vip-button { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: #fff; padding: 10px 20px; border-radius: 25px; text-decoration: none; font-weight: 500; }
'''

# Write CSS using echo
cmd = f'echo \'{css}\' > /www/wwwroot/skillxm.cn/public/wp-content/themes/generatepress/custom.css'
stdin, out, err = c.exec_command(cmd)
print('Write CSS:', err.read().decode() if err.read() else 'OK')

# Check file
stdin, out, err = c.exec_command('ls -la /www/wwwroot/skillxm.cn/public/wp-content/themes/generatepress/custom.css')
print(out.read().decode())

c.close()
print("Done")