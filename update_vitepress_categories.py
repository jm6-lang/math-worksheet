import os

base = "C:\\resource-nav\\docs"

# 创建更多分类目录
categories = ["ai", "books", "tools", "media", "education", "money", "design", "coding", "fitness", "music"]
for cat in categories:
    os.makedirs(f"{base}\\{cat}", exist_ok=True)

# AI分类页
ai_index = '''# 🤖 AI人工智能教程

> AI时代已来，掌握AI工具就是掌握未来

## 热门资源

### ChatGPT系列

| 资源名称 | 描述 | 大小 |
|---------|------|------|
| [ChatGPT从入门到精通](/ai/chatgpt) | 完整教程，含提示词工程 | 2.3GB |
| [ChatGPT提示词大全](/ai/prompts) | 10000+优质提示词模板 | 50MB |
| [ChatGPT API开发教程](/ai/api) | Python调用API实战 | 1GB |
| [ChatGPT商业变现指南](/ai/business) | 用AI赚钱的N种方式 | 800MB |

### AI绘画系列

| 资源名称 | 描述 | 大小 |
|---------|------|------|
| [Midjourney完全教程](/ai/midjourney) | 从入门到精通 | 4.5GB |
| [Stable Diffusion本地部署](/ai/sd) | 含模型资源包 | 20GB |
| [DALL·E 3 使用教程](/ai/dalle) | OpenAI最新绘画AI | 2GB |
| [AI绘画提示词宝典](/ai/art-prompts) | 风格参数详解 | 200MB |

### AI工具集合

| 工具名称 | 用途 | 链接 |
|---------|------|------|
| ChatGPT | 对话问答 | [官网](https://chat.openai.com) |
| Claude | 长文本处理 | [官网](https://claude.ai) |
| Midjourney | AI绘画 | [官网](https://midjourney.com) |
| Runway | AI视频 | [官网](https://runway.ml) |
| ElevenLabs | AI配音 | [官网](https://elevenlabs.io) |

## 分类导航

- [ChatGPT教程](/ai/chatgpt)
- [Midjourney教程](/ai/midjourney)
- [Stable Diffusion](/ai/sd)
- [AI提示词](/ai/prompts)
'''

with open(f"{base}\\ai\\index.md", "w", encoding="utf-8") as f:
    f.write(ai_index)

# ChatGPT详情页
chatgpt = '''# ChatGPT从入门到精通

![ChatGPT](/images/chatgpt-banner.png)

## 课程简介

这是一套完整的ChatGPT使用教程，从注册账号到高级应用，帮助你全面掌握这个强大的AI工具。

## 课程目录

### 第一章：ChatGPT入门
1. 什么是ChatGPT
2. 如何注册ChatGPT账号
3. ChatGPT界面介绍
4. 基础对话技巧

### 第二章：提示词工程
1. 什么是提示词工程
2. 提示词的基本结构
3. 常用提示词模板
4. 提示词优化技巧

### 第三章：高级应用
1. 角色扮演技巧
2. 多轮对话管理
3. 知识库问答
4. 代码辅助开发

### 第四章：API开发
1. OpenAI API入门
2. Python调用示例
3. 构建聊天机器人
4. 成本优化策略

### 第五章：商业变现
1. AI写作接单
2. AI咨询培训
3. AI产品开发
4. 变现案例分析

## 下载信息

| 网盘 | 链接 | 提取码 |
|------|------|--------|
| 夸克网盘 | [点击下载](#) | 无 |
| 阿里网盘 | [点击下载](#) | abcd |
| 百度网盘 | [点击下载](#) | efgh |

## 注意事项

::: warning 提示
- 请使用电脑端下载，手机端可能无法正常解压
- 建议使用夸克网盘，下载速度更快
- 如遇链接失效，请留言反馈
:::

[← 返回AI教程列表](/ai/)
'''

with open(f"{base}\\ai\\chatgpt.md", "w", encoding="utf-8") as f:
    f.write(chatgpt)

