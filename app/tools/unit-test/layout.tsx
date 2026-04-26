import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/unit-test";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "小学单元测试卷生成器 - 数语英科全科试卷免费打印 | 教材工具箱",
    description: "免费生成小学1-6年级单元测试卷，数学语文英语科学四科，305个单元PDF打印",
    keywords: "单元测试卷,期中试卷,期末试卷,小学数学试卷,小学语文试卷,小学英语试卷,小学科学试卷,试卷生成器,免费试卷打印",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "小学单元测试卷生成器 - 数语英科全科试卷免费打印 | 教材工具箱",
      description: "免费生成小学1-6年级单元测试卷，数学语文英语科学四科，305个单元PDF打印",
      type: "website",
    },
  };
}

export default function UnitTestLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
