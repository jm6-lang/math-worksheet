const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const https = require('https');

const REPO = 'jm6-lang/resource-portal';
const TOKEN = execSync('gh auth token', { encoding: 'utf-8' }).trim();
const MOVIES_DIR = "C:\\Users\\Administrator\\.qclaw\\workspace-agent-3bb7b585\\resource-portal\\docs\\movies";

function getSHA(destPath) {
  try {
    return execSync(`gh api repos/${REPO}/contents/${destPath} --jq .sha`, { encoding: 'utf-8', timeout: 15000 }).trim();
  } catch (e) {
    return '';
  }
}

async function uploadFile(filePath, destPath) {
  const sha = getSHA(destPath);
  const content = fs.readFileSync(filePath);
  const b64 = content.toString('base64');
  const body = JSON.stringify({
    message: `feat(music): 音乐资源迁移到影视聚集区`,
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
          console.error(`✗ ${destPath}: ${res.statusCode}`);
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
  // Upload index.md first
  console.log('上传 movies/index.md...');
  await uploadFile(
    path.join(MOVIES_DIR, 'index.md'),
    'docs/movies/index.md'
  );

  // Upload music post files (post_129 to post_144)
  console.log('\n上传音乐资源 post 文件...');
  for (let i = 129; i <= 144; i++) {
    const fileName = `post_${i.toString().padStart(3, '0')}.md`;
    await uploadFile(
      path.join(MOVIES_DIR, fileName),
      `docs/movies/${fileName}`
    );
  }

  console.log('\n全部上传完成!');
})();