// restore-repo.js - Restore all files from GitHub API recursively, overlay local changes
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const repo = 'jm6-lang/math-worksheet';
const commitSha = '7e92ca008b610f6e0d67dcff29a1b6cd9f2dd503';
const workspace = 'C:/Users/Administrator/.qclaw/workspace-agent-3bb7b585/math-worksheet';

// Get full tree (recursive=1)
const treeRaw = execSync(`gh api repos/${repo}/git/trees/${commitSha}?recursive=1 --jq ""`, { encoding: 'utf8' });
const tree = JSON.parse(treeRaw);
console.log(`Tree has ${tree.tree.length} entries (truncated=${tree.truncated})`);

const skipPrefixes = ['math-worksheet/'];

let downloaded = 0;
let skipped = 0;
let dirs = 0;

function processEntries(entries) {
  for (const entry of entries) {
    if (skipPrefixes.some(p => entry.path.startsWith(p))) {
      skipped++;
      continue;
    }

    if (entry.type === 'tree') {
      const dirPath = path.join(workspace, entry.path);
      fs.mkdirSync(dirPath, { recursive: true });
      dirs++;
      continue;
    }

    if (entry.type === 'blob') {
      try {
        const blobRaw = execSync(`gh api ${entry.url} --jq ".content"`, { encoding: 'utf8' });
        const content = Buffer.from(blobRaw.trim(), 'base64');
        const filePath = path.join(workspace, entry.path);
        const dir = path.dirname(filePath);
        fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(filePath, content);
        downloaded++;
        if (downloaded % 5 === 0) process.stdout.write(`\n  [${downloaded} files...]`);
        process.stdout.write('.');
      } catch (e) {
        console.error(`\nError downloading ${entry.path}: ${e.message}`);
      }
    }
  }
}

processEntries(tree.tree);
console.log(`\nDone: ${downloaded} files downloaded, ${dirs} dirs created, ${skipped} skipped`);
