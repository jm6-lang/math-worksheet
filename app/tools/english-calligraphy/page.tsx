'use client';

import { useState, useRef } from 'react';

type LineType = 'four-line' | 'three-line' | 'blank';

// 四线三格字母分类
const LETTER_HEIGHT = {
  top: ['b', 'd', 'h', 'k', 'l', 't', 'f'],           // 顶格
  middle: ['a', 'c', 'e', 'i', 'm', 'n', 'o', 'r', 's', 'u', 'v', 'w', 'x', 'z'], // 中格
  bottom: ['g', 'j', 'p', 'q', 'y'],                    // 底格
  both: ['B', 'D', 'H', 'K', 'L', 'T', 'F'],           // 大写顶格
  middleCap: ['A', 'C', 'E', 'I', 'M', 'N', 'O', 'R', 'S', 'U', 'V', 'W', 'X', 'Z'], // 大写中格
  bottomCap: ['G', 'J', 'P', 'Q', 'Y'],               // 大写底格
};

const LINE_TYPES = [
  { id: 'four-line' as LineType, name: '四线三格', icon: '≡', desc: '标准英语书写格' },
  { id: 'three-line' as LineType, name: '三线格', icon: '=', desc: '上下两线+基线' },
  { id: 'blank' as LineType, name: '横线格', icon: '—', desc: '横线练习' },
];

const FONT_OPTIONS = [
  { value: 'KaiTi, STKaiti, 楷体', name: '楷书', preview: 'Aa Bb Cc' },
  { value: 'SimSun, 宋体', name: '宋体', preview: 'Aa Bb Cc' },
  { value: 'SimHei, 黑体', name: '黑体', preview: 'Aa Bb Cc' },
  { value: 'Georgia, serif', name: '衬线', preview: 'Aa Bb Cc' },
  { value: 'Arial, sans-serif', name: '无衬线', preview: 'Aa Bb Cc' },
  { value: '"Comic Sans MS", cursive', name: '手写体', preview: 'Aa Bb Cc' },
];

const LINE_SPACING_OPTIONS = [
  { value: 60, label: '宽松', desc: '3行/页' },
  { value: 50, label: '适中', desc: '4行/页' },
  { value: 40, label: '紧凑', desc: '5行/页' },
];

// 四线三格 SVG
function FourLineSvg({ width, height }: { width: number; height: number }) {
  const top = height * 0.15;
  const mid = height * 0.5;
  const bottom = height * 0.85;
  return (
    <svg className="absolute inset-0 pointer-events-none" width={width} height={height} style={{ zIndex: 1 }}>
      {/* 上线 */}
      <line x1={0} y1={top} x2={width} y2={top} stroke="#666" strokeWidth="1" />
      {/* 中线 */}
      <line x1={0} y1={mid} x2={width} y2={mid} stroke="#999" strokeWidth="0.5" strokeDasharray="4,3" />
      {/* 基线 */}
      <line x1={0} y1={bottom} x2={width} y2={bottom} stroke="#666" strokeWidth="1" />
    </svg>
  );
}

// 三线格 SVG
function ThreeLineSvg({ width, height }: { width: number; height: number }) {
  const top = height * 0.2;
  const bottom = height * 0.8;
  return (
    <svg className="absolute inset-0 pointer-events-none" width={width} height={height} style={{ zIndex: 1 }}>
      <line x1={0} y1={top} x2={width} y2={top} stroke="#666" strokeWidth="1" />
      <line x1={0} y1={bottom} x2={width} y2={bottom} stroke="#666" strokeWidth="1" />
    </svg>
  );
}

// 横线格 SVG
function LineSvg({ width, height }: { width: number; height: number }) {
  return (
    <svg className="absolute inset-0 pointer-events-none" width={width} height={height} style={{ zIndex: 1 }}>
      <line x1={0} y1={height * 0.85} x2={width} y2={height * 0.85} stroke="#999" strokeWidth="0.5" strokeDasharray="4,3" />
    </svg>
  );
}

