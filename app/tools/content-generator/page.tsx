'use client';

import { useState, useCallback } from 'react';
import ToolNavBar from '@/components/ToolNavBar';

// ===== 类型定义 =====
type Platform = 'zhihu' | 'xiaohongshu' | 'baijiahao' | 'wechat' | 'toutiao' | 'sohu';
type ContentStyle = 'recommend' | 'tutorial' | 'review' | 'parent' | 'teacher';
type ContentLength = 'short' | 'medium' | 'long';

interface PlatformConfig {
  key: Platform;
  name: string;
  icon: string;
  color: string;
}

interface GeneratedContent {
  platform: Platform;
  title: string;
  body: string;
}

// ===== 平台配置 =====
const PLATFORMS: PlatformConfig[] = [
  { key: 'zhihu', name: '知乎', icon: '📖', color: 'blue' },
  { key: 'xiaohongshu', name: '小红书', icon: '📕', color: 'red' },
  { key: 'baijiahao', name: '百家号', icon: '📰', color: 'orange' },
  { key: 'wechat', name: '微信公众号', icon: '💬', color: 'green' },
  { key: 'toutiao', name: '头条号', icon: '📰', color: 'red' },
  { key: 'sohu', name: '搜狐号', icon: '🦊', color: 'orange' },
];

const STYLES: { key: ContentStyle; name: string; icon: string }[] = [
  { key: 'recommend', name: '种草推荐', icon: '🌿' },
  { key: 'tutorial', name: '使用教程', icon: '📖' },
  { key: 'review', name: '评测对比', icon: '⚖️' },
  { key: 'parent', name: '家长经验', icon: '👨‍👩‍👧' },
  { key: 'teacher', name: '老师推荐', icon: '👩‍🏫' },
];

const LENGTHS: { key: ContentLength; name: string; desc: string }[] = [
  { key: 'short', name: '短文', desc: '300字' },
  { key: 'medium', name: '中文', desc: '800字' },
  { key: 'long', name: '长文', desc: '1500字' },
];

// ===== 文案模板库 =====

// 痛点引入开头
const OPENING_PAIN = [
  '作为一名{role}，我深知{pain_point}的困扰。每天晚上辅导孩子写作业，光是找合适的练习题就要花大半天时间，网上搜到的资源要么要付费，要么质量参差不齐。直到最近发现了{keywords}，才真正解决了这个大问题。',
  '不知道大家有没有同样的烦恼：{pain_point}？我之前为了给孩子找一份合适的练习卷，翻遍了各种家长群、公众号，下载了一堆乱七八糟的文件。后来偶然接触到{keywords}，简直打开了新世界的大门。',
  '说实话，在找到{keywords}之前，我对{pain_point}这件事已经快绝望了。市面上的工具要么收费贵得离谱，要么功能单一根本不好用。直到一位同行推荐了这个神器，我才意识到原来可以这么轻松。',
  '每次到了{scenario}的时候，我就特别头疼。{pain_point}，效率低不说，效果还不理想。后来我尝试了{keywords}，没想到从此告别了这个烦恼。',
];

// 数据引入开头
const OPENING_DATA = [
  '根据最新教育调查数据显示，超过78%的家长表示{pain_point}是日常教育中最大的痛点之一。而事实上，借助{keywords}这类工具，完全可以轻松解决这个问题。今天就来详细聊聊这个话题。',
  '一项针对全国5000名小学家长的调查显示，平均每个家庭每周要花费3.5小时在{pain_point}上。这个数据让我非常震惊，同时也让我更加庆幸自己早早发现了{keywords}这个宝藏工具。',
  '你知道吗？据统计，使用{keywords}的家长，在{scenario}方面节省的时间平均达到了每周4小时以上。这不是夸张，而是真实的使用数据。今天就和大家分享一下我的使用心得。',
];

// 故事引入开头
const OPENING_STORY = [
  '记得去年这个时候，我家孩子刚上{grade}，数学成绩一直上不去。老师建议多做练习，但我实在没时间每天出题。后来在家长群里，一位妈妈分享了{keywords}，我抱着试试看的心态用了用，没想到效果出奇的好。',
  '上周五放学接孩子，班主任特意找到我说："你家孩子最近进步很大啊，练习做得特别好。"我笑了笑，心里暗暗感谢{keywords}。要不是这个工具，我可能还在每天手写出题的苦海里挣扎。',
  '前两天和闺蜜聊天，她抱怨说每天给孩子找练习题太累了。我立马给她推荐了{keywords}，她用了一周就跑来感谢我。今天就把这个好东西也分享给大家。',
];

