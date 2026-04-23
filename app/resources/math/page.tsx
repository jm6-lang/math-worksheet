import CategoryPage from '../_components/CategoryPage';
import type { Metadata } from 'next';
import { CATEGORY_SEO } from '../data';

export const metadata: Metadata = {
  title: CATEGORY_SEO.math.title,
  description: CATEGORY_SEO.math.description,
  keywords: CATEGORY_SEO.math.keywords,
};

export default function Page() {
  return <CategoryPage categoryId="math" />;
}
