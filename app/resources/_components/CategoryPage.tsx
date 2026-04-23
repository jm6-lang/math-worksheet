'use client';

import { RESOURCE_CATEGORIES } from '../data';

interface CategoryPageProps {
  categoryId: string;
}

export default function CategoryPage({ categoryId }: CategoryPageProps) {
  const category = RESOURCE_CATEGORIES.find((c) => c.id === categoryId);

  if (!category) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <p className="text-gray-400 text-lg">分类未找到</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* 顶部导航 */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-14">
            {/* Logo */}
            <div className="flex items-center gap-2.5 shrink-0">
              <a href="/" className="flex items-center gap-2.5 group">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-base shadow-lg shadow-blue-500/20">
                  📚
                </div>
                <span className="text-lg font-bold text-white group-hover:opacity-80 transition-opacity">
                  教材工具箱
                </span>
              </a>
            </div>

            {/* 导航链接 */}
            <div className="hidden md:flex items-center gap-1">
              <a href="/" className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                🏠 首页
              </a>
              <a href="/tools/math-worksheet" className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                🧮 数学练习卷
              </a>
              <a href="/tools/calligraphy" className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                ✍️ 字帖生成器
              </a>
              <a href="/tools/sudoku" className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                🧩 数独游戏
              </a>
              <a href="/resources" className="px-3 py-1.5 text-sm bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-lg font-medium hover:from-amber-600 hover:to-orange-600 transition-colors">
                🎁 免费资源
              </a>
            </div>

            {/* 移动端菜单按钮 */}
            <a href="/" className="md:hidden px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
              ← 返回首页
            </a>
          </div>
        </div>
      </nav>

      {/* 主内容 */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-16">
        {/* 面包屑导航 */}
        <nav className="flex items-center gap-2 text-sm text-gray-500 mb-8">
          <a href="/" className="hover:text-white transition-colors">首页</a>
          <span>/</span>
          <a href="/resources" className="hover:text-white transition-colors">免费资源</a>
          <span>/</span>
          <span className="text-gray-300">{category.name}</span>
        </nav>

        {/* 分类标题区域 */}
        <div className="flex items-center gap-4 mb-8">
          <div className="w-14 h-14 bg-gradient-to-br from-amber-500/20 to-orange-500/20 rounded-2xl flex items-center justify-center text-3xl border border-amber-500/20">
            {category.icon}
          </div>
          <div>
            <h1 className="text-2xl md:text-3xl font-black text-white">{category.name}</h1>
            <p className="text-gray-400 mt-1">{category.desc}</p>
          </div>
        </div>

        {/* 资源卡片网格 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {category.resources.map((r) => (
            <div
              key={r.title}
              className="bg-slate-800/60 border border-white/10 rounded-2xl p-5 hover:border-amber-500/30 hover:bg-slate-800/80 transition-all duration-300 group"
            >
              {/* 头部 */}
              <div className="flex items-start gap-3 mb-3">
                <div className="text-3xl shrink-0">{r.icon}</div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-base font-bold text-white mb-1 group-hover:text-amber-400 transition-colors leading-snug">
                    {r.title}
                  </h3>
                  <p className="text-gray-400 text-xs leading-relaxed line-clamp-2">
                    {r.desc}
                  </p>
                </div>
              </div>

              {/* 标签 */}
              <div className="flex flex-wrap gap-1.5 mb-4">
                {r.tags.map((tag) => (
                  <span
                    key={tag}
                    className="px-2 py-0.5 text-xs bg-slate-700/80 text-gray-400 rounded-md border border-white/5"
                  >
                    {tag}
                  </span>
                ))}
              </div>

              {/* 下载按钮 */}
              <a
                href={r.link}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center gap-2 w-full py-2.5 bg-gradient-to-r from-amber-500 to-orange-500 text-white text-sm font-bold rounded-xl hover:from-amber-600 hover:to-orange-600 transition-all shadow-lg shadow-amber-500/20 group-hover:shadow-amber-500/40"
              >
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
                </svg>
                {r.linkLabel}下载
              </a>
            </div>
          ))}
        </div>

        {/* 底部导航 */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-12">
          <a
            href="/resources"
            className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-500 text-white font-bold rounded-xl hover:from-amber-600 hover:to-orange-600 transition-all shadow-lg shadow-amber-500/20"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            返回免费资源中心
          </a>
          <a
            href="/"
            className="inline-flex items-center gap-2 px-6 py-3 bg-slate-700/60 border border-white/10 text-gray-300 rounded-xl hover:bg-slate-700 hover:text-white hover:border-white/20 transition-all"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
              <polyline points="9,22 9,12 15,12 15,22"/>
            </svg>
            返回首页
          </a>
        </div>

        {/* 底部 */}
        <div className="text-center mt-6 text-gray-500 text-sm">
          <p>更多资源持续更新中，欢迎收藏本站</p>
        </div>
      </div>
    </div>
  );
}
