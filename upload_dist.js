const https = require('https');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const t = execSync('gh auth token').toString().trim();
const repo = 'jm6-lang/resource-nav';

const api = (method, pathPart, bodyData) => new Promise((resolve) => {
  const body = bodyData ? JSON.stringify(bodyData) : null;
  const opts = {
    hostname: 'api.github.com', path: `/repos/${repo}${pathPart}`, method,
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
    let d = ''; res.on('data', c => d += c);
    res.on('end', () => {
      try { resolve({ s: res.statusCode, d: JSON.parse(d) }); }
      catch { resolve({ s: res.statusCode, d }); }
    });
  });
  req.on('error', e => resolve({ s: 0, d: e.message }));
  if (body) req.write(body);
  req.end();
});

function walkDir(dir) {
  const results = [];
  const items = fs.readdirSync(dir);
  for (const item of items) {
    const full = path.join(dir, item);
    const stat = fs.statSync(full);
    if (stat.isDirectory()) {
      results.push(...walkDir(full));
    } else {
      results.push(full);
    }
  }
  return results;
}

async function uploadDistFiles() {
  const distDir = 'C:/resource-nav/docs/.vitepress/dist';
  if (!fs.existsSync(distDir)) {
    console.log('ERROR: dist folder not found!');
    return;
  }

  // Get current main branch SHA
  const ref = await api('GET', '/git/refs/heads/main');
  const mainSha = ref.d.object.sha;
  console.log('Main branch SHA:', mainSha);

  // Get main tree SHA
  const commit = await api('GET', `/git/commits/${mainSha}`);
  const mainTreeSha = commit.d.tree.sha;
  console.log('Main tree SHA:', mainTreeSha);

  // Walk dist directory and create blobs
  const distFiles = walkDir(distDir);
  console.log(`Found ${distFiles.length} files in dist/`);

  const treeEntries = [];
  for (const file of distFiles) {
    const rel = path.relative(distDir, file).replace(/\\/g, '/');
    const content = fs.readFileSync(file);
    const blob = await api('POST', '/git/blobs', {
      content: content.toString('base64'),
      encoding: 'base64'
    });
    if (blob.s === 201) {
      treeEntries.push({
        path: rel,
        mode: '100644',
        type: 'blob',
        sha: blob.d.sha
      });
    } else {
      console.log(`  Blob FAIL ${rel}: ${blob.s}`);
    }
    await new Promise(r => setTimeout(r, 100));
  }

  console.log(`Created ${treeEntries.length} blobs`);

  // Create tree
  const newTree = await api('POST', '/git/trees', {
    base_tree: mainTreeSha,
    tree: treeEntries
  });
  console.log('Tree:', newTree.s, newTree.d.sha || newTree.d.message);

  if (!newTree.d.sha) return;

  // Create commit on main
  const nc = await api('POST', '/git/commits', {
    message: 'Deploy VitePress site',
    tree: newTree.d.sha,
    parents: [mainSha]
  });
  console.log('Commit:', nc.s, nc.d.sha || nc.d.message);

  if (!nc.d.sha) return;

  // Update main branch
  const up = await api('PATCH', '/git/refs/heads/main', { sha: nc.d.sha });
  console.log('Branch updated:', up.s, up.d.ref);
}

uploadDistFiles().catch(e => console.error(e.message));
