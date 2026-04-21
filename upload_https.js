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
  
  // Get existing SHA first
  const getOptions = {
    hostname: 'api.github.com',
    path: `/repos/${repo}/contents/${remotePath}?ref=main`,
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Accept': 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
      'User-Agent': 'OpenClaw/1.0'
    }
  };

  return new Promise((resolve) => {
    // GET to get SHA
    const getReq = https.request(getOptions, (getRes) => {
      let data = '';
      getRes.on('data', d => data += d);
      getRes.on('end', () => {
        let sha = null;
        try {
          const j = JSON.parse(data);
          sha = j.sha;
        } catch(e) {}
        
        // PUT to upload
        const body = JSON.stringify({
          message: `Add ${remotePath}`,
          content: b64,
          branch: 'main',
          ...(sha ? { sha } : {})
        });
        
        const putOptions = {
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
        
        const putReq = https.request(putOptions, (putRes) => {
          let responseData = '';
          putRes.on('data', d => responseData += d);
          putRes.on('end', () => {
            console.log(`${putRes.statusCode} ${remotePath}:`, responseData.slice(0, 100));
            resolve();
          });
        });
        
        putReq.on('error', e => {
          console.log(`ERROR ${remotePath}:`, e.message);
          resolve();
        });
        
        putReq.write(body);
        putReq.end();
      });
    });
    
    getReq.on('error', e => {
      console.log(`GET ERROR ${remotePath}:`, e.message);
      resolve();
    });
    
    getReq.end();
  });
}

async function main() {
  for (const file of files) {
    await uploadFile(file);
    await new Promise(r => setTimeout(r, 1000));
  }
  console.log('Done!');
}

main().catch(console.error);
