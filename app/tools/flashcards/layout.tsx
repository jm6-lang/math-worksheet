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
  return <>{children}</>;
}
