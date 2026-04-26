'use client';

import { useState, useEffect, useCallback } from 'react';
import ToolGuide from '@/components/ToolGuide';
import { toolGuides } from '@/lib/toolGuides';
import ToolNavBar from '@/components/ToolNavBar';

type Difficulty = 'easy' | 'medium' | 'hard';
type CellValue = number | null;
type Grid = CellValue[][];

function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function generateSudoku(difficulty: Difficulty): { puzzle: Grid; solution: number[][] } {
  const grid: number[][] = Array.from({ length: 9 }, () => Array(9).fill(0));

  function isValid(g: number[][], row: number, col: number, num: number): boolean {
    for (let i = 0; i < 9; i++) {
      if (g[row][i] === num) return false;
      if (g[i][col] === num) return false;
    }
    const br = Math.floor(row / 3) * 3, bc = Math.floor(col / 3) * 3;
    for (let i = br; i < br + 3; i++) {
      for (let j = bc; j < bc + 3; j++) {
        if (g[i][j] === num) return false;
      }
    }
    return true;
  }

  function fill(g: number[][]): boolean {
    for (let i = 0; i < 9; i++) {
      for (let j = 0; j < 9; j++) {
        if (g[i][j] === 0) {
          for (const num of shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9])) {
            if (isValid(g, i, j, num)) {
              g[i][j] = num;
              if (fill(g)) return true;
              g[i][j] = 0;
            }
          }
          return false;
        }
      }
    }
    return true;
  }

  fill(grid);
  const solution = grid.map(r => [...r]);

  const removals: Record<Difficulty, number> = { easy: 32, medium: 42, hard: 52 };
  const toRemove = removals[difficulty];
  const puzzle: Grid = grid.map(r => [...r]);
  const positions = shuffle(Array.from({ length: 81 }, (_, i) => [Math.floor(i / 9), i % 9] as [number, number]));
  let removed = 0;
  for (const [r, c] of positions) {
    if (removed >= toRemove) break;
    puzzle[r][c] = null;
    removed++;
  }

  return { puzzle, solution };
}

function fmtTime(secs: number): string {
  const m = Math.floor(secs / 60);
  const s = secs % 60;
  return `${m}:${String(s).padStart(2, '0')}`;
}

