import CategoryPage from '../_components/CategoryPage';
import type { Metadata } from 'next';
import { CATEGORY_SEO } from '../data';

export const metadata: Metadata = {
  title: CATEGORY_SEO.calligraphy.title,
  description: CATEGORY_SEO.calligraphy.description,
  keywords: CATEGORY_SEO.calligraphy.keywords,
};

export default function Page() {
  return <CategoryPage categoryId="calligraphy" />;
}
