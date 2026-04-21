import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check full content for copyright/repost warnings
cmd = r"""
for id in 1812 1814 1816 1818 1820 1822; do
  content=$(mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "SELECT post_content FROM wp_posts WHERE ID=$id;" 2>/dev/null)
  title=$(mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "SELECT LEFT(post_title,40) FROM wp_posts WHERE ID=$id;" 2>/dev/null)
  
  # Check for copyright warnings
  if echo "$content" | grep -iq "未经.*许可\|禁止转载\|未经授权\|转载请注明\|严禁转载\|版权所有\|copyright\|转载需.*授权\|谢绝转载\|不得转载"; then
    echo "DELETE $id: $title"
    echo "  Match: $(echo "$content" | grep -io "未经[^<]*\|禁止转载[^<]*\|转载请[^<]*\|版权[^<]*" | head -3)"
  else
    echo "KEEP $id: $title"
  fi
  echo "---"
done
"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode('utf-8', errors='ignore'))
err = stderr.read().decode('utf-8', errors='ignore')
if err:
    print("ERR:", err[:200])

ssh.close()
