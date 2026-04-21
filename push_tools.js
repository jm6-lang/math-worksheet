const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const https = require('https');

const REPO = 'jm6-lang/resource-portal';
const TOKEN = execSync('gh auth token', { encoding: 'utf-8' }).trim();
const TOOLS_DIR = "C:\\Users\\Administrator\\.qclaw\\workspace-agent-3bb7b585\\resource-portal\\docs\\tools";

function getSHA(destPath) {
  try {
    return execSync(`gh api repos/${REPO}/contents/${destPath} --jq .sha`, { encoding: 'utf-8', timeout: 15000 }).trim();
  } catch (e) {
    return ''; // 文件不存在，返回空 SHA
  }
}

async function uploadFile(filePath, destPath) {
  const sha = getSHA(destPath);
  const content = fs.readFileSync(filePath);
  const b64 = content.toString('base64');
  const body = JSON.stringify({
    message: `feat(tools): 新增 ${path.basename(filePath)}`,
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
          console.error(`✗ ${destPath}: ${data.slice(0, 100)}`);
          resolve(); // 不阻塞，继续
        }
      });
    });
    req.on('error', e => { console.error(`Error: ${e.message}`); resolve(); });
    req.write(bodyBytes);
    req.end();
  });
}

(async () => {
  // 先上传 index.md
  console.log('上传 index.md...');
  await uploadFile(
    path.join(TOOLS_DIR, 'index.md'),
    'docs/tools/index.md'
  );

  // 上传 post_194.md 到 post_224.md
  console.log('\n上传 post 文件...');
  for (let i = 194; i <= 224; i++) {
    const fileName = `post_${i.toString().padStart(3, '0')}.md`;
    await uploadFile(
      path.join(TOOLS_DIR, fileName),
      `docs/tools/${fileName}`
    );
  }

  console.log('\n全部上传完成!');
})();