# 电子书分类
books_index = '''# 📚 电子书籍

> 海量电子书资源，覆盖各行各业

## 分类导航

### 编程技术
| 分类 | 数量 | 链接 |
|------|------|------|
| Python编程 | 200+ | [查看](/books/python) |
| JavaScript/前端 | 150+ | [查看](/books/frontend) |
| Java后端 | 100+ | [查看](/books/java) |
| 数据库 | 80+ | [查看](/books/database) |
| 人工智能 | 120+ | [查看](/books/ai) |
| 算法与数据结构 | 50+ | [查看](/books/algorithm) |

### 设计创意
| 分类 | 数量 | 链接 |
|------|------|------|
| UI/UX设计 | 100+ | [查看](/books/ui) |
| 平面设计 | 80+ | [查看](/books/graphic) |
| 室内设计 | 50+ | [查看](/books/interior) |
| 设计理论 | 40+ | [查看](/books/design-theory) |

### 商业管理
| 分类 | 数量 | 链接 |
|------|------|------|
| 创业投资 | 100+ | [查看](/books/startup) |
| 市场营销 | 80+ | [查看](/books/marketing) |
| 人力资源 | 50+ | [查看](/books/hr) |
| 财务管理 | 60+ | [查看](/books/finance) |

### 文学小说
| 分类 | 数量 | 链接 |
|------|------|------|
| 中国文学 | 500+ | [查看](/books/chinese) |
| 外国文学 | 300+ | [查看](/books/foreign) |
| 网络小说 | 1000+ | [查看](/books/webnovel) |
| 科幻奇幻 | 200+ | [查看](/books/scifi) |

## 热门推荐

| 书名 | 作者 | 分类 |
|------|------|------|
| Python编程从入门到实践 | Eric Matthes | 编程 |
| 深入理解计算机系统 | Randal E.Bryant | 编程 |
| 设计心理学 | 唐纳德·诺曼 | 设计 |
| 从0到1 | 彼得·蒂尔 | 商业 |
| 百年孤独 | 加西亚·马尔克斯 | 文学 |
'''

with open(f"{base}\\books\\index.md", "w", encoding="utf-8") as f:
    f.write(books_index)

# 软件工具分类
tools_index = '''# 💻 软件工具

> 精选常用软件，满足工作生活需求

## 办公软件

| 软件名称 | 版本 | 大小 | 下载 |
|---------|------|------|------|
| Microsoft Office 2024 | 专业增强版 | 4GB | [下载](#) |
| WPS Office 2024 | 专业版 | 500MB | [下载](#) |
| Adobe Acrobat Pro 2024 | PDF编辑 | 800MB | [下载](#) |
| XMind 2024 | 思维导图 | 200MB | [下载](#) |

## 设计软件

| 软件名称 | 版本 | 大小 | 下载 |
|---------|------|------|------|
| Adobe Photoshop 2024 | 图像处理 | 2GB | [下载](#) |
| Adobe Illustrator 2024 | 矢量设计 | 1.5GB | [下载](#) |
| Adobe Premiere Pro 2024 | 视频剪辑 | 2GB | [下载](#) |
| Adobe After Effects 2024 | 特效制作 | 2.5GB | [下载](#) |
| Figma | UI设计 | 在线使用 | [官网](https://figma.com) |
| Sketch | UI设计 | Mac版 | [下载](#) |

## 开发工具

| 软件名称 | 用途 | 大小 | 下载 |
|---------|------|------|------|
| VS Code | 代码编辑器 | 100MB | [官网](https://code.visualstudio.com) |
| WebStorm | 前端IDE | 300MB | [下载](#) |
| PyCharm | Python IDE | 400MB | [下载](#) |
| IntelliJ IDEA | Java IDE | 500MB | [下载](#) |
| Git | 版本控制 | 50MB | [官网](https://git-scm.com) |
| Docker | 容器工具 | 500MB | [官网](https://docker.com) |

## 系统工具

| 软件名称 | 用途 | 大小 | 下载 |
|---------|------|------|------|
| 7-Zip | 解压缩 | 1MB | [官网](https://7-zip.org) |
| Everything | 文件搜索 | 2MB | [官网](https://voidtools.com) |
| Geek Uninstaller | 软件卸载 | 3MB | [官网](https://geekuninstaller.com) |
| Snipaste | 截图工具 | 10MB | [官网](https://snipaste.com) |
| uTools | 效率工具 | 50MB | [官网](https://u.tools) |

## 下载须知

::: info 提示
- 部分软件为破解版，仅供学习研究使用
- 请支持正版软件，商业用途请购买授权
- 下载后请自行查毒，确保安全
:::
'''

with open(f"{base}\\tools\\index.md", "w", encoding="utf-8") as f:
    f.write(tools_index)

