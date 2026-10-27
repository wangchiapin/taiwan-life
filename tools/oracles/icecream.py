# 冰淇淋店 icecream：smoke.py 用的正解
ORACLE = """() => {
  const t = Game.task, s = Game.state;
  const m = {
    START: '走進冰淇淋店', SCOOPS: (t.n === 2 ? '兩' : '三') + '球。', CONTAINER: '要' + t.vessel.zh + '。',
    FLAVOR: () => t.flavors[Game.k].zh + '。',
    TOPPING: t.top ? '加' + t.top.zh + '。' : '不用加配料，謝謝。',
    EAT: (t.eat === 'here' ? '內用' : '外帶') + '。',
    ORDER_CHECK: t.ocWrong ? t.ocFix : '對，沒錯。',
    HANDOVER: t.scoopWrong ? '不好意思，第' + CN[t.wIdx + 1] + '球我要的是' + t.flavors[t.wIdx].zh + '。' : '好，謝謝。',
    PAY: t.payWrong ? '不好意思，好像算錯了，應該是' + zhNum(t.total) + '元吧？' : '給你兩百元。',
    PAY_FIX: '給你兩百元。'
  };
  const v = m[s]; return typeof v === 'function' ? v() : (v ?? null);
}"""
