r"""鹽酥雞專用測試：python3 tools/yansuji_test.py
每個選項、每種路線都按過：點卡片、放回去、夾一下換圖、點好了（空籃子）、付錢四個選項（錢夠／阿姨多算／錢不夠）、
錢不夠→拿掉哪一樣（拿 Ami 的／拿自己的／拿了還是不夠）、雞排切不切（沒點雞排就跳過）、阿姨複誦與袋子（對／錯 × 三個選項）、
結局比對（少買／多買／自己多點／切法／辣度／蔥蒜洋蔥）。"""
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('smoke', os.path.join(HERE, 'smoke.py'))
smoke = importlib.util.module_from_spec(spec); sys.modules['smoke'] = smoke; spec.loader.exec_module(smoke)
from playwright.sync_api import sync_playwright

FAILS = []; PASS = [0]
def check(name, ok, info=''):
    if ok: PASS[0] += 1
    else: FAILS.append(f'✗ {name} {info}'); print('✗', name, info)

def new_page(b, vp=None):
    ctx = b.new_context(viewport=vp or {'width': 1000, 'height': 900}); ctx.route('**/*', smoke.route)
    page = ctx.new_page(); errs = []
    page.on('pageerror', lambda e: errs.append(str(e))); page.on('dialog', lambda d: d.accept())
    page.goto(f'http://127.0.0.1:{smoke.PORT}/games/yansuji/index.html'); page.wait_for_timeout(300)
    page.fill('#player-name-input', 'María'); page.click('.btn-primary'); page.wait_for_timeout(200)
    page.errs = errs; return page

def opts(page): return smoke.texts(page)
def press(page, text):
    o = opts(page); i = next((k for k, x in enumerate(o) if x.strip() == text), None)
    assert i is not None, (text, o, page.evaluate('Game.state'))
    smoke.click_i(page, i)
def leave_trans(page):
    while page.evaluate('Game.state') == '_TRANS': page.locator('#options-area .opt').first.click()
def st(page): return page.evaluate('Game.state')
def mis(page): return page.evaluate('Game.mistakes')
def to_item(page): press(page, '走到攤位前'); leave_trans(page); assert st(page) == 'ITEM'
def fill(page, d):   # 照卡片一份一份夾（走真正的點擊入口）
    for zh, n in d.items():
        for _ in range(n): page.evaluate("z=>Game.handleChoice('夾:'+z)", zh)
def to_pay(page, d, cash=None, wrong=None):
    to_item(page); fill(page, d)
    if cash is not None: page.evaluate('c=>{Game.task.cash=c}', cash)
    press(page, '點好了。'); assert st(page) == 'PAY', st(page)
    if wrong is not None:   # 指定阿姨這次有沒有多算（錢夠才會多算）
        page.evaluate("""w=>{const t=Game.task;t.payWrong=w;t.said=w?t.total+t.extra.price:t.total;t.bill=billFor(t.total);t.change=t.bill-t.total;t.changeWrong=false;t.given=t.change;Game.render()}""", wrong)
def pay_opts(page):
    t = page.evaluate('({total:Game.task.total,said:Game.task.said,cash:Game.task.cash,bill:Game.task.bill,extra:Game.task.extra.price})'); return t

