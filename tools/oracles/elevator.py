# 搭電梯 elevator：smoke.py 用的正解
ORACLE = """() => {
  const t = Game.task, s = Game.state;
  const m = {
    START: '走進大樓', LOBBY: '按▲，往上。', WAIT: '按「開門」，等他。', FLOOR: '按' + t.n + '樓。',
    HELP: t.lit ? '不用按，' + t.m + '樓已經亮了喔。' : '好，我幫你按' + t.m + '樓。', EARLY: '不出去，這裡不是' + t.n + '樓。', STOP: '不客氣，慢走！', ARRIVE: '不好意思，借過一下。',
    END: '查看結果', RESULT: '查看排行榜'
  };
  return m[s] ?? null;
}"""
