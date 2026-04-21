const { execSync } = require('child_process');
const fs = require('fs');
const https = require('https');

const REPO = 'jm6-lang/resource-portal';
const DEST = 'docs/exclusive/index.md';
const TOKEN = execSync('gh auth token', { encoding: 'utf-8' }).trim();

// Get SHA
function gh(args) {
  return execSync(`gh ${args}`, { encoding: 'utf-8', timeout: 15000 });
}
const sha = gh(`api repos/${REPO}/contents/${DEST} --jq .sha`).trim();
console.log('SHA:', sha);

// Read local content
const content = fs.readFileSync(
  'C:\\Users\\Administrator\\.qclaw\\workspace-agent-3bb7b585\\resource-portal\\docs\\exclusive\\index.md',
  'utf-8'
);
const b64 = Buffer.from(content, 'utf-8').toString('base64');

const body = JSON.stringify({
  message: 'feat: 独家资源首页改版为大卡片分类布局，支持后期扩展',
  sha,
  content: b64
});
const bodyBytes = Buffer.from(body, 'utf-8');

const options = {
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
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    console.log(`Status: ${res.statusCode}`);
    if (res.statusCode === 200 || res.statusCode === 201) {
      const resp = JSON.parse(data);
      console.log('SUCCESS:', resp.content.html_url);
    } else {
      console.log('FAIL:', data.slice(0, 200));
    }
  });
});
req.on('error', e => console.error('Error:', e.message));
req.write(bodyBytes);
req.end();
