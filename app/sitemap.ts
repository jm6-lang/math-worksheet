import type { MetadataRoute } from 'next';
import { articles } from './blog/data';
import { TOOLS } from '@/lib/toolRegistry';

// output: "export" 模式下需要声明为静态生成
export const dynamic = 'force-static';

const BASE_URL = 'https://www.skillxm.cn';

export default function sitemap(): MetadataRoute.Sitemap {
  const today = new Date().toISOString().split('T')[0];

  // 静态页面
  const staticPages: MetadataRoute.Sitemap = [
    { url: BASE_URL, lastModified: today, changeFrequency: 'daily', priority: 1.0 },
    { url: `${BASE_URL}/blog/`, lastModified: today, changeFrequency: 'weekly', priority: 0.9 },
    { url: `${BASE_URL}/about/`, lastModified: today, changeFrequency: 'monthly', priority: 0.5 },
    { url: `${BASE_URL}/contact/`, lastModified: '2026-04-23', changeFrequency: 'monthly', priority: 0.5 },
    { url: `${BASE_URL}/terms/`, lastModified: '2026-04-23', changeFrequency: 'monthly', priority: 0.3 },
    { url: `${BASE_URL}/privacy/`, lastModified: '2026-04-23', changeFrequency: 'monthly', priority: 0.3 },
  ];

  // 工具页面
  const toolPages: MetadataRoute.Sitemap = TOOLS.filter(t => t.active).map(tool => ({
    url: `${BASE_URL}${tool.path}/`,
    lastModified: today,
    changeFrequency: 'weekly' as const,
    priority: tool.priority || 0.8,
  }));

  // 博客文章（自动从 data.ts 读取）
  const blogPages: MetadataRoute.Sitemap = articles.map(article => ({
    url: `${BASE_URL}/blog/${article.id}/`,
    lastModified: article.date,
    changeFrequency: 'monthly' as const,
    priority: 0.7,
  }));

  return [...staticPages, ...toolPages, ...blogPages];
}
