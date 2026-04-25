import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/calligraphy";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "字帖生成器 - 免费在线田字格米字格练字 | 教材工具箱",
    description: "免费在线生成田字格、米字格、方格、横线格字帖，支持楷体、行楷、宋体、黑体等12种字体，自定义汉字内容，PDF下载即印即用，适合小学生练字使用。",
    keywords: "字帖生成器,田字格字帖,米字格字帖,练字模板,书法练习,汉字字帖,免费字帖,在线练字",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "字帖生成器 - 免费在线田字格米字格练字 | 教材工具箱",
      description: "免费在线生成田字格、米字格字帖，支持12种字体，自定义汉字内容，PDF下载即印即用。",
      type: "website",
    },
  };
}

export default function CalligraphyLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
