# 訂位 reserva：smoke.py 用的正解（會先問 Ami 再回答，這樣三個「打給 Ami」的關卡也會走到）
ORACLE = """() => {
  const t = Game.task, b = Game.booking, s = Game.state, N = Game.N, A = Game.amiAsked || {};
  const ask = '等一下喔……我確認一下。';
  const m = {
    START: '找餐廳的電話', DIAL: () => zhDigits(Game.bookingLine), C1_GREET: '我想訂位。', C1_DAY: () => t.day,
    C1_DATE_CHECK: () => Game._dateShown === b.date ? '對。' : '不對。',
    C1_TIME: () => '晚上' + timeStr(t.T),
    C1_FULL: () => A.time1 ? '那' + timeStr(t.t1) + '好了。' : ask,
    C1_PEOPLE: () => zhNum(t.people) + '位',
    C1_ROOM: () => A.room ? '不用，一般座位就好。' : ask,
    C1_OTHER: () => !Game.otherAsked.chairs ? '我們需要兒童椅。' : !Game.otherAsked.veg ? '有素食的餐點嗎？' : '沒有了。',
    C1_CHAIRS: () => ['一張', '兩張', '三張'][t.kids - 1],
    C1_NAME: () => '我叫' + N + '。', C1_PHONE: () => zhDigits(Game.myPhone),
    CONFIRM: () => Game.repeat.wrongField ? '不對。' : '對，沒錯。',
    FIX: () => ({ date: '日期', time: '時間', people: '人數', phone: '電話' })[Game.repeat.wrongField],
    C1_HOLD: '好，謝謝，到時候見！', MID_AMI: '好，我再打給餐廳。',
    C2_GREET: '你好，我剛剛有打電話訂位，我想要更正一下。',
    C2_LOOKUP: () => N + '，' + zhDigits(Game.myPhone),
    C2_PEOPLE: () => zhNum(t.finalPeople) + '位', C2_TABLE: () => b.seat === '包廂' ? '改成併桌好了。' : '麻煩幫我們併桌。',
    C2_TIME: () => '可以改成' + timeStr(t.ask2) + '嗎？',
    C2_FULL: () => !A.time2 ? ask : (t.amiPrefersKeep ? '維持' + timeStr(t.t1) + '。' : '改到' + timeStr(t.alt2) + '。'),
    C2_CHAIRS: () => b.chairs ? '對，一樣。' : '對，都一樣。', C2_BYE: '謝謝，再見！',
    CALL_AMI: '好，我跟餐廳說。',
    WRONG_NUMBER: '不好意思，打錯了。', DELIVERY_LINE: '好，謝謝。',
    C2_ADD_CHAIRS: () => ['一張', '兩張', '三張'][t.kids - 1],
    END: '查看結果', RESULT: '查看排行榜'
  };
  const v = m[s]; return typeof v === 'function' ? v() : (v ?? null);
}"""
