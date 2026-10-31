# 菜市場 market：smoke.py 用的正解
ORACLE = """() => {
  const t = Game.task, s = Game.state, qn = n => n === 2 ? '兩' : CN[n];
  const m = {
    START: '走進菜市場',
    ITEM: () => { const it = t.items[Game.k]; return '我要' + qn(it.q) + it.m + it.zh + '。'; },
    BARGAIN: '可以算便宜一點嗎？', PAY: '給你五百元。', BAG: '不用，我有環保袋。',
    CHANGE: t.shortChange ? '老闆，好像找錯了，應該找' + zhNum(500 - t.final) + '元吧？' : '好，謝謝。',
    CHECK: () => { const it = t.items[t.wi]; return t.bagWrong ? '老闆，' + it.zh + '我要的是' + qn(it.q) + it.m + '，不是' + qn(t.wq) + it.m + '。' : '好，謝謝。'; },
    END: '查看結果', RESULT: '查看排行榜'
  };
  const v = m[s]; return typeof v === 'function' ? v() : (v ?? null);
}"""
