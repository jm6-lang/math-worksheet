'use client';

import { useState, useRef, useCallback, useEffect } from 'react';
import ToolNavBar from '@/components/ToolNavBar';
import { exportToPDF } from '@/lib/pdfExport';
import {
  unitTestData,
  getUnitsByGradeAndSemester,
  getRandomQuestions,
  type UnitQuestion,
} from '@/lib/unitTestData';

// ===== 类型定义 =====
type ExamType = 'unit' | 'midterm' | 'final';
type Difficulty = 1 | 2 | 3;

interface SelectedQuestion {
  type: string;
  content: string;
  answer: string;
  difficulty: 1 | 2 | 3;
  unitName: string;
}

// ===== 配置常量 =====
const GRADES = [1, 2, 3, 4, 5, 6];
const SEMESTERS: { value: '上' | '下'; label: string }[] = [
  { value: '上', label: '上册' },
  { value: '下', label: '下册' },
];
const EXAM_TYPES: { value: ExamType; label: string; icon: string }[] = [
  { value: 'unit', label: '单元测试', icon: '📝' },
  { value: 'midterm', label: '期中测试', icon: '📋' },
  { value: 'final', label: '期末测试', icon: '📊' },
];
const DIFFICULTY_OPTIONS: { value: Difficulty; label: string; icon: string; desc: string }[] = [
  { value: 1, label: '基础', icon: '🌱', desc: '基础概念' },
  { value: 2, label: '中等', icon: '🌿', desc: '综合运用' },
  { value: 3, label: '提高', icon: '🌳', desc: '拓展提升' },
];
const COUNT_OPTIONS = [10, 20, 40, 60, 80];

const DIFFICULTY_LABEL: Record<Difficulty, string> = {
  1: '基础',
  2: '中等',
  3: '提高',
};

// ===== 题型排序映射 =====
const TYPE_ORDER: Record<string, number> = {
  '填空题': 1,
  '选择题': 2,
  '判断题': 3,
  '比较大小': 4,
  '计算题': 5,
  '竖式计算': 6,
  '估算题': 7,
  '应用题': 8,
};

// ===== 工具函数 =====
function getExamTitle(
  grade: number,
  semester: '上' | '下',
  examType: ExamType,
  unitNames: string[],
  subjectName?: string,
): string {
  const gradeLabel = `${grade}年级${semester}册`;
  const subjectStr = subjectName ? ` ${subjectName}` : '';
  switch (examType) {
    case 'unit':
      return `${gradeLabel}${subjectStr} ${unitNames.length > 0 ? unitNames[0] : ''}测试卷`;
    case 'midterm':
      return `${gradeLabel}${subjectStr} 期中测试卷`;
    case 'final':
      return `${gradeLabel}${subjectStr} 期末测试卷`;
  }
}

