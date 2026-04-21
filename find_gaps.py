# -*- coding: utf-8 -*-
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Get all IDs in range
stdin, stdout, stderr = ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT ID FROM wp_posts WHERE post_type='post' AND post_status='publish' AND ID >= 662 AND ID <= 720 ORDER BY ID;\"")
ids = [int(x) for x in stdout.read().decode().strip().split('\n') if x]

print("Published IDs: {}".format(ids), flush=True)

# Find gaps
all_ids = set(range(662, 711))  # We expected up to 710
published_ids = set(ids)
missing_ids = sorted(all_ids - published_ids)

print("\nMissing IDs: {}".format(missing_ids), flush=True)
print("\nTotal missing: {}".format(len(missing_ids)), flush=True)

ssh.close()
