# 算个题吧 - 数学练习纸生成器

> 参考 [写个字吧（字帖）](https://xgzb.top) 开发的互补产品 · 完全免费 · 免登录

**在线地址：** https://suanzu.pages.dev

---

## 功能亮点

### 🎯 出题系统
- ✅ 加法 / 减法 / 乘法 / 除法（随机不重复）
- ✅ 混合运算 / 填空题 / 比大小
- ✅ 竖式加法 / 竖式减法 / 竖式乘法 / 竖式除法
- ✅ 1-6年级智能筛选（高年级自动过滤低幼题型）
- ✅ 数字范围：10以内 → 100万以内
- ✅ 题目数量：5-100题可调

### 📄 答案卷系统
- ✅ **题目卷**（空白答题区）+ **答案卷**（完整参考答案）
- ✅ **题目内嵌答案**（可选，每题下方直接显示答案）
- ✅ 一键导出：题目卷 PDF / 答案卷 PDF / 双卷同时导出

### 🖨️ 模板系统
| 模板 | 适用年级 | 特点 |
|------|---------|------|
| 🟦 田字格 | 1-2年级 | 红色竖线+蓝色横线辅助 |
| 🟩 方格纸 | 3-4年级 | 普通方格 |
| 📄 横线格 | 高年级 | 标准试卷风格 |
| ⬜ 空白纸 | 任意 | 自由书写 |

---

## 技术栈

- **Next.js 16** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **jsPDF + html2canvas**（PDF 导出）
- **纯 CSS 田字格**（无需图片）

---

## 本地开发

```bash
cd math-worksheet
npm install
npm run dev
# 访问 http://localhost:3000
```

## 构建部署

```bash
npm run build
```

---

## 部署到 Cloudflare Pages

1. 将项目推送到 GitHub
2. 连接 Cloudflare Pages → 选择 GitHub 仓库
3. 构建命令：`npm run build`
4. 输出目录：`out`
5. 环境变量：`NODE_VERSION = 18`

---

## 项目结构

```
math-worksheet/
├── lib/
│   ├── questionGenerator.ts   ← 核心出题算法
│   └── pdfExport.ts           ← PDF 导出
├── components/
│   └── WorksheetPreview.tsx   ← 田字格/方格/横线渲染 + 答案卷
└── app/
    ├── page.tsx               ← 主界面（配置面板+预览）
    └── layout.tsx             ← 布局+SEO
```

---

## 后续路线图

- [ ] 答案卷独立分页打印
- [ ] 应用题支持
- [ ] 分数/小数运算
- [ ] 计时模式
- [ ] 历史记录
- [ ] 接入字帖站导流