// 工具介绍模板
const TOOL_INTRO = [
  '{keywords}是一款专为小学教育设计的在线工具平台。它最大的特点就是免费、好用、功能全面。不需要下载安装，打开网页就能直接使用，对于不太擅长使用电子设备的家长来说也非常友好。',
  '简单来说，{keywords}就是一个"一站式"的小学教学辅助平台。它涵盖了数学练习卷、字帖生成、古诗词默写、单元测试等多个功能模块，基本上小学阶段需要的教学工具都能在这里找到。',
  '我之所以强烈推荐{keywords}，是因为它真正做到了"让教学更简单"。整个平台的设计理念就是降低老师和家长的负担，让每一个孩子都能获得高质量的练习资源。',
  '用过这么多教育类工具，{keywords}是我目前体验最好的一个。首先是完全免费，没有任何隐藏收费；其次是操作简单，几步就能生成需要的练习内容；最重要的是生成的题目质量很高，完全符合教学大纲要求。',
];

// 功能亮点模板
const FEATURE_HIGHLIGHTS = [
  '【核心功能亮点】\n1. 数学练习卷：支持加减乘除、竖式、分数等多种题型，难度可调，一键生成PDF\n2. 字帖生成器：田字格/米字格自由切换，支持楷体、宋体等多种字体\n3. 古诗词默写：收录240首必背古诗，支持填空默写和全诗默写两种模式\n4. 单元测试卷：覆盖数语英科四科，人教版1-6年级上下册全匹配',
  '【为什么值得用？】\n- 完全免费，不需要注册就能使用\n- 题目质量高，紧贴教学大纲\n- 支持PDF导出，打印效果清晰\n- 操作简单，三步完成出题\n- 持续更新，功能越来越丰富',
  '【使用体验】\n我最常用的功能是数学练习卷和字帖生成。数学练习卷可以自定义难度和题量，生成的题目格式规范，打印出来效果非常好。字帖生成器支持多种格子样式，孩子练字积极性明显提高了。',
];

// 结尾模板
const ENDING_TEMPLATES = [
  '总的来说，{keywords}真的是我目前用过最实用的小学教学辅助工具。如果你也在为{pain_point}而烦恼，强烈建议试试看。毕竟免费的东西，试了不亏！\n\n觉得有用的话，记得点赞收藏，也欢迎在评论区分享你的使用体验~',
  '以上就是我对{keywords}的全面介绍和使用心得。作为一个用了大半年的"老用户"，我可以负责任地说，这个工具确实能帮到很多家长和老师。如果你觉得这篇文章对你有帮助，不妨点个赞支持一下，也欢迎转发给有需要的朋友。',
  '教育是一场马拉松，好的工具能让我们跑得更轻松。{keywords}就是这样一个能让你事半功倍的利器。希望这篇文章能帮到正在为{pain_point}而苦恼的你。有任何问题欢迎在评论区留言，我会一一回复。',
  '如果你也想提升孩子的学习效率，或者减轻自己辅导作业的负担，{keywords}绝对值得一试。链接就在这里，打开就能用，不需要下载任何东西。希望每个孩子都能快乐学习，健康成长！',
];

// 小红书专用模板
const XHS_TITLES = [
  '绝了！这个{keywords}太香了🔥家长老师必看',
  '挖到宝了！免费{keywords}分享✨后悔没早点知道',
  '宝妈必看！{keywords}亲测好用😭辅导作业不焦虑了',
  '老师都在用的{keywords}，免费又好用📚建议收藏',
  '不允许还有人不知道这个{keywords}！太绝了吧',
  '救命！有了这个{keywords}再也不用到处找题了',
];

const XHS_BODY_TEMPLATES = [
  '姐妹们！！！今天必须给大家安利一个超级好用的{keywords}✨\n\n我之前每天晚上辅导孩子写作业都要崩溃😭到处找练习题，质量还参差不齐...\n\n直到发现了这个宝藏工具！！！\n\n🌟 主要功能：\n✅ 数学练习卷 - 一键生成，难度可调\n✅ 字帖生成 - 田字格米字格都有\n✅ 古诗词默写 - 240首必背古诗\n✅ 单元测试 - 四科全覆盖\n\n💡 最关键的是：完全免费！不用下载！打开网页就能用！\n\n我现在每天花5分钟就能准备好第二天的练习内容，简直不要太爽👍\n\n#小学教学工具 #免费试卷生成器 #辅导作业 #小学数学 #家长必看 #教育工具 #免费资源',
  '家人们谁懂啊！！！这个{keywords}真的绝了😭😭😭\n\n作为一个每天辅导作业到崩溃的宝妈，我真的太需要这种工具了！！！\n\n之前找练习题：\n❌ 网上搜 - 全是广告\n❌ 买教辅 - 孩子做不完\n❌ 手写出题 - 累到怀疑人生\n\n现在用这个工具：\n✅ 打开网页就能用\n✅ 几秒钟生成练习卷\n✅ 直接打印PDF\n✅ 完全免费！！！\n\n而且题目质量特别好，紧贴教学大纲，老师看了都说好👍\n\n真心建议每个家长都收藏起来！！！\n\n#小学教学工具 #免费试卷 #辅导作业不焦虑 #宝妈分享 #教育工具 #学习神器',
];

