// ============================================================
// 数学出题算法核心模块
// ============================================================

export interface Question {
  id: number;
  question: string;       // 题目文本，如 "12 + 5 ="
  answer: string;         // 答案文本，如 "17"
  // 用于填空题/比大小等特殊格式
  raw?: {
    a?: number;
    b?: number;
    result?: number;
    sign?: string;
  };
}

export interface QuestionConfig {
  types: QuestionType[];
  range: [number, number];    // 数字范围，如 [1, 20]
  count: number;              // 题目数量
  grade: number;              // 年级 1-6
  includeAnswers: boolean;    // 是否包含答案
  shuffle: boolean;           // 是否打乱
  decimal?: boolean;          // 小数运算
  fraction?: boolean;         // 分数运算
}

export type QuestionType =
  | 'addition'       // 加法
  | 'subtraction'    // 减法
  | 'multiplication' // 乘法
  | 'division'       // 除法
  | 'mixed'          // 混合运算
  | 'fill_blank'     // 填空题 a + ( ) = c
  | 'compare'        // 比大小 a ( ) b
  | 'vertical_add'   // 竖式加法
  | 'vertical_sub'   // 竖式减法
  | 'vertical_mul'   // 竖式乘法
  | 'vertical_div'   // 竖式除法
  ;

// 安全的随机整数
function randInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// 打乱数组（Fisher-Yates）
function shuffleArray<T>(arr: T[]): T[] {
  const result = [...arr];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

// 生成不重复的随机数对
function generateUniquePairs(
  count: number,
  range: [number, number],
  validator: (a: number, b: number) => boolean
): Array<[number, number]> {
  const pairs: Array<[number, number]> = [];
  const seen = new Set<string>();

  let attempts = 0;
  const maxAttempts = count * 20;

  while (pairs.length < count && attempts < maxAttempts) {
    attempts++;
    let a = randInt(range[0], Math.min(range[1], 99));
    let b = randInt(range[0], Math.min(range[1], 99));

    // 交换使得 a >= b（对减法和除法更有利）
    if (Math.random() > 0.5) [a, b] = [b, a];

    const key = `${a},${b}`;
    if (!seen.has(key) && validator(a, b)) {
      seen.add(key);
      pairs.push([a, b]);
    }
  }

  return pairs;
}

// 生成不重复的随机数（用于填空题）
function generateUniqueNumbers(
  count: number,
  range: [number, number],
  validator: (n: number) => boolean
): number[] {
  const numbers: number[] = [];
  const seen = new Set<number>();

  let attempts = 0;
  const maxAttempts = count * 20;

  while (numbers.length < count && attempts < maxAttempts) {
    attempts++;
    const n = randInt(range[0], Math.min(range[1], 999));
    if (!seen.has(n) && validator(n)) {
      seen.add(n);
      numbers.push(n);
    }
  }

  return numbers;
}

// 加法
function genAddition(a: number, b: number): Question {
  return {
    id: 0,
    question: `${a} + ${b} = `,
    answer: String(a + b),
  };
}

// 减法（确保结果非负）
function genSubtraction(a: number, b: number): Question {
  return {
    id: 0,
    question: `${a} - ${b} = `,
    answer: String(a - b),
  };
}

// 乘法
function genMultiplication(a: number, b: number): Question {
  return {
    id: 0,
    question: `${a} × ${b} = `,
    answer: String(a * b),
  };
}

// 除法（确保整除）
function genDivision(a: number, b: number): Question {
  return {
    id: 0,
    question: `${a} ÷ ${b} = `,
    answer: String(a / b),
  };
}

// 填空题：( ) + b = c 形式
function genFillBlank(range: [number, number]): Question {
  const type = randInt(1, 4);
  if (type === 1) {
    // a + ( ) = c
    const b = randInt(range[0], Math.min(range[1], 50));
    const c = randInt(b, b + range[1]);
    return {
      id: 0,
      question: `${b} + (  ) = ${c}`,
      answer: String(c - b),
      raw: { a: b, result: c, sign: '+' },
    };
  } else if (type === 2) {
    // a - ( ) = c
    const a = randInt(range[0] + 5, Math.min(range[1] + 10, 60));
    const c = randInt(range[0], a - 1);
    return {
      id: 0,
      question: `${a} - (  ) = ${c}`,
      answer: String(a - c),
      raw: { a, result: c, sign: '-' },
    };
  } else if (type === 3) {
    // ( ) × b = c
    const b = randInt(2, Math.min(range[1], 9));
    const c = randInt(1, Math.min(Math.floor(50 / b), 12)) * b;
    return {
      id: 0,
      question: `(  ) × ${b} = ${c}`,
      answer: String(c / b),
      raw: { a: c / b, b, result: c, sign: '×' },
    };
  } else {
    // a × ( ) = c
    const a = randInt(2, Math.min(range[1], 9));
    const c = randInt(1, Math.min(Math.floor(50 / a), 12)) * a;
    return {
      id: 0,
      question: `${a} × (  ) = ${c}`,
      answer: String(c / a),
      raw: { a, b: c / a, result: c, sign: '×' },
    };
  }
}

// 比大小
function genCompare(range: [number, number]): Question {
  const a = randInt(range[0], Math.min(range[1], 99));
  const b = randInt(range[0], Math.min(range[1], 99));
  const ops = ['<', '>', '='] as const;
  const op = ops[randInt(0, 2)];
  return {
    id: 0,
    question: `${a}  (  )  ${b}`,
    answer: op === '<' ? '<' : op === '>' ? '>' : '=',
    raw: { a, b, sign: op },
  };
}

// 竖式加法
function genVerticalAdd(a: number, b: number): Question {
  const sum = a + b;
  return {
    id: 0,
    question: `${a}`,
    answer: `${b}`,
    raw: { a, b, result: sum, sign: '+' },
  };
}

// 竖式减法
function genVerticalSub(a: number, b: number): Question {
  return {
    id: 0,
    question: `${a}`,
    answer: `${b}`,
    raw: { a, b, result: a - b, sign: '-' },
  };
}

// 竖式乘法
function genVerticalMul(a: number, b: number): Question {
  return {
    id: 0,
    question: `${a}`,
    answer: `${b}`,
    raw: { a, b, result: a * b, sign: '×' },
  };
}

// 竖式除法
function genVerticalDiv(range: [number, number]): Question {
  const b = randInt(2, Math.min(range[1], 9));
  const quotient = randInt(2, Math.min(range[1], 12));
  const a = b * quotient;
  return {
    id: 0,
    question: `${a}`,
    answer: `${b}`,
    raw: { a, b: quotient, result: b, sign: '÷' },
  };
}

// 根据范围和题型获取生成对
function getGeneratorForType(type: QuestionType, range: [number, number]) {
  switch (type) {
    case 'addition':
      return generateUniquePairs(
        100,
        range,
        (a, b) => a + b <= range[1] * 2 && a > 0 && b > 0
      );
    case 'subtraction':
      return generateUniquePairs(
        100,
        [range[0], range[1] + 10],
        (a, b) => a >= b && a - b >= 0 && a > 0 && b > 0
      );
    case 'multiplication':
      return generateUniquePairs(
        100,
        [1, Math.min(range[1], 12)],
        (a, b) => a * b <= 144 && a > 0 && b > 0
      );
    case 'division':
      return generateUniquePairs(
        100,
        [1, Math.min(range[1], 12)],
        (a, b) => b > 0 && a % b === 0 && a / b > 0
      );
    default:
      return [];
  }
}

// ============================================================
// 主出口函数：生成一套题目
// ============================================================
export function generateQuestions(config: QuestionConfig): Question[] {
  const { types, range, count, shuffle: shouldShuffle, grade } = config;

  const questions: Question[] = [];

  // 计算每种题型分配多少题
  const typeCount: Record<string, number> = {};
  const base = Math.floor(count / types.length);
  const remainder = count % types.length;

  types.forEach((type, i) => {
    typeCount[type] = base + (i < remainder ? 1 : 0);
  });

  // 为每种题型生成题目
  for (const type of types) {
    const n = typeCount[type] || 0;
    let generated: Question[] = [];

    switch (type) {
      case 'addition': {
        const pairs = generateUniquePairs(n, range, (a, b) => a > 0 && b > 0);
        generated = pairs.map(([a, b]) => ({ ...genAddition(a, b), id: questions.length + generated.length + 1 }));
        break;
      }
      case 'subtraction': {
        const pairs = generateUniquePairs(n, [range[0], Math.max(range[1], 20)], (a, b) => a >= b && a > 0 && b > 0);
        generated = pairs.map(([a, b]) => ({ ...genSubtraction(a, b), id: questions.length + generated.length + 1 }));
        break;
      }
      case 'multiplication': {
        const mulRange: [number, number] = [1, Math.min(range[1], 12)];
        const pairs = generateUniquePairs(n, mulRange, (a, b) => a > 0 && b > 0);
        generated = pairs.map(([a, b]) => ({ ...genMultiplication(a, b), id: questions.length + generated.length + 1 }));
        break;
      }
      case 'division': {
        const divRange: [number, number] = [1, Math.min(range[1], 12)];
        const pairs = generateUniquePairs(n, divRange, (a, b) => b > 0 && a % b === 0 && a / b > 0);
        generated = pairs.map(([a, b]) => ({ ...genDivision(a, b), id: questions.length + generated.length + 1 }));
        break;
      }
      case 'mixed': {
        const mixedTypes: QuestionType[] = ['addition', 'subtraction', 'multiplication', 'division'];
        for (let i = 0; i < n; i++) {
          const t = mixedTypes[randInt(0, 3)];
          const q = generateMixedQuestion(t, range);
          generated.push({ ...q, id: questions.length + generated.length + 1 });
        }
        break;
      }
      case 'fill_blank': {
        for (let i = 0; i < n; i++) {
          generated.push({ ...genFillBlank(range), id: questions.length + generated.length + 1 });
        }
        break;
      }
      case 'compare': {
        for (let i = 0; i < n; i++) {
          generated.push({ ...genCompare(range), id: questions.length + generated.length + 1 });
        }
        break;
      }
      case 'vertical_add': {
        const pairs = generateUniquePairs(n, range, (a, b) => a > 0 && b > 0);
        generated = pairs.map(([a, b]) => ({ ...genVerticalAdd(a, b), id: questions.length + generated.length + 1 }));
        break;
      }
      case 'vertical_sub': {
        const pairs = generateUniquePairs(n, [range[0], Math.max(range[1], 20)], (a, b) => a >= b && a > 0 && b > 0);
        generated = pairs.map(([a, b]) => ({ ...genVerticalSub(a, b), id: questions.length + generated.length + 1 }));
        break;
      }
      case 'vertical_mul': {
        const mulRange: [number, number] = [1, Math.min(range[1], 12)];
        const pairs = generateUniquePairs(n, mulRange, (a, b) => a > 0 && b > 0);
        generated = pairs.map(([a, b]) => ({ ...genVerticalMul(a, b), id: questions.length + generated.length + 1 }));
        break;
      }
      case 'vertical_div': {
        for (let i = 0; i < n; i++) {
          generated.push({ ...genVerticalDiv(range), id: questions.length + generated.length + 1 });
        }
        break;
      }
    }

    questions.push(...generated);
  }

  // 打乱
  if (shouldShuffle) {
    return shuffleArray(questions);
  }

  return questions;
}

// 混合运算
function generateMixedQuestion(type: QuestionType, range: [number, number]): Question {
  switch (type) {
    case 'addition': {
      const a = randInt(range[0], Math.min(range[1], 50));
      const b = randInt(range[0], Math.min(range[1], 50));
      return { id: 0, question: `${a} + ${b} = `, answer: String(a + b) };
    }
    case 'subtraction': {
      const a = randInt(range[0] + 5, Math.min(range[1], 60));
      const b = randInt(range[0], a);
      return { id: 0, question: `${a} - ${b} = `, answer: String(a - b) };
    }
    case 'multiplication': {
      const a = randInt(1, Math.min(range[1], 12));
      const b = randInt(1, Math.min(range[1], 12));
      return { id: 0, question: `${a} × ${b} = `, answer: String(a * b) };
    }
    case 'division': {
      const b = randInt(2, Math.min(range[1], 12));
      const q = randInt(2, Math.min(range[1], 12));
      const a = b * q;
      return { id: 0, question: `${a} ÷ ${b} = `, answer: String(q) };
    }
    default:
      return { id: 0, question: '1 + 1 = ', answer: '2' };
  }
}

// ============================================================
// 题型元数据（用于 UI 展示）
// ============================================================
export const QUESTION_TYPE_META: Record<QuestionType, { label: string; gradeMin: number; gradeMax: number; icon: string }> = {
  addition:       { label: '加法',       gradeMin: 1, gradeMax: 6, icon: '＋' },
  subtraction:    { label: '减法',       gradeMin: 1, gradeMax: 6, icon: '－' },
  multiplication: { label: '乘法',       gradeMin: 2, gradeMax: 6, icon: '×' },
  division:       { label: '除法',       gradeMin: 2, gradeMax: 6, icon: '÷' },
  mixed:          { label: '混合运算',   gradeMin: 3, gradeMax: 6, icon: '±' },
  fill_blank:     { label: '填空题',     gradeMin: 1, gradeMax: 3, icon: '（ ）' },
  compare:        { label: '比大小',     gradeMin: 1, gradeMax: 2, icon: '＜' },
  vertical_add:   { label: '竖式加法',   gradeMin: 2, gradeMax: 4, icon: '＋竖' },
  vertical_sub:   { label: '竖式减法',   gradeMin: 2, gradeMax: 4, icon: '－竖' },
  vertical_mul:   { label: '竖式乘法',   gradeMin: 3, gradeMax: 5, icon: '×竖' },
  vertical_div:   { label: '竖式除法',   gradeMin: 3, gradeMax: 6, icon: '÷竖' },
};

// 年级列表
export const GRADES = [1, 2, 3, 4, 5, 6];

// 推荐年级范围
export const GRADE_RANGES: Record<number, [number, number]> = {
  1: [1, 20],
  2: [1, 100],
  3: [1, 1000],
  4: [1, 10000],
  5: [1, 100000],
  6: [1, 1000000],
};

// 数字范围选项
export const RANGE_OPTIONS = [
  { label: '10以内', value: [1, 10] as [number, number] },
  { label: '20以内', value: [1, 20] as [number, number] },
  { label: '50以内', value: [1, 50] as [number, number] },
  { label: '100以内', value: [1, 100] as [number, number] },
  { label: '1000以内', value: [1, 1000] as [number, number] },
  { label: '10000以内', value: [1, 10000] as [number, number] },
  { label: '自定义', value: [1, 100] as [number, number] },
];

// 题目数量选项
export const COUNT_OPTIONS = [10, 20, 30, 50, 60, 80, 100];
