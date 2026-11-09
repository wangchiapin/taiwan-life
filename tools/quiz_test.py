#!/usr/bin/env python3
"""單字小考的測試：python3 tools/quiz_test.py [遊戲代號 …]（不指定＝所有有開 vocabQuiz 的遊戲）
每個遊戲：玩到結果頁（故意錯一次）→ 邀請卡片在 → 按「挑戰自己」→ 8 題都答一遍（答對答錯都有）
  檢查：題數、每題 4 個不同選項且正解剛好 1 個、沒抽到不算單字的詞（句型、含你我他、粗話）、答錯過的關卡的單字排在前面、
        答完看得到成績和單字卡圖片、能下載、能去排行榜；中途「先不要」也能去排行榜；
        西文／英文／只有中文三種說明語言、繁體／簡體都不出錯。
沒開 vocabQuiz 的遊戲：確認結果頁沒有邀請卡片。"""
import sys, re, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import smoke
from smoke import sync_playwright, route, PORT

def enabled():
    return [os.path.basename(os.path.dirname(f)) for f in sorted(glob.glob(ROOT + '/games/*/index.html')) if re.search(r'vocabQuiz\s*:\s*true', open(f, encoding='utf-8').read())]

def play_to_result(page, g, wrong_once=True):
    orc = smoke.EXTRA.get(g) or smoke.ORACLES.get(g)
    tried = False; bad = set()
    for _ in range(600):
        st = page.evaluate('Game.state')
        if st == 'RESULT': return True
        if page.locator('#ami-pop').count():   # Ami 的懸浮視窗會擋住按鈕：打開來看，再按「回覆：知道了」
            page.click('#ami-pop [data-act="open"]' if page.locator('#ami-pop [data-act="open"]').count() else '#ami-pop [data-act="reply"]'); continue
        if st == '_TRANS': smoke.click_i(page, 0); continue
        if g == 'breakfast' and page.evaluate("!!(Game.getConfig()[Game.state]||{}).pad"):
            page.evaluate("Game.pad.ticket=[...Game.C.target]; Game.padSubmit()"); continue
        page.evaluate("g=>{if(typeof Game.testPrep==='function')Game.testPrep(g)}", True)
        c = smoke.cands(page); opts = [x for x, _ in c]
        if not opts: page.wait_for_timeout(200); continue
        if page.evaluate('Game.mistakes') >= 8: page.evaluate('Game.mistakes=0')
        ans = page.evaluate(orc) if orc else None   # 沒有正解檔的遊戲：隨機點（答錯也沒關係，一定走得到結果頁）
        if not orc:
            import random
            cand = [i for i, o in enumerate(opts) if (st, o) not in bad] or list(range(len(opts)))
            idx = random.choice(cand); m0 = page.evaluate('Game.mistakes'); smoke.click_c(page, c, idx)
            if page.evaluate('Game.state') == st and page.evaluate('Game.mistakes') > m0: bad.add((st, opts[idx]))
            continue
        az = page.evaluate('a=>a&&Z(a)', ans)   # 簡體時畫面上的選項是簡體字
        idx = next((i for i, o in enumerate(opts) if o.strip() in (ans, az)), None)
        if idx is None: idx = next((i for i, o in enumerate(opts) if ans and (ans in o or az in o)), 0)
        if wrong_once and not tried and len(opts) > 1 and st not in ('START', 'END', 'RESULT'):
            tried = True; idx = (idx + 1) % len(opts)
        smoke.click_c(page, c, idx)
    return False

