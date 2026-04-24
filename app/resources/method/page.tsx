import CategoryPage from '../_components/CategoryPage';
import type { Metadata } from 'next';
import { CATEGORY_SEO } from '../data';

export const metadata: Metadata = {
  title: CATEGORY_SEO.method.title,
  description: CATEGORY_SEO.method.description,
  keywords: CATEGORY_SEO.method.keywords,
  alternates: {
    canonical: 'https://www.skillxm.cn/resources/method',
  },
};

export default function Page() {
  return <CategoryPage categoryId="method" />;
}