// 字母格组件
function LetterCell({ char, showChar, fontFamily, lineType, width, height, showGuide }: {
  char?: string;
  showChar: boolean;
  fontFamily: string;
  lineType: LineType;
  width: number;
  height: number;
  showGuide: boolean;
}) {
  const fontSize = Math.floor(height * 0.55);
  
  return (
    <div
      className="relative flex items-center justify-center overflow-hidden"
      style={{
        width,
        height,
        flexShrink: 0,
        background: '#ffffff',
      }}
    >
      {lineType === 'four-line' && <FourLineSvg width={width} height={height} />}
      {lineType === 'three-line' && <ThreeLineSvg width={width} height={height} />}
      {lineType === 'blank' && <LineSvg width={width} height={height} />}
      
      {showChar && char && (
        <span
          className="absolute select-none"
          style={{
            fontSize,
            fontFamily,
            color: '#b0b0b0',
            zIndex: 2,
            // 根据字母类型调整位置
            top: lineType === 'four-line' ? '15%' : lineType === 'three-line' ? '20%' : '5%',
          }}
        >
          {char}
        </span>
      )}
    </div>
  );
}

// 横线行组件（用于句子练习）
function LineRow({ text, showGuide, fontFamily, lineSpacing, charWidth, showChar }: {
  text: string;
  showGuide: boolean;
  fontFamily: string;
  lineSpacing: number;
  charWidth: number;
  showChar: boolean;
}) {
  const chars = text.split('').filter(c => c.trim());
  const usableWidth = charWidth * Math.min(chars.length, 15);
  
  return (
    <div 
      className="relative border-b flex items-end"
      style={{
        height: lineSpacing,
        width: usableWidth,
        background: '#ffffff',
        borderColor: '#ccc',
      }}
    >
      <LineSvg width={usableWidth} height={lineSpacing} />
      {showGuide && chars.map((c, i) => (
        <span
          key={i}
          className="absolute select-none"
          style={{
            fontSize: Math.floor(lineSpacing * 0.5),
            fontFamily,
            color: '#b0b0b0',
            left: i * charWidth + 4,
            bottom: lineSpacing * 0.15,
          }}
        >
          {c}
        </span>
      ))}
    </div>
  );
}

