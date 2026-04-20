'use client';

import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';
import { Question } from '@/lib/questionGenerator';
import { WorksheetConfig } from '@/components/WorksheetPreview';

export async function exportToPDF(
  worksheetElement: HTMLElement,
  filename: string = '数学练习.pdf'
): Promise<void> {
  // 使用 html2canvas 将 DOM 转换为 canvas
  const canvas = await html2canvas(worksheetElement, {
    scale: 2, // 提高清晰度
    useCORS: true,
    logging: false,
    backgroundColor: '#ffffff',
    windowWidth: 794,
    windowHeight: 1123,
  });

  // A4 尺寸（mm）
  const pageWidth = 210;
  const pageHeight = 297;

  // canvas 像素尺寸
  const imgWidth = canvas.width;
  const imgHeight = canvas.height;

  // 每页图片高度（像素）
  const pageHeightPx = (imgWidth / pageWidth) * pageHeight;

  // 计算总页数
  const totalPages = Math.ceil(imgHeight / pageHeightPx);

  // 创建 PDF
  const pdf = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4',
  });

  for (let i = 0; i < totalPages; i++) {
    if (i > 0) {
      pdf.addPage();
    }

    // 裁剪每页的 canvas 区域
    const pageCanvas = document.createElement('canvas');
    pageCanvas.width = imgWidth;
    pageCanvas.height = pageHeightPx;

    const ctx = pageCanvas.getContext('2d')!;
    ctx.drawImage(
      canvas,
      0,
      i * pageHeightPx,
      imgWidth,
      pageHeightPx,
      0,
      0,
      imgWidth,
      pageHeightPx
    );

    const imgData = pageCanvas.toDataURL('image/jpeg', 0.95);
    pdf.addImage(imgData, 'JPEG', 0, 0, pageWidth, pageHeight);
  }

  pdf.save(filename);
}

export async function exportAllPagesToPDF(
  pageElements: HTMLElement[],
  filename: string = '数学练习.pdf'
): Promise<void> {
  const pdf = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4',
  });

  const pageWidth = 210;
  const pageHeight = 297;

  for (let i = 0; i < pageElements.length; i++) {
    const element = pageElements[i];

    const canvas = await html2canvas(element, {
      scale: 2,
      useCORS: true,
      logging: false,
      backgroundColor: '#ffffff',
    });

    const imgData = canvas.toDataURL('image/jpeg', 0.95);
    const imgWidthMm = (canvas.width / canvas.height) * pageHeight;
    const offsetX = (pageWidth - imgWidthMm) / 2;

    if (i > 0) {
      pdf.addPage();
    }

    pdf.addImage(imgData, 'JPEG', offsetX, 0, imgWidthMm, pageHeight);
  }

  pdf.save(filename);
}

// 打印功能
export function printWorksheet(): void {
  window.print();
}
