import sys, json, random, threading, http.server, socketserver, functools, os
from playwright.sync_api import sync_playwright

ROOT = '/home/claude/taiwan-life/games/clinic'
NPM = '/tmp/claude-0/-home-claude/8f33d4aa-72a3-5658-9ba9-7dc4c57090e0/scratchpad/npm/node_modules'
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
handler = functools.partial(H, directory=ROOT)
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(('127.0.0.1', 8796), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = 'http://127.0.0.1:8796/index.html'
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
  const m = {
    START: '出發去診所', R_CARD: '有，這是我的健保卡', R_FIRST: '對，我第一次來', R_DEPT: '家醫科', R_TICKET: '好，謝謝',
    W_WAIT: Game.cur === t.myNo ? '進診間' : '繼續等候',
    D_SYMPTOM: Game.sentence(t.sym, t.days)[0],
    D_FEVER: t.fever ? '有，我有一點發燒' : '沒有，我沒有發燒',
    D_ALLERGY: t.allergy ? '有，我對止痛藥過敏' : '沒有，沒有過敏',
    D_ADVICE: '好，謝謝醫生', P_PAY: '給200元', M_MED: '好，我知道了',
    M_NOW: t.now === 'lunch' ? '感冒藥' : '止咳藥',
    E_ASK: '醫生說是感冒，藥吃' + NZ(t.rx) + '天，要多喝水、多休息。'
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
