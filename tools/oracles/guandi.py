# 關帝廟 guandi：smoke.py 用的正解（照這個玩應該 100 分）
ORACLE = """() => {
  const t = Game.task, s = Game.state, S = t.slip, N = Game.N;
  const m = {
    START: '走進關帝廟',
    GATE: '從右邊的門（龍邊）進去。',
    TO_FIRE: '去點香處拿香點香',
    FIRE: t.fire === 'shake' ? '用手輕輕晃動，把火晃熄。' : '用另一隻手把火搧熄。',
    HEAVEN: '天公爐拜天公',
    MAIN: MAIN_RIGHT,
    SIDE: '去求籤',
    THROW: () => '走到籤筒前',
    CONFIRM: () => Game.goNext === 'SLIP_NUM' ? '走到籤櫃' : '回去重新求籤',
    DRAW: '輕搖籤筒，等一支籤掉出來。',
    SLIP_NUM: () => t.numWrong ? `不好意思，我抽到的是${slipNo(S.n)}。` : '對，是這張，謝謝。',
    READ: '謝謝關公。我會好好努力。',
    ASK: '廟公，可以請你幫我解籤嗎？', MEAN: () => S.say, FILL: '填好了',
    REGISTER: () => {
      if (!t.regWrong) return '對，沒錯。';
      const f = Game.filled();
      return { name: `不好意思，我的名字是${N}。`, birth: `不好意思，我的生日是${birthZh(f.m, f.d)}。`, addr: `不好意思，我住在${ADDR[f.addr][0]}。` }[t.regKind];
    },
    PAY: () => t.payWrong ? `不好意思，我點的是光明燈，應該是${zhNum(t.total)}元吧？` : `好，這裡是${zhNum(t.bill)}元。`,
    PAY_FIX: `好，這裡是${zhNum(t.bill)}元。`,
    CHANGE: () => t.changeWrong ? `不好意思，好像找錯了，應該找${zhNum(t.change)}元吧？` : '好，謝謝。',
    AMULET: '（拿一個平安符，隨喜投一點香油錢）',
    CHARM: '過香爐',
    GUOLU: '在香爐上方，順時針繞三圈。',
    GO_AMULET: '去領平安符',
    EXIT: '從右邊的門（虎邊）出去。',
    END: '查看結果', RESULT: '查看排行榜'
  };
  const v = m[s]; return typeof v === 'function' ? v() : (v ?? null);
}"""
