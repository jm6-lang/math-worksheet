import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: "教育博客 - 小学数学语文英语学习方法 | 教材工具箱",
  description: "小学数学语文英语学习方法文章集锦，覆盖一年级到六年级学习指南，包含口算训练、字帖练习、阅读理解、作文写作等实用教程。",
  keywords: "教育博客,小学学习方法,数学学习,语文学习,英语学习,教育资讯,小学教育,学习技巧",
  alternates: {
    canonical: 'https://www.skillxm.cn/blog',
  },
};

export default function BlogLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const blogSchema = {
    "@context": "https://schema.org",
    "@type": "Blog",
    "name": "教材工具箱教育博客",
    "description": "小学数学语文英语学习方法文章集锦",
    "url": "https://www.skillxm.cn/blog",
    "publisher": {
      "@type": "Organization",
      "name": "教材工具箱",
      "url": "https://www.skillxm.cn"
    }
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(blogSchema) }}
      />
      <div className="sr-only">
        <h1>教育博客 - 小学学习方法与教育资讯</h1>
        <p>小学数学语文英语学习方法文章集锦，覆盖一年级到六年级学习指南，包含口算训练、字帖练习、阅读理解、作文写作等实用教程。教材工具箱博客致力于为小学生家长和老师提供专业的教育资讯和学习方法指导。</p>
        <p>访问 <a href="https://www.skillxm.cn">教材工具箱</a> 获取更多免费教学工具。</p>
      </div>
      {children}
    </>
  );
}
