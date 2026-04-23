'use client';

import { useState, useRef } from 'react';

type LineType = 'four-line' | 'three-line' | 'blank';

const LINE_TYPES = [
  { id: 'four-line' as LineType, name: '四线三格', icon: '三', desc: '标准英语书写格' },
  { id: 'three-line' as LineType, name: '三线格', icon: '二', desc: '上下两线加基线' },
  { id: 'blank' as LineType, name: '横线格', icon: '一', desc: '横线练习' },
];

const FONT_OPTIONS = [
  { value: 'Georgia', name: '衬线', preview: 'Aa' },
  { value: 'Arial', name: '无衬线', preview: 'Aa' },
  { value: 'Comic Sans MS', name: '手写', preview: 'Aa' },
  { value: 'Times New Roman', name: 'Times', preview: 'Aa' },
  { value: 'Verdana', name: 'Verdana', preview: 'Aa' },
  { value: 'Courier New', name: '等宽', preview: 'Aa' },
];

const ROW_HEIGHT_OPTIONS = [
  { value: 80, label: '宽松' },
  { value: 60, label: '适中' },
  { value: 48, label: '紧凑' },
];

function FourLineRow({ width, height }: { width: number; height: number }) {
  const line1 = height * 0.1;
  const line2 = height * 0.4;
  const line3 = height * 0.7;
  const line4 = height * 0.95;
  return (
    <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, pointerEvents: 'none' }}>
      <div style={{ position: 'absolute', left: 0, top: line1, bottom: 0, borderRight: '1px solid #bbb' }} />
      <div style={{ position: 'absolute', left: '33.33%', top: line1, bottom: 0, borderRight: '1px solid #bbb' }} />
      <div style={{ position: 'absolute', left: '66.66%', top: line1, bottom: 0, borderRight: '1px solid #bbb' }} />
      <div style={{ position: 'absolute', right: 0, top: line1, bottom: 0, borderRight: '1px solid #bbb' }} />
      <div style={{ position: 'absolute', left: 0, right: 0, top: line1, borderBottom: '1px solid #999' }} />
      <div style={{ position: 'absolute', left: 0, right: 0, top: line2, borderBottom: '1px dashed #aaa' }} />
      <div style={{ position: 'absolute', left: 0, right: 0, top: line3, borderBottom: '1.5px solid #666' }} />
      <div style={{ position: 'absolute', left: 0, right: 0, top: line4, borderBottom: '1px solid #999' }} />
    </div>
  );
}

function ThreeLineRow({ width, height }: { width: number; height: number }) {
  const line1 = height * 0.1;
  const line2 = height * 0.65;
  const line3 = height * 0.95;
  return (
    <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, pointerEvents: 'none' }}>
      <div style={{ position: 'absolute', left: 0, top: line1, bottom: 0, borderRight: '1px solid #bbb' }} />
      <div style={{ position: 'absolute', left: '33.33%', top: line1, bottom: 0, borderRight: '1px solid #bbb' }} />
      <div style={{ position: 'absolute', left: '66.66%', top: line1, bottom: 0, borderRight: '1px solid #bbb' }} />
      <div style={{ position: 'absolute', right: 0, top: line1, bottom: 0, borderRight: '1px solid #bbb' }} />
      <div style={{ position: 'absolute', left: 0, right: 0, top: line1, borderBottom: '1px solid #999' }} />
      <div style={{ position: 'absolute', left: 0, right: 0, top: line2, borderBottom: '1.5px solid #666' }} />
      <div style={{ position: 'absolute', left: 0, right: 0, top: line3, borderBottom: '1px solid #999' }} />
    </div>
  );
}

