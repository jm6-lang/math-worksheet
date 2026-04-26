'use client';

import { useState, useRef, useMemo } from 'react';
import ToolNavBar from '@/components/ToolNavBar';
import { poems, gradeGroups, type Poem } from '@/lib/poemData';

/* ============================================================
   类型定义
   ============================================================ */

type MemoMode = 'fill' | 'full' | 'updown';
type GridTemplate = 'tian' | 'fang' | 'hengxian';

interface MemoModeOption {
  id: MemoMode;
  name: string;
  desc: string;
  icon: string;
}

interface GridOption {
  id: GridTemplate;
  name: string;
  icon: string;
  desc: string;
}

/* ============================================================
   常量配置
   ============================================================ */

const MEMO_MODES: MemoModeOption[] = [
  { id: 'fill', name: '填空默写', desc: '随机隐藏部分字词', icon: '田' },
  { id: 'full', name: '全诗默写', desc: '只显示诗名和作者', icon: '白' },
  { id: 'updown', name: '上下句默写', desc: '显示上句，下句留空', icon: '对' },
];

const GRID_OPTIONS: GridOption[] = [
  { id: 'tian', name: '田字格', icon: '田', desc: '十字辅助线' },
  { id: 'fang', name: '方格', icon: '□', desc: '简洁方格' },
  { id: 'hengxian', name: '横线格', icon: '☰', desc: '横线书写' },
];

const CELL_SIZE = 48;
const FILL_RATIO = 0.4; // 填空模式下隐藏字词的比例

/* ============================================================
   工具函数
   ============================================================ */

/** 简单伪随机种子函数，确保每次渲染相同 */
function seededRandom(seed: number): () => number {
  let s = seed;
  return () => {
    s = (s * 16807 + 0) % 2147483647;
    return (s - 1) / 2147483646;
  };
}

/** 对一首诗生成填空默写数据 */
function generateFillBlanks(poem: Poem, seed: number) {
  const rng = seededRandom(seed);
  return poem.content.map(line => {
    const chars = [...line];
    return chars.map(ch => {
      if (ch.trim() === '' || ch === '，' || ch === '。' || ch === '？' || ch === '！' || ch === '、' || ch === '；' || ch === '：') {
        return { char: ch, hidden: false };
      }
      return { char: ch, hidden: rng() < FILL_RATIO };
    });
  });
}

/** 生成上下句默写数据（奇数行显示，偶数行隐藏） */
function generateUpDownLines(poem: Poem) {
  return poem.content.map((line, idx) => ({
    line,
    hidden: idx % 2 === 1,
  }));
}

/* ============================================================
   田字格辅助线组件
   ============================================================ */

function TianGuide({ size }: { size: number }) {
  return (
    <div className="absolute inset-0 pointer-events-none" style={{ zIndex: 1 }}>
      <div style={{ position: 'absolute', width: 0, top: 2, bottom: 2, left: '50%', borderRight: '1px dashed #e74c3c' }} />
      <div style={{ position: 'absolute', height: 0, left: 2, right: 2, top: '50%', borderBottom: '1px dashed #e74c3c' }} />
    </div>
  );
}

/* ============================================================
   默写格子单元
   ============================================================ */

