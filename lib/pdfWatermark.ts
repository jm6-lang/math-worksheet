/**
 * PDF 水印工具 - 在 canvas 上绘制来源信息
 */

/** 来源水印文字 */
const WATERMARK_TEXT = '来源：教材工具箱 | 免费下载：www.skillxm.cn';

/**
 * 在 canvas 顶部绘制来源水印（首页）
 */
export function drawHeaderWatermark(
  ctx: CanvasRenderingContext2D,
  canvasWidth: number,
): void {
  const headerHeight = 28;

  // 白色背景
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, canvasWidth, headerHeight);

  // 底部分隔线
  ctx.strokeStyle = '#eeeeee';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(canvasWidth * 0.1, headerHeight - 1);
  ctx.lineTo(canvasWidth * 0.9, headerHeight - 1);
  ctx.stroke();

  // 水印文字
  ctx.fillStyle = '#999999';
  ctx.font = '12px sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'bottom';
  ctx.fillText(WATERMARK_TEXT, canvasWidth / 2, headerHeight - 5);
}

/**
 * 在 canvas 底部绘制来源水印（末页）
 */
export function drawFooterWatermark(
  ctx: CanvasRenderingContext2D,
  canvasWidth: number,
  canvasHeight: number,
): void {
  const footerHeight = 28;
  const footerY = canvasHeight - footerHeight;

  // 白色背景
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, footerY, canvasWidth, footerHeight);

  // 顶部分隔线
  ctx.strokeStyle = '#eeeeee';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(canvasWidth * 0.1, footerY + 1);
  ctx.lineTo(canvasWidth * 0.9, footerY + 1);
  ctx.stroke();

  // 水印文字
  ctx.fillStyle = '#999999';
  ctx.font = '12px sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'top';
  ctx.fillText(WATERMARK_TEXT, canvasWidth / 2, footerY + 6);
}

/**
 * 兼容旧调用的统一水印函数（底部）
 * @deprecated 请使用 drawFooterWatermark
 */
export function drawWatermarkOnCanvas(
  ctx: CanvasRenderingContext2D,
  canvasWidth: number,
  canvasHeight: number,
): void {
  drawFooterWatermark(ctx, canvasWidth, canvasHeight);
}
