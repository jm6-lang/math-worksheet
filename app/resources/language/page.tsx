import CategoryPage from '../_components/CategoryPage';
import type { Metadata } from 'next';
import { CATEGORY_SEO } from '../data';

export const metadata: Metadata = {
  title: CATEGORY_SEO.language.title,
  description: CATEGORY_SEO.language.description,
  keywords: CATEGORY_SEO.language.keywords,
};

export default function Page() {
  return <CategoryPage categoryId="language" />;
}