function BlankLineRow({ width, height }: { width: number; height: number }) {
  const line = height * 0.85;
  return (
    <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, pointerEvents: 'none' }}>
      <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, borderRight: '1px solid #bbb' }} />
      <div style={{ position: 'absolute', left: '25%', top: 0, bottom: 0, borderRight: '1px solid #bbb' }} />
      <div style={{ position: 'absolute', left: '50%', top: 0, bottom: 0, borderRight: '1px solid #bbb' }} />
      <div style={{ position: 'absolute', left: '75%', top: 0, bottom: 0, borderRight: '1px solid #bbb' }} />
      <div style={{ position: 'absolute', right: 0, top: 0, bottom: 0, borderRight: '1px solid #bbb' }} />
      <div style={{ position: 'absolute', left: 0, right: 0, top: line, borderBottom: '1px solid #999' }} />
    </div>
  );
}

function PracticeRow({
  text,
  showGuide,
  fontFamily,
  lineType,
  rowHeight,
  rowWidth,
}: {
  text: string;
  showGuide: boolean;
  fontFamily: string;
  lineType: LineType;
  rowHeight: number;
  rowWidth: number;
}) {
  const fontSize = lineType === 'four-line' ? rowHeight * 0.50 : lineType === 'three-line' ? rowHeight * 0.45 : rowHeight * 0.55;
  const baselinePos = lineType === 'four-line' ? rowHeight * 0.70 : lineType === 'three-line' ? rowHeight * 0.65 : rowHeight * 0.85;
  const bottomFromBottom = rowHeight - baselinePos;

  return (
    <div style={{ position: 'relative', width: rowWidth, height: rowHeight, background: '#ffffff' }}>
      {lineType === 'four-line' && <FourLineRow width={rowWidth} height={rowHeight} />}
      {lineType === 'three-line' && <ThreeLineRow width={rowWidth} height={rowHeight} />}
      {lineType === 'blank' && <BlankLineRow width={rowWidth} height={rowHeight} />}
      {showGuide && text && (
        <span
          style={{
            position: 'absolute',
            left: 8,
            bottom: bottomFromBottom,
            fontSize,
            fontFamily,
            color: '#d0d0d0',
            lineHeight: 1,
            whiteSpace: 'nowrap',
            userSelect: 'none',
            zIndex: 2,
          }}
        >
          {text}
        </span>
      )}
    </div>
  );
}

// Conditional class helper - avoids complex string concatenation in JSX that Turbopack misparses
function btnClass(active: boolean) {
  return active
    ? 'flex-1 py-2.5 rounded-xl border-2 text-center transition-all bg-blue-50 border-blue-500 text-blue-700'
    : 'flex-1 py-2.5 rounded-xl border-2 text-center transition-all bg-gray-50 border-gray-200 text-gray-600 hover:border-gray-300';
}

function btnClassSmall(active: boolean) {
  return active
    ? 'flex-1 py-2 rounded-lg border-2 text-xs font-medium transition-all bg-blue-50 border-blue-500 text-blue-700'
    : 'flex-1 py-2 rounded-lg border-2 text-xs font-medium transition-all bg-gray-50 border-gray-200 text-gray-600 hover:border-gray-300';
}

