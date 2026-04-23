'use client';

import { useState, useRef, useCallback } from 'react';

// ===== 类型定义 =====
interface CharItem {
  id: string;
  char: string;
  pinyin: string;
  words: string[];
}

type CardSize = 'large' | 'medium' | 'small';
type FontFamily = 'kaiti' | 'songti' | 'heiti';
type BorderStyle = 'solid' | 'dashed' | 'none';

// ===== 预设数据 =====
const GRADE_PRESETS: Record<string, { label: string; icon: string; chars: string }> = {
  grade1: {
    label: '一年级',
    icon: '🌱',
    chars: '一二三四五六七八九十上下左右大小多少',
  },
  grade2: {
    label: '二年级',
    icon: '🌿',
    chars: '春夏秋冬风雨雪花草树木山水日月星',
  },
  grade3: {
    label: '三年级',
    icon: '🌳',
    chars: '学校老师同学朋友读书写字画画唱歌',
  },
};

// 常见汉字拼音映射（部分常用字）
const PINYIN_MAP: Record<string, string> = {
  '一': 'yī', '二': 'èr', '三': 'sān', '四': 'sì', '五': 'wǔ',
  '六': 'liù', '七': 'qī', '八': 'bā', '九': 'jiǔ', '十': 'shí',
  '上': 'shàng', '下': 'xià', '左': 'zuǒ', '右': 'yòu',
  '大': 'dà', '小': 'xiǎo', '多': 'duō', '少': 'shǎo',
  '春': 'chūn', '夏': 'xià', '秋': 'qiū', '冬': 'dōng',
  '风': 'fēng', '雨': 'yǔ', '雪': 'xuě', '花': 'huā',
  '草': 'cǎo', '树': 'shù', '木': 'mù', '山': 'shān',
  '水': 'shuǐ', '日': 'rì', '月': 'yuè', '星': 'xīng',
  '学': 'xué', '校': 'xiào', '老': 'lǎo', '师': 'shī',
  '同': 'tóng', '朋': 'péng', '友': 'yǒu', '读': 'dú',
  '书': 'shū', '写': 'xiě', '字': 'zì', '画': 'huà',
  '唱': 'chàng', '歌': 'gē',
};

// 常见汉字组词映射
const WORDS_MAP: Record<string, string[]> = {
  '一': ['一个', '一起'], '二': ['二月', '第二'], '三': ['三月', '三个'],
  '四': ['四方', '四个'], '五': ['五月', '五个'], '六': ['六月', '六个'],
  '七': ['七月', '七个'], '八': ['八月', '八个'], '九': ['九月', '九个'],
  '十': ['十月', '十个'], '上': ['上学', '上面'], '下': ['下雨', '下面'],
  '左': ['左边', '左手'], '右': ['右边', '右手'], '大': ['大人', '大家'],
  '小': ['小鸟', '小花'], '多': ['多少', '许多'], '少': ['多少', '少年'],
  '春': ['春天', '春风'], '夏': ['夏天', '夏日'], '秋': ['秋天', '秋风'],
  '冬': ['冬天', '冬日'], '风': ['大风', '风雨'], '雨': ['下雨', '大雨'],
  '雪': ['下雪', '雪花'], '花': ['花朵', '开花'], '草': ['小草', '草地'],
  '树': ['大树', '树木'], '木': ['木头', '树木'], '山': ['大山', '山水'],
  '水': ['山水', '喝水'], '日': ['日月', '日子'], '月': ['日月', '月亮'],
  '星': ['星星', '星空'], '学': ['学习', '学校'], '校': ['学校', '校长'],
  '老': ['老师', '老人'], '师': ['老师', '师父'], '同': ['同学', '一同'],
  '朋': ['朋友', '小朋友'], '友': ['朋友', '友好'], '读': ['读书', '朗读'],
  '书': ['读书', '书本'], '写': ['写字', '写作'], '字': ['写字', '汉字'],
  '画': ['画画', '图画'], '唱': ['唱歌', '歌唱'], '歌': ['唱歌', '歌曲'],
};

// 卡片颜色列表
const CARD_COLORS = [
  'border-red-400',
  'border-blue-400',
  'border-green-400',
  'border-yellow-400',
  'border-purple-400',
  'border-pink-400',
  'border-indigo-400',
  'border-orange-400',
  'border-teal-400',
  'border-cyan-400',
];

// ===== 工具函数 =====
function generateId(): string {
  return Math.random().toString(36).substring(2, 9);
}

