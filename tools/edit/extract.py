import re, json, sys
CJK=re.compile(r'[一-鿿]')
def literals(src, base):
    """找出所有含中文的字串常值：('…' 或 `…`)，回傳 (start, end, quote, body)"""
    out=[]; i=0; n=len(src)
    while i<n:
        c=src[i]
        if c=='/' and src[i:i+2]=='//':
            j=src.find('\n',i); i=n if j<0 else j; continue
        if c=='/' and src[i:i+2]=='/*':
            j=src.find('*/',i); i=n if j<0 else j+2; continue
        if c in "'\"`":
            j=i+1; depth=0
            while j<n:
                if src[j]=='\\': j+=2; continue
                if c=='`' and src[j:j+2]=='${':
                    depth+=1; j+=2; continue
                if c=='`' and depth and src[j]=='}': depth-=1; j+=1; continue
                if src[j]==c and not depth: break
                j+=1
            body=src[i+1:j]
            if CJK.search(body): out.append((base+i, base+j+1, c, body))
            i=j+1; continue
        i+=1
    return out
NAMES={'N':'名字'}
def readable(body):
    k=[0]
    def f(m):
        e=m.group(1).strip()
        return '〔'+NAMES.get(e, e)+'〕'
    return re.sub(r'\$\{(.*?)\}', f, body)
def classify(src, start):
    before=src[max(0,start-40):start]
    if re.search(r'\bL\(\s*$', before): return 'line'
    if re.search(r'\bM\(\s*$', before): return '錯誤說明'
    if re.search(r'(good|goodFirst)\(\s*(\'[A-Z_0-9]+\',\s*)?$', before): return '綠卡說明'
    if re.search(r'\bask\(\s*$', before): return 'ask'
    line=src[src.rfind('\n',0,start)+1:start]
    if re.search(r'probs\.push\(\[\s*$', line): return 'line'
    if re.search(r"options:", line) or re.search(r'shuffle\(\[[^\]]*$', before) or re.search(r'o\.push\(\s*$', line) or re.match(r'\s*[?:] \[', line): return '選項'
    return '其他'