def run(b):
    # ── 1. 卡片、夾一下、放回去、空籃子 ──
    p = new_page(b); to_item(p)
    check('16張卡片', p.locator('.food').count() == 16)
    check('卡片有單價', all('元' in x for x in p.locator('.food .pr').all_inner_texts()))
    check('每張圖載得到', p.evaluate("[...document.querySelectorAll('.food img')].every(i=>i.complete&&i.naturalWidth>0)"))
    check('起始圖是pick', 'pick.jpg' in p.evaluate("document.getElementById('npc-avatar').getAttribute('src')"))
    p.locator('.food').first.click()
    check('點一下→喀（換成click圖）', 'pick_click.jpg' in p.evaluate("document.getElementById('npc-avatar').getAttribute('src')"))
    p.wait_for_timeout(600)
    check('0.4秒後換回pick', p.evaluate("document.getElementById('npc-avatar').getAttribute('src')").endswith('pick.jpg'))
    for i in range(16): p.locator('.food').nth(i).click()
    check('每張卡片點一次＝各一份', p.evaluate('Object.values(Game.basket).every(v=>v>=1)&&Object.keys(Game.basket).length===16'))
    p.locator('.food').first.click()
    check('同一張再點一次＝再多一份', p.evaluate("Game.basket['鹽酥雞']") == 3)
    check('籃子顯示× 3', '× 3' in p.locator('.basket').inner_text())
    p.locator('.put').first.click()
    check('放回去少一份', p.evaluate("Game.basket['鹽酥雞']") == 2)
    for z in list(p.evaluate('Object.keys(Game.basket)')):
        for _ in range(p.evaluate('z=>Game.basket[z]||0', z)): p.evaluate('z=>Game.putBack(z)', z)
    check('全部放回去＝空籃子', p.locator('.basket .empty').count() == 1 and st(p) == 'ITEM')
    m0 = mis(p); press(p, '點好了。')
    check('空籃子按點好了：留在點菜、不扣分', st(p) == 'ITEM' and mis(p) == m0)
    check('籃子旁邊有「你身上有」和金額', p.locator('.basket .cash').count() == 1 and str(p.evaluate('Game.task.cash')) in p.locator('.basket .cash').inner_text())
    check('任務提示有身上的錢', '你身上有' in p.evaluate("Game.listHTML(true).map(x=>x.zh).join('')"))
    p.close()

    # ── 2. 付錢：錢夠、阿姨報價對 ──
    for wrong in (False, True):
        for pick_ in ('pay', 'fix', 'short', 'rude'):
            p = new_page(b); to_pay(p, {'雞排': 1, '四季豆': 1}, cash=300, wrong=wrong)
            i = pay_opts(p); t = i['total']
            texts = opts(p); check(f'PAY四個選項 wrong={wrong}', len(texts) == 4, texts)
            payOk = f"給你{p.evaluate('zhNum(Game.task.payWrong?billFor(Game.task.said):Game.task.bill)')}元。"
            fixT = '不好意思，好像算錯了，應該是' + p.evaluate('zhNum(Game.task.payWrong?Game.task.total:Game.task.total+Game.task.extra.price)') + '元吧？'
            SHORT = '不好意思，我的錢不夠，有一樣不要了。'; RUDE = '你是不是想騙我的錢啊？'
            choice = {'pay': payOk, 'fix': fixT, 'short': SHORT, 'rude': RUDE}[pick_]
            right = {'pay': not wrong, 'fix': wrong, 'short': False, 'rude': False}[pick_]
            m0 = mis(p); press(p, choice)
            if right:
                check(f'PAY 正解 {pick_} wrong={wrong} 不扣分', mis(p) == m0)
                check(f'PAY 正解 {pick_} wrong={wrong} 進{st(p)}', st(p) in ('PAY_FIX', 'CHANGE', '_TRANS', 'CUT'), st(p))
            else:
                check(f'PAY 錯誤 {pick_} wrong={wrong} 扣10分並留在PAY', mis(p) == m0 + 1 and st(p) == 'PAY', (mis(p), st(p)))
            p.close()
    # 實際例子：點了270元，付的錢是300（不會因為阿姨多算就變成350）
    p = new_page(b); to_pay(p, {'雞排': 1, '鹽酥雞': 1, '魷魚': 1, '雞塊': 1}, cash=350)   # 75+60+60+45=240
    p.evaluate("Game.basket={'雞排':1,'鹽酥雞':1,'魷魚':1,'地瓜':1};Game.requote();Game.task.payWrong=false;Game.task.said=Game.task.total;Game.render()")   # 75+60+60+40=235
    t = p.evaluate('({total:Game.task.total,bill:Game.task.bill})'); check('235元付250', t['total'] == 235 and t['bill'] == 250, t); p.close()
    p = new_page(b); to_pay(p, {'雞排': 1, '鹽酥雞': 1, '魷魚': 1, '米血': 1, '熱狗': 1, '蘿蔔糕': 1}, cash=400)   # 75+60+60+15+20+35=265
    for _ in range(60):
        p.evaluate("Game.requote();Game.render()")
        t = p.evaluate('({total:Game.task.total,bill:Game.task.bill,said:Game.task.said,w:Game.task.payWrong})')
        if not (t['bill'] == -(-t['total'] // 50) * 50): check('付的錢永遠是真總價湊50', False, t); break
    else: check('付的錢永遠是真總價湊50（含阿姨多算時）', True)
    p.close()
    # 錢夠卻說「錢不夠」的原因文字
    p = new_page(b); to_pay(p, {'雞排': 1}, cash=300, wrong=False); press(p, '不好意思，我的錢不夠，有一樣不要了。')
    check('錢夠卻說不夠：說明錢是夠的', '錢是夠的' in p.evaluate('Game.log[Game.log.length-1].zh')); p.close()

    # ── 3. 錢不夠：自己發現 → 說錢不夠 → 拿掉哪一樣 ──
    for pick_ in ('pay', 'fix', 'short', 'rude'):
        p = new_page(b); to_pay(p, {'雞排': 1, '鹽酥雞': 2, '魷魚': 1}, cash=200)   # 75+120+60=255 > 200
        check('錢不夠：阿姨照實報價、沒提醒', p.evaluate('Game.task.said===Game.task.total&&Game.task.total>Game.task.cash'))
        check('錢不夠：阿姨沒有說錢不夠', '不夠' not in p.locator('#npc-dialogue').inner_text())
        payOk = f"給你{p.evaluate('zhNum(Game.task.bill)')}元。"
        fixT = '不好意思，好像算錯了，應該是' + p.evaluate('zhNum(Game.task.total+Game.task.extra.price)') + '元吧？'
        choice = {'pay': payOk, 'fix': fixT, 'short': '不好意思，我的錢不夠，有一樣不要了。', 'rude': '你是不是想騙我的錢啊？'}[pick_]
        m0 = mis(p); press(p, choice)
        if pick_ == 'short':
            check('錢不夠說對了：不扣分、進REMOVE', mis(p) == m0 and st(p) in ('REMOVE', '_TRANS'), st(p)); leave_trans(p)
            check('REMOVE 選項＝籃子裡每一樣', sorted(opts(p)) == sorted(['雞排不要了。', '鹽酥雞不要了。', '魷魚不要了。']), opts(p))
        else:
            check(f'錢不夠 {pick_}：扣10分留在PAY', mis(p) == m0 + 1 and st(p) == 'PAY', (mis(p), st(p)))
        p.close()
    # 拿掉自己的魷魚 → 剛好夠 → 付錢 → 找錢 → 切 → 辣 → 蔥蒜 → 複誦 → 袋子 → 結局（Ami 要的都在）
    p = new_page(b); to_pay(p, {'雞排': 1, '鹽酥雞': 1, '魷魚': 1}, cash=200)   # 195 ≤ 200 其實夠；改成不夠
    p.evaluate("Game.task.cash=150; Game.requote(); Game.render()")
    check('改成150：不夠', p.evaluate('Game.task.total>Game.task.cash'))
    press(p, '不好意思，我的錢不夠，有一樣不要了。'); leave_trans(p)
    press(p, '魷魚不要了。'); leave_trans(p)
    check('拿掉後重新報價（135）', st(p) == 'PAY' and p.evaluate('Game.task.total') == 135 and '魷魚' not in p.evaluate('Object.keys(Game.basket)'), p.evaluate('Game.task.total'))
    check('拿掉後135≤150 就可以付', p.evaluate('Game.task.total<=Game.task.cash'))
    p.close()
    # 拿了一樣還是不夠 → 再來一次
    p = new_page(b); to_pay(p, {'雞排': 1, '鹽酥雞': 1, '魷魚': 1, '雞塊': 1}, cash=200)   # 240
    press(p, '不好意思，我的錢不夠，有一樣不要了。'); leave_trans(p); press(p, '雞塊不要了。'); leave_trans(p)   # 195 ≤ 200 夠
    p.evaluate("Game.task.cash=100; Game.requote(); Game.render()")
    check('還是不夠：還在PAY、可以再說一次', st(p) == 'PAY' and p.evaluate('Game.task.total>Game.task.cash'))
    press(p, '不好意思，我的錢不夠，有一樣不要了。'); leave_trans(p)
    press(p, '魷魚不要了。'); leave_trans(p)
    check('第二次拿掉後重新報價', st(p) == 'PAY' and p.evaluate('Game.task.total') == 135)
    p.close()
    # 全部拿光 → 回點菜
    p = new_page(b); to_pay(p, {'雞排': 1}, cash=50)
    press(p, '不好意思，我的錢不夠，有一樣不要了。'); leave_trans(p); press(p, '雞排不要了。'); leave_trans(p)
    check('全部拿掉→回到點菜', st(p) == 'ITEM' and p.evaluate('Game.orderList().length') == 0)
    p.close()

    # ── 4. 付完錢之後：沒點雞排跳過 CUT；有雞排有 CUT；兩個切法 ──
    p = new_page(b); to_pay(p, {'四季豆': 1}, cash=200, wrong=False); press(p, f"給你{p.evaluate('zhNum(Game.task.bill)')}元。"); leave_trans(p)
    if st(p) == 'CHANGE': press(p, '好，謝謝。'); leave_trans(p)
    check('沒點雞排：跳過CUT直接問辣度', st(p) == 'SPICY', st(p))
    check('付完錢身上的錢減少', p.evaluate('Game.task.cash') == 200 - 30)
    check('標籤顯示剩下的錢', '170' in p.locator('#cash-badge').inner_text())
    p.close()
    for cut in (True, False):
        p = new_page(b); to_pay(p, {'雞排': 1}, cash=200, wrong=False); press(p, f"給你{p.evaluate('zhNum(Game.task.bill)')}元。"); leave_trans(p)
        if st(p) == 'CHANGE': press(p, '好，謝謝。'); leave_trans(p)
        check('有雞排：進CUT', st(p) == 'CUT')
        o = opts(p); check('CUT兩個選項', sorted(o) == ['不用切。', '要切。'])
        m0 = mis(p); press(p, '要切。' if cut else '不用切。'); leave_trans(p)
        check('CUT 兩種都不當場扣分', mis(p) == m0 and st(p) == 'SPICY')
        o = opts(p); check('SPICY三個選項', len(o) == 3)
        for s in o: pass
        press(p, '大辣。'); leave_trans(p)
        check('TOPS四個選項、含Ami說的那一種', len(opts(p)) == 4 and p.evaluate('Game.task.topOpts.includes(topsOpt(Game.task.tops))'))
        press(p, opts(p)[0]); leave_trans(p)
        check('選完蔥蒜洋蔥→複誦', st(p) == 'ORDER_CHECK')
        p.close()

    # ── 4b. 阿姨道歉的畫面用尷尬臉 ──
    p = new_page(b); to_item(p); fill(p, {'雞排': 1, '鹽酥雞': 2})
    av = lambda: p.evaluate("document.getElementById('npc-avatar').getAttribute('src')")
    p.evaluate("()=>{Game.state='PAY_FIX';Game.render()}")
    check('PAY_FIX（阿姨算錯）用 pay_sorry', av() == 'images/pay_sorry.jpg', av())
    p.evaluate("()=>{const t=Game.task;t.changeWrong=true;Game.state='CHANGE';Game.render()}")
    check('CHANGE 還沒抓到：用一般 pay', av() == 'images/pay.jpg', av())
    p.evaluate("()=>{Game.task.changeWrong=false;Game.state='CHANGE';Game.render()}")
    check('CHANGE 找對：用一般 pay', av() == 'images/pay.jpg', av())
    p.close()

    # ── 5. 複誦、袋子：對／錯 × 三個選項（照「你點的」核對） ──
    for where in ('ORDER_CHECK', 'HANDOVER'):
        for wrong in (False, True):
            for ch in ('ok', 'fix', 'rude'):
                p = new_page(b); to_item(p); fill(p, {'雞排': 1, '鹽酥雞': 2})
                p.evaluate("""([w,wrong])=>{const t=Game.task;t.cash=300;t.pCut=true;t.pSpicy=SPICY[1];t.pTops=[true,false,true];Game.buildChecks();
                  if(w==='ORDER_CHECK'){t.ocWrong=wrong;t.ocSaid={...t.truth,...(wrong?{[t.ocKind]:t.ocFlip}:{})};}else{t.hoWrong=wrong;t.hoGot={...t.truth,...(wrong?{[t.hoKind]:t.hoFlip}:{})};}
                  Game.state=w;Game.render();}""", [where, wrong])
                T = p.evaluate('({k:Game.task.ocKind,hk:Game.task.hoKind})')
                texts = opts(p); check(f'{where} 三個選項', len(texts) == 3, texts)
                kind = p.evaluate('w=>w==="ORDER_CHECK"?Game.task.ocKind:Game.task.hoKind', where)
                fix = p.evaluate('([w,wrong])=>{const t=Game.task,k=w==="ORDER_CHECK"?t.ocKind:t.hoKind;const fl=w==="ORDER_CHECK"?t.ocFlip:t.hoFlip,i=w==="ORDER_CHECK"?t.ocIdx:t.hoIdx;return OC.fix(k,wrong?t.truth[k]:fl,i)}', [where, wrong])
                choice = {'ok': '對，沒錯。' if where == 'ORDER_CHECK' else '好，謝謝。', 'fix': fix, 'rude': '你到底有沒有在聽啊？' if where == 'ORDER_CHECK' else '你是不是耳朵有問題？我說的不是這個！'}[ch]
                right = (ch == 'fix') if wrong else (ch == 'ok')
                m0 = mis(p); press(p, choice)
                check(f'{where} wrong={wrong} {ch} ({kind})', (mis(p) == m0) if right else (mis(p) == m0 + 1 and st(p) == where), (mis(p), st(p)))
                src = p.evaluate("document.getElementById('npc-avatar').getAttribute('src')")
                want = ('images/stall_sorry.jpg' if where == 'ORDER_CHECK' else 'images/bag_sorry.jpg') if (wrong and ch == 'fix') else \
                       ('images/stall.jpg' if where == 'ORDER_CHECK' else 'images/bag.jpg')
                check(f'{where} wrong={wrong} {ch} 圖片：{want}', src == want, src)
                p.close()
    # 複誦的每一種錯法都要能指出來：數量／切法／辣度／蔥蒜洋蔥
    for kind in ('items', 'cut', 'spicy', 'tops'):
        p = new_page(b); to_item(p); fill(p, {'雞排': 1, '鹽酥雞': 2})
        p.evaluate("""k=>{const t=Game.task;t.cash=300;t.pCut=false;t.pSpicy=SPICY[0];t.pTops=[true,true,false];Game.buildChecks();
          t.ocWrong=true;t.ocKind=k;t.ocFlip=flipOf(t.truth,k);t.ocIdx=k==='items'?diffIdx(t.truth.items,t.ocFlip):0;t.ocSaid={...t.truth,[k]:t.ocFlip};Game.state='ORDER_CHECK';Game.render();}""", kind)
        said = p.locator('#npc-dialogue').inner_text()
        fix = p.evaluate("OC.fix(Game.task.ocKind,Game.task.truth[Game.task.ocKind],Game.task.ocIdx)")
        m0 = mis(p); press(p, fix)
        check(f'複誦錯在{kind}：指出來正確', mis(p) == m0, (said, fix)); p.close()

    # ── 6. 結局比對 ──
    def finish(p, d, cut=None, spicy=None, tops=None, ami=None):
        """直接設定 Ami 的要求和玩家的選擇，走到 END 看結果"""
        to_item(p)
        p.evaluate("""([ami,cut,spicy,tops])=>{const t=Game.task;
          t.items=ami.map(([z,q])=>({it:ITEM_BY[z],q}));t.cut=cut[0];t.spicy=SPICY[spicy[0]];t.tops=tops[0];
          t.pCut=cut[1];t.pSpicy=SPICY[spicy[1]];t.pTops=tops[1];t.cash=300}""", [ami, cut, spicy, tops])
        fill(p, d)
        p.evaluate("Game.buildChecks();Game.stopTimer();Game.state='END';Game.render()")
        return p.evaluate('[Game._endGood, Game.mistakes, Game.log.map(m=>m.zh)]')
    A = [('雞排', 1), ('四季豆', 1), ('杏鮑菇', 2)]; same = ([True, True], [1, 1], [[True, True, False]] * 2)
    def case(name, d, cut=(True, True), spicy=(1, 1), tops=([True, True, False], [True, True, False]), good=True, nmis=0, ami=A):
        p = new_page(b); good_, m, log = finish(p, d, list(cut), list(spicy), list(tops), ami)
        check(f'結局 {name}：{"好" if good else "壞"}結局', good_ == good, (good_, m, log))
        check(f'結局 {name}：扣分{nmis}次', m == nmis, (m, log))
        if good: check(f'結局 {name}：好結局圖', 'end_good' in p.evaluate("document.getElementById('npc-avatar').getAttribute('src')"))
        else: check(f'結局 {name}：壞結局圖', 'end_bad' in p.evaluate("document.getElementById('npc-avatar').getAttribute('src')"))
        check(f'結局 {name}：沒有網頁錯誤', not p.errs, p.errs); p.close()
    case('全對', {'雞排': 1, '四季豆': 1, '杏鮑菇': 2})
    case('自己多點別的（不比對）', {'雞排': 1, '四季豆': 1, '杏鮑菇': 2, '熱狗': 1, '地瓜': 1})
    case('Ami的東西多買（不扣分）', {'雞排': 1, '四季豆': 2, '杏鮑菇': 3})
    case('少買一樣（沒買四季豆）', {'雞排': 1, '杏鮑菇': 2}, good=False, nmis=1)
    case('杏鮑菇只買一份', {'雞排': 1, '四季豆': 1, '杏鮑菇': 1}, good=False, nmis=1)
    case('沒買雞排（切法不比）', {'四季豆': 1, '杏鮑菇': 2}, good=False, nmis=1)
    case('雞排切法不對', {'雞排': 1, '四季豆': 1, '杏鮑菇': 2}, cut=(True, False), good=False, nmis=1)
    case('辣度不對', {'雞排': 1, '四季豆': 1, '杏鮑菇': 2}, spicy=(1, 2), good=False, nmis=1)
    case('蔥蒜洋蔥不對', {'雞排': 1, '四季豆': 1, '杏鮑菇': 2}, tops=([True, True, False], [True, True, True]), good=False, nmis=1)
    case('全都錯', {'魷魚': 1}, cut=(True, False), spicy=(0, 2), tops=([True, True, False], [False, False, True]), good=False, nmis=3 + 3 - 0 if False else 5)

    # ── 6b. Ami 點的東西 4～5 項、身上的錢、開頭那句、結局的說法 ──
    p = new_page(b)
    r_ = p.evaluate("""()=>{const out=[];for(let i=0;i<300;i++){Game.setup();const t=Game.task,tot=sum(t.items.map(x=>x.it.p*x.q));out.push([t.items.length,tot,t.cash,t.items.filter(x=>x.it===STEAK).length,new Set(t.items.map(x=>x.it.zh)).size===t.items.length])}return out}""")
    check('Ami 點 4～5 項', all(n in (4, 5) for n, *_ in r_) and {n for n, *_ in r_} == {4, 5})
    check('Ami 總價≤250、永遠付得起', all(tot <= 250 and cash >= tot for _, tot, cash, *_ in r_))
    check('身上的錢是50的倍數、至少多出50（夠買自己的）', all(cash % 50 == 0 and cash >= tot + 50 for _, tot, cash, *_ in r_))
    check('每次一定有雞排、品項不重複', all(c == 1 and u for *_, c, u in r_))
    first = p.evaluate("Game.amiLines()[0].zh")
    check('Ami 開頭第一句', '幫我買一下鹽酥雞可以嗎？你看你要吃什麼，再自己點。' in first, first)
    check('Ami 第二句只有一個「我要」', p.evaluate("Game.amiLines()[1].zh").count('我要') == 1, p.evaluate("Game.amiLines()[1].zh"))
    p.close()
    def dtext(p): return p.evaluate("(()=>{const c=document.getElementById('npc-dialogue').cloneNode(true);c.querySelectorAll('rt').forEach(r=>r.remove());return c.textContent})()")
    B = [('雞排', 1), ('四季豆', 1), ('杏鮑菇', 2), ('熱狗', 1)]
    p = new_page(b); finish(p, {'雞排': 1, '四季豆': 1, '杏鮑菇': 2, '熱狗': 1}, [True, True], [1, 1], [[True, True, False]] * 2, A)
    check('好結局＋另外買了熱狗：沒有問自己要吃的', '沒有買自己要吃的' not in dtext(p) and p.evaluate('Game._endGood')); p.close()
    p = new_page(b); finish(p, {'雞排': 1, '四季豆': 1, '杏鮑菇': 3}, [True, True], [1, 1], [[True, True, False]] * 2, A)
    check('只是多買Ami的杏鮑菇：算有買自己的', '沒有買自己要吃的' not in dtext(p)); p.close()
    p = new_page(b); finish(p, {'雞排': 1, '四季豆': 1, '杏鮑菇': 2}, [True, True], [1, 1], [[True, True, False]] * 2, A)
    check('好結局＋只買Ami的：Ami問「你沒有買自己要吃的喔？」', '你沒有買自己要吃的喔' in dtext(p) and p.evaluate('Game._endGood'), dtext(p)); p.close()
    p = new_page(b); finish(p, {'雞排': 1, '杏鮑菇': 1}, [True, True], [1, 1], [[True, True, False]] * 2, A)
    tx = dtext(p)
    check('壞結局：沒買齊的東西併成一句（只列沒買齊的）', tx.count('你沒有買齊耶') == 1 and '一份四季豆' in tx and '兩份杏鮑菇' in tx and '一片雞排' not in tx, tx)
    check('壞結局：每項仍各扣分', p.evaluate('Game.mistakes') == 2, p.evaluate('Game.mistakes'))
    check('壞結局＋沒買自己的：也會問', '你沒有買自己要吃的喔' in tx); p.close()
    p = new_page(b); finish(p, {'雞排': 1, '四季豆': 1, '杏鮑菇': 2}, [True, False], [1, 1], [[True, True, False]] * 2, A)
    tx = dtext(p); check('只錯切法：沒有「沒買齊」那句', '沒有買齊' not in tx and '雞排我說' in tx, tx); p.close()
    # 袋子畫面：食物照片＋份數、雞排切法、辣度、蔥蒜洋蔥打勾
    p = new_page(b); to_item(p); fill(p, {'雞排': 1, '鹽酥雞': 2})
    p.evaluate("""()=>{const t=Game.task;t.cash=300;t.pCut=true;t.pSpicy=SPICY[2];t.pTops=[true,false,true];Game.buildChecks();t.hoWrong=false;t.hoGot={...t.truth};Game.state='HANDOVER';Game.render()}""")
    check('袋子：每樣食物一張照片', p.locator('.bag .bi img').count() == 2 and p.evaluate("[...document.querySelectorAll('.bag .bi img')].every(i=>i.complete&&i.naturalWidth>0)"))
    check('袋子：份數', sorted(x.strip() for x in p.locator('.bag .cnt').all_inner_texts()) == ['× 1', '× 2'])
    check('袋子：蔥蒜洋蔥打勾（蔥✓蒜空洋蔥✓）', p.evaluate("[...document.querySelectorAll('.bag .ck')].map(e=>e.classList.contains('on'))") == [True, False, True])
    check('袋子：不再有粉紅購物袋表情符號', '🛍' not in p.locator('.bag').inner_text()); p.close()

    # ── 7. 手機版面 ──
    p = new_page(b, {'width': 390, 'height': 800}); to_item(p)
    check('手機：三欄', p.evaluate("getComputedStyle(document.querySelector('.shelf')).gridTemplateColumns.split(' ').length") == 3)
    check('手機：沒有橫向捲動', p.evaluate('document.documentElement.scrollWidth<=window.innerWidth+1'))
    p.close()

with sync_playwright() as pw:
    b = pw.chromium.launch(); run(b); b.close()
print(f'通過 {PASS[0]} 項，失敗 {len(FAILS)} 項')
for f in FAILS: print(f)
sys.exit(1 if FAILS else 0)
