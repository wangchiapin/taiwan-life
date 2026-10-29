r"""涵蓋測試：python3 tools/coverage.py <遊戲…> [--max 40] [--min 10] [--out 資料夾]

用途：不是把幾千萬種組合都跑一遍，而是保證
  1. 每個隨機項的每個選項至少出現過；而且「每兩個隨機項的每種搭配」也至少出現過（處理互相牽動）
  2. 每一關：每個選項（對的、錯的）都按過；錯的選項按完再按對的（處理玩家操作路線）
並回報：哪些搭配沒測到、哪些關卡沒走到、哪些錯的選項沒按過、卡住、網頁錯誤、上傳不對。

做法（不改遊戲本身，只在測試時動手腳）：
  - 瀏覽器載入遊戲時，攔截 shared/game.js 和遊戲 html，把 pick／Math.random() < p／Math.floor(Math.random()*n)
    換成「可以指定選第幾個」的版本。只在 Game.setup()（每局開始決定題目的時候）生效。
  - 每場的指定方式：邊抽邊挑「還沒出現過的搭配最多」的選項（貪心），所以場數很少。
  - shuffle（洗牌）、很大範圍的亂數（電話號碼、幾十種的數字）不指定，用固定種子的亂數；
    所以「洗牌抽到哪幾個」只能靠多跑幾場來碰運氣，報告裡不算涵蓋。
  - 玩的時候：每到一關，先按一個還沒按過的錯選項，再按正解（用 tools/oracles 的正解）。

【限制】正解（oracles）要有；點單板、拖曳這類 oracle 自己處理的操作，只當作「照正解走」，不另外試錯。
【注意】跑的時候不要同時再跑 smoke.py（共用同一套測試伺服器邏輯，但各自開埠，其實可並行；保險起見不要改檔）。
"""
import sys, os, re, json, time, random, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location('smoke', os.path.join(HERE, 'smoke.py'))
smoke = importlib.util.module_from_spec(spec); sys.modules['smoke'] = smoke; spec.loader.exec_module(smoke)
from playwright.sync_api import sync_playwright

CTRL_JS = r"""
(() => {
  let s = 0x9e3779b9;
  window.__seed = v => { s = (v >>> 0) || 1; };
  const rnd = () => { s ^= s << 13; s >>>= 0; s ^= s >>> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; };
  Math.random = rnd;
  const R = window.__R = {
    on: false, log: [], cov: new Set(window.__cov || []),
    key(j, u, k, v) { return j + ':' + u + '|' + k + ':' + v; },
    begin() { this.on = true; this.log = []; }, end() { this.on = false; },
    pickIdx(n, kind) {
      if (!this.on || this.log.length >= 80) return null;
      const k = this.log.length; let best = -1, bs = [];
      for (let v = 0; v < n; v++) {
        let sc = 0; for (const e of this.log) if (!this.cov.has(this.key(e.k, e.v, k, v))) sc++;
        if (!this.cov.has('s' + k + ':' + v)) sc += 0.5;
        if (sc > best) { best = sc; bs = [v]; } else if (sc === best) bs.push(v);
      }
      const v = bs[Math.floor(rnd() * bs.length)]; this.log.push({ k, n, v, kind }); return v;
    },
    rnd,
    pick(a) { const n = a.length; if (n < 2 || n > 40) return a[Math.floor(rnd() * n)]; const v = this.pickIdx(n, 'p'); return v == null ? a[Math.floor(rnd() * n)] : a[v]; },
    fl(n) { n = Math.floor(n); if (!(n >= 2) || n > 9) return Math.floor(rnd() * n); const v = this.pickIdx(n, 'f'); return v == null ? Math.floor(rnd() * n) : v; },
    m2() { const v = this.pickIdx(2, 'b'); return v == null ? rnd() : (v === 0 ? 0.001 : 0.999); }
  };
})();
"""

def patch_src(s, is_game_js):
    s = re.sub(r'Math\.random\(\) <', '__R.m2() <', s)
    s = re.sub(r'Math\.floor\(Math\.random\(\) \* (\([^()]*\)|[^()]+?)\)', r'__R.fl(\1)', s)
    if is_game_js:
        s = re.sub(r'^const pick =.*$', 'const pick = arr => __R.pick(arr);', s, flags=re.M)
        s = re.sub(r'^const shuffle =.*$', 'const shuffle = arr => { const a = [...arr]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(__R.rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };', s, flags=re.M)
    return s

