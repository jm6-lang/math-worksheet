'use client';

import { useState, useRef } from 'react';
import ToolGuide from '@/components/ToolGuide';
import { toolGuides } from '@/lib/toolGuides';
import ToolNavBar from '@/components/ToolNavBar';

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

      // 添加网站水印（顶部 + 底部）
      const { drawWatermarkOnCanvas, drawHeaderWatermark } = await import('@/lib/pdfWatermark');
      const eCtx = canvas.getContext('2d');
      if (eCtx) {
        drawHeaderWatermark(eCtx, canvas.width);
        drawWatermarkOnCanvas(eCtx, canvas.width, canvas.height);
      }
      const finalImgData = canvas.toDataURL('image/png');

      pdf.addImage(finalImgData, 'PNG', 0, 0, pageWidth, pdfHeight);
      pdf.save('英语字帖.pdf');
    } catch (e) {
      console.error(e);
      alert('导出失败，请重试');
    } finally {
      setIsExporting(false);
    }
  };

  const handlePrint = function() {
    const printWindow = window.open('', '_blank');
    if (!printWindow || !previewRef.current) return;
    const content = previewRef.current.innerHTML;
    printWindow.document.write(`<!DOCTYPE html><html><head><meta charset="utf-8"><title>英语字帖</title><style>@page{margin:10mm;size:A4 portrait;}body{margin:0;font-family:'Comic Sans MS','Arial',sans-serif;color:#000;}@media print{body{-webkit-print-color-adjust:exact;print-color-adjust:exact;}}</style></head><body>${content}<p style="text-align:center;color:#999;font-size:12px;margin-top:20px;">来源：教材工具箱 | 免费下载：www.skillxm.cn</p></body></html>`);
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    printWindow.close();
  };

  return (
    <div className="min-h-screen bg-gray-100" style={{ fontFamily: '"Noto Sans SC", "Microsoft YaHei", sans-serif' }}>

      {/* ===== 顶部导航 ===== */}
      <ToolNavBar currentPath="/tools/english-calligraphy" title="英语字帖" />

      <div className="pt-20 pb-12 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">英文字帖生成器</h1>
            <p className="text-gray-500 text-sm">四线三格 · 多种字体 · PDF下载打印</p>
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

          {/* Preview */}
          <div className="print-preview bg-white rounded-2xl border border-gray-200 shadow-sm p-6 mb-6">
            <div className="text-xs text-gray-400 mb-3 text-center">
              A4 预览 · {words.length} 个词 · 每词 {rowsPerWord} 行
            </div>
            <div className="flex justify-center overflow-x-auto bg-gray-50 rounded-xl p-4">
              <div
                ref={previewRef}
                className="bg-white shadow-lg"
                style={{
                  width: pageWidth,
                  minHeight: 850,
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

      {/* ===== 内容三件套 ===== */}
      <div className="print:hidden max-w-5xl mx-auto px-4 pb-8 space-y-8">

        {/* 使用指南 */}
        <section className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 md:p-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <span>📖</span> 使用指南
          </h2>
          <div className="text-gray-600 leading-relaxed space-y-3 text-sm md:text-base">
            <p>
              英文字帖生成器提供标准的四线三格英文字帖模板，支持手写体、印刷体、圆体等多种英文字体风格。可以自定义练习内容，包括26个英文字母、单词、句子等。四线三格是国际通用的英语书写格式，第一线为顶线，第二线为中线（小写字母的主体高度），第三线为基础线，第四线为下降线（g、p、y等字母的尾部延伸）。选择适合的字体和内容后，一键生成PDF下载打印。建议从26个字母的基本笔画开始练习，掌握每个字母的标准占格位置，再过渡到单词和短句书写。
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
              <span><strong className="text-gray-800">英文启蒙：</strong>学完26个字母后，用字帖巩固书写规范</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-500 mt-0.5 shrink-0">●</span>
              <span><strong className="text-gray-800">小学英语作业：</strong>配合学校英语课的书写要求进行练习</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-500 mt-0.5 shrink-0">●</span>
              <span><strong className="text-gray-800">书写纠错：</strong>孩子英文字母大小不分、占格混乱时针对性练习</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-500 mt-0.5 shrink-0">●</span>
              <span><strong className="text-gray-800">考试准备：</strong>剑桥少儿英语、PET等考试的书写规范训练</span>
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
                <span>四线三格怎么用？</span>
                <span className="text-gray-400 group-open:rotate-180 transition-transform text-xs">▼</span>
              </summary>
              <div className="px-4 pb-4 text-sm text-gray-500 leading-relaxed">小写字母的主体写在第二线和第三线之间（中间两格），字母的竖笔向上延伸到第一线，有尾部延伸的字母（如g、p、y）向下延伸到第四线。大写字母占满上面三格。</div>
            </details>
            <details className="group border border-gray-200 rounded-lg">
              <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-700 hover:text-gray-900 list-none font-medium">
                <span>英文字帖和中文田字格字帖有什么区别？</span>
                <span className="text-gray-400 group-open:rotate-180 transition-transform text-xs">▼</span>
              </summary>
              <div className="px-4 pb-4 text-sm text-gray-500 leading-relaxed">英文字帖使用四线三格格式，重点训练字母的占格位置和连笔；中文字帖使用田字格或米字格，重点训练笔画的起止位置和汉字结构。</div>
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
            <a href="/resources/english" className="block bg-gray-50 hover:bg-blue-50 border border-gray-200 hover:border-blue-300 rounded-xl p-4 transition-all group">
              <div className="text-2xl mb-2">📖</div>
              <div className="font-bold text-gray-700 text-sm group-hover:text-blue-600 transition-colors">英语学习资源</div>
              <div className="text-xs text-gray-400 mt-1">英语学习资料</div>
            </a>
          </div>
        </section>
      </div>

      {/* 使用指南 */}
      <div className="max-w-4xl mx-auto px-4 py-12">
        <ToolGuide {...toolGuides['english-calligraphy']} />
      </div>
    </div>
  );
}
