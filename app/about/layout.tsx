export default function AboutLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <div className="sr-only">
        <p>教材工具箱是一个免费的在线教育工具平台，致力于为小学生和家长提供便捷、高效的教学工具。所有功能完全免费，无需注册，即开即用。</p>
      </div>
      {children}
    </>
  );
}
