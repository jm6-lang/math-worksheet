const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const https = require('https');

const REPO = 'jm6-lang/resource-portal';
const TOKEN = execSync('gh auth token', { encoding: 'utf-8' }).trim();

function getSHA(destPath) {
  try {
    return execSync(`gh api repos/${REPO}/contents/${destPath} --jq .sha`, { encoding: 'utf-8', timeout: 15000 }).trim();
  } catch (e) {
    return '';
  }
}

async function uploadFile(filePath, destPath, message) {
  const sha = getSHA(destPath);
  const content = fs.readFileSync(filePath);
  const b64 = content.toString('base64');
  const body = JSON.stringify({
    message,
    sha,
    content: b64
  });
  const bodyBytes = Buffer.from(body, 'utf-8');

  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'api.github.com',
      path: `/repos/${REPO}/contents/${destPath}`,
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${TOKEN}`,
        'User-Agent': 'resource-portal',
        'Content-Type': 'application/json',
        'Content-Length': bodyBytes.length,
        'Accept': 'application/vnd.github+json'
      }
    }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        if (res.statusCode === 200 || res.statusCode === 201) {
          console.log(`✓ ${destPath}`);
          resolve();
        } else {
          console.error(`✗ ${destPath}: ${res.statusCode} - ${data.substring(0,100)}`);
          resolve();
        }
      });
    });
    req.on('error', e => { console.error(`Error: ${e.message}`); resolve(); });
    req.write(bodyBytes);
    req.end();
  });
}

(async () => {
  const files = [
    ['docs/.vitepress/config.ts', 'feat: 更新分类名称'],
    ['docs/tools/index.md', 'fix: 移除生财有术'],
    ['docs/tools/post_069.md', 'fix: 移除生财有术'],
    ['docs/tools/post_152.md', 'fix: 移除生财有术'],
  ];

  for (const [destPath, msg] of files) {
    const fullPath = path.join(__dirname, 'resource-portal', destPath);
    await uploadFile(fullPath, destPath, msg);
    // Small delay between uploads
    await new Promise(r => setTimeout(r, 200));
  }

  console.log('\n全部上传完成!');
})();