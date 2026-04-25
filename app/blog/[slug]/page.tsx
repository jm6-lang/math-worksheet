import { notFound } from 'next/navigation';
import { articles } from '../data';
import type { Metadata } from 'next';
import BlogPostPage from '../_components/BlogPostPage';

export function generateStaticParams() {
  return articles.map(a => ({ slug: a.id }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const article = articles.find(a => a.id === slug);
  if (!article) return { title: '文章未找到' };
  return {
    title: `${article.title} | 教材工具箱`,
    description: article.description,
    authors: [{ name: '教材工具箱' }],
    alternates: {
      canonical: `https://www.skillxm.cn/blog/${slug}`,
    },
    openGraph: {
      title: article.title,
      description: article.description,
      type: 'article',
      publishedTime: article.date,
      authors: ['教材工具箱'],
    },
  };
}

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const article = articles.find(a => a.id === slug);
  if (!article) notFound();

  const articleSchema = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": article.title,
    "description": article.description,
    "datePublished": article.date,
    "dateModified": article.date,
    "author": {
      "@id": "https://www.skillxm.cn/#organization"
    },
    "publisher": {
      "@id": "https://www.skillxm.cn/#organization"
    },
    "mainEntityOfPage": {
      "@type": "WebPage",
      "@id": `https://www.skillxm.cn/blog/${slug}`
    }
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(articleSchema) }}
      />
      <BlogPostPage slug={slug} />
    </>
  );
}
