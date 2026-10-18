# 搭電梯 elevator：smoke.py 用的正解
ORACLE = """() => {
  const t = Game.task, s = Game.state;
  const m = {
    START: '走進大樓', LOBBY: '按▲，往上。', WAIT: '按「開門」，等他。', FLOOR: '按' + t.n + '樓。',
    HELP: '好，我幫你按' + t.m + '樓。', STOP: '不客氣，慢走！', ARRIVE: '不好意思，借過一下。'
  };
  return m[s] ?? null;
}"""
