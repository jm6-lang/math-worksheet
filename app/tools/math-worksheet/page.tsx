'use client';

import { useState, useRef, useCallback, useEffect } from 'react';
import {
  generateQuestions,
  Question,
  QuestionType,
  QuestionConfig,
  QUESTION_TYPE_META,
  GRADES,
  RANGE_OPTIONS,
} from '@/lib/questionGenerator';
import WorksheetPreview, {
  WorksheetConfig,
  TemplateType,
  WorksheetMode,
} from '@/components/WorksheetPreview';
import { exportToPDF } from '@/lib/pdfExport';
import ToolGuide from '@/components/ToolGuide';
import { toolGuides } from '@/lib/toolGuides';

// 快捷配置预设
const QUICK_PRESETS = [
  { label: '10道基础', grade: 1, types: ['addition', 'subtraction'] as QuestionType[], count: 10, rangeIndex: 1, icon: '🎯', desc: '加减法入门' },
  { label: '20道竖式', grade: 2, types: ['vertical_add', 'vertical_sub'] as QuestionType[], count: 20, rangeIndex: 2, icon: '📐', desc: '竖式计算练习' },
  { label: '50道综合', grade: 3, types: ['addition', 'subtraction', 'multiplication', 'division'] as QuestionType[], count: 50, rangeIndex: 3, icon: '🚀', desc: '四则运算混合' },
  { label: '100道强化', grade: 4, types: ['mixed'] as QuestionType[], count: 100, rangeIndex: 3, icon: '⚡', desc: '混合运算强化' },
];

// 模板配置
const TEMPLATES: { value: TemplateType; label: string; desc: string; icon: string; preview: string }[] = [
  { value: 'tianzige', label: '田字格', desc: '1-2年级', icon: '▦', preview: '田' },
  { value: 'fangge', label: '方格纸', desc: '3-4年级', icon: '▤', preview: '□' },
  { value: 'hengxian', label: '横线格', desc: '高年级', icon: '≡', preview: '三' },
  { value: 'kongbai', label: '空白纸', desc: '自由书写', icon: '□', preview: '白' },
];

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

