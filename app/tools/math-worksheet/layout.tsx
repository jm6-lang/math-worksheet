import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/math-worksheet";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "数学练习卷生成器 - 免费在线出题打印 | 教材工具箱",
    description: "免费在线生成小学数学练习卷，支持加减乘除、竖式计算、分数运算、一元一次方程等11种题型，田字格/方格/横线格多模板，PDF即印即用，1-6年级全覆盖。",
    keywords: "数学练习卷,数学出题器,小学数学,加减乘除,竖式计算,分数运算,数学打印,免费数学题",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "数学练习卷生成器 - 免费在线出题打印 | 教材工具箱",
      description: "免费在线生成小学数学练习卷，支持加减乘除、竖式计算、分数运算等11种题型，PDF即印即用，1-6年级全覆盖。",
      type: "website",
    },
  };
}

export default function MathWorksheetLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
