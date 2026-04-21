import os

config = '''import { defineConfig } from 'vitepress'

export default defineConfig({
  title: '资源导航站',
  description: '海量免费资源下载导航 - 超过100T资源分享',
  lang: 'zh-CN',
  lastUpdated: true,
  cleanUrls: true,
  
  head: [
    ['meta', { name: 'theme-color', content: '#3eaf7c' }],
    ['meta', { name: 'keywords', content: '免费资源下载,AI教程,电子书,软件工具,编程教程,副业项目' }],
    ['meta', { property: 'og:title', content: '资源导航站' }],
    ['meta', { property: 'og:description', content: '海量免费资源下载导航' }]
  ],
  
  themeConfig: {
    siteTitle: '资源导航站',
    
    nav: [
      { text: '🏠 首页', link: '/' },
      { text: '📚 资源总览', link: '/resources' },
      { text: '🔥 最新资源', link: '/new' },
      { text: '⭐ 推荐资源', link: '/recommend' },
      {
        text: '📂 分类',
        items: [
          { text: '🤖 AI人工智能', link: '/ai/' },
          { text: '📚 电子书籍', link: '/books/' },
          { text: '💻 软件工具', link: '/tools/' },
          { text: '💰 网赚副业', link: '/money/' },
          { text: '💻 编程开发', link: '/coding/' }
        ]
      },
      { text: 'ℹ️ 关于', link: '/about' }
    ],
    
    sidebar: {
      '/ai/': [
        {
          text: '🤖 AI人工智能',
          items: [
            { text: 'AI教程首页', link: '/ai/' },
            { text: 'ChatGPT教程', link: '/ai/chatgpt' },
            { text: 'Midjourney教程', link: '/ai/midjourney' },
            { text: 'Stable Diffusion', link: '/ai/sd' },
            { text: 'AI提示词大全', link: '/ai/prompts' }
          ]
        }
      ],
      '/books/': [
        {
          text: '📚 电子书籍',
          items: [
            { text: '电子书首页', link: '/books/' },
            { text: '编程书籍', link: '/books/python' },
            { text: '设计书籍', link: '/books/design' },
            { text: '商业书籍', link: '/books/business' }
          ]
        }
      ],
      '/tools/': [
        {
          text: '💻 软件工具',
          items: [
            { text: '软件工具首页', link: '/tools/' }
          ]
        }
      ],
      '/money/': [
        {
          text: '💰 网赚副业',
          items: [
            { text: '网赚副业首页', link: '/money/' }
          ]
        }
      ],
      '/coding/': [
        {
          text: '💻 编程开发',
          items: [
            { text: '编程开发首页', link: '/coding/' }
          ]
        }
      ]
    },
    
    socialLinks: [
      { icon: 'github', link: 'https://github.com/' }
    ],
    
    footer: {
      message: '资源导航站 - 免费资源分享',
      copyright: 'Copyright © 2024-present | 本站资源仅供学习交流'
    },
    
    search: {
      provider: 'local',
      options: {
        translations: {
          button: {
            buttonText: '搜索资源',
            buttonAriaLabel: '搜索资源'
          },
          modal: {
            noResultsText: '没有找到相关资源',
            resetButtonTitle: '清除搜索条件',
            footer: {
              selectText: '选择',
              navigateText: '切换'
            }
          }
        }
      }
    },
    
    outline: {
      label: '目录'
    },
    
    docFooter: {
      prev: '← 上一页',
      next: '下一页 →'
    },
    
    lastUpdated: {
      text: '最后更新于',
      formatOptions: {
        dateStyle: 'short',
        timeStyle: 'short'
      }
    },
    
    editLink: {
      pattern: 'https://github.com/your-repo/edit/main/docs/:path',
      text: '在 GitHub 上编辑此页'
    }
  }
})
'''

with open("C:\\resource-nav\\docs\\.vitepress\\config.mts", "w", encoding="utf-8") as f:
    f.write(config)

print("配置文件已更新")
