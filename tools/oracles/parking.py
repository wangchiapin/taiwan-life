# 停車場 parking：smoke.py 用的正解（照這個玩應該 100 分）
ORACLE = """() => {
  const t = Game.task, s = Game.state;
  const m = {
    START: '開進停車場', ENTRANCE: '按按鈕，拿停車票。', FLOOR: '開到' + FL(t.floor),
    SPOT: '停在' + t.zone + '區' + zhNum(t.n) + '號。', REMEMBER: '我停在' + Game.locZh() + '。',
    PAY: '掃描發票。', PAY_CHECK: t.machWrong ? '機器好像沒有折抵發票，我按對講機問一下。' : '好，付' + t.fee + '元。', FIND_CAR: '在' + Game.locZh() + '。', EXIT: '把停車票放進機器裡。',
    END: '查看結果', RESULT: '查看排行榜'
  };
  return m[s] ?? null;
}"""
