import type { Metadata } from 'next';
import SiteLayout from '../_components/SiteLayout';

export const metadata: Metadata = {
  title: '关于我们 - 教材工具箱',
  description: '了解教材工具箱的建站初衷、使命和团队。我们致力于为每个孩子提供免费、好用的在线教育工具。',
  alternates: {
    canonical: 'https://www.skillxm.cn/about',
  },
};

export default function AboutPage() {
  return (
    <SiteLayout>
      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* 页面标题 */}
        <div className="text-center mb-12">
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">关于教材工具箱</h1>
          <p className="text-gray-400 text-lg">一群家长开发者，为孩子们打造的免费教育工具平台</p>
        </div>

        {/* 建站初衷 */}
        <section className="mb-12">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-2xl">💡</span> 建站初衷
            </h2>
            <p className="text-gray-300 leading-relaxed mb-4">
              作为家长，我们都希望给孩子最好的教育资源。然而在实际生活中，我们发现市面上的教育工具存在诸多问题：要么收费昂贵，动辄几百上千元的会员费让普通家庭望而却步；要么功能单一，一个工具只能做一件事，需要安装十几个APP才能满足基本的学习需求。
            </p>
            <p className="text-gray-300 leading-relaxed">
              更让人头疼的是，很多工具充斥着弹窗和推广链接，严重干扰孩子的学习体验。于是，我们决定自己动手，开发一套免费、好用的在线教育工具，让每一个孩子都能平等地享受优质的教育资源。
            </p>
          </div>
        </section>

        {/* 我们的使命 */}
        <section className="mb-12">
          <div className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 border border-blue-500/30 rounded-2xl p-8">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-2xl">🎯</span> 我们的使命
            </h2>
            <p className="text-gray-200 leading-relaxed text-lg">
              让每个孩子都能免费使用优质的教育工具，不受经济条件限制。
            </p>
            <p className="text-gray-300 leading-relaxed mt-4">
              我们相信，教育公平是社会公平的基石。每一个孩子都值得拥有好的学习工具，无论他们的家庭经济状况如何。通过互联网技术，我们可以打破资源的壁垒，让优质教育工具触手可及。
            </p>
          </div>
        </section>

        {/* 我们的工具 */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
            <span className="text-2xl">🛠️</span> 我们的工具
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              {
                icon: '🧮',
                name: '数学练习卷',
                desc: '一键生成小学1-6年级数学练习卷，支持加减乘除、竖式计算、填空题等11种题型。每次随机出题，可自定义数字范围和题目数量，导出PDF直接打印。',
              },
              {
                icon: '✍️',
                name: '字帖生成器',
                desc: '在线生成田字格、米字格、方格等多种格式的字帖。支持楷体、宋体、黑体等多种字体，可自定义练习内容，适合小学生日常练字使用。',
              },
              {
                icon: '🔤',
                name: '英语字帖',
                desc: '生成标准四线三格英语练习纸，支持英文字母、单词和句子的书写练习。可调整行高和字体大小，帮助孩子养成良好的英文书写习惯。',
              },
              {
                icon: '🧩',
                name: '数独游戏',
                desc: '在线数独游戏，支持简单、中等、困难、专家四个难度等级。内置数字键盘和笔记功能，自动校验答案，是锻炼逻辑思维的好帮手。',
              },
              {
                icon: '⚡',
                name: '口算速练',
                desc: '在线计时口算练习工具，支持4个难度级别和多种题目数量。即时反馈对错，完成后显示成绩统计和错题回顾，有效提升口算速度和准确率。',
              },
              {
                icon: '🃏',
                name: '识字卡片',
                desc: '免费在线生成识字卡片，支持自定义汉字、拼音和组词。提供年级预设字库，可导出PDF打印制作实体卡片，方便随时随地学习。',
              },
              {
                icon: '📝',
                name: '作文模板',
                desc: '提供看图写话、日记、书信、读后感等多种作文模板。选择年级和稿纸样式后可实时预览效果，辅助孩子完成不同类型的写作练习。',
              },
              {
                icon: '📝',
                name: '拼音注音',
                desc: '汉字拼音注音练习工具，支持声母、韵母和整体认读音节的专项练习。自动标注拼音，帮助孩子掌握正确的发音和拼读规则。',
              },
            ].map((tool) => (
              <div
                key={tool.name}
                className="bg-slate-800/50 border border-white/10 rounded-xl p-6 hover:border-white/20 transition-colors"
              >
                <div className="flex items-start gap-4">
                  <span className="text-3xl shrink-0">{tool.icon}</span>
                  <div>
                    <h3 className="text-lg font-bold text-white mb-2">{tool.name}</h3>
                    <p className="text-gray-400 text-sm leading-relaxed">{tool.desc}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* 我们的承诺 */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
            <span className="text-2xl">🤝</span> 我们的承诺
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {[
              {
                icon: '🆓',
                title: '永久免费',
                desc: '所有功能永久免费使用，不设任何付费门槛，不搞会员制，不收订阅费。',
              },
              {
                icon: '🛡️',
                title: '安全可靠',
                desc: '所有数据在浏览器本地处理，不上传任何个人信息，保护用户隐私安全。',
              },
              {
                icon: '🔒',
                title: '保护用户隐私',
                desc: '不收集个人信息，不需要注册登录，不追踪用户行为，保护每一位用户的隐私。',
              },
              {
                icon: '🔄',
                title: '持续更新',
                desc: '团队持续开发和优化工具功能，根据用户反馈不断改进，定期推出新工具。',
              },
            ].map((item) => (
              <div
                key={item.title}
                className="bg-slate-800/50 border border-white/10 rounded-xl p-6 hover:border-white/20 transition-colors"
              >
                <span className="text-2xl">{item.icon}</span>
                <h3 className="text-lg font-bold text-white mt-3 mb-2">{item.title}</h3>
                <p className="text-gray-400 text-sm leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* 团队介绍 */}
        <section className="mb-12">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-2xl">👥</span> 团队介绍
            </h2>
            <p className="text-gray-300 leading-relaxed mb-4">
              教材工具箱由一群热爱教育和技术的开发者创建。我们的团队成员来自不同的行业背景，有程序员、设计师、教师，但有一个共同的身份——我们多数成员本身也是家长。
            </p>
            <p className="text-gray-300 leading-relaxed">
              正因为如此，我们深刻理解家长在辅导孩子学习时的痛点和需求。我们开发的每一个工具，都源自真实的家庭教育场景。我们不仅是在写代码，更是在为自己的孩子和千千万万的孩子创造更好的学习条件。
            </p>
          </div>
        </section>

        {/* 技术保障 */}
        <section className="mb-12">
          <div className="bg-slate-800 rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-2xl">⚙️</span>
              <h3 className="text-white text-lg font-bold">技术保障</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-slate-700/50 rounded-lg p-4 text-center">
                <div className="text-3xl mb-2">⚡</div>
                <div className="text-white font-medium">极速加载</div>
                <div className="text-slate-400 text-sm">全球CDN加速，毫秒级响应</div>
              </div>
              <div className="bg-slate-700/50 rounded-lg p-4 text-center">
                <div className="text-3xl mb-2">🛡️</div>
                <div className="text-white font-medium">安全可靠</div>
                <div className="text-slate-400 text-sm">数据本地处理，隐私安全保障</div>
              </div>
              <div className="bg-slate-700/50 rounded-lg p-4 text-center">
                <div className="text-3xl mb-2">📱</div>
                <div className="text-white font-medium">全端适配</div>
                <div className="text-slate-400 text-sm">手机平板电脑均可流畅使用</div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </SiteLayout>
  );
}
