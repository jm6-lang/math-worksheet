import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/mental-math";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "口算速练 - 在线口算计时挑战 | 教材工具箱",
    description: "免费在线口算速练，4个难度级别，计时挑战即时反馈，一二年级到五六年级全覆盖",
    keywords: "口算速练,口算练习,口算计时,速算训练,数学口算,口算题,在线口算",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "口算速练 - 免费在线口算计时挑战 | 教材工具箱",
      description: "免费在线口算速练，4个难度级别，计时挑战即时反馈，一二年级到五六年级全覆盖",
      type: "website",
    },
  };
}

export default function MentalMathLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
