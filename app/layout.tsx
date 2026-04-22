import type { Metadata } from "next";
import "./globals.css";
import Script from "next/script";

export const metadata: Metadata = {
  title: "算个题吧 - 数学练习卷生成器",
  description: "免费生成数学练习卷，支持加减乘除、竖式、分数、方程等题目类型，可生成打印PDF，全年级覆盖",
  keywords: "数学练习, 练习卷生成器, 打印练习纸, 小学数学, 分数运算",
  openGraph: {
    title: "算个题吧 - 数学练习卷生成器",
    description: "免费生成数学练习卷，支持加减乘除、竖式、分数、方程等题目类型，可生成打印PDF，全年级覆盖",
    type: "website",
    url: "https://www.skillxm.cn",
    siteName: "算个题吧",
    locale: "zh_CN",
  },
  twitter: {
    card: "summary_large_image",
    title: "算个题吧 - 数学练习卷生成器",
    description: "免费生成数学练习卷，支持加减乘除、竖式、分数、方程等题目类型，可生成打印PDF，全年级覆盖",
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
};

// 根布局保持静态预渲染，canonical 由各页面 layout 分别定义
export const dynamic = "force-static";

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
        name: "算个题吧",
        url: "https://www.skillxm.cn",
        description: "免费生成数学练习卷，支持加减乘除、竖式、分数、方程等题目类型，可生成打印PDF，全年级覆盖",
        inLanguage: "zh-CN",
        publisher: {
          "@type": "Organization",
          name: "算个题吧",
          url: "https://www.skillxm.cn",
        },
        potentialAction: {
          "@type": "SearchAction",
          target: {
            "@type": "EntryPoint",
            urlTemplate: "https://www.skillxm.cn/?q={search_term_string}",
          },
          "query-input": "required name=search_term_string",
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
        "@type": "BreadcrumbList",
        itemListElement: [
          {
            "@type": "ListItem",
            position: 1,
            name: "首页",
            item: "https://www.skillxm.cn",
          },
          {
            "@type": "ListItem",
            position: 2,
            name: "数学练习卷",
            item: "https://www.skillxm.cn/tools/math-worksheet",
          },
          {
            "@type": "ListItem",
            position: 2,
            name: "字帖生成器",
            item: "https://www.skillxm.cn/tools/calligraphy",
          },
          {
            "@type": "ListItem",
            position: 2,
            name: "英语字帖生成器",
            item: "https://www.skillxm.cn/tools/english-calligraphy",
          },
          {
            "@type": "ListItem",
            position: 2,
            name: "拼音练习生成器",
            item: "https://www.skillxm.cn/tools/pinyin",
          },
          {
            "@type": "ListItem",
            position: 2,
            name: "数独游戏",
            item: "https://www.skillxm.cn/tools/sudoku",
          },
        ],
      },
    ],
  };

  return (
    <html lang="zh-CN">
      <head>
        <meta name="baidu-site-verification" content="codeva-nVZFsgvPZu" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@400;700&display=swap"
          rel="stylesheet"
        />
        {/* Favicon sizes */}
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
      </head>
      <body className="min-h-screen antialiased">
        {children}
        <Script src="https://push.zhanzhang.baidu.com/push.js" strategy="afterInteractive" />
      </body>
    </html>
  );
}