// 百家号专用模板
const BJJH_TITLES = [
  '2026年最值得使用的{keywords}，老师家长都在用！',
  '别再花钱买练习题了！这款免费{keywords}让你省时又省力',
  '小学老师强烈推荐：这款{keywords}彻底改变了我的教学方式',
  '用了半年{keywords}，我总结了这些使用技巧（附详细教程）',
];

// 微信公众号专用模板
const WECHAT_INTRO = [
  '各位家长朋友们好，今天想和大家分享一个我最近发现的宝藏教育工具。\n\n作为一名教育工作者，我接触过很多教学辅助工具，但真正能让我推荐给家长和同事的，寥寥无几。而{keywords}就是其中之一。',
  '大家好，今天这篇文章可能会帮很多家长省下大量时间和精力。\n\n最近有不少家长私信问我，有没有好用的{keywords}推荐。今天我就来详细介绍一下我一直在用的这个工具。',
];

const WECHAT_OUTRO = [
  '---\n\n📌 如果你觉得这篇文章对你有帮助，欢迎点击右下角的"在看"按钮，也欢迎转发给有需要的家长朋友。\n\n关注本公众号，获取更多教育干货和实用工具推荐。\n\n我们下期见！',
  '---\n\n💬 你在使用{keywords}的过程中有什么心得体会？欢迎在评论区留言交流！\n\n如果觉得有用，别忘了点个"赞"和"在看"哦~\n\n👇 扫码关注公众号，第一时间获取最新教育资讯',
];

// 头条号专用模板
const TOUTIAO_TITLES = [
  '教育行业新变革：免费{keywords}正在改变千万家庭的学习方式',
  '记者调查：超八成家长不知道这款免费的{keywords}',
  '一线教师揭秘：为什么越来越多的老师开始使用{keywords}？',
  '深度测评：这款{keywords}到底好不好用？我们用数据说话',
];

const TOUTIAO_INTRO = [
  '【教育观察】随着在线教育工具的快速发展，越来越多的家长和教师开始借助数字化工具提升教学效率。近日，一款名为{keywords}的免费工具在教育圈引发了广泛关注。',
  '近日，一款免费的{keywords}在家长群和教师圈中迅速走红。记者了解到，该工具凭借其丰富的功能和简洁的操作体验，已经帮助大量家庭解决了{pain_point}的难题。',
];

// 搜狐号专用模板
const SOHU_TITLES = [
  '教育专栏 | {keywords}深度评测：免费工具能否替代付费产品？',
  '名师推荐 | 我为什么向所有家长推荐这款{keywords}',
  '教育观察 | 从{keywords}看在线教育工具的发展趋势',
];

const SOHU_INTRO = [
  '在教育信息化的大背景下，各类教学辅助工具层出不穷。作为一名从事教育工作十余年的教师，笔者近期对多款{keywords}进行了深度体验和评测，今天就来和大家分享我的发现。',
  '近年来，随着"双减"政策的深入推进，越来越多的家长开始关注如何高效利用课后时间进行家庭辅导。在这个过程中，{keywords}成为了不少家庭的新选择。今天，我们就来深入探讨一下这个话题。',
];

// ===== 角色和场景数据 =====
const ROLES = ['家长', '小学老师', '教育工作者', '宝妈', '班主任'];
const GRADES = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级'];
const PAIN_POINTS = [
  '给孩子找合适的练习题',
  '每天手写出题太耗时',
  '网上教育资源质量参差不齐',
  '辅导孩子写作业效率低',
  '找不到免费高质量的教学工具',
  '出题排版太麻烦',
];
const SCENARIOS = [
  '期末复习',
  '日常练习',
  '课后辅导',
  '周末补习',
  '假期预习',
];

// ===== 工具函数 =====
function randomPick<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

function randomPicks<T>(arr: T[], count: number): T[] {
  const shuffled = [...arr].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
}

function replacePlaceholders(template: string, keywords: string): string {
  return template
    .replace(/\{keywords\}/g, keywords)
    .replace(/\{role\}/g, randomPick(ROLES))
    .replace(/\{grade\}/g, randomPick(GRADES))
    .replace(/\{pain_point\}/g, randomPick(PAIN_POINTS))
    .replace(/\{scenario\}/g, randomPick(SCENARIOS));
}

function getLengthMultiplier(length: ContentLength): number {
  switch (length) {
    case 'short': return 0.4;
    case 'medium': return 1;
    case 'long': return 1.8;
  }
}

function truncateToLength(text: string, targetChars: number): string {
  if (text.length <= targetChars) return text;
  const sentences = text.split(/[。！？\n]/).filter(s => s.trim());
  let result = '';
  for (const sentence of sentences) {
    if ((result + sentence + '。').length > targetChars) break;
    result += sentence + '。';
  }
  return result.trim();
}

