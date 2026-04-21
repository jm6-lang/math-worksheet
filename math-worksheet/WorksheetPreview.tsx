'use client';

import React from 'react';
import { Question } from '@/lib/questionGenerator';

export type TemplateType = 'tianzige' | 'fangge' | 'hengxian' | 'kongbai';
export type WorksheetMode = 'worksheet' | 'answersheet';

export interface WorksheetConfig {
  title: string;
  grade: number;
  date: string;
  name: string;
  template: TemplateType;
  questionsPerRow: number;
  fontSize: 'sm' | 'md' | 'lg';
  showPageNumber: boolean;
  showNameField: boolean;
  showDateField: boolean;
  mode: WorksheetMode;       // 题目卷 or 答案卷
  showAnswers: boolean;       // 在题目卷中是否同时显示答案
}

// ============================================================
// 田字格组件（1-2年级用，带十字辅助线）
// ============================================================
function TianZiGe({ children, size }: { children: React.ReactNode; size: number }) {
  return (
    <div
      className="relative flex-shrink-0"
      style={{ width: size, height: size }}
    >
      <div
        className="absolute inset-0 border-2 border-black"
        style={{ background: 'white', boxShadow: 'inset 0 0 0 1px rgba(0,0,0,0.1)' }}
      />
      <div className="absolute left-1/2 top-0 bottom-0 w-px bg-blue-300 opacity-60" style={{ transform: 'translateX(-50%)' }} />
      <div className="absolute top-1/2 left-0 right-0 h-px bg-red-300 opacity-60" style={{ transform: 'translateY(-50%)' }} />
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        {children}
      </div>
    </div>
  );
}

// ============================================================
// 方格组件（3-4年级用）
// ============================================================
function FangGe({ children, size }: { children: React.ReactNode; size: number }) {
  return (
    <div
      className="relative flex-shrink-0 border border-gray-400"
      style={{ width: size, height: size, background: 'white' }}
    >
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        {children}
      </div>
    </div>
  );
}

// ============================================================
// 横线格组件（高年级用）
// ============================================================
function HengXianGe({ children, height }: { children: React.ReactNode; height: number; size?: number; isWide?: boolean }) {
  return (
    <div
      className="relative flex-shrink-0 border-b border-gray-400"
      style={{ height, width: children ? undefined : '100%', background: 'white' }}
    >
      <div className="absolute inset-0 flex flex-col items-end justify-end px-2 pb-1">
        {children}
      </div>
    </div>
  );
}

// ============================================================
// 竖式渲染（上下结构）
// ============================================================
function VerticalQuestion({
  question,
  mode,
  fontSize,
}: {
  question: Question;
  mode: WorksheetMode;
  fontSize: 'sm' | 'md' | 'lg';
}) {
  const raw = question.raw;
  const fs = fontSize === 'sm' ? 'text-base' : fontSize === 'lg' ? 'text-2xl' : 'text-xl';
  const rawA = raw?.a ?? 0;
  const rawB = raw?.b ?? 0;
  const rawSign = raw?.sign ?? '+';
  const rawResult = raw?.result ?? 0;

  // 答案卷模式：直接展示完整竖式（含答案）
  if (mode === 'answersheet') {
    return (
      <div className={`flex flex-col items-end gap-0 ${fs}`}>
        <div className="text-right leading-none">{rawA}</div>
        <div className="flex items-center gap-1 text-right leading-none">
          <span>{rawSign}</span>
          <span className="leading-none">{rawB}</span>
        </div>
        <div className="w-full border-b-2 border-black my-0.5" />
        <div className="text-right leading-none">{String(rawResult)}</div>
      </div>
    );
  }

  // 题目卷模式：显示题目 + 下方答案线
  return (
    <div className={`flex flex-col items-end gap-0 ${fs}`}>
      <div className="text-right leading-none">{rawA}</div>
      <div className="flex items-center gap-1 text-right leading-none">
        <span>{rawSign}</span>
        <span className="leading-none">{rawB}</span>
      </div>
      <div className="w-full border-b-2 border-black mt-1 mb-0.5" />
      {/* 答案区 */}
      <div className="flex items-end gap-1 w-full justify-end">
        <div className="flex-1 border-b border-dotted border-gray-400 mr-1" />
        <span className="font-bold text-green-600 leading-none">{String(rawResult)}</span>
      </div>
    </div>
  );
}

