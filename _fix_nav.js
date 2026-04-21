const fs = require('fs');
const c = fs.readFileSync('C:/Users/Administrator/.qclaw/workspace-agent-3bb7b585/math-worksheet/app/page.tsx', 'utf8');

const i1 = c.indexOf('{/* ===== 顶部导航 ===== */}');
const i2 = c.indexOf('{/* ===== Hero 区域 ===== */}');

if (i1 < 0 || i2 < 0) { console.log('NOT FOUND'); process.exit(1); }

const before = c.substring(0, i1);
const after = c.substring(i2);

const newNav = `
      {/* ===== 顶部导航 ===== */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0f0f0f]/90 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center text-xl">🧮</div>
              <button onClick={() => { setHasGenerated(false); setQuestions([]); setShowGuide(false); window.scrollTo({ top: 0, behavior: 'smooth' }); }} className="text-xl font-bold hover:opacity-80 transition-opacity cursor-pointer bg-transparent border-none text-white">算个题吧</button>
            </div>
            {/* 桌面导航 */}
            <div className="hidden md:flex items-center gap-1">
              <button onClick={() => { setHasGenerated(false); setQuestions([]); setShowGuide(false); window.scrollTo({ top: 0, behavior: 'smooth' }); }} className="px-3 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">快速入门</button>
              <button onClick={() => setShowGuide(true)} className="px-3 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">使用教程</button>
              <div className="relative group">
                <button className="px-3 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors flex items-center gap-1">教材工具 <span className="text-xs">▾</span></button>
                <div className="absolute right-0 top-full pt-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                  <div className="bg-[#1a1a1a] border border-white/10 rounded-xl shadow-xl py-2 min-w-[160px]">
                    <a href="https://xgzb.top" target="_blank" rel="noopener noreferrer" className="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10">写个字吧（字帖）</a>
                    <a href="https://xgzb.top/game/sudoku.html" target="_blank" rel="noopener noreferrer" className="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10">数独游戏</a>
                  </div>
                </div>
              </div>
              <a href="https://xgzb.top/donate/" target="_blank" rel="noopener noreferrer" className="px-3 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">捐赠</a>
            </div>
            {/* 移动端 */}
            <button onClick={() => setMobileMenu(!mobileMenu)} className="md:hidden p-2 text-gray-300 hover:text-white transition-colors">{mobileMenu ? '✕' : '☰'}</button>
          </div>
        </div>
        {mobileMenu && (
          <div className="md:hidden bg-[#1a1a1a] border-t border-white/10 py-4 px-4 space-y-1">
            <button onClick={() => { setHasGenerated(false); setQuestions([]); setShowGuide(false); setMobileMenu(false); window.scrollTo({ top: 0, behavior: 'smooth' }); }} className="block w-full text-left px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">快速入门</button>
            <button onClick={() => { setShowGuide(true); setMobileMenu(false); }} className="block w-full text-left px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">使用教程</button>
            <div className="border-t border-white/10 my-2"></div>
            <a href="https://xgzb.top" target="_blank" rel="noopener noreferrer" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">写个字吧（字帖）</a>
            <a href="https://xgzb.top/game/sudoku.html" target="_blank" rel="noopener noreferrer" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">数独游戏</a>
            <div className="border-t border-white/10 my-2"></div>
            <a href="https://xgzb.top/donate/" target="_blank" rel="noopener noreferrer" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">捐赠</a>
          </div>
        )}
      </nav>

      {/* 使用教程弹窗 */}
      {showGuide && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" onClick={() => setShowGuide(false)}>
          <div className="bg-[#1a1a1a] border border-white/10 rounded-2xl max-w-2xl w-full max-h-[80vh] overflow-y-auto p-8" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">使用教程</h2>
              <button onClick={() => setShowGuide(false)} className="text-gray-400 hover:text-white text-2xl">✕</button>
            </div>
            <div className="space-y-6 text-gray-300">
              <div><h3 className="text-lg font-bold text-white mb-2">1️⃣ 快捷出题</h3><p className="text-sm leading-relaxed">首页提供 4 种快捷预设（10道基础、20道竖式、50道综合、100道强化），点击即可一键生成。</p></div>
              <div><h3 className="text-lg font-bold text-white mb-2">2️⃣ 选择模板</h3><p className="text-sm leading-relaxed">支持田字格、方格纸、横线格、空白纸 4 种模板，点击模板卡片切换。</p></div>
              <div><h3 className="text-lg font-bold text-white mb-2">3️⃣ 自定义配置</h3><p className="text-sm leading-relaxed">展开「高级配置」可设置年级、题型、数字范围、题目数量、每行题数、字体大小等。</p></div>
              <div><h3 className="text-lg font-bold text-white mb-2">4️⃣ 导出打印</h3><p className="text-sm leading-relaxed">导出 PDF（题目卷+答案卷），也可直接打印。PDF 为 A4 尺寸，即印即用。</p></div>
            </div>
            <button onClick={() => setShowGuide(false)} className="mt-6 w-full py-3 bg-blue-500 hover:bg-blue-600 text-white font-bold rounded-xl transition-colors">知道了</button>
          </div>
        </div>
      )}

      `;

const result = before + newNav + after;
fs.writeFileSync('C:/Users/Administrator/.qclaw/workspace-agent-3bb7b585/math-worksheet/app/page.tsx', result, 'utf8');
console.log('OK, len=' + result.length);
console.log('has 教材工具:', result.includes('教材工具'));
console.log('has 写个字吧 →:', result.includes('写个字吧 →'));
console.log('has showGuide:', result.includes('showGuide'));
