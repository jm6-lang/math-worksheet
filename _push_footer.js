const { execSync } = require('child_process');
const fs = require('fs');

const base = 'C:/Users/Administrator/.qclaw/workspace-agent-3bb7b585/math-worksheet';

function pushFile(relPath, message) {
  const fullPath = base + '/' + relPath;
  const content = fs.readFileSync(fullPath);
  const b64 = content.toString('base64');
  
  let sha = '';
  try {
    sha = execSync(`gh api repos/jm6-lang/math-worksheet/contents/${relPath} --jq .sha`, { timeout: 15000 }).toString().trim();
  } catch (e) {}
  
  const body = { message, content: b64 };
  if (sha) body.sha = sha;
  
  fs.writeFileSync('C:/Users/Administrator/.qclaw/workspace-agent-3bb7b585/_push_body.json', JSON.stringify(body));
  const out = execSync(`gh api repos/jm6-lang/math-worksheet/contents/${relPath} --method PUT --input _push_body.json --jq .commit.sha`, { timeout: 20000 });
  console.log(relPath, '->', out.toString().trim());
}

pushFile('app/page.tsx', 'fix: replace footer xgzb.top link with internal tools');
