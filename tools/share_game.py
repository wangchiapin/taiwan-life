"""第 3 步：把一個遊戲改成使用 shared/game.js、shared/game.css。
用法：python3 tools/share_game.py <game> [--dry]
做法：遊戲裡的每一段共用程式，和共用檔裡的同一段比對（忽略註解和空白、遊戲名稱這類參數），
     完全一樣才刪掉；不一樣就停下來，把差在哪裡印出來（不會猜）。"""
import re, sys, json, pathlib, difflib
ROOT = pathlib.Path(__file__).resolve().parent.parent
SHARED_JS = (ROOT / 'shared/game.js').read_text(encoding='utf-8')

def strip_comments(t):
    t = re.sub(r'/\*.*?\*/', '', t, flags=re.S)
    t = re.sub(r"(?m)(?<![:'\"\w\\])//[^\n'\"`]*$", '', t)
    return t
def norm(t):
    return re.sub(r'\s+', ' ', strip_comments(t)).strip()

def unit_span(text, start_re, pos=0):
    """從 start_re 開始的宣告。第一行（去掉行尾註解）結尾是 { ( [ 的，找同樣縮排的結尾行（} 或 ) 開頭）；
    其他都是一行的。"""
    m = re.compile(start_re, re.M).search(text, pos)
    if not m: return None
    i = text.rfind('\n', 0, m.start()) + 1          # 這一行的開頭
    e = text.find('\n', m.start())
    line = text[i:e]
    indent = len(line) - len(line.lstrip(' '))
    first = re.sub(r'\s+//[^\'"`]*$', '', line).rstrip()
    if not first.endswith(('{', '(', '[')):
        return i, e + 1
    pad = ' ' * indent
    for mm in re.finditer(r'(?m)^' + pad + r'[}\])][^\n]*\n', text[e + 1:]):
        return i, e + 1 + mm.end()
    raise SystemExit('找不到結尾：' + start_re)

class Fail(Exception): pass

def back_comments(text, i):
    """往上連同緊貼著的說明註解一起刪（一行的 /* … */，不含段落標題）"""
    while True:
        j = text.rfind('\n', 0, i - 1) + 1
        line = text[j:i]
        if i > 0 and re.match(r'^\s*/\*(?!.*═).*\*/\s*\n$', line): i = j
        else: return i

