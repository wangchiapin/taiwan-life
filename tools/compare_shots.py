r"""改之前／改之後逐畫面比對：python3 tools/compare_shots.py [--keep-pulse] [--real-tabs] <遊戲> <舊檔.html> [輸出資料夾]
兩邊用同一個隨機種子、固定時間，照正解（沒有正解就固定選第一個）玩一遍，
每一步都截圖比對；也比對繁簡、西英、拼音、手機尺寸、嵌入模式、排行榜畫面。
另外每張截圖都記下右邊三顆分頁按鈕（任務提示、本關單字、錯誤紀錄）的座標、樣式、文字，兩邊也要一樣。

【乾淨模式（預設）】右邊那排按鈕在截圖裡有兩種和程式無關的雜訊，所以預設先處理掉：
  1. 「任務提示」登入後約 1 秒開始閃、閃 6.5 秒（減少動態時變成黃色外框），拍到與否看時間
     → 預設設成「已看過提示」，不閃。加 --keep-pulse 可保留。
  2. 分頁條用 top:50% ＋ translateY(-50%) 置中，位置是小數（約 240.305），瀏覽器畫的時候有時進位有時捨去，
     差 1 像素（同一份檔案自己比自己也會）→ 預設把分頁條固定在整數位置。加 --real-tabs 可保留
     （畫面會有 1 像素雜訊；座標數字仍然會比）。
  所以「閃動的瞬間」和「置中的像素畫面」這個工具比不到，要用手機看。

【準備舊檔】舊的共用檔要另存成 shared/game_before.js，舊遊戲檔裡的連結也要指向它。例如（改之前的提交是 abc123）：
  git show abc123:shared/game.js > shared/game_before.js
  git show abc123:games/drinks/index.html | sed 's#\.\./\.\./shared/game\.js#../../shared/game_before.js#' > /tmp/drinks_old.html
  python3 tools/compare_shots.py drinks /tmp/drinks_old.html /tmp/cmp_drinks
  rm shared/game_before.js        # 用完要刪；推之前用 git status 確認沒有未追蹤的檔案

【注意】工具直接讀這個資料夾：比對時不要改檔案，也不要同時跑 smoke.py；同一個遊戲不能同時跑兩次
（都會用 games/<遊戲>/_before.html，跑完或出錯會自動刪掉）。
【判讀】「不一樣」＝畫面有明顯差異（≥ 80 個明顯像素）；「微小差異」是肉眼看不出的雜訊，只列出位置；
「[按鈕]」＝右邊分頁按鈕的座標／樣式／文字不同，會列出哪一項。
某一組（繁西／簡英拼音／手機／嵌入）兩邊的步驟不同時，那一組不比（可能是某次點擊剛好失敗讓編號錯開，重跑一次就好）。
有任何不一樣時，結束代碼是 1。"""
import sys, os, re, json, shutil, pathlib, atexit
FLAGS = {a for a in sys.argv[1:] if a.startswith('--')}
ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
if len(ARGS) < 2 or FLAGS - {'--keep-pulse', '--real-tabs'}:
    print(__doc__); sys.exit(2)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smoke
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops

game, old = ARGS[0], ARGS[1]
OUT = pathlib.Path(ARGS[2] if len(ARGS) > 2 else f'/tmp/cmp_{game}'); OUT.mkdir(parents=True, exist_ok=True)
GDIR = pathlib.Path(smoke.ROOT) / 'games' / game
tmp = GDIR / '_before.html'; shutil.copy(old, tmp)
atexit.register(lambda: tmp.unlink(missing_ok=True))      # 中途出錯也要刪掉暫存檔
KEEP_PULSE = '--keep-pulse' in FLAGS
FIX_TABS = '--real-tabs' not in FLAGS
# 閃動的開關是 shared/game.js 的 HintPulse（localStorage 的 hanziGames.hintSeen）；那邊改名的話，這裡也要跟著改
INIT = ("""(() => { let s = 12345; Math.random = () => { s = (s * 1103515245 + 12345) % 2147483648; return s / 2147483648; };
  const T0 = 1760500000000; Date.now = () => T0; localStorage.clear(); __SEEN__
  document.addEventListener('DOMContentLoaded', () => { const st = document.createElement('style');
    st.textContent = '*,*::before,*::after{transition:none!important;animation:none!important;caret-color:transparent!important}' + __CSS__; document.head.appendChild(st); }); })();"""
        .replace('__SEEN__', '' if KEEP_PULSE else "localStorage.setItem('hanziGames.hintSeen', '1');")
        .replace('__CSS__', json.dumps('#side-tabs{transform:none!important;top:240px!important}' if FIX_TABS else '')))
