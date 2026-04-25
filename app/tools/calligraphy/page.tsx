'use client';

import { useState, useRef } from 'react';
import ToolGuide from '@/components/ToolGuide';
import { toolGuides } from '@/lib/toolGuides';

type GridType = 'tian' | 'mi' | 'fang' | 'hengxian';

const GRID_TYPES = [
  { id: 'tian' as GridType, name: '田字格', icon: '田', desc: '十字辅助线' },
  { id: 'mi' as GridType, name: '米字格', icon: '米', desc: '八向辅助线' },
  { id: 'fang' as GridType, name: '方格', icon: '□', desc: '简洁方格' },
  { id: 'hengxian' as GridType, name: '横线格', icon: '☰', desc: '句子练习' },
];

// 更多字体选择
const FONT_OPTIONS = [
  { value: 'KaiTi, STKaiti, 楷体', name: '楷体', preview: '标准楷书' },
  { value: 'STXingkai, 华文行楷', name: '行楷', preview: '流畅行书' },
  { value: 'STSong, SimSun, 宋体', name: '宋体', preview: '印刷体' },
  { value: 'STHeiti, SimHei, 黑体', name: '黑体', preview: '粗壮醒目' },
  { value: 'STFangsong, 仿宋', name: '仿宋', preview: '秀逸典雅' },
  { value: 'STLiti, LiSu, 隶书', name: '隶书', preview: '古朴宽博' },
  { value: 'YouYuan, 幼圆', name: '幼圆', preview: '圆润可爱' },
  { value: 'STCaiyun, 华文彩云', name: '彩云', preview: '空心艺术' },
  { value: 'FZShuTi, 方正舒体', name: '舒体', preview: '洒脱飘逸' },
  { value: 'FZYaoti, 方正姚体', name: '姚体', preview: '纤细挺拔' },
  { value: 'STXinwei, 华文新魏', name: '新魏', preview: '雄强刚健' },
  { value: 'STHupo, 华文琥珀', name: '琥珀', preview: '圆润厚重' },
];

const CELL_SIZE_OPTIONS = [
  { value: 56, label: '大格', desc: '3字/行' },
  { value: 48, label: '中大', desc: '4字/行' },
  { value: 40, label: '中格', desc: '5字/行' },
  { value: 32, label: '小格', desc: '6字/行' },
];

