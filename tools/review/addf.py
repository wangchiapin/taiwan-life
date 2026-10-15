"""把檢查結果加進 tools/review/out/findings.jsonl：python3 tools/review/addf.py < 一行一筆的 JSON"""
import sys, json
with open('tools/review/out/findings.jsonl', 'a') as f:
    for line in sys.stdin:
        line = line.strip()
        if line: json.loads(line); f.write(line + '\n')
