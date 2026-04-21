# math-worksheet 导航栏 + 捐赠功能 - 2026-04-21 10:42

## 目标
1. 重写顶部导航栏，去掉"写个字吧→"外链，添加完整导航菜单
2. 添加捐赠功能，使用用户自己的收款二维码

## 完成内容

### 导航栏重写
- **快速入门**：点击回首页 Hero
- **使用教程**：弹出 4 步引导弹窗
- **教材工具 ▾**：下拉菜单（写个字吧、数独游戏）
- **捐赠**：弹出用户收款码弹窗
- 移动端：☰ 汉堡菜单 + 同样导航项
- Logo "算个题吧" 可点击回首页

### 捐赠弹窗
- 标题："☕ 请作者喝杯咖啡"
- 双列布局：左侧微信支付、右侧支付宝
- 二维码来源：`C:\Users\Administrator\Desktop\二维码\`
  - `1ef5fd29be088cb532ee3e5b6be46a7.png` → `public/donate/wechat.png`
  - `3568d6d77f687199cbb1f812482ff16.jpg` → `public/donate/alipay.jpg`

### Commits
- `bac9f90` - 删除捐赠链接（跳转别人的网站）
- `1cf7d0f` - 添加捐赠弹窗（page.tsx）
- `1796263` - 微信收款码上传
- `e4aeb67` - 支付宝收款码上传

## 技术细节
- 新增状态变量：`showDonate`、`mobileMenu`、`showGuide`
- GitHub API 推送方式：gh api PUT contents/... （因 HTTPS 被 SSH 替代）
- Cloudflare Pages 自动构建部署
