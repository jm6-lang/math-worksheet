import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/math-worksheet";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "小学数学练习卷生成器 - 1-6年级免费在线出题PDF打印 | 教材工具箱",
    description: "免费在线生成小学1-6年级数学练习卷，支持加减乘除、竖式计算、填空题、应用题等11种题型，随机出题PDF打印",
    keywords: "数学练习卷,数学出题器,小学数学,加减乘除,竖式计算,分数运算,数学打印,免费数学题",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "数学练习卷生成器 - 免费在线出题打印 | 教材工具箱",
      description: "免费在线生成小学1-6年级数学练习卷，支持加减乘除、竖式计算、填空题、应用题等11种题型，随机出题PDF打印",
      type: "website",
      images: [{ url: "https://www.skillxm.cn/og-image.jpg", width: 1200, height: 630, alt: "教材工具箱" }],
  };
}

export default function MathWorksheetLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      {/* 服务端渲染的 SEO 内容 -- 搜索引擎可直接抓取 */}
      <div className="sr-only">
        <h1>小学数学练习卷生成器 - 免费在线出题打印</h1>
        <p>免费在线生成小学1-6年级数学练习卷，支持加减乘除竖式计算、分数方程等11种题型，随机出题PDF打印。教师和家长可一键生成个性化数学练习题，覆盖一年级到六年级全学段，支持简单、中等、困难三档难度调节，答案页独立打印，方便批改。</p>
        <h2>核心功能</h2>
        <ul>
          <li>11种题型：加法、减法、乘法、除法、加减混合、乘除混合、四则混合、竖式计算、填空题、比较大小、应用题</li>
          <li>1-6年级全覆盖：自动匹配各年级知识点范围，一年级20以内加减法到六年级分数方程</li>
          <li>三档难度调节：简单、中等、困难，满足不同学习阶段需求</li>
          <li>PDF导出打印：一键生成A4格式PDF文件，答案页独立分离，方便教师批改</li>
          <li>随机出题：每次生成题目不重复，避免学生死记硬背</li>
          <li>完全免费：无需注册登录，打开即用，不限制使用次数</li>
        </ul>
        <h2>适用对象</h2>
        <p>小学1-6年级学生家长、小学数学教师、课后辅导机构老师。适合日常数学练习、单元测试出题、期末复习巩固、假期作业布置等场景使用。</p>
        <p>访问 <a href="https://www.skillxm.cn">教材工具箱</a> 获取更多免费教学工具，包括字帖生成器、英语字帖、数独游戏、口算速练等。</p>
      </div>
      {children}
    </>
  );
}