export default function EnglishCalligraphyPage() {
  const [text, setText] = useState('ABC DEF GHI JKL MNO PQR STU VWX YZ');
  const [lineType, setLineType] = useState<LineType>('four-line');
  const [rows, setRows] = useState(5);
  const [lineSpacing, setLineSpacing] = useState(50);
  const [showGuide, setShowGuide] = useState(true);
  const [fontFamily, setFontFamily] = useState('KaiTi, STKaiti, 楷体');
  const [isExporting, setIsExporting] = useState(false);
  const previewRef = useRef<HTMLDivElement>(null);

  const chars = text.split(/[\s,]+/).filter(c => c.trim());
  const previewWidth = 794;
  const paddingPx = 57;
  const charWidth = lineType === 'blank' ? 28 : 36;
  const colsPerRow = Math.max(1, Math.floor((previewWidth - paddingPx * 2) / charWidth));

  const handleExportPDF = async () => {
    if (!previewRef.current) return;
    setIsExporting(true);
    try {
      const { default: html2canvas } = await import('html2canvas');
      const { default: jsPDF } = await import('jspdf');
      
      const el = previewRef.current;
      const origBg = el.style.background;
      el.style.background = '#ffffff';
      
      const canvas = await html2canvas(el, {
        scale: 2,
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false,
      });
      
      el.style.background = origBg;
      
      const whiteCanvas = document.createElement('canvas');
      whiteCanvas.width = canvas.width;
      whiteCanvas.height = canvas.height;
      const ctx = whiteCanvas.getContext('2d');
      if (ctx) {
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, whiteCanvas.width, whiteCanvas.height);
        ctx.drawImage(canvas, 0, 0);
      }
      
      const imgData = (whiteCanvas.getContext('2d') ? whiteCanvas : canvas).toDataURL('image/png');
      const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
      const pw = pdf.internal.pageSize.getWidth();
      const ph = pdf.internal.pageSize.getHeight();
      pdf.addImage(imgData, 'PNG', 0, 0, pw, ph);
      pdf.save('英语字帖.pdf');
    } catch (e) {
      console.error(e);
      alert('导出失败，请重试');
    } finally {
      setIsExporting(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  // 渲染四线三格/三线格网格
  const renderGrid = () => {
    const displayChars = chars.slice(0, colsPerRow);
    const actualCols = Math.max(displayChars.length, 1);
    
    return (
      <div
        className="inline-block"
        style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${actualCols}, ${charWidth}px)`,
          gridTemplateRows: `repeat(${rows}, ${lineSpacing}px)`,
          borderBottom: '2px solid #333',
          background: '#ffffff',
        }}
      >
        {Array.from({ length: rows }, (_, rowIdx) =>
          displayChars.map((char, colIdx) => (
            <LetterCell
              key={`${rowIdx}-${colIdx}`}
              char={char}
              showChar={showGuide && rowIdx === 0}
              fontFamily={fontFamily}
              lineType={lineType}
              width={charWidth}
              height={lineSpacing}
              showGuide={showGuide}
            />
          ))
        )}
      </div>
    );
  };

  // 渲染横线格（句子练习）
  const renderLines = () => {
    const words = text.split(/[\s,]+/).filter(c => c.trim());
    return (
      <div className="inline-block" style={{ borderBottom: '2px solid #333', background: '#ffffff' }}>
        {Array.from({ length: rows }, (_, i) => (
          <LineRow
            key={i}
            text={words.slice(0, 15).join(' ')}
            showGuide={showGuide && i === 0}
            fontFamily={fontFamily}
            lineSpacing={lineSpacing}
            charWidth={charWidth}
            showChar={showGuide}
          />
        ))}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Nav */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
          <a href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center text-base">🔤</div>
            <span className="text-base font-bold text-gray-800">英语字帖</span>
          </a>
          <div className="flex items-center gap-5">
            <a href="/tools/sudoku" className="text-sm text-gray-600 hover:text-blue-600 transition-colors">数独游戏</a>
            <a href="/" className="text-sm text-gray-600 hover:text-blue-600 transition-colors">首页</a>
          </div>
        </div>
      </nav>

      <div className="pt-20 pb-12 px-4">
        <div className="max-w-5xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">英语字帖生成器</h1>
            <p className="text-gray-500 text-sm">输入英文字母或单词，一键生成四线三格练习纸 · 支持PDF下载</p>
          </div>

          {/* Controls Card */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 mb-8">
            <div className="space-y-6">
              {/* Line type */}
              <div>
                <p className="text-sm text-gray-500 mb-3 font-medium">模板类型</p>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                  {LINE_TYPES.map(l => (
                    <button
                      key={l.id}
                      onClick={() => setLineType(l.id)}
                      className={`relative p-3 rounded-xl border-2 transition-all duration-200 text-center ${
                        lineType === l.id
                          ? 'bg-blue-50 border-blue-500 text-blue-700'
                          : 'bg-gray-50 border-gray-200 text-gray-600 hover:border-gray-300 hover:bg-gray-100'
                      }`}
                    >
                      <div className="text-2xl mb-0.5">{l.icon}</div>
                      <div className="text-xs font-medium">{l.name}</div>
                      <div className="text-[10px] text-gray-400">{l.desc}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Text input */}
              <div>
                <label className="block text-sm text-gray-500 mb-2 font-medium">
                  输入练习内容
                  {lineType === 'four-line' && <span className="text-gray-400 font-normal ml-2">（建议输入大写字母）</span>}
                </label>
                <input
                  type="text"
                  value={text}
                  onChange={e => setText(e.target.value.toUpperCase())}
                  className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-800 placeholder-gray-400 focus:outline-none focus:border-blue-400 focus:bg-white transition-colors"
                  placeholder="输入英文字母或单词，如 ABC DEF GHI"
                />
                <p className="text-xs text-gray-400 mt-1">已输入 {chars.length} 个词</p>
              </div>

              {/* Font selector */}
              <div>
                <label className="block text-sm text-gray-500 mb-2 font-medium">选择字体</label>
                <div className="grid grid-cols-3 sm:grid-cols-6 gap-2">
                  {FONT_OPTIONS.map(font => (
                    <button
                      key={font.value}
                      onClick={() => setFontFamily(font.value)}
                      className={`p-2.5 rounded-lg border-2 transition-all text-center ${
                        fontFamily === font.value
                          ? 'bg-blue-50 border-blue-500 text-blue-700'
                          : 'bg-gray-50 border-gray-200 text-gray-600 hover:border-gray-300'
                      }`}
                    >
                      <div className="text-xs font-medium">{font.name}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Size + rows */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm text-gray-500 mb-2 font-medium">行高</label>
                  <div className="grid grid-cols-3 gap-1.5">
                    {LINE_SPACING_OPTIONS.map(opt => (
                      <button
                        key={opt.value}
                        onClick={() => setLineSpacing(opt.value)}
                        className={`py-2 px-1 rounded-lg border-2 text-xs transition-all ${
                          lineSpacing === opt.value
                            ? 'bg-blue-50 border-blue-500 text-blue-700'
                            : 'bg-gray-50 border-gray-200 text-gray-600 hover:border-gray-300'
                        }`}
                      >
                        <div className="font-medium">{opt.label}</div>
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="block text-sm text-gray-500 mb-2 font-medium">练习行数</label>
                  <div className="flex items-center gap-3 bg-gray-50 rounded-xl px-4 py-2.5 border border-gray-200">
                    <input
                      type="range"
                      min={3}
                      max={10}
                      value={rows}
                      onChange={e => setRows(Number(e.target.value))}
                      className="flex-1 accent-blue-500 h-1.5"
                    />
                    <span className="text-gray-700 text-sm font-medium w-6 text-center">{rows}</span>
                  </div>
                </div>
                <div className="flex items-end">
                  <label className="flex items-center gap-2.5 cursor-pointer bg-gray-50 rounded-xl px-4 py-2.5 border border-gray-200 w-full">
                    <input
                      type="checkbox"
                      checked={showGuide}
                      onChange={e => setShowGuide(e.target.checked)}
                      className="w-4 h-4 accent-blue-500 rounded"
                    />
                    <span className="text-sm text-gray-600">显示首行范字</span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          {/* Preview Card */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 mb-6">
            <div className="text-xs text-gray-400 mb-3 text-center">
              A4 预览 · {chars.length} 词 · {lineType === 'four-line' ? '四线三格' : lineType === 'three-line' ? '三线格' : '横线格'} · 每行最多 {colsPerRow} 格
            </div>
            <div className="flex justify-center overflow-x-auto bg-gray-50 rounded-xl p-4">
              <div
                ref={previewRef}
                className="bg-white shadow-lg"
                style={{
                  width: previewWidth,
                  minHeight: 1123,
                  padding: '15mm',
                  background: '#ffffff',
                }}
              >
                {lineType === 'blank' ? renderLines() : renderGrid()}
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-center gap-3">
            <button
              onClick={handleExportPDF}
              disabled={isExporting || chars.length === 0}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed px-6 py-2.5 rounded-xl text-white text-sm font-medium transition-colors flex items-center gap-2"
            >
              {isExporting ? '导出中...' : '📄 下载 PDF'}
            </button>
            <button
              onClick={handlePrint}
              disabled={chars.length === 0}
              className="bg-gray-100 hover:bg-gray-200 disabled:bg-gray-50 disabled:text-gray-400 px-6 py-2.5 rounded-xl text-gray-700 text-sm font-medium transition-colors"
            >
              🖨️ 直接打印
            </button>
          </div>
        </div>
      </div>

      {/* Print styles */}
      <style jsx global>{`
        @media print {
          nav, button { display: none !important; }
          body { background: white !important; }
        }
      `}</style>
    </div>
  );
}