// Grid guide lines for each cell (using divs instead of SVG for better html2canvas compatibility)
function CellGuides({ gridType, size }: { gridType: GridType; size: number }) {
  if (gridType === 'fang') return null;
  // Diagonal line length for mi grid: sqrt(2) * size
  const diagLen = Math.ceil(size * 1.414);
  const diagOffset = Math.ceil((diagLen - size) / 2);
  return (
    <div className="absolute inset-0 pointer-events-none" style={{ zIndex: 1 }}>
      {/* Vertical center line */}
      <div style={{ position: 'absolute', width: 0, top: 2, bottom: 2, left: '50%', borderRight: '1px dashed #999' }} />
      {/* Horizontal center line */}
      <div style={{ position: 'absolute', height: 0, left: 2, right: 2, top: '50%', borderBottom: '1px dashed #999' }} />
      {/* Diagonal lines for mi grid */}
      {gridType === 'mi' && (
        <>
          <div style={{
            position: 'absolute', width: diagLen, height: 0, top: '50%', left: '50%',
            transform: 'translate(-50%, -50%) rotate(45deg)',
            borderBottom: '1px dashed #999',
          }} />
          <div style={{
            position: 'absolute', width: diagLen, height: 0, top: '50%', left: '50%',
            transform: 'translate(-50%, -50%) rotate(-45deg)',
            borderBottom: '1px dashed #999',
          }} />
        </>
      )}
    </div>
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
      className="relative flex items-center justify-center overflow-hidden"
      style={{
        width: size,
        height: size,
        flexShrink: 0,
        background: '#fff',
        borderBottom: '1px solid #ccc',
        borderRight: '1px solid #ccc',
      }}
    >
      <CellGuides gridType={gridType} size={size} />
      {showChar && char && (
        <span
          className="absolute select-none"
          style={{
            fontSize,
            fontFamily,
            color: '#d0d0d0',
            zIndex: 2,
            // 字体底部接近格子底部，约 85% 位置
            bottom: size * 0.08,
            left: '50%',
            transform: 'translateX(-50%)',
            lineHeight: 1,
            whiteSpace: 'nowrap',
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
  const [cellSize, setCellSize] = useState(48);
  const [showGuide, setShowGuide] = useState(true);
  const [fontFamily, setFontFamily] = useState('KaiTi, STKaiti, 楷体');
  const [isExporting, setIsExporting] = useState(false);
  const previewRef = useRef<HTMLDivElement>(null);

  const chars = [...text].filter(c => c.trim());
  const previewWidth = 650;
  const colsPerRow = Math.max(1, Math.floor(previewWidth / cellSize));

  const handleExportPDF = async () => {
    if (!previewRef.current) return;
    setIsExporting(true);
    try {
      const { default: html2canvas } = await import('html2canvas');
      const { default: jsPDF } = await import('jspdf');
      
      // Force white background on the preview element before capture
      const el = previewRef.current;
      const origBg = el.style.background;
      el.style.background = '#ffffff';
      
      const canvas = await html2canvas(el, {
        scale: 2,
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false,
      });
      
      // Restore original background
      el.style.background = origBg;
      
      // Create white canvas to ensure no transparency issues
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

      // 添加网站水印（顶部 + 底部）
      const { drawWatermarkOnCanvas, drawHeaderWatermark } = await import('@/lib/pdfWatermark');
      const wCtx = (whiteCanvas.getContext('2d') ? whiteCanvas : canvas).getContext('2d');
      if (wCtx) {
        const target = (whiteCanvas.getContext('2d') ? whiteCanvas : canvas);
        drawHeaderWatermark(wCtx, target.width);
        drawWatermarkOnCanvas(wCtx, target.width, target.height);
      }
      const finalImgData = (whiteCanvas.getContext('2d') ? whiteCanvas : canvas).toDataURL('image/png');

      pdf.addImage(finalImgData, 'PNG', 0, 0, pw, ph);
      pdf.save('字帖.pdf');
    } catch (e) {
      console.error(e);
      alert('导出失败，请重试');
    } finally {
      setIsExporting(false);
    }
  };

  const handlePrint = () => {
    const printWindow = window.open('', '_blank');
    if (!printWindow) return;
    const chars = [...text].filter(c => c.trim());
    const fontSize = Math.floor(cellSize * 0.72);
    const gridHtml = gridType === 'hengxian' ? `
      <div style="width:180mm;margin:10mm auto;">
        ${Array.from({ length: rows }, (_, i) => `
          <div style="height:${cellSize}px;border-bottom:1px solid #ccc;display:flex;align-items:flex-end;padding:0 4px 4px;">
            ${showGuide && i === 0 ? chars.map(c => `<span style="font-size:${fontSize}px;font-family:'${fontFamily}';color:#b0b0b0;margin-right:8px;">${c}</span>`).join('') : ''}
          </div>
        `).join('')}
      </div>
    ` : `
      <div style="width:180mm;margin:10mm auto;display:grid;grid-template-columns:repeat(${Math.min(chars.length, colsPerRow)},${cellSize}px);border:2px solid #333;">
        ${Array.from({ length: rows }, (_, rowIdx) =>
          chars.slice(0, colsPerRow).map(char => `
            <div style="width:${cellSize}px;height:${cellSize}px;border-bottom:1px solid #ccc;border-right:1px solid #ccc;position:relative;background:#fff;">
              ${gridType === 'tian' ? `<div style="position:absolute;width:0;top:2px;bottom:2px;left:50%;border-right:1px dashed #999;"></div><div style="position:absolute;height:0;left:2px;right:2px;top:50%;border-bottom:1px dashed #999;"></div>` : ''}
              ${gridType === 'mi' ? `<div style="position:absolute;width:0;top:2px;bottom:2px;left:50%;border-right:1px dashed #999;"></div><div style="position:absolute;height:0;left:2px;right:2px;top:50%;border-bottom:1px dashed #999;"></div><div style="position:absolute;width:${Math.ceil(cellSize*1.414)}px;height:0;top:50%;left:50%;transform:translate(-50%,-50%) rotate(45deg);border-bottom:1px dashed #999;"></div><div style="position:absolute;width:${Math.ceil(cellSize*1.414)}px;height:0;top:50%;left:50%;transform:translate(-50%,-50%) rotate(-45deg);border-bottom:1px dashed #999;"></div>` : ''}
              ${showGuide && rowIdx === 0 ? `<span style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:${fontSize}px;font-family:'${fontFamily}';color:#b0b0b0;">${char}</span>` : ''}
            </div>
          `).join('')
        ).join('')}
      </div>
    `;
    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <title>字帖打印</title>
        <style>
          @page { margin: 10mm; size: A4 portrait; }
          body { margin: 0; font-family: 'KaiTi', '楷体', serif; }
          @media print { body { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }
        </style>
      </head>
      <body>${gridHtml}</body>
      </html>
    `);
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    printWindow.close();
  };

  // Render grid
  const renderGrid = () => {
    const allChars = chars.slice(0, colsPerRow);
    return (
      <div
        className="inline-block"
        style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${allChars.length}, ${cellSize}px)`,
          gridTemplateRows: `repeat(${rows}, ${cellSize}px)`,
          border: '2px solid #333',
          background: '#fff',
        }}
      >
        {Array.from({ length: rows }, (_, rowIdx) =>
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

  const renderLines = () => {
    const lineHeight = cellSize;
    const usableWidth = cellSize * Math.min(chars.length, 12);
    return (
      <div className="inline-block" style={{ width: usableWidth, border: '2px solid #333', background: '#fff' }}>
        {Array.from({ length: rows }, (_, i) => (
          <div
            key={i}
            className="relative border-b flex items-end"
            style={{
              height: lineHeight,
              paddingLeft: 8,
              paddingRight: 8,
              paddingBottom: 4,
              borderColor: '#ccc',
            }}
          >
            {showGuide && i === 0 && chars.map((c, j) => (
              <span
                key={j}
                className="select-none"
                style={{
                  fontSize: Math.floor(lineHeight * 0.6),
                  fontFamily,
                  color: '#b0b0b0',
                  marginRight: 8,
                }}
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
    <div className="min-h-screen bg-gray-100">
      {/* Nav */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
          <a href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center text-base">🧮</div>
            <span className="text-base font-bold text-gray-800">字帖生成器</span>
          </a>
          <div className="flex items-center gap-5">
            <a href="/tools/sudoku" className="text-sm text-gray-600 hover:text-blue-600 transition-colors">数独游戏</a>
            <a href="/" className="text-sm text-gray-600 hover:text-blue-600 transition-colors">数学练习卷</a>
          </div>
        </div>
      </nav>

      <div className="pt-20 pb-12 px-4">
        <div className="max-w-5xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">免费字帖生成器</h1>
            <p className="text-gray-500 text-sm">田字格/米字格/楷书行楷 · PDF下载打印</p>
          </div>

          {/* Controls Card */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 mb-8">
            <div className="space-y-6">
              {/* Grid type */}
              <div>
                <p className="text-sm text-gray-500 mb-3 font-medium">模板类型</p>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {GRID_TYPES.map(g => (
                    <button
                      key={g.id}
                      onClick={() => setGridType(g.id)}
                      className={`relative p-3 rounded-xl border-2 transition-all duration-200 text-center ${
                        gridType === g.id
                          ? 'bg-blue-50 border-blue-500 text-blue-700'
                          : 'bg-gray-50 border-gray-200 text-gray-600 hover:border-gray-300 hover:bg-gray-100'
                      }`}
                    >
                      <div className="text-2xl mb-0.5">{g.icon}</div>
                      <div className="text-xs font-medium">{g.name}</div>
                      <div className="text-[10px] text-gray-400">{g.desc}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Text input */}
              <div>
                <label className="block text-sm text-gray-500 mb-2 font-medium">输入练习文字</label>
                <input
                  type="text"
                  value={text}
                  onChange={e => setText(e.target.value)}
                  className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-800 placeholder-gray-400 focus:outline-none focus:border-blue-400 focus:bg-white transition-colors"
                  placeholder="输入要练习的汉字"
                />
                <p className="text-xs text-gray-400 mt-1">已输入 {chars.length} 个字</p>
              </div>

              {/* Font selector - 两列显示更多字体 */}
              <div>
                <label className="block text-sm text-gray-500 mb-2 font-medium">选择字体</label>
                <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2">
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
                <p className="text-xs text-gray-400 mt-1.5">提示：不同系统可用字体不同，楷体/宋体/黑体最通用</p>
              </div>

              {/* Size + rows */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm text-gray-500 mb-2 font-medium">格子大小</label>
                  <div className="grid grid-cols-4 gap-1.5">
                    {CELL_SIZE_OPTIONS.map(opt => (
                      <button
                        key={opt.value}
                        onClick={() => setCellSize(opt.value)}
                        className={`py-2 px-1 rounded-lg border-2 text-xs transition-all ${
                          cellSize === opt.value
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
                      max={15}
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
              A4 预览 · {chars.length} 字 · {gridType === 'hengxian' ? '横线格' : `每行最多 ${colsPerRow} 格`}
            </div>
            <div className="flex justify-center overflow-x-auto bg-gray-50 rounded-xl p-4">
              <div
                ref={previewRef}
                className="bg-white shadow-lg"
                style={{
                  width: previewWidth,
                  minHeight: 850,
                  padding: 30,
                  background: '#fff',
                }}
              >
                {gridType === 'hengxian' ? renderLines() : renderGrid()}
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

      {/* ===== 内容三件套 ===== */}
      <div className="print:hidden max-w-4xl mx-auto px-4 pb-8 space-y-8">

        {/* 使用指南 */}
        <section className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 md:p-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <span>📖</span> 使用指南
          </h2>
          <div className="text-gray-600 leading-relaxed space-y-3 text-sm md:text-base">
            <p>
              字帖生成器支持楷书、行楷、隶书等12种字体风格，适合幼儿园到成人各个阶段的书写练习。在输入框中输入想要练习的汉字、词语或句子，选择字体、字号和格子样式后，系统会自动生成规范的字帖模板。提供田字格、米字格、回宫格、方格四种格子样式。田字格适合低年级基础笔画练习，米字格适合结构定位训练，回宫格适合间架结构精细调整。生成的字帖支持PDF格式下载，A4纸打印效果清晰，每个字都有规范的笔画顺序参考。
            </p>
          </div>
        </section>

        {/* 适用场景 */}
        <section className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 md:p-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <span>🎯</span> 适用场景
          </h2>
          <ul className="space-y-3 text-gray-600 text-sm md:text-base">
            <li className="flex items-start gap-2">
              <span className="text-blue-500 mt-0.5 shrink-0">●</span>
              <span><strong className="text-gray-800">幼儿控笔训练：</strong>打印大号田字格，练习基本笔画和简单汉字</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-500 mt-0.5 shrink-0">●</span>
              <span><strong className="text-gray-800">小学生日常练字：</strong>每天15分钟，从楷书基础笔画过渡到常用字</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-500 mt-0.5 shrink-0">●</span>
              <span><strong className="text-gray-800">成人书法入门：</strong>选择行楷字体，练习连笔和行书结构</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-500 mt-0.5 shrink-0">●</span>
              <span><strong className="text-gray-800">教师布置作业：</strong>批量生成全班统一的练字作业</span>
            </li>
          </ul>
        </section>

        {/* 常见问题FAQ */}
        <section className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 md:p-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <span>❓</span> 常见问题
          </h2>
          <div className="space-y-2">
            <details className="group border border-gray-200 rounded-lg">
              <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-700 hover:text-gray-900 list-none font-medium">
                <span>支持哪些字体？</span>
                <span className="text-gray-400 group-open:rotate-180 transition-transform text-xs">▼</span>
              </summary>
              <div className="px-4 pb-4 text-sm text-gray-500 leading-relaxed">目前支持楷书、行楷、隶书等12种字体。小学生建议从楷书开始练习，打好基础后再尝试行楷。</div>
            </details>
            <details className="group border border-gray-200 rounded-lg">
              <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-700 hover:text-gray-900 list-none font-medium">
                <span>格子样式怎么选？</span>
                <span className="text-gray-400 group-open:rotate-180 transition-transform text-xs">▼</span>
              </summary>
              <div className="px-4 pb-4 text-sm text-gray-500 leading-relaxed">一年级建议用田字格，帮助定位笔画起止点；二年级以上可以用米字格，更精细地控制汉字结构；三年级以上可以尝试方格或空白格，培养独立书写能力。</div>
            </details>
            <details className="group border border-gray-200 rounded-lg">
              <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-700 hover:text-gray-900 list-none font-medium">
                <span>可以自定义练字内容吗？</span>
                <span className="text-gray-400 group-open:rotate-180 transition-transform text-xs">▼</span>
              </summary>
              <div className="px-4 pb-4 text-sm text-gray-500 leading-relaxed">可以。输入任意汉字、词语、古诗或句子都可以生成对应的字帖。建议配合学校语文课本的生字表来练习。</div>
            </details>
          </div>
        </section>

        {/* 相关工具推荐 */}
        <section className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 md:p-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <span>🔗</span> 相关工具推荐
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <a href="/tools/pinyin" className="block bg-gray-50 hover:bg-blue-50 border border-gray-200 hover:border-blue-300 rounded-xl p-4 transition-all group">
              <div className="text-2xl mb-2">📚</div>
              <div className="font-bold text-gray-700 text-sm group-hover:text-blue-600 transition-colors">拼音学习工具</div>
              <div className="text-xs text-gray-400 mt-1">声母韵母练习</div>
            </a>
            <a href="/tools/flashcards" className="block bg-gray-50 hover:bg-blue-50 border border-gray-200 hover:border-blue-300 rounded-xl p-4 transition-all group">
              <div className="text-2xl mb-2">🃏</div>
              <div className="font-bold text-gray-700 text-sm group-hover:text-blue-600 transition-colors">识字卡片生成器</div>
              <div className="text-xs text-gray-400 mt-1">自定义汉字卡片</div>
            </a>
            <a href="/resources/calligraphy" className="block bg-gray-50 hover:bg-blue-50 border border-gray-200 hover:border-blue-300 rounded-xl p-4 transition-all group">
              <div className="text-2xl mb-2">✍️</div>
              <div className="font-bold text-gray-700 text-sm group-hover:text-blue-600 transition-colors">小学生硬笔书法课程</div>
              <div className="text-xs text-gray-400 mt-1">系统书法教学</div>
            </a>
          </div>
        </section>
      </div>

      {/* 使用指南 */}
      <div className="max-w-4xl mx-auto px-4 py-12">
        <ToolGuide {...toolGuides['calligraphy']} />
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
