# 菜市場專用測試：地圖、三個攤位、斤數、殺價每個選項、三次太低「不賣了」、錢不夠、加買／改項目、結局好壞與說明、3000 局總價
# 用法：NPM=<有 pinyin-pro 和 opencc-js 的 node_modules> [SHOTS=<截圖資料夾>] python3 tools/market_pick_test.py（約 5 分鐘）
# 最後一段 run_options：每一關的每個選項（對的、錯的）都指定情境按一遍（約 460 項檢查）
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
    """畫面上看得到的選項文字：下方按鈕＋彈跳視窗裡的按鈕"""
    return page.evaluate("[...document.querySelectorAll('#options-area .opt, #msg-pop .opt')].filter(b=>b.offsetParent!==null).map(b=>{const c=b.cloneNode(true);c.querySelectorAll('rt').forEach(r=>r.remove());return c.innerText.replace(/\\n/g,'')})")
def state(page): return ev(page, 'Game.state')
def tap(page, text):
    """按選項（文字開頭符合；「老闆，」在老闆娘的攤位自動換成「老闆娘，」）；地圖上的攤位直接點圖示；遇到過場畫面自動按掉"""
    o = opts(page)
    if not any(t.startswith(text) for t in o) and text.startswith('老闆，'): text = '老闆娘，' + text[3:]
    i = next((k for k, t in enumerate(o) if t.startswith(text)), None)
    STEPS.append((text, state(page))); page.evaluate('t=>window.__last=t', text)
    if i is not None:
        page.locator('#options-area .opt:visible, #msg-pop .opt:visible').nth(i).click()
    else:
        ds = page.evaluate("[...document.querySelectorAll('[data-choice]')].filter(e=>e.offsetParent!==null).map(e=>e.dataset.choice)")
        j = next((k for k, t in enumerate(ds) if t.startswith(text)), None)
        assert j is not None, (text, o, ds, state(page))
        page.locator('[data-choice]:visible').nth(j).click()
    page.wait_for_timeout(80)
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
def pay_through(page):
    """殺價畫面直接成交 → 付錢 → 找錢／袋子／核對（全按對的）"""
    tap(page, '好，'); P = ev(page, 'Game.payInfo()'); tap(page, P['payOk'])
    while state(page) in ('CHANGE', 'BAG', 'CHECK'):
        st = state(page)
        if st == 'CHANGE':
            cc = ev(page, 'Game.cc'); tap(page, '老闆，好像找錯了' if cc['sc'] else '好，謝謝')
        elif st == 'BAG': tap(page, '不用，我有環保袋')
        else:
            ck = ev(page, 'Game.ck'); it = ev(page, 'BYID[Game.ck.id]')
            tap(page, '好，謝謝' if not ck['wrong'] else '老闆，' + it['zh'] + '我要的是')
def shot(page, name):
    d = os.environ.get('SHOTS')
    if d: os.makedirs(d, exist_ok=True); page.screenshot(path=f'{d}/{name}.png')

COUNT = {}
def chk(group, name, ok, info=''):
    COUNT[group] = COUNT.get(group, 0) + 1
    if not ok:
        print('✗ [%s] %s  %s' % (group, name, info)); fails.append('[%s] %s' % (group, name))
def click_i(page, i):
    page.locator('#options-area .opt:visible, #msg-pop .opt:visible').nth(i).click(); page.wait_for_timeout(40)
    while state(page) == '_TRANS':
        page.locator('#options-area .opt').first.click(); page.wait_for_timeout(40)
def card(page):
    """最近一次的回饋卡／錯誤說明文字（錯誤紀錄最後一筆）"""
    return ev(page, "(Game.log[Game.log.length-1]||{}).zh || ''")
def snap(page): return ev(page, '({m: Game.mistakes, s: Game.state, cash: Game.cash, cart: {...Game.cart}, lack: {...Game.lack}})')

def reset(page, req, msg=None):
    ev(page, """()=>{ window.__rnd = window.__rnd || Math.random; Math.random = window.__rnd;
      Game.setup(); Object.assign(Game, {mistakes: 0, score: 100, mistakeLog: [], log: [], att: {}, feedback: [], thought: null, thoughtFirst: false, visit: 0, explained: {}, queue: [], qi: 0, tx: [], cc: null, ck: null}); Game.closeMsgPop(); }""")
    ev(page, "([it,msg])=>{const t=Game.task;t.items=it.map(([id,q])=>({...BYID[id],q}));t.msg=msg?{type:msg.type,y:{...BYID[msg.y[0]],q:msg.y[1]},xid:msg.x||null}:null;t.total=0;t.rot=0;Game.req=it.map(([id,q])=>({id,q}));Game.checkDone=true;Game.bagDone=true;}", [req, msg])
def go(page, js):
    ev(page, "()=>{" + js + "; Game.updateCash(); Game.render();}"); page.wait_for_timeout(30)
def haggle_at(page, cur, cart, floor=None, cash=1000):
    """放到殺價前：在 cur 攤位，籃子是 cart，報價＝合計"""
    go(page, f"Game.cur='{cur}'; Game.cart={cart}; Game.startHaggle(); Game.cash={cash}; " + (f"Game.st.floor={floor}; " if floor else '') + "Game.thought=null; Game.state='HAGGLE'")
def pay_at(page, cur, cart, cash=1000):
    haggle_at(page, cur, cart, None, cash); go(page, "Game.state='PAY'")

def each(page, group, setup, judge, expect_n=None):
    """setup(page) 把遊戲放到這一關；每個選項各按一次（每次重來），judge(text, before, after, ctx) 回傳 (對不對, 說明)"""
    setup(page); o = opts(page)
    if expect_n is not None: chk(group, '選項數量', len(o) == expect_n, o)
    chk(group, '選項不重複', len(set(o)) == len(o), o)
    for i, t in enumerate(o):
        setup(page); ctx = ev(page, 'Game.payInfo ? (Game.st ? Game.payInfo() : null) : null') if state(page) == 'PAY' else None
        b = snap(page); click_i(page, i); a = snap(page)
        ok, why = judge(t, b, a, ctx)
        chk(group, f'「{t}」', ok, f'{why} before={b["m"]},{b["s"]} after={a["m"]},{a["s"]}')

W = lambda b, a: a['m'] == b['m'] + 1 and a['s'] == b['s']      # 選錯：扣一次分、留在原地
R = lambda b, a: a['m'] == b['m'] and a['s'] != b['s']          # 選對：沒扣分、往下走



