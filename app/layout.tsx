import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "算个题吧 - 数学练习纸生成器",
  description: "免费在线数学练习卷生成器，支持加减乘除竖式填空题，生成可打印PDF，完全免费免登录",
  keywords: "数学练习, 口算题生成, 打印练习卷, 小学数学, 出题器",
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
          <meta name="baidu-site-verification" content="codeva-nVZFsgvPZu" />
  </head>
      <body className="min-h-screen antialiased">
        {children}
      </body>
    </html>
  );
}
