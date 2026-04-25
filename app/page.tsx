'use client';

import { useState, useEffect, useRef } from 'react';

// 轮播图数据
const CAROUSEL_ITEMS = [
  {
    id: 1,
    title: '数学练习题',
    subtitle: '一键生成个性化练习题',
    description: '支持加减乘除、竖式计算、填空题等多种题型',
    icon: '🧮',
    gradient: 'from-blue-600 via-indigo-600 to-purple-600',
    link: '/tools/math-worksheet',
  },
  {
    id: 2,
    title: '字帖生成器',
    subtitle: '练字从此不再枯燥',
    description: '田字格、米字格、方格多种模板，自定义内容',
    icon: '✍️',
    gradient: 'from-emerald-500 via-teal-500 to-cyan-500',
    link: '/tools/calligraphy',
  },
  {
    id: 3,
    title: '英语字帖',
    subtitle: '四线三格英语练习',
    description: '标准四线三格英文字母练习，支持PDF导出',
    icon: '🔤',
    gradient: 'from-rose-500 via-pink-500 to-red-500',
    link: '/tools/english-calligraphy',
  },
  {
    id: 4,
    title: '数独挑战',
    subtitle: '锻炼逻辑思维',
    description: '多难度级别，计时挑战，自动校验',
    icon: '🧩',
    gradient: 'from-orange-500 via-red-500 to-pink-500',
    link: '/tools/sudoku',
  },
  {
    id: 5,
    title: '口算速练',
    subtitle: '计时挑战极限速度',
    description: '多难度级别，在线计时口算练习，即时反馈',
    icon: '⚡',
    gradient: 'from-yellow-500 via-amber-500 to-orange-500',
    link: '/tools/mental-math',
  },
  {
    id: 6,
    title: '识字卡片',
    subtitle: '轻松认识汉字',
    description: '自定义汉字卡片，支持拼音组词，可打印制作',
    icon: '🃏',
    gradient: 'from-purple-500 via-violet-500 to-indigo-500',
    link: '/tools/flashcards',
  },
  {
    id: 7,
    title: '作文模板',
    subtitle: '写作不再困难',
    description: '看图写话、日记、书信等多种模板，辅助写作练习',
    icon: '📝',
    gradient: 'from-teal-500 via-cyan-500 to-blue-500',
    link: '/tools/writing-template',
  },
];

// 公告数据
const ANNOUNCEMENTS = [
  '🎉 口算速练全新上线！支持4个难度级别，在线计时挑战',
  '🆕 识字卡片上线！自定义汉字卡片，支持拼音组词，可打印',
  '📝 作文模板生成器上线！看图写话、日记、书信等多种模板',
  '📢 字帖生成器上线！支持楷体/宋体/黑体等多种字体',
  '🧩 数独游戏全新上线，支持4个难度级别',
  '💡 小贴士：点击顶部菜单可快速访问各工具',
  '🔥 免费使用，无需注册，即开即用',
];

// 功能介绍卡片
const FEATURE_CARDS = [
  {
    icon: '⚡',
    title: '即开即用',
    desc: '无需注册、无需登录，打开浏览器即可使用，所有功能完全免费',
    color: 'from-yellow-500 to-orange-500',
  },
  {
    icon: '🖨️',
    title: 'PDF 导出打印',
    desc: '一键将练习卷导出为 PDF，支持 A4 纸直接打印，学校家庭两相宜',
    color: 'from-blue-500 to-indigo-500',
  },
  {
    icon: '📐',
    title: '多种练习模板',
    desc: '田字格、米字格、方格、横线格、空白纸，满足不同年级和使用场景',
    color: 'from-emerald-500 to-teal-500',
  },
];

// 常见问题 FAQ
const FAQ_ITEMS = [
  {
    q: '完全免费吗？',
    a: '是的，教材工具箱所有功能完全免费使用，无需注册账号，无需付费，无任何隐藏费用。',
  },
  {
    q: '生成的 PDF 会有水印或广告吗？',
    a: '不会。导出的 PDF 干净整洁，没有任何水印、品牌标识或广告，适合直接打印使用。',
  },
  {
    q: '支持哪些年级和题型？',
    a: '数学练习卷覆盖小学 1-6 年级，支持加减乘除、竖式计算、填空题、比大小、应用题等 11 种题型，可按年级和难度灵活配置。',
  },
  {
    q: '可以自定义内容吗？',
    a: '可以。字帖生成器支持自定义汉字、词语或句子；数学练习卷支持自定义数字范围、题目数量和混合题型。',
  },
  {
    q: '生成的练习卷会重复吗？',
    a: '每次生成均为随机出题，同一配置下每次结果不同，避免机械重复，真正达到练习效果。',
  },
  {
    q: '适合哪些人使用？',
    a: '适合小学学生、家长（辅导孩子作业）、学校教师（布置练习作业）以及想自主练习的成年人。',
  },
];

