const { execSync } = require('child_process');
const fs = require('fs');
const https = require('https');

const REPO = 'jm6-lang/resource-portal';
const TOKEN = execSync('gh auth token', { encoding: 'utf-8' }).trim();

function gh(args) {
  return execSync(`gh ${args}`, { encoding: 'utf-8', timeout: 15000 });
}

function uploadFile(localPath, destPath) {
  // Check if file exists first
  let sha = '';
  try {
    sha = gh(`api repos/${REPO}/contents/${destPath} --jq .sha`).trim();
  } catch (e) {
    // File doesn't exist yet, sha is empty
  }

  const imgBuf = fs.readFileSync(localPath);
  const b64 = imgBuf.toString('base64');
  console.log(`Uploading ${localPath} (${imgBuf.length} bytes)...`);

  const body = JSON.stringify({ message: `chore: 上传打赏收款码 ${destPath}`, sha, content: b64 });
  const bodyBytes = Buffer.from(body, 'utf-8');

  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'api.github.com',
      path: `/repos/${REPO}/contents/${destPath}`,
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
        if (res.statusCode === 200 || res.statusCode === 201) {
          const resp = JSON.parse(data);
          console.log(`  ✓ ${destPath} -> ${resp.content.html_url}`);
          resolve();
        } else {
          console.error(`  ✗ FAIL: ${data.slice(0, 200)}`);
          reject(new Error(data));
        }
      });
    });
    req.on('error', e => reject(e));
    req.write(bodyBytes);
    req.end();
  });
}

(async () => {
  await uploadFile(
    'C:\\Users\\Administrator\\Desktop\\新建文件夹\\1ef5fd29be088cb532ee3e5b6be46a7.png',
    'docs/public/donate-wechat.png'
  );
  await uploadFile(
    'C:\\Users\\Administrator\\Desktop\\新建文件夹\\3568d6d77f687199cbb1f812482ff16.jpg',
    'docs/public/donate-alipay.jpg'
  );
  console.log('\nAll done!');
})();
