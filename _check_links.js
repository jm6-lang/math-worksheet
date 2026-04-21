const { execSync } = require('child_process');
const content = execSync('gh api repos/jm6-lang/math-worksheet/contents/app/page.tsx --jq .content', { encoding: 'utf8' }).trim();
const decoded = Buffer.from(content, 'base64').toString('utf8');
const lines = decoded.split('\n');
lines.forEach((line, i) => {
  if (line.includes('xgzb') || line.includes('href="/tools')) {
    console.log(`${i + 1}: ${line.trim()}`);
  }
});
