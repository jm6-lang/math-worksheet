export const metadata = {
  title: '免费资源 - 教材工具箱',
  description: '汇集优质学习资源，网盘资料免费分享，涵盖各学科学习资料、工具软件等',
};

const RESOURCES = [
  {
    icon: '✍️',
    title: '书法字帖资源合集',
    desc: '包含多种书法字帖模板，适合各年龄段练习使用',
    tags: ['字帖', '书法', '练字'],
    link: 'https://pan.quark.cn/s/bae1d2a98cc1',
    linkLabel: '夸克网盘',
  },
  {
    icon: '📖',
    title: '练字教程字帖大合集',
    desc: '系统练字教程配合字帖练习，循序渐进掌握书法',
    tags: ['教程', '字帖', '合集'],
    link: 'https://pan.quark.cn/s/ed38ac8a3a44',
    linkLabel: '夸克网盘',
  },
  {
    icon: '📚',
    title: '小学初中高中电子版教科书下载器',
    desc: '支持下载各年级各科目电子版教科书，一键获取全套教材',
    tags: ['教科书', '下载器', '全学段'],
    link: 'https://pan.quark.cn/s/ec6e312bc935',
    linkLabel: '夸克网盘',
  },
  {
    icon: '🎓',
    title: '中小学电子课本下载器 v2.1',
    desc: '最新版电子课本下载工具，支持更多教材版本，界面更友好',
    tags: ['课本', '下载器', '最新版'],
    link: 'https://pan.quark.cn/s/6a29f7a5e914',
    linkLabel: '夸克网盘',
  },
];

export default function ResourcesPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* 顶部导航 */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <a href="/" className="flex items-center gap-3 group">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-xl shadow-lg shadow-blue-500/30">
                  📚
                </div>
                <span className="text-xl font-bold text-white group-hover:opacity-80 transition-opacity">
                  教材工具箱
                </span>
              </a>
            </div>

            {/* 导航链接 */}
            <div className="flex items-center gap-1">
              <a href="/" className="px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                🏠 首页
              </a>
              <a href="/tools/math-worksheet" className="px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                🧮 数学练习卷
              </a>
              <a href="/tools/calligraphy" className="px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                ✍️ 字帖生成器
              </a>
              <a href="/tools/sudoku" className="px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                🧩 数独游戏
              </a>
              <div className="w-px h-6 bg-white/20 mx-2"></div>
              <a href="/resources" className="px-4 py-2 text-sm bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-lg font-medium hover:from-amber-600 hover:to-orange-600 transition-colors">
                🎁 免费资源
              </a>
            </div>
          </div>
        </div>
      </nav>

      {/* 主内容 */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-28 pb-16">
        {/* 页面标题 */}
        <div className="text-center mb-10">
          <div className="text-6xl mb-4">🎁</div>
          <h1 className="text-4xl md:text-5xl font-black text-white mb-4">
            免费资源中心
          </h1>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            汇集优质学习资源，持续更新中
          </p>
        </div>

        {/* 资源卡片列表 */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {RESOURCES.map((r) => (
            <div
              key={r.title}
              className="bg-slate-800/60 border border-white/10 rounded-2xl p-6 hover:border-amber-500/30 hover:bg-slate-800/80 transition-all duration-300 group"
            >
              {/* 头部 */}
              <div className="flex items-start gap-4 mb-4">
                <div className="text-4xl">{r.icon}</div>
                <div className="flex-1">
                  <h2 className="text-xl font-bold text-white mb-1 group-hover:text-amber-400 transition-colors">
                    {r.title}
                  </h2>
                  <p className="text-gray-400 text-sm leading-relaxed">
                    {r.desc}
                  </p>
                </div>
              </div>

              {/* 标签 */}
              <div className="flex flex-wrap gap-2 mb-4">
                {r.tags.map((tag) => (
                  <span
                    key={tag}
                    className="px-3 py-1 text-xs bg-slate-700/80 text-gray-300 rounded-full border border-white/5"
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
                className="flex items-center justify-center gap-2 w-full py-3 bg-gradient-to-r from-amber-500 to-orange-500 text-white font-bold rounded-xl hover:from-amber-600 hover:to-orange-600 transition-all shadow-lg shadow-amber-500/20 group-hover:shadow-amber-500/40"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
                </svg>
                {r.linkLabel}下载
              </a>
            </div>
          ))}
        </div>

        {/* 使用说明 */}
        <div className="mt-10 bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-2xl p-6">
          <div className="flex items-start gap-4">
            <div className="text-3xl">💡</div>
            <div>
              <h3 className="text-lg font-bold text-white mb-2">使用说明</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                点击上方「夸克网盘下载」按钮，跳转到夸克网盘页面。<br />
                点击「保存到盘」或「下载」按钮将资源保存到你的网盘。<br />
                部分资源可能需要输入提取码，我们会持续完善资源详情。
              </p>
            </div>
          </div>
        </div>

        {/* 返回首页 */}
        <div className="text-center mt-8">
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
