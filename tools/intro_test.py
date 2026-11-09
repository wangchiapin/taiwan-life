r"""地圖模式介紹視窗測試：python3 tools/intro_test.py [遊戲…]（不指定＝全部遊戲）
檢查：①地圖模式一進來先跳出視窗（標題、遊戲介紹、「出發吧！」），這時遊戲畫面還沒開始 ②按「出發吧！」才進遊戲、開始畫面是 START
③單機模式不會跳 ④重新開始（r=1）不會再跳 ⑤西／英文、簡體、拼音、手機大小都正常、沒有網頁錯誤 ⑥按鍵盤 Enter 也能出發。"""
import sys, os, glob, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location('smoke', os.path.join(HERE, 'smoke.py'))
smoke = importlib.util.module_from_spec(spec); sys.modules['smoke'] = smoke; spec.loader.exec_module(smoke)
from playwright.sync_api import sync_playwright
games = sys.argv[1:] or sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(ROOT + '/games/*/index.html'))
FAILS = []; N = [0]
def check(name, ok, info=''):
    N[0] += 1
    if not ok: FAILS.append(f'✗ {name} {info}'); print('✗', name, info)
def page_for(b, g, q, vp=None, init=None):
    ctx = b.new_context(viewport=vp or {'width': 1000, 'height': 900}); ctx.route('**/*', smoke.route)
    if init: ctx.add_init_script(init)
    p = ctx.new_page(); p.errs = []; p.on('pageerror', lambda e: p.errs.append(str(e)))
    p.goto(f'http://127.0.0.1:{smoke.PORT}/games/{g}/index.html{q}'); p.wait_for_timeout(350); return p
active = "document.getElementById('game-window').classList.contains('active')"
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for g in games:
        p = page_for(b, g, '?embed=1&name=Ana')
        check(f'{g} 地圖：跳出介紹視窗', p.locator('#intro-pop #intro-go').count() == 1)
        check(f'{g} 地圖：視窗裡有標題和介紹', p.locator('#intro-pop h2').inner_text().strip() != '' and p.locator('#intro-pop .intro-text').count() >= 1)
        check(f'{g} 地圖：視窗出現時遊戲還沒開始', not p.evaluate(active) and p.evaluate('Game.state') == 'START' and p.evaluate('Game.timerInterval') in (None, 0))
        box = p.locator('#intro-pop .intro-card').bounding_box(); vp = p.viewport_size
        check(f'{g} 地圖：視窗在畫面內', box and box['x'] >= 0 and box['x'] + box['width'] <= vp['width'] + 1, box)
        p.keyboard.press('Enter'); p.wait_for_timeout(250)
        check(f'{g} 地圖：Enter 出發', p.locator('#intro-pop').count() == 0 and p.evaluate(active))
        check(f'{g} 地圖：出發後是第一關', p.evaluate('Game.state') == 'START' and p.locator('#npc-dialogue').inner_text().strip() != '')
        check(f'{g} 地圖：沒有網頁錯誤', not p.errs, p.errs); p.context.close()
        p = page_for(b, g, '?embed=1&name=Ana&r=1')
        check(f'{g} 重新開始：不再跳視窗、直接開始', p.locator('#intro-pop').count() == 0 and p.evaluate(active)); p.context.close()
        p = page_for(b, g, '')
        check(f'{g} 單機：不跳視窗', p.locator('#intro-pop').count() == 0 and not p.evaluate(active)); p.fill('#player-name-input', 'María'); p.click('.btn-primary'); p.wait_for_timeout(250)
        check(f'{g} 單機：照常進遊戲', p.locator('#intro-pop').count() == 0 and p.evaluate(active)); p.context.close()
    # 少數遊戲再測：英文、簡體、手機、拼音（不用全部測）
    for g in [x for x in ['yansuji', 'clinic', 'bakery'] if x in games]:
        for tag, q, vp in [('英文', '?embed=1&name=Ana&l=en', None), ('簡體', '?embed=1&name=Ana&s=simp', None), ('手機', '?embed=1&name=Ana', {'width': 360, 'height': 640})]:
            p = page_for(b, g, q, vp); t = p.evaluate("(()=>{const c=document.querySelector('#intro-pop .intro-card').cloneNode(true);c.querySelectorAll('rt').forEach(r=>r.remove());return c.textContent})()")
            if tag == '英文': check(f'{g} {tag}：看得到英文介紹', any(w in t for w in ('Ami', 'Let')) and "Let's go" in t, t[:80])
            if tag == '簡體': check(f'{g} {tag}：標題轉成簡體', '出发吧' in t, t[:80])
            if tag == '手機':
                check(f'{g} {tag}：沒有橫向捲動', p.evaluate('document.documentElement.scrollWidth<=window.innerWidth+1'))
                check(f'{g} {tag}：按鈕按得到', p.locator('#intro-go').is_visible())
            check(f'{g} {tag}：沒有網頁錯誤', not p.errs, p.errs); p.context.close()
    b.close()
print(f'通過 {N[0] - len(FAILS)} 項，失敗 {len(FAILS)} 項')
for f in FAILS: print(f)
sys.exit(1 if FAILS else 0)
