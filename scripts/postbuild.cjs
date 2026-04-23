// Post-build: copy static assets that Next.js may miss
const fs = require('fs');
const path = require('path');

const files = ['_redirects', '_headers', '_routes.json'];
const outDir = path.join(process.cwd(), 'out');
const publicDir = path.join(process.cwd(), 'public');

for (const file of files) {
  const src = path.join(publicDir, file);
  const dst = path.join(outDir, file);
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, dst);
    console.log(`Copied ${file} to out/`);
  }
}
