// Post-build: copy static assets and fix dynamic route HTML files
const fs = require('fs');
const path = require('path');

const outDir = path.join(process.cwd(), 'out');
const publicDir = path.join(process.cwd(), 'public');

// 1. Copy Cloudflare-specific files
const files = ['_redirects', '_headers', '_routes.json'];
for (const file of files) {
  const src = path.join(publicDir, file);
  const dst = path.join(outDir, file);
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, dst);
    console.log(`Copied ${file} to out/`);
  }
}

// 2. Fix dynamic route HTML files
// Next.js static export puts dynamic route HTML at /resources/calligraphy.html
// but Cloudflare Pages needs /resources/calligraphy/index.html
const resourceDir = path.join(outDir, 'resources');
if (fs.existsSync(resourceDir)) {
  const items = fs.readdirSync(resourceDir);
  for (const item of items) {
    const htmlFile = path.join(resourceDir, `${item}.html`);
    const subDir = path.join(resourceDir, item);
    if (fs.existsSync(htmlFile) && fs.existsSync(subDir) && fs.statSync(subDir).isDirectory()) {
      const indexFile = path.join(subDir, 'index.html');
      fs.copyFileSync(htmlFile, indexFile);
      console.log(`Fixed: ${item}.html -> ${item}/index.html`);
    }
  }
}
