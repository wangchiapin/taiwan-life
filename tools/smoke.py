import sys, re, random, threading, http.server, socketserver, functools
from playwright.sync_api import sync_playwright
import os
HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.dirname(HERE)
NPM=os.environ.get('NPM', os.path.join(HERE,'.npm','node_modules'))
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
socketserver.TCPServer.allow_reuse_address=True
PORT=8810+random.randrange(80)
srv=socketserver.ThreadingTCPServer(('127.0.0.1',PORT),functools.partial(H,directory=ROOT)); srv.handle_error=lambda *a: None; threading.Thread(target=srv.serve_forever,daemon=True).start()
# 假的 Firebase：不連網路，把寫入記在 window.__fbw = [[集合, 資料], ...]（測試會檢查上傳的成績紀錄）
FAKE_FB = """const W = (window.__fbw ||= []);
export const initializeApp=()=>({}); export const getFirestore=()=>({});
export const collection=(db,n)=>({n}); export const doc=(db,n,id)=>({n,id});
export const addDoc=async(c,d)=>{W.push([c.n,d]);return {id:'x'+W.length};};
export const setDoc=async(r,d)=>{W.push([r.n+'/'+r.id,d]);};
export const getDoc=async()=>({exists:()=>false,data:()=>null});
export const getDocs=async()=>({docs:[]}); export const deleteDoc=async()=>{};
export const query=c=>c; export const where=()=>({}); export const orderBy=()=>({}); export const limit=()=>({});
export const writeBatch=()=>({delete(){},commit:async()=>{}});"""
def route(r):
    u=r.request.url
    if 'pinyin-pro' in u: return r.fulfill(path=NPM+'/pinyin-pro/dist/index.js',content_type='application/javascript')
    if 'opencc-js' in u: return r.fulfill(path=NPM+'/opencc-js/dist/umd/t2cn.js',content_type='application/javascript')
    if 'gstatic.com/firebasejs' in u: return r.fulfill(body=FAKE_FB,content_type='application/javascript')
    if u.startswith('http://127.0.0.1'): return r.continue_()
    return r.abort()
def oracle_from(path):
    try: s=open(path,encoding='utf8').read()
    except Exception: return None
    m=re.search(r'ORACLE = """(.*?)"""',s,re.S); return m.group(1) if m else None
ORACLES={g:oracle_from(os.path.join(HERE,'oracles',g+'.py')) for g in ['bakery','clinic','mrt','street','parcel','nightmarket','school','ubike','bus','barber']}
EXTRA={'drinks': '''() => {
  const s = Game.state, t = Game.target, me = Game.mine;
  window.__first ??= Math.random() < .5 ? 'ami' : 'me';
  const c1 = (Game.first || window.__first) === 'ami' ? t : me, c2 = c1 === t ? me : t, o1 = Game.order[1];
  const m = { START: '去飲料店', WHO: window.__first === 'ami' ? '先點Ami的' : '先點我的',
    TYPE_1: c1.drink, SIZE_1: c1.size, SUGAR_1: c1.sugar, ICE_1: c1.ice,
    CHECK_1: () => sameOrder(Game.checkShown, o1) ? '對。' : '不對。', CORRECT_1: () => zhOrder(o1),
    TYPE_2: c2.drink, SIZE_2: c2.size, SUGAR_2: c2.sugar, ICE_2: c2.ice,
    TOPPING_2: '椰果', NO_COCONUT: '等一下，我問一下我朋友。', CALL_AMI: '好，我跟店員說。', TOPPING_3: Game.alt,
    PAYMENT: () => '拿出' + Game.bill + '元', CHANGE: () => Game.given === Game.bill - Game.total ? '好，謝謝。' : '不好意思，你找錯了。',
    APOLOGIZE: '沒關係，謝謝。', FINISH: '謝謝！' };
  const v = m[s]; return typeof v === 'function' ? v() : (v ?? null);
}'''}
TRANS=set()  # 每個遊戲額外的 oracle（覆蓋）
def texts(page):
    return page.evaluate("[...document.querySelectorAll('#options-area .opt')].map(b=>b.dataset.raw||b.innerText.replace(/\\n/g,''))")
