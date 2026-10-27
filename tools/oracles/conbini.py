# 超商 conbini：smoke.py 用的正解（照這個玩應該 100 分）
ORACLE = """() => {
  const t = Game.task, s = Game.state;
  const m = {
    START: '走進超商', PROMO: '買' + t.cheap.zh + '。', HEAT: t.heat ? '要加熱。' : '不用加熱。', ALCOHOL: '好，這是我的證件。',
    CARRIER: '有，手機載具，條碼是' + t.code + '。',
    CARRIER_CHECK: () => t.ccWrong ? '不好意思，條碼是' + t.code + '。' : '對，沒錯。',
    DRAW: '好，我來抽！',
    PAY: () => t.payWrong ? '不好意思，好像算錯了，應該是' + zhNum(t.total) + '元吧？' : '給你' + zhNum(t.bill) + '元。',
    PAY_FIX: '給你' + zhNum(t.bill) + '元。',
    CHANGE: () => t.changeWrong ? '不好意思，好像找錯了，應該找' + zhNum(t.change) + '元吧？' : '好，謝謝。'
  };
  const v = m[s]; return typeof v === 'function' ? v() : (v ?? null);
}"""
