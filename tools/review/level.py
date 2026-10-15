"""程度分析：把 9 個遊戲的中文（台詞、選項、扣分原因…）用 TOCFL 詞表（2023 版）分等級
用法：python3 tools/review/level.py <tocfl-202307.csv>"""
import csv, json, re, sys, collections
LV = {'L0': 'A1-', 'L1': 'A1', 'L2': 'A2', 'L3': 'B1', 'L4': 'B2', 'L5': 'C'}
ORDER = ['A1-', 'A1', 'A2', 'B1', 'B2', 'C']
D = {}
for r in csv.DictReader(open(sys.argv[1], encoding='utf8')):
    lv = LV[r['ID'][:2]]
    for w in re.split(r'[/／]', r['Traditional']):
        w = re.sub(r'[（(].*?[)）]|[0-9¹²³⁴]', '', w).strip()
        for v in {w, w.replace('…', '')} if '…' not in w else {w.split('…')[0]}:
            if v and (v not in D or ORDER.index(lv) < ORDER.index(D[v])): D[v] = lv
MAXL = max(map(len, D))
PART = set('喔嗯欸咦唷啦囉耶吼嘛哎喲哇唉呃啊呀吧呢嗎')
def seg(s):
    out, i = [], 0
    while i < len(s):
        for L in range(min(MAXL, len(s) - i), 0, -1):
            w = s[i:i + L]
            if w in D or L == 1: out.append(w); i += L; break
    return out
G = ['drinks', 'reserva', 'breakfast', 'parcel', 'nightmarket', 'bakery', 'clinic', 'mrt', 'street']
NAMES = '飲料店 訂位 早餐店 便利商店 夜市 麵包店 診所 捷運 街頭'.split()
res = {}
for g, nm in zip(G, NAMES):
    d = json.load(open(f'tools/review/out/{g}.json'))
    # 只看玩家在遊戲裡讀到的話：台詞、選項、扣分原因、稱讚（不含介面字：分數、翻譯、任務提示…）
    SPEECH = ('L', 'ask', 'say', 'sayK', 'desk', 'doc', 'staff', 'sc', 'M', 'Game.good', 'this.good', 'good', 'item', 'sentence')
    texts = [t['zh'] for t in d['triples'] if t['kind'] == 'call' and t['fn'] in SPEECH]
    texts += [z['text'] for z in d['zhOnly'] if re.search(r'[。？！，]$', z['text']) or len(z['text']) <= 12 and not re.search(r'分數|翻譯|朗讀|任務|錯誤|排行|紀錄|載入|再玩|開始', z['text'])]
    lines = [re.sub(r'〔.*?〕', '', t) for t in texts]
    tok = collections.Counter(); uniq = {}
    for s in lines:
        for run in re.findall(r'[㐀-鿿]+', s):
            for w in seg(run):
                if w in PART: continue          # 語氣詞（喔、嗯、欸…）不算
                lv = D.get(w, '表外'); tok[lv] += 1; uniq[w] = lv
    dial = [re.sub(r'〔.*?〕', '某', t['zh']) for t in d['triples'] if t['kind'] == 'call' and t['fn'] in ('L', 'ask', 'say', 'sayK', 'desk', 'doc', 'staff', 'sc')]
    lens = sorted(len(re.findall(r'[㐀-鿿]', re.sub(r'^[^：]{1,8}：', '', x))) for x in dial)
    n = sum(tok.values()); u = collections.Counter(uniq.values())
    hard = sorted([w for w, l in uniq.items() if l in ('B1', 'B2', 'C')], key=lambda w: (ORDER.index(uniq[w]), w))
    res[g] = dict(name=nm, tokens=n, uniq=len(uniq), pct={k: round(tok[k] / n * 100, 1) for k in ORDER + ['表外']},
                  upct={k: u[k] for k in ORDER + ['表外']}, avglen=round(sum(lens) / len(lens), 1), p90=lens[int(len(lens) * .9)], lines=len(lens),
                  hard=hard, outside=sorted(w for w, l in uniq.items() if l == '表外' and len(w) == 1)[:60])
json.dump(res, open('tools/review/out/level.json', 'w'), ensure_ascii=False, indent=1)
print(f"{'遊戲':<6}{'詞次':>6}{'不同詞':>6}  A1以下  A2   B1   B2+  表外  | 台詞平均字數 90%句長")
for g, r in res.items():
    p = r['pct']; a1 = p['A1-'] + p['A1']
    print(f"{r['name']:<6}{r['tokens']:>6}{r['uniq']:>6}  {a1:>5}% {p['A2']:>4}% {p['B1']:>4}% {p['B2']+p['C']:>4}% {p['表外']:>4}% | {r['avglen']:>5} {r['p90']:>4}")
