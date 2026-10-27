# 電影院 cinema：smoke.py 用的正解（照這個玩應該 100 分）
ORACLE = """() => {
  const t = Game.task, s = Game.state, nw = (n, w) => (n === 2 ? '兩' : CN[n]) + '張' + w;
  const combo = (m, tm) => '晚上' + tm.zh + '的《' + m.zh + '》';
  const m = {
    START: '走進電影院', BOARD: combo(t.movie, t.time), TICKETS: nw(2, '全票') + '，' + nw(t.kids, '學生票') + '。',
    SEATS: '我選好了', SEAT_CONFIRM: () => t.seatWrong ? '不對，我選的是' + seatZh(Game.chosen) + '。' : '沒錯。', PAY: t.payWrong ? '不好意思，好像算錯了，應該是' + zhNum(t.total) + '元吧？' : '給你' + (t.bills === 1 ? '一' : '兩') + '張一千元。',
    TICKET_CHECK: () => t.tkWrong ? (t.tkKind === 'time' ? '不好意思，場次好像印錯了，我要的是' + combo(t.movie, t.time) + '。' : '不好意思，座位好像印錯了，我選的是' + seatZh(Game.chosen) + '。') : '好，謝謝。',
    CHANGE: Game.given === t.change ? '好，謝謝。' : `不好意思，好像找錯了，應該找${zhNum(t.change)}元吧？`,
    SNACK: '一份' + SNACKS[t.snack][0] + '爆米花。', SNACK_CHECK: () => t.snackWrong ? '不好意思，我要的是' + SNACKS[t.snack][0] + '的，不是' + SNACKS[t.snack === 'salty' ? 'sweet' : 'salty'][0] + '的。' : '好，謝謝。',
    GATE: '好，這是電影票，這是學生證。',
    FIND_HALL: '走進' + CN[t.hall] + '廳', SEAT_TAKEN: () => '不好意思，我們的票是' + seatZh(Game.chosen) + '，請你再看一下票。',
    PHONE: '馬上把手機調成靜音。'
  };
  const v = m[s]; return typeof v === 'function' ? v() : (v ?? null);
}"""
