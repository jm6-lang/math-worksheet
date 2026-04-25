'use client';

import { useState, useRef } from 'react';
import ToolGuide from '@/components/ToolGuide';
import { toolGuides } from '@/lib/toolGuides';

// ===== 内置拼音词库（去重后共 530 条）=====
const PY: Record<string, string> = {
  '一': 'yī',
  '二': 'èr',
  '三': 'sān',
  '四': 'sì',
  '五': 'wǔ',
  '六': 'liù',
  '七': 'qī',
  '八': 'bā',
  '九': 'jiǔ',
  '十': 'shí',
  '百': 'bǎi',
  '千': 'qiān',
  '万': 'wàn',
  '亿': 'yì',
  '元': 'yuán',
  '角': 'jiǎo',
  '分': 'fēn',
  '零': 'líng',
  '两': 'liǎng',
  '上': 'shàng',
  '下': 'xià',
  '左': 'zuǒ',
  '右': 'yòu',
  '前': 'qián',
  '后': 'hòu',
  '中': 'zhōng',
  '里': 'lǐ',
  '外': 'wài',
  '东': 'dōng',
  '西': 'xī',
  '南': 'nán',
  '北': 'běi',
  '大': 'dà',
  '小': 'xiǎo',
  '多': 'duō',
  '少': 'shǎo',
  '高': 'gāo',
  '矮': 'ǎi',
  '长': 'cháng',
  '短': 'duǎn',
  '远': 'yuǎn',
  '近': 'jìn',
  '快': 'kuài',
  '慢': 'màn',
  '胖': 'pàng',
  '瘦': 'shòu',
  '重': 'zhòng',
  '轻': 'qīng',
  '春': 'chūn',
  '夏': 'xià',
  '秋': 'qiū',
  '冬': 'dōng',
  '日': 'rì',
  '月': 'yuè',
  '星': 'xīng',
  '雨': 'yǔ',
  '雪': 'xuě',
  '风': 'fēng',
  '云': 'yún',
  '雷': 'léi',
  '电': 'diàn',
  '冷': 'lěng',
  '热': 'rè',
  '温': 'wēn',
  '凉': 'liáng',
  '天': 'tiān',
  '地': 'dì',
  '和': 'hé',
  '年': 'nián',
  '山': 'shān',
  '水': 'shuǐ',
  '火': 'huǒ',
  '土': 'tǔ',
  '河': 'hé',
  '湖': 'hú',
  '海': 'hǎi',
  '江': 'jiāng',
  '林': 'lín',
  '森': 'sēn',
  '田': 'tián',
  '园': 'yuán',
  '花': 'huā',
  '草': 'cǎo',
  '树': 'shù',
  '木': 'mù',
  '果': 'guǒ',
  '鸟': 'niǎo',
  '虫': 'chóng',
  '鱼': 'yú',
  '马': 'mǎ',
  '牛': 'niú',
  '羊': 'yáng',
  '猪': 'zhū',
  '狗': 'gǒu',
  '猫': 'māo',
  '鸡': 'jī',
  '鸭': 'yā',
  '兔': 'tù',
  '爸': 'bà',
  '妈': 'mā',
  '爷': 'yé',
  '奶': 'nǎi',
  '哥': 'gē',
  '姐': 'jiě',
  '弟': 'dì',
  '妹': 'mèi',
  '叔': 'shū',
  '姑': 'gū',
  '舅': 'jiù',
  '姨': 'yí',
  '儿': 'ér',
  '子': 'zǐ',
  '女': 'nǚ',
  '家': 'jiā',
  '人': 'rén',
  '们': 'men',
  '我': 'wǒ',
  '你': 'nǐ',
  '他': 'tā',
  '她': 'tā',
  '它': 'tā',
  '朋': 'péng',
  '友': 'yǒu',
  '头': 'tóu',
  '目': 'mù',
  '眼': 'yǎn',
  '耳': 'ěr',
  '口': 'kǒu',
  '手': 'shǒu',
  '足': 'zú',
  '脚': 'jiǎo',
  '心': 'xīn',
  '身': 'shēn',
  '体': 'tǐ',
  '面': 'miàn',
  '本': 'běn',
  '书': 'shū',
  '笔': 'bǐ',
  '纸': 'zhǐ',
  '刀': 'dāo',
  '尺': 'chǐ',
  '课': 'kè',
  '作': 'zuò',
  '业': 'yè',
  '卷': 'juàn',
  '考': 'kǎo',
  '试': 'shì',
  '场': 'chǎng',
  '成': 'chéng',
  '绩': 'jì',
  '名': 'míng',
  '字': 'zì',
  '号': 'hào',
  '码': 'mǎ',
  '学': 'xué',
  '生': 'shēng',
  '老': 'lǎo',
  '师': 'shī',
  '校': 'xiào',
  '班': 'bān',
  '语': 'yǔ',
  '数': 'shù',
  '英': 'yīng',
  '音': 'yīn',
  '乐': 'yuè',
  '美': 'měi',
  '术': 'shù',
  '育': 'yù',
  '读': 'dú',
  '写': 'xiě',
  '看': 'kàn',
  '听': 'tīng',
  '说': 'shuō',
  '做': 'zuò',
  '会': 'huì',
  '能': 'néng',
  '要': 'yào',
  '想': 'xiǎng',
  '爱': 'ài',
  '好': 'hǎo',
  '开': 'kāi',
  '关': 'guān',
  '进': 'jìn',
  '出': 'chū',
  '回': 'huí',
  '到': 'dào',
  '去': 'qù',
  '来': 'lái',
  '打': 'dǎ',
  '找': 'zhǎo',
  '给': 'gěi',
  '让': 'ràng',
  '叫': 'jiào',
  '请': 'qǐng',
  '问': 'wèn',
  '答': 'dá',
  '玩': 'wán',
  '唱': 'chàng',
  '跳': 'tiào',
  '画': 'huà',
  '跑': 'pǎo',
  '走': 'zǒu',
  '飞': 'fēi',
  '坐': 'zuò',
  '站': 'zhàn',
  '吃': 'chī',
  '喝': 'hē',
  '睡': 'shuì',
  '醒': 'xǐng',
  '洗': 'xǐ',
  '穿': 'chuān',
  '戴': 'dài',
  '拿': 'ná',
  '放': 'fàng',
  '收': 'shōu',
  '买': 'mǎi',
  '卖': 'mài',
  '送': 'sòng',
  '接': 'jiē',
  '帮': 'bāng',
  '助': 'zhù',
  '新': 'xīn',
  '旧': 'jiù',
  '努': 'nǔ',
  '力': 'lì',
  '勤': 'qín',
  '懒': 'lǎn',
  '干': 'gàn',
  '净': 'jìng',
  '脏': 'zāng',
  '真': 'zhēn',
  '假': 'jiǎ',
  '对': 'duì',
  '错': 'cuò',
  '漂': 'piào',
  '亮': 'liang',
  '丑': 'chǒu',
  '帅': 'shuài',
  '甜': 'tián',
  '酸': 'suān',
  '苦': 'kǔ',
  '辣': 'là',
  '咸': 'xián',
  '聪': 'cōng',
  '明': 'míng',
  '勇': 'yǒng',
  '敢': 'gǎn',
  '可': 'kě',
  '欢': 'huān',
  '怕': 'pà',
  '哭': 'kū',
  '笑': 'xiào',
  '疼': 'téng',
  '饿': 'è',
  '渴': 'kě',
  '累': 'lèi',
  '困': 'kùn',
  '忙': 'máng',
  '闲': 'xián',
  '早': 'zǎo',
  '晚': 'wǎn',
  '迟': 'chí',
  '红': 'hóng',
  '黄': 'huáng',
  '蓝': 'lán',
  '绿': 'lǜ',
  '青': 'qīng',
  '白': 'bái',
  '黑': 'hēi',
  '紫': 'zǐ',
  '橙': 'chéng',
  '灰': 'huī',
  '兴': 'xìng',
  '难': 'nán',
  '过': 'guò',
  '伤': 'shāng',
  '谢': 'xiè',
  '起': 'qǐ',
  '没': 'méi',
  '系': 'xì',
  '客': 'kè',
  '气': 'qì',
  '不': 'bù',
  '用': 'yòng',
  '时': 'shí',
  '秒': 'miǎo',
  '今': 'jīn',
  '昨': 'zuó',
  '午': 'wǔ',
  '半': 'bàn',
  '夜': 'yè',
  '刻': 'kè',
  '期': 'qī',
  '现': 'xiàn',
  '以': 'yǐ',
  '门': 'mén',
  '房': 'fáng',
  '间': 'jiān',
  '厅': 'tīng',
  '厨': 'chú',
  '卫': 'wèi',
  '阳': 'yáng',
  '台': 'tái',
  '卧': 'wò',
  '室': 'shì',
  '床': 'chuáng',
  '桌': 'zhuō',
  '椅': 'yǐ',
  '灯': 'dēng',
  '钟': 'zhōng',
  '沙': 'shā',
  '发': 'fā',
  '窗': 'chuāng',
  '帘': 'lián',
  '毯': 'tǎn',
  '院': 'yuàn',
  '街': 'jiē',
  '店': 'diàn',
  '公': 'gōng',
  '超': 'chāo',
  '市': 'shì',
  '医': 'yī',
  '药': 'yào',
  '病': 'bìng',
  '图': 'tú',
  '馆': 'guǎn',
  '饭': 'fàn',
  '菜': 'cài',
  '汤': 'tāng',
  '肉': 'ròu',
  '蛋': 'dàn',
  '米': 'mǐ',
  '包': 'bāo',
  '油': 'yóu',
  '盐': 'yán',
  '糖': 'táng',
  '茶': 'chá',
  '豆': 'dòu',
  '腐': 'fu',
  '馒': 'mán',
  '洋': 'yáng',
  '葱': 'cōng',
  '萝': 'luó',
  '卜': 'bo',
  '瓜': 'guā',
  '茄': 'qié',
  '椒': 'jiāo',
  '葡': 'pú',
  '萄': 'tao',
  '苹': 'píng',
  '香': 'xiāng',
  '蕉': 'jiāo',
  '橘': 'jú',
  '柠': 'níng',
  '檬': 'méng',
  '核': 'hé',
  '桃': 'tao',
  '栗': 'lì',
  '莓': 'méi',
  '樱': 'yīng',
  '很': 'hěn',
  '都': 'dōu',
  '还': 'hái',
  '又': 'yòu',
  '也': 'yě',
  '就': 'jiù',
  '最': 'zuì',
  '更': 'gèng',
  '再': 'zài',
  '已': 'yǐ',
  '刚': 'gāng',
  '把': 'bǎ',
  '被': 'bèi',
  '跟': 'gēn',
  '像': 'xiàng',
  '样': 'yàng',
  '国': 'guó',
  '城': 'chéng',
  '村': 'cūn',
  '路': 'lù',
  '桥': 'qiáo',
  '车': 'chē',
  '船': 'chuán',
  '机': 'jī',
  '脑': 'nǎo',
  '视': 'shì',
  '空': 'kōng',
  '调': 'tiáo',
  '冰': 'bīng',
  '箱': 'xiāng',
  '衣': 'yī',
  '袜': 'wà',
  '鞋': 'xié',
  '帽': 'mào',
  '伞': 'sǎn',
  '铅': 'qiān',
  '圆': 'yuán',
  '珠': 'zhū',
  '钢': 'gāng',
  '墨': 'mò',
  '习': 'xí',
  '练': 'liàn',
  '认': 'rèn',
  '细': 'xì',
  '虎': 'hu',
  '注': 'zhù',
  '意': 'yì',
  '见': 'jiàn',
  '您': 'nín',
  '知': 'zhī',
  '道': 'dào',
  '早上好': 'zǎo shang hǎo',
  '下午好': 'xià wǔ hǎo',
  '晚上好': 'wǎn shang hǎo',
  '大家好': 'dà jiā hǎo',
  '老师好': 'lǎo shī hǎo',
  '再见': 'zài jiàn',
  '谢谢': 'xiè xie',
  '对不起': 'duì bu qǐ',
  '没关系': 'méi guān xi',
  '不可以': 'bù kě yǐ',
  '不知道': 'bù zhī dào',
  '不相信': 'bù xiāng xìn',
  '不明白': 'bù míng bái',
  '不喜欢': 'bù xǐ huān',
  '不会': 'bù huì',
  '不能': 'bù néng',
  '不要': 'bù yào',
  '明白': 'míng bái',
  '喜欢': 'xǐ huān',
  '讨厌': 'tǎo yàn',
  '希望': 'xī wàng',
  '开始': 'kāi shǐ',
  '结束': 'jié shù',
  '继续': 'jì xù',
  '完成': 'wán chéng',
  '成功': 'chéng gōng',
  '失败': 'shī bài',
  '学习': 'xué xí',
  '读书': 'dú shū',
  '写字': 'xiě zì',
  '游戏': 'yóu xì',
  '运动': 'yùn dòng',
  '休息': 'xiū xi',
  '吃饭': 'chī fàn',
  '喝水': 'hē shuǐ',
  '上学': 'shàng xué',
  '回家': 'huí jiā',
  '出门': 'chū mén',
  '回来': 'huí lái',
  '起床': 'qǐ chuáng',
  '睡觉': 'shuì jiào',
  '刷牙': 'shuā yá',
  '洗脸': 'xǐ liǎn',
  '洗手': 'xǐ shǒu',
  '扫地': 'sǎo dì',
  '洗碗': 'xǐ wǎn',
  '做饭': 'zuò fàn',
  '北京': 'běi jīng',
  '中国': 'zhōng guó',
  '小学生': 'xiǎo xué shēng',
  '小朋友': 'xiǎo péng yǒu',
  '哥哥': 'gē ge',
  '姐姐': 'jiě jie',
  '弟弟': 'dì di',
  '妹妹': 'mèi mei',
  '我们': 'wǒ men',
  '你们': 'nǐ men',
  '他们': 'tā men',
  '这个': 'zhè ge',
  '那个': 'nà ge',
  '哪个': 'nǎ ge',
  '这里': 'zhè lǐ',
  '那里': 'nà lǐ',
  '哪里': 'nǎ lǐ',
  '有的': 'yǒu de',
  '没有': 'méi yǒu',
  '是的': 'shì de',
  '不是': 'bù shì',
  '好的': 'hǎo de',
  '可以': 'kě yǐ',
  '应该': 'yīng gāi',
  '愿意': 'yuàn yì',
  '肯': 'kěn',
  '高兴': 'gāo xìng',
  '开心': 'kāi xīn',
  '快乐': 'kuài lè',
  '难过': 'nán guò',
  '伤心': 'shāng xīn',
  '检查': 'jiǎn chá',
  '复习': 'fù xí',
  '预习': 'yù xí',
  '考试': 'kǎo shì',
  '及格': 'jí gé',
  '优秀': 'yōu xiù',
  '很好': 'hěn hǎo',
  '不好': 'bù hǎo',
  '非常': 'fēi cháng',
  '特别': 'tè bié',
  '大概': 'dà gài',
  '也许': 'yě xǔ',
  '必须': 'bù xū',
  '不必': 'bù bì',
  '不用': 'bù yòng',
  '已经': 'yǐ jīng',
  '经常': 'jīng cháng',
  '总是': 'zǒng shì',
  '马上': 'mǎ shàng',
  '立刻': 'lì kè',
  '然后': 'rán hòu',
  '但是': 'dàn shì',
  '如果': 'rú guǒ',
  '因为': 'yīn wèi',
  '所以': 'suǒ yǐ',
  '虽然': 'suī rán',
  '还是': 'hái shi',
  '关于': 'guān yú',
  '对于': 'duì yú',
  '第一': 'dì yī',
  '一半': 'yī bàn',
  '一共': 'yī gòng',
  '大约': 'dà yuē',
  '左右': 'zuǒ yòu',
  '差不多': 'chà bu duō',
  '差一点': 'chà yī diǎn',
  '一定': 'yī dìng',
  '肯定': 'kěn dìng',
  '突然': 'tū rán',
  '忽然': 'hū rán',
  '十分': 'shí fēn',
};

