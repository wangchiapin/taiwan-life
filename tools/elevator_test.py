r"""搭電梯專用測試：python3 tools/elevator_test.py
三種「對方出錯」每個選項都按過（強制出現，不靠運氣）：
  DIR   大廳先開門的電梯是往下的，阿姨問「是往上的嗎？」：對／客氣提醒／沒禮貌；沒有這一關時直接去 WAIT
  HELP2 鄰居說錯樓層：客氣回應／翻舊帳／不管他
  STOP  電梯停在低一層，鄰居看錯想出去：慢走／客氣提醒／沒禮貌；沒看錯時，亂提醒要扣分；提醒後 STOP_FIX 再來一次
還檢查：每局隨機的條件（m 是 3 或 4、早停樓層在 e 和 Ami 之間）、
過場用的尷尬臉圖片、錯誤紀錄有關卡名稱、小字典的字都出現在那一關的畫面上、三個面板的語言。"""
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
    page.goto(f'http://127.0.0.1:{smoke.PORT}/games/elevator/index.html'); page.wait_for_timeout(300)
    page.fill('#player-name-input', 'María'); page.click('.btn-primary'); page.wait_for_timeout(200)
    page.errs = errs; return page

def opts(page): return smoke.texts(page)
def press(page, text):
    o = opts(page); i = next((k for k, x in enumerate(o) if x.strip() == text), None)
    assert i is not None, (text, o, page.evaluate('Game.state'))
    smoke.click_i(page, i)
def st(page): return page.evaluate('Game.state')
def mis(page): return page.evaluate('Game.mistakes')
def trans_from(page): return page.evaluate("Game.state==='_TRANS'?Game._trans.from:null")
def leave_trans(page):
    while st(page) == '_TRANS': page.locator('#options-area .opt').first.click()
def img(page): return page.evaluate('Game._anim0||""')   # 現在要顯示的圖（圖檔還沒畫好時也看得到檔名）
def txt(page, sel):   # 某個區塊的字（先拿掉拼音 <rt>，不然拼音會混進來）
    return page.evaluate("s=>{const e=document.querySelector(s);if(!e)return '';const c=e.cloneNode(true);c.querySelectorAll('rt').forEach(r=>r.remove());return c.textContent}", sel)
def screen(page):   # 這一關畫面上的字（對話＋選項＋樓層顯示器）
    return txt(page, '#npc-dialogue') + ' ' + ' '.join(opts(page)) + ' ' + txt(page, '.elev')
def disp(page): return page.evaluate("(document.querySelector('.elev .disp')||{innerText:''}).innerText")

def set_task(page, n=8, m=3, misspoke=False, dirDown=False, stopWrong=False, early=False, unit=2, evt='CHAT'):
    """把這一局的隨機條件固定下來（和 setup() 的規則一致）"""
    page.evaluate("""o=>{const t=Game.task; Object.assign(t,{n:o.n,m:o.m,misspoke:o.misspoke,e:o.misspoke?o.m+1:o.m,dirDown:o.dirDown,stopWrong:o.stopWrong,unit:o.unit,evt:o.evt}); Game.wrongUnit=null;
      const xs=Array.from({length:t.n-t.e-1},(_,i)=>t.e+1+i); t.x=xs.length?xs[0]:null; t.early=o.early&&xs.length>0; Game.render();}""",
      dict(n=n, m=m, misspoke=misspoke, dirDown=dirDown, stopWrong=stopWrong, early=early, unit=unit, evt=evt))

EVTS = ('CHAT', 'FART', 'DOG')
EVT_OK = {'CHAT': '對啊，真的很熱。', 'FART': '（假裝沒聞到）', 'DOG': '沒關係，牠很可愛。'}
def guard_ok(page): t = page.evaluate('Game.task'); return f"我要找朋友，她住在{t['n']}樓之{t['unit']}。"
def to_guard(page): press(page, '走進大樓'); leave_trans(page); assert st(page) == 'GUARD', st(page)
def to_lobby(page): to_guard(page); press(page, guard_ok(page)); leave_trans(page); assert st(page) == 'LOBBY', st(page)
def evt_ok(page):   # 電梯裡的小插曲（若有）答對；之後停在 STOP
    if st(page) in EVTS: press(page, EVT_OK[st(page)])
def to_help(page):   # LOBBY 之後到 HELP（DIR 若有，先答對）
    press(page, '按▲，往上。'); leave_trans(page)
    if st(page) == 'DIR': press(page, '不好意思，這部是往下的。'); leave_trans(page)
    assert st(page) == 'WAIT', st(page)
    press(page, '按「開門」，等他。'); leave_trans(page); assert st(page) == 'FLOOR', st(page)
    press(page, f"按{page.evaluate('Game.task.n')}樓。"); leave_trans(page); assert st(page) == 'HELP', st(page)
def help_right(page):
    t = page.evaluate('({m:Game.task.m})')
    press(page, f"好，我幫你按{t['m']}樓。")

