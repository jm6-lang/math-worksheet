const { readFileSync, writeFileSync } = require('fs');
const { execSync } = require('child_process');

const filePath = 'docs/.vitepress/theme/components/ZiWeiCalculator.vue';
const content = readFileSync(filePath);
const b64 = content.toString('base64');
const sha = execSync('gh api repos/jm6-lang/resource-portal/contents/docs/.vitepress/theme/components/ZiWeiCalculator.vue --jq .sha', { encoding: 'utf-8' }).trim();

const msg = 'fix: 使用CDN加载iztro绕过打包问题';
const cmd = `gh api repos/jm6-lang/resource-portal/contents/docs/.vitepress/theme/components/ZiWeiCalculator.vue --method PUT -F message="${msg}" -F content=@/tmp/iztro_b64.txt -F sha="${sha}"`;

writeFileSync('/tmp/iztro_b64.txt', b64);

try {
  const result = execSync(cmd, { encoding: 'utf-8' });
  console.log('SUCCESS:', result);
} catch(e) {
  console.error('ERROR:', e.message);
}
