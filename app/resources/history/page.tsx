import CategoryPage from '../_components/CategoryPage';
import type { Metadata } from 'next';
import { CATEGORY_SEO } from '../data';

export const metadata: Metadata = {
  title: CATEGORY_SEO.history.title,
  description: CATEGORY_SEO.history.description,
  keywords: CATEGORY_SEO.history.keywords,
};

export default function Page() {
  return <CategoryPage categoryId="history" />;
}
