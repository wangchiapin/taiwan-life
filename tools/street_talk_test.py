r"""地圖路人對話測試：python3 tools/street_talk_test.py
檢查：①每個路人走近都會冒出泡泡、台詞是 LINES 裡的那句（繁／簡都對）②新增 3 句＋ IG 那句都有人說
③點泡泡開卡片，IG 那句有「前往 IG」連結（網址正確、新分頁、安全屬性），其他句子沒有連結
④簡體、西／英文、拼音都正常 ⑤沒有網頁錯誤。"""
import sys, os, random, threading, http.server, socketserver, functools
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
socketserver.TCPServer.allow_reuse_address = True
PORT = 8890 + random.randrange(80)
srv = socketserver.ThreadingTCPServer(('127.0.0.1', PORT), functools.partial(H, directory=ROOT)); srv.handle_error = lambda *a: None
threading.Thread(target=srv.serve_forever, daemon=True).start()
FAILS = []; N = [0]
def check(name, ok, info=''):
    N[0] += 1
    if not ok: FAILS.append(f'✗ {name} {info}'); print('✗', name, info)
IG = 'https://www.instagram.com/cadadiaunosminutos_ben_chino/'
NEW = {'class': '要不要上中文課？', 'nice': '你的中文很好欸！', 'learn': '要跟我學中文嗎？', 'ig': '搜尋IG：cadadiaunosminutos_ben_chino'}
def route(r):
    return r.continue_() if r.request.url.startswith('http://127.0.0.1') else r.abort()
def run(b, script, lang, vp):
    ctx = b.new_context(viewport=vp); ctx.route('**/*', route)
    ctx.add_init_script("localStorage.setItem('taiwan_player', JSON.stringify({name:'Ana', script:'%s', lang:'%s'}))" % (script, lang))
    p = ctx.new_page(); errs = []; p.on('pageerror', lambda e: errs.append(str(e)))
    p.goto(f'http://127.0.0.1:{PORT}/index.html'); p.wait_for_timeout(1200)
    p.evaluate("() => { const o = document.getElementById('story-ov'); if (o) { o.classList.remove('show'); o.style.display = 'none'; } P.locked = false; }")
    n = p.evaluate('WALKERS.length'); tag = f'{script}/{lang}/{vp["width"]}'
    seen = {}
    for i in range(n):
        # 把玩家放到路人旁邊（同一行、隔一格），鏡頭跟過去
        p.evaluate("""i => { const w = WALKERS[i]; w.pause = 99; const cx = Math.round(w.x);
          const cands = [cx + 1, cx - 1, cx + 2, cx - 2].filter(x => x >= 0 && x < COLS && sidewalkOk(x, w.row));   // 避開門口，不然會走進建築物
          P.x = cands[0] ?? cx; P.y = w.row; P.moving = null; P.path = []; camSnap = true; }""", i)
        p.wait_for_timeout(400)
        info = p.evaluate("""i => { updateBubble(); const w = WALKERS[i]; const b = document.getElementById('bubble');
          return { hidden: b.hidden, text: b.innerText, line: w.line, now: bubNow && bubNow.key }; }""", i)
        check(f'{tag} 路人{i}：有泡泡', not info['hidden'], str(info))
        if info['hidden']: continue
        zh = p.evaluate("zhOf(LINES[WALKERS[%d].line])" % i)
        check(f'{tag} 路人{i}：泡泡台詞正確', zh in info['text'], f'{info["text"]!r} vs {zh!r}')
        seen[info['line']] = i
        p.click('#bubble'); p.wait_for_timeout(150)
        card = p.evaluate("""() => { const c = document.getElementById('card'), l = c.querySelector('.c-link');
          return { open: !c.hidden, zh: c.querySelector('.c-zh').innerText, py: c.querySelector('.c-py').innerText, tr: c.querySelector('.c-tr').innerText,
                   linkShown: !l.hidden, href: l.getAttribute('href'), target: l.target, rel: l.rel, ltxt: l.innerText }; }""")
        check(f'{tag} 路人{i}：卡片打開', card['open'])
        if info['line'] == 'ig':
            check(f'{tag} IG 卡片：有連結按鈕', card['linkShown'] and card['href'] == IG, str(card))
            check(f'{tag} IG 卡片：新分頁＋安全屬性', card['target'] == '_blank' and 'noopener' in card['rel'], str(card))
            if lang != 'zh': check(f'{tag} IG 卡片：按鈕文字', 'IG' in card['ltxt'], card['ltxt'])
        else:
            check(f'{tag} 路人{i}（{info["line"]}）：沒有連結按鈕', not card['linkShown'] and card['href'] is None, str(card))
        if info['line'] in NEW and script == 'trad': check(f'{tag} {info["line"]} 繁體台詞', card['zh'] == NEW[info['line']], card['zh'])
        if info['line'] == 'nice' and lang != 'zh': check(f'{tag} nice 拼音有 éi', 'éi' in card['py'], card['py'])
        p.click('#card .c-close')
    for k in NEW: check(f'{tag} 「{k}」有人說', k in seen, str(seen))
    check(f'{tag} 沒有網頁錯誤', not errs, str(errs[:2]))
    ctx.close()
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for script, lang in [('trad', 'es'), ('simp', 'en'), ('trad', 'zh')]:
        for vp in [{'width': 1000, 'height': 900}, {'width': 390, 'height': 780}]:
            run(b, script, lang, vp)
    b.close()
print(f'{N[0]} 項檢查，{len(FAILS)} 項失敗')
if FAILS: print('\n'.join(FAILS)); sys.exit(1)
print('全部通過')
