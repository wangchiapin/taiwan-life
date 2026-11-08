# 菜市場 market：smoke.py 用的正解
ORACLE = """() => {
  const t = Game.task, s = Game.state;
  if (s === 'PICK') {   // 點圖片買菜：直接用同樣的入口把籃子裝成 Ami 要的，再按「買好了」
    Game.cart = {};
    t.items.forEach(it => { if (it.meat) Game.handleChoice(buyStr(BYID[it.id], it.q)); else for (let k = 0; k < it.q; k++) Game.handleChoice(buyStr(BYID[it.id], 1)); });
    return PICK_DONE;
  }
  const m = {
    START: '走進菜市場',
    BARGAIN: '可以算便宜一點嗎？', PAY: '給你一千元。', BAG: '不用，我有環保袋。',
    CHANGE: t.shortChange ? '老闆，好像找錯了，應該找' + zhNum(1000 - t.final) + '元吧？' : '好，謝謝。',
    CHECK: () => { const it = t.items[t.wi]; return t.bagWrong ? '老闆，' + it.zh + '我要的是' + qZh(it, it.q) + '，不是' + qZh(it, t.wq) + '。' : '好，謝謝。'; },
    END: '查看結果', RESULT: '查看排行榜'
  };
  const v = m[s]; return typeof v === 'function' ? v() : (v ?? null);
}"""
