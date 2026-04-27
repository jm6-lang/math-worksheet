import type { Metadata } from "next";

const canonicalUrl = "https://www.skillxm.cn/tools/content-generator";

export const metadata: Metadata = {
  title: "种草文案生成器 - 一键生成多平台推广文案 | 教材工具箱",
  description: "免费AI种草文案生成器，一键生成知乎/小红书/百家号/微信公众号等平台的推广文案，支持多种风格和长度，SEO关键词自动嵌入。",
  keywords: "种草文案,推广文案,文案生成器,小红书文案,知乎文案,营销文案",
  alternates: { canonical: canonicalUrl },
  openGraph: {
    url: canonicalUrl,
    title: "种草文案生成器 - 一键生成多平台推广文案 | 教材工具箱",
    description: "免费AI种草文案生成器，一键生成知乎/小红书/百家号/微信公众号等平台的推广文案。",
    type: "website",
  },
};
export default function Layout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
