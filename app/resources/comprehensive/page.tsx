import CategoryPage from '../_components/CategoryPage';
import type { Metadata } from 'next';
import { CATEGORY_SEO } from '../data';

export const metadata: Metadata = {
  title: CATEGORY_SEO.comprehensive.title,
  description: CATEGORY_SEO.comprehensive.description,
  keywords: CATEGORY_SEO.comprehensive.keywords,
};

export default function Page() {
  return <CategoryPage categoryId="comprehensive" />;
}
