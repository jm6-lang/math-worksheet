'use client';

import Link from 'next/link';
import { articles } from '../data';
import SiteLayout from '@/app/_components/SiteLayout';

interface BlogPostPageProps {
  slug: string;
}

function parseMarkdown(markdown: string): string {
  let html = markdown;

  // Headers: ## and ###
  html = html.replace(/^### (.+)$/gm, '<h3 class="text-lg font-bold text-white mt-8 mb-3">$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2 class="text-xl font-bold text-white mt-8 mb-4">$1</h2>');

  // Bold: **text**
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong class="text-white font-semibold">$1</strong>');

  // Italic: *text*
  html = html.replace(/(?<!\*)\*([^*]+?)\*(?!\*)/g, '<em>$1</em>');

  // Code blocks: ~~~...~~~ or ```...```
  html = html.replace(/~~~([\s\S]*?)~~~/g, '<pre class="bg-slate-900 border border-white/10 rounded-xl p-4 my-4 overflow-x-auto"><code class="text-sm text-green-400">$1</code></pre>');
  html = html.replace(/```([\s\S]*?)```/g, '<pre class="bg-slate-900 border border-white/10 rounded-xl p-4 my-4 overflow-x-auto"><code class="text-sm text-green-400">$1</code></pre>');

  // Inline code: `code`
  html = html.replace(/`([^`]+?)`/g, '<code class="bg-slate-700 px-1.5 py-0.5 rounded text-sm text-blue-300">$1</code>');

  // Unordered lists: - item
  html = html.replace(/^- (.+)$/gm, '<li class="text-gray-300 leading-relaxed ml-4 list-disc">$1</li>');

  // Ordered lists: 1. item
  html = html.replace(/^\d+\. (.+)$/gm, '<li class="text-gray-300 leading-relaxed ml-4 list-decimal">$1</li>');

  // Table rows
  html = html.replace(/^\|(.+)\|$/gm, (match) => {
    const cells = match.split('|').filter(c => c.trim());
    if (cells.every(c => /^[\s-:]+$/.test(c))) {
      return '<!-- table separator -->';
    }
    const cellHtml = cells.map(c => `<td class="border border-white/10 px-3 py-2 text-gray-300 text-sm">${c.trim()}</td>`).join('');
    return `<tr>${cellHtml}</tr>`;
  });

  // Wrap consecutive <tr> in table
  html = html.replace(/((?:<tr>[\s\S]*?<\/tr>\s*)+)/g, '<table class="w-full border-collapse my-4 rounded-xl overflow-hidden">$1</table>');

  // Paragraphs: lines that are not already wrapped in HTML tags
  const lines = html.split('\n');
  const result: string[] = [];
  for (const line of lines) {
    const trimmed = line.trim();
    if (
      trimmed === '' ||
      trimmed.startsWith('<h') ||
      trimmed.startsWith('<li') ||
      trimmed.startsWith('<tr') ||
      trimmed.startsWith('<table') ||
      trimmed.startsWith('</table') ||
      trimmed.startsWith('<!--') ||
      trimmed.startsWith('<pre') ||
      trimmed.startsWith('<div')
    ) {
      result.push(line);
    } else {
      result.push(`<p class="text-gray-300 leading-relaxed mb-4">${trimmed}</p>`);
    }
  }

  return result.join('\n');
}

export default function BlogPostPage({ slug }: BlogPostPageProps) {
  const article = articles.find(a => a.id === slug);

  if (!article) {
    return (
      <SiteLayout>
        <div className="text-center py-20">
          <p className="text-gray-400 text-xl mb-4">文章未找到</p>
          <Link
            href="/blog"
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
          >
            返回博客列表
          </Link>
        </div>
      </SiteLayout>
    );
  }

  const categoryColors: Record<string, string> = {
    '数学学习': 'bg-blue-500/20 text-blue-300',
    '语文学习': 'bg-emerald-500/20 text-emerald-300',
    '英语学习': 'bg-rose-500/20 text-rose-300',
    '思维训练': 'bg-orange-500/20 text-orange-300',
    '学习方法': 'bg-purple-500/20 text-purple-300',
    '升学指导': 'bg-yellow-500/20 text-yellow-300',
    '工具推荐': 'bg-teal-500/20 text-teal-300',
    '关于我们': 'bg-pink-500/20 text-pink-300',
  };

  // Related articles: same category, excluding current
  const relatedArticles = articles
    .filter(a => a.category === article.category && a.id !== article.id)
    .slice(0, 3);

  return (
    <SiteLayout>
      <article className="max-w-3xl mx-auto px-4 py-12">
        {/* Breadcrumb */}
        <nav className="mb-8 text-sm">
          <ol className="flex items-center gap-2 text-gray-400">
            <li>
              <a href="/" className="hover:text-white transition-colors">首页</a>
            </li>
            <li>/</li>
            <li>
              <Link href="/blog" className="hover:text-white transition-colors">教育博客</Link>
            </li>
            <li>/</li>
            <li className="text-gray-300 truncate max-w-[200px]">{article.title}</li>
          </ol>
        </nav>

        {/* Article Header */}
        <header className="mb-10">
          <div className="flex items-center gap-3 mb-4">
            <span className={`px-3 py-1 rounded-full text-xs font-medium ${categoryColors[article.category] || 'bg-gray-500/20 text-gray-300'}`}>
              {article.category}
            </span>
            <span className="text-gray-500 text-sm">{article.readTime}</span>
          </div>
          <h1 className="text-2xl md:text-3xl font-bold text-white mb-4 leading-tight">
            {article.title}
          </h1>
          <div className="flex items-center gap-4 text-sm text-gray-500">
            <time>{article.date}</time>
          </div>
        </header>

        {/* Article Content */}
        <div
          className="prose prose-invert max-w-none"
          dangerouslySetInnerHTML={{ __html: parseMarkdown(article.content) }}
        />

        {/* Back Button & Related Articles */}
        <div className="mt-12 pt-8 border-t border-white/10">
          <Link
            href="/blog"
            className="inline-flex items-center gap-2 px-6 py-3 bg-slate-800 hover:bg-slate-700 border border-white/10 text-gray-300 hover:text-white rounded-xl transition-colors"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            返回博客列表
          </Link>

          {/* Related Articles */}
          {relatedArticles.length > 0 && (
            <div className="mt-10">
              <h3 className="text-lg font-bold text-white mb-4">相关文章推荐</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {relatedArticles.map((related) => (
                  <Link
                    key={related.id}
                    href={`/blog/${related.id}`}
                    className="bg-slate-800/50 border border-white/10 rounded-xl p-4 hover:border-white/20 hover:bg-slate-700/50 transition-all group"
                  >
                    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium mb-2 ${categoryColors[related.category] || 'bg-gray-500/20 text-gray-300'}`}>
                      {related.category}
                    </span>
                    <h4 className="text-sm font-medium text-white group-hover:text-blue-400 transition-colors leading-snug line-clamp-2">
                      {related.title}
                    </h4>
                    <p className="text-gray-500 text-xs mt-2">{related.readTime}</p>
                  </Link>
                ))}
              </div>
            </div>
          )}
        </div>
      </article>
    </SiteLayout>
  );
}