// ===== 文案生成器 =====
function generateContent(
  platform: Platform,
  style: ContentStyle,
  length: ContentLength,
  keywords: string,
  includeLink: boolean,
): GeneratedContent {
  const multiplier = getLengthMultiplier(length);
  const targetChars = Math.round({ short: 300, medium: 800, long: 1500 }[length] * multiplier);
  const linkText = includeLink ? `\n\n🔗 工具链接：https://www.skillxm.cn` : '';

  switch (platform) {
    case 'zhihu':
      return generateZhihuContent(style, length, keywords, includeLink, targetChars, linkText);
    case 'xiaohongshu':
      return generateXiaohongshuContent(keywords, includeLink, targetChars, linkText);
    case 'baijiahao':
      return generateBaijiahaoContent(style, length, keywords, includeLink, targetChars, linkText);
    case 'wechat':
      return generateWechatContent(style, length, keywords, includeLink, targetChars, linkText);
    case 'toutiao':
      return generateToutiaoContent(style, length, keywords, includeLink, targetChars, linkText);
    case 'sohu':
      return generateSohuContent(style, length, keywords, includeLink, targetChars, linkText);
  }
}

function generateZhihuContent(
  style: ContentStyle,
  length: ContentLength,
  keywords: string,
  includeLink: boolean,
  targetChars: number,
  linkText: string,
): GeneratedContent {
  const openingPool = [OPENING_PAIN, OPENING_DATA, OPENING_STORY].flat();
  const opening = replacePlaceholders(randomPick(openingPool), keywords);
  const intro = replacePlaceholders(randomPick(TOOL_INTRO), keywords);
  const features = randomPick(FEATURE_HIGHLIGHTS).replace(/\{keywords\}/g, keywords);
  const ending = replacePlaceholders(randomPick(ENDING_TEMPLATES), keywords);

  const stylePrefix = getStylePrefix(style, keywords);
  const body = [stylePrefix, opening, '\n\n', intro, '\n\n', features, '\n\n', ending, linkText].join('');
  const title = generateTitle(style, keywords, 'zhihu');

  return {
    platform: 'zhihu',
    title,
    body: truncateToLength(body, targetChars),
  };
}

function generateXiaohongshuContent(
  keywords: string,
  includeLink: boolean,
  targetChars: number,
  linkText: string,
): GeneratedContent {
  const title = replacePlaceholders(randomPick(XHS_TITLES), keywords);
  const body = replacePlaceholders(randomPick(XHS_BODY_TEMPLATES), keywords) + (includeLink ? '\n\n🔗 链接在评论区置顶～' : '');

  return {
    platform: 'xiaohongshu',
    title,
    body: truncateToLength(body, targetChars),
  };
}

function generateBaijiahaoContent(
  style: ContentStyle,
  length: ContentLength,
  keywords: string,
  includeLink: boolean,
  targetChars: number,
  linkText: string,
): GeneratedContent {
  const title = replacePlaceholders(randomPick(BJJH_TITLES), keywords);
  const opening = replacePlaceholders(randomPick(OPENING_PAIN), keywords);
  const intro = replacePlaceholders(randomPick(TOOL_INTRO), keywords);
  const features = randomPick(FEATURE_HIGHLIGHTS).replace(/\{keywords\}/g, keywords);
  const ending = replacePlaceholders(randomPick(ENDING_TEMPLATES), keywords);

  const body = [opening, '\n\n', intro, '\n\n', features, '\n\n', ending, linkText].join('');
  return {
    platform: 'baijiahao',
    title,
    body: truncateToLength(body, targetChars),
  };
}

function generateWechatContent(
  style: ContentStyle,
  length: ContentLength,
  keywords: string,
  includeLink: boolean,
  targetChars: number,
  linkText: string,
): GeneratedContent {
  const title = `${keywords}使用指南：${randomPick(['全面评测与使用心得', '从入门到精通', '老师家长必看的使用攻略', '手把手教你高效使用'])}`;
  const intro = replacePlaceholders(randomPick(WECHAT_INTRO), keywords);
  const opening = replacePlaceholders(randomPick(OPENING_PAIN), keywords);
  const toolIntro = replacePlaceholders(randomPick(TOOL_INTRO), keywords);
  const features = randomPick(FEATURE_HIGHLIGHTS).replace(/\{keywords\}/g, keywords);
  const outro = replacePlaceholders(randomPick(WECHAT_OUTRO), keywords);

  const body = [intro, '\n\n', opening, '\n\n', toolIntro, '\n\n', features, '\n\n', outro, linkText].join('');
  return {
    platform: 'wechat',
    title,
    body: truncateToLength(body, targetChars),
  };
}

