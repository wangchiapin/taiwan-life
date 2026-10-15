// 第 4 步：把一個遊戲裡所有「中文＋西文＋英文」抽出來（給全面檢查用）
// 用法：node tools/review/extract.js <game>  → 輸出 JSON 到 stdout
// triples：L()/M()/good()… 這類三個字串的呼叫，以及 [中, 西, 英] 陣列（單字表、關卡名稱）
// zhOnly：只有中文的字串（選項、標籤…）；html：畫面上寫死的文字（開始畫面的說明等）
const fs = require('fs'), path = require('path');
const NM = path.join(__dirname, '..', '.npm', 'node_modules');
const acorn = require(path.join(NM, 'acorn')), walk = require(path.join(NM, 'acorn-walk'));
const game = process.argv[2];
const html = fs.readFileSync(path.join(__dirname, '..', '..', 'games', game, 'index.html'), 'utf8');
const CJK = /[㐀-鿿]/;

// 遊戲自己的程式：shared/game.js 後面那一段
const i = html.indexOf('<script src="../../shared/game.js"></script>');
const a = html.indexOf('<script>', i) + 8, b = html.indexOf('</script>', a);
const js = html.slice(a, b);
const lineBase = html.slice(0, a).split('\n').length - 1;
const ast = acorn.parse(js, { ecmaVersion: 'latest', locations: true });
const src = n => js.slice(n.start, n.end);
function str(n) {
  if (!n) return null;
  if (n.type === 'Literal' && typeof n.value === 'string') return n.value;
  if (n.type === 'TemplateLiteral') {
    let s = '';
    n.quasis.forEach((q, k) => { s += q.value.cooked; if (n.expressions[k]) s += '〔' + src(n.expressions[k]) + '〕'; });
    return s;
  }
  if (n.type === 'BinaryExpression' && n.operator === '+') { const l = str(n.left), r = str(n.right); return l != null && r != null ? l + r : null; }
  return null;
}
const triples = [], used = new Set(), zhOnly = [], vocab = [];
const line = n => n.loc.start.line + lineBase;
function addTriple(nodes, kind, fn, at) {
  const [zh, es, en] = nodes.map(str);
  if (zh == null || es == null || en == null || !CJK.test(zh) || CJK.test(es.replace(/〔.*?〕/g, ''))) return false;
  nodes.forEach(n => used.add(n.start));
  triples.push({ zh, es, en, kind, fn, line: line(at) });
  return true;
}
walk.fullAncestor(ast, (node, st, anc) => {
  if (node.type === 'CallExpression' && node.arguments.length >= 3) {
    const fn = node.callee.type === 'Identifier' ? node.callee.name : node.callee.type === 'MemberExpression' ? src(node.callee) : '?';
    addTriple(node.arguments.slice(0, 3), 'call', fn, node);
  }
  if (node.type === 'ArrayExpression' && node.elements.length >= 3) {
    const parentProp = [...anc].reverse().find(x => x.type === 'Property');
    const key = parentProp ? (parentProp.key.name || parentProp.key.value) : '';
    const inVocab = anc.some(x => x.type === 'VariableDeclarator' && x.id.name === 'VOCAB');
    if (addTriple(node.elements.slice(0, 3), inVocab ? 'vocab' : 'array', key, node) && inVocab) {
      const t = triples[triples.length - 1]; vocab.push({ key, zh: t.zh, es: t.es, en: t.en, line: t.line });
    }
  }
});
walk.full(ast, node => {
  const s = (node.type === 'Literal' || node.type === 'TemplateLiteral') ? str(node) : null;
  if (s && CJK.test(s) && !used.has(node.start)) zhOnly.push({ text: s, line: line(node) });
});
// 畫面上寫死的文字：data-zh/data-es/data-en 和一般中文文字
const htmlTexts = [];
const body = html.slice(html.indexOf('<body'), html.indexOf('<script>\n/* 這個遊戲的設定'));
for (const m of body.matchAll(/<([a-z0-9]+)([^>]*)>([^<]*)/g)) {
  const attrs = m[2], text = m[3].trim();
  const es = (attrs.match(/data-es="([^"]*)"/) || [])[1], en = (attrs.match(/data-en="([^"]*)"/) || [])[1], zh = (attrs.match(/data-zh="([^"]*)"/) || [])[1];
  if (es || en) htmlTexts.push({ zh: zh || (CJK.test(text) ? text : ''), es: es || '', en: en || '' });
  else if (CJK.test(text)) htmlTexts.push({ zh: text, es: '', en: '' });
}
// 讀音修正：遊戲可能呼叫好幾次（會合併），全部讀進來
const cpAll = {};
for (const m of js.matchAll(/pinyinPro\.customPinyin\((\{[\s\S]*?\})\);/g)) Object.assign(cpAll, Function('return ' + m[1])());
const cp = null;
console.log(JSON.stringify({ game, triples, zhOnly, vocab, html: htmlTexts, customPinyin: cpAll }, null, 1));
