'use client';

import { useState, useRef } from 'react';

type LineType = 'four-line' | 'three-line' | 'blank';

const LINE_TYPES = [
  { id: 'four-line' as LineType, name: '四线三格', icon: '≡', desc: '标准英语书写格' },
  { id: 'three-line' as LineType, name: '三线格', icon: '=', desc: '上下两线+基线' },
  { id: 'blank' as LineType, name: '横线格', icon: '—', desc: '横线练习' },
];

const FONT_OPTIONS = [
  { value: 'Georgia, serif', name: '衬线体', preview: 'Aa' },
  { value: 'Arial, sans-serif', name: '无衬线', preview: 'Aa' },
  { value: '"Comic Sans MS", cursive', name: '手写体', preview: 'Aa' },
  { value: '"Times New Roman", serif', name: 'Times', preview: 'Aa' },
  { value: 'Verdana, sans-serif', name: 'Verdana', preview: 'Aa' },
  { value: 'Courier New, monospace', name: '等宽', preview: 'Aa' },
];

const ROW_HEIGHT_OPTIONS = [
  { value: 80, label: '宽松' },
  { value: 60, label: '适中' },
  { value: 48, label: '紧凑' },
];

// 单行四线三格背景（CSS 实现，打印友好）- 含竖线
function FourLineRow({ width, height }: { width: number; height: number }) {
  const line1 = height * 0.1;
  const line2 = height * 0.4;
  const line3 = height * 0.7;
  const line4 = height * 0.95;
  return (
    <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, pointerEvents: 'none' }}>
      {/* 竖线 - 分隔每个字母格子 */}
      <div style={{ position: 'absolute', left: 0, top: line1, bottom: 0, borderRight: '0.5px solid #ddd' }} />
      <div style={{ position: 'absolute', left: '33.33%', top: line1, bottom: 0, borderRight: '0.5px solid #ddd' }} />
      <div style={{ position: 'absolute', left: '66.66%', top: line1, bottom: 0, borderRight: '0.5px solid #ddd' }} />
      <div style={{ position: 'absolute', right: 0, top: line1, bottom: 0, borderRight: '0.5px solid #ddd' }} />
      {/* 顶线 - 细实线 */}
      <div style={{ position: 'absolute', left: 0, right: 0, top: line1, borderBottom: '0.8px solid #aaa' }} />
      {/* 上中线 - 虚线 */}
      <div style={{ position: 'absolute', left: 0, right: 0, top: line2, borderBottom: '0.6px dashed #ccc' }} />
      {/* 基线 - 粗实线 */}
      <div style={{ position: 'absolute', left: 0, right: 0, top: line3, borderBottom: '1.2px solid #888' }} />
      {/* 底线 - 细实线 */}
      <div style={{ position: 'absolute', left: 0, right: 0, top: line4, borderBottom: '0.8px solid #aaa' }} />
    </div>
  );
}

function ThreeLineRow({ width, height }: { width: number; height: number }) {
  const line1 = height * 0.1;
  const line2 = height * 0.65;
  const line3 = height * 0.95;
  return (
    <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, pointerEvents: 'none' }}>
      {/* 竖线 */}
      <div style={{ position: 'absolute', left: 0, top: line1, bottom: 0, borderRight: '0.5px solid #ddd' }} />
      <div style={{ position: 'absolute', left: '33.33%', top: line1, bottom: 0, borderRight: '0.5px solid #ddd' }} />
      <div style={{ position: 'absolute', left: '66.66%', top: line1, bottom: 0, borderRight: '0.5px solid #ddd' }} />
      <div style={{ position: 'absolute', right: 0, top: line1, bottom: 0, borderRight: '0.5px solid #ddd' }} />
      <div style={{ position: 'absolute', left: 0, right: 0, top: line1, borderBottom: '0.8px solid #aaa' }} />
      <div style={{ position: 'absolute', left: 0, right: 0, top: line2, borderBottom: '1.2px solid #888' }} />
      <div style={{ position: 'absolute', left: 0, right: 0, top: line3, borderBottom: '0.8px solid #aaa' }} />
    </div>
  );
}

function BlankLineRow({ width, height }: { width: number; height: number }) {
  const line = height * 0.85;
  return (
    <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, pointerEvents: 'none' }}>
      {/* 竖线 */}
      <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, borderRight: '0.5px solid #ddd' }} />
      <div style={{ position: 'absolute', left: '25%', top: 0, bottom: 0, borderRight: '0.5px solid #ddd' }} />
      <div style={{ position: 'absolute', left: '50%', top: 0, bottom: 0, borderRight: '0.5px solid #ddd' }} />
      <div style={{ position: 'absolute', left: '75%', top: 0, bottom: 0, borderRight: '0.5px solid #ddd' }} />
      <div style={{ position: 'absolute', right: 0, top: 0, bottom: 0, borderRight: '0.5px solid #ddd' }} />
      <div style={{ position: 'absolute', left: 0, right: 0, top: line, borderBottom: '0.8px solid #aaa' }} />
    </div>
  );
}

