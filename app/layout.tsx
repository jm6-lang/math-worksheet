import type { Metadata } from "next";
import { Noto_Sans_SC } from "next/font/google";
import "./globals.css";


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
  title: "教材工具箱 - 免费在线教育工具，数学练习卷、字帖、数独、作文模板",
  description: "教材工具箱提供免费的在线教育工具，包括数学练习卷生成器、字帖生成器、英语字帖、数独游戏、口算速练、识字卡片、作文模板、拼音注音，支持PDF导出打印，适合小学生学习使用。",
  keywords: "教材工具箱,数学练习卷,字帖生成器,英语字帖,数独游戏,口算速练,识字卡片,作文模板,拼音注音,小学数学,免费打印,PDF导出,在线学习工具",
  openGraph: {
    title: "教材工具箱 - 免费在线教育工具",
    description: "免费在线生成数学练习卷、字帖、英语字帖、数独、口算速练、识字卡片、作文模板等，支持PDF导出打印，全年级覆盖",
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
    title: "教材工具箱 - 免费在线教育工具",
    description: "免费在线生成数学练习卷、字帖、英语字帖、数独、口算速练、识字卡片、作文模板等，支持PDF导出打印",
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
        publisher: {
          "@type": "Organization",
          name: "教材工具箱",
          url: "https://www.skillxm.cn",
        },
      },
      {
        "@type": "SoftwareApplication",
        name: "数学练习卷生成器",
        url: "https://www.skillxm.cn/tools/math-worksheet",
        description: "免费在线生成小学数学练习卷，支持加减乘除竖式、分数、方程等题型，一键打印PDF",
        applicationCategory: "EducationApplication",
        operatingSystem: "Web Browser",
        offers: {
          "@type": "Offer",
          price: "0",
          priceCurrency: "CNY",
        },
        aggregateRating: {
          "@type": "AggregateRating",
          ratingValue: "4.9",
          ratingCount: "328",
        },
      },
      {
        "@type": "SoftwareApplication",
        name: "字帖生成器",
        url: "https://www.skillxm.cn/tools/calligraphy",
        description: "在线生成田字格/米字格字帖，四种格子样式可选，支持直接打印，适合小学生练字",
        applicationCategory: "EducationApplication",
        operatingSystem: "Web Browser",
        offers: {
          "@type": "Offer",
          price: "0",
          priceCurrency: "CNY",
        },
      },
      {
        "@type": "SoftwareApplication",
        name: "英语字帖生成器",
        url: "https://www.skillxm.cn/tools/english-calligraphy",
        description: "输入英文单词或句子，自动生成四线三格练习纸，支持多种字体和行高，一键打印",
        applicationCategory: "EducationApplication",
        operatingSystem: "Web Browser",
        offers: {
          "@type": "Offer",
          price: "0",
          priceCurrency: "CNY",
        },
      },
      {
        "@type": "SoftwareApplication",
        name: "拼音练习生成器",
        url: "https://www.skillxm.cn/tools/pinyin",
        description: "生成拼音四线三格练习纸，支持声母、韵母、整体认读音节，一键打印PDF",
        applicationCategory: "EducationApplication",
        operatingSystem: "Web Browser",
        offers: {
          "@type": "Offer",
          price: "0",
          priceCurrency: "CNY",
        },
      },
      {
        "@type": "SoftwareApplication",
        name: "数独游戏",
        url: "https://www.skillxm.cn/tools/sudoku",
        description: "在线数独游戏，支持多个难度等级，数字键盘输入，适合各年龄段益智训练",
        applicationCategory: "GameApplication",
        operatingSystem: "Web Browser",
        offers: {
          "@type": "Offer",
          price: "0",
          priceCurrency: "CNY",
        },
      },
      {
        "@type": "SoftwareApplication",
        name: "口算速练",
        url: "https://www.skillxm.cn/tools/mental-math",
        description: "在线口算计时练习，支持4个难度级别，即时反馈，适合小学生数学速算训练",
        applicationCategory: "EducationApplication",
        operatingSystem: "Web Browser",
        offers: {
          "@type": "Offer",
          price: "0",
          priceCurrency: "CNY",
        },
      },
      {
        "@type": "SoftwareApplication",
        name: "识字卡片生成器",
        url: "https://www.skillxm.cn/tools/flashcards",
        description: "免费在线生成识字卡片，支持自定义汉字、拼音、组词，可打印制作实体卡片",
        applicationCategory: "EducationApplication",
        operatingSystem: "Web Browser",
        offers: {
          "@type": "Offer",
          price: "0",
          priceCurrency: "CNY",
        },
      },
      {
        "@type": "SoftwareApplication",
        name: "作文模板生成器",
        url: "https://www.skillxm.cn/tools/writing-template",
        description: "免费在线生成作文模板，支持看图写话、日记、书信等多种格式，适合小学生写作练习",
        applicationCategory: "EducationApplication",
        operatingSystem: "Web Browser",
        offers: {
          "@type": "Offer",
          price: "0",
          priceCurrency: "CNY",
        },
      },
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "首页", item: "https://www.skillxm.cn" },
          { "@type": "ListItem", position: 2, name: "数学练习卷", item: "https://www.skillxm.cn/tools/math-worksheet" },
        ],
      },
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "首页", item: "https://www.skillxm.cn" },
          { "@type": "ListItem", position: 2, name: "字帖生成器", item: "https://www.skillxm.cn/tools/calligraphy" },
        ],
      },
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "首页", item: "https://www.skillxm.cn" },
          { "@type": "ListItem", position: 2, name: "英语字帖生成器", item: "https://www.skillxm.cn/tools/english-calligraphy" },
        ],
      },
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "首页", item: "https://www.skillxm.cn" },
          { "@type": "ListItem", position: 2, name: "拼音练习生成器", item: "https://www.skillxm.cn/tools/pinyin" },
        ],
      },
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "首页", item: "https://www.skillxm.cn" },
          { "@type": "ListItem", position: 2, name: "数独游戏", item: "https://www.skillxm.cn/tools/sudoku" },
        ],
      },
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "首页", item: "https://www.skillxm.cn" },
          { "@type": "ListItem", position: 2, name: "口算速练", item: "https://www.skillxm.cn/tools/mental-math" },
        ],
      },
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "首页", item: "https://www.skillxm.cn" },
          { "@type": "ListItem", position: 2, name: "识字卡片生成器", item: "https://www.skillxm.cn/tools/flashcards" },
        ],
      },
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "首页", item: "https://www.skillxm.cn" },
          { "@type": "ListItem", position: 2, name: "作文模板生成器", item: "https://www.skillxm.cn/tools/writing-template" },
        ],
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
