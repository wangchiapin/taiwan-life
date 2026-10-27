/* ══════════════════════════════════════════════════════════════
   節慶套件：照玩家手機的日期，節日前後 3 天自動換上裝飾和角色
   （萬聖節、亡靈節、春節、元宵、端午、中元、中秋、聖誕、跨年）
   農曆日期用瀏覽器內建的農曆算，不用手動更新。
   網址加 ?fest=halloween（muertos / cny / lantern / dragon / ghost / moon / xmas / nye）強制顯示，?fest=0 關掉（測試用）
   ══════════════════════════════════════════════════════════════ */
(function () {
'use strict';
const R = (x, y, w, h, c) => { g.fillStyle = c; g.fillRect(x, y, w, h); };
/* ── 今天是哪個節慶？ ── */
const lunarOf = d => {
  try {
    const p = new Intl.DateTimeFormat('en-u-ca-chinese', { month: 'numeric', day: 'numeric' }).formatToParts(d);
    const m = p.find(x => x.type === 'month').value, dd = p.find(x => x.type === 'day').value;
    return { leap: /bis|閏|leap/i.test(m), m: parseInt(m, 10), d: parseInt(dd, 10) };
  } catch (e) { return null; }
};
const FESTS = [   // 順序＝同樣遠時的優先順序；lo/hi＝往前、往後幾天
  { id: 'halloween', lo: 3, hi: 0, is: d => d.getMonth() === 9 && d.getDate() === 31 },
  { id: 'muertos',   lo: 1, hi: 1, is: d => d.getMonth() === 10 && d.getDate() === 2 },
  { id: 'cny',       lo: 3, hi: 3, is: d => { const l = lunarOf(d); return l && !l.leap && l.m === 1 && l.d === 1; } },
  { id: 'lantern',   lo: 3, hi: 3, is: d => { const l = lunarOf(d); return l && !l.leap && l.m === 1 && l.d === 15; } },
  { id: 'dragon',    lo: 3, hi: 3, is: d => { const l = lunarOf(d); return l && !l.leap && l.m === 5 && l.d === 5; } },
  { id: 'ghost',     lo: 3, hi: 3, is: d => { const l = lunarOf(d); return l && !l.leap && l.m === 7 && l.d === 15; } },
  { id: 'moon',      lo: 3, hi: 3, is: d => { const l = lunarOf(d); return l && !l.leap && l.m === 8 && l.d === 15; } },
  { id: 'xmas',      lo: 3, hi: 3, is: d => d.getMonth() === 11 && d.getDate() === 25 },
  { id: 'nye',       lo: 3, hi: 3, is: d => d.getMonth() === 11 && d.getDate() === 31 }
];
function detect(mode) {   // 順序：網址 ?fest= ＞ 後台設定 mode（off／節慶id／auto）＞ 照日期
  const q = new URLSearchParams(location.search).get('fest');
  if (q === '0') return null;
  if (q && FESTS.some(f => f.id === q)) return q;
  if (mode === 'off') return null;
  if (mode && FESTS.some(f => f.id === mode)) return mode;
  const now = new Date(); let best = null, bd = 99;
  FESTS.forEach(f => {
    for (let k = -f.hi; k <= f.lo; k++) {   // k＝今天離節日還有幾天（負的＝節日已過）
      const t = new Date(now.getFullYear(), now.getMonth(), now.getDate() + k, 12);
      if (f.is(t) && Math.abs(k) < bd) { bd = Math.abs(k); best = f.id; }
    }
  });
  return best;
}
let NAME = detect('auto');
const TINT = { halloween: '#9b86d0', muertos: '#9b86d0', cny: '#a07a9a', lantern: '#8593c8', dragon: '#8593c8', ghost: '#7a86b8', moon: '#7e8fcf', xmas: '#8593c8', nye: '#7c80c0' };

/* ── 裝飾用的小工具 ── */
const dot = (x, y, r, c) => { g.fillStyle = c; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); };
const L = b => ({ x: b.x * T, y: b.y * T, w: b.w * T, dx: b.door.x * T, dy: b.door.y * T, wallY: b.y * T + 2 * T });
const liveB = () => buildings.filter(b => b.sc.status !== 'build');
const openB = () => liveB().filter(b => !b.soon);
function scatter(thr, fn) {
  for (let y = 0; y < ROWS; y++) for (let x = 0; x < COLS; x++) {
    if (isRoad(x, y) || SIDEWALK_ROWS.includes(y) || (blocked[y] && blocked[y][x]) || y * T < camY - T || y * T > camY + VH) continue;
    const v = rnd(x, y, 11); if (v < thr) continue; fn(x * T, y * T, Math.floor((v - thr) * 1000));
  }
}
function burst(cx, cy, r, c, c2) {
  for (let i = 0; i < 16; i++) { const a = i / 16 * 6.283; for (let k = 1; k <= 3; k++) dot(cx + Math.cos(a) * r * k / 3, cy + Math.sin(a) * r * k / 3, k === 3 ? 2 : 1.5, k === 3 ? c2 : c); }
  dot(cx, cy, 2.5, '#fff');
}
function santaHat(x, y) { R(x, y + 4, 10, 3, '#fff'); R(x + 1, y, 8, 5, '#d6231a'); R(x + 5, y - 3, 4, 4, '#d6231a'); R(x + 8, y - 4, 3, 3, '#fff'); }
function partyHat(x, y, c) { R(x + 3, y, 4, 2, c); R(x + 2, y + 2, 6, 2, c); R(x + 1, y + 4, 8, 3, c); R(x + 4, y - 2, 2, 2, '#ffd34a'); }
// ───────── 各節慶 ─────────
function pumpkin(x, y, s = 1) {   // 左上角 x,y；約 16×14
  R(x + 7, y, 2, 4, '#3f7f3a');
  R(x + 1, y + 3, 14, 10, '#f28c28'); R(x + 3, y + 2, 10, 12, '#f28c28'); R(x + 5, y + 2, 1, 12, '#d9731a'); R(x + 10, y + 2, 1, 12, '#d9731a');
  R(x + 2, y + 5, 3, 2, '#fbb45a');
  R(x + 4, y + 6, 2, 2, '#ffe36a'); R(x + 10, y + 6, 2, 2, '#ffe36a');          // 眼睛（亮的）
  R(x + 4, y + 10, 8, 1, '#ffe36a'); R(x + 5, y + 11, 2, 1, '#ffe36a'); R(x + 9, y + 11, 2, 1, '#ffe36a');
}
function bat(x, y, f) {
  const c = '#241636';
  R(x, y, 4, 3, c); R(x, y - 2, 1, 2, c); R(x + 3, y - 2, 1, 2, c);
  R(x - 3, y - 1 + f, 3, 2, c); R(x - 6, y + f * 2, 3, 2, c); R(x - 8, y + 1 + f * 2, 2, 1, c);
  R(x + 4, y - 1 + f, 3, 2, c); R(x + 7, y + f * 2, 3, 2, c); R(x + 10, y + 1 + f * 2, 2, 1, c);
  R(x + 1, y + 1, 1, 1, '#ffd34a'); R(x + 2, y + 1, 1, 1, '#ffd34a');
}
function ghostDeco(x, y) {
  g.fillStyle = 'rgba(0,0,0,.2)'; g.fillRect(x + 6, y + 27, 18, 3);
  R(x + 8, y + 8, 14, 17, '#f4f4ff'); R(x + 10, y + 5, 10, 4, '#f4f4ff');
  R(x + 8, y + 24, 3, 3, '#f4f4ff'); R(x + 13, y + 24, 4, 2, '#f4f4ff'); R(x + 19, y + 24, 3, 3, '#f4f4ff');
  R(x + 11, y + 11, 2, 3, '#2a2540'); R(x + 17, y + 11, 2, 3, '#2a2540'); R(x + 14, y + 16, 3, 3, '#2a2540');
  R(x + 5, y + 14, 3, 4, '#f4f4ff'); R(x + 22, y + 14, 3, 4, '#f4f4ff');
}
function tomb(x, y) {
  g.fillStyle = 'rgba(0,0,0,.2)'; g.fillRect(x + 6, y + 25, 20, 4);
  R(x + 9, y + 9, 14, 17, '#9aa0ad'); R(x + 11, y + 6, 10, 4, '#9aa0ad'); R(x + 9, y + 9, 2, 17, '#b8bdc8'); R(x + 21, y + 9, 2, 17, '#7d8391');
  R(x + 15, y + 11, 2, 7, '#6a707e'); R(x + 13, y + 13, 6, 2, '#6a707e');
  R(x + 5, y + 24, 4, 3, '#4f8f45'); R(x + 23, y + 24, 4, 3, '#4f8f45');
}
function web(x, y, dir) {   // 屋頂角落的蜘蛛網；dir=1 左上角、-1 右上角
  g.save(); g.translate(x, y); g.scale(dir, 1); g.strokeStyle = 'rgba(255,255,255,.85)'; g.lineWidth = 1;
  g.beginPath(); g.moveTo(0, 0); g.lineTo(26, 0); g.moveTo(0, 0); g.lineTo(20, 20); g.moveTo(0, 0); g.lineTo(0, 26);
  g.moveTo(9, 0); g.quadraticCurveTo(7, 7, 0, 9); g.moveTo(17, 0); g.quadraticCurveTo(13, 13, 0, 17); g.moveTo(25, 0); g.quadraticCurveTo(19, 19, 0, 25); g.stroke();
  R(14, 14, 3, 3, '#1b1a22'); R(15, 17, 1, 3, '#1b1a22'); g.restore();
}
function bunting(x, y, w) {   // 屋頂上緣的三角旗：橘、紫、綠輪流
  const cols = ['#f28c28', '#7a4fc0', '#6cc04a'];
  g.strokeStyle = '#3a2a1e'; g.lineWidth = 1; g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + w / 2, y + 7, x + w, y); g.stroke();
  for (let i = 0, px = x + 5; px < x + w - 6; px += 12, i++) { const sag = 7 * (1 - Math.pow((px - x - w / 2) / (w / 2), 2)) * .9; g.fillStyle = cols[i % 3]; g.beginPath(); g.moveTo(px - 4, y + sag); g.lineTo(px + 4, y + sag); g.lineTo(px, y + sag + 10); g.fill(); }
}
function witchHat(x, y) { R(x, y + 5, 10, 2, '#2b1b3d'); R(x + 2, y + 2, 6, 4, '#2b1b3d'); R(x + 4, y - 1, 3, 3, '#2b1b3d'); R(x + 2, y + 4, 6, 1, '#f28c28'); }

