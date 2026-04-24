import { RESOURCE_CATEGORIES } from './data';

export const metadata = {
  title: '免费资源中心 - 教材工具箱 | 小学初中高中学习资料免费下载',
  description: '免费下载小学初中高中语文、数学、英语学习资料，包括字帖、试卷、阅读理解、自然拼读、教辅电子版、小语种、历史故事等优质学习资源，持续更新。',
  keywords: '小学学习资料,初中学习资料,高中学习资料,免费下载,字帖,试卷,阅读理解,自然拼读,教辅,电子课本,小语种,历史故事,PDF打印',
  alternates: {
    canonical: 'https://www.skillxm.cn/resources',
  },
};

export default function ResourcesPage() {
  const totalResources = RESOURCE_CATEGORIES.reduce((sum, cat) => sum + cat.resources.length, 0);

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
        {/* 页面标题 */}
        <div className="text-center mb-12">
          <div className="text-6xl mb-4">🎁</div>
          <h1 className="text-3xl md:text-4xl font-black text-white mb-4">
            免费资源中心
          </h1>
          <p className="text-lg text-gray-400 max-w-2xl mx-auto">
            汇集优质小学学习资料，涵盖语文、数学、英语全科目，持续更新中
          </p>
        </div>

        {/* 分类卡片网格 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-12">
          {RESOURCE_CATEGORIES.map((cat) => (
            <a
              key={cat.id}
              href={`/resources/${cat.id}`}
              className="block bg-slate-800/60 border border-white/10 rounded-2xl p-6 hover:border-amber-500/30 hover:bg-slate-800/80 transition-all duration-300 group"
            >
              <div className="flex items-center gap-4 mb-3">
                <div className="text-4xl">{cat.icon}</div>
                <div>
                  <h2 className="text-lg font-bold text-white group-hover:text-amber-400 transition-colors">{cat.name}</h2>
                  <p className="text-sm text-gray-500">{cat.desc}</p>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-500">{cat.resources.length} 个资源</span>
                <span className="text-xs text-amber-500 group-hover:translate-x-1 transition-transform">查看全部 →</span>
              </div>
            </a>
          ))}
        </div>

        {/* 使用说明 */}
        <div className="mt-12 bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-2xl p-6">
          <div className="flex items-start gap-4">
            <div className="text-3xl shrink-0">💡</div>
            <div>
              <h3 className="text-lg font-bold text-white mb-2">使用说明</h3>
              <ul className="text-gray-400 text-sm leading-relaxed space-y-1.5">
                <li>• 点击分类卡片进入对应分类，查看该分类下的所有资源</li>
                <li>• 点击「夸克网盘下载」按钮，跳转到夸克网盘页面</li>
                <li>• 点击「保存到盘」或「下载」按钮将资源保存到你的网盘</li>
                <li>• 部分资源可能需要输入提取码，我们会持续完善资源详情</li>
                <li>• 所有资源均来自网络公开分享，仅供学习交流使用</li>
                <li>• 如有资源失效或版权问题，请联系我们处理</li>
              </ul>
            </div>
          </div>
        </div>

        {/* 资源统计 */}
        <div className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: '资源总数', value: `${totalResources}+`, icon: '📦' },
            { label: '覆盖科目', value: '语数英', icon: '📚' },
            { label: '适用年级', value: '1-6年级', icon: '🎓' },
            { label: '更新状态', value: '持续更新', icon: '🔄' },
          ].map((stat) => (
            <div key={stat.label} className="bg-slate-800/40 border border-white/10 rounded-xl p-4 text-center">
              <div className="text-2xl mb-1">{stat.icon}</div>
              <div className="text-lg font-bold text-white">{stat.value}</div>
              <div className="text-xs text-gray-500">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* 返回首页 */}
        <div className="text-center mt-10">
          <a
            href="/"
            className="inline-flex items-center gap-2 px-6 py-3 bg-slate-700/60 border border-white/10 text-gray-300 rounded-xl hover:bg-slate-700 hover:text-white hover:border-white/20 transition-all"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
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
