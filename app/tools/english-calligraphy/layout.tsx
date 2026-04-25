import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/english-calligraphy";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "英语字帖生成器 - 免费四线三格英语练习 | 教材工具箱",
    description: "免费在线生成英语字帖，标准四线三格格式，支持手写体、印刷体等多种英文字体，自定义单词和句子内容，PDF下载即印即用，适合小学生英语书写练习。",
    keywords: "英语字帖,四线三格,英语练习,英文字帖,英语书写,英语打印,免费英语字帖",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "英语字帖生成器 - 免费四线三格英语练习 | 教材工具箱",
      description: "免费在线生成英语字帖，标准四线三格格式，支持多种字体，PDF下载即印即用。",
      type: "website",
    },
  };
}

export default function EnglishCalligraphyLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
