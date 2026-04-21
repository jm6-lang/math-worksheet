const https = require('https');
const { execSync } = require('child_process');
const t = execSync('gh auth token').toString().trim();
const repo = 'jm6-lang/resource-nav';

function apiReq(method, path, bodyData) {
  return new Promise((resolve) => {
    const body = bodyData ? JSON.stringify(bodyData) : null;
    const opts = {
      hostname: 'api.github.com', path, method,
      headers: {
        'Authorization': `Bearer ${t}`,
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'openclaw',
      }
    };
    if (body) {
      opts.headers['Content-Type'] = 'application/json';
      opts.headers['Content-Length'] = Buffer.byteLength(body);
    }
    const req = https.request(opts, (res) => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        try { resolve({ s: res.statusCode, d: JSON.parse(d) }); }
        catch { resolve({ s: res.statusCode, d }); }
      });
    });
    req.on('error', e => resolve({ s: 0, d: e.message }));
    if (body) req.write(body);
    req.end();
  });
}

async function main() {
  // Check current pages setup
  const current = await apiReq('GET', `/repos/${repo}/pages`);
  console.log('Current pages:', current.s, current.d?.build_type || current.d?.message || '');

  // Enable with legacy build from main branch root
  const enable = await apiReq('POST', `/repos/${repo}/pages`, {
    build_type: 'legacy',
    source: { branch: 'main', path: '/' }
  });
  console.log('Enable pages:', enable.s, enable.d?.build_type || enable.d?.message || '');
}

main().catch(e => console.error(e.message));
