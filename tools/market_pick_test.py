# 菜市場專用測試：地圖、三個攤位、斤數、殺價每個選項、三次太低「不賣了」、錢不夠、加買／改項目、結局好壞與說明、3000 局總價
# 用法：NPM=<有 pinyin-pro 和 opencc-js 的 node_modules> [SHOTS=<截圖資料夾>] python3 tools/market_pick_test.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smoke
from smoke import PORT, route, sync_playwright

fails = []
STEPS = []
def check(name, ok, info=''):
    print(('✓ ' if ok else '✗ ') + name + (('  ' + str(info)) if (info != '' and not ok) else ''))
    if not ok: fails.append(name)

def ev(page, js, arg=None): return page.evaluate(js, arg) if arg is not None else page.evaluate(js)
def plain(page, sel):
    return page.evaluate("s=>{const c=document.querySelector(s).cloneNode(true);c.querySelectorAll('rt').forEach(r=>r.remove());return c.innerText.replace(/\\n/g,'')}", sel)
def opts(page):
    return page.evaluate("[...document.querySelectorAll('#options-area .opt')].map(b=>{const c=b.cloneNode(true);c.querySelectorAll('rt').forEach(r=>r.remove());return c.innerText.replace(/\\n/g,'')})")
def state(page): return ev(page, 'Game.state')
def tap(page, text):
    STEPS.append((text, state(page))); page.evaluate('t=>window.__last=t', text)
    """按下方選項（文字開頭符合）；遇到過場畫面自動按掉"""
    o = opts(page); i = next((k for k, t in enumerate(o) if t.startswith(text)), None)
    assert i is not None, (text, o, state(page))
    page.locator('#options-area .opt').nth(i).click(); page.wait_for_timeout(80)
    n = 0
    while state(page) == '_TRANS':
        n += 1; page.locator('#options-area .opt').first.click(); page.wait_for_timeout(80)
    return n      # 中間按掉幾個過場畫面
def new_game(page):
    page.goto(f'http://127.0.0.1:{PORT}/games/market/index.html'); page.wait_for_timeout(400)
    page.fill('#player-name-input', 'María'); page.click('.btn-primary'); page.wait_for_timeout(300)
    tap(page, '走進菜市場'); assert state(page) == 'MAP', state(page)
def setreq(page, items, msg=None):
    """指定這局 Ami 要的東西：items = [[id, q], …]"""
    page.evaluate("([it,msg])=>{const t=Game.task;t.items=it.map(([id,q])=>({...BYID[id],q}));t.msg=msg?{type:msg.type,y:{...BYID[msg.y[0]],q:msg.y[1]},xid:msg.x||null}:null;t.total=0;Game.req=it.map(([id,q])=>({id,q}));Game.checkDone=true;}", [items, msg])
def buy(page, item, q):
    """在攤位上買一樣：按斤賣的先點圖片再選斤數"""
    it = ev(page, f"BYID['{item}'].jin")
    if it:
        page.locator(f'[data-jin="{item}"]').click(); page.locator('.amt .amtb').nth([0.5, 1, 2].index(q) if ev(page, f"BYID['{item}'].qs.length")==3 else ev(page, f"BYID['{item}'].qs.indexOf({q})")).click()
    else:
        for _ in range(int(q)): page.locator(f'[data-veg="{item}"]').click()
    page.wait_for_timeout(50)
