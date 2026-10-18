# 新的十個遊戲（school ubike bus barber cinema parking icecream bookstore market elevator）的台詞抽出工具
# 用法：python3 rows_new.py <game>  → site/rows/<game>.json 和 priv/priv_<game>.json
# 規則和 rows2.py 一樣：只抽「台詞、旁白、選項、錯誤說明、綠卡說明、過場按鈕、位置名稱、提示」
import re, json, sys, html, os
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
exec(open('extract.py').read())
TITLES = {'school': '學校請假', 'ubike': 'YouBike', 'bus': '搭公車', 'barber': '理髮店', 'cinema': '電影院', 'parking': '停車場',
          'icecream': '冰淇淋店', 'bookstore': '書店', 'market': '菜市場', 'elevator': '搭電梯'}
# 〔佔位〕的中文名稱：照程式裡的變數名稱猜；猜不到就直接放變數名稱
NAMEMAP = [('dest', '目的地'), ('route[1]', '路線（中文）'), ('route[0]', '路線號碼'), ('t.dir', '方向'), ('t.other', '另一邊的方向'),
 ('want', '預約的時間'), ('phone', '電話'), ('price', '價錢'), ('given', '店員找的錢'), ('change', '應該找的錢'), ('HZ(', '金額（中文）'),
 ('len[0]', '剪到哪裡'), ('len[1]', '剪到哪裡（西文）'), ('bang[0]', '瀏海怎麼剪'), ('hr', '幾點'), ('stops[', '站名'), ('NZ(', '站數（中文）'), ('n}', '數字'),
 ('borrow', '借車站'), ('ret.', '還車站'), ('name', '名字'), ('leave', '請假原因'), ('reason', '請假原因'), ('time', '時間'), ('date', '日期'), ('who', '人名'),
 ('total', '總價'), ('book', '書名'), ('sec', '書區'), ('flavor', '口味'), ('top', '配料'), ('vessel', '容器'), ('item', '品項'), ('floor', '樓'), ('zone', '區'),
 ('fee', '停車費'), ('rate', '每小時多少錢'), ('movie', '電影'), ('seat', '座位'), ('hall', '廳'), ('n', '數字')]
def nm(e):
    e = e.strip()
    if e == 'N': return '名字'
    cj = re.findall(r"'([^']*[一-鿿][^']*)'", e)
    if len(cj) >= 2 and '?' in e: return cj[0] + '／' + cj[1]
    if cj: return '有時加：' + cj[0]
    if g + ':' + e in LABELS: return LABELS[g + ':' + e]
    for k, v in NAMEMAP:
        if k in e: return v
    return e
def readable_n(body):
    ph = []; out = ''; i = 0
    while i < len(body):
        if body.startswith('${', i):
            j = i + 2; d = 1
            while j < len(body) and d:
                if body[j] == '{': d += 1
                elif body[j] == '}': d -= 1
                j += 1
            e = body[i + 2:j - 1]; lab = nm(e); ph.append((lab, e)); out += '〔' + lab + '〕'; i = j
        else: out += body[i]; i += 1
    return out, ph
LABELS = json.load(open('labels_new.json', encoding='utf8')) if os.path.exists('labels_new.json') else {}
g = sys.argv[1]
s = open(f'../../games/{g}/index.html', encoding='utf8').read()
spk = re.search(r'const SPEAKER_RE = /\^\((.*?)\)：/', s).group(1)
SPK = re.compile(r'^(' + spk + r')：')
# 說話小幫手：const sd = (zh, es, en) => L(`設計師：${zh}`, …
HELP = {m.group(1): m.group(2) for m in re.finditer(r"const (\w+) = \(zh, es, en\) => L\(`([^：`$]+)：\$\{zh\}`", s)}
rows = []; priv = {}
def add(kind, state, who, zh, raw, pos, ph=None):
    rid = f'{g}-{len(rows)+1:03d}'
    rows.append({'id': rid, 'kind': kind, 'stage': state, 'stageName': state or '（共用說明）', 'who': who, 'zh': zh}); priv[rid] = {'raw': raw, 'pos': pos, 'ph': ph or []}
lg0 = s.index('<!-- ── 登入 ── -->'); lg = s[lg0:s.index('<!-- ── 遊戲 ── -->')]
for m in re.finditer(r'>([^<>]*[一-鿿][^<>]*)<', lg):
    t = m.group(1).strip()
    if not t or t in ('開始遊戲', '繁體', '简体') or '你的名字' in t or t.startswith('例：'): continue
    add('開頭介紹', '開始畫面', '', html.unescape(t), m.group(1), lg0 + m.start(1))
