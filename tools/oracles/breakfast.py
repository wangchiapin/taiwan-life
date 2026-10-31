# 早餐店 breakfast：smoke.py 用的正解（點餐板子由 smoke.py 直接送出正確單子）
ORACLE = """() => {
  const c = Game.C, s = Game.state;
  const m = {
    START: '開始顧店', GREET: '歡迎光臨！', HEAR: '不好意思，鐵板麵今天賣完了。',
    PICKUP: () => c._asked ? '拿出' + c.tail + '的那袋' : '請問電話後三碼是幾號？',
    DINE: () => c.saidDine ? '你的早餐好了喔！' : '請問內用還是外帶？',
    PRICE: () => '一共' + c.total + '元。',
    CHANGE: () => '收您' + c.bill + '元，找您' + (c.bill - c.total) + '元。',
    BYE: () => c.dine === '外帶' ? '謝謝光臨，慢走！' : '請慢用！',
    PHONE: '老樣子，還加一個薯餅。',
    END: '查看結果', RESULT: '查看排行榜'
  };
  const v = m[s]; return typeof v === 'function' ? v() : (v ?? null);
}"""
