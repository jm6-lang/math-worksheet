import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        <div className="text-8xl mb-4">🔍</div>
        <h1 className="text-3xl font-bold text-gray-800 mb-2">页面未找到</h1>
        <p className="text-gray-500 mb-8">
          您访问的页面不存在或已被移除。请检查网址是否正确，或返回首页浏览。
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/"
            className="inline-flex items-center justify-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            返回首页
          </Link>
          <Link
            href="/blog"
            className="inline-flex items-center justify-center px-6 py-3 bg-white text-blue-600 font-medium rounded-lg border border-blue-600 hover:bg-blue-50 transition-colors"
          >
            浏览博客
          </Link>
        </div>
        <div className="mt-8 pt-8 border-t border-gray-200">
          <p className="text-sm text-gray-400 mb-3">热门工具</p>
          <div className="flex flex-wrap justify-center gap-3">
            <Link href="/tools/math-worksheet" className="text-sm text-blue-500 hover:underline">数学练习卷</Link>
            <Link href="/tools/calligraphy" className="text-sm text-blue-500 hover:underline">字帖生成器</Link>
            <Link href="/tools/sudoku" className="text-sm text-blue-500 hover:underline">数独游戏</Link>
            <Link href="/tools/pinyin" className="text-sm text-blue-500 hover:underline">拼音学习</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
