"""分享成績按鈕測試（Playwright）。用法：python3 tools/share_test.py [遊戲 ...]（不給就測全部遊戲）
測：按鈕位置／樣式／0 分不顯示、一句話（暱稱有無 × 西／英／中 × 繁／簡）、連結、
系統分享（成功／玩家關掉／出錯／不支援）、複製備案（成功／失敗）、地圖（embed）模式、重複進排行榜、地圖 iframe 權限。"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smoke                                  # 借用它的本機伺服器、假 Firebase、擋外部網路
from playwright.sync_api import sync_playwright

PORT = smoke.PORT
ALL = sorted(d for d in os.listdir(os.path.join(smoke.ROOT, 'games')) if os.path.isfile(os.path.join(smoke.ROOT, 'games', d, 'index.html')))
GAMES = sys.argv[1:] or ALL
URL = 'https://wangchiapin.github.io/taiwan-life/?ref=share'
fails = []; n = [0]
def ok(c, msg, extra=''):
    n[0] += 1
    if not c: fails.append(msg); print('  ✗', msg, extra)

STUB = """(m) => {
  window.__shared = []; window.__copied = [];
  const def = (k, v) => Object.defineProperty(navigator, k, { value: v, configurable: true });
  def('share', (m === 'none' || m === 'copyfail') ? undefined : async d => {
    window.__shared.push(d);
    if (m === 'abort') { const e = new Error('cancel'); e.name = 'AbortError'; throw e; }
    if (m === 'error') { const e = new Error('boom'); e.name = 'NotAllowedError'; throw e; }
  });
  def('clipboard', m === 'copyfail' ? { writeText: async () => { throw new Error('no'); } } : { writeText: async s => { window.__copied.push(s); } });
  if (m === 'copyfail') document.execCommand = () => false;
}"""

def open_game(b, g, embed=False, lang='es', script='trad'):
    ctx = b.new_context(viewport={'width': 430, 'height': 900}); ctx.route('**/*', smoke.route)
    ctx.add_init_script("addEventListener('message',e=>{if(e.data&&e.data.type==='scene-complete')window.__sc=e.data})")
    page = ctx.new_page(); errs = []
    page.on('pageerror', lambda e: errs.append(str(e))); page.on('dialog', lambda d: d.accept())
    page.goto(f'http://127.0.0.1:{PORT}/games/{g}/index.html' + ('?embed=1&name=Ana' if embed else '')); page.wait_for_timeout(400)
    if embed: page.click('#intro-go')
    else: page.fill('#player-name-input', 'Ana'); page.click('.btn-primary')
    page.wait_for_timeout(200)
    if script == 'simp': page.evaluate("loadT2S()"); page.wait_for_timeout(600)   # 選簡體時才載入轉換器
    page.evaluate(f"Settings.lang='{lang}'; Settings.script='{script}'")
    return ctx, page, errs

def to_lb(page, score, name='Ana'):
    page.evaluate(f"Game.playerName={name!r}; Game.score={score}; showLeaderboard()"); page.wait_for_timeout(250)

with sync_playwright() as p:
    b = p.chromium.launch()

    print('[1] 每個遊戲：按鈕位置、樣式、0 分不顯示、重複進排行榜不會變兩顆', len(GAMES), '個遊戲')
    for g in GAMES:
        ctx, page, errs = open_game(b, g)
        title = page.evaluate('document.title')
        ok(' · ' in title, f'{g}: 標題要是「中文 · 西文」', title)
        to_lb(page, 80)
        ok(page.locator('#leaderboard-screen #shareBtn:visible').count() == 1, f'{g}: 有分數時看得到分享鈕')
        ok(page.evaluate("document.getElementById('shareBtn').nextElementSibling.classList.contains('btn-restart')"), f'{g}: 分享鈕在「再玩一次」正上方')
        ok(page.evaluate("!document.getElementById('shareBtn').classList.contains('btn-restart')"), f'{g}: 分享鈕不能用 btn-restart')
        ok(page.inner_text('#shareBtn').replace('\n', ' ') == '分享成績 Compartir resultado', f'{g}: 按鈕文字', page.inner_text('#shareBtn'))
        ok(page.locator('#leaderboard-screen .btn-restart').count() == 1, f'{g}: 「再玩一次」還是只有一顆')
        to_lb(page, 80)
        ok(page.locator('#shareBtn').count() == 1, f'{g}: 再進一次排行榜不會多一顆')
        to_lb(page, 0)
        ok(page.locator('#shareBtn').count() == 0, f'{g}: 0 分不顯示')
        to_lb(page, -20)
        ok(page.locator('#shareBtn').count() == 0, f'{g}: 負分不顯示')
        ok(not errs, f'{g}: 沒有 pageerror', str(errs[:2]))
        ctx.close()

    print('[2] 一句話：暱稱有無 × 語言 × 繁簡（麵店）')
    cases = [
        ('es', 'trad', 'Ana', '¡Soy Ana y saqué 80 puntos en 麵店 (Sobrevive en Taiwán)! ¿Puedes superarme?'),
        ('es', 'trad', '',    '¡Saqué 80 puntos en 麵店 (Sobrevive en Taiwán)! ¿Puedes superarme?'),
        ('en', 'trad', 'Ana', 'I’m Ana and I scored 80 in 麵店 (Survive in Taiwan)! Can you beat me?'),
        ('en', 'trad', '',    'I scored 80 in 麵店 (Survive in Taiwan)! Can you beat me?'),
        ('zh', 'trad', 'Ana', '我是Ana，在台灣生存日記的麵店拿到 80 分！你能超過我嗎？'),
        ('zh', 'trad', '',    '我在台灣生存日記的麵店拿到 80 分！你能超過我嗎？'),
        ('zh', 'simp', 'Ana', '我是Ana，在台湾生存日记的面店拿到 80 分！你能超过我吗？'),
        ('zh', 'simp', '',    '我在台湾生存日记的面店拿到 80 分！你能超过我吗？'),
        ('es', 'simp', 'Ana', '¡Soy Ana y saqué 80 puntos en 面店 (Sobrevive en Taiwán)! ¿Puedes superarme?'),
    ]
    for lang, script, nick, want in cases:
        ctx, page, errs = open_game(b, 'noodle', lang=lang, script=script)
        page.evaluate(f"Game.playerName={nick!r}; Game.score=80")
        got = page.evaluate('shareMessage()')
        ok(got == want, f'一句話 {lang}/{script}/{"有暱稱" if nick else "無暱稱"}', f'{got!r}')
        ctx.close()

    print('[3] 按鈕文字跟著語言／繁簡（含台灣用字）')
    for lang, script, want in [('es', 'trad', '分享成績 Compartir resultado'), ('en', 'trad', '分享成績 Share my score'),
                               ('zh', 'trad', '分享成績'), ('zh', 'simp', '分享成绩'), ('en', 'simp', '分享成绩 Share my score')]:
        ctx, page, errs = open_game(b, 'noodle', lang=lang, script=script)
        to_lb(page, 80)
        got = page.inner_text('#shareBtn').replace('\n', ' ')
        ok(got == want, f'按鈕文字 {lang}/{script}', got)
        ctx.close()

    print('[4] 按下去：系統分享／玩家關掉／出錯／不支援／複製失敗')
    def press(mode, embed=False):
        ctx, page, errs = open_game(b, 'noodle', embed=embed)
        page.evaluate(STUB, mode); to_lb(page, 80)
        page.click('#shareBtn'); page.wait_for_timeout(250)
        return ctx, page, errs
    COPIED = '已複製，可以貼給朋友 Copiado, ¡pégalo a un amigo!'
    label = lambda pg: pg.inner_text('#shareBtn').replace('\n', ' ')
    # 成功
    ctx, page, errs = press('ok')
    sh = page.evaluate('window.__shared')
    ok(len(sh) == 1 and sh[0]['url'] == URL, '系統分享：連結是首頁加 ?ref=share', str(sh))
    ok(sh and sh[0]['title'] == '台灣生存日記 · Sobrevive en Taiwán', '系統分享：標題', str(sh))
    ok(sh and sh[0]['text'] == '¡Soy Ana y saqué 80 puntos en 麵店 (Sobrevive en Taiwán)! ¿Puedes superarme?', '系統分享：一句話', str(sh))
    ok('?code' not in URL and 'embed' not in URL and 'class' not in URL, '連結不帶班級碼等參數')
    ok(page.evaluate('window.__copied') == [], '系統分享成功時不複製')
    ok(label(page) == '分享成績 Compartir resultado', '系統分享成功後按鈕文字不變', label(page))
    ok(not errs, '系統分享：沒有 pageerror', str(errs)); ctx.close()
    # 玩家自己關掉
    ctx, page, errs = press('abort')
    ok(page.evaluate('window.__copied') == [] and label(page) == '分享成績 Compartir resultado', '玩家關掉選單：什麼都不做（不複製、不顯示失敗）', label(page)); ctx.close()
    # 其他錯誤 → 複製
    ctx, page, errs = press('error')
    cp = page.evaluate('window.__copied')
    ok(cp == ['¡Soy Ana y saqué 80 puntos en 麵店 (Sobrevive en Taiwán)! ¿Puedes superarme?\n' + URL], '分享出錯：改複製「一句話＋連結」', str(cp))
    ok(label(page) == COPIED, '分享出錯：按鈕顯示已複製', label(page))
    page.wait_for_timeout(2400)
    ok(label(page) == '分享成績 Compartir resultado', '已複製提示 2 秒後復原', label(page)); ctx.close()
    # 不支援
    ctx, page, errs = press('none')
    ok(len(page.evaluate('window.__copied')) == 1 and label(page) == COPIED, '不支援分享選單：改複製', label(page)); ctx.close()
    # 複製也失敗
    ctx, page, errs = press('copyfail')
    ok(label(page) == '複製失敗 No se pudo copiar', '複製失敗：顯示失敗', label(page))
    ok(not errs, '複製失敗：沒有 pageerror', str(errs)); ctx.close()
    # 連點不會送兩次
    ctx, page, errs = open_game(b, 'noodle')
    page.evaluate(STUB, 'ok'); to_lb(page, 80)
    page.evaluate("document.getElementById('shareBtn').click(); document.getElementById('shareBtn').click()"); page.wait_for_timeout(250)
    ok(len(page.evaluate('window.__shared')) == 1, '連點兩下只送一次', str(page.evaluate('window.__shared'))); ctx.close()
    # 英文 + 複製備案 + 簡體
    ctx, page, errs = open_game(b, 'noodle', lang='en', script='simp')
    page.evaluate(STUB, 'none'); to_lb(page, 80); page.click('#shareBtn'); page.wait_for_timeout(250)
    ok(label(page) == '已复制，可以贴给朋友 Copied, paste it to a friend!', '英文＋簡體的已複製提示', label(page)); ctx.close()

    print('[5] 地圖（embed）模式')
    ctx, page, errs = press('ok', embed=True)
    ok(page.evaluate("document.getElementById('shareBtn').nextElementSibling.classList.contains('btn-restart')"), '地圖模式：分享鈕在按鈕正上方')
    ok('回到地圖' in page.inner_text('#leaderboard-screen .btn-restart'), '地圖模式：主按鈕是「回到地圖」', page.inner_text('#leaderboard-screen .btn-restart'))
    ok(len(page.evaluate('window.__shared')) == 1, '地圖模式：可以分享')
    page.click('#leaderboard-screen .btn-restart'); page.wait_for_timeout(200)
    sc = page.evaluate('window.__sc||null')
    ok(sc and sc.get('score') == 80, '地圖模式：按「回到地圖」仍然送出成績', str(sc))
    ok(not errs, '地圖模式：沒有 pageerror', str(errs)); ctx.close()

    print('[6] 地圖首頁 iframe 要允許分享選單')
    html = open(os.path.join(smoke.ROOT, 'index.html'), encoding='utf8').read()
    ok(re.search(r'<iframe id="frame"[^>]*allow="[^"]*web-share', html) is not None, 'iframe allow 含 web-share')
    b.close()

print(f'\n共 {n[0]} 項，失敗 {len(fails)} 項')
sys.exit(1 if fails else 0)
