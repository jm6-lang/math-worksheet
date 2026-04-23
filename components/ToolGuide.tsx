'use client';

import { useState } from 'react';

interface GuideStep {
  title: string;
  content: string;
}

interface ToolGuideProps {
  title: string;
  icon: string;
  description: string;
  features: string[];
  steps: GuideStep[];
  tips: string[];
  faqs: { question: string; answer: string }[];
}

export default function ToolGuide({
  title,
  icon,
  description,
  features,
  steps,
  tips,
  faqs,
}: ToolGuideProps) {
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  const toggleFaq = (index: number) => {
    setOpenFaq(openFaq === index ? null : index);
  };

  return (
    <div className="space-y-6">
      {/* 标题区域 */}
      <div className="bg-slate-800/60 border border-white/10 rounded-2xl p-6">
        <div className="flex items-center gap-4 mb-3">
          <span className="text-4xl">{icon}</span>
          <div>
            <h2 className="text-2xl font-bold text-white">{title}</h2>
            <p className="text-slate-400 mt-1">{description}</p>
          </div>
        </div>
      </div>

      {/* 功能特点 */}
      <div className="bg-slate-800/60 border border-white/10 rounded-2xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <svg className="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          功能特点
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {features.map((feature, index) => (
            <div
              key={index}
              className="flex items-center gap-3 bg-slate-700/40 border border-white/5 rounded-xl px-4 py-3"
            >
              <span className="flex-shrink-0 w-6 h-6 flex items-center justify-center bg-emerald-500/20 text-emerald-400 rounded-full text-sm">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </span>
              <span className="text-slate-200 text-sm">{feature}</span>
            </div>
          ))}
        </div>
      </div>

      {/* 使用步骤 */}
      <div className="bg-slate-800/60 border border-white/10 rounded-2xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
          </svg>
          使用步骤
        </h3>
        <div className="space-y-4">
          {steps.map((step, index) => (
            <div key={index} className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 flex items-center justify-center bg-blue-500/20 text-blue-400 rounded-full text-sm font-bold border border-blue-500/30">
                  {index + 1}
                </div>
                {index < steps.length - 1 && (
                  <div className="w-px h-full bg-blue-500/20 mx-auto mt-1" />
                )}
              </div>
              <div className="pb-4">
                <h4 className="text-white font-medium mb-1">{step.title}</h4>
                <p className="text-slate-400 text-sm leading-relaxed">{step.content}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 使用技巧 */}
      <div className="bg-slate-800/60 border border-white/10 rounded-2xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <svg className="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          使用技巧
        </h3>
        <div className="space-y-3">
          {tips.map((tip, index) => (
            <div
              key={index}
              className="flex items-start gap-3 bg-amber-500/5 border border-amber-500/10 rounded-xl px-4 py-3"
            >
              <span className="flex-shrink-0 mt-0.5 text-amber-400">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </span>
              <span className="text-slate-300 text-sm leading-relaxed">{tip}</span>
            </div>
          ))}
        </div>
      </div>

      {/* 常见问题 */}
      <div className="bg-slate-800/60 border border-white/10 rounded-2xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          常见问题
        </h3>
        <div className="space-y-2">
          {faqs.map((faq, index) => (
            <div
              key={index}
              className="border border-white/5 rounded-xl overflow-hidden"
            >
              <button
                onClick={() => toggleFaq(index)}
                className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-slate-700/30 transition-colors"
              >
                <span className="text-slate-200 text-sm font-medium pr-4">
                  {faq.question}
                </span>
                <svg
                  className={`w-4 h-4 text-slate-400 flex-shrink-0 transition-transform duration-200 ${
                    openFaq === index ? 'rotate-180' : ''
                  }`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              {openFaq === index && (
                <div className="px-4 pb-3">
                  <p className="text-slate-400 text-sm leading-relaxed">{faq.answer}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