def shot(page, name):
    d = os.environ.get('SHOTS')
    if d: os.makedirs(d, exist_ok=True); page.screenshot(path=f'{d}/{name}.png')

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1000, 'height': 900}); ctx.route('**/*', route)
    page = ctx.new_page(); errs = []; page.on('pageerror', lambda e: errs.append(str(e)[:60] + ' after=' + str(STEPS[-1:])))
    page.add_init_script("window.addEventListener('error',e=>{(window.__es=window.__es||[]).push(Game.state+'|'+JSON.stringify(Game.st&&1)+'|'+(window.__last||''))})")
    new_game(page)

    # 0. 3000 局：總價（含加買）≤900、至少 2 個攤位、4 樣不重複、17 種都出現、改項目的 X 在清單上
    r = ev(page, """()=>{const seen=new Set();let bad=[],msgs=0,adds=0,chg=0;
      for(let i=0;i<3000;i++){Game.setup();const t=Game.task,tot=t.items.reduce((a,it)=>a+cost(it,it.q),0);
        t.items.forEach(it=>seen.add(it.id));
        const stalls=new Set(t.items.map(it=>it.stall)).size, ids=new Set(t.items.map(it=>it.id)).size;
        let all=tot; if(t.msg){msgs++; all+=cost(t.msg.y,t.msg.y.q); if(t.msg.type==='add')adds++; else {chg++; if(!t.items.some(it=>it.id===t.msg.xid))bad.push('x');} if(t.items.some(it=>it.id===t.msg.y.id))bad.push('dupY');}
        if(all>TOTAL_MAX)bad.push('total'+all); if(stalls<2)bad.push('stalls'); if(t.items.length!==4||ids!==4)bad.push('dup');}
      return {seen:seen.size,bad,msgs,adds,chg};}""")
    check('3000 局：17 種都出現', r['seen'] == 17, r)
    check('3000 局：總價≤900、≥2 攤、4 樣不重複', r['bad'] == [], r['bad'][:5])
    check('約一半的局有 Ami 訊息（加買和改項目都有）', 1200 < r['msgs'] < 1800 and r['adds'] > 300 and r['chg'] > 300, r)

    # 1. 地圖
    new_game(page)
    setreq(page, [['pork', 1], ['fish', 1], ['cabbage', 1], ['egg', 1]])
    check('地圖有三個攤位 + 回家', plain(page, '.stalls').count('攤') == 3 and opts(page) == ['去肉攤', '去魚攤', '去菜攤', '東西買好了，回家'], opts(page))
    shot(page, 'map')

    # 2. 肉攤：6 張卡、5 張要選斤數
    tap(page, '去肉攤')
    check('肉攤 6 張卡', page.locator('.shelf .bun').count() == 6)
    check('肉攤 5 張按斤賣、1 張雞腿', page.locator('.shelf [data-jin]').count() == 5 and page.locator('.shelf [data-veg]').count() == 1)
    check('肉攤沒有魚和菜', not any(w in plain(page, '.shelf') for w in ['高麗菜', '蝦', '魚']))
    page.locator('[data-jin="pork"]').click()
    check('點豬肉出現 半斤／一斤 選擇', page.locator('.amt .amtb').count() == 2 or page.locator('.amt .amtb').count() == 3, page.locator('.amt .amtb').count())
    page.locator('.amt .amtx').click()
    check('✕ 收起斤數', page.locator('.amt').count() == 0)
    page.locator('[data-veg="leg"]').click(); page.locator('[data-veg="leg"]').click()
    check('雞腿點兩下＝2', ev(page, 'Game.cart.leg') == 2)
    page.locator('[data-adj="leg"][data-d="-1"]').click()
    check('－ → 1', ev(page, 'Game.cart.leg') == 1)
    page.locator('[data-adj="leg"][data-d="-1"]').click()
    check('－ 到 0 整列消失', ev(page, 'Object.keys(Game.cart).length') == 0)
    buy(page, 'pork', 1)
    check('豬肉一斤＝300', ev(page, 'Game.cartTotal()') == 300)
    shot(page, 'pick_meat')
    tap(page, '先不買了')
    check('離開攤位回地圖、籃子清空', state(page) == 'MAP' and ev(page, 'Object.keys(Game.cart).length') == 0)
    tap(page, '去魚攤')
    check('魚攤 5 張卡（蝦、蛤蜊要斤數）', page.locator('.shelf .bun').count() == 5 and page.locator('.shelf [data-jin]').count() == 2)
    tap(page, '先不買了'); tap(page, '去菜攤')
    check('菜攤 6 張一般卡', page.locator('.shelf [data-veg]').count() == 6 and page.locator('.shelf [data-jin]').count() == 0)
    tap(page, '買好了')
    check('籃子空的按「買好了」→ 回地圖', state(page) == 'MAP')

    # 3. 殺價每個選項（肉攤，豬肉一斤）
    check('購物清單沒有表情符號', not any(ch in plain(page, '.list') for ch in '🥩🍖🍗🐟🦐🦑🐚🦀🥬🌿🍅🌽🧅🥚') if page.locator('.list').count() else True)
    n = tap(page, '去肉攤')
    check('進肉攤直接是挑菜畫面（沒有多一個過場）', state(page) == 'PICK' and n == 0, (state(page), n))
    buy(page, 'pork', 1)
    n = tap(page, '買好了')
    check('按「買好了」直接進殺價（沒有多一個過場）', state(page) == 'HAGGLE' and n == 0, (state(page), n))
    check('老闆複誦和報價是同一句', plain(page, '#npc-dialogue').count('老闆：') == 1 and '一共是' in plain(page, '#npc-dialogue') and '你要的是' in plain(page, '#npc-dialogue'), plain(page, '#npc-dialogue'))
    check('進入殺價、報價 300', state(page) == 'HAGGLE' and ev(page, 'Game.st.ask') == 300)
    o = opts(page)
    check('殺價選項：算便宜一點、三個出價、再看看、我買了', o[0].startswith('老闆，算便宜') and sum(1 for t in o if t.endswith('元可以嗎？')) == 3 and any(t.startswith('我再看看') for t in o) and o[-1] == '好，300元，我買了。', o)
    shot(page, 'haggle')
    ev(page, 'Game.st.floor = 200')
    tap(page, '老闆，算便宜')
    check('「算便宜一點」降價且只能用一次', ev(page, 'Game.st.ask') < 300 and not any(t.startswith('老闆，算便宜') for t in opts(page)), opts(page))
    ask = ev(page, 'Game.st.ask')
    ev(page, 'Math.random = () => 0.9')       # 「再看看」會降價
    tap(page, '我再看看')
    check('「我再看看」老闆叫住你、降價', ev(page, 'Game.st.ask') <= ask, (ask, ev(page, 'Game.st.ask')))
    check('「我再看看」只能用一次', not any(t.startswith('我再看看') for t in opts(page)))
    ev(page, 'Game.st.floor = Math.round(Game.st.ask*0.8/10)*10')
    flo = ev(page, 'Game.st.floor'); ask = ev(page, 'Game.st.ask'); m0 = ev(page, 'Game.mistakes')
    o = [t for t in opts(page) if t.endswith('元可以嗎？')]
    check('出價選項都比現在的價錢低', all(int(t.split('元')[0]) < ask for t in o), (o, ask))
    # 出價在底價 80%~100% → 還價，不扣分
    ev(page, 'Game.st.floor = Game.st.ask - 10')
    lo = ev(page, 'Game.st.floor')
    tap(page, '好，')  # 付錢
    check('「我買了」進入付錢', state(page) == 'PAY' and m0 == ev(page, 'Game.mistakes'))
    # 錢夠、亂說錢不夠 → 錯
    tap(page, SHORT := '不好意思，我的錢不夠')
    check('錢夠卻說不夠 → 扣分', ev(page, 'Game.mistakes') == m0 + 1 and state(page) == 'PAY')
    tap(page, '我下次再付')
    check('賒帳 → 扣分', ev(page, 'Game.mistakes') == m0 + 2)
    pay = [t for t in opts(page) if t.startswith('給你') ]
    check('肉攤付錢畫面用肉攤的圖', 'stall_meat' in ev(page, "document.getElementById('npc-avatar').src"))
    P = ev(page, 'Game.payInfo()')
    tap(page, P['payOk'])
    check('付錢後現金減少', ev(page, 'Game.cash') == 1000 - P['ask'], ev(page, 'Game.cash'))
    check('買到的豬肉記進 bought', ev(page, 'Game.bought.pork') == 1)
    # 找錢、袋子、核對
    while state(page) in ('CHANGE', 'BAG', 'CHECK'):
        st = state(page)
        if st == 'CHANGE':
            shot(page, 'change')
            cc = ev(page, 'Game.cc'); right = '老闆，好像找錯了' if cc['sc'] else '好，謝謝'
            wrong = '好，謝謝' if cc['sc'] else '老闆，好像找錯了'
            mm = ev(page, 'Game.mistakes'); tap(page, wrong); check('找錢：錯的選項扣分', ev(page, 'Game.mistakes') == mm + 1)
            tap(page, right)
        elif st == 'BAG':
            mm = ev(page, 'Game.mistakes'); tap(page, '要，給我五個'); check('塑膠袋：要塑膠袋扣分', ev(page, 'Game.mistakes') == mm + 1)
            check('塑膠袋說明統一', '環保袋' in ev(page, 'Game.log[Game.log.length-1].zh') and '不用再拿塑膠袋' in ev(page, 'Game.log[Game.log.length-1].zh'), ev(page, 'Game.log[Game.log.length-1].zh'))
            tap(page, '不用，我有環保袋')
        else: tap(page, '好，謝謝')
    check('付完一攤回到地圖，這攤打勾', state(page) == 'MAP' and ev(page, 'Game.visited.meat') is True)

    # 4. 殺過頭：三次太低 → 不賣了
    tap(page, '去魚攤'); buy(page, 'fish', 1); tap(page, '買好了')
    ev(page, 'Game.st.floor = 70')
    m1 = ev(page, 'Game.mistakes')
    lowest = lambda: [t for t in opts(page) if t.endswith('元可以嗎？')][0]
    tap(page, lowest()); check('第一次太低：警告、心情 2、不扣分', ev(page, 'Game.st.mood') == 2 and ev(page, 'Game.mistakes') == m1)
    tap(page, lowest()); check('第二次太低：心情 1、不扣分', ev(page, 'Game.st.mood') == 1 and ev(page, 'Game.mistakes') == m1)
    check('警告話提到虧本／不賣', ev(page, 'Game.thought') is not None)
    tap(page, lowest())
    check('第三次太低：老闆不賣了 → 回地圖、扣分 1 次', state(page) == 'MAP' and ev(page, 'Game.mistakes') == m1 + 1, (state(page), ev(page, 'Game.mistakes')))
    check('魚攤收攤、記錄「老闆不賣」', ev(page, 'Game.closed.fish') is True and ev(page, 'Game.lack.fish') == 'refused', ev(page, 'Game.lack'))
    check('地圖上魚攤不能再進去', '去魚攤' not in opts(page) and '收攤' in plain(page, '.stalls'), opts(page))
    shot(page, 'map_closed')

    # 5. 錢不夠：現金設成 50，菜攤買 高麗菜(60)＋雞蛋(55)
    tap(page, '去菜攤'); buy(page, 'cabbage', 1); buy(page, 'egg', 1); tap(page, '買好了')
    ev(page, 'Game.cash = 50'); tap(page, '好，')
    P = ev(page, 'Game.payInfo()')
    check('現金不足 → 付錢關', state(page) == 'PAY' and P['short'], P)
    mm = ev(page, 'Game.mistakes'); tap(page, P['payOk'])
    check('錢不夠硬付 → 扣分', ev(page, 'Game.mistakes') == mm + 1)
    shot(page, 'pay_short')
    tap(page, SHORT)
    check('說「錢不夠」→ 進入選要拿掉哪樣', state(page) == 'REMOVE' and opts(page) == ['高麗菜不要了。', '雞蛋不要了。'] or set(opts(page)) == {'高麗菜不要了。', '雞蛋不要了。'}, opts(page))
    ev(page, 'Game.cash = 100')   # 拿掉雞蛋後 60 元要付得起
    tap(page, '雞蛋不要了')
    check('拿掉雞蛋 → 重新報價、記錄錢不夠', state(page) == 'PAY' and ev(page, 'Game.lack.egg') == 'money' and 'egg' not in ev(page, 'Game.cart'), ev(page, 'Game.st'))
    P = ev(page, 'Game.payInfo()'); tap(page, P['payOk'])
    while state(page) in ('CHANGE', 'BAG', 'CHECK'):
        st = state(page)
        if st == 'CHANGE':
            cc = ev(page, 'Game.cc'); tap(page, '老闆，好像找錯了' if cc['sc'] else '好，謝謝')
        elif st == 'BAG': tap(page, '不用，我有環保袋')
        else: tap(page, '好，謝謝')
    # 6. 回家 → 說明原因（魚：老闆不賣；蛋：錢不夠；豬肉在肉攤買了）
    tap(page, '東西買好了，回家')
    check('回家 → 問少買的原因', state(page) == 'EXPLAIN' and len(opts(page)) == 3, (state(page), opts(page)))
    shot(page, 'explain')
    q = ev(page, 'Game.queue.map(a=>a.id)')
    check('少買兩樣（魚、雞蛋）都要問', set(q) == {'fish', 'egg'}, q)
    lines = []
    for _ in range(2):
        a = ev(page, 'Game.queue[Game.qi].id'); real = ev(page, 'Game.causeOf(Game.queue[Game.qi].id)')
        want = {'money': '我的錢不夠', 'refused': '老闆不賣給我', 'forgot': '對不起，我忘記了'}
        wrong = '對不起，我忘記了' if real != 'forgot' else '我的錢不夠'
        mm = ev(page, 'Game.mistakes'); tap(page, wrong)
        check(f'{a}：選錯原因 → 扣分、留在原題', ev(page, 'Game.mistakes') == mm + 1 and state(page) == 'EXPLAIN')
        tap(page, want[real])
        lines.append(real)
    check('原因記錄：魚＝老闆不賣、蛋＝錢不夠', sorted(lines) == ['money', 'refused'], lines)
    check('進入結局', state(page) == 'END')
    sc = ev(page, 'Game.score'); mk = ev(page, 'Game.mistakes')
    check('少買但原因正確 → 壞結局（只有好壞兩種）', ev(page, 'Game._endGood') is False)
    check('結局句子包含體諒', any('下次' in l for l in ev(page, 'Game.final.map(x=>x.zh)')), ev(page, 'Game.final.map(x=>x.zh)'))
    check('輕扣的兩筆記錄是 −5（錯誤紀錄與回饋卡都顯示 −5）', ev(page, 'Game.log.filter(m=>m.pen===5).length') == 2 and '−5' in ev(page, "document.getElementById('log-body').innerText"), ev(page, 'Game.log.map(m=>m.pen)'))
    check('分數：輕扣只扣 5', ev(page, 'Game.score') == 100 - 10 * (ev(page, 'Game.mistakes') - 2) - 10 + ev(page, 'Game._bonus') , (ev(page, 'Game.score'), ev(page, 'Game.mistakes')))
    shot(page, 'end_bad')
    tap(page, '查看結果'); check('結果頁', state(page) == 'RESULT')

    # 7. 好結局：照 Ami 的買，沒有錯
    new_game(page)
    setreq(page, [['rib', 0.5], ['squid', 1], ['onion', 2], ['egg', 1]])
    for stall, items in [('肉', [('rib', 0.5)]), ('魚', [('squid', 1)]), ('菜', [('onion', 2), ('egg', 1)])]:
        tap(page, f'去{stall}攤')
        for i, q in items: buy(page, i, q)
        tap(page, '買好了'); tap(page, '好，')
        P = ev(page, 'Game.payInfo()'); tap(page, P['payOk'])
        while state(page) in ('CHANGE', 'BAG', 'CHECK'):
            st = state(page)
            if st == 'CHANGE':
                cc = ev(page, 'Game.cc'); tap(page, '老闆，好像找錯了' if cc['sc'] else '好，謝謝')
            elif st == 'BAG': tap(page, '不用，我有環保袋')
            else:
                ck = ev(page, 'Game.ck'); it = ev(page, 'BYID[Game.ck.id]'); tap(page, '好，謝謝')
    check('全買對 → 回到地圖，可以回家', state(page) == 'MAP' or state(page) == 'MSG')
    if state(page) == 'MSG': tap(page, '好，謝謝')
    tap(page, '東西買好了，回家')
    check('全對 → 好結局、沒有扣分', state(page) == 'END' and ev(page, 'Game._endGood') is True and ev(page, 'Game.mistakes') == 0, (state(page), ev(page, 'Game.mistakes')))
    shot(page, 'end_good')

    # 8. Ami 訊息：加買
    new_game(page)
    setreq(page, [['pork', 1], ['mince', 1], ['leg', 1], ['rib', 1]], {'type': 'add', 'y': ['onion', 2]})
    tap(page, '去肉攤')
    for i, q in [('pork', 1), ('mince', 1), ('leg', 1), ('rib', 1)]: buy(page, i, q)
    tap(page, '買好了'); tap(page, '好，'); P = ev(page, 'Game.payInfo()'); tap(page, P['payOk'])
    while state(page) in ('CHANGE', 'BAG', 'CHECK', 'MSG'):
        st = state(page)
        if st == 'CHANGE':
            cc = ev(page, 'Game.cc'); tap(page, '老闆，好像找錯了' if cc['sc'] else '好，謝謝')
        elif st == 'BAG': tap(page, '不用，我有環保袋')
        elif st == 'MSG':
            shot(page, 'msg_add'); tap(page, '好，我知道了')
        else: tap(page, '好，謝謝')
    check('Ami 加買訊息出現在第一攤之後、清單多一樣', state(page) == 'MAP' and ev(page, 'Game.req.length') == 5 and ev(page, 'Game.msgShown'), (state(page), ev(page, 'Game.req')))
    tap(page, '東西買好了，回家')
    check('加買沒買 → 問原因（忘記）', state(page) == 'EXPLAIN' and ev(page, 'Game.causeOf(Game.queue[0].id)') == 'forgot')
    tap(page, '我的錢不夠'); check('忘記卻說錢不夠 → 扣分', ev(page, 'Game.mistakes') == 1)
    tap(page, '對不起，我忘記了')
    check('忘記 → 壞結局、重扣（不是輕扣）', state(page) == 'END' and ev(page, 'Game._endGood') is False and ev(page, 'Game.score') == 100 - 10 - 10, ev(page, 'Game.score'))

    # 9. Ami 訊息：改項目（X 已經買了）→ 三個選項
    new_game(page)
    setreq(page, [['pork', 1], ['fish', 1], ['cabbage', 1], ['egg', 1]], {'type': 'change', 'x': 'pork', 'y': ['beef', 1]})
    tap(page, '去肉攤'); buy(page, 'pork', 1); tap(page, '買好了'); tap(page, '好，'); P = ev(page, 'Game.payInfo()'); tap(page, P['payOk'])
    while state(page) in ('CHANGE', 'BAG', 'CHECK'):
        st = state(page)
        if st == 'CHANGE':
            cc = ev(page, 'Game.cc'); tap(page, '老闆，好像找錯了' if cc['sc'] else '好，謝謝')
        elif st == 'BAG': tap(page, '不用，我有環保袋')
        else: tap(page, '好，謝謝')
    check('改項目、豬肉已買 → 出現三個選項', state(page) == 'MSG' and len(opts(page)) == 3 and any(t.startswith('Ami，一斤豬肉我已經買了') for t in opts(page)), opts(page))
    check('沒有「退貨」字樣', not any('退' in t for t in opts(page)))
    shot(page, 'msg_change')
    mm = ev(page, 'Game.mistakes'); tap(page, '好，我再去買'); check('「我再去買」→ 扣分、說明已買好', ev(page, 'Game.mistakes') == mm + 1 and '已經買好' in ev(page, 'Game.log[Game.log.length-1].zh'))
    tap(page, 'Ami，你自己來買'); check('「你自己來買」→ 扣分（不禮貌）', ev(page, 'Game.mistakes') == mm + 2)
    tap(page, 'Ami，一斤豬肉我已經買了')
    check('正確選項 → 回地圖、需求仍是豬肉', state(page) == 'MAP' and ev(page, "Game.req.some(a=>a.id==='pork')") and not ev(page, "Game.req.some(a=>a.id==='beef')"))

    # 10. Ami 訊息：改項目（X 還沒買）→ 清單換成 Y
    new_game(page)
    setreq(page, [['pork', 1], ['fish', 1], ['cabbage', 1], ['egg', 1]], {'type': 'change', 'x': 'egg', 'y': ['onion', 3]})
    tap(page, '去肉攤'); buy(page, 'pork', 1); tap(page, '買好了'); tap(page, '好，'); P = ev(page, 'Game.payInfo()'); tap(page, P['payOk'])
    while state(page) in ('CHANGE', 'BAG', 'CHECK'):
        st = state(page)
        if st == 'CHANGE':
            cc = ev(page, 'Game.cc'); tap(page, '老闆，好像找錯了' if cc['sc'] else '好，謝謝')
        elif st == 'BAG': tap(page, '不用，我有環保袋')
        else: tap(page, '好，謝謝')
    check('X 還沒買 → 只有一個「知道了」選項', state(page) == 'MSG' and opts(page) == ['好，我知道了。'], opts(page))
    tap(page, '好，我知道了')
    check('雞蛋換成洋蔥', ev(page, "Game.req.some(a=>a.id==='onion')") and not ev(page, "Game.req.some(a=>a.id==='egg')"))

    # 4b. 肉攤被「不賣了」：過場畫面用生氣圖
    new_game(page); setreq(page, [['pork', 1], ['fish', 1], ['cabbage', 1], ['egg', 1]])
    tap(page, '去肉攤'); buy(page, 'pork', 1); tap(page, '買好了'); ev(page, 'Game.st.floor = 280')
    for _ in range(3):
        o = opts(page); i = next(k for k, t_ in enumerate(o) if t_.endswith('元可以嗎？'))
        page.locator('#options-area .opt').nth(i).click(); page.wait_for_timeout(120)
    check('肉攤不賣了：過場畫面是老闆生氣圖', state(page) == '_TRANS' and 'stall_meat_angry' in ev(page, "document.getElementById('npc-avatar').src"), (state(page), ev(page, "document.getElementById('npc-avatar').src")))
    page.locator('#options-area .opt').first.click(); page.wait_for_timeout(100)
    check('離開過場後回地圖，圖片恢復', state(page) == 'MAP' and 'angry' not in ev(page, "document.getElementById('npc-avatar').src"))
    new_game(page); setreq(page, [['pork', 1], ['fish', 1], ['cabbage', 1], ['egg', 1]])
    tap(page, '去魚攤'); buy(page, 'fish', 1); tap(page, '買好了')
    for _ in range(3):
        o = opts(page); i = next(k for k, t_ in enumerate(o) if t_.endswith('元可以嗎？'))
        page.locator('#options-area .opt').nth(i).click(); page.wait_for_timeout(120)
    check('魚攤不賣了：過場畫面是老闆娘生氣圖', state(page) == '_TRANS' and 'stall_fish_angry' in ev(page, "document.getElementById('npc-avatar').src"))
    page.locator('#options-area .opt').first.click(); page.wait_for_timeout(100)

    # 11. 外觀：手機版找錢卡、地圖、殺價
    page.set_viewport_size({'width': 390, 'height': 800})
    new_game(page); setreq(page, [['pork', 1], ['fish', 1], ['cabbage', 1], ['egg', 1]]); shot(page, 'mobile_map')
    tap(page, '去肉攤'); shot(page, 'mobile_pick'); buy(page, 'pork', 1); tap(page, '買好了'); shot(page, 'mobile_haggle')
    ev(page, "Game.st=null; Game.cc={bill:500,ask:270,want:230,given:230,sc:false}; Game.state='CHANGE'; Game.render()")
    shot(page, 'mobile_change')
    w = ev(page, "document.querySelector('.cashcard').getBoundingClientRect().height")
    check('找錢卡高度正常（不是直排被擠）', w < 110, w)
    check('沒有 JS 錯誤', errs == [], (errs[:1], ev(page,'window.__es'), STEPS[-3:]))
    b.close()
print('\n失敗：', fails) if fails else print('\n全部通過')
sys.exit(1 if fails else 0)
