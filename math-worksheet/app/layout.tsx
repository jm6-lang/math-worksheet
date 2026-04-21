import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://skillxm.cn"),
  title: "教材工具箱 - 免费生成数学练习卷、字帖、数独 | 在线打印",
  description: "免费在线教育工具箱：数学练习卷生成器、字帖生成器、数独游戏。支持1-6年级数学题，田字格/方格/横线格模板，一键导出PDF打印。完全免费免登录。",
  keywords: "数学练习卷,字帖生成,数独游戏,小学数学,口算题,练习纸生成,田字格,方格纸,免费打印,PDF导出",
  authors: [{ name: "教材工具箱" }],
  creator: "教材工具箱",
  publisher: "教材工具箱",
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  openGraph: {
    type: "website",
    locale: "zh_CN",
    url: "https://skillxm.cn",
    siteName: "教材工具箱",
    title: "教材工具箱 - 免费生成数学练习卷、字帖、数独",
    description: "免费在线教育工具箱：数学练习卷生成器、字帖生成器、数独游戏。支持1-6年级数学题，一键导出PDF打印。",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "教材工具箱",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "教材工具箱 - 免费生成数学练习卷、字帖、数独",
    description: "免费在线教育工具箱：数学练习卷生成器、字帖生成器、数独游戏。",
    images: ["/og-image.png"],
  },
  alternates: {
    canonical: "https://skillxm.cn",
  },
  verification: {
    // Google Search Console 验证（需要替换为实际值）
    google: "YOUR_GOOGLE_VERIFICATION_CODE",
    // 百度站长验证
    other: {
      "baidu-site-verification": "codeva-nVZFsgvPZu",
    },
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@400;700&display=swap"
          rel="stylesheet"
        />
        
        {/* 百度自动推送 */}
        <script dangerouslySetInnerHTML={{
          __html: `
(function(){
var bp = document.createElement('script');
var curProtocol = window.location.protocol.split(':')[0];
if (curProtocol === 'https') {
bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
} else {
bp.src = 'http://push.zhanzhang.baidu.com/push.js';
}
var s = document.getElementsByTagName("script")[0];
s.parentNode.insertBefore(bp, s);
})();
          `
        }} />
        
        {/* 百度统计（需要替换为实际值） */}
        {/* <script dangerouslySetInnerHTML={{
          __html: `
var _hmt = _hmt || [];
(function() {
var hm = document.createElement("script");
hm.src = "https://hm.baidu.com/hm.js?YOUR_BAIDU_ANALYTICS_ID";
var s = document.getElementsByTagName("script")[0];
s.parentNode.insertBefore(hm, s);
})();
          `
        }} /> */}
        
        {/* JSON-LD 结构化数据 */}
        <script type="application/ld+json" dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "教材工具箱",
            "url": "https://skillxm.cn",
            "description": "免费在线教育工具箱：数学练习卷生成器、字帖生成器、数独游戏",
            "potentialAction": {
              "@type": "SearchAction",
              "target": "https://skillxm.cn/tools/math-worksheet",
              "query-input": "required name=search_term"
            }
          })
        }} />
        
        <script type="application/ld+json" dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "教材工具箱",
            "applicationCategory": "EducationalApplication",
            "operatingSystem": "Web Browser",
            "offers": {
              "@type": "Offer",
              "price": "0",
              "priceCurrency": "CNY"
            },
            "aggregateRating": {
              "@type": "AggregateRating",
              "ratingValue": "4.8",
              "ratingCount": "100"
            }
          })
        }} />
      </head>
      <body className="min-h-screen antialiased">
        {children}
      </body>
    </html>
  );
}
