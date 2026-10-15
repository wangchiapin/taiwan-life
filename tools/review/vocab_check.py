"""單字表檢查：每個 VOCAB 的詞，有沒有出現在那一關（或整個遊戲）的中文裡"""
import json, re, sys
G = ['drinks','reserva','breakfast','parcel','nightmarket','bakery','clinic','mrt','street']
out = {}
for g in G:
    d = json.load(open(f'tools/review/out/{g}.json'))
    html = open(f'games/{g}/index.html', encoding='utf8').read().split('\n')
    texts = [(t['line'], t['zh']) for t in d['triples'] if t['kind'] != 'vocab'] + [(z['line'], z['text']) for z in d['zhOnly']]
    alltext = '\n'.join(t for _, t in texts) + '\n'.join(h['zh'] for h in d['html'])
    # 關卡在 getConfig 裡的行數範圍
    gi = next(i for i, l in enumerate(html) if 'getConfig()' in l and '{' in l and l.startswith('  getConfig'))
    starts = [(i + 1, m.group(1)) for i, l in enumerate(html) if i > gi and (m := re.match(r'^      ([A-Z][A-Z0-9_]*): \{', l))]
    # VOCAB_OF：關卡 → 單字表的 key
    vo = {}
    m = re.search(r'const VOCAB_OF = \{(.*?)\};', open(f'games/{g}/index.html', encoding='utf8').read(), re.S)
    if m:
        for k, v in re.findall(r"(\w+): '(\w+)'", m.group(1)): vo.setdefault(v, []).append(k)
    def state_text(key):
        names = set(vo.get(key, [])) | {key}
        rng = []
        for idx, (ln, nm) in enumerate(starts):
            if nm in names or any(nm.startswith(n + '_') for n in names):
                end = starts[idx + 1][0] if idx + 1 < len(starts) else ln + 400
                rng.append((ln, end))
        return '\n'.join(t for ln, t in texts if any(a <= ln < b for a, b in rng)), bool(rng)
    res = []
    for v in d['vocab']:
        parts = [p for p in re.split(r'…+|\.\.\.', v['zh']) if p]
        anywhere = all(p in alltext for p in parts)
        st, found = state_text(v['key'])
        here = all(p in st for p in parts) if found else None
        if not anywhere or here is False:
            res.append({**v, 'anywhere': anywhere, 'inState': here})
    out[g] = res
    print(g, '單字', len(d['vocab']), '｜整個遊戲都沒出現', sum(1 for r in res if not r['anywhere']), '｜那一關沒出現', sum(1 for r in res if r['anywhere'] and r['inState'] is False))
json.dump(out, open('tools/review/out/vocab_issues.json', 'w'), ensure_ascii=False, indent=1)
