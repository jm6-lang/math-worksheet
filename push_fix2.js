const fs = require('fs');
const { execSync } = require('child_process');

const filePath = 'resource-portal/docs/.vitepress/theme/components/ZiWeiCalculator.vue';
const content = fs.readFileSync(filePath);
const b64 = content.toString('base64');
const sha = execSync('gh api repos/jm6-lang/resource-portal/contents/docs/.vitepress/theme/components/ZiWeiCalculator.vue --jq .sha', { encoding: 'utf8' }).trim();

fs.writeFileSync('C:/tmp/zwb64.txt', b64);

const msg = 'fix: UMD模块需要调用才能获取导出对象';
const cmd = `gh api repos/jm6-lang/resource-portal/contents/docs/.vitepress/theme/components/ZiWeiCalculator.vue --method PUT -F message="${msg}" -F content@C:/tmp/zwb64.txt -F sha=${sha}`;
const result = execSync(cmd, { encoding: 'utf8' });
console.log('SUCCESS');
