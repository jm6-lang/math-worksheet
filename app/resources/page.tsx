export const metadata = {
  title: '免费资源中心 - 教材工具箱 | 小学学习资料免费下载',
  description: '免费下载小学1-6年级语文、数学、英语学习资料，包括字帖、试卷、阅读理解、自然拼读、教辅电子版等优质学习资源，持续更新。',
  keywords: '小学学习资料,免费下载,字帖,试卷,阅读理解,自然拼读,教辅,电子课本,PDF打印,小学语文,小学数学,小学英语',
};

interface Resource {
  icon: string;
  title: string;
  desc: string;
  tags: string[];
  link: string;
  linkLabel: string;
}

interface ResourceCategory {
  id: string;
  name: string;
  icon: string;
  desc: string;
  resources: Resource[];
}

const RESOURCE_CATEGORIES: ResourceCategory[] = [
  {
    id: 'calligraphy',
    name: '字帖书法',
    icon: '✍️',
    desc: '书法字帖模板与练字教程',
    resources: [
      {
        icon: '✍️',
        title: '书法字帖资源合集',
        desc: '包含多种书法字帖模板，楷书、行书、隶书等多种字体，适合各年龄段练习使用',
        tags: ['字帖', '书法', '练字', '多字体'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
      {
        icon: '📖',
        title: '练字教程字帖大合集',
        desc: '系统练字教程配合字帖练习，从基础笔画到完整字形，循序渐进掌握书法技巧',
        tags: ['教程', '字帖', '合集', '系统学习'],
        link: 'https://pan.quark.cn/s/ed38ac8a3a44',
        linkLabel: '夸克网盘',
      },
    ],
  },
  {
    id: 'textbook',
    name: '电子课本',
    icon: '📚',
    desc: '各版本电子教科书下载',
    resources: [
      {
        icon: '📚',
        title: '小学初中高中电子版教科书下载器',
        desc: '支持下载各年级各科目电子版教科书，人教版、苏教版、北师版等主流版本全覆盖',
        tags: ['教科书', '下载器', '全学段', '多版本'],
        link: 'https://pan.quark.cn/s/ec6e312bc935',
        linkLabel: '夸克网盘',
      },
      {
        icon: '🎓',
        title: '中小学电子课本下载器 v2.1',
        desc: '最新版电子课本下载工具，支持更多教材版本，界面更友好，一键获取全套教材',
        tags: ['课本', '下载器', '最新版', '一键下载'],
        link: 'https://pan.quark.cn/s/6a29f7a5e914',
        linkLabel: '夸克网盘',
      },
    ],
  },
  {
    id: 'math',
    name: '数学资料',
    icon: '🧮',
    desc: '数学练习卷与奥数资料',
    resources: [
      {
        icon: '🧮',
        title: '小学1-6年级数学练习卷合集',
        desc: '涵盖人教版、北师版等主流教材，包含单元测试、期中期末试卷，附详细答案解析',
        tags: ['数学', '试卷', '1-6年级', '带答案'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
      {
        icon: '🏆',
        title: '小学奥数举一反三AB版',
        desc: '经典奥数训练教材，从入门到进阶，培养数学思维和逻辑推理能力',
        tags: ['奥数', '举一反三', '思维训练', 'AB版'],
        link: 'https://pan.quark.cn/s/6ed6bab78edf',
        linkLabel: '夸克网盘',
      },
      {
        icon: '📐',
        title: '小学数学口算速算练习册',
        desc: '每日一练口算速算题卡，从10以内到1000以内，分级训练提升计算速度和准确率',
        tags: ['口算', '速算', '每日练习', '分级训练'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
    ],
  },
  {
    id: 'chinese',
    name: '语文资料',
    icon: '📖',
    desc: '阅读理解与作文指导',
    resources: [
      {
        icon: '📖',
        title: '小学语文阅读训练100篇超详解',
        desc: '王朝霞阅读训练系列，1-6年级分级阅读理解训练，涵盖古诗文、现代文、写作训练',
        tags: ['阅读理解', '100篇', '分级', '超详解'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
      {
        icon: '📝',
        title: '小学看图写话与作文指导',
        desc: '低年级看图写话训练 + 中高年级作文技巧指导，包含优秀范文和写作模板',
        tags: ['看图写话', '作文', '范文', '写作技巧'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
      {
        icon: '🔤',
        title: '小学拼音汉字识字资料',
        desc: '拼音学习卡片、汉字笔顺描红、识字练习册，帮助低年级学生打好语文基础',
        tags: ['拼音', '识字', '笔顺', '描红'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
    ],
  },
  {
    id: 'english',
    name: '英语资料',
    icon: '🔤',
    desc: '自然拼读与英语启蒙',
    resources: [
      {
        icon: '🔤',
        title: 'BBC自然拼读 Fun With Phonics',
        desc: 'BBC出品自然拼读全套资源，含44个动画视频 + 14册练习册PDF + 26个单词卡PDF，可打印',
        tags: ['自然拼读', 'BBC', '视频+PDF', '可打印'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
      {
        icon: '🎵',
        title: '小学英语儿歌与绘本资源',
        desc: '经典英语启蒙儿歌合集 + 分级绘本PDF，培养英语语感和阅读兴趣',
        tags: ['儿歌', '绘本', '启蒙', '分级阅读'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
    ],
  },
  {
    id: 'comprehensive',
    name: '综合教辅',
    icon: '📁',
    desc: '全科目综合学习资料',
    resources: [
      {
        icon: '📁',
        title: '2025秋小学全学科教辅资料汇总',
        desc: '语文、数学、英语全科目教辅资料合集，含教材、重点笔记、试卷、练习册，多版本覆盖',
        tags: ['全学科', '教辅', '多版本', '合集'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
      {
        icon: '📋',
        title: '小升初考试真题集',
        desc: '各重点中学小升初考试真题汇总，含数学、语文、英语三科，附详细答案和解析',
        tags: ['小升初', '真题', '重点中学', '带解析'],
        link: 'https://pan.quark.cn/s/fbc1e85d5089',
        linkLabel: '夸克网盘',
      },
    ],
  },
];

export default function ResourcesPage() {
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
          {/* 分类快速导航 */}
          <div className="flex flex-wrap justify-center gap-2 mt-6">
            {RESOURCE_CATEGORIES.map((cat) => (
              <a
                key={cat.id}
                href={`#${cat.id}`}
                className="px-3 py-1.5 text-xs bg-slate-800/60 text-gray-300 rounded-full border border-white/10 hover:border-amber-500/30 hover:text-amber-400 transition-colors"
              >
                {cat.icon} {cat.name}
              </a>
            ))}
          </div>
        </div>

        {/* 资源分类列表 */}
        <div className="space-y-12">
          {RESOURCE_CATEGORIES.map((cat) => (
            <section key={cat.id} id={cat.id}>
              {/* 分类标题 */}
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-gradient-to-br from-amber-500/20 to-orange-500/20 rounded-xl flex items-center justify-center text-xl border border-amber-500/20">
                  {cat.icon}
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white">{cat.name}</h2>
                  <p className="text-sm text-gray-500">{cat.desc}</p>
                </div>
                <div className="flex-1 h-px bg-gradient-to-r from-white/10 to-transparent ml-4"></div>
              </div>

              {/* 资源卡片 */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {cat.resources.map((r) => (
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
            </section>
          ))}
        </div>

        {/* 使用说明 */}
        <div className="mt-12 bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-2xl p-6">
          <div className="flex items-start gap-4">
            <div className="text-3xl shrink-0">💡</div>
            <div>
              <h3 className="text-lg font-bold text-white mb-2">使用说明</h3>
              <ul className="text-gray-400 text-sm leading-relaxed space-y-1.5">
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
            { label: '资源总数', value: `${RESOURCE_CATEGORIES.reduce((sum, cat) => sum + cat.resources.length, 0)}+`, icon: '📦' },
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
          <p>更多资源持续更新中，欢迎收藏本站 📌</p>
        </div>
      </div>
    </div>
  );
}
