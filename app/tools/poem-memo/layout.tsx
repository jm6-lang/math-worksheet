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
    },
  };
}

export default function PoemMemoLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