gi = s.index('  getConfig() {')
def region(a_, b_, dk):
    a = s.index(a_); b = s.index(b_, a); return (a, b, dk)
nl = s.index('const NEXT_LABEL'); regs = [(nl, s.index('\n};', nl), '過場按鈕'), region('const Hints = {', '\n};\n', '任務提示')]
st0 = s.index('  setPlace('); regs.append((st0, s.index('\n  },\n', st0), '位置名稱'))
# Game 裡其他放台詞的函式（amiLines、driverLine…）和 getConfig
gm = s.index('const Game = defineGame({')
for m in re.finditer(r'\n  (amiLines|\w*Lines)\(\) \{', s[gm:gi]):
    a = gm + m.start(); regs.append((a, s.index('\n  },\n', a), 'fn:' + m.group(1)))
cfg_end = s.index('\n  },\n', gi + 20)
# getConfig 的結尾：下一個頂層方法開始前；找「\n  },\n」之後的第一個非 getConfig 內容
ge = s.find('\n  /* ──', gi + 20)
regs.append((gi, ge if ge > 0 else len(s), 'cfg'))
for a, b, dk in regs:
    for stt, en, q, body in literals(s[a:b], a):
        before = s[max(0, stt - 80):stt]; line_ = s[s.rfind('\n', 0, stt) + 1:s.find('\n', stt)]
        if dk == 'cfg':
            sm = re.findall(r'\n      ([A-Z][A-Z_0-9]*): \{', s[gi:stt]); state = sm[-1] if sm else ''
        elif dk.startswith('fn:'): state = {'amiLines': 'Ami 的 LINE 訊息', 'driverLine': '司機說的話'}.get(dk[3:], dk[3:])
        else: state = {'過場按鈕': '過場按鈕', '位置名稱': '位置列', '任務提示': '提示'}[dk]
        kind = classify(s, stt)
        if re.search(r'addMistake\(\s*$', before): kind = '錯誤說明'
        isSay = False
        hm = re.search(r'\b(' + '|'.join(HELP) + r')\(\s*$', before) if HELP else None
        if hm and kind == '其他': kind = 'line'; isSay = HELP[hm.group(1)]
        if kind == '其他' and re.search(r'[?:] *$', before):
            if re.search(r'\bM\(', line_): kind = '錯誤說明'
            elif re.search(r'\bL\(', line_): kind = 'line'
        if dk == 'cfg' and kind == '其他':
            pv = s[gi:stt]
            if pv.rfind('options:') > max(pv.rfind('next:'), pv.rfind('dialogue:')): kind = '選項'
        if dk == '過場按鈕': kind = '過場按鈕'
        if dk == '位置名稱': kind = '位置名稱'
        if dk == '任務提示':
            m = re.match(r'<div class="h-sec">\$\{r\(\'(.*?)\'\)\}</div>$', body)
            if m: add('任務提示（標題）', '提示', '', m.group(1), body, stt); continue
            if not re.search(r'item\(\s*$', before): continue
            kind = '任務提示'
        if state == 'RESULT': continue
        zh, ph = readable_n(body); who = ''
        if kind == '錯誤說明' and re.search(r'[A-Za-z]{3}', zh): zh = re.split(r'(?<=[。！？」])\s*[«"A-Z¡¿]', zh)[0]
        if kind in ('line', '台詞'):
            m = SPK.match(zh)
            if m: who = m.group(1).strip('（）'); zh = zh[len(m.group(0)):]; kind = '台詞'
            elif isSay: who = isSay; kind = '台詞'
            else: kind = '旁白' if zh.startswith('（') else '台詞'
        if zh in ('〔zh〕', '〔變數〕'): continue
        if kind == '其他' or zh.startswith(('查看結果', '回到地圖', '查看排行榜')): continue
        if re.search(r'<(button|div|span|i|b)[ >]', zh) or zh.strip() in ('朗讀', '〔變數〕', '我'): continue
        add(kind, state, who, zh, body, stt, ph)
os.makedirs('site/rows', exist_ok=True); os.makedirs('priv', exist_ok=True)
json.dump({'game': g, 'title': TITLES[g], 'rows': rows}, open(f'site/rows/{g}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
json.dump(priv, open(f'priv/priv_{g}.json', 'w', encoding='utf8'), ensure_ascii=False)
from collections import Counter
print(g, len(rows), dict(Counter(r['kind'] for r in rows)))
