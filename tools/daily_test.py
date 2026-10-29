"""每日排程測試：台灣生存日記 24 個遊戲，從 2026-11-01 起每天 3 個，8 天一輪。
用法：python3 tools/daily_test.py [--date YYYY-MM-DD] [--games a b c] [--out 檔名.csv] [--max 25] [--min 10]
每個遊戲：smoke perfect 2 場（要上排行榜、100 分、無錯誤、上傳成功）＋ coverage（選項配對／玩家路線）。
通過的遊戲也各寫一列。輸出 CSV 欄位：日期,遊戲,測試方式,結果,通過項數,失敗項數,說明
"""
import sys, os, csv, datetime, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
def load(name, fn):
    s = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(s); sys.modules[name] = m; s.loader.exec_module(m); return m
smoke = load('tl_smoke', 'smoke.py')
cov = load('tl_coverage', 'coverage.py')  # 不能叫 coverage（會撞 PyPI 套件）

START = datetime.date(2026, 11, 1)
GAMES = sorted(d for d in os.listdir(os.path.join(os.path.dirname(HERE), 'games')) if os.path.exists(os.path.join(os.path.dirname(HERE), 'games', d, 'index.html')))
PER_DAY = 3

def todays(date):
    n = (date - START).days
    if n < 0: return []
    return [GAMES[(n * PER_DAY + i) % len(GAMES)] for i in range(PER_DAY)]

def test_smoke(g):
    try:
        res = smoke.run(g, 'perfect', 2)
    except Exception as e:
        return ['smoke', '失敗', 0, 1, f'測試程式例外 {str(e)[:150]}']
    ok = 0; bad = []
    for i, (end, tr, score, errs, log, fb) in enumerate(res, 1):
        probs = []
        if end != 'leaderboard': probs.append(f'結束於 {end}')
        if score != 100: probs.append(f'分數 {score}')
        if errs: probs.append(f'網頁錯誤 {errs[0][:80]}')
        if not str(fb).startswith('FB✓'): probs.append(f'上傳 {fb}')
        if probs: bad.append(f'第{i}場：' + '、'.join(probs))
        else: ok += 1
    note = '2 場全過，100 分，上傳成功' if not bad else '；'.join(bad)
    if bad and any('分數' in b for b in bad): note += '（可能是正解過期：題目改了但 tools/oracles 沒跟上）'
    return ['完整通關(perfect)×2', '通過' if not bad else '失敗', ok, len(bad), note]

def test_cov(g, mx, mn, out):
    try:
        r = cov.run_game(g, mx, mn, out)
    except Exception as e:
        return ['覆蓋測試(選項配對+玩家路線)', '失敗', 0, 1, f'測試程式例外 {str(e)[:150]}']
    bad = r['bad_runs']; ok = r['runs'] - bad
    note = (f"{r['runs']} 場；單項覆蓋 {r['got_single']}/{r['total_single']}，配對覆蓋 {r['got_pairs']}/{r['total_pairs']}，"
            f"狀態走訪 {r['visited']}/{r['states']}")
    if r['problems']: note += '；問題：' + ' | '.join(r['problems'][:3])
    return ['覆蓋測試(選項配對+玩家路線)', '通過' if not r['problems'] else '失敗', ok, bad, note]

if __name__ == '__main__':
    a = sys.argv[1:]
    def opt(name, d):
        if name in a: i = a.index(name); v = a[i + 1]; del a[i:i + 2]; return type(d)(v)
        return d
    date = datetime.date.fromisoformat(opt('--date', (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).date().isoformat()))
    out = opt('--out', f'taiwan-life-{date}.csv'); mx = opt('--max', 25); mn = opt('--min', 10)
    games = a[a.index('--games') + 1:] if '--games' in a else todays(date)
    rows = []
    for g in games:
        for r in (test_smoke(g), test_cov(g, mx, mn, '/tmp/cov-' + str(date))):
            rows.append([str(date), 'taiwan-life/' + g] + r)
            print(rows[-1], flush=True)
    with open(out, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f); w.writerow(['日期', '遊戲', '測試方式', '結果', '通過項數', '失敗項數', '說明']); w.writerows(rows)
    print('寫入', out)
