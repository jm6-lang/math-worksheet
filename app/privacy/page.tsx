import type { Metadata } from 'next';
import SiteLayout from '../_components/SiteLayout';

export const metadata: Metadata = {
  title: '隐私政策 - 教材工具箱',
  description: '教材工具箱隐私政策，说明我们如何收集、使用和保护您的信息。',
  alternates: {
    canonical: 'https://www.skillxm.cn/privacy',
  },
};

export default function PrivacyPage() {
  return (
    <SiteLayout>
      <div className="max-w-3xl mx-auto px-4 py-12">
        {/* 页面标题 */}
        <div className="text-center mb-12">
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">隐私政策</h1>
          <p className="text-gray-400">最后更新日期：2026年4月23日</p>
          <p className="text-gray-500 text-sm mt-2">生效日期：2026年4月23日</p>
        </div>

        {/* 概述 */}
        <section className="mb-8">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-xl">📋</span> 概述
            </h2>
            <p className="text-gray-300 leading-relaxed mb-3">
              教材工具箱（以下简称"我们"或"本站"）非常重视用户隐私保护。本隐私政策旨在向您说明我们如何收集、使用、存储和保护您的信息，以及您享有的相关权利。
            </p>
            <p className="text-gray-300 leading-relaxed">
              使用本站服务即表示您同意本隐私政策中描述的信息收集和使用方式。如果您不同意本政策，请停止使用本站服务。
            </p>
          </div>
        </section>

        {/* 信息收集 */}
        <section className="mb-8">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-xl">🔍</span> 一、我们收集的信息
            </h2>
            <div className="space-y-4 text-gray-300 leading-relaxed">
              <div>
                <h3 className="text-white font-medium mb-2">1.1 我们不收集个人信息</h3>
                <p>本站所有工具均在您的浏览器本地运行，不需要注册账号，不要求您提供姓名、邮箱、电话、地址等任何个人身份信息。您生成的练习卷、字帖、卡片等内容完全在本地处理，不会上传到我们的服务器。</p>
              </div>
              <div>
                <h3 className="text-white font-medium mb-2">1.2 自动收集的匿名数据</h3>
                <p>为了解网站的使用情况和改进服务质量，我们通过以下第三方服务自动收集一些匿名访问数据：</p>
                <ul className="list-disc list-inside mt-2 space-y-1 ml-4">
                  <li><strong>百度统计（Baidu Analytics）</strong>：收集访问者的IP地址（匿名化处理）、浏览器类型和版本、操作系统、屏幕分辨率、访问页面、访问时间、来源页面、停留时长等信息。</li>
                  <li><strong>Cloudflare</strong>：作为我们的CDN和托管服务商，可能收集HTTP请求日志、IP地址等基础网络信息，用于保障网站安全和性能优化。</li>
                </ul>
              </div>
              <div>
                <h3 className="text-white font-medium mb-2">1.3 Cookie 和本地存储</h3>
                <p>本站使用以下类型的 Cookie 和本地存储技术：</p>
                <ul className="list-disc list-inside mt-2 space-y-1 ml-4">
                  <li><strong>分析型 Cookie</strong>：由百度统计设置，用于识别回头访客和统计网站流量。典型 Cookie 名称包括 Hm_lvt_*、Hm_lpvt_* 等，有效期通常为1年。</li>
                  <li><strong>Cloudflare Cookie</strong>：包括 __cf_bm（安全防护）和 cf_clearance（人机验证），用于防范恶意访问和保障网站安全。</li>
                  <li><strong>本地存储（LocalStorage）</strong>：本站工具可能使用浏览器的 LocalStorage 保存您的偏好设置（如选择的年级、题型等），这些数据仅存储在您的设备上，不会同步到服务器。</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* 信息使用 */}
        <section className="mb-8">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-xl">📊</span> 二、信息使用方式
            </h2>
            <div className="space-y-4 text-gray-300 leading-relaxed">
              <div>
                <h3 className="text-white font-medium mb-2">2.1 匿名统计数据的使用</h3>
                <p>我们收集的匿名访问数据仅用于以下目的：</p>
                <ul className="list-disc list-inside mt-2 space-y-1 ml-4">
                  <li>了解网站的访问量和访问趋势</li>
                  <li>分析用户使用各工具的频率，优化工具开发优先级</li>
                  <li>发现和修复技术问题，提升用户体验</li>
                  <li>了解用户的地理分布和设备类型，优化页面适配</li>
                </ul>
              </div>
              <div>
                <h3 className="text-white font-medium mb-2">2.2 不用于商业营销</h3>
                <p>我们不会将收集到的任何数据用于商业营销、广告定向、用户画像或出售给第三方。本站承诺核心功能永久免费。</p>
              </div>
            </div>
          </div>
        </section>

        {/* 信息共享 */}
        <section className="mb-8">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-xl">🤝</span> 三、信息共享与披露
            </h2>
            <div className="space-y-4 text-gray-300 leading-relaxed">
              <p>由于我们不收集个人信息，因此不存在个人信息的共享和披露。但以下情况除外：</p>
              <ul className="list-disc list-inside space-y-1 ml-4">
                <li><strong>第三方服务提供商</strong>：如前所述，百度统计和 Cloudflare 作为我们的服务提供商，会接触到匿名访问数据。这些第三方均受各自的数据保护政策约束。</li>
                <li><strong>法律要求</strong>：如果法律法规、政府机关或司法机关要求，我们可能需要披露相关信息。在此情况下，我们将依法配合。</li>
                <li><strong>网站安全</strong>：如果发生安全事件（如黑客攻击），我们可能需要审查访问日志以排查问题。</li>
              </ul>
            </div>
          </div>
        </section>

        {/* 第三方服务 */}
        <section className="mb-8">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-xl">🔗</span> 四、第三方服务
            </h2>
            <div className="space-y-4 text-gray-300 leading-relaxed">
              <p>本站使用了以下第三方服务，它们各自有独立的隐私政策：</p>
              <div className="overflow-x-auto">
                <table className="w-full text-sm mt-2">
                  <thead>
                    <tr className="border-b border-white/10">
                      <th className="text-left text-white py-2 pr-4">服务名称</th>
                      <th className="text-left text-white py-2 pr-4">用途</th>
                      <th className="text-left text-white py-2">隐私政策</th>
                    </tr>
                  </thead>
                  <tbody className="text-gray-400">
                    <tr className="border-b border-white/5">
                      <td className="py-2 pr-4">百度统计</td>
                      <td className="py-2 pr-4">网站访问统计分析</td>
                      <td className="py-2"><a href="https://tongji.baidu.com/web/help/article?id=330" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">查看政策</a></td>
                    </tr>
                    <tr className="border-b border-white/5">
                      <td className="py-2 pr-4">Cloudflare</td>
                      <td className="py-2 pr-4">CDN加速、网站托管、安全防护</td>
                      <td className="py-2"><a href="https://www.cloudflare.com/zh-cn/privacypolicy/" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">查看政策</a></td>
                    </tr>
                    <tr className="border-b border-white/5">
                      <td className="py-2 pr-4">Google Fonts</td>
                      <td className="py-2 pr-4">网页字体加载</td>
                      <td className="py-2"><a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">查看政策</a></td>
                    </tr>
                    <tr>
                      <td className="py-2 pr-4">GitHub Pages</td>
                      <td className="py-2 pr-4">源代码托管</td>
                      <td className="py-2"><a href="https://docs.github.com/zh/site-policy/privacy-policies/github-privacy-statement" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">查看政策</a></td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p className="text-sm text-gray-400 mt-2">我们建议您查阅上述第三方服务的隐私政策，了解它们如何处理您的信息。我们不对第三方服务的隐私做法承担责任。</p>
            </div>
          </div>
        </section>

        {/* 数据安全 */}
        <section className="mb-8">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-xl">🛡️</span> 五、数据安全
            </h2>
            <div className="space-y-4 text-gray-300 leading-relaxed">
              <p>虽然我们不收集个人信息，但我们仍然采取了以下措施保障网站安全：</p>
              <ul className="list-disc list-inside space-y-1 ml-4">
                <li>全站 HTTPS 加密传输，通过 Cloudflare CDN 提供 HTTP/2 和 HTTP/3 支持</li>
                <li>Cloudflare 提供的 DDoS 防护和 Web 应用防火墙（WAF）</li>
                <li>所有工具在浏览器端本地运行，用户数据不上传服务器</li>
                <li>定期检查和更新依赖包，修复已知安全漏洞</li>
              </ul>
            </div>
          </div>
        </section>

        {/* 儿童隐私 */}
        <section className="mb-8">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-xl">👶</span> 六、儿童隐私保护
            </h2>
            <p className="text-gray-300 leading-relaxed mb-3">
              本站的服务对象包括未成年人（主要是小学生及其家长）。我们深知保护儿童在线隐私的重要性。
            </p>
            <ul className="list-disc list-inside space-y-1 ml-4 text-gray-300">
              <li>本站不收集任何14岁以下儿童的个人信息</li>
              <li>不要求用户注册账号或提供任何身份信息</li>
              <li>不设有社交功能、聊天功能或用户互动功能</li>
              <li>工具生成的所有内容均在本地处理，不会上传或存储</li>
            </ul>
            <p className="text-gray-300 leading-relaxed mt-3">
              如果您是家长或监护人，对本站的隐私保护有任何疑虑，欢迎随时联系我们。
            </p>
          </div>
        </section>

        {/* 用户权利 */}
        <section className="mb-8">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-xl">⚖️</span> 七、您的权利
            </h2>
            <p className="text-gray-300 leading-relaxed mb-3">由于我们不收集个人信息，您无需担心数据泄露或滥用。但您仍然享有以下权利：</p>
            <ul className="list-disc list-inside space-y-1 ml-4 text-gray-300">
              <li><strong>拒绝 Cookie</strong>：您可以通过浏览器设置拒绝或删除 Cookie。大多数浏览器允许您在"设置"中管理 Cookie 偏好。请注意，拒绝 Cookie 可能影响网站的部分统计功能，但不影响工具的核心使用。</li>
              <li><strong>清除本地数据</strong>：您可以随时清除浏览器中的 LocalStorage 数据。在浏览器设置中找到"清除浏览数据"选项即可。</li>
              <li><strong>联系我们</strong>：如果您对本隐私政策有任何疑问或建议，欢迎通过邮件与我们联系。</li>
            </ul>
          </div>
        </section>

        {/* 政策更新 */}
        <section className="mb-8">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-xl">📝</span> 八、政策更新
            </h2>
            <p className="text-gray-300 leading-relaxed mb-3">
              我们可能会不时更新本隐私政策。更新后的政策将在本页面发布，并修改"最后更新日期"。重大变更时，我们会在网站首页或博客发布通知。
            </p>
            <p className="text-gray-300 leading-relaxed">
              建议您定期查看本页面以了解最新的隐私保护措施。继续使用本站服务即表示您同意修改后的隐私政策。
            </p>
          </div>
        </section>

        {/* 联系信息 */}
        <section>
          <div className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 border border-blue-500/30 rounded-2xl p-8 text-center">
            <p className="text-gray-300 leading-relaxed mb-3">
              如果您对本隐私政策有任何疑问、意见或建议，请通过邮件联系我们：
            </p>
            <a
              href="mailto:644428571@qq.com"
              className="text-lg font-bold text-blue-400 hover:text-blue-300 transition-colors"
            >
              644428571@qq.com
            </a>
            <p className="text-gray-500 text-sm mt-4">
              我们会在收到您的邮件后尽快回复，通常不超过3个工作日。
            </p>
          </div>
        </section>
      </div>
    </SiteLayout>
  );
}
