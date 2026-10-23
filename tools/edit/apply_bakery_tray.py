import os, sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/bakery/index.html')
s=open(P,encoding='utf-8').read()
R=[
# 1 CSS：托盤每列的 －／＋、架子可點、動作提示
("  .tray .empty { color: var(--muted); }\n",
 """  .tray .empty { color: var(--muted); }
  .tray .th small { font-weight: 400; color: var(--muted); margin-left: 8px; font-size: 12px; }
  .tray .row { align-items: center; }
  .tray .row > span:first-child { flex: 1; min-width: 0; }
  .tray .adj { display: inline-flex; align-items: center; gap: 6px; }
  .tray .adj button { width: 34px; height: 34px; border-radius: 50%; border: 2px solid #b99764; background: #fffaf0; color: var(--red-dark); font: inherit; font-size: 20px; font-weight: 700; line-height: 1; cursor: pointer; padding: 0; }
  .tray .adj button:disabled { opacity: .35; cursor: default; }
  .tray .adj i { min-width: 22px; text-align: center; font-style: normal; font-weight: 700; }
  .tray .row > b { min-width: 64px; text-align: right; }
  .tray .act { margin: 2px 0 4px; font-size: 14px; color: var(--ink); }
  .tray .act small { display: block; color: var(--muted); font-size: 12px; line-height: 1.4; }
  .shelf .bun { cursor: pointer; }
  .shelf .bun:active { transform: translateY(1px); }
""",1),
# 2 托盤 HTML：架子可點、每列 －／＋、提示與動作行
("""    const shelf = withShelf ? `<div class="shelf">${SHELF.map(i => `<div class="bun${i.nut ? ' nut' : ''}"><span class="e">""",
 """    const shelf = withShelf ? `<div class="shelf">${SHELF.map(i => `<div class="bun${i.nut ? ' nut' : ''}" data-bun="${i.zh}"><span class="e">""",1),
("""    const rows = Object.keys(c).map(id => `<div class="row"><span>${breadImg(id, 'sm')} ${r(BYID[id].zh)} × ${c[id]}</span><b>${BYID[id].price * c[id]}${r('元')}</b></div>`).join('')""",
 """    const adj = id => withShelf ? `<span class="adj"><button type="button" data-adj="${id}" data-d="-1" aria-label="－">－</button><i>${c[id]}</i><button type="button" data-adj="${id}" data-d="1" aria-label="＋"${BYID[id].toast ? ' disabled' : ''}>＋</button></span>` : ` × ${c[id]}`;
    const rows = Object.keys(c).map(id => `<div class="row"><span>${breadImg(id, 'sm')} ${r(BYID[id].zh)}</span>${adj(id)}<b>${BYID[id].price * c[id]}${r('元')}</b></div>`).join('')""",1),
("""    return shelf + `<div class="tray"><div class="th">${r('托盤')}</div>${rows}""",
 """    const tip = withShelf ? `<small>${r('＋夾進托盤　－放回去')}</small>` : '';
    const act = (withShelf && this.lastAct) ? `<div class="act">${r(this.lastAct.zh)}${ONLYZH() ? '' : `<small>${esc(X(this.lastAct.es, this.lastAct.en))}</small>`}</div>` : '';
    return shelf + `<div class="tray"><div class="th">${r('托盤')}${tip}</div>${act}${rows}""",1),
# 3 選項：拿掉「把〇〇放回去」
("          if (Game.tray.length) o.push(`把${BYID[Game.tray[Game.tray.length - 1]].zh}放回去`);\n","",1),
("""          if (c.startsWith('把')) { const id = Game.tray.pop(); Game.thought = [L(`（你把${BYID[id].zh}放回架上。）`, `(Devuelves el ${short(BYID[id].es)} al estante.)`, `(You put the ${BYID[id].en} back.)`)]; Game.updateCash(); return; }\n""","",1),
# 4 夾進托盤：不再跳過場頁，改成托盤上的動作行
("""          Game.tray.push(it.id); Game.updateCash();
          Game.thought = [L(`（你用夾子把${it.zh}夾進托盤。）`, `(Con las pinzas pones el ${short(it.es)} en la bandeja.)`, `(You pick up the ${it.en} with the tongs and put it on the tray.)`)];""",
 """          Game.tray.push(it.id); Game.updateCash();
          Game.lastAct = L(`你用夾子把${it.zh}夾進托盤。`, `Con las pinzas pones el ${short(it.es)} en la bandeja.`, `You pick up the ${it.en} with the tongs and put it on the tray.`);""",1),
# 5 －：新方法 adjust、測試用 testPrep；重置時清掉動作行
("    this.tray = [];\n    this.checkFails = 0;\n",
 "    this.tray = [];\n    this.lastAct = null;\n    this.checkFails = 0;\n",1),
("  handleChoice(choice) {\n    if (this.state === '_TRANS') {",
 """  /* 托盤每一列的「－」：把這一種麵包少拿一個（不用管順序） */
  removeOne(id) {
    const i = this.tray.lastIndexOf(id);
    if (i < 0) return;
    this.tray.splice(i, 1);
    this.lastAct = L(`你把${BYID[id].zh}放回去。`, `Devuelves el ${short(BYID[id].es)} al estante.`, `You put the ${BYID[id].en} back.`);
    Tr.closeAll(); Speech.stop();
    this.thought = null; this.feedback = []; this.thoughtFirst = false;
    this.updateCash(); this.render();
  },
  testPrep() { if (this.state === 'PICK' && this.tray.length > 8) { this.tray = []; this.updateCash(); } },   // 自動測試用：亂點到堆太多就清空

  handleChoice(choice) {
    if (this.state === '_TRANS') {""",1),
# 6 接上按鈕
("""    box.querySelectorAll('[data-spk]').forEach(btn => {""",
 """    box.querySelectorAll('[data-adj]').forEach(btn => {
      btn.onclick = () => { const id = btn.dataset.adj; if (+btn.dataset.d < 0) this.removeOne(id); else this.handleChoice(BYID[id].zh); };
    });
    box.querySelectorAll('[data-bun]').forEach(el => { el.onclick = () => this.handleChoice(el.dataset.bun); });
    box.querySelectorAll('[data-spk]').forEach(btn => {""",1),
# 7 單字
("['夾', 'tomar con pinzas', 'pick up with tongs']],\n  C_SLICE",
 "['夾', 'tomar con pinzas', 'pick up with tongs'], ['放回去', 'devolver al estante', 'put back']],\n  C_SLICE",1),
]
for old,new,n in R:
    c=s.count(old)
    if c!=n: print('次數不對（預期 %d，實際 %d）：%s'%(n,c,old[:70])); sys.exit(1)
    s=s.replace(old,new)
open(P,'w',encoding='utf-8').write(s)
print('OK',len(R))
