# 關帝廟 guandi：smoke.py 用的正解（照這個玩應該 100 分）
ORACLE = """() => {
  const t = Game.task, s = Game.state, S = t.slip, N = Game.N;
  const m = {
    START: '走進關帝廟',
    GATE: '走龍邊的門進去（面對廟，在右邊）。',
    FIRE: t.fire === 'shake' ? '用手輕輕晃動，把火晃熄。' : '用另一隻手把火搧熄。',
    HEAVEN: '先在天公爐拜天公，再進去拜關公。',
    MAIN: `關聖帝君，我是${N}，住在附近。最近不太順利，請您保佑我平安順利。`,
    THROW: () => resOpt(t.seq[Game.ti]),
    DRAW: '搖一搖籤筒，讓一支籤自己掉出來。',
    SLIP_NUM: () => t.numWrong ? `不好意思，我抽到的是${slipNo(S.n)}。` : '對，是這張，謝謝。',
    READ: '謝謝關公。我會好好努力。',
    REGISTER: () => t.regWrong ? (t.regKind === 'name' ? `不好意思，我的名字是${N}。` : '不好意思，我要點一年的。') : '對，沒錯。',
    PAY: () => t.payWrong ? `不好意思，好像算錯了，應該是${zhNum(t.total)}元吧？` : `給你${zhNum(t.bill)}元。`,
    PAY_FIX: `給你${zhNum(t.bill)}元。`,
    CHANGE: () => t.changeWrong ? `不好意思，好像找錯了，應該找${zhNum(t.change)}元吧？` : '好，謝謝。',
    AMULET: '自己拿一個平安符，隨喜投一點香油錢。',
    GUOLU: '在香爐上方，順時針繞三圈。',
    EXIT: '走虎邊的門出去（面對廟，在左邊）。'
  };
  const v = m[s]; return typeof v === 'function' ? v() : (v ?? null);
}"""
