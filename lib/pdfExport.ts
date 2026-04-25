'use client';

import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';
import { drawWatermarkOnCanvas } from './pdfWatermark';

// 强制白色背景的 canvas 处理
function ensureWhiteBackground(canvas: HTMLCanvasElement): HTMLCanvasElement {
  const whiteCanvas = document.createElement('canvas');
  whiteCanvas.width = canvas.width;
  whiteCanvas.height = canvas.height;
  const ctx = whiteCanvas.getContext('2d');
  if (ctx) {
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, whiteCanvas.width, whiteCanvas.height);
    ctx.drawImage(canvas, 0, 0);
  }
  return whiteCanvas;
}

export async function exportToPDF(
  worksheetElement: HTMLElement,
  filename: string = '数学练习.pdf'
): Promise<void> {
  // 强制白色背景
  const origBg = worksheetElement.style.background;
  worksheetElement.style.background = '#ffffff';

  // 使用 html2canvas 将 DOM 转换为 canvas
  const canvas = await html2canvas(worksheetElement, {
    scale: 2, // 提高清晰度
    useCORS: true,
    logging: false,
    backgroundColor: '#ffffff',
    windowWidth: 794,
    windowHeight: 1123,
  });

  // 恢复原始背景
  worksheetElement.style.background = origBg;

  // 确保白色背景
  const whiteCanvas = ensureWhiteBackground(canvas);

  // A4 尺寸（mm）
  const pageWidth = 210;
  const pageHeight = 297;

  // canvas 像素尺寸
  const imgWidth = whiteCanvas.width;
  const imgHeight = whiteCanvas.height;

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
    // 先填充白色背景
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, pageCanvas.width, pageCanvas.height);
    ctx.drawImage(
      whiteCanvas,
      0,
      i * pageHeightPx,
      imgWidth,
      pageHeightPx,
      0,
      0,
      imgWidth,
      pageHeightPx
    );

    // 添加网站水印
    drawWatermarkOnCanvas(ctx, pageCanvas.width, pageCanvas.height);

    const imgData = pageCanvas.toDataURL('image/png', 1.0);
    pdf.addImage(imgData, 'PNG', 0, 0, pageWidth, pageHeight);
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

    // 强制白色背景
    const origBg = element.style.background;
    element.style.background = '#ffffff';

    const canvas = await html2canvas(element, {
      scale: 2,
      useCORS: true,
      logging: false,
      backgroundColor: '#ffffff',
    });

    // 恢复原始背景
    element.style.background = origBg;

    // 确保白色背景
    const whiteCanvas = ensureWhiteBackground(canvas);

    // 添加网站水印
    const wCtx = whiteCanvas.getContext('2d');
    if (wCtx) {
      drawWatermarkOnCanvas(wCtx, whiteCanvas.width, whiteCanvas.height);
    }

    const imgData = whiteCanvas.toDataURL('image/png', 1.0);
    const imgWidthMm = (whiteCanvas.width / whiteCanvas.height) * pageHeight;
    const offsetX = (pageWidth - imgWidthMm) / 2;

    if (i > 0) {
      pdf.addPage();
    }

    pdf.addImage(imgData, 'PNG', offsetX, 0, imgWidthMm, pageHeight);
  }

  pdf.save(filename);
}

// 打印功能
export function printWorksheet(): void {
  window.print();
}
