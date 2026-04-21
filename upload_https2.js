const https = require('https');
const fs = require('fs');
const { execSync } = require('child_process');

const token = execSync('gh auth token').toString().trim();
const repo = 'jm6-lang/resource-nav';

const files = [
  '.github/workflows/deploy.yml',
  'docs/recommend.md'
];

const base = 'C:/resource-nav/';

function uploadFile(remotePath) {
  const localPath = base + remotePath;
  const content = fs.readFileSync(localPath);
  const b64 = content.toString('base64');
  
  const body = JSON.stringify({
    message: `Add ${remotePath}`,
    content: b64,
    branch: 'main'
  });
  
  const options = {
    hostname: 'api.github.com',
    path: `/repos/${repo}/contents/${remotePath}`,
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Accept': 'application/vnd.github+json',
      'Content-Type': 'application/json',
      'X-GitHub-Api-Version': '2022-11-28',
      'Content-Length': Buffer.byteLength(body),
      'User-Agent': 'OpenClaw/1.0'
    }
  };

  return new Promise((resolve) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        const j = JSON.parse(data);
        console.log(`${res.statusCode} ${remotePath}: ${j.message || j.content?.name || 'ok'}`);
        resolve();
      });
    });
    
    req.on('error', e => {
      console.log(`ERROR ${remotePath}:`, e.message);
      resolve();
    });
    
    req.write(body);
    req.end();
  });
}

async function main() {
  for (const file of files) {
    await uploadFile(file);
    await new Promise(r => setTimeout(r, 2000));
  }
}

main().catch(console.error);
