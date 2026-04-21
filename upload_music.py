#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import json
import http.client
import base64

# Get existing SHA
result = subprocess.run(['gh', 'api', 'repos/jm6-lang/resource-portal/contents/docs/music/index.md', '--jq', '.sha'], capture_output=True, text=True)
sha = result.stdout.strip()

# Read file
with open('music_index.md', 'rb') as f:
    content = f.read()

# Get token
token = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True).stdout.strip()

# Upload
conn = http.client.HTTPSConnection('api.github.com')
headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/vnd.github+json',
    'User-Agent': 'resource-portal'
}
body = json.dumps({
    'message': 'fix: 修复音乐页面乱码',
    'sha': sha,
    'content': base64.b64encode(content).decode('utf-8')
})
conn.request('PUT', '/repos/jm6-lang/resource-portal/contents/docs/music/index.md', body, headers)
response = conn.getresponse()
print(response.read().decode())
