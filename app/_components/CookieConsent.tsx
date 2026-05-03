'use client';
import { useState, useEffect } from 'react';

export default function CookieConsent() {
  const [show, setShow] = useState(false);

  useEffect(() => {
    const consent = localStorage.getItem('cookie-consent');
    if (!consent) setShow(true);
  }, []);

  const accept = () => {
    localStorage.setItem('cookie-consent', 'accepted');
    setShow(false);
  };

  if (!show) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-gray-900 text-white p-4 z-50 flex items-center justify-between flex-wrap gap-3 text-sm">
      <p className="flex-1 min-w-[200px]">
        本网站使用 Cookie 来提升您的体验。继续浏览即表示您同意我们的{' '}
        <a href="/privacy/" className="text-blue-400 underline">隐私政策</a>。
      </p>
      <div className="flex gap-2">
        <button onClick={accept} className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-white">
          接受
        </button>
      </div>
    </div>
  );
}
