import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/sudoku";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "数独游戏在线玩 - 入门/进阶/挑战三档难度 | 教材工具箱",
    description: "免费在线数独游戏，支持简单、中等、困难三个难度级别，计时挑战，笔记模式，自动校验错误，锻炼逻辑思维能力，适合各年龄段玩家。",
    keywords: "数独游戏,在线数独,数独挑战,逻辑训练,益智游戏,免费数独,数独解题",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "数独游戏 - 免费在线数独挑战 | 教材工具箱",
      description: "免费在线数独游戏，支持三个难度级别，计时挑战，笔记模式，锻炼逻辑思维能力。",
      type: "website",
    },
  };
}

export default function SudokuLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
