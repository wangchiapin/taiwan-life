# 學校（請假）的正解；tools/smoke.py 讀這裡的 ORACLE（Game 裡的 state 對應正確選項）
ORACLE = """() => {
  const L = Game.task.leave, s = Game.state;
  const m = {
    START: '打開跟老師的聊天室', MSG_OPEN: '老師好，我是' + Game.N + '。我想跟您請假。',
    MSG_REASON: '因為我' + L.reasonOpt + '，所以想請假。', MSG_TIME: '我想請' + L.time + '的假。', MSG_OK: '好的，謝謝老師。',
    BACK: L.backA, NOTES: '小美，不好意思，可以請你把' + L.note + '借我拍照嗎？', FORM: L.type,
    SUBMIT: '老師，這是我的請假單，謝謝老師。'
  };
  return m[s] ?? null;
}"""
