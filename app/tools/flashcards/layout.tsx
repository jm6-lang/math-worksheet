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
    description: "免费在线生成识字卡片，支持自定义汉字、拼音、组词，可打印制作实体卡片",
    alternates: { canonical: canonicalUrl },
    openGraph: { url: canonicalUrl, title: "识字卡片生成器 - 教材工具箱", description: "免费在线生成识字卡片，支持自定义汉字、拼音、组词，可打印制作实体卡片" },
  };
}

export default function FlashcardsLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