// ============================================================
// 普通算式渲染（格子内）
// ============================================================
function NormalQuestion({
  question,
  mode,
  fontSize,
  showAnswer,
}: {
  question: Question;
  mode: WorksheetMode;
  fontSize: 'sm' | 'md' | 'lg';
  showAnswer: boolean;
}) {
  const fs = fontSize === 'sm' ? 'text-lg' : fontSize === 'lg' ? 'text-3xl' : 'text-2xl';

  if (mode === 'answersheet') {
    return (
      <div className="flex flex-col items-center justify-center w-full h-full gap-0">
        <span className={`${fs} font-mono font-bold text-gray-800`}>{question.answer}</span>
      </div>
    );
  }

  // 题目卷：题目 + 答案区
  return (
    <div className="flex flex-col items-center justify-center w-full h-full gap-0">
      <span className={`${fs} font-mono font-bold text-gray-800`}>{question.question}</span>
      {/* 答案行（等号+空格） */}
      <div className="flex items-center justify-center w-full mt-1">
        <div className="flex-1 border-b border-dotted border-gray-400 mr-1" />
        {showAnswer && (
          <span className="text-green-600 font-bold text-xl leading-none">={question.answer}</span>
        )}
      </div>
    </div>
  );
}

// ============================================================
// 题目渲染（根据模板分发）
// ============================================================
function QuestionCell({
  question,
  config,
  cellSize,
  lineHeight,
}: {
  question: Question;
  config: WorksheetConfig;
  cellSize: number;
  lineHeight: number;
}) {
  const { template, fontSize, mode, showAnswers } = config;
  const hasRaw = !!question.raw;  // 竖式/填空题
  const fs = fontSize === 'sm' ? 'text-base' : fontSize === 'lg' ? 'text-xl' : 'text-lg';

  // ===== 答案卷模式 =====
  if (mode === 'answersheet') {
    if (hasRaw) {
      return (
        <div className="flex items-center justify-center p-1" style={{ width: cellSize * 1.5, minHeight: cellSize }}>
          <VerticalQuestion question={question} mode="answersheet" fontSize={fontSize} />
        </div>
      );
    }
    return (
      <FangGe size={cellSize}>
        <span className={`${fs} font-mono font-bold text-gray-800`}>{question.answer}</span>
      </FangGe>
    );
  }

  // ===== 题目卷模式 =====
  if (hasRaw) {
    // 竖式/填空题/比大小等特殊题型
    return (
      <div
        className="flex items-center justify-center p-1"
        style={{ width: cellSize * 1.5, minHeight: cellSize }}
      >
        <VerticalQuestion question={question} mode="worksheet" fontSize={fontSize} />
      </div>
    );
  }

  // 普通算术题
  if (template === 'tianzige') {
    return (
      <TianZiGe size={cellSize}>
        <NormalQuestion question={question} mode="worksheet" fontSize={fontSize} showAnswer={showAnswers} />
      </TianZiGe>
    );
  }

  if (template === 'fangge') {
    return (
      <FangGe size={cellSize}>
        <NormalQuestion question={question} mode="worksheet" fontSize={fontSize} showAnswer={showAnswers} />
      </FangGe>
    );
  }

  // 横线格/空白纸
  return (
    <HengXianGe height={lineHeight}>
      <div className="flex items-center gap-2 w-full">
        <span className={`${fs} font-mono font-bold text-gray-800`}>{question.question}</span>
        {showAnswers && (
          <span className="text-green-600 font-bold text-xl">={question.answer}</span>
        )}
      </div>
    </HengXianGe>
  );
}

