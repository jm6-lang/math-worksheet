const https = require('https');
const fs = require('fs');
const { execSync } = require('child_process');

const t = execSync('gh auth token').toString().trim();
const repo = 'jm6-lang/resource-nav';

const wfContent = fs.readFileSync('C:/resource-nav/.github/workflows/deploy.yml', 'utf8');
const b64 = Buffer.from(wfContent).toString('base64');

const body = JSON.stringify({
  name: 'Deploy to GitHub Pages',
  path: '.github/workflows/deploy.yml',
  content: b64,
  sha: 'auto'
});

const options = {
  hostname: 'api.github.com',
  path: `/repos/${repo}/actions/workflows`,
  method: 'POST',
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
    console.log(`Status: ${res.statusCode}`);
    console.log(`Response: ${d.slice(0, 500)}`);
  });
});

req.on('error', e => console.log('ERR:', e.message));
req.write(body);
req.end();
