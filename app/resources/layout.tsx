import type { Metadata } from "next";

const canonicalUrl = "https://www.skillxm.cn/resources";

export const metadata: Metadata = {
  title: "免费教育资源中心 - 小学学习资料下载 | 教材工具箱",
  description: "教材工具箱免费教育资源中心，提供小学数学、语文、英语、科学等各科学习资料和教学资源下载，覆盖一年级到六年级全套教材配套资料。",
  keywords: "免费教育资源,小学学习资料,数学资源,语文资源,英语资源,教学资料下载,小学试题",
  alternates: { canonical: canonicalUrl },
  openGraph: {
    url: canonicalUrl,
    title: "免费教育资源中心 - 小学学习资料下载 | 教材工具箱",
    description: "教材工具箱免费教育资源中心，提供小学各科学习资料和教学资源下载。",
    type: "website",
    images: [{ url: "https://www.skillxm.cn/og-image.jpg", width: 1200, height: 630, alt: "教材工具箱" }],
  },
};

export default function ResourcesLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <div className="sr-only">
        <h1>免费教育资源中心 - 小学学习资料下载</h1>
        <p>教材工具箱免费教育资源中心，提供小学数学、语文、英语、科学、历史等各科学习资料和教学资源下载，覆盖一年级到六年级全套教材配套资料。</p>
        <h2>资源分类</h2>
        <ul>
          <li>数学资源：数学练习卷、口算题、应用题、思维训练题</li>
          <li>语文资源：字帖模板、古诗词默写、作文模板、阅读理解</li>
          <li>英语资源：英语字帖、单词练习、语法练习</li>
          <li>科学资源：科学实验、知识点总结</li>
          <li>历史资源：历史知识、时间线</li>
          <li>学习方法：学习技巧、复习攻略、升学指导</li>
        </ul>
        <p>访问 <a href="https://www.skillxm.cn">教材工具箱</a> 获取更多免费教学工具。</p>
      </div>
      {children}
    </>
  );
}
