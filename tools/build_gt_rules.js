#!/usr/bin/env node
// 把 GoodTeacher 的「需要改讀音」規則，轉成一小段資料，寫進 shared/game.js 中
// 標記「GT-RULES-BEGIN」到「GT-RULES-END」之間的區塊。
//
// 什麼時候跑：GoodTeacher 更新了讀音規則（game-kit/bank/gt/ 換了新版）之後，跑一次，
//            24 個遊戲就一起更新。跑完要重新測試（tools/smoke.py）並比對畫面。
// 用法：node tools/build_gt_rules.js [game-kit 的資料夾，預設 ../../game-kit]
// 只收：有「改」規則的繁體字（簡體字不用，遊戲拼音都用繁體算）。
// 規則的比對方式與 game-kit/bank/gt_compare.js 相同。
'use strict';
const fs = require('fs'), path = require('path');
const kit = path.resolve(process.argv[2] || path.join(__dirname, '..', '..', 'game-kit'));
const G = path.join(kit, 'bank', 'gt') + path.sep;
const read = f => fs.readFileSync(G + f, 'utf8').replace(/^﻿/, '');
const OpenCC = require(path.join(__dirname, '.npm', 'node_modules', 'opencc-js'));
const t2s = OpenCC.Converter({ from: 'tw', to: 'cn' }), s2t = OpenCC.Converter({ from: 'cn', to: 'tw' });
/* 純簡體字：轉成繁體會變、自己當繁體轉簡體不變 → 不收 */
const pureSimp = c => s2t(c) !== c && t2s(c) === c;

const lab = {}, chr = {}; let sec = '';
for (const ln of read('readings.txt').split(/\r?\n/)) {
  if (ln === '[L]') { sec = 'L'; continue; } if (ln === '[C]') { sec = 'C'; continue; }
  const i = ln.indexOf('='); if (i < 0) continue;
  if (sec === 'L') lab[ln.slice(0, i)] = ln.slice(i + 1).split(' ')[0];
  else if (sec === 'C') chr[ln.slice(0, i)] = ln.slice(i + 1).split(',');
}
const cls = {};
for (const ln of read('classes.txt').split(/\r?\n/)) { const i = ln.indexOf('='); if (i > 0) cls['GT_' + ln.slice(0, i)] = ln.slice(i + 1); }

const rows = read('rules.csv').split(/\r?\n/).slice(1).filter(Boolean).map(l => l.split(','));
const hasGai = new Set(rows.filter(r => r[1] === '改').map(r => r[2]));
const keep = c => hasGai.has(c) && !pureSimp(c);

const rules = {}, usedCls = new Set(), usedCodes = new Set();
for (const [g, act, ch, slot, pre, post, hint] of rows) {
  if (!keep(ch)) continue;
  for (const f of [pre, post]) for (const m of (f || '').matchAll(/@(\w+)/g)) usedCls.add(m[1]);
  (rules[ch] = rules[ch] || []).push([act === '改' ? 1 : 0, slot === '' ? -1 : +slot, pre || '', post || '', hint || '']);
}
const chars = {};
for (const c of Object.keys(rules)) {
  if (!chr[c]) continue;
  chars[c] = chr[c].map(code => { usedCodes.add(code); return lab[code] || code; });
}
/* 「下一個字是第幾聲」的三個大類別（一、不 用）：
   T4YI＝本調四聲的字；T123YI＝其餘有聲調的字；輕聲字兩邊都不是（約 200 個：了、子、吧…）。
   為了縮小體積：只存 T4YI（限 4E00–9FFF）、輕聲字，T123YI 與 T4BU 在遊戲裡由這兩者推出來。
   產生時先驗證：T123YI ＝ 漢字 − T4YI − 輕聲字；T4BU 與 T4YI 只差少數字。 */
const inHan = c => c >= '\u4e00' && c <= '\u9fff';
const han = []; for (let c = 0x4e00; c <= 0x9fff; c++) han.push(String.fromCharCode(c));
const T4 = new Set(Array.from(cls.GT_T4YI).filter(inHan)), T123 = new Set(Array.from(cls.GT_T123YI).filter(inHan));
const neutral = han.filter(c => !T4.has(c) && !T123.has(c));
if (han.some(c => T4.has(c) && T123.has(c))) throw new Error('T4YI 與 T123YI 有重疊，推導方式不成立');
const T4BU = new Set(Array.from(cls.GT_T4BU).filter(inHan));
const bu_minus = [...T4].filter(c => !T4BU.has(c)).join(''), bu_plus = [...T4BU].filter(c => !T4.has(c)).join('');
const classes = {};
for (const u of usedCls) {
  if (u === 'GT_HANZI' || u === 'GT_T123YI' || u === 'GT_T4BU') continue;
  classes[u] = u === 'GT_T4YI' ? [...T4].join('') : Array.from(cls[u] || '').filter(c => !pureSimp(c)).join('');
}
classes.NEUTRAL = neutral.join(''); classes.T4BU_MINUS = bu_minus; classes.T4BU_PLUS = bu_plus;

const data = { chars, rules, classes };
const json = JSON.stringify(data);
const block = '/* GT-RULES-BEGIN（由 tools/build_gt_rules.js 產生，請不要手改；GoodTeacher 更新後重跑） */\n' +
  'const GT_DATA = ' + json + ';\n/* GT-RULES-END */';
const target = path.join(__dirname, '..', 'shared', 'game.js');
let src = fs.readFileSync(target, 'utf8');
const re = /\/\* GT-RULES-BEGIN[\s\S]*?GT-RULES-END \*\//;
if (!re.test(src)) { console.error('game.js 裡找不到 GT-RULES 區塊，請先放好標記'); process.exit(1); }
src = src.replace(re, () => block);
fs.writeFileSync(target, src);
console.log('已寫入 shared/game.js：字', Object.keys(chars).length, '規則', Object.values(rules).reduce((a, b) => a + b.length, 0), '大小', json.length, '位元組');