def route(r):
    u = r.request.url
    m = re.match(r'http://127\.0\.0\.1:\d+/(.*?)(\?.*)?$', u)
    if m:
        rel = m.group(1)
        if rel.startswith('games/') and rel.endswith('index.html') or rel == 'shared/game.js':
            try: src = open(os.path.join(ROOT, rel), encoding='utf8').read()
            except Exception: return r.continue_()
            return r.fulfill(body=patch_src(src, rel == 'shared/game.js'), content_type='text/html; charset=utf-8' if rel.endswith('.html') else 'application/javascript')
    return smoke.route(r)

def norm(t): return re.sub(r'\d+', '#', t)

def play_cov(page, g, stats, tried):
    """照正解走；每一關先按一個還沒按過的錯選項，再按正解。回傳 (結束狀態, 卡住的關卡)"""
    orc = smoke.EXTRA.get(g) or smoke.ORACLES.get(g)
    steps = 0; just_wrong = None
    while steps < 500:
        steps += 1
        if page.evaluate("document.getElementById('leaderboard-screen').classList.contains('active')"): return 'leaderboard'
        if page.locator('#ami-pop').count():
            page.click('#ami-pop [data-act="open"]' if page.locator('#ami-pop [data-act="open"]').count() else '#ami-pop [data-act="reply"]'); continue
        st = page.evaluate('Game.state')
        stats['visited'].add(st)
        if page.evaluate('Game.mistakes') >= 8: page.evaluate('Game.mistakes=0')
        if st == '_TRANS':
            stats['visited'].add('_TRANS:' + page.evaluate('Game._trans.from+">"+Game._trans.to'))
            smoke.click_i(page, 0); continue
        if g == 'breakfast' and page.evaluate("!!(Game.getConfig()[Game.state]||{}).pad"):
            page.evaluate("Game.pad.ticket=[...Game.C.target]; Game.padSubmit()"); continue
        opts = smoke.texts(page)
        if not opts: page.wait_for_timeout(200); continue
        page.evaluate("g=>{if(typeof Game.testPrep==='function')Game.testPrep(g)}", True)
        ans = None
        if orc:
            try: ans = page.evaluate(orc)
            except Exception: ans = None
        idx = None
        if ans:
            for i, o in enumerate(opts):
                if o.strip() == ans: idx = i; break
            if idx is None:
                for i, o in enumerate(opts):
                    if ans in o: idx = i; break
        seen = stats['seen'].setdefault(st, set()); seen.update(norm(o) for o in opts)
        if idx is None:
            stats['no_oracle'].add(st)
            idx = random.randrange(len(opts))
        else:
            stats['right'].setdefault(st, set()).add(norm(opts[idx]))
            if just_wrong != st:
                t = tried.setdefault(st, set())
                cand = [i for i in range(len(opts)) if i != idx and norm(opts[i]) not in t]
                if cand:
                    w = cand[0]; t.add(norm(opts[w])); just_wrong = st
                    stats['wrong'].setdefault(st, set()).add(norm(opts[w]))
                    smoke.click_i(page, w); continue
            just_wrong = None
        smoke.click_i(page, idx)
    return 'timeout'

