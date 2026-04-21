const fs = require('fs');
let c = fs.readFileSync('C:/Users/Administrator/.qclaw/workspace-agent-3bb7b585/math-worksheet/app/page.tsx', 'utf8');

const donateModal = `
      {/* 捐赠弹窗 */}
      {showDonate && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm" onClick={() => setShowDonate(false)}>
          <div className="bg-[#1a1a1a] border border-white/10 rounded-2xl max-w-md w-full p-8" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">☕ 请作者喝杯咖啡</h2>
              <button onClick={() => setShowDonate(false)} className="text-gray-400 hover:text-white text-2xl leading-none">✕</button>
            </div>
            <p className="text-gray-400 text-sm text-center mb-6">如果这个工具对你有帮助，欢迎打赏支持持续开发 ❤️</p>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center">
                <p className="text-sm text-gray-400 mb-2">微信支付</p>
                <img src="/donate/wechat.png" alt="微信支付" className="w-full rounded-xl bg-white p-2" />
              </div>
              <div className="text-center">
                <p className="text-sm text-gray-400 mb-2">支付宝</p>
                <img src="/donate/alipay.jpg" alt="支付宝" className="w-full rounded-xl bg-white p-2" />
              </div>
            </div>
          </div>
        </div>
      )}
`;

const marker = '{/* ===== Hero 区域 ===== */}';
if (!c.includes(marker)) { console.log('marker not found'); process.exit(1); }
c = c.replace(marker, donateModal + marker);
fs.writeFileSync('C:/Users/Administrator/.qclaw/workspace-agent-3bb7b585/math-worksheet/app/page.tsx', c, 'utf8');
console.log('done, len=' + c.length);
console.log('has wechat:', c.includes('/donate/wechat.png'));
console.log('has alipay:', c.includes('/donate/alipay.jpg'));
