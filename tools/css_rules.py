"""把 <style> 拆成一條一條的規則（@media 整塊算一條），給 share_css 用"""
import re
def split_rules(css):
    out = []; i = 0; n = len(css)
    while i < n:
        while i < n and css[i] in ' \t\n': i += 1
        if i >= n: break
        if css.startswith('/*', i):
            j = css.index('*/', i) + 2; out.append(('comment', css[i:j])); i = j; continue
        j = css.index('{', i); depth = 0; k = j
        while True:
            if css[k] == '{': depth += 1
            elif css[k] == '}':
                depth -= 1
                if depth == 0: break
            k += 1
        out.append(('rule', css[i:k + 1])); i = k + 1
    return out
def norm(r): return re.sub(r'\s+', ' ', re.sub(r'/\*.*?\*/', '', r, flags=re.S)).strip()
