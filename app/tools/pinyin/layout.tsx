import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/pinyin";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "拼音注音练习 - 免费在线拼音学习工具 | 教材工具箱",
    description: "免费在线拼音注音练习工具，支持声母、韵母、整体认读音节练习，四线三格标准格式，自动标注拼音，PDF下载即印即用，适合小学一年级拼音学习。",
    keywords: "拼音练习,拼音注音,声母韵母,整体认读音节,拼音学习,小学拼音,拼音打印",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "拼音注音练习 - 免费在线拼音学习工具 | 教材工具箱",
      description: "免费在线拼音注音练习，支持声母韵母整体认读音节，PDF下载即印即用。",
      type: "website",
    },
  };
}

export default function PinyinLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