function HWDECO(n) {
  const live = liveB();
  live.forEach(b => { const o = L(b), x = o.x, y = o.y, w = o.w, dx = o.dx, dy = o.dy;
    bunting(x + 2, y + 2, w - 4); web(x, y, 1); web(x + w, y, -1);
    if (!b.soon) { pumpkin(dx - 18, dy + 16); pumpkin(dx + 34, dy + 16); }
  });
  for (let y = 0; y < ROWS; y++) for (let x = 0; x < COLS; x++) {
    if (isRoad(x, y) || SIDEWALK_ROWS.includes(y) || (blocked[y] && blocked[y][x]) || y * T < camY - T || y * T > camY + VH) continue;
    const v = rnd(x, y, 11); if (v < .94) continue;
    const k = Math.floor((v - .94) * 1000) % 3;
    if (k === 0) tomb(x * T, y * T); else if (k === 1) pumpkin(x * T + 8, y * T + 10); else ghostDeco(x * T, y * T);
  }
  const t = Math.floor(n / 220) % 2;
  [[70, 36], [250, 64], [470, 28], [610, 90], [330, 250], [90, 300], [540, 330]].forEach(([bx, by], k) => { g.save(); g.translate(bx, by + camY); g.scale(2, 2); bat(0, 0, (t + k) % 2); g.restore(); });
  PETS.forEach(p => { if (p.kind === 'cat') witchHat(p.x * T + (p.dir > 0 ? 18 : 6), p.row * T + (p.pose === 'sit' ? 1 : 8)); });
}
function HWNIGHT() {
  const pk = [];
  openB().forEach(b => { const dx = b.door.x * T, dy = b.door.y * T; pk.push([dx - 18, dy + 16], [dx + 34, dy + 16]); });
  g.globalCompositeOperation = 'screen';
  pk.forEach(([x, y]) => { const gr = g.createRadialGradient(x + 8, y + 9, 1, x + 8, y + 9, 26); gr.addColorStop(0, 'rgba(255,150,40,.75)'); gr.addColorStop(1, 'rgba(255,150,40,0)'); g.fillStyle = gr; g.fillRect(x - 20, y - 20, 56, 58); });
  g.globalCompositeOperation = 'source-over';
  pk.forEach(([x, y]) => pumpkin(x, y));
}