export default function EnglishCalligraphyPage() {
  const [text, setText] = useState('The quick brown fox jumps over the lazy dog');
  const [lineType, setLineType] = useState<LineType>('four-line');
  const [rowsPerWord, setRowsPerWord] = useState(3);
  const [rowHeight, setRowHeight] = useState(60);
  const [showGuide, setShowGuide] = useState(true);
  const [fontFamily, setFontFamily] = useState('Georgia');
  const [isExporting, setIsExporting] = useState(false);
  const [mobileMenu, setMobileMenu] = useState(false);
  const previewRef = useRef<HTMLDivElement>(null);

  const words = text.trim().split(' ').filter(function(w: string) { return w.length > 0; });

  const pageWidth = 794;
  const pagePadding = 48;
  const rowWidth = pageWidth - pagePadding * 2;

  const handleExportPDF = async function() {
    if (!previewRef.current) return;
    setIsExporting(true);
    try {
      const html2canvas = (await import('html2canvas')).default;
      const jsPDF = (await import('jspdf')).default;

      const el = previewRef.current;
      const canvas = await html2canvas(el, {
        scale: 3,
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false,
        windowWidth: pageWidth,
      });

      const imgData = canvas.toDataURL('image/png');
      const pdfHeight = canvas.height / 2;
      const pdf = new jsPDF({ orientation: 'portrait', unit: 'px', format: [pageWidth, pdfHeight] });
      pdf.addImage(imgData, 'PNG', 0, 0, pageWidth, pdfHeight);
      pdf.save('英语字帖.pdf');
    } catch (e) {
      console.error(e);
      alert('导出失败，请重试');
    } finally {
      setIsExporting(false);
    }
  };

  const handlePrint = function() { window.print(); };

  return (
    <div className="min-h-screen bg-gray-100" style={{ fontFamily: '"Noto Sans SC", "Microsoft YaHei", sans-serif' }}>

      {/* ===== 顶部导航 ===== */}
      <nav className="print:hidden fixed top-0 left-0 right-0 z-50 bg-gray-900/90 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-xl">🔤</div>
              <a href="/" className="text-xl font-bold text-white hover:opacity-80 transition-opacity">英语字帖</a>
            </div>
            <div className="hidden md:flex items-center gap-1">
              <a href="/" className="px-3 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">首页</a>
              <a href="/tools/math-worksheet" className="px-3 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">🧮 数学练习卷</a>
              <a href="/tools/calligraphy" className="px-3 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">✍️ 字帖生成器</a>
              <a href="/tools/english-calligraphy" className="px-3 py-2 text-sm text-white bg-white/10 rounded-lg font-medium">🔤 英语字帖</a>
              <a href="/tools/sudoku" className="px-3 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">🧩 数独游戏</a>
            </div>
            <button onClick={() => setMobileMenu(!mobileMenu)} className="md:hidden p-2 text-gray-300 hover:text-white transition-colors">{mobileMenu ? '✕' : '☰'}</button>
          </div>
        </div>
        {mobileMenu && (
          <div className="md:hidden bg-gray-800 border-t border-white/10 py-4 px-4 space-y-1">
            <a href="/" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">首页</a>
            <a href="/tools/math-worksheet" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">🧮 数学练习卷</a>
            <a href="/tools/calligraphy" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">✍️ 字帖生成器</a>
            <a href="/tools/english-calligraphy" className="block px-4 py-2 text-white bg-white/10 rounded-lg">🔤 英语字帖</a>
            <a href="/tools/sudoku" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">🧩 数独游戏</a>
          </div>
        )}
      </nav>

      <div className="pt-20 pb-12 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">英语字帖生成器</h1>
            <p className="text-gray-500 text-sm">输入英文单词或句子，生成四线三格练习纸</p>
          </div>

          {/* Controls */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 mb-6">
            <div className="space-y-5">
              {/* Line type */}
              <div>
                <p className="text-sm text-gray-500 mb-2 font-medium">格式类型</p>
                <div className="flex gap-2">
                  {LINE_TYPES.map(function(l) {
                    return (
                      <button
                        key={l.id}
                        onClick={function() { setLineType(l.id); }}
                        className={btnClass(lineType === l.id)}
                      >
                        <div className="text-lg">{l.icon}</div>
                        <div className="text-xs font-medium mt-0.5">{l.name}</div>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Text input */}
              <div>
                <label className="block text-sm text-gray-500 mb-2 font-medium">练习内容</label>
                <textarea
                  value={text}
                  onChange={function(e: React.ChangeEvent<HTMLTextAreaElement>) { setText(e.target.value); }}
                  rows={3}
                  className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-800 placeholder-gray-400 focus:outline-none focus:border-blue-400 focus:bg-white transition-colors resize-none"
                  placeholder="输入英文单词或句子，每个空格分隔的词单独一组练习行"
                />
                <p className="text-xs text-gray-400 mt-1">共 {words.length} 个词，每词 {rowsPerWord} 行练习</p>
              </div>

              {/* Font */}
              <div>
                <label className="block text-sm text-gray-500 mb-2 font-medium">字体</label>
                <div className="grid grid-cols-3 sm:grid-cols-6 gap-2">
                  {FONT_OPTIONS.map(function(font) {
                    const isActive = fontFamily === font.value;
                    return (
                      <button
                        key={font.value}
                        onClick={function() { setFontFamily(font.value); }}
                        className={isActive
                          ? 'p-2 rounded-lg border-2 text-center transition-all bg-blue-50 border-blue-500 text-blue-700'
                          : 'p-2 rounded-lg border-2 text-center transition-all bg-gray-50 border-gray-200 text-gray-600 hover:border-gray-300'}
                      >
                        <div className="text-sm font-medium" style={{ fontFamily: font.value }}>{font.preview}</div>
                        <div className="text-[10px] text-gray-400 mt-0.5">{font.name}</div>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Row height + rows per word + guide */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm text-gray-500 mb-2 font-medium">行高</label>
                  <div className="flex gap-1.5">
                    {ROW_HEIGHT_OPTIONS.map(function(opt) {
                      return (
                        <button
                          key={opt.value}
                          onClick={function() { setRowHeight(opt.value); }}
                          className={btnClassSmall(rowHeight === opt.value)}
                        >
                          {opt.label}
                        </button>
                      );
                    })}
                  </div>
                </div>
                <div>
                  <label className="block text-sm text-gray-500 mb-2 font-medium">每词练习行数</label>
                  <div className="flex items-center gap-3 bg-gray-50 rounded-xl px-4 py-2.5 border border-gray-200">
                    <input
                      type="range" min={1} max={6} value={rowsPerWord}
                      onChange={function(e: React.ChangeEvent<HTMLInputElement>) { setRowsPerWord(Number(e.target.value)); }}
                      className="flex-1 accent-blue-500 h-1.5"
                    />
                    <span className="text-gray-700 text-sm font-medium w-4 text-center">{rowsPerWord}</span>
                  </div>
                </div>
                <div className="flex items-end">
                  <label className="flex items-center gap-2.5 cursor-pointer bg-gray-50 rounded-xl px-4 py-2.5 border border-gray-200 w-full">
                    <input
                      type="checkbox" checked={showGuide}
                      onChange={function(e: React.ChangeEvent<HTMLInputElement>) { setShowGuide(e.target.checked); }}
                      className="w-4 h-4 accent-blue-500 rounded"
                    />
                    <span className="text-sm text-gray-600">显示范字（灰色）</span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          {/* Preview - 打印时显示 */}
          <div className="print-only print-preview bg-white rounded-2xl border border-gray-200 shadow-sm p-4 mb-6">
            <p className="text-xs text-gray-400 mb-3 text-center">预览</p>
            <div className="flex justify-center overflow-x-auto">
              <div
                ref={previewRef}
                style={{
                  width: pageWidth,
                  background: '#ffffff',
                  padding: pagePadding,
                  boxSizing: 'border-box',
                }}
              >
                <div style={{ width: rowWidth }}>
                  {words.map(function(word: string, wi: number) {
                    return (
                      <div key={wi} style={{ marginBottom: rowHeight * 0.3 }}>
                        {Array.from({ length: rowsPerWord }, function(_: undefined, ri: number) {
                          return (
                            <PracticeRow
                              key={ri}
                              text={word}
                              showGuide={showGuide && ri === 0}
                              fontFamily={fontFamily}
                              lineType={lineType}
                              rowHeight={rowHeight}
                              rowWidth={rowWidth}
                            />
                          );
                        })}
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-center gap-3">
            <button
              onClick={handleExportPDF}
              disabled={isExporting || words.length === 0}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed px-6 py-2.5 rounded-xl text-white text-sm font-medium transition-colors"
            >
              {isExporting ? '导出中...' : '下载 PDF'}
            </button>
            <button
              onClick={handlePrint}
              disabled={words.length === 0}
              className="bg-gray-100 hover:bg-gray-200 px-6 py-2.5 rounded-xl text-gray-700 text-sm font-medium transition-colors"
            >
              打印
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
