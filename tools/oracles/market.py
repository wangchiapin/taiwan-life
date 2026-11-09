# 菜市場 market：smoke.py 用的正解（每個狀態的 ok() 就是正確選項；攤位那關先把 Ami 要的菜裝進籃子）
ORACLE = """() => {
  const s = Game.state;
  if (s === 'RESULT') return '查看排行榜';
  const c = Game.getConfig()[s];
  if (!c || !c.ok) return null;
  const v = c.ok(); return v ?? null;
}"""
