const { execSync } = require('child_process');
const fs = require('fs');

const base = 'C:/Users/Administrator/.qclaw/workspace-agent-3bb7b585/math-worksheet';

// Update the README to trigger rebuild
const readmePath = base + '/README.md';
let readme = fs.readFileSync(readmePath, 'utf8');
if (!readme.includes('部署时间')) {
  readme += `\n\n<!-- 最后更新: ${new Date().toISOString()} -->\n`;
  fs.writeFileSync(readmePath, readme);
}

const content = fs.readFileSync(readmePath);
const b64 = content.toString('base64');

let sha = '';
try {
  sha = execSync('gh api repos/jm6-lang/math-worksheet/contents/README.md --jq .sha', { timeout: 15000 }).toString().trim();
} catch (e) {}

const body = { message: 'chore: trigger CF Pages rebuild', content: b64 };
if (sha) body.sha = sha;

fs.writeFileSync('C:/Users/Administrator/.qclaw/workspace-agent-3bb7b585/_push_body.json', JSON.stringify(body));
const out = execSync('gh api repos/jm6-lang/math-worksheet/contents/README.md --method PUT --input _push_body.json --jq .commit.sha', { timeout: 20000 });
console.log('README.md ->', out.toString().trim());