// 工具分类
const TOOL_CATEGORIES = [
  {
    category: '📚 学习工具',
    tools: [
      { name: '数学练习题', icon: '🧮', desc: '一键出题，PDF导出', link: '/tools/math-worksheet', color: 'blue', disabled: false },
      { name: '字帖生成器', icon: '✍️', desc: '田字格/米字格模板', link: '/tools/calligraphy', color: 'emerald', disabled: false },
      { name: '英语字帖', icon: '🔤', desc: '四线三格模板', link: '/tools/english-calligraphy', color: 'rose', disabled: false },
      { name: '数独游戏', icon: '🧩', desc: '多难度逻辑训练', link: '/tools/sudoku', color: 'orange', disabled: false },
      { name: '拼音注音', icon: '📝', desc: '汉字注音练习', link: '/tools/pinyin', color: 'blue', disabled: false },
      { name: '口算速练', icon: '⚡', desc: '在线计时练习', link: '/tools/mental-math', color: 'orange', disabled: false },
      { name: '识字卡片', icon: '🃏', desc: '汉字卡片生成', link: '/tools/flashcards', color: 'blue', disabled: false },
      { name: '作文模板', icon: '📝', desc: '多种写作模板', link: '/tools/writing-template', color: 'emerald', disabled: false },
    ],
  },
];

// 颜色映射
const COLOR_MAP: Record<string, string> = {
  blue: 'bg-blue-500 hover:bg-blue-600',
  emerald: 'bg-emerald-500 hover:bg-emerald-600',
  orange: 'bg-orange-500 hover:bg-orange-600',
  rose: 'bg-rose-500 hover:bg-rose-600',
  gray: 'bg-gray-400',
};