// ============================================================
// 单页工作表
// ============================================================
function WorksheetPage({
  pageQuestions,
  config,
  pageNumber,
  totalPages,
}: {
  pageQuestions: Question[];
  config: WorksheetConfig;
  pageNumber: number;
  totalPages: number;
}) {
  const { template, questionsPerRow, fontSize, showPageNumber, showNameField, showDateField, mode } = config;

  // A4: 794px × 1123px (96dpi)
  const pageWidth = 794;
  const pageHeight = 1123;
  const marginTop = 80;
  const marginBottom = 60;
  const marginLeft = 60;
  const marginRight = 60;
  const contentWidth = pageWidth - marginLeft - marginRight;
  const headerHeight = 60;
  const gridTop = marginTop + headerHeight + 20;

  let cellSize = 70;
  let rowHeight = 70;
  const actualPerRow = Math.min(questionsPerRow, Math.floor(contentWidth / cellSize));
  cellSize = Math.floor(contentWidth / actualPerRow);

  if (template === 'hengxian' || template === 'kongbai') {
    rowHeight = fontSize === 'sm' ? 40 : fontSize === 'lg' ? 64 : 52;
  } else {
    rowHeight = cellSize + 8;
  }

  const availableHeight = pageHeight - gridTop - marginBottom;
  const rowsPerPage = Math.floor(availableHeight / rowHeight);
  const questionsPerPage = actualPerRow * rowsPerPage;

  // 分行
  const rows: Question[][] = [];
  for (let i = 0; i < pageQuestions.length; i += actualPerRow) {
    rows.push(pageQuestions.slice(i, i + actualPerRow));
  }

  const titleFontSize = fontSize === 'sm' ? 'text-xl' : fontSize === 'lg' ? 'text-3xl' : 'text-2xl';
  const pageTitle = mode === 'answersheet'
    ? `${config.title}（参考答案）`
    : config.title;

  return (
    <div
      className="bg-white overflow-hidden"
      style={{
        width: pageWidth,
        minHeight: pageHeight,
        fontFamily: '"Noto Sans SC", "Microsoft YaHei", "SimHei", sans-serif',
      }}
    >
      {/* 页眉 */}
      <div
        className="flex items-center justify-between px-4"
        style={{
          height: headerHeight,
          marginTop,
          marginLeft,
          marginRight,
          width: contentWidth,
          borderBottom: '2px solid #dbeafe',
        }}
      >
        <div className={`${titleFontSize} font-bold ${mode === 'answersheet' ? 'text-green-600' : 'text-blue-700'}`}>
          {pageTitle}
        </div>
        <div className="flex items-center gap-4 text-sm text-gray-600">
          {showNameField && mode !== 'answersheet' && (
            <div className="flex items-center gap-1">
              <span>姓名：</span>
              <div className="w-24 border-b border-gray-400 inline-block" />
            </div>
          )}
          {showDateField && mode !== 'answersheet' && (
            <div className="flex items-center gap-1">
              <span>日期：</span>
              <div className="w-20 border-b border-gray-400 inline-block" />
            </div>
          )}
          {showPageNumber && (
            <span className="text-gray-400">
              第 {pageNumber} / {totalPages} 页
            </span>
          )}
        </div>
      </div>

      {/* 题目网格 */}
      <div style={{ marginLeft, marginTop: 20, marginRight, marginBottom }}>
        {rows.map((row, rowIdx) => (
          <div
            key={rowIdx}
            className="flex items-start flex-wrap"
            style={{
              minHeight: rowHeight,
              gap: '4px',
            }}
          >
            {row.map((q) => (
              <div
                key={q.id}
                className="flex items-center justify-center"
                style={{
                  width: template === 'hengxian' || template === 'kongbai'
                    ? contentWidth
                    : cellSize,
                  height: rowHeight,
                }}
              >
                <QuestionCell
                  question={q}
                  config={config}
                  cellSize={cellSize}
                  lineHeight={rowHeight}
                />
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

// ============================================================
// 完整工作表组件（分页）
// ============================================================
export default function WorksheetPreview({
  questions,
  config,
}: {
  questions: Question[];
  config: WorksheetConfig;
}) {
  const pageWidth = 794;
  const pageHeight = 1123;
  const marginTop = 80;
  const marginBottom = 60;
  const marginLeft = 60;
  const marginRight = 60;
  const headerHeight = 60;
  const contentWidth = pageWidth - marginLeft - marginRight;
  const availableHeight = pageHeight - marginTop - marginBottom - headerHeight;

  let cellSize = 70;
  let rowHeight = 70;
  const { template, questionsPerRow, fontSize } = config;
  const actualPerRow = Math.min(questionsPerRow, Math.floor(contentWidth / cellSize));
  cellSize = Math.floor(contentWidth / actualPerRow);

  if (template === 'hengxian' || template === 'kongbai') {
    rowHeight = fontSize === 'sm' ? 40 : fontSize === 'lg' ? 64 : 52;
  } else {
    rowHeight = cellSize + 8;
  }

  const rowsPerPage = Math.floor(availableHeight / rowHeight);
  const questionsPerPage = actualPerRow * rowsPerPage;
  const totalPages = Math.ceil(questions.length / questionsPerPage);

  const pages: Question[][] = [];
  for (let i = 0; i < questions.length; i += questionsPerPage) {
    pages.push(questions.slice(i, i + questionsPerPage));
  }

  return (
    <div className="flex flex-col items-center gap-8">
      <div className="text-sm text-gray-500 text-center">
        共 {questions.length} 题，分 {totalPages} 页
        {config.mode === 'answersheet' && ' · 参考答案'}
        {' · '}建议按 <kbd className="px-2 py-0.5 bg-gray-100 border border-gray-300 rounded text-xs">Ctrl+P</kbd> 打印
      </div>
      <div className="flex flex-col gap-8">
        {pages.map((pageQuestions, idx) => (
          <WorksheetPage
            key={idx}
            pageQuestions={pageQuestions}
            config={config}
            pageNumber={idx + 1}
            totalPages={totalPages}
          />
        ))}
      </div>
    </div>
  );
}
