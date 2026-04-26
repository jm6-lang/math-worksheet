/**
 * 统一工具注册表 - 所有工具的唯一数据源
 * 
 * 新增工具时只需在此文件添加一条记录，以下内容会自动同步：
 * - sitemap.xml（动态生成）
 * - JSON-LD 结构化数据（SoftwareApplication）
 * - 首页导航卡片
 * - 导航栏组件
 * - Organization 描述中的工具数量
 */

export interface ToolConfig {
  /** 工具路径，如 /tools/math-worksheet */
  path: string;
  /** 工具名称，如 数学练习卷 */
  name: string;
  /** 导航栏显示名（简短），如 数学练习卷 */
  navName: string;
  /** 首页卡片图标 */
  icon: string;
  /** 首页卡片简短描述 */
  desc: string;
  /** 首页卡片颜色 */
  color: string;
  /** JSON-LD 中的完整名称 */
  schemaName: string;
  /** JSON-LD 中的描述 */
  schemaDescription: string;
  /** JSON-LD 应用类型 */
  schemaCategory: 'EducationApplication' | 'GameApplication';
  /** sitemap 优先级 */
  priority: number;
  /** sitemap 更新频率 */
  changefreq: 'daily' | 'weekly' | 'monthly';
  /** 是否已上线 */
  active: boolean;
}

export const TOOLS: ToolConfig[] = [
  {
    path: '/tools/math-worksheet',
    name: '数学练习卷',
    navName: '数学练习卷',
    icon: '🧮',
    desc: '一键出题，PDF导出',
    color: 'blue',
    schemaName: '数学练习卷生成器',
    schemaDescription: '免费在线生成小学数学练习卷，支持加减乘除竖式、分数、方程等题型，一键打印PDF',
    schemaCategory: 'EducationApplication',
    priority: 0.9,
    changefreq: 'weekly',
    active: true,
  },
  {
    path: '/tools/calligraphy',
    name: '字帖生成器',
    navName: '字帖生成器',
    icon: '✍️',
    desc: '田字格/米字格模板',
    color: 'emerald',
    schemaName: '字帖生成器',
    schemaDescription: '在线生成田字格/米字格字帖，四种格子样式可选，支持直接打印，适合小学生练字',
    schemaCategory: 'EducationApplication',
    priority: 0.9,
    changefreq: 'weekly',
    active: true,
  },
  {
    path: '/tools/english-calligraphy',
    name: '英语字帖',
    navName: '英语字帖',
    icon: '🔤',
    desc: '四线三格模板',
    color: 'rose',
    schemaName: '英语字帖生成器',
    schemaDescription: '输入英文单词或句子，自动生成四线三格练习纸，支持多种字体和行高，一键打印',
    schemaCategory: 'EducationApplication',
    priority: 0.9,
    changefreq: 'weekly',
    active: true,
  },
  {
    path: '/tools/sudoku',
    name: '数独游戏',
    navName: '数独游戏',
    icon: '🧩',
    desc: '多难度逻辑训练',
    color: 'orange',
    schemaName: '数独游戏',
    schemaDescription: '在线数独游戏，支持多个难度等级，数字键盘输入，适合各年龄段益智训练',
    schemaCategory: 'GameApplication',
    priority: 0.9,
    changefreq: 'weekly',
    active: true,
  },
  {
    path: '/tools/pinyin',
    name: '拼音注音',
    navName: '拼音注音',
    icon: '📝',
    desc: '汉字注音练习',
    color: 'blue',
    schemaName: '拼音练习生成器',
    schemaDescription: '生成拼音四线三格练习纸，支持声母、韵母、整体认读音节，一键打印PDF',
    schemaCategory: 'EducationApplication',
    priority: 0.8,
    changefreq: 'weekly',
    active: true,
  },
  {
    path: '/tools/mental-math',
    name: '口算速练',
    navName: '口算速练',
    icon: '⚡',
    desc: '在线计时练习',
    color: 'orange',
    schemaName: '口算速练',
    schemaDescription: '在线口算计时练习，支持4个难度级别，即时反馈，适合小学生数学速算训练',
    schemaCategory: 'EducationApplication',
    priority: 0.9,
    changefreq: 'weekly',
    active: true,
  },
  {
    path: '/tools/flashcards',
    name: '识字卡片',
    navName: '识字卡片',
    icon: '🃏',
    desc: '汉字卡片生成',
    color: 'blue',
    schemaName: '识字卡片生成器',
    schemaDescription: '免费在线生成识字卡片，支持自定义汉字、拼音、组词，可打印制作实体卡片',
    schemaCategory: 'EducationApplication',
    priority: 0.9,
    changefreq: 'weekly',
    active: true,
  },
  {
    path: '/tools/writing-template',
    name: '作文模板',
    navName: '作文模板',
    icon: '📄',
    desc: '多种写作模板',
    color: 'emerald',
    schemaName: '作文模板生成器',
    schemaDescription: '免费在线生成作文模板，支持看图写话、日记、书信等多种格式，适合小学生写作练习',
    schemaCategory: 'EducationApplication',
    priority: 0.9,
    changefreq: 'weekly',
    active: true,
  },
  {
    path: '/tools/poem-memo',
    name: '古诗词默写',
    navName: '古诗词默写',
    icon: '📜',
    desc: '必背古诗默写练习',
    color: 'blue',
    schemaName: '古诗词默写生成器',
    schemaDescription: '免费在线生成古诗词默写练习卷，覆盖小学1-6年级必背古诗词，支持填空默写、全诗默写、上下句默写三种模式',
    schemaCategory: 'EducationApplication',
    priority: 0.9,
    changefreq: 'weekly',
    active: true,
  },
  {
    path: '/tools/unit-test',
    name: '单元测试卷',
    navName: '单元测试卷',
    icon: '📋',
    desc: '按教材单元出题',
    color: 'orange',
    schemaName: '单元测试卷生成器',
    schemaDescription: '免费在线生成小学数学单元测试卷，按人教版教材单元出题，支持期中期末测试，PDF导出即印即用',
    schemaCategory: 'EducationApplication',
    priority: 0.9,
    changefreq: 'weekly',
    active: true,
  },
];

/** 已上线的工具数量 */
export const ACTIVE_TOOL_COUNT = TOOLS.filter(t => t.active).length;

/** 生成 JSON-LD SoftwareApplication 数组 */
export function generateSchemaApps(): object[] {
  return TOOLS.filter(t => t.active).map(tool => ({
    '@type': 'SoftwareApplication',
    name: tool.schemaName,
    url: `https://www.skillxm.cn${tool.path}`,
    description: tool.schemaDescription,
    applicationCategory: tool.schemaCategory,
    operatingSystem: 'Web Browser',
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'CNY',
    },
  }));
}

/** 生成 JSON-LD BreadcrumbList 数组 */
export function generateSchemaBreadcrumbs(): object[] {
  return TOOLS.filter(t => t.active).map(tool => ({
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: '首页', item: 'https://www.skillxm.cn' },
      { '@type': 'ListItem', position: 2, name: tool.name, item: `https://www.skillxm.cn${tool.path}` },
    ],
  }));
}

/** 首页导航卡片数据 */
export function getHomeToolCards() {
  return TOOLS.filter(t => t.active).map(t => ({
    name: t.name,
    icon: t.icon,
    desc: t.desc,
    link: t.path,
    color: t.color,
    disabled: false,
  }));
}

/** 导航栏链接数据 */
export function getNavBarLinks() {
  return TOOLS.filter(t => t.active).map(t => ({
    name: t.navName,
    href: t.path,
  }));
}