export default function HomePage() {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [mobileMenu, setMobileMenu] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [showDonate, setShowDonate] = useState(false);
  const [showTutorial, setShowTutorial] = useState(false);
  const [showShare, setShowShare] = useState(false);
  const [showToolsMenu, setShowToolsMenu] = useState(false);
  const [copySuccess, setCopySuccess] = useState(false);
  const [openFaq, setOpenFaq] = useState<number | null>(null);
  const announcementRef = useRef<HTMLDivElement>(null);

  const handleCopy = () => {
    navigator.clipboard.writeText('https://www.skillxm.cn');
    setCopySuccess(true);
    setTimeout(() => setCopySuccess(false), 2000);
  };

  // 自动轮播
  useEffect(() => {
    if (isPaused) return;
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % CAROUSEL_ITEMS.length);
    }, 5000);
    return () => clearInterval(timer);
  }, [isPaused]);

  // 公告滚动
  useEffect(() => {
    const container = announcementRef.current;
    if (!container) return;

    const content = container.querySelector('.announcement-content') as HTMLElement | null;
    if (!content) return;

    // 复制内容实现无缝滚动
    content.innerHTML += content.innerHTML;

    let animationId: number;
    let offset = 0;
    const speed = 1;

    const animate = () => {
      offset -= speed;
      if (offset <= -content.scrollWidth / 2) {
        offset = 0;
      }
      content.style.transform = `translateX(${offset}px)`;
      animationId = requestAnimationFrame(animate);
    };

    animationId = requestAnimationFrame(animate);

    return () => cancelAnimationFrame(animationId);
  }, []);

  const goToSlide = (index: number) => {
    setCurrentSlide(index);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* 主 H1 - 视觉隐藏但搜索引擎可见 */}
      <h1 className="sr-only">教材工具箱 - 免费在线教育工具</h1>

      {/* ===== 顶部导航 ===== */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-14">
            {/* Logo */}
            <div className="flex items-center gap-2.5 shrink-0">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-base shadow-lg shadow-blue-500/20">
                📚
              </div>
              <a href="/" className="text-lg font-bold text-white hover:opacity-80 transition-opacity">
                教材工具箱
              </a>
            </div>

            {/* 桌面导航 */}
            <div className="hidden lg:flex items-center gap-1">
              <a href="/" className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                首页
              </a>

              {/* 学习工具下拉 */}
              <div className="relative"
                onMouseEnter={() => setShowToolsMenu(true)}
                onMouseLeave={() => setShowToolsMenu(false)}
              >
                <button className="flex items-center gap-1 px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                  🛠️ 学习工具
                  <svg className={`w-3.5 h-3.5 transition-transform ${showToolsMenu ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
                </button>
                {showToolsMenu && (
                  <div className="absolute left-0 top-full mt-1 bg-slate-800 border border-white/10 rounded-xl shadow-2xl p-2 min-w-[200px] z-50">
                    <a href="/tools/math-worksheet" className="flex items-center gap-3 px-3 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                      <span className="w-7 h-7 bg-blue-500/20 rounded-lg flex items-center justify-center text-sm">🧮</span>
                      <div><div className="text-white font-medium">数学练习卷</div><div className="text-xs text-gray-500">一键出题，PDF导出</div></div>
                    </a>
                    <a href="/tools/calligraphy" className="flex items-center gap-3 px-3 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                      <span className="w-7 h-7 bg-emerald-500/20 rounded-lg flex items-center justify-center text-sm">✍️</span>
                      <div><div className="text-white font-medium">字帖生成器</div><div className="text-xs text-gray-500">田字格/米字格模板</div></div>
                    </a>
                    <a href="/tools/english-calligraphy" className="flex items-center gap-3 px-3 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                      <span className="w-7 h-7 bg-rose-500/20 rounded-lg flex items-center justify-center text-sm">🔤</span>
                      <div><div className="text-white font-medium">英语字帖</div><div className="text-xs text-gray-500">四线三格模板</div></div>
                    </a>
                    <a href="/tools/sudoku" className="flex items-center gap-3 px-3 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                      <span className="w-7 h-7 bg-orange-500/20 rounded-lg flex items-center justify-center text-sm">🧩</span>
                      <div><div className="text-white font-medium">数独游戏</div><div className="text-xs text-gray-500">多难度逻辑训练</div></div>
                    </a>
                    <a href="/tools/mental-math" className="flex items-center gap-3 px-3 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                      <span className="w-7 h-7 bg-yellow-500/20 rounded-lg flex items-center justify-center text-sm">⚡</span>
                      <div><div className="text-white font-medium">口算速练</div><div className="text-xs text-gray-500">在线计时练习</div></div>
                    </a>
                    <a href="/tools/flashcards" className="flex items-center gap-3 px-3 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                      <span className="w-7 h-7 bg-purple-500/20 rounded-lg flex items-center justify-center text-sm">🃏</span>
                      <div><div className="text-white font-medium">识字卡片</div><div className="text-xs text-gray-500">汉字卡片生成</div></div>
                    </a>
                    <a href="/tools/writing-template" className="flex items-center gap-3 px-3 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                      <span className="w-7 h-7 bg-teal-500/20 rounded-lg flex items-center justify-center text-sm">📝</span>
                      <div><div className="text-white font-medium">作文模板</div><div className="text-xs text-gray-500">多种写作模板</div></div>
                    </a>
                    <a href="/tools/pinyin" className="flex items-center gap-3 px-3 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                      <span className="w-7 h-7 bg-blue-500/20 rounded-lg flex items-center justify-center text-sm">📝</span>
                      <div><div className="text-white font-medium">拼音注音</div><div className="text-xs text-gray-500">汉字注音练习</div></div>
                    </a>
                  </div>
                )}
              </div>

              <a href="/resources" className="px-3 py-1.5 text-sm bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-lg font-medium hover:from-amber-600 hover:to-orange-600 transition-colors">
                🎁 免费资源
              </a>
              <a href="/blog" className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                📰 教育博客
              </a>

              <button onClick={() => setShowTutorial(true)} className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                📖 使用教程
              </button>
              <button onClick={() => setShowShare(true)} className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                🔗 分享
              </button>
              <button onClick={() => setShowDonate(true)} className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                💝 赞助支持
              </button>
            </div>

            {/* 移动端菜单按钮 */}
            <button
              onClick={() => setMobileMenu(!mobileMenu)}
              className="lg:hidden p-2 text-gray-300 hover:text-white transition-colors"
            >
              {mobileMenu ? '✕' : '☰'}
            </button>
          </div>
        </div>

        {/* 移动端菜单 - 全屏侧滑 */}
        <div className={`lg:hidden fixed inset-0 z-50 transition-all duration-300 ${mobileMenu ? 'visible' : 'invisible'}`}>
          {/* 遮罩 */}
          <div className={`absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity duration-300 ${mobileMenu ? 'opacity-100' : 'opacity-0'}`} onClick={() => setMobileMenu(false)} />
          {/* 菜单面板 */}
          <div className={`absolute right-0 top-0 h-full w-72 bg-slate-900 border-l border-white/10 shadow-2xl transition-transform duration-300 ${mobileMenu ? 'translate-x-0' : 'translate-x-full'}`}>
            {/* 头部 */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-white/10">
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-sm">📚</div>
                <span className="text-base font-bold text-white">教材工具箱</span>
              </div>
              <button onClick={() => setMobileMenu(false)} className="p-1.5 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </div>

            {/* 导航列表 */}
            <div className="overflow-y-auto h-[calc(100%-60px)] py-3 px-3 space-y-1">
              <a href="/" onClick={() => setMobileMenu(false)} className="flex items-center gap-3 px-3 py-2.5 text-sm text-white bg-white/10 rounded-xl">
                <span className="w-8 h-8 bg-white/10 rounded-lg flex items-center justify-center">🏠</span>
                首页
              </a>

              {/* 工具分组 */}
              <div className="pt-2 pb-1 px-3">
                <span className="text-xs font-medium text-gray-500 uppercase tracking-wider">学习工具</span>
              </div>
              {[
                { icon: '🧮', name: '数学练习卷', desc: '一键出题', link: '/tools/math-worksheet', color: 'bg-blue-500/15' },
                { icon: '✍️', name: '字帖生成器', desc: '田字格/米字格', link: '/tools/calligraphy', color: 'bg-emerald-500/15' },
                { icon: '🔤', name: '英语字帖', desc: '四线三格', link: '/tools/english-calligraphy', color: 'bg-rose-500/15' },
                { icon: '🧩', name: '数独游戏', desc: '逻辑训练', link: '/tools/sudoku', color: 'bg-orange-500/15' },
                { icon: '⚡', name: '口算速练', desc: '计时练习', link: '/tools/mental-math', color: 'bg-yellow-500/15' },
                { icon: '🃏', name: '识字卡片', desc: '汉字卡片', link: '/tools/flashcards', color: 'bg-purple-500/15' },
                { icon: '📝', name: '作文模板', desc: '写作模板', link: '/tools/writing-template', color: 'bg-teal-500/15' },
                { icon: '📝', name: '拼音注音', desc: '注音练习', link: '/tools/pinyin', color: 'bg-blue-500/15' },
              ].map((tool) => (
                <a key={tool.link} href={tool.link} onClick={() => setMobileMenu(false)} className="flex items-center gap-3 px-3 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-white/5 rounded-xl transition-colors">
                  <span className={`w-8 h-8 ${tool.color} rounded-lg flex items-center justify-center text-sm`}>{tool.icon}</span>
                  <div className="flex-1 min-w-0">
                    <div className="font-medium">{tool.name}</div>
                    <div className="text-xs text-gray-500">{tool.desc}</div>
                  </div>
                  <svg className="w-4 h-4 text-gray-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" /></svg>
                </a>
              ))}

              {/* 资源 */}
              <div className="pt-3 pb-1 px-3">
                <span className="text-xs font-medium text-gray-500 uppercase tracking-wider">更多</span>
              </div>
              <a href="/resources" onClick={() => setMobileMenu(false)} className="flex items-center gap-3 px-3 py-2.5 text-sm text-amber-400 bg-amber-500/10 rounded-xl">
                <span className="w-8 h-8 bg-amber-500/15 rounded-lg flex items-center justify-center text-sm">🎁</span>
                <div className="font-medium">免费资源</div>
              </a>
              <button onClick={() => { setShowTutorial(true); setMobileMenu(false); }} className="w-full flex items-center gap-3 px-3 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-white/5 rounded-xl transition-colors">
                <span className="w-8 h-8 bg-white/5 rounded-lg flex items-center justify-center text-sm">📖</span>
                使用教程
              </button>
              <button onClick={() => { navigator.clipboard.writeText('https://www.skillxm.cn'); alert('链接已复制！'); setMobileMenu(false); }} className="w-full flex items-center gap-3 px-3 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-white/5 rounded-xl transition-colors">
                <span className="w-8 h-8 bg-white/5 rounded-lg flex items-center justify-center text-sm">🔗</span>
                分享给朋友
              </button>
              <button onClick={() => { setShowDonate(true); setMobileMenu(false); }} className="w-full flex items-center gap-3 px-3 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-white/5 rounded-xl transition-colors">
                <span className="w-8 h-8 bg-white/5 rounded-lg flex items-center justify-center text-sm">💝</span>
                赞助支持
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* ===== 轮播大图区域 ===== */}
      <section className="pt-14">
        <div
          className="relative h-[500px] md:h-[600px] overflow-hidden"
          onMouseEnter={() => setIsPaused(true)}
          onMouseLeave={() => setIsPaused(false)}
        >
          {CAROUSEL_ITEMS.map((item, index) => (
            <a
              key={item.id}
              href={item.link}
              className={`absolute inset-0 transition-all duration-700 ease-in-out ${
                index === currentSlide
                  ? 'opacity-100 scale-100'
                  : 'opacity-0 scale-105 pointer-events-none'
              }`}
            >
              {/* 背景渐变 */}
              <div className={`absolute inset-0 bg-gradient-to-br ${item.gradient} opacity-90`} />

              {/* 装饰元素 */}
              <div className="absolute inset-0 overflow-hidden">
                {/* 浮动数学符号 */}
                <div className="absolute top-20 left-10 text-6xl opacity-20 animate-float">+</div>
                <div className="absolute top-40 right-20 text-5xl opacity-20 animate-float-delay">−</div>
                <div className="absolute bottom-32 left-1/4 text-7xl opacity-20 animate-float">×</div>
                <div className="absolute bottom-20 right-1/3 text-5xl opacity-20 animate-float-delay">÷</div>

                {/* 网格装饰 */}
                <div className="absolute right-0 top-0 w-1/2 h-full opacity-10">
                  <svg viewBox="0 0 400 600" className="w-full h-full">
                    {[...Array(8)].map((_, i) => (
                      <line key={`h${i}`} x1="0" y1={i * 75 + 50} x2="400" y2={i * 75 + 50} stroke="white" strokeWidth="1" />
                    ))}
                    {[...Array(5)].map((_, i) => (
                      <line key={`v${i}`} x1={i * 100} y1="0" x2={i * 100} y2="600" stroke="white" strokeWidth="1" />
                    ))}
                  </svg>
                </div>
              </div>

              {/* 内容区域 */}
              <div className="relative z-10 h-full flex flex-col items-center justify-center text-center px-4">
                {/* 3D 悬浮标题 */}
                <div className="perspective-1000 mb-6">
                  <h2
                    className="text-6xl md:text-8xl font-black text-white tracking-tight"
                    style={{
                      textShadow: '0 4px 0 rgba(0,0,0,0.2), 0 8px 0 rgba(0,0,0,0.1), 0 12px 20px rgba(0,0,0,0.3)',
                      transform: 'translateZ(50px)',
                    }}
                  >
                    {item.title}
                  </h2>
                </div>

                {/* 副标题 */}
                <p className="text-2xl md:text-3xl font-bold text-white/90 mb-4 drop-shadow-lg">
                  {item.subtitle}
                </p>

                {/* 描述 */}
                <p className="text-lg text-white/80 mb-6 max-w-xl drop-shadow">
                  {item.description}
                </p>

                {/* 免费提示 */}
                <div className="flex items-center gap-2 bg-white/20 backdrop-blur-sm px-6 py-2 rounded-full mb-8 border border-white/30">
                  <span className="text-white font-bold text-lg">🎁 所有资源免费生成，免费下载打印</span>
                </div>

                {/* 大图标 */}
                <div className="text-8xl mb-8 animate-bounce-slow drop-shadow-2xl">
                  {item.icon}
                </div>

                {/* 按钮 */}
                <button className="px-8 py-4 bg-white text-gray-900 font-bold text-lg rounded-full shadow-xl hover:scale-105 transition-transform">
                  立即使用 →
                </button>
              </div>
            </a>
          ))}

          {/* 轮播指示器 */}
          <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex gap-3 z-20">
            {CAROUSEL_ITEMS.map((_, index) => (
              <button
                key={index}
                onClick={() => goToSlide(index)}
                className={`w-3 h-3 rounded-full transition-all ${
                  index === currentSlide
                    ? 'bg-white scale-125'
                    : 'bg-white/40 hover:bg-white/60'
                }`}
              />
            ))}
          </div>

          {/* 左右箭头 */}
          <button
            onClick={() => goToSlide((currentSlide - 1 + CAROUSEL_ITEMS.length) % CAROUSEL_ITEMS.length)}
            className="absolute left-4 top-1/2 -translate-y-1/2 w-12 h-12 bg-white/20 hover:bg-white/30 rounded-full flex items-center justify-center text-white text-2xl backdrop-blur-sm transition-colors z-20"
          >
            ‹
          </button>
          <button
            onClick={() => goToSlide((currentSlide + 1) % CAROUSEL_ITEMS.length)}
            className="absolute right-4 top-1/2 -translate-y-1/2 w-12 h-12 bg-white/20 hover:bg-white/30 rounded-full flex items-center justify-center text-white text-2xl backdrop-blur-sm transition-colors z-20"
          >
            ›
          </button>
        </div>
      </section>

      {/* ===== 公告滚动条 ===== */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 py-3">
        <div ref={announcementRef} className="overflow-hidden">
          <div className="announcement-content flex gap-12 whitespace-nowrap">
            {ANNOUNCEMENTS.map((text, i) => (
              <span key={i} className="text-white font-medium px-4">
                {text}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* ===== 工具导航分类 ===== */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-white text-center mb-12">
            🛠️ 工具导航
          </h2>

          <div className="space-y-10">
            {TOOL_CATEGORIES.map((cat) => (
              <div key={cat.category}>
                <h3 className="text-xl font-bold text-gray-300 mb-6 flex items-center gap-2">
                  <span>{cat.category}</span>
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {cat.tools.map((tool) => (
                    <a
                      key={tool.name}
                      href={tool.link}
                      className={`group relative bg-slate-800/50 hover:bg-slate-700/50 border border-white/10 rounded-2xl p-6 transition-all ${
                        tool.disabled ? 'opacity-60 cursor-not-allowed' : 'hover:scale-105 hover:border-white/20'
                      }`}
                      onClick={tool.disabled ? (e) => e.preventDefault() : undefined}
                    >
                      {/* 图标 */}
                      <div className="text-5xl mb-4 group-hover:scale-110 transition-transform">
                        {tool.icon}
                      </div>

                      {/* 名称 */}
                      <h4 className="text-lg font-bold text-white mb-2">
                        {tool.name}
                        {tool.disabled && <span className="ml-2 text-xs text-gray-400">(开发中)</span>}
                      </h4>

                      {/* 描述 */}
                      <p className="text-gray-400 text-sm">{tool.desc}</p>

                      {/* 箭头 */}
                      {!tool.disabled && (
                        <div className="absolute bottom-6 right-6 text-gray-400 group-hover:text-white group-hover:translate-x-1 transition-all">
                          →
                        </div>
                      )}
                    </a>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== 功能介绍卡片 ===== */}
      <section className="py-16 px-4 bg-slate-800/30">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-white text-center mb-12">
            ✨ 为什么选择我们
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {FEATURE_CARDS.map((card, i) => (
              <div
                key={i}
                className="relative bg-slate-800/50 border border-white/10 rounded-2xl p-8 hover:border-white/20 transition-all hover:scale-105 group"
              >
                <div
                  className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${card.color} flex items-center justify-center text-3xl mb-5 shadow-lg`}
                >
                  {card.icon}
                </div>
                <h3 className="text-xl font-bold text-white mb-3">{card.title}</h3>
                <p className="text-gray-400 leading-relaxed">{card.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== 常见问题 FAQ ===== */}
      <section className="py-16 px-4">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-white text-center mb-12">
            ❓ 常见问题
          </h2>
          <div className="space-y-3">
            {FAQ_ITEMS.map((item, i) => (
              <div
                key={i}
                className="bg-slate-800/50 border border-white/10 rounded-xl overflow-hidden hover:border-white/20 transition-colors"
              >
                <button
                  onClick={() => setOpenFaq(openFaq === i ? null : i)}
                  className="w-full flex items-center justify-between px-6 py-5 text-left"
                >
                  <span className="text-white font-medium pr-4">{item.q}</span>
                  <span
                    className={`text-gray-400 text-xl flex-shrink-0 transition-transform duration-300 ${openFaq === i ? 'rotate-45' : ''}`}
                  >
                    +
                  </span>
                </button>
                <div
                  className={`overflow-hidden transition-all duration-300 ${openFaq === i ? 'max-h-40' : 'max-h-0'}`}
                >
                  <p className="px-6 pb-5 text-gray-400 leading-relaxed">
                    {item.a}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== 站内链接增强 - 热门资源 ===== */}
      <section className="py-12 px-4 bg-slate-800/50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl font-bold text-white text-center mb-8">
            热门资源
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <a href="/resources/calligraphy" className="bg-slate-700/50 hover:bg-slate-600/50 border border-white/10 hover:border-white/20 rounded-xl p-4 text-center transition-all group">
              <span className="text-2xl block mb-2">✍️</span>
              <span className="text-gray-300 group-hover:text-white text-sm font-medium transition-colors">字帖书法资源</span>
            </a>
            <a href="/resources/math" className="bg-slate-700/50 hover:bg-slate-600/50 border border-white/10 hover:border-white/20 rounded-xl p-4 text-center transition-all group">
              <span className="text-2xl block mb-2">🧮</span>
              <span className="text-gray-300 group-hover:text-white text-sm font-medium transition-colors">数学学习资料</span>
            </a>
            <a href="/resources/chinese" className="bg-slate-700/50 hover:bg-slate-600/50 border border-white/10 hover:border-white/20 rounded-xl p-4 text-center transition-all group">
              <span className="text-2xl block mb-2">📚</span>
              <span className="text-gray-300 group-hover:text-white text-sm font-medium transition-colors">语文学习资料</span>
            </a>
            <a href="/resources/english" className="bg-slate-700/50 hover:bg-slate-600/50 border border-white/10 hover:border-white/20 rounded-xl p-4 text-center transition-all group">
              <span className="text-2xl block mb-2">🔤</span>
              <span className="text-gray-300 group-hover:text-white text-sm font-medium transition-colors">英语学习资料</span>
            </a>
            <a href="/resources/comprehensive" className="bg-slate-700/50 hover:bg-slate-600/50 border border-white/10 hover:border-white/20 rounded-xl p-4 text-center transition-all group">
              <span className="text-2xl block mb-2">📖</span>
              <span className="text-gray-300 group-hover:text-white text-sm font-medium transition-colors">综合教辅资源</span>
            </a>
            <a href="/resources/method" className="bg-slate-700/50 hover:bg-slate-600/50 border border-white/10 hover:border-white/20 rounded-xl p-4 text-center transition-all group">
              <span className="text-2xl block mb-2">💡</span>
              <span className="text-gray-300 group-hover:text-white text-sm font-medium transition-colors">学习方法资源</span>
            </a>
            <a href="/blog" className="bg-slate-700/50 hover:bg-slate-600/50 border border-white/10 hover:border-white/20 rounded-xl p-4 text-center transition-all group">
              <span className="text-2xl block mb-2">📰</span>
              <span className="text-gray-300 group-hover:text-white text-sm font-medium transition-colors">教育博客</span>
            </a>
            <a href="/tools/math-worksheet" className="bg-slate-700/50 hover:bg-slate-600/50 border border-white/10 hover:border-white/20 rounded-xl p-4 text-center transition-all group">
              <span className="text-2xl block mb-2">📐</span>
              <span className="text-gray-300 group-hover:text-white text-sm font-medium transition-colors">数学练习卷生成器</span>
            </a>
          </div>
        </div>
      </section>

      {/* ===== 底部页脚 ===== */}
      <footer className="border-t border-white/10 py-8 px-4 mt-8">
        <div className="max-w-6xl mx-auto">
          {/* 链接行 */}
          <div className="flex flex-wrap justify-center gap-4 md:gap-6 text-sm text-gray-400 mb-4">
            <a href="/about" className="hover:text-white transition-colors">关于我们</a>
            <span className="text-gray-600">|</span>
            <a href="/contact" className="hover:text-white transition-colors">联系我们</a>
            <span className="text-gray-600">|</span>
            <a href="/blog" className="hover:text-white transition-colors">教育博客</a>
            <span className="text-gray-600">|</span>
            <a href="/terms" className="hover:text-white transition-colors">服务条款</a>
            <span className="text-gray-600">|</span>
            <a href="/privacy" className="hover:text-white transition-colors">隐私政策</a>
          </div>
          {/* 友情链接 */}
          <div className="border-t border-gray-200 py-4 text-center text-sm text-gray-500">
            <p className="mb-2">友情链接</p>
            <div className="flex flex-wrap justify-center gap-4">
              <a href="https://docs.skillxm.cn" target="_blank" rel="noopener noreferrer" className="hover:text-blue-600 transition-colors">小二郎文档站</a>
              <a href="https://tool.skillxm.cn" target="_blank" rel="noopener noreferrer" className="hover:text-blue-600 transition-colors">在线工具箱</a>
              <a href="https://ziwei.skillxm.cn" target="_blank" rel="noopener noreferrer" className="hover:text-blue-600 transition-colors">紫微资源站</a>
            </div>
          </div>
        </div>
      </footer>

      {/* ===== 使用教程弹窗 ===== */}
      {showTutorial && (
        <div className="fixed inset-0 z-[70] flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm" onClick={() => setShowTutorial(false)}>
          <div className="bg-[#1a1a1a] border border-white/10 rounded-2xl max-w-2xl w-full max-h-[80vh] overflow-y-auto p-8" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">📖 使用教程</h2>
              <button onClick={() => setShowTutorial(false)} className="text-gray-400 hover:text-white text-2xl leading-none">×</button>
            </div>

            <div className="space-y-6">
              {/* 数学练习卷 */}
              <div className="bg-white/5 rounded-xl p-4">
                <h3 className="text-lg font-bold text-blue-400 mb-3">🧮 数学练习卷生成器</h3>
                <ol className="space-y-2 text-gray-300 text-sm list-decimal list-inside">
                  <li>点击首页轮播图进入<span className="text-white">"数学练习卷"</span></li>
                  <li>选择年级（1-6年级可选）</li>
                  <li>勾选题型（加减乘除、竖式、填空等11种）</li>
                  <li>设置数字范围和题目数量</li>
                  <li>选择模板：田字格/方格/横线格/空白纸</li>
                  <li>点击<span className="text-emerald-400 font-bold">"立即出题"</span>生成练习卷</li>
                  <li>点击<span className="text-blue-400 font-bold">"导出PDF"</span>下载打印</li>
                </ol>
              </div>

              {/* 字帖生成器 */}
              <div className="bg-white/5 rounded-xl p-4">
                <h3 className="text-lg font-bold text-emerald-400 mb-3">✍️ 字帖生成器</h3>
                <ol className="space-y-2 text-gray-300 text-sm list-decimal list-inside">
                  <li>点击首页轮播图进入<span className="text-white">"字帖生成器"</span></li>
                  <li>输入要练习的汉字或词语</li>
                  <li>选择模板：田字格/米字格/方格/横线格</li>
                  <li>选择字体：楷体/宋体/黑体/仿宋等</li>
                  <li>设置每行字数和行数</li>
                  <li>点击<span className="text-emerald-400 font-bold">"生成字帖"</span></li>
                  <li>点击<span className="text-blue-400 font-bold">"导出PDF"</span>下载打印</li>
                </ol>
              </div>

              {/* 数独游戏 */}
              <div className="bg-white/5 rounded-xl p-4">
                <h3 className="text-lg font-bold text-orange-400 mb-3">🧩 数独游戏</h3>
                <ol className="space-y-2 text-gray-300 text-sm list-decimal list-inside">
                  <li>点击首页轮播图进入<span className="text-white">"数独游戏"</span></li>
                  <li>选择难度：简单/中等/困难/专家</li>
                  <li>点击空格，用数字键盘填入答案</li>
                  <li>点击<span className="text-yellow-400 font-bold">"笔记"</span>模式可记录候选数</li>
                  <li>点击<span className="text-blue-400 font-bold">"检查"</span>查看错误</li>
                  <li>完成后点击<span className="text-emerald-400 font-bold">"新游戏"</span>继续挑战</li>
                </ol>
              </div>

              {/* 口算速练 */}
              <div className="bg-white/5 rounded-xl p-4">
                <h3 className="text-lg font-bold text-yellow-400 mb-3">⚡ 口算速练</h3>
                <ol className="space-y-2 text-gray-300 text-sm list-decimal list-inside">
                  <li>点击首页轮播图进入<span className="text-white">"口算速练"</span></li>
                  <li>选择难度：入门/简单/困难/专家</li>
                  <li>设置题目数量（10/20/30/50题）</li>
                  <li>点击<span className="text-emerald-400 font-bold">"开始挑战"</span>进入计时模式</li>
                  <li>用数字键盘快速输入答案</li>
                  <li>完成后查看成绩统计和错题回顾</li>
                </ol>
              </div>

              {/* 识字卡片 */}
              <div className="bg-white/5 rounded-xl p-4">
                <h3 className="text-lg font-bold text-purple-400 mb-3">🃏 识字卡片</h3>
                <ol className="space-y-2 text-gray-300 text-sm list-decimal list-inside">
                  <li>点击首页轮播图进入<span className="text-white">"识字卡片"</span></li>
                  <li>输入要学习的汉字（支持批量输入）</li>
                  <li>或点击年级预设快速加载常用字</li>
                  <li>选择卡片大小和样式</li>
                  <li>点击卡片可翻转查看正反面</li>
                  <li>点击<span className="text-blue-400 font-bold">"导出PDF"</span>打印制作实体卡片</li>
                </ol>
              </div>

              {/* 作文模板 */}
              <div className="bg-white/5 rounded-xl p-4">
                <h3 className="text-lg font-bold text-teal-400 mb-3">📝 作文模板生成器</h3>
                <ol className="space-y-2 text-gray-300 text-sm list-decimal list-inside">
                  <li>点击首页轮播图进入<span className="text-white">"作文模板"</span></li>
                  <li>选择作文类型：看图写话/日记/书信/读后感/议论文</li>
                  <li>选择年级和稿纸样式</li>
                  <li>输入标题，可开启写作提示</li>
                  <li>实时预览作文稿纸效果</li>
                  <li>点击<span className="text-blue-400 font-bold">"导出PDF"</span>下载打印</li>
                </ol>
              </div>

              {/* 快捷出题 */}
              <div className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-xl p-4 border border-blue-500/30">
                <h3 className="text-lg font-bold text-white mb-2">⚡ 快捷出题</h3>
                <p className="text-gray-300 text-sm">
                  首页底部提供<span className="text-yellow-400">快捷预设卡片</span>，一键生成10/20/50/100道题目，无需复杂配置！
                </p>
              </div>

              {/* 温馨提示 */}
              <div className="bg-white/5 rounded-xl p-4">
                <h3 className="text-lg font-bold text-yellow-400 mb-2">💡 温馨提示</h3>
                <ul className="space-y-1 text-gray-300 text-sm list-disc list-inside">
                  <li>所有资源<span className="text-emerald-400 font-bold">完全免费</span>，无需注册</li>
                  <li>PDF导出支持A4纸打印，适合家庭/学校使用</li>
                  <li>建议使用Chrome/Edge浏览器获得最佳体验</li>
                  <li>如觉得有帮助，欢迎<span className="text-pink-400">赞助支持</span>或<span className="text-blue-400">分享给朋友</span>！</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ===== 分享弹窗 ===== */}
      {showShare && (
        <div className="fixed inset-0 z-[70] flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm" onClick={() => setShowShare(false)}>
          <div className="bg-[#1a1a1a] border border-white/10 rounded-2xl max-w-md w-full p-8" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">🔗 分享给朋友</h2>
              <button onClick={() => setShowShare(false)} className="text-gray-400 hover:text-white text-2xl leading-none">&times;</button>
            </div>
            <p className="text-gray-400 text-center mb-4">复制下方链接分享给您的朋友</p>
            <div className="flex items-center gap-2 bg-white/5 rounded-xl p-3 border border-white/10">
              <input
                type="text"
                value="https://www.skillxm.cn"
                readOnly
                className="flex-1 bg-transparent text-white text-sm outline-none"
              />
              <button
                onClick={handleCopy}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition-colors shrink-0"
              >
                {copySuccess ? '已复制' : '复制'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ===== 赞助弹窗 ===== */}
      {showDonate && (
        <div className="fixed inset-0 z-[70] flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm" onClick={() => setShowDonate(false)}>
          <div className="bg-[#1a1a1a] border border-white/10 rounded-2xl max-w-md w-full p-8" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">💝 赞助支持</h2>
              <button onClick={() => setShowDonate(false)} className="text-gray-400 hover:text-white text-2xl leading-none">×</button>
            </div>
            <p className="text-gray-400 text-center mb-6">
              如果这些工具对您有帮助，欢迎赞助支持开发维护！
            </p>
            <div className="grid grid-cols-2 gap-6">
              <div className="text-center">
                <p className="text-sm text-gray-500 mb-2">微信支付</p>
                <img src="/donate/wechat.png" alt="微信支付" className="w-full rounded-xl bg-white p-2" />
              </div>
              <div className="text-center">
                <p className="text-sm text-gray-500 mb-2">支付宝</p>
                <img src="/donate/alipay.jpg" alt="支付宝" className="w-full rounded-xl bg-white p-2" />
              </div>
            </div>
            <p className="text-gray-500 text-xs text-center mt-4">感谢您的支持！❤️</p>
          </div>
        </div>
      )}

      {/* ===== 自定义动画样式 ===== */}
      <style jsx global>{`
        @keyframes float {
          0%, 100% { transform: translateY(0) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(5deg); }
        }
        @keyframes float-delay {
          0%, 100% { transform: translateY(0) rotate(0deg); }
          50% { transform: translateY(-15px) rotate(-5deg); }
        }
        @keyframes bounce-slow {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-10px); }
        }
        .animate-float {
          animation: float 4s ease-in-out infinite;
        }
        .animate-float-delay {
          animation: float-delay 5s ease-in-out infinite;
          animation-delay: 1s;
        }
        .animate-bounce-slow {
          animation: bounce-slow 3s ease-in-out infinite;
        }
        .perspective-1000 {
          perspective: 1000px;
        }
      `}</style>
    </div>
  );
}
