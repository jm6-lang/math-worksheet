'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import ToolGuide from '@/components/ToolGuide';
import { toolGuides } from '@/lib/toolGuides';

// 难度配置
const DIFFICULTY_CONFIG = {
  easy: {
    label: '简单',
    icon: '🌱',
    color: 'from-green-500 to-emerald-600',
    operations: ['+', '-'],
    maxNum: 20,
    timeLimit: 60,
    description: '20以内加减法',
  },
  medium: {
    label: '中等',
    icon: '🌿',
    color: 'from-blue-500 to-indigo-600',
    operations: ['+', '-', '×'],
    maxNum: 50,
    timeLimit: 90,
    description: '50以内加减乘',
  },
  hard: {
    label: '困难',
    icon: '🌳',
    color: 'from-orange-500 to-red-600',
    operations: ['+', '-', '×', '÷'],
    maxNum: 100,
    timeLimit: 120,
    description: '100以内四则',
  },
  expert: {
    label: '专家',
    icon: '🏆',
    color: 'from-purple-500 to-pink-600',
    operations: ['+', '-', '×', '÷'],
    maxNum: 200,
    timeLimit: 180,
    description: '200以内四则',
  },
};

type Difficulty = keyof typeof DIFFICULTY_CONFIG;

interface Question {
  id: number;
  num1: number;
  num2: number;
  operation: string;
  answer: number;
  userAnswer: string;
  isCorrect: boolean | null;
  timeSpent: number;
}

// 生成题目
function generateQuestion(id: number, difficulty: Difficulty): Question {
  const config = DIFFICULTY_CONFIG[difficulty];
  const operation = config.operations[Math.floor(Math.random() * config.operations.length)];
  
  let num1: number, num2: number, answer: number;
  
  switch (operation) {
    case '+':
      num1 = Math.floor(Math.random() * config.maxNum) + 1;
      num2 = Math.floor(Math.random() * config.maxNum) + 1;
      answer = num1 + num2;
      break;
    case '-':
      num1 = Math.floor(Math.random() * config.maxNum) + 1;
      num2 = Math.floor(Math.random() * num1) + 1; // 确保结果为正
      answer = num1 - num2;
      break;
    case '×':
      num1 = Math.floor(Math.random() * Math.sqrt(config.maxNum)) + 1;
      num2 = Math.floor(Math.random() * Math.sqrt(config.maxNum)) + 1;
      answer = num1 * num2;
      break;
    case '÷':
      num2 = Math.floor(Math.random() * 10) + 1;
      answer = Math.floor(Math.random() * 10) + 1;
      num1 = num2 * answer; // 确保整除
      break;
    default:
      num1 = 1;
      num2 = 1;
      answer = 2;
  }
  
  return {
    id,
    num1,
    num2,
    operation,
    answer,
    userAnswer: '',
    isCorrect: null,
    timeSpent: 0,
  };
}

// 生成题目列表
function generateQuestions(count: number, difficulty: Difficulty): Question[] {
  return Array.from({ length: count }, (_, i) => generateQuestion(i + 1, difficulty));
}

