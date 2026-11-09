r"""共用檢查：語言／字體／拼音設定、任務提示面板、本關單字面板、錯誤紀錄面板
用法：python3 tools/panels_test.py [遊戲…]（不指定＝全部遊戲）　　要快一點：加 --quick（只測一組設定）

做法：每個遊戲用「正解」玩一整局，每到一個新關卡（含過場）就檢查一次；共三組設定各玩一局：
  ① 繁體 + 西文 + 拼音　② 簡體 + 英文 + 注音　③ 繁體 + 只有中文 + 不顯示拼音
每一關檢查：
  1. 畫面文字裡沒有 undefined / NaN / [object / null
  2. 任務提示面板打得開、有內容
  3. 本關單字面板：數量對、每個單字有翻譯（只有中文時除外）、有拼音或注音（不顯示時除外）
  4. 錯誤紀錄面板打得開
  5. 網頁沒有錯誤
另外（只提醒、不算失敗）：本關單字裡，哪些字這一局在這一關的畫面上沒看到（隨機的變化可能剛好沒抽到）。
其他遊戲自己的測試（例如 yansuji_test.py）最後會呼叫 check_games([自己]) 一起跑這個檢查。"""
import sys, os, re, glob, json, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
if 'smoke' in sys.modules: smoke = sys.modules['smoke']
else:
    _spec = importlib.util.spec_from_file_location('smoke', os.path.join(HERE, 'smoke.py'))
    smoke = importlib.util.module_from_spec(_spec); sys.modules['smoke'] = smoke; _spec.loader.exec_module(smoke)

CONFIGS = [
    ('繁體+西文+拼音', {'script': 'trad', 'lang': 'es', 'phon': 'pinyin'}),
    ('簡體+英文+注音', {'script': 'simp', 'lang': 'en', 'phon': 'zhuyin'}),
    ('繁體+只有中文+不顯示拼音', {'script': 'trad', 'lang': 'zh', 'phon': 'off'}),
]
BAD_TEXT = re.compile(r'undefined|NaN|\[object|\bnull\b')
TEXT_JS = "(()=>{const c=document.getElementById('game-window').cloneNode(true);c.querySelectorAll('rt').forEach(r=>r.remove());return c.innerText})()"


def all_games():
    return sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(ROOT + '/games/*/index.html'))


