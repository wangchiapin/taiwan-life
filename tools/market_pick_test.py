# 菜市場「點圖片買菜」專用測試：每個按鈕都按一次（圖片卡、斤數、－／＋、✕、結帳檢查的三種錯誤）
# 用法：NPM=<有 pinyin-pro 和 opencc-js 的 node_modules> python3 tools/market_pick_test.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smoke
from smoke import PORT, route, sync_playwright

fails = []
def check(name, ok, info=''):
    print(('✓ ' if ok else '✗ ') + name + (('  ' + str(info)) if (info != '' and not ok) else ''))
    if not ok: fails.append(name)

def plain(page, sel):   # 拼音預設開著，先把 <rt> 拿掉再比對文字
    return page.evaluate("s=>{const c=document.querySelector(s).cloneNode(true);c.querySelectorAll('rt').forEach(r=>r.remove());return c.innerText.replace(/\\n/g,'')}", sel)
def cart(page): return page.evaluate('JSON.parse(JSON.stringify(Game.cart))')
def mistakes(page): return page.evaluate('Game.mistakes')
def goto_pick(page):
    page.goto(f'http://127.0.0.1:{PORT}/games/market/index.html'); page.wait_for_timeout(400)
    page.fill('#player-name-input', 'María'); page.click('.btn-primary'); page.wait_for_timeout(300)
    page.locator('#options-area .opt').first.click(); page.wait_for_timeout(200)   # 走進菜市場
    # 如果有過場畫面，按掉
    if page.evaluate('Game.state') == '_TRANS': page.locator('#options-area .opt').first.click(); page.wait_for_timeout(200)
    assert page.evaluate('Game.state') == 'PICK', page.evaluate('Game.state')

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1000, 'height': 900}); ctx.route('**/*', route)
    page = ctx.new_page(); errs = []; page.on('pageerror', lambda e: errs.append(str(e)))
    goto_pick(page)

    # 1. 8 張圖片卡：3 張肉（要選斤數）、5 張其他（點一下就放進籃子）
    check('8 張圖片卡', page.locator('.shelf .bun').count() == 8)
    check('3 張肉卡', page.locator('.shelf [data-meat]').count() == 3)
    check('5 張一般卡', page.locator('.shelf [data-veg]').count() == 5)
    check('青菜已經刪掉', plain(page, '.shelf').count('青菜') == 0)
    check('有 高麗菜 小白菜 雞肉 牛肉', all(w in plain(page, '.shelf') for w in ['高麗菜', '小白菜', '雞肉', '牛肉']))
    check('一開始籃子是空的', cart(page) == {})

    # 2. 一般卡：點一下 +1
    page.locator('[data-veg="tomato"]').click(); page.locator('[data-veg="tomato"]').click()
    check('番茄點兩下＝2', cart(page).get('tomato') == 2, cart(page))
    page.locator('[data-adj="tomato"][data-d="1"]').click()
    check('＋ → 3', cart(page).get('tomato') == 3, cart(page))
    page.locator('[data-adj="tomato"][data-d="-1"]').click()
    check('－ → 2', cart(page).get('tomato') == 2, cart(page))
    page.locator('[data-adj="tomato"][data-d="-1"]').click(); page.locator('[data-adj="tomato"][data-d="-1"]').click()
    check('－ 到 0 整列消失', 'tomato' not in cart(page) and page.locator('[data-adj="tomato"]').count() == 0, cart(page))
    for cid in ['cabbage', 'bokchoy', 'egg', 'fish']:
        page.locator(f'[data-veg="{cid}"]').click()
    check('其他 4 種各點一下', all(cart(page).get(k) == 1 for k in ['cabbage', 'bokchoy', 'egg', 'fish']), cart(page))
    for cid in ['cabbage', 'bokchoy', 'egg', 'fish']:
        page.locator(f'[data-adj="{cid}"][data-d="-1"]').click()
    check('清空', cart(page) == {}, cart(page))

    # 3. 肉：點圖片 → 出現半斤／一斤／兩斤；✕ 收起；每個斤數；再點同一張換斤數＝取代，不是加
    for mid in ['pork', 'beef', 'chicken']:
        page.locator(f'[data-meat="{mid}"]').click()
        check(f'{mid}：出現斤數選項', page.locator('.amt .amtb').count() == 3 and page.locator('.amt').is_visible())
        page.locator('.amt .amtx').click()
        check(f'{mid}：✕ 收起', page.locator('.amt').count() == 0)
        page.locator(f'[data-meat="{mid}"]').click(); page.locator(f'[data-meat="{mid}"]').click()
        check(f'{mid}：再點一次圖片也能收起', page.locator('.amt').count() == 0)
        for k, want in [(0, 0.5), (1, 1), (2, 2)]:
            page.locator(f'[data-meat="{mid}"]').click(); page.locator('.amt .amtb').nth(k).click()
            check(f'{mid}：選第 {k+1} 個斤數＝{want}', cart(page).get(mid) == want and page.locator('.amt').count() == 0, cart(page))
        check(f'{mid}：換斤數是取代（只有一列）', page.locator(f'[data-adj="{mid}"]').count() == 1)
        page.locator(f'[data-adj="{mid}"]').click()
        check(f'{mid}：－ 整份放回去', mid not in cart(page), cart(page))
    check('價錢（豬 300／牛 450／雞 180 元每斤）', page.evaluate("[BYID.pork.price,BYID.beef.price,BYID.chicken.price].join()") == '300,450,180')
    page.locator('[data-meat="beef"]').click(); page.locator('.amt .amtb').nth(1).click()
    check('合計＝450', page.locator('.tray .total b').inner_text().startswith('450'), page.locator('.tray .total b').inner_text())
    check('右上角顯示籃子', '🧺' in page.locator('#cash-badge').inner_text(), page.locator('#cash-badge').inner_text())
    page.locator('[data-adj="beef"]').click()

    # 4. 結帳檢查：空籃子、買了沒要的、數量不對、對
    t = page.evaluate('JSON.parse(JSON.stringify(Game.task))')
    def buy_qty(it, q):
        if it.get('meat'):
            page.locator(f'[data-meat="{it["id"]}"]').click()
            idx = {0.5: 0, 1: 1, 2: 2}[q]; page.locator('.amt .amtb').nth(idx).click()
        else:
            for _ in range(q): page.locator(f'[data-veg="{it["id"]}"]').click()
    m0 = mistakes(page)
    page.locator('#options-area .opt').first.click()
    check('空籃子結帳 → 扣分、還在買菜', mistakes(page) == m0 + 1 and page.evaluate('Game.state') == 'PICK')
    ids = [it['id'] for it in t['items']]
    other = [k for k in ['pork', 'beef', 'chicken', 'egg', 'fish', 'cabbage', 'bokchoy', 'tomato'] if k not in ids][0]
    oit = page.evaluate(f'BYID["{other}"]')
    buy_qty(oit, 1)
    for it in t['items']: buy_qty(it, it['q'])
    m1 = mistakes(page); page.locator('#options-area .opt').first.click()
    check('買了沒要的菜 → 扣分、還在買菜', mistakes(page) == m1 + 1 and page.evaluate('Game.state') == 'PICK')
    check('錯誤說明有「沒有要」', '沒有要' in page.evaluate('Game.log[Game.log.length-1].zh'), page.evaluate('Game.log[Game.log.length-1].zh'))
    page.locator(f'[data-adj="{other}"]').first.click()
    if not oit.get('meat') and cart(page).get(other): page.locator(f'[data-adj="{other}"]').first.click()
    # 數量不對：第一樣菜改成別的數量
    it0 = t['items'][0]
    if it0.get('meat'):
        page.locator(f'[data-meat="{it0["id"]}"]').click(); page.locator('.amt .amtb').nth(2 if it0['q'] != 2 else 0).click()
    else:
        page.locator(f'[data-adj="{it0["id"]}"][data-d="1"]').click()
    m2 = mistakes(page); page.locator('#options-area .opt').first.click()
    check('數量不對 → 扣分、還在買菜', mistakes(page) == m2 + 1 and page.evaluate('Game.state') == 'PICK')
    check('錯誤說明有「你買了」', '你買了' in page.evaluate('Game.log[Game.log.length-1].zh'), page.evaluate('Game.log[Game.log.length-1].zh'))
    # 少一樣
    page.locator(f'[data-adj="{t["items"][1]["id"]}"]').first.click()
    while cart(page).get(t['items'][1]['id']): page.locator(f'[data-adj="{t["items"][1]["id"]}"]').first.click()
    m3 = mistakes(page); page.locator('#options-area .opt').first.click()
    check('少一樣 → 扣分、還在買菜', mistakes(page) == m3 + 1 and page.evaluate('Game.state') == 'PICK')
    check('錯誤說明有「還要」', '還要' in page.evaluate('Game.log[Game.log.length-1].zh'), page.evaluate('Game.log[Game.log.length-1].zh'))
    # 改對
    page.evaluate('Game.cart = {}; Game.render()')
    for it in t['items']: buy_qty(it, it['q'])
    m4 = mistakes(page); page.locator('#options-area .opt').first.click(); page.wait_for_timeout(200)
    st = page.evaluate('Game.state')
    check('買對了 → 往下一關（算錢）', mistakes(page) == m4 and st in ('BARGAIN', '_TRANS'), st)
    if st == '_TRANS': page.locator('#options-area .opt').first.click(); page.wait_for_timeout(200)
    check('老闆複誦買了什麼', '你要的是' in plain(page, '#npc-dialogue'), plain(page, '#npc-dialogue')[:80])

    # 5. 每局總價：不超過 900、付得起；折扣、找零算得對（抽 3000 局）
    r = page.evaluate("""() => { const o = {max:0, min:1e9, bad:0, ids:new Set(), n:0};
      for (let i = 0; i < 3000; i++) { Game.setup(); const t = Game.task; o.n++;
        o.max = Math.max(o.max, t.total); o.min = Math.min(o.min, t.total); t.items.forEach(it => o.ids.add(it.id));
        if (t.total > 900 || t.final > 1000 || t.given < 0 || t.given !== 1000 - t.final - (t.shortChange ? 50 : 0) || t.final !== (t.refuse ? t.total : t.total - t.disc)) o.bad++;
        if (!t.items.every(it => it.qs.includes(it.q)) || t.items.length !== 3 || new Set(t.items.map(it => it.id)).size !== 3) o.bad++; }
      return {max:o.max, min:o.min, bad:o.bad, ids:[...o.ids].sort().join(), n:o.n}; }""")
    check('3000 局：總價 ≤ 900、折扣和找零都對', r['bad'] == 0 and r['max'] <= 900, r)
    check('8 種菜都有機會出現', len(r['ids'].split(',')) == 8, r['ids'])
    print('   總價範圍', r['min'], '～', r['max'])

    # 6. 版面：電腦和手機各截一張圖
    page.evaluate('restartGame && 0')
    for vp, name in [({'width': 1000, 'height': 900}, 'desktop'), ({'width': 390, 'height': 844}, 'mobile')]:
        c2 = b.new_context(viewport=vp); c2.route('**/*', route); pg = c2.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        goto_pick(pg)
        pg.locator('[data-veg="bokchoy"]').click(); pg.locator('[data-meat="pork"]').click()
        out = os.environ.get('SHOTS', '/tmp') + f'/market_pick_{name}.png'
        pg.screenshot(path=out, full_page=True); print('   截圖', out)
        c2.close()
    check('沒有 JS 錯誤', not errs, errs[:3])
    b.close()

print('\n全部通過 ✅' if not fails else f'\n有 {len(fails)} 項失敗：{fails}')
sys.exit(1 if fails else 0)
