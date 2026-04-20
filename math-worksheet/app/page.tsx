'use client';

import { useState, useRef, useCallback } from 'react';
import {
  generateQuestions,
  Question,
  QuestionType,
  QuestionConfig,
  QUESTION_TYPE_META,
  GRADES,
  RANGE_OPTIONS,
  COUNT_OPTIONS,
} from '@/lib/questionGenerator';
import WorksheetPreview, {
  WorksheetConfig,
  TemplateType,
  WorksheetMode,
} from '@/components/WorksheetPreview';
import { exportToPDF } from '@/lib/pdfExport';

// 两个 Ref：一个题目卷，一个答案卷
function WorksheetSection({
  questions,
  config,
  ref,
}: {
  questions: Question[];
  config: WorksheetConfig;
  ref: React.RefObject<HTMLDivElement | null>;
}) {
  return (
    <div ref={ref as React.RefObject<HTMLDivElement>}>
      <WorksheetPreview questions={questions} config={config} />
    </div>
  );
}

export default function Home() {
  // ===== 出题配置 =====
  const [grade, setGrade] = useState(1);
  const [selectedTypes, setSelectedTypes] = useState<QuestionType[]>(['addition']);
  const [rangeIndex, setRangeIndex] = useState(1);
  const [count, setCount] = useState(20);
  const [template, setTemplate] = useState<TemplateType>('tianzige');
  const [questionsPerRow, setQuestionsPerRow] = useState(6);
  const [fontSize, setFontSize] = useState<'sm' | 'md' | 'lg'>('md');
  const [shuffle, setShuffle] = useState(true);
  const [showNameField, setShowNameField] = useState(true);
  const [showDateField, setShowDateField] = useState(true);
  const [sheetTitle, setSheetTitle] = useState('数学练习');
  // ===== 答案卷新增 =====
  const [mode, setMode] = useState<WorksheetMode>('worksheet');
  const [showAnswers, setShowAnswers] = useState(false); // 题目卷内嵌答案

  // ===== 题目状态 =====
  const [questions, setQuestions] = useState<Question[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [hasGenerated, setHasGenerated] = useState(false);

  // 两个 Ref
  const worksheetRef = useRef<HTMLDivElement>(null);
  const answersheetRef = useRef<HTMLDivElement>(null);

  // ===== 题型切换 =====
  const toggleType = (type: QuestionType) => {
    setSelectedTypes(prev => {
      if (prev.includes(type)) {
        if (prev.length === 1) return prev;
        return prev.filter(t => t !== type);
      }
      return [...prev, type];
    });
  };

  // ===== 生成 =====
  const handleGenerate = useCallback(() => {
    setIsGenerating(true);
    setHasGenerated(false);
    setTimeout(() => {
      const config: QuestionConfig = {
        types: selectedTypes,
        range: RANGE_OPTIONS[rangeIndex].value,
        count,
        grade,
        includeAnswers: true,
        shuffle,
      };
      const qs = generateQuestions(config);
      setQuestions(qs);
      setHasGenerated(true);
      setIsGenerating(false);
    }, 50);
  }, [selectedTypes, rangeIndex, count, grade, shuffle]);

  // ===== 导出一份（题目卷或答案卷）=====
  const exportOne = useCallback(
    async (mode: WorksheetMode, label: string) => {
      const ref = mode === 'worksheet' ? worksheetRef : answersheetRef;
      const btn = document.getElementById(`export-${mode}-btn`) as HTMLButtonElement | null;
      if (!ref.current) return;
      if (btn) { btn.textContent = '生成中...'; btn.disabled = true; }
      try {
        await exportToPDF(ref.current, `${sheetTitle || '数学练习'}-${label}.pdf`);
      } catch (err) {
        console.error(err);
        alert(`${label}导出失败`);
      } finally {
        if (btn) { btn.textContent = `📄 ${label}`; btn.disabled = false; }
      }
    },
    [sheetTitle]
  );

  // ===== 导出双卷（题目卷 + 答案卷）=====
  const exportBoth = useCallback(async () => {
    if (!worksheetRef.current || !answersheetRef.current) return;
    const btn = document.getElementById('export-both-btn') as HTMLButtonElement | null;
    if (btn) { btn.textContent = '生成中...'; btn.disabled = true; }
    try {
      // 题目卷
      await exportToPDF(worksheetRef.current, `${sheetTitle || '数学练习'}-题目卷.pdf`);
      // 答案卷
      await exportToPDF(answersheetRef.current, `${sheetTitle || '数学练习'}-答案卷.pdf`);
    } catch (err) {
      console.error(err);
      alert('导出失败');
    } finally {
      if (btn) { btn.textContent = '📄 双卷导出'; btn.disabled = false; }
    }
  }, [sheetTitle]);

  // ===== 打印 ======
  const handlePrint = useCallback(() => {
    window.print();
  }, []);

  // ===== 配置 =====
  const worksheetConfig: WorksheetConfig = {
    title: sheetTitle,
    grade,
    date: new Date().toLocaleDateString('zh-CN'),
    name: '',
    template,
    questionsPerRow,
    fontSize,
    showPageNumber: true,
    showNameField,
    showDateField,
    mode: 'worksheet',
    showAnswers,
  };

  const answersheetConfig: WorksheetConfig = {
    ...worksheetConfig,
    mode: 'answersheet',
    showAnswers: false,
  };

  // ===== 模板选项 =====
  const templates: { value: TemplateType; label: string; desc: string; icon: string }[] = [
    { value: 'tianzige', label: '田字格', desc: '1-2年级，带辅助线', icon: '▦' },
    { value: 'fangge', label: '方格纸', desc: '3-4年级', icon: '▤' },
    { value: 'hengxian', label: '横线格', desc: '高年级', icon: '≡' },
    { value: 'kongbai', label: '空白纸', desc: '自由书写', icon: '□' },
  ];

  return (
    <div
      className="min-h-screen bg-gray-50 flex flex-col"
      style={{ fontFamily: '"Noto Sans SC", "Microsoft YaHei", sans-serif' }}
    >

      {/* ===== 顶部标题栏 ===== */}
      <header className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-wide">🧮 算个题吧</h1>
            <p className="text-blue-100 text-sm mt-0.5">数学练习纸生成器 · 完全免费 · 免登录</p>
          </div>
          <div className="flex items-center gap-3 text-sm">
            <a
              href="https://xgzb.top"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-100 hover:text-white transition-colors"
            >
              📖 写个字吧（字帖）
            </a>
          </div>
        </div>
      </header>

      {/* ===== 主内容区 ===== */}
      <div className="flex-1 max-w-6xl mx-auto w-full px-4 py-6 flex gap-6">

        {/* ===== 左侧配置面板 ===== */}
        <aside className="w-80 flex-shrink-0 space-y-5 print:hidden">

          {/* 出题设置 */}
          <section className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <h2 className="text-base font-bold text-gray-800 mb-4 flex items-center gap-2">
              <span className="w-6 h-6 bg-blue-500 text-white rounded-full text-xs flex items-center justify-center">1</span>
              出题设置
            </h2>

            <div className="mb-4">
              <label className="text-sm font-medium text-gray-600 mb-2 block">年级</label>
              <div className="flex flex-wrap gap-2">
                {GRADES.map(g => (
                  <button
                    key={g}
                    onClick={() => {
                      setGrade(g);
                      if (g <= 2) setTemplate('tianzige');
                      else if (g <= 4) setTemplate('fangge');
                      else setTemplate('hengxian');
                    }}
                    className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                      grade === g
                        ? 'bg-blue-500 text-white shadow-sm'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    {g}年级
                  </button>
                ))}
              </div>
            </div>

            <div className="mb-4">
              <label className="text-sm font-medium text-gray-600 mb-2 block">题型（可多选）</label>
              <div className="flex flex-wrap gap-1.5">
                {(Object.keys(QUESTION_TYPE_META) as QuestionType[])
                  .filter(t => {
                    const meta = QUESTION_TYPE_META[t];
                    return grade >= meta.gradeMin && grade <= meta.gradeMax;
                  })
                  .map(type => {
                    const meta = QUESTION_TYPE_META[type];
                    const isActive = selectedTypes.includes(type);
                    return (
                      <button
                        key={type}
                        onClick={() => toggleType(type)}
                        className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${
                          isActive
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
                        }`}
                      >
                        {meta.icon} {meta.label}
                      </button>
                    );
                  })}
              </div>
            </div>

            <div className="mb-4">
              <label className="text-sm font-medium text-gray-600 mb-2 block">数字范围</label>
              <div className="flex flex-wrap gap-2">
                {RANGE_OPTIONS.map((opt, i) => (
                  <button
                    key={opt.label}
                    onClick={() => setRangeIndex(i)}
                    className={`px-3 py-1.5 rounded-lg text-sm transition-all ${
                      rangeIndex === i
                        ? 'bg-blue-500 text-white shadow-sm'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>

            <div className="mb-4">
              <label className="text-sm font-medium text-gray-600 mb-2 block">
                题目数量：{count} 题
              </label>
              <input
                type="range" min={5} max={100} step={5}
                value={count}
                onChange={e => setCount(Number(e.target.value))}
                className="w-full accent-blue-500"
              />
              <div className="flex justify-between text-xs text-gray-400 mt-1">
                <span>5</span><span>100</span>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <input
                type="checkbox" id="shuffle" checked={shuffle}
                onChange={e => setShuffle(e.target.checked)}
                className="accent-blue-500 w-4 h-4"
              />
              <label htmlFor="shuffle" className="text-sm text-gray-600">打乱题目顺序</label>
            </div>
          </section>

          {/* 模板设置 */}
          <section className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <h2 className="text-base font-bold text-gray-800 mb-4 flex items-center gap-2">
              <span className="w-6 h-6 bg-blue-500 text-white rounded-full text-xs flex items-center justify-center">2</span>
              模板设置
            </h2>

            <div className="mb-4">
              <label className="text-sm font-medium text-gray-600 mb-2 block">纸张模板</label>
              <div className="grid grid-cols-2 gap-2">
                {templates.map(t => (
                  <button
                    key={t.value}
                    onClick={() => setTemplate(t.value)}
                    className={`p-3 rounded-xl border-2 text-left transition-all ${
                      template === t.value
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-100 hover:border-gray-300 bg-white'
                    }`}
                  >
                    <div className="text-lg mb-0.5">{t.icon}</div>
                    <div className="text-sm font-medium text-gray-800">{t.label}</div>
                    <div className="text-xs text-gray-400 mt-0.5">{t.desc}</div>
                  </button>
                ))}
              </div>
              {grade <= 2 && template !== 'tianzige' && (
                <p className="text-xs text-amber-600 mt-2">💡 {grade}年级建议「田字格」</p>
              )}
            </div>

            <div className="mb-4">
              <label className="text-sm font-medium text-gray-600 mb-2 block">每行题数：{questionsPerRow} 题</label>
              <div className="flex gap-2">
                {[4, 5, 6, 8].map(n => (
                  <button
                    key={n}
                    onClick={() => setQuestionsPerRow(n)}
                    className={`flex-1 py-1.5 rounded-lg text-sm font-medium transition-all ${
                      questionsPerRow === n
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    {n}
                  </button>
                ))}
              </div>
            </div>

            <div className="mb-4">
              <label className="text-sm font-medium text-gray-600 mb-2 block">字体大小</label>
              <div className="flex gap-2">
                {([['sm', '小'], ['md', '中'], ['lg', '大']] as const).map(([v, label]) => (
                  <button
                    key={v}
                    onClick={() => setFontSize(v)}
                    className={`flex-1 py-1.5 rounded-lg text-sm font-medium transition-all ${
                      fontSize === v
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-600 mb-2 block">附加内容</label>
              {[
                { label: '显示姓名栏', checked: showNameField, onChange: setShowNameField },
                { label: '显示日期栏', checked: showDateField, onChange: setShowDateField },
              ].map(({ label, checked, onChange }) => (
                <label key={label} className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox" checked={checked}
                    onChange={e => onChange(e.target.checked)}
                    className="accent-blue-500 w-4 h-4"
                  />
                  <span className="text-sm text-gray-600">{label}</span>
                </label>
              ))}
            </div>
          </section>

          {/* 答案卷设置（新增） */}
          <section className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <h2 className="text-base font-bold text-gray-800 mb-4 flex items-center gap-2">
              <span className="w-6 h-6 bg-green-500 text-white rounded-full text-xs flex items-center justify-center">3</span>
              答案卷设置
            </h2>
            <div className="space-y-3">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={showAnswers}
                  onChange={e => setShowAnswers(e.target.checked)}
                  className="accent-blue-500 w-4 h-4"
                />
                <div>
                  <span className="text-sm text-gray-700 font-medium">题目内嵌答案</span>
                  <p className="text-xs text-gray-400">在每道题下方同时显示答案，方便家长检查</p>
                </div>
              </label>
              <div className="bg-green-50 rounded-lg p-3 text-xs text-green-700 leading-relaxed">
                💡 <strong>推荐用法：</strong><br />
                打印题目卷（不加答案）让孩子作答，<br />
                再打印答案卷（红色标注）供家长核对。
              </div>
            </div>
          </section>

          {/* 标题设置 */}
          <section className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <h2 className="text-base font-bold text-gray-800 mb-4 flex items-center gap-2">
              <span className="w-6 h-6 bg-gray-400 text-white rounded-full text-xs flex items-center justify-center">4</span>
              标题设置
            </h2>
            <input
              type="text"
              value={sheetTitle}
              onChange={e => setSheetTitle(e.target.value)}
              placeholder="例如：数学练习 / 单元测验"
              className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent"
            />
          </section>

          {/* 生成按钮 */}
          <button
            onClick={handleGenerate}
            disabled={isGenerating || selectedTypes.length === 0}
            className="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-bold text-base rounded-xl shadow-sm transition-colors flex items-center justify-center gap-2"
          >
            {isGenerating ? '⏳ 生成中...' : '🎲 立即出题'}
          </button>

          {/* 导出按钮（生成后显示） */}
          {hasGenerated && questions.length > 0 && (
            <div className="space-y-2">
              <button
                id="export-both-btn"
                onClick={exportBoth}
                className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-base rounded-xl shadow-sm transition-colors flex items-center justify-center gap-2"
              >
                📄 双卷导出（题目卷 + 答案卷）
              </button>
              <div className="flex gap-2">
                <button
                  id="export-worksheet-btn"
                  onClick={() => exportOne('worksheet', '题目卷')}
                  className="flex-1 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors"
                >
                  📄 题目卷
                </button>
                <button
                  id="export-answersheet-btn"
                  onClick={() => exportOne('answersheet', '答案卷')}
                  className="flex-1 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-colors"
                >
                  📄 答案卷
                </button>
              </div>
              <button
                onClick={handlePrint}
                className="w-full py-2.5 bg-white border-2 border-blue-600 text-blue-600 hover:bg-blue-50 font-bold text-sm rounded-xl transition-colors"
              >
                🖨️ 打印预览
              </button>
            </div>
          )}
        </aside>

        {/* ===== 右侧预览区 ===== */}
        <main className="flex-1 min-w-0">

          {!hasGenerated && (
            <div className="flex flex-col items-center justify-center h-96 bg-white rounded-xl border-2 border-dashed border-gray-200">
              <div className="text-6xl mb-4 opacity-30">📝</div>
              <h3 className="text-xl font-bold text-gray-400 mb-2">还没有生成题目</h3>
              <p className="text-gray-400 text-sm text-center max-w-sm">
                在左侧选择年级、题型，<br />点击「立即出题」开始生成练习卷
              </p>
            </div>
          )}

          {hasGenerated && (
            <div>

              {/* 预览工具栏 */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-100 px-4 py-3 mb-4 flex items-center justify-between print:hidden">
                <div className="flex items-center gap-3">
                  {/* 模式切换 */}
                  <div className="flex rounded-lg border border-gray-200 overflow-hidden">
                    <button
                      onClick={() => setMode('worksheet')}
                      className={`px-3 py-1.5 text-sm font-medium transition-colors ${
                        mode === 'worksheet'
                          ? 'bg-blue-500 text-white'
                          : 'bg-white text-gray-600 hover:bg-gray-50'
                      }`}
                    >
                      📝 题目卷
                    </button>
                    <button
                      onClick={() => setMode('answersheet')}
                      className={`px-3 py-1.5 text-sm font-medium transition-colors ${
                        mode === 'answersheet'
                          ? 'bg-green-500 text-white'
                          : 'bg-white text-gray-600 hover:bg-gray-50'
                      }`}
                    >
                      ✅ 答案卷
                    </button>
                  </div>
                  <div className="text-sm text-gray-500">
                    共 <strong className="text-blue-600">{questions.length}</strong> 题
                    {mode === 'worksheet' && showAnswers && (
                      <span className="ml-2 text-green-600 font-medium">· 含答案</span>
                    )}
                    {mode === 'answersheet' && (
                      <span className="ml-2 text-green-600 font-medium">· 参考答案</span>
                    )}
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={handleGenerate}
                    className="px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-lg transition-colors"
                  >
                    🔄 重新出题
                  </button>
                  {mode === 'worksheet' && (
                    <button
                      id="export-worksheet-btn-top"
                      onClick={() => exportOne('worksheet', '题目卷')}
                      className="px-3 py-1.5 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                    >
                      📄 题目卷
                    </button>
                  )}
                  {mode === 'answersheet' && (
                    <button
                      id="export-answersheet-btn-top"
                      onClick={() => exportOne('answersheet', '答案卷')}
                      className="px-3 py-1.5 text-sm bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
                    >
                      📄 答案卷
                    </button>
                  )}
                  <button
                    onClick={handlePrint}
                    className="px-3 py-1.5 text-sm bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-colors"
                  >
                    🖨️ 打印
                  </button>
                </div>
              </div>

              {/* 题目卷 */}
              <div
                style={{ display: mode === 'worksheet' ? 'block' : 'none' }}
                className="worksheet-wrapper"
              >
                <WorksheetSection
                  questions={questions}
                  config={worksheetConfig}
                  ref={worksheetRef}
                />
              </div>

              {/* 答案卷 */}
              {mode === 'answersheet' && (
                <div className="worksheet-wrapper">
                  <WorksheetSection
                    questions={questions}
                    config={answersheetConfig}
                    ref={answersheetRef}
                  />
                </div>
              )}
            </div>
          )}
        </main>
      </div>

      {/* ===== 底部 ===== */}
      <footer className="bg-white border-t border-gray-100 py-4 text-center text-sm text-gray-400 print:hidden">
        <p>
          🧮 算个题吧 · 完全免费 · 免登录 ·
          <a href="https://xgzb.top" target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">写个字吧</a>
          · © 2026
        </p>
      </footer>

      {/* ===== 打印样式 ===== */}
      <style jsx global>{`
        @media print {
          body * { visibility: hidden; }
          .worksheet-wrapper,
          .worksheet-wrapper * { visibility: visible; }
          .worksheet-wrapper {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
          }
          @page { size: A4 portrait; margin: 0; }
        }
      `}</style>
    </div>
  );
}