function generateToutiaoContent(
  style: ContentStyle,
  length: ContentLength,
  keywords: string,
  includeLink: boolean,
  targetChars: number,
  linkText: string,
): GeneratedContent {
  const title = replacePlaceholders(randomPick(TOUTIAO_TITLES), keywords);
  const intro = replacePlaceholders(randomPick(TOUTIAO_INTRO), keywords);
  const toolIntro = replacePlaceholders(randomPick(TOOL_INTRO), keywords);
  const features = randomPick(FEATURE_HIGHLIGHTS).replace(/\{keywords\}/g, keywords);
  const ending = replacePlaceholders(randomPick(ENDING_TEMPLATES), keywords);

  const body = [intro, '\n\n', toolIntro, '\n\n', features, '\n\n', ending, linkText].join('');
  return {
    platform: 'toutiao',
    title,
    body: truncateToLength(body, targetChars),
  };
}

function generateSohuContent(
  style: ContentStyle,
  length: ContentLength,
  keywords: string,
  includeLink: boolean,
  targetChars: number,
  linkText: string,
): GeneratedContent {
  const title = replacePlaceholders(randomPick(SOHU_TITLES), keywords);
  const intro = replacePlaceholders(randomPick(SOHU_INTRO), keywords);
  const toolIntro = replacePlaceholders(randomPick(TOOL_INTRO), keywords);
  const features = randomPick(FEATURE_HIGHLIGHTS).replace(/\{keywords\}/g, keywords);
  const ending = replacePlaceholders(randomPick(ENDING_TEMPLATES), keywords);

  const body = [intro, '\n\n', toolIntro, '\n\n', features, '\n\n', ending, linkText].join('');
  return {
    platform: 'sohu',
    title,
    body: truncateToLength(body, targetChars),
  };
}

function getStylePrefix(style: ContentStyle, keywords: string): string {
  switch (style) {
    case 'recommend':
      return `【好物推荐】今天给大家推荐一款非常实用的${keywords}，亲测好用，值得收藏。`;
    case 'tutorial':
      return `【使用教程】很多朋友问我怎么用${keywords}，今天出一篇详细教程，手把手教大家。`;
    case 'review':
      return `【深度评测】用了市面上十几款同类产品后，我来客观评价一下这款${keywords}。`;
    case 'parent':
      return `【家长经验分享】作为一个过来人，我想聊聊${keywords}是如何帮我解决辅导难题的。`;
    case 'teacher':
      return `【教师视角】作为一名一线教师，我来谈谈${keywords}在实际教学中的应用价值。`;
  }
}

function generateTitle(style: ContentStyle, keywords: string, platform: string): string {
  const titleTemplates: Record<ContentStyle, string[]> = {
    recommend: [
      `强烈推荐！这款${keywords}让我省了太多时间`,
      `用了三个月${keywords}，说说我的真实感受`,
      `为什么我每天都在用这款${keywords}？`,
    ],
    tutorial: [
      `${keywords}使用教程：从零开始手把手教你`,
      `新手必看！${keywords}完整使用指南`,
      `${keywords}怎么用？一篇文章教会你`,
    ],
    review: [
      `深度测评：${keywords}到底值不值得用？`,
      `对比了10款同类产品，${keywords}排第一`,
      `${keywords}真实体验报告：优缺点全解析`,
    ],
    parent: [
      `家长亲测：${keywords}如何帮我解决辅导难题`,
      `作为一个三年级家长，我是这样用${keywords}的`,
      `辅导作业不再崩溃，多亏了这个${keywords}`,
    ],
    teacher: [
      `一线教师推荐：${keywords}在课堂教学中的应用`,
      `为什么我向所有家长推荐${keywords}？`,
      `从教师角度看${keywords}：真正好用的教学工具长什么样`,
    ],
  };
  return randomPick(titleTemplates[style]);
}

// ===== 复制到剪贴板 =====
async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    // fallback
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand('copy');
      return true;
    } catch {
      return false;
    } finally {
      document.body.removeChild(textarea);
    }
  }
}

