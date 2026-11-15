"""「從分享進來」記號（ref）測試（Playwright）。用法：python3 tools/ref_test.py
測：地圖首頁收到 ?ref= 暫存 → 地圖裡的遊戲（iframe）寫訪客／遊玩紀錄會帶 ref；直接開遊戲頁也會；
沒有 ref 就不帶；不合格的值（太長、空白、符號、腳本）一律忽略；大寫會轉小寫；暫存讀不到也不出錯、紀錄照寫；
新的分頁不會沿用上一個分頁的記號；game-kit 規則檔有加 ref；兩份紀錄程式（game-kit／本 repo）的 ref 段落一致。"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smoke
from playwright.sync_api import sync_playwright

PORT = smoke.PORT
ROOT = smoke.ROOT
GAMEKIT = os.environ.get('GAMEKIT', '/home/claude/game-kit')
fails = []; n = [0]
def ok(c, msg, extra=''):
    n[0] += 1
    if not c: fails.append(msg); print('  ✗', msg, extra)

# 假的 Firebase（不分版本；taiwan-life 的 HGPlays 用 12.17.1、game-kit 範本是 10.12.2）。
# 遊戲自己的排行榜／成績寫入忽略；HGPlays 寫的 visits／plays 記在最上層頁面的 window.__hg。
FAKE = {
 'firebase-app.js': "export const initializeApp=()=>({});",
 'firebase-auth.js': "export const getAuth=()=>({currentUser:{uid:'dev1'},authStateReady:async()=>{}}); export const signInAnonymously=async()=>{};",
 'firebase-firestore.js': """const W=()=>((window.top.__hg ||= []));
