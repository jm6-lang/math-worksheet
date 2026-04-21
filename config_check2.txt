import { defineConfig } from 'vitepress'
import fs from 'node:fs'
import path from 'node:path'

function getSidebarItems(dir: string) {
  const fullPath = path.join(process.cwd(), 'docs', dir)
  if (!fs.existsSync(fullPath)) return []
  const files = fs.readdirSync(fullPath)
    .filter(file => file.endsWith('.md') && file !== 'index.md')
    .sort()

  return files.map(file => {
    const filePath = path.join(fullPath, file)
    const content = fs.readFileSync(filePath, 'utf-8')
    const match = content.match(/^#\s+(.+)$/m)
    const name = match ? match[1].trim() : path.basename(file, '.md')
    return {
      text: name,
      link: `/${dir}/${path.basename(file, '.md')}.html`
    }
  })
}

function getSidebarItemsWithDir(dir: string, subDir: string) {
  const fullPath = path.join(process.cwd(), 'docs', dir, subDir)
  if (!fs.existsSync(fullPath)) return []
  const files = fs.readdirSync(fullPath)
    .filter(file => file.endsWith('.md') && file !== 'index.md')
    .sort()

  return files.map(file => {
    const filePath = path.join(fullPath, file)
    const content = fs.readFileSync(filePath, 'utf-8')
    const match = content.match(/^#\s+(.+)$/m)
    const name = match ? match[1].trim() : path.basename(file, '.md')
    return {
      text: name,
      link: `/${dir}/${subDir}/${path.basename(file, '.md')}.html`
    }
  })
}

export default defineConfig({
  base: process.env.BASE || '/',
  title: "小二郎资源分享站",
  titleTemplate: "全网优质资源聚合平台",
  lang: 'zh-CN',
  lastUpdated: true,
  cleanUrls: true,
  ignoreDeadLinks: true,
  description: "小二郎资源分享站：全网最全的 200TB+ 免费资源下载站，包含 AI 知识、精品书籍、跨境电商、自媒体、教育、健康、影视、提效工具等分类资源，每日持续更新。",

  sitemap: {
    hostname: 'https://docs.skillxm.cn'
  },

  head: [
    ['link', { rel: 'icon', href: '/favicon.png' }],
    ['script', { async: '', src: 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4710405779358793', crossorigin: 'anonymous' }],
    ['script', {}, `
      (function() {
        var link = document.createElement('link');
        link.rel = 'canonical';
        link.href = window.location.protocol + '//' + window.location.host + window.location.pathname;
        document.head.appendChild(link);
      })();
    `],
    ['script', { async: '', src: 'https://busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js' }]
  ],

  themeConfig: {
    logo: { src: '/logo.png', alt: '小二郎资源分享站 Logo' },
    nav: [
      { text: '🏠 首页', link: '/' },
      {
        text: '📂 资源中心',
        items: [
          { text: '🤖 AI 知识', link: '/AIknowledge/' },
          { text: '📚 精品书籍', link: '/book/',
            items: [
              { text: '📚 全部内容', link: '/book/' },
              { text: '📖 古籍文献', link: '/book/book/' },
              { text: '🎭 传统文化', link: '/book/culture/' },
              { text: '🩺 中医合集', link: '/book/tcm/' }
            ]
          },
          { text: '🎬 影视娱乐', link: '/movies/' },
          { text: '📉 跨境电商', link: '/self-media/' },
          { text: '🎓 学习课程', link: '/curriculum/' },
          { text: '🍎 教育资源', link: '/edu-knowlege/' },
          { text: '🛠️ 软件工具', link: '/tools/' },
          { text: '🏛️ 传统文化', link: '/chinese-traditional/' },
        ]
      },
      { text: '🗺️ 资源导航', link: '/nav/' },
      { text: '💎 独家资源', link: '/exclusive/' }
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/jm6-lang/resource-portal' }
    ],
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索海量资源...' },
          modal: { noResultsText: '未找到相关资源' }
        }
      }
    },
    sidebar: [
      {
        text: '📖 资源导航',
        items: [
          { text: '🗺️ 导航首页', collapsed: false, items: [{ text: '🗺️ 全部资源索引', link: '/nav/' }] },
          { text: '💎 独家资源专区', collapsed: false, items: [{ text: '✨ 专区首页', link: '/exclusive/' }, { text: '💳 注册卡采购', link: '/exclusive/registration-card.html' }, { text: '🛠️ 电话标记清除', link: '/exclusive/phone-label-clean.html' }] },
          { text: '🤖 AI 知识专区', collapsed: true, items: [{ text: '✨ 全部内容', link: '/AIknowledge/' }, ...getSidebarItems('AIknowledge')] },
          { text: '📚 书籍文献库', collapsed: true, items: [
            { text: '✨ 全部内容', link: '/book/' },
            { text: '📖 古籍文献', collapsed: false, items: [{ text: '📖 古籍文献首页', link: '/book/book/' }, ...getSidebarItemsWithDir('book', 'book')] },
            { text: '🎭 传统文化', collapsed: false, items: [{ text: '🎭 传统文化首页', link: '/book/culture/' }, ...getSidebarItemsWithDir('book', 'culture')] },
            { text: '🩺 中医合集', collapsed: false, items: [{ text: '🩺 中医合集首页', link: '/book/tcm/' }, ...getSidebarItemsWithDir('book', 'tcm')] },
            ...getSidebarItems('book')
          ] },
          { text: '🎬 在线影视/音乐', collapsed: true, items: [{ text: '✨ 全部内容', link: '/movies/' }, ...getSidebarItems('movies')] },
          { text: '📈 自媒体/电商专栏', collapsed: true, items: [{ text: '✨ 全部内容', link: '/self-media/' }, ...getSidebarItems('self-media')] },
          { text: '🎓 最新互联网项目教程', collapsed: true, items: [{ text: '✨ 全部内容', link: '/curriculum/' }, ...getSidebarItems('curriculum')] },
          { text: '🍎 教育资料馆', collapsed: true, items: [{ text: '✨ 全部内容', link: '/edu-knowlege/' }, ...getSidebarItems('edu-knowlege')] },
          { text: '🛠️ 常用工具/会员版', collapsed: true, items: [{ text: '✨ 全部内容', link: '/tools/' }, ...getSidebarItems('tools')] },
          { text: '🏛️ 传统文化阁', collapsed: true, items: [{ text: '✨ 全部内容', link: '/chinese-traditional/' }, ...getSidebarItems('chinese-traditional')] },
        ]
      }
    ],
    footer: {
      message: '<a href="https://docs.skillxm.cn/about">关于我们</a> | <a href="https://docs.skillxm.cn/disclaimer">免责声明</a> | <a href="https://docs.skillxm.cn/privacy">隐私政策</a> | <a href="https://docs.skillxm.cn/contact">联系我们</a> | <a href="https://docs.skillxm.cn/links">友情链接</a> | <a href="https://docs.skillxm.cn/ads">广告合作</a><br>友情链接：<a href="https://skillxm.cn" target="_blank">skillxm.cn</a> | <a href="https://tool.skillxm.cn" target="_blank">tool.skillxm.cn</a>',
      copyright: 'Copyright © 2026-present 小二郎资源分享站'
    },
    lastUpdatedText: '最近更新于',
    darkModeSwitchLabel: '深色模式切换',
    outlineTitle: '本页目录',
    sidebarMenuLabel: '菜单',
    returnToTopLabel: '返回顶部',
  }
})
