'use client';

import { useState } from 'react';
import { getNavBarLinks } from '@/lib/toolRegistry';

const navLinks = getNavBarLinks();

interface ToolNavBarProps {
  /** 当前页面的路径，用于高亮 */
  currentPath?: string;
  /** 页面标题（显示在 Logo 旁） */
  title?: string;
}

export default function ToolNavBar({ currentPath = '', title }: ToolNavBarProps) {
  const [mobileMenu, setMobileMenu] = useState(false);

  const isActive = (href: string) => currentPath === href;

  return (
    <nav className="print:hidden fixed top-0 left-0 right-0 z-50 bg-[#0f0f0f]/95 backdrop-blur-md border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14">
          {/* Logo */}
          <div className="flex items-center gap-2.5 shrink-0">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-base shadow-lg shadow-blue-500/20">
              📚
            </div>
            <a href="/" className="text-base font-bold text-white hover:opacity-80 transition-opacity">
              教材工具箱
            </a>
            {title && (
              <>
                <span className="text-gray-600">/</span>
                <span className="text-sm font-medium text-gray-300 hidden sm:inline">{title}</span>
              </>
            )}
          </div>

          {/* 桌面端导航 */}
          <div className="hidden lg:flex items-center gap-0.5">
            <a href="/" className="px-2.5 py-1.5 text-xs text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-all">
              首页
            </a>
            {navLinks.map(tool => (
              <a
                key={tool.href}
                href={tool.href}
                className={`px-2.5 py-1.5 text-xs rounded-lg transition-all ${
                  isActive(tool.href)
                    ? 'text-white bg-white/10 font-medium'
                    : 'text-gray-400 hover:text-white hover:bg-white/10'
                }`}
              >
                {tool.name}
              </a>
            ))}
          </div>

          {/* 移动端汉堡按钮 */}
          <button
            onClick={() => setMobileMenu(!mobileMenu)}
            className="lg:hidden p-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
            aria-label="菜单"
          >
            {mobileMenu ? '✕' : '☰'}
          </button>
        </div>
      </div>

      {/* 移动端下拉菜单 */}
      {mobileMenu && (
        <div className="lg:hidden bg-[#1a1a1a] border-t border-white/10 py-3 px-4 max-h-[70vh] overflow-y-auto">
          <a href="/" className="block px-4 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
            🏠 首页
          </a>
          {navLinks.map(tool => (
            <a
              key={tool.href}
              href={tool.href}
              className={`block px-4 py-2.5 text-sm rounded-lg transition-colors ${
                isActive(tool.href)
                  ? 'text-white bg-white/10 font-medium'
                  : 'text-gray-300 hover:text-white hover:bg-white/10'
              }`}
            >
              {tool.name}
            </a>
          ))}
        </div>
      )}
    </nav>
  );
}
