import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/writing-template";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "作文模板生成器 - 看图写话/日记/作文格纸 | 教材工具箱",
    description: "免费生成小学作文格纸模板，涵盖看图写话、日记、作文格子纸等多种格式，支持田字格方格横线格，PDF导出A4打印。适合小学低年级到高年级写作练习。",
    keywords: "作文模板,看图写话,日记模板,作文格纸,小学作文,写作练习,作文纸打印,作文格子",
    alternates: { canonical: canonicalUrl },
    openGraph: { url: canonicalUrl, title: "作文模板生成器 - 教材工具箱", description: "免费生成小学作文格纸模板，涵盖看图写话、日记、作文格子纸等多种格式，支持田字格方格横线格，PDF导出A4打印。适合小学低年级到高年级写作练习。", images: [{ url: "https://www.skillxm.cn/og-image.jpg", width: 1200, height: 630, alt: "教材工具箱" }] },
  };
}

export default function WritingTemplateLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <div className="sr-only">
        <h2>作文模板生成器 - 小学作文格纸免费打印</h2>
        <p>免费生成小学作文格纸模板，看图写话、日记、作文格子纸。教材工具箱提供多种作文书写模板，涵盖小学低年级到高年级的写作练习需求，支持PDF格式免费打印。</p>
        <h2>核心功能</h2>
        <ul>
          <li>看图写话模板：专为小学低年级设计，配有图片区域和拼音格/田字格书写区域，适合一二年级看图写话练习</li>
          <li>日记模板：提供标准日记格式模板，包含日期、天气、星期等栏目，帮助学生养成写日记的习惯</li>
          <li>作文格纸：提供标准作文格子纸模板，支持不同行距和格子大小，适合各年级作文书写练习</li>
          <li>多种格式：支持田字格、方格、横线格等多种书写格式，满足不同年级和不同场景的写作需求</li>
        </ul>
        <h2>适用对象</h2>
        <p>作文模板生成器适合小学语文教师、学生家长以及小学各年级学生使用。无论是日常写作练习、考试作文训练还是家庭作业，都可以通过本工具快速生成规范的作文书写模板，培养孩子良好的书写习惯。</p>
        <p>访问 <a href="https://www.skillxm.cn">教材工具箱</a> 获取更多免费教学工具。</p>
      </div>
      {children}
    </>
  );
}