export default function MathWorksheetPage() {
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
  const [mode, setMode] = useState<WorksheetMode>('worksheet');
  const [showAnswers, setShowAnswers] = useState(false);
  const [showConfig, setShowConfig] = useState(true);
  const [mobileMenu, setMobileMenu] = useState(false);
  const [showGuide, setShowGuide] = useState(false);
  const [showDonate, setShowDonate] = useState(false);

  // ===== 题目状态 =====
  const [questions, setQuestions] = useState<Question[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [hasGenerated, setHasGenerated] = useState(false);

  const worksheetRef = useRef<HTMLDivElement>(null);
  const answersheetRef = useRef<HTMLDivElement>(null);

  // ===== 快捷预设生成 =====
  const handleQuickPreset = useCallback((preset: typeof QUICK_PRESETS[0]) => {
    setGrade(preset.grade);
    setSelectedTypes(preset.types);
    setCount(preset.count);
    setRangeIndex(preset.rangeIndex);
    if (preset.grade <= 2) setTemplate('tianzige');
    else if (preset.grade <= 4) setTemplate('fangge');
    else setTemplate('hengxian');
    
    setTimeout(() => {
      const config: QuestionConfig = {
        types: preset.types,
        range: RANGE_OPTIONS[preset.rangeIndex].value,
        count: preset.count,
        grade: preset.grade,
        includeAnswers: true,
        shuffle: true,
      };
      setQuestions(generateQuestions(config));
      setHasGenerated(true);
    }, 50);
  }, []);

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

  // ===== 导出 =====
  const exportOne = useCallback(
    async (modeType: WorksheetMode, label: string) => {
      const ref = modeType === 'worksheet' ? worksheetRef : answersheetRef;
      if (!ref.current) return;
      try {
        await exportToPDF(ref.current, `${sheetTitle || '数学练习'}-${label}.pdf`);
      } catch (err) {
        console.error(err);
        alert(`${label}导出失败`);
      }
    },
    [sheetTitle]
  );

  const exportBoth = useCallback(async () => {
    if (!worksheetRef.current || !answersheetRef.current) return;
    try {
      await exportToPDF(worksheetRef.current, `${sheetTitle || '数学练习'}-题目卷.pdf`);
      await exportToPDF(answersheetRef.current, `${sheetTitle || '数学练习'}-答案卷.pdf`);
    } catch (err) {
      console.error(err);
      alert('导出失败');
    }
  }, [sheetTitle]);

  const handlePrint = useCallback(() => window.print(), []);

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

  // 滚动到预览区
  useEffect(() => {
    if (hasGenerated) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }, [hasGenerated]);

  return (
    <div className="min-h-screen bg-[#0f0f0f] text-white" style={{ fontFamily: '"Noto Sans SC", "Microsoft YaHei", sans-serif' }}>
      
      {/* ===== 顶部导航 ===== */}
      <nav className="print:hidden fixed top-0 left-0 right-0 z-50 bg-[#0f0f0f]/90 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center text-xl">🧮</div>
              <a href="/" className="text-xl font-bold hover:opacity-80 transition-opacity text-white">数学练习题</a>
            </div>
            {/* 桌面导航 */}
            <div className="hidden md:flex items-center gap-1">
              <a href="/" className="px-3 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">首页</a>
              <a href="/tools/math-worksheet" className="px-3 py-2 text-sm text-white bg-white/10 rounded-lg font-medium">数学练习卷</a>
              <a href="/tools/calligraphy" className="px-3 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">字帖生成器</a>
              <a href="/tools/sudoku" className="px-3 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">数独游戏</a>
            </div>
            {/* 移动端 */}
            <button onClick={() => setMobileMenu(!mobileMenu)} className="md:hidden p-2 text-gray-300 hover:text-white transition-colors">{mobileMenu ? '✕' : '☰'}</button>
          </div>
        </div>
        {mobileMenu && (
          <div className="md:hidden bg-[#1a1a1a] border-t border-white/10 py-4 px-4 space-y-1">
            <a href="/" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">首页</a>
            <a href="/tools/math-worksheet" className="block px-4 py-2 text-white bg-white/10 rounded-lg">数学练习卷</a>
            <a href="/tools/calligraphy" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">字帖生成器</a>
            <a href="/tools/sudoku" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">数独游戏</a>
          </div>
        )}
      </nav>

      {/* ===== Hero 区域 ===== */}
      {!hasGenerated && (
        <div className="print:hidden pt-24 pb-12 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl sm:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent">
              数学练习卷生成器
            </h1>
            <p className="text-xl text-gray-400 mb-10">
              支持加减乘除、竖式计算等11种题型 · 田字格/方格/横线格多模板 · PDF即印即用
            </p>

            {/* 快捷出题卡片 */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto mb-12">
              {QUICK_PRESETS.map((preset) => (
                <button
                  key={preset.label}
                  onClick={() => handleQuickPreset(preset)}
                  className="group relative bg-white/5 hover:bg-white/10 border border-white/10 hover:border-blue-500/50 rounded-2xl p-6 transition-all duration-300 hover:scale-105"
                >
                  <div className="text-4xl mb-3 group-hover:scale-110 transition-transform">{preset.icon}</div>
                  <div className="text-lg font-bold mb-1">{preset.label}</div>
                  <div className="text-sm text-gray-500">{preset.desc}</div>
                  <div className="absolute inset-0 bg-gradient-to-br from-blue-500/0 to-purple-500/0 group-hover:from-blue-500/10 group-hover:to-purple-500/10 rounded-2xl transition-all" />
                </button>
              ))}
            </div>

            {/* 模板选择 */}
            <div className="mb-8">
              <h2 className="text-lg font-medium text-gray-400 mb-6">选择模板样式</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
                {TEMPLATES.map((t) => (
                  <button
                    key={t.value}
                    onClick={() => setTemplate(t.value)}
                    className={`group relative bg-white/5 hover:bg-white/10 border-2 rounded-2xl p-4 transition-all duration-300 ${
                      template === t.value
                        ? 'border-blue-500 bg-blue-500/10'
                        : 'border-white/10 hover:border-white/30'
                    }`}
                  >
                    <div className="text-base font-bold mb-1">{t.label}</div>
                    <div className="text-sm text-gray-500">{t.desc}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* 高级配置按钮 */}
            <button
              onClick={() => setShowConfig(!showConfig)}
              className="text-sm text-gray-500 hover:text-white transition-colors flex items-center gap-2 mx-auto"
            >
              {showConfig ? '收起高级配置 ▲' : '展开高级配置 ▼'}
            </button>
          </div>
        </div>
      )}

      {/* ===== 高级配置面板 ===== */}
      {(showConfig || hasGenerated) && (
        <div className={`print:hidden ${hasGenerated ? 'pt-20' : ''} px-4 pb-12`}>
          <div className="max-w-6xl mx-auto">
            <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* 出题设置 */}
                <div>
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                    <span className="w-6 h-6 bg-blue-500 rounded-full text-xs flex items-center justify-center">1</span>
                    出题设置
                  </h3>
                  
                  <div className="space-y-4">
                    <div>
                      <label className="text-sm text-gray-400 mb-2 block">年级</label>
                      <div className="flex flex-wrap gap-2">
                        {GRADES.map(g => (
                          <button
                            key={g}
                            onClick={() => setGrade(g)}
                            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                              grade === g
                                ? 'bg-blue-500 text-white'
                                : 'bg-white/10 text-gray-300 hover:bg-white/20'
                            }`}
                          >
                            {g}年级
                          </button>
                        ))}
                      </div>
                    </div>

                    <div>
                      <label className="text-sm text-gray-400 mb-2 block">题型</label>
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
                                    : 'bg-white/10 text-gray-400 hover:bg-white/20'
                                }`}
                              >
                                {meta.label}
                              </button>
                            );
                          })}
                      </div>
                    </div>

                    <div>
                      <label className="text-sm text-gray-400 mb-2 block">数字范围</label>
                      <div className="flex flex-wrap gap-2">
                        {RANGE_OPTIONS.map((opt, i) => (
                          <button
                            key={opt.label}
                            onClick={() => setRangeIndex(i)}
                            className={`px-3 py-1.5 rounded-lg text-sm transition-all ${
                              rangeIndex === i
                                ? 'bg-blue-500 text-white'
                                : 'bg-white/10 text-gray-300 hover:bg-white/20'
                            }`}
                          >
                            {opt.label}
                          </button>
                        ))}
                      </div>
                    </div>

                    <div>
                      <label className="text-sm text-gray-400 mb-2 block">题目数量: {count}</label>
                      <input
                        type="range" min={5} max={100} step={5}
                        value={count}
                        onChange={e => setCount(Number(e.target.value))}
                        className="w-full accent-blue-500"
                      />
                    </div>
                  </div>
                </div>

                {/* 模板设置 */}
                <div>
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                    <span className="w-6 h-6 bg-blue-500 rounded-full text-xs flex items-center justify-center">2</span>
                    模板设置
                  </h3>
                  
                  <div className="space-y-4">
                    <div>
                      <label className="text-sm text-gray-400 mb-2 block">每行题数: {questionsPerRow}</label>
                      <div className="flex gap-2">
                        {[4, 5, 6, 8].map(n => (
                          <button
                            key={n}
                            onClick={() => setQuestionsPerRow(n)}
                            className={`flex-1 py-1.5 rounded-lg text-sm font-medium transition-all ${
                              questionsPerRow === n
                                ? 'bg-blue-500 text-white'
                                : 'bg-white/10 text-gray-300 hover:bg-white/20'
                            }`}
                          >
                            {n}
                          </button>
                        ))}
                      </div>
                    </div>

                    <div>
                      <label className="text-sm text-gray-400 mb-2 block">字体大小</label>
                      <div className="flex gap-2">
                        {(['sm', 'md', 'lg'] as const).map((v) => (
                          <button
                            key={v}
                            onClick={() => setFontSize(v)}
                            className={`flex-1 py-1.5 rounded-lg text-sm font-medium transition-all ${
                              fontSize === v
                                ? 'bg-blue-500 text-white'
                                : 'bg-white/10 text-gray-300 hover:bg-white/20'
                            }`}
                          >
                            {v === 'sm' ? '小' : v === 'md' ? '中' : '大'}
                          </button>
                        ))}
                      </div>
                    </div>

                    <div className="space-y-2">
                      <label className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="checkbox" checked={showNameField}
                          onChange={e => setShowNameField(e.target.checked)}
                          className="accent-blue-500 w-4 h-4"
                        />
                        <span className="text-sm text-gray-300">显示姓名栏</span>
                      </label>
                      <label className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="checkbox" checked={showDateField}
                          onChange={e => setShowDateField(e.target.checked)}
                          className="accent-blue-500 w-4 h-4"
                        />
                        <span className="text-sm text-gray-300">显示日期栏</span>
                      </label>
                      <label className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="checkbox" checked={showAnswers}
                          onChange={e => setShowAnswers(e.target.checked)}
                          className="accent-blue-500 w-4 h-4"
                        />
                        <span className="text-sm text-gray-300">题目内嵌答案</span>
                      </label>
                    </div>
                  </div>
                </div>

                {/* 标题与操作 */}
                <div>
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                    <span className="w-6 h-6 bg-blue-500 rounded-full text-xs flex items-center justify-center">3</span>
                    生成练习
                  </h3>
                  
                  <div className="space-y-4">
                    <div>
                      <label className="text-sm text-gray-400 mb-2 block">练习标题</label>
                      <input
                        type="text"
                        value={sheetTitle}
                        onChange={e => setSheetTitle(e.target.value)}
                        placeholder="例如：数学练习"
                        className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
                      />
                    </div>

                    <button
                      onClick={handleGenerate}
                      disabled={isGenerating || selectedTypes.length === 0}
                      className="w-full py-3 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 disabled:opacity-50 text-white font-bold rounded-xl transition-all"
                    >
                      {isGenerating ? '⏳ 生成中...' : '🎲 立即出题'}
                    </button>

                    {hasGenerated && (
                      <div className="space-y-2 pt-4 border-t border-white/10">
                        <button
                          onClick={exportBoth}
                          className="w-full py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-medium rounded-lg transition-colors"
                        >
                          📄 导出题目卷+答案卷
                        </button>

                        <div className="flex gap-2">
                          <button
                            onClick={() => exportOne('worksheet', '题目卷')}
                            className="flex-1 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors"
                          >
                            题目卷
                          </button>
                          <button
                            onClick={() => exportOne('answersheet', '答案卷')}
                            className="flex-1 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-colors"
                          >
                            答案卷
                          </button>
                        </div>
                        <button
                          onClick={handlePrint}
                          className="w-full py-2 bg-white/10 hover:bg-white/20 text-white text-sm font-medium rounded-lg transition-colors"
                        >
                          🖨️ 打印预览
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ===== 预览区 ===== */}
      {hasGenerated && (
        <div className="px-4 pb-20">
          <div className="max-w-6xl mx-auto">
            {/* 预览工具栏 */}
            <div className="print:hidden flex items-center justify-between mb-6">
              <div className="flex items-center gap-4">
                <h2 className="text-2xl font-bold">练习预览</h2>
                <span className="text-gray-500">共 {questions.length} 题</span>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setMode('worksheet')}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    mode === 'worksheet'
                      ? 'bg-blue-500 text-white'
                      : 'bg-white/10 text-gray-300 hover:bg-white/20'
                  }`}
                >
                  📝 题目卷
                </button>
                <button
                  onClick={() => setMode('answersheet')}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    mode === 'answersheet'
                      ? 'bg-green-500 text-white'
                      : 'bg-white/10 text-gray-300 hover:bg-white/20'
                  }`}
                >
                  ✅ 答案卷
                </button>
                <button
                  onClick={() => { setHasGenerated(false); setQuestions([]); }}
                  className="px-4 py-2 bg-white/10 hover:bg-white/20 text-gray-300 rounded-lg font-medium transition-all ml-4"
                >
                  ← 返回首页
                </button>
              </div>
            </div>

            {/* 工作表 */}
            <div className="bg-white rounded-xl overflow-hidden shadow-2xl">
              <div style={{ display: mode === 'worksheet' ? 'block' : 'none' }} className="worksheet-wrapper">
                <WorksheetSection questions={questions} config={worksheetConfig} ref={worksheetRef} />
              </div>
              {mode === 'answersheet' && (
                <div className="worksheet-wrapper">
                  <WorksheetSection questions={questions} config={answersheetConfig} ref={answersheetRef} />
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ===== 功能介绍 + FAQ ===== */}
      {!hasGenerated && (
        <div className="print:hidden px-4 pb-12">
          <div className="max-w-4xl mx-auto">
            {/* 功能介绍卡片 */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
              <div className="bg-white/5 border border-white/10 rounded-2xl p-6 text-center hover:border-blue-500/30 transition-colors">
                <div className="text-3xl mb-3">📐</div>
                <h3 className="font-bold mb-2">11种题型</h3>
                <p className="text-sm text-gray-400 leading-relaxed">加减乘除、竖式计算、分数运算、一元一次方程，覆盖小学全阶段</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-2xl p-6 text-center hover:border-blue-500/30 transition-colors">
                <div className="text-3xl mb-3">🖨️</div>
                <h3 className="font-bold mb-2">即印即用</h3>
                <p className="text-sm text-gray-400 leading-relaxed">标准A4 PDF，支持直接浏览器打印，也可导出保存到本地</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-2xl p-6 text-center hover:border-blue-500/30 transition-colors">
                <div className="text-3xl mb-3">♻️</div>
                <h3 className="font-bold mb-2">题库随机</h3>
                <p className="text-sm text-gray-400 leading-relaxed">每次生成题目随机打乱，可无限次生成同一配置不重复</p>
              </div>
            </div>

            {/* FAQ 手风琴 */}
            <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
              <h2 className="text-2xl font-bold mb-6 text-center">常见问题</h2>
              <div className="space-y-2">
                {[
                  { q: "支持哪些年级？", a: "覆盖小学1-6年级，支持加减乘除、竖式计算、分数、方程等11种题型，幼儿园大班也适用。" },
                  { q: "导出的PDF能直接打印吗？", a: "是的，生成的PDF为标准A4尺寸，可直接在浏览器中按 Ctrl+P 打印，也可导出保存到本地。" },
                  { q: "可以只导出题目卷或答案卷吗？", a: "可以。支持分别导出题目卷、答案卷，或一键同时导出两份PDF，满足不同使用场景。" },
                  { q: "字体大小可以调整吗？", a: "支持小/中/大三种字号，也可自定义每行题目数量，适配不同年级和打印需求。" },
                  { q: "题目会自动打乱吗？", a: "默认开启随机打乱，每次生成的题目顺序不同，防止学生背答案。关闭随机可保持稳定顺序。" },
                  { q: "收费吗？有水印吗？", a: "完全免费，无水印，无广告，可无限次使用。" },
                ].map((item, i) => (
                  <details key={i} className="group border border-white/10 rounded-lg">
                    <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-300 hover:text-white list-none font-medium">
                      <span>{item.q}</span>
                      <span className="text-gray-500 group-open:rotate-180 transition-transform text-xs">▼</span>
                    </summary>
                    <div className="px-4 pb-4 text-sm text-gray-400 leading-relaxed">{item.a}</div>
                  </details>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ===== 底部 ===== */}
      <footer className="print:hidden border-t border-white/10 py-8 px-4 text-center text-gray-500 text-sm">
        <p>© 2026 算个题吧 · 免费好用的数学练习卷生成器</p>
      </footer>

      {/* 使用指南 */}
      <div className="print:hidden max-w-4xl mx-auto px-4 py-12">
        <ToolGuide {...toolGuides['math-worksheet']} />
      </div>

      {/* 打印样式 */}
      <style jsx global>{`
        @page {
          size: A4 portrait;
          margin: 0;
        }
        @media print {
          * {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
          }
          html, body {
            margin: 0 !important;
            padding: 0 !important;
            background: white !important;
            height: auto !important;
            overflow: visible !important;
          }
          body > * {
            display: none !important;
          }
          .print\:block {
            display: block !important;
          }
          nav, footer, .no-print {
            display: none !important;
          }
          .worksheet-wrapper {
            display: block !important;
            position: static !important;
            background: white !important;
          }
          .worksheet-wrapper > * {
            display: block !important;
          }
          /* 每页分页控制 */
          .worksheet-page {
            page-break-after: always;
            break-after: page;
            height: auto !important;
            min-height: 100vh;
          }
          .worksheet-page:last-child {
            page-break-after: auto;
            break-after: auto;
          }
        }
      `}</style>
    </div>
  );
}