function parseCharsInput(input: string): CharItem[] {
  // 支持逗号、空格、换行分隔
  const chars = input
    .replace(/[,，\s]+/g, '\n')
    .split('\n')
    .map(c => c.trim())
    .filter(c => c.length > 0);

  return chars.map(char => ({
    id: generateId(),
    char: char.charAt(0),
    pinyin: PINYIN_MAP[char.charAt(0)] ?? '',
    words: WORDS_MAP[char.charAt(0)] ?? ['', ''],
  }));
}

// ===== 主组件 =====
export default function FlashcardsPage() {
  // 输入状态
  const [inputText, setInputText] = useState('');
  const [charItems, setCharItems] = useState<CharItem[]>([]);

  // 配置状态
  const [cardSize, setCardSize] = useState<CardSize>('large');
  const [showPinyin, setShowPinyin] = useState(true);
  const [showWords, setShowWords] = useState(true);
  const [fontFamily, setFontFamily] = useState<FontFamily>('kaiti');
  const [borderStyle, setBorderStyle] = useState<BorderStyle>('solid');

  // UI 状态
  const [flippedCards, setFlippedCards] = useState<Set<string>>(new Set());
  const [isExporting, setIsExporting] = useState(false);
  const [mobileMenu, setMobileMenu] = useState(false);
  const previewRef = useRef<HTMLDivElement>(null);
  const frontExportRef = useRef<HTMLDivElement>(null);
  const backExportRef = useRef<HTMLDivElement>(null);

  // 字体映射
  const fontFamilyMap: Record<FontFamily, string> = {
    kaiti: '"KaiTi", "楷体", "STKaiti", serif',
    songti: '"SimSun", "宋体", "STSong", serif',
    heiti: '"SimHei", "黑体", "STHeiti", sans-serif',
  };

  // 卡片大小映射
  const cardSizeConfig: Record<CardSize, { label: string; perPage: number; previewClass: string; exportClass: string }> = {
    large: {
      label: '大卡片（每页2个）',
      perPage: 2,
      previewClass: 'w-full sm:w-[280px] h-[380px]',
      exportClass: 'w-[340px] h-[460px]',
    },
    medium: {
      label: '中卡片（每页4个）',
      perPage: 4,
      previewClass: 'w-full sm:w-[200px] h-[280px]',
      exportClass: 'w-[250px] h-[340px]',
    },
    small: {
      label: '小卡片（每页6个）',
      perPage: 6,
      previewClass: 'w-full sm:w-[160px] h-[220px]',
      exportClass: 'w-[190px] h-[260px]',
    },
  };

  // 边框样式映射
  const borderClassMap: Record<BorderStyle, string> = {
    solid: 'border-2',
    dashed: 'border-2 border-dashed',
    none: 'border-0',
  };

  // 生成卡片
  const handleGenerate = useCallback(() => {
    if (!inputText.trim()) return;
    const items = parseCharsInput(inputText);
    setCharItems(items);
    setFlippedCards(new Set());
  }, [inputText]);

  // 加载预设
  const loadPreset = useCallback((gradeKey: string) => {
    const preset = GRADE_PRESETS[gradeKey];
    if (preset) {
      setInputText(preset.chars);
      const items = parseCharsInput(preset.chars);
      setCharItems(items);
      setFlippedCards(new Set());
    }
  }, []);

  // 翻转卡片
  const toggleFlip = useCallback((id: string) => {
    setFlippedCards(prev => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  }, []);

  // 更新单个字的拼音
  const updatePinyin = useCallback((id: string, pinyin: string) => {
    setCharItems(prev => prev.map(item =>
      item.id === id ? { ...item, pinyin } : item
    ));
  }, []);

  // 更新单个字的组词
  const updateWord = useCallback((id: string, index: number, word: string) => {
    setCharItems(prev => prev.map(item => {
      if (item.id !== id) return item;
      const newWords = [...item.words];
      newWords[index] = word;
      return { ...item, words: newWords };
    }));
  }, []);

  // 删除单个字
  const removeChar = useCallback((id: string) => {
    setCharItems(prev => prev.filter(item => item.id !== id));
  }, []);

  // 导出 PDF
  const exportPDF = useCallback(async (side: 'front' | 'back') => {
    if (charItems.length === 0) return;
    setIsExporting(true);

    try {
      const html2canvas = (await import('html2canvas')).default;
      const jsPDF = (await import('jspdf')).default;

      const targetRef = side === 'front' ? frontExportRef.current : backExportRef.current;
      if (!targetRef) return;

      // 临时显示导出区域（放在可见区域，避免 html2canvas 无法渲染屏幕外元素）
      targetRef.style.display = 'block';
      targetRef.style.position = 'fixed';
      targetRef.style.left = '0';
      targetRef.style.top = '0';
      targetRef.style.zIndex = '-1';
      targetRef.style.opacity = '0';
      targetRef.style.pointerEvents = 'none';

      // 等待浏览器完成布局渲染
      await new Promise(resolve => setTimeout(resolve, 300));

      const config = cardSizeConfig[cardSize];
      const perPage = config.perPage;
      const totalPages = Math.ceil(charItems.length / perPage);

      const pdf = new jsPDF('p', 'mm', 'a4');
      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();

      for (let page = 0; page < totalPages; page++) {
        if (page > 0) pdf.addPage();

        // 渲染当前页的卡片
        const pageCards = targetRef.querySelectorAll(`[data-page="${page}"]`);
        if (pageCards.length === 0) continue;

        const canvas = await html2canvas(pageCards[0] as HTMLElement, {
          scale: 2,
          backgroundColor: '#ffffff',
          useCORS: true,
          logging: false,
        });

        const imgData = canvas.toDataURL('image/png');
        const imgWidth = pageWidth;
        const imgHeight = (canvas.height * pageWidth) / canvas.width;

        pdf.addImage(imgData, 'PNG', 0, 0, imgWidth, Math.min(imgHeight, pageHeight));
      }

      // 恢复导出区域的隐藏状态
      targetRef.style.display = 'none';
      targetRef.style.opacity = '';
      targetRef.style.pointerEvents = '';
      targetRef.style.position = '';
      targetRef.style.left = '';
      targetRef.style.top = '';
      targetRef.style.zIndex = '';

      pdf.save(`识字卡片_${side === 'front' ? '正面' : '反面'}.pdf`);
    } catch (error) {
      console.error('导出 PDF 失败:', error);
      alert('导出 PDF 失败，请重试');
    } finally {
      setIsExporting(false);
    }
  }, [charItems, cardSize]);

  // 渲染单个卡片（正面）
  const renderFrontCard = (item: CharItem, index: number, isExport = false) => {
    const colorClass = CARD_COLORS[index % CARD_COLORS.length];
    const config = cardSizeConfig[cardSize];
    const sizeClass = isExport ? config.exportClass : config.previewClass;
    const font = fontFamilyMap[fontFamily];

    return (
      <div
        key={item.id}
        className={`${sizeClass} bg-white rounded-2xl shadow-lg flex flex-col items-center justify-center p-4 ${borderClassMap[borderStyle]} ${colorClass} relative overflow-hidden`}
        style={{ fontFamily: font }}
      >
        {/* 拼音 */}
        {showPinyin && item.pinyin && (
          <div className="text-lg md:text-xl text-gray-500 mb-2 tracking-widest" style={{ fontFamily: 'sans-serif' }}>
            {item.pinyin}
          </div>
        )}

        {/* 汉字 */}
        <div
          className="text-6xl md:text-8xl font-bold text-gray-800 leading-none"
          style={{ fontFamily: font }}
        >
          {item.char}
        </div>

        {/* 序号标记 */}
        {!isExport && (
          <div className="absolute top-2 right-3 text-xs text-gray-300 font-mono">
            {index + 1}
          </div>
        )}
      </div>
    );
  };

  // 渲染单个卡片（反面）
  const renderBackCard = (item: CharItem, index: number, isExport = false) => {
    const colorClass = CARD_COLORS[index % CARD_COLORS.length];
    const config = cardSizeConfig[cardSize];
    const sizeClass = isExport ? config.exportClass : config.previewClass;
    const font = fontFamilyMap[fontFamily];

    return (
      <div
        key={item.id}
        className={`${sizeClass} bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl shadow-lg flex flex-col items-center justify-center p-4 ${borderClassMap[borderStyle]} ${colorClass} relative overflow-hidden`}
        style={{ fontFamily: font }}
      >
        {/* 组词 */}
        {showWords && (
          <div className="text-center space-y-2">
            {item.words.filter(w => w).map((word, wi) => (
              <div
                key={wi}
                className="text-2xl md:text-3xl text-gray-700 font-semibold"
                style={{ fontFamily: font }}
              >
                {word}
              </div>
            ))}
          </div>
        )}

        {/* 笔画数提示 */}
        <div className="mt-4 text-sm text-gray-400" style={{ fontFamily: 'sans-serif' }}>
          笔画数：{item.char.length}画
        </div>

        {/* 序号标记 */}
        {!isExport && (
          <div className="absolute top-2 right-3 text-xs text-gray-300 font-mono">
            {index + 1}
          </div>
        )}
      </div>
    );
  };

  // 渲染可翻转的预览卡片
  const renderFlipCard = (item: CharItem, index: number) => {
    const isFlipped = flippedCards.has(item.id);

    return (
      <div
        key={item.id}
        className="cursor-pointer"
        onClick={() => toggleFlip(item.id)}
      >
        <div
          className={`relative transition-transform duration-500 ${cardSizeConfig[cardSize].previewClass}`}
          style={{
            perspective: '1000px',
          }}
        >
          <div
            className="w-full h-full transition-transform duration-500 relative"
            style={{
              transformStyle: 'preserve-3d',
              transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
            }}
          >
            {/* 正面 */}
            <div className="absolute inset-0" style={{ backfaceVisibility: 'hidden' }}>
              {renderFrontCard(item, index)}
            </div>
            {/* 反面 */}
            <div
              className="absolute inset-0"
              style={{
                backfaceVisibility: 'hidden',
                transform: 'rotateY(180deg)',
              }}
            >
              {renderBackCard(item, index)}
            </div>
          </div>
        </div>
        <div className="text-center text-xs text-gray-500 mt-1">
          点击翻转
        </div>
      </div>
    );
  };

  // 渲染导出用的卡片网格（按页分组）
  const renderExportGrid = (side: 'front' | 'back') => {
    const perPage = cardSizeConfig[cardSize].perPage;
    const totalPages = Math.ceil(charItems.length / perPage);
    const gridCols = perPage === 2 ? 'grid-cols-2' : perPage === 4 ? 'grid-cols-2' : 'grid-cols-3';

    return (
      <div ref={side === 'front' ? frontExportRef : backExportRef} style={{ display: 'none' }}>
        {Array.from({ length: totalPages }, (_, pageIdx) => {
          const startIdx = pageIdx * perPage;
          const pageItems = charItems.slice(startIdx, startIdx + perPage);

          return (
            <div
              key={pageIdx}
              data-page={pageIdx}
              className={`grid ${gridCols} gap-4 p-6 bg-white`}
              style={{ width: '210mm', minHeight: '297mm' }}
            >
              {pageItems.map((item, i) =>
                side === 'front'
                  ? renderFrontCard(item, startIdx + i, true)
                  : renderBackCard(item, startIdx + i, true)
              )}
            </div>
          );
        })}
      </div>
    );
  };

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
              <span className="text-2xl">🃏</span>
              <span className="text-lg font-bold text-white">识字卡片生成器</span>
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
          </div>
        )}
      </nav>

      <main className="pt-20 pb-8 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

            {/* ===== 左侧：输入和配置面板 ===== */}
            <div className="lg:col-span-4 space-y-6">

              {/* 汉字输入区 */}
              <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-6">
                <h2 className="text-xl font-bold text-white mb-4">输入汉字</h2>
                <textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="输入汉字，每行一个或用逗号分隔&#10;例如：一二三四五六七八九十"
                  className="w-full h-32 bg-slate-900/50 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:border-purple-500 focus:outline-none resize-none"
                />
                <button
                  onClick={handleGenerate}
                  disabled={!inputText.trim()}
                  className="w-full mt-3 py-3 bg-gradient-to-r from-purple-500 to-pink-600 text-white font-bold rounded-xl hover:opacity-90 transition-opacity disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  生成卡片
                </button>
              </div>

              {/* 年级预设 */}
              <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-6">
                <h2 className="text-xl font-bold text-white mb-4">年级预设</h2>
                <div className="space-y-2">
                  {Object.entries(GRADE_PRESETS).map(([key, preset]) => (
                    <button
                      key={key}
                      onClick={() => loadPreset(key)}
                      className="w-full flex items-center gap-3 px-4 py-3 bg-slate-700/50 border border-white/10 rounded-xl text-gray-300 hover:bg-slate-600/50 hover:border-white/20 transition-all"
                    >
                      <span className="text-2xl">{preset.icon}</span>
                      <div className="text-left">
                        <div className="font-semibold text-white">{preset.label}</div>
                        <div className="text-xs text-gray-400 truncate max-w-[200px]">{preset.chars}</div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* 卡片样式选择 */}
              <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-6">
                <h2 className="text-xl font-bold text-white mb-4">卡片大小</h2>
                <div className="space-y-2">
                  {(Object.keys(cardSizeConfig) as CardSize[]).map((size) => (
                    <button
                      key={size}
                      onClick={() => setCardSize(size)}
                      className={`w-full px-4 py-3 rounded-xl font-medium transition-all ${
                        cardSize === size
                          ? 'bg-gradient-to-r from-purple-500 to-pink-600 text-white'
                          : 'bg-slate-700/50 text-gray-300 hover:bg-slate-600/50 border border-white/10'
                      }`}
                    >
                      {cardSizeConfig[size].label}
                    </button>
                  ))}
                </div>
              </div>

              {/* 配置选项 */}
              <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-6">
                <h2 className="text-xl font-bold text-white mb-4">配置选项</h2>
                <div className="space-y-4">
                  {/* 显示拼音 */}
                  <label className="flex items-center justify-between cursor-pointer">
                    <span className="text-gray-300">显示拼音</span>
                    <div
                      onClick={() => setShowPinyin(!showPinyin)}
                      className={`w-12 h-6 rounded-full transition-colors relative ${showPinyin ? 'bg-purple-500' : 'bg-slate-600'}`}
                    >
                      <div className={`absolute top-0.5 w-5 h-5 bg-white rounded-full transition-transform ${showPinyin ? 'translate-x-6' : 'translate-x-0.5'}`} />
                    </div>
                  </label>

                  {/* 显示组词 */}
                  <label className="flex items-center justify-between cursor-pointer">
                    <span className="text-gray-300">显示组词</span>
                    <div
                      onClick={() => setShowWords(!showWords)}
                      className={`w-12 h-6 rounded-full transition-colors relative ${showWords ? 'bg-purple-500' : 'bg-slate-600'}`}
                    >
                      <div className={`absolute top-0.5 w-5 h-5 bg-white rounded-full transition-transform ${showWords ? 'translate-x-6' : 'translate-x-0.5'}`} />
                    </div>
                  </label>

                  {/* 字体选择 */}
                  <div>
                    <span className="text-gray-300 block mb-2">字体选择</span>
                    <div className="grid grid-cols-3 gap-2">
                      {([
                        { key: 'kaiti' as FontFamily, label: '楷体' },
                        { key: 'songti' as FontFamily, label: '宋体' },
                        { key: 'heiti' as FontFamily, label: '黑体' },
                      ]).map(({ key, label }) => (
                        <button
                          key={key}
                          onClick={() => setFontFamily(key)}
                          className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                            fontFamily === key
                              ? 'bg-purple-500 text-white'
                              : 'bg-slate-700/50 text-gray-300 hover:bg-slate-600/50'
                          }`}
                        >
                          {label}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* 边框样式 */}
                  <div>
                    <span className="text-gray-300 block mb-2">边框样式</span>
                    <div className="grid grid-cols-3 gap-2">
                      {([
                        { key: 'solid' as BorderStyle, label: '实线' },
                        { key: 'dashed' as BorderStyle, label: '虚线' },
                        { key: 'none' as BorderStyle, label: '无边框' },
                      ]).map(({ key, label }) => (
                        <button
                          key={key}
                          onClick={() => setBorderStyle(key)}
                          className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                            borderStyle === key
                              ? 'bg-purple-500 text-white'
                              : 'bg-slate-700/50 text-gray-300 hover:bg-slate-600/50'
                          }`}
                        >
                          {label}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* 汉字编辑列表 */}
              {charItems.length > 0 && (
                <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-6">
                  <h2 className="text-xl font-bold text-white mb-4">编辑汉字 ({charItems.length})</h2>
                  <div className="space-y-3 max-h-[400px] overflow-y-auto pr-1">
                    {charItems.map((item) => (
                      <div key={item.id} className="bg-slate-900/50 rounded-xl p-3 border border-white/5">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-2xl font-bold text-white">{item.char}</span>
                          <button
                            onClick={() => removeChar(item.id)}
                            className="text-red-400 hover:text-red-300 text-sm px-2 py-1 rounded-lg hover:bg-red-500/10 transition-colors"
                          >
                            删除
                          </button>
                        </div>
                        <input
                          type="text"
                          value={item.pinyin}
                          onChange={(e) => updatePinyin(item.id, e.target.value)}
                          placeholder="拼音"
                          className="w-full bg-slate-800 border border-white/10 rounded-lg px-3 py-1.5 text-sm text-white placeholder-gray-500 focus:border-purple-500 focus:outline-none mb-1.5"
                        />
                        <div className="flex gap-2">
                          <input
                            type="text"
                            value={item.words[0] ?? ''}
                            onChange={(e) => updateWord(item.id, 0, e.target.value)}
                            placeholder="组词1"
                            className="flex-1 bg-slate-800 border border-white/10 rounded-lg px-3 py-1.5 text-sm text-white placeholder-gray-500 focus:border-purple-500 focus:outline-none"
                          />
                          <input
                            type="text"
                            value={item.words[1] ?? ''}
                            onChange={(e) => updateWord(item.id, 1, e.target.value)}
                            placeholder="组词2"
                            className="flex-1 bg-slate-800 border border-white/10 rounded-lg px-3 py-1.5 text-sm text-white placeholder-gray-500 focus:border-purple-500 focus:outline-none"
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* ===== 右侧：卡片预览区域 ===== */}
            <div className="lg:col-span-8 space-y-6">
              <div ref={previewRef}>
                {charItems.length === 0 ? (
                  /* 空状态 */
                  <div className="bg-slate-800/30 border border-white/10 rounded-2xl p-12 text-center">
                    <div className="text-6xl mb-4">🃏</div>
                    <h2 className="text-2xl font-bold text-white mb-2">识字卡片预览</h2>
                    <p className="text-gray-400">在左侧输入汉字或选择年级预设，即可生成识字卡片</p>
                  </div>
                ) : (
                  <>
                    {/* 预览标题 */}
                    <div className="flex items-center justify-between mb-4">
                      <h2 className="text-xl font-bold text-white">
                        卡片预览 ({charItems.length} 张)
                      </h2>
                      <div className="flex gap-2">
                        <button
                          onClick={() => setFlippedCards(new Set())}
                          className="px-3 py-1.5 text-sm bg-slate-700/50 text-gray-300 rounded-lg hover:bg-slate-600/50 transition-colors"
                        >
                          全部翻回正面
                        </button>
                        <button
                          onClick={() => setFlippedCards(new Set(charItems.map(i => i.id)))}
                          className="px-3 py-1.5 text-sm bg-slate-700/50 text-gray-300 rounded-lg hover:bg-slate-600/50 transition-colors"
                        >
                          全部翻到反面
                        </button>
                      </div>
                    </div>

                    {/* 卡片网格 */}
                    <div className={`grid gap-6 justify-items-center ${
                      cardSize === 'large' ? 'grid-cols-1 sm:grid-cols-2' :
                      cardSize === 'medium' ? 'grid-cols-2 sm:grid-cols-2 md:grid-cols-4' :
                      'grid-cols-2 sm:grid-cols-3 md:grid-cols-3'
                    }`}>
                      {charItems.map((item, index) => renderFlipCard(item, index))}
                    </div>

                    {/* 导出按钮区域 */}
                    <div className="mt-8 bg-slate-800/50 border border-white/10 rounded-2xl p-6">
                      <h3 className="text-lg font-bold text-white mb-4">导出 PDF</h3>
                      <p className="text-gray-400 text-sm mb-4">
                        正反面分开导出，方便双面打印。打印时将正面和反面分别打印在纸张的两面。
                      </p>
                      <div className="flex flex-wrap gap-3">
                        <button
                          onClick={() => exportPDF('front')}
                          disabled={isExporting || charItems.length === 0}
                          className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-600 text-white font-bold rounded-xl hover:opacity-90 transition-opacity disabled:opacity-40 disabled:cursor-not-allowed"
                        >
                          {isExporting ? '导出中...' : '📄 导出正面'}
                        </button>
                        <button
                          onClick={() => exportPDF('back')}
                          disabled={isExporting || charItems.length === 0}
                          className="px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-bold rounded-xl hover:opacity-90 transition-opacity disabled:opacity-40 disabled:cursor-not-allowed"
                        >
                          {isExporting ? '导出中...' : '📄 导出反面'}
                        </button>
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* ===== 导出用隐藏区域 ===== */}
      {renderExportGrid('front')}
      {renderExportGrid('back')}

      {/* ===== 页脚 ===== */}
      <footer className="border-t border-white/10 py-6 px-4 mt-8">
        <div className="max-w-7xl mx-auto text-center text-gray-500 text-sm">
          <p>🃏 识字卡片生成器 - 免费在线生成识字卡片，支持自定义汉字、拼音、组词，可打印制作实体卡片</p>
          <p className="mt-1">© 2024 教材工具箱</p>
        </div>
      </footer>
    </div>
  );
}
