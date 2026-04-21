const https = require('https');
const fs = require('fs');
const { execSync } = require('child_process');

const token = execSync('gh auth token').toString().trim();
const repo = 'jm6-lang/resource-nav';

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
        'User-Agent': 'openclaw-cli',  // Required by GitHub
      }
    };
    if (body) {
      options.headers['Content-Type'] = 'application/json; charset=utf-8';
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
  const localPath = 'C:/resource-nav/' + remotePath;
  if (!fs.existsSync(localPath)) {
    console.log(`SKIP: ${remotePath} not found`);
    return;
  }
  
  const fileContent = fs.readFileSync(localPath);
  const b64 = fileContent.toString('base64');
  
  // Get existing SHA
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
  const msg = result.data.message || result.data.name || JSON.stringify(result.data).slice(0,50);
  console.log(`${result.status} ${remotePath}: ${msg}`);
  return result;
}

async function main() {
  // Upload deploy.yml
  const r1 = await uploadFile('.github/workflows/deploy.yml');
  
  await new Promise(r => setTimeout(r, 2000));
  
  // Check if .github directory now exists
  const r2 = await api('GET', '/contents/.github?ref=main');
  console.log('github dir:', r2.status, typeof r2.data === 'string' ? r2.data.slice(0,80) : (r2.data.name || r2.data.message || ''));
  
  // Check workflows
  const r3 = await api('GET', '/contents/.github/workflows?ref=main');
  console.log('workflows dir:', r3.status, typeof r3.data === 'string' ? r3.data.slice(0,80) : (r3.data.message || (Array.isArray(r3.data) ? r3.data.length + ' items' : '')));
}

main().catch(e => console.error('Fatal:', e.message));
