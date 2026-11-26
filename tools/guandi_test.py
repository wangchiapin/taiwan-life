# 關帝廟測試：擲筊三種劇本、往上滑／拖／點的操作、每個選項、插香流程。用法：python3 tools/guandi_test.py
import sys, collections
sys.argv = ['x', 'perfect', 'guandi']
import smoke
from smoke import sync_playwright, route, PORT

ok = fail = 0
def check(name, cond, extra=''):
    global ok, fail
    if cond: ok += 1
    else: fail += 1; print('✗', name, extra)
ev = lambda p, js: p.evaluate(js)

def open_game(b, errs, mobile=False):
    kw = dict(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True) if mobile else dict(viewport={'width': 1000, 'height': 900})
    ctx = b.new_context(**kw); ctx.route('**/*', route); page = ctx.new_page()
    page.on('pageerror', lambda e: errs.append(str(e))); page.on('dialog', lambda d: d.accept())
    page.goto(f'http://127.0.0.1:{PORT}/games/guandi/index.html'); page.wait_for_timeout(400)
    page.fill('#player-name-input', 'María'); page.click('.btn-primary'); page.wait_for_timeout(300)
    return ctx, page

def jump(page, state, plan=None):
    ev(page, f"""(()=>{{ {f"let n=0; do Game.setup(); while(Game.task.plan!=='{plan}' && ++n<500);" if plan else 'Game.setup();'}
      Game.state='{state}'; Game.thought=null; Game.feedback=[]; Game._trans=null; Game.render(); }})()""")

def opt(page, text):
    page.locator('#options-area .opt', has_text=text).first.click() if False else ev(page, f"Game.handleChoice({text!r})")

def txt(page, sel='#npc-dialogue'):
    """畫面上的文字（拿掉拼音）"""
    return ev(page, f"(()=>{{const c=document.querySelector('{sel}').cloneNode(true);c.querySelectorAll('rt').forEach(r=>r.remove());return c.textContent}})()")

def swipe(page, dy, steps=5):
    """用 CDP 送真的觸控事件（手指滑動）"""
    el = page.locator('.toss[role=button]'); el.scroll_into_view_if_needed(); b = el.bounding_box()
    x, y = b['x'] + b['width'] / 2, b['y'] + b['height'] * .7
    cdp = page.context.new_cdp_session(page)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]})
    for i in range(1, steps + 1):
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x, 'y': y + dy * i / steps}]}); page.wait_for_timeout(16)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); page.wait_for_timeout(60); cdp.detach()

