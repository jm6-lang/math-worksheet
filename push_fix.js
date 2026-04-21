const { readFileSync } = require('fs');
const { execSync } = require('child_process');

const filePath = 'resource-portal/docs/.vitepress/theme/components/ZiWeiCalculator.vue';
const content = readFileSync(filePath);
const b64 = content.toString('base64');
const sha = execSync('gh api repos/jm6-lang/resource-portal/contents/docs/.vitepress/theme/components/ZiWeiCalculator.vue --jq .sha', { encoding: 'utf-8' }).trim();

require('fs').writeFileSync('C:/tmp/iztro_b64.txt', b64);

const msg = 'fix: 修复getInterpretation函数声明缺失和类型错误';
const cmd = 'gh api repos/jm6-lang/resource-portal/contents/docs/.vitepress/theme/components/ZiWeiCalculator.vue --method PUT -F message="' + msg + '" -F content=@C:/tmp/iztro_b64.txt -F sha=' + sha;
const result = execSync(cmd, { encoding: 'utf-8' });
console.log('SUCCESS');
