# 创建 VitePress 资源导航站

$projectName = "resource-nav"
$projectPath = "C:\$projectName"

# 检查目录是否存在
if (Test-Path $projectPath) {
    Write-Host "目录已存在，删除重建..."
    Remove-Item $projectPath -Recurse -Force
}

# 创建项目目录
New-Item -ItemType Directory -Path $projectPath -Force | Out-Null
Set-Location $projectPath

Write-Host "初始化 npm 项目..."
npm init -y | Out-Null

Write-Host "安装 VitePress..."
npm install -D vitepress | Out-Null

# 创建目录结构
New-Item -ItemType Directory -Path "docs\.vitepress" -Force | Out-Null
New-Item -ItemType Directory -Path "docs\public" -Force | Out-Null

# 创建 VitePress 配置
$config = @'
import { defineConfig } from 'vitepress'

export default defineConfig({
  title: '资源导航站',
  description: '海量免费资源下载导航',
  lang: 'zh-CN',
  lastUpdated: true,
  cleanUrls: true,
  head: [
    ['meta', { name: 'theme-color', content: '#3eaf7c' }],
    ['link', { rel: 'icon', href: '/favicon.ico' }]
  ],
  themeConfig: {
    logo: '/logo.png',
    siteTitle: '资源导航站',
    nav: [
      { text: '首页', link: '/' },
      { text: 'AI教程', link: '/ai/' },
      { text: '电子书', link: '/books/' },
      { text: '软件工具', link: '/tools/' },
      { text: '关于', link: '/about' }
    ],
    sidebar: {
      '/ai/': [
        {
          text: 'AI教程',
          items: [
            { text: 'ChatGPT教程', link: '/ai/chatgpt' },
            { text: 'Midjourney教程', link: '/ai/midjourney' },
            { text: 'Stable Diffusion', link: '/ai/sd' }
          ]
        }
      ],
      '/books/': [
        {
          text: '电子书',
          items: [
            { text: '编程书籍', link: '/books/programming' },
            { text: '设计书籍', link: '/books/design' }
          ]
        }
      ]
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/' }
    ],
    footer: {
      message: '资源导航站 - 免费资源分享',
      copyright: 'Copyright © 2024-present'
    },
    search: {
      provider: 'local'
    },
    outline: {
      label: '目录'
    },
    docFooter: {
      prev: '上一页',
      next: '下一页'
    },
    lastUpdated: {
      text: '最后更新于',
      formatOptions: {
        dateStyle: 'short',
        timeStyle: 'short'
      }
    }
  }
})
'@

$config | Out-File -FilePath "docs\.vitepress\config.mts" -Encoding UTF8

# 创建首页
$index = @'
---
layout: home

hero:
  name: 资源导航站
  text: 超过100T免费资源下载
  tagline: 免费 · 海量 · 持续更新 | 专注提供优质免费资源下载
  image:
    src: /logo.png
    alt: 资源导航站
  actions:
    - theme: brand
      text: 开始浏览
      link: /resources
    - theme: alt
      text: GitHub
      link: https://github.com/

features:
  - icon: 🚀
    title: 完全免费
    details: 所有资源100%免费下载，永无隐藏费用
  - icon: 🔄
    title: 持续更新
    details: 每日更新最新优质资源，紧跟时代潮流
  - icon: ⭐
    title: 品质保证
    details: 专业团队精心筛选，严格把关资源质量
  - icon: 🎯
    title: 分类清晰
    details: 科学的分类体系，帮您快速精准找到所需资源
  - icon: 🌐
    title: 多平台支持
    details: 支持夸克网盘、阿里网盘、百度网盘等主流平台
  - icon: 👥
    title: 社区互动
    details: 加入社区与万千用户交流，分享资源
---

## 📈 平台数据

| 指标 | 数据 |
|------|------|
| 资源总量 | 超过 100TB |
| 分类数量 | 12 个主要类别 |
| 更新频率 | 每日更新 |

## 🔍 热门搜索

免费资源下载 | AI教程 | 电子书下载 | 跨境电商教程 | 自媒体运营 | 在线教育 | 健身视频 | 电影资源 | 软件工具 | 设计素材 | 编程教程 | 考试资料
'@

$index | Out-File -FilePath "docs\index.md" -Encoding UTF8

# 创建资源列表页
$resources = @'
# 资源列表

## AI教程

| 资源名称 | 描述 | 下载 |
|---------|------|------|
| ChatGPT从入门到精通 | 完整教程包含提示词工程 | [下载](/ai/chatgpt) |
| Midjourney绘画教程 | AI绘图完整指南 | [下载](/ai/midjourney) |
| Stable Diffusion本地部署 | 含模型资源包 | [下载](/ai/sd) |

## 电子书

| 资源名称 | 描述 | 下载 |
|---------|------|------|
| Python编程从入门到实践 | 经典入门书籍 | [下载](/books/programming) |
| JavaScript高级程序设计 | 前端必读 | [下载](/books/design) |

## 软件工具

| 资源名称 | 描述 | 下载 |
|---------|------|------|
| Adobe全家桶 | PS/PR/AE等 | [下载](/tools/adobe) |
| Office2024 | 办公套件 | [下载](/tools/office) |
'@

$resources | Out-File -FilePath "docs\resources.md" -Encoding UTF8

# 创建关于页面
$about = @'
# 关于我们

## 平台介绍

资源导航站是一个专注于提供免费优质资源下载的开放平台。我们坚信知识和资源应该人人可得，致力于为全球用户提供超过100T的海量优质资源。

## 联系方式

- QQ群: XXXXXXXXX
- 邮箱: contact@example.com
- GitHub: [GitHub仓库](https://github.com/)
'@

$about | Out-File -FilePath "docs\about.md" -Encoding UTF8

# 创建分类目录
New-Item -ItemType Directory -Path "docs\ai" -Force | Out-Null
New-Item -ItemType Directory -Path "docs\books" -Force | Out-Null
New-Item -ItemType Directory -Path "docs\tools" -Force | Out-Null

# 创建分类页面
$aiIndex = @'
# AI教程

## ChatGPT教程

完整的ChatGPT使用教程，包含：
- 基础使用方法
- 提示词工程技巧
- 高级应用场景

[点击下载](#)
'@

$aiIndex | Out-File -FilePath "docs\ai\index.md" -Encoding UTF8
$aiIndex | Out-File -FilePath "docs\ai\chatgpt.md" -Encoding UTF8

# 更新 package.json 添加脚本
$pkg = Get-Content "package.json" | ConvertFrom-Json
$pkg.scripts = @{
    "docs:dev" = "vitepress dev docs"
    "docs:build" = "vitepress build docs"
    "docs:preview" = "vitepress preview docs"
}
$pkg | ConvertTo-Json -Depth 10 | Out-File "package.json" -Encoding UTF8

Write-Host ""
Write-Host "✅ VitePress 项目创建完成！" -ForegroundColor Green
Write-Host ""
Write-Host "项目位置: $projectPath"
Write-Host ""
Write-Host "下一步操作："
Write-Host "  cd $projectPath"
Write-Host "  npm run docs:dev     # 本地预览"
Write-Host "  npm run docs:build   # 构建静态文件"
Write-Host ""
