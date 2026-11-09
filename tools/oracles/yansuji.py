# 鹽酥雞 yansuji：smoke.py 用的正解（照這個玩應該 100 分）
ORACLE = """() => {
  const t = Game.task, s = Game.state, T = t.truth;
  if (s === 'ITEM') {   // 照 Ami 說的，一份一份夾進籃子，再按「點好了」
    t.items.forEach(a => { while ((Game.basket[a.it.zh] || 0) < a.q) Game.handleChoice('夾:' + a.it.zh); });
    return '點好了。';
  }
  const m = {
    START: '走到攤位前', CUT: t.cut ? '要切。' : '不用切。', SPICY: t.spicy.opt, TOPS: topsOpt(t.tops),
    ORDER_CHECK: () => t.ocWrong ? OC.fix(t.ocKind, T[t.ocKind], t.ocIdx) : '對，沒錯。',
    HANDOVER: () => t.hoWrong ? OC.fix(t.hoKind, T[t.hoKind], t.hoIdx) : '好，謝謝。',
    PAY: () => t.payWrong ? '不好意思，好像算錯了，應該是' + zhNum(t.total) + '元吧？' : '給你' + zhNum(t.bill) + '元。',
    PAY_FIX: () => '給你' + zhNum(t.bill) + '元。',
    CHANGE: () => t.changeWrong ? '不好意思，好像找錯了，應該找' + zhNum(t.change) + '元吧？' : '好，謝謝。',
    END: '查看結果', RESULT: '查看排行榜'
  };
  const v = m[s]; return typeof v === 'function' ? v() : (v ?? null);
}"""
