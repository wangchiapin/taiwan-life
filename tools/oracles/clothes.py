# 服飾店 clothes：smoke.py 用的正解（照這個玩應該 100 分）
ORACLE = """() => {
  const t = Game.task, s = Game.state;
  const m = {
    START: '走進服飾店', SIZE: () => ['我拿M號的襯衫和三十腰的長褲。', '我拿L號的襯衫和三十腰的長褲。', '我拿M號的襯衫和三十二腰的長褲。'][Math.floor(Math.random() * 3)],   // 挑什麼都不扣分，要靠試穿發現
    ROOM_TAG: () => t.countWrong ? '不好意思，我只有兩件。' : '好，謝謝。',
    FIT_SHIRT: () => Game.shirtFit() !== 0 ? Game.fixShirtText() : '剛好，我要這件。',
    SHIRT_SWAP: () => t.tagWrong ? '不好意思，這是' + SZ[t.wrongSize] + '號，我要' + SZ[t.tgt] + '號。' : '好，謝謝。',
    FIT_WAIST: '不好意思，腰有點鬆，請問有三十腰的嗎？',
    FIT_LENGTH: () => t.hemNeed ? '不好意思，褲子有點長，可以幫我改褲管嗎？' : '剛好，我要這件。',
    HEM: () => t.hemWrong ? '不好意思，有點短，請再放長一點，剛好蓋到鞋面就好。' : '好，這樣可以。',
    PAY: () => t.payWrong ? '不好意思，好像算錯了，應該是' + zhNum(t.total) + '元吧？' : '給你' + zhNum(t.bill) + '元。',
    PAY_FIX: '給你' + zhNum(t.bill) + '元。',
    CHANGE: () => t.changeWrong ? '不好意思，好像找錯了，應該找' + zhNum(t.change) + '元吧？' : '好，謝謝。',
    PICKUP: () => t.pickupWrong ? '不好意思，這條褲子還沒有改，還是很長。' : '好，謝謝。'
  };
  const v = m[s]; return typeof v === 'function' ? v() : (v ?? null);
}"""
