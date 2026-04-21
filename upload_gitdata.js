const https = require('https');
const fs = require('fs');
const { execSync } = require('child_process');

const t = execSync('gh auth token').toString().trim();
const repo = 'jm6-lang/resource-nav';

function api(method, path, bodyData) {
  return new Promise((resolve) => {
    const body = bodyData ? JSON.stringify(bodyData) : null;
    const opts = {
      hostname: 'api.github.com',
      path: `/repos/${repo}${path}`,
      method,
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
        try { resolve({ status: res.statusCode, data: JSON.parse(d) }); }
        catch { resolve({ status: res.statusCode, data: d }); }
      });
    });
    req.on('error', e => resolve({ status: 0, data: e.message }));
    if (body) req.write(body);
    req.end();
  });
}

async function main() {
  // 1. Get current branch SHA
  const branch = await api('GET', '/git/refs/heads/main');
  console.log('Branch ref:', branch.status, branch.data.ref, '->', branch.data.object?.sha);
  const currentTreeSha = branch.data.object?.sha;

  // 2. Get current commit to find parent tree
  const commit = await api('GET', `/git/commits/${currentTreeSha}`);
  const parentTreeSha = commit.data.tree?.sha;
  console.log('Parent tree:', parentTreeSha);

  // 3. Create blob for workflow file
  const wfContent = fs.readFileSync('C:/resource-nav/.github/workflows/deploy.yml', 'utf8');
  const blob = await api('POST', '/git/blobs', {
    content: wfContent,
    encoding: 'utf-8'
  });
  console.log('Blob created:', blob.status, blob.data.sha);

  // 4. Create tree with new workflow file
  const tree = await api('POST', '/git/trees', {
    base_tree: parentTreeSha,
    tree: [{
      path: '.github/workflows/deploy.yml',
      mode: '100644',
      type: 'blob',
      sha: blob.data.sha
    }]
  });
  console.log('Tree created:', tree.status, tree.data.sha);

  // 5. Create commit
  const newCommit = await api('POST', '/git/commits', {
    message: 'Add GitHub Actions deploy workflow',
    tree: tree.data.sha,
    parents: [currentTreeSha]
  });
  console.log('Commit created:', newCommit.status, newCommit.data.sha);

  // 6. Update branch ref
  const updated = await api('PATCH', '/git/refs/heads/main', {
    sha: newCommit.data.sha
  });
  console.log('Branch updated:', updated.status, updated.data.ref);
  
  console.log('\n✅ Workflow uploaded via Git Data API!');
}

main().catch(e => console.error('Fatal:', e.message));