def run(game, dry=False):
    path = ROOT / 'games' / game / 'index.html'
    html = path.read_text(encoding='utf-8')
    a = html.index('<script>\n/* ═'); b = html.index('</script>', a)
    js = html[a + len('<script>\n'):b]
    report = []

    # ── 參數 ──
    key = re.search(r"localStorage\.getItem\('(\w+_settings)'\)", js).group(1)
    trk = re.search(r"track\('game_start', \{ game: '(\w+)'", js).group(1)
    tm = re.search(r"getElementById\('timer-display'\)\.textContent = `(.*?)\$\{m\}", js).group(1)
    rm = re.search(r"\n  ROLE: (\{.*?\n?.*?\}),\n  speak", js, re.S)
    roles = rm.group(1)
    P = {'GAME.settingsKey': f"'{key}'", 'GAME.track': f"'{trk}'", 'GAME.scene': f"'{game}'"}
    def lit(t):   # 共用版 → 這個遊戲的寫法
        t = t.replace("`${GAME.timerPrefix ?? '⏱ '}${m}:${s}`", '`' + tm + '${m}:${s}`')
        for k, v in P.items(): t = t.replace(k, v)
        return t

    def shared_unit(start_re):
        sp = unit_span(SHARED_JS, start_re)
        if not sp: raise SystemExit('共用檔沒有：' + start_re)
        return SHARED_JS[sp[0]:sp[1]]

    removed = []
    def remove_unit(start_re, label, fix_game=lambda t: t, fix_shared=lambda t: t, required=True):
        nonlocal js
        sp = unit_span(js, start_re)
        if not sp:
            if required: raise Fail(f'{label}：遊戲裡找不到')
            return
        g = js[sp[0]:sp[1]]
        s = lit(shared_unit(start_re))
        if norm(fix_game(g)) != norm(fix_shared(s)):
            d = '\n'.join(difflib.unified_diff(norm(fix_shared(s)).split('; '), norm(fix_game(g)).split('; '), 'shared', game, lineterm='', n=1))
            raise Fail(f'{label} 不一樣：\n' + '\n'.join(d.split('\n')[:40]))
        js = js[:back_comments(js, sp[0])] + js[sp[1]:]
        removed.append(label)

    # 拼音、小工具
    for name in ['PY_OPT', 'isDigits']: remove_unit(rf'^const {name} = ', name)
    remove_unit(r'^function toPinyin\(', 'toPinyin')
    for name in ['CN', 'L', 'M', 'pick', 'shuffle', 'esc']: remove_unit(rf'^const {name} = ', name)
    remove_unit(r'^function track\(', 'track')
    # 網址參數、設定
    for name in ['QS', 'EMBED']: remove_unit(rf'^const {name} = ', name)
    remove_unit(r"^if \(EMBED && QS\.get\('name'\)\)", 'embed-boot')
    remove_unit(r'^const Settings = ', 'Settings')
    remove_unit(r'^try \{\n  const saved = JSON\.parse\(localStorage\.getItem', '讀設定')
    remove_unit(r'^\(\(\) => \{   // 從「重新開始」回來時', '網址設定')
    for name in ['X', 'Z', 'simpObserver', '_loginOrig']: remove_unit(rf'^const {name} = ', name)
    remove_unit(r'^let _t2s = ', '_t2s')
    for f in ['loadT2S', 'convertNode', 'applyLang', 'convertLogin', 'saveSettings']: remove_unit(rf'^function {f}\(', f)
    # 翻譯小視窗、音樂、朗讀、單字
    for name in ['Tr', 'SPK_ICON', 'TR_ICON', 'Music']: remove_unit(rf'^const {name} = ', name)
    remove_unit(r'^const Speech = ', 'Speech',
                fix_game=lambda t: re.sub(r"\n  ROLE: \{.*?\n?.*?\},\n  speak", "\n  get ROLE() { return GAME.roles || {}; },\n  speak", t, flags=re.S))
    remove_unit(r'^if \(Speech\.ok\)', 'pickVoice')
    remove_unit(r'^const spkBtn = ', 'spkBtn')
    remove_unit(r'^const Vocab = ', 'Vocab')
    remove_unit(r"^document\.getElementById\('vocab-tab'\)\.onclick", 'vocab-tab')
    remove_unit(r"^document\.getElementById\('vocab-close'\)\.onclick", 'vocab-close')
    # 錯誤紀錄
    remove_unit(r'^function stageOf\(', 'stageOf',
                fix_game=lambda t: t.replace('{ return STAGE[Game.state] || [Game.state, Game.state, Game.state]; }',
                                             '{ const s = STAGE[Game.state]; return s ? [s[0], s[1], s[2]] : [Game.state, Game.state, Game.state]; }'))
    remove_unit(r'^const Log = ', 'Log')
    remove_unit(r"^document\.getElementById\('log-tab'\)\.onclick", 'log-tab')
    remove_unit(r"^document\.getElementById\('log-close'\)\.onclick", 'log-close')
    # 登入（開始後多做的事 → Game.onStart）
    sp = unit_span(js, r'^function startGame\(')
    sg = js[sp[0]:sp[1]]
    extra = re.search(r"  document\.getElementById\('player-badge'\)\.textContent = '玩家：' \+ name;\n(.*?)  document\.getElementById\('login-screen'\)", sg, re.S).group(1)
    on_start = extra.strip()
    remove_unit(r'^function startGame\(', 'startGame',
                fix_game=lambda t: t.replace("'玩家：' + name;\n" + extra, "'玩家：' + name;\n  if (Game.onStart) Game.onStart();\n"))
    remove_unit(r"^document\.getElementById\('player-name-input'\)\.addEventListener\('keydown'", '名字 Enter')
    remove_unit(r"^document\.querySelectorAll\('\[data-script\]'\)\.forEach", '繁簡按鈕')
    remove_unit(r"^document\.querySelectorAll\('\[data-lang\]'\)\.forEach", '西英按鈕')
    remove_unit(r'^applyLang\(\);', 'applyLang()')
    remove_unit(r"^if \(Settings\.script === 'simp' && !_t2s\) loadT2S\(\)\.then\(applyLang\);", '預先載入簡體')
    remove_unit(r'^function restartGame\(', 'restartGame',
                fix_shared=lambda t: t.replace(" if (QS.get('code')) p.set('code', QS.get('code'));", '').replace("  if (GAME.restartParams) GAME.restartParams(p);\n", ''))
    remove_unit(r'^function finishEmbed\(', 'finishEmbed',
                fix_game=lambda t: t.replace('try { Tr.closeAll(); Speech.stop(); } catch (e) {}', 'Tr.closeAll(); Speech.stop();'))
    remove_unit(r'^function uploadResult\(', 'uploadResult')
    remove_unit(r'^async function showLeaderboard\(', 'showLeaderboard')

    # ── Game 物件：和 GameCore 一樣的功能刪掉 ──
    gi = js.index('\nconst Game = {') + 1
    ge = unit_span(js, r'^const Game = \{', gi)[1]
    body = js[gi:ge]
    core_src = SHARED_JS[SHARED_JS.index('const GameCore = {'):]
    core_names = re.findall(r'(?m)^  (?:get )?(\w+)\s*[\(:]', core_src[:core_src.index('\n};')])
    kept = []
    for n in core_names:
        pat = rf'^  (?:get )?{n}\s*[\(:]'
        sp = unit_span(body, pat)
        if not sp: continue
        g = body[sp[0]:sp[1]]
        s = lit(unit_span(core_src, pat) and core_src[slice(*unit_span(core_src, pat))])
        # 舊版 imageMissing（沒有輪流圖的遊戲）：和共用版效果一樣
        OLD_IMG = norm('''  imageMissing() {
    const img = document.getElementById('npc-avatar'), ph = document.getElementById('scene-placeholder');
    if (img.getAttribute('src')) this.missing.add(img.getAttribute('src'));
    img.style.display = 'none'; ph.style.display = 'grid';
  },''')
        if norm(g).rstrip(',') == norm(s).rstrip(',') or (n == 'imageMissing' and norm(g).rstrip(',') == OLD_IMG.rstrip(',') and '_anim' not in js):
            body = body[:back_comments(body, sp[0])] + body[sp[1]:]; removed.append('Game.' + n)
        else:
            kept.append(n)
    if on_start:
        body = body.replace('\n  get N()', '\n  /* 按開始後、換到遊戲畫面前（shared/game.js 的 startGame 會呼叫） */\n  onStart() {\n    '
                            + on_start.replace('Game.', 'this.').replace('\n', '\n  ') + '\n  },\n\n  get N()', 1) if '\n  get N()' in body else body
        if 'onStart()' not in body: raise Fail('onStart 放不進去')
    body = body.replace('const Game = {', 'const Game = defineGame({', 1)
    body = re.sub(r'\n\};\n$', '\n});\n', body)
    if not body.endswith('});\n'): raise Fail('Game 結尾不對：' + body[-30:])
    js = js[:gi] + body + js[ge:]

    # ── 最後的「重新開始」→ GameBoot() ──
    boot = re.search(r"/\* 從「重新開始」回來：直接用原本的名字開新的一局 \*/\n\(\(\) => \{\n  const again = .*?\n\}\)\(\);\n", js, re.S)
    if not boot: raise Fail('找不到最後的重新開始區塊')
    exp = "(() => { const again = EMBED ? QS.get('name') : QS.get('again'); if (!again) return; if (!EMBED) history.replaceState(null, '', location.pathname); document.getElementById('player-name-input').value = again; startGame(); })();"
    if norm(boot.group(0)) != exp: raise Fail('重新開始區塊不一樣')
    js = js.replace(boot.group(0), '/* 從「重新開始」或清單頁回來：直接用原本的名字開新的一局 */\nGameBoot();\n')

    # ── 清掉只剩標題的段落 ──
    js = re.sub(r'(?m)^/\* ═+\n(?:   .*\n)+═+ \*/\n(?:\s*\n)*(?=/\* ═|\Z)', '', js)
    js = re.sub(r'\n{3,}', '\n\n', js)

    cfg = (f"<script>\n/* 這個遊戲的設定（共用程式在 shared/game.js） */\nconst GAME = {{\n  scene: '{game}', track: '{trk}', settingsKey: '{key}',"
           + (f" timerPrefix: '{tm}'," if tm != '⏱ ' else '')
           + f"\n  roles: {roles}\n}};\n</script>\n<script src=\"../../shared/game.js\"></script>\n")
    html = html[:a] + cfg + '<script>\n' + js + html[b:]
    print(game, '刪掉', len(removed), '段；Game 保留自己的版本：', kept or '無', '；onStart：', on_start or '無')
    if not dry: path.write_text(html, encoding='utf-8')
    return removed, kept

