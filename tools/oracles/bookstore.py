# 書店 bookstore：smoke.py／coverage.py 用的正解（照這個玩應該 100 分）
ORACLE = """() => {
  const t = Game.task, s = Game.state;
  const m = {
    START: '走進書店', SECTION: '去' + t.sec.zh + '區。', FIND: t.soldOut ? '找不到，去問店員。' : '拿《' + t.book[0] + '》。',
    STOCK: '請問《' + t.book[0] + '》還有嗎？', SEEK: '去找書籤。', LOOK: '問店員。', ASK: '請問書籤在哪裡？', MARK: '挑一張漂亮的書籤。',
    WRAP: '要，麻煩幫我包裝一下。',
    PAY: t.payWrong ? '不好意思，好像算錯了，應該是' + zhNum(t.total) + '元吧？' : '給你' + zhNum(t.bill) + '元。',
    PAY_FIX: '給你' + zhNum(t.bill) + '元。',
    CHANGE: t.changeWrong ? '不好意思，好像找錯了，應該找' + zhNum(t.change) + '元吧？' : '好，謝謝。',
    FAREWELL: '謝謝，你包得很漂亮。', END: '查看結果', RESULT: '查看排行榜'
  };
  return m[s] ?? null;
}"""
