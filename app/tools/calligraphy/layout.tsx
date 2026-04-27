import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/calligraphy";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "免费字帖生成器 - 田字格/米字格/楷体字帖 | 教材工具箱",
    description: "免费在线生成田字格米字格汉字字帖，支持楷体宋体黑体，自定义内容输入，PDF导出A4打印",
    keywords: "字帖生成器,田字格字帖,米字格字帖,练字模板,书法练习,汉字字帖,免费字帖,在线练字",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "字帖生成器 - 免费在线田字格米字格练字 | 教材工具箱",
      description: "免费在线生成田字格米字格汉字字帖，支持楷体宋体黑体，自定义内容输入，PDF导出A4打印",
      type: "website",
    },
  };
}

export default function CalligraphyLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      {/* 服务端渲染的 SEO 内容 -- 搜索引擎可直接抓取 */}
      <div className="sr-only">
        <h1>字帖生成器 - 田字格米字格汉字字帖免费打印</h1>
        <p>免费在线生成田字格米字格汉字字帖，支持楷体宋体黑体，自定义内容输入，PDF导出A4打印。适合小学生练字、书法初学者描红练习，输入任意汉字即可生成标准字帖模板，支持笔画顺序展示，一键打印高清字帖。</p>
        <h2>核心功能</h2>
        <ul>
          <li>四种格子样式：田字格、米字格、回宫格、空白格，满足不同练字阶段需求</li>
          <li>三种字体选择：楷体、宋体、黑体，适合不同书写风格练习</li>
          <li>自定义内容输入：支持输入任意汉字、词语、古诗、课文内容生成字帖</li>
          <li>PDF导出A4打印：一键生成高清PDF文件，A4纸张直接打印，字迹清晰</li>
          <li>描红与临摹模式：支持描红练习和空白临摹两种模式切换</li>
          <li>完全免费：无需注册登录，打开即用，不限制使用次数</li>
        </ul>
        <h2>适用对象</h2>
        <p>小学1-6年级学生、书法初学者、汉字书写需要提升的中小学生、语文教师布置练字作业。适合日常练字、书法兴趣培养、汉字书写规范训练等场景。</p>
        <p>访问 <a href="https://www.skillxm.cn">教材工具箱</a> 获取更多免费教学工具，包括数学练习卷生成器、英语字帖、数独游戏、口算速练等。</p>
      </div>
      {children}
    </>
  );
}
