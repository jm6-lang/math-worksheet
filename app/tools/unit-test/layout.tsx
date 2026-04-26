import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/unit-test";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "单元测试卷生成器 - 小学数学期中期末试卷 | 教材工具箱",
    description: "免费在线生成小学数学单元测试卷，按教材单元出题，覆盖人教版/北师大版1-6年级上下册，支持期中/期末/单元测试，PDF导出即印即用。",
    keywords: "单元测试卷,期中试卷,期末试卷,小学数学试卷,数学测试题,试卷生成器",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "单元测试卷生成器 - 小学数学期中期末试卷 | 教材工具箱",
      description: "免费在线生成小学数学单元测试卷，按教材单元出题，PDF导出即印即用。",
      type: "website",
    },
  };
}

export default function UnitTestLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
