"""單字表檢查（實際玩）：每一關打開時，單字抽屜裡的詞有沒有出現在畫面上（台詞、選項、清單、手機…）。
用法：python3 tools/review/vocab_live.py [games...]   輸出 tools/review/out/vocab_live.json
每個遊戲玩 6 遍（正解 2 遍＋隨機 4 遍；隨機任務每次不同），某個詞在那一關「一次都沒出現」才算問題。"""
import sys, os, json, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import smoke
from playwright.sync_api import sync_playwright

GAMES = sys.argv[1:] or ['drinks', 'reserva', 'breakfast', 'parcel', 'nightmarket', 'bakery', 'clinic', 'mrt', 'street']
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'vocab_live.json')
res = json.load(open(OUT)) if os.path.exists(OUT) else {}
SNAP = """() => {
  const vz = [...document.querySelectorAll('#vocab-list .v-zh')].map(e => e.textContent);
  const gw = document.getElementById('game-window').cloneNode(true);
  gw.querySelectorAll('rt').forEach(r => r.remove());
  return { st: Game.state === '_TRANS' ? '_TRANS>' + Game._trans.to : Game.state, vz, text: gw.innerText };
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for g in GAMES:
        seen = {}          # (關卡, 詞) → [出現次數, 打開次數]
        orc = smoke.EXTRA.get(g) or smoke.ORACLES.get(g)
        for run in range(6):
            rng = random.Random(run)
            ctx = b.new_context(viewport={'width': 1000, 'height': 900}); ctx.route('**/*', smoke.route)
            page = ctx.new_page(); page.on('dialog', lambda d: d.accept())
            page.goto(f'http://127.0.0.1:{smoke.PORT}/games/{g}/index.html'); page.wait_for_timeout(400)
            page.fill('#player-name-input', 'María'); page.click('.btn-primary'); page.wait_for_timeout(300)
            bad = set()
            for step in range(200):
                try:
                    if page.evaluate("document.getElementById('leaderboard-screen').classList.contains('active')"): break
                    if page.evaluate('Game.mistakes') >= 8: page.evaluate('Game.mistakes = 0')
                    snap = page.evaluate(SNAP); st = snap['st']
                    if not st.startswith('_TRANS'):
                        for w in snap['vz']:
                            parts = [x for x in w.replace('...', '……').split('……') if x]
                            k = st + '|' + w
                            c = seen.setdefault(k, [0, 0]); c[1] += 1
                            if all(x in snap['text'] for x in parts): c[0] += 1
                    if g == 'breakfast' and page.evaluate("!!(Game.getConfig()[Game.state]||{}).pad"):
                        page.evaluate("Game.pad.ticket=[...Game.C.target]; Game.padSubmit()"); continue
                    opts = smoke.texts(page)
                    if not opts: page.wait_for_timeout(150); continue
                    ans = None
                    if orc and (run < 2 or rng.random() < 0.6):
                        try: ans = page.evaluate(orc)
                        except Exception: ans = None
                    idx = None
                    if ans:
                        for i, o in enumerate(opts):
                            if o.strip() == ans or ans in o: idx = i; break
                    if idx is None:
                        cand = [i for i, o in enumerate(opts) if (st, o) not in bad] or list(range(len(opts)))
                        idx = rng.choice(cand)
                    m0 = page.evaluate('Game.mistakes'); smoke.click_i(page, idx); page.wait_for_timeout(80)
                    if page.evaluate('Game.mistakes') > m0: bad.add((st, opts[idx]))
                except Exception:
                    page.wait_for_timeout(500)
            ctx.close()
        issues = [{'state': k.split('|')[0], 'word': k.split('|')[1], 'opened': v[1]} for k, v in seen.items() if v[0] == 0]
        res[g] = {'checked': len(seen), 'issues': issues}
        print(g, '檢查', len(seen), '個（關卡, 詞）｜畫面上從沒出現：', len(issues))
        json.dump(res, open(OUT, 'w'), ensure_ascii=False, indent=1)
    b.close()
