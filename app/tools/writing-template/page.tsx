'use client';

import { useState, useRef, useCallback } from 'react';
import ToolGuide from '@/components/ToolGuide';
import { toolGuides } from '@/lib/toolGuides';

// ===== 类型定义 =====
type EssayType = 'picture' | 'diary' | 'letter' | 'reading' | 'argumentative';
type GridType = 'grid' | 'lined' | 'blank';
type Grade = 1 | 2 | 3 | 4 | 5 | 6;

// ===== 作文类型配置 =====
const ESSAY_TYPE_CONFIG: Record<EssayType, {
  label: string;
  icon: string;
  description: string;
  color: string;
  tips: string[];
  openingGuide: string;
}> = {
  picture: {
    label: '看图写话',
    icon: '🖼️',
    description: '低年级适用，根据图片写话',
    color: 'from-green-500 to-emerald-600',
    tips: [
      '仔细观察图片，看看图中有什么人、物、景',
      '想一想：他们在做什么？发生了什么事？',
      '按顺序描述：先写看到的，再写想到的',
      '用上一些好词好句，让文章更生动',
    ],
    openingGuide: '仔细观察图片，我看到了……',
  },
  diary: {
    label: '日记',
    icon: '📖',
    description: '记录生活点滴',
    color: 'from-blue-500 to-cyan-600',
    tips: [
      '第一行写明日期、星期、天气',
      '选择一天中最有趣或最难忘的事来写',
      '写出自己的真实感受',
      '按时间顺序把事情的经过写清楚',
    ],
    openingGuide: '今天，我……',
  },
  letter: {
    label: '书信',
    icon: '✉️',
    description: '学会书信格式',
    color: 'from-purple-500 to-pink-600',
    tips: [
      '称呼要顶格写，后面加冒号',
      '正文每段开头空两格',
      '祝语要另起一行，空两格写',
      '署名和日期写在右下角',
    ],
    openingGuide: '您好！最近……',
  },
  reading: {
    label: '读后感',
    icon: '📚',
    description: '分享阅读感悟',
    color: 'from-orange-500 to-red-600',
    tips: [
      '开头简要介绍书名和主要内容',
      '写一写自己印象最深的情节',
      '联系实际生活，写出自己的感受',
      '结尾总结收获，表达推荐意愿',
    ],
    openingGuide: '我读了一本书，名叫《……》，它讲述了……',
  },
  argumentative: {
    label: '议论文',
    icon: '💡',
    description: '高年级适用，表达观点',
    color: 'from-indigo-500 to-violet-600',
    tips: [
      '开头明确提出自己的观点',
      '用具体事例来证明观点',
      '可以从正反两方面进行论证',
      '结尾总结观点，发出号召',
    ],
    openingGuide: '我认为……，理由如下：',
  },
};

// ===== 年级配置 =====
const GRADE_CONFIG: Record<Grade, {
  label: string;
  wordCountRange: string;
  recommendedLines: number;
  gridCount: number;
}> = {
  1: { label: '一年级', wordCountRange: '100-200字', recommendedLines: 8, gridCount: 120 },
  2: { label: '二年级', wordCountRange: '100-200字', recommendedLines: 8, gridCount: 120 },
  3: { label: '三年级', wordCountRange: '200-400字', recommendedLines: 14, gridCount: 240 },
  4: { label: '四年级', wordCountRange: '200-400字', recommendedLines: 14, gridCount: 240 },
  5: { label: '五年级', wordCountRange: '400-600字', recommendedLines: 20, gridCount: 360 },
  6: { label: '六年级', wordCountRange: '400-600字', recommendedLines: 20, gridCount: 360 },
};

// ===== 格子类型配置 =====
const GRID_TYPE_CONFIG: Record<GridType, {
  label: string;
  icon: string;
}> = {
  grid: { label: '方格稿纸', icon: '▦' },
  lined: { label: '横线稿纸', icon: '☰' },
  blank: { label: '空白纸', icon: '◻' },
};

