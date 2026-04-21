# math-worksheet 仓库分析与改进建议

## 一、现状概览

- **仓库**：`jm6-lang/math-worksheet`（2026-04-20 创建）
- **技术栈**：Next.js 16 + Tailwind CSS + TypeScript
- **目标**：数学口算题生成器 + 田字格/方格/横线模板 + PDF 导出
- **引用站点**：`xgzb.top`（字帖生成器，功能丰富、设计现代）

---

## 二、需要改进的问题（按优先级）

### 🔴 P0 — 必须修复

#### 1. 没有 GitHub Actions 自动部署
**问题**：目前代码 push 到 master 后不会自动构建并发布到 GitHub Pages。

**解决方案**：在 `.github/workflows/` 下创建 `deploy.yml`。

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [master]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./out

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**注意**：需要在仓库 Settings → Pages → Source 设置为 "GitHub Actions"

#### 2. package.json 缺少 homepage 和 description
当前 `package.json` 没有 `homepage` 字段，这影响 GitHub Pages 访问和 SEO。

#### 3. README 为空（没有内容）
README.md 存在但内容为空，不便于展示和引流。

---

### 🟡 P1 — 重要优化

#### 4. next.config.ts 缺少 basePath 配置
当仓库部署到 `https://jm6-lang.github.io/math-worksheet/` 时，必须设置 `basePath` 才能正常加载 JS/CSS。

```typescript
const nextConfig: NextConfig = {
  output: 'export',
  images: { unoptimized: true },
  basePath: '/math-worksheet',  // 添加这行
}
```

#### 5. 问题类型不够丰富
当前只有加法，建议增加：
- **减法**（被减数不小于减数，自动判断）
- **乘法**（乘法口诀表范围内）
- **比大小**（两个结果比大小）
- **填空题**（如 `3 + ☐ = 7`）

#### 6. 缺少打印优化（print CSS）
目前 `globals.css` 有基础的 `@media print`，但没有针对打印机做更精细的优化（比如隐藏侧边栏、控制分页等）。

---

### 🟢 P2 — 体验优化

#### 7. 增加模板种类
当前 4 种模板，可参考 xgzb.top 增加：
- **拼音格**（用于拼音练习）
- **四线格**（英语/拼音）
- **作文纸**（带方格的写作纸）
- **自定义行列数**

#### 8. README 增强展示
添加使用截图、功能说明、在线访问地址。

#### 9. 底部 Footer 链接待完善
当前 Footer 链接指向 `xgzb.top`，应改为指向自己项目的 GitHub 仓库地址。

---

## 三、建议的功能拓展（参考 xgzb.top）

| 功能 | 说明 | 难度 |
|------|------|------|
| 年级切换（1-6年级） | 不同年级显示不同难度范围 | 🟡 中 |
| 历史记录 | localStorage 记录最近生成 | 🟢 低 |
| 批量生成多页 | 一次生成多页口算题 | 🟢 低 |
| 答案卷单独导出 | 题卷和答案卷分开下载 | 🟢 低 |
| 竖式排版 | 数学竖式、脱式计算 | 🟡 中 |
| 英语练习 | 英文字母、单词默写 | 🟡 中 |

---

## 四、执行计划建议

**第一阶段（立即可做）**：
1. 创建 `.github/workflows/deploy.yml`（实现自动化部署）
2. 修复 `next.config.ts` 的 `basePath`
3. 补充 README 内容
4. 设置 package.json 的 homepage 字段

**第二阶段（功能增强）**：
1. 增加减法、乘法、比大小题型
2. 优化 print CSS
3. 增加更多模板

**第三阶段（运营优化）**：
1. SEO 优化（meta tags、Sitemap）
2. 添加访问统计
3. 用户反馈机制

---

## 五、参考：xgzb.top 的亮点设计

1. **顶部导航**：模板 / 快速入门 / 使用教程 分级清晰
2. **左侧边栏**：工具分类一目了然
3. **卡片式布局**：模板选择用卡片，操作感强
4. **颜色搭配**：蓝绿渐变 header + 白色卡片，干净清爽
5. **响应式设计**：移动端也能正常使用

---

> 💡 **核心建议**：先把自动化部署跑通，让网站能正常在线访问，再逐步丰富功能。