// ===== 主组件 =====
export default function ContentGeneratorPage() {
  // 配置状态
  const [selectedPlatforms, setSelectedPlatforms] = useState<Set<Platform>>(new Set(['zhihu', 'xiaohongshu']));
  const [contentStyle, setContentStyle] = useState<ContentStyle>('recommend');
  const [contentLength, setContentLength] = useState<ContentLength>('medium');
  const [keywords, setKeywords] = useState('小学教学工具 免费试卷生成器');
  const [includeLink, setIncludeLink] = useState(true);

  // 生成结果
  const [generatedContents, setGeneratedContents] = useState<GeneratedContent[]>([]);
  const [activeTab, setActiveTab] = useState<Platform>('zhihu');
  const [isGenerating, setIsGenerating] = useState(false);
  const [copiedPlatform, setCopiedPlatform] = useState<Platform | null>(null);

  // 平台选择切换
  const togglePlatform = useCallback((platform: Platform) => {
    setSelectedPlatforms(prev => {
      const next = new Set(prev);
      if (next.has(platform)) {
        if (next.size > 1) next.delete(platform);
      } else {
        next.add(platform);
      }
      return next;
    });
  }, []);

  // 生成文案
  const handleGenerate = useCallback(() => {
    if (selectedPlatforms.size === 0) return;
    setIsGenerating(true);

    // 模拟短暂延迟，增强体验
    setTimeout(() => {
      const results: GeneratedContent[] = Array.from(selectedPlatforms).map(platform =>
        generateContent(platform, contentStyle, contentLength, keywords, includeLink)
      );
      setGeneratedContents(results);
      setActiveTab(results[0].platform);
      setIsGenerating(false);
    }, 600);
  }, [selectedPlatforms, contentStyle, contentLength, keywords, includeLink]);

  // 复制文案
  const handleCopy = useCallback(async (content: GeneratedContent) => {
    const fullText = `${content.title}\n\n${content.body}`;
    const success = await copyToClipboard(fullText);
    if (success) {
      setCopiedPlatform(content.platform);
      setTimeout(() => setCopiedPlatform(null), 2000);
    }
  }, []);

  // 复制全部文案
  const handleCopyAll = useCallback(async () => {
    const allText = generatedContents
      .map(c => `【${PLATFORMS.find(p => p.key === c.platform)?.name}】\n${c.title}\n\n${c.body}`)
      .join('\n\n' + '='.repeat(40) + '\n\n');
    const success = await copyToClipboard(allText);
    if (success) {
      setCopiedPlatform('all' as Platform);
      setTimeout(() => setCopiedPlatform(null), 2000);
    }
  }, [generatedContents]);

  const activeContent = generatedContents.find(c => c.platform === activeTab);

  return (
    <div className="min-h-screen bg-[#0f0f0f] text-white">
      <ToolNavBar currentPath="/tools/content-generator" title="文案生成器" />

      {/* 主内容区 */}
      <main className="pt-20 pb-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        {/* 页面标题 */}
        <div className="text-center mb-10">
          <h1 className="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-rose-400 to-pink-500 bg-clip-text text-transparent mb-3">
            多平台种草文案生成器
          </h1>
          <p className="text-gray-400 text-sm sm:text-base max-w-2xl mx-auto">
            一键生成知乎、小红书、百家号、微信公众号等多平台推广文案，支持多种风格和长度，SEO关键词自动嵌入
          </p>
        </div>

        {/* 主体布局：左侧配置 + 右侧预览 */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* 左侧：配置面板 */}
          <div className="lg:col-span-4">
            <div className="bg-[#1a1a1a] rounded-2xl border border-white/10 p-6 sticky top-20">
              <h2 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <span className="w-1 h-5 bg-rose-500 rounded-full" />
                配置面板
              </h2>

              {/* 平台选择 */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-300 mb-3">
                  目标平台 <span className="text-gray-500 text-xs">（可多选）</span>
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {PLATFORMS.map(p => (
                    <button
                      key={p.key}
                      onClick={() => togglePlatform(p.key)}
                      className={`flex items-center gap-2 px-3 py-2.5 rounded-xl text-sm transition-all border ${
                        selectedPlatforms.has(p.key)
                          ? 'bg-rose-500/15 border-rose-500/40 text-rose-300'
                          : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10 hover:text-gray-300'
                      }`}
                    >
                      <span>{p.icon}</span>
                      <span>{p.name}</span>
                      {selectedPlatforms.has(p.key) && (
                        <span className="ml-auto text-rose-400 text-xs">✓</span>
                      )}
                    </button>
                  ))}
                </div>
              </div>

              {/* 文案风格 */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-300 mb-3">文案风格</label>
                <div className="grid grid-cols-1 gap-2">
                  {STYLES.map(s => (
                    <button
                      key={s.key}
                      onClick={() => setContentStyle(s.key)}
                      className={`flex items-center gap-2 px-3 py-2.5 rounded-xl text-sm transition-all border text-left ${
                        contentStyle === s.key
                          ? 'bg-rose-500/15 border-rose-500/40 text-rose-300'
                          : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10 hover:text-gray-300'
                      }`}
                    >
                      <span>{s.icon}</span>
                      <span>{s.name}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* 文案长度 */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-300 mb-3">文案长度</label>
                <div className="flex gap-2">
                  {LENGTHS.map(l => (
                    <button
                      key={l.key}
                      onClick={() => setContentLength(l.key)}
                      className={`flex-1 px-3 py-2.5 rounded-xl text-sm transition-all border text-center ${
                        contentLength === l.key
                          ? 'bg-rose-500/15 border-rose-500/40 text-rose-300'
                          : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10 hover:text-gray-300'
                      }`}
                    >
                      <div className="font-medium">{l.name}</div>
                      <div className="text-xs opacity-70">{l.desc}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* 目标关键词 */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-300 mb-2">目标关键词</label>
                <input
                  type="text"
                  value={keywords}
                  onChange={e => setKeywords(e.target.value)}
                  placeholder="输入目标关键词，用空格分隔"
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-rose-500/50 focus:ring-1 focus:ring-rose-500/25 transition-all"
                />
                <p className="text-xs text-gray-500 mt-1.5">关键词将自动嵌入到标题和正文中</p>
              </div>

              {/* 包含工具链接 */}
              <div className="mb-8">
                <label className="flex items-center justify-between cursor-pointer">
                  <span className="text-sm font-medium text-gray-300">包含工具链接</span>
                  <button
                    onClick={() => setIncludeLink(!includeLink)}
                    className={`relative w-11 h-6 rounded-full transition-colors ${
                      includeLink ? 'bg-rose-500' : 'bg-white/20'
                    }`}
                  >
                    <span
                      className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform ${
                        includeLink ? 'translate-x-5' : 'translate-x-0'
                      }`}
                    />
                  </button>
                </label>
              </div>

              {/* 生成按钮 */}
              <button
                onClick={handleGenerate}
                disabled={selectedPlatforms.size === 0 || isGenerating}
                className={`w-full py-3.5 rounded-xl font-medium text-sm transition-all ${
                  selectedPlatforms.size === 0 || isGenerating
                    ? 'bg-white/10 text-gray-500 cursor-not-allowed'
                    : 'bg-gradient-to-r from-rose-500 to-pink-600 text-white hover:from-rose-600 hover:to-pink-700 shadow-lg shadow-rose-500/25 active:scale-[0.98]'
                }`}
              >
                {isGenerating ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    生成中...
                  </span>
                ) : (
                  `生成文案（${selectedPlatforms.size}个平台）`
                )}
              </button>
            </div>
          </div>

          {/* 右侧：预览区域 */}
          <div className="lg:col-span-8">
            {generatedContents.length === 0 ? (
              /* 空状态 */
              <div className="bg-[#1a1a1a] rounded-2xl border border-white/10 p-12 text-center">
                <div className="text-6xl mb-4 opacity-30">✏️</div>
                <h3 className="text-lg font-medium text-gray-400 mb-2">选择平台并生成文案</h3>
                <p className="text-sm text-gray-500 max-w-md mx-auto">
                  在左侧配置面板中选择目标平台、文案风格和长度，然后点击生成按钮即可一键生成多平台推广文案
                </p>
              </div>
            ) : (
              <div className="bg-[#1a1a1a] rounded-2xl border border-white/10 overflow-hidden">
                {/* 标签页头部 */}
                <div className="flex items-center border-b border-white/10 overflow-x-auto">
                  {generatedContents.map(content => {
                    const platform = PLATFORMS.find(p => p.key === content.platform);
                    return (
                      <button
                        key={content.platform}
                        onClick={() => setActiveTab(content.platform)}
                        className={`flex items-center gap-2 px-4 py-3.5 text-sm whitespace-nowrap border-b-2 transition-all ${
                          activeTab === content.platform
                            ? 'border-rose-500 text-white bg-white/5'
                            : 'border-transparent text-gray-400 hover:text-gray-300 hover:bg-white/5'
                        }`}
                      >
                        <span>{platform?.icon}</span>
                        <span>{platform?.name}</span>
                      </button>
                    );
                  })}
                  <div className="ml-auto px-4 shrink-0">
                    <button
                      onClick={handleCopyAll}
                      className="text-xs text-gray-400 hover:text-rose-400 transition-colors flex items-center gap-1"
                    >
                      {copiedPlatform === ('all' as Platform) ? (
                        <>
                          <span>✓</span> 已复制全部
                        </>
                      ) : (
                        <>
                          <span>📋</span> 复制全部
                        </>
                      )}
                    </button>
                  </div>
                </div>

                {/* 内容预览 */}
                {activeContent && (
                  <div className="p-6 sm:p-8">
                    {/* 平台标识 */}
                    <div className="flex items-center justify-between mb-6">
                      <div className="flex items-center gap-2">
                        <span className="text-2xl">{PLATFORMS.find(p => p.key === activeContent.platform)?.icon}</span>
                        <span className="text-sm text-gray-400">
                          {PLATFORMS.find(p => p.key === activeContent.platform)?.name}风格预览
                        </span>
                      </div>
                      <button
                        onClick={() => handleCopy(activeContent)}
                        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs transition-all ${
                          copiedPlatform === activeContent.platform
                            ? 'bg-green-500/15 text-green-400 border border-green-500/30'
                            : 'bg-white/5 text-gray-400 border border-white/10 hover:bg-white/10 hover:text-gray-300'
                        }`}
                      >
                        {copiedPlatform === activeContent.platform ? (
                          <><span>✓</span> 已复制</>
                        ) : (
                          <><span>📋</span> 复制文案</>
                        )}
                      </button>
                    </div>

                    {/* 标题 */}
                    <h2 className="text-xl sm:text-2xl font-bold text-white mb-4 leading-relaxed">
                      {activeContent.title}
                    </h2>

                    {/* 分隔线 */}
                    <div className="w-16 h-0.5 bg-rose-500/50 rounded-full mb-6" />

                    {/* 正文 */}
                    <div className="text-gray-300 text-sm sm:text-base leading-relaxed whitespace-pre-line">
                      {activeContent.body}
                    </div>

                    {/* 字数统计 */}
                    <div className="mt-6 pt-4 border-t border-white/10 flex items-center justify-between">
                      <span className="text-xs text-gray-500">
                        共 {activeContent.title.length + activeContent.body.length} 字
                      </span>
                      <span className="text-xs text-gray-500">
                        {LENGTHS.find(l => l.key === contentLength)?.desc}
                      </span>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* 使用说明 */}
        <section className="mt-16">
          <h2 className="text-2xl font-bold text-white mb-8 text-center">使用说明</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                step: '01',
                title: '选择平台和风格',
                desc: '在左侧配置面板中选择需要生成文案的目标平台（支持多选），然后选择文案风格和长度。',
              },
              {
                step: '02',
                title: '设置关键词',
                desc: '输入目标推广关键词，关键词将自动嵌入到生成的标题和正文中，提升SEO效果。',
              },
              {
                step: '03',
                title: '生成并复制',
                desc: '点击生成按钮，即可在右侧预览区查看各平台文案。支持一键复制单篇或全部文案。',
              },
            ].map(item => (
              <div
                key={item.step}
                className="bg-[#1a1a1a] rounded-2xl border border-white/10 p-6 hover:border-rose-500/30 transition-colors"
              >
                <div className="text-3xl font-bold text-rose-500/30 mb-3">{item.step}</div>
                <h3 className="text-base font-semibold text-white mb-2">{item.title}</h3>
                <p className="text-sm text-gray-400 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* FAQ */}
        <section className="mt-16">
          <h2 className="text-2xl font-bold text-white mb-8 text-center">常见问题</h2>
          <div className="max-w-3xl mx-auto space-y-4">
            {[
              {
                q: '生成的文案是否可以直接发布？',
                a: '生成的文案是基于模板组合的初稿，建议发布前根据实际情况进行适当修改和润色，确保内容符合平台规范和个人风格。',
              },
              {
                q: '支持哪些平台的文案格式？',
                a: '目前支持知乎、小红书、百家号、微信公众号、头条号、搜狐号六个平台。每个平台的文案格式和风格都经过专门优化，符合各平台的内容特点。',
              },
              {
                q: '文案生成是否需要联网或调用AI接口？',
                a: '不需要。文案生成完全在浏览器本地完成，使用预设模板和随机组合算法，不会调用任何外部API，也不会上传您的数据。',
              },
              {
                q: '如何让生成的文案效果更好？',
                a: '建议：1) 使用精准的关键词，避免过于宽泛；2) 选择与目标平台匹配的文案风格；3) 生成后根据实际需求进行个性化修改；4) 多次生成选择最佳版本。',
              },
            ].map((faq, i) => (
              <div
                key={i}
                className="bg-[#1a1a1a] rounded-2xl border border-white/10 p-6"
              >
                <h3 className="text-base font-semibold text-white mb-2 flex items-start gap-2">
                  <span className="text-rose-500 shrink-0">Q</span>
                  {faq.q}
                </h3>
                <p className="text-sm text-gray-400 leading-relaxed pl-6">{faq.a}</p>
              </div>
            ))}
          </div>
        </section>

        {/* 相关工具推荐 */}
        <section className="mt-16">
          <h2 className="text-2xl font-bold text-white mb-8 text-center">相关工具推荐</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
            {[
              { name: '数学练习卷', icon: '🧮', href: '/tools/math-worksheet', desc: '一键出题PDF导出' },
              { name: '字帖生成器', icon: '✍️', href: '/tools/calligraphy', desc: '田字格/米字格模板' },
              { name: '古诗词默写', icon: '📜', href: '/tools/poem-memo', desc: '必背古诗默写练习' },
              { name: '单元测试卷', icon: '📋', href: '/tools/unit-test', desc: '数语英科全科试卷' },
              { name: '口算速练', icon: '⚡', href: '/tools/mental-math', desc: '在线计时练习' },
            ].map(tool => (
              <a
                key={tool.href}
                href={tool.href}
                className="bg-[#1a1a1a] rounded-2xl border border-white/10 p-4 hover:border-rose-500/30 transition-all group block"
              >
                <div className="text-2xl mb-2">{tool.icon}</div>
                <div className="text-sm font-medium text-white group-hover:text-rose-400 transition-colors">
                  {tool.name}
                </div>
                <div className="text-xs text-gray-500 mt-1">{tool.desc}</div>
              </a>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
