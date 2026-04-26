/**
 * 单元测试卷题库数据 - 人教版小学数学、语文、英语、科学
 * 按年级、学期、单元组织，每个单元至少8道题
 */

export type Subject = '数学' | '语文' | '英语' | '科学';

export interface UnitQuestion {
  id: string;
  unitName: string;
  grade: number;
  semester: '上' | '下';
  subject: Subject;
  questions: {
    type: string;
    content: string;
    answer: string;
    difficulty: 1 | 2 | 3;
  }[];
}

export const unitTestData: UnitQuestion[] = [
  // ==================== 一年级上册 ====================
  {
    id: 'g1s-u1',
    unitName: '准备课',
    grade: 1,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '数一数，图中有（  ）朵花。\n（图略：5朵花）', answer: '5', difficulty: 1 },
      { type: '填空题', content: '在多的后面画"√"。\n△△△    ○○○○', answer: '○○○○ 后面画√', difficulty: 1 },
      { type: '填空题', content: '在少的后面画"○"。\n☆☆☆☆☆    □□', answer: '□□ 后面画○', difficulty: 1 },
      { type: '填空题', content: '把同样多的用线连起来。\n3个苹果    3个橘子', answer: '连线：3个苹果连3个橘子', difficulty: 1 },
      { type: '选择题', content: '下面哪种水果最多？\nA. 2个苹果  B. 5个香蕉  C. 3个橘子', answer: 'B', difficulty: 1 },
      { type: '选择题', content: '4和6中间的数是（  ）。\nA. 3  B. 5  C. 7', answer: 'B', difficulty: 2 },
      { type: '判断题', content: '3比4多。（  ）', answer: '×', difficulty: 1 },
      { type: '判断题', content: '5和5一样多。（  ）', answer: '√', difficulty: 1 },
      { type: '填空题', content: '从大到小排列：2、5、1、4、3\n（  ）>（  ）>（  ）>（  ）>（  ）', answer: '5 > 4 > 3 > 2 > 1', difficulty: 2 },
      { type: '填空题', content: '从1数到10，6的后面是（  ），前面是（  ）。', answer: '7；5', difficulty: 2 },
    ],
  },
  {
    id: 'g1s-u2',
    unitName: '位置',
    grade: 1,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '小明前面有3人，后面有2人，这一排一共有（  ）人。', answer: '6', difficulty: 2 },
      { type: '填空题', content: '看图填空：小鸟在小狗的（  ）面，小狗在小鸟的（  ）面。\n（小鸟在上，小狗在下）', answer: '上；下', difficulty: 1 },
      { type: '选择题', content: '小华站在队伍的第3个，他前面有（  ）人。\nA. 1人  B. 2人  C. 3人', answer: 'B', difficulty: 1 },
      { type: '选择题', content: '从左数，第4个是△：○△□○△□\n从右数，△排在第（  ）个。\nA. 2  B. 3  C. 4', answer: 'B', difficulty: 2 },
      { type: '判断题', content: '面对太阳，你的前面是东面。（  ）', answer: '√', difficulty: 2 },
      { type: '判断题', content: '小猫在小狗的左边，那么小狗在小猫的右边。（  ）', answer: '√', difficulty: 1 },
      { type: '填空题', content: '小红住在小明楼上，小明住在小红（  ）面。', answer: '下', difficulty: 1 },
      { type: '应用题', content: '一排小朋友，从左往右数小明排第5，从右往左数小明排第4，这排一共有几个小朋友？', answer: '5+4-1=8（个）', difficulty: 3 },
      { type: '填空题', content: '书桌的上面放着书，书的（  ）面是书桌。', answer: '下', difficulty: 1 },
      { type: '应用题', content: '小明的前面有4个人，后面有5个人，从前面数小明排第几？', answer: '第5', difficulty: 2 },
    ],
  },
  {
    id: 'g1s-u3',
    unitName: '1-5的认识和加减法',
    grade: 1,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '计算题', content: '1 + 2 =', answer: '3', difficulty: 1 },
      { type: '计算题', content: '3 + 1 =', answer: '4', difficulty: 1 },
      { type: '计算题', content: '5 - 2 =', answer: '3', difficulty: 1 },
      { type: '计算题', content: '4 - 1 =', answer: '3', difficulty: 1 },
      { type: '计算题', content: '2 + 3 =', answer: '5', difficulty: 1 },
      { type: '计算题', content: '5 - 3 =', answer: '2', difficulty: 1 },
      { type: '填空题', content: '3 +（  ）= 5', answer: '2', difficulty: 2 },
      { type: '填空题', content: '（  ）- 2 = 3', answer: '5', difficulty: 2 },
      { type: '比较大小', content: '在○里填上">"、"<"或"="。\n3 + 1 ○ 5', answer: '<', difficulty: 2 },
      { type: '应用题', content: '树上有3只小鸟，又飞来了2只，现在一共有几只小鸟？', answer: '3+2=5（只）', difficulty: 2 },
      { type: '应用题', content: '小明有5个苹果，吃了2个，还剩几个？', answer: '5-2=3（个）', difficulty: 2 },
      { type: '计算题', content: '1 + 1 + 1 =', answer: '3', difficulty: 2 },
    ],
  },
  {
    id: 'g1s-u4',
    unitName: '6-10的认识和加减法',
    grade: 1,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '计算题', content: '4 + 3 =', answer: '7', difficulty: 1 },
      { type: '计算题', content: '6 + 2 =', answer: '8', difficulty: 1 },
      { type: '计算题', content: '9 - 4 =', answer: '5', difficulty: 1 },
      { type: '计算题', content: '10 - 3 =', answer: '7', difficulty: 1 },
      { type: '计算题', content: '5 + 5 =', answer: '10', difficulty: 1 },
      { type: '计算题', content: '8 - 6 =', answer: '2', difficulty: 1 },
      { type: '填空题', content: '6 +（  ）= 10', answer: '4', difficulty: 2 },
      { type: '填空题', content: '（  ）- 3 = 7', answer: '10', difficulty: 2 },
      { type: '比较大小', content: '在○里填上">"、"<"或"="。\n5 + 3 ○ 9', answer: '<', difficulty: 2 },
      { type: '应用题', content: '池塘里有6只青蛙，跳走了3只，还剩几只？', answer: '6-3=3（只）', difficulty: 2 },
      { type: '应用题', content: '小红有4朵红花和5朵黄花，一共有几朵花？', answer: '4+5=9（朵）', difficulty: 2 },
      { type: '计算题', content: '2 + 3 + 4 =', answer: '9', difficulty: 2 },
    ],
  },
  {
    id: 'g1s-u5',
    unitName: '11-20各数的认识',
    grade: 1,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '1个十和5个一组成（  ）。', answer: '15', difficulty: 1 },
      { type: '填空题', content: '20里面有（  ）个十。', answer: '2', difficulty: 1 },
      { type: '填空题', content: '18的十位上是（  ），个位上是（  ）。', answer: '1；8', difficulty: 1 },
      { type: '填空题', content: '与16相邻的两个数是（  ）和（  ）。', answer: '15；17', difficulty: 2 },
      { type: '计算题', content: '10 + 5 =', answer: '15', difficulty: 1 },
      { type: '计算题', content: '18 - 10 =', answer: '8', difficulty: 1 },
      { type: '计算题', content: '12 + 6 =', answer: '18', difficulty: 1 },
      { type: '计算题', content: '17 - 7 =', answer: '10', difficulty: 1 },
      { type: '比较大小', content: '在○里填上">"、"<"或"="。\n12 ○ 15', answer: '<', difficulty: 1 },
      { type: '应用题', content: '小明有10支铅笔，妈妈又给他买了5支，现在一共有多少支？', answer: '10+5=15（支）', difficulty: 2 },
      { type: '填空题', content: '从大到小排列：11、18、14、20、16\n（  ）>（  ）>（  ）>（  ）>（  ）', answer: '20 > 18 > 16 > 14 > 11', difficulty: 2 },
      { type: '填空题', content: '个位上是3的两位数有（  ）、（  ）、（  ）。（从小到大写三个）', answer: '13、23、33', difficulty: 3 },
    ],
  },

  // ==================== 一年级下册 ====================
  {
    id: 'g1x-u1',
    unitName: '认识图形（二）',
    grade: 1,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '长方形有（  ）条边，（  ）个角。', answer: '4；4', difficulty: 1 },
      { type: '填空题', content: '正方形有（  ）条边，每条边都（  ）。', answer: '4；相等', difficulty: 1 },
      { type: '填空题', content: '三角形有（  ）条边，（  ）个角。', answer: '3；3', difficulty: 1 },
      { type: '选择题', content: '下面哪个是正方形？\nA. 长长方方的  B. 四条边一样长  C. 三个角', answer: 'B', difficulty: 1 },
      { type: '选择题', content: '用4根小棒可以拼成一个（  ）。\nA. 三角形  B. 正方形  C. 圆', answer: 'B', difficulty: 1 },
      { type: '判断题', content: '长方形和正方形的四个角都是直角。（  ）', answer: '√', difficulty: 2 },
      { type: '判断题', content: '圆没有角。（  ）', answer: '√', difficulty: 1 },
      { type: '填空题', content: '硬币的面是（  ）形。', answer: '圆', difficulty: 1 },
      { type: '应用题', content: '用3根同样长的小棒可以拼成一个什么图形？', answer: '三角形', difficulty: 1 },
      { type: '填空题', content: '长方形对边（  ），正方形四条边都（  ）。', answer: '相等；相等', difficulty: 2 },
    ],
  },
  {
    id: 'g1x-u2',
    unitName: '20以内的退位减法',
    grade: 1,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '计算题', content: '12 - 5 =', answer: '7', difficulty: 1 },
      { type: '计算题', content: '15 - 8 =', answer: '7', difficulty: 1 },
      { type: '计算题', content: '17 - 9 =', answer: '8', difficulty: 1 },
      { type: '计算题', content: '13 - 6 =', answer: '7', difficulty: 1 },
      { type: '计算题', content: '11 - 4 =', answer: '7', difficulty: 1 },
      { type: '计算题', content: '16 - 7 =', answer: '9', difficulty: 1 },
      { type: '计算题', content: '14 - 9 =', answer: '5', difficulty: 1 },
      { type: '计算题', content: '18 - 9 =', answer: '9', difficulty: 1 },
      { type: '填空题', content: '（  ）+ 7 = 15', answer: '8', difficulty: 2 },
      { type: '填空题', content: '13 -（  ）= 6', answer: '7', difficulty: 2 },
      { type: '应用题', content: '树上有15只鸟，飞走了8只，还剩几只？', answer: '15-8=7（只）', difficulty: 2 },
      { type: '应用题', content: '小明有12颗糖，吃了9颗，还剩几颗？', answer: '12-9=3（颗）', difficulty: 2 },
    ],
  },
  {
    id: 'g1x-u3',
    unitName: '100以内数的认识',
    grade: 1,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '3个十和5个一组成（  ）。', answer: '35', difficulty: 1 },
      { type: '填空题', content: '68里面有（  ）个十和（  ）个一。', answer: '6；8', difficulty: 1 },
      { type: '填空题', content: '100里面有（  ）个十。', answer: '10', difficulty: 1 },
      { type: '填空题', content: '个位上是7，十位上是4的数是（  ）。', answer: '47', difficulty: 1 },
      { type: '计算题', content: '30 + 5 =', answer: '35', difficulty: 1 },
      { type: '计算题', content: '46 - 6 =', answer: '40', difficulty: 1 },
      { type: '计算题', content: '20 + 30 =', answer: '50', difficulty: 1 },
      { type: '计算题', content: '58 - 50 =', answer: '8', difficulty: 1 },
      { type: '比较大小', content: '在○里填上">"、"<"或"="。\n45 ○ 54', answer: '<', difficulty: 2 },
      { type: '比较大小', content: '在○里填上">"、"<"或"="。\n78 ○ 75', answer: '>', difficulty: 2 },
      { type: '应用题', content: '学校有30个篮球，又买了20个，现在一共有多少个？', answer: '30+20=50（个）', difficulty: 2 },
      { type: '填空题', content: '与69相邻的两个数是（  ）和（  ）。', answer: '68；70', difficulty: 2 },
    ],
  },

  // ==================== 二年级上册 ====================
  {
    id: 'g2s-u1',
    unitName: '长度单位',
    grade: 2,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '1米 =（  ）厘米', answer: '100', difficulty: 1 },
      { type: '填空题', content: '课桌高约70（  ）。（填"米"或"厘米"）', answer: '厘米', difficulty: 1 },
      { type: '填空题', content: '教室的长约8（  ）。（填"米"或"厘米"）', answer: '米', difficulty: 1 },
      { type: '选择题', content: '下面哪个物体的长度最接近1米？\nA. 铅笔  B. 课桌  C. 教室的门', answer: 'B', difficulty: 2 },
      { type: '选择题', content: '一根绳子对折后是5米，这根绳子原来长（  ）米。\nA. 5  B. 10  C. 15', answer: 'B', difficulty: 2 },
      { type: '计算题', content: '3米 - 100厘米 =（  ）米', answer: '2', difficulty: 2 },
      { type: '计算题', content: '200厘米 =（  ）米', answer: '2', difficulty: 1 },
      { type: '计算题', content: '1米50厘米 + 50厘米 =（  ）米', answer: '2', difficulty: 2 },
      { type: '判断题', content: '1米比100厘米长。（  ）', answer: '×', difficulty: 1 },
      { type: '应用题', content: '小明身高1米20厘米，小华比小明高10厘米，小华身高多少？', answer: '1米30厘米（或130厘米）', difficulty: 2 },
      { type: '应用题', content: '一根铁丝长80厘米，剪去30厘米，还剩多少厘米？', answer: '80-30=50（厘米）', difficulty: 2 },
      { type: '填空题', content: '量比较短的物体，可以用（  ）作单位。', answer: '厘米', difficulty: 1 },
    ],
  },
  {
    id: 'g2s-u2',
    unitName: '100以内的加法和减法（二）',
    grade: 2,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '计算题', content: '36 + 47 =', answer: '83', difficulty: 1 },
      { type: '计算题', content: '53 + 29 =', answer: '82', difficulty: 1 },
      { type: '计算题', content: '80 - 36 =', answer: '44', difficulty: 1 },
      { type: '计算题', content: '72 - 45 =', answer: '27', difficulty: 1 },
      { type: '计算题', content: '45 + 38 =', answer: '83', difficulty: 1 },
      { type: '计算题', content: '90 - 56 =', answer: '34', difficulty: 1 },
      { type: '竖式计算', content: '用竖式计算：\n  56\n+ 37\n------', answer: '93', difficulty: 2 },
      { type: '竖式计算', content: '用竖式计算：\n  83\n- 47\n------', answer: '36', difficulty: 2 },
      { type: '应用题', content: '图书馆有故事书45本，科技书38本，一共有多少本？', answer: '45+38=83（本）', difficulty: 2 },
      { type: '应用题', content: '停车场有65辆车，开走了28辆，还剩多少辆？', answer: '65-28=37（辆）', difficulty: 2 },
      { type: '应用题', content: '一年级有42人，二年级有39人，两个年级一共有多少人？', answer: '42+39=81（人）', difficulty: 2 },
      { type: '比较大小', content: '在○里填上">"、"<"或"="。\n36 + 28 ○ 55', answer: '>', difficulty: 2 },
    ],
  },
  {
    id: 'g2s-u3',
    unitName: '角的初步认识',
    grade: 2,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '一个角有（  ）个顶点和（  ）条边。', answer: '1；2', difficulty: 1 },
      { type: '填空题', content: '角的大小与边的（  ）无关，与两条边张开的（  ）有关。', answer: '长短；大小', difficulty: 2 },
      { type: '选择题', content: '下面哪个图形是角？\nA. ○  B. △  C. □的角', answer: 'C', difficulty: 1 },
      { type: '判断题', content: '角的两条边越长，角就越大。（  ）', answer: '×', difficulty: 2 },
      { type: '判断题', content: '直角是最大的角。（  ）', answer: '×', difficulty: 2 },
      { type: '判断题', content: '三角板上的直角和黑板上的直角一样大。（  ）', answer: '√', difficulty: 2 },
      { type: '填空题', content: '长方形有（  ）个直角，正方形有（  ）个直角。', answer: '4；4', difficulty: 1 },
      { type: '填空题', content: '三角板上有（  ）个角，其中最大的角是（  ）角。', answer: '3；直', difficulty: 2 },
      { type: '选择题', content: '一个角的两条边张开得越大，角就越（  ）。\nA. 大  B. 小  C. 不变', answer: 'A', difficulty: 1 },
      { type: '应用题', content: '一张长方形纸剪去一个角，还剩几个角？（写出一种情况即可）', answer: '3个、4个或5个（写出一种即可）', difficulty: 3 },
    ],
  },

  // ==================== 二年级下册 ====================
  {
    id: 'g2x-u1',
    unitName: '数据收集整理',
    grade: 2,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '统计表可以帮助我们清楚地看出数据的（  ）。', answer: '多少', difficulty: 1 },
      { type: '应用题', content: '二（1）班同学最喜欢的颜色统计如下：\n红色8人，蓝色12人，绿色6人，黄色4人。\n（1）喜欢（  ）色的人最多。\n（2）喜欢蓝色的比喜欢红色的多（  ）人。', answer: '（1）蓝；（2）4', difficulty: 2 },
      { type: '应用题', content: '下面是某班同学最喜欢吃的水果统计：\n苹果10人，香蕉8人，橘子5人，葡萄7人。\n（1）一共调查了（  ）人。\n（2）最喜欢吃（  ）的人最少。', answer: '（1）30；（2）橘子', difficulty: 2 },
      { type: '选择题', content: '统计同学们最喜欢的运动，应该用（  ）来记录。\nA. 画图  B. 列表  C. 画正字', answer: 'C', difficulty: 1 },
      { type: '判断题', content: '统计的时候，一个正字代表5个人。（  ）', answer: '√', difficulty: 1 },
      { type: '填空题', content: '"正"字一共有（  ）笔，一笔代表（  ）个。', answer: '5；1', difficulty: 1 },
      { type: '应用题', content: '动物园里有猴子15只，熊猫8只，老虎6只，大象4只。\n（1）猴子比熊猫多几只？\n（2）熊猫和老虎一共有几只？', answer: '（1）15-8=7（只）；（2）8+6=14（只）', difficulty: 2 },
      { type: '填空题', content: '用画"正"字的方法统计，"正正"表示（  ）个。', answer: '10', difficulty: 1 },
      { type: '应用题', content: '学校门口5分钟内通过的车辆统计：\n小汽车12辆，自行车8辆，公交车4辆，摩托车6辆。\n哪种车最多？多几辆？', answer: '小汽车最多，比自行车多4辆', difficulty: 2 },
      { type: '选择题', content: '要调查全班同学最喜欢哪个季节，最好的方法是（  ）。\nA. 问老师  B. 举手统计  C. 猜一猜', answer: 'B', difficulty: 1 },
    ],
  },
  {
    id: 'g2x-u2',
    unitName: '表内除法（一）',
    grade: 2,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '计算题', content: '6 ÷ 2 =', answer: '3', difficulty: 1 },
      { type: '计算题', content: '12 ÷ 3 =', answer: '4', difficulty: 1 },
      { type: '计算题', content: '15 ÷ 5 =', answer: '3', difficulty: 1 },
      { type: '计算题', content: '18 ÷ 6 =', answer: '3', difficulty: 1 },
      { type: '计算题', content: '24 ÷ 4 =', answer: '6', difficulty: 1 },
      { type: '计算题', content: '20 ÷ 5 =', answer: '4', difficulty: 1 },
      { type: '计算题', content: '36 ÷ 6 =', answer: '6', difficulty: 1 },
      { type: '计算题', content: '30 ÷ 5 =', answer: '6', difficulty: 1 },
      { type: '填空题', content: '把12个苹果平均分成3份，每份（  ）个。', answer: '4', difficulty: 1 },
      { type: '填空题', content: '24里面有（  ）个4。', answer: '6', difficulty: 2 },
      { type: '应用题', content: '有18个橘子，平均分给6个小朋友，每人分几个？', answer: '18÷6=3（个）', difficulty: 2 },
      { type: '应用题', content: '有20朵花，每4朵扎一束，可以扎几束？', answer: '20÷4=5（束）', difficulty: 2 },
    ],
  },
  {
    id: 'g2x-u3',
    unitName: '混合运算',
    grade: 2,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '计算题', content: '5 + 3 × 2 =', answer: '11', difficulty: 1 },
      { type: '计算题', content: '12 - 4 × 2 =', answer: '4', difficulty: 1 },
      { type: '计算题', content: '(6 + 3) × 2 =', answer: '18', difficulty: 2 },
      { type: '计算题', content: '15 ÷ 3 + 4 =', answer: '9', difficulty: 1 },
      { type: '计算题', content: '20 - 12 ÷ 4 =', answer: '17', difficulty: 1 },
      { type: '计算题', content: '(18 - 6) ÷ 3 =', answer: '4', difficulty: 2 },
      { type: '计算题', content: '4 × 5 - 10 =', answer: '10', difficulty: 1 },
      { type: '计算题', content: '24 ÷ (6 - 2) =', answer: '6', difficulty: 2 },
      { type: '判断题', content: '5 + 3 × 2 = 16。（  ）', answer: '×', difficulty: 2 },
      { type: '判断题', content: '在没有括号的算式里，要先算乘除法，再算加减法。（  ）', answer: '√', difficulty: 1 },
      { type: '应用题', content: '小明买了3本笔记本，每本4元，付了20元，应找回多少元？', answer: '20-3×4=8（元）', difficulty: 2 },
      { type: '应用题', content: '有24个苹果，吃了6个，剩下的平均分给3个人，每人分几个？', answer: '(24-6)÷3=6（个）', difficulty: 3 },
    ],
  },

  // ==================== 三年级上册 ====================
  {
    id: 'g3s-u1',
    unitName: '时、分、秒',
    grade: 3,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '1时 =（  ）分', answer: '60', difficulty: 1 },
      { type: '填空题', content: '1分 =（  ）秒', answer: '60', difficulty: 1 },
      { type: '填空题', content: '1时 =（  ）秒', answer: '3600', difficulty: 2 },
      { type: '填空题', content: '120秒 =（  ）分', answer: '2', difficulty: 1 },
      { type: '填空题', content: '3时 =（  ）分', answer: '180', difficulty: 1 },
      { type: '计算题', content: '2时30分 + 40分 =（  ）时（  ）分', answer: '3；10', difficulty: 2 },
      { type: '计算题', content: '5分 - 180秒 =（  ）分', answer: '2', difficulty: 2 },
      { type: '选择题', content: '小明跑50米用了9（  ）。\nA. 时  B. 分  C. 秒', answer: 'C', difficulty: 1 },
      { type: '判断题', content: '秒针走一圈是60秒，也就是1分。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '时针从数字3走到数字6，经过了3小时。（  ）', answer: '×', difficulty: 2 },
      { type: '应用题', content: '一场电影从下午2时开始，到下午4时30分结束，这场电影放映了多长时间？', answer: '2时30分', difficulty: 2 },
      { type: '应用题', content: '小红7:30从家出发，走了25分钟到学校，她几点到学校？', answer: '7:55', difficulty: 2 },
    ],
  },
  {
    id: 'g3s-u2',
    unitName: '万以内的加法和减法（一）',
    grade: 3,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '计算题', content: '230 + 450 =', answer: '680', difficulty: 1 },
      { type: '计算题', content: '560 - 280 =', answer: '280', difficulty: 1 },
      { type: '计算题', content: '370 + 480 =', answer: '850', difficulty: 1 },
      { type: '计算题', content: '800 - 350 =', answer: '450', difficulty: 1 },
      { type: '计算题', content: '125 + 367 =', answer: '492', difficulty: 2 },
      { type: '计算题', content: '603 - 245 =', answer: '358', difficulty: 2 },
      { type: '竖式计算', content: '用竖式计算：\n  456\n+ 378\n------', answer: '834', difficulty: 2 },
      { type: '竖式计算', content: '用竖式计算：\n  702\n- 385\n------', answer: '317', difficulty: 2 },
      { type: '应用题', content: '学校图书馆有故事书350本，科技书280本，一共有多少本？', answer: '350+280=630（本）', difficulty: 2 },
      { type: '应用题', content: '水果店有苹果500千克，卖出235千克，还剩多少千克？', answer: '500-235=265（千克）', difficulty: 2 },
      { type: '估算题', content: '估算：398 + 204 ≈（  ）', answer: '600', difficulty: 2 },
      { type: '估算题', content: '估算：603 - 297 ≈（  ）', answer: '300', difficulty: 2 },
    ],
  },
  {
    id: 'g3s-u3',
    unitName: '倍的认识',
    grade: 3,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '5的3倍是（  ）。', answer: '15', difficulty: 1 },
      { type: '填空题', content: '24是6的（  ）倍。', answer: '4', difficulty: 1 },
      { type: '填空题', content: '（  ）的4倍是20。', answer: '5', difficulty: 2 },
      { type: '选择题', content: '小明有6颗糖，小红的糖是小明的3倍，小红有（  ）颗糖。\nA. 9  B. 18  C. 3', answer: 'B', difficulty: 1 },
      { type: '选择题', content: '鸡有8只，鸭的只数是鸡的2倍，鸭有（  ）只。\nA. 4  B. 10  C. 16', answer: 'C', difficulty: 1 },
      { type: '应用题', content: '动物园里有猴子8只，大熊猫的只数是猴子的3倍，大熊猫有多少只？', answer: '8×3=24（只）', difficulty: 2 },
      { type: '应用题', content: '小红有12朵花，小兰的花是小红的一半，小兰有几朵花？', answer: '12÷2=6（朵）', difficulty: 2 },
      { type: '应用题', content: '爸爸今年36岁，是小明年龄的4倍，小明今年几岁？', answer: '36÷4=9（岁）', difficulty: 2 },
      { type: '应用题', content: '果园里有梨树15棵，苹果树是梨树的3倍，苹果树比梨树多多少棵？', answer: '15×3-15=30（棵）', difficulty: 3 },
      { type: '比较大小', content: '在○里填上">"、"<"或"="。\n4的5倍 ○ 5的4倍', answer: '=', difficulty: 2 },
      { type: '应用题', content: '一支钢笔8元，一支铅笔的价钱是钢笔的2倍少3元，一支铅笔多少元？', answer: '8×2-3=13（元）', difficulty: 3 },
      { type: '填空题', content: '一个数的5倍是35，这个数是（  ）。', answer: '7', difficulty: 2 },
    ],
  },

  // ==================== 三年级下册 ====================
  {
    id: 'g3x-u1',
    unitName: '位置与方向（一）',
    grade: 3,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '早晨起来，面向太阳，前面是（  ），后面是（  ），左面是（  ），右面是（  ）。', answer: '东；西；北；南', difficulty: 1 },
      { type: '填空题', content: '地图通常是按上（  ）、下（  ）、左（  ）、右（  ）绘制的。', answer: '北；南；西；东', difficulty: 1 },
      { type: '选择题', content: '小明的家在学校的东面，那么学校在小明家的（  ）面。\nA. 东  B. 西  C. 南', answer: 'B', difficulty: 1 },
      { type: '选择题', content: '图书馆在教学楼的东北方向，教学楼在图书馆的（  ）方向。\nA. 东北  B. 西南  C. 东南', answer: 'B', difficulty: 2 },
      { type: '判断题', content: '南和北是相对的方向。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '面对北方，右手边是东方。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '西北方向在北和西之间。（  ）', answer: '√', difficulty: 1 },
      { type: '应用题', content: '小明从家出发，先向东走200米到学校，再向北走300米到图书馆。请描述从图书馆回家的路线。', answer: '先向南走300米到学校，再向西走200米到家', difficulty: 3 },
      { type: '填空题', content: '东北方向和（  ）方向相对。', answer: '西南', difficulty: 2 },
      { type: '应用题', content: '看图回答：小兔在小猫的南面，小狗在小猫的东面，那么小兔在小狗的（  ）面。', answer: '西南', difficulty: 3 },
    ],
  },
  {
    id: 'g3x-u2',
    unitName: '除数是一位数的除法',
    grade: 3,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '计算题', content: '84 ÷ 4 =', answer: '21', difficulty: 1 },
      { type: '计算题', content: '96 ÷ 3 =', answer: '32', difficulty: 1 },
      { type: '计算题', content: '75 ÷ 5 =', answer: '15', difficulty: 1 },
      { type: '计算题', content: '68 ÷ 2 =', answer: '34', difficulty: 1 },
      { type: '计算题', content: '144 ÷ 6 =', answer: '24', difficulty: 2 },
      { type: '计算题', content: '205 ÷ 5 =', answer: '41', difficulty: 2 },
      { type: '计算题', content: '312 ÷ 3 =', answer: '104', difficulty: 2 },
      { type: '计算题', content: '450 ÷ 9 =', answer: '50', difficulty: 2 },
      { type: '竖式计算', content: '用竖式计算：\n  96\n÷  4\n------', answer: '24', difficulty: 2 },
      { type: '竖式计算', content: '用竖式计算：\n  78\n÷  3\n------', answer: '26', difficulty: 2 },
      { type: '应用题', content: '学校买了156本课外书，平均分给3个年级，每个年级分多少本？', answer: '156÷3=52（本）', difficulty: 2 },
      { type: '应用题', content: '一箱苹果重24千克，4箱苹果重多少千克？', answer: '24×4=96（千克）', difficulty: 2 },
      { type: '应用题', content: '有425个乒乓球，每5个装一盒，可以装多少盒？还剩几个？', answer: '425÷5=85（盒），不剩', difficulty: 3 },
    ],
  },
  {
    id: 'g3x-u3',
    unitName: '面积',
    grade: 3,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '长方形的面积 =（  ）×（  ）', answer: '长；宽', difficulty: 1 },
      { type: '填空题', content: '正方形的面积 =（  ）×（  ）', answer: '边长；边长', difficulty: 1 },
      { type: '填空题', content: '1平方米 =（  ）平方分米', answer: '100', difficulty: 1 },
      { type: '填空题', content: '1平方分米 =（  ）平方厘米', answer: '100', difficulty: 1 },
      { type: '计算题', content: '一个长方形，长8厘米，宽5厘米，面积是多少？', answer: '8×5=40（平方厘米）', difficulty: 1 },
      { type: '计算题', content: '一个正方形，边长6分米，面积是多少？', answer: '6×6=36（平方分米）', difficulty: 1 },
      { type: '计算题', content: '一个长方形，长12米，宽8米，周长是多少？', answer: '(12+8)×2=40（米）', difficulty: 2 },
      { type: '选择题', content: '用4个边长1厘米的小正方形拼成一个大正方形，大正方形的面积是（  ）。\nA. 4平方厘米  B. 8平方厘米  C. 16平方厘米', answer: 'A', difficulty: 2 },
      { type: '判断题', content: '面积相等的长方形，周长也一定相等。（  ）', answer: '×', difficulty: 3 },
      { type: '判断题', content: '周长相等的正方形，面积一定相等。（  ）', answer: '√', difficulty: 2 },
      { type: '应用题', content: '一间教室长9米，宽6米，这间教室的面积是多少平方米？', answer: '9×6=54（平方米）', difficulty: 2 },
      { type: '应用题', content: '一块长方形菜地，长15米，宽8米。如果在菜地四周围上篱笆，篱笆长多少米？', answer: '(15+8)×2=46（米）', difficulty: 2 },
      { type: '应用题', content: '一个长方形花坛，面积是48平方米，长是8米，宽是多少米？', answer: '48÷8=6（米）', difficulty: 2 },
      { type: '计算题', content: '5平方米 =（  ）平方分米', answer: '500', difficulty: 1 },
    ],
  },

  // ==================== 四年级上册 ====================
  {
    id: 'g4s-u1',
    unitName: '大数的认识',
    grade: 4,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '从个位起，每（  ）个数位是一级，分别是个级、万级、亿级。', answer: '四', difficulty: 1 },
      { type: '填空题', content: '10个一万是（  ），10个一百万是（  ）。', answer: '十万；一千万', difficulty: 1 },
      { type: '填空题', content: '5006000读作（  ），这个数的最高位是（  ）位。', answer: '五百万六千；百万', difficulty: 2 },
      { type: '填空题', content: '由3个亿、5个百万和2个一组成的数是（  ）。', answer: '305000002', difficulty: 2 },
      { type: '填空题', content: '把345670省略万位后面的尾数约是（  ）万。', answer: '35', difficulty: 2 },
      { type: '计算题', content: '30000 + 5000 + 400 + 70 =', answer: '35470', difficulty: 1 },
      { type: '计算题', content: '800000 - 35000 =', answer: '765000', difficulty: 1 },
      { type: '选择题', content: '下面各数中，一个零也不读的是（  ）。\nA. 3005000  B. 3050000  C. 3000500', answer: 'B', difficulty: 2 },
      { type: '判断题', content: '万级包括万位、十万位、百万位、千万位。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '40506000读作四千零五十万六千。（  ）', answer: '√', difficulty: 2 },
      { type: '应用题', content: '一个数由2个亿、8个千万和5个万组成，这个数是多少？', answer: '280050000', difficulty: 2 },
      { type: '应用题', content: '某城市人口约是8960000人，省略万位后面的尾数约是多少万人？', answer: '896万人', difficulty: 2 },
    ],
  },
  {
    id: 'g4s-u2',
    unitName: '公顷和平方千米',
    grade: 4,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '1公顷 =（  ）平方米', answer: '10000', difficulty: 1 },
      { type: '填空题', content: '1平方千米 =（  ）公顷', answer: '100', difficulty: 1 },
      { type: '填空题', content: '1平方千米 =（  ）平方米', answer: '1000000', difficulty: 2 },
      { type: '填空题', content: '5公顷 =（  ）平方米', answer: '50000', difficulty: 1 },
      { type: '填空题', content: '300公顷 =（  ）平方千米', answer: '3', difficulty: 1 },
      { type: '选择题', content: '一个足球场的面积大约是7000平方米，（  ）个这样的足球场面积约是1公顷。\nA. 7  B. 10  C. 14', answer: 'C', difficulty: 2 },
      { type: '选择题', content: '计量一个国家的面积，通常用（  ）作单位。\nA. 平方米  B. 公顷  C. 平方千米', answer: 'C', difficulty: 1 },
      { type: '判断题', content: '1公顷比1平方千米大。（  ）', answer: '×', difficulty: 1 },
      { type: '判断题', content: '边长是100米的正方形面积是1公顷。（  ）', answer: '√', difficulty: 2 },
      { type: '计算题', content: '8公顷 - 30000平方米 =（  ）平方米', answer: '50000', difficulty: 2 },
      { type: '应用题', content: '一个长方形果园，长500米，宽200米，这个果园的面积是多少公顷？', answer: '500×200=100000（平方米）=10公顷', difficulty: 3 },
      { type: '应用题', content: '一块正方形土地的面积是4公顷，它的边长是多少米？', answer: '200米', difficulty: 3 },
    ],
  },
  {
    id: 'g4s-u3',
    unitName: '角的度量',
    grade: 4,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '线段有（  ）个端点，射线有（  ）个端点，直线（  ）端点。', answer: '两；一；没有', difficulty: 1 },
      { type: '填空题', content: '1个平角 =（  ）度 =（  ）个直角', answer: '180；2', difficulty: 1 },
      { type: '填空题', content: '1个周角 =（  ）度 =（  ）个平角', answer: '360；2', difficulty: 1 },
      { type: '填空题', content: '把线段向两端无限延伸，就得到一条（  ）。', answer: '直线', difficulty: 1 },
      { type: '填空题', content: '度量角的大小要用（  ），角的计量单位是（  ）。', answer: '量角器；度', difficulty: 1 },
      { type: '计算题', content: '一个角是35度，它是（  ）角。', answer: '锐', difficulty: 1 },
      { type: '计算题', content: '一个钝角的范围是大于（  ）度且小于（  ）度。', answer: '90；180', difficulty: 2 },
      { type: '选择题', content: '下面各角中，最大的是（  ）。\nA. 锐角  B. 直角  C. 钝角', answer: 'C', difficulty: 1 },
      { type: '判断题', content: '一条射线长5厘米。（  ）', answer: '×', difficulty: 2 },
      { type: '判断题', content: '角的两边画得越长，角就越大。（  ）', answer: '×', difficulty: 1 },
      { type: '计算题', content: '已知∠1 = 35度，∠2 = 55度，∠1 + ∠2 =（  ）度。', answer: '90', difficulty: 2 },
      { type: '应用题', content: '把一个平角分成两个角，其中一个角是70度，另一个角是多少度？', answer: '180-70=110（度）', difficulty: 2 },
    ],
  },
  {
    id: 'g4s-u4',
    unitName: '三位数乘两位数',
    grade: 4,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '计算题', content: '123 × 12 =', answer: '1476', difficulty: 1 },
      { type: '计算题', content: '245 × 13 =', answer: '3185', difficulty: 1 },
      { type: '计算题', content: '306 × 24 =', answer: '7344', difficulty: 2 },
      { type: '计算题', content: '450 × 20 =', answer: '9000', difficulty: 1 },
      { type: '计算题', content: '178 × 35 =', answer: '6230', difficulty: 2 },
      { type: '计算题', content: '260 × 14 =', answer: '3640', difficulty: 1 },
      { type: '计算题', content: '408 × 25 =', answer: '10200', difficulty: 2 },
      { type: '估算题', content: '估算：298 × 31 ≈（  ）', answer: '9000', difficulty: 2 },
      { type: '估算题', content: '估算：412 × 19 ≈（  ）', answer: '8000', difficulty: 2 },
      { type: '应用题', content: '学校买了15套桌椅，每套185元，一共花了多少元？', answer: '185×15=2775（元）', difficulty: 2 },
      { type: '应用题', content: '一个果园有24行苹果树，每行126棵，这个果园一共有多少棵苹果树？', answer: '126×24=3024（棵）', difficulty: 2 },
      { type: '应用题', content: '一辆汽车从甲地开往乙地，每小时行驶85千米，行驶了12小时到达，甲乙两地相距多少千米？', answer: '85×12=1020（千米）', difficulty: 2 },
    ],
  },
  {
    id: 'g4s-u5',
    unitName: '平行四边形和梯形',
    grade: 4,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '在同一个平面内不相交的两条直线叫做（  ），也可以说这两条直线（  ）。', answer: '平行线；互相平行', difficulty: 1 },
      { type: '填空题', content: '两条直线相交成直角，就说这两条直线互相（  ），其中一条直线是另一条直线的（  ）。', answer: '垂直；垂线', difficulty: 1 },
      { type: '填空题', content: '平行四边形有（  ）组对边分别平行，梯形只有（  ）组对边平行。', answer: '两；一', difficulty: 1 },
      { type: '填空题', content: '从平行四边形一条边上的一点到对边引一条垂线，这点和垂足之间的线段叫做平行四边形的（  ），垂足所在的边叫做平行四边形的（  ）。', answer: '高；底', difficulty: 2 },
      { type: '填空题', content: '梯形中互相平行的一组对边分别叫做梯形的（  ）和（  ）。', answer: '上底；下底', difficulty: 1 },
      { type: '判断题', content: '长方形和正方形都是特殊的平行四边形。（  ）', answer: '√', difficulty: 2 },
      { type: '判断题', content: '平行四边形是特殊的梯形。（  ）', answer: '×', difficulty: 2 },
      { type: '判断题', content: '两条直线不相交就一定平行。（  ）', answer: '×', difficulty: 3 },
      { type: '选择题', content: '下面图形中，只有一组对边平行的是（  ）。\nA. 平行四边形  B. 长方形  C. 梯形', answer: 'C', difficulty: 1 },
      { type: '选择题', content: '过直线外一点画已知直线的平行线，可以画（  ）条。\nA. 1  B. 2  C. 无数', answer: 'A', difficulty: 2 },
      { type: '填空题', content: '两腰相等的梯形叫做（  ）梯形。', answer: '等腰', difficulty: 1 },
      { type: '判断题', content: '平行四边形的对角相等。（  ）', answer: '√', difficulty: 2 },
    ],
  },

  // ==================== 四年级下册 ====================
  {
    id: 'g4x-u1',
    unitName: '四则运算',
    grade: 4,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '计算题', content: '125 + 75 - 50 =', answer: '150', difficulty: 1 },
      { type: '计算题', content: '360 ÷ 9 × 4 =', answer: '160', difficulty: 1 },
      { type: '计算题', content: '200 - 36 × 4 =', answer: '56', difficulty: 2 },
      { type: '计算题', content: '(125 + 25) × 4 =', answer: '600', difficulty: 2 },
      { type: '计算题', content: '480 ÷ (16 - 4) =', answer: '40', difficulty: 2 },
      { type: '计算题', content: '72 ÷ 8 + 56 × 2 =', answer: '121', difficulty: 2 },
      { type: '计算题', content: '350 - 150 ÷ 5 × 3 =', answer: '260', difficulty: 3 },
      { type: '填空题', content: '在没有括号的算式里，如果只有加减法或者只有乘除法，都要从（  ）往（  ）按顺序计算。', answer: '左；右', difficulty: 1 },
      { type: '填空题', content: '在没有括号的算式里，有乘除法和加减法，要先算（  ）法，再算（  ）法。', answer: '乘除；加减', difficulty: 1 },
      { type: '选择题', content: '50 + 50 ÷ 5 =（  ）\nA. 20  B. 60  C. 100', answer: 'B', difficulty: 2 },
      { type: '应用题', content: '学校买了6箱乒乓球，每箱12个，每个2元，一共花了多少元？', answer: '6×12×2=144（元）', difficulty: 2 },
      { type: '应用题', content: '小明有100元，买了3本书，每本25元，还剩多少元？', answer: '100-3×25=25（元）', difficulty: 2 },
    ],
  },
  {
    id: 'g4x-u2',
    unitName: '运算定律',
    grade: 4,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '两个数相加，交换加数的位置，（  ）不变，这叫做加法交换律。', answer: '和', difficulty: 1 },
      { type: '填空题', content: '三个数相加，先把前两个数相加，或者先把后两个数相加，（  ）不变，这叫做加法结合律。', answer: '和', difficulty: 1 },
      { type: '填空题', content: 'a × b = b × a 这是（  ）律。', answer: '乘法交换', difficulty: 1 },
      { type: '填空题', content: '(a × b) × c = a × (b × c) 这是（  ）律。', answer: '乘法结合', difficulty: 1 },
      { type: '填空题', content: 'a × (b + c) = a × b + a × c 这是（  ）律。', answer: '乘法分配', difficulty: 1 },
      { type: '计算题', content: '用简便方法计算：\n125 × 32 =', answer: '125×8×4=4000', difficulty: 2 },
      { type: '计算题', content: '用简便方法计算：\n99 × 45 =', answer: '(100-1)×45=4500-45=4455', difficulty: 2 },
      { type: '计算题', content: '用简便方法计算：\n36 × 99 + 36 =', answer: '36×(99+1)=36×100=3600', difficulty: 2 },
      { type: '计算题', content: '用简便方法计算：\n25 × (40 + 4) =', answer: '25×40+25×4=1000+100=1100', difficulty: 2 },
      { type: '计算题', content: '用简便方法计算：\n987 - 299 =', answer: '987-300+1=688', difficulty: 2 },
      { type: '判断题', content: 'a + b = b + a 运用了加法交换律。（  ）', answer: '√', difficulty: 1 },
      { type: '计算题', content: '用简便方法计算：\n72 × 125 =', answer: '9×(8×125)=9×1000=9000', difficulty: 3 },
    ],
  },
  {
    id: 'g4x-u3',
    unitName: '小数的意义和性质',
    grade: 4,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '0.3里面有（  ）个十分之一，0.03里面有（  ）个百分之一。', answer: '3；3', difficulty: 1 },
      { type: '填空题', content: '0.8的计数单位是（  ），它有（  ）个这样的单位。', answer: '0.1（或十分之一）；8', difficulty: 1 },
      { type: '填空题', content: '3.56是由（  ）个一、（  ）个十分之一和（  ）个百分之一组成的。', answer: '3；5；6', difficulty: 2 },
      { type: '填空题', content: '把0.36的小数点向右移动两位是（  ），扩大到原来的（  ）倍。', answer: '36；100', difficulty: 2 },
      { type: '填空题', content: '把25缩小到原来的1/100是（  ）。', answer: '0.25', difficulty: 2 },
      { type: '判断题', content: '小数点的末尾添上"0"或去掉"0"，小数的大小不变。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '0.8和0.80的大小相等，计数单位也相同。（  ）', answer: '×', difficulty: 2 },
      { type: '判断题', content: '小数一定比整数小。（  ）', answer: '×', difficulty: 1 },
      { type: '选择题', content: '把3.090化简后是（  ）。\nA. 3.09  B. 3.9  C. 3.090', answer: 'A', difficulty: 1 },
      { type: '选择题', content: '与4.5相等的小数是（  ）。\nA. 4.05  B. 4.50  C. 4.500', answer: 'B', difficulty: 2 },
      { type: '计算题', content: '比较大小：0.6 ○ 0.59', answer: '>', difficulty: 1 },
      { type: '计算题', content: '把下面的数按从小到大排列：\n0.8、0.801、0.81、0.799', answer: '0.799 < 0.8 < 0.801 < 0.81', difficulty: 3 },
    ],
  },
  {
    id: 'g4x-u4',
    unitName: '三角形',
    grade: 4,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '三角形有（  ）条边，（  ）个角，（  ）个顶点。', answer: '3；3；3', difficulty: 1 },
      { type: '填空题', content: '三角形的内角和是（  ）度。', answer: '180', difficulty: 1 },
      { type: '填空题', content: '按角分类，三角形可以分为（  ）三角形、（  ）三角形和（  ）三角形。', answer: '锐角；直角；钝角', difficulty: 1 },
      { type: '填空题', content: '等腰三角形的两条（  ）相等，两个（  ）相等。', answer: '腰；底角', difficulty: 1 },
      { type: '填空题', content: '三角形中任意两边之和（  ）第三边。', answer: '大于', difficulty: 2 },
      { type: '判断题', content: '一个三角形中最多有一个直角。（  ）', answer: '√', difficulty: 2 },
      { type: '判断题', content: '等边三角形一定是锐角三角形。（  ）', answer: '√', difficulty: 2 },
      { type: '判断题', content: '一个三角形中可以有两个钝角。（  ）', answer: '×', difficulty: 1 },
      { type: '选择题', content: '一个三角形中，两个内角分别是50度和70度，第三个内角是（  ）度。\nA. 50  B. 60  C. 70', answer: 'B', difficulty: 2 },
      { type: '选择题', content: '下面哪组线段可以围成三角形？（  ）\nA. 3cm、4cm、8cm  B. 2cm、3cm、6cm  C. 3cm、4cm、5cm', answer: 'C', difficulty: 2 },
      { type: '计算题', content: '一个等腰三角形的一个底角是70度，它的顶角是多少度？', answer: '180-70×2=40（度）', difficulty: 2 },
      { type: '应用题', content: '一个三角形的三个内角的度数比是1:2:3，这个三角形中最大的角是多少度？是什么三角形？', answer: '180÷(1+2+3)×3=90（度），直角三角形', difficulty: 3 },
    ],
  },
  {
    id: 'g4x-u5',
    unitName: '小数的加法和减法',
    grade: 4,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '计算题', content: '3.5 + 2.8 =', answer: '6.3', difficulty: 1 },
      { type: '计算题', content: '7.2 - 3.5 =', answer: '3.7', difficulty: 1 },
      { type: '计算题', content: '10 - 4.36 =', answer: '5.64', difficulty: 2 },
      { type: '计算题', content: '12.5 + 7.86 =', answer: '20.36', difficulty: 2 },
      { type: '计算题', content: '8.45 - 3.67 =', answer: '4.78', difficulty: 2 },
      { type: '计算题', content: '15.3 + 4.7 - 6.8 =', answer: '13.2', difficulty: 2 },
      { type: '计算题', content: '20 - (5.4 + 3.6) =', answer: '11', difficulty: 2 },
      { type: '计算题', content: '6.38 + 2.45 + 3.62 =', answer: '12.45', difficulty: 2 },
      { type: '计算题', content: '9.56 - 2.78 - 4.22 =', answer: '2.56', difficulty: 2 },
      { type: '选择题', content: '5.2 + 3.8 - 5.2 + 3.8 =（  ）\nA. 0  B. 7.6  C. 15.2', answer: 'B', difficulty: 3 },
      { type: '应用题', content: '小明买一本书花了12.5元，买一支钢笔花了8.6元，他付了25元，应找回多少元？', answer: '25-12.5-8.6=3.9（元）', difficulty: 2 },
      { type: '应用题', content: '一根绳子长10米，第一次剪去3.5米，第二次剪去2.8米，还剩多少米？', answer: '10-3.5-2.8=3.7（米）', difficulty: 2 },
    ],
  },

  // ==================== 五年级上册 ====================
  {
    id: 'g5s-u1',
    unitName: '小数乘法',
    grade: 5,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '计算题', content: '2.5 × 3 =', answer: '7.5', difficulty: 1 },
      { type: '计算题', content: '0.8 × 0.5 =', answer: '0.4', difficulty: 1 },
      { type: '计算题', content: '3.6 × 0.25 =', answer: '0.9', difficulty: 2 },
      { type: '计算题', content: '1.25 × 0.8 =', answer: '1', difficulty: 1 },
      { type: '计算题', content: '4.5 × 12 =', answer: '54', difficulty: 1 },
      { type: '计算题', content: '0.35 × 0.4 =', answer: '0.14', difficulty: 2 },
      { type: '计算题', content: '2.4 × 0.15 =', answer: '0.36', difficulty: 2 },
      { type: '计算题', content: '7.2 × 0.5 =', answer: '3.6', difficulty: 1 },
      { type: '估算题', content: '估算：2.9 × 3.1 ≈（  ）', answer: '9', difficulty: 2 },
      { type: '应用题', content: '苹果每千克5.6元，买3.5千克需要多少元？', answer: '5.6×3.5=19.6（元）', difficulty: 2 },
      { type: '应用题', content: '一块长方形菜地，长8.5米，宽4.6米，这块菜地的面积是多少平方米？', answer: '8.5×4.6=39.1（平方米）', difficulty: 2 },
      { type: '应用题', content: '小明家每月用水8.5吨，每吨水费2.4元，小明家每月要交水费多少元？', answer: '8.5×2.4=20.4（元）', difficulty: 2 },
    ],
  },
  {
    id: 'g5s-u2',
    unitName: '小数除法',
    grade: 5,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '计算题', content: '7.2 ÷ 0.8 =', answer: '9', difficulty: 1 },
      { type: '计算题', content: '4.5 ÷ 0.05 =', answer: '90', difficulty: 1 },
      { type: '计算题', content: '6.3 ÷ 0.7 =', answer: '9', difficulty: 1 },
      { type: '计算题', content: '12.6 ÷ 0.3 =', answer: '42', difficulty: 1 },
      { type: '计算题', content: '5.6 ÷ 0.04 =', answer: '140', difficulty: 2 },
      { type: '计算题', content: '3.6 ÷ 1.2 =', answer: '3', difficulty: 1 },
      { type: '计算题', content: '10 ÷ 0.25 =', answer: '40', difficulty: 1 },
      { type: '计算题', content: '7.5 ÷ 2.5 =', answer: '3', difficulty: 1 },
      { type: '填空题', content: '5.7454545...是一个（  ）小数，用简便方法写作（  ）。', answer: '循环；5.74̇5̇', difficulty: 2 },
      { type: '选择题', content: '下面各数中，是有限小数的是（  ）。\nA. 1/3  B. 2/5  C. 5/6', answer: 'B', difficulty: 2 },
      { type: '应用题', content: '妈妈买了4.5千克苹果，花了27元，平均每千克苹果多少元？', answer: '27÷4.5=6（元）', difficulty: 2 },
      { type: '应用题', content: '一辆汽车行驶15.6千米用了1.2升汽油，平均每升汽油能行驶多少千米？', answer: '15.6÷1.2=13（千米）', difficulty: 2 },
    ],
  },
  {
    id: 'g5s-u3',
    unitName: '简易方程',
    grade: 5,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '用字母表示乘法分配律：（a + b）× c =（  ）', answer: 'a×c + b×c', difficulty: 1 },
      { type: '填空题', content: '用字母表示长方形的周长公式：C =（  ）', answer: '2(a + b)', difficulty: 1 },
      { type: '填空题', content: '用字母表示正方形的面积公式：S =（  ）', answer: 'a²', difficulty: 1 },
      { type: '填空题', content: '当 a = 5 时，2a + 3 =（  ）。', answer: '13', difficulty: 2 },
      { type: '填空题', content: '当 x = 4 时，x² - 2x =（  ）。', answer: '8', difficulty: 2 },
      { type: '计算题', content: '解方程：\nx + 8 = 15', answer: 'x = 7', difficulty: 1 },
      { type: '计算题', content: '解方程：\nx - 3.5 = 7.2', answer: 'x = 10.7', difficulty: 1 },
      { type: '计算题', content: '解方程：\n2x = 18', answer: 'x = 9', difficulty: 1 },
      { type: '计算题', content: '解方程：\n3x + 5 = 20', answer: 'x = 5', difficulty: 2 },
      { type: '计算题', content: '解方程：\n4x - 7 = 13', answer: 'x = 5', difficulty: 2 },
      { type: '应用题', content: '小明买了3本笔记本，每本x元，付了20元，找回5元。列出方程并求解。', answer: '3x + 5 = 20，x = 5', difficulty: 3 },
      { type: '应用题', content: '一个数的3倍减去4.5等于10.5，这个数是多少？（用方程解）', answer: '3x - 4.5 = 10.5，x = 5', difficulty: 3 },
    ],
  },
  {
    id: 'g5s-u4',
    unitName: '多边形的面积',
    grade: 5,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '平行四边形的面积 =（  ）×（  ）', answer: '底；高', difficulty: 1 },
      { type: '填空题', content: '三角形的面积 =（  ）×（  ）÷ 2', answer: '底；高', difficulty: 1 },
      { type: '填空题', content: '梯形的面积 =（  ）×（  ）÷ 2', answer: '(上底+下底)；高', difficulty: 1 },
      { type: '计算题', content: '一个平行四边形，底12厘米，高8厘米，面积是多少？', answer: '12×8=96（平方厘米）', difficulty: 1 },
      { type: '计算题', content: '一个三角形，底10分米，高6分米，面积是多少？', answer: '10×6÷2=30（平方分米）', difficulty: 1 },
      { type: '计算题', content: '一个梯形，上底5厘米，下底9厘米，高6厘米，面积是多少？', answer: '(5+9)×6÷2=42（平方厘米）', difficulty: 2 },
      { type: '计算题', content: '一个平行四边形的面积是48平方米，底是8米，高是多少？', answer: '48÷8=6（米）', difficulty: 2 },
      { type: '计算题', content: '一个三角形的面积是25平方厘米，底是10厘米，高是多少？', answer: '25×2÷10=5（厘米）', difficulty: 2 },
      { type: '选择题', content: '一个平行四边形和一个三角形等底等高，平行四边形的面积是三角形的（  ）倍。\nA. 2  B. 3  C. 4', answer: 'A', difficulty: 2 },
      { type: '判断题', content: '两个面积相等的三角形一定能拼成一个平行四边形。（  ）', answer: '×', difficulty: 3 },
      { type: '应用题', content: '一块平行四边形菜地，底15米，高8米，如果每平方米收白菜6千克，这块地一共可以收白菜多少千克？', answer: '15×8×6=720（千克）', difficulty: 2 },
      { type: '应用题', content: '一块梯形花坛，上底4米，下底6米，高5米，面积是多少平方米？', answer: '(4+6)×5÷2=25（平方米）', difficulty: 2 },
    ],
  },

  // ==================== 五年级下册 ====================
  {
    id: 'g5x-u1',
    unitName: '观察物体',
    grade: 5,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '判断题', content: '从不同方向观察同一个物体，看到的形状可能不同。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '从正面看到的形状是正方形，这个物体一定是正方体。（  ）', answer: '×', difficulty: 2 },
      { type: '判断题', content: '一个物体从左面和右面看到的形状一定相同。（  ）', answer: '×', difficulty: 2 },
      { type: '选择题', content: '一个正方体从正面、上面和左面看到的都是（  ）。\nA. 三角形  B. 正方形  C. 长方形', answer: 'B', difficulty: 1 },
      { type: '选择题', content: '用4个小正方体搭成一个立体图形，从正面看到的是3个正方形，从上面看到的是2个正方形，这个立体图形最少需要（  ）个小正方体。\nA. 3  B. 4  C. 5', answer: 'B', difficulty: 3 },
      { type: '判断题', content: '一个长方体从不同方向看到的形状一定都是长方形。（  ）', answer: '×', difficulty: 2 },
      { type: '判断题', content: '观察一个物体，最多能同时看到3个面。（  ）', answer: '√', difficulty: 1 },
      { type: '选择题', content: '一个圆柱从正面看到的是一个（  ）。\nA. 圆  B. 长方形  C. 三角形', answer: 'B', difficulty: 1 },
      { type: '判断题', content: '用同样的小正方体搭成的立体图形，从正面看到的形状相同，它们的实际形状也一定相同。（  ）', answer: '×', difficulty: 3 },
      { type: '选择题', content: '从上面看一个立体图形，看到的是"田"字形，这个立体图形至少由（  ）个小正方体组成。\nA. 4  B. 5  C. 6', answer: 'A', difficulty: 3 },
    ],
  },
  {
    id: 'g5x-u2',
    unitName: '因数与倍数',
    grade: 5,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '在算式 3 × 7 = 21 中，（  ）和（  ）是21的因数，21是（  ）和（  ）的倍数。', answer: '3；7；3；7', difficulty: 1 },
      { type: '填空题', content: '一个数的最小因数是（  ），最大因数是（  ）。', answer: '1；它本身', difficulty: 1 },
      { type: '填空题', content: '一个数的最小倍数是（  ），（  ）最大倍数。', answer: '它本身；没有', difficulty: 1 },
      { type: '填空题', content: '在1~20中，既是偶数又是质数的数是（  ）。', answer: '2', difficulty: 2 },
      { type: '填空题', content: '12的因数有（  ），其中质数有（  ）。', answer: '1、2、3、4、6、12；2、3', difficulty: 2 },
      { type: '判断题', content: '1是所有非零自然数的因数。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '一个数的因数的个数是有限的。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '所有的质数都是奇数。（  ）', answer: '×', difficulty: 2 },
      { type: '判断题', content: '两个质数的和一定是偶数。（  ）', answer: '×', difficulty: 3 },
      { type: '选择题', content: '下面各数中，既是奇数又是合数的是（  ）。\nA. 7  B. 9  C. 2', answer: 'B', difficulty: 2 },
      { type: '选择题', content: '下面各数中，是质数的是（  ）。\nA. 21  B. 29  C. 33', answer: 'B', difficulty: 2 },
      { type: '填空题', content: '50以内最大的质数是（  ）。', answer: '47', difficulty: 2 },
    ],
  },
  {
    id: 'g5x-u3',
    unitName: '长方体和正方体',
    grade: 5,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '长方体有（  ）个面，（  ）条棱，（  ）个顶点。', answer: '6；12；8', difficulty: 1 },
      { type: '填空题', content: '长方体的表面积 =（  ）', answer: '(长×宽+长×高+宽×高)×2', difficulty: 1 },
      { type: '填空题', content: '长方体的体积 =（  ）', answer: '长×宽×高', difficulty: 1 },
      { type: '填空题', content: '正方体的体积 =（  ）', answer: '棱长×棱长×棱长', difficulty: 1 },
      { type: '填空题', content: '1立方米 =（  ）立方分米', answer: '1000', difficulty: 1 },
      { type: '计算题', content: '一个长方体，长8厘米，宽5厘米，高4厘米，表面积是多少？', answer: '(8×5+8×4+5×4)×2=184（平方厘米）', difficulty: 2 },
      { type: '计算题', content: '一个正方体，棱长6分米，体积是多少？', answer: '6×6×6=216（立方分米）', difficulty: 1 },
      { type: '计算题', content: '一个长方体，长10厘米，宽6厘米，高5厘米，体积是多少？', answer: '10×6×5=300（立方厘米）', difficulty: 1 },
      { type: '计算题', content: '一个正方体水箱，棱长4分米，它的容积是多少升？', answer: '4×4×4=64（升）', difficulty: 2 },
      { type: '应用题', content: '一个长方体游泳池，长50米，宽25米，深2米，这个游泳池的容积是多少立方米？', answer: '50×25×2=2500（立方米）', difficulty: 2 },
      { type: '应用题', content: '一个长方体纸箱，长40厘米，宽30厘米，高20厘米，做这个纸箱至少需要多少平方厘米的纸板？', answer: '(40×30+40×20+30×20)×2=5200（平方厘米）', difficulty: 2 },
      { type: '应用题', content: '一个正方体石块，棱长5分米，它的体积是多少立方分米？如果每立方分米重2.5千克，这块石块重多少千克？', answer: '5×5×5=125（立方分米），125×2.5=312.5（千克）', difficulty: 3 },
    ],
  },
  {
    id: 'g5x-u4',
    unitName: '分数的意义和性质',
    grade: 5,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '把单位"1"平均分成8份，表示其中的3份，用分数表示是（  ），它的分数单位是（  ）。', answer: '3/8；1/8', difficulty: 1 },
      { type: '填空题', content: '3/4的分数单位是（  ），它有（  ）个这样的分数单位。', answer: '1/4；3', difficulty: 1 },
      { type: '填空题', content: '分子和分母（  ）的分数，叫做最简分数。', answer: '只有公因数1', difficulty: 1 },
      { type: '填空题', content: '把12/18化成最简分数是（  ）。', answer: '2/3', difficulty: 2 },
      { type: '填空题', content: '分数的分子和分母同时乘以或除以（  ）的数（0除外），分数的大小不变。', answer: '相同', difficulty: 1 },
      { type: '判断题', content: '分数的分子和分母同时加上同一个数，分数的大小不变。（  ）', answer: '×', difficulty: 2 },
      { type: '判断题', content: '最简分数的分子和分母只有公因数1。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '假分数都大于1。（  ）', answer: '×', difficulty: 2 },
      { type: '选择题', content: '下面各分数中，是最简分数的是（  ）。\nA. 4/8  B. 5/7  C. 6/9', answer: 'B', difficulty: 1 },
      { type: '选择题', content: '把5/6和3/4通分，用（  ）作公分母。\nA. 10  B. 12  C. 24', answer: 'B', difficulty: 2 },
      { type: '计算题', content: '把2/3和4/5通分。', answer: '2/3=10/15，4/5=12/15', difficulty: 2 },
      { type: '计算题', content: '把8/12化成最简分数。', answer: '8/12=2/3', difficulty: 2 },
    ],
  },
  {
    id: 'g5x-u5',
    unitName: '分数的加法和减法',
    grade: 5,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '计算题', content: '1/4 + 2/4 =', answer: '3/4', difficulty: 1 },
      { type: '计算题', content: '5/6 - 1/6 =', answer: '2/3', difficulty: 1 },
      { type: '计算题', content: '1/2 + 1/3 =', answer: '5/6', difficulty: 2 },
      { type: '计算题', content: '3/4 - 1/3 =', answer: '5/12', difficulty: 2 },
      { type: '计算题', content: '2/5 + 3/10 =', answer: '7/10', difficulty: 2 },
      { type: '计算题', content: '7/8 - 3/4 =', answer: '1/8', difficulty: 2 },
      { type: '计算题', content: '1 - 3/7 =', answer: '4/7', difficulty: 1 },
      { type: '计算题', content: '5/6 + 3/8 =', answer: '29/24', difficulty: 2 },
      { type: '计算题', content: '1/2 + 1/3 + 1/6 =', answer: '1', difficulty: 2 },
      { type: '计算题', content: '5/6 - 1/4 - 1/3 =', answer: '1/4', difficulty: 3 },
      { type: '应用题', content: '一根铁丝长2米，第一次用去1/3米，第二次用去1/4米，还剩多少米？', answer: '2 - 1/3 - 1/4 = 5/12（米）', difficulty: 2 },
      { type: '应用题', content: '一块蛋糕，小明吃了1/4，小红吃了1/3，两人一共吃了这块蛋糕的几分之几？', answer: '1/4 + 1/3 = 7/12', difficulty: 2 },
    ],
  },

  // ==================== 六年级上册 ====================
  {
    id: 'g6s-u1',
    unitName: '分数乘法',
    grade: 6,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '计算题', content: '2/3 × 3/4 =', answer: '1/2', difficulty: 1 },
      { type: '计算题', content: '5/6 × 12 =', answer: '10', difficulty: 1 },
      { type: '计算题', content: '3/8 × 4/9 =', answer: '1/6', difficulty: 2 },
      { type: '计算题', content: '7/12 × 6/7 =', answer: '1/2', difficulty: 1 },
      { type: '计算题', content: '15 × 2/5 =', answer: '6', difficulty: 1 },
      { type: '计算题', content: '4/5 × 5/8 =', answer: '1/2', difficulty: 1 },
      { type: '计算题', content: '2/3 × 3/5 × 5/7 =', answer: '2/7', difficulty: 2 },
      { type: '计算题', content: '3/4 × 8 =', answer: '6', difficulty: 1 },
      { type: '应用题', content: '一根绳子长12米，用去了它的2/3，用去了多少米？', answer: '12×2/3=8（米）', difficulty: 2 },
      { type: '应用题', content: '一本书有240页，小红第一天看了全书的1/4，第二天看了全书的1/6，两天一共看了多少页？', answer: '240×1/4+240×1/6=100（页）', difficulty: 2 },
      { type: '应用题', content: '果园里有苹果树120棵，梨树的棵数是苹果树的3/4，梨树有多少棵？', answer: '120×3/4=90（棵）', difficulty: 2 },
      { type: '应用题', content: '一件衣服原价200元，现在打八折出售，现在售价多少元？', answer: '200×8/10=160（元）', difficulty: 3 },
    ],
  },
  {
    id: 'g6s-u2',
    unitName: '位置与方向（二）',
    grade: 6,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '确定物体位置的两个条件是（  ）和（  ）。', answer: '方向；距离', difficulty: 1 },
      { type: '填空题', content: '小明在小红的北偏东30度方向200米处，那么小红在小明的（  ）方向（  ）米处。', answer: '南偏西30度；200', difficulty: 2 },
      { type: '填空题', content: '以学校为观测点，图书馆在学校的北偏西45度方向300米处，这句话中的观测点是（  ）。', answer: '学校', difficulty: 1 },
      { type: '填空题', content: '描述路线时，需要说清楚每一段的（  ）和（  ）。', answer: '方向；距离', difficulty: 1 },
      { type: '填空题', content: '东偏北30度也可以说成（  ）偏（  ）60度。', answer: '北；东', difficulty: 2 },
      { type: '选择题', content: '以广场为观测点，学校在广场的北偏西35度方向，那么以学校为观测点，广场在学校的（  ）方向。\nA. 南偏东35度  B. 南偏西35度  C. 北偏东35度', answer: 'A', difficulty: 2 },
      { type: '判断题', content: '确定位置时，方向和距离缺一不可。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '北偏东40度和东偏北50度表示的方向相同。（  ）', answer: '√', difficulty: 2 },
      { type: '应用题', content: '从学校出发，向北偏东30度方向走400米到书店，再向东偏南45度方向走300米到超市。请描述从超市回到学校的路线。', answer: '从超市出发，向西偏北45度方向走300米到书店，再向南偏西30度方向走400米到学校', difficulty: 3 },
      { type: '填空题', content: '在平面图上，通常用（  ）方向为基准方向来描述物体的位置。', answer: '北', difficulty: 1 },
    ],
  },
  {
    id: 'g6s-u3',
    unitName: '分数除法',
    grade: 6,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '计算题', content: '3/4 ÷ 3 =', answer: '1/4', difficulty: 1 },
      { type: '计算题', content: '5/6 ÷ 5/12 =', answer: '2', difficulty: 1 },
      { type: '计算题', content: '8 ÷ 4/5 =', answer: '10', difficulty: 1 },
      { type: '计算题', content: '2/3 ÷ 4/9 =', answer: '3/2', difficulty: 2 },
      { type: '计算题', content: '7/8 ÷ 7 =', answer: '1/8', difficulty: 1 },
      { type: '计算题', content: '12 ÷ 3/4 =', answer: '16', difficulty: 1 },
      { type: '计算题', content: '5/6 ÷ 10/9 =', answer: '3/4', difficulty: 2 },
      { type: '计算题', content: '4/5 ÷ 2/3 =', answer: '6/5', difficulty: 2 },
      { type: '应用题', content: '一桶油重20千克，用去了它的3/4，用去了多少千克？', answer: '20×3/4=15（千克）', difficulty: 2 },
      { type: '应用题', content: '小明看一本书，已经看了全书的2/5，正好是60页，这本书一共有多少页？', answer: '60÷2/5=150（页）', difficulty: 2 },
      { type: '应用题', content: '一段路程，甲车行了全程的3/8，正好是45千米，全程是多少千米？', answer: '45÷3/8=120（千米）', difficulty: 2 },
      { type: '应用题', content: '学校图书馆有故事书480本，是科技书的3/5，科技书有多少本？', answer: '480÷3/5=800（本）', difficulty: 3 },
    ],
  },
  {
    id: 'g6s-u4',
    unitName: '比',
    grade: 6,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '两个数（  ）又叫做两个数的比。', answer: '相除', difficulty: 1 },
      { type: '填空题', content: '15 ÷ 10 =（  ）：（  ） =（  ）/（  ）', answer: '15；10；15；10', difficulty: 1 },
      { type: '填空题', content: '比的前项和后项同时乘以或除以（  ）的数（0除外），比值不变。', answer: '相同', difficulty: 1 },
      { type: '填空题', content: '化简比：12:8 =（  ）：（  ）', answer: '3；2', difficulty: 1 },
      { type: '填空题', content: '化简比：0.5:0.3 =（  ）：（  ）', answer: '5；3', difficulty: 2 },
      { type: '填空题', content: '化简比：2/3:4/9 =（  ）：（  ）', answer: '3；2', difficulty: 2 },
      { type: '计算题', content: '求比值：24:16 =', answer: '3/2（或1.5）', difficulty: 1 },
      { type: '计算题', content: '求比值：3/5:2/5 =', answer: '3/2（或1.5）', difficulty: 1 },
      { type: '选择题', content: '比的前项是6，比值是2/3，比的后项是（  ）。\nA. 4  B. 9  C. 12', answer: 'B', difficulty: 2 },
      { type: '判断题', content: '比的前项不能为0。（  ）', answer: '√', difficulty: 1 },
      { type: '应用题', content: '一杯糖水中，糖和水的比是1:20，如果有5克糖，需要加水多少克？', answer: '5×20=100（克）', difficulty: 2 },
      { type: '应用题', content: '甲乙两数的比是3:5，甲数是27，乙数是多少？', answer: '27÷3×5=45', difficulty: 2 },
    ],
  },
  {
    id: 'g6s-u5',
    unitName: '圆',
    grade: 6,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '圆的周长 C =（  ）或 C =（  ）', answer: 'πd；2πr', difficulty: 1 },
      { type: '填空题', content: '圆的面积 S =（  ）', answer: 'πr²', difficulty: 1 },
      { type: '填空题', content: '一个圆的半径是3厘米，它的直径是（  ）厘米，周长是（  ）厘米。', answer: '6；18.84', difficulty: 2 },
      { type: '填空题', content: '一个圆的直径是10厘米，它的面积是（  ）平方厘米。（π取3.14）', answer: '78.5', difficulty: 2 },
      { type: '计算题', content: '一个圆的半径是5厘米，求它的周长。（π取3.14）', answer: '2×3.14×5=31.4（厘米）', difficulty: 1 },
      { type: '计算题', content: '一个圆的直径是8分米，求它的面积。（π取3.14）', answer: '3.14×(8÷2)²=50.24（平方分米）', difficulty: 2 },
      { type: '计算题', content: '一个半圆形花坛，直径是6米，这个花坛的周长是多少米？（π取3.14）', answer: '3.14×6÷2+6=15.42（米）', difficulty: 3 },
      { type: '选择题', content: '圆的半径扩大2倍，面积扩大（  ）倍。\nA. 2  B. 4  C. 8', answer: 'B', difficulty: 2 },
      { type: '判断题', content: '所有的直径都是半径的2倍。（  ）', answer: '×', difficulty: 2 },
      { type: '判断题', content: '圆是轴对称图形，它有无数条对称轴。（  ）', answer: '√', difficulty: 1 },
      { type: '应用题', content: '一个圆形水池，周长是31.4米，它的面积是多少平方米？（π取3.14）', answer: '31.4÷3.14÷2=5（米），3.14×5²=78.5（平方米）', difficulty: 3 },
      { type: '应用题', content: '一个圆形花坛的直径是10米，在花坛周围铺一条2米宽的小路，小路的面积是多少平方米？（π取3.14）', answer: '3.14×(5+2)²-3.14×5²=3.14×(49-25)=75.36（平方米）', difficulty: 3 },
    ],
  },

  // ==================== 六年级下册 ====================
  {
    id: 'g6x-u1',
    unitName: '负数',
    grade: 6,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '在数轴上，0右边的数是（  ）数，左边的数是（  ）数。', answer: '正；负', difficulty: 1 },
      { type: '填空题', content: '如果零上5度记作+5度，那么零下3度记作（  ）度。', answer: '-3', difficulty: 1 },
      { type: '填空题', content: '如果收入500元记作+500元，那么支出300元记作（  ）元。', answer: '-300', difficulty: 1 },
      { type: '填空题', content: '在-3、0、+5、-1.5、+2.4中，正数有（  ），负数有（  ）。', answer: '+5、+2.4；-3、-1.5', difficulty: 1 },
      { type: '填空题', content: '（  ）既不是正数，也不是负数。', answer: '0', difficulty: 1 },
      { type: '判断题', content: '0是正数。（  ）', answer: '×', difficulty: 1 },
      { type: '判断题', content: '-5大于-3。（  ）', answer: '×', difficulty: 2 },
      { type: '判断题', content: '所有的正数都大于负数。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '在数轴上，从左到右的顺序就是数从小到大的顺序。（  ）', answer: '√', difficulty: 1 },
      { type: '选择题', content: '下面各数中，最小的数是（  ）。\nA. -2  B. 0  C. 1', answer: 'A', difficulty: 1 },
      { type: '选择题', content: '海拔-100米表示（  ）。\nA. 高于海平面100米  B. 低于海平面100米  C. 海平面100米处', answer: 'B', difficulty: 1 },
      { type: '填空题', content: '把+3、-5、0、-1、+2按从小到大的顺序排列：（  ）<（  ）<（  ）<（  ）<（  ）', answer: '-5 < -1 < 0 < +2 < +3', difficulty: 2 },
    ],
  },
  {
    id: 'g6x-u2',
    unitName: '百分数',
    grade: 6,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '3/5 =（  ）/20 =（  ）% =（  ）（填小数）', answer: '12；60；0.6', difficulty: 1 },
      { type: '填空题', content: '45%读作（  ），百分之三十五写作（  ）。', answer: '百分之四十五；35%', difficulty: 1 },
      { type: '填空题', content: '一件商品打八折出售，表示现价是原价的（  ）%。', answer: '80', difficulty: 1 },
      { type: '填空题', content: '出勤率 =（  ）÷（  ）× 100%', answer: '出勤人数；总人数', difficulty: 1 },
      { type: '计算题', content: '把3/8化成百分数。', answer: '37.5%', difficulty: 2 },
      { type: '计算题', content: '把75%化成分数。', answer: '3/4', difficulty: 1 },
      { type: '计算题', content: '250的40%是多少？', answer: '100', difficulty: 1 },
      { type: '计算题', content: '一个数的25%是60，这个数是多少？', answer: '240', difficulty: 2 },
      { type: '选择题', content: '某班有50人，今天有2人请假，今天的出勤率是（  ）。\nA. 96%  B. 4%  C. 98%', answer: 'A', difficulty: 2 },
      { type: '判断题', content: '百分数的分子一定小于100。（  ）', answer: '×', difficulty: 1 },
      { type: '应用题', content: '一件衣服原价300元，现在打七五折出售，现在售价多少元？', answer: '300×75%=225（元）', difficulty: 2 },
      { type: '应用题', content: '小明存入银行5000元，年利率是2.5%，存2年，到期后利息是多少元？', answer: '5000×2.5%×2=250（元）', difficulty: 3 },
    ],
  },
  {
    id: 'g6x-u3',
    unitName: '圆柱与圆锥',
    grade: 6,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '圆柱的侧面积 =（  ）×（  ）', answer: '底面周长；高', difficulty: 1 },
      { type: '填空题', content: '圆柱的体积 =（  ）', answer: '底面积×高', difficulty: 1 },
      { type: '填空题', content: '圆锥的体积 =（  ）', answer: '1/3×底面积×高', difficulty: 1 },
      { type: '填空题', content: '一个圆柱和一个圆锥等底等高，圆柱的体积是圆锥体积的（  ）倍。', answer: '3', difficulty: 1 },
      { type: '计算题', content: '一个圆柱，底面半径是3厘米，高是10厘米，体积是多少？（π取3.14）', answer: '3.14×3²×10=282.6（立方厘米）', difficulty: 2 },
      { type: '计算题', content: '一个圆锥，底面直径是6米，高是4米，体积是多少？（π取3.14）', answer: '1/3×3.14×(6÷2)²×4=37.68（立方米）', difficulty: 2 },
      { type: '计算题', content: '一个圆柱的底面周长是12.56厘米，高是5厘米，侧面积是多少？', answer: '12.56×5=62.8（平方厘米）', difficulty: 1 },
      { type: '计算题', content: '一个圆柱的底面半径是2分米，高是8分米，表面积是多少？（π取3.14）', answer: '2×3.14×2×8+3.14×2²=125.6（平方分米）', difficulty: 3 },
      { type: '选择题', content: '把一个圆柱的侧面展开，得到一个（  ）。\nA. 长方形  B. 正方形  C. 长方形或正方形', answer: 'C', difficulty: 2 },
      { type: '判断题', content: '圆锥的体积是圆柱体积的1/3。（  ）', answer: '×', difficulty: 2 },
      { type: '应用题', content: '一个圆柱形水桶，底面半径是20厘米，高是50厘米，这个水桶的容积是多少升？（π取3.14）', answer: '3.14×20²×50=62800（立方厘米）=62.8（升）', difficulty: 2 },
      { type: '应用题', content: '一个圆锥形沙堆，底面直径是4米，高是1.5米，这堆沙的体积是多少立方米？（π取3.14）', answer: '1/3×3.14×(4÷2)²×1.5=6.28（立方米）', difficulty: 2 },
    ],
  },
  {
    id: 'g6x-u4',
    unitName: '比例',
    grade: 6,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '表示两个比相等的式子叫做（  ）。', answer: '比例', difficulty: 1 },
      { type: '填空题', content: '在比例中，两个外项的积（  ）两个内项的积。', answer: '等于', difficulty: 1 },
      { type: '填空题', content: '如果 a × 3 = b × 5，那么 a:b =（  ）：（  ）。', answer: '5；3', difficulty: 2 },
      { type: '填空题', content: '图上距离和实际距离的比，叫做这幅图的（  ）。', answer: '比例尺', difficulty: 1 },
      { type: '填空题', content: '一幅地图的比例尺是1:5000000，图上1厘米表示实际距离（  ）千米。', answer: '50', difficulty: 2 },
      { type: '计算题', content: '解比例：\n2:5 = x:15', answer: 'x = 6', difficulty: 1 },
      { type: '计算题', content: '解比例：\n3/x = 9/12', answer: 'x = 4', difficulty: 2 },
      { type: '计算题', content: '解比例：\nx/4 = 7/8', answer: 'x = 3.5', difficulty: 2 },
      { type: '判断题', content: '两个比可以组成一个比例。（  ）', answer: '×', difficulty: 2 },
      { type: '判断题', content: '如果3a=5b，那么a:b=5:3。（  ）', answer: '√', difficulty: 2 },
      { type: '应用题', content: '在一幅比例尺是1:2000000的地图上，量得甲乙两地的距离是5厘米，甲乙两地的实际距离是多少千米？', answer: '5×2000000=10000000（厘米）=100（千米）', difficulty: 2 },
      { type: '应用题', content: '一辆汽车3小时行驶了180千米，照这样的速度，5小时行驶多少千米？（用比例解）', answer: '180/3=x/5，x=300（千米）', difficulty: 3 },
    ],
  },

  // ==================== 补充数学单元 ====================

  // 一年级上册补充：认识图形（一）
  {
    id: 'g1s-u6',
    unitName: '认识图形（一）',
    grade: 1,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '长方体有（  ）个面。', answer: '6', difficulty: 1 },
      { type: '填空题', content: '正方体有（  ）个面，每个面都是（  ）形。', answer: '6；正方', difficulty: 1 },
      { type: '填空题', content: '圆柱有（  ）个圆形的面。', answer: '2', difficulty: 1 },
      { type: '选择题', content: '下面哪个物体的形状是球？\nA. 魔方  B. 足球  C. 铅笔盒', answer: 'B', difficulty: 1 },
      { type: '选择题', content: '冰箱的形状是（  ）。\nA. 球  B. 圆柱  C. 长方体', answer: 'C', difficulty: 1 },
      { type: '判断题', content: '球的表面是平平的。（  ）', answer: '×', difficulty: 1 },
      { type: '判断题', content: '正方体的每个面都一样大。（  ）', answer: '√', difficulty: 1 },
      { type: '填空题', content: '硬币的形状是（  ）体。', answer: '圆柱', difficulty: 1 },
      { type: '选择题', content: '能滚动又能堆叠的物体是（  ）。\nA. 球  B. 长方体  C. 圆柱', answer: 'C', difficulty: 2 },
      { type: '判断题', content: '长方体和正方体都有6个面。（  ）', answer: '√', difficulty: 1 },
    ],
  },
  // 一年级上册补充：总复习
  {
    id: 'g1s-u7',
    unitName: '总复习',
    grade: 1,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '计算题', content: '8 + 5 =', answer: '13', difficulty: 1 },
      { type: '计算题', content: '17 - 9 =', answer: '8', difficulty: 1 },
      { type: '填空题', content: '1个十和5个一合起来是（  ）。', answer: '15', difficulty: 1 },
      { type: '填空题', content: '18里面有（  ）个十和（  ）个一。', answer: '1；8', difficulty: 1 },
      { type: '比较大小', content: '在○里填上">"、"<"或"="。\n9 + 5 ○ 15', answer: '<', difficulty: 2 },
      { type: '比较大小', content: '在○里填上">"、"<"或"="。\n16 - 8 ○ 7', answer: '>', difficulty: 2 },
      { type: '应用题', content: '小明有10支铅笔，送给小红3支，还剩几支？', answer: '10-3=7（支）', difficulty: 2 },
      { type: '应用题', content: '草地上有6只白兔，7只黑兔，一共有几只兔子？', answer: '6+7=13（只）', difficulty: 2 },
      { type: '填空题', content: '钟面上有（  ）个数，时针走一大格是（  ）小时。', answer: '12；1', difficulty: 2 },
      { type: '判断题', content: '正方体有6个面，每个面都是正方形。（  ）', answer: '√', difficulty: 1 },
    ],
  },
  // 一年级下册补充：认识人民币
  {
    id: 'g1x-u4',
    unitName: '认识人民币',
    grade: 1,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '1元 =（  ）角', answer: '10', difficulty: 1 },
      { type: '填空题', content: '1角 =（  ）分', answer: '10', difficulty: 1 },
      { type: '填空题', content: '1元 =（  ）分', answer: '100', difficulty: 2 },
      { type: '计算题', content: '5角 + 3角 =（  ）角', answer: '8', difficulty: 1 },
      { type: '计算题', content: '1元2角 - 5角 =（  ）元（  ）角', answer: '0；7', difficulty: 2 },
      { type: '选择题', content: '一支铅笔5角，小明付了1元，应找回（  ）。\nA. 5角  B. 4角  C. 6角', answer: 'A', difficulty: 1 },
      { type: '选择题', content: '一本练习本2元3角，付了5元，应找回（  ）。\nA. 2元7角  B. 3元7角  C. 2元3角', answer: 'A', difficulty: 2 },
      { type: '判断题', content: '1张5元可以换5张1元。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '1角可以换10个1分。（  ）', answer: '√', difficulty: 1 },
      { type: '应用题', content: '小明买一个书包花了15元，付了20元，应找回多少元？', answer: '20-15=5（元）', difficulty: 2 },
    ],
  },
  // 一年级下册补充：100以内的加法和减法（一）
  {
    id: 'g1x-u5',
    unitName: '100以内的加法和减法（一）',
    grade: 1,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '计算题', content: '35 + 4 =', answer: '39', difficulty: 1 },
      { type: '计算题', content: '56 - 3 =', answer: '53', difficulty: 1 },
      { type: '计算题', content: '28 + 30 =', answer: '58', difficulty: 1 },
      { type: '计算题', content: '75 - 20 =', answer: '55', difficulty: 1 },
      { type: '计算题', content: '36 + 42 =', answer: '78', difficulty: 1 },
      { type: '计算题', content: '80 - 45 =', answer: '35', difficulty: 2 },
      { type: '计算题', content: '47 + 38 =', answer: '85', difficulty: 2 },
      { type: '计算题', content: '63 - 27 =', answer: '36', difficulty: 2 },
      { type: '应用题', content: '一年级有男生25人，女生23人，一共有多少人？', answer: '25+23=48（人）', difficulty: 2 },
      { type: '应用题', content: '书架上有60本书，借走了28本，还剩多少本？', answer: '60-28=32（本）', difficulty: 2 },
    ],
  },
  // 二年级上册补充：表内乘法（一）
  {
    id: 'g2s-u4',
    unitName: '表内乘法（一）',
    grade: 2,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '计算题', content: '3 × 4 =', answer: '12', difficulty: 1 },
      { type: '计算题', content: '5 × 6 =', answer: '30', difficulty: 1 },
      { type: '计算题', content: '2 × 8 =', answer: '16', difficulty: 1 },
      { type: '计算题', content: '4 × 7 =', answer: '28', difficulty: 1 },
      { type: '计算题', content: '6 × 6 =', answer: '36', difficulty: 1 },
      { type: '填空题', content: '5 + 5 + 5 =（  ）×（  ）', answer: '5；3', difficulty: 2 },
      { type: '填空题', content: '4 × 3 表示（  ）个（  ）相加。', answer: '3；4', difficulty: 2 },
      { type: '选择题', content: '6个3相加，用乘法算式表示是（  ）。\nA. 6 + 3  B. 6 × 3  C. 3 + 6', answer: 'B', difficulty: 1 },
      { type: '应用题', content: '每个小朋友有5支铅笔，4个小朋友一共有多少支铅笔？', answer: '5×4=20（支）', difficulty: 2 },
      { type: '应用题', content: '一棵树上有3只小鸟，6棵树上一共有多少只小鸟？', answer: '3×6=18（只）', difficulty: 2 },
    ],
  },
  // 二年级上册补充：表内乘法（二）
  {
    id: 'g2s-u5',
    unitName: '表内乘法（二）',
    grade: 2,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '计算题', content: '7 × 8 =', answer: '56', difficulty: 1 },
      { type: '计算题', content: '9 × 6 =', answer: '54', difficulty: 1 },
      { type: '计算题', content: '8 × 9 =', answer: '72', difficulty: 1 },
      { type: '计算题', content: '7 × 7 =', answer: '49', difficulty: 1 },
      { type: '计算题', content: '9 × 9 =', answer: '81', difficulty: 1 },
      { type: '填空题', content: '8 ×（  ）= 56', answer: '7', difficulty: 2 },
      { type: '填空题', content: '（  ）× 6 = 42', answer: '7', difficulty: 2 },
      { type: '比较大小', content: '在○里填上">"、"<"或"="。\n7 × 8 ○ 6 × 9', answer: '>', difficulty: 2 },
      { type: '应用题', content: '每排有8把椅子，9排一共有多少把椅子？', answer: '8×9=72（把）', difficulty: 2 },
      { type: '应用题', content: '小明每天看7页书，看了8天，一共看了多少页？', answer: '7×8=56（页）', difficulty: 2 },
    ],
  },
  // 二年级上册补充：观察物体（一）
  {
    id: 'g2s-u6',
    unitName: '观察物体（一）',
    grade: 2,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '判断题', content: '从不同方向看同一个物体，看到的形状可能不同。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '从正面看一个正方体，看到的是一个正方形。（  ）', answer: '√', difficulty: 1 },
      { type: '选择题', content: '一个长方体从正面看是（  ）。\nA. 正方形  B. 长方形  C. 三角形', answer: 'B', difficulty: 1 },
      { type: '选择题', content: '一个圆柱从上面看是（  ）。\nA. 长方形  B. 正方形  C. 圆', answer: 'C', difficulty: 1 },
      { type: '判断题', content: '一个球从任何方向看都是圆形。（  ）', answer: '√', difficulty: 1 },
      { type: '选择题', content: '从左面看一个玩具熊，看到的是（  ）。\nA. 正面  B. 侧面  C. 上面', answer: 'B', difficulty: 1 },
      { type: '判断题', content: '一个物体最多能同时看到4个面。（  ）', answer: '×', difficulty: 2 },
      { type: '填空题', content: '观察一个物体，我们通常从（  ）、（  ）、（  ）三个方向来观察。', answer: '正面；侧面；上面', difficulty: 2 },
      { type: '判断题', content: '从上面看一个正方体，看到的是正方形。（  ）', answer: '√', difficulty: 1 },
      { type: '选择题', content: '一个茶杯从侧面看是（  ）。\nA. 长方形  B. 圆形  C. 三角形', answer: 'A', difficulty: 2 },
    ],
  },
  // 二年级下册补充：图形的运动（一）
  {
    id: 'g2x-u4',
    unitName: '图形的运动（一）',
    grade: 2,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '判断题', content: '荡秋千是平移现象。（  ）', answer: '×', difficulty: 1 },
      { type: '判断题', content: '推拉窗是平移现象。（  ）', answer: '√', difficulty: 1 },
      { type: '选择题', content: '下面哪个是轴对称图形？\nA. 平行四边形  B. 正方形  C. 梯形', answer: 'B', difficulty: 1 },
      { type: '选择题', content: '下面哪个是旋转现象？\nA. 滑滑梯  B. 陀螺转动  C. 电梯上下', answer: 'B', difficulty: 1 },
      { type: '判断题', content: '国旗的升降是平移现象。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '所有的三角形都是轴对称图形。（  ）', answer: '×', difficulty: 2 },
      { type: '填空题', content: '对折后两边能完全重合的图形叫做（  ）图形。', answer: '轴对称', difficulty: 1 },
      { type: '选择题', content: '字母"A"是（  ）图形。\nA. 轴对称  B. 不是轴对称', answer: 'A', difficulty: 1 },
      { type: '判断题', content: '钟表指针的运动是旋转现象。（  ）', answer: '√', difficulty: 1 },
      { type: '填空题', content: '物体沿着一条直线移动的现象叫做（  ）。', answer: '平移', difficulty: 1 },
    ],
  },
  // 二年级下册补充：万以内数的认识
  {
    id: 'g2x-u5',
    unitName: '万以内数的认识',
    grade: 2,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '10个一百是（  ），10个一千是（  ）。', answer: '一千；一万', difficulty: 1 },
      { type: '填空题', content: '3个千、5个百和2个一组成的数是（  ）。', answer: '3502', difficulty: 1 },
      { type: '填空题', content: '4856是由（  ）个千、（  ）个百、（  ）个十和（  ）个一组成的。', answer: '4；8；5；6', difficulty: 1 },
      { type: '计算题', content: '2000 + 500 + 30 =', answer: '2530', difficulty: 1 },
      { type: '计算题', content: '4560 - 500 =', answer: '4060', difficulty: 1 },
      { type: '比较大小', content: '在○里填上">"、"<"或"="。\n3025 ○ 3205', answer: '<', difficulty: 2 },
      { type: '比较大小', content: '在○里填上">"、"<"或"="。\n5600 ○ 5060', answer: '>', difficulty: 2 },
      { type: '填空题', content: '与999相邻的两个数是（  ）和（  ）。', answer: '998；1000', difficulty: 2 },
      { type: '选择题', content: '下面各数中，一个零也不读的是（  ）。\nA. 3005  B. 3050  C. 3500', answer: 'C', difficulty: 2 },
      { type: '应用题', content: '图书馆有故事书2000本，科技书比故事书少500本，科技书有多少本？', answer: '2000-500=1500（本）', difficulty: 2 },
    ],
  },
  // 三年级上册补充：多位数乘一位数
  {
    id: 'g3s-u4',
    unitName: '多位数乘一位数',
    grade: 3,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '计算题', content: '23 × 3 =', answer: '69', difficulty: 1 },
      { type: '计算题', content: '45 × 2 =', answer: '90', difficulty: 1 },
      { type: '计算题', content: '124 × 2 =', answer: '248', difficulty: 1 },
      { type: '计算题', content: '315 × 3 =', answer: '945', difficulty: 2 },
      { type: '计算题', content: '207 × 4 =', answer: '828', difficulty: 2 },
      { type: '计算题', content: '450 × 6 =', answer: '2700', difficulty: 2 },
      { type: '计算题', content: '180 × 5 =', answer: '900', difficulty: 1 },
      { type: '应用题', content: '学校买了12箱粉笔，每箱24盒，一共有多少盒？', answer: '12×24=288（盒）', difficulty: 2 },
      { type: '应用题', content: '一本故事书有125页，小明看了3天，每天看多少页才能看完？', answer: '125×3=375（页），每天看125页', difficulty: 2 },
      { type: '估算题', content: '估算：498 × 3 ≈（  ）', answer: '1500', difficulty: 2 },
    ],
  },
  // 三年级上册补充：长方形和正方形
  {
    id: 'g3s-u5',
    unitName: '长方形和正方形',
    grade: 3,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '长方形的周长 =（  ）。', answer: '（长+宽）× 2', difficulty: 1 },
      { type: '填空题', content: '正方形的周长 =（  ）。', answer: '边长 × 4', difficulty: 1 },
      { type: '计算题', content: '一个长方形长8厘米，宽5厘米，周长是多少厘米？', answer: '（8+5）×2=26（厘米）', difficulty: 1 },
      { type: '计算题', content: '一个正方形边长是6分米，周长是多少分米？', answer: '6×4=24（分米）', difficulty: 1 },
      { type: '选择题', content: '一个长方形长10米，宽6米，它的周长是（  ）米。\nA. 16  B. 60  C. 32', answer: 'C', difficulty: 1 },
      { type: '判断题', content: '四个角都是直角的四边形一定是长方形或正方形。（  ）', answer: '√', difficulty: 2 },
      { type: '判断题', content: '正方形是特殊的长方形。（  ）', answer: '√', difficulty: 2 },
      { type: '应用题', content: '一块正方形桌布，边长是9分米，在它四周缝上花边，花边长多少分米？', answer: '9×4=36（分米）', difficulty: 2 },
      { type: '应用题', content: '一个长方形操场，长120米，宽80米，小明沿操场跑一圈，跑了多少米？', answer: '（120+80）×2=400（米）', difficulty: 2 },
      { type: '填空题', content: '长方形有（  ）条边，（  ）个角，都是（  ）角。', answer: '4；4；直', difficulty: 1 },
    ],
  },
  // 三年级下册补充：复式统计表
  {
    id: 'g3x-u4',
    unitName: '复式统计表',
    grade: 3,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '复式统计表可以同时表示（  ）组或（  ）组以上的数据。', answer: '两；两', difficulty: 1 },
      { type: '应用题', content: '下面是某班男生和女生最喜欢课外活动统计：\n男生：体育12人、阅读5人、游戏8人\n女生：体育4人、阅读10人、游戏6人\n（1）男生最喜欢（  ）的人数最多。\n（2）女生最喜欢（  ）的人数最多。', answer: '（1）体育；（2）阅读', difficulty: 2 },
      { type: '选择题', content: '复式统计表和单式统计表相比，最大的优点是（  ）。\nA. 更好看  B. 便于比较  C. 更简单', answer: 'B', difficulty: 1 },
      { type: '判断题', content: '复式统计表必须有表头。（  ）', answer: '√', difficulty: 1 },
      { type: '应用题', content: '三年级一班和二班参加课外小组人数如下：\n一班：书法8人、绘画12人、唱歌6人\n二班：书法10人、绘画8人、唱歌10人\n（1）两个班参加（  ）小组的总人数最多。\n（2）一班参加书法和绘画的一共有多少人？', answer: '（1）绘画；（2）8+12=20（人）', difficulty: 2 },
      { type: '填空题', content: '看统计表时，首先要看懂（  ）。', answer: '表头', difficulty: 1 },
      { type: '判断题', content: '统计表中的数据可以随意修改。（  ）', answer: '×', difficulty: 1 },
      { type: '应用题', content: '某商店一周销售苹果和橘子数量如下（千克）：\n周一：苹果30、橘子20\n周二：苹果25、橘子30\n周三：苹果35、橘子25\n（1）哪天卖出的水果总量最多？\n（2）三天一共卖出苹果多少千克？', answer: '（1）周三（60千克）；（2）30+25+35=90（千克）', difficulty: 3 },
      { type: '选择题', content: '要比较两个班级各科成绩，最好使用（  ）。\nA. 单式统计表  B. 复式统计表  C. 文字记录', answer: 'B', difficulty: 1 },
      { type: '填空题', content: '复式统计表的表头一般分为（  ）栏。', answer: '3', difficulty: 2 },
    ],
  },
  // 三年级下册补充：两位数乘两位数
  {
    id: 'g3x-u5',
    unitName: '两位数乘两位数',
    grade: 3,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '计算题', content: '12 × 13 =', answer: '156', difficulty: 1 },
      { type: '计算题', content: '23 × 14 =', answer: '322', difficulty: 1 },
      { type: '计算题', content: '45 × 22 =', answer: '990', difficulty: 2 },
      { type: '计算题', content: '36 × 25 =', answer: '900', difficulty: 2 },
      { type: '计算题', content: '54 × 16 =', answer: '864', difficulty: 2 },
      { type: '估算题', content: '估算：31 × 48 ≈（  ）', answer: '1500', difficulty: 2 },
      { type: '估算题', content: '估算：39 × 52 ≈（  ）', answer: '2000', difficulty: 2 },
      { type: '选择题', content: '25 × 40 的末尾有（  ）个0。\nA. 1  B. 2  C. 3', answer: 'B', difficulty: 2 },
      { type: '应用题', content: '学校有24个班，每班45人，学校一共有多少人？', answer: '24×45=1080（人）', difficulty: 2 },
      { type: '应用题', content: '每箱牛奶有12瓶，买了35箱，一共有多少瓶？', answer: '12×35=420（瓶）', difficulty: 2 },
    ],
  },
  // 四年级上册补充：除数是两位数的除法
  {
    id: 'g4s-u6',
    unitName: '除数是两位数的除法',
    grade: 4,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '计算题', content: '84 ÷ 12 =', answer: '7', difficulty: 1 },
      { type: '计算题', content: '96 ÷ 16 =', answer: '6', difficulty: 1 },
      { type: '计算题', content: '144 ÷ 24 =', answer: '6', difficulty: 1 },
      { type: '计算题', content: '375 ÷ 15 =', answer: '25', difficulty: 2 },
      { type: '计算题', content: '672 ÷ 21 =', answer: '32', difficulty: 2 },
      { type: '计算题', content: '840 ÷ 28 =', answer: '30', difficulty: 2 },
      { type: '填空题', content: '（  ）÷ 35 = 8', answer: '280', difficulty: 2 },
      { type: '选择题', content: '试商时，如果余数比除数大，应该把商（  ）。\nA. 调大  B. 调小  C. 不变', answer: 'A', difficulty: 2 },
      { type: '应用题', content: '学校有840本图书，分给28个班，每个班分多少本？', answer: '840÷28=30（本）', difficulty: 2 },
      { type: '应用题', content: '服装厂生产了960件衣服，每24件装一箱，可以装多少箱？', answer: '960÷24=40（箱）', difficulty: 2 },
    ],
  },
  // 四年级上册补充：条形统计图
  {
    id: 'g4s-u7',
    unitName: '条形统计图',
    grade: 4,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '条形统计图用（  ）的长短来表示数量的多少。', answer: '直条', difficulty: 1 },
      { type: '选择题', content: '条形统计图的优点是（  ）。\nA. 能清楚看出各数量的多少  B. 能看出变化趋势  C. 能看出部分与整体的关系', answer: 'A', difficulty: 1 },
      { type: '判断题', content: '条形统计图的每格代表的数量可以不同。（  ）', answer: '×', difficulty: 1 },
      { type: '判断题', content: '条形统计图的标题要写在图的上方。（  ）', answer: '√', difficulty: 1 },
      { type: '应用题', content: '下面是某班同学最喜欢的运动统计（人数）：\n跑步15人、跳绳20人、踢球12人、游泳8人\n（1）喜欢（  ）的人最多。\n（2）喜欢跑步的比喜欢踢球的多（  ）人。', answer: '（1）跳绳；（2）3', difficulty: 2 },
      { type: '填空题', content: '在条形统计图中，如果1格代表5人，那么3格代表（  ）人。', answer: '15', difficulty: 1 },
      { type: '选择题', content: '要表示各年级人数的多少，最适合用（  ）。\nA. 条形统计图  B. 折线统计图  C. 扇形统计图', answer: 'A', difficulty: 1 },
      { type: '应用题', content: '某地四个月降水量统计如下：\n一月20mm、二月25mm、三月35mm、四月50mm\n（1）（  ）月降水量最多。\n（2）四个月总降水量是多少？', answer: '（1）四；（2）20+25+35+50=130（mm）', difficulty: 2 },
      { type: '判断题', content: '条形统计图可以横向画，也可以纵向画。（  ）', answer: '√', difficulty: 1 },
      { type: '填空题', content: '绘制条形统计图时，直条的宽度要（  ），间隔要（  ）。', answer: '相同；相等', difficulty: 2 },
    ],
  },
  // 四年级下册补充：平均数与条形统计图
  {
    id: 'g4x-u6',
    unitName: '平均数与条形统计图',
    grade: 4,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '平均数 = 总数 ÷（  ）。', answer: '份数', difficulty: 1 },
      { type: '计算题', content: '小明5次数学测验的成绩分别是：85、90、78、92、95，他的平均成绩是多少？', answer: '(85+90+78+92+95)÷5=88', difficulty: 2 },
      { type: '计算题', content: '四个同学的身高分别是135cm、140cm、138cm、143cm，他们的平均身高是多少？', answer: '(135+140+138+143)÷4=139（cm）', difficulty: 2 },
      { type: '选择题', content: '三个数的平均数是15，这三个数的和是（  ）。\nA. 15  B. 30  C. 45', answer: 'C', difficulty: 1 },
      { type: '判断题', content: '平均数一定等于这组数据中的某一个数。（  ）', answer: '×', difficulty: 2 },
      { type: '判断题', content: '平均数能较好地反映一组数据的总体情况。（  ）', answer: '√', difficulty: 1 },
      { type: '应用题', content: '甲组有4人，共植树20棵；乙组有6人，共植树30棵。平均每人植树多少棵？', answer: '(20+30)÷(4+6)=5（棵）', difficulty: 2 },
      { type: '应用题', content: '小明看一本书，前3天每天看12页，后2天共看了30页，平均每天看多少页？', answer: '(12×3+30)÷5=13.2（页）', difficulty: 3 },
      { type: '填空题', content: '一组数据是3、5、7、9、11，这组数据的平均数是（  ）。', answer: '7', difficulty: 2 },
      { type: '选择题', content: '小明身高145cm，他在平均水深120cm的游泳池里游泳，（  ）。\nA. 一定安全  B. 不一定安全  C. 一定不安全', answer: 'B', difficulty: 3 },
    ],
  },
  // 五年级上册补充：植树问题
  {
    id: 'g5s-u5',
    unitName: '植树问题',
    grade: 5,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '在一条长100米的路一边植树，每隔5米种一棵，两端都种，一共需要（  ）棵树。', answer: '21', difficulty: 2 },
      { type: '填空题', content: '在一条长100米的路一边植树，每隔5米种一棵，两端都不种，一共需要（  ）棵树。', answer: '19', difficulty: 2 },
      { type: '填空题', content: '在一条长100米的路一边植树，每隔5米种一棵，只种一端，一共需要（  ）棵树。', answer: '20', difficulty: 2 },
      { type: '应用题', content: '一条长120米的小路一边植树，每隔6米种一棵，两端都种，一共需要多少棵树？', answer: '120÷6+1=21（棵）', difficulty: 2 },
      { type: '应用题', content: '在一条200米的路两旁种树，每隔8米种一棵，两端都种，一共需要多少棵树？', answer: '(200÷8+1)×2=52（棵）', difficulty: 3 },
      { type: '选择题', content: '锯一根木头，每锯一次需要3分钟，锯成5段需要（  ）分钟。\nA. 15  B. 12  C. 10', answer: 'B', difficulty: 2 },
      { type: '应用题', content: '圆形花坛周长60米，每隔3米种一棵树，一共需要多少棵树？', answer: '60÷3=20（棵）', difficulty: 2 },
      { type: '判断题', content: '在封闭图形上植树，棵数 = 间隔数。（  ）', answer: '√', difficulty: 1 },
      { type: '应用题', content: '5路公共汽车行驶路线全长12千米，相邻两站之间的距离是1千米，一共有几个车站？', answer: '12÷1+1=13（个）', difficulty: 2 },
      { type: '选择题', content: '一根木棒锯成3段需要6分钟，锯成6段需要（  ）分钟。\nA. 12  B. 15  C. 18', answer: 'B', difficulty: 3 },
    ],
  },
  // 五年级下册补充：图形的运动（三）
  {
    id: 'g5x-u6',
    unitName: '图形的运动（三）',
    grade: 5,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '图形旋转的三个要素是（  ）、（  ）和（  ）。', answer: '旋转中心；旋转方向；旋转角度', difficulty: 1 },
      { type: '判断题', content: '图形旋转后，形状和大小都不改变。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '顺时针旋转90度和逆时针旋转90度，得到的图形一样。（  ）', answer: '×', difficulty: 2 },
      { type: '选择题', content: '一个图形绕某点顺时针旋转90度后，图形的（  ）不变。\nA. 位置  B. 大小和形状  C. 方向', answer: 'B', difficulty: 1 },
      { type: '判断题', content: '旋转后的图形与原图形关于旋转中心对称。（  ）', answer: '×', difficulty: 2 },
      { type: '填空题', content: '指针从"12"顺时针旋转90度指向"（  ）"。', answer: '3', difficulty: 1 },
      { type: '填空题', content: '指针从"3"逆时针旋转90度指向"（  ）"。', answer: '12', difficulty: 1 },
      { type: '选择题', content: '将一个三角形绕一个顶点旋转180度后，与原图形（  ）。\nA. 完全相同  B. 面积相同  C. 形状不同', answer: 'B', difficulty: 2 },
      { type: '判断题', content: '平移和旋转都不改变图形的形状和大小。（  ）', answer: '√', difficulty: 1 },
      { type: '应用题', content: '画一个直角三角形，将它绕直角顶点顺时针旋转90度，画出旋转后的图形。旋转后斜边的方向发生了怎样的变化？', answer: '斜边方向旋转了90度', difficulty: 3 },
    ],
  },
  // 五年级下册补充：分数与除法
  {
    id: 'g5x-u7',
    unitName: '分数与除法',
    grade: 5,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '被除数 ÷ 除数 =（  ）/（  ）', answer: '被除数；除数', difficulty: 1 },
      { type: '填空题', content: '3 ÷ 5 =（  ）/（  ）', answer: '3；5', difficulty: 1 },
      { type: '填空题', content: '7 ÷ 12 =（  ）/（  ）', answer: '7；12', difficulty: 1 },
      { type: '填空题', content: '（  ）÷（  ）= 3/4', answer: '3；4', difficulty: 1 },
      { type: '选择题', content: '把5米长的绳子平均分成8段，每段长（  ）米。\nA. 5/8  B. 8/5  C. 1/8', answer: 'A', difficulty: 1 },
      { type: '判断题', content: '分数的分子相当于除法中的被除数。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '1 ÷ 3 和 1/3 表示的意义相同。（  ）', answer: '√', difficulty: 1 },
      { type: '应用题', content: '把3块饼平均分给4个小朋友，每个小朋友分到多少块？', answer: '3÷4=3/4（块）', difficulty: 2 },
      { type: '应用题', content: '把5千克糖平均分成6袋，每袋重多少千克？', answer: '5÷6=5/6（千克）', difficulty: 2 },
      { type: '选择题', content: 'a ÷ b = a/b，其中 b 不能为（  ）。\nA. 0  B. 1  C. 任意数', answer: 'A', difficulty: 1 },
    ],
  },
  // 六年级上册补充：百分数（一）
  {
    id: 'g6s-u6',
    unitName: '百分数（一）',
    grade: 6,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '45%读作（  ），百分之三十五写作（  ）。', answer: '百分之四十五；35%', difficulty: 1 },
      { type: '填空题', content: '3/5 =（  ）% =（  ）÷（  ）', answer: '60；3；5', difficulty: 2 },
      { type: '填空题', content: '1/4 =（  ）%', answer: '25', difficulty: 1 },
      { type: '填空题', content: '80% =（  ）/（  ）', answer: '4；5', difficulty: 1 },
      { type: '计算题', content: '250 × 40% =', answer: '100', difficulty: 1 },
      { type: '计算题', content: '60 ÷ 25% =', answer: '240', difficulty: 2 },
      { type: '选择题', content: '一件商品打八折出售，表示现价是原价的（  ）。\nA. 80%  B. 20%  C. 8%', answer: 'A', difficulty: 1 },
      { type: '应用题', content: '六年级有学生200人，今天出勤196人，出勤率是多少？', answer: '196÷200×100%=98%', difficulty: 2 },
      { type: '应用题', content: '一种商品原价500元，现价400元，降价了百分之几？', answer: '(500-400)÷500×100%=20%', difficulty: 2 },
      { type: '判断题', content: '百分数的分子可以是小数。（  ）', answer: '√', difficulty: 2 },
    ],
  },
  // 六年级上册补充：扇形统计图
  {
    id: 'g6s-u7',
    unitName: '扇形统计图',
    grade: 6,
    semester: '上',
    subject: '数学',
    questions: [
      { type: '填空题', content: '扇形统计图是用整个圆表示（  ），用圆内大小不同的扇形表示各部分占总数的（  ）。', answer: '总数；百分比', difficulty: 1 },
      { type: '选择题', content: '要表示各部分占总数的百分比，最适合用（  ）。\nA. 条形统计图  B. 折线统计图  C. 扇形统计图', answer: 'C', difficulty: 1 },
      { type: '判断题', content: '扇形统计图中各扇形所占的百分比之和是100%。（  ）', answer: '√', difficulty: 1 },
      { type: '应用题', content: '六年级学生最喜欢的课外活动统计如下：\n体育40%、阅读25%、音乐20%、其他15%\n如果六年级有200人，喜欢体育的有多少人？', answer: '200×40%=80（人）', difficulty: 2 },
      { type: '应用题', content: '某校学生人数统计：低年级占30%，中年级占40%，高年级占30%。\n已知低年级有300人，全校一共有多少人？', answer: '300÷30%=1000（人）', difficulty: 2 },
      { type: '选择题', content: '在扇形统计图中，扇形的面积越大，说明该部分占总数的百分比越（  ）。\nA. 大  B. 小  C. 不确定', answer: 'A', difficulty: 1 },
      { type: '判断题', content: '扇形统计图能清楚地看出各部分数量的多少。（  ）', answer: '×', difficulty: 2 },
      { type: '应用题', content: '果园里苹果树占总数的35%，梨树占25%，其余是桃树。\n（1）桃树占总数的百分之几？\n（2）如果果园共有400棵树，桃树有多少棵？', answer: '（1）100%-35%-25%=40%；（2）400×40%=160（棵）', difficulty: 3 },
      { type: '填空题', content: '扇形统计图中，一个扇形的圆心角是90度，这个扇形占总数的（  ）%。', answer: '25', difficulty: 2 },
      { type: '判断题', content: '扇形统计图不能直接看出各部分的具体数量。（  ）', answer: '√', difficulty: 2 },
    ],
  },
  // 六年级下册补充：比例尺
  {
    id: 'g6x-u5',
    unitName: '比例尺',
    grade: 6,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '填空题', content: '比例尺 =（  ）距离 : （  ）距离。', answer: '图上；实际', difficulty: 1 },
      { type: '填空题', content: '一幅地图的比例尺是1:2000000，图上1厘米表示实际距离（  ）千米。', answer: '20', difficulty: 2 },
      { type: '填空题', content: '实际距离是100千米，画在比例尺是1:5000000的地图上，应画（  ）厘米。', answer: '2', difficulty: 2 },
      { type: '计算题', content: '在比例尺是1:3000000的地图上，量得甲乙两地的距离是8厘米，甲乙两地的实际距离是多少千米？', answer: '8×3000000=24000000（厘米）=240（千米）', difficulty: 2 },
      { type: '计算题', content: '甲乙两地相距60千米，画在比例尺是1:200000的地图上，应画多少厘米？', answer: '6000000÷200000=30（厘米）', difficulty: 2 },
      { type: '选择题', content: '比例尺1:5000000表示（  ）。\nA. 图上1厘米等于实际50千米  B. 图上1厘米等于实际500千米  C. 图上1厘米等于实际5千米', answer: 'A', difficulty: 1 },
      { type: '判断题', content: '比例尺是一个比，没有单位。（  ）', answer: '√', difficulty: 1 },
      { type: '判断题', content: '线段比例尺和数值比例尺可以互相转换。（  ）', answer: '√', difficulty: 1 },
      { type: '应用题', content: '一个长方形操场长120米，宽80米，把它画在比例尺是1:4000的图纸上，长和宽各应画多少厘米？', answer: '长：12000÷4000=3（厘米）；宽：8000÷4000=2（厘米）', difficulty: 3 },
      { type: '应用题', content: '在一幅比例尺是1:500000的地图上，量得一长方形地的长是4厘米，宽是2厘米，这块地的实际面积是多少平方千米？', answer: '长：4×500000=2000000（厘米）=20（千米）；宽：2×500000=1000000（厘米）=10（千米）；面积：20×10=200（平方千米）', difficulty: 3 },
    ],
  },
  // 六年级下册补充：整理和复习
  {
    id: 'g6x-u6',
    unitName: '整理和复习',
    grade: 6,
    semester: '下',
    subject: '数学',
    questions: [
      { type: '计算题', content: '3/4 × 2/5 =', answer: '3/10', difficulty: 1 },
      { type: '计算题', content: '5/6 ÷ 5/3 =', answer: '1/2', difficulty: 1 },
      { type: '计算题', content: '2.5 × 0.4 =', answer: '1', difficulty: 1 },
      { type: '计算题', content: '7.2 ÷ 0.8 =', answer: '9', difficulty: 1 },
      { type: '计算题', content: '3/8 + 1/4 =', answer: '5/8', difficulty: 1 },
      { type: '计算题', content: '5/6 - 1/3 =', answer: '1/2', difficulty: 1 },
      { type: '应用题', content: '一个圆的直径是10厘米，它的面积是多少平方厘米？', answer: '3.14×(10÷2)²=78.5（平方厘米）', difficulty: 2 },
      { type: '应用题', content: '一件商品原价800元，打七五折出售，现价多少元？', answer: '800×75%=600（元）', difficulty: 2 },
      { type: '填空题', content: '一个圆柱的底面半径是3厘米，高是5厘米，它的体积是（  ）立方厘米。（π取3.14）', answer: '3.14×3²×5=141.3', difficulty: 2 },
      { type: '应用题', content: '甲乙两地相距360千米，一辆汽车从甲地出发，每小时行60千米，几小时到达乙地？（用比例解）', answer: '360÷60=6（小时）', difficulty: 2 },
    ],
  },

  // ==================== 语文题库 ====================

  {
    id: "cn-g1s-u1",
    unitName: "汉语拼音",
    grade: 1,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\nmā ma（ ）", answer: "妈妈", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nshān shuǐ（ ）", answer: "山水", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\ntiān dì（ ）", answer: "天地", difficulty: 1 },
      { type: "选择题", content: "下列拼音中，声母是\"b\"的是（ ）。\nA. pō  B. bō  C. mō", answer: "B", difficulty: 1 },
      { type: "选择题", content: "\"花\"的正确拼音是（ ）。\nA. huā  B. hāu  C. huá", answer: "A", difficulty: 1 },
      { type: "判断题", content: "\"ü\"和\"j、q、x\"相拼时，上面的两点要省去。（ ）", answer: "√", difficulty: 2 },
      { type: "判断题", content: "\"zi\"是整体认读音节。（ ）", answer: "√", difficulty: 1 },
      { type: "填空题", content: "写出下列字母的大写形式：\na —（ ）  b —（ ）  d —（ ）", answer: "A；B；D", difficulty: 1 },
      { type: "填空题", content: "给下列汉字注音：\n日（ ）  月（ ）  水（ ）", answer: "rì；yuè；shuǐ", difficulty: 2 },
      { type: "组词", content: "用\"大\"字组两个词：（ ）、（ ）", answer: "大人；大家（答案不唯一）", difficulty: 1 }
    ],
  },

  {
    id: "cn-g1s-u2",
    unitName: "识字一",
    grade: 1,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "组词", content: "用\"一\"字组两个词：（ ）、（ ）", answer: "一个；一天（答案不唯一）", difficulty: 1 },
      { type: "组词", content: "用\"二\"字组两个词：（ ）、（ ）", answer: "二月；二十（答案不唯一）", difficulty: 1 },
      { type: "组词", content: "用\"三\"字组两个词：（ ）、（ ）", answer: "三月；三个（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: "\"十\"字共（ ）画，第一画是（ ）", answer: "2；横", difficulty: 1 },
      { type: "填空题", content: "\"木\"字共（ ）画，第三画是（ ）", answer: "4；撇", difficulty: 2 },
      { type: "选择题", content: "\"人\"字的笔顺是（ ）。\nA. 先撇后捺  B. 先捺后撇", answer: "A", difficulty: 1 },
      { type: "判断题", content: "\"口\"字是三面包围结构。（ ）", answer: "√", difficulty: 2 },
      { type: "判断题", content: "\"日\"和\"目\"是同一个字。（ ）", answer: "×", difficulty: 1 },
      { type: "选词填空", content: "选词填空：人  入\n门口（ ）了很多（ ）。", answer: "入；人", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n我是小学生。\n________是________。", answer: "我是好孩子。（答案不唯一）", difficulty: 2 }
    ],
  },

  {
    id: "cn-g1s-u3",
    unitName: "课文",
    grade: 1,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "填空题", content: "补充句子：\n弯弯的月亮像（ ）。", answer: "小船（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: "补充句子：\n蓝蓝的天空是（ ）的家。", answer: "白云", difficulty: 1 },
      { type: "选择题", content: "\"小小的船\"指的是（ ）。\nA. 小船  B. 月亮  C. 星星", answer: "B", difficulty: 1 },
      { type: "判断题", content: "\"影子在左，影子在右\"这句话中，影子会一直跟着我们。（ ）", answer: "√", difficulty: 1 },
      { type: "照样子写句子", content: "照样子写词语：\n大大的  ________  ________", answer: "红红的；高高的（答案不唯一）", difficulty: 1 },
      { type: "组词", content: "用\"白\"字组两个词：（ ）、（ ）", answer: "白云；白天（答案不唯一）", difficulty: 1 },
      { type: "选词填空", content: "选词填空：什么  怎么\n你（ ）名字？\n这是（ ）？", answer: "什么；什么", difficulty: 2 },
      { type: "阅读理解", content: "阅读短文回答问题：\n\"天上的白云，一会儿变成小羊，一会儿变成小马。\"\n白云变成了什么？\n答：____________________", answer: "白云变成了小羊和小马。", difficulty: 2 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nxiǎo niǎo（ ）", answer: "小鸟", difficulty: 1 },
      { type: "古诗文填空", content: "补充古诗：\n鹅鹅鹅，曲项向（ ）歌。\n白毛浮绿水，红掌拨（ ）波。", answer: "天；清", difficulty: 2 }
    ],
  },

  {
    id: "cn-g1x-u1",
    unitName: "识字",
    grade: 1,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\nchūn tiān（ ）", answer: "春天", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nhuā duǒ（ ）", answer: "花朵", difficulty: 1 },
      { type: "组词", content: "用\"春\"字组两个词：（ ）、（ ）", answer: "春天；春风（答案不唯一）", difficulty: 1 },
      { type: "组词", content: "用\"风\"字组两个词：（ ）、（ ）", answer: "大风；风车（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: "\"春\"字共（ ）画，第五画是（ ）", answer: "9；日", difficulty: 2 },
      { type: "选词填空", content: "选词填空：青  清\n（ ）草  （ ）水", answer: "青；清", difficulty: 2 },
      { type: "判断题", content: "\"冬\"和\"东\"读音相同。（ ）", answer: "×", difficulty: 1 },
      { type: "判断题", content: "\"雪\"字上面是\"雨\"字头。（ ）", answer: "√", difficulty: 1 },
      { type: "照样子写句子", content: "照样子写句子：\n春天来了，小草绿了。\n________来了，________。", answer: "秋天来了，树叶黄了。（答案不唯一）", difficulty: 2 },
      { type: "古诗文填空", content: "补充古诗：\n春眠不觉晓，处处闻（ ）鸟。\n夜来（ ）声，花落知多少。", answer: "啼；风雨", difficulty: 2 }
    ],
  },

  {
    id: "cn-g1x-u2",
    unitName: "课文",
    grade: 1,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "填空题", content: "补充句子：\n我替爸爸（ ）。", answer: "拿拖鞋（答案不唯一）", difficulty: 1 },
      { type: "选择题", content: "\"小壁虎借尾巴\"中，小壁虎最后（ ）。\nA. 借到了尾巴  B. 自己长出了新尾巴", answer: "B", difficulty: 1 },
      { type: "判断题", content: "小壁虎的尾巴断了可以再长出来。（ ）", answer: "√", difficulty: 1 },
      { type: "阅读理解", content: "阅读短文回答问题：\n\"小白兔割草。一只小鸡走过来，小白兔把草给小鸡吃。\"\n小白兔把草给了谁？\n答：____________________", answer: "小白兔把草给了小鸡。", difficulty: 1 },
      { type: "照样子写句子", content: "照样子写句子：\n他正在写字。\n________正在________。", answer: "我正在读书。（答案不唯一）", difficulty: 2 },
      { type: "组词", content: "用\"吃\"字组两个词：（ ）、（ ）", answer: "吃饭；好吃（答案不唯一）", difficulty: 1 },
      { type: "选词填空", content: "选词填空：他  她  它\n（ ）是我的妈妈。（ ）是一只小猫。", answer: "她；它", difficulty: 2 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nzhuó yú（ ）", answer: "捉鱼", difficulty: 1 },
      { type: "古诗文填空", content: "补充古诗：\n（ ）眠不觉晓，处处闻啼鸟。", answer: "春", difficulty: 1 },
      { type: "填空题", content: "\"草\"字头是（ ），带有这个偏旁的字大多与（ ）有关。", answer: "艹；植物", difficulty: 2 }
    ],
  },

  {
    id: "cn-g2s-u1",
    unitName: "识字",
    grade: 2,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\nyí qiè（ ）", answer: "一切", difficulty: 1 },
      { type: "组词", content: "用\"识\"字组两个词：（ ）、（ ）", answer: "认识；识字（答案不唯一）", difficulty: 1 },
      { type: "组词", content: "用\"交\"字组两个词：（ ）、（ ）", answer: "交朋友；交通（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: "\"识\"字的偏旁是（ ），右边是（ ）", answer: "讠；只", difficulty: 2 },
      { type: "选词填空", content: "选词填空：园  圆\n花（ ）  （ ）月", answer: "园；圆", difficulty: 2 },
      { type: "判断题", content: "\"棉\"和\"绵\"读音相同，意思也相同。（ ）", answer: "×", difficulty: 2 },
      { type: "判断题", content: "\"枫\"字的偏旁是\"木\"字旁。（ ）", answer: "√", difficulty: 1 },
      { type: "照样子写词语", content: "照样子写词语：\nABB式：绿油油  ________  ________", answer: "红彤彤；黄澄澄（答案不唯一）", difficulty: 2 },
      { type: "阅读理解", content: "阅读短文回答问题：\n\"黄山有四绝：奇松、怪石、云海、温泉。\"\n黄山有哪四绝？\n答：____________________", answer: "奇松、怪石、云海、温泉。", difficulty: 2 },
      { type: "古诗文填空", content: "补充古诗：\n（ ）寒山径斜，白云生处有人家。\n停车坐爱枫林晚，霜叶红于（ ）花。", answer: "远上；二月", difficulty: 2 }
    ],
  },

  {
    id: "cn-g2s-u2",
    unitName: "课文",
    grade: 2,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "填空题", content: "补充句子：\n（ ）的树叶从树上落下来。", answer: "黄黄（答案不唯一）", difficulty: 1 },
      { type: "选择题", content: "\"曹冲称象\"中，曹冲用了（ ）的方法称象。\nA. 用大秤  B. 用船代替秤", answer: "B", difficulty: 1 },
      { type: "判断题", content: "曹冲是曹操的儿子。（ ）", answer: "√", difficulty: 1 },
      { type: "阅读理解", content: "阅读短文回答问题：\n\"小蝌蚪先长出后腿，再长出前腿，最后尾巴不见了，变成了青蛙。\"\n小蝌蚪先长出什么？\n答：____________________", answer: "小蝌蚪先长出后腿。", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n他一边唱歌一边跳舞。\n________一边________一边________。", answer: "妈妈一边做饭一边唱歌。（答案不唯一）", difficulty: 2 },
      { type: "选词填空", content: "选词填空：飘  漂\n树叶（ ）落下来。\n这件衣服真（ ）亮。", answer: "飘；漂", difficulty: 2 },
      { type: "组词", content: "用\"快\"字组两个词：（ ）、（ ）", answer: "快乐；赶快（答案不唯一）", difficulty: 1 },
      { type: "古诗文填空", content: "补充古诗：\n床前明月光，疑是地上（ ）。\n举头望明月，低头思（ ）。", answer: "霜；故乡", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nzhōng yú（ ）", answer: "终于", difficulty: 1 },
      { type: "照样子写词语", content: "照样子写词语：\nAABB式：高高兴兴  ________  ________", answer: "开开心心；快快乐乐（答案不唯一）", difficulty: 2 }
    ],
  },

  {
    id: "cn-g2x-u1",
    unitName: "课文",
    grade: 2,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "填空题", content: "补充句子：\n春天来了，（ ）绿了，（ ）开了。", answer: "小草；花（答案不唯一）", difficulty: 1 },
      { type: "选择题", content: "\"小柳树和小枣树\"中，小枣树的特点是（ ）。\nA. 长得漂亮  B. 结了很多枣子", answer: "B", difficulty: 1 },
      { type: "判断题", content: "每个人都有自己的长处和短处。（ ）", answer: "√", difficulty: 1 },
      { type: "阅读理解", content: "阅读短文回答问题：\n\"笋芽儿终于钻出了地面。她睁开眼睛一看，啊，多么明亮、多么美丽的世界呀！\"\n笋芽儿看到了什么？\n答：____________________", answer: "笋芽儿看到了明亮、美丽的世界。", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n渐渐地，雨停了。\n________，________。", answer: "渐渐地，天亮了。（答案不唯一）", difficulty: 2 },
      { type: "选词填空", content: "选词填空：急  及\n（ ）时  着（ ）", answer: "及；急", difficulty: 2 },
      { type: "古诗文填空", content: "补充古诗：\n草长莺飞（ ）天，拂堤杨柳醉春烟。\n儿童散学归来早，忙趁（ ）放纸鸢。", answer: "二；东风", difficulty: 2 },
      { type: "组词", content: "用\"找\"字组两个词：（ ）、（ ）", answer: "找到；找人（答案不唯一）", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nzhù yì（ ）", answer: "注意", difficulty: 1 },
      { type: "照样子写词语", content: "照样子写词语：\n又大又圆  ________  ________", answer: "又高又壮；又白又胖（答案不唯一）", difficulty: 2 }
    ],
  },

  {
    id: "cn-g3s-u1",
    unitName: "课文",
    grade: 3,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "填空题", content: "补充句子：\n秋天的雨，有一盒（ ）的颜料。", answer: "五彩缤纷", difficulty: 1 },
      { type: "选择题", content: "\"望天门山\"的作者是（ ）。\nA. 杜甫  B. 李白  C. 白居易", answer: "B", difficulty: 1 },
      { type: "判断题", content: "\"天门中断楚江开\"中\"楚江\"指的是长江。（ ）", answer: "√", difficulty: 2 },
      { type: "阅读理解", content: "阅读短文回答问题：\n\"秋天的雨，把黄色给了银杏树，红红的枫叶像一枚枚邮票，飘哇飘哇，邮来了秋天的凉爽。\"\n短文把枫叶比作什么？\n答：____________________", answer: "短文把枫叶比作邮票。", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n它把红色给了枫树，红红的枫叶像一枚枚邮票。\n它把________给了________，________像________。", answer: "它把黄色给了银杏树，黄黄的叶子像一把把小扇子。（答案不唯一）", difficulty: 2 },
      { type: "古诗文填空", content: "补充古诗：\n望天门山\n天门中断楚江开，（ ）水东流至此回。\n两岸青山相对出，（ ）一片日边来。", answer: "碧；孤帆", difficulty: 2 },
      { type: "选词填空", content: "选词填空：安静  平静\n教室里非常（ ）。\n湖面十分（ ）。", answer: "安静；平静", difficulty: 2 },
      { type: "组词", content: "用\"飘\"字组两个词：（ ）、（ ）", answer: "飘动；飘扬（答案不唯一）", difficulty: 1 },
      { type: "照样子写词语", content: "照样子写词语：\n表示颜色：金黄  ________  ________", answer: "火红；翠绿（答案不唯一）", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nfēng shōu（ ）", answer: "丰收", difficulty: 1 }
    ],
  },

  {
    id: "cn-g3s-u2",
    unitName: "习作",
    grade: 3,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "照样子写句子", content: "把下面的句子写具体：\n原句：花开了。\n具体：____________________", answer: "美丽的鲜花在春风中轻轻地开放了。（答案不唯一）", difficulty: 2 },
      { type: "照样子写句子", content: "用比喻句补充句子：\n弯弯的月亮像________。", answer: "一把镰刀（答案不唯一）", difficulty: 2 },
      { type: "选词填空", content: "选词填空：陆续  继续  连续\n同学们（ ）走进教室。\n他（ ）三天没来上学了。\n请大家（ ）做作业。", answer: "陆续；连续；继续", difficulty: 3 },
      { type: "判断题", content: "\"他跑得像兔子一样快\"是一个比喻句。（ ）", answer: "√", difficulty: 1 },
      { type: "照样子写句子", content: "照样子写句子：\n不但……而且……\n____________________", answer: "他不但学习好，而且品德好。（答案不唯一）", difficulty: 2 },
      { type: "填空题", content: "写出一个拟人句：\n____________________", answer: "小草从土里探出头来。（答案不唯一）", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n因为……所以……\n____________________", answer: "因为下雨了，所以我带了伞。（答案不唯一）", difficulty: 2 },
      { type: "阅读理解", content: "阅读短文，找出比喻句并抄写下来：\n\"荷叶圆圆的，绿绿的。小水珠说：荷叶是我的摇篮。\"\n比喻句：____________________", answer: "荷叶是我的摇篮。", difficulty: 2 },
      { type: "照样子写句子", content: "用\"有的……有的……有的……\"写一句话：\n____________________", answer: "下课了，同学们有的在跑步，有的在跳绳，有的在做游戏。（答案不唯一）", difficulty: 2 },
      { type: "组词", content: "用\"观察\"写一句话：\n____________________", answer: "我仔细观察了小蚂蚁搬家的过程。（答案不唯一）", difficulty: 2 }
    ],
  },

  {
    id: "cn-g3x-u1",
    unitName: "课文",
    grade: 3,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "填空题", content: "补充句子：\n荷花已经开了不少了。荷叶（ ）的，像一个个碧绿的大圆盘。", answer: "挨挨挤挤", difficulty: 1 },
      { type: "选择题", content: "\"绝句\"的作者是（ ）。\nA. 杜甫  B. 李白  C. 苏轼", answer: "A", difficulty: 1 },
      { type: "判断题", content: "\"泥融飞燕子，沙暖睡鸳鸯\"描写的是春天的景色。（ ）", answer: "√", difficulty: 2 },
      { type: "阅读理解", content: "阅读短文回答问题：\n\"有的才展开两三片花瓣儿。有的花瓣儿全展开了，露出嫩黄色的小莲蓬。有的还是花骨朵儿，看起来饱胀得马上要破裂似的。\"\n这段话写了几种形态的荷花？\n答：____________________", answer: "这段话写了三种形态的荷花。", difficulty: 2 },
      { type: "古诗文填空", content: "补充古诗：\n绝句\n迟日江山丽，春风花草（ ）。\n泥融飞燕子，沙暖睡（ ）鸯。", answer: "香；鸳", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n荷叶像一个个碧绿的大圆盘。\n________像________。", answer: "白云像一群洁白的绵羊。（答案不唯一）", difficulty: 2 },
      { type: "选词填空", content: "选词填空：清香  芳香\n荷花的（ ）吸引了很多游客。\n花园里飘来阵阵（ ）。", answer: "清香；芳香", difficulty: 2 },
      { type: "组词", content: "用\"莲\"字组两个词：（ ）、（ ）", answer: "莲花；莲子（答案不唯一）", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nfǎng fú（ ）", answer: "仿佛", difficulty: 1 },
      { type: "照样子写词语", content: "照样子写词语：\n挨挨挤挤（AABB式）________  ________", answer: "清清楚楚；明明白白（答案不唯一）", difficulty: 2 }
    ],
  },

  {
    id: "cn-g3x-u2",
    unitName: "习作",
    grade: 3,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "照样子写句子", content: "把句子改成比喻句：\n原句：秋风吹过，树叶落了下来。\n改写：____________________", answer: "秋风吹过，树叶像蝴蝶一样飘落下来。（答案不唯一）", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n不仅……还……\n____________________", answer: "小明不仅学习好，还乐于助人。（答案不唯一）", difficulty: 2 },
      { type: "选词填空", content: "选词填空：希望  盼望  愿望\n我的（ ）是当一名老师。\n妈妈（ ）我能考个好成绩。\n我（ ）着假期的到来。", answer: "愿望；希望；盼望", difficulty: 3 },
      { type: "判断题", content: "\"小明长得像他爸爸\"是一个比喻句。（ ）", answer: "×", difficulty: 2 },
      { type: "照样子写句子", content: "用\"如果……就……\"写一句话：\n____________________", answer: "如果明天不下雨，我们就去公园玩。（答案不唯一）", difficulty: 2 },
      { type: "填空题", content: "写出一个排比句：\n____________________", answer: "天上的云，有的像小狗，有的像小猫，有的像小兔。（答案不唯一）", difficulty: 3 },
      { type: "照样子写句子", content: "用修改符号修改病句：\n\"我忍不住不禁笑了起来。\"", answer: "去掉“忍不住”或去掉“不禁”", difficulty: 3 },
      { type: "阅读理解", content: "阅读短文，找出拟人句：\n\"春天来了，小草从土里探出头来，桃花笑红了脸。\"\n拟人句：____________________", answer: "小草从土里探出头来，桃花笑红了脸。", difficulty: 2 },
      { type: "照样子写句子", content: "用\"虽然……但是……\"写一句话：\n____________________", answer: "虽然今天很冷，但是我仍然坚持上学。（答案不唯一）", difficulty: 2 },
      { type: "组词", content: "用\"惊讶\"写一句话：\n____________________", answer: "听到这个消息，我感到非常惊讶。（答案不唯一）", difficulty: 2 }
    ],
  },

  {
    id: "en-g3s-u1",
    unitName: "Hello",
    grade: 3,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "当你早上见到老师时，你应该说（ ）。\nA. Good morning!  B. Good evening!  C. Good night!", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"再见\"用英语怎么说？（ ）\nA. Hello  B. Goodbye  C. Hi", answer: "B", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nruler —（ ）  pencil —（ ）  eraser —（ ）", answer: "尺子；铅笔；橡皮", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n书包 —（ ）  文具盒 —（ ）", answer: "bag；pencil box", difficulty: 1 },
      { type: "连词成句", content: "连词成句：\nare / you / How（ ? ）", answer: "How are you?", difficulty: 1 },
      { type: "连词成句", content: "连词成句：\nI / am / fine（ . ）", answer: "I am fine.", difficulty: 1 },
      { type: "情景交际", content: "当你想问别人的名字时，你应该说（ ）。\nA. How are you?  B. What's your name?  C. Good morning.", answer: "B", difficulty: 1 },
      { type: "情景交际", content: "别人对你说\"How are you?\"，你应该回答（ ）。\nA. I'm fine, thank you.  B. My name is Tom.  C. Goodbye.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"crayon\"的意思是（ ）。\nA. 蜡笔  B. 钢笔  C. 尺子", answer: "A", difficulty: 1 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: Hello! I'm Mike.\nB: Hi! I'm Wu Yifan.\nA: What's your name?\nC: My name is Sarah.\nWho is C?\n答：____________________", answer: "C is Sarah.", difficulty: 2 }
    ],
  },

  {
    id: "en-g3s-u2",
    unitName: "Colours",
    grade: 3,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"红色\"用英语怎么说？（ ）\nA. blue  B. red  C. green", answer: "B", difficulty: 1 },
      { type: "单词选择", content: "\"yellow\"的意思是（ ）。\nA. 蓝色  B. 绿色  C. 黄色", answer: "C", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nblack —（ ）  white —（ ）  orange —（ ）", answer: "黑色；白色；橙色", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n蓝色 —（ ）  绿色 —（ ）  棕色 —（ ）", answer: "blue；green；brown", difficulty: 1 },
      { type: "情景交际", content: "你想告诉别人你看到了一朵红色的花，你应该说（ ）。\nA. I see a red flower.  B. I see a blue flower.  C. I see a green flower.", answer: "A", difficulty: 1 },
      { type: "连词成句", content: "连词成句：\nis / it / What / colour（ ? ）", answer: "What colour is it?", difficulty: 2 },
      { type: "情景交际", content: "别人问你\"What colour is it?\"，它是绿色的，你应回答（ ）。\nA. It's green.  B. It's a green.  C. I see green.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"purple\"的意思是（ ）。\nA. 粉色  B. 紫色  C. 橙色", answer: "B", difficulty: 1 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: Good morning, Miss White!\nB: Good morning! I have a bag.\nA: What colour is it?\nB: It's yellow.\nWhat colour is the bag?\n答：____________________", answer: "It's yellow.", difficulty: 2 },
      { type: "单词选择", content: "\"pink\"的意思是（ ）。\nA. 粉色  B. 红色  C. 白色", answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g3s-u3",
    unitName: "Look at me",
    grade: 3,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"face\"的意思是（ ）。\nA. 脸  B. 手  C. 脚", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"ear\"的意思是（ ）。\nA. 眼睛  B. 鼻子  C. 耳朵", answer: "C", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\neye —（ ）  nose —（ ）  mouth —（ ）", answer: "眼睛；鼻子；嘴巴", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n头 —（ ）  手 —（ ）  脚 —（ ）", answer: "head；hand；foot", difficulty: 1 },
      { type: "情景交际", content: "你想让别人看你，你应该说（ ）。\nA. Look at me!  B. Look at my face!  C. Touch your face.", answer: "A", difficulty: 1 },
      { type: "连词成句", content: "连词成句：\nyour / Touch / nose（ . ）", answer: "Touch your nose.", difficulty: 1 },
      { type: "情景交际", content: "老师让你摸摸你的脸，你应该（ ）。\nA. Touch your face.  B. Clap your hands.  C. Stamp your foot.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"arm\"的意思是（ ）。\nA. 腿  B. 胳膊  C. 手指", answer: "B", difficulty: 1 },
      { type: "单词选择", content: "\"leg\"的意思是（ ）。\nA. 手  B. 脚  C. 腿", answer: "C", difficulty: 1 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: Let's make a puppet!\nB: Great!\nA: This is the face.\nB: OK.\nWhat are they making?\n答：____________________", answer: "They are making a puppet.", difficulty: 2 }
    ],
  },

  {
    id: "en-g3x-u1",
    unitName: "Welcome back",
    grade: 3,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"boy\"的意思是（ ）。\nA. 女孩  B. 男孩  C. 老师", answer: "B", difficulty: 1 },
      { type: "单词选择", content: "\"girl\"的意思是（ ）。\nA. 男孩  B. 女孩  C. 朋友", answer: "B", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nteacher —（ ）  student —（ ）  pupil —（ ）", answer: "老师；学生；小学生", difficulty: 1 },
      { type: "情景交际", content: "你想介绍自己是新同学，你应该说（ ）。\nA. I'm a new student.  B. I'm a new teacher.  C. I'm a boy.", answer: "A", difficulty: 1 },
      { type: "连词成句", content: "连词成句：\na / I / am / student（ . ）", answer: "I am a student.", difficulty: 1 },
      { type: "情景交际", content: "你想问别人是哪里人，你应该说（ ）。\nA. Where are you from?  B. Who are you?  C. How are you?", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"she\"的意思是（ ）。\nA. 他  B. 她  C. 它", answer: "B", difficulty: 1 },
      { type: "单词选择", content: "\"he\"的意思是（ ）。\nA. 他  B. 她  C. 它", answer: "A", difficulty: 1 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: Hi, I'm Amy. I'm from the UK.\nB: Hi, I'm Zhang Peng. I'm from China.\nWhere is Amy from?\n答：____________________", answer: "She is from the UK.", difficulty: 2 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n他 —（ ）  她 —（ ）  它 —（ ）", answer: "he；she；it", difficulty: 1 }
    ],
  },

  {
    id: "en-g3x-u2",
    unitName: "My family",
    grade: 3,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"father\"的意思是（ ）。\nA. 妈妈  B. 爸爸  C. 兄弟", answer: "B", difficulty: 1 },
      { type: "单词选择", content: "\"mother\"的意思是（ ）。\nA. 妈妈  B. 爸爸  C. 姐妹", answer: "A", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nbrother —（ ）  sister —（ ）  grandmother —（ ）", answer: "兄弟；姐妹；奶奶/外婆", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n爷爷/外公 —（ ）  家人 —（ ）", answer: "grandfather/grandpa；family", difficulty: 1 },
      { type: "情景交际", content: "你想介绍你的爸爸，你应该说（ ）。\nA. This is my father.  B. That is my mother.  C. He is my brother.", answer: "A", difficulty: 1 },
      { type: "连词成句", content: "连词成句：\nis / Who / that / man（ ? ）", answer: "Who is that man?", difficulty: 2 },
      { type: "情景交际", content: "别人问你\"Who's that woman?\"，她是你的妈妈，你应回答（ ）。\nA. She is my mother.  B. He is my father.  C. She is my sister.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"uncle\"的意思是（ ）。\nA. 叔叔/舅舅  B. 阿姨/姑姑  C. 表兄弟", answer: "A", difficulty: 1 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: Who's that man?\nB: He's my father.\nA: Who's that woman?\nB: She's my mother.\nWho is the man?\n答：____________________", answer: "B's father.", difficulty: 2 },
      { type: "单词选择", content: "\"aunt\"的意思是（ ）。\nA. 叔叔  B. 阿姨/姑姑  C. 奶奶", answer: "B", difficulty: 1 }
    ],
  },

  {
    id: "en-g3x-u3",
    unitName: "At the zoo",
    grade: 3,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"monkey\"的意思是（ ）。\nA. 猴子  B. 大象  C. 老虎", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"elephant\"的意思是（ ）。\nA. 狮子  B. 大象  C. 熊猫", answer: "B", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\ngiraffe —（ ）  tiger —（ ）  panda —（ ）", answer: "长颈鹿；老虎；熊猫", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n大的 —（ ）  小的 —（ ）  高的 —（ ）", answer: "big；small；tall", difficulty: 1 },
      { type: "情景交际", content: "你想描述一只大象很大，你应该说（ ）。\nA. Look at the elephant. It's so big!  B. Look at the monkey. It's small.", answer: "A", difficulty: 1 },
      { type: "连词成句", content: "连词成句：\nis / It / so / big（ ! ）", answer: "It is so big!", difficulty: 1 },
      { type: "情景交际", content: "你想描述长颈鹿很高，你应该说（ ）。\nA. The giraffe is so tall.  B. The giraffe is so short.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"fat\"的反义词是（ ）。\nA. thin  B. tall  C. big", answer: "A", difficulty: 1 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: Look at that giraffe!\nB: Wow! It's so tall!\nA: Look at that bear!\nB: Ha! It's short and fat!\nIs the giraffe tall?\n答：____________________", answer: "Yes, it is.", difficulty: 2 },
      { type: "单词选择", content: "\"short\"的反义词是（ ）。\nA. fat  B. tall  C. long", answer: "B", difficulty: 1 }
    ],
  },

  {
    id: "en-g4s-u1",
    unitName: "My classroom",
    grade: 4,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"classroom\"的意思是（ ）。\nA. 教室  B. 学校  C. 操场", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"window\"的意思是（ ）。\nA. 门  B. 窗户  C. 黑板", answer: "B", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nblackboard —（ ）  light —（ ）  picture —（ ）", answer: "黑板；灯；图画", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n门 —（ ）  电脑 —（ ）  书桌 —（ ）", answer: "door；computer；desk", difficulty: 1 },
      { type: "情景交际", content: "你想问教室里有什么，你应该说（ ）。\nA. What's in the classroom?  B. Where is the classroom?", answer: "A", difficulty: 1 },
      { type: "连词成句", content: "连词成句：\nis / This / my / classroom（ . ）", answer: "This is my classroom.", difficulty: 1 },
      { type: "情景交际", content: "你想说\"让我们擦黑板吧\"，你应该说（ ）。\nA. Let's clean the blackboard.  B. Let's clean the window.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"floor\"的意思是（ ）。\nA. 墙壁  B. 地板  C. 天花板", answer: "B", difficulty: 1 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: What's in the classroom?\nB: One blackboard, one TV, many desks and chairs.\nHow many blackboards are there?\n答：____________________", answer: "One blackboard.", difficulty: 2 },
      { type: "情景交际", content: "你想表达\"它在窗户旁边\"，你应该说（ ）。\nA. It's near the window.  B. It's on the window.", answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g4s-u2",
    unitName: "My schoolbag",
    grade: 4,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"schoolbag\"的意思是（ ）。\nA. 书包  B. 书本  C. 文具盒", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"notebook\"的意思是（ ）。\nA. 故事书  B. 笔记本  C. 数学书", answer: "B", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nstorybook —（ ）  maths book —（ ）  English book —（ ）", answer: "故事书；数学书；英语书", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n语文书 —（ ）  玩具 —（ ）  糖果 —（ ）", answer: "Chinese book；toy；candy", difficulty: 1 },
      { type: "情景交际", content: "你想问书包里有什么，你应该说（ ）。\nA. What's in your schoolbag?  B. Where is your schoolbag?", answer: "A", difficulty: 1 },
      { type: "连词成句", content: "连词成句：\nin / What / your / is / schoolbag（ ? ）", answer: "What is in your schoolbag?", difficulty: 2 },
      { type: "情景交际", content: "你想说\"我有一个新书包\"，你应该说（ ）。\nA. I have a new schoolbag.  B. I have a new book.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"key\"的意思是（ ）。\nA. 钥匙  B. 钢笔  C. 铅笔", answer: "A", difficulty: 1 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: I have a new schoolbag.\nB: What's in it?\nA: An English book, a maths book and three storybooks.\nHow many books are in the schoolbag?\n答：____________________", answer: "Five books.", difficulty: 2 },
      { type: "单词选择", content: "\"candy\"的意思是（ ）。\nA. 面包  B. 糖果  C. 蛋糕", answer: "B", difficulty: 1 }
    ],
  },

  {
    id: "en-g4s-u3",
    unitName: "My friends",
    grade: 4,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"friendly\"的意思是（ ）。\nA. 友好的  B. 安静的  C. 高的", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"quiet\"的意思是（ ）。\nA. 强壮的  B. 安静的  C. 友好的", answer: "B", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\ntall —（ ）  strong —（ ）  thin —（ ）", answer: "高的；强壮的；瘦的", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n头发 —（ ）  鞋子 —（ ）  眼镜 —（ ）", answer: "hair；shoes；glasses", difficulty: 1 },
      { type: "情景交际", content: "你想介绍你的朋友，你应该说（ ）。\nA. This is my friend. His name is Tom.  B. He is my teacher.", answer: "A", difficulty: 1 },
      { type: "连词成句", content: "连词成句：\nHe / is / tall / and / strong（ . ）", answer: "He is tall and strong.", difficulty: 1 },
      { type: "情景交际", content: "你想问\"他叫什么名字？\"，你应该说（ ）。\nA. What's his name?  B. What's her name?  C. Who is he?", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"glasses\"的意思是（ ）。\nA. 帽子  B. 眼镜  C. 鞋子", answer: "B", difficulty: 1 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: I have a good friend. He's tall and strong. He has big eyes.\nB: Who is he?\nA: His name is Zhang Peng.\nIs Zhang Peng tall?\n答：____________________", answer: "Yes, he is.", difficulty: 2 },
      { type: "情景交际", content: "你想说\"她又高又瘦\"，你应该说（ ）。\nA. She is tall and thin.  B. She is short and thin.", answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g4x-u1",
    unitName: "My school",
    grade: 4,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"playground\"的意思是（ ）。\nA. 教室  B. 操场  C. 图书馆", answer: "B", difficulty: 1 },
      { type: "单词选择", content: "\"library\"的意思是（ ）。\nA. 图书馆  B. 操场  C. 花园", answer: "A", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nfirst floor —（ ）  second floor —（ ）  garden —（ ）", answer: "一楼；二楼；花园", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n教师办公室 —（ ）  电脑房 —（ ）  美术教室 —（ ）", answer: "teachers' office；computer room；art room", difficulty: 1 },
      { type: "情景交际", content: "你想问图书馆在哪里，你应该说（ ）。\nA. Where is the library?  B. Is this the library?", answer: "A", difficulty: 1 },
      { type: "连词成句", content: "连词成句：\nthe / Where / is / library（ ? ）", answer: "Where is the library?", difficulty: 1 },
      { type: "情景交际", content: "你想问\"这是教师办公室吗？\"，你应该说（ ）。\nA. Is this the teachers' office?  B. Where is the teachers' office?", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"music room\"的意思是（ ）。\nA. 音乐教室  B. 美术教室  C. 电脑房", answer: "A", difficulty: 1 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: Excuse me. Where is the library?\nB: It's on the second floor.\nA: Is it next to the computer room?\nB: Yes, it is.\nWhere is the library?\n答：____________________", answer: "It's on the second floor.", difficulty: 2 },
      { type: "情景交际", content: "你想说\"教室在一楼\"，你应该说（ ）。\nA. The classroom is on the first floor.  B. The classroom is on the second floor.", answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g4x-u2",
    unitName: "What time is it",
    grade: 4,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"breakfast\"的意思是（ ）。\nA. 早餐  B. 午餐  C. 晚餐", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"lunch\"的意思是（ ）。\nA. 早餐  B. 午餐  C. 晚餐", answer: "B", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\ndinner —（ ）  English class —（ ）  PE class —（ ）", answer: "晚餐；英语课；体育课", difficulty: 1 },
      { type: "情景交际", content: "你想问\"现在几点了？\"，你应该说（ ）。\nA. What time is it?  B. What day is it?", answer: "A", difficulty: 1 },
      { type: "连词成句", content: "连词成句：\nit / is / What / time（ ? ）", answer: "What time is it?", difficulty: 1 },
      { type: "情景交际", content: "现在是9点，你想说\"It's nine o'clock.\"，对吗？（ ）", answer: "√", difficulty: 1 },
      { type: "单词选择", content: "\"dinner\"的意思是（ ）。\nA. 早餐  B. 午餐  C. 晚餐", answer: "C", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n该上学了 —（ ）  该起床了 —（ ）", answer: "It's time for school；It's time to get up", difficulty: 2 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: What time is it?\nB: It's 8 o'clock. It's time for English class.\nWhat class is it?\n答：____________________", answer: "It's English class.", difficulty: 2 },
      { type: "情景交际", content: "你想说\"到吃午餐的时间了\"，你应该说（ ）。\nA. It's time for lunch.  B. It's time for breakfast.", answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g4x-u3",
    unitName: "Weather",
    grade: 4,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"sunny\"的意思是（ ）。\nA. 晴天的  B. 多云的  C. 下雨的", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"cloudy\"的意思是（ ）。\nA. 晴天的  B. 多云的  C. 下雪的", answer: "B", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nrainy —（ ）  snowy —（ ）  windy —（ ）", answer: "下雨的；下雪的；有风的", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n温暖的 —（ ）  寒冷的 —（ ）  凉爽的 —（ ）", answer: "warm；cold；cool", difficulty: 1 },
      { type: "情景交际", content: "你想问\"今天天气怎么样？\"，你应该说（ ）。\nA. What's the weather like today?  B. How are you today?", answer: "A", difficulty: 1 },
      { type: "连词成句", content: "连词成句：\nis / the / weather / What / like（ ? ）", answer: "What is the weather like?", difficulty: 2 },
      { type: "情景交际", content: "外面在下雨，妈妈让你带伞，她应该说（ ）。\nA. It's rainy. Take your umbrella.  B. It's sunny. Put on your sunglasses.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"hot\"的反义词是（ ）。\nA. warm  B. cold  C. cool", answer: "B", difficulty: 1 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: What's the weather like in Beijing?\nB: It's warm and sunny.\nA: Can I go outside?\nB: Yes, you can.\nWhat's the weather like in Beijing?\n答：____________________", answer: "It's warm and sunny.", difficulty: 2 },
      { type: "情景交际", content: "你想说\"今天很冷\"，你应该说（ ）。\nA. It's cold today.  B. It's hot today.", answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "sc-g3s-u1",
    unitName: "植物",
    grade: 3,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: "植物的根的主要作用是（ ）。\nA. 吸收水分  B. 进行光合作用  C. 开花结果", answer: "A", difficulty: 1 },
      { type: "选择题", content: "植物的叶子主要作用是（ ）。\nA. 吸收水分  B. 进行光合作用  C. 输送养分", answer: "B", difficulty: 1 },
      { type: "判断题", content: "所有植物都开花结果。（ ）", answer: "×", difficulty: 2 },
      { type: "判断题", content: "植物的茎能将水分和养料输送到叶子和花。（ ）", answer: "√", difficulty: 1 },
      { type: "填空题", content: "植物的六大器官是根、茎、叶、花、（ ）、（ ）。", answer: "果实；种子", difficulty: 2 },
      { type: "填空题", content: "植物的叶子是绿色的，因为叶子中含有（ ）。", answer: "叶绿素", difficulty: 2 },
      { type: "选择题", content: "下列哪种植物是用种子繁殖的？（ ）\nA. 蕨类  B. 苹果树  C. 青苔", answer: "B", difficulty: 2 },
      { type: "简答题", content: "请说出植物的根有什么作用。", answer: "根能固定植物，吸收土壤中的水分和矿物质。", difficulty: 2 },
      { type: "填空题", content: "植物生长需要（ ）、（ ）、适宜的温度和空气。", answer: "阳光；水", difficulty: 1 },
      { type: "判断题", content: "没有阳光，植物也能正常生长。（ ）", answer: "×", difficulty: 1 }
    ],
  },

  {
    id: "sc-g3s-u2",
    unitName: "动物",
    grade: 3,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: "下列动物中属于哺乳动物的是（ ）。\nA. 鸡  B. 狗  C. 鱼", answer: "B", difficulty: 1 },
      { type: "选择题", content: "下列动物中属于昆虫的是（ ）。\nA. 蝴蝶  B. 蜘蛛  C. 蜈蚣", answer: "A", difficulty: 2 },
      { type: "判断题", content: "鱼用鳃呼吸。（ ）", answer: "√", difficulty: 1 },
      { type: "判断题", content: "所有动物都是胎生的。（ ）", answer: "×", difficulty: 1 },
      { type: "填空题", content: "动物可以分为脊椎动物和（ ）动物两大类。", answer: "无脊椎", difficulty: 2 },
      { type: "填空题", content: "鸟类身体表面覆盖着（ ），用（ ）呼吸。", answer: "羽毛；肺", difficulty: 1 },
      { type: "选择题", content: "下列动物中生活在水中的是（ ）。\nA. 麻雀  B. 蝴蝶  C. 金鱼", answer: "C", difficulty: 1 },
      { type: "简答题", content: "请说出鱼类和哺乳动物的一个区别。", answer: "鱼类用鳃呼吸，哺乳动物用肺呼吸。（答案不唯一）", difficulty: 2 },
      { type: "填空题", content: "动物的运动方式有飞行、（ ）、游泳、爬行等。", answer: "奔跑（或行走）", difficulty: 1 },
      { type: "判断题", content: "蜻蜓有四只翅膀。（ ）", answer: "√", difficulty: 2 }
    ],
  },

  {
    id: "sc-g3s-u3",
    unitName: "我们周围的材料",
    grade: 3,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: "下列材料中属于天然材料的是（ ）。\nA. 塑料  B. 木材  C. 玻璃", answer: "B", difficulty: 1 },
      { type: "选择题", content: "下列材料中属于人造材料的是（ ）。\nA. 棉花  B. 皮革  C. 塑料", answer: "C", difficulty: 1 },
      { type: "判断题", content: "金属能导电。（ ）", answer: "√", difficulty: 1 },
      { type: "判断题", content: "塑料是天然材料。（ ）", answer: "×", difficulty: 1 },
      { type: "填空题", content: "我们常见的材料有金属、木头、（ ）、（ ）、塑料等。", answer: "纸；玻璃（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: "金属的共同性质是：有光泽、能导热、能（ ）、有延展性。", answer: "导电", difficulty: 2 },
      { type: "选择题", content: "做衣服最常用的材料是（ ）。\nA. 金属  B. 玻璃  C. 棉布", answer: "C", difficulty: 1 },
      { type: "简答题", content: "请说出木头和塑料各有什么优点。", answer: "木头：天然、环保、较轻。塑料：防水、耐用、轻便。（答案不唯一）", difficulty: 2 },
      { type: "填空题", content: "玻璃的特点是透明、（ ）、易碎。", answer: "光滑", difficulty: 1 },
      { type: "判断题", content: "不同材料有不同的性质，用途也不同。（ ）", answer: "√", difficulty: 1 }
    ],
  },

  {
    id: "sc-g3x-u1",
    unitName: "物体的运动",
    grade: 3,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: "下列运动中属于直线运动的是（ ）。\nA. 荡秋千  B. 电梯升降  C. 旋转的陀螺", answer: "B", difficulty: 1 },
      { type: "选择题", content: "下列运动中属于曲线运动的是（ ）。\nA. 滑滑梯  B. 荡秋千  C. 拉抽屉", answer: "B", difficulty: 1 },
      { type: "判断题", content: "物体的运动方式只有直线运动和曲线运动两种。（ ）", answer: "√", difficulty: 1 },
      { type: "判断题", content: "滚动的足球既在做直线运动，也在做旋转运动。（ ）", answer: "√", difficulty: 2 },
      { type: "填空题", content: "物体的运动方式有（ ）运动和（ ）运动。", answer: "直线；曲线", difficulty: 1 },
      { type: "填空题", content: "在相同距离内，所用时间越（ ），物体运动越快。", answer: "短", difficulty: 2 },
      { type: "选择题", content: "测量物体运动快慢需要用到的工具是（ ）。\nA. 温度计  B. 秒表  C. 天平", answer: "B", difficulty: 1 },
      { type: "简答题", content: "怎样比较两个物体运动的快慢？", answer: "在相同距离内比较时间，时间短的快；在相同时间内比较距离，距离长的快。", difficulty: 2 },
      { type: "填空题", content: "在相同时间内，通过的（ ）越长，物体运动越快。", answer: "距离", difficulty: 2 },
      { type: "判断题", content: "运动物体的速度与方向无关。（ ）", answer: "×", difficulty: 2 }
    ],
  },

  {
    id: "sc-g3x-u2",
    unitName: "动物的生命周期",
    grade: 3,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: "蝴蝶的一生要经历（ ）个阶段。\nA. 3  B. 4  C. 5", answer: "B", difficulty: 1 },
      { type: "选择题", content: "下列动物中经历完全变态发育的是（ ）。\nA. 蝗虫  B. 蝴蝶  C. 蜻蜓", answer: "B", difficulty: 2 },
      { type: "判断题", content: "青蛙的幼体和成体长得一样。（ ）", answer: "×", difficulty: 1 },
      { type: "判断题", content: "所有动物都是从卵孵化出来的。（ ）", answer: "×", difficulty: 2 },
      { type: "填空题", content: "蝴蝶的发育过程经历卵、（ ）、（ ）、成虫四个阶段。", answer: "幼虫；蛹", difficulty: 2 },
      { type: "填空题", content: "鸡的发育过程经历卵、（ ）、成鸡三个阶段。", answer: "雏鸡", difficulty: 1 },
      { type: "选择题", content: "青蛙的幼体叫（ ）。\nA. 蝌蚪  B. 毛毛虫  C. 子孓", answer: "A", difficulty: 1 },
      { type: "简答题", content: "请说出蝴蝶和蚕的生命周期有什么相同点。", answer: "它们都经历卵、幼虫、蛹、成虫四个阶段，都属于完全变态发育。", difficulty: 3 },
      { type: "填空题", content: "蚕的一生经历卵、（ ）、蛹、（ ）四个阶段。", answer: "幼虫；成虫", difficulty: 2 },
      { type: "判断题", content: "蚕蛹不会变成蚕蛾。（ ）", answer: "×", difficulty: 1 }
    ],
  },

  {
    id: "sc-g4s-u1",
    unitName: "声音",
    grade: 4,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: "声音是由物体的（ ）产生的。\nA. 静止  B. 振动  C. 转动", answer: "B", difficulty: 1 },
      { type: "选择题", content: "声音的传播需要（ ）。\nA. 空气  B. 介质  C. 光", answer: "B", difficulty: 2 },
      { type: "判断题", content: "声音能在真空中传播。（ ）", answer: "×", difficulty: 2 },
      { type: "判断题", content: "声音在固体中传播速度最快。（ ）", answer: "√", difficulty: 2 },
      { type: "填空题", content: "声音可以在（ ）、液体和（ ）中传播。", answer: "气体；固体", difficulty: 1 },
      { type: "填空题", content: "声音的高低叫做（ ），声音的大小叫做（ ）。", answer: "音调；响度", difficulty: 2 },
      { type: "选择题", content: "下列哪种方法可以减小声音的响度？（ ）\nA. 用更大的力敲鼓  B. 用更小的力敲鼓  C. 换一个更大的鼓", answer: "B", difficulty: 1 },
      { type: "简答题", content: "怎样使声音变大？", answer: "增大振动的幅度，声音就会变大。", difficulty: 2 },
      { type: "填空题", content: "控制噪声的三种方法：在声源处（ ）、在传播过程中（ ）、在人耳处（ ）。", answer: "减弱；减弱；减弱", difficulty: 3 },
      { type: "判断题", content: "物体振动越快，声音越高。（ ）", answer: "√", difficulty: 1 }
    ],
  },

  {
    id: "sc-g4s-u2",
    unitName: "呼吸与消化",
    grade: 4,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: "人体的呼吸器官中，进行气体交换的主要场所是（ ）。\nA. 鼻腔  B. 气管  C. 肺", answer: "C", difficulty: 1 },
      { type: "选择题", content: "我们吸入的气体中含量最多的是（ ）。\nA. 氧气  B. 氮气  C. 二氧化碳", answer: "B", difficulty: 2 },
      { type: "判断题", content: "食物的营养主要在小肠中被吸收。（ ）", answer: "√", difficulty: 1 },
      { type: "判断题", content: "口腔是消化的第一站。（ ）", answer: "√", difficulty: 1 },
      { type: "填空题", content: "人呼吸时，吸入（ ），呼出（ ）。", answer: "氧气；二氧化碳", difficulty: 1 },
      { type: "填空题", content: "人体的消化器官有口腔、食道、胃、（ ）、大肠和肛门。", answer: "小肠", difficulty: 2 },
      { type: "选择题", content: "下列食物中富含蛋白质的是（ ）。\nA. 米饭  B. 鸡蛋  C. 苹果", answer: "B", difficulty: 1 },
      { type: "简答题", content: "请说出保护呼吸器官的方法（至少两种）。", answer: "不吸烟、多运动、保持空气清新、戴口罩等。（答案不唯一）", difficulty: 2 },
      { type: "填空题", content: "食物中的营养成分主要有蛋白质、糖类、脂肪、维生素、（ ）和（ ）。", answer: "矿物质；水", difficulty: 2 },
      { type: "判断题", content: "运动后呼吸会加快。（ ）", answer: "√", difficulty: 1 }
    ],
  },

  {
    id: "sc-g4x-u1",
    unitName: "电",
    grade: 4,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: "下列物体中属于导体的是（ ）。\nA. 塑料  B. 铁丝  C. 木头", answer: "B", difficulty: 1 },
      { type: "选择题", content: "下列物体中属于绝缘体的是（ ）。\nA. 铜线  B. 铝箔  C. 橡胶", answer: "C", difficulty: 1 },
      { type: "判断题", content: "一个完整的电路需要电源、导线、用电器和开关。（ ）", answer: "√", difficulty: 1 },
      { type: "判断题", content: "干电池的铜帽一端是正极。（ ）", answer: "√", difficulty: 1 },
      { type: "填空题", content: "电路有两种连接方式：（ ）联和（ ）联。", answer: "串；并", difficulty: 2 },
      { type: "填空题", content: "容易导电的物体叫做（ ），不容易导电的物体叫做（ ）。", answer: "导体；绝缘体", difficulty: 1 },
      { type: "选择题", content: "下列做法中安全的是（ ）。\nA. 用湿手触摸开关  B. 在高压线下放风筝  C. 使用绝缘手柄的工具", answer: "C", difficulty: 1 },
      { type: "简答题", content: "请说出安全用电的注意事项（至少两条）。", answer: "不用湿手触摸电器、不私自拆装电器、不在高压线下玩耍等。（答案不唯一）", difficulty: 2 },
      { type: "填空题", content: "开关的作用是控制（ ）的通断。", answer: "电流", difficulty: 1 },
      { type: "判断题", content: "人体是导体。（ ）", answer: "√", difficulty: 1 }
    ],
  },

  {
    id: "sc-g4x-u2",
    unitName: "岩石与土壤",
    grade: 4,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: "下列岩石中属于沉积岩的是（ ）。\nA. 花岗岩  B. 砂岩  C. 大理岩", answer: "B", difficulty: 2 },
      { type: "选择题", content: "土壤中最多的成分是（ ）。\nA. 空气  B. 水分  C. 矿物质", answer: "C", difficulty: 2 },
      { type: "判断题", content: "花岗岩很坚硬，不容易被划伤。（ ）", answer: "√", difficulty: 1 },
      { type: "判断题", content: "土壤是由岩石变化而来的。（ ）", answer: "√", difficulty: 1 },
      { type: "填空题", content: "常见的岩石有花岗岩、（ ）、（ ）和石灰岩等。", answer: "砂岩；大理岩（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: "土壤按含量从多到少排列为：矿物质、（ ）、（ ）、腐殖质。", answer: "水分；空气", difficulty: 2 },
      { type: "选择题", content: "下列哪种行为会破坏土壤？（ ）\nA. 种树  B. 乱砍滥伐  C. 轮作", answer: "B", difficulty: 1 },
      { type: "简答题", content: "请说出保护土壤的方法（至少两种）。", answer: "植树造林、合理使用化肥、减少乱砍滥伐、垃圾分类等。（答案不唯一）", difficulty: 2 },
      { type: "填空题", content: "岩石可以分为岩浆岩、（ ）和变质岩三大类。", answer: "沉积岩", difficulty: 2 },
      { type: "判断题", content: "所有的土壤都适合种植农作物。（ ）", answer: "×", difficulty: 2 }
    ],
  },

  // ==================== 语文 - 四年级上册 ====================
  {
    id: "cn-g4s-u1",
    unitName: "观潮",
    grade: 4,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\nguān cháo（ ）", answer: "观潮", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nlóng zhào（ ）", answer: "笼罩", difficulty: 1 },
      { type: "组词", content: "用\"潮\"字组两个词：（ ）、（ ）", answer: "潮水；潮汐（答案不唯一）", difficulty: 1 },
      { type: "选词填空", content: "选词填空：奔腾  沸腾\n只见东边水天相接的地方出现了一条白线，人群又（ ）起来。\n那浪越来越近，犹如千万匹白色战马（ ）而来。", answer: "沸腾；奔腾", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n浪潮越来越近，犹如千万匹白色战马齐头并进。\n________犹如________。", answer: "落叶纷纷飘落，犹如一只只蝴蝶翩翩起舞。（答案不唯一）", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"那条白线很快地向我们移来，逐渐拉长，变粗，横贯江面。\"\n\"那条白线\"指的是什么？\n答：____________________", answer: "“那条白线”指的是钱塘江大潮。", difficulty: 2 },
      { type: "修辞手法判断", content: "判断下列句子用了什么修辞手法：\n\"浪潮越来越近，犹如千万匹白色战马齐头并进。\"\n答：____________________", answer: "比喻", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"钱塘江大潮，自古以来被称为天下奇观。\"", answer: "原句没有语病。（此题为判断题）", difficulty: 2 },
      { type: "古诗文填空", content: "补充诗句：\n八月十八潮，壮观天下（ ）。\n鲲鹏水击三千里，组练长驱十万（ ）。", answer: "无；夫", difficulty: 3 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"霎时，潮头奔腾西去，可是余波还在漫天卷地般涌来，江面上依旧风号浪吼。\"\n\"霎时\"是什么意思？\n答：____________________", answer: "“霎时”的意思是极短的时间，一会儿。", difficulty: 2 }
    ],
  },

  {
    id: "cn-g4s-u2",
    unitName: "走月亮",
    grade: 4,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\ntián sǒng（ ）", answer: "田埂", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nshuì lián（ ）", answer: "睡莲", difficulty: 1 },
      { type: "组词", content: "用\"淘\"字组两个词：（ ）、（ ）", answer: "淘气；淘洗（答案不唯一）", difficulty: 1 },
      { type: "选词填空", content: "选词填空：柔和  柔软\n月光是那样（ ），照亮了高高的点苍山。\n草地上铺着（ ）的青苔。", answer: "柔和；柔软", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n月光照亮了高高的点苍山，照亮了村头的大青树，也照亮了村间的大道和小路。\n________照亮了________，照亮了________。", answer: "阳光照亮了田野，照亮了河流，也照亮了我们的校园。（答案不唯一）", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"秋天的夜晚，月亮升起来了，从洱海那边升起来了。\"\n月亮是从哪里升起来的？\n答：____________________", answer: "月亮是从洱海那边升起来的。", difficulty: 1 },
      { type: "修辞手法判断", content: "判断下列句子用了什么修辞手法：\n\"月盘是那样明亮，月光是那样柔和。\"\n答：____________________", answer: "排比（反复）", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"走月亮，让我看到了美丽的景色。\"", answer: "去掉“走月亮”前面的逗号，改为：走月亮让我看到了美丽的景色。或：在“走月亮”前加“和妈妈”。", difficulty: 3 },
      { type: "古诗文填空", content: "补充诗句：\n床前明月光，疑是地上（ ）。\n举头望明月，低头思（ ）。", answer: "霜；故乡", difficulty: 1 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"细细的溪水，流着山草和野花的香味，流着月光。\"\n溪水流着什么？\n答：____________________", answer: "溪水流着山草和野花的香味，流着月光。", difficulty: 2 }
    ],
  },

  {
    id: "cn-g4s-u3",
    unitName: "现代诗二首",
    grade: 4,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\nluò yè（ ）", answer: "落叶", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nfán xīng（ ）", answer: "繁星", difficulty: 1 },
      { type: "组词", content: "用\"巢\"字组两个词：（ ）、（ ）", answer: "鸟巢；巢穴（答案不唯一）", difficulty: 1 },
      { type: "选词填空", content: "选词填空：归巢  回家\n鸟儿（ ）了，在叽叽喳喳地聊着天。\n天黑了，小朋友们都（ ）了。", answer: "归巢；回家", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n\"秋天的声音，在每一片叶子里，在每一朵花里，在每一滴水里。\"\n________在________，在________，在________。", answer: "春天的气息在每一棵小草里，在每一朵鲜花里，在每一缕微风中。（答案不唯一）", difficulty: 3 },
      { type: "阅读理解", content: "阅读诗歌回答问题：\n\"花牛在草地里坐，压扁了一穗剪秋罗。\"\n花牛在做什么？\n答：____________________", answer: "花牛在草地里坐着。", difficulty: 1 },
      { type: "修辞手法判断", content: "判断下列句子用了什么修辞手法：\n\"花牛在草地里眠，白云霸占了半个天。\"\n答：____________________", answer: "拟人", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"现代诗很优美，我喜欢读现代诗和古诗。\"", answer: "原句没有语病。", difficulty: 2 },
      { type: "古诗文填空", content: "补充诗句：\n《繁星》（七一）\n这些事——是永不漫灭的（ ）：月明的（ ），藤萝的（ ），母亲的膝上。", answer: "回忆；园中；叶下", difficulty: 2 },
      { type: "阅读理解", content: "阅读诗歌回答问题：\n\"花牛在草地里走，小尾巴甩得滴溜溜。\"\n花牛的小尾巴怎么样？\n答：____________________", answer: "花牛的小尾巴甩得滴溜溜。", difficulty: 1 }
    ],
  },

  // ==================== 语文 - 四年级下册 ====================
  {
    id: "cn-g4x-u1",
    unitName: "古诗词三首",
    grade: 4,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "古诗文填空", content: "补充古诗：\n四时田园杂兴（其二十五）\n梅子金黄杏子肥，麦花雪白菜花（ ）。\n日长篱落无人过，惟有蜻蜓蛱蝶（ ）。", answer: "稀；飞", difficulty: 2 },
      { type: "古诗文填空", content: "补充古诗：\n宿新市徐公店\n篱落疏疏一径深，树头新绿未成（ ）。\n儿童急走追黄蝶，飞入菜花（ ）处寻。", answer: "阴；无", difficulty: 2 },
      { type: "古诗文填空", content: "补充古诗：\n清平乐·村居\n茅檐低小，溪上青青（ ）。\n醉里吴音相媚好，白发谁家（ ）媪？", answer: "草；翁", difficulty: 2 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nshū lí（ ）", answer: "疏篱", difficulty: 1 },
      { type: "组词", content: "用\"篱\"字组两个词：（ ）、（ ）", answer: "篱落；篱笆（答案不唯一）", difficulty: 1 },
      { type: "阅读理解", content: "阅读古诗回答问题：\n\"儿童急走追黄蝶，飞入菜花无处寻。\"\n儿童在做什么？为什么\"无处寻\"？\n答：____________________", answer: "儿童在追黄蝴蝶。因为蝴蝶飞入了黄色的菜花中，和菜花颜色一样，所以找不到。", difficulty: 2 },
      { type: "修辞手法判断", content: "判断下列诗句用了什么修辞手法：\n\"白发谁家翁媪？\"\n答：____________________", answer: "设问", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"我大概差不多把作业写完了。\"", answer: "去掉“大概”或“差不多”（语义重复）。", difficulty: 2 },
      { type: "选词填空", content: "选词填空：稀疏  繁密\n篱笆（ ），小路幽深。\n树叶（ ），遮住了阳光。", answer: "稀疏；繁密", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n\"最喜小儿亡赖，溪头卧剥莲蓬。\"\n用\"最喜……\"写一句话：\n____________________", answer: "最喜春天到来，满园的花儿竞相开放。（答案不唯一）", difficulty: 2 }
    ],
  },

  {
    id: "cn-g4x-u2",
    unitName: "乡下人家",
    grade: 4,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\ngòu chéng（ ）", answer: "构成", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nshuài lǐng（ ）", answer: "率领", difficulty: 1 },
      { type: "组词", content: "用\"饰\"字组两个词：（ ）、（ ）", answer: "装饰；修饰（答案不唯一）", difficulty: 1 },
      { type: "选词填空", content: "选词填空：独特  特别\n乡下人家的生活有一种（ ）的韵味。\n今天天气（ ）好。", answer: "独特；特别", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n\"几场春雨过后，到那里走走，常常会看见许多鲜嫩的笋，成群地从土里探出头来。\"\n________常常会________。", answer: "春天到了，到公园走走，常常会看见许多美丽的花朵竞相开放。（答案不唯一）", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"有些人家，还在门前的场地上种几株花，芍药、凤仙、鸡冠花，大丽菊，它们依着时令，顺序开放。\"\n门前种了哪些花？\n答：____________________", answer: "种了芍药、凤仙、鸡冠花和大丽菊。", difficulty: 1 },
      { type: "修辞手法判断", content: "判断下列句子用了什么修辞手法：\n\"几场春雨过后，到那里走走，常常会看见许多鲜嫩的笋，成群地从土里探出头来。\"\n答：____________________", answer: "拟人", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"乡下人家，虽然住着小小的房屋，但总爱在屋前搭一瓜架。\"", answer: "原句没有语病。", difficulty: 2 },
      { type: "古诗文填空", content: "补充诗句：\n昼出耘田夜绩麻，村庄儿女各当（ ）。\n童孙未解供耕织，也傍桑阴学种（ ）。", answer: "家；瓜", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"若是在夏天的傍晚出去散步，常常会瞧见乡下人家吃晚饭的情景。\"\n乡下人家在什么时候吃晚饭？\n答：____________________", answer: "在夏天的傍晚。", difficulty: 1 }
    ],
  },

  {
    id: "cn-g4x-u3",
    unitName: "纳米技术就在我们身边",
    grade: 4,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\nnà mǐ（ ）", answer: "纳米", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nxiāo fáng（ ）", answer: "消防", difficulty: 1 },
      { type: "组词", content: "用\"钢\"字组两个词：（ ）、（ ）", answer: "钢铁；钢琴（答案不唯一）", difficulty: 1 },
      { type: "选词填空", content: "选词填空：无能为力  神奇\n纳米技术非常（ ），可以让很多以前（ ）的事情变成可能。", answer: "神奇；无能为力", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n\"纳米技术就在我们身边。\"\n用\"就在我们身边\"写一句话：\n____________________", answer: "科学就在我们身边。（答案不唯一）", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"纳米技术是20世纪90年代出现的高新技术。\"\n纳米技术是什么时候出现的？\n答：____________________", answer: "纳米技术是20世纪90年代出现的高新技术。", difficulty: 1 },
      { type: "修辞手法判断", content: "判断下列句子用了什么修辞手法：\n\"纳米技术就在我们身边。\"\n答：____________________", answer: "没有使用修辞手法（陈述句）", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"纳米技术可以让人类的生活变得更方便和美好。\"", answer: "原句没有语病。", difficulty: 2 },
      { type: "古诗文填空", content: "补充诗句：\n不识庐山真面目，只缘身在此（ ）中。", answer: "山", difficulty: 1 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"纳米涂层具有杀菌和除臭功能。\"\n纳米涂层有什么功能？\n答：____________________", answer: "纳米涂层具有杀菌和除臭功能。", difficulty: 1 }
    ],
  },

  // ==================== 语文 - 五年级上册 ====================
  {
    id: "cn-g5s-u1",
    unitName: "白鹭",
    grade: 5,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\nbái lù（ ）", answer: "白鹭", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nxián shì（ ）", answer: "嫌弃", difficulty: 1 },
      { type: "组词", content: "用\"嵌\"字组两个词：（ ）、（ ）", answer: "镶嵌；嵌入（答案不唯一）", difficulty: 1 },
      { type: "选词填空", content: "选词填空：精巧  精美\n白鹭是一首（ ）的诗。\n这件工艺品非常（ ）。", answer: "精巧；精美", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n\"白鹭是一首精巧的诗。\"\n________是________。", answer: "荷花是一幅美丽的画。（答案不唯一）", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"白鹤太大而嫌生硬，即使如粉红的朱鹭或灰色的苍鹭，也觉得大了一些，而且太不寻常了。\"\n作者为什么说白鹤和朱鹭等不如白鹭？\n答：____________________", answer: "因为白鹤太大而嫌生硬，朱鹭和苍鹭也太不寻常了，不如白鹭大小适宜、自然优美。", difficulty: 2 },
      { type: "修辞手法判断", content: "判断下列句子用了什么修辞手法：\n\"白鹭是一首精巧的诗。\"\n答：____________________", answer: "比喻（暗喻）", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"白鹭实在是一首诗，一首韵在骨子里的散文诗。\"", answer: "原句没有语病。", difficulty: 2 },
      { type: "古诗文填空", content: "补充诗句：\n两个黄鹂鸣翠柳，一行（ ）上青天。", answer: "白鹭", difficulty: 1 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"晴天的清晨，每每看见它孤独地站立于小树的绝顶，看来像是不安稳，而它却很悠然。\"\n白鹭站在哪里？看起来怎样？\n答：____________________", answer: "白鹭站立于小树的绝顶，看起来像是不安稳，实际上却很悠然。", difficulty: 2 }
    ],
  },

  {
    id: "cn-g5s-u2",
    unitName: "落花生",
    grade: 5,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\nmǔ qīn（ ）", answer: "母亲", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\njiào huì（ ）", answer: "教诲", difficulty: 1 },
      { type: "组词", content: "用\"播\"字组两个词：（ ）、（ ）", answer: "播种；播放（答案不唯一）", difficulty: 1 },
      { type: "选词填空", content: "选词填空：爱慕  羡慕\n不要做只讲体面，而对别人没有（ ）的人。\n我很（ ）小明取得了好成绩。", answer: "好处；羡慕", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n\"所以你们要像花生，它虽然不好看，可是很有用。\"\n用\"虽然……可是……\"写一句话：\n____________________", answer: "虽然这道题很难，可是我还是做出来了。（答案不唯一）", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"父亲说：'花生的好处很多，有一样最可贵。它的果实埋在地里，不像桃子、石榴、苹果那样，把鲜红嫩绿的果实高高地挂在枝上。'\"\n花生最可贵的地方是什么？\n答：____________________", answer: "花生最可贵的地方是果实埋在地里，不张扬，朴实无华。", difficulty: 2 },
      { type: "修辞手法判断", content: "判断下列句子用了什么修辞手法：\n\"花生矮矮地长在地上，等到成熟了，也不能立刻分辨出来它有没有果实。\"\n答：____________________", answer: "没有使用修辞手法（对比）", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"大家都喜欢花生，因为花生很便宜，而且很好吃。\"", answer: "原句没有语病。", difficulty: 2 },
      { type: "古诗文填空", content: "补充诗句：\n春种一粒粟，秋收（ ）颗子。\n四海无闲田，农夫犹饿（ ）。", answer: "万；死", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文回答问题：\n课文借落花生告诉了我们什么道理？\n答：____________________", answer: "做人要做有用的人，不要做只讲体面而对别人没有好处的人。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g5s-u3",
    unitName: "桂花雨",
    grade: 5,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\nguì huā（ ）", answer: "桂花", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nchán rào（ ）", answer: "缠绕", difficulty: 1 },
      { type: "组词", content: "用\"缠\"字组两个词：（ ）、（ ）", answer: "缠绕；缠绵（答案不唯一）", difficulty: 1 },
      { type: "选词填空", content: "选词填空：欣赏  观赏\n母亲每天都要在院子里（ ）桂花。\n我们到公园去（ ）菊花展。", answer: "欣赏；观赏", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n\"桂花盛开的时候，不说香飘十里，至少前后左右十几家邻居，没有不浸在桂花香里的。\"\n用\"没有不……\"写一句话：\n____________________", answer: "听了这个好消息，同学们没有不高兴的。（答案不唯一）", difficulty: 3 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"摇花对我来说是件大事，我总是缠着母亲问：'妈，怎么还不摇桂花呢？'\"\n\"我\"为什么急着要摇桂花？\n答：____________________", answer: "因为“我”很喜欢桂花，摇下来的桂花可以做桂花糕、泡桂花茶，非常香。", difficulty: 2 },
      { type: "修辞手法判断", content: "判断下列句子用了什么修辞手法：\n\"全年，整个村子都浸在桂花的香气里。\"\n答：____________________", answer: "夸张", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"这里的桂花再香，也比不上家乡院子里的桂花。\"", answer: "原句没有语病。", difficulty: 2 },
      { type: "古诗文填空", content: "补充诗句：\n人闲桂花落，夜静春山（ ）。\n月出惊山鸟，时鸣春涧（ ）。", answer: "空；中", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文回答问题：\n\"于是，我又想起了在故乡童年时代的'摇花乐'，和那摇落的阵阵桂花雨。\"\n\"摇花乐\"指的是什么？\n答：____________________", answer: "“摇花乐”指的是小时候在故乡摇桂花树，桂花纷纷落下的快乐时光。", difficulty: 2 }
    ],
  },

  // ==================== 语文 - 五年级下册 ====================
  {
    id: "cn-g5x-u1",
    unitName: "古诗三首",
    grade: 5,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "古诗文填空", content: "补充古诗：\n四时田园杂兴（其三十一）\n昼出耘田夜绩麻，村庄儿女各当（ ）。\n童孙未解供耕织，也傍桑阴学种（ ）。", answer: "家；瓜", difficulty: 2 },
      { type: "古诗文填空", content: "补充古诗：\n稚子弄冰\n稚子金盆脱晓冰，彩丝穿取当银（ ）。\n敲成玉磬穿林响，忽作玻璃碎地（ ）。", answer: "钲；声", difficulty: 2 },
      { type: "古诗文填空", content: "补充古诗：\n村晚\n草满池塘水满陂，山衔落日浸寒（ ）。\n牧童归去横牛背，短笛无腔信口（ ）。", answer: "漪；吹", difficulty: 2 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nyún tián（ ）", answer: "耘田", difficulty: 1 },
      { type: "组词", content: "用\"昼\"字组两个词：（ ）、（ ）", answer: "白昼；昼夜（答案不唯一）", difficulty: 1 },
      { type: "阅读理解", content: "阅读古诗回答问题：\n\"童孙未解供耕织，也傍桑阴学种瓜。\"\n小孩子在做什么？表现了什么？\n答：____________________", answer: "小孩子虽然不懂耕织，但也在桑树阴下学着种瓜。表现了农村儿童的勤劳和天真可爱。", difficulty: 2 },
      { type: "修辞手法判断", content: "判断下列诗句用了什么修辞手法：\n\"山衔落日浸寒漪。\"\n答：____________________", answer: "拟人", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"牧童骑着牛，吹着笛子回家了。\"", answer: "原句没有语病。", difficulty: 2 },
      { type: "选词填空", content: "选词填空：稚子  儿童\n（ ）弄冰，天真可爱。\n（ ）散学归来早，忙趁东风放纸鸢。", answer: "稚子；儿童", difficulty: 2 },
      { type: "阅读理解", content: "阅读古诗回答问题：\n\"稚子金盆脱晓冰，彩丝穿取当银钲。\"\n小孩子把冰当成了什么？\n答：____________________", answer: "小孩子把冰当成了银钲（一种乐器）。", difficulty: 2 }
    ],
  },

  {
    id: "cn-g5x-u2",
    unitName: "祖父的园子",
    grade: 5,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\nchí nào（ ）", answer: "蝴蝶", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nyīng tao（ ）", answer: "樱桃", difficulty: 1 },
      { type: "组词", content: "用\"蚂\"字组两个词：（ ）、（ ）", answer: "蚂蚁；蚂蚱（答案不唯一）", difficulty: 1 },
      { type: "选词填空", content: "选词填空：随意  随便\n在祖父的园子里，（ ）地玩，想做什么就做什么。\n这道题不会做，不能（ ）猜答案。", answer: "随意；随便", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n\"花开了，就像睡醒了似的。鸟飞了，就像在天上逛似的。虫子叫了，就像虫子在说话似的。\"\n________，就像________似的。", answer: "树叶落了，就像蝴蝶飞舞似的。（答案不唯一）", difficulty: 3 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"祖父的园子是一幅明丽的漂亮的童话画。\"\n为什么说祖父的园子是童话画？\n答：____________________", answer: "因为园子里有各种各样的植物和昆虫，充满了生机和童趣，像童话一样美好。", difficulty: 2 },
      { type: "修辞手法判断", content: "判断下列句子用了什么修辞手法：\n\"花开了，就像睡醒了似的。\"\n答：____________________", answer: "拟人", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"花园里明晃晃的，红的红，绿的绿，新鲜漂亮。\"", answer: "原句没有语病。", difficulty: 2 },
      { type: "古诗文填空", content: "补充诗句：\n草铺横野六七里，笛弄晚风三四（ ）。\n归来饱饭黄昏后，不脱蓑衣卧月（ ）。", answer: "声；明", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文回答问题：\n'我'在祖父的园子里做了哪些事情？\n答：____________________", answer: "'我'在园子里栽花、拔草、种菜、铲地、摘黄瓜、追蜻蜓、采倭瓜花等。（答案不唯一）", difficulty: 2 }
    ],
  },

  {
    id: "cn-g5x-u3",
    unitName: "月是故乡明",
    grade: 5,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\nxiāng yì（ ）", answer: "乡谊", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nqī liáng（ ）", answer: "凄凉", difficulty: 1 },
      { type: "组词", content: "用\"萌\"字组两个词：（ ）、（ ）", answer: "萌发；萌芽（答案不唯一）", difficulty: 1 },
      { type: "选词填空", content: "选词填空：盼望  期望\n我（ ）着能早日回到故乡。\n父母对我充满了（ ）。", answer: "盼望；期望", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n\"每个人都有个故乡，每个人的故乡都有个月亮。人人都爱自己故乡的月亮。\"\n用\"人人都……\"写一句话：\n____________________", answer: "人人都爱自己的家乡。（答案不唯一）", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"然而，每逢望夜，一轮当空，月光闪耀于碧波之上，上下空蒙，一碧数顷。\"\n这段话描写了什么景色？\n答：____________________", answer: "描写了月亮当空、月光照耀在水面上的美丽景色。", difficulty: 2 },
      { type: "修辞手法判断", content: "判断下列句子用了什么修辞手法：\n\"山高月小，水落石出。\"\n答：____________________", answer: "对偶", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"我看了很多书，有《西游记》《水浒传》和四大名著。\"", answer: "去掉“和四大名著”（包含关系不能并列）。", difficulty: 3 },
      { type: "古诗文填空", content: "补充诗句：\n露从今夜白，月是故乡（ ）。\n（ ）明月何时照我还？", answer: "明；春风又绿江南岸", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文回答问题：\n\"月是故乡明\"表达了作者怎样的感情？\n答：____________________", answer: "表达了作者对故乡深深的思念和热爱之情。", difficulty: 2 }
    ],
  },

  // ==================== 语文 - 六年级上册 ====================
  {
    id: "cn-g6s-u1",
    unitName: "草原",
    grade: 6,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\nlǜ tǎn（ ）", answer: "绿毯", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nmǎ tí（ ）", answer: "马蹄", difficulty: 1 },
      { type: "组词", content: "用\"渲染\"的\"渲\"字组两个词：（ ）、（ ）", answer: "渲染；渲泄（答案不唯一）", difficulty: 1 },
      { type: "选词填空", content: "选词填空：洒脱  自然\n蒙古族同胞非常（ ）好客。\n草原上的风光十分（ ）。", answer: "洒脱；自然", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n\"那些小丘的线条是那么柔美，就像只用绿色渲染，不用墨线勾勒的中国画。\"\n________就像________。", answer: "西湖的水是那么清澈，就像一面巨大的镜子。（答案不唯一）", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"在天底下，一碧千里，而并不茫茫。\"\n\"一碧千里\"是什么意思？\n答：____________________", answer: "“一碧千里”的意思是一眼望去全部都是绿色，形容范围很广。", difficulty: 2 },
      { type: "修辞手法判断", content: "判断下列句子用了什么修辞手法：\n\"羊群一会儿上了小丘，一会儿又下来，走在哪里都像给无边的绿毯绣上了白色的大花。\"\n答：____________________", answer: "比喻", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"这次到草原去，我看到了一望无际的草原和清新的空气。\"", answer: "原句没有语病。", difficulty: 2 },
      { type: "古诗文填空", content: "补充诗句：\n敕勒川，阴山下，天似穹庐，笼盖四（ ）。\n天苍苍，野茫茫，风吹草低见牛（ ）。", answer: "野；羊", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文回答问题：\n\"蒙汉情深何忍别，天涯碧草话斜阳。\"\n这句话表达了什么感情？\n答：____________________", answer: "表达了蒙汉两族人民之间的深厚情谊和依依惜别之情。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g6s-u2",
    unitName: "丁香结",
    grade: 6,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\ndīng xiāng（ ）", answer: "丁香", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nyōu yǎ（ ）", answer: "幽雅", difficulty: 1 },
      { type: "组词", content: "用\"愁\"字组两个词：（ ）、（ ）", answer: "忧愁；愁闷（答案不唯一）", difficulty: 1 },
      { type: "选词填空", content: "选词填空：幽雅  优雅\n丁香花的香气令人感到（ ）。\n她举止（ ），深受大家喜欢。", answer: "幽雅；优雅", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n\"丁香结，这三个字给人许多想象。\"\n用\"……，这三个字给人许多想象\"写一句话：\n____________________", answer: "故乡情，这三个字给人许多想象。（答案不唯一）", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"今年的丁香花似乎开得格外茂盛，城里城外，都是一样。\"\n丁香花开得怎么样？\n答：____________________", answer: "今年的丁香花开得格外茂盛，城里城外都是一样。", difficulty: 1 },
      { type: "修辞手法判断", content: "判断下列句子用了什么修辞手法：\n\"小小的花苞圆圆的，鼓鼓的，恰如衣襟上的盘花扣。\"\n答：____________________", answer: "比喻", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"丁香结年年都有，因为丁香结象征着解不开的愁怨。\"", answer: "原句没有语病。", difficulty: 2 },
      { type: "古诗文填空", content: "补充诗句：\n芭蕉不展丁香结，同向春风各自（ ）。\n殷勤解却丁香结，纵放繁枝散（ ）香。", answer: "愁；诞", difficulty: 3 },
      { type: "阅读理解", content: "阅读课文回答问题：\n\"丁香结\"在课文中象征什么？\n答：____________________", answer: "“丁香结”象征着生活中解不开的愁怨和人生中遇到的困难与挫折。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g6s-u3",
    unitName: "古诗词三首",
    grade: 6,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "古诗文填空", content: "补充古诗：\n宿建德江\n移舟泊烟渚，日暮客愁（ ）。\n野旷天低树，江清月近（ ）。", answer: "新；人", difficulty: 2 },
      { type: "古诗文填空", content: "补充古诗：\n六月二十七日望湖楼醉书\n黑云翻墨未遮山，白雨跳珠乱入（ ）。\n卷地风来忽吹散，望湖楼下水如（ ）。", answer: "船；天", difficulty: 2 },
      { type: "古诗文填空", content: "补充古诗：\n西江月·夜行黄沙道中\n明月别枝惊鹊，清风半夜鸣（ ）。\n稻花香里说丰年，听取蛙声一（ ）。", answer: "蝉；片", difficulty: 2 },
      { type: "拼音写汉字", content: "看拼音写汉字：\njuàn lián（ ）", answer: "卷帘", difficulty: 1 },
      { type: "组词", content: "用\"渚\"字组两个词：（ ）、（ ）", answer: "汀渚；洲渚（答案不唯一）", difficulty: 2 },
      { type: "阅读理解", content: "阅读古诗回答问题：\n\"野旷天低树，江清月近人。\"\n\"月近人\"表达了诗人怎样的感情？\n答：____________________", answer: "表达了诗人旅途中的孤独寂寞和对故乡的思念之情。", difficulty: 3 },
      { type: "修辞手法判断", content: "判断下列诗句用了什么修辞手法：\n\"黑云翻墨未遮山，白雨跳珠乱入船。\"\n答：____________________", answer: "比喻", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"辛弃疾是宋代著名的诗人，他写了很多著名的词。\"", answer: "原句没有语病。", difficulty: 2 },
      { type: "选词填空", content: "选词填空：愁  愁绪\n日暮客（ ）新。\n丁香结象征着解不开的（ ）。", answer: "愁；愁绪", difficulty: 2 },
      { type: "阅读理解", content: "阅读古诗回答问题：\n\"稻花香里说丰年，听取蛙声一片。\"\n词人听到了什么？想到了什么？\n答：____________________", answer: "词人听到了蛙声一片，想到了今年是一个丰收年。", difficulty: 2 }
    ],
  },

  // ==================== 语文 - 六年级下册 ====================
  {
    id: "cn-g6x-u1",
    unitName: "北京的春节",
    grade: 6,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\nzhǎn lǎn（ ）", answer: "展览", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\njiào zi（ ）", answer: "饺子", difficulty: 1 },
      { type: "组词", content: "用\"腊\"字组两个词：（ ）、（ ）", answer: "腊月；腊肉（答案不唯一）", difficulty: 1 },
      { type: "选词填空", content: "选词填空：热闹  喧闹\n除夕夜，家家户户（ ）非凡。\n市场上（ ）的人群渐渐散去。", answer: "热闹；喧闹", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n\"这不是粥，而是小型的农业展览会。\"\n用\"不是……而是……\"写一句话：\n____________________", answer: "这不是浪费时间，而是在积累经验。（答案不唯一）", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"腊八这天，家家都熬腊八粥。粥是用各种米、各种豆、各种干果熬成的。\"\n腊八粥是用什么熬成的？\n答：____________________", answer: "腊八粥是用各种米、各种豆和各种干果熬成的。", difficulty: 1 },
      { type: "修辞手法判断", content: "判断下列句子用了什么修辞手法：\n\"这不是粥，而是小型的农业展览会。\"\n答：____________________", answer: "比喻", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"春节是我国最重要的传统节日之一。\"", answer: "原句没有语病。", difficulty: 2 },
      { type: "古诗文填空", content: "补充诗句：\n爆竹声中一岁除，春风送暖入屠（ ）。\n千门万户曈曈日，总把新桃换旧（ ）。", answer: "苏；符", difficulty: 1 },
      { type: "阅读理解", content: "阅读课文回答问题：\n课文中北京的春节从什么时候开始，到什么时候结束？\n答：____________________", answer: "从腊月初开始，到正月十九结束。", difficulty: 2 }
    ],
  },

  {
    id: "cn-g6x-u2",
    unitName: "腊八粥",
    grade: 6,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: "看拼音写汉字：\nzhǒu（ ）", answer: "粥", difficulty: 1 },
      { type: "拼音写汉字", content: "看拼音写汉字：\ntān chī（ ）", answer: "贪吃", difficulty: 1 },
      { type: "组词", content: "用\"熬\"字组两个词：（ ）、（ ）", answer: "熬粥；熬夜（答案不唯一）", difficulty: 1 },
      { type: "选词填空", content: "选词填空：叹气  叹息\n八儿（ ）着说：\"妈，什么时候才能熬好呢？\"\n他望着空空的碗，不由得（ ）。", answer: "叹气；叹息", difficulty: 2 },
      { type: "照样子写句子", content: "照样子写句子：\n\"初学喊爸爸的小孩子，会出门叫迎春回来的燕子，不会说话的婴儿，嗡嗡嗡的蜜蜂，甚至飘落的树叶，都感受到腊八粥的香甜。\"\n用\"甚至\"写一句话：\n____________________", answer: "大家都喜欢这本书，甚至老师也爱不释手。（答案不唯一）", difficulty: 2 },
      { type: "阅读理解", content: "阅读课文片段回答问题：\n\"住方家大院的八儿，今天喜得快要发疯了。\"\n八儿为什么\"喜得快要发疯了\"？\n答：____________________", answer: "因为今天是腊八节，可以吃到盼望已久的腊八粥。", difficulty: 2 },
      { type: "修辞手法判断", content: "判断下列句子用了什么修辞手法：\n\"初学喊爸爸的小孩子，会出门叫迎春回来的燕子，不会说话的婴儿，嗡嗡嗡的蜜蜂，甚至飘落的树叶，都感受到腊八粥的香甜。\"\n答：____________________", answer: "排比", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"腊八粥是用大米、小米、红枣、花生、栗子和白糖等熬成的。\"", answer: "原句没有语病。", difficulty: 2 },
      { type: "古诗文填空", content: "补充诗句：\n（ ）（ ）一粒粟，秋收万颗子。\n四海无闲田，农夫犹饿死。", answer: "春种", difficulty: 1 },
      { type: "阅读理解", content: "阅读课文回答问题：\n八儿是一个怎样的孩子？\n答：____________________", answer: "八儿是一个天真可爱、嘴馋、活泼的孩子。", difficulty: 2 }
    ],
  },

  {
    id: "cn-g6x-u3",
    unitName: "古诗三首",
    grade: 6,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "古诗文填空", content: "补充古诗：\n寒食\n春城无处不飞花，寒食东风御柳（ ）。\n日暮汉宫传蜡烛，轻烟散入五侯（ ）。", answer: "斜；家", difficulty: 2 },
      { type: "古诗文填空", content: "补充古诗：\n迢迢牵牛星\n迢迢牵牛星，皎皎河汉（ ）。\n纤纤擢素手，札札弄机（ ）。", answer: "女；杼", difficulty: 2 },
      { type: "古诗文填空", content: "补充古诗：\n十五夜望月\n中庭地白树栖鸦，冷露无声湿（ ）花。\n今夜月明人尽望，不知秋思落谁（ ）。", answer: "桂；家", difficulty: 2 },
      { type: "拼音写汉字", content: "看拼音写汉字：\nqī xī（ ）", answer: "七夕", difficulty: 1 },
      { type: "组词", content: "用\"栖\"字组两个词：（ ）、（ ）", answer: "栖息；栖身（答案不唯一）", difficulty: 2 },
      { type: "阅读理解", content: "阅读古诗回答问题：\n\"今夜月明人尽望，不知秋思落谁家。\"\n\"秋思\"指的是什么？\n答：____________________", answer: "“秋思”指的是中秋之夜对亲人的思念之情。", difficulty: 2 },
      { type: "修辞手法判断", content: "判断下列诗句用了什么修辞手法：\n\"迢迢牵牛星，皎皎河汉女。\"\n答：____________________", answer: "对偶", difficulty: 2 },
      { type: "修改病句", content: "修改病句：\n\"中秋节是我国的传统节日，人们有赏月和吃月饼的习惯。\"", answer: "原句没有语病。", difficulty: 2 },
      { type: "选词填空", content: "选词填空：望  看\n十五夜（ ）月。\n我（ ）见天上有许多星星。", answer: "望；看", difficulty: 1 },
      { type: "阅读理解", content: "阅读古诗回答问题：\n\"日暮汉宫传蜡烛，轻烟散入五侯家。\"\n这首诗描写了哪个节日的情景？\n答：____________________", answer: "描写了寒食节的情景。", difficulty: 2 }
    ],
  },

  // ==================== 英语 - 五年级上册 ====================
  {
    id: "en-g5s-u1",
    unitName: "What's he like?",
    grade: 5,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"old\"的意思是（ ）。\nA. 年轻的  B. 年老的  C. 高的", answer: "B", difficulty: 1 },
      { type: "单词选择", content: "\"kind\"的意思是（ ）。\nA. 严格的  B. 和蔼的  C. 聪明的", answer: "B", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nyoung —（ ）  funny —（ ）  strict —（ ）", answer: "年轻的；滑稽的；严格的", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n聪明的 —（ ）  有礼貌的 —（ ）  努力的 —（ ）", answer: "clever；polite；hard-working", difficulty: 2 },
      { type: "连词成句", content: "连词成句：\nis / he / What / like（ ? ）", answer: "What is he like?", difficulty: 1 },
      { type: "情景交际", content: "你想问\"她长什么样？\"，你应该说（ ）。\nA. What's she like?  B. What does she do?  C. Where is she?", answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: "用所给词的正确形式填空：\nMr. Jones ________ (be) tall and strong.", answer: "is", difficulty: 1 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: Who's your English teacher?\nB: Miss White.\nA: Is she kind?\nB: Yes, she is.\nWho is the English teacher?\n答：____________________", answer: "Miss White.", difficulty: 2 },
      { type: "情景交际", content: "你想说\"他又高又壮\"，你应该说（ ）。\nA. He is tall and strong.  B. She is tall and strong.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"shy\"的意思是（ ）。\nA. 害羞的  B. 友好的  C. 安静的", answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g5s-u2",
    unitName: "My week",
    grade: 5,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"Monday\"的意思是（ ）。\nA. 星期一  B. 星期二  C. 星期三", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"Wednesday\"的意思是（ ）。\nA. 星期一  B. 星期三  C. 星期五", answer: "B", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nTuesday —（ ）  Thursday —（ ）  Friday —（ ）", answer: "星期二；星期四；星期五", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n星期六 —（ ）  星期日 —（ ）  周末 —（ ）", answer: "Saturday；Sunday；weekend", difficulty: 1 },
      { type: "连词成句", content: "连词成句：\ndo / you / What / have / on / Mondays（ ? ）", answer: "What do you have on Mondays?", difficulty: 2 },
      { type: "情景交际", content: "你想问\"你星期一有什么课？\"，你应该说（ ）。\nA. What do you have on Mondays?  B. What day is it today?", answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: "用所给词的正确形式填空：\nI often ________ (read) books on weekends.", answer: "read", difficulty: 1 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: What day is it today?\nB: It's Wednesday.\nA: What do you have on Wednesdays?\nB: I have Chinese, English and music.\nWhat classes does B have on Wednesdays?\n答：____________________", answer: "Chinese, English and music.", difficulty: 2 },
      { type: "情景交际", content: "你想说\"我经常在周末做作业\"，你应该说（ ）。\nA. I often do homework on weekends.  B. I often play football on weekends.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"weekend\"的意思是（ ）。\nA. 工作日  B. 周末  C. 假期", answer: "B", difficulty: 1 }
    ],
  },

  {
    id: "en-g5s-u3",
    unitName: "What would you like?",
    grade: 5,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"sandwich\"的意思是（ ）。\nA. 汉堡包  B. 三明治  C. 面条", answer: "B", difficulty: 1 },
      { type: "单词选择", content: "\"thirsty\"的意思是（ ）。\nA. 饥饿的  B. 口渴的  C. 疲倦的", answer: "B", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nsalad —（ ）  hamburger —（ ）  ice cream —（ ）", answer: "沙拉；汉堡包；冰淇淋", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n新鲜的 —（ ）  健康的 —（ ）  美味的 —（ ）", answer: "fresh；healthy；delicious", difficulty: 2 },
      { type: "连词成句", content: "连词成句：\nwould / What / you / like（ ? ）", answer: "What would you like?", difficulty: 1 },
      { type: "情景交际", content: "在餐厅，服务员问你想要什么，你应该回答（ ）。\nA. I'd like some beef, please.  B. I like beef.", answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: "用所给词的正确形式填空：\nI'd like some ________ (juice).", answer: "juice", difficulty: 1 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: What would you like to eat?\nB: I'd like a sandwich, please.\nA: What would you like to drink?\nB: I'd like some milk.\nWhat would B like to eat?\n答：____________________", answer: "A sandwich.", difficulty: 2 },
      { type: "情景交际", content: "你想说\"我最喜欢的食物是鱼\"，你应该说（ ）。\nA. My favourite food is fish.  B. I'd like some fish.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"favourite\"的意思是（ ）。\nA. 最喜欢的  B. 不喜欢的  C. 普通的", answer: "A", difficulty: 1 }
    ],
  },

  // ==================== 英语 - 五年级下册 ====================
  {
    id: "en-g5x-u1",
    unitName: "My day",
    grade: 5,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"eat breakfast\"的意思是（ ）。\nA. 吃早餐  B. 吃午餐  C. 吃晚餐", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"do morning exercises\"的意思是（ ）。\nA. 做作业  B. 做早操  C. 做运动", answer: "B", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\neat dinner —（ ）  go to school —（ ）  go to bed —（ ）", answer: "吃晚餐；去上学；去睡觉", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n做早操 —（ ）  上课 —（ ）  回家 —（ ）", answer: "do morning exercises；have class；go home", difficulty: 2 },
      { type: "连词成句", content: "连词成句：\nyou / When / do / breakfast / eat（ ? ）", answer: "When do you eat breakfast?", difficulty: 2 },
      { type: "情景交际", content: "你想问\"你什么时候起床？\"，你应该说（ ）。\nA. When do you get up?  B. What do you do?", answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: "用所给词的正确形式填空：\nI usually ________ (get) up at 6:30.", answer: "get", difficulty: 1 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: When do you get up?\nB: I get up at 6:00.\nA: What do you do at 7:00?\nB: I eat breakfast.\nWhen does B eat breakfast?\n答：____________________", answer: "At 7:00.", difficulty: 2 },
      { type: "情景交际", content: "你想说\"我通常在晚上9点睡觉\"，你应该说（ ）。\nA. I usually go to bed at 9:00 p.m.  B. I usually get up at 9:00 p.m.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"usually\"的意思是（ ）。\nA. 通常  B. 有时  C. 总是", answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g5x-u2",
    unitName: "My favourite season",
    grade: 5,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"spring\"的意思是（ ）。\nA. 夏天  B. 春天  C. 秋天", answer: "B", difficulty: 1 },
      { type: "单词选择", content: "\"winter\"的意思是（ ）。\nA. 春天  B. 秋天  C. 冬天", answer: "C", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nsummer —（ ）  autumn —（ ）  season —（ ）", answer: "夏天；秋天；季节", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n去游泳 —（ ）  堆雪人 —（ ）  放风筝 —（ ）", answer: "go swimming；make a snowman；fly kites", difficulty: 2 },
      { type: "连词成句", content: "连词成句：\nseason / Which / do / you / like / best（ ? ）", answer: "Which season do you like best?", difficulty: 2 },
      { type: "情景交际", content: "你想问\"你最喜欢哪个季节？\"，你应该说（ ）。\nA. Which season do you like best?  B. What's your favourite colour?", answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: "用所给词的正确形式填空：\nI like ________ (snow) in winter.", answer: "snow", difficulty: 2 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: Which season do you like best?\nB: I like summer best.\nA: Why?\nB: Because I can go swimming.\nWhy does B like summer?\n答：____________________", answer: "Because he/she can go swimming.", difficulty: 2 },
      { type: "情景交际", content: "你想说\"我喜欢春天，因为可以放风筝\"，你应该说（ ）。\nA. I like spring because I can fly kites.  B. I like winter because I can make a snowman.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"pick apples\"的意思是（ ）。\nA. 摘苹果  B. 吃苹果  C. 买苹果", answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g5x-u3",
    unitName: "Whose dog is it?",
    grade: 5,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"climbing\"的意思是（ ）。\nA. 跑步  B. 攀爬  C. 跳跃", answer: "B", difficulty: 1 },
      { type: "单词选择", content: "\"eating\"的意思是（ ）。\nA. 喝  B. 吃  C. 睡", answer: "B", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\njumping —（ ）  drinking —（ ）  sleeping —（ ）", answer: "跳跃；喝水；睡觉", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n玩耍 —（ ）  攀爬 —（ ）  游泳 —（ ）", answer: "playing；climbing；swimming", difficulty: 2 },
      { type: "连词成句", content: "连词成句：\ndog / Whose / it / is（ ? ）", answer: "Whose dog is it?", difficulty: 1 },
      { type: "情景交际", content: "你想问\"这是谁的狗？\"，你应该说（ ）。\nA. Whose dog is this?  B. What is this?", answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: "用所给词的正确形式填空：\nLook! The cat ________ (sleep) under the tree.", answer: "is sleeping", difficulty: 2 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: Whose dog is it?\nB: It's Mike's.\nA: What is the dog doing?\nB: It's running.\nWhose dog is it?\n答：____________________", answer: "It's Mike's.", difficulty: 2 },
      { type: "情景交际", content: "你想说\"兔子在跳\"，你应该说（ ）。\nA. The rabbit is jumping.  B. The rabbit is running.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"mine\"的意思是（ ）。\nA. 我的  B. 你的  C. 他的", answer: "A", difficulty: 1 }
    ],
  },

  // ==================== 英语 - 六年级上册 ====================
  {
    id: "en-g6s-u1",
    unitName: "How can I get there?",
    grade: 6,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"science museum\"的意思是（ ）。\nA. 科学博物馆  B. 图书馆  C. 邮局", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"post office\"的意思是（ ）。\nA. 医院  B. 邮局  C. 书店", answer: "B", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nhospital —（ ）  cinema —（ ）  bookstore —（ ）", answer: "医院；电影院；书店", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n左转 —（ ）  右转 —（ ）  直走 —（ ）", answer: "turn left；turn right；go straight", difficulty: 2 },
      { type: "连词成句", content: "连词成句：\nI / How / can / get / there（ ? ）", answer: "How can I get there?", difficulty: 1 },
      { type: "情景交际", content: "你想问\"我怎么才能到那里？\"，你应该说（ ）。\nA. How can I get there?  B. Where is it?", answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: "用所给词的正确形式填空：\nTurn left at the ________ (two) traffic lights.", answer: "second", difficulty: 2 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: Excuse me, where is the cinema?\nB: It's next to the bookstore.\nA: How can I get there?\nB: Turn left at the school. Then go straight.\nWhere is the cinema?\n答：____________________", answer: "It's next to the bookstore.", difficulty: 2 },
      { type: "情景交际", content: "你想说\"在医院左转\"，你应该说（ ）。\nA. Turn left at the hospital.  B. Turn right at the hospital.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"crossing\"的意思是（ ）。\nA. 十字路口  B. 路灯  C. 斑马线", answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g6s-u2",
    unitName: "My weekend plan",
    grade: 6,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"visit\"的意思是（ ）。\nA. 参观  B. 离开  C. 到达", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"trip\"的意思是（ ）。\nA. 旅行  B. 聚会  C. 比赛", answer: "A", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nsupermarket —（ ）  evening —（ ）  tonight —（ ）", answer: "超市；晚上；今晚", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n下周 —（ ）  看电影 —（ ）  去旅行 —（ ）", answer: "next week；see a film；take a trip", difficulty: 2 },
      { type: "连词成句", content: "连词成句：\nare / What / you / going / to / do（ ? ）", answer: "What are you going to do?", difficulty: 2 },
      { type: "情景交际", content: "你想问\"你打算做什么？\"，你应该说（ ）。\nA. What are you going to do?  B. What do you do?", answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: "用所给词的正确形式填空：\nI ________ (visit) my grandparents this weekend.", answer: "am going to visit / will visit", difficulty: 2 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: What are you going to do tomorrow?\nB: I'm going to see a film.\nA: Where are you going?\nB: To the cinema.\nWhat is B going to do tomorrow?\n答：____________________", answer: "He/She is going to see a film.", difficulty: 2 },
      { type: "情景交际", content: "你想说\"我打算这周末去超市\"，你应该说（ ）。\nA. I'm going to the supermarket this weekend.  B. I go to the supermarket every weekend.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"dictionary\"的意思是（ ）。\nA. 字典  B. 漫画书  C. 故事书", answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g6s-u3",
    unitName: "I have a pen pal",
    grade: 6,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"hobby\"的意思是（ ）。\nA. 爱好  B. 工作  C. 家庭", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"jasmine\"的意思是（ ）。\nA. 玫瑰  B. 茉莉花  C. 百合花", answer: "B", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\npen pal —（ ）  idea —（ ）  hiking —（ ）", answer: "笔友；主意；远足", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n唱歌 —（ ）  跳舞 —（ ）  读故事 —（ ）", answer: "singing；dancing；reading stories", difficulty: 2 },
      { type: "连词成句", content: "连词成句：\ndoes / he / What / do（ ? ）", answer: "What does he do?", difficulty: 1 },
      { type: "情景交际", content: "你想问\"他的爱好是什么？\"，你应该说（ ）。\nA. What are his hobbies?  B. What does he like?", answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: "用所给词的正确形式填空：\nHe likes ________ (cook) Chinese food.", answer: "cooking", difficulty: 2 },
      { type: "阅读理解", content: "阅读短文回答问题：\n\"My pen pal is Peter. He lives in Australia. He likes reading stories and doing kung fu.\"\nWhere does Peter live?\n答：____________________", answer: "He lives in Australia.", difficulty: 2 },
      { type: "情景交际", content: "你想说\"他住在悉尼\"，你应该说（ ）。\nA. He lives in Sydney.  B. He is from Sydney.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"also\"的意思是（ ）。\nA. 也  B. 不  C. 非常", answer: "A", difficulty: 1 }
    ],
  },

  // ==================== 英语 - 六年级下册 ====================
  {
    id: "en-g6x-u1",
    unitName: "How tall are you?",
    grade: 6,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"taller\"的意思是（ ）。\nA. 更矮的  B. 更高的  C. 更胖的", answer: "B", difficulty: 1 },
      { type: "单词选择", content: "\"heavier\"的意思是（ ）。\nA. 更轻的  B. 更瘦的  C. 更重的", answer: "C", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nshorter —（ ）  longer —（ ）  thinner —（ ）", answer: "更矮的；更长的；更瘦的", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n更大的 —（ ）  更小的 —（ ）  更强壮的 —（ ）", answer: "bigger；smaller；stronger", difficulty: 2 },
      { type: "连词成句", content: "连词成句：\ntall / How / are / you（ ? ）", answer: "How tall are you?", difficulty: 1 },
      { type: "情景交际", content: "你想问\"你有多高？\"，你应该说（ ）。\nA. How tall are you?  B. How old are you?", answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: "用所给词的正确形式填空：\nI am ________ (tall) than my brother.", answer: "taller", difficulty: 2 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: How tall are you?\nB: I'm 1.65 metres.\nA: I'm 1.60 metres. You are taller than me.\nWho is taller?\n答：____________________", answer: "B is taller.", difficulty: 2 },
      { type: "情景交际", content: "你想说\"我的手比你的大\"，你应该说（ ）。\nA. My hands are bigger than yours.  B. My hands are smaller than yours.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"dinosaur\"的意思是（ ）。\nA. 大象  B. 恐龙  C. 长颈鹿", answer: "B", difficulty: 1 }
    ],
  },

  {
    id: "en-g6x-u2",
    unitName: "Last weekend",
    grade: 6,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"watched TV\"的意思是（ ）。\nA. 看电影  B. 看电视  C. 看书", answer: "B", difficulty: 1 },
      { type: "单词选择", content: "\"washed clothes\"的意思是（ ）。\nA. 洗衣服  B. 洗碗  C. 拖地", answer: "A", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nstayed at home —（ ）  cleaned the room —（ ）  had a cold —（ ）", answer: "待在家里；打扫房间；感冒了", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n看电影 —（ ）  读书 —（ ）  睡觉 —（ ）", answer: "saw a film；read a book；slept", difficulty: 2 },
      { type: "连词成句", content: "连词成句：\ndid / What / you / do / weekend / last（ ? ）", answer: "What did you do last weekend?", difficulty: 2 },
      { type: "情景交际", content: "你想问\"你上周末做了什么？\"，你应该说（ ）。\nA. What did you do last weekend?  B. What do you do?", answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: "用所给词的正确形式填空：\nI ________ (watch) TV last night.", answer: "watched", difficulty: 2 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: How was your weekend?\nB: It was good.\nA: What did you do?\nB: I stayed at home and read a book.\nWhat did B do last weekend?\n答：____________________", answer: "He/She stayed at home and read a book.", difficulty: 2 },
      { type: "情景交际", content: "你想说\"我昨天感冒了\"，你应该说（ ）。\nA. I had a cold yesterday.  B. I have a cold today.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"yesterday\"的意思是（ ）。\nA. 今天  B. 昨天  C. 明天", answer: "B", difficulty: 1 }
    ],
  },

  {
    id: "en-g6x-u3",
    unitName: "Where did you go?",
    grade: 6,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: "\"went swimming\"的意思是（ ）。\nA. 去游泳  B. 去钓鱼  C. 去购物", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"took pictures\"的意思是（ ）。\nA. 画画  B. 拍照  C. 写字", answer: "B", difficulty: 1 },
      { type: "英汉互译", content: "将下列英文翻译成中文：\nbought gifts —（ ）  ate good food —（ ）  went camping —（ ）", answer: "买礼物；吃美食；去露营", difficulty: 1 },
      { type: "英汉互译", content: "将下列中文翻译成英文：\n去海滩 —（ ）  骑马 —（ ）  滑冰 —（ ）", answer: "went to the beach；rode a horse；went ice-skating", difficulty: 2 },
      { type: "连词成句", content: "连词成句：\nyou / Where / go / did / yesterday（ ? ）", answer: "Where did you go yesterday?", difficulty: 2 },
      { type: "情景交际", content: "你想问\"你昨天去哪里了？\"，你应该说（ ）。\nA. Where did you go yesterday?  B. Where are you going?", answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: "用所给词的正确形式填空：\nI ________ (go) to Beijing last summer holiday.", answer: "went", difficulty: 2 },
      { type: "阅读理解", content: "阅读对话回答问题：\nA: Where did you go over the winter holiday?\nB: I went to Sanya.\nA: What did you do there?\nB: I went swimming and took lots of pictures.\nWhere did B go over the winter holiday?\n答：____________________", answer: "He/She went to Sanya.", difficulty: 2 },
      { type: "情景交际", content: "你想说\"我拍了很多照片\"，你应该说（ ）。\nA. I took lots of pictures.  B. I take lots of pictures.", answer: "A", difficulty: 1 },
      { type: "单词选择", content: "\"beach\"的意思是（ ）。\nA. 海滩  B. 山  C. 森林", answer: "A", difficulty: 1 }
    ],
  },

  // ==================== 科学 - 五年级上册 ====================
  {
    id: "sc-g5s-u1",
    unitName: "光",
    grade: 5,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: "光在空气中是以（ ）形式传播的。\nA. 曲线  B. 直线  C. 波浪线", answer: "B", difficulty: 1 },
      { type: "选择题", content: "下列物体中属于光源的是（ ）。\nA. 月亮  B. 镜子  C. 太阳", answer: "C", difficulty: 1 },
      { type: "判断题", content: "光的速度比声音的速度快。（ ）", answer: "√", difficulty: 1 },
      { type: "判断题", content: "月亮是光源。（ ）", answer: "×", difficulty: 1 },
      { type: "填空题", content: "光从空气进入水中时会发生（ ）现象。", answer: "折射", difficulty: 2 },
      { type: "填空题", content: "光遇到物体表面会被（ ）回来，这种现象叫做光的反射。", answer: "反射", difficulty: 1 },
      { type: "选择题", content: "下列哪种现象是光的折射？（ ）\nA. 水中筷子看起来弯了  B. 镜子中的像  C. 影子的形成", answer: "A", difficulty: 2 },
      { type: "简答题", content: "请说出彩虹是怎样形成的。", answer: "太阳光经过空气中的水滴折射和反射后，分解成七种颜色的光，形成彩虹。", difficulty: 3 },
      { type: "实验探究题", content: "小明做了一个实验：把一根铅笔放入装满水的玻璃杯中，从侧面观察铅笔。他看到了什么现象？这是什么原理？\n答：____________________", answer: "他看到铅笔在水面处好像折断了。这是光的折射原理。", difficulty: 2 },
      { type: "填空题", content: "光是由（ ）种颜色组成的。", answer: "七", difficulty: 1 }
    ],
  },

  {
    id: "sc-g5s-u2",
    unitName: "地球表面及其变化",
    grade: 5,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: "地球表面大部分被（ ）覆盖。\nA. 陆地  B. 海洋  C. 冰川", answer: "B", difficulty: 1 },
      { type: "选择题", content: "下列地形中海拔最高的是（ ）。\nA. 平原  B. 高原  C. 山地", answer: "C", difficulty: 1 },
      { type: "判断题", content: "地球表面的地形是永远不变的。（ ）", answer: "×", difficulty: 1 },
      { type: "判断题", content: "地震和火山喷发会改变地球表面的地形。（ ）", answer: "√", difficulty: 1 },
      { type: "填空题", content: "地球表面的主要地形有山地、高原、平原、（ ）和（ ）。", answer: "盆地；丘陵", difficulty: 2 },
      { type: "填空题", content: "地球内部由外到内分为地壳、（ ）和地核三层。", answer: "地幔", difficulty: 2 },
      { type: "选择题", content: "下列哪种力量会缓慢改变地球表面？（ ）\nA. 火山喷发  B. 风力侵蚀  C. 地震", answer: "B", difficulty: 2 },
      { type: "简答题", content: "请说出两种改变地球表面的力量。", answer: "地震、火山喷发、风化作用、侵蚀作用、沉积作用等。（答案不唯一）", difficulty: 2 },
      { type: "实验探究题", content: "在模拟地震的实验中，我们用多层泡沫板叠放，从两侧向中间挤压，观察到了什么现象？\n答：____________________", answer: "泡沫板会弯曲、隆起甚至断裂，模拟了地震时地壳的运动。", difficulty: 2 },
      { type: "填空题", content: "地球的陆地面积约占地球总面积的（ ）%。", answer: "29", difficulty: 2 }
    ],
  },

  {
    id: "sc-g5s-u3",
    unitName: "计量时间",
    grade: 5,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: "古代人们最早利用（ ）来计时。\nA. 钟表  B. 太阳  C. 沙漏", answer: "B", difficulty: 1 },
      { type: "选择题", content: "下列计时工具中，利用水来计时的是（ ）。\nA. 日晷  B. 沙漏  C. 水钟", answer: "C", difficulty: 1 },
      { type: "判断题", content: "日晷在阴天也能正常使用。（ ）", answer: "×", difficulty: 1 },
      { type: "判断题", content: "摆钟是利用摆的等时性来计时的。（ ）", answer: "√", difficulty: 2 },
      { type: "填空题", content: "古代的计时工具有日晷、（ ）、水钟和（ ）等。", answer: "沙漏；燃香（答案不唯一）", difficulty: 2 },
      { type: "填空题", content: "一分钟等于（ ）秒。", answer: "60", difficulty: 1 },
      { type: "选择题", content: "摆的快慢与（ ）有关。\nA. 摆锤重量  B. 摆线长度  C. 摆动幅度", answer: "B", difficulty: 2 },
      { type: "简答题", content: "请说出日晷的计时原理。", answer: "日晷利用太阳光照射在晷针上产生的影子来指示时间，影子随太阳位置变化而移动。", difficulty: 2 },
      { type: "实验探究题", content: "小明做了一个摆，发现它每分钟摆动30次。他想让摆动加快，应该怎样调整？\n答：____________________", answer: "应该缩短摆线的长度，摆线越短，摆动越快。", difficulty: 3 },
      { type: "填空题", content: "钟表上时针走一圈是（ ）小时。", answer: "12", difficulty: 1 }
    ],
  },

  // ==================== 科学 - 五年级下册 ====================
  {
    id: "sc-g5x-u1",
    unitName: "生物与环境",
    grade: 5,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: "绿豆种子发芽需要的条件是（ ）。\nA. 阳光、土壤  B. 水分、空气、适宜温度  C. 肥料、阳光", answer: "B", difficulty: 1 },
      { type: "选择题", content: "下列食物链正确的是（ ）。\nA. 草→兔→鹰  B. 鹰→兔→草  C. 兔→草→鹰", answer: "A", difficulty: 2 },
      { type: "判断题", content: "植物的生长不需要阳光。（ ）", answer: "×", difficulty: 1 },
      { type: "判断题", content: "同一种生物在不同环境中，形态可能不同。（ ）", answer: "√", difficulty: 2 },
      { type: "填空题", content: "食物链通常从（ ）开始，到凶猛的（ ）结束。", answer: "绿色植物；肉食动物", difficulty: 2 },
      { type: "填空题", content: "生物与环境相互（ ）、相互（ ）。", answer: "依存；影响", difficulty: 2 },
      { type: "选择题", content: "仙人掌的叶子变成刺是为了（ ）。\nA. 减少水分蒸发  B. 防止被动物吃  C. 进行光合作用", answer: "A", difficulty: 2 },
      { type: "简答题", content: "请说出植物适应环境的两个例子。", answer: "仙人掌叶子变成刺减少水分蒸发；浮萍有气囊能浮在水面；蒲公英种子有绒毛能随风传播等。（答案不唯一）", difficulty: 2 },
      { type: "实验探究题", content: "小明把绿豆种子放在不同环境中观察发芽情况：一组有水、有空气、温度适宜；另一组没有水。结果会怎样？\n答：____________________", answer: "有水、有空气、温度适宜的一组绿豆种子会发芽，没有水的一组不会发芽。", difficulty: 2 },
      { type: "填空题", content: "动物适应环境的方式有冬眠、（ ）、保护色等。", answer: "迁徙", difficulty: 1 }
    ],
  },

  {
    id: "sc-g5x-u2",
    unitName: "船的研究",
    grade: 5,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: "同样重的物体，做成（ ）形状受到的浮力最大。\nA. 实心球  B. 空心船形  C. 正方体", answer: "B", difficulty: 1 },
      { type: "选择题", content: "钢铁做的船能浮在水面上是因为（ ）。\nA. 钢铁比水轻  B. 船是空心的，排开的水量大  C. 船有发动机", answer: "B", difficulty: 2 },
      { type: "判断题", content: "物体在水中受到向上的浮力。（ ）", answer: "√", difficulty: 1 },
      { type: "判断题", content: "船的载重量与船的体积无关。（ ）", answer: "×", difficulty: 1 },
      { type: "填空题", content: "船的发展经历了独木舟、（ ）、蒸汽船和现代轮船等阶段。", answer: "帆船（或摇橹木船）", difficulty: 2 },
      { type: "填空题", content: "相同重量的橡皮泥，做成（ ）的形状能装载更多的货物。", answer: "船形（或空心碗形）", difficulty: 2 },
      { type: "选择题", content: "下列哪种方法可以使船更稳定？（ ）\nA. 把船做得很高  B. 把船底做得很宽  C. 减少船的重量", answer: "B", difficulty: 2 },
      { type: "简答题", content: "请说出使船浮在水面上的原理。", answer: "船做成空心形状后，排开的水量增大，受到的浮力增大，当浮力大于船的重力时，船就能浮在水面上。", difficulty: 3 },
      { type: "实验探究题", content: "小明用橡皮泥做船，第一次做成实心球沉入水中，第二次做成船形浮在了水面上。这说明什么？\n答：____________________", answer: "这说明改变物体的形状可以改变它受到的浮力，做成空心船形能增大排开的水量，从而增大浮力。", difficulty: 2 },
      { type: "填空题", content: "现代船的动力来源有风力和（ ）等。", answer: "发动机（或电力）", difficulty: 1 }
    ],
  },

  {
    id: "sc-g5x-u3",
    unitName: "环境与我们",
    grade: 5,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: "下列行为中有利于保护环境的是（ ）。\nA. 随意丢弃塑料袋  B. 垃圾分类回收  C. 乱砍滥伐", answer: "B", difficulty: 1 },
      { type: "选择题", content: "下列能源中属于可再生能源的是（ ）。\nA. 煤  B. 石油  C. 太阳能", answer: "C", difficulty: 1 },
      { type: "判断题", content: "地球上的水资源是取之不尽的。（ ）", answer: "×", difficulty: 1 },
      { type: "判断题", content: "温室效应会导致全球气候变暖。（ ）", answer: "√", difficulty: 1 },
      { type: "填空题", content: "垃圾处理的方法有填埋、（ ）和回收利用。", answer: "焚烧", difficulty: 2 },
      { type: "填空题", content: "减少空气污染的方法有少开私家车、（ ）、使用清洁能源等。", answer: "多植树造林", difficulty: 2 },
      { type: "选择题", content: "下列垃圾中属于可回收物的是（ ）。\nA. 废电池  B. 废纸  C. 剩饭", answer: "B", difficulty: 1 },
      { type: "简答题", content: "请说出三种保护环境的方法。", answer: "垃圾分类、节约用水、少用塑料袋、多植树、使用清洁能源等。（答案不唯一）", difficulty: 2 },
      { type: "实验探究题", content: "小明做了一个对比实验：在两个密封袋中各放一块面包，一个袋中加干燥剂，另一个不加。一周后观察，哪个面包更容易发霉？为什么？\n答：____________________", answer: "不加干燥剂的面包更容易发霉，因为霉菌生长需要水分，干燥的环境不利于霉菌生长。", difficulty: 2 },
      { type: "填空题", content: "地球上的淡水资源非常（ ），我们要节约用水。", answer: "有限（或稀少）", difficulty: 1 }
    ],
  },

  // ==================== 科学 - 六年级上册 ====================
  {
    id: "sc-g6s-u1",
    unitName: "微小世界",
    grade: 6,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: "下列工具中能放大物体的是（ ）。\nA. 平面镜  B. 放大镜  C. 哈哈镜", answer: "B", difficulty: 1 },
      { type: "选择题", content: "放大镜的镜片特点是（ ）。\nA. 中间厚边缘薄  B. 中间薄边缘厚  C. 一样厚", answer: "A", difficulty: 1 },
      { type: "判断题", content: "肉眼能看到所有的微小物体。（ ）", answer: "×", difficulty: 1 },
      { type: "判断题", content: "列文虎克发明了世界上第一台显微镜。（ ）", answer: "×", difficulty: 2 },
      { type: "填空题", content: "放大镜又叫（ ）镜，它的特点是透明、（ ）。", answer: "凸透；中间厚边缘薄", difficulty: 2 },
      { type: "填空题", content: "显微镜主要由目镜和（ ）组成，能将物体放大很多倍。", answer: "物镜", difficulty: 1 },
      { type: "选择题", content: "下列生物中属于微生物的是（ ）。\nA. 蚂蚁  B. 细菌  C. 蚯蚓", answer: "B", difficulty: 1 },
      { type: "简答题", content: "请说出显微镜和放大镜的区别。", answer: "放大镜只能放大几倍到几十倍，显微镜可以放大几百倍到几千倍；显微镜由目镜和物镜两组镜片组成，放大镜只有一块镜片。", difficulty: 2 },
      { type: "实验探究题", content: "小明用放大镜观察报纸上的文字，发现放大镜离文字越近，文字看起来越大还是越小？\n答：____________________", answer: "在一定范围内，放大镜离文字越近，文字看起来越大。但太近了会模糊。", difficulty: 2 },
      { type: "填空题", content: "（ ）是生命体最基本的单位，用显微镜才能看清。", answer: "细胞", difficulty: 1 }
    ],
  },

  {
    id: "sc-g6s-u2",
    unitName: "地球的运动",
    grade: 6,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: "地球绕太阳公转一周大约需要（ ）。\nA. 一天  B. 一个月  C. 一年", answer: "C", difficulty: 1 },
      { type: "选择题", content: "地球自转一周大约需要（ ）。\nA. 12小时  B. 24小时  C. 365天", answer: "B", difficulty: 1 },
      { type: "判断题", content: "地球自转产生了昼夜交替现象。（ ）", answer: "√", difficulty: 1 },
      { type: "判断题", content: "太阳绕地球转。（ ）", answer: "×", difficulty: 1 },
      { type: "填空题", content: "地球的自转方向是自（ ）向（ ）。", answer: "西；东", difficulty: 2 },
      { type: "填空题", content: "地球绕着（ ）公转，公转方向是自（ ）向（ ）。", answer: "太阳；西；东", difficulty: 2 },
      { type: "选择题", content: "四季变化是由（ ）引起的。\nA. 地球自转  B. 地球公转  C. 月球运动", answer: "B", difficulty: 2 },
      { type: "简答题", content: "请说出昼夜交替是怎样形成的。", answer: "地球是一个不发光也不透明的球体，太阳只能照亮地球的一半。地球不停地自转，被照亮和未被照亮的部分不断交替，就形成了昼夜交替。", difficulty: 2 },
      { type: "实验探究题", content: "小明用手电筒照射地球仪，并转动地球仪，模拟的是什么现象？\n答：____________________", answer: "模拟的是地球自转产生的昼夜交替现象。手电筒代表太阳，地球仪代表地球。", difficulty: 2 },
      { type: "填空题", content: "当北半球是夏季时，南半球是（ ）季。", answer: "冬", difficulty: 2 }
    ],
  },

  {
    id: "sc-g6s-u3",
    unitName: "物质的变化",
    grade: 6,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: "下列变化中属于物理变化的是（ ）。\nA. 铁生锈  B. 木头燃烧  C. 冰融化", answer: "C", difficulty: 1 },
      { type: "选择题", content: "下列变化中产生了新物质的是（ ）。\nA. 把纸撕碎  B. 把糖溶于水  C. 铁生锈", answer: "C", difficulty: 2 },
      { type: "判断题", content: "物理变化和化学变化的本质区别是有没有新物质生成。（ ）", answer: "√", difficulty: 1 },
      { type: "判断题", content: "蜡烛燃烧只发生了化学变化。（ ）", answer: "×", difficulty: 2 },
      { type: "填空题", content: "物质的变化可以分为（ ）变化和（ ）变化两大类。", answer: "物理；化学", difficulty: 1 },
      { type: "填空题", content: "铁生锈是铁与（ ）和（ ）发生化学反应的结果。", answer: "氧气；水", difficulty: 2 },
      { type: "选择题", content: "下列方法中能防止铁生锈的是（ ）。\nA. 放在潮湿处  B. 涂上油漆  C. 放在盐水中", answer: "B", difficulty: 1 },
      { type: "简答题", content: "请说出物理变化和化学变化的区别。", answer: "物理变化没有产生新物质，化学变化产生了新物质。化学变化常伴随发光、发热、变色、产生气体或沉淀等现象。", difficulty: 2 },
      { type: "实验探究题", content: "小明把小苏打和白醋混合在一起，观察到产生了大量气泡。这是什么变化？产生了什么气体？\n答：____________________", answer: "这是化学变化，产生了二氧化碳气体。", difficulty: 2 },
      { type: "填空题", content: "小苏打和白醋混合会产生（ ）气体。", answer: "二氧化碳", difficulty: 1 }
    ],
  },

  // ==================== 科学 - 六年级下册 ====================
  {
    id: "sc-g6x-u1",
    unitName: "进化",
    grade: 6,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: "化石是研究（ ）的重要证据。\nA. 天气变化  B. 生物进化  C. 地震", answer: "B", difficulty: 1 },
      { type: "选择题", content: "达尔文提出了（ ）学说。\nA. 相对论  B. 进化论  C. 万有引力", answer: "B", difficulty: 1 },
      { type: "判断题", content: "现代人类是由猿进化而来的。（ ）", answer: "√", difficulty: 1 },
      { type: "判断题", content: "所有生物从出现到现在都没有变化。（ ）", answer: "×", difficulty: 1 },
      { type: "填空题", content: "生物进化的规律是从（ ）到（ ），从（ ）到（ ）。", answer: "简单；复杂；低等；高等", difficulty: 2 },
      { type: "填空题", content: "自然选择学说的核心是（ ）。", answer: "适者生存，不适者被淘汰", difficulty: 2 },
      { type: "选择题", content: "长颈鹿的长脖子是通过（ ）形成的。\nA. 自己努力伸长  B. 自然选择  C. 人工选择", answer: "B", difficulty: 2 },
      { type: "简答题", content: "请说出化石对研究生物进化的意义。", answer: "化石是古代生物的遗体或遗迹，通过研究化石可以了解古代生物的形态结构和生活环境，推断生物的进化过程。", difficulty: 2 },
      { type: "实验探究题", content: "科学家在不同地层中发现了不同的生物化石，越古老的地层中发现的生物越简单。这说明什么？\n答：____________________", answer: "这说明生物是不断进化的，从简单到复杂，从低等到高等，经历了漫长的变化过程。", difficulty: 2 },
      { type: "填空题", content: "恐龙灭绝大约发生在（ ）万年前。", answer: "6500", difficulty: 2 }
    ],
  },

  {
    id: "sc-g6x-u2",
    unitName: "宇宙",
    grade: 6,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: "太阳系中最大的行星是（ ）。\nA. 地球  B. 火星  C. 木星", answer: "C", difficulty: 1 },
      { type: "选择题", content: "月球绕地球公转一周大约需要（ ）。\nA. 一天  B. 一个月  C. 一年", answer: "B", difficulty: 1 },
      { type: "判断题", content: "太阳是一颗恒星。（ ）", answer: "√", difficulty: 1 },
      { type: "判断题", content: "银河系就是整个宇宙。（ ）", answer: "×", difficulty: 1 },
      { type: "填空题", content: "太阳系有（ ）大行星，其中离太阳最近的是（ ）。", answer: "八；水星", difficulty: 2 },
      { type: "填空题", content: "月球表面高低不平，有许多大大小小的（ ），没有（ ）和（ ）。", answer: "环形山；空气；水", difficulty: 2 },
      { type: "选择题", content: "下列天体中属于卫星的是（ ）。\nA. 太阳  B. 地球  C. 月球", answer: "C", difficulty: 1 },
      { type: "简答题", content: "请说出太阳系八大行星的名称。", answer: "水星、金星、地球、火星、木星、土星、天王星、海王星。", difficulty: 2 },
      { type: "实验探究题", content: "在模拟月相变化的实验中，用乒乓球代表月球，手电筒代表太阳，观察乒乓球被照亮的部分。当乒乓球在太阳和观察者之间时，看到的是什么月相？\n答：____________________", answer: "看到的是新月（或朔月），因为被照亮的一面背对着观察者。", difficulty: 3 },
      { type: "填空题", content: "人类第一位登上月球的宇航员是（ ）。", answer: "阿姆斯特朗", difficulty: 2 }
    ],
  },

  {
    id: "sc-g6x-u3",
    unitName: "物质在我们身边",
    grade: 6,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: "下列物质中属于混合物的是（ ）。\nA. 纯水  B. 食盐  C. 空气", answer: "C", difficulty: 1 },
      { type: "选择题", content: "下列方法中能将盐从盐水中分离出来的是（ ）。\nA. 过滤  B. 蒸发  C. 沉淀", answer: "B", difficulty: 2 },
      { type: "判断题", content: "水可以溶解所有的物质。（ ）", answer: "×", difficulty: 1 },
      { type: "判断题", content: "铁、铜、铝都是金属材料。（ ）", answer: "√", difficulty: 1 },
      { type: "填空题", content: "物质有三种常见状态：（ ）、（ ）和（ ）。", answer: "固态；液态；气态", difficulty: 1 },
      { type: "填空题", content: "分离混合物的方法有过滤、（ ）、蒸发和（ ）等。", answer: "沉淀；蒸馏（答案不唯一）", difficulty: 2 },
      { type: "选择题", content: "下列变化中，水的状态发生变化的是（ ）。\nA. 水结冰  B. 铁生锈  C. 木头燃烧", answer: "A", difficulty: 1 },
      { type: "简答题", content: "请说出三种分离混合物的方法及其适用情况。", answer: "过滤：分离不溶于液体的固体和液体；蒸发：从溶液中分离出溶解的固体；沉淀：利用重力使不溶物沉降。", difficulty: 2 },
      { type: "实验探究题", content: "小明把一杯盐水放在阳光下，几天后杯底出现了白色的盐粒。这是什么过程？\n答：____________________", answer: "这是蒸发过程。水蒸发后，溶解在水中的盐结晶析出，留在杯底。", difficulty: 2 },
      { type: "填空题", content: "把糖放入水中搅拌后看不见了，说明糖（ ）在水中了。", answer: "溶解", difficulty: 1 }
    ],
  },

{
    id: "cn-g1s-u4",
    unitName: "日月明",
    grade: 1,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
míng tiān（ ）`, answer: "明天", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
lì qì（ ）`, answer: "力气", difficulty: 1 },
      { type: "组词", content: `用"明"字组两个词：（ ）、（ ）`, answer: "明天；明白（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"林"字组两个词：（ ）、（ ）`, answer: "森林；树林（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `"日"加"月"组成（ ）字。
"木"加"木"组成（ ）字。`, answer: "明；林", difficulty: 1 },
      { type: "选择题", content: `"尖"字是由哪两个字组成的？（ ）
A. 上和下  B. 小和大  C. 大和小`, answer: "B", difficulty: 2 },
      { type: "判断题", content: `"尘"字是"小"加"土"组成的。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `"从"字是由两个"人"字组成的。（ ）`, answer: "√", difficulty: 1 },
      { type: "选词填空", content: `选词填空：明  朋
（ ）天我去找（ ）友玩。`, answer: "明；朋", difficulty: 2 },
      { type: "照样子写句子", content: `照样子写句子：
日月明，田力男。
小大（ ），（ ）（ ）（ ）。`, answer: "尖；二木林（答案不唯一）", difficulty: 2 }
    ],
  },

  {
    id: "cn-g1s-u5",
    unitName: "大小多少",
    grade: 1,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
dà xiǎo（ ）`, answer: "大小", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
duō shǎo（ ）`, answer: "多少", difficulty: 1 },
      { type: "组词", content: `用"多"字组两个词：（ ）、（ ）`, answer: "多少；很多（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"少"字组两个词：（ ）、（ ）`, answer: "多少；少量（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `一头（ ），一只（ ），一群（ ）。
请填上合适的动物名称。`, answer: "牛；猫；鸭子（答案不唯一）", difficulty: 1 },
      { type: "选择题", content: `"一群"可以用来形容（ ）。
A. 一只猫  B. 一群鸭子  C. 一头牛`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `"大"和"小"是一对反义词。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `"一颗苹果"用量词"颗"是对的。（ ）`, answer: "×", difficulty: 2 },
      { type: "选词填空", content: `选词填空：颗  棵
一（ ）树  一（ ）星星`, answer: "棵；颗", difficulty: 2 },
      { type: "照样子写句子", content: `照样子写句子：
一个大，一个小，一头黄牛一只猫。
一个（ ），一个（ ），一（ ）苹果一（ ）枣。`, answer: "大；小；个；颗（答案不唯一）", difficulty: 2 }
    ],
  },

  {
    id: "cn-g1x-u3",
    unitName: "小公鸡和小鸭子",
    grade: 1,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
tā men（ ）`, answer: "他们", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
hé shuǐ（ ）`, answer: "河水", difficulty: 1 },
      { type: "组词", content: `用"他"字组两个词：（ ）、（ ）`, answer: "他们；他的（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"河"字组两个词：（ ）、（ ）`, answer: "河水；小河（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `小公鸡和小鸭子一块儿去（ ）玩。
小公鸡找到了很多（ ），给小鸭子吃。`, answer: "草地；虫子", difficulty: 1 },
      { type: "选择题", content: `小公鸡不会（ ），差点淹死。
A. 跑步  B. 游泳  C. 飞行`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `小公鸡和小鸭子是好朋友，他们互相帮助。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `小鸭子捉虫子比小公鸡厉害。（ ）`, answer: "×", difficulty: 1 },
      { type: "选词填空", content: `选词填空：块  快
一（ ）石头  跑得很（ ）`, answer: "块；快", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
"小鸭子捉不到虫子，小公鸡捉到了虫子就给小鸭子吃。"
小公鸡是怎样帮助小鸭子的？
答：____________________`, answer: "小公鸡捉到虫子后给小鸭子吃，帮助小鸭子。", difficulty: 2 }
    ],
  },

  {
    id: "cn-g1x-u4",
    unitName: "树和喜鹊",
    grade: 1,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
dān dú（ ）`, answer: "单独", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
kuài lè（ ）`, answer: "快乐", difficulty: 1 },
      { type: "组词", content: `用"乐"字组两个词：（ ）、（ ）`, answer: "快乐；欢乐（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"呼"字组两个词：（ ）、（ ）`, answer: "呼叫；欢呼（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `树很（ ），喜鹊也很（ ），后来有了很多树和喜鹊，大家都很（ ）。`, answer: "孤单；孤单；快乐", difficulty: 1 },
      { type: "选择题", content: `喜鹊住在（ ）。
A. 地上  B. 树上  C. 水里`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `树和喜鹊多了以后，大家变得更快乐了。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `只有一棵树的时候，喜鹊也很快乐。（ ）`, answer: "×", difficulty: 1 },
      { type: "选词填空", content: `选词填空：招呼  呼叫
老师（ ）同学们集合。
喜鹊在树上（ ）伙伴。`, answer: "招呼；呼叫", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
"每天天一亮，喜鹊们叽叽喳喳叫几声，打着招呼一起飞出去了。"
喜鹊们每天早上做什么？
答：____________________`, answer: "喜鹊们每天早上叽叽喳喳叫几声，打着招呼一起飞出去。", difficulty: 2 }
    ],
  },

  {
    id: "cn-g2s-u3",
    unitName: "曹冲称象",
    grade: 2,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
chēng zhòng（ ）`, answer: "称重", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
lùn chǐ（ ）`, answer: "论尺", difficulty: 1 },
      { type: "组词", content: `用"称"字组两个词：（ ）、（ ）`, answer: "称重；称呼（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"杆"字组两个词：（ ）、（ ）`, answer: "秤杆；旗杆（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `曹冲称象的步骤：先把大象赶到（ ）上，看船身（ ）到哪里，在水面画一条线。
再把大象赶上岸，往船上装（ ），装到画线的地方为止。`, answer: "船；沉；石头", difficulty: 2 },
      { type: "选择题", content: `曹冲称象时，用（ ）代替大象来称重量。
A. 沙子  B. 石头  C. 水`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `曹冲是曹操的儿子。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `官员们想出了称象的好办法。（ ）`, answer: "×", difficulty: 1 },
      { type: "选词填空", content: `选词填空：议论  讨论
大家都在（ ）这头大象有多重。
同学们在（ ）如何完成作业。`, answer: "议论；讨论", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
曹冲称象的办法好在哪里？
答：____________________`, answer: "曹冲的办法巧妙地利用了船的浮力，用石头代替大象，化大为小，解决了称大象重量的问题。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g2s-u4",
    unitName: "玲玲的画",
    grade: 2,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
jiǎng huà（ ）`, answer: "评画", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
nǎo jí（ ）`, answer: "着急", difficulty: 1 },
      { type: "组词", content: `用"画"字组两个词：（ ）、（ ）`, answer: "画画；画笔（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"楼"字组两个词：（ ）、（ ）`, answer: "楼梯；楼房（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `玲玲画了一幅（ ），不小心弄脏了，爸爸帮她画了一只（ ），画变得更好了。`, answer: "画；小狗", difficulty: 1 },
      { type: "选择题", content: `玲玲不小心把画弄脏了，她（ ）。
A. 重新画了一幅  B. 哭了  C. 爸爸帮她改了画`, answer: "C", difficulty: 1 },
      { type: "判断题", content: `玲玲的画弄脏后，爸爸帮她把脏的地方画成了小花狗。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `玲玲的画参加评奖得了第一名。（ ）`, answer: "×", difficulty: 1 },
      { type: "选词填空", content: `选词填空：满意  得意
玲玲对自己的画很（ ）。
他（ ）地笑了。`, answer: "满意；得意", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
"好多事情并不像我们想象的那么糟。只要肯动脑筋，坏事有时也能变成好事。"
这句话告诉我们什么道理？
答：____________________`, answer: "遇到困难不要灰心，只要动脑筋想办法，坏事也可能变成好事。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g2x-u2",
    unitName: "寓言二则",
    grade: 2,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
wáng yáng bǔ láo（ ）`, answer: "亡羊补牢", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
huà shé tiān zú（ ）`, answer: "画蛇添足", difficulty: 1 },
      { type: "组词", content: `用"亡"字组两个词：（ ）、（ ）`, answer: "亡羊补牢；死亡（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"牢"字组两个词：（ ）、（ ）`, answer: "牢房；牢记（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `"亡羊补牢"的意思是丢了（ ）再去修补（ ），还不算晚。
比喻出了问题以后想办法（ ），可以防止继续受损失。`, answer: "羊；羊圈；补救", difficulty: 2 },
      { type: "选择题", content: `"亡羊补牢"告诉我们的道理是（ ）。
A. 羊丢了不用管  B. 出了问题要及时补救  C. 羊圈不用修`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `"画蛇添足"告诉我们做事不要多此一举。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `寓言故事都是真实发生的事情。（ ）`, answer: "×", difficulty: 1 },
      { type: "选词填空", content: `选词填空：劝告  告诉
邻居（ ）他赶快修补羊圈。
妈妈（ ）我要认真写作业。`, answer: "劝告；告诉", difficulty: 2 },
      { type: "阅读理解", content: `阅读寓言回答问题：
"画蛇添足"中，那个人为什么没有喝到酒？
答：____________________`, answer: "因为他给蛇画了脚，不再是蛇了，所以没有喝到酒。", difficulty: 2 }
    ],
  },

  {
    id: "cn-g2x-u3",
    unitName: "画杨桃",
    grade: 2,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
yáng táo（ ）`, answer: "杨桃", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
shú xī（ ）`, answer: "熟悉", difficulty: 1 },
      { type: "组词", content: `用"图"字组两个词：（ ）、（ ）`, answer: "图画；地图（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"座"字组两个词：（ ）、（ ）`, answer: "座位；一座山（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `"我"把杨桃画成了（ ）形，同学们都（ ）"我"。
老师让同学们坐到"我"的（ ）上看，发现确实像五角星。`, answer: "五角星；嘲笑；座位", difficulty: 2 },
      { type: "选择题", content: `老师告诉同学们，看问题要（ ）。
A. 只看一面  B. 从不同角度看  C. 不用看`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `从不同角度看杨桃，形状可能不同。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `同学们嘲笑"我"画错了，老师也觉得"我"画错了。（ ）`, answer: "×", difficulty: 1 },
      { type: "选词填空", content: `选词填空：审视  注视
老师（ ）了一下那幅画。
他（ ）着黑板上的字。`, answer: "审视；注视", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
"老师的教诲让我终生难忘。"
老师的教诲是什么？
答：____________________`, answer: "老师的教诲是看问题要从不同角度去看，不要轻易嘲笑别人。", difficulty: 2 }
    ],
  },

  {
    id: "cn-g2x-u4",
    unitName: "小马过河",
    grade: 2,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
yuàn yì（ ）`, answer: "愿意", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
mài zi（ ）`, answer: "麦子", difficulty: 1 },
      { type: "组词", content: `用"磨"字组两个词：（ ）、（ ）`, answer: "磨坊；磨刀（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"挡"字组两个词：（ ）、（ ）`, answer: "挡住；阻挡（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `小马要帮妈妈把半口袋（ ）驮到磨坊去。
（ ）说河水很浅，（ ）说河水很深。`, answer: "麦子；老牛；松鼠", difficulty: 2 },
      { type: "选择题", content: `小马最后（ ）过了河。
A. 自己  B. 被妈妈背过去  C. 没有过河`, answer: "A", difficulty: 1 },
      { type: "判断题", content: `小马听了老牛和松鼠的话后，自己亲自去试了试。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `老牛和松鼠说的都不对。（ ）`, answer: "×", difficulty: 1 },
      { type: "选词填空", content: `选词填空：难为情  难过
小马（ ）地低下了头。
他考试没考好，心里很（ ）。`, answer: "难为情；难过", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
"孩子，光听别人说，自己不动脑筋，不去试试，是不行的。"
妈妈的话告诉了小马什么道理？
答：____________________`, answer: "遇到问题不能只听别人的，要自己动脑筋想一想，亲自去试一试才能知道答案。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g3s-u3",
    unitName: "卖火柴的小女孩",
    grade: 3,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
huǒ chái（ ）`, answer: "火柴", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
wēi xiào（ ）`, answer: "微笑", difficulty: 1 },
      { type: "组词", content: `用"暖"字组两个词：（ ）、（ ）`, answer: "温暖；暖和（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"苦"字组两个词：（ ）、（ ）`, answer: "痛苦；辛苦（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `卖火柴的小女孩擦燃火柴后，分别看到了（ ）、（ ）、（ ）和奶奶。`, answer: "大火炉；烤鹅；圣诞树", difficulty: 2 },
      { type: "选择题", content: `《卖火柴的小女孩》的作者是（ ）。
A. 格林兄弟  B. 安徒生  C. 伊索`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `小女孩最后在幸福中死去了。（ ）`, answer: "√", difficulty: 2 },
      { type: "判断题", content: `小女孩真的看到了大火炉和烤鹅。（ ）`, answer: "×", difficulty: 1 },
      { type: "选词填空", content: `选词填空：温暖  寒冷
大年夜的街上非常（ ）。
火柴的光芒让小女孩感到了（ ）。`, answer: "寒冷；温暖", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文片段回答问题：
"她俩在光明和快乐中飞走了，越飞越高，飞到那没有寒冷，没有饥饿，也没有痛苦的地方去了。"
"没有寒冷，没有饥饿，也没有痛苦的地方"指的是什么？
答：____________________`, answer: "指的是小女孩和奶奶一起去了天堂，在那里她不再受苦。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g3s-u4",
    unitName: "那一定会很好",
    grade: 3,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
suì（ ）`, answer: "缩", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
tuī（ ）`, answer: "推", difficulty: 1 },
      { type: "组词", content: `用"根"字组两个词：（ ）、（ ）`, answer: "树根；根本（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"破"字组两个词：（ ）、（ ）`, answer: "打破；破旧（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `种子发芽后变成了（ ），后来被砍倒变成了（ ），又变成了（ ），最后变成了（ ）。`, answer: "大树；手推车；椅子；木地板", difficulty: 2 },
      { type: "选择题", content: `种子第一次想变成（ ）。
A. 大树  B. 手推车  C. 椅子`, answer: "A", difficulty: 1 },
      { type: "判断题", content: `种子每一次变化都是它自己主动想改变的。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `木地板最后又变回了种子。（ ）`, answer: "×", difficulty: 1 },
      { type: "选词填空", content: `选词填空：满意  舒服
农夫对这把椅子很（ ）。
躺在木地板上很（ ）。`, answer: "满意；舒服", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
"那一定会很好"这句话在课文中出现了几次？表达了什么？
答：____________________`, answer: "这句话出现了多次，表达了种子（木头）每一次变化时积极乐观的心态和对美好生活的向往。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g3x-u3",
    unitName: "慢性子裁缝和急性子顾客",
    grade: 3,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
cái feng（ ）`, answer: "裁缝", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
bù liào（ ）`, answer: "布料", difficulty: 1 },
      { type: "组词", content: `用"性"字组两个词：（ ）、（ ）`, answer: "性格；急性子（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"卷"字组两个词：（ ）、（ ）`, answer: "卷尺；卷起（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `急性子顾客第一天想做（ ）装，第二天改成（ ）装，第三天改成（ ）装，第四天改成（ ）装。`, answer: "冬；秋；夏；春", difficulty: 2 },
      { type: "选择题", content: `慢性子裁缝最后做的是（ ）。
A. 冬装  B. 春装  C. 什么也没做`, answer: "A", difficulty: 2 },
      { type: "判断题", content: `慢性子裁缝一直没有开始做衣服。（ ）`, answer: "×", difficulty: 1 },
      { type: "判断题", content: `急性子顾客每次都改变了主意。（ ）`, answer: "√", difficulty: 1 },
      { type: "选词填空", content: `选词填空：耐心  急躁
慢性子裁缝做事很（ ）。
急性子顾客非常（ ），总是改主意。`, answer: "耐心；急躁", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
这个故事告诉了我们什么道理？
答：____________________`, answer: "做事不能太急躁，也不能太拖拉，要有计划地做事，并且坚持自己的想法。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g3x-u4",
    unitName: "漏",
    grade: 3,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
lòu（ ）`, answer: "漏", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
láng（ ）`, answer: "狼", difficulty: 1 },
      { type: "组词", content: `用"贼"字组两个词：（ ）、（ ）`, answer: "贼人；做贼（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"胖"字组两个词：（ ）、（ ）`, answer: "胖子；肥胖（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `老爷爷和老奶奶说"（ ）"，老虎和贼都以为"漏"是一个很厉害的东西，吓得（ ）。`, answer: "漏；跑了", difficulty: 2 },
      { type: "选择题", content: `"漏"在课文中指的是（ ）。
A. 一个怪物  B. 屋顶漏雨  C. 一个人的名字`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `老虎和贼最后都被吓跑了。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `老爷爷家的驴被老虎吃掉了。（ ）`, answer: "×", difficulty: 1 },
      { type: "选词填空", content: `选词填空：翻  滚
老虎从墙上（ ）了下来。
贼从屋顶上（ ）了下来。`, answer: "翻；滚", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
老虎和贼为什么会害怕"漏"？
答：____________________`, answer: "因为他们偷听到老爷爷和老奶奶说“漏”，以为“漏”是一个非常厉害的东西，其实“漏”只是指屋顶漏雨。", difficulty: 2 }
    ],
  },

  {
    id: "cn-g4s-u4",
    unitName: "爬山虎的脚",
    grade: 4,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
pá shān hǔ（ ）`, answer: "爬山虎", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
jūn yún（ ）`, answer: "均匀", difficulty: 1 },
      { type: "组词", content: `用"嫩"字组两个词：（ ）、（ ）`, answer: "嫩绿；嫩芽（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"茎"字组两个词：（ ）、（ ）`, answer: "根茎；茎叶（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `爬山虎的脚长在茎上，茎上长（ ）的地方，反面伸出（ ）的六七根细丝，这就是爬山虎的脚。`, answer: "叶柄；枝状", difficulty: 2 },
      { type: "选择题", content: `爬山虎是靠（ ）爬墙的。
A. 根  B. 茎  C. 脚（细丝）`, answer: "C", difficulty: 1 },
      { type: "判断题", content: `爬山虎的脚像蛟龙的爪子。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `爬山虎的脚触着墙后就会变成灰色。（ ）`, answer: "×", difficulty: 2 },
      { type: "修辞手法判断", content: `判断下列句子用了什么修辞手法：
"爬山虎的脚触着墙的时候，细丝就像蛟龙的爪子。"
答：____________________`, answer: "比喻", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文片段回答问题：
"爬山虎的嫩叶，一顺儿朝下，铺在墙上没有重叠，也不留一点儿空隙。"
爬山虎的叶子有什么特点？
答：____________________`, answer: "爬山虎的嫩叶一顺儿朝下，铺在墙上没有重叠，也不留空隙，长得非常均匀。", difficulty: 2 }
    ],
  },

  {
    id: "cn-g4s-u5",
    unitName: "女娲补天",
    grade: 4,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
nǚ wā（ ）`, answer: "女娲", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
zhù rù（ ）`, answer: "注入", difficulty: 1 },
      { type: "组词", content: `用"塌"字组两个词：（ ）、（ ）`, answer: "塌陷；倒塌（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"治"字组两个词：（ ）、（ ）`, answer: "治理；治病（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `天塌下来后，人们遭受了（ ）、（ ）和（ ）等灾难。
女娲用（ ）炼成石浆，补好了天上的窟窿。`, answer: "火灾；水灾；猛兽（答案不唯一）；五彩石", difficulty: 2 },
      { type: "选择题", content: `女娲补天用了（ ）色的石头。
A. 红  B. 五彩  C. 白`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `女娲补天是一个神话故事。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `女娲只用了三天就补好了天。（ ）`, answer: "×", difficulty: 1 },
      { type: "修辞手法判断", content: `判断下列句子用了什么修辞手法：
"天哪，太可怕了！远远的天空塌下一大块，露出一个黑黑的大窟窿。"
答：____________________`, answer: "夸张", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
女娲为什么要补天？她是怎么做的？
答：____________________`, answer: "因为天塌了一大块，人们遭受了各种灾难。女娲找了五彩石，用神火熔化成石浆，把天上的窟窿补好了。", difficulty: 2 }
    ],
  },

  {
    id: "cn-g4x-u4",
    unitName: "海上日出",
    grade: 4,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
fàn wéi（ ）`, answer: "范围", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
chǔn jié（ ）`, answer: "纯洁", difficulty: 1 },
      { type: "组词", content: `用"纵"字组两个词：（ ）、（ ）`, answer: "纵横；纵然（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"刹"字组两个词：（ ）、（ ）`, answer: "刹那；刹车（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `日出前，天空还是一片（ ），转眼间天边出现了（ ），慢慢地太阳露出了（ ）。`, answer: "浅蓝；红霞；小半边脸", difficulty: 2 },
      { type: "选择题", content: `《海上日出》的作者是（ ）。
A. 老舍  B. 巴金  C. 鲁迅`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `太阳升起时，阳光穿过云层，直射到水面上。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `有云的时候，太阳就完全看不到了。（ ）`, answer: "×", difficulty: 1 },
      { type: "修辞手法判断", content: `判断下列句子用了什么修辞手法：
"太阳像负着什么重担似的，慢慢儿，一纵一纵地，使劲儿向上升。"
答：____________________`, answer: "拟人", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
"这不是很伟大的奇观吗？"
这句话表达了作者怎样的感情？
答：____________________`, answer: "这句话用反问的语气表达了作者对海上日出这一伟大奇观的赞美和热爱之情。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g4x-u5",
    unitName: "记金华的双龙洞",
    grade: 4,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
zhè jiāng（ ）`, answer: "浙江", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
dù juān（ ）`, answer: "杜鹃", difficulty: 1 },
      { type: "组词", content: `用"窄"字组两个词：（ ）、（ ）`, answer: "狭窄；窄小（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"郁"字组两个词：（ ）、（ ）`, answer: "葱郁；郁闷（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `作者游览双龙洞的顺序是：路上→（ ）→外洞→（ ）→（ ）。`, answer: "洞口；孔隙；内洞", difficulty: 2 },
      { type: "选择题", content: `双龙洞内洞有两条形状像（ ）的钟乳石。
A. 龙  B. 虎  C. 狮子`, answer: "A", difficulty: 1 },
      { type: "判断题", content: `作者通过孔隙时是仰卧在小船里过去的。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `孔隙非常宽敞，可以站起来通过。（ ）`, answer: "×", difficulty: 1 },
      { type: "修辞手法判断", content: `判断下列句子用了什么修辞手法：
"随着山势，溪流时而宽，时而窄，时而缓，时而急，溪声也时时变换调子。"
答：____________________`, answer: "排比、拟人", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
孔隙有什么特点？作者是怎样通过孔隙的？
答：____________________`, answer: "孔隙非常窄小，只能容得下一只小船进出。作者是仰卧在小船上，由工人拉绳子通过的。", difficulty: 2 }
    ],
  },

  {
    id: "cn-g5s-u4",
    unitName: "搭石",
    grade: 5,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
dā shí（ ）`, answer: "搭石", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
xié tiáo（ ）`, answer: "协调", difficulty: 1 },
      { type: "组词", content: `用"汛"字组两个词：（ ）、（ ）`, answer: "汛期；秋汛（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"衡"字组两个词：（ ）、（ ）`, answer: "平衡；衡量（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `人们走搭石的时候，动作要（ ），前面的（ ），后面的（ ）上去。`, answer: "协调有序；抬起脚来；紧跟", difficulty: 2 },
      { type: "选择题", content: `搭石是人们在小溪里（ ）的石头。
A. 随便放的  B. 按照一定距离摆放的  C. 用水泥固定的`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `如果搭石不稳，人们会主动挑选合适的石头换上。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `走搭石的时候可以跑得很快。（ ）`, answer: "×", difficulty: 1 },
      { type: "修辞手法判断", content: `判断下列句子用了什么修辞手法：
"每当上工、下工，一行人走搭石的时候，动作是那么协调有序！前面的抬起脚来，后面的紧跟上去。踏踏的声音，像轻快的音乐。"
答：____________________`, answer: "比喻", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
"一排排搭石，任人走，任人踏，它们联结着故乡的小路，也联结着乡亲们美好的情感。"
搭石联结着什么？
答：____________________`, answer: "搭石联结着故乡的小路，也联结着乡亲们美好的情感。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g5s-u5",
    unitName: "将相和",
    grade: 5,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
jiàng xiàng（ ）`, answer: "将相", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
zhào guó（ ）`, answer: "赵国", difficulty: 1 },
      { type: "组词", content: `用"胆"字组两个词：（ ）、（ ）`, answer: "胆量；胆怯（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"拒"字组两个词：（ ）、（ ）`, answer: "拒绝；抗拒（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `"将相和"中"将"指的是（ ），"相"指的是（ ）。
课文讲了三个小故事：（ ）、（ ）、（ ）。`, answer: "廉颇；蔺相如；完璧归赵；渑池之会；负荆请罪", difficulty: 2 },
      { type: "选择题", content: `蔺相如是一个（ ）的人。
A. 胆小怕事  B. 勇敢机智、顾全大局  C. 骄傲自大`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `廉颇最后负荆请罪，向蔺相如道歉。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `蔺相如怕廉颇是因为胆子小。（ ）`, answer: "×", difficulty: 1 },
      { type: "修改病句", content: `修改病句：
"蔺相如和廉颇是赵国的人。"`, answer: "改为：蔺相如和廉颇都是赵国人。", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
蔺相如为什么避让廉颇？这说明了什么？
答：____________________`, answer: "蔺相如避让廉颇是因为他把国家利益放在第一位，认为将相和睦才能保卫赵国。这说明他顾全大局、心胸宽广。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g5x-u4",
    unitName: "草船借箭",
    grade: 5,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
dù jì（ ）`, answer: "妒忌", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
wěi tuō（ ）`, answer: "委托", difficulty: 1 },
      { type: "组词", content: `用"曹"字组两个词：（ ）、（ ）`, answer: "曹操；曹军（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"弩"字组两个词：（ ）、（ ）`, answer: "弓弩；弩箭（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `诸葛亮用（ ）条小船，船上扎满了（ ），利用大雾天气向曹操"借"了（ ）支箭。`, answer: "二十；草把子；十万", difficulty: 2 },
      { type: "选择题", content: `诸葛亮"草船借箭"利用了（ ）。
A. 大风  B. 大雾  C. 大雨`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `周瑜让诸葛亮造箭是想考验他的能力。（ ）`, answer: "×", difficulty: 2 },
      { type: "判断题", content: `诸葛亮算准了第三天四更时一定有大雾。（ ）`, answer: "√", difficulty: 1 },
      { type: "修辞手法判断", content: `判断下列句子用了什么修辞手法：
"雾这样大，曹操一定不敢派兵出来。"
答：____________________`, answer: "没有使用修辞手法（心理描写）", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
诸葛亮为什么能成功"借"到箭？
答：____________________`, answer: "因为诸葛亮精通天文气象，算准了第三天有大雾，又了解曹操多疑的性格，所以能成功借到箭。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g5x-u5",
    unitName: "景阳冈",
    grade: 5,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
jǐng yáng gāng（ ）`, answer: "景阳冈", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
xiè lòu（ ）`, answer: "泄露", difficulty: 1 },
      { type: "组词", content: `用"冈"字组两个词：（ ）、（ ）`, answer: "山冈；景阳冈（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"肋"字组两个词：（ ）、（ ）`, answer: "肋骨；两肋（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `武松在景阳冈上喝了（ ）碗酒，打死了（ ）只大虫（老虎）。`, answer: "十八；一", difficulty: 1 },
      { type: "选择题", content: `《景阳冈》选自（ ）。
A. 《三国演义》  B. 《水浒传》  C. 《西游记》`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `武松一开始不相信冈上有老虎。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `武松是被老虎吓跑的。（ ）`, answer: "×", difficulty: 1 },
      { type: "修辞手法判断", content: `判断下列句子用了什么修辞手法：
"大虫见掀他不着，吼一声，就像半天里起了个霹雳，震得那山冈也动。"
答：____________________`, answer: "比喻、夸张", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
武松是一个怎样的人？从哪些地方可以看出来？
答：____________________`, answer: "武松是一个武艺高强、英勇无畏的人。从他赤手空拳打死老虎可以看出他的勇敢和力量。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g6s-u4",
    unitName: "狼牙山五壮士",
    grade: 6,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
zhuàng shì（ ）`, answer: "壮士", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
qū tǐ（ ）`, answer: "躯体", difficulty: 1 },
      { type: "组词", content: `用"寇"字组两个词：（ ）、（ ）`, answer: "日寇；敌寇（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"屹"字组两个词：（ ）、（ ）`, answer: "屹立；屹然（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `狼牙山五壮士是（ ）、（ ）、（ ）、（ ）和（ ）。
他们最后跳下了（ ）。`, answer: "马宝玉；葛振林；宋学义；胡德林；胡福才；悬崖", difficulty: 2 },
      { type: "选择题", content: `五壮士把敌人引向（ ）。
A. 主力部队的方向  B. 狼牙山顶峰  C. 安全的地方`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `五壮士是为了保护群众和主力部队的安全才把敌人引上绝路的。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `五壮士最后全部牺牲了。（ ）`, answer: "×", difficulty: 2 },
      { type: "修辞手法判断", content: `判断下列句子用了什么修辞手法：
"这是英雄的中国人民坚强不屈的声音！这声音惊天动地，气壮山河！"
答：____________________`, answer: "夸张", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
五壮士为什么要选择跳崖？这表现了他们怎样的精神？
答：____________________`, answer: "五壮士跳崖是为了不当俘虏，宁死不屈。这表现了他们热爱祖国、忠于人民、英勇无畏的牺牲精神。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g6s-u5",
    unitName: "少年闰土",
    grade: 6,
    semester: "上",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
rùn tǔ（ ）`, answer: "闰土", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
chá fán（ ）`, answer: "祭祀", difficulty: 1 },
      { type: "组词", content: `用"猹"字组两个词：（ ）、（ ）`, answer: "猹（此字较特殊，组词困难）；刺猹", difficulty: 1 },
      { type: "组词", content: `用"厨"字组两个词：（ ）、（ ）`, answer: "厨房；厨具（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `闰土给"我"讲了（ ）、（ ）、（ ）和（ ）四件事。`, answer: "雪地捕鸟；海边拾贝；看瓜刺猹；看跳鱼儿", difficulty: 2 },
      { type: "选择题", content: `《少年闰土》的作者是（ ）。
A. 老舍  B. 鲁迅  C. 巴金`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `闰土是一个见多识广、聪明能干的农村少年。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `"我"和闰土的生活环境完全一样。（ ）`, answer: "×", difficulty: 1 },
      { type: "修辞手法判断", content: `判断下列句子用了什么修辞手法：
"深蓝的天空中挂着一轮金黄的圆月，下面是海边的沙地，都种着一望无际的碧绿的西瓜。"
答：____________________`, answer: "没有使用修辞手法（景物描写）", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
"我"和闰土之间有什么不同？"我"对闰土的生活有什么感受？
答：____________________`, answer: "“我”是富家少爷，生活圈子很小；闰土是农村少年，见多识广。“我”对闰土的生活非常羡慕和向往。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g6x-u4",
    unitName: "匆匆",
    grade: 6,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
cōng cōng（ ）`, answer: "匆匆", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
zhēng rěn（ ）`, answer: "挣扎", difficulty: 1 },
      { type: "组词", content: `用"挪"字组两个词：（ ）、（ ）`, answer: "挪动；挪移（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"蒸"字组两个词：（ ）、（ ）`, answer: "蒸发；蒸笼（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `《匆匆》的作者是（ ），课文以（ ）为线索，表达了作者对（ ）的感慨。`, answer: "朱自清；时间流逝；时光流逝", difficulty: 2 },
      { type: "选择题", content: `"燕子去了，有再来的时候"用的是（ ）写法。
A. 对比  B. 排比  C. 拟人`, answer: "B", difficulty: 2 },
      { type: "判断题", content: `课文表达了作者对时光流逝的惋惜和珍惜时间的感情。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `作者认为时间是可以留住的。（ ）`, answer: "×", difficulty: 1 },
      { type: "修辞手法判断", content: `判断下列句子用了什么修辞手法：
"八千多日子已经从我手中溜去，像针尖上一滴水滴在大海里。"
答：____________________`, answer: "比喻", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
"我们的日子为什么一去不复返呢？"
作者为什么要反复提出这个问题？
答：____________________`, answer: "作者反复提出这个问题，表达了对时光一去不复返的无奈和感慨，提醒人们要珍惜时间。", difficulty: 3 }
    ],
  },

  {
    id: "cn-g6x-u5",
    unitName: "那个星期天",
    grade: 6,
    semester: "下",
    subject: "语文",
    questions: [
      { type: "拼音写汉字", content: `看拼音写汉字：
zhòu rán（ ）`, answer: "骤然", difficulty: 1 },
      { type: "拼音写汉字", content: `看拼音写汉字：
wàng què（ ）`, answer: "忘却", difficulty: 1 },
      { type: "组词", content: `用"惶"字组两个词：（ ）、（ ）`, answer: "惶恐；惊惶（答案不唯一）", difficulty: 1 },
      { type: "组词", content: `用"吻"字组两个词：（ ）、（ ）`, answer: "亲吻；吻合（答案不唯一）", difficulty: 1 },
      { type: "填空题", content: `《那个星期天》中，"我"一直盼望母亲带"我"出去，从（ ）等到（ ），但母亲一直没有时间。`, answer: "早晨；黄昏", difficulty: 2 },
      { type: "选择题", content: `《那个星期天》的作者是（ ）。
A. 朱自清  B. 史铁生  C. 老舍`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `课文主要运用了心理描写来表现"我"的情感变化。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `母亲最后带"我"出去了。（ ）`, answer: "×", difficulty: 1 },
      { type: "修辞手法判断", content: `判断下列句子用了什么修辞手法：
"我坐在草丛里看她们，想象她们的家，想象她们此刻在干什么，想象她们的兄弟姐妹和她们的父母。"
答：____________________`, answer: "排比", difficulty: 2 },
      { type: "阅读理解", content: `阅读课文回答问题：
"我"的情感经历了怎样的变化？
答：____________________`, answer: "“我”的情感从满怀期待到焦急等待，再到失望、绝望，最后陷入深深的失落之中。", difficulty: 3 }
    ],
  },

  {
    id: "en-g3s-u4",
    unitName: "We love animals",
    grade: 3,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: `"duck"的意思是（ ）。
A. 鸡  B. 鸭子  C. 鹅`, answer: "B", difficulty: 1 },
      { type: "单词选择", content: `"pig"的意思是（ ）。
A. 狗  B. 猫  C. 猪`, answer: "C", difficulty: 1 },
      { type: "英汉互译", content: `将下列英文翻译成中文：
bear —（ ）  cat —（ ）  dog —（ ）`, answer: "熊；猫；狗", difficulty: 1 },
      { type: "英汉互译", content: `将下列中文翻译成英文：
兔子 —（ ）  鸟 —（ ）  鱼 —（ ）`, answer: "rabbit；bird；fish", difficulty: 1 },
      { type: "情景交际", content: `你想表达"我喜欢小狗"，你应该说（ ）。
A. I like dogs.  B. I like cats.  C. I like birds.`, answer: "A", difficulty: 1 },
      { type: "连词成句", content: `连词成句：
love / We / animals（ . ）`, answer: "We love animals.", difficulty: 1 },
      { type: "情景交际", content: `别人问你"What's this?"，它是一只鸟，你应回答（ ）。
A. It's a bird.  B. It's a dog.  C. It's a cat.`, answer: "A", difficulty: 1 },
      { type: "单词选择", content: `"rabbit"的意思是（ ）。
A. 兔子  B. 老鼠  C. 松鼠`, answer: "A", difficulty: 1 },
      { type: "阅读理解", content: `阅读对话回答问题：
A: What's this?
B: It's a duck.
A: Do you like ducks?
B: Yes, I do.
Does B like ducks?
答：____________________`, answer: "Yes, he/she does.", difficulty: 2 },
      { type: "情景交际", content: `你想说"它好可爱"，你应该说（ ）。
A. It's so cute!  B. It's so big!  C. It's so fat!`, answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g3s-u5",
    unitName: "Happy birthday!",
    grade: 3,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: `"birthday"的意思是（ ）。
A. 假日  B. 生日  C. 节日`, answer: "B", difficulty: 1 },
      { type: "单词选择", content: `"cake"的意思是（ ）。
A. 面包  B. 蛋糕  C. 饼干`, answer: "B", difficulty: 1 },
      { type: "英汉互译", content: `将下列英文翻译成中文：
bread —（ ）  juice —（ ）  milk —（ ）`, answer: "面包；果汁；牛奶", difficulty: 1 },
      { type: "英汉互译", content: `将下列中文翻译成英文：
鸡蛋 —（ ）  水 —（ ）  米饭 —（ ）`, answer: "egg；water；rice", difficulty: 1 },
      { type: "情景交际", content: `朋友过生日，你应该说（ ）。
A. Happy birthday!  B. Happy New Year!  C. Merry Christmas!`, answer: "A", difficulty: 1 },
      { type: "连词成句", content: `连词成句：
Happy / birthday / to / you（ ! ）`, answer: "Happy birthday to you!", difficulty: 1 },
      { type: "情景交际", content: `你想问"你几岁了？"，你应该说（ ）。
A. How old are you?  B. How are you?  C. How big are you?`, answer: "A", difficulty: 1 },
      { type: "单词选择", content: `"one"的意思是（ ）。
A. 二  B. 一  C. 三`, answer: "B", difficulty: 1 },
      { type: "阅读理解", content: `阅读对话回答问题：
A: Happy birthday, John!
B: Thank you!
A: How old are you?
B: I'm nine years old.
How old is John?
答：____________________`, answer: "He is nine years old.", difficulty: 2 },
      { type: "情景交际", content: `你想说"给我一个蛋糕"，你应该说（ ）。
A. Can I have some cake, please?  B. I want a cake.`, answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g3x-u4",
    unitName: "At the farm",
    grade: 3,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: `"tomato"的意思是（ ）。
A. 土豆  B. 西红柿  C. 洋葱`, answer: "B", difficulty: 1 },
      { type: "单词选择", content: `"potato"的意思是（ ）。
A. 土豆  B. 番茄  C. 黄瓜`, answer: "A", difficulty: 1 },
      { type: "英汉互译", content: `将下列英文翻译成中文：
carrot —（ ）  green beans —（ ）  onion —（ ）`, answer: "胡萝卜；豆角；洋葱", difficulty: 1 },
      { type: "英汉互译", content: `将下列中文翻译成英文：
农场 —（ ）  蔬菜 —（ ）  动物 —（ ）`, answer: "farm；vegetable；animal", difficulty: 1 },
      { type: "情景交际", content: `你想问"这些是什么？"，你应该说（ ）。
A. What are these?  B. What is this?  C. What are those?`, answer: "A", difficulty: 1 },
      { type: "连词成句", content: `连词成句：
are / What / these（ ? ）`, answer: "What are these?", difficulty: 1 },
      { type: "情景交际", content: `你想说"它们是西红柿"，你应该说（ ）。
A. They are tomatoes.  B. It is a tomato.  C. These are tomato.`, answer: "A", difficulty: 1 },
      { type: "单词选择", content: `"sheep"的意思是（ ）。
A. 山羊  B. 绵羊  C. 马`, answer: "B", difficulty: 1 },
      { type: "阅读理解", content: `阅读对话回答问题：
A: Look at the farm!
B: Wow! Are these carrots?
A: Yes, they are.
What are these?
答：____________________`, answer: "They are carrots.", difficulty: 2 },
      { type: "情景交际", content: `你想说"我喜欢胡萝卜"，你应该说（ ）。
A. I like carrots.  B. I like potatoes.  C. I like tomatoes.`, answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g3x-u5",
    unitName: "Recycle",
    grade: 3,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: `"swim"的意思是（ ）。
A. 跑步  B. 游泳  C. 跳跃`, answer: "B", difficulty: 1 },
      { type: "单词选择", content: `"fly"的意思是（ ）。
A. 飞  B. 走  C. 爬`, answer: "A", difficulty: 1 },
      { type: "英汉互译", content: `将下列英文翻译成中文：
jump —（ ）  run —（ ）  walk —（ ）`, answer: "跳；跑；走", difficulty: 1 },
      { type: "英汉互译", content: `将下列中文翻译成英文：
唱歌 —（ ）  跳舞 —（ ）  画画 —（ ）`, answer: "sing；dance；draw", difficulty: 1 },
      { type: "情景交际", content: `你想问"你会游泳吗？"，你应该说（ ）。
A. Can you swim?  B. Do you swim?  C. Are you swim?`, answer: "A", difficulty: 1 },
      { type: "连词成句", content: `连词成句：
can / I / swim（ . ）`, answer: "I can swim.", difficulty: 1 },
      { type: "情景交际", content: `别人问你"Can you sing?"，你会唱歌，你应回答（ ）。
A. Yes, I can.  B. No, I can't.  C. Yes, I do.`, answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: `用所给词的正确形式填空：
I can ________ (play) football.`, answer: "play", difficulty: 1 },
      { type: "阅读理解", content: `阅读短文回答问题：
"Hello! I'm Sarah. I can sing and dance. I can't swim. My friend Mike can swim and play football."
Can Sarah swim?
答：____________________`, answer: "No, she can't.", difficulty: 2 },
      { type: "情景交际", content: `你想说"我不会画画"，你应该说（ ）。
A. I can't draw.  B. I can draw.  C. I don't draw.`, answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g4s-u4",
    unitName: "Dinner's ready",
    grade: 4,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: `"beef"的意思是（ ）。
A. 鸡肉  B. 牛肉  C. 猪肉`, answer: "B", difficulty: 1 },
      { type: "单词选择", content: `"chicken"的意思是（ ）。
A. 鸡肉  B. 牛肉  C. 鱼`, answer: "A", difficulty: 1 },
      { type: "英汉互译", content: `将下列英文翻译成中文：
noodles —（ ）  soup —（ ）  vegetable —（ ）`, answer: "面条；汤；蔬菜", difficulty: 1 },
      { type: "英汉互译", content: `将下列中文翻译成英文：
筷子 —（ ）  碗 —（ ）  叉子 —（ ）`, answer: "chopsticks；bowl；fork", difficulty: 1 },
      { type: "情景交际", content: `你想问"晚餐准备好了吗？"，你应该说（ ）。
A. What's for dinner?  B. Is dinner ready?  C. Let's have dinner.`, answer: "B", difficulty: 1 },
      { type: "连词成句", content: `连词成句：
for / What / is / dinner（ ? ）`, answer: "What is for dinner?", difficulty: 2 },
      { type: "情景交际", content: `你想说"请递给我筷子"，你应该说（ ）。
A. Pass me the chopsticks, please.  B. Give me the chopsticks.`, answer: "A", difficulty: 1 },
      { type: "单词选择", content: `"spoon"的意思是（ ）。
A. 刀  B. 勺子  C. 碗`, answer: "B", difficulty: 1 },
      { type: "阅读理解", content: `阅读对话回答问题：
A: What's for dinner?
B: Fish and vegetables.
A: Great! I'd like some fish, please.
What would A like?
答：____________________`, answer: "He/She would like some fish.", difficulty: 2 },
      { type: "情景交际", content: `你想说"请帮我倒点水"，你应该说（ ）。
A. Help yourself.  B. Can I have some water, please?`, answer: "B", difficulty: 1 }
    ],
  },

  {
    id: "en-g4s-u5",
    unitName: "Meet my family",
    grade: 4,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: `"doctor"的意思是（ ）。
A. 老师  B. 医生  C. 护士`, answer: "B", difficulty: 1 },
      { type: "单词选择", content: `"farmer"的意思是（ ）。
A. 工人  B. 司机  C. 农民`, answer: "C", difficulty: 1 },
      { type: "英汉互译", content: `将下列英文翻译成中文：
nurse —（ ）  cook —（ ）  driver —（ ）`, answer: "护士；厨师；司机", difficulty: 1 },
      { type: "英汉互译", content: `将下列中文翻译成英文：
老师 —（ ）  工人 —（ ）  警察 —（ ）`, answer: "teacher；worker；police officer", difficulty: 2 },
      { type: "情景交际", content: `你想问"你爸爸是做什么工作的？"，你应该说（ ）。
A. What's your father's job?  B. Who is your father?  C. Where is your father?`, answer: "A", difficulty: 1 },
      { type: "连词成句", content: `连词成句：
job / What's / your / father's（ ? ）`, answer: "What's your father's job?", difficulty: 2 },
      { type: "情景交际", content: `你想说"我妈妈是一名护士"，你应该说（ ）。
A. My mother is a nurse.  B. My mother is a doctor.`, answer: "A", difficulty: 1 },
      { type: "单词选择", content: `"cook"的意思是（ ）。
A. 厨师  B. 农民  C. 医生`, answer: "A", difficulty: 1 },
      { type: "阅读理解", content: `阅读对话回答问题：
A: How many people are there in your family?
B: Three. My parents and me.
A: What's your father's job?
B: He's a doctor.
How many people are there in B's family?
答：____________________`, answer: "Three.", difficulty: 2 },
      { type: "情景交际", content: `你想说"我家有三口人"，你应该说（ ）。
A. There are three people in my family.  B. My family has three peoples.`, answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g4x-u4",
    unitName: "Shopping",
    grade: 4,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: `"gloves"的意思是（ ）。
A. 帽子  B. 手套  C. 围巾`, answer: "B", difficulty: 1 },
      { type: "单词选择", content: `"scarf"的意思是（ ）。
A. 围巾  B. 手套  C. 雨伞`, answer: "A", difficulty: 1 },
      { type: "英汉互译", content: `将下列英文翻译成中文：
umbrella —（ ）  sunglasses —（ ）  coat —（ ）`, answer: "雨伞；太阳镜；外套", difficulty: 1 },
      { type: "英汉互译", content: `将下列中文翻译成英文：
便宜的 —（ ）  昂贵的 —（ ）  好的 —（ ）`, answer: "cheap；expensive；nice", difficulty: 2 },
      { type: "情景交际", content: `你想问"这条围巾多少钱？"，你应该说（ ）。
A. How much is this scarf?  B. How many scarves?`, answer: "A", difficulty: 1 },
      { type: "连词成句", content: `连词成句：
much / is / this / How（ ? ）`, answer: "How much is this?", difficulty: 2 },
      { type: "情景交际", content: `这条围巾50元，你想说"太贵了"，你应该说（ ）。
A. It's too expensive.  B. It's too cheap.  C. It's very nice.`, answer: "A", difficulty: 1 },
      { type: "单词选择", content: `"cheap"的反义词是（ ）。
A. nice  B. expensive  C. good`, answer: "B", difficulty: 1 },
      { type: "阅读理解", content: `阅读对话回答问题：
A: Can I help you?
B: Yes. This dress is nice. How much is it?
A: It's 100 yuan.
How much is the dress?
答：____________________`, answer: "It's 100 yuan.", difficulty: 2 },
      { type: "情景交际", content: `你想说"我买下了"，你应该说（ ）。
A. I'll take it.  B. I don't want it.  C. It's too expensive.`, answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g4x-u5",
    unitName: "My clothes",
    grade: 4,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: `"pants"的意思是（ ）。
A. 裤子  B. 裙子  C. 衬衫`, answer: "A", difficulty: 1 },
      { type: "单词选择", content: `"dress"的意思是（ ）。
A. 裤子  B. 连衣裙  C. 外套`, answer: "B", difficulty: 1 },
      { type: "英汉互译", content: `将下列英文翻译成中文：
shirt —（ ）  sweater —（ ）  jacket —（ ）`, answer: "衬衫；毛衣；夹克", difficulty: 1 },
      { type: "英汉互译", content: `将下列中文翻译成英文：
短袜 —（ ）  鞋子 —（ ）  短裤 —（ ）`, answer: "socks；shoes；shorts", difficulty: 1 },
      { type: "情景交际", content: `你想说"这是我的衬衫"，你应该说（ ）。
A. This is my shirt.  B. These are my shirts.`, answer: "A", difficulty: 1 },
      { type: "连词成句", content: `连词成句：
are / Whose / pants / these（ ? ）`, answer: "Whose pants are these?", difficulty: 2 },
      { type: "情景交际", content: `你想问"这是谁的帽子？"，你应该说（ ）。
A. Whose hat is this?  B. Whose hats are these?`, answer: "A", difficulty: 1 },
      { type: "单词选择", content: `"sweater"的意思是（ ）。
A. 裙子  B. 毛衣  C. 外套`, answer: "B", difficulty: 1 },
      { type: "阅读理解", content: `阅读对话回答问题：
A: Whose coat is this?
B: It's mine.
A: Are these your shoes?
B: No, they aren't. They are Mike's.
Whose shoes are these?
答：____________________`, answer: "They are Mike's.", difficulty: 2 },
      { type: "情景交际", content: `你想说"这些是我的裤子"，你应该说（ ）。
A. These are my pants.  B. This is my pants.`, answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g5s-u4",
    unitName: "There is a big bed",
    grade: 5,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: `"closet"的意思是（ ）。
A. 衣柜  B. 书桌  C. 椅子`, answer: "A", difficulty: 1 },
      { type: "单词选择", content: `"curtain"的意思是（ ）。
A. 门  B. 窗帘  C. 窗户`, answer: "B", difficulty: 1 },
      { type: "英汉互译", content: `将下列英文翻译成中文：
trash bin —（ ）  mirror —（ ）  end table —（ ）`, answer: "垃圾桶；镜子；床头柜", difficulty: 1 },
      { type: "英汉互译", content: `将下列中文翻译成英文：
在……上面 —（ ）  在……旁边 —（ ）  在……后面 —（ ）`, answer: "on；near/next to；behind", difficulty: 1 },
      { type: "情景交际", content: `你想说"房间里有一张大床"，你应该说（ ）。
A. There is a big bed in the room.  B. There are a big bed in the room.`, answer: "A", difficulty: 1 },
      { type: "连词成句", content: `连词成句：
there / Is / a / picture / on / the / wall（ ? ）`, answer: "Is there a picture on the wall?", difficulty: 2 },
      { type: "情景交际", content: `你想说"桌子上有一台电脑"，你应该说（ ）。
A. There is a computer on the desk.  B. There are a computer on the desk.`, answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: `用所给词的正确形式填空：
There ________ (be) a book and two pens on the desk.`, answer: "is", difficulty: 2 },
      { type: "阅读理解", content: `阅读短文回答问题：
"I have my own room now. There is a big bed, a desk, a chair and a bookshelf. The desk is near the window."
Where is the desk?
答：____________________`, answer: "The desk is near the window.", difficulty: 2 },
      { type: "情景交际", content: `你想问"墙上有一幅画吗？"，你应该说（ ）。
A. Is there a picture on the wall?  B. Are there a picture on the wall?`, answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g5s-u5",
    unitName: "In a nature park",
    grade: 5,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: `"forest"的意思是（ ）。
A. 森林  B. 公园  C. 花园`, answer: "A", difficulty: 1 },
      { type: "单词选择", content: `"mountain"的意思是（ ）。
A. 河流  B. 山  C. 湖`, answer: "B", difficulty: 1 },
      { type: "英汉互译", content: `将下列英文翻译成中文：
river —（ ）  lake —（ ）  bridge —（ ）`, answer: "河流；湖；桥", difficulty: 1 },
      { type: "英汉互译", content: `将下列中文翻译成英文：
村庄 —（ ）  花 —（ ）  草 —（ ）`, answer: "village；flower；grass", difficulty: 1 },
      { type: "情景交际", content: `你想说"公园里有一条河"，你应该说（ ）。
A. There is a river in the park.  B. There are a river in the park.`, answer: "A", difficulty: 1 },
      { type: "连词成句", content: `连词成句：
there / Are / any / tall / buildings / in / the / village（ ? ）`, answer: "Are there any tall buildings in the village?", difficulty: 2 },
      { type: "情景交际", content: `你想问"森林里有湖吗？"，你应该说（ ）。
A. Is there a lake in the forest?  B. Are there a lake in the forest?`, answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: `用所给词的正确形式填空：
There ________ (be) many birds in the forest.`, answer: "are", difficulty: 1 },
      { type: "阅读理解", content: `阅读短文回答问题：
"The nature park is so quiet. There is a forest and a lake. There are many flowers near the lake."
What's near the lake?
答：____________________`, answer: "There are many flowers near the lake.", difficulty: 2 },
      { type: "情景交际", content: `你想说"没有高楼"，你应该说（ ）。
A. There aren't any tall buildings.  B. There isn't tall buildings.`, answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g5x-u4",
    unitName: "My school calendar",
    grade: 5,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: `"January"的意思是（ ）。
A. 一月  B. 二月  C. 三月`, answer: "A", difficulty: 1 },
      { type: "单词选择", content: `"December"的意思是（ ）。
A. 十月  B. 十一月  C. 十二月`, answer: "C", difficulty: 1 },
      { type: "英汉互译", content: `将下列英文翻译成中文：
Easter —（ ）  summer vacation —（ ）  winter vacation —（ ）`, answer: "复活节；暑假；寒假", difficulty: 1 },
      { type: "英汉互译", content: `将下列中文翻译成英文：
植树节 —（ ）  儿童节 —（ ）  教师节 —（ ）`, answer: "Tree Planting Day；Children's Day；Teachers' Day", difficulty: 2 },
      { type: "情景交际", content: `你想问"学校旅行在什么时候？"，你应该说（ ）。
A. When is the school trip?  B. Where is the school trip?`, answer: "A", difficulty: 1 },
      { type: "连词成句", content: `连词成句：
is / When / Easter（ ? ）`, answer: "When is Easter?", difficulty: 1 },
      { type: "情景交际", content: `你想说"儿童节在六月"，你应该说（ ）。
A. Children's Day is in June.  B. Children's Day is in July.`, answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: `用所给词的正确形式填空：
Mother's Day ________ (be) in May.`, answer: "is", difficulty: 1 },
      { type: "阅读理解", content: `阅读短文回答问题：
"We have a few fun things in spring. Tree Planting Day is in March. Easter is in April. May Day is in May."
When is Tree Planting Day?
答：____________________`, answer: "Tree Planting Day is in March.", difficulty: 2 },
      { type: "情景交际", content: `你想说"我们在七月和八月放暑假"，你应该说（ ）。
A. We have summer vacation in July and August.  B. We have winter vacation in July and August.`, answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g5x-u5",
    unitName: "Work quietly!",
    grade: 5,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: `"doing morning exercises"的意思是（ ）。
A. 上课  B. 做早操  C. 吃午饭`, answer: "B", difficulty: 1 },
      { type: "单词选择", content: `"having English class"的意思是（ ）。
A. 上英语课  B. 上数学课  C. 上体育课`, answer: "A", difficulty: 1 },
      { type: "英汉互译", content: `将下列英文翻译成中文：
eating lunch —（ ）  reading a book —（ ）  listening to music —（ ）`, answer: "吃午饭；看书；听音乐", difficulty: 1 },
      { type: "英汉互译", content: `将下列中文翻译成英文：
保持你的课桌干净 —（ ）  排队 —（ ）`, answer: "keep your desk clean；line up", difficulty: 2 },
      { type: "情景交际", content: `你想让别人安静，你应该说（ ）。
A. Talk loudly!  B. Keep to the right.  C. Work quietly.`, answer: "C", difficulty: 1 },
      { type: "连词成句", content: `连词成句：
they / What / doing / are（ ? ）`, answer: "What are they doing?", difficulty: 2 },
      { type: "情景交际", content: `你想问"他在做什么？"，你应该说（ ）。
A. What is he doing?  B. What does he do?  C. What did he do?`, answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: `用所给词的正确形式填空：
She ________ (read) a book now.`, answer: "is reading", difficulty: 2 },
      { type: "阅读理解", content: `阅读短文回答问题：
"It's 10:00 a.m. The students are in the classroom. Some are reading books. Some are writing. Tom is drawing a picture."
What is Tom doing?
答：____________________`, answer: "Tom is drawing a picture.", difficulty: 2 },
      { type: "情景交际", content: `你想说"请靠右走"，你应该说（ ）。
A. Keep to the right.  B. Keep to the left.  C. Keep quiet.`, answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g6s-u4",
    unitName: "I'm going to study the moon",
    grade: 6,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: `"scientist"的意思是（ ）。
A. 医生  B. 科学家  C. 老师`, answer: "B", difficulty: 1 },
      { type: "单词选择", content: `"pilot"的意思是（ ）。
A. 飞行员  B. 司机  C. 医生`, answer: "A", difficulty: 1 },
      { type: "英汉互译", content: `将下列英文翻译成中文：
postman —（ ）  fisherman —（ ）  coach —（ ）`, answer: "邮递员；渔民；教练", difficulty: 1 },
      { type: "英汉互译", content: `将下列中文翻译成英文：
警察 —（ ）  工厂工人 —（ ）  秘书 —（ ）`, answer: "police officer；factory worker；secretary", difficulty: 2 },
      { type: "情景交际", content: `你想问"你长大后想做什么？"，你应该说（ ）。
A. What do you want to be?  B. What are you doing?  C. What do you do?`, answer: "A", difficulty: 1 },
      { type: "连词成句", content: `连词成句：
do / you / What / want / to / be（ ? ）`, answer: "What do you want to be?", difficulty: 2 },
      { type: "情景交际", content: `你想说"我想当一名科学家"，你应该说（ ）。
A. I want to be a scientist.  B. I am a scientist.`, answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: `用所给词的正确形式填空：
She ________ (study) the moon every day.`, answer: "studies", difficulty: 2 },
      { type: "阅读理解", content: `阅读短文回答问题：
"I want to be a pilot. I'm going to fly a plane. My friend wants to be a scientist. He's going to study the moon."
What does the writer want to be?
答：____________________`, answer: "The writer wants to be a pilot.", difficulty: 2 },
      { type: "情景交际", content: `你想说"他在哪里工作？"，你应该说（ ）。
A. Where does he work?  B. What does he do?`, answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g6s-u5",
    unitName: "Review",
    grade: 6,
    semester: "上",
    subject: "英语",
    questions: [
      { type: "单词选择", content: `"angry"的意思是（ ）。
A. 高兴的  B. 生气的  C. 害怕的`, answer: "B", difficulty: 1 },
      { type: "单词选择", content: `"afraid"的意思是（ ）。
A. 害怕的  B. 难过的  C. 担心的`, answer: "A", difficulty: 1 },
      { type: "英汉互译", content: `将下列英文翻译成中文：
worried —（ ）  happy —（ ）  sad —（ ）`, answer: "担心的；高兴的；难过的", difficulty: 1 },
      { type: "英汉互译", content: `将下列中文翻译成英文：
看病 —（ ）  深呼吸 —（ ）  数到十 —（ ）`, answer: "see a doctor；take a deep breath；count to ten", difficulty: 2 },
      { type: "情景交际", content: `朋友看起来很难过，你想问"你怎么了？"，你应该说（ ）。
A. What's wrong?  B. How are you?  C. What are you doing?`, answer: "A", difficulty: 1 },
      { type: "连词成句", content: `连词成句：
should / You / a / doctor / see（ . ）`, answer: "You should see a doctor.", difficulty: 2 },
      { type: "情景交际", content: `你想建议别人"你应该深呼吸"，你应该说（ ）。
A. You should take a deep breath.  B. You should be angry.`, answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: `用所给词的正确形式填空：
He is ill. He should ________ (stay) in bed.`, answer: "stay", difficulty: 1 },
      { type: "阅读理解", content: `阅读短文回答问题：
"Amy is ill today. She should see a doctor. She should drink more water and stay in bed."
What should Amy do?
答：____________________`, answer: "She should see a doctor, drink more water and stay in bed.", difficulty: 2 },
      { type: "情景交际", content: `你想说"别担心"，你应该说（ ）。
A. Don't worry.  B. Don't be happy.  C. Don't go.`, answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g6x-u4",
    unitName: "Day and night",
    grade: 6,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: `"morning"的意思是（ ）。
A. 早上  B. 中午  C. 晚上`, answer: "A", difficulty: 1 },
      { type: "单词选择", content: `"evening"的意思是（ ）。
A. 早上  B. 下午  C. 傍晚/晚上`, answer: "C", difficulty: 1 },
      { type: "英汉互译", content: `将下列英文翻译成中文：
afternoon —（ ）  noon —（ ）  midnight —（ ）`, answer: "下午；中午；午夜", difficulty: 1 },
      { type: "英汉互译", content: `将下列中文翻译成英文：
日出 —（ ）  日落 —（ ）  黎明 —（ ）`, answer: "sunrise；sunset；dawn", difficulty: 2 },
      { type: "情景交际", content: `你想说"我通常在早上7点起床"，你应该说（ ）。
A. I usually get up at 7 a.m.  B. I usually get up at 7 p.m.`, answer: "A", difficulty: 1 },
      { type: "连词成句", content: `连词成句：
the / sun / rises / in / the / morning（ . ）`, answer: "The sun rises in the morning.", difficulty: 2 },
      { type: "情景交际", content: `你想说"月亮在晚上出来"，你应该说（ ）。
A. The moon comes out at night.  B. The sun comes out at night.`, answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: `用所给词的正确形式填空：
The sun ________ (rise) in the east.`, answer: "rises", difficulty: 2 },
      { type: "阅读理解", content: `阅读短文回答问题：
"The sun rises in the morning and sets in the evening. The moon and stars come out at night. We have day and night because the Earth rotates."
Why do we have day and night?
答：____________________`, answer: "Because the Earth rotates.", difficulty: 2 },
      { type: "情景交际", content: `你想说"白天很长"，你应该说（ ）。
A. The days are long.  B. The days are short.`, answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "en-g6x-u5",
    unitName: "Story time",
    grade: 6,
    semester: "下",
    subject: "英语",
    questions: [
      { type: "单词选择", content: `"prince"的意思是（ ）。
A. 国王  B. 王子  C. 皇后`, answer: "B", difficulty: 1 },
      { type: "单词选择", content: `"princess"的意思是（ ）。
A. 公主  B. 皇后  C. 王后`, answer: "A", difficulty: 1 },
      { type: "英汉互译", content: `将下列英文翻译成中文：
king —（ ）  queen —（ ）  castle —（ ）`, answer: "国王；王后；城堡", difficulty: 1 },
      { type: "英汉互译", content: `将下列中文翻译成英文：
从前 —（ ）  魔法 —（ ）  镜子 —（ ）`, answer: "once upon a time；magic；mirror", difficulty: 2 },
      { type: "情景交际", content: `你想用英语讲故事开头，你应该说（ ）。
A. Once upon a time...  B. Long long ago...  C. A and B are both correct.`, answer: "C", difficulty: 1 },
      { type: "连词成句", content: `连词成句：
lived / a / beautiful / princess / There / once（ . ）`, answer: "There once lived a beautiful princess.", difficulty: 3 },
      { type: "情景交际", content: `你想说"他们从此幸福地生活在一起"，你应该说（ ）。
A. They lived happily ever after.  B. They lived sadly.`, answer: "A", difficulty: 1 },
      { type: "用所给词的正确形式填空", content: `用所给词的正确形式填空：
The prince ________ (fall) in love with the princess.`, answer: "fell", difficulty: 2 },
      { type: "阅读理解", content: `阅读短文回答问题：
"Once upon a time, there was a kind girl named Cinderella. She had to do all the housework. One day, a fairy helped her go to the ball."
Who helped Cinderella go to the ball?
答：____________________`, answer: "A fairy helped her.", difficulty: 2 },
      { type: "情景交际", content: `你想说"故事结束了"，你应该说（ ）。
A. The story is over.  B. The story begins.`, answer: "A", difficulty: 1 }
    ],
  },

  {
    id: "sc-g3s-u4",
    unitName: "水",
    grade: 3,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: `水在常温下是（ ）。
A. 固体  B. 液体  C. 气体`, answer: "B", difficulty: 1 },
      { type: "选择题", content: `水变成水蒸气的过程叫做（ ）。
A. 凝结  B. 蒸发  C. 融化`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `水没有固定的形状，但有固定的体积。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `冰和水是同一种物质。（ ）`, answer: "√", difficulty: 1 },
      { type: "填空题", content: `水有三种状态：（ ）、（ ）和（ ）。`, answer: "固态；液态；气态", difficulty: 1 },
      { type: "填空题", content: `水在（ ）°C时会结冰，在（ ）°C时会沸腾。`, answer: "0；100", difficulty: 2 },
      { type: "选择题", content: `下列方法中能加快水蒸发的是（ ）。
A. 降低温度  B. 增大表面积  C. 密封容器`, answer: "B", difficulty: 2 },
      { type: "简答题", content: `请说出水的三种状态分别是什么，并举出例子。`, answer: "固态：冰、雪；液态：水、雨水；气态：水蒸气、雾。", difficulty: 2 },
      { type: "实验探究题", content: `小明把两块同样大小的湿布分别放在阳光下和阴凉处，哪块布先干？为什么？
答：____________________`, answer: "放在阳光下的布先干，因为温度高，水蒸发得快。", difficulty: 2 },
      { type: "判断题", content: `地球上的淡水资源非常丰富，用不完。（ ）`, answer: "×", difficulty: 1 }
    ],
  },

  {
    id: "sc-g3s-u5",
    unitName: "空气",
    grade: 3,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: `空气（ ）。
A. 有颜色  B. 无色无味  C. 有味道`, answer: "B", difficulty: 1 },
      { type: "选择题", content: `空气（ ）。
A. 占据空间  B. 不占据空间  C. 有固定形状`, answer: "A", difficulty: 1 },
      { type: "判断题", content: `空气看不见摸不着，所以它不存在。（ ）`, answer: "×", difficulty: 1 },
      { type: "判断题", content: `风是空气流动形成的。（ ）`, answer: "√", difficulty: 1 },
      { type: "填空题", content: `空气主要由（ ）和（ ）组成，其中（ ）约占78%。`, answer: "氮气；氧气；氮气", difficulty: 2 },
      { type: "填空题", content: `把纸团塞入杯底，将杯子倒扣入水中，纸团（ ）湿，因为杯中有（ ）。`, answer: "不会；空气", difficulty: 2 },
      { type: "选择题", content: `下列方法中可以证明空气存在的是（ ）。
A. 看一看  B. 闻一闻  C. 用扇子扇风`, answer: "C", difficulty: 1 },
      { type: "简答题", content: `请说出两种证明空气存在的方法。`, answer: "1. 用扇子扇风能感觉到风（空气流动）；2. 把杯子倒扣入水中，纸团不会湿；3. 给气球打气，气球会变大。（答案不唯一）", difficulty: 2 },
      { type: "实验探究题", content: `小明把一个气球吹大后松开手，气球飞了出去。这是什么原理？
答：____________________`, answer: "气球里的空气被压缩后释放出来，空气向外喷出产生的反作用力推动气球飞出去。", difficulty: 2 },
      { type: "判断题", content: `压缩空气有弹性。（ ）`, answer: "√", difficulty: 1 }
    ],
  },

  {
    id: "sc-g3x-u3",
    unitName: "磁铁",
    grade: 3,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: `磁铁能吸引（ ）材料。
A. 所有  B. 铁一类  C. 塑料`, answer: "B", difficulty: 1 },
      { type: "选择题", content: `条形磁铁有（ ）个磁极。
A. 1  B. 2  C. 4`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `磁铁的同极相互吸引，异极相互排斥。（ ）`, answer: "×", difficulty: 1 },
      { type: "判断题", content: `磁铁隔着物体也能吸引铁。（ ）`, answer: "√", difficulty: 1 },
      { type: "填空题", content: `磁铁有两个磁极，分别叫（ ）极和（ ）极。`, answer: "南（S）；北（N）", difficulty: 1 },
      { type: "填空题", content: `指南针是利用磁铁能够指示（ ）的性质制成的。`, answer: "南北方向", difficulty: 2 },
      { type: "选择题", content: `下列物体中能被磁铁吸引的是（ ）。
A. 铁钉  B. 铝片  C. 铜线`, answer: "A", difficulty: 1 },
      { type: "简答题", content: `请说出磁铁有哪些形状。`, answer: "条形磁铁、蹄形磁铁、环形磁铁、圆形磁铁等。（答案不唯一）", difficulty: 1 },
      { type: "实验探究题", content: `小明把两块条形磁铁的N极靠近，会发生什么现象？如果把N极和S极靠近呢？
答：____________________`, answer: "N极和N极靠近会相互排斥；N极和S极靠近会相互吸引。", difficulty: 2 },
      { type: "判断题", content: `把磁铁摔在地上，它的磁性会减弱。（ ）`, answer: "√", difficulty: 2 }
    ],
  },

  {
    id: "sc-g3x-u4",
    unitName: "太阳、地球和月球",
    grade: 3,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: `太阳是一颗（ ）。
A. 行星  B. 恒星  C. 卫星`, answer: "B", difficulty: 1 },
      { type: "选择题", content: `月球是地球的（ ）。
A. 恒星  B. 行星  C. 卫星`, answer: "C", difficulty: 1 },
      { type: "判断题", content: `太阳比地球大得多。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `月球上有人居住。（ ）`, answer: "×", difficulty: 1 },
      { type: "填空题", content: `太阳、地球和月球中，最大的是（ ），最小的是（ ）。`, answer: "太阳；月球", difficulty: 1 },
      { type: "填空题", content: `月球绕地球公转一周大约需要（ ）天。`, answer: "29.5（约30）", difficulty: 2 },
      { type: "选择题", content: `月球上没有（ ），所以听不到声音。
A. 水  B. 空气  C. 土壤`, answer: "B", difficulty: 1 },
      { type: "简答题", content: `请说出太阳和月球的两个不同点。`, answer: "1. 太阳是恒星，月球是卫星；2. 太阳能发光发热，月球不能；3. 太阳比月球大得多；4. 太阳上有黑子，月球上有环形山。（答案不唯一）", difficulty: 2 },
      { type: "实验探究题", content: `在模拟日食的实验中，用手电筒代表太阳，乒乓球代表月球，大球代表地球。当月球运行到太阳和地球之间时，观察到了什么现象？
答：____________________`, answer: "月球的影子落在地球上，地球上的人会看到太阳被遮挡，这就是日食现象。", difficulty: 3 },
      { type: "判断题", content: `月相变化是因为月球形状在变化。（ ）`, answer: "×", difficulty: 2 }
    ],
  },

  {
    id: "sc-g4s-u3",
    unitName: "运动和力",
    grade: 4,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: `要使静止的物体运动起来，需要对它施加（ ）。
A. 重力  B. 力  C. 摩擦力`, answer: "B", difficulty: 1 },
      { type: "选择题", content: `摩擦力的方向与物体运动方向（ ）。
A. 相同  B. 相反  C. 垂直`, answer: "B", difficulty: 2 },
      { type: "判断题", content: `没有力，物体就不能运动。（ ）`, answer: "×", difficulty: 2 },
      { type: "判断题", content: `滚动的摩擦力比滑动的摩擦力小。（ ）`, answer: "√", difficulty: 1 },
      { type: "填空题", content: `力的三要素是大小、（ ）和（ ）。`, answer: "方向；作用点", difficulty: 2 },
      { type: "填空题", content: `物体在斜面上会向下滚动，这是因为受到（ ）的作用。`, answer: "重力", difficulty: 1 },
      { type: "选择题", content: `下列哪种方法可以增大摩擦力？（ ）
A. 在冰面上撒沙子  B. 给机器加润滑油  C. 把滑动改为滚动`, answer: "A", difficulty: 2 },
      { type: "简答题", content: `请说出生活中利用摩擦力的两个例子。`, answer: "1. 走路时鞋底与地面的摩擦力防止打滑；2. 刹车时刹车片与车轮的摩擦力使车停下。（答案不唯一）", difficulty: 2 },
      { type: "实验探究题", content: `小明用弹簧测力计拉着木块在桌面上匀速运动，弹簧测力计的读数是2N。这个读数表示什么？
答：____________________`, answer: "这个读数表示木块受到的摩擦力大小是2N。", difficulty: 2 },
      { type: "判断题", content: `重力总是竖直向下的。（ ）`, answer: "√", difficulty: 1 }
    ],
  },

  {
    id: "sc-g4s-u4",
    unitName: "健康生活",
    grade: 4,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: `下列食物中富含维生素的是（ ）。
A. 米饭  B. 青菜  C. 肉类`, answer: "B", difficulty: 1 },
      { type: "选择题", content: `运动后应该（ ）。
A. 马上喝大量水  B. 适当休息再喝水  C. 不喝水`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `经常锻炼身体有利于身体健康。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `小学生每天需要睡10小时以上。（ ）`, answer: "√", difficulty: 1 },
      { type: "填空题", content: `人体需要的六大营养素是蛋白质、糖类、脂肪、维生素、矿物质和（ ）。`, answer: "水", difficulty: 1 },
      { type: "填空题", content: `保护视力的方法有：读书写字时眼睛与书本保持（ ）厘米左右的距离。`, answer: "33（约一尺）", difficulty: 2 },
      { type: "选择题", content: `下列行为中不利于健康的是（ ）。
A. 早起早睡  B. 挑食偏食  C. 适量运动`, answer: "B", difficulty: 1 },
      { type: "简答题", content: `请说出三种保持健康的方法。`, answer: "合理饮食、适量运动、充足睡眠、保持良好心态、注意个人卫生等。（答案不唯一）", difficulty: 2 },
      { type: "实验探究题", content: `小明调查了同学们的饮食习惯，发现很多同学喜欢吃零食而不爱吃蔬菜。请你给出建议。
答：____________________`, answer: "建议同学们多吃蔬菜水果，少吃零食，保持营养均衡，这样才能健康成长。", difficulty: 2 },
      { type: "判断题", content: `感冒了可以不吃药，多喝水多休息就好了。（ ）`, answer: "×", difficulty: 2 }
    ],
  },

  {
    id: "sc-g4x-u3",
    unitName: "种子的萌发",
    grade: 4,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: `种子萌发必需的条件是（ ）。
A. 阳光、土壤  B. 水分、空气、适宜温度  C. 肥料、阳光`, answer: "B", difficulty: 1 },
      { type: "选择题", content: `种子萌发时最先长出来的是（ ）。
A. 茎  B. 根  C. 叶`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `所有种子都能萌发。（ ）`, answer: "×", difficulty: 1 },
      { type: "判断题", content: `种子萌发不需要阳光。（ ）`, answer: "√", difficulty: 2 },
      { type: "填空题", content: `种子由（ ）、（ ）和（ ）组成。`, answer: "种皮；胚；胚乳（子叶）", difficulty: 2 },
      { type: "填空题", content: `种子萌发的过程：先吸收（ ），然后（ ）突破种皮，长出（ ），再长出茎和叶。`, answer: "水分；胚根；根", difficulty: 2 },
      { type: "选择题", content: `把种子放在干燥的环境中，种子会（ ）。
A. 萌发  B. 不萌发  C. 马上死亡`, answer: "B", difficulty: 1 },
      { type: "简答题", content: `请说出种子萌发需要哪些条件。`, answer: "种子萌发需要适量的水分、充足的空气和适宜的温度。", difficulty: 2 },
      { type: "实验探究题", content: `小明把种子分成三组：A组有水、有空气、温度适宜；B组有水、无空气；C组无水、有空气。哪组种子会萌发？
答：____________________`, answer: "A组种子会萌发，因为种子萌发需要水分、空气和适宜温度三个条件同时满足。", difficulty: 2 },
      { type: "判断题", content: `种子萌发后，胚根发育成茎和叶。（ ）`, answer: "×", difficulty: 2 }
    ],
  },

  {
    id: "sc-g4x-u4",
    unitName: "养蚕",
    grade: 4,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: `蚕最喜欢吃（ ）。
A. 菜叶  B. 桑叶  C. 果叶`, answer: "B", difficulty: 1 },
      { type: "选择题", content: `蚕的一生经历（ ）个阶段。
A. 3  B. 4  C. 5`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `蚕从卵孵化出来后就能吐丝。（ ）`, answer: "×", difficulty: 1 },
      { type: "判断题", content: `蚕蛹会变成蚕蛾。（ ）`, answer: "√", difficulty: 1 },
      { type: "填空题", content: `蚕的一生经历卵、（ ）、（ ）、成虫四个阶段。`, answer: "幼虫；蛹", difficulty: 2 },
      { type: "填空题", content: `蚕在（ ）阶段会蜕皮，一共蜕（ ）次皮。`, answer: "幼虫；4", difficulty: 2 },
      { type: "选择题", content: `蚕吐丝结茧是在（ ）阶段。
A. 幼虫  B. 蛹  C. 成虫`, answer: "A", difficulty: 2 },
      { type: "简答题", content: `请说出养蚕需要注意什么。`, answer: "要保持清洁、提供新鲜桑叶、注意温度和通风、避免用手直接触摸蚕等。（答案不唯一）", difficulty: 2 },
      { type: "实验探究题", content: `小明观察到蚕在吐丝前不再吃桑叶，身体变得透明。这说明什么？
答：____________________`, answer: "这说明蚕即将进入吐丝结茧阶段，身体变透明是因为体内充满了丝液。", difficulty: 2 },
      { type: "判断题", content: `蚕丝可以织成丝绸。（ ）`, answer: "√", difficulty: 1 }
    ],
  },

  {
    id: "sc-g5s-u4",
    unitName: "地球的结构",
    grade: 5,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: `地球内部从外到内依次是（ ）。
A. 地核、地幔、地壳  B. 地壳、地幔、地核  C. 地幔、地壳、地核`, answer: "B", difficulty: 1 },
      { type: "选择题", content: `地球的表面大部分被（ ）覆盖。
A. 陆地  B. 海洋  C. 冰川`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `地壳是最薄的一层。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `地核的温度很高。（ ）`, answer: "√", difficulty: 1 },
      { type: "填空题", content: `地球的内部结构分为三层：地壳、（ ）和（ ）。`, answer: "地幔；地核", difficulty: 1 },
      { type: "填空题", content: `地球的陆地面积约占地球总面积的（ ）%。`, answer: "29", difficulty: 2 },
      { type: "选择题", content: `下列岩石中属于岩浆岩的是（ ）。
A. 花岗岩  B. 砂岩  C. 石灰岩`, answer: "A", difficulty: 2 },
      { type: "简答题", content: `请说出地球内部三层的名称和特点。`, answer: "地壳：最薄的一层，由岩石组成；地幔：最厚的一层，温度很高，有岩浆；地核：最内层，温度最高，由铁和镍组成。", difficulty: 2 },
      { type: "实验探究题", content: `小明用一个煮熟的鸡蛋来模拟地球内部结构。蛋壳、蛋白和蛋黄分别模拟地球的哪一部分？
答：____________________`, answer: "蛋壳模拟地壳，蛋白模拟地幔，蛋黄模拟地核。", difficulty: 2 },
      { type: "判断题", content: `地球是一个不规则的球体。（ ）`, answer: "√", difficulty: 1 }
    ],
  },

  {
    id: "sc-g5s-u5",
    unitName: "制作计时工具",
    grade: 5,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: `摆钟是利用摆的（ ）来计时的。
A. 等时性  B. 摆动幅度  C. 摆锤重量`, answer: "A", difficulty: 1 },
      { type: "选择题", content: `自制水钟时，滴水速度与（ ）有关。
A. 水的颜色  B. 水位高低  C. 容器形状`, answer: "B", difficulty: 2 },
      { type: "判断题", content: `摆线越长，摆动越快。（ ）`, answer: "×", difficulty: 2 },
      { type: "判断题", content: `自制计时工具需要反复测试和调整。（ ）`, answer: "√", difficulty: 1 },
      { type: "填空题", content: `摆的快慢与（ ）有关，与摆锤重量和摆动幅度无关。`, answer: "摆线长度", difficulty: 2 },
      { type: "填空题", content: `制作一个一分钟计时器，需要先测定摆每（ ）秒摆动一次，然后计算一分钟需要摆动多少次。`, answer: "一", difficulty: 2 },
      { type: "选择题", content: `要使摆动加快，应该（ ）。
A. 加长摆线  B. 缩短摆线  C. 增加摆锤重量`, answer: "B", difficulty: 2 },
      { type: "简答题", content: `请说出制作水钟的步骤。`, answer: "1. 在容器底部扎一个小孔；2. 在容器上标好刻度；3. 装入水，记录水滴到每个刻度的时间；4. 根据刻度来计时。", difficulty: 3 },
      { type: "实验探究题", content: `小明做了一个摆，摆长20厘米，每分钟摆动40次。他想让摆每分钟摆动60次，应该怎样调整？
答：____________________`, answer: "应该缩短摆线的长度，摆线越短，摆动越快。", difficulty: 3 },
      { type: "判断题", content: `古代的日晷只能在白天有太阳时使用。（ ）`, answer: "√", difficulty: 1 }
    ],
  },

  {
    id: "sc-g5x-u4",
    unitName: "我们身边的物质",
    grade: 5,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: `下列变化中属于物理变化的是（ ）。
A. 铁生锈  B. 蜡烛融化  C. 木头燃烧`, answer: "B", difficulty: 1 },
      { type: "选择题", content: `下列变化中产生了新物质的是（ ）。
A. 把纸撕碎  B. 铁丝弯曲  C. 面包发霉`, answer: "C", difficulty: 2 },
      { type: "判断题", content: `物质的变化有些是缓慢的，有些是快速的。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `冰融化成水是化学变化。（ ）`, answer: "×", difficulty: 1 },
      { type: "填空题", content: `物质的变化可以分为（ ）变化和（ ）变化。`, answer: "物理；化学", difficulty: 1 },
      { type: "填空题", content: `物理变化的特点是（ ），化学变化的特点是（ ）。`, answer: "没有产生新物质；产生了新物质", difficulty: 2 },
      { type: "选择题", content: `下列现象中属于化学变化的是（ ）。
A. 玻璃破碎  B. 铁生锈  C. 水结冰`, answer: "B", difficulty: 1 },
      { type: "简答题", content: `请举出两个物理变化和两个化学变化的例子。`, answer: "物理变化：冰融化、铁丝弯曲；化学变化：铁生锈、木炭燃烧。（答案不唯一）", difficulty: 2 },
      { type: "实验探究题", content: `小明把白糖加热，白糖先融化，然后变成褐色，最后变成黑色的物质。这是物理变化还是化学变化？为什么？
答：____________________`, answer: "这是化学变化，因为产生了新的物质（黑色的碳），不仅仅是形态的改变。", difficulty: 3 },
      { type: "判断题", content: `化学变化中一定伴随着物理变化。（ ）`, answer: "√", difficulty: 2 }
    ],
  },

  {
    id: "sc-g5x-u5",
    unitName: "热",
    grade: 5,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: `热传递的方式有三种：传导、对流和（ ）。
A. 蒸发  B. 辐射  C. 融化`, answer: "B", difficulty: 1 },
      { type: "选择题", content: `下列材料中导热性最好的是（ ）。
A. 木头  B. 塑料  C. 金属`, answer: "C", difficulty: 1 },
      { type: "判断题", content: `热总是从温度高的地方传向温度低的地方。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `羽绒服能产生热量，所以穿羽绒服暖和。（ ）`, answer: "×", difficulty: 2 },
      { type: "填空题", content: `热传递有三种方式：（ ）、（ ）和辐射。`, answer: "传导；对流", difficulty: 2 },
      { type: "填空题", content: `容易导热的物体叫做热的（ ）导体，不容易导热的物体叫做热的（ ）导体。`, answer: "良；不良（或绝缘体）", difficulty: 2 },
      { type: "选择题", content: `下列哪种现象是对流？（ ）
A. 用铁勺搅热汤  B. 烧水时水上下翻滚  C. 太阳晒热地面`, answer: "B", difficulty: 2 },
      { type: "简答题", content: `请说出羽绒服为什么能保暖。`, answer: "羽绒服中的羽绒是热的不良导体，能阻止人体热量向外散失，所以能保暖。", difficulty: 2 },
      { type: "实验探究题", content: `小明把一根铜棒的一端放入热水中，用手摸另一端，过一会儿感觉铜棒变热了。这是什么传热方式？
答：____________________`, answer: "这是热传导。热量通过铜棒从热的一端传到了冷的一端。", difficulty: 2 },
      { type: "判断题", content: `不同材料的导热性能不同。（ ）`, answer: "√", difficulty: 1 }
    ],
  },

  {
    id: "sc-g6s-u4",
    unitName: "工具与技术",
    grade: 6,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: `下列工具中属于杠杆类的是（ ）。
A. 剪刀  B. 螺丝刀  C. 锤子`, answer: "A", difficulty: 1 },
      { type: "选择题", content: `使用工具可以（ ）。
A. 增加工作量  B. 省力或方便  C. 减少能量`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `所有的杠杆都能省力。（ ）`, answer: "×", difficulty: 2 },
      { type: "判断题", content: `斜面是一种简单机械。（ ）`, answer: "√", difficulty: 1 },
      { type: "填空题", content: `常见的简单机械有杠杆、（ ）、滑轮、（ ）和斜面等。`, answer: "轮轴；齿轮", difficulty: 2 },
      { type: "填空题", content: `杠杆有三个点：支点、（ ）和（ ）。`, answer: "力点；重点（阻力点）", difficulty: 2 },
      { type: "选择题", content: `下列哪种情况使用斜面最合适？（ ）
A. 切菜  B. 把重物推上车  C. 钉钉子`, answer: "B", difficulty: 1 },
      { type: "简答题", content: `请说出杠杆省力的条件。`, answer: "当动力臂大于阻力臂时，杠杆可以省力。即支点到动力作用点的距离大于支点到阻力作用点的距离。", difficulty: 3 },
      { type: "实验探究题", content: `小明用杠杆撬石头，发现石头很重撬不动。他应该怎样调整才能撬动石头？
答：____________________`, answer: "他应该把支点向石头方向移动，增大动力臂，这样就能用更小的力撬动石头。", difficulty: 2 },
      { type: "判断题", content: `轮轴由一个轮和一个轴组成，也是一种杠杆的变形。（ ）`, answer: "√", difficulty: 2 }
    ],
  },

  {
    id: "sc-g6s-u5",
    unitName: "能量",
    grade: 6,
    semester: "上",
    subject: "科学",
    questions: [
      { type: "选择题", content: `下列能源中属于可再生能源的是（ ）。
A. 煤  B. 太阳能  C. 石油`, answer: "B", difficulty: 1 },
      { type: "选择题", content: `电灯工作时把电能转化为（ ）和热能。
A. 光能  B. 声能  C. 动能`, answer: "A", difficulty: 1 },
      { type: "判断题", content: `能量可以从一种形式转化为另一种形式。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `能量可以凭空产生或消失。（ ）`, answer: "×", difficulty: 1 },
      { type: "填空题", content: `常见的能量形式有电能、光能、热能、（ ）、声能和（ ）。`, answer: "动能（机械能）；化学能", difficulty: 2 },
      { type: "填空题", content: `电风扇工作时，把（ ）能转化为（ ）能。`, answer: "电；动（风）", difficulty: 1 },
      { type: "选择题", content: `下列能量转化过程中，化学能转化为动能的是（ ）。
A. 用电灯照明  B. 汽车行驶  C. 太阳能热水器`, answer: "B", difficulty: 2 },
      { type: "简答题", content: `请说出两种节约能源的方法。`, answer: "1. 随手关灯；2. 使用节能电器；3. 多走路少开车；4. 利用太阳能等可再生能源。（答案不唯一）", difficulty: 2 },
      { type: "实验探究题", content: `小明用手搓一搓，手变热了。这是什么能量转化过程？
答：____________________`, answer: "这是动能转化为热能的过程。手搓动时消耗了动能，产生了热能，所以手变热了。", difficulty: 2 },
      { type: "判断题", content: `煤和石油是不可再生能源。（ ）`, answer: "√", difficulty: 1 }
    ],
  },

  {
    id: "sc-g6x-u4",
    unitName: "生物的多样性",
    grade: 6,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: `下列生物中属于植物的是（ ）。
A. 蘑菇  B. 松树  C. 海葵`, answer: "B", difficulty: 1 },
      { type: "选择题", content: `下列做法中有利于保护生物多样性的是（ ）。
A. 砍伐森林  B. 建立自然保护区  C. 乱捕滥猎`, answer: "B", difficulty: 1 },
      { type: "判断题", content: `生物多样性包括物种多样性、基因多样性和生态系统多样性。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `每一种生物的消失对人类都没有影响。（ ）`, answer: "×", difficulty: 1 },
      { type: "填空题", content: `生物可以分为（ ）、（ ）和（ ）三大类。`, answer: "动物；植物；微生物", difficulty: 1 },
      { type: "填空题", content: `目前已知地球上大约有（ ）多万种生物。`, answer: "870", difficulty: 2 },
      { type: "选择题", content: `下列动物中属于濒危动物的是（ ）。
A. 家猫  B. 大熊猫  C. 麻雀`, answer: "B", difficulty: 1 },
      { type: "简答题", content: `请说出保护生物多样性的意义。`, answer: "保护生物多样性可以维持生态平衡，保护基因资源，为人类提供食物、药物等资源，维持地球生态系统的稳定。", difficulty: 2 },
      { type: "实验探究题", content: `小明在校园里调查生物种类，发现校园里有各种树木、花草、昆虫和鸟类。他应该怎样记录调查结果？
答：____________________`, answer: "可以用表格、分类清单或照片等方式记录，按植物、动物、微生物分类整理，标注名称和数量。", difficulty: 2 },
      { type: "判断题", content: `基因多样性对物种的生存和进化非常重要。（ ）`, answer: "√", difficulty: 2 }
    ],
  },

  {
    id: "sc-g6x-u5",
    unitName: "地球的公转与自转",
    grade: 6,
    semester: "下",
    subject: "科学",
    questions: [
      { type: "选择题", content: `地球自转一周大约需要（ ）。
A. 12小时  B. 24小时  C. 365天`, answer: "B", difficulty: 1 },
      { type: "选择题", content: `地球公转一周大约需要（ ）。
A. 一个月  B. 半年  C. 一年`, answer: "C", difficulty: 1 },
      { type: "判断题", content: `地球自转产生了昼夜交替现象。（ ）`, answer: "√", difficulty: 1 },
      { type: "判断题", content: `地球公转产生了四季变化。（ ）`, answer: "√", difficulty: 1 },
      { type: "填空题", content: `地球自转的方向是自（ ）向（ ），公转的方向也是自（ ）向（ ）。`, answer: "西；东；西；东", difficulty: 2 },
      { type: "填空题", content: `当北半球是夏季时，太阳直射在（ ），北半球白天（ ），夜晚（ ）。`, answer: "北半球；长；短", difficulty: 2 },
      { type: "选择题", content: `北京白天最长的一天是（ ）。
A. 春分  B. 夏至  C. 冬至`, answer: "B", difficulty: 2 },
      { type: "简答题", content: `请解释为什么会有四季变化。`, answer: "因为地球是倾斜着绕太阳公转的，在公转过程中，太阳直射点在南北回归线之间移动，导致各地获得的太阳辐射量不同，从而产生四季变化。", difficulty: 3 },
      { type: "实验探究题", content: `小明用地球仪和手电筒模拟地球的自转。他发现地球仪被照亮的一半是白天，没有被照亮的一半是黑夜。当他转动地球仪时，观察到了什么？
答：____________________`, answer: "他观察到地球仪上被照亮和未被照亮的部分不断交替变化，模拟了昼夜交替现象。", difficulty: 2 },
      { type: "判断题", content: `地球是太阳系中唯一有生命存在的星球。（ ）`, answer: "√", difficulty: 1 }
    ],
  }

];

export function getUnitsByGradeAndSemester(grade: number, semester: '上' | '下', subject?: Subject): UnitQuestion[] {
  return unitTestData.filter(u => u.grade === grade && u.semester === semester && (subject === undefined || u.subject === subject));
}

/**
 * 获取所有年级学期组合
 */
export function getAllGradeSemesterCombinations(): { grade: number; semester: '上' | '下' }[] {
  const combos: { grade: number; semester: '上' | '下' }[] = [];
  for (let g = 1; g <= 6; g++) {
    combos.push({ grade: g, semester: '上' });
    combos.push({ grade: g, semester: '下' });
  }
  return combos;
}

/**
 * 从指定单元中随机抽取指定数量和难度的题目
 */
export function getRandomQuestions(
  unitIds: string[],
  count: number,
  difficulty?: 1 | 2 | 3,
  subject?: Subject,
): { type: string; content: string; answer: string; difficulty: 1 | 2 | 3; unitName: string }[] {
  // 收集所有符合条件的题目
  let pool: { type: string; content: string; answer: string; difficulty: 1 | 2 | 3; unitName: string }[] = [];

  for (const unitId of unitIds) {
    const unit = unitTestData.find(u => u.id === unitId);
    if (unit && (subject === undefined || unit.subject === subject)) {
      for (const q of unit.questions) {
        if (difficulty === undefined || q.difficulty === difficulty) {
          pool.push({ ...q, unitName: unit.unitName });
        }
      }
    }
  }

  // 如果指定难度后题目不足，则从所有难度中补充
  if (pool.length < count && difficulty !== undefined) {
    for (const unitId of unitIds) {
      const unit = unitTestData.find(u => u.id === unitId);
      if (unit && (subject === undefined || unit.subject === subject)) {
        for (const q of unit.questions) {
          if (q.difficulty !== difficulty && !pool.find(p => p.content === q.content)) {
            pool.push({ ...q, unitName: unit.unitName });
          }
        }
      }
    }
  }

  // 随机打乱
  pool.sort(() => Math.random() - 0.5);

  // 返回指定数量
  return pool.slice(0, count);
}