function shuffleArray<T>(arr: T[]): T[] {
  const shuffled = [...arr];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

// ===== 主组件 =====
export default function UnitTestPage() {
  // 配置状态
  const [subject, setSubject] = useState<'数学' | '语文' | '英语' | '科学'>('数学');
  const [grade, setGrade] = useState(1);
  const [semester, setSemester] = useState<'上' | '下'>('上');
  const [selectedUnits, setSelectedUnits] = useState<string[]>([]);
  const [examType, setExamType] = useState<ExamType>('unit');
  const [difficulty, setDifficulty] = useState<Difficulty>(1);
  const [questionCount, setQuestionCount] = useState(15);

  // 生成状态
  const [questions, setQuestions] = useState<SelectedQuestion[]>([]);
  const [hasGenerated, setHasGenerated] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [showAnswers, setShowAnswers] = useState(false);

  const previewRef = useRef<HTMLDivElement>(null);

  // 获取当前年级学期的可用单元（按科目过滤）
  const availableUnits = getUnitsByGradeAndSemester(grade, semester, subject);

  // 年级或学期变化时重置单元选择
  useEffect(() => {
    setSelectedUnits([]);
  }, [grade, semester]);

  // 根据试卷类型自动选择单元
  const getAutoUnitIds = useCallback((): string[] => {
    const units = availableUnits;
    if (examType === 'unit') {
      return selectedUnits.length > 0 ? selectedUnits : [];
    }
    if (examType === 'midterm') {
      // 期中：前一半单元
      const half = Math.ceil(units.length / 2);
      return units.slice(0, half).map(u => u.id);
    }
    if (examType === 'final') {
      // 期末：所有单元
      return units.map(u => u.id);
    }
    return [];
  }, [availableUnits, examType, selectedUnits]);

  // 切换单元选择
  const toggleUnit = (unitId: string) => {
    setSelectedUnits(prev =>
      prev.includes(unitId) ? prev.filter(id => id !== unitId) : [...prev, unitId],
    );
  };

  // 生成试卷
  const handleGenerate = useCallback(() => {
    setIsGenerating(true);
    setHasGenerated(false);

    setTimeout(() => {
      const unitIds = getAutoUnitIds();
      if (unitIds.length === 0) {
        alert('请至少选择一个单元');
        setIsGenerating(false);
        return;
      }

      const qs = getRandomQuestions(unitIds, questionCount, difficulty);
      setQuestions(qs);
      setHasGenerated(true);
      setIsGenerating(false);
      setShowAnswers(false);
    }, 100);
  }, [getAutoUnitIds, questionCount, difficulty]);

  // 导出 PDF
  const handleExportPDF = useCallback(async () => {
    if (!previewRef.current) return;
    try {
      const title = getExamTitle(grade, semester, examType, availableUnits.filter(u => selectedUnits.includes(u.id)).map(u => u.unitName), subject);
      await exportToPDF(previewRef.current, `${title}.pdf`);
    } catch (err) {
      console.error(err);
      alert('PDF导出失败，请重试');
    }
  }, [grade, semester, examType, selectedUnits, availableUnits, subject]);

  // 打印
  const handlePrint = useCallback(() => {
    const printWindow = window.open('', '_blank');
    if (!printWindow || !previewRef.current) return;
    const title = getExamTitle(grade, semester, examType, availableUnits.filter(u => selectedUnits.includes(u.id)).map(u => u.unitName), subject);
    const content = previewRef.current.innerHTML;
    printWindow.document.write(`<!DOCTYPE html><html><head><meta charset="utf-8"><title>${title}</title><style>@page{margin:10mm;size:A4 portrait;}body{margin:0;font-family:'Microsoft YaHei','SimSun',sans-serif;color:#000;}@media print{body{-webkit-print-color-adjust:exact;print-color-adjust:exact;}}</style></head><body>${content}<p style="text-align:center;color:#999;font-size:12px;margin-top:20px;">来源：教材工具箱 | 免费下载：www.skillxm.cn</p></body></html>`);
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    printWindow.close();
  }, [grade, semester, examType, selectedUnits, availableUnits, subject]);

  // 按题型分组
  const groupedQuestions = questions.reduce<Record<string, SelectedQuestion[]>>((acc, q) => {
    if (!acc[q.type]) acc[q.type] = [];
    acc[q.type].push(q);
    return acc;
  }, {});

  // 按题型排序
  const sortedTypes = Object.keys(groupedQuestions).sort(
    (a, b) => (TYPE_ORDER[a] ?? 99) - (TYPE_ORDER[b] ?? 99),
  );

  // 试卷标题
  const examTitle = hasGenerated
    ? getExamTitle(
        grade,
        semester,
        examType,
        availableUnits.filter(u => {
          const ids = getAutoUnitIds();
          return ids.includes(u.id);
        }).map(u => u.unitName),
        subject,
      )
    : '';

  // 滚动到预览区
  useEffect(() => {
    if (hasGenerated) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }, [hasGenerated]);

  return (
    <div className="min-h-screen bg-[#0f0f0f] text-white" style={{ fontFamily: '"Noto Sans SC", "Microsoft YaHei", sans-serif' }}>

      {/* ===== 顶部导航 ===== */}
      <ToolNavBar currentPath="/tools/unit-test" title="单元测试卷" />

      {/* ===== Hero 区域 ===== */}
      {!hasGenerated && (
        <div className="print:hidden pt-24 pb-12 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl sm:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent">
              单元测试卷生成器
            </h1>
            <p className="text-xl text-gray-400 mb-10">
              按教材单元出题 · 覆盖人教版1-6年级上下册 · 支持数学/语文/英语/科学四科 · 期中/期末/单元测试 · PDF即印即用
            </p>
          </div>
        </div>
      )}

      {/* ===== 配置面板 ===== */}
      <div className={`print:hidden ${hasGenerated ? 'pt-20' : ''} px-4 pb-12`}>
        <div className="max-w-6xl mx-auto">
          <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

              {/* 科目选择 */}
              <div>
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <span className="w-6 h-6 bg-blue-500 rounded-full text-xs flex items-center justify-center">1</span>
                  选择科目
                </h3>
                <div className="flex flex-wrap gap-2">
                  {(['数学', '语文', '英语', '科学'] as const).map(s => (
                    <button
                      key={s}
                      onClick={() => { setSubject(s); setSelectedUnits([]); setQuestions([]); setHasGenerated(false); }}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                        subject === s
                          ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/20'
                          : 'bg-white/10 text-gray-300 hover:bg-white/20'
                      }`}
                    >
                      {s === '数学' ? '🧮' : s === '语文' ? '📖' : s === '英语' ? '🔤' : '🔬'} {s}
                    </button>
                  ))}
                </div>
              </div>

              {/* 年级选择 */}
              <div>
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <span className="w-6 h-6 bg-blue-500 rounded-full text-xs flex items-center justify-center">2</span>
                  选择年级
                </h3>
                <div className="flex flex-wrap gap-2">
                  {GRADES.map(g => (
                    <button
                      key={g}
                      onClick={() => setGrade(g)}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
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

              {/* 学期选择 */}
              <div>
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <span className="w-6 h-6 bg-blue-500 rounded-full text-xs flex items-center justify-center">3</span>
                  选择学期
                </h3>
                <div className="flex gap-2">
                  {SEMESTERS.map(s => (
                    <button
                      key={s.value}
                      onClick={() => setSemester(s.value)}
                      className={`flex-1 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                        semester === s.value
                          ? 'bg-blue-500 text-white'
                          : 'bg-white/10 text-gray-300 hover:bg-white/20'
                      }`}
                    >
                      {s.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* 单元选择 */}
              <div>
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <span className="w-6 h-6 bg-blue-500 rounded-full text-xs flex items-center justify-center">4</span>
                  选择单元
                </h3>
                {availableUnits.length === 0 ? (
                  <p className="text-gray-500 text-sm">暂无该科目的单元数据</p>
                ) : (
                  <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto">
                    {availableUnits.map(u => (
                      <button
                        key={u.id}
                        onClick={() => toggleUnit(u.id)}
                        disabled={examType !== 'unit'}
                        className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                          examType !== 'unit'
                            ? 'bg-white/5 text-gray-600 cursor-not-allowed'
                            : selectedUnits.includes(u.id)
                              ? 'bg-blue-500 text-white'
                              : 'bg-white/10 text-gray-300 hover:bg-white/20'
                        }`}
                      >
                        {u.unitName}
                      </button>
                    ))}
                  </div>
                )}
                {examType !== 'unit' && (
                  <p className="text-gray-500 text-xs mt-2">
                    {examType === 'midterm' ? '期中测试自动选取前半单元' : '期末测试自动选取全部单元'}
                  </p>
                )}
              </div>

              {/* 试卷类型 */}
              <div>
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <span className="w-6 h-6 bg-blue-500 rounded-full text-xs flex items-center justify-center">5</span>
                  试卷类型
                </h3>
                <div className="grid grid-cols-3 gap-2">
                  {EXAM_TYPES.map(t => (
                    <button
                      key={t.value}
                      onClick={() => setExamType(t.value)}
                      className={`px-3 py-3 rounded-xl text-sm font-medium transition-all text-center ${
                        examType === t.value
                          ? 'bg-blue-500 text-white'
                          : 'bg-white/10 text-gray-300 hover:bg-white/20'
                      }`}
                    >
                      <div className="text-xl mb-1">{t.icon}</div>
                      <div>{t.label}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* 难度选择 */}
              <div>
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <span className="w-6 h-6 bg-blue-500 rounded-full text-xs flex items-center justify-center">6</span>
                  难度选择
                </h3>
                <div className="flex gap-2">
                  {DIFFICULTY_OPTIONS.map(d => (
                    <button
                      key={d.value}
                      onClick={() => setDifficulty(d.value)}
                      className={`flex-1 px-3 py-3 rounded-xl text-sm font-medium transition-all text-center ${
                        difficulty === d.value
                          ? 'bg-blue-500 text-white'
                          : 'bg-white/10 text-gray-300 hover:bg-white/20'
                      }`}
                    >
                      <div className="text-xl mb-1">{d.icon}</div>
                      <div>{d.label}</div>
                      <div className="text-xs opacity-60">{d.desc}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* 题目数量 + 生成按钮 */}
              <div>
                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                  <span className="w-6 h-6 bg-blue-500 rounded-full text-xs flex items-center justify-center">7</span>
                  题目数量
                </h3>
                <div className="flex gap-2 mb-4">
                  {COUNT_OPTIONS.map(c => (
                    <button
                      key={c}
                      onClick={() => setQuestionCount(c)}
                      className={`flex-1 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                        questionCount === c
                          ? 'bg-blue-500 text-white'
                          : 'bg-white/10 text-gray-300 hover:bg-white/20'
                      }`}
                    >
                      {c}题
                    </button>
                  ))}
                </div>
                <button
                  onClick={handleGenerate}
                  disabled={isGenerating || (examType === 'unit' && selectedUnits.length === 0)}
                  className="w-full py-3 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 disabled:opacity-50 text-white font-bold rounded-xl transition-all"
                >
                  {isGenerating ? '生成中...' : '生成试卷'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ===== 试卷预览 ===== */}
      {hasGenerated && (
        <div className="px-4 pb-20">
          <div className="max-w-4xl mx-auto">
            {/* 预览工具栏 */}
            <div className="print:hidden flex flex-wrap items-center justify-between mb-6 gap-4">
              <div className="flex items-center gap-4">
                <h2 className="text-2xl font-bold">试卷预览</h2>
                <span className="text-gray-500">共 {questions.length} 题</span>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setShowAnswers(!showAnswers)}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    showAnswers
                      ? 'bg-amber-500 text-white'
                      : 'bg-white/10 text-gray-300 hover:bg-white/20'
                  }`}
                >
                  {showAnswers ? '隐藏答案' : '显示答案'}
                </button>
                <button
                  onClick={handleExportPDF}
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-medium transition-colors"
                >
                  导出PDF
                </button>
                <button
                  onClick={handlePrint}
                  className="px-4 py-2 bg-white/10 hover:bg-white/20 text-gray-300 rounded-lg font-medium transition-colors"
                >
                  打印
                </button>
                <button
                  onClick={() => { setHasGenerated(false); setQuestions([]); }}
                  className="px-4 py-2 bg-white/10 hover:bg-white/20 text-gray-300 rounded-lg font-medium transition-all ml-2"
                >
                  返回配置
                </button>
              </div>
            </div>

            {/* A4 纸效果试卷 */}
            <div className="bg-white rounded-xl overflow-hidden shadow-2xl">
              <div ref={previewRef} className="bg-white text-black p-8 sm:p-12" style={{ minHeight: '1123px', width: '100%', maxWidth: '794px', margin: '0 auto' }}>
                {/* 试卷标题 */}
                <div className="text-center mb-8">
                  <h1 className="text-2xl font-bold mb-2">{examTitle}</h1>
                  <p className="text-sm text-gray-500">（人教版 · {DIFFICULTY_LABEL[difficulty]}难度）</p>
                </div>

                {/* 姓名班级等信息栏 */}
                <div className="flex justify-between mb-8 border-b border-gray-300 pb-4 text-sm">
                  <div className="flex-1">姓名：______________</div>
                  <div className="flex-1">班级：______________</div>
                  <div className="flex-1">日期：______________</div>
                  <div className="flex-1">分数：______________</div>
                </div>

                {/* 题目区域 */}
                <div className="space-y-8">
                  {sortedTypes.map((type, typeIdx) => {
                    const typeQuestions = groupedQuestions[type];
                    const chineseNum = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十'];
                    return (
                      <div key={type}>
                        <h2 className="text-lg font-bold mb-4 border-b border-gray-200 pb-2">
                          {chineseNum[typeIdx] ?? typeIdx}、{type}（共{typeQuestions.length}题）
                        </h2>
                        <div className="space-y-4">
                          {typeQuestions.map((q, qIdx) => (
                            <div key={qIdx} className="leading-relaxed">
                              <p className="text-sm whitespace-pre-line">
                                <span className="font-medium">{qIdx + 1}.</span> {q.content}
                              </p>
                              {showAnswers && (
                                <div className="mt-1 text-sm text-red-600 bg-red-50 px-2 py-1 rounded inline-block">
                                  答案：{q.answer}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </div>

                {/* 答案区（独立区域，可选显示） */}
                {showAnswers && (
                  <div className="mt-12 pt-8 border-t-2 border-gray-300">
                    <h2 className="text-lg font-bold mb-4 text-center">参考答案</h2>
                    <div className="space-y-3 text-sm">
                      {sortedTypes.map(type => {
                        const typeQuestions = groupedQuestions[type];
                        return (
                          <div key={type}>
                            <p className="font-bold text-gray-700 mb-1">{type}：</p>
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-1">
                              {typeQuestions.map((q, qIdx) => (
                                <p key={qIdx} className="text-gray-600">
                                  {qIdx + 1}. {q.answer}
                                </p>
                              ))}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ===== 内容三件套 ===== */}
      {!hasGenerated && (
        <div className="print:hidden px-4 pb-12">
          <div className="max-w-4xl mx-auto space-y-8">

            {/* 使用指南 */}
            <section className="bg-white/5 border border-white/10 rounded-2xl p-6 md:p-8">
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <span className="text-2xl">📖</span> 使用指南
              </h2>
              <div className="text-gray-400 leading-relaxed space-y-3 text-sm md:text-base">
                <p>
                  单元测试卷生成器按照人教版小学教材单元体系组织题库，支持数学、语文、英语、科学四个科目，覆盖一年级到六年级上下册。使用时先选择科目、年级和学期，系统会自动显示该学期的可用单元。选择单元后可以设定试卷类型（单元测试、期中测试或期末测试），期中和期末测试会自动选取对应范围内的单元。支持三档难度调节，题目数量可选10、20、40、60或80题，每次生成都会从题库中随机抽取，保证每次练习内容不重复。生成后可在线预览试卷效果，支持显示/隐藏答案，确认无误后一键导出PDF文件，A4纸打印效果清晰规范。
                </p>
                <p><strong className="text-gray-300">数学：</strong>涵盖计算题、填空题、选择题、判断题、比较大小、应用题等题型。低年级侧重加减法运算和基础概念，中年级引入乘除法、分数、面积等知识点，高年级覆盖小数、百分数、方程、几何等综合内容。每道计算题均自动生成，确保题目不重复。</p>
                <p><strong className="text-gray-300">语文：</strong>包含字词填空、选择题、判断题、句子改写、阅读理解等题型。题库紧密贴合人教版教材单元主题，涵盖生字词、成语、修辞手法、课文理解等核心考点，帮助学生巩固每单元的语文基础知识。</p>
                <p><strong className="text-gray-300">英语：</strong>提供单词选择、句型填空、情景交际、阅读理解等题型。题库按单元话题组织，涵盖字母、单词拼写、日常用语、语法结构等内容，适合小学生英语单元复习和阶段性检测。</p>
                <p><strong className="text-gray-300">科学：</strong>涵盖科学概念填空、判断题、选择题、简答题等题型。题库依据人教版科学教材单元编排，涉及生命科学、物质科学、地球与宇宙、技术与工程等领域，培养学生科学探究能力和基础知识掌握。</p>
              </div>
            </section>

            {/* 适用场景 */}
            <section className="bg-white/5 border border-white/10 rounded-2xl p-6 md:p-8">
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <span className="text-2xl">🎯</span> 适用场景
              </h2>
              <ul className="space-y-3 text-gray-400 text-sm md:text-base">
                <li className="flex items-start gap-2">
                  <span className="text-blue-400 mt-0.5 shrink-0">●</span>
                  <span><strong className="text-gray-300">单元复习检测：</strong>学完一个单元后，生成对应的单元测试卷检验学习效果</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-400 mt-0.5 shrink-0">●</span>
                  <span><strong className="text-gray-300">期中模拟考试：</strong>期中考试前生成模拟试卷，提前熟悉考试形式</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-400 mt-0.5 shrink-0">●</span>
                  <span><strong className="text-gray-300">期末总复习：</strong>期末考试前生成综合测试卷，覆盖所有单元知识点</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-400 mt-0.5 shrink-0">●</span>
                  <span><strong className="text-gray-300">分层教学布置：</strong>根据学生水平选择不同难度，实现分层作业布置</span>
                </li>
              </ul>
            </section>

            {/* 常见问题FAQ */}
            <section className="bg-white/5 border border-white/10 rounded-2xl p-6 md:p-8">
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <span className="text-2xl">❓</span> 常见问题
              </h2>
              <div className="space-y-2">
                <details className="group border border-white/10 rounded-lg">
                  <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-300 hover:text-white list-none font-medium">
                    <span>覆盖哪些教材版本？</span>
                    <span className="text-gray-500 group-open:rotate-180 transition-transform text-xs">▼</span>
                  </summary>
                  <div className="px-4 pb-4 text-sm text-gray-400 leading-relaxed">目前支持人教版小学数学、语文、英语、科学四个科目，覆盖一年级到三年级上下册共18个核心单元。后续将持续更新四年级到六年级的单元数据，并计划支持北师大版、苏教版等主流教材版本。</div>
                </details>
                <details className="group border border-white/10 rounded-lg">
                  <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-300 hover:text-white list-none font-medium">
                    <span>试卷难度如何划分？</span>
                    <span className="text-gray-500 group-open:rotate-180 transition-transform text-xs">▼</span>
                  </summary>
                  <div className="px-4 pb-4 text-sm text-gray-400 leading-relaxed">试卷分为三档难度：基础难度侧重基本概念和简单计算，适合课后巩固；中等难度侧重知识点的综合运用，适合单元检测；提高难度包含拓展思维题和综合应用题，适合培优训练。每道题目都标注了难度等级。</div>
                </details>
                <details className="group border border-white/10 rounded-lg">
                  <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-300 hover:text-white list-none font-medium">
                    <span>每次生成的题目一样吗？</span>
                    <span className="text-gray-500 group-open:rotate-180 transition-transform text-xs">▼</span>
                  </summary>
                  <div className="px-4 pb-4 text-sm text-gray-400 leading-relaxed">不会。每次点击生成按钮，系统都会从题库中随机抽取题目并打乱顺序。即使使用相同的配置参数，每次生成的试卷内容也不一样，确保练习的多样性和有效性。</div>
                </details>
                <details className="group border border-white/10 rounded-lg">
                  <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-300 hover:text-white list-none font-medium">
                    <span>可以打印吗？</span>
                    <span className="text-gray-500 group-open:rotate-180 transition-transform text-xs">▼</span>
                  </summary>
                  <div className="px-4 pb-4 text-sm text-gray-400 leading-relaxed">可以。支持导出为A4标准尺寸的PDF文件，排版规范清晰，可直接打印使用。也可以使用浏览器的打印功能直接打印预览。PDF文件带有来源水印，方便识别试卷出处。</div>
                </details>
                <details className="group border border-white/10 rounded-lg">
                  <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-300 hover:text-white list-none font-medium">
                    <span>支持哪些年级？</span>
                    <span className="text-gray-500 group-open:rotate-180 transition-transform text-xs">▼</span>
                  </summary>
                  <div className="px-4 pb-4 text-sm text-gray-400 leading-relaxed">覆盖小学一年级到六年级上下册，共12个学期的完整单元体系。每个年级每个学期都包含对应的教材单元数据，教师和家长可以根据实际教学进度灵活选择对应的年级和学期生成试卷。</div>
                </details>
                <details className="group border border-white/10 rounded-lg">
                  <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-300 hover:text-white list-none font-medium">
                    <span>期中/期末试卷怎么出？</span>
                    <span className="text-gray-500 group-open:rotate-180 transition-transform text-xs">▼</span>
                  </summary>
                  <div className="px-4 pb-4 text-sm text-gray-400 leading-relaxed">选择"期中测试"或"期末测试"试卷类型后，系统会自动选取对应学期范围内的单元。期中测试自动选取前半学期的所有单元，期末测试自动选取该学期的全部单元，无需手动逐个选择单元，一键即可生成综合性试卷。</div>
                </details>
                <details className="group border border-white/10 rounded-lg">
                  <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-300 hover:text-white list-none font-medium">
                    <span>可以混合不同单元的题目吗？</span>
                    <span className="text-gray-500 group-open:rotate-180 transition-transform text-xs">▼</span>
                  </summary>
                  <div className="px-4 pb-4 text-sm text-gray-400 leading-relaxed">可以。在单元测试模式下，您可以同时勾选多个单元，系统会从所有选中的单元中随机抽取题目组合成一份试卷。这样非常适合跨单元综合复习，帮助学生巩固多个单元的知识点。</div>
                </details>
                <details className="group border border-white/10 rounded-lg">
                  <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-300 hover:text-white list-none font-medium">
                    <span>试卷格式是什么样的？</span>
                    <span className="text-gray-500 group-open:rotate-180 transition-transform text-xs">▼</span>
                  </summary>
                  <div className="px-4 pb-4 text-sm text-gray-400 leading-relaxed">试卷采用A4标准纸张排版，包含完整的试卷标题、姓名、班级、日期、分数栏等信息栏。题目按题型自动分组排列（如填空题、选择题、计算题、应用题等），排版规范清晰，打印效果与正式考试试卷一致，可直接用于课堂测试或家庭练习。</div>
                </details>
              </div>
            </section>

            {/* 相关工具推荐 */}
            <section className="bg-white/5 border border-white/10 rounded-2xl p-6 md:p-8">
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <span className="text-2xl">🔗</span> 相关工具推荐
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                <a href="/tools/math-worksheet" className="block bg-white/5 hover:bg-white/10 border border-white/10 hover:border-blue-500/30 rounded-xl p-4 transition-all group">
                  <div className="text-2xl mb-2">📐</div>
                  <div className="font-bold text-gray-200 text-sm group-hover:text-white transition-colors">数学练习卷</div>
                  <div className="text-xs text-gray-500 mt-1">自由出题打印</div>
                </a>
                <a href="/tools/mental-math" className="block bg-white/5 hover:bg-white/10 border border-white/10 hover:border-blue-500/30 rounded-xl p-4 transition-all group">
                  <div className="text-2xl mb-2">⚡</div>
                  <div className="font-bold text-gray-200 text-sm group-hover:text-white transition-colors">口算速练</div>
                  <div className="text-xs text-gray-500 mt-1">计时挑战训练</div>
                </a>
                <a href="/tools/poem-memo" className="block bg-white/5 hover:bg-white/10 border border-white/10 hover:border-blue-500/30 rounded-xl p-4 transition-all group">
                  <div className="text-2xl mb-2">📜</div>
                  <div className="font-bold text-gray-200 text-sm group-hover:text-white transition-colors">古诗词默写</div>
                  <div className="text-xs text-gray-500 mt-1">古诗文默写生成</div>
                </a>
                <a href="/tools/calligraphy" className="block bg-white/5 hover:bg-white/10 border border-white/10 hover:border-blue-500/30 rounded-xl p-4 transition-all group">
                  <div className="text-2xl mb-2">✍️</div>
                  <div className="font-bold text-gray-200 text-sm group-hover:text-white transition-colors">字帖生成器</div>
                  <div className="text-xs text-gray-500 mt-1">汉字书写练习</div>
                </a>
              </div>
            </section>
          </div>
        </div>
      )}

      {/* ===== 底部 ===== */}
      <footer className="print:hidden border-t border-white/10 py-8 px-4 text-center text-gray-500 text-sm">
        <p>© 2026 教材工具箱 · 免费好用的单元测试卷生成器</p>
      </footer>

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
          .print\\:block {
            display: block !important;
          }
          nav, footer, .no-print {
            display: none !important;
          }
        }
      `}</style>
    </div>
  );
}