// ===== 天气选项（日记用） =====
const WEATHER_OPTIONS = ['☀️ 晴', '⛅ 多云', '🌧️ 雨', '❄️ 雪', '🌬️ 风'];

// ===== 书信称呼选项 =====
const LETTER_RECIPIENTS = ['亲爱的妈妈', '亲爱的爸爸', '敬爱的老师', '亲爱的同学', '亲爱的朋友'];

export default function WritingTemplatePage() {
  // 配置状态
  const [essayType, setEssayType] = useState<EssayType>('picture');
  const [grade, setGrade] = useState<Grade>(3);
  const [gridType, setGridType] = useState<GridType>('grid');
  const [title, setTitle] = useState('');
  const [showTips, setShowTips] = useState(true);
  const [showOpeningGuide, setShowOpeningGuide] = useState(true);
  const [mobileMenu, setMobileMenu] = useState(false);

  // 日记特有状态
  const [diaryDate, setDiaryDate] = useState(() => {
    const now = new Date();
    return `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日`;
  });
  const [diaryWeekday, setDiaryWeekday] = useState(() => {
    const days = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
    return days[new Date().getDay()];
  });
  const [diaryWeather, setDiaryWeather] = useState('☀️ 晴');

  // 书信特有状态
  const [letterRecipient, setLetterRecipient] = useState('亲爱的妈妈');
  const [letterSender, setLetterSender] = useState('您的孩子');

  // 导出相关
  const [exporting, setExporting] = useState(false);
  const previewRef = useRef<HTMLDivElement>(null);

  // 当前配置
  const currentEssayConfig = ESSAY_TYPE_CONFIG[essayType];
  const currentGradeConfig = GRADE_CONFIG[grade];

  // 计算格子/行数
  const getLineCount = useCallback(() => {
    return currentGradeConfig.recommendedLines;
  }, [currentGradeConfig]);

  // 导出 PDF
  const handleExportPDF = useCallback(async () => {
    if (!previewRef.current) return;
    setExporting(true);
    try {
      const html2canvas = (await import('html2canvas')).default;
      const jsPDF = (await import('jspdf')).default;

      const element = previewRef.current;
      const canvas = await html2canvas(element, {
        scale: 2,
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false,
      });

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = pdf.internal.pageSize.getHeight();
      const imgWidth = canvas.width;
      const imgHeight = canvas.height;
      const ratio = Math.min(pdfWidth / imgWidth, pdfHeight / imgHeight);
      const imgX = (pdfWidth - imgWidth * ratio) / 2;
      const imgY = 0;

      pdf.addImage(imgData, 'PNG', imgX, imgY, imgWidth * ratio, imgHeight * ratio);
      pdf.save(`${title || currentEssayConfig.label}_作文模板.pdf`);
    } catch (error) {
      console.error('PDF export failed:', error);
      alert('导出失败，请重试');
    } finally {
      setExporting(false);
    }
  }, [title, currentEssayConfig.label]);

  // ===== 渲染稿纸 =====
  const renderPaper = () => {
    const lineCount = getLineCount();

    if (gridType === 'grid') {
      // 方格稿纸
      const cols = 20;
      const rows = Math.ceil(lineCount * 2.5);
      return (
        <div className="flex flex-col items-center">
          <div
            className="border border-gray-300 bg-white"
            style={{
              display: 'grid',
              gridTemplateColumns: `repeat(${cols}, 24px)`,
              gridTemplateRows: `repeat(${rows}, 24px)`,
            }}
          >
            {Array.from({ length: cols * rows }).map((_, i) => (
              <div
                key={i}
                className="border border-gray-200"
                style={{ width: 24, height: 24 }}
              />
            ))}
          </div>
        </div>
      );
    }

    if (gridType === 'lined') {
      // 横线稿纸
      return (
        <div className="flex flex-col">
          {Array.from({ length: lineCount * 2 }).map((_, i) => (
            <div
              key={i}
              className="border-b border-gray-300"
              style={{ height: 32 }}
            />
          ))}
        </div>
      );
    }

    // 空白纸
    return (
      <div
        className="border border-gray-200 bg-white"
        style={{ minHeight: lineCount * 40 }}
      />
    );
  };

  // ===== 渲染模板头部（日记格式） =====
  const renderDiaryHeader = () => (
    <div className="flex items-center justify-between mb-4 text-gray-700" style={{ fontSize: 14 }}>
      <span>{diaryDate}</span>
      <span>{diaryWeekday}</span>
      <span>{diaryWeather}</span>
    </div>
  );

  // ===== 渲染模板头部（书信格式） =====
  const renderLetterHeader = () => (
    <div className="mb-4 text-gray-700" style={{ fontSize: 14 }}>
      <div className="mb-2">{letterRecipient}：</div>
    </div>
  );

  // ===== 渲染模板尾部（书信格式） =====
  const renderLetterFooter = () => (
    <div className="mt-6 text-gray-700 text-right" style={{ fontSize: 14 }}>
      <div className="mb-2">此致</div>
      <div className="mb-4">敬礼！</div>
      <div className="mb-1">{letterSender}</div>
      <div>{diaryDate}</div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* ===== 顶部导航 ===== */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <a href="/" className="text-xl font-bold text-white hover:opacity-80 transition-opacity">
                ← 教材工具箱
              </a>
            </div>

            <div className="hidden md:flex items-center gap-2">
              <span className="text-2xl">📝</span>
              <span className="text-lg font-bold text-white">作文模板生成器</span>
            </div>

            <button
              onClick={() => setMobileMenu(!mobileMenu)}
              className="md:hidden p-2 text-gray-300 hover:text-white transition-colors"
            >
              {mobileMenu ? '✕' : '☰'}
            </button>
          </div>
        </div>

        {mobileMenu && (
          <div className="md:hidden bg-slate-800 border-t border-white/10 py-4 px-4 space-y-1">
            <a href="/" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg">首页</a>
            <a href="/tools/math-worksheet" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg">🧮 数学练习卷</a>
            <a href="/tools/calligraphy" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg">✍️ 字帖生成器</a>
            <a href="/tools/mental-math" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg">⚡ 口算速练</a>
          </div>
        )}
      </nav>

      {/* ===== 主内容 ===== */}
      <main className="pt-20 pb-8 px-4">
        <div className="max-w-7xl mx-auto">
          {/* 页面标题 */}
          <div className="text-center mb-8">
            <div className="text-5xl mb-3">📝</div>
            <h1 className="text-3xl md:text-4xl font-black text-white mb-2">作文模板生成器</h1>
            <p className="text-gray-400">选择类型，自定义配置，生成专属作文稿纸</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* ===== 左侧配置面板 ===== */}
            <div className="lg:col-span-4 space-y-5">
              {/* 作文类型选择 */}
              <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-5">
                <h2 className="text-lg font-bold text-white mb-4">选择作文类型</h2>
                <div className="space-y-2">
                  {(Object.keys(ESSAY_TYPE_CONFIG) as EssayType[]).map((type) => {
                    const config = ESSAY_TYPE_CONFIG[type];
                    return (
                      <button
                        key={type}
                        onClick={() => setEssayType(type)}
                        className={`w-full flex items-center gap-3 p-3 rounded-xl border-2 transition-all text-left ${
                          essayType === type
                            ? `border-transparent bg-gradient-to-r ${config.color} text-white`
                            : 'border-white/10 bg-slate-700/30 text-gray-300 hover:border-white/30 hover:bg-slate-700/50'
                        }`}
                      >
                        <span className="text-2xl">{config.icon}</span>
                        <div>
                          <div className="font-bold">{config.label}</div>
                          <div className={`text-xs ${essayType === type ? 'text-white/80' : 'text-gray-500'}`}>
                            {config.description}
                          </div>
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* 年级选择 */}
              <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-5">
                <h2 className="text-lg font-bold text-white mb-4">选择年级</h2>
                <div className="grid grid-cols-3 gap-2">
                  {([1, 2, 3, 4, 5, 6] as Grade[]).map((g) => (
                    <button
                      key={g}
                      onClick={() => setGrade(g)}
                      className={`py-2 px-3 rounded-xl font-bold text-sm transition-all ${
                        grade === g
                          ? 'bg-blue-500 text-white'
                          : 'bg-slate-700/50 text-gray-300 hover:bg-slate-600'
                      }`}
                    >
                      {GRADE_CONFIG[g].label}
                    </button>
                  ))}
                </div>
                <div className="mt-3 flex items-center gap-2 text-sm text-gray-400">
                  <span>推荐字数：</span>
                  <span className="text-blue-400 font-bold">{currentGradeConfig.wordCountRange}</span>
                </div>
              </div>

              {/* 格子类型 */}
              <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-5">
                <h2 className="text-lg font-bold text-white mb-4">稿纸样式</h2>
                <div className="grid grid-cols-3 gap-2">
                  {(Object.keys(GRID_TYPE_CONFIG) as GridType[]).map((type) => {
                    const config = GRID_TYPE_CONFIG[type];
                    return (
                      <button
                        key={type}
                        onClick={() => setGridType(type)}
                        className={`py-3 px-3 rounded-xl font-bold text-sm transition-all ${
                          gridType === type
                            ? 'bg-indigo-500 text-white'
                            : 'bg-slate-700/50 text-gray-300 hover:bg-slate-600'
                        }`}
                      >
                        <div className="text-xl mb-1">{config.icon}</div>
                        <div>{config.label}</div>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* 标题输入 */}
              <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-5">
                <h2 className="text-lg font-bold text-white mb-4">作文标题</h2>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="输入作文标题（可选）"
                  className="w-full bg-slate-700/50 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none transition-colors"
                />
              </div>

              {/* 日记专属配置 */}
              {essayType === 'diary' && (
                <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-5">
                  <h2 className="text-lg font-bold text-white mb-4">日记信息</h2>
                  <div className="space-y-3">
                    <div>
                      <label className="text-sm text-gray-400 mb-1 block">日期</label>
                      <input
                        type="text"
                        value={diaryDate}
                        onChange={(e) => setDiaryDate(e.target.value)}
                        className="w-full bg-slate-700/50 border border-white/10 rounded-xl px-4 py-2 text-white focus:border-blue-500 focus:outline-none transition-colors"
                      />
                    </div>
                    <div>
                      <label className="text-sm text-gray-400 mb-1 block">星期</label>
                      <select
                        value={diaryWeekday}
                        onChange={(e) => setDiaryWeekday(e.target.value)}
                        className="w-full bg-slate-700/50 border border-white/10 rounded-xl px-4 py-2 text-white focus:border-blue-500 focus:outline-none transition-colors"
                      >
                        {['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'].map((d) => (
                          <option key={d} value={d} className="bg-slate-800">{d}</option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="text-sm text-gray-400 mb-1 block">天气</label>
                      <div className="flex flex-wrap gap-2">
                        {WEATHER_OPTIONS.map((w) => (
                          <button
                            key={w}
                            onClick={() => setDiaryWeather(w)}
                            className={`px-3 py-1 rounded-lg text-sm transition-all ${
                              diaryWeather === w
                                ? 'bg-blue-500 text-white'
                                : 'bg-slate-700/50 text-gray-300 hover:bg-slate-600'
                            }`}
                          >
                            {w}
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* 书信专属配置 */}
              {essayType === 'letter' && (
                <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-5">
                  <h2 className="text-lg font-bold text-white mb-4">书信信息</h2>
                  <div className="space-y-3">
                    <div>
                      <label className="text-sm text-gray-400 mb-1 block">称呼</label>
                      <div className="flex flex-wrap gap-2 mb-2">
                        {LETTER_RECIPIENTS.map((r) => (
                          <button
                            key={r}
                            onClick={() => setLetterRecipient(r)}
                            className={`px-3 py-1 rounded-lg text-sm transition-all ${
                              letterRecipient === r
                                ? 'bg-purple-500 text-white'
                                : 'bg-slate-700/50 text-gray-300 hover:bg-slate-600'
                            }`}
                          >
                            {r}
                          </button>
                        ))}
                      </div>
                      <input
                        type="text"
                        value={letterRecipient}
                        onChange={(e) => setLetterRecipient(e.target.value)}
                        className="w-full bg-slate-700/50 border border-white/10 rounded-xl px-4 py-2 text-white focus:border-purple-500 focus:outline-none transition-colors"
                      />
                    </div>
                    <div>
                      <label className="text-sm text-gray-400 mb-1 block">署名</label>
                      <input
                        type="text"
                        value={letterSender}
                        onChange={(e) => setLetterSender(e.target.value)}
                        className="w-full bg-slate-700/50 border border-white/10 rounded-xl px-4 py-2 text-white focus:border-purple-500 focus:outline-none transition-colors"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* 显示选项 */}
              <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-5">
                <h2 className="text-lg font-bold text-white mb-4">显示选项</h2>
                <div className="space-y-3">
                  <label className="flex items-center justify-between cursor-pointer">
                    <span className="text-gray-300">显示写作提示</span>
                    <div
                      onClick={() => setShowTips(!showTips)}
                      className={`w-12 h-6 rounded-full transition-colors relative ${
                        showTips ? 'bg-blue-500' : 'bg-slate-600'
                      }`}
                    >
                      <div
                        className={`w-5 h-5 bg-white rounded-full absolute top-0.5 transition-transform ${
                          showTips ? 'translate-x-6' : 'translate-x-0.5'
                        }`}
                      />
                    </div>
                  </label>
                  <label className="flex items-center justify-between cursor-pointer">
                    <span className="text-gray-300">显示开头引导</span>
                    <div
                      onClick={() => setShowOpeningGuide(!showOpeningGuide)}
                      className={`w-12 h-6 rounded-full transition-colors relative ${
                        showOpeningGuide ? 'bg-blue-500' : 'bg-slate-600'
                      }`}
                    >
                      <div
                        className={`w-5 h-5 bg-white rounded-full absolute top-0.5 transition-transform ${
                          showOpeningGuide ? 'translate-x-6' : 'translate-x-0.5'
                        }`}
                      />
                    </div>
                  </label>
                </div>
              </div>
            </div>

            {/* ===== 右侧预览区域 ===== */}
            <div className="lg:col-span-8 space-y-5">
              {/* 写作提示 */}
              {showTips && (
                <div className={`bg-gradient-to-r ${currentEssayConfig.color} bg-opacity-20 border border-white/10 rounded-2xl p-5`}>
                  <h3 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
                    <span>{currentEssayConfig.icon}</span>
                    {currentEssayConfig.label}写作提示
                  </h3>
                  <ul className="space-y-2">
                    {currentEssayConfig.tips.map((tip, i) => (
                      <li key={i} className="flex items-start gap-2 text-white/90 text-sm">
                        <span className="text-white/60 mt-0.5 shrink-0">{i + 1}.</span>
                        <span>{tip}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* 模板预览 */}
              <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-5">
                <h2 className="text-lg font-bold text-white mb-4">模板预览</h2>
                <div className="bg-white rounded-xl shadow-2xl overflow-hidden">
                  <div
                    ref={previewRef}
                    className="p-8 md:p-12"
                    style={{ backgroundColor: '#ffffff' }}
                  >
                    {/* 标题区域 */}
                    <div className="text-center mb-6">
                      {title && (
                        <h2
                          className="font-bold text-gray-800 mb-2"
                          style={{ fontSize: 20 }}
                        >
                          {title}
                        </h2>
                      )}
                      <div className="text-gray-400 text-sm">
                        {currentEssayConfig.label} | {GRADE_CONFIG[grade].label} | 推荐字数：{currentGradeConfig.wordCountRange}
                      </div>
                    </div>

                    {/* 日记头部 */}
                    {essayType === 'diary' && renderDiaryHeader()}

                    {/* 书信头部 */}
                    {essayType === 'letter' && renderLetterHeader()}

                    {/* 开头引导 */}
                    {showOpeningGuide && essayType !== 'letter' && (
                      <div
                        className="mb-4 pl-4 border-l-4 border-blue-300 text-gray-400 italic"
                        style={{ fontSize: 14 }}
                      >
                        {currentEssayConfig.openingGuide}
                      </div>
                    )}

                    {/* 稿纸区域 */}
                    {renderPaper()}

                    {/* 书信尾部 */}
                    {essayType === 'letter' && renderLetterFooter()}
                  </div>
                </div>
              </div>

              {/* 导出按钮 */}
              <div className="flex flex-wrap gap-4 justify-center">
                <button
                  onClick={handleExportPDF}
                  disabled={exporting}
                  className="px-8 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-bold rounded-xl shadow-lg hover:scale-105 transition-transform disabled:opacity-50 disabled:hover:scale-100 flex items-center gap-2"
                >
                  {exporting ? (
                    <>
                      <span className="animate-spin">⏳</span>
                      导出中...
                    </>
                  ) : (
                    <>
                      <span>📄</span>
                      导出 PDF
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* ===== 页脚 ===== */}
      <footer className="border-t border-white/10 py-6 px-4 mt-8">
        <div className="max-w-7xl mx-auto text-center text-gray-500 text-sm">
          <p>📝 作文模板生成器 - 教材工具箱 | 免费在线生成作文稿纸模板</p>
        </div>
      </footer>

      {/* 工具介绍（SEO） */}
      <section className="max-w-7xl mx-auto px-4 pb-8">
        <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-6 md:p-8">
          <h2 className="text-xl font-bold text-white mb-4">作文模板生成器 - 功能介绍与使用指南</h2>
          <div className="text-gray-400 leading-relaxed space-y-3 text-sm md:text-base">
            <p>
              作文模板生成器是一款专为小学1-6年级学生设计的作文稿纸在线生成工具，提供看图写话、日记、书信、读后感、议论文5种常见作文类型模板。每种类型都配有针对性的写作提示和开头引导语，帮助学生快速理清写作思路。例如，看图写话模板会引导学生从"观察图片-描述内容-展开想象"三个层次进行写作，书信模板则自动生成标准的称呼、此致敬礼、署名日期等格式要素。
            </p>
            <p>
              在稿纸样式方面，工具提供方格稿纸、横线稿纸、空白纸三种格式。方格稿纸是最常用的小学作文书写格式，每个方格对应一个汉字，帮助学生控制字数和书写工整度；横线稿纸适合高年级学生进行流畅的段落书写；空白纸则给有更高自由度需求的学生使用。系统根据年级自动推荐合适的字数范围（低年级100-200字、中年级200-400字、高年级400-600字），并据此调整稿纸的行列数量。日记模板支持自定义日期、星期和天气信息，书信模板提供多种常用称呼选项。生成的模板支持PDF格式导出，可直接打印使用。
            </p>
            <p>
              <strong className="text-gray-300">使用场景：</strong>日常写作练习、周末日记、读书笔记、语文课堂作文训练、假期作文作业等。建议孩子养成每天写日记的习惯，从低年级的几句话开始，逐步过渡到完整的段落和文章。写作时先列提纲再动笔，注意段落分明、语句通顺，善用学过的好词好句。坚持练习，写作能力会得到显著提升。
            </p>
          </div>
        </div>
      </section>

      {/* 使用指南 */}
      <div className="max-w-4xl mx-auto px-4 py-12">
        <ToolGuide {...toolGuides['writing-template']} />
      </div>
    </div>
  );
}
