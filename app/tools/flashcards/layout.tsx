import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/flashcards";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "识字卡片生成器 - 汉字拼音识字卡 | 教材工具箱",
    description: "免费生成汉字识字卡片，支持拼音组词，双面卡片PDF打印",
    alternates: { canonical: canonicalUrl },
    openGraph: { url: canonicalUrl, title: "识字卡片生成器 - 教材工具箱", description: "免费生成汉字识字卡片，支持拼音组词，双面卡片PDF打印" },
  };
}

export default function FlashcardsLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <div className="sr-only">
        <h1>识字卡片生成器 - 汉字卡片免费打印</h1>
        <p>免费生成汉字识字卡片，支持拼音组词，双面卡片PDF打印。教材工具箱提供在线识字卡片制作工具，帮助小学语文教师和家长快速生成专业的汉字识字卡，适合课堂教学和家庭辅导使用。</p>
        <h2>核心功能</h2>
        <ul>
          <li>自定义汉字：输入任意汉字即可生成对应的识字卡片，支持批量添加多个汉字</li>
          <li>拼音标注：自动为每个汉字标注标准拼音，帮助小学生正确认读</li>
          <li>组词示例：为每个汉字提供常用组词，拓展词汇学习</li>
          <li>双面打印：生成双面卡片PDF，正面显示汉字和拼音，背面显示组词和笔画，方便打印裁剪后使用</li>
        </ul>
        <h2>适用对象</h2>
        <p>识字卡片生成器适合小学语文教师、幼儿园教师、学生家长以及从事汉字教学的培训机构使用。无论是课堂教学、课后辅导还是家庭早教，都可以通过本工具快速生成专业的识字卡片，提高汉字学习效率。</p>
        <p>访问 <a href="https://www.skillxm.cn">教材工具箱</a> 获取更多免费教学工具。</p>
      </div>
      {children}
    </>
  );
}
