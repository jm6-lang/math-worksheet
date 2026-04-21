# 侧边栏去除子分类层级

## 目标
用户要求侧边栏所有分类去掉子分类嵌套，点击大类直接展示全部资源列表，只保留"全部内容"入口。

## 改动
- `docs/.vitepress/config.ts` sidebar 配置：
  - 删除书籍文献库下的古籍文献/传统文化/中医合集三个子分类嵌套
  - 导航首页从 `{ text: '🗺️ 导航首页', collapsed: false, items: [...] }` 简化为直接链接 `{ text: '🗺️ 全部资源索引', link: '/nav/' }`
  - 所有分类统一为：`{ text: '✨ 全部内容', link }` + 扁平资源列表
- 删除 `getSidebarItemsWithDir` 函数（已无引用）

## 状态
- commit `56f5b95` 已提交本地
- GitHub 443端口不通，推送失败，待网络恢复后 `git push`
