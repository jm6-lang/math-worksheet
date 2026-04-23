import CategoryPage from '../_components/CategoryPage';
import type { Metadata } from 'next';
import { CATEGORY_SEO } from '../data';

export const metadata: Metadata = {
  title: CATEGORY_SEO.junior.title,
  description: CATEGORY_SEO.junior.description,
  keywords: CATEGORY_SEO.junior.keywords,
};

export default function Page() {
  return <CategoryPage categoryId="junior" />;
}
