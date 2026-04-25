import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: "教育博客 - 小学数学语文英语学习方法 | 教材工具箱",
  description: "小学数学语文英语学习方法文章集锦，覆盖一年级到六年级学习指南，包含口算训练、字帖练习、阅读理解、作文写作等实用教程。",
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
