import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/writing-template";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "作文模板生成器 - 看图写话/日记/作文格纸 | 教材工具箱",
    description: "免费在线生成作文模板，支持看图写话、日记、书信等多种格式，适合小学生写作练习",
    alternates: { canonical: canonicalUrl },
    openGraph: { url: canonicalUrl, title: "作文模板生成器 - 教材工具箱", description: "免费在线生成作文模板，支持看图写话、日记、书信等多种格式" },
  };
}

export default function WritingTemplateLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