print(f'模式：任務提示閃動{"保留" if KEEP_PULSE else "關閉"}、右邊分頁條{"原本位置" if not FIX_TABS else "固定在整數位置"}')

# 右邊三顆分頁按鈕＋外框的座標、樣式、文字、裡面的小字（每拍一張截圖就記一份）
SNAP_JS = """() => { const props = ['display','width','height','paddingTop','paddingBottom','paddingLeft','paddingRight','marginTop','fontSize','fontWeight','letterSpacing','lineHeight','color','backgroundColor','borderRadius','transform','outlineStyle','outlineWidth','boxShadow','opacity','writingMode'];
  const r = id => { const e = document.getElementById(id); if (!e) return null; const b = e.getBoundingClientRect(), c = getComputedStyle(e), st = {}; props.forEach(p => st[p] = c[p]);
    const kids = [...e.children].map(k => { const kc = getComputedStyle(k), kb = k.getBoundingClientRect(); return { cls: k.className, text: k.textContent, top: +kb.top.toFixed(3), height: +kb.height.toFixed(3), fontSize: kc.fontSize, display: kc.display, color: kc.color, bg: kc.backgroundColor }; });
    return { rect: [+b.top.toFixed(3), +b.height.toFixed(3), +b.left.toFixed(3), +b.width.toFixed(3)], text: e.textContent, cls: e.className, hidden: e.hidden, st, kids }; };
  return { stack: r('side-tabs'), hint: r('hint-tab'), vocab: r('vocab-tab'), log: r('log-tab') }; }"""
SNAPS = []

def snap_diff(a, b, path=''):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)): out += snap_diff(a.get(k), b.get(k), f'{path}/{k}')
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)): out += snap_diff(x, y, f'{path}/{i}')
    elif a != b: out.append(f'{path}: {a!r} → {b!r}')
    return out

def shot(page):
    page.mouse.move(0, 0); page.wait_for_timeout(60)
    try: page.wait_for_function("[...document.images].every(i => i.complete)", timeout=3000)   # 等圖片載完
    except Exception: pass
    SNAPS.append(page.evaluate(SNAP_JS))
    return page.screenshot(full_page=True)

def play(page, scenario):
    shots = []; bad = set(); rng = __import__('random').Random(42)
    orc = smoke.EXTRA.get(game) or smoke.ORACLES.get(game)
    for step in range(150):
      try:
            page.wait_for_timeout(120)
            if page.evaluate("document.getElementById('leaderboard-screen').classList.contains('active')"):
                page.wait_for_timeout(300); shots.append(('leaderboard', shot(page))); break
            st = page.evaluate('Game.state')
            if page.evaluate('Game.mistakes') >= 8: page.evaluate('Game.mistakes = 0')   # 不要觸發「錯太多次重來」（和 smoke.py 一樣）
            if st == 'RESULT' and page.evaluate('EMBED'): shots.append(('RESULT', shot(page))); break
            if game == 'breakfast' and page.evaluate("!!(Game.getConfig()[Game.state]||{}).pad"):
                page.evaluate("Game.pad.ticket=[...Game.C.target]; Game.padSubmit()"); continue
            if page.locator('#ami-pop').count():          # Ami 的懸浮視窗（冰淇淋店）會擋住選項：和 smoke.py 一樣先按掉
                page.click('#ami-pop [data-act="open"]' if page.locator('#ami-pop [data-act="open"]').count() else '#ami-pop [data-act="reply"]'); continue
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
            idx = None
            if ans:
                for i, o in enumerate(opts):
                    if o.strip() == ans or ans in o: idx = i; break
            if idx is None:      # 沒有正解：照順序試，選錯的記起來，下次換下一個（兩邊完全一樣）
                cand = [i for i, o in enumerate(opts) if (st, o) not in bad] or list(range(len(opts)))
                idx = rng.choice(cand)        # 兩邊用同一組隨機數字，所以選的一樣
            m0 = page.evaluate('Game.mistakes')
            try:
                smoke.click_i(page, idx)
                page.wait_for_timeout(60)
                if page.evaluate('Game.mistakes') > m0: bad.add((st, opts[idx]))
            except Exception as e:
                page.wait_for_timeout(600); continue          # 畫面剛好在換（例如錯太多次重新開始），下一輪再看
      except Exception as e:       # 畫面剛好在重新整理（錯太多次自動重來）
        if 'closed' in str(e): raise
        page.wait_for_timeout(700)
    return shots

