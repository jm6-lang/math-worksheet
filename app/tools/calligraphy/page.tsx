'use client';

import { useState, useRef } from 'react';

type GridType = 'tian' | 'mi' | 'fang' | 'hengxian';

const GRID_TYPES = [
  { id: 'tian' as GridType, name: '田字格', icon: '田', desc: '十字辅助线，适合初学' },
  { id: 'mi' as GridType, name: '米字格', icon: '米', desc: '八向辅助线，精准定位' },
  { id: 'fang' as GridType, name: '方格', icon: '□', desc: '简洁方格，自由书写' },
  { id: 'hengxian' as GridType, name: '横线格', icon: '☰', desc: '横线格，练习句子' },
];

const CELL_SIZE_OPTIONS = [
  { value: 56, label: '大格', desc: '3字/行' },
  { value: 44, label: '中格', desc: '4字/行' },
  { value: 34, label: '小格', desc: '6字/行' },
];

// SVG grid lines for each cell
function CellSvg({ gridType, size }: { gridType: GridType; size: number }) {
  if (gridType === 'fang') return null;
  return (
    <svg className="absolute inset-0 pointer-events-none" width={size} height={size} style={{ zIndex: 1 }}>
      {gridType === 'tian' && (
        <>
          <line x1={size / 2} y1={2} x2={size / 2} y2={size - 2} stroke="#ddd" strokeWidth="0.8" strokeDasharray="4,3" />
          <line x1={2} y1={size / 2} x2={size - 2} y2={size / 2} stroke="#ddd" strokeWidth="0.8" strokeDasharray="4,3" />
        </>
      )}
      {gridType === 'mi' && (
        <>
          <line x1={size / 2} y1={2} x2={size / 2} y2={size - 2} stroke="#ddd" strokeWidth="0.8" strokeDasharray="4,3" />
          <line x1={2} y1={size / 2} x2={size - 2} y2={size / 2} stroke="#ddd" strokeWidth="0.8" strokeDasharray="4,3" />
          <line x1={2} y1={2} x2={size - 2} y2={size - 2} stroke="#ddd" strokeWidth="0.8" strokeDasharray="4,3" />
          <line x1={size - 2} y1={2} x2={2} y2={size - 2} stroke="#ddd" strokeWidth="0.8" strokeDasharray="4,3" />
        </>
      )}
    </svg>
  );
}

// One cell in the grid
function GridCell({ char, showChar, fontFamily, gridType, size }: {
  char?: string;
  showChar: boolean;
  fontFamily: string;
  gridType: GridType;
  size: number;
}) {
  const fontSize = Math.floor(size * 0.72);
  return (
    <div
      className="relative bg-white border border-gray-300 flex items-center justify-center overflow-hidden"
      style={{ width: size, height: size, flexShrink: 0 }}
    >
      <CellSvg gridType={gridType} size={size} />
      {showChar && char && (
        <span
          className="absolute inset-0 flex items-center justify-center select-none"
          style={{
            fontSize,
            fontFamily,
            color: '#c8c8c8',
            zIndex: 2,
          }}
        >
          {char}
        </span>
      )}
    </div>
  );
}

