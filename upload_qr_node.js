const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const https = require('https');
const REPO = 'jm6-lang/resource-portal';
const DEST = 'docs/public/data-card-qr.png';
const SRC = 'C:\\Users\\Administrator\\Desktop\\新建文件夹\\9951d3ac2a60b345235b026e181af1c.jpg';

// Read image and encode
const imgBuf = fs.readFileSync(SRC);
const b64 = imgBuf.toString('base64');
console.log(`Image: ${imgBuf.length} bytes, base64: ${b64.length} chars`);

// Get SHA via gh
function gh(args) {
  return execSync(`gh ${args}`, { encoding: 'utf-8', timeout: 15000 });
}

const shaJson = gh(`api repos/${REPO}/contents/${DEST} --jq .sha`).trim();
console.log(`SHA: ${shaJson}`);

// Build JSON body
const body = JSON.stringify({
  message: 'chore: 替换大流量卡二维码图片',
  sha: shaJson,
  content: b64
});

const bodyBytes = Buffer.from(body, 'utf-8');
console.log(`Body: ${bodyBytes.length} bytes`);

// Get gh token
const token = execSync('gh auth token', { encoding: 'utf-8' }).trim();

// HTTP request
const options = {
  hostname: 'api.github.com',
  path: `/repos/${REPO}/contents/${DEST}`,
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${token}`,
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
      console.log('FAIL:', data.slice(0, 300));
    }
  });
});

req.on('error', e => console.error('Network error:', e.message));
req.write(bodyBytes);
req.end();
