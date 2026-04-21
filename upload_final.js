const https = require('https');
const fs = require('fs');
const { execSync } = require('child_process');

const token = execSync('gh auth token').toString().trim();
const repo = 'jm6-lang/resource-nav';
const base = 'C:/resource-nav/';

function api(method, path, bodyData) {
  return new Promise((resolve, reject) => {
    const body = bodyData ? JSON.stringify(bodyData) : null;
    const options = {
      hostname: 'api.github.com',
      path: `/repos/${repo}${path}`,
      method,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'OpenClaw/1.0',
      }
    };
    if (body) {
      options.headers['Content-Type'] = 'application/json';
      options.headers['Content-Length'] = Buffer.byteLength(body);
    }
    
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(data) });
        } catch {
          resolve({ status: res.statusCode, data });
        }
      });
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

async function uploadFile(remotePath) {
  const localPath = base + remotePath;
  if (!fs.existsSync(localPath)) {
    console.log(`SKIP (not found): ${remotePath}`);
    return;
  }
  
  const content = fs.readFileSync(localPath);
  const b64 = content.toString('base64');
  
  // Get existing SHA if file exists
  let sha = null;
  const existing = await api('GET', `/contents/${remotePath}?ref=main`);
  if (existing.status === 200) {
    sha = existing.data.sha;
  }
  
  const body = {
    message: `Add ${remotePath}`,
    content: b64,
    branch: 'main'
  };
  if (sha) body.sha = sha;
  
  const result = await api('PUT', `/contents/${remotePath}`, body);
  const name = result.data.name || result.data.message || '';
  console.log(`${result.status} ${remotePath}: ${name}`);
}

async function main() {
  const files = [
    '.github/workflows/deploy.yml',
    'docs/recommend.md'
  ];
  
  for (const f of files) {
    await uploadFile(f);
    await new Promise(r => setTimeout(r, 1000));
  }
}

main().catch(e => console.error('Fatal:', e.message));
