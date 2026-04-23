'use client';

import { useState } from 'react';

export default function SiteLayout({ children }: { children: React.ReactNode }) {
  const [mobileMenu, setMobileMenu] = useState(false);
  const [showToolsMenu, setShowToolsMenu] = useState(false);
  const [showDonate, setShowDonate] = useState(false);
  const [showTutorial, setShowTutorial] = useState(false);
  const [showShare, setShowShare] = useState(false);
  const [copySuccess, setCopySuccess] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText('https://www.skillxm.cn');
    setCopySuccess(true);
    setTimeout(() => setCopySuccess(false), 2000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
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
              <div
                className="relative"
                onMouseEnter={() => setShowToolsMenu(true)}
                onMouseLeave={() => setShowToolsMenu(false)}
              >
                <button className="flex items-center gap-1 px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                  学习工具
                  <svg
                    className={`w-3.5 h-3.5 transition-transform ${showToolsMenu ? 'rotate-180' : ''}`}
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
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
                免费资源
              </a>

              <button onClick={() => setShowTutorial(true)} className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                使用教程
              </button>
              <button onClick={() => setShowShare(true)} className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                分享
              </button>
              <button onClick={() => setShowDonate(true)} className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                赞助支持
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

        {/* 移动端菜单 */}
        <div className={`lg:hidden fixed inset-0 z-50 transition-all duration-300 ${mobileMenu ? 'visible' : 'invisible'}`}>
          <div className={`absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity duration-300 ${mobileMenu ? 'opacity-100' : 'opacity-0'}`} onClick={() => setMobileMenu(false)} />
          <div className={`absolute right-0 top-0 h-full w-72 bg-slate-900 border-l border-white/10 shadow-2xl transition-transform duration-300 ${mobileMenu ? 'translate-x-0' : 'translate-x-full'}`}>
            <div className="flex items-center justify-between px-5 py-4 border-b border-white/10">
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-sm">📚</div>
                <span className="text-base font-bold text-white">教材工具箱</span>
              </div>
              <button onClick={() => setMobileMenu(false)} className="p-1.5 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </div>
            <div className="overflow-y-auto h-[calc(100%-60px)] py-3 px-3 space-y-1">
              <a href="/" onClick={() => setMobileMenu(false)} className="flex items-center gap-3 px-3 py-2.5 text-sm text-white bg-white/10 rounded-xl">
                <span className="w-8 h-8 bg-white/10 rounded-lg flex items-center justify-center">🏠</span>
                首页
              </a>
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
              <button onClick={() => { handleCopy(); setMobileMenu(false); }} className="w-full flex items-center gap-3 px-3 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-white/5 rounded-xl transition-colors">
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

      {/* ===== 页面内容 ===== */}
      <main className="pt-14">
        {children}
      </main>

      {/* ===== 底部页脚 ===== */}
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

      {/* ===== 赞助弹窗 ===== */}
      {showDonate && (
        <div className="fixed inset-0 z-[70] flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm" onClick={() => setShowDonate(false)}>
          <div className="bg-[#1a1a1a] border border-white/10 rounded-2xl max-w-md w-full p-8" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-white">赞助支持</h2>
              <button onClick={() => setShowDonate(false)} className="text-gray-400 hover:text-white text-2xl leading-none">&times;</button>
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
            <p className="text-gray-500 text-xs text-center mt-4">感谢您的支持！</p>
          </div>
        </div>
      )}

      {/* ===== 分享弹窗 ===== */}
      {showShare && (
        <div className="fixed inset-0 z-[70] flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm" onClick={() => setShowShare(false)}>
          <div className="bg-[#1a1a1a] border border-white/10 rounded-2xl max-w-md w-full p-8" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-white">分享给朋友</h2>
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

      {/* ===== 使用教程弹窗 ===== */}
      {showTutorial && (
        <div className="fixed inset-0 z-[70] flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm" onClick={() => setShowTutorial(false)}>
          <div className="bg-[#1a1a1a] border border-white/10 rounded-2xl max-w-2xl w-full max-h-[80vh] overflow-y-auto p-8" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-white">使用教程</h2>
              <button onClick={() => setShowTutorial(false)} className="text-gray-400 hover:text-white text-2xl leading-none">&times;</button>
            </div>
            <div className="space-y-6">
              <div className="bg-white/5 rounded-xl p-4">
                <h3 className="text-lg font-bold text-blue-400 mb-3">数学练习卷生成器</h3>
                <ol className="space-y-2 text-gray-300 text-sm list-decimal list-inside">
                  <li>选择年级（1-6年级可选）</li>
                  <li>勾选题型（加减乘除、竖式、填空等）</li>
                  <li>设置数字范围和题目数量</li>
                  <li>选择模板样式</li>
                  <li>点击&ldquo;立即出题&rdquo;生成练习卷</li>
                  <li>点击&ldquo;导出PDF&rdquo;下载打印</li>
                </ol>
              </div>
              <div className="bg-white/5 rounded-xl p-4">
                <h3 className="text-lg font-bold text-emerald-400 mb-3">字帖生成器</h3>
                <ol className="space-y-2 text-gray-300 text-sm list-decimal list-inside">
                  <li>输入要练习的汉字或词语</li>
                  <li>选择模板：田字格/米字格/方格/横线格</li>
                  <li>选择字体和排版</li>
                  <li>点击&ldquo;生成字帖&rdquo;</li>
                  <li>点击&ldquo;导出PDF&rdquo;下载打印</li>
                </ol>
              </div>
              <div className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-xl p-4 border border-blue-500/30">
                <h3 className="text-lg font-bold text-white mb-2">温馨提示</h3>
                <ul className="space-y-1 text-gray-300 text-sm list-disc list-inside">
                  <li>所有资源完全免费，无需注册</li>
                  <li>PDF导出支持A4纸打印</li>
                  <li>建议使用Chrome/Edge浏览器</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
