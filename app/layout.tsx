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
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
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
      </head>
      <body className="min-h-screen antialiased">
        {children}
        <Script src="https://push.zhanzhang.baidu.com/push.js" strategy="afterInteractive" />
      </body>
    </html>
  );
}