def click_i(page,i): page.locator('#options-area .opt').nth(i).click()
def play(page,g,mode,log):
    bad=set(); trans=0; steps=0; seen=[]
    orc=EXTRA.get(g) or ORACLES.get(g)
    while steps<400:
        steps+=1
        if page.evaluate("document.getElementById('leaderboard-screen').classList.contains('active')"):
            if page.evaluate('EMBED'):   # 地圖模式：看完排行榜按「回到地圖」
                page.wait_for_timeout(300); page.click('#leaderboard-screen .btn-restart'); return 'embed-done',trans
            return 'leaderboard',trans
        st=page.evaluate('Game.state')
        if page.evaluate('Game.mistakes')>=8: page.evaluate('Game.mistakes=0')
        if st=='_TRANS':
            trans+=1; lab=texts(page); TRANS.add(page.evaluate('Game._trans.from+">"+Game._trans.to'))
            click_i(page,0); continue
        if g=='breakfast' and page.evaluate("!!(Game.getConfig()[Game.state]||{}).pad"):
            page.evaluate("Game.pad.ticket=[...Game.C.target]; Game.padSubmit()"); continue
        opts=texts(page)
        if not opts: page.wait_for_timeout(200); continue
        ans=None
        if orc and (mode=='perfect' or random.random()<0.6):
            try: ans=page.evaluate(orc)
            except Exception: ans=None
        idx=None
        if ans:
            for i,o in enumerate(opts):
                if o.strip()==ans: idx=i; break
            if idx is None:
                for i,o in enumerate(opts):
                    if ans in o: idx=i; break
        if idx is None:
            cand=[i for i,o in enumerate(opts) if (st,o) not in bad] or list(range(len(opts)))
            idx=random.choice(cand)
        m0=page.evaluate('Game.mistakes'); click_i(page,idx)
        if page.evaluate('Game.state')==st and page.evaluate('Game.mistakes')>m0: bad.add((st,opts[idx]))
    log.append(seen); return 'timeout',trans
def fbcheck(page,g,embed):
    """檢查上傳：每局剛好一筆 results（分數、錯誤數和遊戲一致）；單機版還要寫排行榜"""
    w=page.evaluate('window.__fbw||[]'); res=[d for c,d in w if c=='results']
    if len(res)!=1: return f'FB✗ results={len(res)}'
    r=res[0]; gs=page.evaluate('[Game.score,Game.mistakes,Game.log.length]')
    bad=[k for k,ok in [('scene',r['scene']==g),('score',r['score']==gs[0]),('mistakes',r['mistakes']==gs[1]),('errors',len(r['errors'])==gs[2]),
        ('embed',r['embed']==embed),('code',bool(re.match(r'^[A-Z]{3}-[0-9]{4}$',r['playerId']))),('stage',all(e['stage'] for e in r['errors']))] if not ok]
    lb=[c for c,d in w if c.endswith('_scores')]
    if len(lb)!=1: bad.append(f'leaderboard={len(lb)}')   # 單機和地圖模式都寫排行榜
    if embed:
        sc=page.evaluate('window.__sc||null')
        if not sc or sc.get('score')!=gs[0]: bad.append(f'scene-complete={sc}')
    return 'FB✓ '+r['playerId'] if not bad else 'FB✗ '+','.join(bad)
def run(g,mode='mixed',runs=3,embed=False,vp=None):
    out=[]
    with sync_playwright() as p:
        b=p.chromium.launch()
        for k in range(runs):
            ctx=b.new_context(viewport=vp or {'width':1000,'height':900}); ctx.route('**/*',route); ctx.add_init_script("addEventListener('message',e=>{if(e.data&&e.data.type==='scene-complete')window.__sc=e.data})"); page=ctx.new_page()
            errs=[]; page.on('pageerror',lambda e:errs.append(str(e))); page.on('dialog',lambda d:d.accept())
            url=f'http://127.0.0.1:{PORT}/games/{g}/index.html'+('?embed=1&name=Ana' if embed else '')
            page.goto(url); page.wait_for_timeout(400)
            if not embed: page.fill('#player-name-input','María'); page.click('.btn-primary')
            page.wait_for_timeout(300); log=[]
            end,tr=play(page,g,mode,log)
            page.wait_for_timeout(300)
            out.append((end,tr,page.evaluate('Game.score'),errs[:2], page.evaluate('Game.log.map(m=>m.zh).slice(0,4)') if mode=='perfect' else '', fbcheck(page,g,embed)))
            ctx.close()
        b.close()
    return out
if __name__=='__main__':
    games=sys.argv[2:] or ['drinks','reserva','breakfast','parcel','nightmarket','bakery','clinic','mrt','street']
    mode=sys.argv[1]
    for g in games:
        TRANS.clear()
        print(g, run(g, 'perfect' if mode=='perfect' else 'mixed', 1 if mode=='embed' else int(sys.argv[3] if False else 2), embed=(mode=='embed')))
        if mode=='trans': print('   ', sorted(TRANS))
