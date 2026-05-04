import type { Metadata } from 'next';
import SiteLayout from '../_components/SiteLayout';

export const metadata: Metadata = {
  title: '联系我们 - 教材工具箱',
  description: '如果您有任何问题、建议或合作意向，欢迎通过邮件联系教材工具箱团队。',
  alternates: {
    canonical: 'https://www.skillxm.cn/contact',
  },
  openGraph: {
    url: 'https://www.skillxm.cn/contact/',
    title: '联系我们 - 教材工具箱',
    description: '如果您有任何问题、建议或合作意向，欢迎通过邮件联系教材工具箱团队。',
    type: 'website',
    images: [{ url: 'https://www.skillxm.cn/og-image.jpg', width: 1200, height: 630, alt: '教材工具箱' }],
  },
  twitter: {
    card: 'summary_large_image',
    title: '联系我们 - 教材工具箱',
    description: '如果您有任何问题、建议或合作意向，欢迎通过邮件联系教材工具箱团队。',
    images: ['https://www.skillxm.cn/og-image.jpg'],
  },
};

export default function ContactPage() {
  return (
    <SiteLayout>
      <div className="max-w-3xl mx-auto px-4 py-12">
        {/* 页面标题 */}
        <div className="text-center mb-12">
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">联系我们</h1>
          <p className="text-gray-400 text-lg">我们很乐意听取您的声音</p>
        </div>

        {/* 联系方式 */}
        <section className="mb-10">
          <div className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 border border-blue-500/30 rounded-2xl p-8 text-center">
            <div className="text-4xl mb-4">📧</div>
            <h2 className="text-xl font-bold text-white mb-3">邮箱联系</h2>
            <a
              href="mailto:lang@skillxm.cn"
              className="text-2xl font-bold text-blue-400 hover:text-blue-300 transition-colors"
            >
              lang@skillxm.cn
            </a>
            <p className="text-gray-300 mt-4 leading-relaxed">
              如果您有任何问题、建议或合作意向，欢迎通过邮件联系我们。我们会在1-3个工作日内回复您的邮件。
            </p>
          </div>
        </section>

        {/* 常见联系原因 */}
        <section className="mb-10">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
            <span className="text-2xl">📋</span> 常见联系原因
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {[
              {
                icon: '💡',
                title: '功能建议',
                desc: '希望我们增加新功能或改进现有功能，欢迎提出您的想法和建议。',
              },
              {
                icon: '🐛',
                title: 'Bug 反馈',
                desc: '在使用过程中遇到问题或发现异常，请告诉我们具体情况，我们会尽快修复。',
              },
              {
                icon: '🔗',
                title: '链接问题反馈',
                desc: '网站链接失效或内容有误，请告知我们以便及时修复。',
              },
              {
                icon: '🤝',
                title: '商务合作',
                desc: '如果您有合作意向，包括内容合作、技术合作或其他形式的合作，欢迎联系。',
              },
              {
                icon: '©️',
                title: '版权问题',
                desc: '如果您发现网站内容侵犯了您的版权，请提供相关证明，我们会及时处理。',
              },
              {
                icon: '❓',
                title: '其他问题',
                desc: '任何其他问题或咨询，我们都欢迎您通过邮件与我们沟通。',
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

        {/* 响应时间 */}
        <section className="mb-10">
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-8">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
              <span className="text-2xl">⏰</span> 响应时间
            </h2>
            <div className="flex items-center gap-4 mb-4">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span className="text-white font-medium">一般咨询</span>
                </div>
                <p className="text-gray-400 text-sm">1-3个工作日内回复</p>
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                  <span className="text-white font-medium">Bug 反馈</span>
                </div>
                <p className="text-gray-400 text-sm">1-2个工作日内回复</p>
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                  <span className="text-white font-medium">商务合作</span>
                </div>
                <p className="text-gray-400 text-sm">3-5个工作日内回复</p>
              </div>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              我们是一个小型团队，所有成员都是利用业余时间维护这个项目。虽然我们无法保证即时回复，但我们会认真阅读每一封邮件，并尽快给您答复。感谢您的理解和支持！
            </p>
          </div>
        </section>

        {/* 温馨提示 */}
        <section>
          <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-2xl p-8">
            <h2 className="text-xl font-bold text-yellow-400 mb-3 flex items-center gap-2">
              <span>💡</span> 温馨提示
            </h2>
            <ul className="space-y-2 text-gray-300 text-sm">
              <li className="flex items-start gap-2">
                <span className="text-yellow-400 mt-0.5">*</span>
                发送邮件时，请尽量详细描述您的问题或建议，以便我们更好地理解和处理。
              </li>
              <li className="flex items-start gap-2">
                <span className="text-yellow-400 mt-0.5">*</span>
                如果是Bug反馈，请附上浏览器类型、操作系统和问题截图，有助于我们快速定位问题。
              </li>
              <li className="flex items-start gap-2">
                <span className="text-yellow-400 mt-0.5">*</span>
                版权相关问题请提供版权证明材料，我们会在核实后及时处理。
              </li>
            </ul>
          </div>
        </section>
      </div>
    </SiteLayout>
  );
}
