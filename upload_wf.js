const https = require('https');
const fs = require('fs');
const { execSync } = require('child_process');
const t = execSync('gh auth token').toString().trim();
const repo = 'jm6-lang/resource-nav';

const b64 = fs.readFileSync('C:/resource-nav/.github/workflows/deploy.yml').toString('base64');
const body = JSON.stringify({ message: 'Add deploy workflow', content: b64, branch: 'main' });

const options = {
  hostname: 'api.github.com',
  path: `/repos/${repo}/contents/.github/workflows/deploy.yml`,
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${t}`,
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'User-Agent': 'openclaw',
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(body)
  }
};

const req = https.request(options, (res) => {
  let d = '';
  res.on('data', c => d += c);
  res.on('end', () => {
    try {
      const j = JSON.parse(d);
      console.log(`${res.statusCode} ${j.message || j.content?.name || 'ok'}`);
    } catch {
      console.log(`${res.statusCode} ${d.slice(0, 100)}`);
    }
  });
});

req.on('error', e => console.log('ERR:', e.message));
req.write(body);
req.end();
