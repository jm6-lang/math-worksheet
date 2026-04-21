const { execSync } = require('child_process');
const fs = require('fs');
const https = require('https');

const REPO = 'jm6-lang/resource-portal';
const TOKEN = execSync('gh auth token', { encoding: 'utf-8' }).trim();
const DEST = 'docs/index.md';

function gh(args) {
  return execSync(`gh ${args}`, { encoding: 'utf-8', timeout: 15000 });
}

const sha = gh(`api repos/${REPO}/contents/${DEST} --jq .sha`).trim();
const content = fs.readFileSync(
  'C:\\Users\\Administrator\\.qclaw\\workspace-agent-3bb7b585\\resource-portal\\docs\\index.md',
  'utf-8'
);
const b64 = Buffer.from(content, 'utf-8').toString('base64');
const body = JSON.stringify({
  message: 'feat: 首页添加打赏收款区（微信+支付宝）',
  sha,
  content: b64
});
const bodyBytes = Buffer.from(body, 'utf-8');

const req = https.request({
  hostname: 'api.github.com',
  path: `/repos/${REPO}/contents/${DEST}`,
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${TOKEN}`,
    'User-Agent': 'resource-portal-uploader',
    'Content-Type': 'application/json',
    'Content-Length': bodyBytes.length,
    'Accept': 'application/vnd.github+json'
  }
}, (res) => {
  let data = '';
  res.on('data', c => data += c);
  res.on('end', () => {
    console.log(`Status: ${res.statusCode}`);
    if (res.statusCode === 200 || res.statusCode === 201) {
      const resp = JSON.parse(data);
      console.log('SUCCESS:', resp.content.html_url);
    } else {
      console.log('FAIL:', data.slice(0, 300));
    }
  });
});
req.on('error', e => console.error('Error:', e.message));
req.write(bodyBytes);
req.end();
