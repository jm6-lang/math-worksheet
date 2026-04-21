- **2026-04-14**：记忆系统启用
- **2026-04-17**：成功学习并部署 AI Website Cloner Template（GitHub 11k+ star）为 OpenClaw Skill，路径 `E:\Qclaw\resources\openclaw\config\skills\website-cloner\`，支持通过 browser CDP + AI 分析执行完整网站克隆流程
- **2026-04-19**：为用户创建微信小程序「JM的工具箱」(wx92d88f2ddf8bad27) 完整源码并部署到 GitHub Actions 自动化流水线。关键经验：miniprogram-ci 必须用 JS API（Project + upload）而非 CLI；GitHub Actions 用 Azure 动态 IP 需关闭微信后台 IP 白名单；仓库 jm6-lang/jm-toolbox。wxml模板中不能有JS表达式（Math.pow、三元运算、.findIndex等），必须在JS中预计算。已完成两轮SEO优化：7个新功能（倒计时/二维码/图片压缩/房贷计算/亲戚称谓/颜色识别/手机尺子）+ 全面搜索关键词优化

## 当前项目与关注

- GitHub组织/账号：jm6-lang，维护仓库 resource-portal（基于VitePress的资源门户站点）
- 2026-04-13: 修复resource-portal中紫微斗数排盘功能，根因为iztro CDN bundle需作为函数调用，commit 6384e505fe03443b94627980abf5474317e985cd，CI构建成功并已部署
- 用户拥有网站 https://www.skillxm.cn/，后台账号 admin，密码 Langlang0.；Search Console 报告网页因 noindex 标记无法被编入索引，正在排查SEO问题

## 经验与决策

- iztro库使用UMD模块格式，需调用window.iztro()获取模块对象，再通过iztro.astro.bySolar()或iztro.astro.byLunar()访问API
- **⚠️ 资源分类必须准确**：用户明确要求每次上传资源时，必须根据标题判断正确分类，严禁放错。分类对照：
  - AIknowledge：AI/人工智能/大模型/AIGC/ChatGPT/Claude/Midjourney等
  - book：书籍/电子书/阅读/古籍/文献/词典/百科
  - chinese-traditional：传统文化/紫微斗数/八字/风水/命理/国学/中医古籍
  - curriculum：学习课程/职场技能/考研考公/编程课/设计课/PPT/Excel等
  - edu-knowlege：教育资料/考试/试题/真题/教材/四六级/雅思托福/幼教
  - movies：在线影视/音乐/电影/剧集/动漫/综艺/歌单/播放器/追剧
  - self-media：自媒体/电商/抖音/小红书/闲鱼/淘宝/直播带货/涨粉/变现/副业/赚钱项目
  - tools：常用工具/会员版/VIP/破解/软件/插件/办公/网盘/VPN/Adobe/Office
  - healthy：健康/养生/健身/减肥/瑜伽/冥想
  - cross-border：跨境电商/Amazon/Shopify/外贸
- 容易混淆的边界：会员版软件→tools（不是原分类），变现/副业/电商项目→self-media（不是curriculum），雅思托福→edu-knowlege（不是tools），音乐合集→movies（不是curriculum）

## ⚠️ 绝对禁区 — 不可删除或修改

维护 resource-portal 时，**严禁**对以下内容做任何删除、修改或批量操作：
- **紫微斗数页面**：`docs/chinese-traditional/ziwei.md` 及其相关组件 `ZiWeiCalculator.vue`
- **独家资源板块**：该分类下的所有页面和数据，包括 `docs/` 下对应目录的所有 .md 文件

违反此规则的操作包括但不限于：清理重复文件、删除无效链接、批量重命名、扫描脚本等。
