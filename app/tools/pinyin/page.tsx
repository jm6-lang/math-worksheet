'use client';

import { useState, useRef } from 'react';

// ===== 内置拼音转换器 =====
const PINYIN_DICT: Record<string, string> = {
  '一': 'yī', '二': 'èr', '三': 'sān', '四': 'sì', '五': 'wǔ',
  '六': 'liù', '七': 'qī', '八': 'bā', '九': 'jiǔ', '十': 'shí',
  '百': 'bǎi', '千': 'qiān', '万': 'wàn', '元': 'yuán', '角': 'jiǎo', '分': 'fēn',
  '上': 'shàng', '下': 'xià', '左': 'zuǒ', '右': 'yòu',
  '大': 'dà', '小': 'xiǎo', '多': 'duō', '少': 'shǎo', '高': 'gāo', '矮': 'ǎi',
  '长': 'cháng', '短': 'duǎn', '远': 'yuǎn', '近': 'jìn', '快': 'kuài', '慢': 'màn',
  '天': 'tiān', '地': 'dì', '人': 'rén', '和': 'hé',
  '春': 'chūn', '夏': 'xià', '秋': 'qiū', '冬': 'dōng',
  '日': 'rì', '月': 'yuè', '星': 'xīng', '雨': 'yǔ', '雪': 'xuě',
  '风': 'fēng', '云': 'yún', '雷': 'léi', '电': 'diàn',
  '山': 'shān', '水': 'shuǐ', '火': 'huǒ', '土': 'tǔ',
  '东': 'dōng', '西': 'xī', '南': 'nán', '北': 'běi',
  '花': 'huā', '草': 'cǎo', '树': 'shù', '木': 'mù', '林': 'lín', '森': 'sēn',
  '鸟': 'niǎo', '虫': 'chóng', '鱼': 'yú', '马': 'mǎ', '牛': 'niú', '羊': 'yáng',
  '猪': 'zhū', '狗': 'gǒu', '猫': 'māo', '鸡': 'jī', '鸭': 'yā', '兔': 'tù',
  '爸': 'bà', '妈': 'mā', '爷': 'yé', '奶': 'nǎi', '哥': 'gē', '姐': 'jiě',
  '弟': 'dì', '妹': 'mèi', '叔': 'shū', '姑': 'gū', '舅': 'jiù', '姨': 'yí',
  '儿': 'ér', '子': 'zǐ', '女': 'nǚ', '家': 'jiā', '门': 'mén', '口': 'kǒu',
  '目': 'mù', '耳': 'ěr', '手': 'shǒu', '足': 'zú', '心': 'xīn', '头': 'tóu',
  '本': 'běn', '书': 'shū', '笔': 'bǐ', '纸': 'zhǐ', '刀': 'dāo', '尺': 'chǐ',
  '学': 'xué', '生': 'shēng', '老': 'lǎo', '师': 'shī', '校': 'xiào', '班': 'bān',
  '我': 'wǒ', '你': 'nǐ', '他': 'tā', '她': 'tā', '它': 'tā', '们': 'men',
  '这': 'zhè', '那': 'nà', '哪': 'nǎ', '谁': 'shuí', '什': 'shén', '么': 'me',
  '为': 'wèi', '的': 'de', '了': 'le', '着': 'zhe', '过': 'guò', '得': 'dé',
  '是': 'shì', '有': 'yǒu', '没': 'méi', '在': 'zài', '来': 'lái', '去': 'qù',
  '说': 'shuō', '看': 'kàn', '听': 'tīng', '写': 'xiě', '读': 'dú', '做': 'zuò',
  '会': 'huì', '能': 'néng', '要': 'yào', '想': 'xiǎng', '爱': 'ài', '好': 'hǎo',
  '很': 'hěn', '都': 'dōu', '还': 'hái', '又': 'yòu', '也': 'yě', '就': 'jiù',
  '明': 'míng', '亮': 'liàng', '红': 'hóng', '黄': 'huáng', '蓝': 'lán', '绿': 'lǜ',
  '白': 'bái', '黑': 'hēi', '青': 'qīng', '紫': 'zǐ', '橙': 'chéng', '灰': 'huī',
  '开': 'kāi', '关': 'guān', '进': 'jìn', '出': 'chū', '回': 'huí', '到': 'dào',
  '打': 'dǎ', '找': 'zhǎo', '给': 'gěi', '让': 'ràng', '叫': 'jiào', '请': 'qǐng',
  '谢': 'xiè', '对': 'duì', '错': 'cuò', '真': 'zhēn', '太': 'tài',
  '最': 'zuì', '更': 'gèng', '再': 'zài', '已': 'yǐ', '刚': 'gāng',
  '把': 'bǎ', '被': 'bèi', '跟': 'gēn', '像': 'xiàng', '样': 'yàng', '可': 'kě',
  '以': 'yǐ', '后': 'hòu', '前': 'qián', '中': 'zhōng', '外': 'wài', '里': 'lǐ',
  '国': 'guó', '城': 'chéng', '村': 'cūn', '河': 'hé', '海': 'hǎi', '湖': 'hú',
  '江': 'jiāng', '路': 'lù', '桥': 'qiáo', '车': 'chē', '船': 'chuán',
  '飞': 'fēi', '机': 'jī', '跑': 'pǎo', '走': 'zǒu',
  '坐': 'zuò', '站': 'zhàn', '吃': 'chī', '喝': 'hē', '睡': 'shuì', '醒': 'xǐng',
  '洗': 'xǐ', '穿': 'chuān', '戴': 'dài', '拿': 'ná', '放': 'fàng', '收': 'shōu',
  '买': 'mǎi', '卖': 'mài', '送': 'sòng', '接': 'jiē', '帮': 'bāng',
  '问': 'wèn', '答': 'dá', '考': 'kǎo', '试': 'shì', '玩': 'wán', '唱': 'chàng',
  '跳': 'tiào', '画': 'huà',
  '字': 'zì', '词': 'cí', '句': 'jù', '段': 'duàn', '文': 'wén', '章': 'zhāng',
  '语': 'yǔ', '数': 'shù', '英': 'yīng',
  '音': 'yīn', '乐': 'yuè', '美': 'měi', '术': 'shù', '体': 'tǐ', '育': 'yù',
  '床': 'chuáng', '桌': 'zhuō', '椅': 'yǐ', '灯': 'dēng', '钟': 'zhōng', '房': 'fáng',
  '院': 'yuàn', '场': 'chǎng', '街': 'jiē', '店': 'diàn', '饭': 'fàn', '菜': 'cài',
  '汤': 'tāng', '肉': 'ròu', '蛋': 'dàn', '奶': 'nǎi', '果': 'guǒ',
  '米': 'mǐ', '面': 'miàn', '包': 'bāo', '油': 'yóu', '盐': 'yán', '糖': 'táng', '茶': 'chá',
  '病': 'bìng', '医': 'yī', '药': 'yào', '疼': 'téng',
  '冷': 'lěng', '热': 'rè', '饿': 'è', '渴': 'kě', '累': 'lèi', '困': 'kùn',
  '怕': 'pà', '哭': 'kū', '笑': 'xiào',
  '漂': 'piào', '亮': 'liang', '开': 'kāi', '心': 'xīn',
  '努': 'nǔ', '力': 'lì', '勤': 'qín',
  '脏': 'zāng', '新': 'xīn', '旧': 'jiù',
  '经': 'jīng', '常': 'cháng', '总': 'zǒng',
  '年': 'nián', '月': 'yuè', '日': 'rì', '时': 'shí', '分': 'fēn', '秒': 'miǎo',
  '今': 'jīn', '天': 'tiān', '昨': 'zuó', '明': 'míng',
  '早': 'zǎo', '上': 'shàng', '中': 'zhōng', '午': 'wǔ', '晚': 'wǎn',
  '半': 'bàn', '夜': 'yè', '刻': 'kè',
  '星': 'xīng', '期': 'qī', '日': 'rì',
  '公': 'gōng', '园': 'yuán', '超': 'chāo', '市': 'shì', '图': 'tú', '书': 'shū', '馆': 'guǎn',
  '跑': 'pǎo', '踢': 'tī', '游': 'yóu', '泳': 'yǒng',
  '做': 'zuò', '业': 'yè', '习': 'xí', '练': 'liàn',
  '认': 'rèn', '真': 'zhēn', '仔': 'zǐ', '细': 'xì', '马': 'mǎ', '虎': 'hu',
  '聪': 'cōng', '明': 'míng', '勇': 'yǒng', '敢': 'gǎn',
  '可': 'kě', '爱': 'ài',
  '高': 'gāo', '兴': 'xìng', '快': 'kuài', '乐': 'lè',
  '难': 'nán', '过': 'guò', '伤': 'shāng',
  '注': 'zhù', '意': 'yì', '关': 'guān',
  '帮': 'bāng', '助': 'zhù',
  '对': 'duì', '起': 'qǐ', '没': 'méi', '关': 'guān', '系': 'xì',
  '客': 'kè', '气': 'qì',
  '房': 'fáng', '间': 'jiān', '客': 'kè', '厅': 'tīng', '厨': 'chú',
  '卫': 'wèi', '生': 'shēng', '阳': 'yáng', '台': 'tái',
  '卧': 'wò', '室': 'shì', '书': 'shū', '沙': 'shā', '发': 'fā',
  '窗': 'chuāng', '帘': 'lián', '地': 'dì', '毯': 'tǎn',
  '衣': 'yī', '服': 'fú', '袜': 'wà', '鞋': 'xié',
  '帽': 'mào', '包': 'bāo', '伞': 'sǎn',
  '笔': 'bǐ', '本': 'běn', '橡': 'xiàng', '皮': 'pí', '擦': 'cā',
  '铅': 'qiān', '圆': 'yuán', '珠': 'zhū',
  '钢': 'gāng', '墨': 'mò',
  '课': 'kè', '作': 'zuò', '卷': 'juàn',
  '考': 'kǎo', '场': 'chǎng', '成': 'chéng', '绩': 'jì',
  '名': 'míng', '号': 'hào', '码': 'mǎ',
  '电': 'diàn', '脑': 'nǎo', '视': 'shì', '空': 'kōng', '调': 'tiáo',
  '冰': 'bīng', '箱': 'xiāng', '洗': 'xǐ', '衣': 'yī',
  '豆': 'dòu', '腐': 'fu', '馒': 'mán', '头': 'tou',
  '土': 'tǔ', '豆': 'dòu', '洋': 'yáng', '葱': 'cōng', '萝': 'luó', '卜': 'bo',
  '黄': 'huáng', '瓜': 'guā', '茄': 'qié', '辣': 'là', '椒': 'jiāo',
  '葡': 'pú', '萄': 'tao', '西': 'xī', '瓜': 'guā',
  '苹': 'píng', '果': 'guǒ', '香': 'xiāng', '蕉': 'jiāo',
  '橘': 'jú', '柠': 'níng', '檬': 'méng',
  '核': 'hé', '桃': 'tao', '栗': 'lì',
  '草': 'cǎo', '莓': 'méi', '樱': 'yīng', '桃': 'táo',
  '跑': 'pǎo', '跳': 'tiào', '踢': 'tī', '游': 'yóu', '泳': 'yǒng',
  '做': 'zuò', '业': 'yè', '习': 'xí', '练': 'liàn',
  '认': 'rèn', '真': 'zhēn', '仔': 'zǐ', '细': 'xì', '马': 'mǎ', '虎': 'hu',
  '聪': 'cōng', '明': 'míng', '勇': 'yǒng', '敢': 'gǎn',
  '漂': 'piào', '亮': 'liang', '可': 'kě', '爱': 'ài',
  '高': 'gāo', '兴': 'xìng', '快': 'kuài', '乐': 'lè',
  '难': 'nán', '过': 'guò', '伤': 'shāng', '心': 'xīn',
  '注': 'zhù', '意': 'yì', '关': 'guān', '心': 'xīn',
  '帮': 'bāng', '助': 'zhù', '谢': 'xiè',
  '对': 'duì', '起': 'qǐ', '没': 'méi', '关': 'guān', '系': 'xì',
  '爸': 'bà', '妈': 'mā', '谢': 'xiè', '您': 'nín', '再': 'zài', '见': 'jiàn',
  '请': 'qǐng', '问': 'wèn',
  '客': 'kè', '气': 'qì', '不': 'bù', '用': 'yòng',
  '不': 'bù', '知': 'zhī', '道': 'dào',
  '医': 'yī', '院': 'yuàn', '药': 'yào', '病': 'bìng',
  '疼': 'téng', '冷': 'lěng', '热': 'rè', '饿': 'è', '渴': 'kě', '累': 'lèi',
  '怕': 'pà', '哭': 'kū', '笑': 'xiào',
  '高': 'gāo', '矮': 'ǎi', '胖': 'pàng', '瘦': 'shòu',
  '重': 'zhòng', '轻': 'qīng', '软': 'ruǎn', '硬': 'yìng',
  '甜': 'tián', '酸': 'suān', '苦': 'kǔ', '辣': 'là', '咸': 'xián',
  '漂': 'piào', '亮': 'liang', '丑': 'chǒu', '帅': 'shuài',
  '新': 'xīn', '旧': 'jiù', '好': 'hǎo', '坏': 'huài',
  '老': 'lǎo', '少': 'shào', '年': 'nián', '轻': 'qīng',
  '努': 'nǔ', '力': 'lì', '勤': 'qín', '懒': 'lǎn',
  '干': 'gàn', '净': 'jìng', '脏': 'zāng',
  '早': 'zǎo', '晚': 'wǎn', '迟': 'chí',
  '忙': 'máng', '闲': 'xián', '快': 'kuài', '慢': 'màn',
  '简单': 'jiǎn dān', '复杂': 'fù zá',
  '容易': 'róng yì', '困难': 'kùn nan',
  '干净': 'gān jìng', '整齐': 'zhěng qí',
  '安静': 'ān jìng', '热闹': 'rè nao',
  '开心': 'kāi xīn', '快乐': 'kuài lè', '高兴': 'gāo xìng',
  '难过': 'nán guò', '伤心': 'shāng xīn', '害怕': 'hài pà',
  '相信': 'xiāng xìn', '知道': 'zhī dào', '明白': 'míng bái',
  '喜欢': 'xǐ huān', '讨厌': 'tǎo yàn', '希望': 'xī wàng',
  '开始': 'kāi shǐ', '结束': 'jié shù', '继续': 'jì xù',
  '完成': 'wán chéng', '成功': 'chéng gōng', '失败': 'shī bài',
  '学习': 'xué xí', '读书': 'dú shū', '写字': 'xiě zì',
  '游戏': 'yóu xì', '运动': 'yùn dòng', '休息': 'xiū xi',
  '起床': 'qǐ chuáng', '睡觉': 'shuì jiào',
  '吃饭': 'chī fàn', '喝水': 'hē shuǐ', '上学': 'shàng xué',
  '回家': 'huí jiā', '出门': 'chū mén', '回来': 'huí lái',
  '刷牙': 'shuā yá', '洗脸': 'xǐ liǎn', '洗手': 'xǐ shǒu',
  '扫地': 'sǎo dì', '洗碗': 'xǐ wǎn', '做饭': 'zuò fàn',
  '今天': 'jīn tiān', '明天': 'míng tiān', '昨天': 'zuó tiān',
  '早上': 'zǎo shang', '下午': 'xià wǔ', '晚上': 'wǎn shang',
  '现在': 'xiàn zài', '以后': 'yǐ hòu', '以前': 'yǐ qián',
  '什么': 'shén me', '怎么': 'zěn me', '为什么': 'wèi shén me',
  '多少': 'duō shǎo', '北京': 'běi jīng', '中国': 'zhōng guó',
  '爸爸妈妈': 'bà ba mā ma', '小朋友': 'xiǎo péng yǒu',
  '小学生': 'xiǎo xué shēng', '老师好': 'lǎo shī hǎo',
  '大家好': 'dà jiā hǎo', '早上好': 'zǎo shang hǎo',
  '下午好': 'xià wǔ hǎo', '晚上好': 'wǎn shang hǎo',
  '再见': 'zài jiàn', '谢谢': 'xiè xie',
  '对不起': 'duì bu qǐ', '没关系': 'méi guān xi',
  '不可以': 'bù kě yǐ', '没关系': 'méi guān xi',
};

