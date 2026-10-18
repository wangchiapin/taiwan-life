# 書店 bookstore：smoke.py 用的正解
ORACLE = """() => {
  const t = Game.task, s = Game.state;
  const m = {
    START: '走進書店', SECTION: '去' + t.sec.zh + '書區。', FIND: '拿《' + t.book[0] + '》。',
    ASK: '請問書籤在哪裡？', WRAP: '麻煩幫我包裝。', PAY: '給你五百元。'
  };
  return m[s] ?? null;
}"""
