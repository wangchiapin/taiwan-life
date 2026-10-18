# 菜市場 market：smoke.py 用的正解
ORACLE = """() => {
  const t = Game.task, s = Game.state, qn = n => n === 2 ? '兩' : CN[n];
  const m = {
    START: '走進菜市場',
    ITEM: () => { const it = t.items[Game.k]; return '我要' + qn(it.q) + it.m + it.zh + '。'; },
    BARGAIN: '可以算便宜一點嗎？', PAY: '給你五百元。', BAG: '不用，我有環保袋。'
  };
  const v = m[s]; return typeof v === 'function' ? v() : (v ?? null);
}"""
