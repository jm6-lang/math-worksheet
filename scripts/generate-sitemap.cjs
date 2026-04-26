/**
 * 构建 sitemap.xml 的脚本
 * 从 toolRegistry.ts 和 blog/data.ts 读取数据，生成静态 sitemap.xml
 * 用法：node scripts/generate-sitemap.cjs
 */
const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://www.skillxm.cn';
const today = new Date().toISOString().split('T')[0];

// 工具列表（与 toolRegistry.ts 保持同步）
const TOOLS = [
  { path: '/tools/math-worksheet', priority: 0.9 },
  { path: '/tools/calligraphy', priority: 0.9 },
  { path: '/tools/english-calligraphy', priority: 0.9 },
  { path: '/tools/sudoku', priority: 0.9 },
  { path: '/tools/pinyin', priority: 0.8 },
  { path: '/tools/mental-math', priority: 0.9 },
  { path: '/tools/flashcards', priority: 0.9 },
  { path: '/tools/writing-template', priority: 0.9 },
  { path: '/tools/poem-memo', priority: 0.9 },
  { path: '/tools/unit-test', priority: 0.9 },
];

// 资源子页面
const RESOURCES = [
  'calligraphy', 'textbook', 'math', 'chinese', 'english',
  'history', 'language', 'junior', 'senior', 'method', 'comprehensive',
];

// 博客文章（从 data.ts 提取 id）
const blogDataPath = path.join(__dirname, '..', 'app', 'blog', 'data.ts');
const blogContent = fs.readFileSync(blogDataPath, 'utf-8');
const idMatches = blogContent.matchAll(/id:\s*['"]([^'"]+)['"]/g);
const blogIds = [...idMatches].map(m => m[1]);

function url(loc, lastmod, changefreq, priority) {
  return `  <url>
    <loc>${BASE_URL}${loc}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>${changefreq}</changefreq>
    <priority>${priority}</priority>
  </url>`;
}

const lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'];

// 静态页面
lines.push(url('/', today, 'daily', '1.0'));
lines.push(url('/blog', today, 'weekly', '0.9'));
lines.push(url('/resources', '2026-04-23', 'weekly', '0.9'));

// 资源子页面
RESOURCES.forEach(slug => {
  lines.push(url(`/resources/${slug}`, '2026-04-23', 'weekly', '0.8'));
});

// 工具页面
TOOLS.forEach(tool => {
  lines.push(url(tool.path, today, 'weekly', tool.priority));
});

// 博客文章
blogIds.forEach(id => {
  lines.push(url(`/blog/${id}`, '2026-04-23', 'monthly', '0.7'));
});

lines.push('</urlset>');

const outputPath = path.join(__dirname, '..', 'public', 'sitemap.xml');
fs.writeFileSync(outputPath, lines.join('\n') + '\n', 'utf-8');
console.log(`✅ sitemap.xml generated: ${blogIds.length + TOOLS.length + RESOURCES.length + 3} URLs`);
