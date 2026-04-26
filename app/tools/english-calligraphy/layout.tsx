import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/english-calligraphy";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "英文字帖生成器 - 四线三格英文书写练习 | 教材工具箱",
    description: "免费生成四线三格英文字帖，多种字体，PDF导出A4打印",
    keywords: "英语字帖,四线三格,英语练习,英文字帖,英语书写,英语打印,免费英语字帖",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "英语字帖生成器 - 免费四线三格英语练习 | 教材工具箱",
      description: "免费生成四线三格英文字帖，多种字体，PDF导出A4打印",
      type: "website",
    },
  };
}

export default function EnglishCalligraphyLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
