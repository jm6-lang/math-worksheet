const https = require('https');
const fs = require('fs');
const path = require('path');

const TOKEN = process.env.GH_TOKEN;
const OWNER = 'jm6-lang';
const REPO = 'tool-nav';
const DIST_DIR = 'C:/tool-nav/docs/.vitepress/dist';

const api = (method, p, data) =>
  new Promise((resolve, reject) => {
    const body = data ? JSON.stringify(data) : null;
    const opts = {
      hostname: 'api.github.com',
      path: p,
      method,
      headers: {
        'Authorization': `Bearer ${TOKEN}`,
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'tool-nav-deploy',
        'Content-Type': 'application/json',
      }
    };
    if (body) opts.headers['Content-Length'] = Buffer.byteLength(body);
    const req = https.request({ ...opts, timeout: 20000 }, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        try { resolve({ status: res.statusCode, data: JSON.parse(d) }); }
        catch { resolve({ status: res.statusCode, data: d }); }
      });
    });
    req.on('timeout', () => reject(new Error('timeout')));
    req.on('error', e => reject(e));
    if (body) req.write(body);
    req.end();
  });

const listDir = (dir, base = '') => {
  const res = [];
  for (const f of fs.readdirSync(dir)) {
    const full = path.join(dir, f);
    const rel = path.join(base, f).replace(/\\/g, '/');
    if (fs.statSync(full).isDirectory()) {
      res.push(...listDir(full, rel));
    } else {
      res.push({ rel, full });
    }
  }
  return res;
};

async function uploadFile(filePath, content) {
  const b64 = content.toString('base64');
  const { status, data } = await api('PUT', `/repos/${OWNER}/${REPO}/contents/${filePath}`, {
    message: `upload ${filePath}`,
    content: b64,
  });
  return { status, data, filePath };
}

async function main() {
  const files = listDir(DIST_DIR);
  console.log(`Uploading ${files.length} files...`);

  let ok = 0, fail = 0;
  for (const { rel, full } of files) {
    const content = fs.readFileSync(full);
    const { status, data, filePath } = await uploadFile(rel, content);
    if (status === 201 || status === 200) {
      ok++;
      process.stdout.write('.');
    } else {
      fail++;
      if (fail <= 3) console.error(`\n${filePath}: ${status} ${data.message || data}`);
    }
  }

  console.log(`\nDone: ${ok} ok, ${fail} failed`);
  if (fail > 0) console.log('Tip: Some files may need SHA (already exist) - re-uploading now...');

  // Retry failed ones
  if (fail > 0) {
    for (const { rel, full } of files) {
      const content = fs.readFileSync(full);
      const b64 = content.toString('base64');
      // Get SHA first
      const { data: shaData } = await api('GET', `/repos/${OWNER}/${REPO}/contents/${rel}`);
      const sha = shaData.sha;
      const { status } = await api('PUT', `/repos/${OWNER}/${REPO}/contents/${rel}`, {
        message: `upload ${rel}`,
        content: b64,
        sha,
      });
      if (status === 200) { ok++; fail--; process.stdout.write('R'); }
    }
    console.log(`\nRetry: ${ok} ok, ${fail} failed`);
  }

  console.log('\nDeploy complete!');
  console.log('Enable GitHub Pages at: https://github.com/jm6-lang/tool-nav/settings/pages');
  console.log('Select: Source = main branch, folder = / (root)');
}

main().catch(e => { console.error('Error:', e.message); process.exit(1); });