def check_game(p, g, lang='es', script='trad'):
    errs, fails = [], []
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 390, 'height': 844}); ctx.route('**/*', route)
    ctx.add_init_script("localStorage.setItem('hanziGames.settings', JSON.stringify({script:'%s',lang:'%s',phon:'pinyin',rate:'normal'}))" % (script, lang))
    page = ctx.new_page(); page.on('pageerror', lambda e: errs.append(str(e)))
    page.goto(f'http://127.0.0.1:{PORT}/games/{g}/index.html'); page.wait_for_timeout(500)
    page.fill('#player-name-input', 'AAA'); page.click('.btn-primary'); page.wait_for_timeout(800)
    if not play_to_result(page, g): fails.append('玩不到結果頁'); b.close(); return fails, errs
    page.wait_for_timeout(400)
    bad_states = page.evaluate('[...(Game._mistakeSt||[])]')
    if not page.locator('[data-quiz-go]').count(): fails.append('結果頁沒有邀請卡片'); b.close(); return fails, errs
    page.click('[data-quiz-go]'); page.wait_for_timeout(400)
    qs = page.evaluate('VocabQuiz.qs.map(q=>({zh:q.w[0],es:q.w[1],right:q.right,opts:q.opts}))')
    n = len(qs)
    if n < 4: fails.append(f'題數太少：{n}')
    if n > 8: fails.append(f'題數超過 8：{n}')
    zhs = [q['zh'] for q in qs]
    if len(set(zhs)) != n: fails.append('有重複的單字')
    for q in qs:
        if len(q['opts']) != 4 or len(set(q['opts'])) != 4: fails.append(f'選項不是 4 個不同的：{q}')
        if q['opts'].count(q['right']) != 1: fails.append(f'正解不是剛好 1 個：{q}')
        if re.search(r'[…、，。？！你我他妳]', q['zh']) or len(q['zh']) > 5: fails.append(f'抽到不算單字的詞：{q["zh"]}')
        if lang == 'en' and q['right'] == q['es'] and False: pass
    # 答錯過的關卡的單字要排前面
    if bad_states:
        bad_words = set(page.evaluate("s=>s.flatMap(k=>{try{return (VOCAB[k]||[]).filter(w=>VocabQuiz.isWord(w)).map(w=>w[0])}catch(e){return []}})", bad_states))
        cand_bad = list(bad_words)
        k = min(len(cand_bad), n)
        if k and not all(z in bad_words for z in zhs[:k]): fails.append(f'答錯過的關卡的單字沒排前面：{zhs} / 錯的關卡 {bad_states}')
    hits = 0
    for i in range(n):
        opts = page.evaluate("[...document.querySelectorAll('#quiz-screen [data-q]')].map(b=>b.dataset.choice)")
        right = page.evaluate('VocabQuiz.qs[VocabQuiz.i].right')
        pick = right if i % 2 == 0 else next(o for o in opts if o != right)   # 單數題答對、雙數題答錯
        page.click(f'#quiz-screen [data-choice="{pick}"]'); page.wait_for_timeout(120)
        ok_cls = page.evaluate("document.querySelectorAll('#quiz-screen .q-ok').length")
        bad_cls = page.evaluate("document.querySelectorAll('#quiz-screen .q-bad').length")
        if ok_cls != 1 or bad_cls != (0 if pick == right else 1): fails.append(f'第 {i+1} 題答完的顏色不對')
        if pick == right: hits += 1
        if i == 1 and n > 2:   # 中途「先不要」也能去排行榜（只測一次）
            pass
        page.click('[data-quiz-next]'); page.wait_for_timeout(120)
    shown = page.evaluate("document.querySelector('.q-score') && document.querySelector('.q-score').innerText")
    if not shown or str(hits) not in shown: fails.append(f'成績顯示不對：{shown}（答對 {hits}）')
    w = page.evaluate("new Promise(r=>{const i=document.querySelector('.q-img');if(!i)return r(0);const f=()=>r(i.naturalWidth);i.complete?f():i.onload=f})")
    if w < 800: fails.append('單字卡圖片沒產生')
    with page.expect_download() as d: page.click('[data-quiz-dl]')
    if not d.value.suggested_filename.endswith('.png'): fails.append('下載的不是 png')
    page.click('[data-quiz-lb]'); page.wait_for_timeout(1500)
    if not page.evaluate("document.getElementById('leaderboard-screen').classList.contains('active')"): fails.append('考完去不了排行榜')
    # 中途離開
    page.goto(f'http://127.0.0.1:{PORT}/games/{g}/index.html'); page.wait_for_timeout(400)
    page.fill('#player-name-input', 'AAA'); page.click('.btn-primary'); page.wait_for_timeout(800)
    play_to_result(page, g, wrong_once=False); page.wait_for_timeout(300)
    if not page.locator('[data-quiz-go]').count(): b.close(); return ['結果頁沒有邀請卡片（點不到）'], errs
    page.click('[data-quiz-go]'); page.wait_for_timeout(300)
    page.click('[data-quiz-skip]'); page.wait_for_timeout(1500)
    if not page.evaluate("document.getElementById('leaderboard-screen').classList.contains('active')"): fails.append('中途「先不要」去不了排行榜')
    b.close()
    return fails, errs

