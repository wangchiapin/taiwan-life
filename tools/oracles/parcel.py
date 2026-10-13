import sys, json, random, threading, http.server, socketserver, functools, os
from playwright.sync_api import sync_playwright

ROOT = '/home/claude/parcel'
NPM = '/tmp/claude-0/-home-claude/8f33d4aa-72a3-5658-9ba9-7dc4c57090e0/scratchpad/npm/node_modules'
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
handler = functools.partial(H, directory=ROOT)
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(('127.0.0.1', 8791), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = 'http://127.0.0.1:8791/index.html'

def route(r):
    u = r.request.url
    if 'pinyin-pro' in u: return r.fulfill(path=NPM + '/pinyin-pro/dist/index.js', content_type='application/javascript')
    if 'opencc-js' in u: return r.fulfill(path=NPM + '/opencc-js/dist/umd/t2cn.js', content_type='application/javascript')
    if 'firebase' in u: return r.fulfill(body='export const initializeApp=()=>({});export const getFirestore=()=>({});export const collection=()=>({});export const addDoc=async()=>({});export const query=()=>({});export const orderBy=()=>({});export const limit=()=>({});export const getDocs=async()=>({docs:[]});', content_type='application/javascript')
    if u.startswith('http://127.0.0.1'): return r.continue_()
    return r.abort()

ORACLE = """() => {
  const t = Game.task, s = Game.state, N = Game.N;
  const amt = {100:'一百元',300:'三百元',500:'五百元',1000:'一千元'};
  const m = {
    START: '好，出門去超商！', STORE: '去' + t.store, GREET: '我要取貨。',
    M_TAIL: '末三碼是' + t.momTail + '。', M_NAME: t.momName + '。',
    M_CHECK: Game._wrongBox ? '不對，名字不一樣。' : '對，是這個。',
    M_PAY: '好，給你一千元。',
    M_CHANGE: Game._changeGiven === Game._change ? '好，謝謝。' : '不好意思，好像少找了。',
    CALL: '好，我再問問看。', D_TAIL: '末三碼是' + t.dadTail + '。', D_NAME: t.dadName + '。', D_CONFIRM: '按「確認取貨」',
    Y_ASK: t.yourArrived ? '還有我的包裹，末三碼是' + t.yourTail + '。' : '我的包裹還沒到店，不用了。',
    Y_NAME: N + '。', Y_CONFIRM: '按「確認取貨」', CARD: '我要幫悠遊卡加值。', CARD_AMT: amt[t.cardTop],
    CARD_TAP: '把卡放在感應區上', BAG: '不用，我自己拿就好，謝謝。'
  };
  return m[s] ?? null;
}"""

def click_text(page, text):
    btns = page.locator('#options-area .opt')
    n = btns.count()
    for i in range(n):
        if btns.nth(i).inner_text().replace('\n','').strip() == text or text in btns.nth(i).inner_text().replace('\n',''):
            btns.nth(i).click(); return True
    return False

def play(page, mode):
    steps = 0
    while steps < 200:
        steps += 1
        try: st = page.evaluate('Game.state')
        except Exception: page.wait_for_timeout(500); continue
        try:
            if page.evaluate("document.getElementById('leaderboard-screen').classList.contains('active')"): return 'leaderboard'
        except Exception: page.wait_for_timeout(500); continue
        if mode == 'perfect' or (mode == 'mixed' and random.random() < 0.65):
            ans = page.evaluate(ORACLE)
            if ans is None:   # END / RESULT
                if st == 'RESULT' and page.evaluate('EMBED'):
                    page.locator('#options-area .opt').first.click(); return 'embed-done'
                page.locator('#options-area .opt').first.click()
            else:
                try: assert click_text(page, ans), (st, ans, page.locator('#options-area').inner_text())
                except Exception as e:
                    if mode == 'perfect': raise
                    page.wait_for_timeout(300)
        else:
            btns = page.locator('#options-area .opt'); n = btns.count()
            if st == 'RESULT' and page.evaluate('EMBED'):
                btns.first.click(); return 'embed-done'
            try: btns.nth(random.randrange(n)).click(timeout=2000)
            except Exception: page.wait_for_timeout(500)
    return 'timeout'

def run(mode, url, runs, extra=None, viewport=None):
    results = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for i in range(runs):
            ctx = b.new_context(viewport=viewport or {'width': 1100, 'height': 900})
            ctx.route('**/*', route)
            page = ctx.new_page()
            errs = []
            page.on('pageerror', lambda e: errs.append(str(e)))
            page.on('dialog', lambda d: d.accept())
            page.add_init_script("window.__msgs=[];window.addEventListener('message',e=>window.__msgs.push(e.data));")
            page.goto(url); page.wait_for_timeout(300)
            if 'embed=1' not in url:
                page.fill('#player-name-input', 'María'); page.click('.btn-primary')
            page.wait_for_timeout(200)
            end = play(page, mode)
            page.wait_for_timeout(800)
            try: page.wait_for_load_state('load')
            except Exception: pass
            info = page.evaluate('({score: Game.score, mistakes: Game.mistakes, state: Game.state, msgs: window.__msgs, store: Game.task && Game.task.store})')
            results.append((end, info, errs))
        b.close()
    return results

if __name__ == '__main__':
    which = sys.argv[1]
    if which == 'random':
        res = run('mixed', BASE, 8)
        print('ends', [r[0] for r in res], 'scores', [(r[1]['score'], r[1]['mistakes']) for r in res], 'errors', [r[2] for r in res if r[2]][:3])
    if which == 'embed':
        res = run('perfect', BASE + '?embed=1&name=Ana&store=仁愛門市', 3)
        for r in res: print(r[0], r[1]['score'], r[1]['msgs'], r[1]['store'], r[2])
