import CategoryPage from '../_components/CategoryPage';
import type { Metadata } from 'next';
import { CATEGORY_SEO } from '../data';

export const metadata: Metadata = {
  title: CATEGORY_SEO.english.title,
  description: CATEGORY_SEO.english.description,
  keywords: CATEGORY_SEO.english.keywords,
  alternates: {
    canonical: 'https://www.skillxm.cn/resources/english',
  },
};

export default function Page() {
  return <CategoryPage categoryId="english" />;
}
