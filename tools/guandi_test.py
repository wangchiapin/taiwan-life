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
    ev(page, f"""(()=>{{ {f"let n=0; do Game.setup(); while(Game.task.ask.length+'-'+Game.task.miss!=='{plan}' && ++n<2000);" if plan else 'Game.setup();'}
      Game.state='{state}'; Game.mistakes=0; Game.score=100; Game.thought=null; Game.feedback=[]; Game._trans=null; Game.render(); }})()""")

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
    jump(page, 'THROW', '2-0')
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
    page.wait_for_timeout(1200)
    check('第一次笑筊／陰筊時沒有任何按鈕', ev(page, 'Game.phase') == 'landed' and page.locator('#options-area .opt').count() == 0)
    check('Ami 說結果', 'Ami：是' in txt(page) and '再試一次' in txt(page), txt(page))
    check('可以直接再滑', '再往上滑一次' in txt(page))
    page.wait_for_timeout(500)
    check('落地後看得到 Ami 的話', ev(page, "document.querySelector('#npc-dialogue').getBoundingClientRect().bottom <= innerHeight + 1"))
    page.screenshot(path='/tmp/t_landed.png', full_page=True)
    page.locator('.toss.again').tap(); page.wait_for_timeout(200)
    check('落地後點一下不會丟', ev(page, 'Game.ti') == 1 and ev(page, 'Game.phase') == 'landed')
    swipe(page, -110); page.wait_for_timeout(1550)
    check('再滑一次得到聖筊、出現一顆按鈕', ev(page, 'Game.ti') == 2 and page.locator('#options-area .opt').count() == 1 and '關聖帝君說可以，去求籤吧' in txt(page))
    check('聖筊以後不能再丟', page.locator('.toss[role=button]').count() == 0)
    page.screenshot(path='/tmp/t_pass.png', full_page=True)
    page.locator('#options-area .opt').click(); page.wait_for_timeout(200)
    check('按鈕直接到抽籤（不跳過場）', ev(page, 'Game.state') == 'DRAW')
    ctx.close()
    # ── 電腦：點、拖、鍵盤 ──
    ctx, page = open_game(b, errs)
    for name in ('點一下', '往上拖', '鍵盤'):
        jump(page, 'THROW', '1-1'); el = page.locator('.toss.ready'); bb = el.bounding_box(); x, y = bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] * .7
        if name == '點一下': page.mouse.click(x, y)
        elif name == '往上拖': page.mouse.move(x, y); page.mouse.down(); page.mouse.move(x, y - 120, steps=6); page.mouse.up()
        else: el.focus(); page.keyboard.press('Enter')
        page.wait_for_timeout(1550); check('電腦' + name + '會丟', ev(page, 'Game.phase') == 'landed')
    jump(page, 'THROW', '2-0')
    for i in (1, 2):
        el = page.locator('.toss[role=button]'); bb = el.bounding_box(); page.mouse.click(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] * .5); page.wait_for_timeout(1550)
        check('電腦落地後再點一下會再丟', ev(page, 'Game.ti') == i)
    jump(page, 'THROW', '1-1'); bb = page.locator('.toss.ready').bounding_box(); x, y = bb['x'] + bb['width'] / 2, bb['y'] + 40
    page.mouse.move(x, y); page.mouse.down(); page.mouse.move(x, y + 80, steps=4); page.mouse.up(); page.wait_for_timeout(200)
    check('電腦往下拖不會丟', ev(page, 'Game.phase') == 'ready')
    # ── 七種劇本（抽籤前丟幾次-第一支籤第幾丟沒過）：次數、重抽、Ami 的話、按鈕 ──
    page.emulate_media(reduced_motion='reduce')
    for plan, want in (('1-0', 4), ('1-1', 5), ('1-2', 6), ('1-3', 7), ('2-0', 5), ('2-1', 6), ('2-2', 7)):
        for run in range(3):
            jump(page, 'THROW', plan); ev(page, "Game.mistakes=0; Game.score=100")
            throws, non, sticks, steps = 0, 0, [], 0
            while ev(page, 'Game.state') != 'SLIP_NUM' and steps < 60:
                steps += 1; st = ev(page, 'Game.state')
                if st == '_TRANS': ev(page, 'Game.handleChoice(Game.transLabel())'); continue
                if st == 'DRAW':
                    again = len(sticks) > 0
                    check('抽籤頁 Ami 的話', ('我們再求一支籤吧！' if again else '你來求一支籤吧！') in txt(page) and '籤筒裡有很多' not in txt(page), txt(page))
                    check('抽籤只有一個按鈕', page.locator('#options-area .opt').count() == 1 and txt(page, '#options-area') == '輕搖籤筒，等一支籤掉出來。')
                    m = ev(page, 'Game.mistakes'); sticks.append(ev(page, 'Game.drawnSlip().n')); opt(page, '輕搖籤筒，等一支籤掉出來。'); page.wait_for_function('()=>!Game.busy')
                    n = ev(page, 'slipNo(Game.drawnSlip().n)')
                    check('抽籤過場的旁白、按鈕、圖', f'一支籤掉出來了。籤支上寫著「{n}」。' in txt(page) and '桌上' not in txt(page) and txt(page, '#options-area') == '問問關聖帝君是不是這支籤'
                          and ev(page, "document.querySelector('#npc-avatar').getAttribute('src')") == 'images/draw_done.jpg' and ev(page, 'Game.mistakes') == m, txt(page))
                    continue
                if ev(page, 'Game.phase') == 'ready':
                    n = ev(page, 'slipNo(Game.drawnSlip().n)')
                    mine = '請問關聖帝君，可以給我一支籤嗎？' if st == 'THROW' else f'請問是{n}嗎？'
                    t_ = txt(page)
                    ask = '要先問問關聖帝君可不可以給你一支籤唷！'
                    check('丟之前的台詞', mine in t_ and (t_.index(ask) < t_.index(mine) if st == 'THROW' else 'Ami' not in t_) and page.locator('#options-area .opt').count() == 0, t_)
                page.locator('.toss[role=button]').focus(); page.keyboard.press('Enter'); page.wait_for_timeout(230); throws += 1
                k = ev(page, 'Game.last'); non += k != 'sheng'
                faces = ev(page, "[...document.querySelectorAll('.toss.landed .bei')].map(e=>e.classList.contains('flat')?'flat':'round')")
                check('畫面的筊杯和結果一致', faces == ev(page, f"RES['{k}'].cups"), (k, faces))
                t_, streak, go = txt(page), ev(page, 'Game.streak'), ev(page, 'Game.goNext')
                zh = ev(page, f"RES['{k}'].zh")
                if st == 'THROW': say = {'sheng': '是聖筊！關聖帝君說可以，去求籤吧！', 'xiao': '是笑筊，關聖帝君笑笑的沒有回答，再試一次看看吧！', 'yin': '是陰筊，關聖帝君說不行，再試一次看看吧！'}[k]
                elif k == 'xiao': say = '是笑筊，可能不是這支，再求一支看看吧！'
                elif k == 'yin': say = '是陰筊，關聖帝君說不是這支，再求一支看看吧！'
                else: say = '三個聖筊！關聖帝君說就是這支籤！' if streak == 3 else '是聖筊！很好，再丟一次！'
                check('Ami 說的結果正確', 'Ami：' + say in t_, (st, k, streak, t_))
                if st == 'CONFIRM': check('連續聖筊計數', f'：{streak} / 3' in t_, t_)
                btns = page.locator('#options-area .opt').count()
                check('只有要換下一步時才有一顆按鈕', btns == (1 if go else 0), (btns, go))
                if go:
                    label = txt(page, '#options-area')
                    want_label = '走到籤櫃' if go == 'SLIP_NUM' else ('走到籤筒前' if st == 'THROW' else '回去重新求籤')
                    check('按鈕文字', label == want_label, label)
                    page.locator('#options-area .opt').click(); page.wait_for_timeout(60)
                    check('按鈕直接到下一步', ev(page, 'Game.state') == go, ev(page, 'Game.state'))
            check(f'{plan} 丟 {want} 次', throws == want, throws)
            ask_n, miss = map(int, plan.split('-'))
            check(f'{plan} 笑筊／陰筊次數', non == (ask_n - 1) + (miss > 0), non)
            check(f'{plan} 抽籤次數', len(sticks) == (2 if miss else 1), sticks)
            check(f'{plan} 重抽是不同的籤', len(set(sticks)) == len(sticks), sticks)
            check(f'{plan} 最後的籤和籤櫃一致', sticks and sticks[-1] == ev(page, 'Game.task.slip.n'))
    page.emulate_media(reduced_motion='no-preference')
    dist = ev(page, "(()=>{const c={},n={};let max=0;for(let i=0;i<40000;i++){Game.setup();const t=Game.task,k=t.ask.length+'-'+t.miss;c[k]=(c[k]||0)+1;const total=t.ask.length+(t.miss?t.miss+3:3);n[total]=(n[total]||0)+1;max=Math.max(max,total)}return {c,n,max}})()")
    want = {'1-0': .21, '1-1': .175, '1-2': .175, '1-3': .14, '2-0': .12, '2-1': .09, '2-2': .09}
    check('劇本比例', sorted(dist['c']) == sorted(want) and all(abs(dist['c'][k] / 40000 - v) < .012 for k, v in want.items()), dist)
    check('總次數 4～7 次的比例，最多 7 次', dist['max'] == 7 and all(abs(dist['n'][str(k)] / 40000 - v) < .012 for k, v in ((4, .21), (5, .295), (6, .265), (7, .23))), dist)
    # ── 丟到一半重畫、離開關卡 ──
    jump(page, 'THROW', '2-0'); ev(page, 'Game.toss(); Game.toss(); Game.render()'); page.wait_for_timeout(1550)
    check('連按只丟一次', ev(page, 'Game.phase') == 'landed' and ev(page, 'Game.ti') == 1)
    # ── 擲筊落地聲：五聲、有聲才播、靜音照樣丟 ──
    snd = ev(page, """(async()=>{const c=new OfflineAudioContext(1,44100,44100);beiSound(c,.05,BEI);const d=(await c.startRendering()).getChannelData(0);
      const W=441,e=[];for(let i=0;i+W<=d.length;i+=W){let m=0;for(let j=i;j<i+W;j++)m=Math.max(m,Math.abs(d[j]));e.push(m)}
      const peaks=BEI.at.map(a=>{const k=Math.round((a+.05)*100);const near=Math.max(...e.slice(k,k+4));const before=k>6?Math.min(...e.slice(k-4,k)):0;return [near,before]});
      let m=0,l=0;for(let i=0;i<d.length;i++){const a=Math.abs(d[i]);if(a>m)m=a;if(a>.01)l=i}return {peaks,m,l:l/44100}})()""")
    check('落地聲有五聲，聲音之間分得開', len(snd['peaks']) == 5 and all(a > .08 and a > b * 2.5 for a, b in snd['peaks']), snd)
    check('落地聲不破音、長度合理', .4 < snd['m'] <= 1 and .5 < snd['l'] < .75, snd)
    ev(page, "(()=>{window.__bei=0; const old=beiSound; beiSound=(...a)=>{window.__bei++; old(...a)}; return 1})()")
    for muted in (False, True):
        ev(page, f"localStorage.setItem('hg.mute.taiwan-life','{int(muted)}'); window.__bei=0")
        jump(page, 'THROW', '2-0'); ev(page, 'Game.toss()'); page.wait_for_timeout(1000)
        check('落地前還在飛', ev(page, 'Game.phase') == 'fly'); page.wait_for_timeout(500)
        check(('靜音：不播，照樣落地' if muted else '有聲：丟一次播一次'), ev(page, 'window.__bei') == (0 if muted else 1) and ev(page, 'Game.phase') == 'landed', ev(page, 'window.__bei'))
    ev(page, "localStorage.removeItem('hg.mute.taiwan-life')")
    # ── 籤筒聲和搖晃動畫：點了才晃、播完才跳頁、靜音照樣晃 ──
    SHK = '輕搖籤筒，等一支籤掉出來。'
    btn = lambda: page.locator('#options-area .opt').first
    snap = "document.querySelector('#shake-canvas').toDataURL()"
    for muted in (False, True):
        tag = '靜音' if muted else '有聲'
        ev(page, f"localStorage.setItem('hg.mute.taiwan-life','{int(muted)}')")
        jump(page, 'DRAW'); page.wait_for_function('()=>drawArt()'); page.wait_for_timeout(500)
        check(tag + '：點之前沒有動畫', page.locator('#shake-canvas').count() == 0)
        a0 = ev(page, 'Game.att.DRAW||0'); btn().click(); page.wait_for_timeout(250)
        check(tag + '：按下後開始、還沒跳頁', ev(page, 'Game.busy') and ev(page, 'Game.state') == 'DRAW' and page.locator('#shake-canvas').count() == 1)
        if not muted: check('有聲：聲音在播', ev(page, 'Game.sfx.state') == 'running')
        box = ev(page, "['#shake-canvas','#npc-avatar'].map(q=>{const r=document.querySelector(q).getBoundingClientRect();return [r.x,r.y,r.width,r.height].map(Math.round)})")
        check(tag + '：動畫蓋住場景圖', box[0] == box[1], box)
        f1 = ev(page, snap); page.wait_for_timeout(130); check(tag + '：畫面在動', f1 != ev(page, snap))
        page.screenshot(path=f'/tmp/t_shake_{int(muted)}.png')
        check(tag + '：播放中按鈕不能按', ev(page, "[...document.querySelectorAll('#options-area .opt')].every(b=>b.disabled)"))
        ev(page, "Game.handleChoice(" + repr(SHK) + ")")
        page.wait_for_timeout(1200); check(tag + '：約 1.6 秒時還在播', ev(page, 'Game.state') == 'DRAW' and page.locator('#shake-canvas').count() == 1)
        page.wait_for_timeout(1100); check(tag + '：播完跳過場、畫布拿掉', ev(page, 'Game.state') == '_TRANS' and not ev(page, 'Game.busy') and ev(page, 'Game._trans.to') == 'CONFIRM' and ev(page, 'Game.att.DRAW') == a0 + 1 and page.locator('#shake-canvas').count() == 0)
    ev(page, "localStorage.removeItem('hg.mute.taiwan-life')")
    peak = ev(page, "(async()=>{const c=new OfflineAudioContext(1,44100*2.5,44100);rattle(c,.05,RATTLE);const d=(await c.startRendering()).getChannelData(0);let m=0,l=0;for(let i=0;i<d.length;i++){const a=Math.abs(d[i]);if(a>m)m=a;if(a>.01)l=i}return [m,l/44100]})()")
    check('聲音聽得到、不破音、在跳頁前結束', .3 < peak[0] <= 1 and peak[1] < 2.3, peak)
    jump(page, 'DRAW'); btn().click(); page.wait_for_timeout(200); jump(page, 'HEAVEN'); page.wait_for_timeout(2500)
    check('播放中重開新局：不會亂跳', ev(page, 'Game.state') == 'HEAVEN' and not ev(page, 'Game.busy') and page.locator('#shake-canvas').count() == 0)
    page.emulate_media(reduced_motion='reduce'); jump(page, 'DRAW'); btn().click(); page.wait_for_timeout(200)
    check('減少動態：不晃，等聲音播完', ev(page, 'Game.busy') and page.locator('#shake-canvas').count() == 0)
    page.wait_for_function('()=>!Game.busy')
    ev(page, "localStorage.setItem('hg.mute.taiwan-life','1')"); jump(page, 'DRAW'); btn().click(); page.wait_for_timeout(100)
    check('減少動態又靜音：直接跳頁', ev(page, 'Game.state') == '_TRANS' and not ev(page, 'Game.busy'))
    ev(page, "localStorage.removeItem('hg.mute.taiwan-life')"); page.emulate_media(reduced_motion='no-preference')
    # ── 插香：天公爐 → 大殿 → 側殿 ──
    jump(page, 'HEAVEN'); opt(page, '天公爐拜天公'); check('天公爐插一支', '把一支香插進天公爐' in ev(page, 'Game.thought[0].zh'))
    ev(page, 'Game.handleChoice(Game.transLabel()); Game.handleChoice(MAIN_RIGHT.slice())'); check('大殿插一支', any('把一支香插進大殿' in t for t in ev(page, 'Game.thought.map(t=>t.zh)')))
    ev(page, 'Game.handleChoice(Game.transLabel())'); check('進側殿', ev(page, 'Game.state') == 'SIDE')
    check('側殿一頁看完', '（你走到側殿，向其他神明拜了三下，插上最後一支香，雙手合十再拜一次。）' in txt(page) and 'Ami：你知道這些是哪些神明嗎？我們去跟關聖帝君求個籤吧！' in txt(page) and txt(page, '#options-area') == '去求籤', txt(page))
    opt(page, '去求籤'); check('回大殿擲筊', ev(page, 'Game.state') == 'THROW' and ev(page, 'Game.phase') == 'ready')
    ctx.close()
    # ── 籤支方框拿掉、籤櫃、側殿、解籤、聽懂題、登記單 ──
    ctx, page = open_game(b, errs)
    opts = lambda: ev(page, "[...document.querySelectorAll('#options-area .opt')].map(b=>b.dataset.raw||(c=>{c.querySelectorAll('rt').forEach(r=>r.remove());return c.textContent})(b.cloneNode(true)))")
    pick_ = lambda c: ev(page, f"Game.handleChoice({c!r})")
    src = lambda: ev(page, "document.querySelector('#npc-avatar').getAttribute('src')")
    st = lambda: ev(page, 'Game.state')
    m = lambda: ev(page, 'Game.mistakes')
    go = lambda: pick_(ev(page, 'Game.transLabel()'))
    # 登記處道歉用尷尬圖：唸錯、算錯錢、找錯錢才換，沒錯就用原圖
    SORRY, DESK = 'images/desk_sorry.jpg', 'images/desk.jpg'
    for state, flag in (('REGISTER', 'regWrong'), ('PAY', 'payWrong'), ('CHANGE', 'changeWrong')):
        for wrong in (True, False):
            jump(page, state); ev(page, f"Game.task.{flag}={str(wrong).lower()}; Game.render()")
            check(f'{state} 抓錯前用原圖', src() == DESK, src())
            ans = ev(page, f"({smoke.ORACLES['guandi']})()")
            pick_(ans); page.wait_for_timeout(300)
            check(f'{state} {"說錯：道歉用尷尬圖" if wrong else "沒說錯：不用尷尬圖"}', (src() == SORRY if wrong else src() != SORRY) and page.locator('#npc-avatar').is_visible(), (src(), st()))
            if state == 'PAY' and wrong:
                if st() == '_TRANS': go()
                check('重算那一關也是尷尬圖', st() == 'PAY_FIX' and src() == SORRY, (st(), src()))
                pick_(ev(page, f"({smoke.ORACLES['guandi']})()")); check('付完錢換回原圖', src() == DESK, src())
    for state in ('ASK', 'MEAN'):
        jump(page, state); check(state + ' 用解籤圖', src() == 'images/explain.jpg' and page.locator('#npc-avatar').is_visible(), src())
    jump(page, 'SIDE'); check('側殿只有一個按鈕', opts() == ['去求籤'], opts())
    for state in ev(page, 'Object.keys(STAGE)'):
        jump(page, state); ev(page, 'Hints.toggle(true)'); h = txt(page, '#hint-body')
        if 'Ami 說的話' in h or '今天我帶你去關帝廟' in h or '今天的事' not in h: check('任務提示沒有 Ami 的話：' + state, False, h)
        ev(page, 'Hints.toggle(false)')
    check('每一關的任務提示都檢查過', True)
    jump(page, 'MAIN'); check('遊戲裡的確定只有中文', ev(page, "(()=>{const c=document.querySelector('#options-area .opt:last-child').cloneNode(true);c.querySelectorAll('rt').forEach(r=>r.remove());return c.textContent.trim()})()") == '確定')
    for state in ('CONFIRM', 'SLIP_NUM'):
        jump(page, state); check(state + ' 沒有籤支方框', '你抽到的籤支' not in txt(page))
    for wrong in (True, False):
        jump(page, 'SLIP_NUM'); ev(page, f"Game.task.numWrong={str(wrong).lower()}; Game.render()")
        o = opts(); n, claim, mine = ev(page, '[Game.task.numSaid, Game.task.numClaim, Game.task.slip.n]')
        fix = ev(page, f"`不好意思，我抽到的是${{slipNo({mine if wrong else claim})}}。`")
        check(f'籤櫃選項（廟公{"拿錯" if wrong else "拿對"}）', fix in o and '廟公，你的眼睛是不是不太好？' in o and (wrong or claim != mine), o)
        if wrong:
            pick_(fix); page.wait_for_timeout(300)
            check('廟公道歉用尷尬圖', st() == '_TRANS' and src() == 'images/cabinet_sorry.jpg' and page.locator('#npc-avatar').is_visible(), src())
            go(); check('下一關換回原圖', st() == 'READ' and src() == 'images/read.jpg', src())
        else:
            pick_('對，是這張，謝謝。'); check('拿對時不用尷尬圖', src() != 'images/cabinet_sorry.jpg', src())
    # 看籤詩：選項照籤的等級；Ami 只說等級
    good = '謝謝關公。我會好好努力。'
    lines = {'上上': '，你很幸運欸！', '上吉': '，運氣很不錯喔！', '中吉': '，還不錯唷！', '中平': '，普普通通，慢慢來就好。', '下下': '……沒關係，最近小心一點就好。'}
    missing = ev(page, "(()=>{const out=[];for(const s of SLIPS){Game.task.slip=s;const g=GRADES[s.g],z=g.zh+g.ami[0];for(const [w] of g.words)if(!z.includes(w))out.push(w)}return out})()")
    check('看籤詩新單字都在台詞裡', missing == [], missing)
    for n in ev(page, 'SLIPS.map(s=>s.n)'):
        jump(page, 'READ'); ev(page, f"Game.task.slip=SLIPS.find(s=>s.n==={n}); Game.render()")
        g, gloss = ev(page, '[Game.task.slip.g, Game.task.slip.gloss.zh]'); o = opts()
        third = '那我可以不用學中文了吧！' if g == '上上' else '再抽一次，抽到上上籤為止。'; rude = '到底在供三小？'
        if sorted(o) != sorted([good, '那我可以躺平了。', third, rude]) or gloss in txt(page) or f'Ami：這是{g}籤{lines[g]}' not in txt(page): check(f'第{n}籤看籤詩', False, (o, txt(page)))
    check('20 支籤的看籤詩選項都檢查過', True)
    for g in ('上上', '下下'):
        jump(page, 'READ'); ev(page, f"Game.task.slip=SLIPS.find(s=>s.g==='{g}'); Game.render()")
        for c in opts():
            if c != good: k = m(); pick_(c); check('看籤詩錯的選項：' + c, st() == 'READ' and m() == k + 1)
    check('粗話的提醒', ev(page, "Game.log.some(x=>x.zh==='這句話很不禮貌，不要這樣說。')"))
    pick_(good); check('看籤詩過場', st() == '_TRANS' and 'Ami：María，請廟公幫你解籤吧！' in txt(page), txt(page))
    go(); check('到解籤', st() == 'ASK' and sorted(opts()) == sorted(['廟公，可以請你幫我解籤嗎？', '欸，老頭，這什麼意思？', '（把籤紙揉爛丟掉）']), opts())
    for c in opts():
        if not c.startswith('廟公'): k = m(); pick_(c); check('解籤錯的選項：' + c, st() == 'ASK' and m() == k + 1)
    pick_('廟公，可以請你幫我解籤嗎？')
    if st() == '_TRANS': go()
    check('到聽懂題', st() == 'MEAN' and 'Ami：María，你覺得廟公的意思是什麼？' in txt(page) and ev(page, 'Game.task.slip.gloss.zh') in txt(page) and len(opts()) == 3, txt(page))
    bad = ev(page, """(()=>{const out=[];for(const s of SLIPS){if(!s.say||!s.tags)out.push([s.n,'缺']);for(let i=0;i<60;i++){const w=otherSlips(s);
      if(new Set([s,...w]).size!==3||w.some(x=>x.tags.some(g=>s.tags.includes(g)))||w[0].tags.some(g=>w[1].tags.includes(g)))out.push([s.n,w.map(x=>x.n)])}}
      if(new Set(SLIPS.map(s=>s.say)).size!==SLIPS.length)out.push('重複');return out})()""")
    check('聽懂題的錯選項和正解意思不重疊', bad == [], bad[:5])
    right = ev(page, 'Game.task.slip.say')
    for c in opts():
        if c != right: k = m(); pick_(c); check('聽懂題錯的選項', st() == 'MEAN' and m() == k + 1)
    pick_(right); check('聽懂題過場', st() == '_TRANS' and 'Ami：走吧，我們去點光明燈。' in txt(page) and txt(page, '#options-area') == '走到登記處', txt(page))
    go(); check('到填登記單', st() == 'FILL' and 'Ami：你自己填填看登記單吧！應該可以看得懂吧？' in txt(page) and '光明燈1年500元' in txt(page), txt(page))
    tap = lambda k, v: page.locator(f'.pick[data-k="{k}"][data-v="{v}"]').click()
    head = lambda r: page.locator(f'.grp[data-row="{r}"] .head').click()
    opened = lambda: ev(page, "[...document.querySelectorAll('.fill .grp')].filter(g=>g.querySelector('.body')).map(g=>g.dataset.row)")
    check('登記單四行、先開姓名', page.locator('.fill .grp').count() == 4 and opened() == ['name'], opened())
    check('名字三選一、含自己', page.locator('.pick[data-k="name"]').count() == 3 and page.locator('.pick[data-k="name"][data-v="María"]').count() == 1)
    check('一開始什麼都沒選', page.locator('.pick.on').count() == 0)
    head('name'); check('再點一次收起來', opened() == [])
    head('addr'); check('一次只開一行', opened() == ['addr']); head('term'); check('換開另一行', opened() == ['term'])
    k = m(); pick_('填好了'); check('沒填完不扣分、打開第一個沒填的', st() == 'FILL' and m() == k and '登記單還沒填完' in txt(page) and opened() == ['name'])
    other = ev(page, 'Game.task.names.find(n=>n!==Game.N)'); tap('name', other); check('選完名字自動開生日', opened() == ['birth'] and page.locator('.pick[data-k="m"]').count() == 12 and page.locator('.pick[data-k="d"]').count() == 0)
    tap('m', 1); check('選月後換成日期', page.locator('.pick[data-k="m"]').count() == 0 and page.locator('.pick[data-k="d"]').count() == 31 and '請選日期' in txt(page, '.grp[data-row="birth"] .head'))
    head('birth'); head('birth'); check('收起再打開仍是選日期', page.locator('.pick[data-k="d"]').count() == 31)
    page.locator('.pick.back').click(); check('可以換月份', page.locator('.pick[data-k="m"]').count() == 12)
    tap('m', 2); check('二月 29 天', page.locator('.pick[data-k="d"]').count() == 29)
    page.locator('.pick.back').click(); tap('m', 4); check('四月 30 天', page.locator('.pick[data-k="d"]').count() == 30)
    tap('d', 21); check('選完日期自動開住址', opened() == ['addr'] and '4月21號' in txt(page, '.grp[data-row="birth"] .head'))
    tap('addr', 2); check('選完住址開期限', opened() == ['term']); tap('term', '半年'); check('全部選完都收起來', opened() == [] and txt(page, '.fill').count('✓') == 4)
    head('birth'); page.locator('.pick.back').click(); tap('m', 1); tap('d', 31); page.locator('.grp[data-row="birth"] .head').click(); page.locator('.pick.back').click(); tap('m', 2)
    check('換成較短的月份：清掉超過的日期', ev(page, 'Game.task.form.d') is None and '請選日期' in txt(page, '.grp[data-row="birth"] .head'))
    page.locator('.pick.back').click(); tap('m', 4); tap('d', 21); check('改完沒有未填的就收起來', opened() == [])
    page.screenshot(path='/tmp/t_fill.png', full_page=True)
    k = m(); pick_('填好了'); check('名字、期限填錯只扣一次', st() == 'FILL' and m() == k + 1)
    check('扣分後已選的還在、打開填錯的那行', txt(page, '.fill').count('✓') == 3 and opened() == ['name'] and page.locator('.pick.on').count() == 1, (opened(), txt(page, '.fill')))
    check('錯誤說明兩項', '姓名要寫自己的名字。' in ev(page, 'Game.log.at(-1).zh') and '期限要選一年' in ev(page, 'Game.log.at(-1).zh'))
    tap('name', 'María'); head('term'); tap('term', '一年'); pick_('填好了'); card = txt(page)
    check('填對直接到登記、沒有過場和稱讚卡', st() == 'REGISTER' and '（你把登記單交給廟公。）' in card and '登記單填好了' not in card, (st(), card))
    check('登記單顯示剛才填的', st() == 'REGISTER' and all(x in txt(page, '#npc-dialogue .card') for x in ('María', '4月21號', '台南市成功路25號', '1年', '500元')) and all(x in card for x in ('生日是四月二十一號', '住在台南市成功路二十五號', '點一年')), card)
    # 複誦：名字、生日（差一天／差一個月）、住址（整個換掉／只錯門牌）；說對時「不好意思」要說別的內容
    kinds = [('name', ''), ('birth', 'day'), ('birth', 'month'), ('addr', 'whole'), ('addr', 'number')]
    for kind, sub in kinds:
        for wrong in (True, False):
            for mm, d, ai, step in ((4, 1, 3, 1), (4, 30, 0, -1), (3, 31, 1, 1), (1, 31, 2, -1), (12, 15, 1, 1)):
                jump(page, 'REGISTER'); ev(page, f"Object.assign(Game.task,{{form:{{name:Game.N,m:{mm},d:{d},addr:{ai},term:'一年'}},regWrong:{str(wrong).lower()},regKind:'{kind}',regBirth:'{sub}',regAddr:'{sub}',regStep:{step}}}); Game.render()")
                said = txt(page); said = said[said.index('光明燈登記：'):]; said = said[:said.index('對嗎')]
                mine = ['María', ev(page, f'birthZh({mm},{d})'), ev(page, f'ADDR[{ai}][0]'), '一年']
                miss = [i for i, x in enumerate(mine) if f'{x}' not in said]
                idx = ('name', 'birth', 'addr').index(kind); tag = f'{kind} {sub} {mm}/{d} {"錯" if wrong else "對"}'
                check('複誦只錯該錯的那一項：' + tag, miss == ([idx] if wrong else []), (said, miss))
                if wrong and sub in ('day', 'month'):
                    sm, sd = ev(page, f"(()=>{{for(let m=1;m<=12;m++)for(let d=1;d<=daysIn(m);d++)if({said!r}.includes('是'+birthZh(m,d)+'，'))return [m,d]}})()")
                    no_month = sub == 'month' and (mm, d) in ((3, 31), (1, 31))
                    want_ok = (abs(sm - mm) == 1 and sd == d) if sub == 'month' and not no_month else (sm == mm and abs(sd - d) == 1)
                    check('生日差一天或差一個月：' + tag, want_ok, (sm, sd))
                if wrong and sub == 'number': check('只錯門牌：' + tag, mine[2].split('路')[0] + '路' in said, said)
                o = opts(); check('複誦三個選項：' + tag, len(o) == 3 and '對，沒錯。' in o and '你到底有沒有在看我寫的啊？' in o, o)
                fix = [x for x in o if x.startswith('不好意思')][0]
                if wrong: check('更正選項說正確內容：' + tag, mine[idx] in fix, fix)
                else: check('說對時更正選項是別的內容：' + tag, mine[idx] + '。' not in fix, (fix, mine[idx]))
                ans = fix if wrong else '對，沒錯。'
                for c in o:
                    if c != ans: k = m(); pick_(c); check('複誦錯的選項：' + c, st() == 'REGISTER' and m() == k + 1)
                pick_(ans); check('複誦答對往付錢：' + tag, ev(page, 'Game._trans?Game._trans.to:Game.state') == 'PAY', st())
                t_ = txt(page)
                if wrong: one = t_.count('廟公：') == 1 and '廟公：啊，不好意思！我改過來。好，「María」，' in t_ and '，一年。沒問題！這樣要先跟你收費。' in t_ and all(x in t_ for x in mine[1:3])
                else: one = t_.count('廟公：') == 1 and '廟公：沒問題！這樣要先跟你收費。' in t_
                check('複誦過場廟公只有一句：' + tag, st() == '_TRANS' and one and txt(page, '#options-area') == '付錢', t_)
    d = ev(page, "(()=>{const c={};for(let i=0;i<3000;i++){Game.setup();const t=Game.task;c[t.regKind]=1;c[t.regBirth]=1;c[t.regAddr]=1;c['p'+t.said]=1}return Object.keys(c).sort()})()")
    check('每局會抽到的種類（沒有期限）', d == sorted(['name', 'birth', 'addr', 'day', 'month', 'whole', 'number', 'p300', 'p500', 'p1000']), d)
    # 付錢：三種燈、三個選項
    for said in (500, 300, 1000):
        jump(page, 'PAY'); ev(page, f"Object.assign(Game.task,{{payWrong:{str(said != 500).lower()},said:{said},other:LAMPS.find(x=>x.price==={said if said != 500 else 300})}}); Game.render()")
        t_ = txt(page, '#game-window')
        check(f'價目牌三種燈（{said}）', all(x in t_ for x in ('光明燈（一年）500元', '文昌燈（一年）300元', '財神燈（一年）1000元')) and '金紙' not in t_ and '蠟燭' not in t_, t_)
        o = opts(); fix = [x for x in o if x.startswith('不好意思')][0]
        check(f'付錢三個選項（{said}）', len(o) == 3 and '好，這裡是一千元。' in o and '可以算便宜一點嗎？' in o and (('五百元' in fix) == (said != 500)), o)
        ans = fix if said != 500 else '好，這裡是一千元。'
        for c in o:
            if c != ans: k = m(); pick_(c); check(f'付錢錯的選項（{said}）：' + c, st() == 'PAY' and m() == k + 1)
        pick_('可以算便宜一點嗎？'); check('講價的說明', '不能講價' in ev(page, 'Game.log.at(-1).zh'))
        pick_(ans); check(f'付錢答對（{said}）', ev(page, 'Game._trans?Game._trans.to:Game.state') == ('PAY_FIX' if said != 500 else 'CHANGE'), st())
    for wrong in (True, False):
        jump(page, 'CHANGE'); ev(page, f"Game.task.changeWrong={str(wrong).lower()}; Game.render()"); pick_(ev(page, f"({smoke.ORACLES['guandi']})()"))
        check('找錢過場', st() == '_TRANS' and 'Ami：María，我們去領一個平安符吧！' in txt(page) and txt(page, '#options-area') == '去領平安符', txt(page))
    jump(page, 'AMULET'); check('平安符 Ami 的話', 'Ami：哇！這些平安符好漂亮喔！' in txt(page), txt(page))
    ok_amulet = '（拿一個平安符，隨喜投一點香油錢）'
    check('平安符三個選項', sorted(opts()) == sorted([ok_amulet, '（拿走全部的平安符）', '這些平安符好醜喔！我不要拿！']), opts())
    for c in opts():
        if c != ok_amulet: k = m(); pick_(c); check('平安符錯的選項：' + c, st() == 'AMULET' and m() == k + 1)
    check('嫌醜的提醒', '很不禮貌' in ev(page, "Game.log.map(x=>x.zh).join()"))
    pick_(ok_amulet); check('拿到平安符的過場', st() == '_TRANS' and '（你拿了一個平安符。）' in txt(page) and '過爐' not in txt(page) and txt(page, '#options-area') == '繼續', txt(page))
    go(); check('Ami 問平安符', st() == 'CHARM' and 'Ami：María，你知道拿到平安符之後還要做什麼嗎？' in txt(page) and sorted(opts()) == sorted(['掛在樹上', '燒掉', '過香爐']) and src() == 'images/amulet.jpg', txt(page))
    ev(page, 'Hints.toggle(true)'); check('回答前任務提示沒有過爐告示', '順時針' not in txt(page, '#hint-body')); ev(page, 'Hints.toggle(false)')
    for c, why in (('掛在樹上', '平安符要帶在身上，才可以保佑平安啦！'), ('燒掉', '關聖帝君剛剛給你的平安符，怎麼可以馬上就燒掉？')):
        k = m(); pick_(c); check('平安符問題錯的選項：' + c, st() == 'CHARM' and m() == k + 1 and why in txt(page, '#npc-dialogue .fb.bad'), txt(page))
    pick_('過香爐'); check('答對：稱讚、走回天公爐（錯過再答對也有稱讚）', st() == '_TRANS' and '很棒喔！你很清楚台灣的拜拜文化呢！' in txt(page, '#npc-dialogue .fb.good') and '（你走回前面的天公爐。）' in txt(page) and txt(page, '#options-area') == '走到香爐前', txt(page))
    go(); check('過爐 Ami 的話', st() == 'GUOLU' and 'Ami：你做一次，我看看你會不會。' in txt(page), txt(page))
    # 第三個聖筊換笑臉圖
    page.emulate_media(reduced_motion='reduce'); jump(page, 'CONFIRM', '2-0'); seen = []
    for i in range(3):
        page.locator('.toss[role=button]').focus(); page.keyboard.press('Enter'); page.wait_for_timeout(260); seen.append(src())
        if i == 2: page.wait_for_timeout(300); page.screenshot(path='/tmp/t_happy.png', full_page=True)
    check('只有第三個聖筊換笑臉圖', seen == ['images/throw.jpg', 'images/throw.jpg', 'images/throw_happy.jpg'] and page.locator('#npc-avatar').is_visible(), seen)
    pick_('走到籤櫃'); check('離開後換回別的圖', st() == 'SLIP_NUM' and src() == 'images/cabinet.jpg', src())
    page.emulate_media(reduced_motion='no-preference')
    for state in ('REGISTER', 'PAY', 'MEAN', 'AMULET'):
        jump(page, state); ev(page, "if(!Game.showPinyin)Game.togglePinyin()"); page.wait_for_timeout(300); page.screenshot(path=f'/tmp/t_{state}_py.png', full_page=True); ev(page, "Game.togglePinyin()")
    check('生日、住址只用在這一局', ev(page, "(()=>{Game.setup();return Object.keys(Game.task.form).length===0 && !JSON.stringify(localStorage).includes('成功路')})()"))
    ctx.close()
    # ── 手機：登記單排得下 ──
    ctx, page = open_game(b, errs, mobile=True)
    jump(page, 'FILL')
    page.screenshot(path='/tmp/t_fill_m.png', full_page=True)
    for row, extra in (('name', ''), ('birth', ''), ('birth', 'Game.task.form.m=1;'), ('addr', ''), ('term', '')):
        ev(page, f"Game.task.form={{}}; {extra} Game.task.fillOpen='{row}'; Game.render()")
        check('手機登記單不超出畫面：' + row + extra, ev(page, 'document.documentElement.scrollWidth <= innerWidth + 1') and ev(page, "[...document.querySelectorAll('.fill button')].every(e=>{const r=e.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&e.scrollWidth<=e.clientWidth+1})"))
        h = ev(page, "document.querySelector('.fill').offsetHeight"); check('手機登記單高度不超過七成畫面：' + row + extra, h < 844 * .7, h)
        if extra: page.screenshot(path='/tmp/t_fill_days_m.png', full_page=True)
    for state in ('ASK', 'MEAN', 'READ', 'SIDE', 'REGISTER', 'PAY', 'AMULET', 'CHARM', 'GUOLU'):
        jump(page, state); page.screenshot(path=f'/tmp/t_{state}_m.png', full_page=True)
        check('手機不超出畫面：' + state, ev(page, 'document.documentElement.scrollWidth <= innerWidth + 1'))
    for py in (False, True):
        jump(page, 'PAY'); ev(page, f"if(Game.showPinyin!=={str(py).lower()})Game.togglePinyin()"); page.screenshot(path=f'/tmp/t_price_m_{int(py)}.png', full_page=True)
        w = ev(page, "[document.querySelector('.card.price').offsetWidth, document.querySelector('#npc-dialogue').clientWidth]")
        check('手機價目牌排得下', w[0] <= w[1] and ev(page, 'document.documentElement.scrollWidth <= innerWidth + 1'), w)
    ctx.close(); b.close()
    check('沒有程式錯誤', not errs, errs[:3])
print(f'通過 {ok} 項，失敗 {fail} 項')
sys.exit(1 if fail else 0)
