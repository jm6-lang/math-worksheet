import os, json, subprocess, sys

project_name = "resource-nav"
project_path = f"C:\\{project_name}"

# 删除已存在目录
if os.path.exists(project_path):
    import shutil
    shutil.rmtree(project_path)
    print(f"删除已存在目录: {project_path}")

# 创建目录
os.makedirs(project_path)
os.makedirs(f"{project_path}\\docs\\.vitepress")
os.makedirs(f"{project_path}\\docs\\public")
os.makedirs(f"{project_path}\\docs\\ai")
os.makedirs(f"{project_path}\\docs\\books")
os.makedirs(f"{project_path}\\docs\\tools")

print(f"创建项目目录: {project_path}")

# 初始化 npm
subprocess.run(["npm", "init", "-y"], cwd=project_path, shell=True, capture_output=True)
print("npm init 完成")

# 安装 vitepress
result = subprocess.run(["npm", "install", "-D", "vitepress"], cwd=project_path, shell=True, capture_output=True)
if result.returncode != 0:
    print(f"安装 vitepress 失败: {result.stderr.decode()}")
else:
    print("vitepress 安装完成")

# 写配置文件
config_content = '''import { defineConfig } from 'vitepress'

export default defineConfig({
  title: '资源导航站',
  description: '海量免费资源下载导航',
  lang: 'zh-CN',
  lastUpdated: true,
  cleanUrls: true,
  head: [
    ['meta', { name: 'theme-color', content: '#3eaf7c' }]
  ],
  themeConfig: {
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
            { text: 'Midjourney教程', link: '/ai/midjourney' }
          ]
        }
      ]
    },
    footer: {
      message: '资源导航站 - 免费资源分享',
      copyright: 'Copyright 2024-present'
    },
    search: {
      provider: 'local'
    }
  }
})
'''

with open(f"{project_path}\\docs\\.vitepress\\config.mts", "w", encoding="utf-8") as f:
    f.write(config_content)

# 写首页
index_content = '''---
layout: home

hero:
  name: "资源导航站"
  text: "超过100T免费资源下载"
  tagline: "免费 · 海量 · 持续更新"
  actions:
    - theme: brand
      text: 开始浏览
      link: /resources
    - theme: alt
      text: GitHub
      link: https://github.com/

features:
  - icon: "🚀"
    title: 完全免费
    details: 所有资源100%免费下载，永无隐藏费用
  - icon: "🔄"
    title: 持续更新
    details: 每日更新最新优质资源，紧跟时代潮流
  - icon: "⭐"
    title: 品质保证
    details: 专业团队精心筛选，严格把关资源质量
  - icon: "🎯"
    title: 分类清晰
    details: 科学的分类体系，帮您快速精准找到所需资源
---

## 平台数据

| 指标 | 数据 |
|------|------|
| 资源总量 | 超过 100TB |
| 分类数量 | 12 个主要类别 |
| 更新频率 | 每日更新 |
'''

with open(f"{project_path}\\docs\\index.md", "w", encoding="utf-8") as f:
    f.write(index_content)

# 写资源页
resources_content = '''# 资源列表

## AI教程

| 资源名称 | 描述 | 下载 |
|---------|------|------|
| ChatGPT从入门到精通 | 完整教程包含提示词工程 | [下载](/ai/chatgpt) |
| Midjourney绘画教程 | AI绘图完整指南 | [下载](/ai/midjourney) |

## 电子书

| 资源名称 | 描述 | 下载 |
|---------|------|------|
| Python编程从入门到实践 | 经典入门书籍 | [下载](#) |
| JavaScript高级程序设计 | 前端必读 | [下载](#) |

## 软件工具

| 资源名称 | 描述 | 下载 |
|---------|------|------|
| Adobe全家桶 | PS/PR/AE等 | [下载](#) |
| Office2024 | 办公套件 | [下载](#) |
'''

with open(f"{project_path}\\docs\\resources.md", "w", encoding="utf-8") as f:
    f.write(resources_content)

# 写关于页
about_content = '''# 关于我们

资源导航站是一个专注于提供免费优质资源下载的开放平台。

## 联系方式

- QQ群: XXXXXXXXX
- 邮箱: contact@example.com
'''

with open(f"{project_path}\\docs\\about.md", "w", encoding="utf-8") as f:
    f.write(about_content)

# 写分类页
ai_content = '''# AI教程

## ChatGPT教程

完整的ChatGPT使用教程，包含基础使用方法、提示词工程技巧。

[点击下载](#)
'''

with open(f"{project_path}\\docs\\ai\\index.md", "w", encoding="utf-8") as f:
    f.write(ai_content)
with open(f"{project_path}\\docs\\ai\\chatgpt.md", "w", encoding="utf-8") as f:
    f.write(ai_content)

# 更新 package.json
pkg_path = f"{project_path}\\package.json"
with open(pkg_path, "r", encoding="utf-8") as f:
    pkg = json.load(f)

pkg["scripts"] = {
    "docs:dev": "vitepress dev docs",
    "docs:build": "vitepress build docs",
    "docs:preview": "vitepress preview docs"
}

with open(pkg_path, "w", encoding="utf-8") as f:
    json.dump(pkg, f, indent=2)

print("\n" + "="*50)
print("VitePress 项目创建完成!")
print("="*50)
print(f"\n项目位置: {project_path}")
print("\n下一步:")
print(f"  cd {project_path}")
print("  npm run docs:dev     # 本地预览")
print("  npm run docs:build   # 构建静态文件")
