import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/calligraphy";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "免费字帖生成器 - 田字格/米字格/楷体字帖 | 教材工具箱",
    description: "免费在线生成田字格米字格汉字字帖，支持楷体宋体黑体，自定义内容输入，PDF导出A4打印",
    keywords: "字帖生成器,田字格字帖,米字格字帖,练字模板,书法练习,汉字字帖,免费字帖,在线练字",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "字帖生成器 - 免费在线田字格米字格练字 | 教材工具箱",
      description: "免费在线生成田字格米字格汉字字帖，支持楷体宋体黑体，自定义内容输入，PDF导出A4打印",
      type: "website",
    },
  };
}

export default function CalligraphyLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