# 网赚副业分类
money_index = '''# 💰 网赚副业

> 真正可落地的副业项目，帮你实现被动收入

## 自媒体运营

| 项目名称 | 描述 | 难度 | 教程 |
|---------|------|------|------|
| 短视频运营全攻略 | 抖音/快手从0到1 | ⭐⭐ | [查看](#) |
| 小红书运营实操 | 变现全流程 | ⭐⭐ | [查看](#) |
| 公众号运营变现 | 从涨粉到接广告 | ⭐⭐⭐ | [查看](#) |
| B站UP主成长指南 | 视频创作与变现 | ⭐⭐ | [查看](#) |
| 直播带货话术大全 | 抖音/快手直播 | ⭐⭐ | [查看](#) |

## 电商运营

| 项目名称 | 描述 | 难度 | 教程 |
|---------|------|------|------|
| 淘宝无货源开店 | 零库存电商模式 | ⭐⭐⭐ | [查看](#) |
| 亚马逊跨境电商 | 从注册到出单 | ⭐⭐⭐⭐ | [查看](#) |
| 拼多多运营攻略 | 低成本流量获取 | ⭐⭐ | [查看](#) |
| 抖音小店运营 | 短视频+电商 | ⭐⭐⭐ | [查看](#) |
| TikTok跨境电商 | 海外版抖音 | ⭐⭐⭐⭐ | [查看](#) |

## 知识付费

| 项目名称 | 描述 | 难度 | 教程 |
|---------|------|------|------|
| 在线课程制作 | 从选题到上线 | ⭐⭐⭐ | [查看](#) |
| 付费社群运营 | 打造知识社群 | ⭐⭐⭐ | [查看](#) |
| 电子书出版 | Kindle等平台 | ⭐⭐ | [查看](#) |
| 知识IP打造 | 个人品牌建设 | ⭐⭐⭐ | [查看](#) |

## 其他副业

| 项目名称 | 描述 | 预期收入 |
|---------|------|---------|
| AI写作接单 | 用ChatGPT接单 | 500-5000/月 |
| 视频剪辑接单 | 短视频剪辑 | 1000-10000/月 |
| 设计外包 | Logo/海报设计 | 2000-20000/月 |
| 代写文案 | 公众号/小红书文案 | 500-3000/月 |
| 数据标注 | AI训练数据标注 | 1000-3000/月 |

## 副业建议

::: tip 重要提醒
- 任何声称"躺赚"的项目都是骗局
- 副业需要持续投入时间和精力
- 选择与自己技能匹配的项目
- 不要辞职全职做副业，先当尝试
:::
'''

with open(f"{base}\\money\\index.md", "w", encoding="utf-8") as f:
    f.write(money_index)

# 编程开发分类
coding_index = '''# 💻 编程开发教程

> 从零基础到大厂，系统化学习路径

## 前端开发

| 教程名称 | 技术栈 | 难度 | 下载 |
|---------|--------|------|------|
| HTML+CSS零基础入门 | HTML5/CSS3 | ⭐ | [下载](#) |
| JavaScript从入门到精通 | ES6+ | ⭐⭐ | [下载](#) |
| Vue3全家桶实战 | Vue3+Pinia+Router | ⭐⭐⭐ | [下载](#) |
| React18实战教程 | React+Redux+TS | ⭐⭐⭐ | [下载](#) |
| TypeScript深入浅出 | TypeScript | ⭐⭐ | [下载](#) |
| 前端工程化实战 | Webpack/Vite | ⭐⭐⭐ | [下载](#) |

## 后端开发

| 教程名称 | 技术栈 | 难度 | 下载 |
|---------|--------|------|------|
| Python全栈开发 | Python/Django | ⭐⭐ | [下载](#) |
| Java企业级开发 | Spring Boot | ⭐⭐⭐ | [下载](#) |
| Go语言实战 | Gin/GORM | ⭐⭐ | [下载](#) |
| Node.js后端开发 | Express/Nest.js | ⭐⭐ | [下载](#) |
| 数据库设计优化 | MySQL/Redis | ⭐⭐⭐ | [下载](#) |

## 移动开发

| 教程名称 | 技术栈 | 难度 | 下载 |
|---------|--------|------|------|
| Flutter跨平台开发 | Flutter/Dart | ⭐⭐⭐ | [下载](#) |
| React Native实战 | RN+TypeScript | ⭐⭐⭐ | [下载](#) |
| Android原生开发 | Kotlin | ⭐⭐⭐ | [下载](#) |
| iOS原生开发 | Swift | ⭐⭐⭐⭐ | [下载](#) |

## 人工智能

| 教程名称 | 技术栈 | 难度 | 下载 |
|---------|--------|------|------|
| 机器学习入门 | Python/Sklearn | ⭐⭐ | [下载](#) |
| 深度学习实战 | PyTorch | ⭐⭐⭐ | [下载](#) |
| NLP自然语言处理 | Transformers | ⭐⭐⭐ | [下载](#) |
| 计算机视觉 | OpenCV/YOLO | ⭐⭐⭐ | [下载](#) |
| 大模型开发实战 | LangChain/LLM | ⭐⭐⭐⭐ | [下载](#) |

## 学习路径

```
前端路线: HTML/CSS → JavaScript → Vue/React → 工程化 → 全栈
后端路线: 基础语法 → Web框架 → 数据库 → 微服务 → 架构设计
AI路线: Python基础 → 机器学习 → 深度学习 → 大模型应用
```
'''

with open(f"{base}\\coding\\index.md", "w", encoding="utf-8") as f:
    f.write(coding_index)

print("所有分类页面创建完成！")
print(f"创建了 {len(categories)} 个分类目录")