// 智能分词：优先匹配最长词组
function convertPinyin(text: string): Array<{ char: string; py: string }> {
  const result: Array<{ char: string; py: string }> = [];
  let i = 0;
  while (i < text.length) {
    let matched = false;
    // 尝试 4->3->2 字词
    for (let len = Math.min(4, text.length - i); len >= 2; len--) {
      const word = text.slice(i, i + len);
      const py = PY[word];
      if (py) {
        if (py.includes(' ')) {
          // 多字词，拆分
          const chars = [...word];
          const pys = py.split(' ');
          chars.forEach((c, idx) => {
            result.push({ char: c, py: pys[idx] || pys[pys.length - 1] });
          });
        } else {
          result.push({ char: word, py });
        }
        i += len;
        matched = true;
        break;
      }
    }
    if (!matched) {
      const char = text[i];
      result.push({ char, py: PY[char] || '' });
      i++;
    }
  }
  return result;
}

// 声调颜色
const TONE_COLORS = ['text-red-500', 'text-orange-500', 'text-green-500', 'text-blue-500'];
function getToneColor(py: string): string {
  if (!py) return 'text-gray-400';
  if (/[āēīōūǖ]/i.test(py)) return TONE_COLORS[0];
  if (/[áéíóúǘ]/i.test(py)) return TONE_COLORS[1];
  if (/[ǎěǐǒǔǚ]/i.test(py)) return TONE_COLORS[2];
  if (/[àèìòùǜ]/i.test(py)) return TONE_COLORS[3];
  return 'text-gray-700';
}

