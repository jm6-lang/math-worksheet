// Post-build: copy static assets and fix nested route HTML files
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

// 2. Fix nested route HTML files
// Next.js static export creates both /resources/calligraphy.html and /resources/calligraphy/ dir
// Cloudflare Pages matches the directory first (no index.html inside = 404)
// Solution: copy .html content into the directory as index.html
function fixNestedRoutes(dir) {
  if (!fs.existsSync(dir)) return;
  const items = fs.readdirSync(dir);
  for (const item of items) {
    const htmlFile = path.join(dir, `${item}.html`);
    const subDir = path.join(dir, item);
    if (fs.existsSync(htmlFile) && fs.existsSync(subDir) && fs.statSync(subDir).isDirectory()) {
      const indexFile = path.join(subDir, 'index.html');
      if (!fs.existsSync(indexFile)) {
        fs.copyFileSync(htmlFile, indexFile);
        console.log(`Fixed: ${path.relative(outDir, htmlFile)} -> ${path.relative(outDir, indexFile)}`);
      }
    }
  }
}

fixNestedRoutes(path.join(outDir, 'resources'));
fixNestedRoutes(path.join(outDir, 'tools'));
fixNestedRoutes(path.join(outDir, 'blog'));