// 智能拼音转换
function convertPinyin(text: string): Array<{ char: string; py: string }> {
  const result: Array<{ char: string; py: string }> = [];
  // 先尝试匹配词组
  let i = 0;
  while (i < text.length) {
    // 尝试最长匹配（最多4字词组）
    let matched = false;
    for (let len = Math.min(4, text.length - i); len >= 2; len--) {
      const word = text.slice(i, i + len);
      if (PINYIN_DICT[word]) {
        const py = PINYIN_DICT[word];
        if (py.includes(' ')) {
          // 多字词组，拆分
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
      result.push({ char, py: PINYIN_DICT[char] || '' });
      i++;
    }
  }
  return result;
}

// 声调颜色映射
const TONE_COLORS = [
  'text-red-500',   // 一声 - 红
  'text-orange-500', // 二声 - 橙
  'text-green-500',  // 三声 - 绿
  'text-blue-500',   // 四声 - 蓝
];

function getToneColor(py: string): string {
  if (!py) return 'text-gray-400';
  if (py.includes('ā') || py.includes('ē') || py.includes('ī') || py.includes('ō') || py.includes('ū')) return TONE_COLORS[0];
  if (py.includes('á') || py.includes('é') || py.includes('í') || py.includes('ó') || py.includes('ú')) return TONE_COLORS[1];
  if (py.includes('ǎ') || py.includes('ě') || py.includes('ǐ') || py.includes('ǒ') || py.includes('ǔ')) return TONE_COLORS[2];
  if (py.includes('à') || py.includes('è') || py.includes('ì') || py.includes('ò') || py.includes('ù')) return TONE_COLORS[3];
  return 'text-gray-700';
}

type Mode = 'learn' | 'practice' | 'sige' | 'hengxian';
type FontSize = 'sm' | 'md' | 'lg';

const MODES = [
  { id: 'learn' as Mode, label: '学习模式', icon: '📖', desc: '显示汉字和拼音，对照学习' },
  { id: 'practice' as Mode, label: '练习模式', icon: '✏️', desc: '只显示汉字，填写拼音' },
  { id: 'sige' as Mode, label: '四线三格', icon: '📝', desc: '标准拼音格练习纸' },
  { id: 'hengxian' as Mode, label: '横线拼音', icon: '📄', desc: '横线格式练习卷' },
];

// 声母
const INITIALS = ['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x', 'zh', 'ch', 'sh', 'r', 'z', 'c', 's', 'y', 'w'];
// 韵母
const FINALS = ['a', 'o', 'e', 'i', 'u', 'ü', 'ai', 'ei', 'ui', 'ao', 'ou', 'iu', 'ie', 'üe', 'er', 'an', 'en', 'in', 'un', 'ün', 'ang', 'eng', 'ing', 'ong'];

export default function PinyinPage() {
  const [text, setText] = useState('爸爸妈妈爷爷奶奶哥哥姐姐弟弟妹妹');
  const [mode, setMode] = useState<Mode>('learn');
  const [fontSize, setFontSize] = useState<FontSize>('md');
  const [showAnswer, setShowAnswer] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const previewRef = useRef<HTMLDivElement>(null);

  const converted = convertPinyin(text);

  const fontSizes: Record<FontSize, number> = { sm: 20, md: 28, lg: 36 };

  const handleExportPDF = async () => {
    if (!previewRef.current) return;
    setIsExporting(true);
    try {
      const { default: html2canvas } = await import('html2canvas');
      const { default: jsPDF } = await import('jspdf');
      const el = previewRef.current;
      const origBg = el.style.background;
      el.style.background = '#ffffff';
      const canvas = await html2canvas(el, {
        scale: 2, useCORS: true, backgroundColor: '#ffffff', logging: false,
      });
      el.style.background = origBg;
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });
      const pw = pdf.internal.pageSize.getWidth();
      const ph = pdf.internal.pageSize.getHeight();
      const ratio = canvas.width / canvas.height;
      let w = pw;
      let h = pw / ratio;
      if (h > ph) { h = ph; w = ph * ratio; }
      const x = (pw - w) / 2;
      const y = (ph - h) / 2;
      pdf.addImage(imgData, 'PNG', x, y, w, h);
      pdf.save('拼音练习卷.pdf');
    } catch (err) {
      console.error(err);
    }
    setIsExporting(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* 顶部导航 */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <a href="/" className="flex items-center gap-3 group">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-xl shadow-lg shadow-blue-500/30">📚</div>
                <span className="text-xl font-bold text-white group-hover:opacity-80 transition-opacity">教材工具箱</span>
              </a>
            </div>
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
        {/* 页面标题 */}
        <div className="text-center mb-8">
          <div className="text-5xl mb-3">📝</div>
          <h1 className="text-3xl md:text-4xl font-black text-white mb-2">拼音注音练习</h1>
          <p className="text-gray-400">输入汉字，自动标注拼音，支持多种练习模式</p>
        </div>

        {/* 控制面板 */}
        <div className="bg-slate-800/60 border border-white/10 rounded-2xl p-6 mb-6">
          {/* 输入区 */}
          <div className="mb-5">
            <label className="block text-sm font-medium text-gray-300 mb-2">输入汉字</label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="请输入要练习的汉字，例如：爸爸妈妈爷爷奶奶"
              className="w-full px-4 py-3 bg-slate-900/80 border border-white/10 rounded-xl text-white text-lg resize-none focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20"
              rows={2}
            />
            <div className="flex justify-between items-center mt-2 text-xs text-gray-500">
              <span>已输入 {text.length} 个字符</span>
              <div className="flex gap-2">
                <button onClick={() => setText('天地人和春夏秋冬')} className="px-2 py-1 bg-slate-700 rounded hover:bg-slate-600 transition-colors">示例1</button>
                <button onClick={() => setText('爸爸妈妈爷爷奶奶哥哥姐姐弟弟妹妹叔叔阿姨')} className="px-2 py-1 bg-slate-700 rounded hover:bg-slate-600 transition-colors">示例2</button>
                <button onClick={() => setText('上学读书写字做作业考试第一名优秀学生')} className="px-2 py-1 bg-slate-700 rounded hover:bg-slate-600 transition-colors">示例3</button>
              </div>
            </div>
          </div>

          {/* 模式选择 */}
          <div className="mb-5">
            <label className="block text-sm font-medium text-gray-300 mb-2">练习模式</label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {MODES.map((m) => (
                <button
                  key={m.id}
                  onClick={() => { setMode(m.id); setShowAnswer(false); }}
                  className={`px-3 py-3 rounded-xl border text-sm font-medium transition-all ${
                    mode === m.id
                      ? 'border-blue-500 bg-blue-500/20 text-blue-300'
                      : 'border-white/10 text-gray-400 hover:border-white/30 hover:text-white'
                  }`}
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
                <button
                  key={s}
                  onClick={() => setFontSize(s)}
                  className={`px-3 py-1.5 rounded-lg text-sm ${
                    fontSize === s ? 'bg-blue-500 text-white' : 'bg-slate-700 text-gray-400 hover:text-white'
                  }`}
                >
                  {s === 'sm' ? '小' : s === 'md' ? '中' : '大'}
                </button>
              ))}
            </div>
            <div className="flex items-center gap-2 ml-auto">
              {mode === 'practice' && (
                <button
                  onClick={() => setShowAnswer(!showAnswer)}
                  className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors text-sm"
                >
                  {showAnswer ? '隐藏答案' : '显示答案'}
                </button>
              )}
              <button
                onClick={handleExportPDF}
                disabled={isExporting}
                className="px-4 py-2 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-lg hover:from-amber-600 hover:to-orange-600 transition-colors text-sm font-medium disabled:opacity-50"
              >
                {isExporting ? '生成中...' : '📄 导出PDF'}
              </button>
            </div>
          </div>
        </div>

        {/* 预览区 */}
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden print:shadow-none" ref={previewRef}>
          {/* 打印头部 */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-8 py-4 flex items-center justify-between">
            <div>
              <h2 className="text-white font-bold text-xl">拼音注音练习卷</h2>
              <p className="text-blue-200 text-sm mt-1">姓名：__________ &nbsp;&nbsp; 日期：__________</p>
            </div>
            <div className="text-white text-3xl">📝</div>
          </div>

          {/* 内容区 */}
          <div className="p-6">
            {/* 学习模式 */}
            {mode === 'learn' && (
              <div className="space-y-4">
                <div className="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 gap-3">
                  {converted.map((item, i) => (
                    <div key={i} className="flex flex-col items-center justify-center py-3 bg-slate-50 rounded-xl border-2 border-dashed border-slate-200">
                      <span className="text-3xl font-bold text-slate-800" style={{ fontSize: fontSizes[fontSize] * 1.2 }}>
                        {item.char}
                      </span>
                      <span className={`text-lg font-semibold mt-1 ${getToneColor(item.py)}`} style={{ fontSize: fontSizes[fontSize] }}>
                        {item.py}
                      </span>
                    </div>
                  ))}
                </div>
                <div className="mt-4 text-center text-gray-400 text-sm">
                  共 {converted.length} 个字，点击「显示答案」可在练习模式下查看
                </div>
              </div>
            )}

            {/* 练习模式 */}
            {mode === 'practice' && (
              <div>
                <div className="mb-3 text-sm text-gray-500 bg-blue-50 px-4 py-2 rounded-lg">
                  练习要求：请在拼音栏填写正确的拼音（含声调）
                </div>
                <div className="space-y-3">
                  {converted.map((item, i) => (
                    <div key={i} className="flex items-center gap-3 py-2 border-b border-gray-100">
                      <span className="text-3xl font-bold text-slate-800 w-12 text-center" style={{ fontSize: fontSizes[fontSize] * 1.2 }}>
                        {item.char}
                      </span>
                      <div className="flex-1 flex items-center">
                        {/* 填写区 */}
                        <div className="flex-1 h-10 border-b-2 border-blue-300 flex items-end pb-1">
                          {showAnswer && (
                            <span className={`font-semibold ${getToneColor(item.py)}`} style={{ fontSize: fontSizes[fontSize] }}>
                              {item.py}
                            </span>
                          )}
                        </div>
                      </div>
                      <div className="w-12 text-right text-xs text-gray-400">{i + 1}</div>
                    </div>
                  ))}
                </div>
                {showAnswer && (
                  <div className="mt-4 text-center text-sm text-green-600">
                    答案已显示，核对完成后可打印练习
                  </div>
                )}
              </div>
            )}

            {/* 四线三格模式 */}
            {mode === 'sige' && (
              <div className="space-y-4">
                {Array.from({ length: Math.min(8, Math.ceil(converted.length / 8)) }).map((_, rowIdx) => {
                  const row = converted.slice(rowIdx * 8, rowIdx * 8 + 8);
                  return (
                    <div key={rowIdx}>
                      {/* 四线三格 */}
                      <div className="relative" style={{ height: fontSizes[fontSize] * 4 }}>
                        {/* 四条线 */}
                        <div className="absolute inset-0 flex flex-col justify-around">
                          {[0, 1, 2, 3].map((line) => (
                            <div key={line} className="border-t border-blue-300" style={{ borderTopWidth: line === 1 || line === 2 ? 1 : 1.5 }} />
                          ))}
                        </div>
                        {/* 拼音和汉字 */}
                        <div className="absolute inset-0 flex">
                          {row.map((item, colIdx) => (
                            <div key={colIdx} className="flex-1 flex flex-col items-center justify-around border-r border-gray-100 last:border-r-0">
                              {/* 拼音区（上格） */}
                              <div className="text-center" style={{ height: `${fontSizes[fontSize] * 1.5}px`, display: 'flex', alignItems: 'flex-end', justifyContent: 'center', paddingBottom: '2px' }}>
                                <span className={`font-semibold ${getToneColor(item.py)}`} style={{ fontSize: fontSizes[fontSize] }}>
                                  {showAnswer ? item.py : '　'}
                                </span>
                              </div>
                              {/* 声调标注线 */}
                              <div className="h-0.5 w-full bg-pink-300"></div>
                              {/* 汉字区（下格） */}
                              <div className="text-center font-bold text-slate-800" style={{ height: `${fontSizes[fontSize] * 2}px`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: fontSizes[fontSize] * 1.5 }}>
                                {item.char}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  );
                })}
                {!showAnswer && (
                  <div className="text-center text-sm text-gray-400 mt-2">点击「显示答案」查看完整拼音</div>
                )}
              </div>
            )}

            {/* 横线拼音模式 */}
            {mode === 'hengxian' && (
              <div className="space-y-3">
                {/* 表头 */}
                <div className="grid grid-cols-10 gap-2 text-sm text-gray-400 border-b border-gray-200 pb-2">
                  {Array.from({ length: 10 }).map((_, i) => (
                    <div key={i} className="text-center">{i + 1}</div>
                  ))}
                </div>
                {Array.from({ length: Math.min(10, Math.ceil(converted.length / 10)) }).map((_, rowIdx) => {
                  const row = converted.slice(rowIdx * 10, rowIdx * 10 + 10);
                  return (
                    <div key={rowIdx} className="relative" style={{ minHeight: fontSizes[fontSize] * 3 }}>
                      {/* 横线 */}
                      <div className="absolute bottom-0 left-0 right-0 border-t-2 border-gray-300"></div>
                      <div className="absolute bottom-0 left-0 right-0" style={{ borderTopWidth: '1px', borderTopStyle: 'dashed', borderTopColor: '#ccc', marginBottom: '2px' }}></div>
                      <div className="flex">
                        {row.map((item, colIdx) => (
                          <div key={colIdx} className="flex-1 border-r border-gray-100 last:border-r-0">
                            <div className="text-center" style={{ height: `${fontSizes[fontSize] * 1.2}px`, display: 'flex', alignItems: 'flex-end', justifyContent: 'center', paddingBottom: '2px' }}>
                              <span className={`font-semibold ${getToneColor(item.py)}`} style={{ fontSize: fontSizes[fontSize] }}>
                                {showAnswer ? item.py : '　'}
                              </span>
                            </div>
                            <div className="text-center font-bold text-slate-800" style={{ fontSize: fontSizes[fontSize] * 1.5, height: `${fontSizes[fontSize] * 1.8}px`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                              {item.char}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  );
                })}
                {!showAnswer && (
                  <div className="text-center text-sm text-gray-400">点击「显示答案」查看完整拼音</div>
                )}
              </div>
            )}
          </div>

          {/* 打印底部 */}
          <div className="bg-slate-100 px-8 py-3 text-center text-xs text-gray-400">
            教材工具箱 · 拼音注音练习 · 免费使用
          </div>
        </div>

        {/* 使用说明 */}
        <div className="mt-6 bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-2xl p-5">
          <h3 className="text-lg font-bold text-white mb-2">使用说明</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-gray-400">
            <div className="flex items-start gap-2">
              <span className="text-blue-400 font-bold">01</span>
              <span>在文本框中输入要练习的汉字（支持词组自动分词）</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-blue-400 font-bold">02</span>
              <span>选择练习模式：学习模式对照查看，练习模式填写答案</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-blue-400 font-bold">03</span>
              <span>点击「显示答案」可显示/隐藏参考答案</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-blue-400 font-bold">04</span>
              <span>点击「导出PDF」可生成可打印的练习卷</span>
            </div>
          </div>
        </div>

        {/* 返回首页 */}
        <div className="text-center mt-6">
          <a href="/" className="inline-flex items-center gap-2 px-6 py-3 bg-slate-700/60 border border-white/10 text-gray-300 rounded-xl hover:bg-slate-700 hover:text-white transition-all">
            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            返回首页
          </a>
        </div>
      </div>
    </div>
  );
}
