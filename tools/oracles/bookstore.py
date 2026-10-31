# 書店 bookstore：smoke.py 用的正解
ORACLE = """() => {
  const t = Game.task, s = Game.state;
  const m = {
    START: '走進書店', SECTION: '去' + t.sec.zh + '書區。', FIND: t.soldOut ? '找不到，去問店員。' : '拿《' + t.book[0] + '》。', STOCK: '請問《' + t.book[0] + '》還有嗎？',
    ASK: '請問書籤在哪裡？', WRAP: '麻煩幫我包裝。', PAY: t.payWrong ? '不好意思，好像算錯了，應該是' + zhNum(t.total) + '元吧？' : '給你五百元。',
    END: '查看結果', RESULT: '查看排行榜'
  };
  return m[s] ?? null;
}"""
