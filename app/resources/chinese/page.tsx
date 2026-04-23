import CategoryPage from '../_components/CategoryPage';
import type { Metadata } from 'next';
import { CATEGORY_SEO } from '../data';

export const metadata: Metadata = {
  title: CATEGORY_SEO.chinese.title,
  description: CATEGORY_SEO.chinese.description,
  keywords: CATEGORY_SEO.chinese.keywords,
};

export default function Page() {
  return <CategoryPage categoryId="chinese" />;
}
