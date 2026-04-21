'use client';

import { useState, useEffect, useCallback, useRef } from 'react';

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
  // Fill grid with backtracking
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

  const removals: Record<Difficulty, number> = { easy: 35, medium: 45, hard: 54 };
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

  const checkErrors = (g: Grid, er: Set<string>) => {
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
    er !== undefined && setErrors(ne);
    return ne;
  };

  const placeNumber = (num: number) => {
    if (!selected || !isPlaying) return;
    const [r, c] = selected;
    if (puzzle[r][c] !== null) return;

    const newGrid = userGrid.map(row => [...row]);
    const newNotes = notes.map(row => row.map(cell => [...cell]));

    if (notesMode) {
      newNotes[r][c][num] = !newNotes[r][c][num];
      setNotes(newNotes);
    } else {
      newGrid[r][c] = num;
      newNotes[r][c].fill(false);
      setUserGrid(newGrid);
      const ne = checkErrors(newGrid, errors);

      if (newGrid.every(row => row.every(cell => cell !== null)) && ne.size === 0) {
        setIsWon(true);
        setIsPlaying(false);
      }
    }
  };

  const eraseCell = () => {
    if (!selected || !isPlaying) return;
    const [r, c] = selected;
    if (puzzle[r][c] !== null) return;
    const newGrid = userGrid.map(row => [...row]);
    newGrid[r][c] = null;
    setUserGrid(newGrid);
    setErrors(new Set());
  };

  const getCellValue = (r: number, c: number) => {
    if (showSolution) return solution[r][c];
    return userGrid[r][c];
  };

  const isGiven = (r: number, c: number) => puzzle[r][c] !== null;

  const isHighlighted = (r: number, c: number) => {
    if (!selected) return false;
    const [sr, sc] = selected;
    return r === sr || c === sc || (Math.floor(r / 3) === Math.floor(sr / 3) && Math.floor(c / 3) === Math.floor(sc / 3));
  };

  const getCellErrors = (r: number, c: number) => errors.has(`${r}-${c}`);

  // Handle empty state during SSR
  if (puzzle.length === 0) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] text-white flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center text-2xl mx-auto mb-4">🧮</div>
          <p className="text-gray-400">加载中...</p>
        </div>
      </div>
    );
  }

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
            <a href="/tools/calligraphy" className="text-sm text-gray-400 hover:text-white transition-colors">字帖生成器</a>
            <a href="/" className="text-sm text-gray-400 hover:text-white transition-colors">数学练习卷</a>
          </div>
        </div>
      </nav>

      <div className="pt-24 pb-16 px-4">
        <div className="max-w-lg mx-auto">
          {/* Hero */}
          <div className="text-center mb-6">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent mb-2">
              数独游戏
            </h1>
            <p className="text-gray-400 text-sm">填入 1-9，使每行、每列、每宫格都含 1-9</p>
          </div>

          {/* Win banner */}
          {isWon && (
            <div className="bg-green-500/20 border border-green-500/40 rounded-2xl p-4 mb-4 text-center">
              <p className="text-green-400 text-xl font-bold mb-1">🎉 恭喜通关！</p>
              <p className="text-gray-400 text-sm">用时 {fmtTime(timer)}</p>
            </div>
          )}

          {/* Top bar */}
          <div className="flex items-center justify-between mb-4 bg-[#111] rounded-xl border border-white/10 px-4 py-3">
            <div className="flex gap-2">
              {(['easy', 'medium', 'hard'] as Difficulty[]).map(d => (
                <button
                  key={d}
                  onClick={() => { setDifficulty(d); }}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                    difficulty === d ? 'bg-blue-500/30 text-blue-300 border border-blue-500/50' : 'text-gray-400 hover:text-white border border-transparent'
                  }`}
                >
                  {{ easy: '简单', medium: '中等', hard: '困难' }[d]}
                </button>
              ))}
            </div>
            <div className="text-gray-400 text-sm font-mono">{fmtTime(timer)}</div>
          </div>

          {/* Grid */}
          <div className="bg-[#111] rounded-2xl border border-white/10 p-4 mb-4">
            <div className="inline-grid gap-[2px]" style={{ gridTemplateColumns: 'repeat(9, 1fr)' }}>
              {Array.from({ length: 81 }, (_, idx) => {
                const r = Math.floor(idx / 9), c = idx % 9;
                const val = getCellValue(r, c);
                const given = isGiven(r, c);
                const sel = selected && selected[0] === r && selected[1] === c;
                const hl = isHighlighted(r, c);
                const err = getCellErrors(r, c);
                const cellNotes = notes[r][c];
                const hasNotes = cellNotes.some(n => n);

                return (
                  <button
                    key={idx}
                    onClick={() => setSelected([r, c])}
                    className={`
                      w-9 h-9 sm:w-10 sm:h-10 flex items-center justify-center text-sm font-medium transition-colors
                      relative
                      ${sel ? 'bg-blue-500/60 text-white z-10' : hl ? 'bg-white/10 text-white' : 'bg-[#0d0d0d] text-gray-200'}
                      ${err ? 'text-red-400' : ''}
                      ${given && !sel ? 'font-bold text-white' : ''}
                      border border-transparent
                      ${c === 2 || c === 5 ? 'border-r-2 border-r-gray-600' : ''}
                      ${r === 2 || r === 5 ? 'border-b-2 border-b-gray-600' : ''}
                    `}
                  >
                    {val !== null ? (
                      <span className={`${given ? '' : 'text-blue-300'}`}>{val}</span>
                    ) : hasNotes ? (
                      <div className="grid grid-cols-3 gap-px w-full h-full p-0.5">
                        {Array.from({ length: 9 }, (_, ni) => (
                          <span key={ni} className={`text-[7px] text-center leading-none ${cellNotes[ni + 1] ? 'text-gray-500' : 'text-transparent'}`}>
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

          {/* Number pad */}
          <div className="grid grid-cols-5 gap-2 mb-4">
            {[1, 2, 3, 4, 5, 6, 7, 8, 9].map(n => (
              <button
                key={n}
                onClick={() => placeNumber(n)}
                className="py-3 rounded-xl bg-[#111] border border-white/10 text-lg font-medium text-gray-200 hover:bg-white/10 hover:border-white/30 active:scale-95 transition-all"
              >
                {n}
              </button>
            ))}
            <button
              onClick={eraseCell}
              className="py-3 rounded-xl bg-[#111] border border-white/10 text-gray-400 hover:bg-white/10 hover:border-white/30 active:scale-95 transition-all flex items-center justify-center"
            >
              ✕
            </button>
            <button
              onClick={() => setNotesMode(m => !m)}
              className={`py-3 rounded-xl border text-sm font-medium transition-all flex items-center justify-center ${
                notesMode ? 'bg-yellow-500/20 border-yellow-500/50 text-yellow-300' : 'bg-[#111] border-white/10 text-gray-400 hover:bg-white/10'
              }`}
            >
              📝{notesMode ? ' 笔记关' : ' 笔记开'}
            </button>
          </div>

          {/* Actions */}
          <div className="flex gap-3">
            <button
              onClick={newGame}
              className="flex-1 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-medium transition-colors"
            >
              🔄 新游戏
            </button>
            <button
              onClick={() => { setShowSolution(s => !s); setIsPlaying(false); }}
              className="flex-1 py-3 rounded-xl bg-white/10 hover:bg-white/20 text-white font-medium transition-colors"
            >
              {showSolution ? '🙈 隐藏答案' : '💡 显示答案'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
