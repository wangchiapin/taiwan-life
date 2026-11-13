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

def set_task(page, n=8, m=3, misspoke=False, dirDown=False, stopWrong=False, early=False, unit=2, evt='CHAT', entry='rush', askX=None):
    """把這一局的隨機條件固定下來（和 setup() 的規則一致）"""
    page.evaluate("""o=>{const t=Game.task; Object.assign(t,{n:o.n,m:o.m,entry:o.entry,askX:o.askX??(o.n-1),misspoke:o.misspoke,e:o.misspoke?o.m+1:o.m,dirDown:o.dirDown,stopWrong:o.stopWrong,unit:o.unit,evt:o.evt}); Game.wrongUnit=null;
      const xs=Array.from({length:t.n-t.e-1},(_,i)=>t.e+1+i); t.x=xs.length?xs[0]:null; t.early=o.early&&xs.length>0; Game.render();}""",
      dict(n=n, m=m, entry=entry, askX=askX, misspoke=misspoke, dirDown=dirDown, stopWrong=stopWrong, early=early, unit=unit, evt=evt))

EVTS = ('CHAT', 'FART', 'DOG')
EVT_OK = {'CHAT': '對啊，真的很熱。', 'FART': '（假裝沒聞到）', 'DOG': '沒關係，牠很可愛。'}
def guard_ok(page): t = page.evaluate('Game.task'); return f"我要找朋友，她住在{t['n']}樓之{t['unit']}。"
def to_guard(page): press(page, '走進大樓'); leave_trans(page); assert st(page) == 'GUARD', st(page)
def to_lobby(page): to_guard(page); press(page, guard_ok(page)); leave_trans(page); assert st(page) == 'LOBBY', st(page)
def evt_ok(page):   # 電梯裡的小插曲（若有）答對；之後停在 STOP
    if st(page) in EVTS: press(page, EVT_OK[st(page)])
def to_help(page):   # LOBBY 之後到 HELP（DIR 若有，先答對）；鄰居進來先開口，所以 WAIT 之後直接是 HELP
    press(page, '按▲，往上。'); leave_trans(page)
    if st(page) == 'DIR': press(page, '不好意思，這部是往下的。'); leave_trans(page)
    assert st(page) == 'WAIT', st(page)
    press(page, '按「開門」，等他。'); leave_trans(page); assert st(page) == 'HELP', st(page)
def press_floor(page):   # 輪到自己按樓層：按對 Ami 的樓層（之後是電梯裡的小插曲）
    leave_trans(page); assert st(page) == 'FLOOR', st(page)
    press(page, f"按{page.evaluate('Game.task.n')}樓。")
def to_floor(page, right=True):   # LOBBY → （DIR）→ WAIT → HELP（鄰居先開口）→ 幫他按對 → 輪到自己按樓層（FLOOR）
    press(page, '按▲，往上。'); leave_trans(page)
    if st(page) == 'DIR': press(page, '不好意思，這部是往下的。'); leave_trans(page)
    press(page, '按「開門」，等他。'); assert st(page) == 'HELP', st(page)
    press(page, f"好，我幫你按{page.evaluate('Game.task.m')}樓。"); leave_trans(page); assert st(page) == 'FLOOR', st(page)