def check_embed(p, g):
    """地圖模式：進小考前就把成績交給地圖（只交一次）；考完／跳過去排行榜不會再交"""
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}); ctx.route('**/*', route)
    ctx.add_init_script("window.__m=[];addEventListener('message',e=>{if(e.data&&e.data.type)window.__m.push(e.data.type)})")
    page = ctx.new_page(); page.goto(f'http://127.0.0.1:{PORT}/games/{g}/index.html?embed=1&name=Ana'); page.wait_for_timeout(600)
    if page.locator('#intro-go').count(): page.click('#intro-go'); page.wait_for_timeout(300)   # 地圖模式的介紹視窗
    fails = []
    if not play_to_result(page, g, wrong_once=False): b.close(); return ['地圖模式玩不到結果頁']
    page.wait_for_timeout(300)
    if not page.locator('[data-quiz-go]').count(): b.close(); return ['地圖模式結果頁沒有邀請卡片']
    page.click('[data-quiz-go]'); page.wait_for_timeout(400)
    n1 = page.evaluate("__m.filter(t=>t==='scene-result').length")
    if n1 != 1: fails.append(f'進小考時 scene-result 應該送 1 次，實際 {n1}')
    page.click('[data-quiz-skip]'); page.wait_for_timeout(1200)
    n2 = page.evaluate("__m.filter(t=>t==='scene-result').length")
    if n2 != 1: fails.append(f'去排行榜後 scene-result 應該還是 1 次，實際 {n2}')
    b.close(); return fails

def VocabQuiz_ok(page, zh):
    return page.evaluate("z=>VocabQuiz.isWord([z,''])", zh)

def check_disabled(p, g):
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 390, 'height': 844}); ctx.route('**/*', route)
    page = ctx.new_page(); page.goto(f'http://127.0.0.1:{PORT}/games/{g}/index.html'); page.wait_for_timeout(400)
    page.fill('#player-name-input', 'AAA'); page.click('.btn-primary'); page.wait_for_timeout(800)
    page.evaluate('GAME.vocabQuiz=false')
    ok = play_to_result(page, g, wrong_once=False); page.wait_for_timeout(300)
    n = page.locator('[data-quiz-go]').count(); b.close()
    return [] if (ok and n == 0) else ['沒開小考的遊戲結果頁卻出現邀請卡片' if n else '玩不到結果頁']

def main():
    args = sys.argv[1:]
    games = args or enabled()
    bad = 0
    with sync_playwright() as p:
        for g in games:
            for lang, script in (('es', 'trad'), ('en', 'trad'), ('zh', 'trad'), ('es', 'simp')):
                try: f, e = check_game(p, g, lang, script)
                except Exception as ex: f, e = [f'測試中斷：{str(ex).splitlines()[0][:80]}'], []
                tag = f'{g} [{lang}/{script}]'
                if f or e: bad += 1; print('✗', tag, f, e)
                else: print('✓', tag)
        for g in games:
            try: f = check_embed(p, g)
            except Exception as ex: f = [f'測試中斷：{str(ex).splitlines()[0][:80]}']
            print('✓' if not f else '✗', g, '（地圖模式）', f); bad += bool(f)
        for g in ['bakery']:   # 旗標關掉就不能出現邀請卡
            f = check_disabled(p, g); print('✓' if not f else '✗', g, '（沒開小考）', f); bad += bool(f)
    sys.exit(1 if bad else 0)

if __name__ == '__main__': main()
