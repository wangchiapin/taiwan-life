import json, sys
g = sys.argv[1]; part = sys.argv[2] if len(sys.argv) > 2 else 'triples'
d = json.load(open(f'tools/review/out/{g}.json'))
if part == 'triples':
    for t in d['triples']:
        if t['kind'] == 'vocab': continue
        print(f"{t['line']}|{t['fn']}| {t['zh']} ‖ {t['es']} ‖ {t['en']}")
elif part == 'vocab':
    for v in d['vocab']: print(f"{v['line']} {v['key']}: {v['zh']} | {v['es']} | {v['en']}")
    for h in d['html']:
        if h['es'] or h['en']: print('html:', h['zh'], '|', h['es'], '|', h['en'])