SCEN = [('trad_es', {}, '', 'panels'), ('simp_en_py', {}, 'simp_en', 'pinyin'), ('phone', {'width': 390, 'height': 844}, '', ''),
        ('embed', {}, 'embed', '')]
diffs = 0; total = 0; tabdiffs = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    res = {}
    for which, fname in [('old', '_before.html'), ('new', 'index.html')]:
        for name, vp, mode, extra in SCEN:
            ctx = b.new_context(viewport=vp or {'width': 1000, 'height': 900}, reduced_motion='reduce'); ctx.route('**/*', smoke.route); ctx.add_init_script(INIT)
            page = ctx.new_page(); page.set_default_timeout(8000); errs = []      # 單次等待最多 8 秒，卡住時不會一等 30 秒
            page.on('pageerror', lambda e: errs.append(str(e))); page.on('dialog', lambda d: d.accept())
            q = '?embed=1&name=Ana' if mode == 'embed' else ''
            SNAPS.clear()
            page.goto(f'http://127.0.0.1:{smoke.PORT}/games/{game}/{fname}{q}'); page.wait_for_timeout(500)
            shots = [('login', shot(page))]
            if mode != 'embed':
                if mode == 'simp_en':
                    page.click('#set-open'); page.click('[data-k=script][data-v=simp]'); page.wait_for_timeout(400); page.click('[data-k=lang][data-v=en]'); page.click('#set-done'); page.wait_for_timeout(400)   # 設定畫面改版後的按鈕
                    shots.append(('login2', shot(page)))
                page.fill('#player-name-input', 'María'); page.click('.btn-primary'); page.wait_for_timeout(300)
                if extra == 'pinyin': page.click('#btn-pinyin'); page.click('[data-k=phon][data-v=pinyin]'); page.click('#set-done'); page.wait_for_timeout(200)
            shots += play(page, extra)
            res[(which, name)] = (shots, errs, list(SNAPS))
            ctx.close()
    b.close()
for name, *_ in SCEN:
    so, eo, ao = res[('old', name)]; sn, en, an = res[('new', name)]
    if eo or en: print(f'  {name} 錯誤 old={eo[:2]} new={en[:2]}')
    if [k for k, _ in so] != [k for k, _ in sn]:
        print(f'  {name} 步驟不同：old 共 {len(so)} 步、new 共 {len(sn)} 步；第一個不同：', next((a[0]+' / '+b[0] for a, b in zip(so, sn) if a[0] != b[0]), '長度不同'), '（這一組沒有比對，請重跑）'); diffs += 1; continue
    for (k, a), (_, c) in zip(so, sn):
        total += 1
        fa, fc = OUT / f'{name}_{k}_old.png', OUT / f'{name}_{k}_new.png'
        fa.write_bytes(a); fc.write_bytes(c)
        A, C = Image.open(fa).convert('RGB'), Image.open(fc).convert('RGB')
        D = ImageChops.difference(A, C) if A.size == C.size else None
        if D is None or D.getbbox():
            big = None if D is None else sum(D.convert('L').histogram()[17:])
            if big is not None and big < 80:          # 肉眼看不出的雜訊（反鋸齒、陰影動畫的瞬間）
                print(f'  · {name} {k} 微小差異（{big} 個明顯像素）box={D.getbbox()}，不算'); fa.unlink(); fc.unlink(); continue
            diffs += 1
            print(f'  ✗ {name} {k} 不一樣 size {A.size}/{C.size} box={None if D is None else D.getbbox()} 明顯像素={big}')
        else: fa.unlink(); fc.unlink()
    shown = 0; bad_snaps = 0
    for i, (a, c) in enumerate(zip(ao, an)):
        d = snap_diff(a, c)
        if d:
            bad_snaps += 1
            if shown < 3:
                shown += 1; print(f'  [按鈕] {name} 第{i}張（{so[i][0]}）：' + '；'.join(d[:4]) + (f'…共 {len(d)} 項' if len(d) > 4 else ''))
    tabdiffs += bad_snaps
    if bad_snaps: print(f'  [按鈕] {name}：{len(ao)} 張裡右邊分頁按鈕不一樣的有 {bad_snaps} 張')
print(f'{game}：比對 {total} 張畫面，不一樣 {diffs} 張；右邊分頁按鈕不一樣 {tabdiffs} 張')
sys.exit(1 if diffs or tabdiffs else 0)
