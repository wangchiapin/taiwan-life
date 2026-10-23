"""單字抽屜對齊：把畫面上沒有的詞拿掉、放錯關卡的詞搬過去（只動 VOCAB，不動台詞）。"""
import os, re, sys
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games')
def load(g): return open(f'{ROOT}/{g}/index.html',encoding='utf-8').read()
def save(g,s): open(f'{ROOT}/{g}/index.html','w',encoding='utf-8').write(s)
def skip_str(s,i):
    q=s[i]; i+=1
    while s[i]!=q:
        i+= 2 if s[i]=='\\' else 1
    return i+1
def span(s,start):
    """從 start（'['）找到配對的 ']' 之後的位置"""
    assert s[start]=='['
    d=0;i=start
    while True:
        c=s[i]
        if c in '\'"`': i=skip_str(s,i); continue
        if c=='[': d+=1
        elif c==']':
            d-=1
            if d==0: return i+1
        i+=1
def entries(s,a,b):
    out=[];i=a+1
    while i<b-1:
        if s[i]=='[':
            j=span(s,i); out.append(s[i:j]); i=j
        else: i+=1
    return out
def find(s,state):
    m=list(re.finditer(r'^  %s: \[\['%re.escape(state),s,re.M))
    if len(m)!=1: print('找不到或不只一個：',state,len(m)); sys.exit(1)
    a=m[0].end()-2; return m[0].start(), a, span(s,a)
def word(e): return re.match(r"\[\s*'([^']*)'",e).group(1)
class G:
    def __init__(s,g): s.g=g; s.s=load(g)
    def ents(s,st):
        _,a,b=find(s.s,st); return entries(s.s,a,b)
    def put(s,st,es):
        ms,a,b=find(s.s,st); s.s=s.s[:a]+'['+', '.join(es)+']'+s.s[b:]
    def take(s,st,w):
        es=s.ents(st); hit=[e for e in es if word(e)==w]
        if len(hit)!=1: print('詞不對',s.g,st,w,len(hit)); sys.exit(1)
        s.put(st,[e for e in es if e is not hit[0]]); return hit[0]
    def give(s,st,e,after=None):
        es=s.ents(st)
        if any(word(x)==word(e) for x in es): return
        es.append(e); s.put(st,es)
    def rm(s,st,*ws):
        for w in ws: s.take(st,w)
    def mv(s,src,w,dst): s.give(dst,s.take(src,w))
    def done(s): save(s.g,s.s)
# ── barber ──
g=G('barber')
g.rm('START','剪髮'); g.mv('START','理髮店','BOOK_OPEN')
g.mv('BOOK_OPEN','設計師','ARRIVE'); g.rm('ARRIVE','姓名'); g.mv('BOOK_PHONE','請問','ARRIVE'); g.rm('BOOK_PHONE','確認')
g.rm('STYLE_BANG','眉毛'); g.rm('MIRROR','滿意'); g.mv('END','剪好','MIRROR'); g.rm('CHANGE','數'); g.done()
# ── 單純刪除 ──
for gm,st,ws in [('bookstore','FIND',['作者']),('icecream','END',['好吃']),('icecream','EAT',['融化']),('market','BAG',['自己的']),
                 ('cinema','SEATS',['前面']),('bakery','C_SLICE',['一條']),('reserva','C1_NAME',['我姓…']),
                 ('nightmarket','A_QTY',['划算']),('parcel','BAG',['塑膠袋']),('parcel','CARD_AMT',['順便']),('parcel','Y_ASK',['預計'])]:
    g=G(gm); g.rm(st,*ws); g.done()
# ── bus ──
g=G('bus')
g.mv('START','往…方向','HAIL'); g.rm('START','刷卡'); g.rm('HAIL','公車來了'); g.mv('END','終於','WAIT')
g.rm('TAP_ON','車門'); g.rm('TAP_OFF','叮咚'); g.done()
# ── parking ──
g=G('parking')
g.rm('REMEMBER','傳'); g.rm('FIND_CAR','找到'); g.mv('EXIT','出場','PAY'); g.mv('EXIT','十五分鐘','PAY'); g.rm('PAY','一共'); g.done()
# ── ubike ──
g=G('ubike')
g.mv('LIGHT','斑馬線','ROAD'); g.mv('RETURN_FIND','快到了','LIGHT'); g.done()
# ── parcel：共用的確認詞寫法對齊畫面 ──
g=G('parcel'); old="['已經付過款', 'ya está pagado', 'already paid']"
assert g.s.count(old)==1; g.s=g.s.replace(old,"['已經付過', 'ya está pagado', 'already paid']"); g.done()
# ── drinks：第一杯、第二杯各用自己的抽屜 ──
g=G('drinks'); es=g.ents('TYPE')
byw={word(e):e for e in es}
t1=[byw[w] for w in ['歡迎光臨','想喝','奶茶','紅茶','綠茶','烏龍茶']]
t2=[byw[w] for w in ['還要','奶茶','紅茶','綠茶','烏龍茶']]
ms,a,b=find(g.s,'TYPE')
g.s=g.s[:ms]+"  TYPE_1: ["+', '.join(t1)+"],\n  TYPE_2: ["+', '.join(t2)+"]"+g.s[b:]
old="TYPE_1: 'TYPE', TYPE_2: 'TYPE', "
assert g.s.count(old)==1; g.s=g.s.replace(old,''); g.done()
print('OK')
