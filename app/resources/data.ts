export interface Resource {
  icon: string;
  title: string;
  desc: string;
  tags: string[];
  link: string;
  linkLabel: string;
}

export interface ResourceCategory {
  id: string;
  name: string;
  icon: string;
  desc: string;
  resources: Resource[];
}

export const RESOURCE_CATEGORIES: ResourceCategory[] = [
  {
    id: 'calligraphy',
    name: '字帖书法',
    icon: '✍️',
    desc: '书法字帖模板与练字教程',
    resources: [
      {
        icon: '✍️',
        title: '书法字帖资源合集',
        desc: '包含多种书法字帖模板，楷书、行书、隶书等多种字体，适合各年龄段练习使用',
        tags: ['字帖', '书法', '练字', '多字体'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
      {
        icon: '📖',
        title: '练字教程字帖大合集',
        desc: '系统练字教程配合字帖练习，从基础笔画到完整字形，循序渐进掌握书法技巧',
        tags: ['教程', '字帖', '合集', '系统学习'],
        link: 'https://pan.quark.cn/s/ed38ac8a3a44',
        linkLabel: '夸克网盘',
      },
    ],
  },
  {
    id: 'textbook',
    name: '电子课本',
    icon: '📚',
    desc: '各版本电子教科书下载',
    resources: [
      {
        icon: '📚',
        title: '小学初中高中电子版教科书下载器',
        desc: '支持下载各年级各科目电子版教科书，人教版、苏教版、北师版等主流版本全覆盖',
        tags: ['教科书', '下载器', '全学段', '多版本'],
        link: 'https://pan.quark.cn/s/ec6e312bc935',
        linkLabel: '夸克网盘',
      },
      {
        icon: '🎓',
        title: '中小学电子课本下载器 v2.1',
        desc: '最新版电子课本下载工具，支持更多教材版本，界面更友好，一键获取全套教材',
        tags: ['课本', '下载器', '最新版', '一键下载'],
        link: 'https://pan.quark.cn/s/6a29f7a5e914',
        linkLabel: '夸克网盘',
      },
    ],
  },
  {
    id: 'math',
    name: '数学资料',
    icon: '🧮',
    desc: '数学练习卷与奥数资料',
    resources: [
      {
        icon: '🧮',
        title: '小学1-6年级数学练习卷合集',
        desc: '涵盖人教版、北师版等主流教材，包含单元测试、期中期末试卷，附详细答案解析',
        tags: ['数学', '试卷', '1-6年级', '带答案'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
      {
        icon: '🏆',
        title: '小学奥数举一反三AB版',
        desc: '经典奥数训练教材，从入门到进阶，培养数学思维和逻辑推理能力',
        tags: ['奥数', '举一反三', '思维训练', 'AB版'],
        link: 'https://pan.quark.cn/s/6ed6bab78edf',
        linkLabel: '夸克网盘',
      },
      {
        icon: '📐',
        title: '小学数学口算速算练习册',
        desc: '每日一练口算速算题卡，从10以内到1000以内，分级训练提升计算速度和准确率',
        tags: ['口算', '速算', '每日练习', '分级训练'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
    ],
  },
  {
    id: 'chinese',
    name: '语文资料',
    icon: '📖',
    desc: '阅读理解与作文指导',
    resources: [
      {
        icon: '📖',
        title: '小学语文阅读训练100篇超详解',
        desc: '王朝霞阅读训练系列，1-6年级分级阅读理解训练，涵盖古诗文、现代文、写作训练',
        tags: ['阅读理解', '100篇', '分级', '超详解'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
      {
        icon: '📝',
        title: '小学看图写话与作文指导',
        desc: '低年级看图写话训练 + 中高年级作文技巧指导，包含优秀范文和写作模板',
        tags: ['看图写话', '作文', '范文', '写作技巧'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
      {
        icon: '🔤',
        title: '小学拼音汉字识字资料',
        desc: '拼音学习卡片、汉字笔顺描红、识字练习册，帮助低年级学生打好语文基础',
        tags: ['拼音', '识字', '笔顺', '描红'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
    ],
  },
  {
    id: 'english',
    name: '英语资料',
    icon: '🔤',
    desc: '自然拼读、音标、词汇课程',
    resources: [
      {
        icon: '🔤',
        title: 'BBC自然拼读 Fun With Phonics',
        desc: 'BBC出品自然拼读全套资源，含44个动画视频 + 14册练习册PDF + 26个单词卡PDF，可打印',
        tags: ['自然拼读', 'BBC', '视频+PDF', '可打印'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
      {
        icon: '🎵',
        title: '启蒙英语动画',
        desc: '精选英语启蒙动画资源，趣味学习英语，培养语感和听力理解能力',
        tags: ['启蒙', '动画', '英语', '趣味学习'],
        link: 'https://pan.quark.cn/s/58476c46e35e',
        linkLabel: '夸克网盘',
      },
      {
        icon: '🎓',
        title: '自然拼读音标课语法课新概念全套',
        desc: '跟着老师学英语全套课程，包含自然拼读、音标课、语法课、新概念英语，共80GB',
        tags: ['自然拼读', '音标', '语法', '新概念', '80GB'],
        link: 'https://pan.quark.cn/s/37db7af0aad7',
        linkLabel: '夸克网盘',
      },
      {
        icon: '📚',
        title: '乔伯伯5500词汇系统英语课',
        desc: '127节系统词汇课程，从基础到进阶，科学记忆法掌握5500核心词汇',
        tags: ['词汇', '5500词', '127节', '系统课程'],
        link: 'https://pan.quark.cn/s/fe1f2edbbb28',
        linkLabel: '夸克网盘',
      },
    ],
  },
  {
    id: 'history',
    name: '历史人文',
    icon: '🏛️',
    desc: '历史故事与人文素养',
    resources: [
      {
        icon: '📜',
        title: '孩子必听的100个历史故事',
        desc: '精选100个中国历史故事，生动有趣，培养孩子历史兴趣和人文素养，已完结',
        tags: ['历史故事', '100个', '儿童', '完结'],
        link: 'https://pan.quark.cn/s/260d646d91d5',
        linkLabel: '夸克网盘',
      },
      {
        icon: '📖',
        title: '十三天快速通关高中历史',
        desc: '高中历史高效复习课程，13天系统梳理历史知识点，快速提升历史成绩',
        tags: ['高中历史', '13天', '快速通关', '复习'],
        link: 'https://pan.quark.cn/s/9618fa92528a',
        linkLabel: '夸克网盘',
      },
    ],
  },
  {
    id: 'language',
    name: '小语种学习',
    icon: '🌍',
    desc: '多语种零基础学习资料',
    resources: [
      {
        icon: '🌐',
        title: '26门小语种零基础全套学习资料',
        desc: '全球外语学习资源，涵盖日语、韩语、法语、德语、西班牙语等26门小语种，零基础入门',
        tags: ['小语种', '26门', '零基础', '多语言'],
        link: 'https://pan.quark.cn/s/f67180336b4e',
        linkLabel: '夸克网盘',
      },
      {
        icon: '🇰🇷',
        title: '韩语零基础0-TOPIK4全程班',
        desc: '考神大牛韩语系统课程，从零基础到TOPIK4级，全程指导，适合自学备考',
        tags: ['韩语', 'TOPIK4', '零基础', '全程班'],
        link: 'https://pan.quark.cn/s/9fdfb7c2b17e',
        linkLabel: '夸克网盘',
      },
    ],
  },
  {
    id: 'junior',
    name: '初中资料',
    icon: '📘',
    desc: '初中各科知识点与学霸笔记',
    resources: [
      {
        icon: '📋',
        title: '初中各科知识点梳理',
        desc: '语数英物化生政史地全科知识点系统梳理，重点难点一目了然，复习备考必备',
        tags: ['初中', '知识点', '全科', '梳理'],
        link: 'https://pan.quark.cn/s/74153e93c83e',
        linkLabel: '夸克网盘',
      },
      {
        icon: '📝',
        title: '初中九科学霸笔记',
        desc: '九科学霸手写笔记，无水印高清版，涵盖重点知识点、易错题、解题技巧',
        tags: ['初中', '学霸笔记', '九科', '无水印'],
        link: 'https://pan.quark.cn/s/79183bb66cc5',
        linkLabel: '夸克网盘',
      },
    ],
  },
  {
    id: 'senior',
    name: '高中资料',
    icon: '📕',
    desc: '高中教辅与高考备考资料',
    resources: [
      {
        icon: '📁',
        title: '高中教辅资源汇总合集',
        desc: '高中全科教辅资料大合集，涵盖各科目重点笔记、试卷、练习册，多版本覆盖',
        tags: ['高中', '教辅', '合集', '全科'],
        link: 'https://pan.quark.cn/s/4807ab495ed8',
        linkLabel: '夸克网盘',
      },
      {
        icon: '🎯',
        title: '高考能力提升卷',
        desc: '高考冲刺能力提升试卷，模拟真题训练，查漏补缺，助力高考提分',
        tags: ['高考', '提升卷', '模拟', '冲刺'],
        link: 'https://pan.quark.cn/s/873a9bb68de4',
        linkLabel: '夸克网盘',
      },
    ],
  },
  {
    id: 'method',
    name: '学习方法',
    icon: '🧠',
    desc: '记忆力训练与学霸经验',
    resources: [
      {
        icon: '💡',
        title: '超级记忆力训练课程',
        desc: '16天记忆力提升训练课程，科学记忆方法，提升学习效率，轻松记住知识点',
        tags: ['记忆力', '16天', '训练', '提升'],
        link: 'https://pan.quark.cn/s/00fa9188dd84',
        linkLabel: '夸克网盘',
      },
      {
        icon: '🏆',
        title: '985学霸逆袭学习方法',
        desc: '985学霸亲授学习方法和提分经验，从普通到逆袭，掌握高效学习技巧',
        tags: ['学习方法', '985学霸', '提分', '逆袭'],
        link: 'https://pan.quark.cn/s/6c1fc54308ad',
        linkLabel: '夸克网盘',
      },
    ],
  },
  {
    id: 'comprehensive',
    name: '综合教辅',
    icon: '📁',
    desc: '全科目综合学习资料',
    resources: [
      {
        icon: '📁',
        title: '2025秋小学全学科教辅资料汇总',
        desc: '语文、数学、英语全科目教辅资料合集，含教材、重点笔记、试卷、练习册，多版本覆盖',
        tags: ['全学科', '教辅', '多版本', '合集'],
        link: 'https://pan.quark.cn/s/bae1d2a98cc1',
        linkLabel: '夸克网盘',
      },
      {
        icon: '📋',
        title: '小升初考试真题集',
        desc: '各重点中学小升初考试真题汇总，含数学、语文、英语三科，附详细答案和解析',
        tags: ['小升初', '真题', '重点中学', '带解析'],
        link: 'https://pan.quark.cn/s/fbc1e85d5089',
        linkLabel: '夸克网盘',
      },
    ],
  },
];

export const CATEGORY_SEO: Record<string, { title: string; description: string; keywords: string }> = {
  calligraphy: {
    title: '字帖书法资源 - 免费下载 | 教材工具箱',
    description: '免费下载书法字帖、练字教程，楷书行书隶书多种字体，适合各年龄段练习使用',
    keywords: '字帖下载,书法字帖,练字教程,楷书字帖,行书字帖,免费字帖',
  },
  textbook: {
    title: '电子课本下载 - 免费教科书 | 教材工具箱',
    description: '免费下载小学初中高中电子版教科书，人教版苏教版北师版等多版本全覆盖',
    keywords: '电子课本,教科书下载,电子教材,人教版,苏教版,北师版',
  },
  math: {
    title: '数学学习资料 - 免费下载 | 教材工具箱',
    description: '免费下载小学数学练习卷、奥数训练、口算速算题卡，1-6年级全覆盖',
    keywords: '数学练习卷,小学数学,奥数,口算速算,数学试卷,免费下载',
  },
  chinese: {
    title: '语文学习资料 - 免费下载 | 教材工具箱',
    description: '免费下载语文阅读理解训练、看图写话、作文指导、拼音识字资料',
    keywords: '语文阅读理解,看图写话,作文指导,拼音识字,小学语文',
  },
  english: {
    title: '英语学习资料 - 免费下载 | 教材工具箱',
    description: '免费下载英语自然拼读、音标课、语法课、词汇课、启蒙动画等学习资源',
    keywords: '英语自然拼读,音标课,英语语法,英语词汇,启蒙英语,新概念英语',
  },
  history: {
    title: '历史学习资料 - 免费下载 | 教材工具箱',
    description: '免费下载历史故事、历史复习课程，培养历史兴趣和人文素养',
    keywords: '历史故事,高中历史,历史复习,历史课程,儿童历史',
  },
  language: {
    title: '小语种学习资料 - 免费下载 | 教材工具箱',
    description: '免费下载日语韩语法语德语等26门小语种零基础学习资料',
    keywords: '小语种,日语学习,韩语学习,法语学习,德语学习,零基础',
  },
  junior: {
    title: '初中学习资料 - 免费下载 | 教材工具箱',
    description: '免费下载初中各科知识点梳理、学霸笔记，语数英物化生政史地全科覆盖',
    keywords: '初中资料,初中知识点,学霸笔记,初中复习,中考备考',
  },
  senior: {
    title: '高中学习资料 - 免费下载 | 教材工具箱',
    description: '免费下载高中教辅资料、高考能力提升卷，助力高考冲刺提分',
    keywords: '高中教辅,高考复习,高考真题,高中资料,高考提分',
  },
  method: {
    title: '学习方法课程 - 免费下载 | 教材工具箱',
    description: '免费下载超级记忆力训练课程、985学霸学习方法，提升学习效率',
    keywords: '学习方法,记忆力训练,学霸方法,学习技巧,提分经验',
  },
  comprehensive: {
    title: '综合教辅资料 - 免费下载 | 教材工具箱',
    description: '免费下载小学全学科教辅资料汇总、小升初考试真题集',
    keywords: '综合教辅,小升初真题,教辅资料,全学科,学习资料',
  },
};
