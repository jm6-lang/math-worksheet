import type { Metadata } from 'next';
import SiteLayout from '../_components/SiteLayout';

export const metadata: Metadata = {
  title: '服务条款 - 教材工具箱',
  description: '教材工具箱服务条款，包括使用规则、知识产权、免责声明和隐私保护等内容。',
  alternates: {
    canonical: 'https://www.skillxm.cn/terms',
  },
};

export default function TermsPage() {
  return (
    <SiteLayout>
      <div className="max-w-3xl mx-auto px-4 py-12">
        {/* 页面标题 */}
        <div className="text-center mb-12">
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">服务条款</h1>
          <p className="text-gray-400">最后更新日期：2026年4月</p>
        </div>

        {/* 服务说明 */}
        <section className="mb-8">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-xl">📖</span> 一、服务说明
            </h2>
            <p className="text-gray-300 leading-relaxed mb-3">
              欢迎使用教材工具箱（以下简称&ldquo;本站&rdquo;）。本站提供免费的在线教育工具服务，包括但不限于数学练习卷生成器、字帖生成器、英语字帖、数独游戏、口算速练、识字卡片、作文模板和拼音注音等工具。
            </p>
            <p className="text-gray-300 leading-relaxed">
              本站所有工具均可免费使用，无需注册账号，无需付费。使用本站服务即表示您同意遵守以下服务条款。
            </p>
          </div>
        </section>

        {/* 使用规则 */}
        <section className="mb-8">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-xl">📋</span> 二、使用规则
            </h2>
            <div className="space-y-4 text-gray-300 leading-relaxed">
              <div>
                <h3 className="text-white font-medium mb-2">2.1 合法使用</h3>
                <p>您在使用本站服务时，应遵守中华人民共和国相关法律法规。不得利用本站工具从事任何违法或侵权活动。</p>
              </div>
              <div>
                <h3 className="text-white font-medium mb-2">2.2 禁止商业用途</h3>
                <p>本站提供的工具和服务仅供个人学习和教育用途。未经书面授权，禁止将本站工具或生成的内容用于商业目的，包括但不限于销售、转售、商业培训等。</p>
              </div>
              <div>
                <h3 className="text-white font-medium mb-2">2.3 禁止爬取数据</h3>
                <p>未经许可，禁止使用爬虫、机器人或其他自动化工具对本站进行数据抓取、内容采集或大量访问。如需引用本站内容，请注明出处并提供链接。</p>
              </div>
              <div>
                <h3 className="text-white font-medium mb-2">2.4 禁止滥用</h3>
                <p>禁止对本站进行恶意攻击、干扰正常运营、或试图获取未经授权的系统访问权限。</p>
              </div>
            </div>
          </div>
        </section>

        {/* 知识产权 */}
        <section className="mb-8">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-xl">©️</span> 三、知识产权
            </h2>
            <div className="space-y-4 text-gray-300 leading-relaxed">
              <div>
                <h3 className="text-white font-medium mb-2">3.1 工具代码</h3>
                <p>本站所有工具的源代码、设计、界面和功能均归教材工具箱所有，受中华人民共和国著作权法保护。未经授权，不得复制、修改、分发本站代码。</p>
              </div>
              <div>
                <h3 className="text-white font-medium mb-2">3.2 用户生成内容</h3>
                <p>用户使用本站工具生成的练习卷、字帖、卡片等内容，其知识产权归用户所有。用户可自由使用、打印和分享这些内容。</p>
              </div>
              <div>
                <h3 className="text-white font-medium mb-2">3.3 网站内容</h3>
                <p>本站的文字内容、图片、图标、布局设计等均受知识产权法保护。未经许可，不得擅自复制或转载。</p>
              </div>
            </div>
          </div>
        </section>

        {/* 免责声明 */}
        <section className="mb-8">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-xl">⚠️</span> 四、免责声明
            </h2>
            <div className="space-y-4 text-gray-300 leading-relaxed">
              <div>
                <h3 className="text-white font-medium mb-2">4.1 内容准确性</h3>
                <p>本站尽力确保工具生成内容的准确性和正确性，但不对内容的准确性作出任何明示或暗示的保证。数学练习卷的题目和答案可能存在错误，建议家长和教师在使用时进行核实。</p>
              </div>
              <div>
                <h3 className="text-white font-medium mb-2">4.2 损失免责</h3>
                <p>因使用本站工具而造成的任何直接或间接损失，本站不承担任何责任。本站提供的工具仅供参考和学习使用，不能替代专业的教育教学。</p>
              </div>
              <div>
                <h3 className="text-white font-medium mb-2">4.3 服务可用性</h3>
                <p>本站可能会因服务器维护、系统升级或其他原因暂时中断服务，不对服务中断造成的损失承担责任。我们会尽力保持服务的稳定性和可用性。</p>
              </div>
            </div>
          </div>
        </section>

        {/* 隐私保护 */}
        <section className="mb-8">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-xl">🔒</span> 五、隐私保护
            </h2>
            <div className="space-y-4 text-gray-300 leading-relaxed">
              <div>
                <h3 className="text-white font-medium mb-2">5.1 信息收集</h3>
                <p>本站不收集用户的个人信息，不需要注册账号，不要求提供姓名、邮箱、电话等个人数据。所有工具均在浏览器端运行，数据不会上传到服务器。</p>
              </div>
              <div>
                <h3 className="text-white font-medium mb-2">5.2 访问统计</h3>
                <p>本站使用百度统计（Baidu Analytics）对网站访问量进行统计分析。百度统计会收集访问者的IP地址、浏览器类型、访问页面等匿名数据，仅用于了解网站使用情况，不会关联到具体个人。</p>
              </div>
              <div>
                <h3 className="text-white font-medium mb-2">5.3 Cookie 使用</h3>
                <p>百度统计可能会在您的浏览器中设置Cookie，用于识别回头访客。您可以通过浏览器设置拒绝Cookie，但这可能影响统计数据的准确性。</p>
              </div>
            </div>
          </div>
        </section>

        {/* 资源免责 */}
        <section className="mb-8">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-xl">📎</span> 六、资源免责
            </h2>
            <p className="text-gray-300 leading-relaxed mb-3">
              本站&ldquo;免费资源&rdquo;板块提供的资源链接来自网络公开分享，仅供学习和交流使用。我们不对这些资源的完整性、准确性和合法性负责。
            </p>
            <p className="text-gray-300 leading-relaxed mb-3">
              如果您是资源的版权所有者，且不希望您的资源在本站展示，请通过邮件联系我们，我们会在核实后及时删除相关链接。
            </p>
            <p className="text-gray-300 leading-relaxed">
              使用本站链接的资源时，请遵守原资源的版权声明和使用条款。
            </p>
          </div>
        </section>

        {/* 条款修改 */}
        <section className="mb-8">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-xl">📝</span> 七、条款修改
            </h2>
            <p className="text-gray-300 leading-relaxed mb-3">
              教材工具箱保留随时修改本服务条款的权利。修改后的条款将在本页面发布，并更新&ldquo;最后更新日期&rdquo;。继续使用本站服务即表示您同意修改后的条款。
            </p>
            <p className="text-gray-300 leading-relaxed">
              建议您定期查看本页面，以了解最新的服务条款。如有任何疑问，请通过邮件与我们联系。
            </p>
          </div>
        </section>

        {/* 联系信息 */}
        <section>
          <div className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 border border-blue-500/30 rounded-2xl p-8 text-center">
            <p className="text-gray-300 leading-relaxed mb-3">
              如果您对本服务条款有任何疑问，请通过邮件联系我们：
            </p>
            <a
              href="mailto:lang@skillxm.cn"
              className="text-lg font-bold text-blue-400 hover:text-blue-300 transition-colors"
            >
              lang@skillxm.cn
            </a>
          </div>
        </section>
      </div>
    </SiteLayout>
  );
}
