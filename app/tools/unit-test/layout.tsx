import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/unit-test";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "小学单元测试卷生成器 - 数语英科全科试卷免费打印 | 教材工具箱",
    description: "免费生成小学1-6年级单元测试卷，数学语文英语科学四科，305个单元PDF打印",
    keywords: "单元测试卷,期中试卷,期末试卷,小学数学试卷,小学语文试卷,小学英语试卷,小学科学试卷,试卷生成器,免费试卷打印",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "小学单元测试卷生成器 - 数语英科全科试卷免费打印 | 教材工具箱",
      description: "免费生成小学1-6年级单元测试卷，数学语文英语科学四科，305个单元PDF打印",
      type: "website",
    },
  };
}

export default function UnitTestLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <div className="sr-only">
        <h1>单元测试卷生成器 - 小学数语英科全科试卷免费打印</h1>
        <p>免费生成小学1-6年级单元测试卷，数学语文英语科学四科，305个单元PDF打印。教材工具箱提供完整的小学单元测试卷生成服务，覆盖人教版、北师大版等主流教材版本，是小学教师备课和考试出题的得力助手。</p>
        <h2>核心功能</h2>
        <ul>
          <li>四科覆盖：支持数学、语文、英语、科学四个学科，满足小学全科测试需求</li>
          <li>305个单元：完整覆盖小学1-6年级所有单元知识点，每个单元都有对应的测试卷</li>
          <li>单元测试/期中/期末：支持单元测试卷、期中测试卷、期末测试卷三种考试类型，全面评估学习成果</li>
          <li>三档难度：提供基础、提高、拓展三个难度等级，适应不同学生的学习水平，实现分层教学</li>
          <li>PDF导出：一键生成PDF格式试卷，排版规范，方便打印分发，支持A4纸张标准格式</li>
        </ul>
        <h2>适用对象</h2>
        <p>单元测试卷生成器适合小学各学科教师、教育培训机构以及学生家长使用。无论是日常单元测验、期中期末考试还是课后练习，都可以通过本工具快速生成高质量的测试试卷，节省教师备课时间，提高教学效率。</p>
        <p>访问 <a href="https://www.skillxm.cn">教材工具箱</a> 获取更多免费教学工具。</p>
      </div>
      {children}
    </>
  );
}
