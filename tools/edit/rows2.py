import re, json, sys, html
import os
HERE=os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
exec(open('extract.py').read())
CONF={
 'reserva': dict(title='打電話訂位', regions=[('const NEXT_LABEL','const Game = {','過場按鈕'),('  setCall(','  /* ── 圖片','位置名稱'),
    ('  /* ── 店員複述','  /* ── 狀態設定','台詞'),('  getConfig() {','  /* ── 換關卡','cfg'),('const Hints = {','\n};\n','任務提示')],
    speakers='Ami|店員|我|（一個不認識的人）', extra={'START':'開場：Ami 請你訂位','END':'結局','MID_AMI':'Ami 回電','CALL_AMI':'打電話問 Ami','WRONG_NUMBER':'打錯電話','DELIVERY_LINE':'打到外送專線','C2_BYE':'第二通：結束'}),
'breakfast': dict(title='早餐店打工', stagevar='const STAGE_BASE = {', regions=[('const NEXT_LABEL','const Game = {','過場按鈕'),
    ('  /* ── 每局隨機任務','  /* ── 計時','setup'),('  getConfig() {','  /* ── 換關卡','cfg'),('const Hints = {','\n};\n','任務提示')],
    speakers='陳姐|我|李先生|王伯伯|張太太|小朋友|林小姐', extra={'START':'開場：陳姐交代','END':'陳姐回來','PHONE':'電話訂餐'},
    guess=[('=n','金額'),('=d','金額'),('sales','金額'),('dine','內用/外帶'),('u.say','老樣子內容'),('usual.say','老樣子內容'),('usual','老樣子內容'),('m1','餐點'),('momMain','餐點'),('kidNew','餐點'),('d1','飲料'),('momDrink','飲料'),('kidDrink','飲料'),('add4','飲料'),('drink','飲料'),('tail','電話末三碼'),('total','金額'),('bill','金額'),('change','金額'),('who','客人'),('w[','客人'),('food','餐點')]),
}
def guess(e):
    e=e.strip()
    if e=='N': return '名字'
    cj=re.findall(r"'([^']*[一-鿿][^']*)'", e)
    if cj: return '有時加：'+cj[0]
    for k,v in C.get('guess',[]):
        if (k[1:]==e if k.startswith('=') else k in e): return v
    for k,v in [('phone','電話'),('Phone','電話'),('date','日期'),('Date','日期'),('time','時間'),('Time','時間'),('.T','時間'),('people','人數'),('adults','大人人數'),('kids','小孩人數'),('chairs','兒童椅張數'),('day','星期幾'),('Line','電話號碼'),('name','名字'),('seat','座位'),('ask2','時間'),('alt2','時間'),('t1','時間')]:
        if k in e: return v
    return '變數'
def readable2(body): return re.sub(r'\$\{(.*?)\}', lambda m:'〔'+guess(m.group(1))+'〕', body)
g=sys.argv[1]; C=CONF[g]
s=open(f'../../games/{g}/index.html',encoding='utf8').read()
SV=C.get('stagevar','const STAGE = {'); st=s[s.index(SV):s.index('};',s.index(SV))]
ST=dict(re.findall(r"([A-Z_0-9]+): \['(.*?)'",st)); ST.update(C['extra'])
rows=[]; priv={}
def add(kind,state,who,zh,raw,pos):
    rid=f'{g}-{len(rows)+1:03d}'
    rows.append({'id':rid,'kind':kind,'stage':state,'stageName':ST.get(state,state),'who':who,'zh':zh}); priv[rid]={'raw':raw,'pos':pos}
lg0=s.index('<!-- ── 登入 ── -->'); lg=s[lg0:s.index('<!-- ── 遊戲 ── -->')]
for m in re.finditer(r'>([^<>]*[一-鿿][^<>]*)<', lg):
    t=m.group(1).strip()
    if not t or t in ('開始遊戲','繁體','简体') or '你的名字' in t or t.startswith('例：'): continue
    add('開頭介紹','開始畫面','',html.unescape(t),m.group(1),lg0+m.start(1))
SPK=re.compile(r'^('+C['speakers']+')：')
gi=s.index('  getConfig() {')
for a_,b_,dk in C['regions']:
    a=s.index(a_); b=s.index(b_,a)
    for stt,en,q,body in literals(s[a:b],a):
        before=s[max(0,stt-60):stt]
        if dk=='cfg':
            sm=re.findall(r'\n      ([A-Z][A-Z_0-9]*): \{', s[gi:stt]); state=sm[-1] if sm else ''
        elif dk=='setup':
            wm=re.findall(r"who: '(.+?)'", s[a:stt]); state='客人：'+wm[-1] if wm else '王伯伯的老樣子'
        else: state={'過場按鈕':'過場按鈕','位置名稱':'位置列','任務提示':'提示','台詞':'CONFIRM'}[dk]
        kind=classify(s,stt)
        if re.search(r'addMistake\(\s*$',before): kind='錯誤說明'
        if dk=='過場按鈕': kind='過場按鈕'
        if dk=='位置名稱': kind='位置名稱'
        if dk=='任務提示':
            m=re.match(r'<div class="h-sec">\$\{r\(\'(.*?)\'\)\}</div>$', body)
            if m: add('任務提示（標題）','提示','',m.group(1),body,stt); continue
            if not re.search(r'item\(\s*$',before): continue
            kind='任務提示'
        if state=='RESULT': continue
        zh=readable2(body); who=''
        if kind=='錯誤說明' and re.search(r'[A-Za-z]{3}',zh):
            zh=re.split(r'(?<=[。！？」])\s*[«"A-Z¡¿]',zh)[0]
        if kind in ('line','台詞'):
            m=SPK.match(zh)
            if m: who=m.group(1).strip('（）'); zh=zh[len(m.group(0)):]; kind='台詞'
            elif zh.startswith('〔客人〕：'): who='客人'; zh=zh[5:]; kind='台詞'
            else: kind='旁白' if zh.startswith('（') else '台詞'
        line=s[s.rfind('\n',0,stt)+1:s.find('\n',stt)]
        if dk=='setup' and kind=='其他' and re.search(r'say: *$',before): kind='台詞'
        if kind=='其他' or zh.startswith(('查看結果','回到地圖','查看排行榜')): continue
        if re.search(r'(===|!==|==) *$', before): continue
        if kind=='選項' and zh=='晚上': zh='晚上〔時間〕'
        if 'probs.push' in line: who='Ami'
        if dk=='setup' and state=='王伯伯的老樣子' and who: state='客人：'+who
        if dk=='setup' and state=='王伯伯的老樣子': kind='老樣子說法'
        dup=[r for r in rows if r['zh']==zh and r['stage']==state and r['kind']==kind]
        if dup: priv[dup[0]['id']].setdefault('also',[]).append(stt); continue
        if kind=='選項': who='我'
        add(kind,state,who,zh,body,stt)
json.dump({'game':g,'title':C['title'],'rows':rows},open(f'site/rows/{g}.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
json.dump(priv,open(f'priv/priv_{g}.json','w',encoding='utf8'),ensure_ascii=False)
from collections import Counter
print(len(rows), Counter(r['kind'] for r in rows))
for r in rows: print(r['id'],r['kind'],r['stageName'],r['who'],'|',r['zh'][:80])
