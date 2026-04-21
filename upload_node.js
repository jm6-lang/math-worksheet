const { execSync } = require('child_process');
const fs = require('fs');

const token = execSync('gh auth token').toString().trim();
const repo = 'jm6-lang/resource-nav';

const files = [
  ['.github/workflows/deploy.yml', 'C:/resource-nav/.github/workflows/deploy.yml'],
  ['docs/recommend.md', 'C:/resource-nav/docs/recommend.md'],
];

files.forEach(([remote, local]) => {
  const content = fs.readFileSync(local);
  const b64 = content.toString('base64');
  const tmp = 'C:/Temp/' + remote.replace(/[\/\.]/g, '_') + '.txt';
  fs.writeFileSync(tmp, b64);
  console.log('Encoded:', remote, 'b64 length:', b64.length);

  const cmd = 'gh api repos/' + repo + '/contents/' + remote + ' --method PUT -f message="Add ' + remote + '" -f branch=main -f content=@' + tmp;
  try {
    const out = execSync(cmd, { timeout: 20000, encoding: 'utf-8' });
    console.log('OK:', remote);
  } catch(e) {
    console.log('FAIL:', remote, e.stderr ? e.stderr.toString().slice(0,300) : e.message);
  }
});