def run_game(g, max_runs, min_runs, out):
    cov = set(); sites = {}; stats = {'visited': set(), 'seen': {}, 'right': {}, 'wrong': {}, 'no_oracle': set()}
    tried = {}; problems = []; all_states = set(); stale = 0; runs = 0; t0 = time.time(); ends = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        while runs < max_runs:
            runs += 1
            ctx = b.new_context(viewport={'width': 1000, 'height': 900}); ctx.route('**/*', route)
            ctx.add_init_script(f"window.__cov={json.dumps(sorted(cov))};" + CTRL_JS + f"window.__seed({runs * 7919 + 13});")
            page = ctx.new_page(); errs = []
            page.on('pageerror', lambda e: errs.append(str(e))); page.on('dialog', lambda d: d.accept())
            try:
                page.goto(f'http://127.0.0.1:{smoke.PORT}/games/{g}/index.html'); page.wait_for_timeout(400)
                page.fill('#player-name-input', 'María')
                page.evaluate("()=>{const o=Game.setup; Game.setup=function(){__R.begin(); try{return o.apply(this,arguments)}finally{__R.end()}}}")
                page.click('.btn-primary'); page.wait_for_timeout(300)
                log = page.evaluate('__R.log')
                try: all_states.update(page.evaluate('Object.keys(Game.getConfig())'))
                except Exception: pass
                before_w = sum(len(v) for v in stats['wrong'].values()); before_s = len(stats['visited'])
                end = play_cov(page, g, stats, tried); page.wait_for_timeout(200)
                ends.append(end)
                if end != 'leaderboard': problems.append(f'第{runs}場：{end}（狀態 {page.evaluate("Game.state")}）')
                if errs: problems.append(f'第{runs}場：網頁錯誤 {errs[0][:120]}')
                if end == 'leaderboard':
                    fb = smoke.fbcheck(page, g, False)
                    if not fb.startswith('FB✓'): problems.append(f'第{runs}場：上傳 {fb}')
            except Exception as e:
                problems.append(f'第{runs}場：測試程式例外 {str(e)[:150]}'); log = []; before_w = before_s = 0
            ctx.close()
            new = 0
            for e in log:
                sites[e['k']] = max(sites.get(e['k'], 0), e['n'])
                if f"s{e['k']}:{e['v']}" not in cov: cov.add(f"s{e['k']}:{e['v']}"); new += 1
                for f in log:
                    if f['k'] < e['k']:
                        key = f"{f['k']}:{f['v']}|{e['k']}:{e['v']}"
                        if key not in cov: cov.add(key); new += 1
            new += sum(len(v) for v in stats['wrong'].values()) - before_w + len(stats['visited']) - before_s
            stale = 0 if new else stale + 1
            print(f'  [{g}] 第 {runs} 場 新增 {new}  ({int(time.time() - t0)} 秒)', flush=True)
            if runs >= min_runs and stale >= 4: break
        b.close()
    ks = sorted(sites); total_pairs = sum(sites[a] * sites[b2] for i, a in enumerate(ks) for b2 in ks[i + 1:])
    got_pairs = sum(1 for c in cov if '|' in c); got_single = sum(1 for c in cov if c.startswith('s')); total_single = sum(sites.values())
    rep = [f'## {g}', f'- 跑了 {runs} 場（{int(time.time() - t0)} 秒）；結束狀態：{dict((e, ends.count(e)) for e in set(ends))}',
           f'- 隨機項：{len(ks)} 個被我指定的抽取點，單一選項涵蓋 {got_single}/{total_single}；兩兩搭配涵蓋 {got_pairs}/{total_pairs}（沒涵蓋的有些本來就不可能同時出現）',
           f'- 關卡：總共 {len(all_states)} 個，走到 {len(stats["visited"] & all_states)} 個；沒走到：{sorted(all_states - stats["visited"]) or "無"}']
    allw = sum(len(v) for v in stats['wrong'].values()); alls = sum(len(v) for v in stats['seen'].values())
    rep.append(f'- 選項：出現過 {alls} 種不同選項文字（數字視為同一個），其中正解 {sum(len(v) for v in stats["right"].values())} 種、按過的錯選項 {allw} 種')
    nm = []
    for st, seen in sorted(stats['seen'].items()):
        miss = seen - stats['right'].get(st, set()) - stats['wrong'].get(st, set())
        if miss: nm.append(f'{st}（{len(miss)} 種沒按過）')
    rep.append('- 還有錯選項沒按過的關卡：' + ('、'.join(nm) or '無'))
    if stats['no_oracle']: rep.append(f'- 沒有正解可用（隨機點選）的關卡：{sorted(stats["no_oracle"])}')
    rep.append('- 問題：' + ('；'.join(problems) if problems else '無'))
    text = '\n'.join(rep); print(text, flush=True)
    os.makedirs(out, exist_ok=True); open(os.path.join(out, f'{g}.md'), 'w', encoding='utf8').write(text + '\n')
    return text

if __name__ == '__main__':
    a = sys.argv[1:]
    def opt(name, d):
        if name in a: i = a.index(name); v = a[i + 1]; del a[i:i + 2]; return type(d)(v)
        return d
    mx, mn, out = opt('--max', 40), opt('--min', 10), opt('--out', '/tmp/coverage')
    games = a or ['school', 'bookstore', 'reserva']
    for g in games: run_game(g, mx, mn, out)
