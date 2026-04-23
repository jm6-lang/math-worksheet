import { notFound } from 'next/navigation';
import { articles } from '../data';
import type { Metadata } from 'next';
import BlogPostPage from '../_components/BlogPostPage';

export function generateStaticParams() {
  return articles.map(a => ({ slug: a.id }));
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const article = articles.find(a => a.id === params.slug);
  if (!article) return { title: '文章未找到' };
  return {
    title: `${article.title} - 教材工具箱`,
    description: article.description,
    openGraph: {
      title: article.title,
      description: article.description,
      type: 'article',
      publishedTime: article.date,
    },
  };
}

export default function Page({ params }: { params: { slug: string } }) {
  const article = articles.find(a => a.id === params.slug);
  if (!article) notFound();
  return <BlogPostPage slug={params.slug} />;
}
