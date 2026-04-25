import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: "教育博客 - 小学数学语文英语学习方法 | 教材工具箱",
  alternates: {
    canonical: 'https://www.skillxm.cn/blog',
  },
};

export default function BlogLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