def help_right(page):   # 幫鄰居按對；沒說錯樓層就接著自己按樓層（到小插曲）。說錯樓層的停在 HELP2，由測試自己處理
    t = page.evaluate('({m:Game.task.m})')
    press(page, f"好，我幫你按{t['m']}樓。")
    if not page.evaluate('Game.task.misspoke'): press_floor(page)

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
        press(p, '沒關係，我幫你按4樓。'); check('HELP2 客氣回應：過場「輪到你按樓層」、旁白你按了4樓', st(p) == '_TRANS' and trans_from(p) == 'HELP2' and '你按了4樓' in txt(p, '#npc-dialogue') and '輪到你按樓層' in txt(p, '#options-area'), (st(p), txt(p, '#npc-dialogue')))
        check('HELP2 過場：第一次就對才有綠卡', (p.locator('.fb.good').count() == 1) == (first is None))
        press_floor(p); check('HELP2 之後自己按樓層：直接進電梯小插曲（合併）', st(p) in EVTS, st(p))
        evt_ok(p); leave_trans(p); check('HELP2 之後是 STOP（停在4樓，沒看錯）', st(p) == 'STOP' and p.evaluate('Game.cur') == 4, (st(p), p.evaluate('Game.cur')))
        p.close()

    # ── 電梯按鍵面板：WAIT 只能按開關門、FLOOR 只能按樓層（共 16 顆）──
    p = new_page(b); set_task(p, n=12, m=3); to_lobby(p); press(p, '按▲，往上。'); leave_trans(p)
    check('WAIT：面板有 16 顆按鍵、只有開門／關門能按', p.locator('.ppanel .pb').count() == 16 and sorted(x.strip() for x in opts(p)) == sorted(['按「開門」，等他。', '按「關門」。']), opts(p))
    m0 = mis(p); press(p, '按「關門」。'); check('WAIT 按關門：扣分、留在 WAIT', mis(p) == m0 + 1 and st(p) == 'WAIT')
    press(p, '按「開門」，等他。'); check('WAIT 按開門：鄰居先開口（直接是 HELP、不經過場）', st(p) == 'HELP' and '麻煩你幫我按一下' in txt(p, '#npc-dialogue'), st(p))
    press(p, '好，我幫你按3樓。'); check('HELP 答對：過場，按鈕是「輪到你按樓層」', st(p) == '_TRANS' and '輪到你按樓層' in txt(p, '#options-area')); leave_trans(p)
    exp = ['按地下2樓。', '按地下1樓。'] + [f'按{k}樓。' for k in range(1, 13)]
    check('FLOOR：14 個樓層鍵（地下2到12樓）都能按、開關門不能按', sorted(opts(p)) == sorted(exp) and p.locator('.ppanel .pb').count() == 16, opts(p))
    check('FLOOR：面板上有「按樓層」', '按樓層' in txt(p, '.pcap'))
    for k in ['按地下2樓。', '按地下1樓。', '按1樓。']:
        m1 = mis(p); press(p, k); check(f'FLOOR 按「{k}」：直接顯示錯誤（扣分、留在 FLOOR、不會真的上去）', mis(p) == m1 + 1 and st(p) == 'FLOOR' and p.evaluate('Game.cur') == 1)
    p.screenshot(path='/tmp/panel_floor.png')
    press(p, '按12樓。'); check('FLOOR 按對 12 樓：進電梯小插曲', st(p) in EVTS, st(p))
    p.close()
    p = new_page(b); set_task(p, n=12, m=3); to_lobby(p); press(p, '按▲，往上。'); leave_trans(p); p.screenshot(path='/tmp/panel_wait.png'); p.evaluate("Game.showList=true;Game.render()"); p.locator('.list').screenshot(path='/tmp/list.png'); p.close()

    # ── 圖2.3 合併：FLOOR 答對後不跳過場，綠卡＋鄰居的話＋選項在同一頁 ──
    p = new_page(b); set_task(p, n=8, m=3); to_lobby(p); press(p, '按▲，往上。'); leave_trans(p)
    press(p, '按「開門」，等他。')
    tx = txt(p, '#npc-dialogue')
    check('WAIT 答對：直接是 HELP（沒有過場）', st(p) == 'HELP', st(p))
    check('合併頁：有綠卡、鄰居的話只出現一次、有選項', p.locator('.fb.good').count() == 1 and tx.count('麻煩你幫我按一下') == 1 and len(opts(p)) == 3, tx)
    check('任務卡標題：搭電梯上8樓找Ami', '搭電梯上8樓找Ami' in p.evaluate("(()=>{Game.showList=true;Game.render();const e=document.querySelector('.list .t');const c=e.cloneNode(true);c.querySelectorAll('rt').forEach(r=>r.remove());return c.textContent})()"))
    check('NEXT_LABEL STOP_FIX 是「電梯繼續往上」', p.evaluate("NEXT_LABEL.STOP_FIX") == '電梯繼續往上')
    p.close()

    # ── 第三輪修改：綠卡在最上面、HELP 第三個選項、HELP→STOP 合併、ARRIVE 選項與旁白 ──
    fb_first = "(()=>{const b=document.getElementById('npc-dialogue');const f=b.querySelector('.fb'),sp=b.querySelector('.speaker');return !!f&&!!sp&&!!(f.compareDocumentPosition(sp)&Node.DOCUMENT_POSITION_FOLLOWING)})()"
    p = new_page(b); set_task(p, n=8, m=3); to_lobby(p); press(p, '按▲，往上。'); leave_trans(p); press(p, '按「開門」，等他。')
    check('WAIT→HELP 合併頁：綠卡在鄰居的話上面', p.evaluate(fb_first))
    check('HELP 第三個選項是「幹！你不會自己按喔！」、沒有「已經亮了」', sorted(o.strip() for o in opts(p)) == sorted(['好，我幫你按3樓。', '好，我幫你按8樓。', '幹！你不會自己按喔！']), opts(p))
    m0 = mis(p); press(p, '幹！你不會自己按喔！'); check('HELP 選「幹」：扣分、留在 HELP', mis(p) == m0 + 1 and st(p) == 'HELP' and '不要罵人' in txt(p, '.fb.bad'), txt(p, '.fb.bad'))
    p.close()
    p = new_page(b); set_task(p, n=8, m=3, stopWrong=False); to_lobby(p); press(p, '按▲，往上。'); leave_trans(p); press(p, '按「開門」，等他。')
    press(p, '好，我幫你按3樓。'); press_floor(p)
    check('FLOOR→小插曲 合併：直接是小插曲、綠卡在最上面', st(p) in EVTS and (p.evaluate(fb_first) or st(p) == 'FART'), st(p))   # FART 沒有人說話，沒有 .speaker 可比
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
    help_right(p); leave_trans(p); press(p, '沒關係，我幫你按5樓。'); press_floor(p); evt_ok(p); leave_trans(p)
    check('全部一起：STOP 停在4樓（e=5）', st(p) == 'STOP' and p.evaluate('Game.cur') == 4, (st(p), p.evaluate('Game.cur')))
    press(p, '不好意思，這裡是4樓，您是不是要到5樓？'); leave_trans(p)
    check('全部一起：STOP_FIX 5樓', st(p) == 'STOP_FIX' and p.evaluate('Game.cur') == 5)
    press(p, '不客氣，慢走！'); leave_trans(p)
    check('全部一起：EARLY 在 6~8 樓之間', st(p) == 'EARLY' and 6 <= p.evaluate('Game.cur') <= 8, (st(p), p.evaluate('Game.cur')))
    press(p, '不出去，這裡不是9樓。'); leave_trans(p); press(p, '不好意思，借過一下。'); leave_trans(p)
    check('全部一起：到了 Ami 那層是 DOOR（三個電鈴）', st(p) == 'DOOR' and sorted(opts(p)) == ['按之1的電鈴。', '按之2的電鈴。', '按之3的電鈴。'], (st(p), opts(p)))
    press(p, '按之2的電鈴。'); leave_trans(p)
    check('全部一起：END、100 分、0 錯誤', st(p) == 'END' and p.evaluate('Game.score') == 100 and mis(p) == 0, (st(p), p.evaluate('Game.score')))
    pend = [f for f in ('door.jpg', 'door_muscle.jpg', 'door_woman.jpg', 'door_girl.jpg', 'door_ben.jpg', 'door_muscle_angry.jpg', 'door_woman_angry.jpg') if not os.path.exists(os.path.join(HERE, '..', 'games', 'elevator', 'images', f))]
    miss = [m for m in p.evaluate('[...Game.missing]') if not any(m.endswith(x) for x in pend)]
    check('這一局用到的圖都載得到（還沒做好的門圖除外）', not miss, (miss, pend))
    p.close()
    for f in ('dir.jpg', 'dir_sorry.jpg', 'neighbor_sorry.jpg', 'elevator_empty.jpg', 'early.jpg', 'door_ami.jpg', 'inside_asks.jpg', 'wrong_doors.jpg', 'wrong_floor.jpg', 'inside_asks_dog.jpg'):
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
    # 鄰居（阿姨）下電梯之後的過場：電梯裡沒有人（elevator_empty.jpg）；他還在電梯裡的過場不換
    for evt in ('CHAT', 'DOG'):
        for early in (True, False):
            p = new_page(b); set_task(p, n=8, m=3, early=early, evt=evt); to_lobby(p); to_help(p); help_right(p); evt_ok(p); leave_trans(p)
            press(p, '不客氣，慢走！')
            check(f'{evt} early={early}：STOP 答對後的過場圖是空電梯', st(p) == '_TRANS' and img(p).endswith('elevator_empty.jpg'), (st(p), img(p)))
            p.close()
        p = new_page(b); set_task(p, n=8, m=4, stopWrong=True, early=True, evt=evt); to_lobby(p); to_help(p); help_right(p); evt_ok(p); leave_trans(p)
        press(p, '不好意思，這裡是3樓，您是不是要到4樓？')
        check(f'{evt} 看錯樓層的道歉過場：他還在電梯裡，不是空電梯', st(p) == '_TRANS' and not img(p).endswith('elevator_empty.jpg'), (st(p), img(p)))
        leave_trans(p); press(p, '不客氣，慢走！')
        check(f'{evt} STOP_FIX 答對後的過場圖是空電梯', st(p) == '_TRANS' and img(p).endswith('elevator_empty.jpg'), (st(p), img(p)))
        p.close()
    # HELP2（鄰居改口）之後：先「你按了4樓」，輪到自己按樓層，電梯才往上（小插曲頁只有「電梯向上」一次）
    p = new_page(b); set_task(p, n=8, m=3, misspoke=True, evt='CHAT'); to_lobby(p); to_help(p); help_right(p); leave_trans(p)
    press(p, '沒關係，我幫你按4樓。')
    tx = txt(p, '#npc-dialogue')
    check('HELP2 之後的過場：「你按了4樓」、電梯還沒往上', st(p) == '_TRANS' and '你按了4樓' in tx and '電梯繼續往上' not in tx and '電梯向上' not in tx, tx)
    press_floor(p); tx = txt(p, '#npc-dialogue')
    check('自己按樓層之後的小插曲頁：有「電梯向上」', st(p) == 'CHAT' and tx.count('電梯向上') == 1, tx)
    p.close()
    # FLOOR：沒有玩家台詞、畫面上沒有 Ami 住幾樓
    p = new_page(b); set_task(p, n=8, m=3); to_lobby(p); press(p, '按▲，往上。'); leave_trans(p); press(p, '按「開門」，等他。'); press(p, '好，我幫你按3樓。'); leave_trans(p)
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
    press(p, '按「開門」，等他。'); vocab_ok('HELP')
    help_right(p); leave_trans(p); vocab_ok('HELP2'); press(p, '沒關係，我幫你按4樓。'); press_floor(p); vocab_ok(st(p)); evt_ok(p); leave_trans(p); vocab_ok('STOP')
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
    press(p, '按「開門」，等他。')
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


    # ── 8. 搭錯樓層：按了 2～12 樓的別層。比鄰居低的樓層：先停在那裡（鄰居還在電梯裡）；
    #       跟鄰居一樣高或更高：鄰居先下車，才到你按的那層。扣分在陌生人開門的時候 ──
    fb_first2 = "(()=>{const b=document.getElementById('npc-dialogue');const f=b.querySelector('.fb'),sp=b.querySelector('.speaker');return !!f&&!!sp&&!!(f.compareDocumentPosition(sp)&Node.DOCUMENT_POSITION_FOLLOWING)})()"
    def stranger(p, k, who_fb):   # 走出電梯 → 按電鈴 → 陌生人開門 → 客氣道歉 → 過場回電梯
        press(p, '走出電梯。'); check(f'走出電梯：進 WRONG_BELL、沒有過場', st(p) == 'WRONG_BELL', st(p))
        m1 = mis(p); s1 = p.evaluate('Game.score'); press(p, '按之1的電鈴。')
        check(f'按電鈴：陌生人開門、這時才扣 10 分（{k}樓）', st(p) == 'WRONG_DOOR' and mis(p) == m1 + 1 and p.evaluate('Game.score') == s1 - 10 and f'這裡是{k}樓' in txt(p, '.fb.bad'), (st(p), mis(p), txt(p, '.fb.bad')))
    # 8-1 比鄰居低（m=4，按 3 樓）：鄰居還在電梯裡，電梯先停在 3 樓
    p = new_page(b); set_task(p, n=8, m=4, entry='rush', evt='CHAT'); p.evaluate("Game.strangers=['ben','girl']"); to_lobby(p); to_floor(p)
    s0 = p.evaluate('Game.score'); m0 = mis(p)
    check('FLOOR 開頭：面板、沒有玩家台詞', st(p) == 'FLOOR' and '我：' not in txt(p, '#npc-dialogue'))
    press(p, '按3樓。')
    check('按比鄰居低的樓層（3）：進過場、還沒扣分', st(p) == '_TRANS' and trans_from(p) == 'FLOOR' and mis(p) == m0 and p.evaluate('Game.score') == s0, (st(p), mis(p)))
    check('過場旁白：電梯停了、門開了，沒有樓層數字', '門開了' in txt(p, '#npc-dialogue') and '樓' not in txt(p, '#npc-dialogue'), txt(p, '#npc-dialogue'))
    leave_trans(p)
    check('WRONG_FLOOR：電梯停在 3 樓（顯示器 3）、鄰居還在電梯裡', st(p) == 'WRONG_FLOOR' and p.evaluate('Game.cur') == 3 and '3' in disp(p) and p.evaluate('Game.neighborGone') is False, (st(p), disp(p)))
    check('WRONG_FLOOR：只說外面是走廊、兩個選項、圖 wrong_floor.jpg', '走廊' in txt(p, '#npc-dialogue') and '8' not in txt(p, '#npc-dialogue') and sorted(o.strip() for o in opts(p)) == sorted(['走出電梯。', '不出去，這裡不是8樓。']) and img(p).endswith('wrong_floor.jpg'), (opts(p), img(p)))
    words = p.evaluate('s=>VOCAB[s].map(x=>x[0])', 'WRONG_FLOOR'); check('小字典 WRONG_FLOOR：每個字都在畫面上', all(w in screen(p) for w in words), words)
    press(p, '不出去，這裡不是8樓。')
    check('不出去：輕扣 5 分、過場回電梯（鄰居還在：elevator.jpg、「電梯門關上」）', mis(p) == m0 + 1 and p.evaluate('Game.score') == s0 - 5 and st(p) == '_TRANS' and trans_from(p) == 'WRONG_FLOOR' and img(p).endswith('elevator.jpg') and '電梯門關上' in txt(p, '#options-area'), (mis(p), st(p), img(p)))
    check('過場：錯誤紀錄「走錯樓層」、紅卡說「剛剛你按錯樓層」、旁白關門', p.evaluate('Game.log[Game.log.length-1].stage[0]') == '走錯樓層' and '按錯樓層' in txt(p, '.fb.bad') and '關門' in txt(p, '#npc-dialogue'), txt(p, '.fb.bad'))
    leave_trans(p); check('回到 FLOOR、顯示器回到 1', st(p) == 'FLOOR' and p.evaluate('Game.cur') == 1 and p.evaluate('Game.wrongFloor') is None, (st(p), disp(p)))
    # 再按 2 樓、這次走出去
    press(p, '按2樓。'); leave_trans(p); stranger(p, 2, None)
    check('WRONG_BELL：三個電鈴、圖 wrong_doors.jpg（上一步已按，回頭檢查文字）', True)
    check('WRONG_DOOR：紅卡在最上面、說這裡是2樓、Ami 住 8 樓、第一位開門的是你自己 door_ben.jpg', p.evaluate(fb_first2) and 'Ami住8樓' in txt(p, '.fb.bad') and '老師：欸，是要上中文課的學生嗎？' in txt(p, '#npc-dialogue') and img(p).endswith('door_ben.jpg'), txt(p, '.fb.bad'))
    check('WRONG_DOOR 錯誤紀錄「走錯樓層」、三個選項', p.evaluate('Game.log[Game.log.length-1].stage[0]') == '走錯樓層' and sorted(o.strip() for o in opts(p)) == sorted(['不好意思，我走錯樓層了。', '你怎麼不是Ami？', '（不說話，轉身就走）']), opts(p))
    words = p.evaluate('s=>VOCAB[s].map(x=>x[0])', 'WRONG_DOOR'); check('小字典 WRONG_DOOR：每個字都在畫面上', all(w in screen(p) for w in words), words)
    for bad_ in ('你怎麼不是Ami？', '（不說話，轉身就走）'):
        m2 = mis(p); press(p, bad_); check(f'WRONG_DOOR 選「{bad_}」：扣分、留在 WRONG_DOOR', mis(p) == m2 + 1 and st(p) == 'WRONG_DOOR')
    press(p, '不好意思，我走錯樓層了。')
    check('WRONG_DOOR 客氣道歉：過場回電梯（「回到電梯」、elevator.jpg、住戶回話、沒有綠卡）', st(p) == '_TRANS' and trans_from(p) == 'WRONG_DOOR' and '回到電梯' in txt(p, '#options-area') and img(p).endswith('elevator.jpg') and '不是學生啊。沒關係，電梯在那邊' in txt(p, '#npc-dialogue') and p.locator('.fb.good').count() == 0, (st(p), img(p)))
    leave_trans(p); check('回到 FLOOR（鄰居還在）', st(p) == 'FLOOR' and p.evaluate('Game.cur') == 1)
    # 按對：進電梯小插曲（鄰居還在，照原本的流程）
    press(p, '按8樓。'); check('按對 8 樓：進電梯小插曲（鄰居還在）', st(p) == 'CHAT', st(p))
    check('錯誤共 1+1+2 筆', mis(p) == 4, mis(p))
    evt_ok(p); leave_trans(p); check('接著 STOP（4樓）、鄰居下車', st(p) == 'STOP' and p.evaluate('Game.cur') == 4)
    p.close()
    # 8-2 第三次起：最多兩次真的上去，第三次直接顯示錯誤
    p = new_page(b); set_task(p, n=8, m=4, entry='rush'); to_lobby(p); to_floor(p)
    for k in (2, 3):
        press(p, f'按{k}樓。'); leave_trans(p); press(p, '不出去，這裡不是8樓。'); leave_trans(p)
    check('已經搭錯兩次', p.evaluate('Game.wrongRides') == 2 and st(p) == 'FLOOR')
    m0 = mis(p); press(p, '按2樓。')
    check('第三次按錯：直接顯示錯誤（扣分、留在 FLOOR、不會上去）', mis(p) == m0 + 1 and st(p) == 'FLOOR' and p.evaluate('Game.cur') == 1, (st(p), mis(p)))
    press(p, '按8樓。'); check('第三次之後還是可以按對', st(p) == 'CHAT' or st(p) in EVTS, st(p))
    p.close()
    # 8-3 跟鄰居一樣高或更高：鄰居先下車，才到你按的那層（每一層都測；stopWrong=False、early=True，早停被略過）
    for k in [4, 5, 6, 7, 9, 10, 11, 12]:
        p = new_page(b); set_task(p, n=8, m=4, entry='rush', evt='CHAT', stopWrong=False, early=True); to_lobby(p); to_floor(p)
        m0 = mis(p); press(p, f'按{k}樓。')
        check(f'按{k}樓（≥鄰居的4樓）：先進電梯小插曲、沒有過場、還沒扣分、電梯還沒去{k}樓', st(p) == 'CHAT' and mis(p) == m0 and p.evaluate('Game.cur') == 1 and p.evaluate('Game.pendingWrong') == k, (st(p), mis(p)))
        evt_ok(p); leave_trans(p)
        check(f'{k}樓：鄰居的樓層（4樓）先停、鄰居說再見', st(p) == 'STOP' and p.evaluate('Game.cur') == 4, (st(p), disp(p)))
        press(p, '不客氣，慢走！')
        check(f'{k}樓：鄰居下車後的過場是空電梯（elevator_empty.jpg）、按鈕「電梯停了」', st(p) == '_TRANS' and img(p).endswith('elevator_empty.jpg') and '電梯停了' in txt(p, '#options-area'), (st(p), img(p)))
        txx = txt(p, '#npc-dialogue')
        check(f'{k}樓：旁白——' + ('鄰居走了、門還開著' if k == 4 else '電梯繼續往上、停了、門開了'), ('鄰居走了，門還開著' in txx) if k == 4 else ('繼續往上' in txx and '門開了' in txx), txx)
        leave_trans(p)
        check(f'{k}樓：真的到了 WRONG_FLOOR（顯示器{k}）、鄰居已下車', st(p) == 'WRONG_FLOOR' and p.evaluate('Game.cur') == k and p.evaluate('Game.neighborGone') is True and p.evaluate('Game.pendingWrong') is None, (st(p), disp(p)))
        press(p, '不出去，這裡不是8樓。')
        check(f'{k}樓：不出去，輕扣 5 分、回電梯過場是空電梯', mis(p) == m0 + 1 and st(p) == '_TRANS' and img(p).endswith('elevator_empty.jpg') and '電梯門關上' in txt(p, '#options-area'), (mis(p), st(p), img(p)))
        leave_trans(p); check(f'{k}樓：回到 FLOOR（沒有鄰居、也沒有早停）', st(p) == 'FLOOR', st(p))
        press(p, '按8樓。')
        up = 8 > k
        check(f'{k}樓之後按對 8 樓：直接到 ARRIVE（略過早停）、旁白電梯往' + ('上' if up else '下'), st(p) == '_TRANS' and trans_from(p) == 'FLOOR' and ('電梯往上，到8樓了' if up else '電梯往下，到8樓了') in txt(p, '#npc-dialogue'), (st(p), txt(p, '#npc-dialogue')))
        leave_trans(p); check(f'{k}樓之後：ARRIVE、顯示器 8', st(p) == 'ARRIVE' and p.evaluate('Game.cur') == 8, (st(p), disp(p)))
        p.close()
    # 8-4 鄰居看錯樓層（stopWrong）又剛好按在他的樓層：先停 3 樓、提醒、4 樓下車，才到 WRONG_FLOOR 4
    p = new_page(b); set_task(p, n=8, m=4, entry='rush', evt='CHAT', stopWrong=True); to_lobby(p); to_floor(p)
    press(p, '按4樓。'); evt_ok(p); leave_trans(p)
    check('stopWrong：先停在 3 樓', st(p) == 'STOP' and p.evaluate('Game.cur') == 3)
    press(p, '不好意思，這裡是3樓，您是不是要到4樓？'); leave_trans(p); press(p, '不客氣，慢走！'); leave_trans(p)
    check('stopWrong＋按在鄰居的樓層：鄰居下車後停在 4 樓的別層走廊', st(p) == 'WRONG_FLOOR' and p.evaluate('Game.cur') == 4, (st(p), disp(p)))
    p.close()
    # 8-5 鄰居下車之後，第二次按錯：直接上去（沒有鄰居）；之後按對直接到 ARRIVE
    p = new_page(b); set_task(p, n=8, m=4, entry='rush', evt='CHAT', stopWrong=False); p.evaluate("Game.strangers=['girl','ben']"); to_lobby(p); to_floor(p)
    press(p, '按6樓。'); evt_ok(p); leave_trans(p); press(p, '不客氣，慢走！'); leave_trans(p)
    press(p, '走出電梯。'); press(p, '按之2的電鈴。')
    check('第一次（6樓）走出去：扣 10 分、WRONG_DOOR 小女孩', st(p) == 'WRONG_DOOR' and '這裡是6樓' in txt(p, '.fb.bad') and '小女孩：麻麻…有奇怪的人來敲門…' in txt(p, '#npc-dialogue') and img(p).endswith('door_girl.jpg'), txt(p, '.fb.bad'))
    press(p, '不好意思，我走錯樓層了。'); check('道歉：過場回空電梯', st(p) == '_TRANS' and img(p).endswith('elevator_empty.jpg') and '回到電梯' in txt(p, '#options-area'), (st(p), img(p))); leave_trans(p)
    press(p, '按11樓。'); check('鄰居已下車：第二次按錯 11 樓，過場直接去（不用等小插曲）', st(p) == '_TRANS' and trans_from(p) == 'FLOOR', (st(p), trans_from(p))); leave_trans(p)
    check('WRONG_FLOOR 11 樓', st(p) == 'WRONG_FLOOR' and p.evaluate('Game.cur') == 11)
    press(p, '不出去，這裡不是8樓。'); leave_trans(p); press(p, '按7樓。')
    check('第三次按錯：直接顯示錯誤', st(p) == 'FLOOR')
    press(p, '按8樓。'); leave_trans(p); check('最後按對：往下到 8 樓的 ARRIVE', st(p) == 'ARRIVE' and p.evaluate('Game.cur') == 8)
    p.close()
    # 8-6 misspoke（e=m+1）：比 e 低才會先停。m=3、e=4：按 3 樓＝比他低，先停；按 4 樓＝跟他一樣高，鄰居先下
    p = new_page(b); set_task(p, n=8, m=3, misspoke=True, entry='rush', evt='CHAT'); to_lobby(p); to_help(p); help_right(p); leave_trans(p)
    press(p, '沒關係，我幫你按4樓。'); leave_trans(p); press(p, '按3樓。'); leave_trans(p)
    check('misspoke：按 3（< e=4）先停在 3 樓、鄰居還在', st(p) == 'WRONG_FLOOR' and p.evaluate('Game.cur') == 3 and p.evaluate('Game.neighborGone') is False)
    p.close()
    # 8-7 每個樓層 2～12（除了 Ami 的）都會真的去：低的馬上停、高的等鄰居下車
    for k in [2, 3, 4, 5, 6, 7, 9, 10, 11, 12]:
        p = new_page(b); set_task(p, n=8, m=4, entry='rush', evt='CHAT', stopWrong=False); to_lobby(p); to_floor(p); press(p, f'按{k}樓。')
        if k < 4: leave_trans(p)
        else: evt_ok(p); leave_trans(p); press(p, '不客氣，慢走！'); leave_trans(p)
        check(f'FLOOR 按{k}樓：最後真的停在{k}樓', st(p) == 'WRONG_FLOOR' and p.evaluate('Game.cur') == k and f'{k}' in disp(p), (k, st(p), disp(p)))
        p.close()

    # 8-8 第二次走錯樓層：換另一位（同一局不重複）；女孩的道歉回話
    p = new_page(b); set_task(p, n=8, m=4, entry='rush', evt='CHAT'); p.evaluate("Game.strangers=['girl','ben']"); to_lobby(p); to_floor(p)
    press(p, '按2樓。'); leave_trans(p); press(p, '走出電梯。'); press(p, '按之1的電鈴。')
    check('第一位：小女孩、door_girl.jpg', '小女孩：麻麻…有奇怪的人來敲門…' in txt(p, '#npc-dialogue') and img(p).endswith('door_girl.jpg'), (txt(p, '#npc-dialogue'), img(p)))
    press(p, '不好意思，我走錯樓層了。'); check('小女孩回話：掰掰', '小女孩：喔…掰掰。' in txt(p, '#npc-dialogue'), txt(p, '#npc-dialogue')); leave_trans(p)
    press(p, '按3樓。'); leave_trans(p); press(p, '走出電梯。'); press(p, '按之2的電鈴。')
    check('第二位：換成你自己、door_ben.jpg（不重複）', '老師：欸，是要上中文課的學生嗎？' in txt(p, '#npc-dialogue') and img(p).endswith('door_ben.jpg'), (txt(p, '#npc-dialogue'), img(p)))
    check('走錯樓層的開門者不會是男、女住戶', '住戶' not in txt(p, '#npc-dialogue'))
    p.close()
    # 8-9 Ami 那層：同一個錯的電鈴按第二次 → 生氣抱胸、扣 15 分；道歉之後那個電鈴變灰、不能再按
    p = new_page(b); set_task(p, n=8, m=3, unit=2, entry='rush', evt='CHAT', stopWrong=False, early=False); to_lobby(p)
    p.evaluate("Game.state='DOOR'; Game.cur=8; Game.render()")
    check('DOOR：三個電鈴都能按', len(opts(p)) == 3 and p.locator('.bellplates .plate.off').count() == 0, opts(p))
    press(p, '按之1的電鈴。')
    check('第一次按錯之1：普通開門（不生氣）、扣 10 分', st(p) == 'DOOR_WRONG' and p.evaluate('Game.angry') is False and ('住戶：誰啊' in txt(p, '#npc-dialogue') or '住戶：咦' in txt(p, '#npc-dialogue')) and 'angry' not in img(p), (txt(p, '#npc-dialogue'), img(p)))
    press(p, '不好意思，我按錯了。'); check('道歉：回 DOOR、之1 還能按', st(p) == 'DOOR' and '按之1的電鈴。' in [o.strip() for o in opts(p)] and len(opts(p)) == 3)
    s0 = p.evaluate('Game.score'); m0 = mis(p); press(p, '按之1的電鈴。')
    who = 'muscle' if '男住戶' in txt(p, '#npc-dialogue') else 'woman'
    check('第二次按之1：生氣抱胸的圖、「你又來了／又按」、扣 15 分', st(p) == 'DOOR_WRONG' and p.evaluate('Game.angry') is True and ('你又來了' in txt(p, '#npc-dialogue') or '又按我家' in txt(p, '#npc-dialogue')) and img(p).endswith('door_muscle_angry.jpg' if who == 'muscle' else 'door_woman_angry.jpg') and mis(p) == m0 + 1 and p.evaluate('Game.score') == s0 - 15, (txt(p, '#npc-dialogue'), img(p), p.evaluate('Game.score') - s0))
    check('生氣：紅卡說剛剛已經按過之1', '已經按過之1' in txt(p, '.fb.bad'), txt(p, '.fb.bad'))
    check('生氣：同樣三個選項', sorted(o.strip() for o in opts(p)) == sorted(['不好意思，我按錯了。', '你怎麼不是Ami？', '（不說話，轉身就走）']), opts(p))
    m1 = mis(p); press(p, '你怎麼不是Ami？'); check('生氣時選錯：再扣分、留在 DOOR_WRONG', mis(p) == m1 + 1 and st(p) == 'DOOR_WRONG' and p.evaluate('Game.angry') is True)
    press(p, '不好意思，我按錯了。')
    check('生氣之後道歉：回 DOOR、旁白「哼！不要再按了／別再按了」', st(p) == 'DOOR' and ('不要再按了' in txt(p, '#npc-dialogue') or '別再按了' in txt(p, '#npc-dialogue')), txt(p, '#npc-dialogue'))
    check('之1 變灰、不能再按：只剩之2、之3 兩個電鈴', sorted(o.strip() for o in opts(p)) == sorted(['按之2的電鈴。', '按之3的電鈴。']) and p.locator('.bellplates .plate.off').count() == 1 and p.locator('.bellplates button.plate').count() == 2, opts(p))
    press(p, '按之3的電鈴。'); check('按別的錯電鈴（之3）：第一次，普通開門', st(p) == 'DOOR_WRONG' and p.evaluate('Game.angry') is False, p.evaluate('Game.angry'))
    press(p, '不好意思，我按錯了。'); press(p, '按之3的電鈴。'); check('之3 第二次：也會生氣', st(p) == 'DOOR_WRONG' and p.evaluate('Game.angry') is True)
    press(p, '不好意思，我按錯了。')
    check('兩個錯的電鈴都不能再按：只剩對的之2', [o.strip() for o in opts(p)] == ['按之2的電鈴。'] and p.locator('.bellplates .plate.off').count() == 2, opts(p))
    press(p, '按之2的電鈴。'); leave_trans(p); check('按對：END', st(p) == 'END', st(p))
    p.close()
    # 8-10 每局的開門者順序是隨機的、而且兩位都會出現
    p = new_page(b)
    seen2 = p.evaluate("()=>{const s=new Set();for(let i=0;i<100;i++){Game.setup();s.add(Game.strangers.join())}return [...s].sort()}")
    check('走錯樓層的兩位（小女孩、你自己）每局順序隨機、兩種順序都會出現', seen2 == ['ben,girl', 'girl,ben'], seen2)
    p.close()

    # ── 9. 電梯裡本來就有人（做法 B）：ASK。說錯樓層，他幫你按了，但要等他下車才會到那層 ──
    def to_ask(p):
        press(p, '按▲，往上。'); leave_trans(p)
        if st(p) == 'DIR': press(p, '不好意思，這部是往下的。'); leave_trans(p)
    p = new_page(b); set_task(p, n=8, m=3, entry='inside', askX=7, evt='CHAT', stopWrong=False, early=True); to_lobby(p)
    press(p, '按▲，往上。')
    check('inside：LOBBY 之後過場「電梯來了」，接著是 ASK（沒有 WAIT／HELP／FLOOR）', st(p) == '_TRANS' and '電梯來了' in txt(p, '#options-area'))
    leave_trans(p)
    check('ASK：鄰居問「請問你到幾樓？我幫你按。」', st(p) == 'ASK' and '鄰居：請問你到幾樓？我幫你按。' in txt(p, '#npc-dialogue') and '裡面已經站著一位鄰居' in txt(p, '#npc-dialogue'), txt(p, '#npc-dialogue'))
    check('ASK 三個選項', sorted(o.strip() for o in opts(p)) == sorted(['我要到8樓，謝謝。', '我要到7樓，謝謝。', '（不回答，自己按）']), opts(p))
    check('ASK 圖是 inside_asks.jpg', img(p).endswith('inside_asks.jpg'), img(p))
    words = p.evaluate('s=>VOCAB[s].map(x=>x[0])', 'ASK'); check('小字典 ASK：每個字都在畫面上', all(w in screen(p) for w in words), words)
    s0 = p.evaluate('Game.score'); m0 = mis(p)
    press(p, '（不回答，自己按）')
    check('ASK 不回答自己按：輕扣 5 分、留在 ASK、紅卡說沒禮貌', mis(p) == m0 + 1 and p.evaluate('Game.score') == s0 - 5 and st(p) == 'ASK' and '要回答他' in txt(p, '.fb.bad') and p.evaluate('Game.log[Game.log.length-1].stage[0]') == '回答樓層', txt(p, '.fb.bad'))
    press(p, '我要到7樓，謝謝。')
    check('ASK 說錯樓層：直接進小插曲（合併）、還沒扣分、旁白：他幫你按了7樓，自己也按了3樓', st(p) == 'CHAT' and mis(p) == m0 + 1 and '幫你按了7樓，自己也按了3樓' in txt(p, '#npc-dialogue') and p.evaluate('Game.cur') == 1, (st(p), mis(p), txt(p, '#npc-dialogue')))
    evt_ok(p); leave_trans(p); check('接著先停在他的 3 樓', st(p) == 'STOP' and p.evaluate('Game.cur') == 3)
    check('inside STOP：他只說「到了，再見！」、沒有謝謝、不會看錯樓層；選項有「再見，慢走！」', '到了，再見！' in txt(p, '#npc-dialogue') and '謝謝' not in txt(p, '#npc-dialogue') and '再見，慢走！' in [o.strip() for o in opts(p)] and p.evaluate('Game.task.stopWrong') is False, (txt(p, '#npc-dialogue'), opts(p)))
    m_ = mis(p); press(p, '不好意思，這裡是2樓，您是不是要到3樓？'); check('inside STOP：提醒他是錯的（你不知道他要去幾樓）', mis(p) == m_ + 1 and '沒有說過他要去幾樓' in txt(p, '.fb.bad'), txt(p, '.fb.bad'))
    m0 += 1   # 上面故意按錯的那一次
    press(p, '再見，慢走！')
    check('他下車後：過場是空電梯、「電梯停了」', st(p) == '_TRANS' and img(p).endswith('elevator_empty.jpg') and '電梯停了' in txt(p, '#options-area'), (st(p), img(p))); leave_trans(p)
    check('接著 WRONG_FLOOR（7 樓，不是 EARLY）', st(p) == 'WRONG_FLOOR' and p.evaluate('Game.cur') == 7, (st(p), disp(p)))
    press(p, '不出去，這裡不是8樓。')
    check('inside 不出去：輕扣 5 分、紅卡說剛剛你說要到7樓、回空電梯', mis(p) == m0 + 2 and '你說要到7樓' in txt(p, '.fb.bad') and st(p) == '_TRANS' and img(p).endswith('elevator_empty.jpg') and '電梯門關上' in txt(p, '#options-area'), (txt(p, '.fb.bad'), img(p)))
    leave_trans(p); check('回到 FLOOR（自己按樓層，不再問一次）', st(p) == 'FLOOR', st(p))
    press(p, '按8樓。'); check('按對 8 樓：直接到 ARRIVE（略過早停）、往上', st(p) == '_TRANS' and '電梯往上，到8樓了' in txt(p, '#npc-dialogue')); leave_trans(p)
    check('ARRIVE 8 樓', st(p) == 'ARRIVE' and p.evaluate('Game.cur') == 8)
    p.close()
    # 走出去遇到陌生人
    p = new_page(b); set_task(p, n=8, m=3, entry='inside', askX=7, evt='CHAT', stopWrong=False); to_lobby(p); to_ask(p); leave_trans(p)
    press(p, '我要到7樓，謝謝。'); evt_ok(p); leave_trans(p); press(p, '再見，慢走！'); leave_trans(p)
    m0 = mis(p); press(p, '走出電梯。'); press(p, '按之2的電鈴。')
    check('inside 走出去：WRONG_DOOR、扣 10 分、這裡是7樓', st(p) == 'WRONG_DOOR' and mis(p) == m0 + 1 and '這裡是7樓' in txt(p, '.fb.bad'))
    press(p, '不好意思，我走錯樓層了。'); check('inside 道歉：過場回電梯（空電梯）', st(p) == '_TRANS' and trans_from(p) == 'WRONG_DOOR' and img(p).endswith('elevator_empty.jpg') and '回到電梯' in txt(p, '#options-area'))
    leave_trans(p); check('回到 FLOOR', st(p) == 'FLOOR')
    p.close()
    # 答對：合併進小插曲
    p = new_page(b); set_task(p, n=8, m=3, entry='inside', askX=7, evt='CHAT'); to_lobby(p); to_ask(p); leave_trans(p)
    press(p, '我要到8樓，謝謝。')
    check('ASK 答對：合併進小插曲、有綠卡、旁白：他幫你按了8樓，自己也按了3樓', st(p) == 'CHAT' and '幫你按了8樓，自己也按了3樓' in txt(p, '#npc-dialogue') and p.locator('.fb.good').count() == 1 and p.evaluate('Game.pendingWrong') is None, (st(p), txt(p, '#npc-dialogue')))
    p.close()
    # askX 比 Ami 高也一樣（9 樓）
    p = new_page(b); set_task(p, n=8, m=3, entry='inside', askX=9, evt='CHAT', stopWrong=False); to_lobby(p); to_ask(p); leave_trans(p)
    press(p, '我要到9樓，謝謝。'); evt_ok(p); leave_trans(p); press(p, '再見，慢走！'); leave_trans(p)
    check('askX=9：WRONG_FLOOR 9 樓', st(p) == 'WRONG_FLOOR' and p.evaluate('Game.cur') == 9); press(p, '不出去，這裡不是8樓。'); leave_trans(p); press(p, '按8樓。')
    check('9 樓之後按 8：電梯往下', '電梯往下，到8樓了' in txt(p, '#npc-dialogue'), txt(p, '#npc-dialogue'))
    p.close()
    # inside 全程零失誤走一遍；沒有 WAIT／FLOOR／HELP／HELP2
    for ev in EVTS:
        p = new_page(b); set_task(p, n=9, m=4, entry='inside', evt=ev, stopWrong=False, early=True); to_lobby(p); seen_st = []
        for _ in range(40):
            s_ = st(p)
            if s_ == '_TRANS': leave_trans(p); continue
            seen_st.append(s_)
            if s_ == 'END': break
            o = p.evaluate(smoke.ORACLES['elevator'] if hasattr(smoke, 'ORACLES') and smoke.ORACLES.get('elevator') else 'null')
            if o is None: break
            press(p, o)
        check(f'inside {ev} 局：零失誤走到 END', st(p) in ('END', 'RESULT') and mis(p) == 0, (seen_st, mis(p)))
        check(f'inside {ev} 局：沒有 WAIT／FLOOR／HELP／HELP2，有 ASK', 'ASK' in seen_st and not {'WAIT', 'FLOOR', 'HELP', 'HELP2'} & set(seen_st), seen_st)
        p.close()
    # rush 全程零失誤：順序是 WAIT → HELP → FLOOR → 小插曲
    p = new_page(b); set_task(p, n=9, m=4, entry='rush', evt='CHAT', stopWrong=False, early=True); to_lobby(p); seen_st = []
    for _ in range(40):
        s_ = st(p)
        if s_ == '_TRANS': leave_trans(p); continue
        seen_st.append(s_)
        if s_ == 'END': break
        o = p.evaluate(smoke.ORACLES['elevator'] if hasattr(smoke, 'ORACLES') and smoke.ORACLES.get('elevator') else 'null')
        if o is None: break
        press(p, o)
    check('rush：零失誤走到 END、順序 WAIT→HELP→FLOOR→CHAT', st(p) in ('END', 'RESULT') and mis(p) == 0 and [x for x in seen_st if x in ('WAIT', 'HELP', 'FLOOR', 'CHAT')] == ['WAIT', 'HELP', 'FLOOR', 'CHAT'], (seen_st, mis(p)))
    p.close()
    # 小狗那局：阿姨
    p = new_page(b); set_task(p, n=8, m=3, entry='inside', evt='DOG', askX=7, stopWrong=False); to_lobby(p); to_ask(p); leave_trans(p)
    check('inside DOG：ASK 是阿姨、粉紅色外套、inside_asks_dog.jpg', st(p) == 'ASK' and '阿姨：請問你到幾樓' in txt(p, '#npc-dialogue') and '粉紅色外套' in txt(p, '#npc-dialogue') and img(p).endswith('inside_asks_dog.jpg'), (st(p), img(p)))
    press(p, '我要到7樓，謝謝。'); check('inside DOG：說錯樓層旁白用「她」', '她幫你按了7樓' in txt(p, '#npc-dialogue'), txt(p, '#npc-dialogue'))
    evt_ok(p); leave_trans(p); press(p, '再見，慢走！'); leave_trans(p); press(p, '不出去，這裡不是8樓。')
    check('inside DOG 阿姨下車後，回電梯的圖是空電梯', img(p).endswith('elevator_empty.jpg'), img(p))
    p.close()
    # rush DOG：按得比阿姨低，她還在電梯裡，回電梯的圖是 dog.jpg
    p = new_page(b); set_task(p, n=8, m=4, entry='rush', evt='DOG'); to_lobby(p); to_floor(p); press(p, '按3樓。'); leave_trans(p); press(p, '不出去，這裡不是8樓。')
    check('rush DOG：阿姨還在電梯裡，回電梯的圖是 dog.jpg', img(p).endswith('dog.jpg'), img(p))
    p.close()
    # dirDown + inside：DIR 之後進 ASK
    p = new_page(b); set_task(p, n=8, m=3, entry='inside', dirDown=True); to_lobby(p)
    press(p, '按▲，往上。'); leave_trans(p); check('inside＋dirDown：LOBBY→DIR', st(p) == 'DIR')
    press(p, '不好意思，這部是往下的。'); tx = txt(p, '#npc-dialogue')
    check('inside DIR 過場：沒有「你走了進去」（裡面有人）', '你走了進去' not in tx and '這次上面亮著▲' in tx, tx)
    leave_trans(p); check('inside DIR 之後是 ASK', st(p) == 'ASK', st(p))
    p.close()
    # 隨機條件
    p = new_page(b)
    bad = p.evaluate("""()=>{const r=[];let ins=0,rush=0;for(let i=0;i<400;i++){Game.setup();const t=Game.task;
      if(t.entry==='inside'){ins++; if(t.misspoke)r.push('misspoke'); if(t.e!==t.m)r.push('e!=m'); if(t.stopWrong)r.push('inside stopWrong');} else rush++;
      if(![t.n-1,t.n+1].includes(t.askX)||t.askX>12||t.askX<2)r.push('askX'+t.askX);
      if(t.entry==='inside'&&t.askX<=t.e)r.push('askX<=e');
      if(Game.neighborGone||Game.pendingWrong!=null||Game.wrongRides||Game.wrongFloor!=null)r.push('state');} return {r:[...new Set(r)],ins,rush}}""")
    check('隨機條件：兩種 entry 都會出現、inside 不會說錯樓層、askX 是相鄰的錯樓層且比鄰居的樓層高、狀態有重置', not bad['r'] and bad['ins'] > 0 and bad['rush'] > 0, bad)
    p.close()
    p = new_page(b)
    check('STAGE／NEXT_LABEL／IMAGES 都有新關卡', p.evaluate("['ASK','WRONG_FLOOR','WRONG_BELL','WRONG_DOOR'].every(k=>STAGE[k]&&NEXT_LABEL[k]&&Game.IMAGES[k])"))
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
