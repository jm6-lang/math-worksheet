# 修复curriculum索引页不显示新资源

**问题：** curriculum/index.md 是静态硬编码的表格，只列到 post_106，新添加的 post_132-155 不在索引页显示

**根因：** VitePress 索引页不是动态扫描生成的，新增文件不会自动出现在列表中

**解决方案：**
1. 创建 `scripts/gen_index.mjs` 脚本，扫描目录下所有 post_*.md 文件，从文件内容提取标题和平台，重新生成 index.md 表格
2. 重新生成 curriculum/index.md，现在包含 140 个条目

**结果：**
- Commit: aaef9ca，CI 构建成功
- 所有资源（post_001 ~ post_155）现在都能在索引页看到