const DECO = {
  muertos(n) {
    const cols = ['#ff4fa3', '#ff9b1a', '#2ec4b6', '#8e5bd6', '#ffd23f'];
    liveB().forEach(b => { const o = L(b); g.strokeStyle = '#3a2a1e'; g.lineWidth = 1; g.beginPath(); g.moveTo(o.x + 2, o.y + 3); g.quadraticCurveTo(o.x + o.w / 2, o.y + 8, o.x + o.w - 2, o.y + 3); g.stroke();
      for (let i = 0, px = o.x + 6; px < o.x + o.w - 12; px += 13, i++) { const sag = 5 * (1 - Math.pow((px - o.x - o.w / 2) / (o.w / 2), 2)); R(px, o.y + 3 + sag, 10, 13, cols[i % 5]); R(px + 2, o.y + 6 + sag, 2, 2, 'rgba(255,255,255,.85)'); R(px + 6, o.y + 6 + sag, 2, 2, 'rgba(255,255,255,.85)'); R(px + 4, o.y + 10 + sag, 2, 2, 'rgba(255,255,255,.85)'); R(px, o.y + 14 + sag, 2, 2, 'rgba(0,0,0,.25)'); } });
    openB().forEach(b => { const o = L(b);
      for (let i = 0; i < 9; i++) { const ox = Math.sin(i * 2.3) * 5; dot(o.dx + 16 + ox, o.dy + 36 + i * 5, 2.6, i % 2 ? '#ff9b1a' : '#ffb938'); dot(o.dx + 16 + ox + 3, o.dy + 38 + i * 5, 1.6, '#ff7a00'); }
      R(o.dx - 24, o.dy + 14, 18, 18, '#b9437a'); R(o.dx - 24, o.dy + 14, 18, 3, '#ffd23f'); R(o.dx - 22, o.dy + 8, 3, 7, '#fff2c8'); R(o.dx - 15, o.dy + 8, 3, 7, '#fff2c8'); dot(o.dx - 20.5, o.dy + 6, 2, '#ffb938'); dot(o.dx - 13.5, o.dy + 6, 2, '#ffb938'); dot(o.dx - 15, o.dy + 22, 4, '#ff9b1a'); dot(o.dx - 15, o.dy + 22, 2, '#ffd23f');
      const sx = o.dx + 36, sy = o.dy + 16; R(sx, sy, 14, 12, '#f7f3ea'); R(sx + 2, sy + 10, 10, 5, '#f7f3ea'); R(sx + 2, sy + 4, 4, 4, '#2b2b36'); R(sx + 8, sy + 4, 4, 4, '#2b2b36'); R(sx + 3, sy + 5, 2, 2, '#ff4fa3'); R(sx + 9, sy + 5, 2, 2, '#2ec4b6'); R(sx + 6, sy + 8, 2, 2, '#2b2b36'); R(sx + 3, sy + 12, 8, 1, '#2b2b36'); R(sx + 5, sy + 11, 1, 3, '#2b2b36'); R(sx + 8, sy + 11, 1, 3, '#2b2b36'); R(sx + 1, sy + 1, 3, 2, '#ff9b1a'); R(sx + 10, sy + 1, 3, 2, '#8e5bd6'); });
    scatter(.945, (x, y, k) => { for (let i = 0; i < 5; i++) dot(x + 6 + (i % 3) * 8, y + 10 + Math.floor(i / 3) * 8, 3.2, i % 2 ? '#ff9b1a' : '#ffb938'); });
  },
  cny(n) {
    liveB().forEach(b => { const o = L(b);
      [o.x + 10, o.x + o.w - 10].forEach(lx => { R(lx - 1, o.y, 2, 6, '#3a2a1e'); R(lx - 4, o.y + 5, 8, 2, '#e8b923'); dot(lx, o.y + 13, 8, '#d6231a'); dot(lx - 2, o.y + 10, 2.2, '#f26a5a'); R(lx - 3, o.y + 20, 6, 2, '#e8b923'); R(lx - 1, o.y + 22, 2, 6, '#e8b923'); R(lx - 6, o.y + 11, 1, 5, '#a8160f'); R(lx + 5, o.y + 11, 1, 5, '#a8160f'); });
      g.fillStyle = '#d6231a'; g.beginPath(); g.moveTo(o.x + 28, o.y + 4); [0, 1, 2, 3].forEach(() => 0); g.stroke();
    });
    openB().forEach(b => { const o = L(b);
      [[o.dx - 14, 0], [o.dx + 38, 0]].forEach(([cx]) => { R(cx, o.dy + 2, 8, 28, '#d6231a'); R(cx + 1, o.dy + 3, 6, 1, '#e8b923'); for (let i = 0; i < 4; i++) { R(cx + 2, o.dy + 7 + i * 6, 4, 1, '#e8b923'); R(cx + 3, o.dy + 9 + i * 6, 2, 1, '#e8b923'); } });
      g.save(); g.translate(o.dx + 16, o.dy - 5); g.rotate(.785); R(-5, -5, 10, 10, '#d6231a'); R(-4, -4, 8, 1, '#e8b923'); R(-4, 3, 8, 1, '#e8b923'); R(-1, -2, 2, 4, '#e8b923'); g.restore();
    });
    // 鞭炮串（人行道上）
    scatter(.955, (x, y) => { R(x + 8, y + 6, 3, 14, '#d6231a'); R(x + 14, y + 4, 3, 14, '#d6231a'); R(x + 20, y + 6, 3, 14, '#d6231a'); R(x + 8, y + 6, 3, 3, '#e8b923'); R(x + 14, y + 4, 3, 3, '#e8b923'); R(x + 20, y + 6, 3, 3, '#e8b923'); R(x + 14, y, 1, 4, '#3a2a1e'); });
  },
  lantern(n) {
    const cols = ['#ff5a5a', '#ffb02e', '#4fc3f7', '#7ed957', '#d38bff'];
    liveB().forEach((b, bi) => { const o = L(b); g.strokeStyle = '#3a2a1e'; g.lineWidth = 1; g.beginPath(); g.moveTo(o.x, o.y + 6); g.quadraticCurveTo(o.x + o.w / 2, o.y + 12, o.x + o.w, o.y + 6); g.stroke();
      for (let i = 0, px = o.x + 8; px < o.x + o.w - 6; px += 14, i++) { const sag = 6 * (1 - Math.pow((px - o.x - o.w / 2) / (o.w / 2), 2)); const c = cols[(i + bi) % 5]; R(px - 1, o.y + 6 + sag, 2, 3, '#3a2a1e'); dot(px, o.y + 15 + sag, 5.5, c); R(px - 2, o.y + 20 + sag, 4, 4, '#ffe9a8'); R(px - 1, o.y + 8 + sag, 2, 2, 'rgba(255,255,255,.7)'); } });
    // 兔子花燈
    scatter(.95, (x, y) => { R(x + 8, y + 2, 4, 12, '#fff'); R(x + 18, y + 2, 4, 12, '#fff'); R(x + 9, y + 4, 2, 8, '#ffb0c8'); R(x + 19, y + 4, 2, 8, '#ffb0c8'); dot(x + 15, y + 20, 9, '#fff'); dot(x + 15, y + 24, 6, '#fff'); R(x + 10, y + 17, 3, 3, '#d6231a'); R(x + 18, y + 17, 3, 3, '#d6231a'); R(x + 14, y + 21, 3, 2, '#ffb0c8'); R(x + 3, y + 27, 24, 2, '#8a5a2b'); });
    // 天燈
    [[60, 40], [180, 110], [300, 50], [420, 130], [520, 60], [600, 150], [120, 240], [260, 300], [480, 280], [570, 360]].forEach(([sx, sy], i) => { const x = sx, y = sy + camY - ((n / 60) % 12) * 0; R(x, y, 12, 16, '#ffe59a'); R(x, y, 12, 3, '#e8a32a'); R(x + 2, y + 5, 3, 7, '#ffd46a'); R(x + 5, y + 16, 2, 3, '#ff7a00'); R(x + 2, y + 12, 1, 3, '#d6231a'); });
  },
  dragon(n) {
    liveB().forEach(b => { const o = L(b);
      [o.x + 12, o.x + o.w - 20].forEach((zx, k) => { R(zx + 7, o.y + 4, 1, 10, '#3a2a1e'); for (let j = 0; j < 3; j++) { const px = zx + j * 7 - 3, py = o.y + 12 + (j === 1 ? 4 : 0); g.fillStyle = '#4f9a43'; g.beginPath(); g.moveTo(px, py + 12); g.lineTo(px + 8, py + 12); g.lineTo(px + 4, py); g.fill(); g.fillStyle = '#3b7d34'; g.beginPath(); g.moveTo(px + 4, py); g.lineTo(px + 8, py + 12); g.lineTo(px + 4, py + 12); g.fill(); R(px + 3, py + 5, 2, 7, '#d6231a'); } });
    });
    openB().forEach(b => { const o = L(b);
      for (let i = -2; i <= 2; i++) { g.strokeStyle = '#3f8a3a'; g.lineWidth = 2; g.beginPath(); g.moveTo(o.dx + 16, o.dy + 6); g.lineTo(o.dx + 16 + i * 5, o.dy - 12 + Math.abs(i)); g.stroke(); }
      R(o.dx + 13, o.dy + 3, 6, 4, '#d6231a'); dot(o.dx + 16, o.dy - 13, 2, '#8e5bd6');
      [[o.dx - 14, '#e83a6a'], [o.dx + 38, '#f2b632']].forEach(([cx, c]) => { R(cx + 3, o.dy + 4, 1, 6, '#3a2a1e'); g.fillStyle = c; g.beginPath(); g.moveTo(cx + 4, o.dy + 10); g.lineTo(cx + 10, o.dy + 17); g.lineTo(cx + 4, o.dy + 24); g.lineTo(cx - 2, o.dy + 17); g.fill(); R(cx + 3, o.dy + 15, 2, 2, '#fff'); R(cx + 3, o.dy + 24, 1, 5, c); });
    });
    // 龍舟（草地上）
    scatter(.965, (x, y) => { R(x + 2, y + 18, 28, 6, '#d6231a'); R(x + 5, y + 24, 22, 3, '#a8160f'); R(x + 26, y + 10, 6, 10, '#2f9a4a'); R(x + 29, y + 8, 4, 4, '#2f9a4a'); R(x + 30, y + 9, 1, 1, '#fff'); for (let i = 0; i < 4; i++) { R(x + 6 + i * 6, y + 13, 4, 5, '#ffd23f'); R(x + 7 + i * 6, y + 10, 2, 3, '#f1c9a0'); } });
  },
  ghost(n) {
    liveB().forEach((b, bi) => { const o = L(b);
      [o.x + 14, o.x + o.w - 14].forEach(lx => { R(lx - 1, o.y, 2, 5, '#3a2a1e'); dot(lx, o.y + 12, 7, '#f7f1dc'); R(lx - 7, o.y + 11, 14, 1, '#d8cfae'); R(lx - 3, o.y + 6, 6, 1, '#d8cfae'); R(lx - 3, o.y + 18, 6, 1, '#d8cfae'); R(lx - 2, o.y + 19, 4, 3, '#d6231a'); });
    });
    openB().forEach((b, bi) => { const o = L(b);
      if (bi % 2 === 0) { const tx = o.dx - 28, ty = o.dy + 22; R(tx, ty, 24, 12, '#c4252b'); R(tx, ty, 24, 2, '#e8b923'); dot(tx + 6, ty - 2, 4, '#ff9b1a'); dot(tx + 13, ty - 1, 3.2, '#e8d24a'); R(tx + 17, ty - 4, 5, 4, '#f4e4b8'); R(tx + 4, ty + 12, 2, 5, '#4a3320'); R(tx + 18, ty + 12, 2, 5, '#4a3320');
        [8, 13, 18].forEach(ix => { R(tx + ix, ty - 14, 1, 10, '#6b4a2f'); R(tx + ix, ty - 15, 1, 2, '#ff3a1a'); });
        g.strokeStyle = 'rgba(220,220,230,.55)'; g.lineWidth = 2; g.beginPath(); g.moveTo(tx + 13, ty - 16); g.bezierCurveTo(tx + 6, ty - 26, tx + 20, ty - 30, tx + 12, ty - 42); g.stroke();
      } else { const bx = o.dx + 38, by = o.dy + 22; R(bx, by + 4, 16, 14, '#5a5560'); R(bx - 1, by + 3, 18, 3, '#3d3a42'); R(bx + 2, by - 3, 4, 8, '#ff7a00'); R(bx + 8, by - 8, 4, 12, '#ff9b1a'); R(bx + 12, by - 4, 3, 8, '#ffd23f'); R(bx + 4, by + 1, 8, 4, '#ffe38a');
        g.strokeStyle = 'rgba(190,190,200,.5)'; g.lineWidth = 2; g.beginPath(); g.moveTo(bx + 8, by - 10); g.bezierCurveTo(bx + 14, by - 20, bx + 2, by - 24, bx + 10, by - 36); g.stroke(); }
    });
  },
  moon(n) {
    liveB().forEach((b, bi) => { const o = L(b);
      [o.x + 12, o.x + o.w / 2, o.x + o.w - 12].forEach((lx, k) => { R(lx, o.y, 1, 6, '#3a2a1e'); dot(lx, o.y + 13, 7, k === 1 ? '#ffb02e' : '#ff7a3a'); R(lx - 2, o.y + 5, 4, 2, '#e8b923'); R(lx - 1, o.y + 20, 2, 4, '#e8b923'); R(lx - 4, o.y + 10, 2, 2, 'rgba(255,255,255,.5)'); });
    });
    openB().forEach((b, bi) => { const o = L(b);
      dot(o.dx - 12, o.dy + 24, 8, '#d9d35a'); dot(o.dx - 14, o.dy + 21, 3, '#eee98a'); R(o.dx - 14, o.dy + 14, 4, 4, '#4f9a43'); R(o.dx - 12, o.dy + 12, 2, 3, '#3b7d34');
      if (bi % 2 === 0) { const gx = o.dx + 38, gy = o.dy + 22; R(gx, gy + 6, 18, 10, '#2e2e36'); R(gx + 2, gy + 5, 14, 2, '#ff3a1a'); R(gx + 4, gy + 4, 3, 2, '#ffb02e'); R(gx + 2, gy + 16, 2, 5, '#2e2e36'); R(gx + 14, gy + 16, 2, 5, '#2e2e36'); R(gx + 4, gy + 1, 10, 1, '#b8b8c4'); [[6, -4, 4], [12, -12, 5], [9, -22, 6]].forEach(([ox, oy, r]) => dot(gx + ox, gy + oy, r, 'rgba(210,210,220,.55)')); }
    });
    // 月亮（固定在畫面右上）
    const mx = W - 62, my = camY + 56; dot(mx, my, 26, 'rgba(255,243,176,.25)'); dot(mx, my, 21, '#fff3b0'); dot(mx - 6, my - 5, 4, '#f0e090'); dot(mx + 7, my + 4, 5, '#f0e090'); dot(mx - 2, my + 9, 2.5, '#f0e090'); dot(mx + 5, my - 9, 2, '#f0e090');
  },
  xmas(n) {
    const cols = ['#ff3b3b', '#ffd23f', '#3bd16f', '#3bb0ff', '#ff7ad9'];
    liveB().forEach(b => { const o = L(b); g.strokeStyle = '#1f5a2a'; g.lineWidth = 2; g.beginPath(); g.moveTo(o.x, o.y + 4); g.quadraticCurveTo(o.x + o.w / 2, o.y + 12, o.x + o.w, o.y + 4); g.stroke();
      for (let i = 0, px = o.x + 6; px < o.x + o.w - 4; px += 10, i++) { const sag = 8 * (1 - Math.pow((px - o.x - o.w / 2) / (o.w / 2), 2)); dot(px, o.y + 5 + sag, 2.6, cols[i % 5]); } });
    openB().forEach(b => { const o = L(b);
      [o.dx - 22, o.dx + 36].forEach((tx, k) => { const ty = o.dy + 2; R(tx + 7, ty + 26, 4, 5, '#7a4e2b'); [[2, 18, 14], [4, 10, 10], [6, 4, 6]].forEach(([ox, oy, w]) => { g.fillStyle = '#2f8f46'; g.beginPath(); g.moveTo(tx + 9, ty + oy - 5); g.lineTo(tx + 9 + w, ty + oy + 9); g.lineTo(tx + 9 - w, ty + oy + 9); g.fill(); }); R(tx + 8, ty - 2, 2, 2, '#ffd23f'); dot(tx + 5, ty + 15, 1.6, '#ff3b3b'); dot(tx + 13, ty + 19, 1.6, '#ffd23f'); dot(tx + 9, ty + 9, 1.6, '#3bb0ff'); dot(tx + 4, ty + 22, 1.6, '#ff7ad9'); R(tx + 14, ty + 24, 5, 5, '#d6231a'); R(tx + 16, ty + 24, 1, 5, '#ffd23f'); });
      g.strokeStyle = '#2f8f46'; g.lineWidth = 4; g.beginPath(); g.arc(o.dx + 16, o.dy + 14, 7, 0, 7); g.stroke(); R(o.dx + 13, o.dy + 20, 6, 3, '#d6231a'); dot(o.dx + 12, o.dy + 8, 1.6, '#d6231a'); dot(o.dx + 20, o.dy + 10, 1.6, '#d6231a');
    });
    scatter(.96, (x, y) => { dot(x + 16, y + 24, 8, '#fff'); dot(x + 16, y + 14, 6, '#fff'); R(x + 13, y + 11, 2, 2, '#2b2b36'); R(x + 18, y + 11, 2, 2, '#2b2b36'); R(x + 16, y + 14, 3, 2, '#ff8a1a'); R(x + 11, y + 6, 10, 2, '#2b2b36'); R(x + 13, y + 1, 6, 6, '#2b2b36'); R(x + 6, y + 18, 3, 1, '#7a4e2b'); R(x + 23, y + 18, 3, 1, '#7a4e2b'); });
    for (let i = 0; i < 40; i++) { const sx = (i * 97) % W, sy = camY + ((i * 53 + n / 40) % VH); R(sx, sy, 2, 2, 'rgba(255,255,255,.85)'); }
    PETS.forEach(p => santaHat(p.x * T + (p.dir > 0 ? 17 : 5), p.row * T + (p.pose === 'sit' ? 1 : 7)));
  },
  nye(n) {
    liveB().forEach((b, bi) => { const o = L(b); ['#ffd34a', '#c8d0e0'].forEach((c, k) => { g.strokeStyle = c; g.lineWidth = 2; g.beginPath(); g.moveTo(o.x, o.y + 4); g.quadraticCurveTo(o.x + o.w / 2, o.y + 12 + k * 4, o.x + o.w, o.y + 4); g.stroke(); });
      for (let i = 0, px = o.x + 8; px < o.x + o.w - 4; px += 14, i++) dot(px, o.y + 9 + i % 2 * 3, 2, ['#ff4fa3', '#4fd1ff', '#ffd34a'][i % 3]); });
    openB().forEach((b, bi) => { const o = L(b);
      [[o.dx - 16, ['#ff4fa3', '#4fd1ff']], [o.dx + 36, ['#ffd34a', '#a56bff']]].forEach(([bx, cs]) => cs.forEach((c, k) => { const x = bx + k * 7, y = o.dy + 4 + k * 5; g.strokeStyle = '#6b6b78'; g.lineWidth = 1; g.beginPath(); g.moveTo(x, y + 12); g.lineTo(x + 2 - k * 3, y + 28); g.stroke(); g.fillStyle = c; g.beginPath(); g.ellipse(x, y + 5, 6, 8, 0, 0, 7); g.fill(); R(x - 3, y + 1, 2, 3, 'rgba(255,255,255,.6)'); }));
    });
    // 橫幅 2027（第一排建築之間）
    const top = liveB().filter(b => b.y * T > camY - 20 && b.y * T < camY + VH - 100);
    if (top.length) { const o = L(top[0]); const bx = o.x - 6, by = Math.max(camY + 4, o.y - 28); R(bx, by, 150, 24, '#1b1a22'); g.strokeStyle = '#ffd34a'; g.lineWidth = 2; g.strokeRect(bx, by, 150, 24); g.fillStyle = '#ffd34a'; g.font = 'bold 18px sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('★ ' + (new Date().getMonth() === 11 ? new Date().getFullYear() + 1 : new Date().getFullYear()) + ' ★', bx + 75, by + 13); }
    for (let i = 0; i < 70; i++) { const sx = (i * 71) % W, sy = camY + ((i * 37) % VH); R(sx, sy, 3, 3, ['#ff4fa3', '#4fd1ff', '#ffd34a', '#7ed957', '#a56bff'][i % 5]); }
    PETS.forEach((p, i) => partyHat(p.x * T + (p.dir > 0 ? 17 : 5), p.row * T + (p.pose === 'sit' ? 2 : 8), ['#ff4fa3', '#4fd1ff', '#ffd34a'][i % 3]));
  },
  halloween(n) { HWDECO(n); }
};
function glowAt(x, y, r, c, a) { const gr = g.createRadialGradient(x, y, 1, x, y, r); gr.addColorStop(0, `rgba(${c},${a})`); gr.addColorStop(1, `rgba(${c},0)`); g.fillStyle = gr; g.fillRect(x - r, y - r, r * 2, r * 2); }
const NIGHTFX = {
  muertos() { g.globalCompositeOperation = 'screen'; openB().forEach(b => { const o = L(b); glowAt(o.dx - 17, o.dy + 8, 26, '255,190,70', .8); for (let i = 0; i < 9; i++) glowAt(o.dx + 16 + Math.sin(i * 2.3) * 5, o.dy + 36 + i * 5, 10, '255,160,40', .5); }); liveB().forEach(b => { const o = L(b); glowAt(o.x + o.w / 2, o.y + 12, 50, '255,120,200', .25); }); g.globalCompositeOperation = 'source-over'; },
  cny() { g.globalCompositeOperation = 'screen'; liveB().forEach(b => { const o = L(b); [o.x + 10, o.x + o.w - 10].forEach(lx => glowAt(lx, o.y + 13, 30, '255,60,40', .85)); }); g.globalCompositeOperation = 'source-over'; liveB().forEach(b => { const o = L(b); [o.x + 10, o.x + o.w - 10].forEach(lx => { dot(lx, o.y + 13, 8, '#ff3b2a'); dot(lx - 2, o.y + 10, 2.4, '#ffa59a'); R(lx - 3, o.y + 20, 6, 2, '#ffd34a'); }); });
    [[90, 60, '#ffd34a', '#ff5a5a'], [330, 40, '#4fd1ff', '#ffffff'], [560, 90, '#ff7ad9', '#ffd34a'], [200, 170, '#7ed957', '#ffd34a']].forEach(([x, y, c, c2]) => { g.globalCompositeOperation = 'screen'; glowAt(x, y + camY, 40, '255,220,120', .35); g.globalCompositeOperation = 'source-over'; burst(x, y + camY, 26, c, c2); }); },
  lantern() { g.globalCompositeOperation = 'screen'; const cols = ['255,90,90', '255,180,50', '80,190,250', '120,220,90', '210,140,255']; liveB().forEach((b, bi) => { const o = L(b); for (let i = 0, px = o.x + 8; px < o.x + o.w - 6; px += 14, i++) { const sag = 6 * (1 - Math.pow((px - o.x - o.w / 2) / (o.w / 2), 2)); glowAt(px, o.y + 15 + sag, 22, cols[(i + bi) % 5], .75); } });
    [[60, 40], [180, 110], [300, 50], [420, 130], [520, 60], [600, 150], [120, 240], [260, 300], [480, 280], [570, 360]].forEach(([sx, sy]) => glowAt(sx + 6, sy + camY + 8, 34, '255,200,90', .85)); g.globalCompositeOperation = 'source-over';
    [[60, 40], [180, 110], [300, 50], [420, 130], [520, 60], [600, 150], [120, 240], [260, 300], [480, 280], [570, 360]].forEach(([sx, sy]) => { const x = sx, y = sy + camY; R(x, y, 12, 16, '#ffe9a8'); R(x, y, 12, 3, '#e8a32a'); R(x + 5, y + 16, 2, 3, '#ff7a00'); }); },
  dragon() { g.globalCompositeOperation = 'screen'; liveB().forEach(b => { const o = L(b); glowAt(o.x + o.w / 2, o.y + 20, 44, '120,255,150', .18); }); g.globalCompositeOperation = 'source-over'; },
  ghost() { g.globalCompositeOperation = 'screen'; liveB().forEach(b => { const o = L(b); [o.x + 14, o.x + o.w - 14].forEach(lx => glowAt(lx, o.y + 12, 28, '255,235,170', .85)); }); openB().forEach((b, bi) => { const o = L(b); if (bi % 2 === 0) glowAt(o.dx - 22, o.dy + 20, 30, '255,150,60', .8); else glowAt(o.dx + 46, o.dy + 22, 34, '255,120,30', .9); }); g.globalCompositeOperation = 'source-over'; liveB().forEach(b => { const o = L(b); [o.x + 14, o.x + o.w - 14].forEach(lx => { dot(lx, o.y + 12, 7, '#fff8e0'); R(lx - 2, o.y + 19, 4, 3, '#ff5a3a'); }); }); },
  moon() { g.globalCompositeOperation = 'screen'; glowAt(W - 62, camY + 56, 90, '255,243,176', .5); liveB().forEach(b => { const o = L(b); [o.x + 12, o.x + o.w / 2, o.x + o.w - 12].forEach(lx => glowAt(lx, o.y + 13, 24, '255,160,60', .8)); }); openB().forEach((b, bi) => { const o = L(b); if (bi % 2 === 0) glowAt(o.dx + 47, o.dy + 28, 26, '255,70,20', .9); }); g.globalCompositeOperation = 'source-over'; const mx = W - 62, my = camY + 56; dot(mx, my, 21, '#fff7c4'); dot(mx - 6, my - 5, 4, '#f2e69a'); dot(mx + 7, my + 4, 5, '#f2e69a'); dot(mx - 2, my + 9, 2.5, '#f2e69a'); liveB().forEach(b => { const o = L(b); [o.x + 12, o.x + o.w / 2, o.x + o.w - 12].forEach((lx, k) => dot(lx, o.y + 13, 7, k === 1 ? '#ffc04a' : '#ff8a4a')); }); },
  xmas() { g.globalCompositeOperation = 'screen'; const cols = ['255,60,60', '255,210,60', '60,210,110', '60,170,255', '255,120,220']; liveB().forEach(b => { const o = L(b); for (let i = 0, px = o.x + 6; px < o.x + o.w - 4; px += 10, i++) { const sag = 8 * (1 - Math.pow((px - o.x - o.w / 2) / (o.w / 2), 2)); glowAt(px, o.y + 5 + sag, 12, cols[i % 5], .9); } }); openB().forEach(b => { const o = L(b); [o.dx - 13, o.dx + 45].forEach(tx => { glowAt(tx, o.dy + 14, 22, '255,230,120', .55); }); }); g.globalCompositeOperation = 'source-over'; liveB().forEach(b => { const o = L(b); for (let i = 0, px = o.x + 6; px < o.x + o.w - 4; px += 10, i++) { const sag = 8 * (1 - Math.pow((px - o.x - o.w / 2) / (o.w / 2), 2)); dot(px, o.y + 5 + sag, 2.8, ['#ff4a4a', '#ffd84a', '#4ae07c', '#4ab8ff', '#ff86e0'][i % 5]); } }); },
  nye() { [[90, 60, '#ffd34a', '#ff5a5a'], [250, 120, '#4fd1ff', '#ffffff'], [420, 50, '#ff7ad9', '#ffd34a'], [560, 140, '#7ed957', '#ffd34a'], [150, 230, '#a56bff', '#4fd1ff'], [500, 300, '#ffd34a', '#ff7ad9']].forEach(([x, y, c, c2]) => { g.globalCompositeOperation = 'screen'; glowAt(x, y + camY, 55, '255,220,140', .35); g.globalCompositeOperation = 'source-over'; burst(x, y + camY, 32, c, c2); }); },
  halloween() { HWNIGHT(); }
};

/* ── 說話的角色 ── */
const WHOS = {
  ghost: ['鬼魂', '鬼魂', 'Fantasma', 'Ghost'], witch: ['女巫', '女巫', 'Bruja', 'Witch'], zombie: ['殭屍', '僵尸', 'Zombi', 'Zombie'],
  nian: ['年獸', '年兽', 'Monstruo Nian', 'Nian beast'], dragon: ['龍', '龙', 'Dragón', 'Dragon'], rabbit: ['兔子', '兔子', 'Conejo', 'Rabbit'],
  santa: ['聖誕老人', '圣诞老人', 'Papá Noel', 'Santa Claus'], reindeer: ['馴鹿', '驯鹿', 'Reno', 'Reindeer']
};
let whoDone = false;
const TALK = {
  ghost_halloween: [
    ['不給糖，就搗蛋！', '不给糖，就捣蛋！', 'bù gěi táng, jiù dǎo dàn!', '¡Dulce o truco!', 'Trick or treat!'],
    ['嘻嘻，我是小鬼，你不要怕。', '嘻嘻，我是小鬼，你不要怕。', 'xī xī, wǒ shì xiǎo guǐ, nǐ bú yào pà.', 'Jeje, soy un fantasmita, no tengas miedo.', "Hehe, I'm a little ghost — don't be afraid."]],
  ghost_muertos: [
    ['歡迎回家！今天是亡靈節。', '欢迎回家！今天是亡灵节。', 'huān yíng huí jiā! jīn tiān shì wáng líng jié.', '¡Bienvenido a casa! Hoy es el Día de Muertos.', 'Welcome home! Today is the Day of the Dead.'],
    ['我想念家人，所以回來看看。', '我想念家人，所以回来看看。', 'wǒ xiǎng niàn jiā rén, suǒ yǐ huí lái kàn kan.', 'Extraño a mi familia, así que vine a visitarla.', 'I miss my family, so I came back to visit.']],
  ghost_ghost: [
    ['農曆七月，鬼門開了。', '农历七月，鬼门开了。', 'nóng lì qī yuè, guǐ mén kāi le.', 'Es el séptimo mes lunar: se abre la puerta de los fantasmas.', 'It is the seventh lunar month: the Ghost Gate is open.'],
    ['我是好兄弟，請不要怕我。', '我是好兄弟，请不要怕我。', 'wǒ shì hǎo xiōng dì, qǐng bú yào pà wǒ.', 'Soy un «buen hermano» (así se llama con respeto a los espíritus); por favor, no me tengas miedo.', 'I am a "good brother" (a polite name for spirits) — please don\'t be afraid of me.']],
  witch: [
    ['小心！我要飛過去了！', '小心！我要飞过去了！', 'xiǎo xīn! wǒ yào fēi guò qù le!', '¡Cuidado! ¡Voy a pasar volando!', "Watch out! I'm flying through!"],
    ['萬聖節快樂！你的糖果呢？', '万圣节快乐！你的糖果呢？', 'wàn shèng jié kuài lè! nǐ de táng guǒ ne?', '¡Feliz Halloween! ¿Y tus dulces?', 'Happy Halloween! Where are your candies?']],
  zombie: [
    ['我好餓⋯⋯我想吃糖果。', '我好饿⋯⋯我想吃糖果。', 'wǒ hǎo è…… wǒ xiǎng chī táng guǒ.', 'Tengo mucha hambre… quiero dulces.', "I'm so hungry… I want candy."],
    ['不要怕，我只是在散步。', '不要怕，我只是在散步。', 'bú yào pà, wǒ zhǐ shì zài sàn bù.', 'No tengas miedo, solo estoy paseando.', "Don't be scared, I'm just taking a walk."]],
  nian: [
    ['新年快樂！恭喜發財！', '新年快乐！恭喜发财！', 'xīn nián kuài lè! gōng xǐ fā cái!', '¡Feliz Año Nuevo! ¡Que te llegue la prosperidad!', 'Happy New Year! Wishing you prosperity!'],
    ['我是年獸，我最怕紅色和鞭炮！', '我是年兽，我最怕红色和鞭炮！', 'wǒ shì nián shòu, wǒ zuì pà hóng sè hàn biān pào!', 'Soy el monstruo Nian: ¡le tengo miedo al rojo y a los petardos!', "I am the Nian beast — I'm most afraid of red and firecrackers!"]],
  dragon: [
    ['端午節快樂！你吃粽子了嗎？', '端午节快乐！你吃粽子了吗？', 'duān wǔ jié kuài lè! nǐ chī zòng zi le ma?', '¡Feliz Festival del Bote del Dragón! ¿Ya comiste zongzi?', 'Happy Dragon Boat Festival! Have you eaten zongzi yet?'],
    ['今天有龍舟比賽，一起來看吧！', '今天有龙舟比赛，一起来看吧！', 'jīn tiān yǒu lóng zhōu bǐ sài, yì qǐ lái kàn ba!', 'Hoy hay carrera de botes dragón, ¡vamos a verla!', "There is a dragon boat race today — let's go watch!"]],
  rabbit: [
    ['中秋節快樂！你吃月餅了嗎？', '中秋节快乐！你吃月饼了吗？', 'zhōng qiū jié kuài lè! nǐ chī yuè bǐng le ma?', '¡Feliz Festival de Medio Otoño! ¿Ya comiste pastel de luna?', 'Happy Mid-Autumn Festival! Have you had mooncake yet?'],
    ['今天晚上月亮好圓喔！', '今天晚上月亮好圆喔！', 'jīn tiān wǎn shàng yuè liàng hǎo yuán ō!', '¡Esta noche la luna está muy redonda!', 'The moon is so round tonight!'],
    ['我住在月亮上，這裡也很好玩。', '我住在月亮上，这里也很好玩。', 'wǒ zhù zài yuè liàng shàng, zhè lǐ yě hěn hǎo wán.', 'Vivo en la luna, ¡pero aquí también es divertido!', "I live on the moon, but it's fun here too!"]],
  santa: [
    ['聖誕快樂！Ho ho ho！', '圣诞快乐！Ho ho ho！', 'shèng dàn kuài lè! Ho ho ho!', '¡Feliz Navidad! ¡Jo, jo, jo!', 'Merry Christmas! Ho ho ho!'],
    ['你想要什麼聖誕禮物？', '你想要什么圣诞礼物？', 'nǐ xiǎng yào shén me shèng dàn lǐ wù?', '¿Qué regalo de Navidad quieres?', 'What Christmas present do you want?']],
  reindeer: [
    ['我要幫聖誕老人送禮物。', '我要帮圣诞老人送礼物。', 'wǒ yào bāng shèng dàn lǎo rén sòng lǐ wù.', 'Voy a ayudar a Papá Noel a repartir regalos.', "I'm helping Santa deliver presents."],
    ['我的鼻子是紅色的，好不好看？', '我的鼻子是红色的，好不好看？', 'wǒ de bí zi shì hóng sè de, hǎo bù hǎo kàn?', 'Mi nariz es roja, ¿verdad que es bonita?', 'My nose is red — isn\'t it nice?']],
  sleigh: [
    ['Ho ho ho！我要去送禮物囉！', 'Ho ho ho！我要去送礼物啰！', 'Ho ho ho! wǒ yào qù sòng lǐ wù lō!', '¡Jo, jo, jo! ¡Voy a repartir regalos!', 'Ho ho ho! Off to deliver presents!'],
    ['聖誕快樂！', '圣诞快乐！', 'shèng dàn kuài lè!', '¡Feliz Navidad!', 'Merry Christmas!']]
};

/* ── 角色的畫法（都用小方塊拼成；x,y 是畫面上的位置） ── */
const at = (x, y, s, f, fn) => { g.save(); g.translate(x, y); g.scale(f ? -s : s, s); fn(); g.restore(); };
function glow(x, y, r, c, a) { const gr = g.createRadialGradient(x, y, 1, x, y, r); gr.addColorStop(0, `rgba(${c},${a})`); gr.addColorStop(1, `rgba(${c},0)`); g.fillStyle = gr; g.fillRect(x - r, y - r, r * 2, r * 2); }
function ghostSpr(x, y, n, i, tint, bodyC) {
  g.save(); g.globalCompositeOperation = 'screen'; glow(x + 14, y + 14, 38, tint, .45); g.restore();
  g.save(); g.globalAlpha = .82;
  at(x, y, 1.3, 0, () => {
    const w = Math.sin(n / 200 + i) > 0 ? 1 : 0;
    R(2, 6, 18, 18, bodyC); R(4, 3, 14, 4, bodyC); R(6, 1, 10, 3, bodyC);
    R(2, 24, 4, 3 + w, bodyC); R(8, 24, 4, 4 - w, bodyC); R(14, 24, 4, 3 + w, bodyC); R(18, 24, 2, 3, bodyC);
    R(-2, 12 + w, 4, 5, bodyC); R(20, 12 + (1 - w), 4, 5, bodyC);
    R(6, 9, 3, 4, '#2a2540'); R(14, 9, 3, 4, '#2a2540'); R(10, 16, 4, 4, '#2a2540');
  });
  g.restore();
}
function witchSpr(x, y, n, f) {
  at(x, y + Math.sin(n / 300) * 4, 2.2, f, () => {
    R(-2, 11, 26, 2, '#7a4a22'); for (let k = 0; k < 4; k++) R(-8 - k, 9 + k, 7, 1, '#e0b341'); R(-9, 10, 8, 3, '#e0b341');
    R(6, 3, 8, 8, '#241636'); R(5, 8, 10, 3, '#241636'); R(14, 8, 3, 4, '#241636');
    R(8, -4, 6, 7, '#f0c9a0'); R(8, -6, 6, 3, '#4a2d7a');
    R(5, -4, 12, 2, '#241636'); R(8, -9, 6, 5, '#241636'); R(10, -12, 3, 4, '#241636'); R(8, -5, 6, 1, '#f28c28');
    R(9, -2, 1, 1, '#241636'); R(12, -2, 1, 1, '#241636'); R(6, -3, 2, 6, '#4a2d7a'); R(5, 1, 2, 5, '#4a2d7a');
  });
}
function zombieSpr(x, y, n, f) {
  const st = Math.floor(n / 350) % 2;
  at(x, y, 1.5, f, () => {
    R(5, 20 + st, 4, 7, '#4a4a5a'); R(11, 20 + (1 - st), 4, 7, '#4a4a5a'); R(4, 26, 5, 2, '#2b2b36'); R(11, 26, 5, 2, '#2b2b36');
    R(4, 11, 12, 10, '#5b6f8a'); R(4, 17, 3, 3, '#3d4a5e'); R(12, 14, 2, 2, '#8bc06a');
    R(15, 11, 9, 3, '#8bc06a'); R(15, 15, 8, 3, '#8bc06a');
    R(5, 2, 10, 9, '#8bc06a'); R(4, 1, 12, 3, '#3a2a1e'); R(6, 5, 2, 2, '#fff'); R(11, 5, 2, 2, '#fff'); R(7, 6, 1, 1, '#c0201a'); R(12, 6, 1, 1, '#c0201a'); R(7, 9, 6, 1, '#3a2a1e'); R(8, 9, 1, 1, '#fff'); R(11, 9, 1, 1, '#fff');
  });
}
function nianSpr(x, y, n, f) {
  const hop = Math.abs(Math.sin(n / 260)) * 4;
  at(x, y - hop, 2, f, () => {
    R(4, 14, 4, 8, '#b82a22'); R(22, 14, 4, 8, '#b82a22'); R(4, 21, 5, 3, '#3a1e12'); R(22, 21, 5, 3, '#3a1e12');
    R(3, 6, 26, 12, '#d6322a'); R(5, 4, 22, 3, '#d6322a');
    for (let k = 0; k < 5; k++) R(5 + k * 5, 2, 3, 4, '#ffb938');
    R(28, 8, 6, 3, '#d6322a'); R(32, 6, 3, 3, '#ffb938');
    R(-4, 0, 14, 16, '#ffb938'); R(-6, 3, 4, 10, '#ffb938'); R(-2, -3, 10, 4, '#ff8a1a');
    R(-3, 3, 11, 12, '#e8352a');
    R(-2, -6, 2, 5, '#fff2c8'); R(5, -6, 2, 5, '#fff2c8');
    R(-1, 6, 3, 3, '#fff7a8'); R(4, 6, 3, 3, '#fff7a8'); R(0, 7, 1, 1, '#241636'); R(5, 7, 1, 1, '#241636');
    R(-3, 11, 12, 3, '#6a0d0d'); R(-2, 11, 2, 2, '#fff'); R(2, 11, 2, 2, '#fff'); R(6, 11, 2, 2, '#fff');
    R(-5, 9, 2, 2, '#ff8a1a'); R(8, 9, 2, 2, '#ff8a1a');
  });
}
function dragonPts(x0, x1, y, n) {
  const N = 18, pts = [];
  for (let i = 0; i < N; i++) { const t = i / (N - 1); pts.push([x0 + (x1 - x0) * t, y + Math.sin(t * 9 + n / 380) * 14]); }
  return pts;
}
function dragonSpr(pts) {
  const N = pts.length;
  g.lineCap = 'round'; g.lineJoin = 'round';
  [[17, '#14502a'], [13, '#2e9b4e']].forEach(([w, c]) => { g.strokeStyle = c; g.lineWidth = w; g.beginPath(); pts.forEach((p, k) => k ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); g.stroke(); });
  for (let i = N - 1; i >= 0; i--) {
    const [px, py] = pts[i], rr = 6 + 6 * (i / (N - 1));
    g.fillStyle = 'rgba(0,0,0,.18)'; g.beginPath(); g.ellipse(px, py + 12, rr, rr * .45, 0, 0, 7); g.fill();
    dot(px, py + 3, 3.2, '#ffd34a');
    if (i % 2 === 0) R(px - 1.5, py - rr - 4, 3, 5, '#e8352a');
  }
  const [hx, hy] = pts[N - 1];
  at(hx + 2, hy - 14, 2.3, 0, () => {
    R(0, 4, 14, 10, '#2e9b4e'); R(10, 7, 8, 6, '#3fb862'); R(16, 10, 4, 3, '#2e9b4e'); R(12, 12, 6, 2, '#fff'); R(14, 6, 2, 2, '#ffd34a'); R(5, 6, 3, 3, '#fff'); R(6, 7, 2, 2, '#241636');
    R(2, 0, 2, 5, '#ffd34a'); R(6, -2, 2, 6, '#ffd34a'); R(0, 12, 2, 6, '#e8352a'); R(-2, 14, 3, 1, '#e8352a'); R(18, 4, 3, 2, '#e8352a');
  });
  const [tx, ty] = pts[0]; R(tx - 9, ty - 1, 5, 3, '#2e9b4e'); R(tx - 13, ty - 3, 4, 3, '#e8352a');
}
function rabbitSpr(x, y, n, i, pestle, f) {
  const hop = Math.max(0, Math.sin(n / 220 + i * 2)) * 6;
  g.fillStyle = 'rgba(0,0,0,.18)'; g.beginPath(); g.ellipse(x + 14, y + 22, 10, 3, 0, 0, 7); g.fill();
  at(x + (f ? 28 : 0), y - hop, 1.6, f, () => {
    R(4, 8, 12, 10, '#fbf7f2'); R(2, 12, 4, 6, '#fbf7f2'); R(14, 14, 4, 4, '#fbf7f2');
    R(12, 3, 8, 7, '#fbf7f2'); R(13, -7, 3, 11, '#fbf7f2'); R(17, -6, 3, 10, '#fbf7f2'); R(14, -5, 1, 7, '#ffb3c6'); R(18, -4, 1, 6, '#ffb3c6');
    R(17, 5, 2, 2, '#c0201a'); R(20, 7, 1, 1, '#ff8aa0'); R(0, 13, 3, 3, '#fff');
    if (pestle) { R(-3, 4, 3, 16, '#9b6a3c'); R(-5, 2, 7, 3, '#b9824a'); }
  });
}
function reindeerSpr(x, y, n, f, run) {
  const l = Math.floor(n / 180) % 2;
  at(x + (f ? 36 : 0), y, 1.8, f, () => {
    R(4, 14 + (run ? l : 0), 3, 7, '#7a4a28'); R(14, 14 + (run ? 1 - l : 0), 3, 7, '#7a4a28'); R(1, 14, 3, 6, '#6a3e20'); R(17, 14, 3, 6, '#6a3e20');
    R(2, 7, 18, 9, '#9b6a3c'); R(0, 8, 3, 3, '#fff2d8');
    R(18, 3, 4, 8, '#9b6a3c'); R(20, 1, 7, 6, '#9b6a3c'); R(26, 3, 3, 3, '#e8352a'); R(22, 2, 1, 1, '#241636');
    R(20, -3, 1, 5, '#f0e2c4'); R(22, -5, 1, 7, '#f0e2c4'); R(18, -2, 3, 1, '#f0e2c4'); R(24, -3, 3, 1, '#f0e2c4'); R(22, -2, 1, 1, '#f0e2c4');
  });
}
function sleighSpr(x, y, n) {
  const bob = Math.sin(n / 400) * 4;
  g.fillStyle = 'rgba(0,0,0,.2)'; g.beginPath(); g.ellipse(x + 40, y + 62, 40, 7, 0, 0, 7); g.fill();
  at(x, y + bob, 1.8, 0, () => {
    R(2, 12, 26, 9, '#c7261d'); R(0, 8, 6, 6, '#c7261d'); R(2, 12, 26, 2, '#ffd34a'); R(0, 23, 30, 2, '#ffd34a'); R(-2, 20, 3, 4, '#ffd34a');
    R(6, 3, 8, 9, '#d6231a'); R(7, -3, 7, 6, '#f0c9a0'); R(6, -6, 9, 4, '#d6231a'); R(14, -8, 3, 4, '#fff'); R(6, 0, 9, 3, '#fff'); R(8, -1, 2, 1, '#241636'); R(11, -1, 2, 1, '#241636');
    R(18, 6, 8, 7, '#8a5a2b'); R(19, 4, 3, 3, '#8a5a2b'); R(30, 14, 12, 1, '#8a8a99');
  });
  reindeerSpr(x + 76, y + 6 + bob, n, 0, true); reindeerSpr(x + 118, y + 10 + bob, n + 90, 0, true);
}
function santaSpr(x, y, n, f) {
  const st = Math.floor(n / 300) % 2;
  at(x, y, 1.5, f, () => {
    R(5, 20 + st, 4, 6, '#2b2b36'); R(11, 20 + (1 - st), 4, 6, '#2b2b36'); R(4, 25, 5, 2, '#111'); R(11, 25, 5, 2, '#111');
    R(4, 10, 12, 11, '#d6231a'); R(4, 17, 12, 2, '#2b2b36'); R(9, 17, 2, 2, '#ffd34a'); R(4, 20, 12, 2, '#fff');
    R(-2, 11, 7, 9, '#8a5a2b'); R(-3, 9, 4, 3, '#8a5a2b');
    R(5, 1, 10, 9, '#f0c9a0'); R(5, 6, 10, 5, '#fff'); R(4, 4, 2, 6, '#fff'); R(14, 4, 2, 6, '#fff'); R(7, 4, 1, 1, '#241636'); R(12, 4, 1, 1, '#241636'); R(9, 5, 2, 2, '#ff9a9a');
    R(4, -2, 12, 4, '#d6231a'); R(10, -5, 6, 4, '#d6231a'); R(14, -6, 3, 3, '#fff'); R(3, 2, 14, 2, '#fff');
  });
}

/* ── 角色放在哪裡、怎麼動（位置用「格」；地圖每 14 列重複一次） ── */
const BANDS = [0, 14, 28];
const rnd2 = (a, b) => a + Math.random() * (b - a);
const E = [];   // 所有角色
const patrol = (kind, row, x0, x1, o = {}) => E.push({ type: 'patrol', kind, row, x0, x1, x: rnd2(x0, x1), dir: Math.random() < .5 ? 1 : -1, speed: o.speed || .6, pause: 0, phase: Math.random() * 9, tall: o.tall || .3, pestle: o.pestle, idle: o.idle, li: Math.floor(Math.random() * 3), far: true });
const flier = (kind, o = {}) => E.push({ type: 'flier', kind, x: -9, y: 0, vx: o.vx || 2.4, wait: o.wait0 || 2, o, li: Math.floor(Math.random() * 3), far: true });
const ghosts = () => {
  const SP = [[2, 10], [7.5, 12.5], [14, 9.4], [17.5, 12.8], [3.5, 3.7], [11, 7.3]];
  BANDS.forEach((b, bi) => SP.forEach(([x, y], i) => E.push({ type: 'ghost', kind: 'ghost', bx: x, by: y + b, i: i + bi * 6, x, y: y + b, li: i % 2, far: true })));
};
function build() {
if (NAME === 'halloween') {
  ghosts(); flier('witch', { vx: 2.4, wait0: 1.5 });
  BANDS.forEach(b => { patrol('zombie', 4 + b, 12, 18, { speed: .45, tall: .8 }); patrol('zombie', 7 + b, 1, 8, { speed: .45, tall: .8 }); });
} else if (NAME === 'muertos' || NAME === 'ghost') ghosts();
else if (NAME === 'cny') BANDS.forEach(b => { patrol('nian', 5 + b, 1, 7, { speed: .9, tall: 1.2 }); });
else if (NAME === 'dragon') BANDS.forEach(b => E.push({ type: 'dragon', kind: 'dragon', row: 12.9 + b, x0: 30, x1: 540, li: Math.floor(Math.random() * 2), far: true }));
else if (NAME === 'moon') BANDS.forEach(b => {
  patrol('rabbit', 12 + b, 1, 7, { speed: .5, pestle: true, tall: .6 }); patrol('rabbit', 12.3 + b, 12, 15, { speed: .5, tall: .6 });
  patrol('rabbit', 13 + b, 15, 18, { speed: .5, tall: .6 }); patrol('rabbit', 7 + b, 1, 8, { speed: .5, tall: .6 });
});
else if (NAME === 'xmas') {
  BANDS.forEach(b => { patrol('santa', 7 + b, 11, 18, { speed: .5, tall: .8 }); patrol('reindeer', 12.4 + b, 1, 4, { speed: .35, tall: .9 }); });
  flier('sleigh', { vx: 3, wait0: 3 });
}
}
build();

const NEAR = { ghost: 1.7, witch: 3, zombie: 1.7, nian: 2.2, dragon: 2.6, rabbit: 1.6, santa: 1.7, reindeer: 1.8, sleigh: 4 };
function update(dt) {
  if (!NAME) return;
  const pt = typeof playerTile === 'function' ? playerTile() : { x: P.x, y: P.y };
  E.forEach(e => {
    if (e.type === 'patrol') {
      e.phase += dt;
      if (e.pause > 0) { e.pause -= dt; return; }
      if (Math.hypot(pt.x - e.x, pt.y - e.row) < 1.1) { e.pause = .5; return; }   // 玩家擋在前面就等一下
      e.x += e.dir * e.speed * dt;
      if (e.x > e.x1) { e.x = e.x1; e.dir = -1; } else if (e.x < e.x0) { e.x = e.x0; e.dir = 1; }
      if (Math.random() < dt * .1) e.pause = 1 + Math.random() * 2;
    } else if (e.type === 'flier') {
      if (e.wait > 0) { e.wait -= dt; if (e.wait <= 0) { e.x = -9; e.y = Math.max(0.5, camY / T + 1.5 + Math.random() * 6); e.live = true; } return; }
      if (!e.live) return;
      e.x += e.vx * dt;
      if (e.x > COLS + 9) { e.live = false; e.wait = 8 + Math.random() * 8; }
    }
  });
}
const onScreen = (y, pad = 80) => y * T > camY - pad && y * T < camY + VH + pad;
function drawBelow(now) {
  if (!NAME) return;
  g.save();
  if (DECO[NAME]) DECO[NAME](now);
  E.forEach(e => {
    if (e.type === 'patrol') {
      if (!onScreen(e.row)) return;
      const f = e.dir < 0, px = e.x * T, py = e.row * T;
      if (e.kind === 'zombie') zombieSpr(px + (f ? 24 : 0), py - 10, now + e.phase * 350, f);
      else if (e.kind === 'nian') nianSpr(px + (f ? 40 : 0), py - 8, now + e.phase * 100, f);
      else if (e.kind === 'rabbit') rabbitSpr(px, py + 2, now, e.phase, e.pestle, f);
      else if (e.kind === 'santa') santaSpr(px + (f ? 24 : 0), py - 10, now, f);
      else if (e.kind === 'reindeer') reindeerSpr(px, py - 6, now, f, false);
    } else if (e.type === 'dragon') {
      if (!onScreen(e.row, 60)) return;
      e.pts = dragonPts(e.x0, e.x1, e.row * T, now); dragonSpr(e.pts);
    } else if (e.type === 'flier' && e.live && e.kind === 'witch') {
      if (onScreen(e.y, 60)) witchSpr(e.x * T, e.y * T, now, false);
    } else if (e.type === 'flier' && e.live && e.kind === 'sleigh') {
      if (onScreen(e.y, 120)) sleighSpr(e.x * T, e.y * T, now);
    }
  });
  g.restore();
}
const GH = { halloween: ['255,255,255', '#f4f4ff'], muertos: ['255,160,220', '#ffe3f1'], ghost: ['150,240,200', '#dff7ee'] };
function drawTop(now, night) {
  if (!NAME) return;
  g.save();
  if (night && NIGHTFX[NAME]) NIGHTFX[NAME]();
  const gh = GH[NAME];
  if (gh) E.forEach(e => {
    if (e.type !== 'ghost' || !onScreen(e.by, 60)) return;
    e.x = e.bx + Math.sin(now / 900 + e.i) * 6 / T; e.y = e.by + Math.sin(now / 420 + e.i * 1.7) * 5 / T;
    ghostSpr(e.x * T, e.y * T, now, e.i, gh[0], gh[1]);
  });
  g.restore();
}
function speakers(dist) {
  if (!NAME) return [];
  if (!whoDone) { Object.assign(WHO, WHOS); whoDone = true; }
  const out = [];
  E.forEach((e, i) => {
    let x, y, kind = e.kind, lines;
    if (e.type === 'patrol') { x = e.x; y = e.row - e.tall; }
    else if (e.type === 'flier') { if (!e.live) return; x = e.x + (kind === 'sleigh' ? 2.5 : 0); y = e.y - 1; }
    else if (e.type === 'dragon') { const h = e.pts && e.pts[e.pts.length - 1]; if (!h) return; x = h[0] / T; y = h[1] / T - 1; }
    else { x = e.x; y = e.y - .3; }
    lines = TALK[kind === 'ghost' ? 'ghost_' + NAME : kind];
    if (!lines) return;
    const d = dist(x, e.type === 'patrol' ? e.row : y + (e.type === 'flier' || e.type === 'dragon' ? 1 : 0));
    const r = NEAR[kind] || 1.7;
    if (d > r) { e.far = true; return; }
    if (e.far) { e.far = false; e.li = (e.li || 0) + 1; }
    out.push({ key: 'f' + i, who: kind, line: lines[e.li % lines.length], x, y, d, r });
  });
  return out;
}
window.FEST = { name: NAME, tint: TINT[NAME], update, drawBelow, drawTop, speakers,
  setMode(mode) { NAME = detect(mode); E.length = 0; build(); FEST.name = NAME; FEST.tint = TINT[NAME]; }
};
})();