def share_css(game, dry=False):
    """把和 shared/game.css 完全一樣的規則從遊戲的 <style> 刪掉，並在前面載入 game.css"""
    sys.path.insert(0, str(ROOT / 'tools'))
    from css_rules import split_rules, norm as cnorm
    shared = {cnorm(t) for k, t in split_rules((ROOT / 'shared/game.css').read_text(encoding='utf-8')) if k == 'rule'}
    path = ROOT / 'games' / game / 'index.html'
    html = path.read_text(encoding='utf-8')
    if 'shared/game.css' in html: print(game, 'CSS 已經處理過'); return
    a = html.index('<style>') + len('<style>'); b = html.index('</style>', a)
    items = split_rules(html[a:b])
    keep, n = [], 0
    for idx, (k, t) in enumerate(items):
        if k == 'rule' and cnorm(t) in shared: n += 1; continue
        # 註解：後面緊接的規則全部被刪掉（直到下一個註解）就一起刪
        if k == 'comment':
            nxt = []
            for k2, t2 in items[idx + 1:]:
                if k2 == 'comment': break
                nxt.append(cnorm(t2) in shared)
            if nxt and all(nxt): continue
        keep.append(t)
    if n != len(shared): raise Fail(f'CSS：共用 {len(shared)} 條，這個遊戲只找到 {n} 條')
    css = '\n  ' + '\n  '.join(keep) + '\n'
    html = html[:a - len('<style>')] + '<link rel="stylesheet" href="../../shared/game.css">\n<style>' + css + html[b:]
    print(game, 'CSS 刪掉', n, '條共用規則，保留', sum(1 for t in keep if not t.startswith('/*')), '條')
    if not dry: path.write_text(html, encoding='utf-8')

if __name__ == '__main__':
    try:
        if '--css' not in sys.argv: run(sys.argv[1], '--dry' in sys.argv)
        share_css(sys.argv[1], '--dry' in sys.argv)
    except Fail as e: print('停下來 ✋', e); sys.exit(1)
