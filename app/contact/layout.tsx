export default function ContactLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <div className="sr-only">
        <p>如有问题或建议，欢迎通过以下方式联系教材工具箱团队。</p>
      </div>
      {children}
    </>
  );
}
