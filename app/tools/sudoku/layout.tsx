import type { Metadata } from "next";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const headersList = await headers();
  const host = headersList.get("host") ?? "www.skillxm.cn";
  const protocol = host.includes("localhost") ? "http" : "https";
  const pathname = headersList.get("x-invoke-path") ?? headersList.get("x-matched-path") ?? "/tools/sudoku";
  const canonicalUrl = `${protocol}://${host}${pathname}`;
  return {
    title: "数独游戏在线玩 - 入门/进阶/挑战三档难度 | 教材工具箱",
    description: "免费在线数独游戏，3档难度（入门/进阶/挑战），锻炼逻辑思维和专注力，适合小学生课余训练，无需下载即开即玩",
    keywords: "数独游戏,在线数独,数独挑战,逻辑训练,益智游戏,免费数独,数独解题",
    alternates: { canonical: canonicalUrl },
    openGraph: {
      url: canonicalUrl,
      title: "数独游戏 - 免费在线数独挑战 | 教材工具箱",
      description: "免费在线数独游戏，3档难度，锻炼逻辑思维，适合小学生课余训练",
      type: "website",
    },
  };
}

export default function SudokuLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      {/* 服务端渲染的 SEO 内容 -- 搜索引擎可直接抓取 */}
      <div className="sr-only">
        <h1>数独游戏 - 在线益智逻辑训练</h1>
        <p>免费在线数独游戏，3档难度，锻炼逻辑思维，适合小学生课余训练。无需下载安装，打开浏览器即可玩数独，支持入门、进阶、挑战三个难度等级，内置数字键盘方便手机操作，即时验证答案正误，帮助提升逻辑推理和专注力。</p>
        <h2>核心功能</h2>
        <ul>
          <li>3档难度等级：入门（适合初学者）、进阶（有一定基础）、挑战（高难度），循序渐进提升</li>
          <li>数字键盘输入：内置虚拟数字键盘，手机平板操作便捷，支持笔记模式</li>
          <li>即时验证反馈：实时检查填写是否正确，错误高亮提示，帮助快速定位问题</li>
          <li>适合各年龄段：小学生到成人都能玩，既是益智游戏也是逻辑训练工具</li>
          <li>计时功能：记录解题用时，挑战自我速度极限</li>
          <li>完全免费：无需注册登录，打开即玩，不限制游戏次数</li>
        </ul>
        <h2>适用对象</h2>
        <p>小学3-6年级学生、逻辑思维训练爱好者、数独入门学习者、课余时间需要益智活动的中小学生。适合课间休息、家庭亲子互动、逻辑思维训练、数学兴趣培养等场景。</p>
        <p>访问 <a href="https://www.skillxm.cn">教材工具箱</a> 获取更多免费教学工具，包括数学练习卷生成器、字帖生成器、英语字帖、口算速练等。</p>
      </div>
      {children}
    </>
  );
}
