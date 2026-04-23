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

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const article = articles.find(a => a.id === slug);
  if (!article) notFound();
  return <BlogPostPage slug={slug} />;
}