export default function CalligraphyPage() {
  const [text, setText] = useState('天地人和春夏秋冬');
  const [gridType, setGridType] = useState<GridType>('tian');
  const [rows, setRows] = useState(8);
  const [cellSize, setCellSize] = useState(44);
  const [showGuide, setShowGuide] = useState(true);
  const [fontFamily, setFontFamily] = useState('KaiTi, STKaiti, 楷体, serif');
  const [isExporting, setIsExporting] = useState(false);
  const previewRef = useRef<HTMLDivElement>(null);

  const chars = [...text].filter(c => c.trim());
  // How many chars fit per row on the A4 preview (180mm / cellSize px)
  const previewWidth = 680; // px for the preview area (210mm * 3.24px/mm ≈ 680px)
  const colsPerRow = Math.max(1, Math.floor(previewWidth / cellSize));

  const handleExportPDF = async () => {
    if (!previewRef.current) return;
    setIsExporting(true);
    try {
      const { default: html2canvas } = await import('html2canvas');
      const { default: jsPDF } = await import('jspdf');
      const canvas = await html2canvas(previewRef.current, {
        scale: 2,
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false,
      });
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
      const pw = pdf.internal.pageSize.getWidth();
      const ph = pdf.internal.pageSize.getHeight();
      pdf.addImage(imgData, 'PNG', 0, 0, pw, ph);
      pdf.save('字帖.pdf');
    } catch (e) {
      console.error(e);
      alert('导出失败，请重试');
    } finally {
      setIsExporting(false);
    }
  };

  // Render grid for tian/mi/fang
  const renderGrid = () => {
    const allChars = chars.slice(0, colsPerRow);
    const pageRows = rows;

    // Build grid rows: row 0 = guide chars, rows 1..pageRows-1 = empty
    return (
      <div
        className="inline-block"
        style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${allChars.length}, ${cellSize}px)`,
          gridTemplateRows: `repeat(${pageRows}, ${cellSize}px)`,
          gap: 0,
          border: '2px solid #999',
        }}
      >
        {Array.from({ length: pageRows }, (_, rowIdx) =>
          allChars.map((char, colIdx) => (
            <GridCell
              key={`${rowIdx}-${colIdx}`}
              char={char}
              showChar={showGuide && rowIdx === 0}
              fontFamily={fontFamily}
              gridType={gridType}
              size={cellSize}
            />
          ))
        )}
      </div>
    );
  };

  // Render horizontal lines for hengxian
  const renderLines = () => {
    const lineHeight = cellSize;
    const usableWidth = cellSize * Math.min(chars.length, 12);
    const lineCount = rows;

    return (
      <div className="inline-block border-2 border-gray-400" style={{ width: usableWidth }}>
        {Array.from({ length: lineCount }, (_, i) => (
          <div
            key={i}
            className="relative border-b border-gray-300 flex items-end"
            style={{ height: lineHeight, paddingLeft: 8, paddingRight: 8, paddingBottom: 4 }}
          >
            {showGuide && i === 0 && chars.map((c, j) => (
              <span
                key={j}
                className="select-none mr-4"
                style={{ fontSize: Math.floor(lineHeight * 0.6), fontFamily, color: '#d0d0d0' }}
              >
                {c}
              </span>
            ))}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      {/* Nav */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0f0f0f]/90 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <a href="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
            <div className="w-9 h-9 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center text-lg">🧮</div>
            <span className="text-lg font-bold text-white">算个题吧</span>
          </a>
          <div className="flex items-center gap-6">
            <a href="/tools/sudoku" className="text-sm text-gray-400 hover:text-white transition-colors">数独游戏</a>
            <a href="/" className="text-sm text-gray-400 hover:text-white transition-colors">数学练习卷</a>
          </div>
        </div>
      </nav>

      <div className="pt-24 pb-16 px-4">
        <div className="max-w-4xl mx-auto">
          {/* Hero */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent mb-3">
              字帖生成器
            </h1>
            <p className="text-gray-400">输入文字，一键生成田字格/米字格练习纸 · PDF 即印即用</p>
          </div>

          {/* Controls */}
          <div className="bg-[#111] rounded-2xl border border-white/10 p-6 mb-8 space-y-6">

            {/* Grid type */}
            <div>
              <p className="text-sm text-gray-400 mb-3">模板类型</p>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {GRID_TYPES.map(g => (
                  <button
                    key={g.id}
                    onClick={() => setGridType(g.id)}
                    className={`relative p-4 rounded-xl border transition-all duration-200 text-center ${
                      gridType === g.id
                        ? 'bg-blue-500/20 border-blue-500/60 text-white'
                        : 'bg-white/5 border-white/10 text-gray-300 hover:border-white/30'
                    }`}
                  >
                    <div className="text-3xl mb-1">{g.icon}</div>
                    <div className="text-sm font-medium">{g.name}</div>
                    <div className="text-xs text-gray-500 mt-0.5">{g.desc}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Text input + settings */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">输入文字</label>
                <input
                  type="text"
                  value={text}
                  onChange={e => setText(e.target.value)}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-blue-500/60 transition-colors"
                  placeholder="输入要练习的汉字，如：天地人和"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-2">字体</label>
                <select
                  value={fontFamily}
                  onChange={e => setFontFamily(e.target.value)}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500/60 transition-colors"
                >
                  <option value="KaiTi, STKaiti, 楷体, serif">楷体（推荐）</option>
                  <option value="STSong, SimSun, 宋体, serif">宋体</option>
                  <option value="STHeiti, SimHei, 黑体, sans-serif">黑体</option>
                  <option value="STLiti, STFangsong, 仿宋, serif">仿宋</option>
                </select>
              </div>
            </div>

            {/* Size + rows */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">格子大小</label>
                <div className="grid grid-cols-3 gap-2">
                  {CELL_SIZE_OPTIONS.map(opt => (
                    <button
                      key={opt.value}
                      onClick={() => setCellSize(opt.value)}
                      className={`py-2 px-1 rounded-lg border text-xs transition-all ${
                        cellSize === opt.value
                          ? 'bg-blue-500/20 border-blue-500/60 text-white'
                          : 'bg-white/5 border-white/10 text-gray-400 hover:border-white/30'
                      }`}
                    >
                      <div className="font-medium">{opt.label}</div>
                      <div className="text-[10px] text-gray-600">{opt.desc}</div>
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-2">练习行数（每字）</label>
                <div className="flex items-center gap-2">
                  <input
                    type="range"
                    min={3}
                    max={15}
                    value={rows}
                    onChange={e => setRows(Number(e.target.value))}
                    className="flex-1 accent-blue-500"
                  />
                  <span className="text-white text-sm w-6 text-center">{rows}</span>
                </div>
              </div>
              <div className="flex items-end">
                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={showGuide}
                    onChange={e => setShowGuide(e.target.checked)}
                    className="w-4 h-4 accent-blue-500"
                  />
                  <span className="text-sm text-gray-300">显示首行范字</span>
                </label>
              </div>
            </div>
          </div>

          {/* Preview */}
          <div className="flex justify-center mb-6">
            <div className="text-xs text-gray-500 mb-2 text-center">
              预计 {chars.length} 字 · {gridType === 'hengxian' ? '横线格' : `格子 ${cellSize}px`}
            </div>
          </div>

          <div className="flex justify-center mb-6 overflow-x-auto">
            <div
              ref={previewRef}
              className="bg-white shadow-2xl mx-auto"
              style={{
                width: 680,
                minHeight: 900,
                padding: 40,
                background: '#fff',
              }}
            >
              {gridType === 'hengxian' ? renderLines() : renderGrid()}
            </div>
          </div>

          {/* Export */}
          <div className="flex justify-center gap-4">
            <button
              onClick={handleExportPDF}
              disabled={isExporting}
              className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed px-8 py-3 rounded-xl text-white font-medium transition-colors flex items-center gap-2"
            >
              {isExporting ? '导出中...' : '📄 下载 PDF'}
            </button>
            <button
              onClick={() => window.print()}
              className="bg-white/10 hover:bg-white/20 px-8 py-3 rounded-xl text-white font-medium transition-colors"
            >
              🖨️ 直接打印
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