def run(b):
    # ── 1. 每局隨機條件的規則（setup 跑 300 次）──
    p = new_page(b)
    bad = p.evaluate("""()=>{const r=[];for(let i=0;i<300;i++){Game.setup();const t=Game.task;
      if(![3,4].includes(t.m))r.push('m'+t.m); if(t.e!==(t.misspoke?t.m+1:t.m))r.push('e');
      if(t.e>=t.n)r.push('e>=n'); if(t.early&&!(t.x>t.e&&t.x<t.n))r.push('x'+t.x+'e'+t.e+'n'+t.n); if(!t.early&&t.x!=null&&!(t.x>t.e&&t.x<t.n))r.push('x2');
      if(t.e-1<2)r.push('e-1<2');}
      const seen={misspoke:0,dirDown:0,stopWrong:0,early:0};for(let i=0;i<300;i++){Game.setup();for(const k in seen)if(Game.task[k])seen[k]++;}
      return {r:[...new Set(r)],seen}}""")
    check('每局隨機條件都符合規則', not bad['r'], bad['r'])
    check('三種錯誤、早停都會出現（300 局）', all(v > 0 for v in bad['seen'].values()), bad['seen'])
    p.close()

    # ── 2. DIR：阿姨問「這部是往上的嗎？」──
    p = new_page(b); set_task(p, dirDown=False); to_lobby(p)
    press(p, '按▲，往上。'); leave_trans(p)
    check('dirDown=False：大廳之後直接 WAIT（沒有 DIR）', st(p) == 'WAIT')
    p.close()
    for first in ('ok', 'rude', 'fix'):
        p = new_page(b); set_task(p, dirDown=True); to_lobby(p)
        press(p, '按▲，往上。'); leave_trans(p)
        check('dirDown=True：大廳之後是 DIR', st(p) == 'DIR', st(p))
        check('DIR 電梯上面是▼', '▼' in disp(p), disp(p))
        check('DIR 阿姨的話', '請問，這部是往上的嗎？' in screen(p), screen(p))
        check('DIR 三個選項', sorted(o.strip() for o in opts(p)) == sorted(['對，往上，請進。', '不好意思，這部是往下的。', '你自己不會看嗎？']), opts(p))
        check('DIR 開始的圖是 dir.jpg', img(p).endswith('dir.jpg'), img(p))
        m0 = mis(p)
        if first != 'fix':
            press(p, '對，往上，請進。' if first == 'ok' else '你自己不會看嗎？')
            check(f'DIR 選「{first}」：扣分、留在 DIR', mis(p) == m0 + 1 and st(p) == 'DIR', (mis(p), st(p)))
            check('DIR 錯誤紀錄有關卡名稱', p.evaluate('Game.log[Game.log.length-1].stage[0]') == '看箭頭', p.evaluate('Game.log[Game.log.length-1].stage'))
        press(p, '不好意思，這部是往下的。')
        check('DIR 客氣提醒：進過場、不扣分', st(p) == '_TRANS' and trans_from(p) == 'DIR' and mis(p) == m0 + (0 if first == 'fix' else 1), (st(p), mis(p)))
        check('DIR 過場：阿姨不好意思（dir_sorry.jpg）', img(p).endswith('dir_sorry.jpg'), img(p))
        tx = txt(p, '#npc-dialogue')
        check('DIR 過場：阿姨的道歉＋新來的電梯', '是往下的！不好意思，謝謝你！' in tx and '電梯又來了，這次上面亮著▲' in tx, tx)
        check('DIR 過場：第一次就對才有綠卡', (p.locator('.fb.good').count() == 1) == (first == 'fix'), p.locator('.fb.good').count())
        leave_trans(p); check('DIR 之後是 WAIT', st(p) == 'WAIT' and not disp(p).startswith('▼'), (st(p), disp(p)))
        p.close()

    # ── 3. HELP2：鄰居說錯樓層 ──
    for first in ('rude1', 'rude2', None):
        p = new_page(b); set_task(p, misspoke=True); to_lobby(p); to_help(p)
        check('HELP 鄰居說要到 m 樓', '3樓' in screen(p) and '面板上' not in screen(p), screen(p))
        help_right(p)
        check('HELP 答對之後是過場（旁白：你按了3樓）', st(p) == '_TRANS' and trans_from(p) == 'HELP' and '你按了3樓' in txt(p, '#npc-dialogue'))
        leave_trans(p); check('接著是 HELP2', st(p) == 'HELP2', st(p))
        check('HELP2 鄰居改口', '我說錯了！我是要到4樓' in screen(p), screen(p))
        check('HELP2 三個選項', sorted(o.strip() for o in opts(p)) == sorted(['沒關係，我幫你按4樓。', '你剛剛明明說3樓！', '那你自己按吧。']), opts(p))
        check('HELP2 圖是 neighbor_sorry.jpg', img(p).endswith('neighbor_sorry.jpg'), img(p))
        m0 = mis(p)
        if first:
            press(p, '你剛剛明明說3樓！' if first == 'rude1' else '那你自己按吧。')
            check(f'HELP2 選「{first}」：扣分、留在 HELP2', mis(p) == m0 + 1 and st(p) == 'HELP2')
            check('HELP2 錯誤紀錄有關卡名稱', p.evaluate('Game.log[Game.log.length-1].stage[0]') == '鄰居改口')
        press(p, '沒關係，我幫你按4樓。'); check('HELP2 客氣回應：直接進電梯小插曲（合併，不跳過場）', st(p) in EVTS, st(p))
        check('HELP2 合併頁：第一次就對才有綠卡', (p.locator('.fb.good').count() == 1) == (first is None))
        evt_ok(p); leave_trans(p); check('HELP2 之後是 STOP（停在4樓，沒看錯）', st(p) == 'STOP' and p.evaluate('Game.cur') == 4, (st(p), p.evaluate('Game.cur')))
        p.close()

    # ── 電梯按鍵面板：WAIT 只能按開關門、FLOOR 只能按樓層（共 16 顆）──
    p = new_page(b); set_task(p, n=12, m=3); to_lobby(p); press(p, '按▲，往上。'); leave_trans(p)
    check('WAIT：面板有 16 顆按鍵、只有開門／關門能按', p.locator('.ppanel .pb').count() == 16 and sorted(x.strip() for x in opts(p)) == sorted(['按「開門」，等他。', '按「關門」。']), opts(p))
    m0 = mis(p); press(p, '按「關門」。'); check('WAIT 按關門：扣分、留在 WAIT', mis(p) == m0 + 1 and st(p) == 'WAIT')
    press(p, '按「開門」，等他。'); check('WAIT 按開門：過場，按鈕是「鄰居走進電梯」', st(p) == '_TRANS' and '鄰居走進電梯' in txt(p, '#options-area')); leave_trans(p)
    exp = ['按地下2樓。', '按地下1樓。'] + [f'按{k}樓。' for k in range(1, 13)]
    check('FLOOR：14 個樓層鍵（地下2到12樓）都能按、開關門不能按', sorted(opts(p)) == sorted(exp) and p.locator('.ppanel .pb').count() == 16, opts(p))
    check('FLOOR：面板上有「按樓層」', '按樓層' in txt(p, '.pcap'))
    for k in ['按地下2樓。', '按地下1樓。', '按1樓。', '按11樓。', '按13樓。'] if False else ['按地下2樓。', '按地下1樓。', '按1樓。', '按11樓。']:
        m1 = mis(p); press(p, k); check(f'FLOOR 按錯「{k}」：扣分、留在 FLOOR', mis(p) == m1 + 1 and st(p) == 'FLOOR')
    p.screenshot(path='/tmp/panel_floor.png')
    press(p, '按12樓。'); check('FLOOR 按對 12 樓：進 HELP', st(p) == 'HELP')
    p.close()
    p = new_page(b); set_task(p, n=12, m=3); to_lobby(p); press(p, '按▲，往上。'); leave_trans(p); p.screenshot(path='/tmp/panel_wait.png'); p.evaluate("Game.showList=true;Game.render()"); p.locator('.list').screenshot(path='/tmp/list.png'); p.close()

    # ── 圖2.3 合併：FLOOR 答對後不跳過場，綠卡＋鄰居的話＋選項在同一頁 ──
    p = new_page(b); set_task(p, n=8, m=3); to_lobby(p); press(p, '按▲，往上。'); leave_trans(p)
    press(p, '按「開門」，等他。'); leave_trans(p); press(p, '按8樓。')
    tx = txt(p, '#npc-dialogue')
    check('FLOOR 答對：直接是 HELP（沒有過場）', st(p) == 'HELP', st(p))
    check('合併頁：有綠卡、鄰居的話只出現一次、有選項', p.locator('.fb.good').count() == 1 and tx.count('麻煩你幫我按一下') == 1 and len(opts(p)) == 3, tx)
    check('任務卡標題：搭電梯上8樓找Ami', '搭電梯上8樓找Ami' in p.evaluate("(()=>{Game.showList=true;Game.render();const e=document.querySelector('.list .t');const c=e.cloneNode(true);c.querySelectorAll('rt').forEach(r=>r.remove());return c.textContent})()"))
    check('NEXT_LABEL STOP_FIX 是「電梯繼續往上」', p.evaluate("NEXT_LABEL.STOP_FIX") == '電梯繼續往上')
    p.close()

    # ── 第三輪修改：綠卡在最上面、HELP 第三個選項、HELP→STOP 合併、ARRIVE 選項與旁白 ──
    fb_first = "(()=>{const b=document.getElementById('npc-dialogue');const f=b.querySelector('.fb'),sp=b.querySelector('.speaker');return !!f&&!!sp&&!!(f.compareDocumentPosition(sp)&Node.DOCUMENT_POSITION_FOLLOWING)})()"
    p = new_page(b); set_task(p, n=8, m=3); to_lobby(p); press(p, '按▲，往上。'); leave_trans(p); press(p, '按「開門」，等他。'); leave_trans(p); press(p, '按8樓。')
    check('FLOOR→HELP 合併頁：綠卡在鄰居的話上面', p.evaluate(fb_first))
    check('HELP 第三個選項是「幹！你不會自己按喔！」、沒有「已經亮了」', sorted(o.strip() for o in opts(p)) == sorted(['好，我幫你按3樓。', '好，我幫你按8樓。', '幹！你不會自己按喔！']), opts(p))
    m0 = mis(p); press(p, '幹！你不會自己按喔！'); check('HELP 選「幹」：扣分、留在 HELP', mis(p) == m0 + 1 and st(p) == 'HELP' and '不要罵人' in txt(p, '.fb.bad'), txt(p, '.fb.bad'))
    p.close()
    p = new_page(b); set_task(p, n=8, m=3, stopWrong=False); to_lobby(p); press(p, '按▲，往上。'); leave_trans(p); press(p, '按「開門」，等他。'); leave_trans(p); press(p, '按8樓。')
    press(p, '好，我幫你按3樓。')
    check('HELP→小插曲 合併：直接是小插曲、綠卡在最上面', st(p) in EVTS and (p.evaluate(fb_first) or st(p) == 'FART'), st(p))   # FART 沒有人說話，沒有 .speaker 可比
    check('小插曲頁：旁白「電梯向上」、有三個選項', '電梯向上' in txt(p, '#npc-dialogue') and len(opts(p)) == 3, txt(p, '#npc-dialogue'))
    press(p, EVT_OK[st(p)])
    tx = txt(p, '#npc-dialogue')
    check('小插曲→STOP 合併：直接是 STOP、綠卡在最上面', st(p) == 'STOP' and p.evaluate(fb_first), st(p))
    check('STOP 合併頁：旁白「電梯在3樓停了下來」、鄰居的話只出現一次、有三個選項', '電梯在3樓停了下來' in tx and tx.count('到了，謝謝你！再見！') == 1 and len(opts(p)) == 3, tx)
    p.close()
    p = new_page(b); set_task(p, n=8, m=3, stopWrong=False, early=False); to_lobby(p); to_help(p); help_right(p); evt_ok(p); leave_trans(p)
    press(p, '不客氣，慢走！'); check('STOP→ARRIVE 過場：只有綠卡、沒有「電梯繼續往上」旁白', st(p) == '_TRANS' and '電梯繼續往上' not in txt(p, '#npc-dialogue') and p.locator('.fb.good').count() == 1, txt(p, '#npc-dialogue')); leave_trans(p)
    check('ARRIVE 沒有「電梯繼續往上，到8樓了」旁白（直接到 ARRIVE）', st(p) == 'ARRIVE' and '電梯繼續往上' not in txt(p, '#npc-dialogue'), (st(p), txt(p, '#npc-dialogue')))
    check('ARRIVE 選項：借過／滾開！別擋路！／用力推開', sorted(o.strip() for o in opts(p)) == sorted(['不好意思，借過一下。', '滾開！別擋路！', '（用力推開）']), opts(p))
    m0 = mis(p); press(p, '滾開！別擋路！'); check('ARRIVE 選「滾開」：扣分', mis(p) == m0 + 1 and st(p) == 'ARRIVE')
    p.close()

    # ── 4. STOP：鄰居看錯樓層（stopWrong）──
    for first in ('ok', 'rude', 'fix'):
        p = new_page(b); set_task(p, stopWrong=True, early=(first == 'fix')); to_lobby(p); to_help(p); help_right(p); evt_ok(p); leave_trans(p)
        check('STOP 停在低一層（2樓）', st(p) == 'STOP' and p.evaluate('Game.cur') == 2 and '2' in disp(p), (st(p), disp(p)))
        check('STOP 三個選項', sorted(o.strip() for o in opts(p)) == sorted(['不客氣，慢走！', '不好意思，這裡是2樓，您是不是要到3樓？', '靠杯！你不是要去3樓？']), opts(p))
        m0 = mis(p)
        if first != 'fix':
            press(p, '不客氣，慢走！' if first == 'ok' else '靠杯！你不是要去3樓？')
            check(f'STOP 選「{first}」：扣分、留在 STOP', mis(p) == m0 + 1 and st(p) == 'STOP', (mis(p), st(p)))
            check('STOP 錯誤紀錄有關卡名稱', p.evaluate('Game.log[Game.log.length-1].stage[0]') == '鄰居下樓')
        press(p, '不好意思，這裡是2樓，您是不是要到3樓？')
        check('STOP 客氣提醒：進過場', st(p) == '_TRANS' and trans_from(p) == 'STOP' and mis(p) == m0 + (0 if first == 'fix' else 1))
        check('STOP 過場：鄰居不好意思（neighbor_sorry.jpg）', img(p).endswith('neighbor_sorry.jpg'), img(p))
        tx = txt(p, '#npc-dialogue')
        check('STOP 過場：道歉＋電梯往上到3樓', '我看錯了！謝謝你提醒我' in tx and '到3樓了' in tx, tx)
        check('STOP 過場：第一次就對才有綠卡', (p.locator('.fb.good').count() == 1) == (first == 'fix'))
        leave_trans(p); check('接著是 STOP_FIX（3樓）', st(p) == 'STOP_FIX' and p.evaluate('Game.cur') == 3 and '3' in disp(p), (st(p), disp(p)))
        check('STOP_FIX 三個選項', sorted(o.strip() for o in opts(p)) == sorted(['不客氣，慢走！', '你走錯了！', '（不說話）']), opts(p))
        for bad_ in ('你走錯了！', '（不說話）'):
            m1 = mis(p); press(p, bad_); check(f'STOP_FIX 選「{bad_}」：扣分、留在 STOP_FIX', mis(p) == m1 + 1 and st(p) == 'STOP_FIX')
        check('STOP_FIX 錯誤紀錄有關卡名稱', p.evaluate('Game.log[Game.log.length-1].stage[0]') == '鄰居下樓')
        press(p, '不客氣，慢走！'); leave_trans(p)
        check('STOP_FIX 之後：早停（x）或 Ami 的樓層', st(p) == ('EARLY' if first == 'fix' else 'ARRIVE'), st(p))
        p.close()

    # 鄰居沒有看錯：亂提醒要扣分
    p = new_page(b); set_task(p, stopWrong=False); to_lobby(p); to_help(p); help_right(p); evt_ok(p); leave_trans(p)
    check('沒看錯：STOP 停在3樓', st(p) == 'STOP' and p.evaluate('Game.cur') == 3 and '3' in disp(p), (st(p), disp(p)))
    m0 = mis(p); press(p, '不好意思，這裡是2樓，您是不是要到3樓？')
    check('沒看錯時亂提醒：扣分、留在 STOP', mis(p) == m0 + 1 and st(p) == 'STOP')
    check('亂提醒的提示：這裡就是3樓', '這裡就是3樓' in txt(p, '.fb.bad'), txt(p, '.fb.bad'))
    press(p, '靠杯！你不是要去2樓？'); check('沒看錯時說「靠杯」：扣分（數字跟現在樓層不同）', mis(p) == m0 + 2)
    press(p, '不客氣，慢走！')
    check('沒看錯時慢走：不進 STOP_FIX', st(p) in ('_TRANS', 'ARRIVE', 'EARLY') and trans_from(p) in (None, 'STOP')); leave_trans(p)
    check('沒看錯時慢走：直接 ARRIVE', st(p) == 'ARRIVE', st(p))
    p.close()

    # ── 6. 門鈴：Ami 住 n 樓之 u，三戶電鈴，按錯有人開門 ──
    for u in (1, 2, 3):
        p = new_page(b); set_task(p, n=8, m=3, unit=u)
        check(f'Ami 的 LINE 說住 8樓之{u}', f'8樓之{u}' in p.evaluate('Game.amiLines().map(x=>x.zh).join()'))
        check(f'任務卡寫「Ami住：8樓之{u}」', f'Ami住：8樓之{u}' in p.evaluate('Game.listHTML(true).map(x=>x.zh).join()'))
        to_lobby(p); to_help(p); help_right(p); evt_ok(p); leave_trans(p); press(p, '不客氣，慢走！'); leave_trans(p)
        press(p, '不好意思，借過一下。'); leave_trans(p)
        check('DOOR：三顆電鈴、有「按電鈴」、畫面上不再提示 Ami 住幾號（要自己記得）', st(p) == 'DOOR' and p.locator('.bellplates button.plate').count() == 3 and f'樓之{u}' not in txt(p, '#npc-dialogue') and 'Ami住' not in txt(p, '#npc-dialogue') and '按電鈴' in txt(p, '.pcap'), (st(p), opts(p)))
        check('DOOR 圖是 door.jpg', img(p).endswith('door.jpg'), img(p))
        seen = {}
        for k in [x for x in (1, 2, 3) if x != u]:
            m0 = mis(p); press(p, f'按之{k}的電鈴。')
            check(f'DOOR 按錯之{k}：扣分、進 DOOR_WRONG（合併頁，紅卡在最上面）', mis(p) == m0 + 1 and st(p) == 'DOOR_WRONG' and p.evaluate("(()=>{const b=document.getElementById('npc-dialogue');const f=b.querySelector('.fb'),sp=b.querySelector('.speaker');return !!f&&!!sp&&!!(f.compareDocumentPosition(sp)&Node.DOCUMENT_POSITION_FOLLOWING)})()"), (mis(p), st(p)))
            tx = txt(p, '#npc-dialogue'); who = 'muscle' if '男住戶' in tx else 'woman' if '女住戶' in tx else None
            seen[k] = who
            check(f'DOOR_WRONG 之{k}：有開門的人（{who}）、圖對得上', who is not None and img(p).endswith('door_muscle.jpg' if who == 'muscle' else 'door_woman.jpg'), (tx, img(p)))
            check('DOOR_WRONG 三個選項', sorted(o.strip() for o in opts(p)) == sorted(['不好意思，我按錯了。', '你怎麼不是Ami？', '（不說話，轉身就走）']), opts(p))
            for bad_ in ('你怎麼不是Ami？', '（不說話，轉身就走）'):
                m1 = mis(p); press(p, bad_); check(f'DOOR_WRONG 選「{bad_}」：扣分、留在 DOOR_WRONG', mis(p) == m1 + 1 and st(p) == 'DOOR_WRONG')
            check('DOOR_WRONG 錯誤紀錄有關卡名稱', p.evaluate('Game.log[Game.log.length-1].stage[0]') == '按錯門')
            press(p, '不好意思，我按錯了。')
            check('DOOR_WRONG 道歉：回到 DOOR、有住戶回話', st(p) == 'DOOR' and ('沒事' in txt(p, '#npc-dialogue') or '再找找看' in txt(p, '#npc-dialogue')), (st(p), txt(p, '#npc-dialogue')))
        check('兩個錯的門是不同的人（一個壯男、一個女生）', sorted(seen.values()) == ['muscle', 'woman'], seen)
        press(p, f'按之{u}的電鈴。'); check('DOOR 按對：過場後是 END、計時停止', st(p) in ('_TRANS', 'END')); leave_trans(p)
        check('END：Ami 迎接你', st(p) == 'END' and '迎接' in txt(p, '#npc-dialogue'), txt(p, '#npc-dialogue'))
        p.close()
    # 第一次就按對：過場「門開了」用 Ami 探頭的圖
    p = new_page(b); set_task(p, n=8, m=3, unit=2); to_lobby(p); to_help(p); help_right(p); evt_ok(p); leave_trans(p); press(p, '不客氣，慢走！'); leave_trans(p); press(p, '不好意思，借過一下。'); leave_trans(p)
    press(p, '按之2的電鈴。'); check('DOOR 一次按對：過場圖是 Ami 探頭 door_ami.jpg', st(p) == '_TRANS' and img(p).endswith('door_ami.jpg'), (st(p), img(p)))
    p.close()
    # 同一戶按錯兩次，是同一個人
    p = new_page(b); set_task(p, n=8, m=3, unit=2); to_lobby(p); to_help(p); help_right(p); evt_ok(p); leave_trans(p); press(p, '不客氣，慢走！'); leave_trans(p); press(p, '不好意思，借過一下。'); leave_trans(p)
    press(p, '按之1的電鈴。'); a1 = '男住戶' in txt(p, '#npc-dialogue'); press(p, '不好意思，我按錯了。'); press(p, '按之1的電鈴。'); check('同一戶再按錯：還是同一個人', ('男住戶' in txt(p, '#npc-dialogue')) == a1)
    p.close()

    # ── 5. 三種錯誤一次都遇到，整局打到排行榜（照提醒、照回應走）──
    p = new_page(b); set_task(p, n=9, m=4, misspoke=True, dirDown=True, stopWrong=True, early=True); to_lobby(p); to_help(p)
    check('全部一起：HELP 要按4樓', '4樓' in screen(p))
    help_right(p); leave_trans(p); press(p, '沒關係，我幫你按5樓。'); evt_ok(p); leave_trans(p)
    check('全部一起：STOP 停在4樓（e=5）', st(p) == 'STOP' and p.evaluate('Game.cur') == 4, (st(p), p.evaluate('Game.cur')))
    press(p, '不好意思，這裡是4樓，您是不是要到5樓？'); leave_trans(p)
    check('全部一起：STOP_FIX 5樓', st(p) == 'STOP_FIX' and p.evaluate('Game.cur') == 5)
    press(p, '不客氣，慢走！'); leave_trans(p)
    check('全部一起：EARLY 在 6~8 樓之間', st(p) == 'EARLY' and 6 <= p.evaluate('Game.cur') <= 8, (st(p), p.evaluate('Game.cur')))
    press(p, '不出去，這裡不是9樓。'); leave_trans(p); press(p, '不好意思，借過一下。'); leave_trans(p)
    check('全部一起：到了 Ami 那層是 DOOR（三個電鈴）', st(p) == 'DOOR' and sorted(opts(p)) == ['按之1的電鈴。', '按之2的電鈴。', '按之3的電鈴。'], (st(p), opts(p)))
    press(p, '按之2的電鈴。'); leave_trans(p)
    check('全部一起：END、100 分、0 錯誤', st(p) == 'END' and p.evaluate('Game.score') == 100 and mis(p) == 0, (st(p), p.evaluate('Game.score')))
    pend = [f for f in ('door.jpg', 'door_muscle.jpg', 'door_woman.jpg') if not os.path.exists(os.path.join(HERE, '..', 'games', 'elevator', 'images', f))]
    miss = [m for m in p.evaluate('[...Game.missing]') if not any(m.endswith(x) for x in pend)]
    check('這一局用到的圖都載得到（還沒做好的門圖除外）', not miss, (miss, pend))
    p.close()
    for f in ('dir.jpg', 'dir_sorry.jpg', 'neighbor_sorry.jpg'):
        check(f'新圖檔存在：{f}', os.path.exists(os.path.join(HERE, '..', 'games', 'elevator', 'images', f)))
    # LOBBY：三個選項、按▼和不按都扣分、答對才往下走
    p = new_page(b); set_task(p, n=8, m=3, dirDown=False); to_lobby(p)
    check('LOBBY 三個選項、圖是 lobby.jpg', sorted(o.strip() for o in opts(p)) == sorted(['按▲，往上。', '按▼，往下。', '不按，站在旁邊等。']) and img(p).endswith('lobby.jpg'), (opts(p), img(p)))
    for bad_ in ('按▼，往下。', '不按，站在旁邊等。'):
        m0 = mis(p); press(p, bad_); check(f'LOBBY 選「{bad_}」：扣分、留在 LOBBY', mis(p) == m0 + 1 and st(p) == 'LOBBY', (st(p), mis(p)))
    check('LOBBY 錯誤紀錄有關卡名稱', p.evaluate('Game.log[Game.log.length-1].stage[0]') == '大廳')
    p.close()
    # 其他關卡的每個錯誤選項（HELP 按成 Ami 的樓層、FLOOR 其他樓層在上面已測、ARRIVE 用力推開、STOP_FIX 兩個錯的）
    p = new_page(b); set_task(p, n=8, m=3); to_lobby(p); to_help(p)
    m0 = mis(p); press(p, '好，我幫你按8樓。'); check('HELP 按成 Ami 的樓層：扣分、留在 HELP', mis(p) == m0 + 1 and st(p) == 'HELP', (st(p), mis(p)))
    p.close()
    p = new_page(b); set_task(p, n=8, m=3, evt='CHAT'); to_lobby(p); to_help(p); help_right(p); evt_ok(p); leave_trans(p); press(p, '不客氣，慢走！'); leave_trans(p)
    m0 = mis(p); press(p, '（用力推開）'); check('ARRIVE 選「用力推開」：扣分、留在 ARRIVE', mis(p) == m0 + 1 and st(p) == 'ARRIVE', (st(p), mis(p)))
    p.close()
    # EARLY：沒有樓層提示、三個選項、每個錯的都扣分、答對才往下、圖是 early.jpg
    p = new_page(b); set_task(p, n=8, m=3, early=True, evt='CHAT'); to_lobby(p); to_help(p); help_right(p); evt_ok(p); leave_trans(p); press(p, '不客氣，慢走！'); leave_trans(p)
    x = p.evaluate('Game.task.x'); tx = txt(p, '#npc-dialogue')
    check('EARLY：旁白只有「門開了，外面有人要上電梯」、沒有樓層數字、沒有玩家台詞', st(p) == 'EARLY' and '外面有人要上電梯' in tx and '牆上' not in tx and '我：' not in tx and p.evaluate('Game.cur') == x, (st(p), tx))
    check('EARLY 三個選項、圖是 early.jpg', sorted(o.strip() for o in opts(p)) == sorted(['走出電梯。', '不出去，這裡不是8樓。', '（直接按關門，不讓別人進電梯）']) and img(p).endswith('early.jpg'), (opts(p), img(p)))
    for bad_ in ('走出電梯。', '（直接按關門，不讓別人進電梯）'):
        m0 = mis(p); press(p, bad_); check(f'EARLY 選「{bad_}」：扣分、留在 EARLY', mis(p) == m0 + 1 and st(p) == 'EARLY', (st(p), mis(p)))
    check('EARLY 錯誤紀錄有關卡名稱', p.evaluate('Game.log[Game.log.length-1].stage[0]') == '看樓層')
    press(p, '不出去，這裡不是8樓。'); leave_trans(p)
    check('EARLY 答對（已錯過，沒有綠卡）：到 ARRIVE、樓層是 8', st(p) == 'ARRIVE' and p.evaluate('Game.cur') == 8, (st(p), p.evaluate('Game.cur')))
    p.close()
    p = new_page(b); set_task(p, n=8, m=3, early=True, evt='CHAT'); to_lobby(p); to_help(p); help_right(p); evt_ok(p); leave_trans(p); press(p, '不客氣，慢走！'); leave_trans(p)
    press(p, '不出去，這裡不是8樓。')
    check('EARLY 第一次就對：過場有綠卡「你很細心」、旁白「那個人走進電梯」', st(p) == '_TRANS' and p.locator('.fb.good').count() == 1 and '那個人走進電梯' in txt(p, '#npc-dialogue'), (st(p), txt(p, '#npc-dialogue')))
    p.close()
    # 結局圖：錯 2 次以內是 end_good、超過是 end_bad
    for nbad, want in ((2, 'end_good.jpg'), (3, 'end_bad.jpg')):
        p = new_page(b); set_task(p, n=8, m=3, evt='CHAT'); to_lobby(p); to_help(p); help_right(p); evt_ok(p); leave_trans(p); press(p, '不客氣，慢走！'); leave_trans(p); press(p, '不好意思，借過一下。'); leave_trans(p)
        p.evaluate(f'Game.mistakes={nbad}'); press(p, '按之2的電鈴。'); leave_trans(p)
        check(f'END：錯 {nbad} 次，圖是 {want}', st(p) == 'END' and img(p).endswith(want), (st(p), img(p)))
        p.close()
    # 拼音：「終於」念 zhōng yú（pinyin-pro 預設會念成 wū）
    p = new_page(b)
    check('拼音：終於 念 zhōng yú', 'yú' in p.evaluate("(()=>{const d=document.createElement('div');d.innerHTML=Game.ruby('你終於來了');return [...d.querySelectorAll('rt')].map(x=>x.textContent).join(' ')})()"))
    p.close()
    # FLOOR：沒有玩家台詞、畫面上沒有 Ami 住幾樓
    p = new_page(b); set_task(p, n=8, m=3); to_lobby(p); press(p, '按▲，往上。'); leave_trans(p); press(p, '按「開門」，等他。'); leave_trans(p)
    check('FLOOR：沒有「我：」台詞、對話框沒有 Ami 住幾樓', st(p) == 'FLOOR' and '我：' not in txt(p, '#npc-dialogue') and 'Ami住' not in txt(p, '#npc-dialogue'), txt(p, '#npc-dialogue'))
    p.screenshot(path='/tmp/floor_nodialogue.png')
    p.close()
    # FART：旁白中性（不暗示是玩家放的）
    p = new_page(b); set_task(p, n=8, m=3, evt='FART'); to_lobby(p); to_help(p); help_right(p)
    check('FART 旁白：「鄰居低下頭，很尷尬」、沒有「看了你一眼」', '鄰居低下頭' in txt(p, '#npc-dialogue') and '看了你' not in txt(p, '#npc-dialogue'), txt(p, '#npc-dialogue'))
    p.close()
    # FART：「怪味道」輕扣 5 分，「是你吧」照常扣 10 分
    p = new_page(b); set_task(p, n=8, m=3, evt='FART'); to_lobby(p); to_help(p); help_right(p); leave_trans(p)
    s0 = p.evaluate('Game.score'); press(p, '這個電梯怎麼有怪味道？'); s1 = p.evaluate('Game.score'); press(p, '好臭喔！是你吧？'); s2 = p.evaluate('Game.score')
    check('FART 「怎麼有怪味道」只扣 5 分、「是你吧」扣 10 分', st(p) == 'FART' and s0 - s1 == 5 and s1 - s2 == 10, (st(p), s0, s1, s2))
    p.close()
    # 圖片載入失敗：自動重試一次（斷一下網路還是看得到圖）；重試也失敗才換成表情
    p = new_page(b); n1 = [0]
    def flaky(route):
        n1[0] += 1
        route.abort() if n1[0] == 1 else route.fulfill(path=os.path.join(HERE, '..', 'games', 'elevator', 'images', 'hall.jpg'), content_type='image/jpeg')
    p.context.route('**/images/zz_retry.jpg*', flaky)
    p.evaluate("Game.setImage('images/zz_retry.jpg', '🚪')"); p.wait_for_timeout(2500)
    check('圖片第一次失敗：自動重試後顯示圖片、沒記成缺圖', p.evaluate("(()=>{const i=document.getElementById('npc-avatar');return i.style.display==='block'&&i.naturalWidth>0})()") and not p.evaluate("[...Game.missing].some(m=>m.includes('zz_retry.jpg'))") and n1[0] == 2, (n1[0], p.evaluate('[...Game.missing]')))
    p.close()
    p = new_page(b); n2 = [0]
    def dead(route):
        n2[0] += 1; route.abort()
    p.context.route('**/images/zz_retry.jpg*', dead)
    p.evaluate("Game.setImage('images/zz_retry.jpg', '🚪')"); p.wait_for_timeout(2500)
    check('圖片連續失敗：只重試一次，之後顯示表情、記成缺圖', n2[0] == 2 and p.evaluate("document.getElementById('scene-placeholder').style.display") == 'grid' and p.evaluate("[...Game.missing].some(m=>m.includes('zz_retry.jpg'))"), (n2[0], p.evaluate('[...Game.missing]')))
    p.close()
    # 邊界：n=6, m=4, misspoke → e=5，後面沒有樓層可以早停
    p = new_page(b); set_task(p, n=6, m=4, misspoke=True, early=True)
    check('n=6,m=4,misspoke：沒有早停', p.evaluate('Game.task.early') is False and p.evaluate('Game.task.x') is None)
    p.close()

    # ── 6. 小字典的字都出現在那一關的畫面上 ──
    p = new_page(b); set_task(p, misspoke=True, dirDown=True, stopWrong=True); to_guard(p); vocab_ok_g = p.evaluate('s=>VOCAB[s].map(x=>x[0])', 'GUARD')
    check('小字典 GUARD：每個字都在畫面上', all(w in screen(p) for w in vocab_ok_g), vocab_ok_g)
    press(p, guard_ok(p)); leave_trans(p)
    press(p, '按▲，往上。'); leave_trans(p)
    def vocab_ok(state):
        words = p.evaluate('s=>VOCAB[s].map(x=>x[0])', state); sc = screen(p)
        miss = [w for w in words if w not in sc]; check(f'小字典 {state}：每個字都在畫面上', not miss, miss)
    vocab_ok('DIR'); press(p, '不好意思，這部是往下的。'); leave_trans(p)
    press(p, '按「開門」，等他。'); leave_trans(p)
    press(p, f"按{p.evaluate('Game.task.n')}樓。"); leave_trans(p)
    help_right(p); evt_ok(p); leave_trans(p); vocab_ok('HELP2'); press(p, '沒關係，我幫你按4樓。'); vocab_ok(st(p)); evt_ok(p); leave_trans(p); vocab_ok('STOP')
    press(p, '不好意思，這裡是3樓，您是不是要到4樓？'); leave_trans(p); vocab_ok('STOP_FIX')
    p.close()

    # ── 管理員：問你找哪一戶 ──
    p = new_page(b); set_task(p, n=9, m=3, unit=3); to_guard(p)
    check('GUARD：管理員問「你找哪一戶？」、沒有先生小姐', '管理員：你找哪一戶？' in txt(p, '#npc-dialogue') and '先生' not in screen(p) and '小姐' not in screen(p), txt(p, '#npc-dialogue'))
    check('GUARD 三個選項', sorted(o.strip() for o in opts(p)) == sorted(['我要找朋友，她住在9樓之3。', '（不理他，直接走）', '閃開啦！']), opts(p))
    check('GUARD 圖是 guard.jpg', img(p).endswith('guard.jpg'), img(p))
    for bad in ('（不理他，直接走）', '閃開啦！'):
        m0 = mis(p); press(p, bad); check(f'GUARD 選「{bad}」：扣分、留在 GUARD', mis(p) == m0 + 1 and st(p) == 'GUARD')
    press(p, '我要找朋友，她住在9樓之3。'); leave_trans(p)
    check('GUARD 答對：進 LOBBY', st(p) == 'LOBBY', st(p))
    p.close()

    # ── 電梯小插曲：聊天、怪味道、小狗 ──
    ev_bad = {'CHAT': ['你吃飽了嗎？', '（不說話，看手機）'], 'FART': ['好臭喔！是你吧？', '這個電梯怎麼有怪味道？'], 'DOG': ['走開！你的狗好可怕！', '（尖叫）']}
    ev_opts = {'CHAT': ['對啊，真的很熱。', '你吃飽了嗎？', '（不說話，看手機）'], 'FART': ['（假裝沒聞到）', '好臭喔！是你吧？', '這個電梯怎麼有怪味道？'], 'DOG': ['沒關係，牠很可愛。', '走開！你的狗好可怕！', '（尖叫）']}
    for ev in EVTS:
        p = new_page(b); set_task(p, n=8, m=3, stopWrong=False); p.evaluate('e=>{Game.task.evt=e}', ev); to_lobby(p); to_help(p); help_right(p)
        check(f'{ev}：HELP 之後是 {ev}', st(p) == ev, st(p))
        check(f'{ev} 三個選項', sorted(o.strip() for o in opts(p)) == sorted(ev_opts[ev]), opts(p))
        check(f'{ev} 圖是 {ev.lower()}.jpg', img(p).endswith(ev.lower() + '.jpg'), img(p))
        words = p.evaluate('s=>VOCAB[s].map(x=>x[0])', ev); check(f'小字典 {ev}：每個字都在畫面上', all(w in screen(p) for w in words), words)
        for bad in ev_bad[ev]:
            m0 = mis(p); press(p, bad); check(f'{ev} 選「{bad}」：扣分、留在 {ev}', mis(p) == m0 + 1 and st(p) == ev)
            if bad == '好臭喔！是你吧？': check('FART 說「是你吧」：鄰居回「不是我啦！」', '不是我啦' in txt(p, '#npc-dialogue'), txt(p, '#npc-dialogue'))
        press(p, EVT_OK[ev]); check(f'{ev} 答對：電梯停在3樓、進 STOP', st(p) == 'STOP' and p.evaluate('Game.cur') == 3, (st(p), p.evaluate('Game.cur')))
        p.close()
    # 小狗那局：整局都是穿粉紅色外套、牽小狗的阿姨（旁白、說話的人、圖都換）
    p = new_page(b); set_task(p, n=8, m=3, stopWrong=True, evt='DOG'); to_lobby(p); press(p, '按▲，往上。'); leave_trans(p)
    if st(p) == 'DIR': press(p, '不好意思，這部是往下的。'); leave_trans(p)
    check('DOG 局：WAIT 旁白是穿粉紅色外套、牽著小狗的阿姨', '粉紅色外套' in txt(p, '#npc-dialogue') and '阿姨：等一下' in txt(p, '#npc-dialogue'), txt(p, '#npc-dialogue'))
    check('DOG 局：WAIT 圖是 wait_dog.jpg', img(p).endswith('wait_dog.jpg'), img(p))
    press(p, '按「開門」，等他。'); leave_trans(p); press(p, '按8樓。'); leave_trans(p)
    check('DOG 局：HELP 是阿姨在說話、圖是 dog.jpg', st(p) == 'HELP' and '阿姨：不好意思，我要到3樓' in txt(p, '#npc-dialogue') and img(p).endswith('dog.jpg'), (st(p), img(p)))
    help_right(p)
    check('DOG 局：小狗頁是阿姨說「牠不會咬人」、旁白是阿姨的小狗', st(p) == 'DOG' and '阿姨：不好意思，牠不會咬人' in txt(p, '#npc-dialogue') and '阿姨牽著的小狗' in txt(p, '#npc-dialogue'), txt(p, '#npc-dialogue'))
    press(p, '沒關係，牠很可愛。'); check('DOG 局：STOP 是阿姨、圖是 dog.jpg', st(p) == 'STOP' and '阿姨：到了' in txt(p, '#npc-dialogue') and img(p).endswith('dog.jpg'), (st(p), img(p)))
    press(p, '不好意思，這裡是2樓，您是不是要到3樓？')
    check('DOG 局：看錯樓層的道歉過場用 neighbor_sorry_dog.jpg', st(p) == '_TRANS' and img(p).endswith('neighbor_sorry_dog.jpg'), (st(p), img(p)))
    p.close()
    p = new_page(b); set_task(p, misspoke=True, evt='DOG'); to_lobby(p); to_help(p); help_right(p); leave_trans(p)
    check('DOG 局：HELP2 圖是 neighbor_sorry_dog.jpg', st(p) == 'HELP2' and img(p).endswith('neighbor_sorry_dog.jpg'), (st(p), img(p)))
    p.close()
    p = new_page(b); set_task(p, evt='CHAT'); to_lobby(p); press(p, '按▲，往上。'); leave_trans(p)
    if st(p) == 'DIR': press(p, '不好意思，這部是往下的。'); leave_trans(p)
    check('非小狗局：WAIT 還是鄰居、圖是 wait.jpg', '一位鄰居跑過來' in txt(p, '#npc-dialogue') and img(p).endswith('wait.jpg') and not img(p).endswith('wait_dog.jpg'), img(p))
    p.close()
    p = new_page(b)
    seen = p.evaluate("()=>{const s=new Set();for(let i=0;i<200;i++){Game.setup();s.add(Game.task.evt)}return [...s].sort()}")
    check('每局隨機抽一種小插曲（三種都會出現）', seen == sorted(EVTS), seen)
    p.close()

    # ── 7. 網頁沒有出錯 ──
    p = new_page(b); set_task(p, misspoke=True, dirDown=True, stopWrong=True, early=True)
    to_lobby(p); to_help(p)   # 拼音預設就是開的，新台詞的 ruby 也會一起畫出來
    check('沒有網頁錯誤', not p.errs, p.errs)
    p.close()

if __name__ == '__main__':
    with sync_playwright() as pw:
        b = pw.chromium.launch(); run(b); b.close()
    print(f'通過 {PASS[0]} 項，失敗 {len(FAILS)} 項')
    for f in FAILS: print(f)
    sys.exit(1 if FAILS else 0)
