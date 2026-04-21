const https = require('https');
const fs = require('fs');
const { execSync } = require('child_process');
const t = execSync('gh auth token').toString().trim();
const repo = 'jm6-lang/resource-nav';

const get = path => new Promise(r => {
  const req = https.request({
    hostname: 'api.github.com', path: `/repos/${repo}${path}`, method: 'GET',
    headers: { 'Authorization': `Bearer ${t}`, 'Accept': 'application/vnd.github+json', 'User-Agent': 'openclaw', 'X-GitHub-Api-Version': '2022-11-28' }
  }, res => { let d = ''; res.on('data', c => d += c); res.on('end', () => r({ s: res.statusCode, d: JSON.parse(d) })); });
  req.end();
});

const post = (path, body) => new Promise(r => {
  const b = JSON.stringify(body);
  const req = https.request({
    hostname: 'api.github.com', path: `/repos/${repo}${path}`, method: 'POST',
    headers: { 'Authorization': `Bearer ${t}`, 'Accept': 'application/vnd.github+json', 'User-Agent': 'openclaw', 'X-GitHub-Api-Version': '2022-11-28', 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(b) }
  }, res => { let d = ''; res.on('data', c => d += c); res.on('end', () => r({ s: res.statusCode, d: JSON.parse(d) })); });
  req.write(b); req.end();
});

const patch = (path, body) => new Promise(r => {
  const b = JSON.stringify(body);
  const req = https.request({
    hostname: 'api.github.com', path: `/repos/${repo}${path}`, method: 'PATCH',
    headers: { 'Authorization': `Bearer ${t}`, 'Accept': 'application/vnd.github+json', 'User-Agent': 'openclaw', 'X-GitHub-Api-Version': '2022-11-28', 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(b) }
  }, res => { let d = ''; res.on('data', c => d += c); res.on('end', () => r({ s: res.statusCode, d: JSON.parse(d) })); });
  req.write(b); req.end();
});

async function main() {
  // Get current branch
  const ref = await get('/git/refs/heads/main');
  console.log('Current commit:', ref.d.object.sha);

  // Get commit to find tree
  const c = await get('/git/commits/' + ref.d.object.sha);
  console.log('Current tree:', c.d.tree.sha);

  // Create blob for workflow
  const wf = fs.readFileSync('C:/resource-nav/.github/workflows/deploy.yml', 'utf8');
  const blob = await post('/git/blobs', { content: wf, encoding: 'utf-8' });
  console.log('Blob:', blob.s, blob.d.sha || blob.d.message);

  if (!blob.d.sha) { console.log('Blob creation failed'); return; }

  // Create tree with new file
  const newTree = await post('/git/trees', {
    base_tree: c.d.tree.sha,
    tree: [{ path: '.github/workflows/deploy.yml', mode: '100644', type: 'blob', sha: blob.d.sha }]
  });
  console.log('Tree:', newTree.s, newTree.d.sha || newTree.d.message);

  if (!newTree.d.sha) { console.log('Tree creation failed'); return; }

  // Create commit
  const nc = await post('/git/commits', {
    message: 'Add GitHub Actions deploy workflow',
    tree: newTree.d.sha,
    parents: [ref.d.object.sha]
  });
  console.log('Commit:', nc.s, nc.d.sha || nc.d.message);

  if (!nc.d.sha) { console.log('Commit creation failed'); return; }

  // Update branch
  const up = await patch('/git/refs/heads/main', { sha: nc.d.sha });
  console.log('Branch:', up.s, up.d.ref || up.d.message);
  
  console.log('\n✅ Done!');
}

main().catch(e => console.error('Fatal:', e.message));