export default function MentalMathPage() {
  // 游戏状态
  const [difficulty, setDifficulty] = useState<Difficulty>('easy');
  const [questionCount, setQuestionCount] = useState(20);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userInput, setUserInput] = useState('');
  const [gameState, setGameState] = useState<'idle' | 'playing' | 'finished'>('idle');
  
  // 计时
  const [timeLeft, setTimeLeft] = useState(0);
  const [elapsedTime, setElapsedTime] = useState(0);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const startTimeRef = useRef<number>(0);
  
  // 统计
  const [correctCount, setCorrectCount] = useState(0);
  const [wrongCount, setWrongCount] = useState(0);
  const [streak, setStreak] = useState(0);
  const [bestStreak, setBestStreak] = useState(0);
  
  // UI 状态
  const [mobileMenu, setMobileMenu] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [showKeyboard, setShowKeyboard] = useState(true);
  const inputRef = useRef<HTMLInputElement>(null);
  
  // 当前题目
  const currentQuestion = questions[currentIndex];
  
  // 开始游戏
  const startGame = useCallback(() => {
    const newQuestions = generateQuestions(questionCount, difficulty);
    setQuestions(newQuestions);
    setCurrentIndex(0);
    setUserInput('');
    setGameState('playing');
    setCorrectCount(0);
    setWrongCount(0);
    setStreak(0);
    setBestStreak(0);
    setTimeLeft(DIFFICULTY_CONFIG[difficulty].timeLimit);
    setElapsedTime(0);
    startTimeRef.current = Date.now();
    setShowHistory(false);
    
    // 聚焦输入框
    setTimeout(() => {
      inputRef.current?.focus();
    }, 100);
  }, [difficulty, questionCount]);
  
  // 计时器
  useEffect(() => {
    if (gameState === 'playing') {
      timerRef.current = setInterval(() => {
        const elapsed = Math.floor((Date.now() - startTimeRef.current) / 1000);
        setElapsedTime(elapsed);
        setTimeLeft(prev => {
          if (prev <= 1) {
            // 时间到，结束游戏
            setGameState('finished');
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      
      return () => {
        if (timerRef.current) {
          clearInterval(timerRef.current);
        }
      };
    }
  }, [gameState]);
  
  // 提交答案
  const submitAnswer = useCallback(() => {
    if (!currentQuestion || userInput.trim() === '') return;
    
    const answer = parseInt(userInput, 10);
    const isCorrect = answer === currentQuestion.answer;
    const timeSpent = Math.floor((Date.now() - startTimeRef.current) / 1000);
    
    // 更新题目状态
    setQuestions(prev => prev.map((q, i) => 
      i === currentIndex 
        ? { ...q, userAnswer: userInput, isCorrect, timeSpent }
        : q
    ));
    
    // 更新统计
    if (isCorrect) {
      setCorrectCount(prev => prev + 1);
      setStreak(prev => {
        const newStreak = prev + 1;
        setBestStreak(best => Math.max(best, newStreak));
        return newStreak;
      });
    } else {
      setWrongCount(prev => prev + 1);
      setStreak(0);
    }
    
    // 下一题或结束
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
      setUserInput('');
      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    } else {
      setGameState('finished');
    }
  }, [currentQuestion, currentIndex, userInput, questions.length]);
  
  // 键盘事件
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      submitAnswer();
    }
  }, [submitAnswer]);
  
  // 数字键盘点击
  const handleNumPad = (value: string) => {
    if (value === 'C') {
      setUserInput('');
    } else if (value === '←') {
      setUserInput(prev => prev.slice(0, -1));
    } else if (value === 'OK') {
      submitAnswer();
    } else {
      setUserInput(prev => prev + value);
    }
  };
  
  // 计算统计
  const accuracy = questions.length > 0 
    ? Math.round((correctCount / (correctCount + wrongCount)) * 100) || 0 
    : 0;
  const avgTime = correctCount + wrongCount > 0 
    ? Math.round(elapsedTime / (correctCount + wrongCount)) 
    : 0;
  
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* ===== 顶部导航 ===== */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <a href="/" className="text-xl font-bold text-white hover:opacity-80 transition-opacity">
                ← 教材工具箱
              </a>
            </div>
            
            <div className="hidden md:flex items-center gap-2">
              <span className="text-2xl">⚡</span>
              <span className="text-lg font-bold text-white">口算速练</span>
            </div>
            
            <button
              onClick={() => setMobileMenu(!mobileMenu)}
              className="md:hidden p-2 text-gray-300 hover:text-white transition-colors"
            >
              {mobileMenu ? '✕' : '☰'}
            </button>
          </div>
        </div>
        
        {mobileMenu && (
          <div className="md:hidden bg-slate-800 border-t border-white/10 py-4 px-4 space-y-1">
            <a href="/" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg">首页</a>
            <a href="/tools/math-worksheet" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg">🧮 数学练习卷</a>
            <a href="/tools/calligraphy" className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg">✍️ 字帖生成器</a>
          </div>
        )}
      </nav>
      
      <main className="pt-20 pb-8 px-4">
        <div className="max-w-4xl mx-auto">
          
          {/* ===== 开始界面 ===== */}
          {gameState === 'idle' && (
            <div className="space-y-8">
              {/* 标题 */}
              <div className="text-center">
                <div className="text-6xl mb-4">⚡</div>
                <h1 className="text-4xl font-black text-white mb-2">口算速练</h1>
                <p className="text-gray-400">在线计时答题，锻炼口算速度</p>
              </div>
              
              {/* 难度选择 */}
              <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-6">
                <h2 className="text-xl font-bold text-white mb-4">选择难度</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {(Object.keys(DIFFICULTY_CONFIG) as Difficulty[]).map((d) => {
                    const config = DIFFICULTY_CONFIG[d];
                    return (
                      <button
                        key={d}
                        onClick={() => setDifficulty(d)}
                        className={`p-4 rounded-xl border-2 transition-all ${
                          difficulty === d
                            ? `border-transparent bg-gradient-to-br ${config.color} text-white`
                            : 'border-white/20 bg-slate-700/50 text-gray-300 hover:border-white/40'
                        }`}
                      >
                        <div className="text-3xl mb-2">{config.icon}</div>
                        <div className="font-bold">{config.label}</div>
                        <div className="text-xs opacity-80 mt-1">{config.description}</div>
                      </button>
                    );
                  })}
                </div>
              </div>
              
              {/* 题目数量 */}
              <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-6">
                <h2 className="text-xl font-bold text-white mb-4">题目数量</h2>
                <div className="flex flex-wrap gap-3">
                  {[10, 20, 30, 50].map((count) => (
                    <button
                      key={count}
                      onClick={() => setQuestionCount(count)}
                      className={`px-6 py-3 rounded-xl font-bold transition-all ${
                        questionCount === count
                          ? 'bg-blue-500 text-white'
                          : 'bg-slate-700/50 text-gray-300 hover:bg-slate-600'
                      }`}
                    >
                      {count} 题
                    </button>
                  ))}
                </div>
              </div>
              
              {/* 开始按钮 */}
              <div className="text-center">
                <button
                  onClick={startGame}
                  className="px-12 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold text-xl rounded-2xl shadow-xl hover:scale-105 transition-transform"
                >
                  开始挑战 🚀
                </button>
              </div>
              
              {/* 规则说明 */}
              <div className="bg-slate-800/30 border border-white/10 rounded-xl p-4 text-sm text-gray-400">
                <h3 className="font-bold text-white mb-2">📖 游戏规则</h3>
                <ul className="space-y-1 list-disc list-inside">
                  <li>在规定时间内完成所有题目</li>
                  <li>输入答案后按 Enter 或点击 OK 提交</li>
                  <li>连续答对可获得连击奖励</li>
                  <li>时间结束或答完所有题目后显示成绩</li>
                </ul>
              </div>
            </div>
          )}
          
          {/* ===== 游戏界面 ===== */}
          {gameState === 'playing' && currentQuestion && (
            <div className="space-y-6">
              {/* 进度条 */}
              <div className="bg-slate-800/50 border border-white/10 rounded-xl p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-400">进度</span>
                  <span className="text-white font-bold">{currentIndex + 1} / {questions.length}</span>
                </div>
                <div className="h-3 bg-slate-700 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-blue-500 to-purple-600 transition-all duration-300"
                    style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}
                  />
                </div>
              </div>
              
              {/* 计时和统计 */}
              <div className="grid grid-cols-3 gap-4">
                <div className="bg-slate-800/50 border border-white/10 rounded-xl p-4 text-center">
                  <div className="text-gray-400 text-sm mb-1">剩余时间</div>
                  <div className={`text-3xl font-black ${timeLeft <= 10 ? 'text-red-400 animate-pulse' : 'text-white'}`}>
                    {timeLeft}s
                  </div>
                </div>
                <div className="bg-slate-800/50 border border-white/10 rounded-xl p-4 text-center">
                  <div className="text-gray-400 text-sm mb-1">正确</div>
                  <div className="text-3xl font-black text-green-400">{correctCount}</div>
                </div>
                <div className="bg-slate-800/50 border border-white/10 rounded-xl p-4 text-center">
                  <div className="text-gray-400 text-sm mb-1">连击</div>
                  <div className="text-3xl font-black text-yellow-400">{streak}🔥</div>
                </div>
              </div>
              
              {/* 题目卡片 */}
              <div className="bg-gradient-to-br from-slate-800 to-slate-700 border border-white/20 rounded-3xl p-8 md:p-12 text-center">
                <div className="text-6xl md:text-8xl font-black text-white mb-8">
                  {currentQuestion.num1} {currentQuestion.operation} {currentQuestion.num2} = ?
                </div>
                
                {/* 输入框 */}
                <div className="max-w-xs mx-auto">
                  <input
                    ref={inputRef}
                    type="number"
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    className="w-full text-center text-4xl font-bold bg-slate-900 border-2 border-white/30 rounded-2xl px-6 py-4 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="?"
                    autoFocus
                  />
                </div>
              </div>
              
              {/* 数字键盘 */}
              {showKeyboard && (
                <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-4">
                  <div className="grid grid-cols-4 gap-2 max-w-xs mx-auto">
                    {['7', '8', '9', 'C', '4', '5', '6', '←', '1', '2', '3', 'OK', '0', '-', '-', '-'].map((key, i) => {
                      if (key === '-') return <div key={i} />;
                      return (
                        <button
                          key={i}
                          onClick={() => handleNumPad(key)}
                          className={`py-4 rounded-xl font-bold text-xl transition-all ${
                            key === 'OK'
                              ? 'bg-green-500 hover:bg-green-600 text-white col-span-1'
                              : key === 'C'
                              ? 'bg-red-500/80 hover:bg-red-500 text-white'
                              : key === '←'
                              ? 'bg-orange-500/80 hover:bg-orange-500 text-white'
                              : 'bg-slate-700 hover:bg-slate-600 text-white'
                          }`}
                        >
                          {key === '←' ? '⌫' : key}
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}
              
              {/* 键盘开关 */}
              <div className="text-center">
                <button
                  onClick={() => setShowKeyboard(!showKeyboard)}
                  className="text-gray-400 hover:text-white text-sm"
                >
                  {showKeyboard ? '隐藏键盘 ⌨' : '显示键盘 ⌨'}
                </button>
              </div>
            </div>
          )}
          
          {/* ===== 结束界面 ===== */}
          {gameState === 'finished' && (
            <div className="space-y-8">
              {/* 成绩卡片 */}
              <div className="bg-gradient-to-br from-slate-800 to-slate-700 border border-white/20 rounded-3xl p-8 text-center">
                <div className="text-6xl mb-4">
                  {accuracy >= 90 ? '🏆' : accuracy >= 70 ? '🥈' : accuracy >= 50 ? '🥉' : '💪'}
                </div>
                <h2 className="text-3xl font-black text-white mb-2">挑战完成！</h2>
                <p className="text-gray-400 mb-6">
                  {accuracy >= 90 ? '太棒了！你是口算高手！' : accuracy >= 70 ? '不错！继续加油！' : '多多练习，你会越来越好的！'}
                </p>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="bg-slate-900/50 rounded-xl p-4">
                    <div className="text-gray-400 text-sm">正确率</div>
                    <div className="text-3xl font-black text-green-400">{accuracy}%</div>
                  </div>
                  <div className="bg-slate-900/50 rounded-xl p-4">
                    <div className="text-gray-400 text-sm">答对</div>
                    <div className="text-3xl font-black text-white">{correctCount}/{questions.length}</div>
                  </div>
                  <div className="bg-slate-900/50 rounded-xl p-4">
                    <div className="text-gray-400 text-sm">用时</div>
                    <div className="text-3xl font-black text-blue-400">{elapsedTime}s</div>
                  </div>
                  <div className="bg-slate-900/50 rounded-xl p-4">
                    <div className="text-gray-400 text-sm">最高连击</div>
                    <div className="text-3xl font-black text-yellow-400">{bestStreak}🔥</div>
                  </div>
                </div>
                
                <div className="flex flex-wrap justify-center gap-4">
                  <button
                    onClick={startGame}
                    className="px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl hover:scale-105 transition-transform"
                  >
                    再来一局 🔄
                  </button>
                  <button
                    onClick={() => setGameState('idle')}
                    className="px-8 py-3 bg-slate-700 text-white font-bold rounded-xl hover:bg-slate-600"
                  >
                    返回设置 ⚙️
                  </button>
                  <button
                    onClick={() => setShowHistory(!showHistory)}
                    className="px-8 py-3 bg-slate-700 text-white font-bold rounded-xl hover:bg-slate-600"
                  >
                    {showHistory ? '隐藏详情' : '查看详情'} 📋
                  </button>
                </div>
              </div>
              
              {/* 答题详情 */}
              {showHistory && (
                <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-6">
                  <h3 className="text-xl font-bold text-white mb-4">答题详情</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    {questions.map((q, i) => (
                      <div
                        key={q.id}
                        className={`p-3 rounded-xl text-center ${
                          q.isCorrect === true
                            ? 'bg-green-500/20 border border-green-500/30'
                            : q.isCorrect === false
                            ? 'bg-red-500/20 border border-red-500/30'
                            : 'bg-slate-700/50 border border-white/10'
                        }`}
                      >
                        <div className="text-sm text-gray-300 mb-1">
                          {q.num1} {q.operation} {q.num2} =
                        </div>
                        <div className={`font-bold ${q.isCorrect ? 'text-green-400' : 'text-red-400'}`}>
                          {q.userAnswer || '-'}
                          {q.isCorrect === false && (
                            <span className="text-gray-400 ml-2">({q.answer})</span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* 错题回顾 */}
              {questions.filter(q => q.isCorrect === false).length > 0 && (
                <div className="bg-red-500/10 border border-red-500/30 rounded-2xl p-6">
                  <h3 className="text-xl font-bold text-red-400 mb-4">❌ 错题回顾</h3>
                  <div className="space-y-2">
                    {questions.filter(q => q.isCorrect === false).map((q) => (
                      <div key={q.id} className="flex items-center justify-between bg-slate-800/50 rounded-lg p-3">
                        <span className="text-white">
                          {q.num1} {q.operation} {q.num2} = ?
                        </span>
                        <div>
                          <span className="text-red-400 mr-4">你的答案: {q.userAnswer}</span>
                          <span className="text-green-400">正确答案: {q.answer}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
          
        </div>
      </main>
      
      {/* ===== 页脚 ===== */}
      <footer className="border-t border-white/10 py-6 px-4">
        <div className="max-w-4xl mx-auto text-center text-gray-500 text-sm">
          <p>⚡ 口算速练 - 锻炼口算速度，提升计算能力</p>
        </div>
      </footer>

      {/* 使用指南 */}
      <div className="max-w-4xl mx-auto px-4 py-12">
        <ToolGuide {...toolGuides['mental-math']} />
      </div>
    </div>
  );
}
