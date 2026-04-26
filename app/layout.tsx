import type { Metadata } from "next";
import { Noto_Sans_SC } from "next/font/google";
import "./globals.css";
import { TOOLS, generateSchemaApps, generateSchemaBreadcrumbs, ACTIVE_TOOL_COUNT } from "@/lib/toolRegistry";


const notoSansSC = Noto_Sans_SC({
  // 不限制 subsets，next/font/google 默认下载完整字体包（含 CJK 中文字符）
  weight: ["400", "500", "700"],
  variable: "--font-noto-sans-sc",
  display: "swap",
  preload: true,
});

// 根布局保持静态预渲染，canonical 由各页面 layout 分别定义
export const dynamic = "force-static";

export const metadata: Metadata = {
  title: "教材工具箱 - 免费小学数学练习卷/字帖/口算题生成器",
  description: "免费在线教育工具，支持小学1-6年级数学练习卷、字帖、拼音卡片、数独、作文模板等，PDF导出即印即用，无需注册完全免费。",
  keywords: "小学练习卷生成器,字帖生成器,数学练习题,作文模板,拼音学习工具,免费教育资源,小学数学,字帖打印,数独游戏,口算练习,识字卡片,英语字帖,在线教育工具,免费打印",
  openGraph: {
    title: "教材工具箱 - 免费小学数学练习卷生成器/字帖/作文模板",
    description: "免费在线教育工具，支持小学1-6年级数学练习卷、字帖、拼音卡片、数独、作文模板等，PDF导出即印即用，无需注册完全免费。",
    type: "website",
    url: "https://www.skillxm.cn",
    siteName: "教材工具箱",
    locale: "zh_CN",
    images: [
      {
        url: "https://www.skillxm.cn/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "教材工具箱 - 免费在线教育工具",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "教材工具箱 - 免费小学数学练习卷生成器/字帖/作文模板",
    description: "免费在线教育工具，支持小学1-6年级数学练习卷、字帖、拼音卡片、数独、作文模板等，PDF导出即印即用，无需注册完全免费。",
    images: ["https://www.skillxm.cn/og-image.jpg"],
  },
  alternates: {
    canonical: "https://www.skillxm.cn",
  },
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "16x16 32x32 48x48 256x256", type: "image/x-icon" },
      { url: "/favicon.svg", type: "image/svg+xml" },
    ],
    apple: "/favicons/apple-touch-icon.png",
  },
  manifest: "/manifest.json",
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
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const schemaOrg = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebSite",
        name: "教材工具箱",
        url: "https://www.skillxm.cn",
        description: "免费在线教育工具集合，包括数学练习卷生成器、字帖生成器、英语字帖、数独游戏、口算速练、识字卡片、作文模板、拼音注音，支持PDF导出打印",
        inLanguage: "zh-CN",
        potentialAction: {
          "@type": "SearchAction",
          target: "https://www.skillxm.cn/search?q={search_term_string}",
          "query-input": "required name=search_term_string"
        },
        publisher: {
          "@id": "https://www.skillxm.cn/#organization"
        },
      },
      {
        "@type": "Organization",
        "@id": "https://www.skillxm.cn/#organization",
        name: "教材工具箱",
        url: "https://www.skillxm.cn",
        logo: {
          "@type": "ImageObject",
          url: "https://www.skillxm.cn/og-image.jpg",
        },
        description: `免费在线教育工具集合，为小学生和家长提供数学练习卷、字帖、数独等${ACTIVE_TOOL_COUNT}款实用工具`,
        address: {
          "@type": "PostalAddress",
          addressCountry: "CN",
          addressRegion: "浙江",
          addressLocality: "绍兴",
        },
        geo: {
          "@type": "GeoCoordinates",
          latitude: 30.0,
          longitude: 120.5833,
        },
        areaServed: {
          "@type": "Country",
          name: "CN",
        },
        contactPoint: {
          "@type": "ContactPoint",
          email: "644428571@qq.com",
          contactType: "customer support",
          availableLanguage: "Chinese",
        },
      },
      ...generateSchemaApps(),
      ...generateSchemaBreadcrumbs(),
      {
        "@type": "HowTo",
        "name": "如何使用数学练习卷生成器",
        "description": "使用教材工具箱的数学练习卷生成器，只需5步即可生成可打印的数学练习卷",
        "totalTime": "PT3M",
        "step": [
          {
            "@type": "HowToStep",
            "name": "选择题型和年级",
            "text": "在工具页面选择需要的题型（加法、减法、乘法、除法等）和对应的年级（1-6年级）"
          },
          {
            "@type": "HowToStep",
            "name": "设置题目数量和数字范围",
            "text": "设定每次生成的题目数量（10/20/50/100道）和数字范围（10以内到10000以内）"
          },
          {
            "@type": "HowToStep",
            "name": "选择模板样式",
            "text": "从田字格、方格纸、横线格、空白纸4种模板中选择适合的打印样式"
          },
          {
            "@type": "HowToStep",
            "name": "点击生成",
            "text": "点击「立即出题」按钮，系统会随机生成不重复的数学练习卷"
          },
          {
            "@type": "HowToStep",
            "name": "预览并导出PDF",
            "text": "预览生成的练习卷，确认无误后点击「下载PDF」或「直接打印」按钮"
          }
        ]
      },
      {
        "@type": "FAQPage",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "教材工具箱是免费的吗？",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "是的，教材工具箱所有功能完全免费使用，无需注册账号，不收取任何费用。我们承诺永久免费，让每个孩子都能享受到优质的教育工具。"
            }
          },
          {
            "@type": "Question",
            "name": "生成的练习卷和字帖可以打印吗？",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "可以。所有工具都支持一键导出PDF文件，您可以直接打印使用。PDF文件格式规范，打印效果清晰，适合A4纸打印。"
            }
          },
          {
            "@type": "Question",
            "name": "支持哪些年级？",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "主要面向小学1-6年级学生，部分工具（如数独游戏、作文模板）也适合初中生和成年人使用。数学练习卷支持按年级选择题型和难度。"
            }
          },
          {
            "@type": "Question",
            "name": "需要注册账号吗？",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "不需要。所有工具打开即用，无需注册、登录或提供任何个人信息。您的数据完全在浏览器本地处理，不会上传到服务器。"
            }
          },
          {
            "@type": "Question",
            "name": "题目会重复吗？",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "不会。每次生成的练习卷都是随机出题，同一配置下每次结果都不同，避免机械重复，真正达到练习效果。"
            }
          },
          {
            "@type": "Question",
            "name": "手机上能用吗？",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "可以。网站采用响应式设计，手机、平板、电脑都能正常使用。不过在手机上生成PDF后，建议发送到电脑或连接打印机进行打印。"
            }
          }
        ]
      },
    ],
  };

  return (
    <html lang="zh-CN" className={notoSansSC.className}>
      <head>
        <meta name="baidu-site-verification" content="codeva-nVZFsgvPZu" />
        <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
        <link rel="icon" type="image/x-icon" href="/favicon.ico" sizes="any" />
        <link rel="apple-touch-icon" href="/favicons/apple-touch-icon.png" />
        <meta name="msapplication-TileImage" content="/favicons/favicon-32x32.png" />
        <meta name="msapplication-TileColor" content="#1e40af" />
        <meta name="theme-color" content="#1e40af" />

        {/* hreflang GEO 信号 */}
        <link rel="alternate" hrefLang="zh-CN" href="https://www.skillxm.cn/" />

        {/* dns-prefetch 第三方资源 */}
        <link rel="dns-prefetch" href="https://hm.baidu.com" />
        <link rel="dns-prefetch" href="https://pagead2.googlesyndication.com" />
        <link rel="dns-prefetch" href="https://zz.bdstatic.com" />

        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schemaOrg) }}
        />

        {/* Google AdSense */}
        <script
          async
          src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4710405779358793"
          crossOrigin="anonymous"
        />

        {/* 百度主动推送 */}
        <script
          dangerouslySetInnerHTML={{
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
            `,
          }}
        />
      </head>
      <body className="min-h-screen antialiased">
        {children}
        <script
          dangerouslySetInnerHTML={{
            __html: `
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?b1c5ccce83f4e80c4c12dea6bd544723";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();`,
          }}
 />
      </body>
    </html>
  );
}
