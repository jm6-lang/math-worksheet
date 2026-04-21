const fs = require('fs');
const { execSync } = require('child_process');

const content = fs.readFileSync('C:/Users/Administrator/.qclaw/workspace-agent-3bb7b585/math-worksheet/app/page.tsx', 'utf8');
const base64 = Buffer.from(content).toString('base64');

// Write body to temp file
const body = JSON.stringify({
  message: 'feat: 全新暗色主题设计，仿 xgzb.top 风格',
  content: base64,
  sha: 'd2fa215fb382857c27a2700cb5196305dee2efae'
});

fs.writeFileSync('C:/Users/Administrator/.qclaw/workspace-agent-3bb7b585/_push_body.json', body);

console.log(`Body size: ${body.length} bytes`);