// 单行练习行：横线 + 可选范字
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
  // 字体大小
  const fontSize = lineType === 'four-line'
    ? rowHeight * 0.50   // 四线三格：顶线到基线约占60%，字体占50%
    : lineType === 'three-line'
    ? rowHeight * 0.45
    : rowHeight * 0.55;

  // 基线位置（从顶部算）
  const baselinePos = lineType === 'four-line'
    ? rowHeight * 0.70   // 四线三格基线在70%位置
    : lineType === 'three-line'
    ? rowHeight * 0.65
    : rowHeight * 0.85;

  // 用 bottom 让字母底部对齐基线
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

export default function EnglishCalligraphyPage() {
  const [text, setText] = useState('The quick brown fox jumps over the lazy dog');
  const [lineType, setLineType] = useState<LineType>('four-line');
  const [rowsPerWord, setRowsPerWord] = useState(3);
  const [rowHeight, setRowHeight] = useState(60);
  const [showGuide, setShowGuide] = useState(true);
  const [fontFamily, setFontFamily] = useState('Georgia, serif');
  const [isExporting, setIsExporting] = useState(false);
  const previewRef = useRef<HTMLDivElement>(null);

  // 按空格分词，每个词单独一组
  const words = text.trim().split(/\s+/).filter(Boolean);

  // A4 内容区宽度（794px - 2*57px padding）
  const pageWidth = 794;
  const pagePadding = 48;
  const rowWidth = pageWidth - pagePadding * 2;

  const handleExportPDF = async () => {
    if (!previewRef.current) return;
    setIsExporting(true);
    try {
      const { default: html2canvas } = await import('html2canvas');
      const { default: jsPDF } = await import('jspdf');

      const el = previewRef.current;
      const canvas = await html2canvas(el, {
        scale: 3,
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false,
        windowWidth: pageWidth,
        onclone: (clonedDoc) => {
          // 确保克隆的文档中所有元素都可见
          const clonedEl = clonedDoc.querySelector('[data-html2canvas-ignore]');
          if (clonedEl) clonedEl.remove();
        },
      });

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({ orientation: 'portrait', unit: 'px', format: [pageWidth, canvas.height / 2] });
      pdf.addImage(imgData, 'PNG', 0, 0, pageWidth, canvas.height / 2);
      pdf.save('英语字帖.pdf');
    } catch (e) {
      console.error(e);
      alert('导出失败，请重试');
    } finally {
      setIsExporting(false);
    }
  };

  const handlePrint = () => window.print();

  // 渲染预览内容
  const renderContent = () => {
    return (
      <div style={{ width: rowWidth }}>
        {words.map((word, wi) => (
          <div key={wi} style={{ marginBottom: rowHeight * 0.3 }}>
            {Array.from({ length: rowsPerWord }, (_, ri) => (
              <PracticeRow
                key={ri}
                text={word}
                showGuide={showGuide && ri === 0}
                fontFamily={fontFamily}
                lineType={lineType}
                rowHeight={rowHeight}
                rowWidth={rowWidth}
              />
            ))}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Nav */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md border-b border-gray-200 shadow-sm print:hidden">
        <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
          <a href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center text-base">🔤</div>
            <span className="text-base font-bold text-gray-800">英语字帖</span>
          </a>
          <div className="flex items-center gap-5">
            <a href="/" className="text-sm text-gray-600 hover:text-blue-600 transition-colors">首页</a>
          </div>
        </div>
      </nav>

      <div className="pt-20 pb-12 px-4 print:hidden">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">英语字帖生成器</h1>
            <p className="text-gray-500 text-sm">输入英文单词或句子，生成四线三格练习纸 · 支持打印/PDF</p>
          </div>

          {/* Controls */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 mb-6">
            <div className="space-y-5">
              {/* Line type */}
              <div>
                <p className="text-sm text-gray-500 mb-2 font-medium">格式类型</p>
                <div className="flex gap-2">
                  {LINE_TYPES.map(l => (
                    <button
                      key={l.id}
                      onClick={() => setLineType(l.id)}
                      className={`flex-1 py-2.5 rounded-xl border-2 text-center transition-all ${
                        lineType === l.id
                          ? 'bg-blue-50 border-blue-500 text-blue-700'
                          : 'bg-gray-50 border-gray-200 text-gray-600 hover:border-gray-300'
                      }`}
                    >
                      <div className="text-lg">{l.icon}</div>
                      <div className="text-xs font-medium mt-0.5">{l.name}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Text input */}
              <div>
                <label className="block text-sm text-gray-500 mb-2 font-medium">练习内容</label>
                <textarea
                  value={text}
                  onChange={e => setText(e.target.value)}
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
                  {FONT_OPTIONS.map(font => (
                    <button
                      key={font.value}
                      onClick={() => setFontFamily(font.value)}
                      className={`p-2 rounded-lg border-2 text-center transition-all ${
                        fontFamily === font.value
                          ? 'bg-blue-50 border-blue-500 text-blue-700'
                          : 'bg-gray-50 border-gray-200 text-gray-600 hover:border-gray-300'
                      }`}
                    >
                      <div className="text-sm font-medium" style={{ fontFamily: font.value }}>{font.preview}</div>
                      <div className="text-[10px] text-gray-400 mt-0.5">{font.name}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Row height + rows per word + guide */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm text-gray-500 mb-2 font-medium">行高</label>
                  <div className="flex gap-1.5">
                    {ROW_HEIGHT_OPTIONS.map(opt => (
                      <button
                        key={opt.value}
                        onClick={() => setRowHeight(opt.value)}
                        className={`flex-1 py-2 rounded-lg border-2 text-xs font-medium transition-all ${
                          rowHeight === opt.value
                            ? 'bg-blue-50 border-blue-500 text-blue-700'
                            : 'bg-gray-50 border-gray-200 text-gray-600 hover:border-gray-300'
                        }`}
                      >
                        {opt.label}
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="block text-sm text-gray-500 mb-2 font-medium">每词练习行数</label>
                  <div className="flex items-center gap-3 bg-gray-50 rounded-xl px-4 py-2.5 border border-gray-200">
                    <input
                      type="range" min={1} max={6} value={rowsPerWord}
                      onChange={e => setRowsPerWord(Number(e.target.value))}
                      className="flex-1 accent-blue-500 h-1.5"
                    />
                    <span className="text-gray-700 text-sm font-medium w-4 text-center">{rowsPerWord}</span>
                  </div>
                </div>
                <div className="flex items-end">
                  <label className="flex items-center gap-2.5 cursor-pointer bg-gray-50 rounded-xl px-4 py-2.5 border border-gray-200 w-full">
                    <input
                      type="checkbox" checked={showGuide}
                      onChange={e => setShowGuide(e.target.checked)}
                      className="w-4 h-4 accent-blue-500 rounded"
                    />
                    <span className="text-sm text-gray-600">显示范字（灰色）</span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          {/* Preview */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-4 mb-6">
            <p className="text-xs text-gray-400 mb-3 text-center">预览</p>
            <div className="flex justify-center overflow-x-auto">
              <div
                ref={previewRef}
                style={{
                  width: pageWidth,
                  background: '#ffffff',
                  padding: `${pagePadding}px`,
                  boxSizing: 'border-box',
                }}
              >
                {renderContent()}
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
              {isExporting ? '导出中...' : '📄 下载 PDF'}
            </button>
            <button
              onClick={handlePrint}
              disabled={words.length === 0}
              className="bg-gray-100 hover:bg-gray-200 px-6 py-2.5 rounded-xl text-gray-700 text-sm font-medium transition-colors"
            >
              🖨️ 打印
            </button>
          </div>
        </div>
      </div>

      {/* 打印区域：只打印字帖内容，无多余空白 */}
      <div className="print-calligraphy" style={{ width: '210mm', padding: `${pagePadding}px`, background: '#ffffff', boxSizing: 'border-box', display: 'none' }}>
        <div style={{ width: rowWidth }}>
            {words.map((word, wi) => (
              <div key={wi} style={{ marginBottom: rowHeight * 0.3 }}>
                {Array.from({ length: rowsPerWord }, (_, ri) => (
                  <PracticeRow
                    key={ri}
                    text={word}
                    showGuide={showGuide && ri === 0}
                    fontFamily={fontFamily}
                    lineType={lineType}
                    rowHeight={rowHeight}
                    rowWidth={rowWidth}
                  />
                ))}
              </div>
            ))}
          </div>
        </div>
      </div>

      <style jsx global>{`
        @media print {
          @page { margin: 0; size: A4; }
          * { display: none !important; }
          body, html { display: block !important; margin: 0 !important; padding: 0 !important; background: white !important; }
          .print-calligraphy { display: block !important; }
          .print-calligraphy * { display: block !important; }
        }
      `}</style>
    </div>
  );
}
