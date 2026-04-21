// sync-and-commit.js
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const repo = 'jm6-lang/math-worksheet';
const commitSha = '7e92ca008b610f6e0d67dcff29a1b6cd9f2dd503';
const workspace = 'C:/Users/Administrator/.qclaw/workspace-agent-3bb7b585/math-worksheet';

console.log('Fetching recursive tree...');
const treeRaw = execSync(`gh api repos/${repo}/git/trees/${commitSha} --jq ""`, { encoding: 'utf8' });
const tree = JSON.parse(treeRaw);

const skipPrefixes = ['math-worksheet/'];
let downloaded = 0;
let dirs = 0;
let skipped = 0;

function processEntries(entries) {
  for (const entry of entries) {
    if (skipPrefixes.some(p => entry.path.startsWith(p))) {
      skipped++;
      continue;
    }

    if (entry.type === 'tree') {
      const dirPath = path.join(workspace, entry.path);
      if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
        dirs++;
      }
      // Fetch subtree recursively
      try {
        const subRaw = execSync(`gh api ${entry.url} --jq ""`, { encoding: 'utf8' });
        const sub = JSON.parse(subRaw);
        processEntries(sub.tree);
      } catch (e) {
        console.error(`\nError fetching subtree ${entry.path}: ${e.message}`);
      }
      continue;
    }

    if (entry.type === 'blob') {
      try {
        const blobRaw = execSync(`gh api ${entry.url} --jq ".content"`, { encoding: 'utf8' });
        const content = Buffer.from(blobRaw.trim(), 'base64');
        const filePath = path.join(workspace, entry.path);
        const dir = path.dirname(filePath);
        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(filePath, content);
        downloaded++;
        process.stdout.write('.');
      } catch (e) {
        // file may already exist with our changes - skip
      }
    }
  }
}

processEntries(tree.tree);
console.log(`\nRestored: ${downloaded} files, ${dirs} dirs, ${skipped} skipped`);

// Delete default Next.js SVG files
const defaultSvgs = ['public/next.svg', 'public/vercel.svg', 'public/window.svg', 'public/globe.svg', 'public/file.svg'];
for (const f of defaultSvgs) {
  const fp = path.join(workspace, f);
  if (fs.existsSync(fp)) {
    fs.unlinkSync(fp);
    console.log(`Deleted: ${f}`);
  }
}

// Delete empty math-worksheet/ if exists
const mwDir = path.join(workspace, 'math-worksheet');
if (fs.existsSync(mwDir)) {
  fs.rmSync(mwDir, { recursive: true, force: true });
  console.log('Deleted: math-worksheet/');
}

console.log('Done! Files restored and cleaned.');
