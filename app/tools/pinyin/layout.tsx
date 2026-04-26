import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/pinyin";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "拼音学习工具 - 声母韵母/拼音注音/四线三格 | 教材工具箱",
    description: "免费拼音学习工具，声母韵母练习，四线三格标准格式PDF打印",
    keywords: "拼音练习,拼音注音,声母韵母,整体认读音节,拼音学习,小学拼音,拼音打印",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "拼音注音练习 - 免费在线拼音学习工具 | 教材工具箱",
      description: "免费拼音学习工具，声母韵母练习，四线三格标准格式PDF打印",
      type: "website",
    },
  };
}

export default function PinyinLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