function MemoCell({
  char,
  hidden,
  gridTemplate,
  size,
}: {
  char: string;
  hidden: boolean;
  gridTemplate: GridTemplate;
  size: number;
}) {
  const fontSize = Math.floor(size * 0.72);

  if (gridTemplate === 'hengxian') {
    // 横线格：每个字占一个固定宽度
    return (
      <span
        style={{
          display: 'inline-block',
          width: size,
          height: size,
          lineHeight: `${size}px`,
          textAlign: 'center',
          fontSize,
          fontFamily: "'KaiTi', 'STKaiti', '楷体', serif",
          borderBottom: '1px solid #ccc',
          color: hidden ? 'transparent' : '#333',
        }}
      >
        {hidden ? '\u00A0' : char}
      </span>
    );
  }

  // 田字格 / 方格
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
      {gridTemplate === 'tian' && <TianGuide size={size} />}
      {hidden ? (
        <span style={{ color: 'transparent' }}>{char}</span>
      ) : (
        <span
          className="absolute select-none"
          style={{
            fontSize,
            fontFamily: "'KaiTi', 'STKaiti', '楷体', serif",
            color: '#333',
            zIndex: 2,
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

/* ============================================================
   主页面组件
   ============================================================ */

export default function PoemMemoPage() {
  /* ---- 状态 ---- */
  const [selectedGrade, setSelectedGrade] = useState<number | null>(null); // null = 全部
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedPoemIds, setSelectedPoemIds] = useState<Set<string>>(new Set());
  const [memoMode, setMemoMode] = useState<MemoMode>('fill');
  const [gridTemplate, setGridTemplate] = useState<GridTemplate>('tian');
  const [isExporting, setIsExporting] = useState(false);
  const previewRef = useRef<HTMLDivElement>(null);

  /* ---- 过滤诗词列表 ---- */
  const filteredPoems = useMemo(() => {
    let list = poems;
    if (selectedGrade !== null) {
      const group = gradeGroups.find(g => g.grades.includes(selectedGrade));
      if (group) {
        list = list.filter(p => group.grades.includes(p.grade));
      }
    }
    if (searchQuery.trim()) {
      const q = searchQuery.trim().toLowerCase();
      list = list.filter(
        p =>
          p.title.toLowerCase().includes(q) ||
          p.author.toLowerCase().includes(q) ||
          p.content.some(line => line.toLowerCase().includes(q))
      );
    }
    return list;
  }, [selectedGrade, searchQuery]);

  /* ---- 选中的诗词对象 ---- */
  const selectedPoems = useMemo(
    () => poems.filter(p => selectedPoemIds.has(p.id)),
    [selectedPoemIds]
  );

  /* ---- 诗词选择操作 ---- */
  const togglePoem = (id: string) => {
    setSelectedPoemIds(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const selectAllVisible = () => {
    setSelectedPoemIds(prev => {
      const next = new Set(prev);
      filteredPoems.forEach(p => next.add(p.id));
      return next;
    });
  };

  const clearAllVisible = () => {
    setSelectedPoemIds(prev => {
      const next = new Set(prev);
      filteredPoems.forEach(p => next.delete(p.id));
      return next;
    });
  };

  /* ---- 渲染默写内容 ---- */
  const renderMemoContent = () => {
    if (selectedPoems.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center py-20 text-gray-400">
          <div className="text-5xl mb-4">📜</div>
          <p className="text-sm">请从左侧选择古诗词</p>
        </div>
      );
    }

    return selectedPoems.map((poem, poemIdx) => {
      const seed = poemIdx * 1000 + poem.grade * 100;

      if (memoMode === 'fill') {
        // 填空默写
        const lines = generateFillBlanks(poem, seed);
        return (
          <div key={poem.id} className="mb-8">
            {/* 诗名和作者 */}
            <div className="mb-3">
              <span className="text-base font-bold" style={{ fontFamily: "'KaiTi', 'STKaiti', '楷体', serif" }}>
                {poem.title}
              </span>
              <span className="text-sm ml-3 text-gray-600" style={{ fontFamily: "'KaiTi', 'STKaiti', '楷体', serif" }}>
                {poem.dynasty} · {poem.author}
              </span>
            </div>
            {/* 诗句 */}
            {lines.map((line, lineIdx) => (
              <div key={lineIdx} className="mb-1">
                {gridTemplate === 'hengxian' ? (
                  <div
                    style={{
                      borderBottom: '1px solid #e5e5e5',
                      minHeight: CELL_SIZE,
                      display: 'flex',
                      alignItems: 'center',
                      padding: '2px 0',
                    }}
                  >
                    {line.map((item, charIdx) => (
                      <MemoCell
                        key={charIdx}
                        char={item.char}
                        hidden={item.hidden}
                        gridTemplate={gridTemplate}
                        size={CELL_SIZE}
                      />
                    ))}
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexWrap: 'wrap', borderTop: '1px solid #ccc', borderLeft: '1px solid #ccc' }}>
                    {line.map((item, charIdx) => (
                      <MemoCell
                        key={charIdx}
                        char={item.char}
                        hidden={item.hidden}
                        gridTemplate={gridTemplate}
                        size={CELL_SIZE}
                      />
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        );
      }

      if (memoMode === 'updown') {
        // 上下句默写
        const lines = generateUpDownLines(poem);
        return (
          <div key={poem.id} className="mb-8">
            <div className="mb-3">
              <span className="text-base font-bold" style={{ fontFamily: "'KaiTi', 'STKaiti', '楷体', serif" }}>
                {poem.title}
              </span>
              <span className="text-sm ml-3 text-gray-600" style={{ fontFamily: "'KaiTi', 'STKaiti', '楷体', serif" }}>
                {poem.dynasty} · {poem.author}
              </span>
            </div>
            {lines.map((item, lineIdx) => (
              <div key={lineIdx} className="mb-1">
                {item.hidden ? (
                  // 下句留空 - 显示空行让学生填写
                  gridTemplate === 'hengxian' ? (
                    <div
                      style={{
                        borderBottom: '1px dashed #999',
                        minHeight: CELL_SIZE,
                        display: 'flex',
                        alignItems: 'center',
                      }}
                    >
                      {[...item.line].map((_, ci) => (
                        <MemoCell key={ci} char="" hidden={true} gridTemplate={gridTemplate} size={CELL_SIZE} />
                      ))}
                    </div>
                  ) : (
                    <div style={{ display: 'flex', flexWrap: 'wrap', borderTop: '1px solid #ccc', borderLeft: '1px solid #ccc' }}>
                      {[...item.line].map((_, ci) => (
                        <MemoCell key={ci} char="" hidden={true} gridTemplate={gridTemplate} size={CELL_SIZE} />
                      ))}
                    </div>
                  )
                ) : (
                  // 上句显示
                  <div
                    className="text-sm leading-relaxed"
                    style={{
                      fontFamily: "'KaiTi', 'STKaiti', '楷体', serif",
                      color: '#333',
                      minHeight: CELL_SIZE,
                      display: 'flex',
                      alignItems: 'center',
                    }}
                  >
                    {item.line}
                  </div>
                )}
              </div>
            ))}
          </div>
        );
      }

      // 全诗默写
      return (
        <div key={poem.id} className="mb-8">
          <div className="mb-3">
            <span className="text-base font-bold" style={{ fontFamily: "'KaiTi', 'STKaiti', '楷体', serif" }}>
              {poem.title}
            </span>
            <span className="text-sm ml-3 text-gray-600" style={{ fontFamily: "'KaiTi', 'STKaiti', '楷体', serif" }}>
              {poem.dynasty} · {poem.author}
            </span>
          </div>
          {/* 空白书写区域 */}
          {poem.content.map((line, lineIdx) => (
            <div key={lineIdx} className="mb-1">
              {gridTemplate === 'hengxian' ? (
                <div
                  style={{
                    borderBottom: '1px solid #e5e5e5',
                    minHeight: CELL_SIZE,
                    display: 'flex',
                    alignItems: 'center',
                  }}
                >
                  {[...line].map((_, ci) => (
                    <MemoCell key={ci} char="" hidden={true} gridTemplate={gridTemplate} size={CELL_SIZE} />
                  ))}
                </div>
              ) : (
                <div style={{ display: 'flex', flexWrap: 'wrap', borderTop: '1px solid #ccc', borderLeft: '1px solid #ccc' }}>
                  {[...line].map((_, ci) => (
                    <MemoCell key={ci} char="" hidden={true} gridTemplate={gridTemplate} size={CELL_SIZE} />
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      );
    });
  };

  /* ---- PDF 导出 ---- */
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

      // 白底画布
      const whiteCanvas = document.createElement('canvas');
      whiteCanvas.width = canvas.width;
      whiteCanvas.height = canvas.height;
      const ctx = whiteCanvas.getContext('2d');
      if (ctx) {
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, whiteCanvas.width, whiteCanvas.height);
        ctx.drawImage(canvas, 0, 0);
      }

      const target = ctx ? whiteCanvas : canvas;
      const wCtx = target.getContext('2d');
      if (wCtx) {
        const { drawWatermarkOnCanvas, drawHeaderWatermark } = await import('@/lib/pdfWatermark');
        drawHeaderWatermark(wCtx, target.width);
        drawWatermarkOnCanvas(wCtx, target.width, target.height);
      }

      const imgData = target.toDataURL('image/png');
      const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
      const pw = pdf.internal.pageSize.getWidth();
      const ph = pdf.internal.pageSize.getHeight();

      // 如果内容超过一页，分页处理
      const imgWidth = pw;
      const imgHeight = (target.height * pw) / target.width;
      if (imgHeight <= ph) {
        pdf.addImage(imgData, 'PNG', 0, 0, pw, imgHeight);
      } else {
        let yOffset = 0;
        const pageImgHeight = ph;
        const pageCanvasHeight = (ph * target.width) / pw;
        while (yOffset < target.height) {
          const sliceCanvas = document.createElement('canvas');
          sliceCanvas.width = target.width;
          const sliceH = Math.min(pageCanvasHeight, target.height - yOffset);
          sliceCanvas.height = sliceH;
          const sliceCtx = sliceCanvas.getContext('2d');
          if (sliceCtx) {
            sliceCtx.fillStyle = '#ffffff';
            sliceCtx.fillRect(0, 0, sliceCanvas.width, sliceCanvas.height);
            sliceCtx.drawImage(target, 0, yOffset, target.width, sliceH, 0, 0, target.width, sliceH);
          }
          const sliceData = sliceCanvas.toDataURL('image/png');
          const sliceDrawH = (sliceH * pw) / target.width;
          if (yOffset > 0) pdf.addPage();
          pdf.addImage(sliceData, 'PNG', 0, 0, pw, sliceDrawH);
          yOffset += pageCanvasHeight;
        }
      }

      pdf.save('古诗词默写.pdf');
    } catch (e) {
      console.error(e);
      alert('导出失败，请重试');
    } finally {
      setIsExporting(false);
    }
  };

  /* ---- 打印 ---- */
  const handlePrint = () => {
    const printWindow = window.open('', '_blank');
    if (!printWindow || !previewRef.current) return;
    const content = previewRef.current.innerHTML;
    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <title>古诗词默写</title>
        <style>
          @page { margin: 10mm; size: A4 portrait; }
          body { margin: 0; font-family: 'KaiTi', '楷体', serif; }
          @media print { body { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }
        </style>
      </head>
      <body>${content}<p style="text-align:center;color:#999;font-size:12px;margin-top:20px;">来源：教材工具箱 | 免费下载：www.skillxm.cn</p></body>
      </html>
    `);
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    printWindow.close();
  };

  /* ============================================================
     渲染
     ============================================================ */

  return (
    <div className="min-h-screen bg-gray-100">
      {/* ===== 导航栏（深色主题）===== */}
      <ToolNavBar currentPath="/tools/poem-memo" title="古诗词默写" />

      {/* ===== 主内容 ===== */}
      <div className="pt-20 pb-12 px-4">
        <div className="max-w-6xl mx-auto">
          {/* 标题 */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">古诗词默写生成器</h1>
            <p className="text-gray-500 text-sm">
              小学1-6年级必背古诗词 · 填空/全诗/上下句三种默写模式 · PDF导出即印即用
            </p>
          </div>

          {/* ===== 主体两栏布局 ===== */}
          <div className="flex flex-col lg:flex-row gap-6">
            {/* ----- 左侧：诗词选择面板 ----- */}
            <div className="w-full lg:w-80 flex-shrink-0">
              <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 sticky top-20">
                {/* 年级筛选 */}
                <div className="mb-4">
                  <p className="text-sm text-gray-500 mb-2 font-medium">年级筛选</p>
                  <div className="flex flex-wrap gap-2">
                    <button
                      onClick={() => setSelectedGrade(null)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                        selectedGrade === null
                          ? 'bg-amber-500 text-white'
                          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                      }`}
                    >
                      全部
                    </button>
                    {gradeGroups.map(g => (
                      <button
                        key={g.label}
                        onClick={() => setSelectedGrade(g.grades[0])}
                        className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                          selectedGrade !== null && g.grades.includes(selectedGrade)
                            ? 'bg-amber-500 text-white'
                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                        }`}
                      >
                        {g.label}
                      </button>
                    ))}
                  </div>
                </div>

                {/* 搜索框 */}
                <div className="mb-4">
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={e => setSearchQuery(e.target.value)}
                    className="w-full bg-gray-50 border border-gray-200 rounded-xl px-3 py-2 text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:border-amber-400 focus:bg-white transition-colors"
                    placeholder="搜索诗名、作者或诗句..."
                  />
                </div>

                {/* 全选/清空 */}
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs text-gray-400">
                    已选 {selectedPoemIds.size} 首 / 共 {filteredPoems.length} 首
                  </span>
                  <div className="flex gap-2">
                    <button
                      onClick={selectAllVisible}
                      className="text-xs text-amber-600 hover:text-amber-700 font-medium"
                    >
                      全选
                    </button>
                    <button
                      onClick={clearAllVisible}
                      className="text-xs text-gray-400 hover:text-gray-600 font-medium"
                    >
                      清空
                    </button>
                  </div>
                </div>

                {/* 诗词列表 */}
                <div className="max-h-[480px] overflow-y-auto space-y-1 pr-1">
                  {filteredPoems.map(poem => (
                    <label
                      key={poem.id}
                      className={`flex items-start gap-2.5 p-2.5 rounded-lg cursor-pointer transition-all ${
                        selectedPoemIds.has(poem.id)
                          ? 'bg-amber-50 border border-amber-200'
                          : 'bg-gray-50 border border-transparent hover:bg-gray-100'
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={selectedPoemIds.has(poem.id)}
                        onChange={() => togglePoem(poem.id)}
                        className="mt-0.5 w-4 h-4 accent-amber-500 rounded"
                      />
                      <div className="flex-1 min-w-0">
                        <div className="text-sm font-medium text-gray-800 truncate">{poem.title}</div>
                        <div className="text-xs text-gray-400">
                          {poem.dynasty} · {poem.author} · {poem.grade}年级
                        </div>
                      </div>
                    </label>
                  ))}
                  {filteredPoems.length === 0 && (
                    <div className="text-center text-gray-400 text-sm py-8">没有找到匹配的诗词</div>
                  )}
                </div>
              </div>
            </div>

            {/* ----- 右侧：预览和控制 ----- */}
            <div className="flex-1 min-w-0">
              {/* 控制面板 */}
              <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 mb-6">
                <div className="space-y-5">
                  {/* 默写模式 */}
                  <div>
                    <p className="text-sm text-gray-500 mb-2 font-medium">默写模式</p>
                    <div className="grid grid-cols-3 gap-2">
                      {MEMO_MODES.map(m => (
                        <button
                          key={m.id}
                          onClick={() => setMemoMode(m.id)}
                          className={`p-3 rounded-xl border-2 transition-all text-center ${
                            memoMode === m.id
                              ? 'bg-amber-50 border-amber-500 text-amber-700'
                              : 'bg-gray-50 border-gray-200 text-gray-600 hover:border-gray-300 hover:bg-gray-100'
                          }`}
                        >
                          <div className="text-lg mb-0.5">{m.icon}</div>
                          <div className="text-xs font-medium">{m.name}</div>
                          <div className="text-[10px] text-gray-400">{m.desc}</div>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* 模板选择 */}
                  <div>
                    <p className="text-sm text-gray-500 mb-2 font-medium">书写模板</p>
                    <div className="grid grid-cols-3 gap-2">
                      {GRID_OPTIONS.map(g => (
                        <button
                          key={g.id}
                          onClick={() => setGridTemplate(g.id)}
                          className={`p-3 rounded-xl border-2 transition-all text-center ${
                            gridTemplate === g.id
                              ? 'bg-amber-50 border-amber-500 text-amber-700'
                              : 'bg-gray-50 border-gray-200 text-gray-600 hover:border-gray-300 hover:bg-gray-100'
                          }`}
                        >
                          <div className="text-lg mb-0.5">{g.icon}</div>
                          <div className="text-xs font-medium">{g.name}</div>
                          <div className="text-[10px] text-gray-400">{g.desc}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* 预览区域 */}
              <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5 mb-6">
                <div className="text-xs text-gray-400 mb-3 text-center">
                  A4 预览 · {selectedPoems.length} 首诗词 · {MEMO_MODES.find(m => m.id === memoMode)?.name}
                </div>
                <div className="flex justify-center overflow-x-auto bg-gray-50 rounded-xl p-4">
                  <div
                    ref={previewRef}
                    className="bg-white shadow-lg"
                    style={{
                      width: '210mm',
                      minHeight: '297mm',
                      padding: '15mm',
                      background: '#fff',
                      boxSizing: 'border-box',
                    }}
                  >
                    {/* 练习卷标题 */}
                    <div className="text-center mb-6 pb-4 border-b-2 border-gray-800">
                      <h2
                        className="text-xl font-bold"
                        style={{ fontFamily: "'KaiTi', 'STKaiti', '楷体', serif" }}
                      >
                        古诗词默写练习
                      </h2>
                      <div className="flex justify-between mt-2 text-xs text-gray-500">
                        <span>姓名：__________</span>
                        <span>班级：__________</span>
                        <span>日期：__________</span>
                      </div>
                    </div>

                    {/* 默写内容 */}
                    {renderMemoContent()}
                  </div>
                </div>
              </div>

              {/* 操作按钮 */}
              <div className="flex justify-center gap-3">
                <button
                  onClick={handleExportPDF}
                  disabled={isExporting || selectedPoems.length === 0}
                  className="bg-amber-600 hover:bg-amber-700 disabled:bg-gray-300 disabled:cursor-not-allowed px-6 py-2.5 rounded-xl text-white text-sm font-medium transition-colors flex items-center gap-2"
                >
                  {isExporting ? '导出中...' : '📄 下载 PDF'}
                </button>
                <button
                  onClick={handlePrint}
                  disabled={selectedPoems.length === 0}
                  className="bg-gray-100 hover:bg-gray-200 disabled:bg-gray-50 disabled:text-gray-400 px-6 py-2.5 rounded-xl text-gray-700 text-sm font-medium transition-colors"
                >
                  🖨️ 直接打印
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ===== 底部 SEO 内容三件套 ===== */}
      <div className="print:hidden max-w-4xl mx-auto px-4 pb-8 space-y-8">
        {/* 使用指南 */}
        <section className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 md:p-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <span>📖</span> 使用指南
          </h2>
          <div className="text-gray-600 leading-relaxed space-y-3 text-sm md:text-base">
            <p>
              古诗词默写生成器是一款专为小学生设计的古诗词复习工具。内置小学1-6年级必背古诗词75首和80首，
              涵盖唐诗、宋词、汉乐府、北朝民歌等多种体裁。使用方法非常简单：首先在左侧面板选择年级筛选，
              然后勾选需要练习的诗词；接着选择默写模式（填空默写、全诗默写、上下句默写）和书写模板（田字格、方格、横线格）；
              最后点击"下载PDF"或"直接打印"即可获得规范的默写练习卷。
            </p>
            <p>
              填空默写模式会随机隐藏约40%的字词，适合日常复习巩固；全诗默写模式只显示诗名和作者，
              适合阶段性检测；上下句默写模式显示上句、隐藏下句，适合检测对诗句对应关系的掌握程度。
              生成的练习卷包含姓名、班级、日期填写栏，可直接用于课堂测验或家庭作业。
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
              <span className="text-amber-500 mt-0.5 shrink-0">●</span>
              <span>
                <strong className="text-gray-800">课堂默写测验：</strong>
                教师可快速生成标准化默写卷，包含姓名班级栏，打印即用
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-amber-500 mt-0.5 shrink-0">●</span>
              <span>
                <strong className="text-gray-800">课后复习巩固：</strong>
                家长可按年级选择诗词，每天练习几首，循序渐进
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-amber-500 mt-0.5 shrink-0">●</span>
              <span>
                <strong className="text-gray-800">期末备考冲刺：</strong>
                使用全诗默写模式进行全面自测，查漏补缺
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-amber-500 mt-0.5 shrink-0">●</span>
              <span>
                <strong className="text-gray-800">古诗词兴趣培养：</strong>
                通过填空模式降低难度，让孩子在完成中建立信心
              </span>
            </li>
          </ul>
        </section>

        {/* FAQ */}
        <section className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 md:p-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <span>❓</span> 常见问题
          </h2>
          <div className="space-y-2">
            <details className="group border border-gray-200 rounded-lg">
              <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-700 hover:text-gray-900 list-none font-medium">
                <span>包含哪些古诗词？</span>
                <span className="text-gray-400 group-open:rotate-180 transition-transform text-xs">▼</span>
              </summary>
              <div className="px-4 pb-4 text-sm text-gray-500 leading-relaxed">
                本工具覆盖小学1-6年级必背古诗词75首和80首，包括《咏鹅》《静夜思》《春晓》《望庐山瀑布》《登鹳雀楼》
                《题西林壁》《示儿》《石灰吟》等经典篇目。诗词按年级分组，方便按需选择。目前内置60首，
                后续将持续扩充至完整版本。
              </div>
            </details>
            <details className="group border border-gray-200 rounded-lg">
              <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-700 hover:text-gray-900 list-none font-medium">
                <span>三种默写模式有什么区别？</span>
                <span className="text-gray-400 group-open:rotate-180 transition-transform text-xs">▼</span>
              </summary>
              <div className="px-4 pb-4 text-sm text-gray-500 leading-relaxed">
                <strong>填空默写</strong>：随机隐藏约40%的字词（标点符号不隐藏），适合日常复习，降低默写难度。
                <strong>全诗默写</strong>：只显示诗名、朝代和作者，诗句部分全部留空，适合阶段性检测。
                <strong>上下句默写</strong>：显示奇数行（上句），偶数行（下句）留空，适合训练诗句对应关系。
              </div>
            </details>
            <details className="group border border-gray-200 rounded-lg">
              <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-700 hover:text-gray-900 list-none font-medium">
                <span>可以自定义添加诗词吗？</span>
                <span className="text-gray-400 group-open:rotate-180 transition-transform text-xs">▼</span>
              </summary>
              <div className="px-4 pb-4 text-sm text-gray-500 leading-relaxed">
                目前版本支持从内置诗词库中选择。自定义添加功能正在开发中，未来将支持用户输入任意诗词内容来生成默写练习。
                如有需要的诗词，欢迎通过反馈渠道告诉我们。
              </div>
            </details>
            <details className="group border border-gray-200 rounded-lg">
              <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-700 hover:text-gray-900 list-none font-medium">
                <span>PDF打印效果如何？</span>
                <span className="text-gray-400 group-open:rotate-180 transition-transform text-xs">▼</span>
              </summary>
              <div className="px-4 pb-4 text-sm text-gray-500 leading-relaxed">
                导出的PDF为标准A4尺寸，支持田字格、方格、横线格三种模板。田字格带有十字辅助线，
                适合低年级学生规范书写；方格简洁明了，适合中高年级；横线格适合连续书写练习。
                打印时建议选择"实际大小"或100%缩放，确保格子尺寸准确。
              </div>
            </details>
          </div>
        </section>

        {/* 相关工具推荐 */}
        <section className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 md:p-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <span>🔗</span> 相关工具推荐
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
            <a
              href="/tools/calligraphy"
              className="block bg-gray-50 hover:bg-amber-50 border border-gray-200 hover:border-amber-300 rounded-xl p-4 transition-all group"
            >
              <div className="text-2xl mb-2">✍️</div>
              <div className="font-bold text-gray-700 text-sm group-hover:text-amber-600 transition-colors">
                字帖生成器
              </div>
              <div className="text-xs text-gray-400 mt-1">田字格/米字格练字</div>
            </a>
            <a
              href="/tools/math-worksheet"
              className="block bg-gray-50 hover:bg-amber-50 border border-gray-200 hover:border-amber-300 rounded-xl p-4 transition-all group"
            >
              <div className="text-2xl mb-2">🧮</div>
              <div className="font-bold text-gray-700 text-sm group-hover:text-amber-600 transition-colors">
                数学练习卷
              </div>
              <div className="text-xs text-gray-400 mt-1">口算/竖式/应用题</div>
            </a>
            <a
              href="/tools/writing-template"
              className="block bg-gray-50 hover:bg-amber-50 border border-gray-200 hover:border-amber-300 rounded-xl p-4 transition-all group"
            >
              <div className="text-2xl mb-2">📝</div>
              <div className="font-bold text-gray-700 text-sm group-hover:text-amber-600 transition-colors">
                作文模板
              </div>
              <div className="text-xs text-gray-400 mt-1">作文格纸生成</div>
            </a>
            <a
              href="/tools/pinyin"
              className="block bg-gray-50 hover:bg-amber-50 border border-gray-200 hover:border-amber-300 rounded-xl p-4 transition-all group"
            >
              <div className="text-2xl mb-2">📚</div>
              <div className="font-bold text-gray-700 text-sm group-hover:text-amber-600 transition-colors">
                拼音注音
              </div>
              <div className="text-xs text-gray-400 mt-1">汉字拼音标注</div>
            </a>
          </div>
        </section>
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
