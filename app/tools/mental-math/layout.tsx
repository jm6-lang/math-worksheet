import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/mental-math";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "口算速练 - 在线口算计时挑战 | 教材工具箱",
    description: "免费在线口算速练工具，提供4个难度级别，涵盖加减乘除全运算类型，计时挑战即时反馈，适合小学一二年级到五六年级学生日常口算打卡训练。",
    keywords: "口算速练,口算练习,口算计时,速算训练,数学口算,口算题,在线口算",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "口算速练 - 免费在线口算计时挑战 | 教材工具箱",
      description: "免费在线口算速练工具，提供4个难度级别，涵盖加减乘除全运算类型，计时挑战即时反馈，适合小学一二年级到五六年级学生日常口算打卡训练。",
      type: "website",
      images: [{ url: "https://www.skillxm.cn/og-image.jpg", width: 1200, height: 630, alt: "教材工具箱" }],
    },
  };
}

export default function MentalMathLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      {/* 服务端渲染的 SEO 内容 -- 搜索引擎可直接抓取 */}
      <div className="sr-only">
        <h1>口算速练 - 在线计时口算练习</h1>
        <p>免费在线口算速练，4个难度级别，计时挑战即时反馈，一二年级到五六年级全覆盖。通过限时口算训练快速提升计算能力，支持加减乘除全运算类型，答题即时判定对错，训练结束自动统计正确率和用时，适合日常口算打卡练习。</p>
        <h2>核心功能</h2>
        <ul>
          <li>4个难度级别：入门级（10以内加减）、基础级（20以内加减）、提高级（100以内加减乘除）、挑战级（大数运算混合），匹配不同年级水平</li>
          <li>计时挑战模式：倒计时答题，营造紧迫感，提升计算速度和专注力</li>
          <li>即时反馈判定：每道题答完立即显示对错，错误题目可回顾复习</li>
          <li>加减乘除全覆盖：支持加法、减法、乘法、除法及混合运算，全面训练计算能力</li>
          <li>成绩统计报告：训练结束后自动统计正确率、答题数量、用时等数据</li>
          <li>完全免费：无需注册登录，打开即练，不限制练习次数</li>
        </ul>
        <h2>适用对象</h2>
        <p>小学1-6年级学生、需要提升计算速度的中小学生、家长辅导孩子口算练习、教师课堂口算训练。适合每日口算打卡、课前热身练习、期末口算复习、假期计算能力巩固等场景。</p>
        <p>访问 <a href="https://www.skillxm.cn">教材工具箱</a> 获取更多免费教学工具，包括数学练习卷生成器、字帖生成器、英语字帖、数独游戏等。</p>
      </div>
      {children}
    </>
  );
}
