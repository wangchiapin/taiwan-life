# 麵店 noodle：smoke.py 用的正解（照這個玩應該 100 分）
ORACLE = """() => {
  const t = Game.task, s = Game.state, T = t.truth;
  const sideOk = () => Game.k < t.sides.length ? '加' + t.sides[Game.k].m + t.sides[Game.k].zh + '。' : (Game.k === 0 ? '不用小菜，謝謝。' : '不用了，謝謝。');
  const m = {
    START: '走進麵店', NOODLE: '我要' + t.noodle.zh + '。', SIZE: SIZES[t.size].zh + '。', SPICY: t.spicy.opt, SCAL: t.scal ? '要蔥。' : '不要蔥。',
    SIDE: sideOk, EAT: EATS[t.eat].zh + '。',
    ORDER_CHECK: () => t.ocWrong ? OC.fix(t.ocKind, T[t.ocKind]) : '對，沒錯。',
    HANDOVER: () => t.hoWrong ? OC.fix(t.hoKind, T[t.hoKind]) : '好，謝謝。',
    PAY: () => t.payWrong ? '不好意思，好像算錯了，應該是' + zhNum(t.total) + '元吧？' : '給你' + zhNum(t.bill) + '元。',
    PAY_FIX: '給你' + zhNum(t.bill) + '元。',
    CHANGE: () => t.changeWrong ? '不好意思，好像找錯了，應該找' + zhNum(t.change) + '元吧？' : '好，謝謝。'
  };
  const v = m[s]; return typeof v === 'function' ? v() : (v ?? null);
}"""
