/**
 * 在 canvas 上绘制网站水印（底部居中）
 * @param ctx - Canvas 2D 上下文
 * @param canvasWidth - canvas 宽度（像素）
 * @param canvasHeight - canvas 高度（像素）
 */
export function drawWatermarkOnCanvas(
  ctx: CanvasRenderingContext2D,
  canvasWidth: number,
  canvasHeight: number
): void {
  // 水印区域高度
  const watermarkHeight = 40;
  const watermarkY = canvasHeight - watermarkHeight;

  // 白色背景覆盖水印区域
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, watermarkY, canvasWidth, watermarkHeight);

  // 分隔线
  ctx.strokeStyle = '#eeeeee';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(canvasWidth * 0.2, watermarkY + 4);
  ctx.lineTo(canvasWidth * 0.8, watermarkY + 4);
  ctx.stroke();

  // 水印文字
  ctx.fillStyle = '#999999';
  ctx.font = '14px sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'top';

  // 第一行
  const line1 = '\uD83D\uDCE7 \u66F4\u591A\u514D\u8D39\u7EC3\u4E60\u5377 \u2192 skillxm.cn';
  ctx.fillText(line1, canvasWidth / 2, watermarkY + 10);

  // 第二行
  const line2 = '\uD83D\uDD0D \u641C\u7D22"\u6559\u6750\u5DE5\u5177\u7BB1"\u83B7\u53D6\u66F4\u591A\u5DE5\u5177';
  ctx.fillText(line2, canvasWidth / 2, watermarkY + 26);
}
