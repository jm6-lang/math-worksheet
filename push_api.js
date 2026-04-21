const https = require('https');
const fs = require('fs');
const path = 'C:/tmp/zw_encode.txt';
const content = fs.readFileSync(path, 'utf8').trim();
const sha = 'd0d96c34dfad5bf95f046abde548e69b2ee657d1';

const data = JSON.stringify({
  message: 'fix: UMD模块需要调用才能获取导出对象',
  content: content,
  sha: sha
});

const options = {
  hostname: 'api.github.com',
  path: '/repos/jm6-lang/resource-portal/contents/docs/.vitepress/theme/components/ZiWeiCalculator.vue',
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + process.env.GITHUB_TOKEN,
    'User-Agent': 'OpenClaw'
  }
};

const req = https.request(options, (res) => {
  let body = '';
  res.on('data', chunk => body += chunk);
  res.on('end', () => {
    console.log('Status:', res.statusCode);
    console.log(body);
  });
});

req.on('error', e => console.error('Error:', e));
req.write(data);
req.end();
