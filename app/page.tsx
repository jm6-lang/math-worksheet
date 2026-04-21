'use client';

import { useState, useEffect, useRef } from 'react';

// 轮播图数据
const CAROUSEL_ITEMS = [
  {
    id: 1,
    title: '数学练习卷',
    subtitle: '一键生成个性化练习卷',
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
    title: '数独挑战',
    subtitle: '锻炼逻辑思维',
    description: '多难度级别，计时挑战，自动校验',
    icon: '🧩',
    gradient: 'from-orange-500 via-red-500 to-pink-500',
    link: '/tools/sudoku',
  },
];

// 公告数据
const ANNOUNCEMENTS = [
  '🎉 算个题吧全新上线！支持11种题型，田字格/方格/横线格多模板',
  '📢 字帖生成器上线！支持楷体/宋体/黑体等多种字体',
  '🆕 数独游戏全新上线，支持4个难度级别',
  '💡 小贴士：点击顶部菜单可快速访问各工具',
  '🔥 免费使用，无需注册，即开即用',
];

// 工具分类
const TOOL_CATEGORIES = [
  {
    category: '📚 学习工具',
    tools: [
      { name: '数学练习卷', icon: '🧮', desc: '一键出题，PDF导出', link: '/tools/math-worksheet', color: 'blue', disabled: false },
      { name: '字帖生成器', icon: '✍️', desc: '田字格/米字格模板', link: '/tools/calligraphy', color: 'emerald', disabled: false },
      { name: '数独游戏', icon: '🧩', desc: '多难度逻辑训练', link: '/tools/sudoku', color: 'orange', disabled: false },
    ],
  },
  {
    category: '🎨 敬请期待',
    tools: [
      { name: '拼音注音', icon: '📝', desc: '汉字注音练习', link: '#', color: 'gray', disabled: true },
      { name: '英语字帖', icon: '🔤', desc: '四线三格模板', link: '#', color: 'gray', disabled: true },
      { name: '口算速练', icon: '⚡', desc: '在线计时练习', link: '#', color: 'gray', disabled: true },
    ],
  },
];

// 颜色映射
const COLOR_MAP: Record<string, string> = {
  blue: 'bg-blue-500 hover:bg-blue-600',
  emerald: 'bg-emerald-500 hover:bg-emerald-600',
  orange: 'bg-orange-500 hover:bg-orange-600',
  gray: 'bg-gray-400',
};

export default function HomePage() {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [mobileMenu, setMobileMenu] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const announcementRef = useRef<HTMLDivElement>(null);

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
      {/* ===== 顶部导航 ===== */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-xl shadow-lg shadow-blue-500/30">
                📚
              </div>
              <a href="/" className="text-xl font-bold text-white hover:opacity-80 transition-opacity">
                教材工具箱
              </a>
            </div>

            {/* 桌面导航 */}
            <div className="hidden md:flex items-center gap-1">
              <a href="/" className="px-4 py-2 text-sm text-white bg-white/10 rounded-lg font-medium">
                首页
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
            </div>

            {/* 移动端菜单按钮 */}
            <button
              onClick={() => setMobileMenu(!mobileMenu)}
              className="md:hidden p-2 text-gray-300 hover:text-white transition-colors"
            >
              {mobileMenu ? '✕' : '☰'}
            </button>
          </div>
        </div>

        {/* 移动端菜单 */}
        {mobileMenu && (
          <div className="md:hidden bg-slate-800 border-t border-white/10 py-4 px-4 space-y-1">
            <a href="/" className="block px-4 py-2 text-white bg-white/10 rounded-lg">首页</a>
            <a href="/tools/math-worksheet" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg">🧮 数学练习卷</a>
            <a href="/tools/calligraphy" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg">✍️ 字帖生成器</a>
            <a href="/tools/sudoku" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg">🧩 数独游戏</a>
          </div>
        )}
      </nav>

      {/* ===== 轮播大图区域 ===== */}
      <section className="pt-16">
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
                  <h1
                    className="text-6xl md:text-8xl font-black text-white tracking-tight"
                    style={{
                      textShadow: '0 4px 0 rgba(0,0,0,0.2), 0 8px 0 rgba(0,0,0,0.1), 0 12px 20px rgba(0,0,0,0.3)',
                      transform: 'translateZ(50px)',
                    }}
                  >
                    {item.title}
                  </h1>
                </div>

                {/* 副标题 */}
                <p className="text-2xl md:text-3xl font-bold text-white/90 mb-4 drop-shadow-lg">
                  {item.subtitle}
                </p>

                {/* 描述 */}
                <p className="text-lg text-white/80 mb-8 max-w-xl drop-shadow">
                  {item.description}
                </p>

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

      {/* ===== 底部 ===== */}
      <footer className="border-t border-white/10 py-8 px-4 text-center text-gray-500 text-sm">
        <p>© 2026 教材工具箱 · 免费好用的在线工具</p>
      </footer>

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
