# 打印布局优化 - 2026-04-21

## 问题描述

用户反馈：打印预览时会把网页的出题设置面板也包含进去，但打印时只需要题目内容，而且模板需要按 A4 纸来布局。

## 解决方案

### 1. 页面组件添加打印隐藏类

在 `app/page.tsx` 中为以下区域添加 `print:hidden` 类：
- **导航栏** (197行)：`<nav className="print:hidden fixed...`
- **Hero 区域** (282行)：`<div className="print:hidden pt-24...`
- **高级配置面板** (449行)：`<div className="print:hidden ${hasGenerated...`
- **预览工具栏** (685行)：`<div className="print:hidden flex...`

### 2. 全局打印样式优化

更新 `app/globals.css` 的 `@media print` 规则：
- Tailwind `print:hidden` 类支持
- 隐藏所有固定元素（导航、弹窗）
- 隐藏按钮和输入控件
- 页面容器重置（去除 padding/margin）
- 工作表容器去掉圆角和阴影
- A4 尺寸强制（210mm × 297mm）
- 分页控制（`page-break-after: always`）

### 3. PDF 导出白色背景修复

同时修复了 PDF 导出时的白色背景问题：
- 导出前临时设置元素背景为白色
- 创建白色 canvas 确保无透明问题
- 使用 PNG 格式导出

## Git Commits

| Commit | 说明 |
|--------|------|
| `3be1d72` | 字帖生成器 PDF 白色背景 |
| `559e6ab` | 数学练习卷 PDF 白色背景 |
| `0cd6f0a` | 打印时隐藏控制面板 |
| `72f84f0` | 优化打印样式 |

## 打印效果

打印预览时：
- ✅ 只显示题目内容
- ✅ A4 纸尺寸正确
- ✅ 白色背景
- ✅ 无控制面板干扰

## 使用方式

1. 点击「立即出题」生成练习卷
2. 点击「打印预览」或按 `Ctrl+P`
3. 在打印对话框中选择打印机或保存为 PDF
