import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/poem-memo";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "古诗词默写生成器 - 240首小学必背古诗词在线打印 | 教材工具箱",
    description: "免费生成小学必背古诗词默写练习卷，240首经典古诗词，三种默写模式PDF打印",
    keywords: "古诗词默写,小学古诗词,必背古诗,古诗打印,默写练习,古诗词填空,唐诗三百首,宋词,古诗文默写",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "古诗词默写生成器 - 240首小学必背古诗词在线打印 | 教材工具箱",
      description: "免费生成小学必背古诗词默写练习卷，240首经典古诗词，三种默写模式PDF打印",
      type: "website",
      images: [{ url: "https://www.skillxm.cn/og-image.jpg", width: 1200, height: 630, alt: "教材工具箱" }],
  };
}

export default function PoemMemoLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <div className="sr-only">
        <h1>古诗词默写生成器 - 240首小学必背古诗词在线打印</h1>
        <p>免费生成小学必背古诗词默写练习卷，240首经典古诗词，三种默写模式PDF打印。教材工具箱收录小学1-6年级全部必背古诗词，支持填空默写、全诗默写、上下句默写等多种练习方式，是语文教师和学生家长必备的古诗词复习工具。</p>
        <h2>核心功能</h2>
        <ul>
          <li>240首古诗词：完整收录小学阶段必背古诗词，涵盖唐诗、宋词、元曲等经典篇目</li>
          <li>1-6年级覆盖：按年级分类，一年级到六年级的古诗词均可选择，方便针对性练习</li>
          <li>填空默写/全诗默写/上下句默写：三种默写模式，从易到难，满足不同学习阶段的需求。填空默写适合初学阶段，全诗默写适合巩固复习，上下句默写适合考试冲刺</li>
          <li>田字格/方格/横线格：支持田字格、方格、横线格三种书写格式，适应不同年级的书写要求</li>
          <li>PDF导出：一键生成PDF文件，方便打印使用，支持A4纸张标准格式</li>
        </ul>
        <h2>适用对象</h2>
        <p>古诗词默写生成器适合小学语文教师、学生家长以及小学各年级学生使用。无论是日常古诗词背诵检查、期中期末考试复习还是假期作业布置，都可以通过本工具快速生成专业的古诗词默写练习卷，提高古诗词学习效率。</p>
        <p>访问 <a href="https://www.skillxm.cn">教材工具箱</a> 获取更多免费教学工具。</p>
      </div>
      {children}
    </>
  );
}
