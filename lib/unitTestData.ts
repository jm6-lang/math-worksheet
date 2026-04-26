/**
 * 单元测试卷题库数据 - 人教版小学数学
 * 按年级、学期、单元组织，每个单元至少8道题
 */

export interface UnitQuestion {
  id: string;
  unitName: string;
  grade: number;
  semester: '上' | '下';
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
];

/**
 * 根据年级和学期获取可用单元列表
 */
export function getUnitsByGradeAndSemester(grade: number, semester: '上' | '下'): UnitQuestion[] {
  return unitTestData.filter(u => u.grade === grade && u.semester === semester);
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
): { type: string; content: string; answer: string; difficulty: 1 | 2 | 3; unitName: string }[] {
  // 收集所有符合条件的题目
  let pool: { type: string; content: string; answer: string; difficulty: 1 | 2 | 3; unitName: string }[] = [];

  for (const unitId of unitIds) {
    const unit = unitTestData.find(u => u.id === unitId);
    if (unit) {
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
      if (unit) {
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