with sync_playwright() as p:
    b = p.chromium.launch(); errs = []
    # ── 手機：往上滑才丟 ──
    ctx, page = open_game(b, errs, mobile=True)
    jump(page, 'THROW', '甲')
    check('手機提示是往上滑', '往上滑' in ev(page, "(()=>{const c=document.querySelector('.toss').cloneNode(true);c.querySelectorAll('rt').forEach(r=>r.remove());return c.textContent})()"))
    check('丟之前沒有選項', page.locator('#options-area .opt').count() == 0)
    page.screenshot(path='/tmp/t_ready.png')
    page.locator('.toss.ready').tap(); page.wait_for_timeout(200)
    check('手機點一下不會丟', ev(page, 'Game.phase') == 'ready')
    swipe(page, 90)
    check('往下滑不會丟', ev(page, 'Game.phase') == 'ready')
    y0 = ev(page, 'scrollY'); swipe(page, -110)
    check('往上滑會丟', ev(page, 'Game.phase') in ('fly', 'landed'))
    check('上滑時畫面不捲動', abs(ev(page, 'scrollY') - y0) < 3, (y0, ev(page, 'scrollY')))
    page.wait_for_timeout(350); page.screenshot(path='/tmp/t_fly.png')
    page.wait_for_timeout(1000)
    check('第一次笑筊／陰筊時沒有任何按鈕', ev(page, 'Game.phase') == 'landed' and page.locator('#options-area .opt').count() == 0)
    check('Ami 說結果', 'Ami：是' in txt(page) and '再丟一次' in txt(page), txt(page))
    check('可以直接再滑', '再往上滑一次' in txt(page))
    page.wait_for_timeout(500)
    check('落地後看得到 Ami 的話', ev(page, "document.querySelector('#npc-dialogue').getBoundingClientRect().bottom <= innerHeight + 1"))
    page.screenshot(path='/tmp/t_landed.png', full_page=True)
    page.locator('.toss.again').tap(); page.wait_for_timeout(200)
    check('落地後點一下不會丟', ev(page, 'Game.ti') == 1 and ev(page, 'Game.phase') == 'landed')
    swipe(page, -110); page.wait_for_timeout(1300)
    check('再滑一次得到聖筊、出現一顆按鈕', ev(page, 'Game.ti') == 2 and page.locator('#options-area .opt').count() == 1 and '可以抽籤了' in txt(page))
    check('聖筊以後不能再丟', page.locator('.toss[role=button]').count() == 0)
    page.screenshot(path='/tmp/t_pass.png', full_page=True)
    page.locator('#options-area .opt').click(); page.wait_for_timeout(200)
    check('按鈕直接到抽籤（不跳過場）', ev(page, 'Game.state') == 'DRAW')
    ctx.close()
    # ── 電腦：點、拖、鍵盤 ──
    ctx, page = open_game(b, errs)
    for name in ('點一下', '往上拖', '鍵盤'):
        jump(page, 'THROW', '乙'); el = page.locator('.toss.ready'); bb = el.bounding_box(); x, y = bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] * .7
        if name == '點一下': page.mouse.click(x, y)
        elif name == '往上拖': page.mouse.move(x, y); page.mouse.down(); page.mouse.move(x, y - 120, steps=6); page.mouse.up()
        else: el.focus(); page.keyboard.press('Enter')
        page.wait_for_timeout(1300); check('電腦' + name + '會丟', ev(page, 'Game.phase') == 'landed')
    jump(page, 'THROW', '甲')
    for i in (1, 2):
        el = page.locator('.toss[role=button]'); bb = el.bounding_box(); page.mouse.click(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] * .5); page.wait_for_timeout(1300)
        check('電腦落地後再點一下會再丟', ev(page, 'Game.ti') == i)
    jump(page, 'THROW', '乙'); bb = page.locator('.toss.ready').bounding_box(); x, y = bb['x'] + bb['width'] / 2, bb['y'] + 40
    page.mouse.move(x, y); page.mouse.down(); page.mouse.move(x, y + 80, steps=4); page.mouse.up(); page.wait_for_timeout(200)
    check('電腦往下拖不會丟', ev(page, 'Game.phase') == 'ready')
    # ── 三種劇本：次數、重抽、Ami 的話、按鈕 ──
    page.emulate_media(reduced_motion='reduce')
    for plan, want in (('甲', 5), ('乙', 5), ('丙', 6)):
        for run in range(4):
            jump(page, 'THROW', plan); ev(page, "Game.mistakes=0; Game.score=100")
            throws, non, sticks, steps = 0, 0, [], 0
            while ev(page, 'Game.state') != 'SLIP_NUM' and steps < 60:
                steps += 1; st = ev(page, 'Game.state')
                if st == '_TRANS': ev(page, 'Game.handleChoice(Game.transLabel())'); continue
                if st == 'DRAW':
                    for bad in ('一次抽兩支，比較保險。', '用手在籤筒裡挑一支自己喜歡的。'):
                        m = ev(page, 'Game.mistakes'); opt(page, bad); check('抽籤錯選扣分', ev(page, 'Game.mistakes') == m + 1 and ev(page, 'Game.state') == 'DRAW')
                    sticks.append(ev(page, 'Game.drawnSlip().n')); opt(page, '搖一搖籤筒，讓一支籤自己掉出來。'); page.wait_for_function('()=>!Game.busy'); continue
                if ev(page, 'Game.phase') == 'ready':
                    n = ev(page, 'slipNo(Game.drawnSlip().n)')
                    mine = '我可以抽籤嗎？' if st == 'THROW' else f'請問是{n}嗎？'
                    t_ = txt(page)
                    check('丟之前只有玩家那一句', mine in t_ and 'Ami' not in t_ and page.locator('#options-area .opt').count() == 0, t_)
                page.locator('.toss[role=button]').focus(); page.keyboard.press('Enter'); page.wait_for_timeout(230); throws += 1
                k = ev(page, 'Game.last'); non += k != 'sheng'
                faces = ev(page, "[...document.querySelectorAll('.toss.landed .bei')].map(e=>e.classList.contains('flat')?'flat':'round')")
                check('畫面的筊杯和結果一致', faces == ev(page, f"RES['{k}'].cups"), (k, faces))
                t_, streak, go = txt(page), ev(page, 'Game.streak'), ev(page, 'Game.goNext')
                zh = ev(page, f"RES['{k}'].zh")
                if st == 'THROW': say = '是聖筊！可以抽籤了。' if k == 'sheng' else f'是{zh}，神明'
                elif k != 'sheng': say = f'是{zh}，不是這支籤。重新抽一支吧。'
                else: say = '三個聖筊！就是這支籤。' if streak == 3 else '聖筊！再丟一次。'
                check('Ami 說的結果正確', 'Ami：' + say in t_, (st, k, streak, t_))
                if st == 'CONFIRM': check('連續聖筊計數', f'：{streak} / 3' in t_, t_)
                btns = page.locator('#options-area .opt').count()
                check('只有要換下一步時才有一顆按鈕', btns == (1 if go else 0), (btns, go))
                if go:
                    label = txt(page, '#options-area')
                    want_label = '走到籤櫃' if go == 'SLIP_NUM' else ('走到籤筒前' if st == 'THROW' else '回到籤筒重抽')
                    check('按鈕文字', label == want_label, label)
                    page.locator('#options-area .opt').click(); page.wait_for_timeout(60)
                    check('按鈕直接到下一步', ev(page, 'Game.state') == go, ev(page, 'Game.state'))
            check(f'{plan} 丟 {want} 次', throws == want, throws)
            check(f'{plan} 剛好一次笑筊／陰筊', non == 1, non)
            check(f'{plan} 抽籤次數', len(sticks) == (1 if plan == '甲' else 2), sticks)
            check(f'{plan} 重抽是不同的籤', len(set(sticks)) == len(sticks), sticks)
            check(f'{plan} 最後的籤和籤櫃一致', sticks and sticks[-1] == ev(page, 'Game.task.slip.n'))
    page.emulate_media(reduced_motion='no-preference')
    dist = ev(page, "(()=>{const c={};for(let i=0;i<4000;i++){Game.setup();c[Game.task.plan]=(c[Game.task.plan]||0)+1}return c})()")
    check('劇本比例 50/25/25', abs(dist['甲'] / 4000 - .5) < .05 and abs(dist['乙'] / 4000 - .25) < .04 and abs(dist['丙'] / 4000 - .25) < .04, dist)
    # ── 丟到一半重畫、離開關卡 ──
    jump(page, 'THROW', '甲'); ev(page, 'Game.toss(); Game.toss(); Game.render()'); page.wait_for_timeout(1300)
    check('連按只丟一次', ev(page, 'Game.phase') == 'landed' and ev(page, 'Game.ti') == 1)
    # ── 籤筒聲：播完才跳頁、靜音不用等 ──
    SHK = '搖一搖籤筒，讓一支籤自己掉出來。'
    def btn():   # 「搖一搖」那顆按鈕（選項順序每局不同）
        i = ev(page, "[...document.querySelectorAll('#options-area .opt')].findIndex(b=>{const c=b.cloneNode(true);c.querySelectorAll('rt').forEach(r=>r.remove());return c.textContent.includes('搖一搖')})")
        return page.locator('#options-area .opt').nth(i)
    jump(page, 'DRAW'); a0 = ev(page, 'Game.att.DRAW||0'); btn().click(); page.wait_for_timeout(400)
    check('按下後先播聲音、還沒跳頁', ev(page, 'Game.busy') and ev(page, 'Game.state') == 'DRAW' and ev(page, 'Game.sfx.state') == 'running')
    check('播放中按鈕不能按', ev(page, "[...document.querySelectorAll('#options-area .opt')].every(b=>b.disabled)"))
    ev(page, "Game.handleChoice(" + repr(SHK) + ")")
    m = ev(page, 'Game.mistakes'); ev(page, "Game.handleChoice('一次抽兩支，比較保險。')"); check('播放中錯選沒有作用', ev(page, 'Game.mistakes') == m)
    page.wait_for_timeout(1200); check('1.6 秒時還在播', ev(page, 'Game.state') == 'DRAW')
    page.wait_for_timeout(1100); check('播完跳過場', ev(page, 'Game.state') == '_TRANS' and not ev(page, 'Game.busy') and ev(page, 'Game._trans.to') == 'CONFIRM' and ev(page, 'Game.att.DRAW') == a0 + 1, (a0, ev(page, 'Game.att.DRAW')))
    peak = ev(page, "(async()=>{const c=new OfflineAudioContext(1,44100*2.5,44100);rattle(c,.05,RATTLE);const d=(await c.startRendering()).getChannelData(0);let m=0,l=0;for(let i=0;i<d.length;i++){const a=Math.abs(d[i]);if(a>m)m=a;if(a>.01)l=i}return [m,l/44100]})()")
    check('聲音聽得到、不破音、在跳頁前結束', .3 < peak[0] <= 1 and peak[1] < 2.3, peak)
    jump(page, 'DRAW'); btn().click(); page.wait_for_timeout(200); jump(page, 'HEAVEN'); page.wait_for_timeout(2500)
    check('播放中重開新局：不會亂跳', ev(page, 'Game.state') == 'HEAVEN' and not ev(page, 'Game.busy'))
    ev(page, "localStorage.setItem('hg.mute.taiwan-life','1')"); jump(page, 'DRAW'); btn().click(); page.wait_for_timeout(100)
    check('靜音時直接跳頁', ev(page, 'Game.state') == '_TRANS' and not ev(page, 'Game.busy'))
    ev(page, "localStorage.removeItem('hg.mute.taiwan-life')")
    # ── 插香：天公爐 → 大殿 → 側殿 ──
    jump(page, 'HEAVEN'); opt(page, '天公爐拜天公'); check('天公爐插一支', '把一支香插進天公爐' in ev(page, 'Game.thought[0].zh'))
    ev(page, 'Game.handleChoice(Game.transLabel()); Game.handleChoice(MAIN_RIGHT.slice())'); check('大殿插一支', any('把一支香插進大殿' in t for t in ev(page, 'Game.thought.map(t=>t.zh)')))
    ev(page, 'Game.handleChoice(Game.transLabel())'); check('進側殿', ev(page, 'Game.state') == 'SIDE')
    opt(page, '插上最後一支香。'); ev(page, 'Game.handleChoice(Game.transLabel())'); check('回大殿擲筊', ev(page, 'Game.state') == 'THROW' and ev(page, 'Game.phase') == 'ready')
    ctx.close(); b.close()
    check('沒有程式錯誤', not errs, errs[:3])
print(f'通過 {ok} 項，失敗 {fail} 項')
sys.exit(1 if fail else 0)