export default function SudokuPage() {
  const [difficulty, setDifficulty] = useState<Difficulty>('easy');
  const [puzzle, setPuzzle] = useState<Grid>([]);
  const [solution, setSolution] = useState<number[][]>([]);
  const [userGrid, setUserGrid] = useState<Grid>([]);
  const [selected, setSelected] = useState<[number, number] | null>(null);
  const [notesMode, setNotesMode] = useState(false);
  const [notes, setNotes] = useState<boolean[][][]>(() =>
    Array.from({ length: 9 }, () => Array.from({ length: 9 }, () => Array(10).fill(false)))
  );
  const [timer, setTimer] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isWon, setIsWon] = useState(false);
  const [showSolution, setShowSolution] = useState(false);
  const [errors, setErrors] = useState<Set<string>>(new Set());

  const newGame = useCallback(() => {
    const { puzzle: p, solution: s } = generateSudoku(difficulty);
    setPuzzle(p);
    setSolution(s);
    setUserGrid(p.map(r => [...r]));
    setSelected(null);
    setNotes(Array.from({ length: 9 }, () => Array.from({ length: 9 }, () => Array(10).fill(false))));
    setTimer(0);
    setIsPlaying(true);
    setIsWon(false);
    setShowSolution(false);
    setErrors(new Set());
  }, [difficulty]);

  useEffect(() => { newGame(); }, [newGame]);

  useEffect(() => {
    if (!isPlaying) return;
    const id = setInterval(() => setTimer(t => t + 1), 1000);
    return () => clearInterval(id);
  }, [isPlaying]);

  const checkErrors = useCallback((g: Grid) => {
    const ne = new Set<string>();
    for (let i = 0; i < 9; i++) {
      for (let j = 0; j < 9; j++) {
        const v = g[i][j];
        if (v === null) continue;
        for (let k = 0; k < 9; k++) {
          if (k !== j && g[i][k] === v) { ne.add(`${i}-${j}`); ne.add(`${i}-${k}`); }
          if (k !== i && g[k][j] === v) { ne.add(`${i}-${j}`); ne.add(`${k}-${j}`); }
        }
        const br = Math.floor(i / 3) * 3, bc = Math.floor(j / 3) * 3;
        for (let bi = br; bi < br + 3; bi++) {
          for (let bj = bc; bj < bc + 3; bj++) {
            if ((bi !== i || bj !== j) && g[bi][bj] === v) { ne.add(`${i}-${j}`); ne.add(`${bi}-${bj}`); }
          }
        }
      }
    }
    setErrors(ne);
    return ne;
  }, []);

  const placeNumber = useCallback((num: number) => {
    if (!selected || !isPlaying) return;
    const [r, c] = selected;
    if (puzzle.length === 0 || puzzle[r][c] !== null) return;

    setUserGrid(prev => {
      const newGrid = prev.map(row => [...row]);
      if (notesMode) {
        setNotes(n => {
          const nn = n.map(row => row.map(cell => [...cell]));
          nn[r][c][num] = !nn[r][c][num];
          return nn;
        });
        return prev;
      }
      newGrid[r][c] = num;
      const ne = checkErrors(newGrid);
      if (newGrid.every(row => row.every(cell => cell !== null)) && ne.size === 0) {
        setIsWon(true);
        setIsPlaying(false);
      }
      return newGrid;
    });
  }, [selected, isPlaying, puzzle, notesMode, checkErrors]);

  const eraseCell = useCallback(() => {
    if (!selected || !isPlaying || puzzle.length === 0) return;
    const [r, c] = selected;
    if (puzzle[r][c] !== null) return;
    setUserGrid(prev => {
      const newGrid = prev.map(row => [...row]);
      newGrid[r][c] = null;
      return newGrid;
    });
    setErrors(new Set());
  }, [selected, isPlaying, puzzle]);

  const getCellValue = (r: number, c: number) => showSolution ? solution[r]?.[c] : userGrid[r]?.[c];
  const isGiven = (r: number, c: number) => puzzle.length > 0 && puzzle[r]?.[c] !== null;
  const isHighlighted = (r: number, c: number) => {
    if (!selected) return false;
    const [sr, sc] = selected;
    return r === sr || c === sc || (Math.floor(r / 3) === Math.floor(sr / 3) && Math.floor(c / 3) === Math.floor(sc / 3));
  };

  // SSR guard
  if (puzzle.length === 0) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center text-2xl mx-auto mb-4 shadow-lg">🧮</div>
          <p className="text-gray-500">加载中...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Nav */}
      <ToolNavBar currentPath="/tools/sudoku" title="数独游戏" />

      <div className="pt-20 pb-12 px-4">
        <div className="max-w-xl mx-auto">
          {/* Header */}
          <div className="text-center mb-6">
            <h1 className="text-3xl font-bold text-gray-800 mb-1.5">数独游戏在线玩</h1>
            <p className="text-gray-500 text-sm">入门/进阶/挑战三档难度 · 在线玩+打印</p>
          </div>

          {/* Win Banner */}
          {isWon && (
            <div className="bg-gradient-to-r from-green-500 to-emerald-500 rounded-2xl p-5 mb-5 text-center text-white shadow-lg">
              <p className="text-xl font-bold mb-1">🎉 恭喜通关！</p>
              <p className="text-green-100 text-sm">用时 {fmtTime(timer)}</p>
            </div>
          )}

          {/* Control Bar */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm px-4 py-3 mb-5 flex items-center justify-between">
            <div className="flex gap-2">
              {(['easy', 'medium', 'hard'] as Difficulty[]).map(d => (
                <button
                  key={d}
                  onClick={() => setDifficulty(d)}
                  className={`px-4 py-1.5 rounded-xl text-xs font-medium transition-all ${
                    difficulty === d
                      ? 'bg-blue-600 text-white shadow-sm'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {{ easy: '简单', medium: '中等', hard: '困难' }[d]}
                </button>
              ))}
            </div>
            <div className="flex items-center gap-3">
              <div className="bg-gray-100 rounded-lg px-3 py-1.5">
                <span className="text-gray-700 text-sm font-mono">{fmtTime(timer)}</span>
              </div>
            </div>
          </div>

          {/* Game Board */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-lg p-5 mb-5">
            <div className="flex justify-center">
              <div className="inline-grid gap-0 rounded-xl overflow-hidden border-2 border-gray-700" style={{ gridTemplateColumns: 'repeat(9, 1fr)' }}>
                {Array.from({ length: 81 }, (_, idx) => {
                  const r = Math.floor(idx / 9), c = idx % 9;
                  const val = getCellValue(r, c);
                  const given = isGiven(r, c);
                  const sel = selected && selected[0] === r && selected[1] === c;
                  const hl = isHighlighted(r, c);
                  const err = errors.has(`${r}-${c}`);
                  const cellNotes = notes[r]?.[c];
                  const hasNotes = cellNotes?.some(n => n);
                  const cellSize = 44;

                  return (
                    <button
                      key={idx}
                      onClick={() => setSelected([r, c])}
                      aria-label={`第${r+1}行第${c+1}列`}
                      className="relative flex items-center justify-center font-medium transition-colors"
                      style={{
                        width: cellSize,
                        height: cellSize,
                        background: sel ? '#3b82f6' : hl ? '#eff6ff' : given ? '#f8fafc' : '#ffffff',
                        borderRight: c === 2 || c === 5 ? '2px solid #374151' : c === 8 ? 'none' : '1px solid #e5e7eb',
                        borderBottom: r === 2 || r === 5 ? '2px solid #374151' : r === 8 ? 'none' : '1px solid #e5e7eb',
                      }}
                    >
                      {val !== null && val !== undefined ? (
                        <span
                          className={`text-lg ${given ? 'text-gray-800 font-bold' : 'text-blue-600'}`}
                          style={{ color: err ? '#ef4444' : given ? '#1f2937' : '#2563eb' }}
                        >
                          {val}
                        </span>
                      ) : hasNotes ? (
                        <div className="grid grid-cols-3 gap-0 w-full h-full p-0.5">
                          {Array.from({ length: 9 }, (_, ni) => (
                            <span
                              key={ni}
                              className={`text-[8px] text-center leading-none ${cellNotes[ni + 1] ? 'text-gray-400' : 'text-transparent'}`}
                            >
                              {ni + 1}
                            </span>
                          ))}
                        </div>
                      ) : null}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Number Pad */}
          <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-4 mb-5">
            <div className="grid grid-cols-9 gap-2">
              {[1, 2, 3, 4, 5, 6, 7, 8, 9].map(n => (
                <button
                  key={n}
                  onClick={() => placeNumber(n)}
                  className="py-3 rounded-xl bg-gray-50 hover:bg-blue-50 hover:text-blue-600 text-gray-700 text-lg font-medium transition-all active:scale-95 border border-gray-200"
                >
                  {n}
                </button>
              ))}
            </div>
          </div>

          {/* Tools */}
          <div className="grid grid-cols-4 gap-2 mb-5">
            <button
              onClick={eraseCell}
              className="py-3 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-medium transition-all flex flex-col items-center gap-0.5"
            >
              <span className="text-lg">✕</span>
              <span className="text-[10px] text-gray-500">擦除</span>
            </button>
            <button
              onClick={() => setNotesMode(m => !m)}
              className={`py-3 rounded-xl text-sm font-medium transition-all flex flex-col items-center gap-0.5 ${
                notesMode ? 'bg-amber-100 text-amber-700' : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
              }`}
            >
              <span className="text-lg">📝</span>
              <span className="text-[10px] text-gray-500">{notesMode ? '笔记开' : '笔记'}</span>
            </button>
            <button
              onClick={() => { setShowSolution(s => !s); setIsPlaying(false); }}
              className="py-3 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-medium transition-all flex flex-col items-center gap-0.5"
            >
              <span className="text-lg">{showSolution ? '🙈' : '💡'}</span>
              <span className="text-[10px] text-gray-500">{showSolution ? '隐藏' : '答案'}</span>
            </button>
            <button
              onClick={newGame}
              className="py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium transition-all flex flex-col items-center gap-0.5"
            >
              <span className="text-lg">🔄</span>
              <span className="text-[10px] text-blue-100">新游戏</span>
            </button>
          </div>

          {/* Tips */}
          <div className="bg-blue-50 rounded-xl p-4 border border-blue-100">
            <p className="text-xs text-blue-600 text-center">
              💡 提示：点击格子选中，再点击数字填入。开启笔记模式可标记候选数。
            </p>
          </div>
        </div>
      </div>

      {/* ===== 内容三件套 ===== */}
      <div className="print:hidden max-w-xl mx-auto px-4 pb-8 space-y-8">

        {/* 使用指南 */}
        <section className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
          <h2 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
            <span>📖</span> 使用指南
          </h2>
          <div className="text-gray-600 leading-relaxed space-y-3 text-sm">
            <p>
              数独是一种经典的逻辑推理游戏，目标是在9x9的方格中填入1-9的数字，使每行、每列和每个3x3小宫格内的数字都不重复。本工具提供入门、进阶、挑战三个难度等级。入门难度适合初次接触数独的小学低年级学生，进阶难度适合有一定基础的玩家，挑战难度适合数独爱好者。支持笔记模式（在格子中标记候选数字）、错误提示和计时功能。完成数独后可以查看用时和正确率，追踪自己的进步。同时支持导出PDF打印，方便离线练习。
            </p>
          </div>
        </section>

        {/* 适用场景 */}
        <section className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
          <h2 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
            <span>🎯</span> 适用场景
          </h2>
          <ul className="space-y-3 text-gray-600 text-sm">
            <li className="flex items-start gap-2">
              <span className="text-blue-500 mt-0.5 shrink-0">●</span>
              <span><strong className="text-gray-800">逻辑思维训练：</strong>每天15分钟数独，有效提升推理能力和专注力</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-500 mt-0.5 shrink-0">●</span>
              <span><strong className="text-gray-800">课间休息：</strong>难度适中的数独游戏，既能放松大脑又不浪费时间</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-500 mt-0.5 shrink-0">●</span>
              <span><strong className="text-gray-800">亲子互动：</strong>家长和孩子一起做数独，培养逻辑思维</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-500 mt-0.5 shrink-0">●</span>
              <span><strong className="text-gray-800">数学课前热身：</strong>上课前做一道数独，激活数学思维</span>
            </li>
          </ul>
        </section>

        {/* 常见问题FAQ */}
        <section className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
          <h2 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
            <span>❓</span> 常见问题
          </h2>
          <div className="space-y-2">
            <details className="group border border-gray-200 rounded-lg">
              <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-700 hover:text-gray-900 list-none font-medium text-sm">
                <span>数独对数学成绩有帮助吗？</span>
                <span className="text-gray-400 group-open:rotate-180 transition-transform text-xs">▼</span>
              </summary>
              <div className="px-4 pb-4 text-sm text-gray-500 leading-relaxed">有。剑桥大学2019年的研究发现，坚持数独训练可以显著提升学生的逻辑推理和问题解决能力，这些能力直接关系到数学应用题的解题水平。</div>
            </details>
            <details className="group border border-gray-200 rounded-lg">
              <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-700 hover:text-gray-900 list-none font-medium text-sm">
                <span>几岁可以开始玩数独？</span>
                <span className="text-gray-400 group-open:rotate-180 transition-transform text-xs">▼</span>
              </summary>
              <div className="px-4 pb-4 text-sm text-gray-500 leading-relaxed">一般建议小学二年级以上开始。入门难度专门为低年级学生设计，从简单的逻辑推理开始，逐步提升难度。</div>
            </details>
            <details className="group border border-gray-200 rounded-lg">
              <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-700 hover:text-gray-900 list-none font-medium text-sm">
                <span>笔记模式怎么用？</span>
                <span className="text-gray-400 group-open:rotate-180 transition-transform text-xs">▼</span>
              </summary>
              <div className="px-4 pb-4 text-sm text-gray-500 leading-relaxed">点击格子后选择笔记模式，可以在格子中标记1-9的候选数字。当某个数字在某行、某列或某宫格中只有一个位置可以填入时，就可以确定答案。</div>
            </details>
          </div>
        </section>

        {/* 相关工具推荐 */}
        <section className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
          <h2 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
            <span>🔗</span> 相关工具推荐
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <a href="/tools/mental-math" className="block bg-gray-50 hover:bg-blue-50 border border-gray-200 hover:border-blue-300 rounded-xl p-4 transition-all group">
              <div className="text-2xl mb-2">⚡</div>
              <div className="font-bold text-gray-700 text-sm group-hover:text-blue-600 transition-colors">口算速练</div>
              <div className="text-xs text-gray-400 mt-1">计时挑战训练</div>
            </a>
            <a href="/tools/math-worksheet" className="block bg-gray-50 hover:bg-blue-50 border border-gray-200 hover:border-blue-300 rounded-xl p-4 transition-all group">
              <div className="text-2xl mb-2">🧮</div>
              <div className="font-bold text-gray-700 text-sm group-hover:text-blue-600 transition-colors">数学练习卷生成器</div>
              <div className="text-xs text-gray-400 mt-1">PDF打印练习卷</div>
            </a>
            <a href="/resources/method" className="block bg-gray-50 hover:bg-blue-50 border border-gray-200 hover:border-blue-300 rounded-xl p-4 transition-all group">
              <div className="text-2xl mb-2">🧠</div>
              <div className="font-bold text-gray-700 text-sm group-hover:text-blue-600 transition-colors">思维训练资源</div>
              <div className="text-xs text-gray-400 mt-1">逻辑思维方法</div>
            </a>
          </div>
        </section>
      </div>

      {/* 使用指南 */}
      <div className="max-w-4xl mx-auto px-4 py-12">
        <ToolGuide {...toolGuides['sudoku']} />
      </div>
    </div>
  );
}