def run_one(g, cfg_name, cfg):
    """玩一局、邊玩邊檢查。回傳 (檢查數, 失敗清單, 提醒清單)"""
    st = {'n': 0, 'fails': [], 'done': set(), 'seen': {}, 'vocab': None}
    def check(name, ok, info=''):
        st['n'] += 1
        if not ok: st['fails'].append(f'✗ {g}［{cfg_name}］{name} {info}'.strip())
    def probe(page, state):
        try:
            if state == '_TRANS':
                frm = page.evaluate('Game._trans.from'); to = page.evaluate('Game._trans.to')
                for k in (frm, to): st['seen'][k] = st['seen'].get(k, '') + page.evaluate(TEXT_JS)   # 過場的話和按鈕，前後兩關都算
                key = '_TRANS:' + frm
                if key in st['done']: return
                st['done'].add(key)
                check(f'過場（{frm}）畫面文字', not BAD_TEXT.search(page.evaluate(TEXT_JS)), BAD_TEXT.search(page.evaluate(TEXT_JS)) and BAD_TEXT.search(page.evaluate(TEXT_JS)).group())
                return
            txt = page.evaluate(TEXT_JS)
            st['seen'][state] = st['seen'].get(state, '') + txt
            if state in st['done']: return
            st['done'].add(state)
            if st['vocab'] is None:
                st['vocab'] = page.evaluate("typeof VOCAB!=='undefined'?VOCAB:{}")
                st['vocab_of'] = page.evaluate("typeof VOCAB_OF!=='undefined'?VOCAB_OF:{}")   # 有些遊戲（飲料店）好幾關共用同一組單字
            m = BAD_TEXT.search(txt)
            check(f'{state} 畫面文字沒有 undefined 之類', not m, m and m.group())
            if state in ('START', 'RESULT') or page.evaluate("!document.getElementById('game-window').classList.contains('active')"):
                return   # 開始畫面、結果頁沒有側邊分頁
            # 任務提示
            if page.evaluate("(()=>{const b=document.getElementById('hint-tab');return !!b&&!b.hidden&&b.offsetParent!==null})()"):
                page.evaluate('Hints.toggle(true)')
                st['seen'][state] += page.evaluate("document.getElementById('hints').innerText")
                n = page.evaluate("document.getElementById('hints').innerText.trim().length")
                check(f'{state} 任務提示有內容', n > 5, n)
                page.evaluate('Hints.toggle(false)')
            # 本關單字
            vl = (st['vocab'] or {}).get((st.get('vocab_of') or {}).get(state) or state) or []
            hidden = page.evaluate("document.getElementById('vocab-tab').hidden")
            check(f'{state} 單字分頁{"隱藏" if not vl else "顯示"}', hidden == (not vl), (len(vl), hidden))
            if vl:
                page.evaluate('Vocab.toggle(true)')
                items = page.evaluate("[...document.querySelectorAll('#vocab-list li')].map(li=>({zh:li.querySelector('.v-zh').textContent.trim(),py:li.querySelector('.v-py').textContent.trim(),tr:li.querySelector('.v-tr').textContent.trim()}))")
                check(f'{state} 單字數量', len(items) == len(vl) and page.evaluate("document.getElementById('vocab-count').textContent") == str(len(vl)), (len(items), len(vl)))
                if cfg['lang'] != 'zh':
                    check(f'{state} 每個單字有翻譯', all(i['tr'] for i in items), [i['zh'] for i in items if not i['tr']])
                if cfg['phon'] != 'off':
                    check(f'{state} 每個單字有拼音／注音', all(i['py'] for i in items), [i['zh'] for i in items if not i['py']])
                page.evaluate('Vocab.toggle(false)')
            # 錯誤紀錄
            if page.evaluate("!!document.getElementById('log-tab')&&!document.getElementById('log-tab').hidden"):
                page.evaluate('Log.toggle(true)'); page.evaluate('Log.toggle(false)')
        except Exception as e:
            check(f'{state} 檢查時發生錯誤', False, str(e)[:120])
    init = "try{localStorage.setItem('hanziGames.settings',JSON.stringify(%s))}catch(e){}" % json.dumps(dict(cfg, v=1, rate='normal'))
    smoke.PROBE = probe
    try:
        end, tr, score, errs, *_ = smoke.run(g, 'perfect', 1, init=init)[0]
    finally:
        smoke.PROBE = None
    check('玩完一局', end in ('leaderboard', 'embed-done'), end)
    check('網頁沒有錯誤', not errs, errs)
    warn = []
    if cfg_name == CONFIGS[0][0] and st['vocab']:
        by = {}   # 單字組 → 用到它的那幾關
        for stt in st['seen']: by.setdefault((st.get('vocab_of') or {}).get(stt) or stt, []).append(stt)
        for s, words in st['vocab'].items():
            if s not in by: continue
            seen = re.sub(r'\s+', '', ''.join(st['seen'][x] for x in by[s]))
            miss = [w[0] for w in words if re.sub(r'\s+', '', w[0]) not in seen]
            if miss: warn.append(f'{g} 的 {s}：{"、".join(miss)}')
    return st['n'], st['fails'], warn


def check_games(games, quick=False, verbose=True):
    """回傳 (檢查數, 失敗清單, 提醒清單)；給其他測試呼叫"""
    N, FAILS, WARN = 0, [], []
    for g in games:
        for name, cfg in (CONFIGS[:1] if quick else CONFIGS):
            n, f, w = run_one(g, name, cfg)
            N += n; FAILS += f; WARN += w
            for x in f: print(x, flush=True)
        if verbose: print(f'  [panels] {g}：{N} 項累計，失敗 {len(FAILS)}', flush=True)
    return N, FAILS, WARN


if __name__ == '__main__':
    a = sys.argv[1:]; quick = '--quick' in a; a = [x for x in a if x != '--quick']
    games = a or all_games()
    N, FAILS, WARN = check_games(games, quick)
    if WARN:
        print('\n提醒（不算失敗）：本關單字在這一局的這一關畫面上沒看到：')
        for w in WARN: print('  -', w)
    print(f'\n通過 {N - len(FAILS)} 項，失敗 {len(FAILS)} 項；提醒 {len(WARN)} 則')
    sys.exit(1 if FAILS else 0)
