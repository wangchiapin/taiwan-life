# 搭電梯 elevator：smoke.py 用的正解
# 三種「對方出錯」：DIR（大廳阿姨問往上嗎，其實是往下）、HELP2（鄰居說錯樓層）、STOP（鄰居看錯樓層想下電梯）
ORACLE = """() => {
  const t = Game.task, s = Game.state;
  const m = {
    START: '走進大樓', LOBBY: '按▲，往上。', DIR: '不好意思，這部是往下的。', WAIT: '按「開門」，等他。', FLOOR: '按' + t.n + '樓。',
    HELP: t.lit ? '不用按，' + t.m + '樓已經亮了喔。' : '好，我幫你按' + t.m + '樓。',
    HELP2: '沒關係，我幫你按' + t.e + '樓。',
    STOP: t.stopWrong ? '不好意思，這裡是' + (t.e - 1) + '樓，您是不是要到' + t.e + '樓？' : '不客氣，慢走！',
    STOP_FIX: '不客氣，慢走！',
    EARLY: '不出去，這裡不是' + t.n + '樓。', ARRIVE: '不好意思，借過一下。',
    END: '查看結果', RESULT: '查看排行榜'
  };
  return m[s] ?? null;
}"""
