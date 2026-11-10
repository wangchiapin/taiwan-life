r"""搭電梯專用測試：python3 tools/elevator_test.py
三種「對方出錯」每個選項都按過（強制出現，不靠運氣）：
  DIR   大廳先開門的電梯是往下的，阿姨問「是往上的嗎？」：對／客氣提醒／沒禮貌；沒有這一關時直接去 WAIT
  HELP2 鄰居說錯樓層：客氣回應／翻舊帳／不管他
  STOP  電梯停在低一層，鄰居看錯想出去：慢走／客氣提醒／沒禮貌；沒看錯時，亂提醒要扣分；提醒後 STOP_FIX 再來一次
還檢查：每局隨機的條件（m 是 3 或 4、misspoke 不會和 lit 同時、早停樓層在 e 和 Ami 之間）、
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

def set_task(page, n=8, m=3, misspoke=False, dirDown=False, stopWrong=False, early=False, lit=False):
    """把這一局的隨機條件固定下來（和 setup() 的規則一致）"""
    page.evaluate("""o=>{const t=Game.task; Object.assign(t,{n:o.n,m:o.m,misspoke:o.misspoke,e:o.misspoke?o.m+1:o.m,lit:o.lit&&!o.misspoke,dirDown:o.dirDown,stopWrong:o.stopWrong});
      const xs=Array.from({length:t.n-t.e-1},(_,i)=>t.e+1+i); t.x=xs.length?xs[0]:null; t.early=o.early&&xs.length>0; Game.render();}""",
      dict(n=n, m=m, misspoke=misspoke, dirDown=dirDown, stopWrong=stopWrong, early=early, lit=lit))

def to_lobby(page): press(page, '走進大樓'); leave_trans(page); assert st(page) == 'LOBBY', st(page)
def to_help(page):   # LOBBY 之後到 HELP（DIR 若有，先答對）
    press(page, '按▲，往上。'); leave_trans(page)
    if st(page) == 'DIR': press(page, '不好意思，這部是往下的。'); leave_trans(page)
    assert st(page) == 'WAIT', st(page)
    press(page, '按「開門」，等他。'); leave_trans(page); assert st(page) == 'FLOOR', st(page)
    press(page, f"按{page.evaluate('Game.task.n')}樓。"); leave_trans(page); assert st(page) == 'HELP', st(page)
def help_right(page):
    t = page.evaluate('({m:Game.task.m,lit:Game.task.lit})')
    press(page, f"不用按，{t['m']}樓已經亮了喔。" if t['lit'] else f"好，我幫你按{t['m']}樓。")

def run(b):
    # ── 1. 每局隨機條件的規則（setup 跑 300 次）──
    p = new_page(b)
    bad = p.evaluate("""()=>{const r=[];for(let i=0;i<300;i++){Game.setup();const t=Game.task;
      if(![3,4].includes(t.m))r.push('m'+t.m); if(t.misspoke&&t.lit)r.push('misspoke+lit'); if(t.e!==(t.misspoke?t.m+1:t.m))r.push('e');
      if(t.e>=t.n)r.push('e>=n'); if(t.early&&!(t.x>t.e&&t.x<t.n))r.push('x'+t.x+'e'+t.e+'n'+t.n); if(!t.early&&t.x!=null&&!(t.x>t.e&&t.x<t.n))r.push('x2');
      if(t.e-1<2)r.push('e-1<2');}
      const seen={misspoke:0,lit:0,dirDown:0,stopWrong:0,early:0};for(let i=0;i<300;i++){Game.setup();for(const k in seen)if(Game.task[k])seen[k]++;}
      return {r:[...new Set(r)],seen}}""")
    check('每局隨機條件都符合規則', not bad['r'], bad['r'])
    check('三種錯誤和燈、早停都會出現（300 局）', all(v > 0 for v in bad['seen'].values()), bad['seen'])
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
        check('DIR 過場：阿姨的道歉＋右邊電梯', '是往下的！不好意思，謝謝你！' in tx and '右邊那部電梯也開了' in tx, tx)
        check('DIR 過場：第一次就對才有綠卡', (p.locator('.fb.good').count() == 1) == (first == 'fix'), p.locator('.fb.good').count())
        leave_trans(p); check('DIR 之後是 WAIT', st(p) == 'WAIT' and not disp(p).startswith('▼'), (st(p), disp(p)))
        p.close()

    # ── 3. HELP2：鄰居說錯樓層 ──
    for first in ('rude1', 'rude2', None):
        p = new_page(b); set_task(p, misspoke=True); to_lobby(p); to_help(p)
        check('HELP 鄰居說要到 m 樓、燈沒亮', '3樓' in screen(p) and '面板上' not in screen(p), screen(p))
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
        press(p, '沒關係，我幫你按4樓。'); check('HELP2 客氣回應：進過場', st(p) == '_TRANS' and trans_from(p) == 'HELP2')
        check('HELP2 過場：第一次就對才有綠卡', (p.locator('.fb.good').count() == 1) == (first is None))
        leave_trans(p); check('HELP2 之後是 STOP（停在4樓，沒看錯）', st(p) == 'STOP' and p.evaluate('Game.cur') == 4, (st(p), p.evaluate('Game.cur')))
        p.close()
    # misspoke 時 lit 不會出現：HELP 沒有「不用按」的選項是對的
    p = new_page(b); set_task(p, misspoke=True, lit=True); to_lobby(p); to_help(p)
    check('misspoke 時燈不會亮', '面板上' not in screen(p) and p.evaluate('Game.task.lit') is False, screen(p))
    p.close()

    # ── 4. STOP：鄰居看錯樓層（stopWrong）──
    for first in ('ok', 'rude', 'fix'):
        p = new_page(b); set_task(p, stopWrong=True, early=(first == 'fix')); to_lobby(p); to_help(p); help_right(p); leave_trans(p)
        check('STOP 停在低一層（2樓）', st(p) == 'STOP' and p.evaluate('Game.cur') == 2 and '2' in disp(p), (st(p), disp(p)))
        check('STOP 三個選項', sorted(o.strip() for o in opts(p)) == sorted(['不客氣，慢走！', '不好意思，這裡是2樓，您是不是要到3樓？', '你走錯了！']), opts(p))
        m0 = mis(p)
        if first != 'fix':
            press(p, '不客氣，慢走！' if first == 'ok' else '你走錯了！')
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
    p = new_page(b); set_task(p, stopWrong=False); to_lobby(p); to_help(p); help_right(p); leave_trans(p)
    check('沒看錯：STOP 停在3樓', st(p) == 'STOP' and p.evaluate('Game.cur') == 3 and '3' in disp(p), (st(p), disp(p)))
    m0 = mis(p); press(p, '不好意思，這裡是2樓，您是不是要到3樓？')
    check('沒看錯時亂提醒：扣分、留在 STOP', mis(p) == m0 + 1 and st(p) == 'STOP')
    check('亂提醒的提示：這裡就是3樓', '這裡就是3樓' in txt(p, '.fb.bad'), txt(p, '.fb.bad'))
    press(p, '你走錯了！'); check('沒看錯時說「你走錯了」：扣分', mis(p) == m0 + 2)
    press(p, '不客氣，慢走！')
    check('沒看錯時慢走：不進 STOP_FIX', st(p) in ('_TRANS', 'ARRIVE', 'EARLY') and trans_from(p) in (None, 'STOP')); leave_trans(p)
    check('沒看錯時慢走：直接 ARRIVE', st(p) == 'ARRIVE', st(p))
    p.close()

    # ── 5. 三種錯誤一次都遇到，整局打到排行榜（照提醒、照回應走）──
    p = new_page(b); set_task(p, n=9, m=4, misspoke=True, dirDown=True, stopWrong=True, early=True); to_lobby(p); to_help(p)
    check('全部一起：HELP 要按4樓', '4樓' in screen(p))
    help_right(p); leave_trans(p); press(p, '沒關係，我幫你按5樓。'); leave_trans(p)
    check('全部一起：STOP 停在4樓（e=5）', st(p) == 'STOP' and p.evaluate('Game.cur') == 4, (st(p), p.evaluate('Game.cur')))
    press(p, '不好意思，這裡是4樓，您是不是要到5樓？'); leave_trans(p)
    check('全部一起：STOP_FIX 5樓', st(p) == 'STOP_FIX' and p.evaluate('Game.cur') == 5)
    press(p, '不客氣，慢走！'); leave_trans(p)
    check('全部一起：EARLY 在 6~8 樓之間', st(p) == 'EARLY' and 6 <= p.evaluate('Game.cur') <= 8, (st(p), p.evaluate('Game.cur')))
    press(p, '不出去，這裡不是9樓。'); leave_trans(p); press(p, '不好意思，借過一下。'); leave_trans(p)
    check('全部一起：END、100 分、0 錯誤', st(p) == 'END' and p.evaluate('Game.score') == 100 and mis(p) == 0, (st(p), p.evaluate('Game.score')))
    check('這一局用到的圖都載得到（沒有缺圖）', p.evaluate('Game.missing.size') == 0, p.evaluate('[...Game.missing]'))
    p.close()
    for f in ('dir.jpg', 'dir_sorry.jpg', 'neighbor_sorry.jpg'):
        check(f'新圖檔存在：{f}', os.path.exists(os.path.join(HERE, '..', 'games', 'elevator', 'images', f)))
    # 邊界：n=6, m=4, misspoke → e=5，後面沒有樓層可以早停
    p = new_page(b); set_task(p, n=6, m=4, misspoke=True, early=True)
    check('n=6,m=4,misspoke：沒有早停', p.evaluate('Game.task.early') is False and p.evaluate('Game.task.x') is None)
    p.close()

    # ── 6. 小字典的字都出現在那一關的畫面上 ──
    p = new_page(b); set_task(p, misspoke=True, dirDown=True, stopWrong=True); to_lobby(p)
    press(p, '按▲，往上。'); leave_trans(p)
    def vocab_ok(state):
        words = p.evaluate('s=>VOCAB[s].map(x=>x[0])', state); sc = screen(p)
        miss = [w for w in words if w not in sc]; check(f'小字典 {state}：每個字都在畫面上', not miss, miss)
    vocab_ok('DIR'); press(p, '不好意思，這部是往下的。'); leave_trans(p)
    press(p, '按「開門」，等他。'); leave_trans(p)
    press(p, f"按{p.evaluate('Game.task.n')}樓。"); leave_trans(p)
    help_right(p); leave_trans(p); vocab_ok('HELP2'); press(p, '沒關係，我幫你按4樓。'); leave_trans(p); vocab_ok('STOP')
    press(p, '不好意思，這裡是3樓，您是不是要到4樓？'); leave_trans(p); vocab_ok('STOP_FIX')
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
