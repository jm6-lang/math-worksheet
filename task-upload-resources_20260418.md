# 2026-04-18 互联网项目教程资源上传

## 任务
用户要求将24个夸克网盘资源上传到 resource-portal 的"最新互联网项目教程"分类（curriculum 目录）。

## 执行
- 在 `docs/curriculum/` 下创建了24个文件（post_108.md 到 post_131.md）
- 每个文件包含：frontmatter（title/description/keywords）、资源导读、资源详情、下载链接、版权申明
- 标题和链接来自用户提供的清单，分类和详细描述由AI生成
- 覆盖分类：财商理财、副业赚钱、自媒体运营、职场技能、电商运营、创业指导、流量获取

## 状态
- ✅ 本地 commit: a200441 "feat(curriculum): 新增24个互联网项目教程资源(post_108-131)"
- ❌ git push 失败（GitHub 443端口超时），commit 仅保存在本地

## 待办
- 网络恢复后执行 `git push`
- 之前未推送的 commit（删除42个空文件 02d1846）也需要一并推送

## 之前的规则
- 紫微斗数页面和独家资源板块不可删除或修改（已写入 MEMORY.md）
