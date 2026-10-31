# 理髮店的正解；tools/smoke.py 讀這裡的 ORACLE
ORACLE = """() => {
  const t = Game.task, s = Game.state, N = Game.N;
  const m = {
    START: '拿起手機', BOOK_SEARCH: t.shops[0].zh, BOOK_OPEN: '打電話預約', BOOK_CALL: '對，我要預約', BOOK_TIME: '我要' + t.want, BOOK_PHONE: t.phoneZh, BOOK_CONFIRM: t.bossWrong ? '不對，我要的是' + t.want + '。' : '好，謝謝，再見！',
    ARRIVE: '有，我有預約，我叫' + N + '。', STYLE_LEN: '剪到' + t.len[0], STYLE_BANG: '瀏海' + t.bang[0],
    WASH: '不好意思，水有點燙。', MIRROR: '後面可以再短一點嗎？', PAY: '給老闆五百元，請他找錢',
    CHANGE: t.wrong ? '老闆' : '沒錯，謝謝',
    CHANGE_FIX: '這次對了，謝謝',
    END: '查看結果', RESULT: '查看排行榜'
  };
  return m[s] ?? null;
}"""
