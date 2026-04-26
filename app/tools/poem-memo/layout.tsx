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
    description: "免费在线生成古诗词默写练习卷，收录240首经典古诗词，覆盖小学1-6年级必背古诗词75+80首及课外拓展，支持填空默写、全诗默写、上下句默写三种模式，田字格/方格/横线格模板，PDF导出即印即用。",
    keywords: "古诗词默写,小学古诗词,必背古诗,古诗打印,默写练习,古诗词填空,唐诗三百首,宋词,古诗文默写",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "古诗词默写生成器 - 240首小学必背古诗词在线打印 | 教材工具箱",
      description: "收录240首经典古诗词，覆盖1-6年级必背古诗及课外拓展，三种默写模式，PDF导出即印即用。",
      type: "website",
    },
  };
}

export default function PoemMemoLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
