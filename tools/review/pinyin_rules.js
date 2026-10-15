// 拼音：找出念錯的詞（和遊戲同樣的算法），列出每個遊戲、哪一句、算出來的讀音、台灣（教育部）讀音
// 用法：node tools/review/pinyin_rules.js   → tools/review/out/pinyin_wrong.json
const fs = require('fs'), path = require('path');
const NM = path.join(__dirname, '..', '.npm', 'node_modules');
const G = ['drinks', 'reserva', 'breakfast', 'parcel', 'nightmarket', 'bakery', 'clinic', 'mrt', 'street'];
// 詞 → 台灣讀音（教育部《重編國語辭典修訂本》）；同一個詞在句子裡的讀音
const WANT = {
  '怎麼': 'zěn me', '為什麼': 'wèi shén me', '因為': 'yīn wèi', '長輩': 'zhǎng bèi', '累積': 'lěi jī', '嚇了一跳': 'xià le yí tiào',
  '仔細': 'zǐ xì', '禮貌地': 'lǐ mào de', '慢慢地': 'màn màn de', '客氣地': 'kè qì de', '聽得懂': 'tīng de dǒng', '走得': 'zǒu de', '處理得': 'chǔ lǐ de',
  '認識': 'rèn shì', '日期': 'rì qí', '星期': 'xīng qí', '休息': 'xiū xí', '訊息': 'xùn xí', '突然': 'tú rán', '突發': 'tú fā', '跌倒': 'dié dǎo',
  '危險': 'wéi xiǎn', '微糖': 'wéi táng', '微冰': 'wéi bīng', '淑芬': 'shú fēn', '淑芳': 'shú fāng', '淑貞': 'shú zhēn',
  '下車': 'xià chē', '轉車': 'zhuǎn chē', '搭車': 'dā chē', '上車': 'shàng chē', '車站': 'chē zhàn', '機車': 'jī chē', '車廂': 'chē xiāng', '公車': 'gōng chē', '救護車': 'jiù hù chē', '車門': 'chē mén',
  '切': 'qiē', '切成': 'qiē chéng', '切片': 'qiē piàn', '還記得': 'hái jì de', '還會': 'hái huì', '還在': 'hái zài', '還收到': 'hái shōu dào'
};
const out = [];
for (const g of G) {
  // 每個遊戲各自載入一次 pinyin-pro（customPinyin 是全域的，不能混在一起）
  for (const k of Object.keys(require.cache)) if (k.includes('pinyin-pro')) delete require.cache[k];
  const { pinyin, customPinyin } = require(path.join(NM, '..', 'v320', 'node_modules', 'pinyin-pro'))  // 和遊戲一樣用 3.20.0;
  const d = JSON.parse(fs.readFileSync(path.join(__dirname, 'out', g + '.json'), 'utf8'));
  customPinyin(d.customPinyin || {});
  const isDigits = seg => /^[零一二三四五六七八九]+$/.test(seg);
  const py = seg => pinyin(seg, { toneType: 'symbol', toneSandhi: !isDigits(seg), type: 'array' });
  const sents = [...d.triples.map(t => ({ zh: t.zh, line: t.line })), ...d.zhOnly.map(z => ({ zh: z.text, line: z.line })), ...d.html.filter(h => h.zh).map(h => ({ zh: h.zh, line: 0 }))];
  const seen = new Set();
  for (const s of sents) for (const seg of s.zh.replace(/〔.*?〕/g, '　').split(/([㐀-鿿]+)/)) {
    if (!/^[㐀-鿿]+$/.test(seg)) continue;
    const p = py(seg);
    for (const [w, want] of Object.entries(WANT)) {
      let i = seg.indexOf(w);
      while (i >= 0) {
        const got = p.slice(i, i + w.length).join(' ');
        if (got !== want && !(w === '切' && /切[成片]/.test(seg.slice(i, i + 2)))) {
          const k = g + w + got + seg;
          if (!seen.has(k)) { seen.add(k); out.push({ game: g, word: w, got, want, seg, line: s.line }); }
        }
        i = seg.indexOf(w, i + 1);
      }
    }
  }
}
fs.writeFileSync(path.join(__dirname, 'out', 'pinyin_wrong.json'), JSON.stringify(out, null, 1));
for (const o of out) console.log(o.game.padEnd(12), o.word.padEnd(5), o.got.padEnd(14), '→', o.want.padEnd(14), o.seg);
