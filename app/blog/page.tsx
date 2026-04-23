'use client';

import { useState, useEffect } from 'react';
import { articles, categories } from './data';
import type { Category } from './data';
import BlogPost from './_components/BlogPost';

const categoryColors: Record<string, string> = {
  '数学学习': 'bg-blue-500/20 text-blue-300 border-blue-500/30',
  '语文学习': 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
  '英语学习': 'bg-rose-500/20 text-rose-300 border-rose-500/30',
  '思维训练': 'bg-orange-500/20 text-orange-300 border-orange-500/30',
  '学习方法': 'bg-purple-500/20 text-purple-300 border-purple-500/30',
  '升学指导': 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
  '工具推荐': 'bg-teal-500/20 text-teal-300 border-teal-500/30',
  '关于我们': 'bg-pink-500/20 text-pink-300 border-pink-500/30',
};

export default function BlogPage() {
  const [activeCategory, setActiveCategory] = useState<Category>('全部');
  const [activeArticleId, setActiveArticleId] = useState<string | null>(null);

  useEffect(() => {
    const handleHash = () => {
      const hash = window.location.hash.replace('#', '');
      if (hash) {
        setActiveArticleId(hash);
      } else {
        setActiveArticleId(null);
      }
    };

    handleHash();
    window.addEventListener('hashchange', handleHash);
    return () => window.removeEventListener('hashchange', handleHash);
  }, []);

  const filteredArticles = activeCategory === '全部'
    ? articles
    : articles.filter(a => a.category === activeCategory);

  const handleArticleClick = (id: string) => {
    window.location.hash = id;
    setActiveArticleId(id);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleBack = () => {
    history.pushState(null, '', '/blog');
    setActiveArticleId(null);
  };

  // If an article is active, show the article detail
  if (activeArticleId) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-white/10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-14">
              <div className="flex items-center gap-2.5 shrink-0">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-base shadow-lg shadow-blue-500/20">
                  📚
                </div>
                <a href="/" className="text-lg font-bold text-white hover:opacity-80 transition-opacity">
                  教材工具箱
                </a>
              </div>
              <div className="hidden lg:flex items-center gap-1">
                <a href="/" className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">首页</a>
                <a href="/blog" onClick={(e) => { e.preventDefault(); handleBack(); }} className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">教育博客</a>
                <a href="/about" className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">关于我们</a>
                <a href="/contact" className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">联系我们</a>
              </div>
            </div>
          </div>
        </nav>
        <main className="pt-14">
          <BlogPost articleId={activeArticleId} onBack={handleBack} />
        </main>
        <footer className="border-t border-white/10 py-8 px-4 mt-8">
          <div className="max-w-6xl mx-auto text-center text-gray-500 text-sm">
            &copy; 2026 教材工具箱
          </div>
        </footer>
      </div>
    );
  }

  // Blog list view
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-14">
            <div className="flex items-center gap-2.5 shrink-0">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-base shadow-lg shadow-blue-500/20">
                📚
              </div>
              <a href="/" className="text-lg font-bold text-white hover:opacity-80 transition-opacity">
                教材工具箱
              </a>
            </div>
            <div className="hidden lg:flex items-center gap-1">
              <a href="/" className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">首页</a>
              <a href="/resources" className="px-3 py-1.5 text-sm bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-lg font-medium hover:from-amber-600 hover:to-orange-600 transition-colors">免费资源</a>
              <a href="/about" className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">关于我们</a>
              <a href="/contact" className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">联系我们</a>
            </div>
          </div>
        </div>
      </nav>

      <main className="pt-14">
        <div className="max-w-5xl mx-auto px-4 py-12">
          {/* Page Title */}
          <div className="text-center mb-10">
            <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">教育博客</h1>
            <p className="text-gray-400 text-lg">分享实用的教育方法和学习技巧，助力孩子成长</p>
          </div>

          {/* Category Filter */}
          <div className="flex flex-wrap justify-center gap-2 mb-10">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                  activeCategory === cat
                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/25'
                    : 'bg-slate-800/50 text-gray-400 hover:text-white hover:bg-slate-700/50 border border-white/10'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Article Count */}
          <div className="mb-6 text-sm text-gray-500">
            共 {filteredArticles.length} 篇文章
            {activeCategory !== '全部' && (
              <span>
                {' '}· 分类：<span className="text-gray-300">{activeCategory}</span>
              </span>
            )}
          </div>

          {/* Article Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {filteredArticles.map((article) => (
              <button
                key={article.id}
                onClick={() => handleArticleClick(article.id)}
                className="text-left bg-slate-800/50 border border-white/10 rounded-2xl p-6 hover:border-white/20 hover:bg-slate-700/50 transition-all group"
              >
                {/* Category & Read Time */}
                <div className="flex items-center gap-3 mb-3">
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium border ${categoryColors[article.category] || 'bg-gray-500/20 text-gray-300 border-gray-500/30'}`}>
                    {article.category}
                  </span>
                  <span className="text-gray-500 text-xs">{article.readTime}</span>
                </div>

                {/* Title */}
                <h2 className="text-lg font-bold text-white mb-2 group-hover:text-blue-400 transition-colors leading-snug">
                  {article.title}
                </h2>

                {/* Description */}
                <p className="text-gray-400 text-sm leading-relaxed mb-4 line-clamp-2">
                  {article.description}
                </p>

                {/* Date & Arrow */}
                <div className="flex items-center justify-between">
                  <time className="text-gray-500 text-xs">{article.date}</time>
                  <span className="text-gray-400 group-hover:text-blue-400 group-hover:translate-x-1 transition-all">
                    阅读全文 &rarr;
                  </span>
                </div>
              </button>
            ))}
          </div>

          {/* Empty State */}
          {filteredArticles.length === 0 && (
            <div className="text-center py-20">
              <p className="text-gray-400 text-lg">该分类暂无文章</p>
            </div>
          )}
        </div>
      </main>

      <footer className="border-t border-white/10 py-8 px-4 mt-8">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-wrap justify-center gap-4 md:gap-6 text-sm text-gray-400 mb-4">
            <a href="/about" className="hover:text-white transition-colors">关于我们</a>
            <span className="text-gray-600">|</span>
            <a href="/terms" className="hover:text-white transition-colors">服务条款</a>
            <span className="text-gray-600">|</span>
            <a href="/contact" className="hover:text-white transition-colors">联系我们</a>
            <span className="text-gray-600">|</span>
            <a href="/blog" className="hover:text-white transition-colors">教育博客</a>
          </div>
          <div className="text-center text-gray-500 text-sm">
            &copy; 2026 教材工具箱
          </div>
        </div>
      </footer>
    </div>
  );
}
