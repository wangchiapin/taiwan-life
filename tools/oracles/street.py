import sys, json, random, threading, http.server, socketserver, functools, os
from playwright.sync_api import sync_playwright

ROOT = '/home/claude/taiwan-life/games/street'
NPM = '/tmp/claude-0/-home-claude/8f33d4aa-72a3-5658-9ba9-7dc4c57090e0/scratchpad/npm/node_modules'
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
handler = functools.partial(H, directory=ROOT)
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(('127.0.0.1', 8799), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = 'http://127.0.0.1:8799/index.html'
SMART = False

def route(r):
    u = r.request.url
    if 'pinyin-pro' in u: return r.fulfill(path=NPM + '/pinyin-pro/dist/index.js', content_type='application/javascript')
    if 'opencc-js' in u: return r.fulfill(path=NPM + '/opencc-js/dist/umd/t2cn.js', content_type='application/javascript')
    if 'firebase' in u: return r.fulfill(body='export const initializeApp=()=>({});export const getFirestore=()=>({});export const collection=()=>({});export const addDoc=async()=>({});export const query=()=>({});export const orderBy=()=>({});export const limit=()=>({});export const getDocs=async()=>({docs:[]});', content_type='application/javascript')
    if u.startswith('http://127.0.0.1'): return r.continue_()
    return r.abort()

ORACLE = """() => {
  const t = Game.task, s = Game.state;
  const fw = t.fallWho[0], ew = t.elderWho[0], ww = t.walletWho[0];
  const m = {
    START: '走上街', E_light: '等到小綠人亮了再走。', E_honk: '往旁邊靠一下，讓他先過。', E_fall: '「您還好嗎？哪裡痛？」', E_fall2: '您先別動，我幫您叫救護車。',
    E_elder: ew + '，我陪您慢慢過。', E_ask: '直走，到第' + CN[t.n] + '個路口' + t.dir[0] + '，在' + t.lm[0] + '旁邊。',
    E_wallet: ww + '，不好意思，您的錢包掉了！', E_rain: '好，謝謝你，那就麻煩你了。', E_flyer: '不好意思，我趕時間，不用了，謝謝。',
    END: '查看結果', RESULT: '查看排行榜'
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
            page.add_init_script(('window.__SMART=true;' if SMART else '') + "window.__msgs=[];window.addEventListener('message',e=>window.__msgs.push(e.data));")
            page.goto(url); page.wait_for_timeout(300)
            if 'embed=1' not in url:
                page.fill('#player-name-input', 'María'); page.click('.btn-primary')
            page.wait_for_timeout(200)
            end = play(page, mode)
            page.wait_for_timeout(800)
            try: page.wait_for_load_state('load')
            except Exception: pass
            info = page.evaluate('({score: Game.score, mistakes: Game.mistakes, state: Game.state, msgs: window.__msgs, bonus: Game._bonus, tray: Game.cur, hv: Game.hintViews})')
            results.append((end, info, errs))
        b.close()
    return results

if __name__ == '__main__':
    which = sys.argv[1]
    if which == 'perfect':
        res = run('perfect', BASE, 4)
        print([(r[0], r[1]['score'], r[1]['mistakes'], r[1]['tray'], r[2]) for r in res])
    if which == 'smart':
        SMART = True
        res = run('perfect', BASE, 6)
        print([(r[0], r[1]['score'], r[1]['mistakes'], r[2]) for r in res])
    if which == 'random':
        res = run('mixed', BASE, 8)
        print('ends', [r[0] for r in res], 'scores', [(r[1]['score'], r[1]['mistakes']) for r in res], 'errors', [r[2] for r in res if r[2]][:3])
    if which == 'embed':
        res = run('perfect', BASE + '?embed=1&name=Ana', 3)
        for r in res: print(r[0], r[1]['score'], r[1]['msgs'], r[2])