type Mode = 'learn' | 'practice' | 'sige' | 'hengxian';
type FontSize = 'sm' | 'md' | 'lg';

const MODES = [
  { id: 'learn' as Mode, label: '学习模式', icon: '📖', desc: '显示汉字和拼音对照学习' },
  { id: 'practice' as Mode, label: '练习模式', icon: '✏️', desc: '只显示汉字，填写拼音' },
  { id: 'sige' as Mode, label: '四线三格', icon: '📝', desc: '标准拼音格练习纸' },
  { id: 'hengxian' as Mode, label: '横线拼音', icon: '📄', desc: '横线格式练习卷' },
];

const FONT_SIZES: Record<FontSize, number> = { sm: 20, md: 28, lg: 36 };

export default function PinyinPage() {
  const [text, setText] = useState('爸爸妈妈爷爷奶奶哥哥姐姐弟弟妹妹');
  const [mode, setMode] = useState<Mode>('learn');
  const [fontSize, setFontSize] = useState<FontSize>('md');
  const [showAnswer, setShowAnswer] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const previewRef = useRef<HTMLDivElement>(null);

  const converted = convertPinyin(text);

  const handleExportPDF = async () => {
    if (!previewRef.current) return;
    setIsExporting(true);
    try {
      const { default: html2canvas } = await import('html2canvas');
      const { default: jsPDF } = await import('jspdf');
      const el = previewRef.current;
      const origBg = el.style.background;
      el.style.background = '#ffffff';
      const canvas = await html2canvas(el, { scale: 2, useCORS: true, backgroundColor: '#ffffff', logging: false });
      el.style.background = origBg;

      // 添加网站水印
      const { drawWatermarkOnCanvas } = await import('@/lib/pdfWatermark');
      const pCtx = canvas.getContext('2d');
      if (pCtx) {
        drawWatermarkOnCanvas(pCtx, canvas.width, canvas.height);
      }

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });
      const pw = pdf.internal.pageSize.getWidth();
      const ph = pdf.internal.pageSize.getHeight();
      const ratio = canvas.width / canvas.height;
      let w = pw; let h = pw / ratio;
      if (h > ph) { h = ph; w = ph * ratio; }
      pdf.addImage(imgData, 'PNG', (pw - w) / 2, (ph - h) / 2, w, h);
      pdf.save('拼音练习卷.pdf');
    } catch (err) { console.error(err); }
    setIsExporting(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* 导航栏 */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <a href="/" className="flex items-center gap-3 group">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-xl shadow-lg shadow-blue-500/30">📚</div>
              <span className="text-xl font-bold text-white group-hover:opacity-80 transition-opacity">拼音注音练习</span>
            </a>
            <div className="flex items-center gap-1">
              <a href="/" className="px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">🏠 首页</a>
              <a href="/tools/math-worksheet" className="px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">🧮 数学练习卷</a>
              <a href="/tools/calligraphy" className="px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">✍️ 字帖生成器</a>
              <a href="/tools/sudoku" className="px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">🧩 数独游戏</a>
              <div className="w-px h-6 bg-white/20 mx-2"></div>
              <a href="/resources" className="px-4 py-2 text-sm bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-lg font-medium hover:from-amber-600 hover:to-orange-600 transition-colors">🎁 免费资源</a>
            </div>
          </div>
        </div>
      </nav>

      {/* 主内容 */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-28 pb-16">
        {/* 标题 */}
        <div className="text-center mb-8">
          <div className="text-5xl mb-3">📝</div>
          <h1 className="text-3xl md:text-4xl font-black text-white mb-2">拼音学习工具</h1>
          <p className="text-gray-400">声母韵母 · 拼音注音 · 四线三格打印</p>
        </div>

        {/* 控制面板 */}
        <div className="bg-slate-800/60 border border-white/10 rounded-2xl p-6 mb-6">
          <div className="mb-5">
            <label className="block text-sm font-medium text-gray-300 mb-2">输入汉字</label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="请输入要练习的汉字"
              className="w-full px-4 py-3 bg-slate-900/80 border border-white/10 rounded-xl text-white text-lg resize-none focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20"
              rows={2}
            />
            <div className="flex justify-between items-center mt-2 text-xs text-gray-500">
              <span>已输入 {text.length} 个字符，识别拼音 {converted.filter(c => c.py).length} 个</span>
              <div className="flex gap-2">
                {['天地人和', '爸爸妈妈', '上学读书'].map(t => (
                  <button key={t} onClick={() => setText(t)} className="px-2 py-1 bg-slate-700 rounded hover:bg-slate-600 transition-colors">{t}</button>
                ))}
              </div>
            </div>
          </div>

          {/* 模式 */}
          <div className="mb-5">
            <label className="block text-sm font-medium text-gray-300 mb-2">练习模式</label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {MODES.map((m) => (
                <button
                  key={m.id}
                  onClick={() => { setMode(m.id); setShowAnswer(false); }}
                  className={`px-3 py-3 rounded-xl border text-sm font-medium transition-all ${mode === m.id ? 'border-blue-500 bg-blue-500/20 text-blue-300' : 'border-white/10 text-gray-400 hover:border-white/30 hover:text-white'}`}
                >
                  <div className="text-xl mb-1">{m.icon}</div>
                  <div>{m.label}</div>
                  <div className="text-xs mt-1 opacity-60">{m.desc}</div>
                </button>
              ))}
            </div>
          </div>

          {/* 字号和功能 */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-400">字号：</span>
              {(['sm', 'md', 'lg'] as FontSize[]).map((s) => (
                <button key={s} onClick={() => setFontSize(s)}
                  className={`px-3 py-1.5 rounded-lg text-sm ${fontSize === s ? 'bg-blue-500 text-white' : 'bg-slate-700 text-gray-400 hover:text-white'}`}>
                  {s === 'sm' ? '小' : s === 'md' ? '中' : '大'}
                </button>
              ))}
            </div>
            <div className="flex items-center gap-2 ml-auto">
              {mode === 'practice' && (
                <button onClick={() => setShowAnswer(!showAnswer)}
                  className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors text-sm">
                  {showAnswer ? '隐藏答案' : '显示答案'}
                </button>
              )}
              <button onClick={handleExportPDF} disabled={isExporting}
                className="px-4 py-2 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-lg hover:from-amber-600 hover:to-orange-600 transition-colors text-sm font-medium disabled:opacity-50">
                {isExporting ? '生成中...' : '📄 导出PDF'}
              </button>
            </div>
          </div>
        </div>

        {/* 预览区 */}
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden" ref={previewRef}>
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-8 py-4 flex items-center justify-between">
            <div>
              <h2 className="text-white font-bold text-xl">拼音注音练习卷</h2>
              <p className="text-blue-200 text-sm mt-1">姓名：__________ &nbsp;&nbsp; 日期：__________</p>
            </div>
            <div className="text-white text-3xl">📝</div>
          </div>

          <div className="p-6">
            {/* 学习模式 */}
            {mode === 'learn' && (
              <div className="space-y-4">
                <div className="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 gap-3">
                  {converted.map((item, i) => (
                    <div key={i} className="flex flex-col items-center justify-center py-3 bg-slate-50 rounded-xl border-2 border-dashed border-slate-400">
                      <span className="font-bold text-slate-800" style={{ fontSize: FONT_SIZES[fontSize] * 1.2 }}>{item.char}</span>
                      <span className={`font-semibold mt-1 ${getToneColor(item.py)}`} style={{ fontSize: FONT_SIZES[fontSize] }}>
                        {item.py || '—'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 练习模式 */}
            {mode === 'practice' && (
              <div>
                <div className="mb-3 text-sm text-gray-500 bg-blue-50 px-4 py-2 rounded-lg">练习要求：请在拼音栏填写正确的拼音（含声调）</div>
                <div className="space-y-3">
                  {converted.map((item, i) => (
                    <div key={i} className="flex items-center gap-3 py-2 border-b border-gray-300">
                      <span className="font-bold text-slate-800 w-12 text-center" style={{ fontSize: FONT_SIZES[fontSize] * 1.2 }}>{item.char}</span>
                      <div className="flex-1 flex items-center">
                        <div className="flex-1 h-10 border-b-2 border-blue-300 flex items-end pb-1">
                          {showAnswer && <span className={`font-semibold ${getToneColor(item.py)}`} style={{ fontSize: FONT_SIZES[fontSize] }}>{item.py}</span>}
                        </div>
                      </div>
                      <div className="w-12 text-right text-xs text-gray-400">{i + 1}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 四线三格 */}
            {mode === 'sige' && (
              <div className="space-y-4">
                {Array.from({ length: Math.min(8, Math.ceil(converted.length / 8)) }).map((_, rowIdx) => {
                  const row = converted.slice(rowIdx * 8, rowIdx * 8 + 8);
                  return (
                    <div key={rowIdx}>
                      <div className="relative" style={{ height: FONT_SIZES[fontSize] * 4 }}>
                        <div className="absolute inset-0 flex flex-col justify-around">
                          {[0, 1, 2, 3].map(l => (
                            <div key={l} className="border-t border-blue-300" style={{ borderTopWidth: l === 1 || l === 2 ? 1 : 1.5 }} />
                          ))}
                        </div>
                        <div className="absolute inset-0 flex">
                          {row.map((item, colIdx) => (
                            <div key={colIdx} className="flex-1 flex flex-col items-center justify-around border-r border-gray-300 last:border-r-0">
                              <div className="text-center" style={{ height: `${FONT_SIZES[fontSize] * 1.5}px`, display: 'flex', alignItems: 'flex-end', justifyContent: 'center', paddingBottom: '2px' }}>
                                <span className={`font-semibold ${getToneColor(item.py)}`} style={{ fontSize: FONT_SIZES[fontSize] }}>{showAnswer ? item.py : '　'}</span>
                              </div>
                              <div className="h-0.5 w-full bg-pink-400"></div>
                              <div className="text-center font-bold text-slate-800" style={{ height: `${FONT_SIZES[fontSize] * 2}px`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: FONT_SIZES[fontSize] * 1.5 }}>{item.char}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}

            {/* 横线拼音 */}
            {mode === 'hengxian' && (
              <div className="space-y-3">
                {Array.from({ length: Math.min(10, Math.ceil(converted.length / 10)) }).map((_, rowIdx) => {
                  const row = converted.slice(rowIdx * 10, rowIdx * 10 + 10);
                  return (
                    <div key={rowIdx} className="relative" style={{ minHeight: FONT_SIZES[fontSize] * 3 }}>
                      <div className="absolute bottom-0 left-0 right-0 border-t-2 border-gray-300"></div>
                      <div className="absolute bottom-0 left-0 right-0" style={{ borderTopWidth: '1px', borderTopStyle: 'dashed', borderTopColor: '#ccc', marginBottom: '2px' }}></div>
                      <div className="flex">
                        {row.map((item, colIdx) => (
                          <div key={colIdx} className="flex-1 border-r border-gray-300 last:border-r-0">
                            <div className="text-center" style={{ height: `${FONT_SIZES[fontSize] * 1.2}px`, display: 'flex', alignItems: 'flex-end', justifyContent: 'center', paddingBottom: '2px' }}>
                              <span className={`font-semibold ${getToneColor(item.py)}`} style={{ fontSize: FONT_SIZES[fontSize] }}>{showAnswer ? item.py : '　'}</span>
                            </div>
                            <div className="text-center font-bold text-slate-800" style={{ fontSize: FONT_SIZES[fontSize] * 1.5, height: `${FONT_SIZES[fontSize] * 1.8}px`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>{item.char}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <div className="bg-slate-100 px-8 py-3 text-center text-xs text-gray-400">
            教材工具箱 · 拼音注音练习 · 免费使用
          </div>
        </div>

        {/* 说明 */}
        <div className="mt-6 bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-2xl p-5">
          <h3 className="text-lg font-bold text-white mb-2">使用说明</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-gray-400">
            {[['01', '输入汉字，支持词组自动分词'], ['02', '选择模式：学习对照 / 练习填写'], ['03', '点击显示答案可查看参考答案'], ['04', '导出PDF生成可打印练习卷']].map(([n, t]) => (
              <div key={n} className="flex items-start gap-2">
                <span className="text-blue-400 font-bold">{n}</span>
                <span>{t}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="text-center mt-6">
          <a href="/" className="inline-flex items-center gap-2 px-6 py-3 bg-slate-700/60 border border-white/10 text-gray-300 rounded-xl hover:bg-slate-700 hover:text-white transition-all">
            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
            返回首页
          </a>
        </div>

        {/* ===== 内容三件套 ===== */}
        <div className="print:hidden mt-8 space-y-8">

          {/* 使用指南 */}
          <section className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-2xl p-6">
            <h2 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
              <span>📖</span> 使用指南
            </h2>
            <div className="text-gray-400 leading-relaxed space-y-3 text-sm">
              <p>
                拼音学习工具是专为小学一年级学生设计的拼音练习辅助工具。支持声母（23个）、韵母（24个）和整体认读音节（16个）的分类练习，可以给任意汉字标注正确的拼音声调。提供四线三格拼音书写模板，帮助学生掌握拼音字母的标准书写格式。工具还支持多音字识别和声调标注功能，生成的拼音练习内容可以导出PDF打印，方便日常复习使用。建议一年级学生在学完拼音基础后，每天用10分钟进行拼音注音练习，巩固声母、韵母和声调的组合规则。
              </p>
            </div>
          </section>

          {/* 适用场景 */}
          <section className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-2xl p-6">
            <h2 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
              <span>🎯</span> 适用场景
            </h2>
            <ul className="space-y-3 text-gray-400 text-sm">
              <li className="flex items-start gap-2">
                <span className="text-blue-400 mt-0.5 shrink-0">●</span>
                <span><strong className="text-gray-300">拼音入门：</strong>学完声母韵母后，用工具生成练习巩固记忆</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-400 mt-0.5 shrink-0">●</span>
                <span><strong className="text-gray-300">拼音复习：</strong>期中期末考试前，生成专项拼音练习卷</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-400 mt-0.5 shrink-0">●</span>
                <span><strong className="text-gray-300">多音字训练：</strong>针对容易读错的多音字进行专项练习</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-400 mt-0.5 shrink-0">●</span>
                <span><strong className="text-gray-300">幼小衔接：</strong>大班下学期开始接触拼音，为一年级做准备</span>
              </li>
            </ul>
          </section>

          {/* 常见问题FAQ */}
          <section className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-2xl p-6">
            <h2 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
              <span>❓</span> 常见问题
            </h2>
            <div className="space-y-2">
              <details className="group border border-white/10 rounded-lg">
                <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-300 hover:text-white list-none font-medium text-sm">
                  <span>拼音学习工具支持哪些功能？</span>
                  <span className="text-gray-500 group-open:rotate-180 transition-transform text-xs">▼</span>
                </summary>
                <div className="px-4 pb-4 text-sm text-gray-400 leading-relaxed">支持声母、韵母、整体认读音节的分类练习，汉字拼音标注，四线三格拼音书写模板生成，以及PDF导出打印功能。</div>
              </details>
              <details className="group border border-white/10 rounded-lg">
                <summary className="flex items-center justify-between cursor-pointer p-4 text-gray-300 hover:text-white list-none font-medium text-sm">
                  <span>孩子拼音学不会怎么办？</span>
                  <span className="text-gray-500 group-open:rotate-180 transition-transform text-xs">▼</span>
                </summary>
                <div className="px-4 pb-4 text-sm text-gray-400 leading-relaxed">拼音学习的关键是多读多练。建议每天10分钟大声朗读拼音，配合拼音卡片进行认读练习。b/d、p/q等易混淆的声母需要重点反复练习。</div>
              </details>
            </div>
          </section>

          {/* 相关工具推荐 */}
          <section className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-2xl p-6">
            <h2 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
              <span>🔗</span> 相关工具推荐
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <a href="/tools/flashcards" className="block bg-white/5 hover:bg-white/10 border border-white/10 hover:border-blue-500/30 rounded-xl p-4 transition-all group">
                <div className="text-2xl mb-2">🃏</div>
                <div className="font-bold text-gray-200 text-sm group-hover:text-white transition-colors">识字卡片生成器</div>
                <div className="text-xs text-gray-500 mt-1">自定义汉字卡片</div>
              </a>
              <a href="/tools/calligraphy" className="block bg-white/5 hover:bg-white/10 border border-white/10 hover:border-blue-500/30 rounded-xl p-4 transition-all group">
                <div className="text-2xl mb-2">✍️</div>
                <div className="font-bold text-gray-200 text-sm group-hover:text-white transition-colors">字帖生成器</div>
                <div className="text-xs text-gray-500 mt-1">田字格米字格练字</div>
              </a>
              <a href="/resources/chinese" className="block bg-white/5 hover:bg-white/10 border border-white/10 hover:border-blue-500/30 rounded-xl p-4 transition-all group">
                <div className="text-2xl mb-2">📚</div>
                <div className="font-bold text-gray-200 text-sm group-hover:text-white transition-colors">拼音学习资源</div>
                <div className="text-xs text-gray-500 mt-1">语文学习资料</div>
              </a>
            </div>
          </section>
        </div>

        {/* 使用指南 */}
        <div className="max-w-4xl mx-auto px-4 py-12">
          <ToolGuide {...toolGuides['pinyin']} />
        </div>
      </div>
    </div>
  );
}
