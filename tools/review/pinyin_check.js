// 拼音檢查：用和遊戲一樣的方法（pinyin-pro＋各遊戲的 customPinyin＋變調）算出每句的拼音，
// 列出（1）兩岸讀音不同的字、（2）多音字，在句子裡被念成什麼。輸出 tools/review/out/pinyin_<game>.json
const fs = require('fs'), path = require('path');
const NM = path.join(__dirname, '..', '.npm', 'node_modules');
const { pinyin, customPinyin, polyphonic } = require(path.join(NM, '..', 'v320', 'node_modules', 'pinyin-pro'))  // 和遊戲一樣用 3.20.0;
const game = process.argv[2];
const d = JSON.parse(fs.readFileSync(path.join(__dirname, 'out', game + '.json'), 'utf8'));
customPinyin(d.customPinyin || {});
const PY_OPT = { toneType: 'symbol', toneSandhi: true };
const isDigits = seg => /^[零一二三四五六七八九]+$/.test(seg);
const toPinyin = seg => pinyin(seg, { ...PY_OPT, toneSandhi: !isDigits(seg), type: 'array' });

// 台灣（教育部）和大陸讀音不同、常見的字：[字, 台灣讀音（可以有好幾個，都算對）]
const TW = {
  '期': ['qí'], '微': ['wéi'], '危': ['wéi'], '企': ['qì'], '質': ['zhí'], '液': ['yì'], '綜': ['zòng'], '識': ['shì'],
  '寂': ['jí'], '暫': ['zhàn'], '擁': ['yǒng'], '跌': ['dié'], '突': ['tú'], '檔': ['dǎng'], '擊': ['jí'], '息': ['xí'],
  '惜': ['xí'], '熄': ['xí'], '昔': ['xí'], '夕': ['xì'], '跡': ['jī'], '蹟': ['jī'], '誼': ['yí'], '偽': ['wèi'], '叔': ['shú'],
  '淑': ['shú'], '穴': ['xuè'], '菌': ['jùn'], '癌': ['yán'], '骰': ['tóu'], '蝸': ['guā'], '曝': ['pù'], '秘': ['mì'],
  '姆': ['mǔ'], '帆': ['fán'], '艘': ['sāo'], '侶': ['lǚ'], '塑': ['sù'], '溯': ['sù'], '召': ['zhào'], '爪': ['zhuǎ', 'zhǎo'],
  '亞': ['yà'], '涉': ['shè'], '拂': ['fú'], '戚': ['qī'], '垃': ['lè'], '圾': ['sè'], '髮': ['fǎ'], '輯': ['jí'], '緝': ['qì', 'jí'],
  '括': ['kuò'], '琅': ['láng'], '暴': ['bào', 'pù'], '靜': ['jìng'], '幟': ['zhì'], '撈': ['lāo'], '眶': ['kuàng'], '框': ['kuàng'],
  '潛': ['qián'], '頸': ['jǐng'], '鳩': ['jiū'], '酵': ['xiào'], '蛤': ['gé'], '迫': ['pò'], '擠': ['jǐ'], '濟': ['jì', 'jǐ'],
  '寧': ['níng', 'nìng'], '嗯': ['ēn', 'en', 'ǹg', 'ńg'], '喔': ['ō', 'o'], '啦': ['la'], '囉': ['luo', 'luō'], '欸': ['éi', 'ēi', 'ê̄', 'ěi', 'èi', 'ai'],
  '誰': ['shéi'], '剎': ['chà', 'shā'], '卡': ['kǎ', 'qiǎ'], '傘': ['sǎn'], '號': ['hào', 'háo'], '冷': ['lěng']
};
// 常見、套件通常念得對的字，不用逐一列出（只看其他多音字）
const SKIP = new Set([...'的了是不一我你他她們在有這那就都也很要會說好嗎吧呢啊哦喔呀嘛啦'.split('')]);
const sentences = [];
for (const t of d.triples) if (t.kind !== 'vocab') sentences.push({ zh: t.zh, line: t.line });
for (const t of d.vocab) sentences.push({ zh: t.zh, line: t.line, vocab: true });
for (const z of d.zhOnly) sentences.push({ zh: z.text, line: z.line });
for (const h of d.html) if (h.zh) sentences.push({ zh: h.zh, line: 0 });
const twIssues = [], poly = {};
for (const s of sentences) {
  const text = s.zh.replace(/〔.*?〕/g, '　');
  for (const seg of text.split(/([㐀-鿿]+)/)) {
    if (!/^[㐀-鿿]+$/.test(seg)) continue;
    const py = toPinyin(seg);
    [...seg].forEach((c, i) => {
      const ctx = seg.slice(Math.max(0, i - 3), i + 4), p = py[i];
      if (TW[c] && !TW[c].includes(p)) twIssues.push({ char: c, got: p, want: TW[c].join('/'), ctx, line: s.line, sentence: s.zh });
      if (SKIP.has(c)) return;
      const all = (polyphonic(c, { type: 'array' })[0] || []);
      if (all.length > 1) {
        const k = c + '|' + p;
        (poly[k] ||= { char: c, py: p, all, ctx: new Set(), lines: new Set() });
        if (poly[k].ctx.size < 6) poly[k].ctx.add(ctx);
        poly[k].lines.add(s.line);
      }
    });
  }
}
const polyList = Object.values(poly).map(x => ({ ...x, ctx: [...x.ctx], lines: [...x.lines].slice(0, 5) }));
fs.writeFileSync(path.join(__dirname, 'out', `pinyin_${game}.json`), JSON.stringify({ twIssues, poly: polyList }, null, 1));
console.log(game, '兩岸讀音不同、念錯的：', twIssues.length, '｜多音字（字＋讀音）組合：', polyList.length);
