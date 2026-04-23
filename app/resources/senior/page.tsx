import CategoryPage from '../_components/CategoryPage';
import type { Metadata } from 'next';
import { CATEGORY_SEO } from '../data';

export const metadata: Metadata = {
  title: CATEGORY_SEO.senior.title,
  description: CATEGORY_SEO.senior.description,
  keywords: CATEGORY_SEO.senior.keywords,
};

export default function Page() {
  return <CategoryPage categoryId="senior" />;
}