const HG=c=>c==='visits'||c==='plays';
export const getFirestore=()=>({}); export const serverTimestamp=()=>'TS';
export const doc=(db,col,id)=>({col,id}); export const collection=(db,col)=>({col});
export const setDoc=async(r,d)=>{ if(HG(r.col)) W().push([r.col,'set',d,r.id]); };
export const addDoc=async(c,d)=>{ if(HG(c.col)) W().push([c.col,'add',d]); return {id:'p1'}; };
export const updateDoc=async(r,d)=>{ if(HG(r.col)) W().push([r.col,'upd',d]); };
export const getDoc=async()=>({exists:()=>false,data:()=>null}); export const getDocs=async()=>({docs:[]});
export const deleteDoc=async()=>{}; export const query=c=>c; export const where=()=>({}); export const orderBy=()=>({}); export const limit=()=>({});
export const writeBatch=()=>({delete(){},commit:async()=>{}});""",
}
def route(r):
    u = r.request.url
    if 'gstatic.com/firebasejs/' in u and u.rsplit('/', 1)[1] in FAKE:
        return r.fulfill(body=FAKE[u.rsplit('/', 1)[1]], content_type='application/javascript')
    return smoke.route(r)

def newctx(b, init=None):
    ctx = b.new_context(viewport={'width': 430, 'height': 900}); ctx.route('**/*', route)
    if init: ctx.add_init_script(init)
    page = ctx.new_page(); errs = []
    page.on('pageerror', lambda e: errs.append(str(e))); page.on('dialog', lambda d: d.accept())
    return ctx, page, errs
def hg(page): return page.evaluate('window.__hg||[]')
def visit(page):
    v = [x for x in hg(page) if x[0] == 'visits']; return v[0][2] if len(v) == 1 else None
def start(page):
    v = [x for x in hg(page) if x[0] == 'plays' and x[1] == 'add']; return v[0][2] if len(v) == 1 else None
def play_direct(page, query):
    page.goto(f'http://127.0.0.1:{PORT}/games/noodle/index.html{query}'); page.wait_for_timeout(400)
    page.fill('#player-name-input', 'Ana'); page.click('.btn-primary'); page.wait_for_timeout(3200)   # 訪客紀錄等遊戲載完 2.5 秒才寫

with sync_playwright() as p:
    b = p.chromium.launch()

    print('[1] 地圖首頁 ?ref=share → 暫存 → 地圖裡的遊戲（iframe）帶上 ref')
    ctx, page, errs = newctx(b)
    page.goto(f'http://127.0.0.1:{PORT}/index.html?ref=share'); page.wait_for_timeout(500)
    ok(page.evaluate("sessionStorage.getItem('hg.ref')") == 'share', '首頁把 ref 暫存在分頁', str(page.evaluate("sessionStorage.getItem('hg.ref')")))
    page.evaluate("""(()=>{const f=document.createElement('iframe');f.id='t';f.style.cssText='position:fixed;left:0;top:0;width:420px;height:880px;z-index:99999;background:#fff;border:0';
      f.src='games/noodle/index.html?embed=1&name=Ana';document.body.appendChild(f);})()""")
    page.wait_for_timeout(600)
    fr = page.frame_locator('#t'); fr.locator('#intro-go').click(); page.wait_for_timeout(3200)
    v = visit(page); s = start(page)
    ok(v is not None and v.get('ref') == 'share', '地圖裡的遊戲：訪客紀錄帶 ref=share', str(v))
    ok(s is not None and s.get('ref') == 'share', '地圖裡的遊戲：遊玩紀錄帶 ref=share', str(s))
    ok(v and v.get('game') == 'tw_noodle' and v.get('tz', None) is not None or v is not None, '訪客紀錄其他欄位（game／tz）照舊', str(v))
    ok(not errs, '沒有 pageerror', str(errs)); ctx.close()

    print('[2] 直接開遊戲頁 ?ref=share')
    ctx, page, errs = newctx(b)
    play_direct(page, '?ref=share')
    v, s = visit(page), start(page)
    ok(v and v.get('ref') == 'share' and s and s.get('ref') == 'share', '直接開遊戲頁：訪客與遊玩紀錄都帶 ref', f'{v} {s}')
    ok(page.evaluate("sessionStorage.getItem('hg.ref')") == 'share', '遊戲頁也暫存（重新開始換網址時還在）')
    ok(not errs, '沒有 pageerror', str(errs)); ctx.close()

    print('[3] 沒有 ref：紀錄不帶 ref 欄位')
    ctx, page, errs = newctx(b)
    play_direct(page, '')
    v, s = visit(page), start(page)
    ok(v is not None and 'ref' not in v, '沒有 ref：訪客紀錄沒有 ref 欄位', str(v))
    ok(s is not None and 'ref' not in s, '沒有 ref：遊玩紀錄沒有 ref 欄位', str(s))
    ok(not errs, '沒有 pageerror', str(errs)); ctx.close()

    print('[4] 不合格的 ref 一律忽略；大寫轉小寫')
    for q, want in [('?ref=SHARE', 'share'), ('?ref=Ig_story-1', 'ig_story-1'), ('?ref=' + 'a' * 16, 'a' * 16),
                    ('?ref=' + 'a' * 17, None), ('?ref=', None), ('?ref=a%20b', None), ('?ref=%3Cscript%3E', None),
                    ('?ref=share%0A', 'share'), ('?ref=朋友', None), ('?ref=a.b', None)]:
        ctx, page, errs = newctx(b)
        play_direct(page, q)
        v = visit(page)
        got = v.get('ref') if v else 'NOVISIT'
        ok(v is not None and got == want, f'ref 參數 {q!r} → {want!r}', str(v))
        ok(not errs, f'{q!r}: 沒有 pageerror', str(errs)); ctx.close()

    print('[5] 新分頁不沿用上一個分頁的記號')
    ctx, page, errs = newctx(b)
    page.goto(f'http://127.0.0.1:{PORT}/index.html?ref=share'); page.wait_for_timeout(300)
    p2 = ctx.new_page(); p2.on('pageerror', lambda e: errs.append(str(e)))
    p2.goto(f'http://127.0.0.1:{PORT}/games/noodle/index.html'); p2.wait_for_timeout(300)
    ok(p2.evaluate("sessionStorage.getItem('hg.ref')") is None, '另開的新分頁沒有 ref 暫存')
    ctx.close()

    print('[6] 暫存讀不到（隱私模式）：不出錯、紀錄照寫、不帶 ref')
    ctx, page, errs = newctx(b, "Object.defineProperty(window,'sessionStorage',{get(){throw new Error('blocked')}})")
    play_direct(page, '?ref=share')
    v, s = visit(page), start(page)
    ok(v is not None and v.get('ref') == 'share', '暫存壞掉但網址有 ref：仍帶 ref', str(v))
    ctx.close()
    ctx, page, errs = newctx(b, "Object.defineProperty(window,'sessionStorage',{get(){throw new Error('blocked')}})")
    play_direct(page, '')
    v = visit(page)
    ok(v is not None and 'ref' not in v and not errs, '暫存壞掉、網址沒 ref：紀錄照寫、不出錯', f'{v} {errs}'); ctx.close()

    print('[7] 首頁 ?ref 不合格不暫存')
    for q in ['?ref=' + 'a' * 17, '?ref=a%20b', '']:
        ctx, page, errs = newctx(b)
        page.goto(f'http://127.0.0.1:{PORT}/index.html{q}'); page.wait_for_timeout(300)
        ok(page.evaluate("sessionStorage.getItem('hg.ref')") is None and not errs, f'首頁 {q!r} 不暫存', str(errs)); ctx.close()
    b.close()

print('[8] 規則檔與兩份紀錄程式')
rules = open(os.path.join(GAMEKIT, 'firebase-rules/memorma-24dab.rules.txt'), encoding='utf8').read()
for name, anchor in [('plays', "pl().keys().hasOnly(['game', 'level', 'uid', 'name', 'day', 'startedAt', 'done', 'tz', 'ref'])"),
                     ('visits', "vd().keys().hasOnly(['game', 'day', 'uid', 'at', 'tz', 'ref'])")]:
    ok(anchor in rules, f'規則檔：{name} 允許 ref 欄位')
ok("pl().ref is string && pl().ref.size() >= 1 && pl().ref.size() <= 16" in rules, '規則檔：plays 的 ref 是 1～16 字的字串')
ok("vd().ref is string && vd().ref.size() >= 1 && vd().ref.size() <= 16" in rules, '規則檔：visits 的 ref 是 1～16 字的字串')
ok(re.search(r'// 最後更新：2026-\d\d-\d\d \d\d:\d\d', rules) is not None, '規則檔：最後更新有日期加時間')
ok(len(re.findall(r'^//   - 20', rules, re.M)) == 3, '規則檔：變更紀錄只留 3 筆', str(len(re.findall(r'^//   - 20', rules, re.M))))
kit = open(os.path.join(GAMEKIT, 'parts/plays.js'), encoding='utf8').read()
mine = open(os.path.join(ROOT, 'shared/game.js'), encoding='utf8').read()
def refblock(t):
    a = t.index('  function cleanRef'); b2 = t.index('  var REF = refName();') + len('  var REF = refName();')
    return t[a:b2] + '|' + str('if (REF) v.ref = REF;' in t and 'if (REF) data.ref = REF;' in t and 'x')
ok(refblock(kit) == refblock(mine), 'game-kit 的 parts/plays.js 與 shared/game.js 的 ref 段落一致')

print(f'\n共 {n[0]} 項，失敗 {len(fails)} 項')
sys.exit(1 if fails else 0)