def run_options(page):
    """每一關的每個選項（對的、錯的）都指定情境按一遍"""
    # ═══ MAP：三個攤位＋回家 ═══
    for k, zh in (('meat', '肉攤'), ('fish', '魚攤'), ('veg', '菜攤')):
        reset(page, [['pork', 1], ['fish', 1], ['egg', 1], ['onion', 2]]); go(page, "Game.state='MAP'")
        page.locator(f'button.stall[data-choice="去{zh}"]').click(); page.wait_for_timeout(60)
        chk('MAP', f'去{zh} → 進 PICK', state(page) == 'PICK' and ev(page, 'Game.cur') == k, (state(page), ev(page, 'Game.cur')))
    reset(page, [['pork', 1]]); go(page, "Game.state='MAP'")
    page.locator('#options-area .opt').first.click(); page.wait_for_timeout(60)
    chk('MAP', '回家（還有沒買的）→ 問原因', state(page) == 'EXPLAIN', state(page))
    reset(page, [['pork', 1]]); go(page, "Game.bought={pork:1}; Game.state='MAP'")
    page.locator('#options-area .opt').first.click(); page.wait_for_timeout(60)
    chk('MAP', '回家（都買對了）→ 好結局', state(page) == 'END' and ev(page, 'Game._endGood') is True, state(page))
    reset(page, [['pork', 1]]); go(page, "Game.closed={fish:true}; Game.state='MAP'")
    chk('MAP', '收攤的魚攤不能點', page.locator('button.stall[data-choice="去魚攤"]').count() == 0 and page.locator('button.stall[data-choice="去肉攤"]').count() == 1)

    # ═══ PICK：17 種菜、每個數量、＋／－、✕、買好了、先不買了 ═══
    for k in ('meat', 'fish', 'veg'):
        for it in [x for x in ev(page, 'ITEMS') if x['stall'] == k]:
            reset(page, [['pork', 1]]); go(page, f"Game.cur='{k}'; Game.cart={{}}; Game.state='PICK'")
            id_ = it['id']
            if it.get('jin'):
                for q in (0.5, 1, 2):
                    page.locator(f'[data-jin="{id_}"]').click(); page.wait_for_timeout(30)
                    chk('PICK', f'{it["zh"]}：點圖片出現斤數選擇', page.locator('.amt .amtb').count() == 3, page.locator('.amt .amtb').count())
                    page.locator('.amt .amtb').nth([0.5, 1, 2].index(q)).click(); page.wait_for_timeout(30)
                    chk('PICK', f'{it["zh"]}：選{q}斤 → 籃子裡是{q}', ev(page, f"Game.cart['{id_}']") == q, ev(page, 'Game.cart'))
                page.locator(f'[data-jin="{id_}"]').click(); page.wait_for_timeout(30); page.locator('.amt .amtx').click(); page.wait_for_timeout(30)
                chk('PICK', f'{it["zh"]}：✕ 收起斤數', page.locator('.amt').count() == 0)
                page.locator(f'[data-adj="{id_}"][data-d="-1"]').click(); page.wait_for_timeout(30)
                chk('PICK', f'{it["zh"]}：－ 整份放回去', ev(page, f"'{id_}' in Game.cart") is False)
            else:
                for n in (1, 2, 3):
                    page.locator(f'[data-veg="{id_}"]').click(); page.wait_for_timeout(30)
                    chk('PICK', f'{it["zh"]}：點第{n}下 → {n}', ev(page, f"Game.cart['{id_}']") == n, ev(page, 'Game.cart'))
                page.locator(f'[data-adj="{id_}"][data-d="1"]').click(); page.wait_for_timeout(30)
                chk('PICK', f'{it["zh"]}：＋ → 4', ev(page, f"Game.cart['{id_}']") == 4, ev(page, 'Game.cart'))
                for n in (3, 2, 1):
                    page.locator(f'[data-adj="{id_}"][data-d="-1"]').click(); page.wait_for_timeout(30)
                    chk('PICK', f'{it["zh"]}：－ → {n}', ev(page, f"Game.cart['{id_}']") == n, ev(page, 'Game.cart'))
                page.locator(f'[data-adj="{id_}"][data-d="-1"]').click(); page.wait_for_timeout(30)
                chk('PICK', f'{it["zh"]}：－ 到 0 整列消失', ev(page, f"'{id_}' in Game.cart") is False)
        # 買好了／先不買了
        reset(page, [['pork', 1]]); go(page, f"Game.cur='{k}'; Game.cart={{}}; Game.state='PICK'")
        o = opts(page); chk('PICK', f'{k}：兩個下方選項', len(o) == 2 and o[0].startswith('買好了') and o[1].startswith('先不買了'), o)
        click_i(page, 0); chk('PICK', f'{k}：籃子空的按買好了 → 回地圖', state(page) == 'MAP' and ev(page, 'Game.mistakes') == 0, state(page))
        go(page, f"Game.cur='{k}'; Game.cart={{}}; Game.state='PICK'")
        click_i(page, 1); chk('PICK', f'{k}：先不買了 → 回地圖', state(page) == 'MAP' and ev(page, 'Game.mistakes') == 0)
        it0 = [x for x in ev(page, 'ITEMS') if x['stall'] == k][-1]['id']
        go(page, f"Game.cur='{k}'; Game.cart={{{it0}:1}}; Game.state='PICK'".replace(f'{{{it0}:1}}', "{'%s':1}" % it0))
        click_i(page, 0); chk('PICK', f'{k}：有東西按買好了 → 殺價', state(page) == 'HAGGLE' and ev(page, 'Game.st.ask') > 0, state(page))
        go(page, f"Game.cur='{k}'; Game.cart={{'{it0}':1}}; Game.state='PICK'")
        click_i(page, 1); chk('PICK', f'{k}：有東西按先不買了 → 回地圖、籃子清空', state(page) == 'MAP' and ev(page, 'Object.keys(Game.cart).length') == 0)

    # ═══ HAGGLE：算便宜、三種出價（三種結果）、再看看（三種結果）、成交 ═══
    def hg(floor, ask_override=None, mood=None, soft=None, walked=None, rnd=None):
        def f(pg):
            reset(pg, [['pork', 1]]); haggle_at(pg, 'meat', "{'pork':1}", floor)
            js = ''
            if ask_override: js += f"Game.st.ask={ask_override}; "
            if mood is not None: js += f"Game.st.mood={mood}; "
            if soft is not None: js += f"Game.st.soft={str(soft).lower()}; "
            if walked is not None: js += f"Game.st.walked={str(walked).lower()}; "
            if js: go(pg, js)
            if rnd is not None: ev(pg, f"Math.random = () => {rnd}")
        return f
    def judge_haggle(t, b, a, ctx):
        st0 = HST['st']; fl, ask, mood = st0['floor'], st0['ask'], st0['mood']
        st1 = ev(page, 'Game.st && {ask: Game.st.ask, mood: Game.st.mood, soft: Game.st.soft, walked: Game.st.walked, acc: !!Game.st.acc}')
        th = ev(page, "(Game.thought||[]).map(x=>x.zh).join('|')")
        if '算便宜' in t:
            p_ = max(fl, int(round(ask * 0.9 / 10)) * 10)
            if p_ < ask: return (a['s'] == 'HAGGLE' and st1['ask'] == p_ and st1['soft'] and '好啦好啦' in th and a['m'] == b['m'], (st1, th))
            return (a['s'] == 'HAGGLE' and st1['ask'] == ask and '最便宜' in th and a['m'] == b['m'], (st1, th))
        if t.startswith('我再看看'):
            if not (a['m'] == b['m'] and st1 and st1['walked'] and a['s'] == 'HAGGLE'): return (False, (st1, th))
            if ask <= fl: return ('最低價' in th and st1['ask'] == ask, (st1, th))
            if HST['rnd'] < 0.35: return ('慢慢看' in th and st1['ask'] == ask, (st1, th))
            return ('等一下' in th and st1['ask'] < ask and st1['ask'] >= fl, (st1, th))
        if t.startswith('好，'):
            return (a['s'] == 'PAY' and a['m'] == b['m'] and a['cash'] == b['cash'], (a, b))
        o = int(t.split('元')[0])
        if o >= fl: return (a['s'] == 'PAY' and a['m'] == b['m'], (a, st1))
        if o >= fl * 0.8:
            p_ = max(fl, int(round((o + ask) / 2 / 10)) * 10)
            return (a['s'] == 'HAGGLE' and st1['ask'] == p_ and st1['mood'] == mood and a['m'] == b['m'] and '不能再少' in th, (st1, th))
        if mood == 1: return (a['s'] == 'MAP' and a['m'] == b['m'] + 1 and ev(page, 'Game.closed.meat') is True, (a, th))
        return (a['s'] == 'HAGGLE' and st1['mood'] == mood - 1 and a['m'] == b['m'] and ('虧本' in th or '不賣' in th), (st1, th))
    HST = {}
    def run_haggle(name, setup, rnd=0.9):
        def s2(pg): setup(pg); ev(pg, f"Math.random = () => {rnd}"); HST['st'] = ev(pg, '({...Game.st})'); HST['rnd'] = rnd
        each(page, 'HAGGLE', s2, judge_haggle)
    run_haggle('底價210（出價：太低／可成交／可成交）', hg(210))
    run_haggle('底價240（出價：太低／還價／可成交）', hg(240))
    run_haggle('底價=報價（沒有降價空間）', hg(300, mood=3))
    run_haggle('心情剩 2（太低 → 心情 1）', hg(210, mood=2))
    run_haggle('心情剩 1（太低 → 不賣了）', hg(210, mood=1))
    run_haggle('已經用過算便宜', hg(210, soft=True))
    run_haggle('再看看：老闆不留人（不降價）', hg(210), 0.1)
    ev(page, "Math.random = window.__rnd")
    # 再看看三種結果的細節：降價＋綠卡、不降價、已經最低價
    hg(210)(page); ev(page, "Math.random = () => 0.9"); click_i(page, len(opts(page)) - 2)
    chk('HAGGLE', '再看看（不是最低價）→ 降價、「欸欸欸等一下」', ev(page, 'Game.st.ask') < 300 and '等一下' in ev(page, "(Game.thought||[]).map(x=>x.zh).join('|')"), ev(page, 'Game.st.ask'))
    chk('HAGGLE', '再看看之後這個選項不見', not any(t.startswith('我再看看') for t in opts(page)), opts(page))
    hg(300)(page); ev(page, "Math.random = () => 0.9"); click_i(page, len(opts(page)) - 2)
    chk('HAGGLE', '再看看（已經最低價）→ 「這已經是最低價了」', ev(page, 'Game.st.ask') == 300 and '最低價' in ev(page, "(Game.thought||[]).map(x=>x.zh).join('|')"))
    hg(210)(page); ev(page, "Math.random = () => 0.1"); click_i(page, len(opts(page)) - 2)
    chk('HAGGLE', '再看看（老闆不留人）→ 價錢不變、「慢慢看」', ev(page, 'Game.st.ask') == 300 and '慢慢看' in ev(page, "(Game.thought||[]).map(x=>x.zh).join('|')"))
    ev(page, "Math.random = window.__rnd")
    # 魚攤、菜攤的老闆娘：選項文字也是「老闆娘，算便宜一點啦！」，算便宜能按
    for k, cart in (('fish', "{'fish':1}"), ('veg', "{'egg':1}")):
        reset(page, [['pork', 1]]); haggle_at(page, k, cart, 40)
        o = opts(page); chk('HAGGLE', f'{k}攤選項', o[0] == '老闆娘，算便宜一點啦！', o)
        click_i(page, 0); chk('HAGGLE', f'{k}攤算便宜 → 降價', ev(page, 'Game.st.ask') < ev(page, 'Game.st.start') and state(page) == 'HAGGLE')

    # ═══ PAY：五個選項 × 錢夠／錢不夠 ═══
    def judge_pay(t, b, a, P):
        if t.startswith('不好意思，我買多了'): return (a['s'] == 'REDUCE' and a['m'] == b['m'], a)
        if t.startswith('不好意思，我的錢不夠'):
            return (a['s'] == 'REMOVE' and a['m'] == b['m'], a) if P['short'] else (W(b, a), a)
        if t == P['payOk']:
            return (W(b, a), a) if P['short'] else (a['s'] != 'PAY' and a['m'] == b['m'] and a['cash'] == b['cash'] - P['ask'], (a, P))
        return (W(b, a), a)          # 給的錢不夠付／賒帳
    for k, cart, cash in (('meat', "{'pork':1}", 1000), ('meat', "{'pork':1,'beef':1}", 1000), ('meat', "{'pork':1}", 100), ('meat', "{'pork':1,'beef':1}", 600),
                          ('fish', "{'fish':2}", 1000), ('fish', "{'crab':1,'shrimp':1}", 300), ('veg', "{'egg':1}", 1000), ('veg', "{'cabbage':1,'egg':1}", 50)):
        each(page, 'PAY', lambda pg, k=k, cart=cart, cash=cash: (reset(pg, [['pork', 1], ['beef', 1], ['fish', 2], ['crab', 1], ['shrimp', 1], ['egg', 1], ['cabbage', 1]]), pay_at(pg, k, cart, cash)), judge_pay, 5)

    # ═══ REMOVE：錢不夠，每一樣都能拿掉 ═══
    def rm_setup(cart):
        return lambda pg: (reset(pg, [['pork', 1], ['beef', 1], ['rib', 1]]), haggle_at(pg, 'meat', cart), go(pg, "Game.state='REMOVE'"))
    for cart in ("{'pork':1,'beef':1}", "{'pork':1,'beef':1,'rib':1}"):
        ids = eval(cart.replace("{", "[").replace("}", "]").replace(":1", "").replace("'", '"')) if False else [x.strip("'") for x in cart.strip('{}').replace(':1', '').split(',')]
        def jr(t, b, a, ctx, ids=ids):
            zh = t.replace('不要了。', ''); id_ = next(i for i in ids if ev(page, f"BYID['{i}'].zh") == zh)
            return (a['s'] == 'PAY' and id_ not in a['cart'] and a['lack'].get(id_) == 'money' and a['m'] == b['m'] and len(a['cart']) == len(ids) - 1, (a, b))
        each(page, 'REMOVE', rm_setup(cart), jr, len(ids))
    each(page, 'REMOVE', rm_setup("{'pork':1}"), lambda t, b, a, c: (a['s'] == 'MAP' and a['m'] == b['m'] and a['lack'].get('pork') == 'money', (a, b)), 1)

    # ═══ REDUCE：買多了，選哪一樣；沒事不用改了 ═══
    def rd_setup(pg):
        reset(pg, [['pork', 1], ['egg', 1]]); haggle_at(pg, 'meat', "{'pork':2,'beef':1}"); go(pg, "Game.state='REDUCE'")
    def jr2(t, b, a, c):
        if t.startswith('啊，沒事'): return (a['s'] == 'PAY' and a['m'] == b['m'] and a['cart'] == b['cart'], a)
        id_ = 'pork' if t.startswith('豬肉') else 'beef'
        return (a['s'] == 'REDUCE_Q' and ev(page, 'Game.redId') == id_ and a['m'] == b['m'], (a, t))
    each(page, 'REDUCE', rd_setup, jr2, 3)

    # ═══ REDUCE_Q：改成多少（每個數量）／我不要了 ═══
    def rq_setup(cart, red, req=None):
        def f(pg):
            reset(pg, req or [['pork', 1], ['egg', 1]]); haggle_at(pg, 'meat' if red in ('pork', 'beef', 'leg') else 'veg', cart); go(pg, f"Game.redId='{red}'; Game.state='REDUCE_Q'")
        return f
    def jq(red, cart_total_before):
        def j(t, b, a, c):
            zh = ev(page, f"BYID['{red}'].zh")
            if t == f'{zh}我不要了。': return (a['m'] == b['m'] and red not in a['cart'] and (a['s'] == 'PAY' or (a['s'] == 'MAP' and not a['cart'])), (a, b))
            qs = [q for q in ([0.5, 1, 2] if ev(page, f"BYID['{red}'].jin") else [1, 2, 3, 4, 5, 6]) if ev(page, f"qZh(BYID['{red}'], {q})") + '' and t == f'{zh}改成' + ev(page, f"qZh(BYID['{red}'], {q})") + '。']
            return (len(qs) == 1 and a['s'] == 'PAY' and a['cart'].get(red) == qs[0] and a['m'] == b['m'], (a, t))
        return j
    each(page, 'REDUCE_Q', rq_setup("{'pork':2,'beef':1}", 'pork'), jq('pork', 0), 3)                 # 兩斤 → 半斤／一斤／不要了
    each(page, 'REDUCE_Q', rq_setup("{'pork':1,'beef':1}", 'pork'), jq('pork', 0), 2)                 # 一斤 → 半斤／不要了
    each(page, 'REDUCE_Q', rq_setup("{'pork':1}", 'pork'), jq('pork', 0), 2)                          # 只有這一樣：不要了 → 回地圖
    each(page, 'REDUCE_Q', rq_setup("{'egg':3}", 'egg', [['egg', 1]]), jq('egg', 0), 3)               # 三盒 → 一盒／兩盒／不要了
    each(page, 'REDUCE_Q', rq_setup("{'corn':3,'tomato':1}", 'corn', [['corn', 2]]), jq('corn', 0), 3)  # 三根 → 一根／兩根／不要了

    # ═══ CHANGE：好謝謝／亂說找錯了／靠北，少找錢＝對 ═══
    for k in ('meat', 'fish', 'veg'):
        for sc in (False, True):
            cc = "{bill:500,ask:270,want:230,given:%d,sc:%s}" % (180 if sc else 230, 'true' if sc else 'false')
            def cs(pg, k=k, cc=cc):
                reset(pg, [['pork', 1]]); go(pg, f"Game.cur='{k}'; Game.tx=[{{id:'pork',q:1}}]; Game.st=null; Game.cc={cc}; Game.bagDone=true; Game.checkDone=true; Game.state='CHANGE'")
            def jc(t, b, a, c, sc=sc, k=k):
                fix = t.startswith('老闆') and '好像找錯了' in t
                if sc: return ((R(b, a) if fix else W(b, a)) and (not fix or True), (a, t))
                return ((R(b, a) if t == '好，謝謝。' else W(b, a)), (a, t))
            each(page, 'CHANGE', cs, jc, 3)
            # 說明文字
            cs(page); o = opts(page)
            for i, t in enumerate(o):
                cs(page); click_i(page, i); cd = card(page)
                if t == '好，謝謝。' and sc: chk('CHANGE', f'{k}少找、說好謝謝 → 說明是「少找了」', '少找了' in cd, cd)
                if t.startswith('靠北'): chk('CHANGE', f'{k}{"少找" if sc else "對"}、說靠北 → 說明', ('要有禮貌' in cd) if sc else ('找的錢是對的' in cd), cd)
                if (t.startswith('老闆') and not sc): chk('CHANGE', f'{k}沒少找、亂說 → 「找的錢是對的」', '找的錢是對的' in cd, cd)

    # ═══ BAG：三個選項 ═══
    def bag_setup(pg):
        reset(pg, [['pork', 1]]); go(pg, "Game.cur='meat'; Game.bagDone=true; Game.checkDone=true; Game.st=null; Game.tx=[{id:'pork',q:1}]; Game.state='BAG'")
    def jb(t, b, a, c): return (R(b, a), a) if t.startswith('不用') else (W(b, a), a)
    each(page, 'BAG', bag_setup, jb, 3)
    bag_setup(page)
    for i, t in enumerate(opts(page)):
        bag_setup(page); click_i(page, i); cd = card(page)
        if t == '我不要了。': chk('BAG', '我不要了 → 「你都已經付錢了，突然說不要了很奇怪欸。」', cd == '你都已經付錢了，突然說不要了很奇怪欸。', cd)
        if t.startswith('要，'): chk('BAG', '要塑膠袋 → 說明有環保袋', '環保袋' in cd, cd)

    # ═══ CHECK：核對東西，老闆放錯／沒放錯 × 三個選項 ═══
    for k, it_ in (('meat', 'pork'), ('fish', 'fish'), ('veg', 'egg')):
        for wrong in (False, True):
            def ck_setup(pg, k=k, it_=it_, wrong=wrong):
                reset(pg, [[it_, 1]]); go(pg, f"Game.cur='{k}'; Game.bagDone=true; Game.checkDone=true; Game.st=null; Game.tx=[{{id:'{it_}',q:1}}]; Game.ck={{id:'{it_}',q:1,wrong:{str(wrong).lower()},wq:2}}; Game.state='CHECK'")
            def jk(t, b, a, c, wrong=wrong):
                right = ('我要的是' in t) if wrong else (t == '好，謝謝。')
                return ((R(b, a) if right else W(b, a)), (a, t))
            each(page, 'CHECK', ck_setup, jk, 3)
            ck_setup(page); o = opts(page)
            chk('CHECK', f'{k} 第三個選項：{"故意的" if wrong else "你裝錯了"}', any(('故意' in t) if wrong else t.startswith('靠北！你裝錯') for t in o), o)
            for i, t in enumerate(o):
                ck_setup(page); click_i(page, i); cd = card(page)
                if t == '好，謝謝。' and wrong: chk('CHECK', f'{k}放錯、說好謝謝 → 說明「數量不對」', '數量不對' in cd, cd)
                if '我要的是' in t and not wrong: chk('CHECK', f'{k}沒放錯、亂說 → 說明「數量是對的」', '數量是對的' in cd, cd)
                if t.startswith('靠北'): chk('CHECK', f'{k}沒放錯、說靠北 → 說明「數量是對的」', '數量是對的' in cd, cd)
                if '故意' in t: chk('CHECK', f'{k}放錯、問是不是故意 → 說明「要有禮貌」', '禮貌' in cd, cd)

    # ═══ PHONE：不要理她／看訊息 ═══
    for ty in ('add', 'change'):
        def ph(pg, ty=ty):
            reset(pg, [['pork', 1], ['egg', 1]], {'type': ty, 'y': ['onion', 2], 'x': 'egg' if ty == 'change' else None}); go(pg, "Game.state='PHONE'")
        ph(page); o = opts(page); chk('PHONE', f'{ty}：兩個選項', sorted(o) == sorted(['不要理她。', '看訊息。']), o)
        for i, t in enumerate(o):
            ph(page); click_i(page, i)
            if t == '看訊息。': chk('PHONE', f'{ty}：看訊息 → MSG', state(page) == 'MSG' and ev(page, 'Game.msgShown') is True and ev(page, 'Game.mistakes') == 0)
            else: chk('PHONE', f'{ty}：不要理她 → 回地圖、清單照樣改、不扣分', state(page) == 'MAP' and ev(page, 'Game.ignoredMsg') is True and ev(page, 'Game.mistakes') == 0 and ev(page, "Game.req.some(a=>a.id==='onion')") is True)

    # ═══ MSG：加買／改項目（已買／沒買）═══
    def ms_setup(ty, bought):
        def f(pg):
            reset(pg, [['pork', 1], ['egg', 1]], {'type': ty, 'y': ['onion', 2], 'x': 'pork' if ty == 'change' else None})
            go(pg, ("Game.bought={pork:1}; " if bought else '') + "Game.state='MSG'")
        return f
    def jm(ty, bought):
        def j(t, b, a, c):
            if not bought: return (a['s'] == 'MAP' and a['m'] == b['m'], a)
            if '我已經買了' in t: return (a['s'] == 'MAP' and a['m'] == b['m'] and ev(page, "Game.req.some(a=>a.id==='pork')") is True, a)
            return (W(b, a), a)
        return j
    each(page, 'MSG', ms_setup('add', False), jm('add', False), 1)
    each(page, 'MSG', ms_setup('change', False), jm('change', False), 1)
    each(page, 'MSG', ms_setup('change', True), jm('change', True), 3)
    each(page, 'MSG', ms_setup('add', False), lambda t, b, a, c: (ev(page, "Game.req.some(a=>a.id==='onion')") is True and a['s'] == 'MAP', a), 1)
    ms_setup('change', False)(page); click_i(page, 0)
    chk('MSG', '改項目、還沒買 → 清單換成洋蔥', ev(page, "Game.req.some(a=>a.id==='onion')") and not ev(page, "Game.req.some(a=>a.id==='pork')"))
    ms_setup('change', True)(page); o = opts(page)
    for i, t in enumerate(o):
        ms_setup('change', True)(page); click_i(page, i); cd = card(page)
        if t.startswith('Ami，你自己'): chk('MSG', '「你自己來買吧」→ 說明要有禮貌', '禮貌' in cd or '客氣' in cd or '請' in cd, cd)
        if t.startswith('好，我再去買'): chk('MSG', '「我再去買」→ 說明已經買好了要告訴 Ami', '告訴Ami' in cd, cd)

    # ═══ EXPLAIN：三種原因 × 三個說法 ═══
    CAUSE = {'money': '我的錢不夠，所以沒買。', 'refused': '老闆不賣給我。', 'forgot': '對不起，我忘記了。'}
    for real in ('money', 'refused', 'forgot'):
        def ex_setup(pg, real=real):
            reset(pg, [['fish', 1]]); go(pg, "Game.bought={}; Game.queue=[Game.req[0]]; Game.qi=0; Game.explained={}; Game.lack=" + ("{fish:'%s'}" % real if real != 'forgot' else '{}') + "; Game.state='EXPLAIN'")
        each(page, 'EXPLAIN', ex_setup, lambda t, b, a, c, real=real: (a['s'] == 'END', a) if t == CAUSE[real] else (W(b, a), a), 3)
        ex_setup(page)
        for said in ('money', 'refused', 'forgot'):
            if said == real: continue
            ex_setup(page); o = opts(page); i = o.index(CAUSE[said]); click_i(page, i); cd = card(page)
            w = {('money', 'refused'): '不是錢不夠，是老闆生氣不賣給你', ('money', 'forgot'): '你的錢是夠的，你是忘記買了',
                 ('refused', 'money'): '老闆沒有不賣，是你的錢不夠', ('refused', 'forgot'): '老闆沒有不賣，你是忘記買了',
                 ('forgot', 'money'): '你不是忘記，是錢不夠', ('forgot', 'refused'): '你不是忘記，是老闆不賣給你'}[(said, real)]
            chk('EXPLAIN', f'實際={real}、說{said} → 說明「{w}」', w in cd, cd)
        # 說對的綠卡
        ex_setup(page); click_i(page, opts(page).index(CAUSE[real]))
        chk('EXPLAIN', f'實際={real}、說對 → 記錄原因、進結局', ev(page, f"Game.explained['fish']") == real and state(page) == 'END')
    # 老闆不賣卻說「錢不夠」不能被 Ami 抓到說謊；忘記卻說「老闆不賣」→ Ami 懷疑
    ex_setup = lambda pg: (reset(pg, [['fish', 1]]), go(pg, "Game.bought={}; Game.queue=[Game.req[0]]; Game.qi=0; Game.explained={}; Game.lack={}; Game.state='EXPLAIN'"))
    ex_setup(page); click_i(page, opts(page).index(CAUSE['refused']))
    chk('EXPLAIN', '忘記卻說老闆不賣 → Ami：你應該沒有騙我吧', '你應該沒有騙我吧' in plain(page, '#npc-dialogue'))
    ex_setup(page); click_i(page, opts(page).index(CAUSE['money']))
    chk('EXPLAIN', '忘記卻說錢不夠 → Ami：可是你的錢是夠的啊', '你的錢是夠的' in plain(page, '#npc-dialogue'))

    # ═══ END／RESULT ═══
    reset(page, [['pork', 1]]); go(page, "Game.bought={pork:1}; Game.queue=[]; Game.settle()")
    o = opts(page); chk('END', '一個選項「查看結果」', len(o) == 1 and o[0].startswith('查看結果'), o)
    click_i(page, 0); chk('END', '查看結果 → 結果頁', state(page) == 'RESULT', state(page))
    o = opts(page); chk('RESULT', '一個選項「查看排行榜」', len(o) == 1 and o[0].startswith('查看排行榜'), o)
    check('每個選項都按過（%s，共 %d 項檢查）' % ('、'.join(f'{k} {v}' for k, v in COUNT.items()), sum(COUNT.values())), not [f for f in fails if f.startswith('[')], [f for f in fails if f.startswith('[')][:3])

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
    check('地圖：三個攤位圖示直接點，下方只有「回家」', plain(page, '.stalls').count('攤') == 3 and page.locator('button.stall[data-choice]').count() == 3 and opts(page) == ['東西買好了，回家'], (opts(page), page.locator('button.stall[data-choice]').count()))
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
    check('肉攤付錢畫面用肉攤的付錢圖', 'stall_meat_pay' in ev(page, "document.getElementById('npc-avatar').src"), ev(page, "document.getElementById('npc-avatar').src"))
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
            mm = ev(page, 'Game.mistakes'); tap(page, '我不要了'); lg = ev(page, 'Game.log[Game.log.length-1].zh')
            check('塑膠袋關選「我不要了」→ 說明是「已經付錢要收下」，不是環保袋', ev(page, 'Game.mistakes') == mm + 1 and '已經付錢' in lg and '奇怪' in lg and '環保袋' not in lg, lg)
            tap(page, '不用，我有環保袋')
        else: tap(page, '好，謝謝')
    check('付完一攤回到地圖，這攤打勾', state(page) == 'MAP' and ev(page, 'Game.visited.meat') is True)

    # 3b. 魚攤、菜攤是老闆娘：選項跟著改
    tap(page, '去菜攤'); buy(page, 'cabbage', 1); tap(page, '買好了')
    check('菜攤的選項是「老闆娘，算便宜一點啦！」', opts(page)[0] == '老闆娘，算便宜一點啦！', opts(page))
    tap(page, '好，'); P = ev(page, 'Game.payInfo()'); tap(page, P['payOk'])
    while state(page) in ('CHANGE', 'BAG', 'CHECK'):
        st = state(page)
        if st == 'CHANGE':
            cc = ev(page, 'Game.cc'); tap(page, '老闆，好像找錯了' if cc['sc'] else '好，謝謝')
        elif st == 'BAG': tap(page, '不用，我有環保袋')
        else: tap(page, '好，謝謝')
    ev(page, "Game.visited.veg = false; Game.bought.cabbage = 0")

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

    # 7b. 沒買是因為忘記，卻說「老闆不賣給我」→ 扣分、Ami 說「你應該沒有騙我吧！」
    new_game(page); setreq(page, [['pork', 1], ['fish', 1], ['cabbage', 1], ['egg', 1]])
    tap(page, '東西買好了，回家')
    mm = ev(page, 'Game.mistakes'); tap(page, CAUSE_REF := '老闆不賣給我')
    check('忘記卻說老闆不賣 → 扣分', ev(page, 'Game.mistakes') == mm + 1)
    check('Ami：你應該沒有騙我吧！', '你應該沒有騙我吧' in plain(page, '#npc-dialogue'), plain(page, '#npc-dialogue')[:80])

    # 8. Ami 訊息：加買
    new_game(page)
    setreq(page, [['pork', 1], ['mince', 1], ['leg', 1], ['rib', 1]], {'type': 'add', 'y': ['onion', 2]})
    tap(page, '去肉攤')
    for i, q in [('pork', 1), ('mince', 1), ('leg', 1), ('rib', 1)]: buy(page, i, q)
    tap(page, '買好了'); tap(page, '好，'); P = ev(page, 'Game.payInfo()'); tap(page, P['payOk'])
    while state(page) in ('CHANGE', 'BAG', 'CHECK', 'PHONE', 'MSG'):
        st = state(page)
        if st == 'CHANGE':
            cc = ev(page, 'Game.cc'); tap(page, '老闆，好像找錯了' if cc['sc'] else '好，謝謝')
        elif st == 'BAG': tap(page, '不用，我有環保袋')
        elif st == 'PHONE':
            check('手機響了 → 選項是「不要理她」「看訊息」', sorted(opts(page)) == sorted(['不要理她。', '看訊息。']), opts(page)); tap(page, '看訊息')
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
    check('第一攤之後手機響了', state(page) == 'PHONE', state(page)); tap(page, '看訊息')
    check('改項目、豬肉已買 → 出現三個選項', state(page) == 'MSG' and len(opts(page)) == 3 and any(t.startswith('Ami，一斤豬肉我已經買了') for t in opts(page)), opts(page))
    check('沒有「退貨」字樣', not any('退' in t for t in opts(page)))
    check('Ami 的訊息是彈跳視窗，下方選項列隱藏', page.locator('#msg-pop').count() == 1 and page.locator('#options-area .opt').count() == 0 and '改買' in plain(page, '#msg-pop'), plain(page, '#msg-pop')[:60])
    shot(page, 'msg_change')
    mm = ev(page, 'Game.mistakes'); tap(page, '好，我再去買'); check('「我再去買」→ 扣分、說明已買好', ev(page, 'Game.mistakes') == mm + 1 and '已經買好' in ev(page, 'Game.log[Game.log.length-1].zh'))
    tap(page, 'Ami，你自己來買'); check('「你自己來買」→ 扣分（不禮貌）', ev(page, 'Game.mistakes') == mm + 2)
    tap(page, 'Ami，一斤豬肉我已經買了')
    check('答完彈跳視窗消失', page.locator('#msg-pop').count() == 0)
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
    tap(page, '看訊息')
    check('X 還沒買 → 只有一個「知道了」選項', state(page) == 'MSG' and opts(page) == ['好，我知道了。'], opts(page))
    tap(page, '好，我知道了')
    check('雞蛋換成洋蔥', ev(page, "Game.req.some(a=>a.id==='onion')") and not ev(page, "Game.req.some(a=>a.id==='egg')"))

    # 9b. 不理她：加買 → 清單照樣多一樣、提示裡沒有訊息、不問原因、一次扣分、壞結局、Ami 說「你都不看訊息」
    new_game(page)
    setreq(page, [['pork', 1], ['fish', 1], ['cabbage', 1], ['egg', 1]], {'type': 'add', 'y': ['onion', 2]})
    tap(page, '去肉攤'); buy(page, 'pork', 1); tap(page, '買好了'); tap(page, '好，'); P = ev(page, 'Game.payInfo()'); tap(page, P['payOk'])
    while state(page) in ('CHANGE', 'BAG', 'CHECK'):
        st = state(page)
        if st == 'CHANGE':
            cc = ev(page, 'Game.cc'); tap(page, '老闆，好像找錯了' if cc['sc'] else '好，謝謝')
        elif st == 'BAG': tap(page, '不用，我有環保袋')
        else: tap(page, '好，謝謝')
    check('手機響了', state(page) == 'PHONE', state(page))
    tap(page, '不要理她')
    check('不理她 → 回地圖、當場不扣分、清單照樣多一樣', state(page) == 'MAP' and ev(page, 'Game.mistakes') == 0 and ev(page, "Game.req.some(a=>a.id==='onion')") and ev(page, 'Game.ignoredMsg'), (state(page), ev(page, 'Game.req')))
    ev(page, "Hints.toggle(true)"); hh = ev(page, "document.getElementById('hint-body').textContent"); ev(page, "Hints.toggle(false)")
    check('沒看訊息 → 任務提示裡沒有那則訊息', 'Ami 後來傳的訊息' not in hh and '洋蔥' not in hh, hh[:80])
    ev(page, "Game.bought = {pork: 1, fish: 1, cabbage: 1, egg: 1}"); tap(page, '東西買好了，回家')
    log_ = ev(page, "Game.log.map(x=>x.zh)"); fin_ = ev(page, "Game.final.map(x=>x.zh)")
    check('不理她：不問原因，直接結局', state(page) == 'END', state(page))
    check('不理她：壞結局、只扣一次 −10（說明沒看訊息）', ev(page, 'Game._endGood') is False and ev(page, 'Game.mistakes') == 1 and any('沒有看' in l for l in log_), (ev(page, 'Game.mistakes'), log_))
    check('Ami：我有傳訊息給你要加買…欸！你都不看訊息！', any('我有傳訊息給你，要加買兩顆洋蔥欸！你都不看訊息！' in l for l in fin_), fin_)
    # 9c. 不理她：改項目，剛好已經買了 Ami 說不要的那樣 → 也是壞結局
    new_game(page)
    setreq(page, [['pork', 1], ['fish', 1], ['cabbage', 1], ['egg', 1]], {'type': 'change', 'x': 'pork', 'y': ['beef', 1]})
    ev(page, "Game.bagDone = true; Game.checkDone = true")
    tap(page, '去肉攤'); buy(page, 'pork', 1); tap(page, '買好了'); tap(page, '好，'); P = ev(page, 'Game.payInfo()'); tap(page, P['payOk'])
    while state(page) in ('CHANGE', 'BAG', 'CHECK'):
        st = state(page)
        if st == 'CHANGE':
            cc = ev(page, 'Game.cc'); tap(page, '老闆，好像找錯了' if cc['sc'] else '好，謝謝')
        else: tap(page, '好，謝謝')
    tap(page, '不要理她')
    check('不理她（改項目）：清單照樣換成牛肉', ev(page, "Game.req.some(a=>a.id==='beef')") and not ev(page, "Game.req.some(a=>a.id==='pork')"))
    ev(page, "Game.bought = {pork: 1, fish: 1, cabbage: 1, egg: 1}"); tap(page, '東西買好了，回家')
    fin_ = ev(page, "Game.final.map(x=>x.zh)")
    check('不理她（改項目）：不問原因、壞結局、只扣一次、Ami 說「不要豬肉、改買牛肉」', state(page) == 'END' and ev(page, 'Game._endGood') is False and ev(page, 'Game.mistakes') == 1 and any('說不要豬肉、改買一斤牛肉欸！你都不看訊息' in l for l in fin_), (state(page), ev(page, 'Game.mistakes'), fin_))

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
    tap(page, '去魚攤'); buy(page, 'fish', 1); tap(page, '買好了'); ev(page, 'Game.st.floor = 100')
    for _ in range(3):
        o = opts(page); i = next(k for k, t_ in enumerate(o) if t_.endswith('元可以嗎？'))
        page.locator('#options-area .opt').nth(i).click(); page.wait_for_timeout(120)
    check('魚攤不賣了：過場畫面是老闆娘生氣圖', state(page) == '_TRANS' and 'stall_fish_angry' in ev(page, "document.getElementById('npc-avatar').src"))
    page.locator('#options-area .opt').first.click(); page.wait_for_timeout(100)
    new_game(page); setreq(page, [['pork', 1], ['fish', 1], ['cabbage', 1], ['egg', 1]])
    tap(page, '去魚攤'); buy(page, 'fish', 1); tap(page, '買好了'); ev(page, 'Game.st.floor = 99')
    tap(page, '好，')
    check('魚攤付錢畫面用魚攤的付錢圖', state(page) == 'PAY' and 'stall_fish_pay' in ev(page, "document.getElementById('npc-avatar').src"), (state(page), ev(page, "document.getElementById('npc-avatar').src")))
    new_game(page); setreq(page, [['pork', 1], ['fish', 1], ['cabbage', 1], ['egg', 1]])
    tap(page, '去菜攤'); buy(page, 'cabbage', 1); tap(page, '買好了'); ev(page, 'Game.st.floor = 100')
    for _ in range(3):
        o = opts(page); i = next(k for k, t_ in enumerate(o) if t_.endswith('元可以嗎？'))
        page.locator('#options-area .opt').nth(i).click(); page.wait_for_timeout(120)
    check('菜攤不賣了：過場畫面是老闆娘生氣圖', state(page) == '_TRANS' and 'stall_veg_angry' in ev(page, "document.getElementById('npc-avatar').src"))
    page.locator('#options-area .opt').first.click(); page.wait_for_timeout(100)

    # 10c2. 忘記買的（兩樣以上）Ami 合成一句；只有一樣時照原本的句子
    new_game(page); setreq(page, [['pork', 1], ['egg', 1], ['onion', 1]])
    ev(page, 'Game.bought = {}; Game.lack = {}; Game.explained = {}; Game.queue = []; Game.settle()')
    fl = ev(page, 'Game.final.map(x=>x.zh)')
    wl = [l for l in fl if '沒有買' in l]
    check('忘記買三樣：Ami 合成一句、每樣仍各扣分', len(wl) == 1 and wl[0].count('Ami：') == 1 and wl[0].count('沒有買') == 1 and '豬肉' in wl[0] and '雞蛋' in wl[0] and '洋蔥' in wl[0] and ev(page, 'Game.mistakes') == 3, (fl, ev(page, 'Game.mistakes')))
    new_game(page); setreq(page, [['pork', 1], ['egg', 1]])
    ev(page, 'Game.bought = {egg: 1}; Game.lack = {}; Game.explained = {}; Game.queue = []; Game.settle()')
    fl = ev(page, 'Game.final.map(x=>x.zh)')
    check('只忘記一樣：照原本的句子', any('我要' in l and '你沒有買耶' in l for l in fl), fl)

    # 10c3. 忘記買＋數量不對：合成同一句（只有一個「Ami：」）
    new_game(page); setreq(page, [['pork', 1], ['egg', 1], ['onion', 1]])
    ev(page, 'Game.bought = {egg: 2}; Game.lack = {}; Game.explained = {}; Game.queue = []; Game.settle()')
    fl = ev(page, 'Game.final.map(x=>x.zh)')
    wl = [l for l in fl if '沒有買' in l]
    check('沒買＋買錯數量：合成同一句', len(wl) == 1 and wl[0].count('Ami：') == 1 and '你都沒有買' in wl[0] and '還有，' in wl[0] and '雞蛋' in wl[0] and not any(('買太' in l or '買錯了啦' in l) and l is not wl[0] for l in fl), fl)

    # 10c4. 回家問原因：第一樣完整問、第二樣「那……怎麼也沒買？」、第三樣以後「……呢？」
    new_game(page); setreq(page, [['pork', 1], ['egg', 1], ['onion', 1]])
    ev(page, 'Game.bought = {}; Game.lack = {}; Game.explained = {}; Game.queue = Game.req.slice(); Game.qi = 0; Game.state = "EXPLAIN"')
    q3 = [ev(page, '(() => { Game.qi = %d; return Game.getConfig().EXPLAIN.dialogue().map(x => x.zh).join("|"); })()' % i) for i in range(3)]
    check('回家問原因：第一／第二／第三樣的問法不同', '怎麼沒買？' in q3[0] and '那……' in q3[1] and '怎麼也沒買？' in q3[1] and q3[2].endswith('呢？') and '怎麼' not in q3[2], q3)

    # 10c5. 少買三樣以上：每一樣都問（沒有上限）
    new_game(page); setreq(page, [['pork', 1], ['egg', 1], ['onion', 1], ['fish', 1]])
    ev(page, 'Game.bought = {}; Game.lack = {}; Game.explained = {}; Game.bagDone = true; Game.checkDone = true; Game.goHome()')
    check('少買四樣：四樣都要問', state(page) == 'EXPLAIN' and ev(page, 'Game.queue.length') == 4, ev(page, 'Game.queue.length'))

    # 10c6. 翻譯小視窗會自己加上說話的人（「Ami:」），西文／英文本身不能再寫一次
    src_ = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'games', 'market', 'index.html'), encoding='utf-8').read()
    check('西文／英文台詞前面不重複寫「Ami:」', 'Ami: ' not in src_ and '`Ami: ' not in src_)

    # 10b. 去過的攤位還可以再去：第一次少買（半斤），回頭補買（再半斤）→ 湊成一斤，不用扣分
    new_game(page); setreq(page, [['pork', 1]])
    ev(page, 'Game.checkDone = true; Game.bagDone = true')
    tap(page, '去肉攤'); buy(page, 'pork', 0.5); tap(page, '買好了'); pay_through(page)
    check('去過的肉攤，地圖上還能再點', state(page) == 'MAP' and page.locator('button.stall[data-choice="去肉攤"]').count() == 1 and '買過了' not in plain(page, '.stalls') and ev(page, "getComputedStyle(document.querySelector('button.stall[data-choice]')).opacity") == '1')
    tap(page, '去肉攤'); buy(page, 'pork', 0.5); tap(page, '買好了'); pay_through(page)
    check('補買後數量加起來是一斤', ev(page, 'Game.bought.pork') == 1, ev(page, 'Game.bought.pork'))
    tap(page, '東西買好了，回家')
    check('補買完整 → 好結局、沒有扣分', state(page) == 'END' and ev(page, 'Game._endGood') is True and ev(page, 'Game.mistakes') == 0, (state(page), ev(page, 'Game.mistakes')))

    # 10c. 買錯的（數量不對＋多買）Ami 合成一句
    new_game(page); setreq(page, [['pork', 1], ['egg', 1]])
    ev(page, 'Game.bought = {pork: 0.5, egg: 2, onion: 2}; Game.lack = {}')
    tap(page, '東西買好了，回家')
    fl = ev(page, 'Game.final.map(x=>x.zh)')
    wl = [l for l in fl if '買錯了啦' in l or '買太' in l or '沒有要' in l]
    check('買錯的（有少有多有多買）合成同一句、只說一次「買錯了」', len(wl) == 1 and wl[0].count('Ami：') == 1 and wl[0].count('買錯了啦') == 1 and '豬肉要一斤' in wl[0] and '雞蛋只要' in wl[0] and '洋蔥我沒有要' in wl[0], fl)
    # 全部都買太多：開頭說一次「買太多了」，後面只列要多少，不重複
    new_game(page); setreq(page, [['pork', 1], ['egg', 1], ['onion', 1]])
    ev(page, 'Game.bought = {pork: 2, egg: 2, onion: 2}; Game.lack = {}')
    tap(page, '東西買好了，回家')
    fl = ev(page, 'Game.final.map(x=>x.zh)')
    wl = [l for l in fl if '買太' in l]
    check('買太多：只說一次「買太多了」，後面列每樣要多少', len(wl) == 1 and wl[0].count('買太多了') == 1 and wl[0].count('只要') == 3, fl)

    # 10d. 老闆弄錯（少找錢／放錯數量）玩家指出來 → 過場畫面是老闆尷尬臉（肉攤）
    new_game(page); setreq(page, [['pork', 1]]); ev(page, 'Game.bagDone = true; Game.checkDone = true')
    tap(page, '去肉攤'); buy(page, 'pork', 1); tap(page, '買好了'); tap(page, '好，'); P = ev(page, 'Game.payInfo()'); tap(page, P['payOk'])
    check('付錢後進入找錢', state(page) == 'CHANGE', state(page))
    ev(page, "Game.cc = {bill: 500, ask: 300, want: 200, given: 150, sc: true}; Game.render()")
    o = opts(page); page.locator('#options-area .opt').nth(next(k for k, t_ in enumerate(o) if '好像找錯了' in t_)).click(); page.wait_for_timeout(120)
    check('少找錢被指出來 → 過場畫面是肉攤老闆拿零錢的尷尬臉', state(page) == '_TRANS' and 'stall_meat_change' in ev(page, "document.getElementById('npc-avatar').src"), (state(page), ev(page, "document.getElementById('npc-avatar').src")))
    page.locator('#options-area .opt').first.click(); page.wait_for_timeout(100)
    check('離開過場後恢復平常的圖', 'sorry' not in ev(page, "document.getElementById('npc-avatar').src") and 'change' not in ev(page, "document.getElementById('npc-avatar').src"))
    ev(page, "Game.state = 'CHECK'; Game.tx = [{id:'pork', q:1}]; Game.ck = {id:'pork', q:1, wrong:true, wq:2}; Game.render()")
    o = opts(page); page.locator('#options-area .opt').nth(next(k for k, t_ in enumerate(o) if '我要的是' in t_)).click(); page.wait_for_timeout(120)
    check('放錯數量被指出來 → 過場畫面也是尷尬臉', state(page) == '_TRANS' and 'stall_meat_sorry' in ev(page, "document.getElementById('npc-avatar').src"), state(page))

    # 10e. 老闆沒弄錯時，「亂說他弄錯」的那個選項，講的數字不能跟畫面上實際的一樣
    new_game(page); setreq(page, [['pork', 1]]); ev(page, 'Game.bagDone = true; Game.checkDone = true')
    tap(page, '去肉攤'); buy(page, 'pork', 1); tap(page, '買好了'); tap(page, '好，'); P = ev(page, 'Game.payInfo()'); tap(page, P['payOk'])
    ev(page, "Game.cc = {bill: 1000, ask: 300, want: 700, given: 700, sc: false}; Game.render()")
    o = [t_ for t_ in opts(page) if '好像找錯了' in t_]
    check('找對錢時，「應該找X元」的X不能等於實際找的錢', len(o) == 1 and '七百五十元' in o[0] and '七百元' not in o[0].replace('七百五十元', ''), o)
    ev(page, "Game.state = 'CHECK'; Game.tx = [{id:'pork', q:1}]; Game.ck = {id:'pork', q:1, wrong:false, wq:2}; Game.render()")
    o = [t_ for t_ in opts(page) if '我要的是' in t_]
    shown = ev(page, "document.querySelector('.basket').innerText")
    check('數量放對時，「我要的是」的數量要和畫面上看到的相反', len(o) == 1 and o[0].index('我要的是') < o[0].index('不是') and '我要的是一斤' not in o[0], (o, shown))

    # 10f. 買多了：付錢前跟老闆說「我買多了」→ 選哪一樣 → 選改成多少；選錯不當場糾正（最後結局才判斷），也不是「錢不夠」
    new_game(page); setreq(page, [['pork', 1], ['egg', 1]]); ev(page, 'Game.bagDone = true; Game.checkDone = true')
    tap(page, '去肉攤'); buy(page, 'pork', 2); tap(page, '買好了'); ev(page, 'Game.st.floor = 99'); tap(page, '好，')
    check('付錢畫面有「我買多了」選項', state(page) == 'PAY' and '不好意思，我買多了，有一樣要改。' in opts(page), opts(page))
    ask0 = ev(page, 'Game.st.ask'); m0 = ev(page, 'Game.mistakes')
    tap(page, '不好意思，我買多了')
    check('買多了 → 選哪一樣（有「沒事不用改了」），不扣分', state(page) == 'REDUCE' and '豬肉我買多了。' in opts(page) and '啊，沒事，不用改了。' in opts(page) and ev(page, 'Game.mistakes') == m0, (state(page), opts(page)))
    tap(page, '豬肉我買多了')
    check('再選改成多少：半斤、一斤、不要了', state(page) == 'REDUCE_Q' and sorted(opts(page)) == sorted(['豬肉改成半斤。', '豬肉改成一斤。', '豬肉我不要了。']), (state(page), opts(page)))
    tap(page, '豬肉改成一斤')
    check('改成一斤、價錢變低、不扣分、不記「錢不夠」', state(page) == 'PAY' and ev(page, 'Game.cart.pork') == 1 and ev(page, 'Game.st.ask') < ask0 and ev(page, 'Game.lack.pork') is None and ev(page, 'Game.mistakes') == m0, (ev(page, 'Game.cart'), ev(page, 'Game.st.ask'), ask0))
    # 選錯就選錯：改成半斤（比 Ami 要的少）不當場扣分
    tap(page, '不好意思，我買多了'); tap(page, '豬肉我買多了')
    check('一斤再改只剩半斤、不要了', sorted(opts(page)) == sorted(['豬肉改成半斤。', '豬肉我不要了。']), opts(page))
    tap(page, '豬肉改成半斤')
    check('選錯數量（改成半斤）不當場扣分，回付錢', state(page) == 'PAY' and ev(page, 'Game.cart.pork') == 0.5 and ev(page, 'Game.mistakes') == m0, (state(page), ev(page, 'Game.cart')))
    tap(page, '不好意思，我買多了'); tap(page, '啊，沒事')
    check('「沒事不用改了」回付錢、不扣分', state(page) == 'PAY' and ev(page, 'Game.mistakes') == m0)
    # Ami 沒要的東西買了 → 整樣不要
    new_game(page); setreq(page, [['cabbage', 1], ['egg', 1]]); ev(page, 'Game.bagDone = true; Game.checkDone = true')
    tap(page, '去菜攤'); buy(page, 'cabbage', 1); buy(page, 'egg', 1); buy(page, 'tomato', 1); tap(page, '買好了'); ev(page, 'Game.st.floor = 99'); tap(page, '好，')
    tap(page, '不好意思，我買多了'); tap(page, '番茄我買多了'); tap(page, '番茄我不要了')
    check('Ami沒要的番茄 → 整樣不要，不記「錢不夠」', state(page) == 'PAY' and 'tomato' not in ev(page, 'Game.cart') and ev(page, 'Game.lack.tomato') is None)

    # 10g. 任務提示：有「你現在買了什麼」，隨買東西更新；籃子裡還沒付錢的另外列
    new_game(page); setreq(page, [['pork', 1], ['egg', 1]])
    ev(page, "Game.render(); Hints.toggle(true)")
    h = ev(page, "[...document.querySelectorAll('#hint-body .h-sec, #hint-body .h-zh')].map(e => { const c = e.cloneNode(true); c.querySelectorAll('rt,rp').forEach(x => x.remove()); return c.textContent; }).join('|')")
    check('任務提示：還沒買東西 → 寫「還沒買任何東西」', '你現在買了什麼' in h and '還沒買任何東西' in h, h)
    ev(page, "Hints.toggle(false)")
    tap(page, '去肉攤'); buy(page, 'pork', 1)
    ev(page, "Hints.toggle(true)")
    h = ev(page, "[...document.querySelectorAll('#hint-body .h-sec, #hint-body .h-zh')].map(e => { const c = e.cloneNode(true); c.querySelectorAll('rt,rp').forEach(x => x.remove()); return c.textContent; }).join('|')")
    check('任務提示：籃子裡的豬肉列在「籃子裡（還沒付錢）」', '籃子裡（還沒付錢）' in h and '豬肉' in h.split('籃子裡（還沒付錢）')[1], h)
    ev(page, "Hints.toggle(false)")
    ev(page, "Game.bought = {pork: 1}; Game.cart = {}; Hints.toggle(true)")
    h = ev(page, "[...document.querySelectorAll('#hint-body .h-sec, #hint-body .h-zh')].map(e => { const c = e.cloneNode(true); c.querySelectorAll('rt,rp').forEach(x => x.remove()); return c.textContent; }).join('|')")
    check('任務提示：付完錢的豬肉列在「你現在買了什麼」', '一斤豬肉' in h.split('你現在買了什麼')[1] and '還沒買任何東西' not in h, h)
    ev(page, "Hints.toggle(false)")

    # 10h. 小字典：PICK 依攤位列量詞；MSG 有字典；END 依好壞結局
    for cur_, want_, no_ in (('meat', ['斤', '半斤', '隻'], ['顆', '把', '根', '盒']), ('fish', ['斤', '半斤', '條', '隻'], ['顆', '把', '根', '盒']), ('veg', ['顆', '把', '根', '盒'], ['斤', '半斤', '隻', '條'])):
        ev(page, "Game.cur = '%s'" % cur_)
        ws = ev(page, "VOCAB.PICK.map(w => w[0])")
        check('PICK 小字典（%s攤）只列這一攤的量詞' % cur_, all(w in ws for w in want_) and not any(w in ws for w in no_) and '籃子' in ws, ws)
    # MSG 小字典：依 Ami 傳的是加買還是改項目，列訊息裡真的有的字
    for ty_, want_ in (('add', ['突然想到', '加買']), ('change', ['不用', '改買'])):
        setreq(page, [['pork', 1], ['egg', 1]], {'type': ty_, 'y': ['onion', 2], 'x': 'egg' if ty_ == 'change' else None})
        wv = ev(page, "VOCAB.MSG.map(w => w[0])"); line_ = ev(page, "Game.msgLine().zh")
        check('MSG 小字典（%s）：字都在訊息裡' % ty_, all(w in wv for w in want_) and all(w in line_ for w in wv if w != '已經'), (wv, line_))
    ev(page, "Game._endGood = true"); g_ = ev(page, "VOCAB.END.map(w => w[0])")
    ev(page, "Game._endGood = false"); b_ = ev(page, "VOCAB.END.map(w => w[0])")
    check('END 小字典：好結局和壞結局不一樣', '新鮮' in g_ and '買錯' in b_ and '新鮮' not in b_, (g_, b_))
    # 找錢：老闆沒少找時，「靠北你找錯了」也要說「找的錢是對的」
    new_game(page); setreq(page, [['pork', 1]]); ev(page, 'Game.bagDone = true; Game.checkDone = true')
    tap(page, '去肉攤'); buy(page, 'pork', 1); tap(page, '買好了'); ev(page, 'Game.st.floor = 99'); tap(page, '好，'); P = ev(page, 'Game.payInfo()'); tap(page, P['payOk'])
    ev(page, "Game.cc = {bill: 1000, ask: 300, want: 700, given: 700, sc: false}; Game.render()")
    tap(page, '靠北'); lg = ev(page, 'Game.log[Game.log.length-1].zh')
    check('找對錢時選「靠北！你找錯錢了吧！」→ 說明是「找的錢是對的」', '找的錢是對的' in lg and '禮貌' not in lg, lg)

    # 10i. 測試網址 ?msg=add / change / 1：Ami 一定會傳訊息
    for q_, want_ in (('add', {'add'}), ('change', {'change'}), ('1', {'add', 'change'})):
        for _ in range(6):
            page.goto(f'http://127.0.0.1:{PORT}/games/market/index.html?msg={q_}'); page.wait_for_timeout(250)
            t_ = ev(page, 'Game.setup(), Game.task.msg && Game.task.msg.type')
            check(f'網址 ?msg={q_} → 這局一定有 Ami 的訊息（{"/".join(sorted(want_))}）', t_ in want_, t_)
    page.goto(f'http://127.0.0.1:{PORT}/games/market/index.html'); page.wait_for_timeout(250)

    for stall_, item_, key_ in (('魚攤', 'fish', 'fish'), ('菜攤', 'cabbage', 'veg')):
        new_game(page); setreq(page, [[item_, 1]]); ev(page, 'Game.bagDone = true; Game.checkDone = true')
        tap(page, '去' + stall_); buy(page, item_, 1); tap(page, '買好了'); ev(page, 'Game.st.floor = 99'); tap(page, '好，'); P = ev(page, 'Game.payInfo()'); tap(page, P['payOk'])
        ev(page, "Game.cc = {bill: 500, ask: 300, want: 200, given: 150, sc: true}; Game.render()")
        o = opts(page); page.locator('#options-area .opt').nth(next(k for k, t_ in enumerate(o) if '好像找錯了' in t_)).click(); page.wait_for_timeout(120)
        check('少找錢被指出來 → 過場畫面是%s拿零錢的尷尬臉' % stall_, state(page) == '_TRANS' and 'stall_%s_change' % key_ in ev(page, "document.getElementById('npc-avatar').src"), (state(page), ev(page, "document.getElementById('npc-avatar').src")))
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
    # 12. 每一關的每個選項（對的、錯的）都按一遍：另開一頁，用 Game.setup() 重來，不用重新載入
    pg2 = ctx.new_page(); errs2 = []; pg2.on('pageerror', lambda e: errs2.append(str(e)[:80]))
    pg2.goto(f'http://127.0.0.1:{PORT}/games/market/index.html'); pg2.wait_for_timeout(400)
    pg2.fill('#player-name-input', 'María'); pg2.click('.btn-primary'); pg2.wait_for_timeout(300)
    pg2.locator('#options-area .opt').first.click(); pg2.wait_for_timeout(100)
    run_options(pg2)
    check('每個選項測試期間沒有 JS 錯誤', errs2 == [], errs2[:2])
    b.close()
# 共用檢查（語言／字體／拼音、任務提示、本關單字、錯誤紀錄面板）：順便跑菜市場這一個
import panels_test
_n, _f, _w = panels_test.check_games(['market'], verbose=False); fails.extend(_f)
print('\n失敗：', fails) if fails else print('\n全部通過')
sys.exit(1 if fails else 0)
