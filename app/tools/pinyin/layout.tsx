import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/pinyin";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "拼音学习工具 - 声母韵母/拼音注音/四线三格 | 教材工具箱",
    description: "免费拼音学习工具，声母韵母练习，四线三格标准格式PDF打印",
    keywords: "拼音练习,拼音注音,声母韵母,整体认读音节,拼音学习,小学拼音,拼音打印",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "拼音注音练习 - 免费在线拼音学习工具 | 教材工具箱",
      description: "免费拼音学习工具，声母韵母练习，四线三格标准格式PDF打印",
      type: "website",
      images: [{ url: "https://www.skillxm.cn/og-image.jpg", width: 1200, height: 630, alt: "教材工具箱" }],
    },
  };
}

export default function PinyinLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <div className="sr-only">
        <h1>拼音学习工具 - 声母韵母四线三格练习免费打印</h1>
        <p>免费拼音学习工具，声母韵母练习，四线三格标准格式PDF打印。教材工具箱提供专业的拼音书写练习工具，涵盖声母、韵母、整体认读音节全部内容，采用标准四线三格格式，帮助小学生规范拼音书写。</p>
        <h2>核心功能</h2>
        <ul>
          <li>声母练习：完整收录23个声母（b p m f d t n l g k h j q x zh ch sh r z c s y w），提供标准四线三格书写练习</li>
          <li>韵母练习：完整收录24个韵母（单韵母、复韵母、鼻韵母），帮助学生掌握韵母的正确书写方式</li>
          <li>整体认读音节：收录16个整体认读音节（zhi chi shi ri zi ci si yi wu yu ye yue yuan yin yun ying），方便专项练习</li>
          <li>四线三格标准格式：采用标准四线三格排版，与教材格式一致，培养学生规范的拼音书写习惯</li>
          <li>PDF导出：一键生成PDF文件，方便打印使用，支持A4纸张标准格式，可反复练习</li>
        </ul>
        <h2>适用对象</h2>
        <p>拼音学习工具适合小学一年级语文教师、幼儿园大班教师、学生家长以及从事拼音教学的培训机构使用。无论是课堂教学、课后辅导还是家庭早教，都可以通过本工具生成专业的拼音书写练习纸，帮助孩子打好拼音基础。</p>
        <p>访问 <a href="https://www.skillxm.cn">教材工具箱</a> 获取更多免费教学工具。</p>
      </div>
      {children}
    </>
  );
}
