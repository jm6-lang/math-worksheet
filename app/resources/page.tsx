export const metadata = {
  title: '免费资源 - 教材工具箱',
  description: '汇集优质学习资源，网盘资料免费分享，涵盖各学科学习资料、工具软件等',
};

export default function ResourcesPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* 顶部导航占位 */}
      <div className="h-16"></div>

      {/* 页面标题 */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <div className="text-6xl mb-4">🎁</div>
          <h1 className="text-4xl md:text-5xl font-black text-white mb-4">
            免费资源中心
          </h1>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            汇集优质学习资源，持续更新中
          </p>
        </div>

        {/* 资源列表 */}
        <div className="space-y-6 max-w-4xl mx-auto">
          {/* 空状态 */}
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-12 text-center">
            <div className="text-6xl mb-4">📦</div>
            <h2 className="text-2xl font-bold text-white mb-3">资源整理中...</h2>
            <p className="text-gray-400 mb-6">
              我们正在收集整理各类优质资源<br />
              包括学习资料、工具软件、课程视频等<br />
              近期将陆续上线
            </p>
            <div className="inline-flex items-center gap-2 bg-amber-500/20 text-amber-400 px-6 py-3 rounded-xl border border-amber-500/30">
              <span className="text-2xl">⏰</span>
              <span className="font-medium">即将上线，敬请期待</span>
            </div>
          </div>

          {/* 提示卡片 */}
          <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-2xl p-6">
            <div className="flex items-start gap-4">
              <div className="text-3xl">💡</div>
              <div>
                <h3 className="text-lg font-bold text-white mb-2">如何获取资源？</h3>
                <p className="text-gray-400 text-sm leading-relaxed">
                  资源上线后，你可以直接点击对应的网盘链接进行下载。<br />
                  部分资源可能需要输入提取码，我们会在资源详情中注明。<br />
                  如有问题，欢迎通过赞助页面联系我们。
                </p>
              </div>
            </div>
          </div>

          {/* 期待列表 */}
          <div className="bg-slate-800/50 border border-white/10 rounded-2xl p-6">
            <h3 className="text-lg font-bold text-white mb-4">🔜 即将上线</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {[
                { icon: '📚', text: '小学语数英同步资料' },
                { icon: '🎬', text: '思维训练课程视频' },
                { icon: '📱', text: '学习工具软件合集' },
                { icon: '📝', text: '各年级试卷真题' },
                { icon: '🎨', text: '兴趣特长学习资料' },
                { icon: '🌏', text: '英语启蒙资源' },
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-3 text-gray-300 text-sm">
                  <span className="text-lg">{item.icon}</span>
                  <span>{item.text}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* 底部提示 */}
        <div className="text-center mt-12 text-gray-500 text-sm">
          <p>如果你有优质资源想要分享，欢迎联系我们</p>
        </div>
      </div>
    </div>
  );
}
