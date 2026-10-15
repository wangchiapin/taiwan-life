"""第 2 步：9 個遊戲改用 shared/firebase.js（正確的 Firebase 設定）＋每局上傳完整紀錄到 results。
只跑一次；每個取代都檢查次數，不對就停。"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
GAMES = ['drinks', 'reserva', 'breakfast', 'parcel', 'nightmarket', 'bakery', 'clinic', 'mrt', 'street']

UPLOAD = '''
/* 每局完整紀錄：結果頁出現時上傳到 results（管理員成績頁看得到）；一局只傳一次 */
function uploadResult() {
  if (Game._sent) return; Game._sent = true;
  try {
    TWResults.send({ scene: '%s', name: Game.playerName, code: QS.get('code'), score: Game.score, mistakes: Game.mistakes,
      log: Game.log, elapsed: Game.elapsedTime, hintViews: Game.hintViews, script: Settings.script, lang: Settings.lang, embed: EMBED });
  } catch (e) { console.error('成績紀錄上傳失敗', e); }
}
'''

for g in GAMES:
    p = ROOT / 'games' / g / 'index.html'
    s = p.read_text(encoding='utf-8')
    # 1. Firebase 區塊 → 載入共用檔
    m = re.search(r'<!-- Firebase[^\n]*-->\n<script type="module">.*?</script>\n', s, re.S)
    if not m: sys.exit(f'{g}: 找不到 Firebase 區塊')
    col = re.search(r'const COL = "([a-z_]+)";', m.group(0)).group(1)
    new = (f'<!-- Firebase：設定在 shared/firebase.js（所有遊戲共用）；排行榜 collection：{col}（不要改名） -->\n'
           f'<script src="../../shared/player.js"></script>\n'
           f'<script type="module">\n'
           f'  import {{ initFB }} from "../../shared/firebase.js";\n'
           f'  initFB({{ scoresCol: "{col}" }});\n'
           f'</script>\n')
    s = s[:m.start()] + new + s[m.end():]
    # 2. 上傳函式放在 finishEmbed 後面
    i = s.index('\nfunction finishEmbed() {')
    j = s.index('\n}\n', i) + 3
    s = s[:j] + UPLOAD % g + s[j:]
    # 3. 進結果頁時上傳
    old = "next: () => { Game.state = 'RESULT'; }"
    if s.count(old) != 1: sys.exit(f'{g}: RESULT 次數 {s.count(old)}')
    s = s.replace(old, "next: () => { Game.state = 'RESULT'; uploadResult(); }")
    p.write_text(s, encoding='utf-8')
    print(g, col, 'OK')
