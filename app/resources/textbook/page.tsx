import CategoryPage from '../_components/CategoryPage';
import type { Metadata } from 'next';
import { CATEGORY_SEO } from '../data';

export const metadata: Metadata = {
  title: CATEGORY_SEO.textbook.title,
  description: CATEGORY_SEO.textbook.description,
  keywords: CATEGORY_SEO.textbook.keywords,
};

export default function Page() {
  return <CategoryPage categoryId="textbook" />;
}
