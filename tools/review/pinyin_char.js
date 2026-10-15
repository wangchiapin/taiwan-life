// 列出指定的字在每個遊戲每一處的讀音：node tools/review/pinyin_char.js 還為麼…
const fs = require('fs'), path = require('path');
const P = path.join(__dirname, '..', '.npm', 'v320', 'node_modules', 'pinyin-pro');
const chars = process.argv[2];
const G = ['drinks', 'reserva', 'breakfast', 'parcel', 'nightmarket', 'bakery', 'clinic', 'mrt', 'street'];
const res = {};
for (const g of G) {
  for (const k of Object.keys(require.cache)) if (k.includes('pinyin-pro')) delete require.cache[k];
  const { pinyin, customPinyin } = require(P);
  const d = JSON.parse(fs.readFileSync(path.join(__dirname, 'out', g + '.json'), 'utf8'));
  customPinyin(d.customPinyin || {});
  const sents = [...d.triples.map(t => t.zh), ...d.zhOnly.map(z => z.text), ...d.html.map(h => h.zh)];
  for (const s of sents) for (const seg of s.replace(/〔.*?〕/g, '　').split(/([㐀-鿿]+)/)) {
    if (!/^[㐀-鿿]+$/.test(seg)) continue;
    const p = pinyin(seg, { toneType: 'symbol', toneSandhi: !/^[零一二三四五六七八九]+$/.test(seg), type: 'array' });
    [...seg].forEach((c, i) => {
      if (!chars.includes(c)) return;
      const ctx = seg.slice(Math.max(0, i - 2), i) + '【' + c + '】' + seg.slice(i + 1, i + 3);
      const k = c + ' ' + p[i];
      ((res[k] ||= {})[ctx] ||= new Set()).add(g);
    });
  }
}
for (const k of Object.keys(res).sort()) console.log(k, '：', Object.entries(res[k]).map(([c, gs]) => c).join('  '));
