"""改之前／改之後逐畫面比對：python3 tools/compare_shots.py <game> <舊檔.html> [輸出資料夾]
兩邊用同一個隨機種子、固定時間，照正解（沒有正解就固定選第一個）玩一遍，
每一步都截圖比對；也比對繁簡、西英、拼音、手機尺寸、嵌入模式、排行榜畫面。"""
import sys, os, re, json, shutil, pathlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smoke
smoke_timeout = 8000
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops

game, old = sys.argv[1], sys.argv[2]
OUT = pathlib.Path(sys.argv[3] if len(sys.argv) > 3 else f'/tmp/cmp_{game}'); OUT.mkdir(parents=True, exist_ok=True)
GDIR = pathlib.Path(smoke.ROOT) / 'games' / game
tmp = GDIR / '_before.html'; shutil.copy(old, tmp)
INIT = """(() => { let s = 12345; Math.random = () => { s = (s * 1103515245 + 12345) % 2147483648; return s / 2147483648; };
  const T0 = 1760500000000; Date.now = () => T0; localStorage.clear();
  document.addEventListener('DOMContentLoaded', () => { const st = document.createElement('style');
    st.textContent = '*,*::before,*::after{transition:none!important;caret-color:transparent!important}'; document.head.appendChild(st); }); })();"""

def shot(page):
    page.mouse.move(0, 0); page.wait_for_timeout(60)
    return page.screenshot(full_page=True)

def play(page, scenario):
    shots = []
    orc = smoke.EXTRA.get(game) or smoke.ORACLES.get(game)
    for step in range(200):
        page.wait_for_timeout(120)
        if page.evaluate("document.getElementById('leaderboard-screen').classList.contains('active')"):
            page.wait_for_timeout(300); shots.append(('leaderboard', shot(page))); break
        st = page.evaluate('Game.state')
        if st == 'RESULT' and page.evaluate('EMBED'): shots.append(('RESULT', shot(page))); break
        if game == 'breakfast' and page.evaluate("!!(Game.getConfig()[Game.state]||{}).pad"):
            page.evaluate("Game.pad.ticket=[...Game.C.target]; Game.padSubmit()"); continue
        opts = smoke.texts(page)
        if not opts: continue
        shots.append((f'{step:02d}_{st}', shot(page)))
        if step == 2 and scenario == 'panels':        # 打開三個側邊分頁各拍一張
            for tab in ['vocab-tab', 'hint-tab', 'log-tab']:
                if page.locator('#' + tab).is_visible():
                    page.click('#' + tab); page.wait_for_timeout(150); shots.append((f'{step:02d}_{tab}', shot(page)))
                    page.evaluate('Vocab.toggle(false); Hints.toggle(false); Log.toggle(false)'); page.wait_for_timeout(100)
            if page.locator('.tr-btn[data-tr]').count():
                page.locator('.tr-btn[data-tr]').first.click(); page.wait_for_timeout(150)
                shots.append((f'{step:02d}_tr', shot(page))); page.evaluate('Tr.closeAll()')
        ans = None
        if orc:
            try: ans = page.evaluate(orc)
            except Exception: ans = None
        idx = 0
        if ans:
            for i, o in enumerate(opts):
                if o.strip() == ans or ans in o: idx = i; break
        elif step % 3 == 1 and len(opts) > 1: idx = 1          # 沒有正解：偶爾選錯，看到錯誤卡片
        try: smoke.click_i(page, idx)
        except Exception as e:
            page.wait_for_timeout(600); continue          # 畫面剛好在換（例如錯太多次重新開始），下一輪再看
    return shots

SCEN = [('trad_es', {}, '', 'panels'), ('simp_en_py', {}, 'simp_en', 'pinyin'), ('phone', {'width': 390, 'height': 844}, '', ''),
        ('embed', {}, 'embed', '')]
diffs = 0; total = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    res = {}
    for which, fname in [('old', '_before.html'), ('new', 'index.html')]:
        for name, vp, mode, extra in SCEN:
            ctx = b.new_context(viewport=vp or {'width': 1000, 'height': 900}); ctx.route('**/*', smoke.route); ctx.add_init_script(INIT)
            page = ctx.new_page(); errs = []
            page.on('pageerror', lambda e: errs.append(str(e))); page.on('dialog', lambda d: d.accept())
            q = '?embed=1&name=Ana' if mode == 'embed' else ''
            page.goto(f'http://127.0.0.1:{smoke.PORT}/games/{game}/{fname}{q}'); page.wait_for_timeout(500)
            shots = [('login', shot(page))]
            if mode != 'embed':
                if mode == 'simp_en':
                    page.click('[data-script=simp]'); page.click('[data-lang=en]'); page.wait_for_timeout(400)
                    shots.append(('login2', shot(page)))
                page.fill('#player-name-input', 'María'); page.click('.btn-primary'); page.wait_for_timeout(300)
                if extra == 'pinyin': page.click('#btn-pinyin'); page.wait_for_timeout(200)
            shots += play(page, extra)
            res[(which, name)] = (shots, errs)
            ctx.close()
    b.close()
for name, *_ in SCEN:
    so, eo = res[('old', name)]; sn, en = res[('new', name)]
    if eo or en: print(f'  {name} 錯誤 old={eo[:2]} new={en[:2]}')
    if [k for k, _ in so] != [k for k, _ in sn]:
        print(f'  {name} 步驟不同：old={[k for k,_ in so]} new={[k for k,_ in sn]}'); diffs += 1; continue
    for (k, a), (_, c) in zip(so, sn):
        total += 1
        fa, fc = OUT / f'{name}_{k}_old.png', OUT / f'{name}_{k}_new.png'
        fa.write_bytes(a); fc.write_bytes(c)
        A, C = Image.open(fa).convert('RGB'), Image.open(fc).convert('RGB')
        D = ImageChops.difference(A, C) if A.size == C.size else None
        if D is None or D.getbbox():
            big = None if D is None else sum(1 for px in D.convert('L').point(lambda v: 255 if v > 16 else 0).getdata() if px)
            if big is not None and big < 80:          # 肉眼看不出的雜訊（反鋸齒、陰影動畫的瞬間）
                print(f'  · {name} {k} 微小差異（{big} 個明顯像素），不算'); fa.unlink(); fc.unlink(); continue
            diffs += 1
            print(f'  ✗ {name} {k} 不一樣 size {A.size}/{C.size} box={None if D is None else D.getbbox()} 明顯像素={big}')
        else: fa.unlink(); fc.unlink()
tmp.unlink()
print(f'{game}：比對 {total} 張畫面，不一樣 {diffs} 張')
