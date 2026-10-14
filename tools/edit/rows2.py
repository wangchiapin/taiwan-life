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
'parcel': dict(title='超商領包裹', regions=[('const NEXT_LABEL','const Game = {','過場按鈕'),
    ('const Hints = {','\n};\n','任務提示'),
    ('  setPlace(mode) {','  /* ── 圖片','位置名稱'),
    ('  lineMsgs() {','  /* ── 狀態設定','phone'),
    ('  getConfig() {','  /* ── 換關卡','cfg')],
    speakers='店員|我|房東太太', extra={'START':'開場：看手機','END':'回家'},
    guess=[('zhItems','拿回來的包裹'),('otherStore','另一家門市'),('store','門市'),('momName','房東太太的名字'),('momFake','相似的名字'),('dadName','房東先生的名字'),('dadFake','相似的名字'),('Tail','末三碼'),('No','包裹編號'),('cod','金額'),('cardTop','金額'),('money(','金額'),('_change','金額'),('md(','日期'),('Sender','寄件人'),('=d','日期'),('=x','末三碼')]),
'nightmarket': dict(title='夜市購物', regions=[('const NEXT_LABEL','const Game = {','過場按鈕'),
    ('  setPlace(mode) {','  /* ── 圖片','位置名稱'),
    ('  /* ── Ami 交代的話','  /* ── 狀態設定','nm'),
    ('const Hints = {','\n};\n','任務提示'),
    ('  getConfig() {','  /* ── 換關卡','cfg')],
    speakers='Ami|老闆|老闆娘|我', extra={'START':'開場：Ami 請你買東西','END':'結局：和 Ami 會合'},
    guess=[('vend','攤販（老闆／老闆娘）'),('st.start - st.ask','省下的錢'),('given - st.ask','找的錢'),('Game.saved','殺價省下的錢'),('spent','花的錢'),('Game.cash','剩下的錢'),('bonus','獎勵分數'),
    ('r10(t.chicken','殺價後的雞排價錢'),('t.chicken * t.chickenPrice','雞排總價'),('chickenPrice','雞排單價'),('chicken - 1','要辣的份數'),('CN[','份數（中文）'),('chicken','份數'),
    ('tColor','T恤顏色'),('aColor','髮夾顏色'),('tSize','尺寸'),('bigSize','大一號的尺寸'),('r10(S.A.start','髮夾三個的價錢'),('S.A.start','髮夾開價'),
    ('=p','價錢'),('=o','價錢'),('=n','價錢'),('given','給的錢'),('item','商品'),('.ask','價錢'),('.start','價錢'),('x','給的錢'),('cur','攤位')]),
'bakery': dict(title='麵包店買麵包', stagevar='const STAGE = (() => {', ternary=True, regions=[('const NEXT_LABEL','const Game = {','過場按鈕'),
    ('  setPlace(mode) {','  /* ── 圖片','位置名稱'),
    ('  /* ── Ami 交代的話','  /* ── 狀態設定','nm'),
    ('const Hints = {','\n};\n','任務提示'),
    ('  getConfig() {','  /* ── 換關卡','cfg')],
    speakers='Ami|店員|我', extra={'START':'開場：Ami 請你買麵包','TONGS':'拿托盤和夾子','PICK':'夾麵包','C_SLICE':'櫃台：切吐司','C_HEAT':'櫃台：加熱','C_SEP':'櫃台：分開裝','C_MEMBER':'櫃台：會員卡','C_PAY':'櫃台：付錢','K_GREET':'Ami 的 LINE 訊息','K_SIZE':'訂蛋糕：尺寸','K_FLAVOR':'訂蛋糕：口味','K_CANDLE':'訂蛋糕：蠟燭','K_PLATE':'訂蛋糕：巧克力片','K_TIME':'訂蛋糕：取貨時間','K_CONFIRM':'訂蛋糕：店員確認','K_FIX':'訂蛋糕：哪裡不對','K_NAME':'訂蛋糕：留名字','END':'結局：Ami 進來'},
    fnmap={'amiLines':'Ami 在店門口說的話','cakeLines':'Ami 的 LINE 訊息','listHTML':'清單','trayHTML':'托盤畫面','breadName':'麵包名稱'},
    first=[('c.slice','選的片數')],
    guess=[('errName[t.err]','店員講錯的項目'),('errName[k]','選的項目'),('NZ(recapSize)','吋數（店員說的）'),('NZ(recapCandle)','蠟燭根數（店員說的）'),('recapTime','取貨時間（店員說的）'),('recapSize','吋數（店員說的）'),('recapCandle','蠟燭根數（店員說的）'),('flName','口味'),('NZ(t.people)','人數'),('NZ(t.candles)','蠟燭根數'),('NZ(t.size)','吋數'),('NZ(t.slice)','片數'),('NZ(t.n)','個數'),('=sz','片數'),('=nz','個數'),('=bz','麵包名稱'),('breadName','麵包名稱'),('t.pickup','取貨時間'),('t.friend','朋友名字'),('t.flavor','口味'),('given - total','找的錢'),('given','給的錢'),('total','總價'),('have','夾的個數'),('it.zh','麵包名稱'),('it.nut','堅果'),('BYID[','麵包名稱'),('other','別的名字')]),
}
def guess(e):
    e=e.strip()
    if e=='N': return '名字'
    for k,v in C.get('first',[]):
        if k in e: return v
    cj=re.findall(r"'([^']*[一-鿿][^']*)'", e)
    if cj:
        if C.get('ternary') and len(cj)>=2 and '?' in e: return cj[0]+'／'+cj[1]
        return '有時加：'+cj[0]
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
    if g=='nightmarket' and t in ('夜','市'): continue   # 招牌燈籠的裝飾字
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
        elif dk=='phone':
            fm=re.findall(r'\n  (\w+)\(.*?\) \{', '\n'+s[a:stt]); state={'lineMsgs':'房東太太的LINE','momSmsLines':'簡訊（房東太太轉傳）','yourSmsLines':'簡訊（你的手機）','phoneHTML':'手機畫面','bubble':'手機畫面','boxHTML':'包裹標籤','callLines':'房東太太來電'}.get(fm[-1] if fm else '', '手機')
        elif dk=='nm':
            fm=re.findall(r'\n  (\w+)\(.*?\) \{', '\n'+s[a:stt]); fn=fm[-1] if fm else ''
            state=C.get('fnmap',{'amiLines':'Ami 交代的話','tShirtLine':'衣服攤老闆開場','callLines':'Ami 來電','listHTML':'購物清單','mapHTML':'選攤位畫面','haggleHTML':'殺價畫面','haggleOptions':'殺價選項','haggleChoose':'殺價：老闆回應'}).get(fn,fn)
        else: state={'過場按鈕':'過場按鈕','位置名稱':'位置列','任務提示':'提示','台詞':'CONFIRM'}[dk]
        kind=classify(s,stt); line_=s[s.rfind('\n',0,stt)+1:s.find('\n',stt)]
        if re.search(r'addMistake\(\s*$',before): kind='錯誤說明'
        if g=='parcel':
            if re.search(r'zh: *$',before): kind='簡訊'
            elif re.search(r"bubble\(\s*'[a-z-]+',\s*$",before): kind='手機標題'
            elif dk=='phone' and state=='房東太太的LINE' and kind=='line': kind='LINE訊息'
            elif 'tailOpts' in line_ and kind=='其他': kind='選項'
            elif 'zhItems' in line_ and 'const zhItems' in line_ and kind=='其他': kind='結尾包裹說法'
            elif 'zhItems.push' in line_ and kind=='其他': kind='結尾包裹說法'
        isSay=False
        if g=='bakery':
            if re.search(r'sayK\(\s*$',before) and kind=='其他': kind='line'; isSay=True
            elif kind=='其他' and re.search(r'[?:] *$',before):
                if 'sayK(' in line_: kind='line'; isSay=True
                elif re.search(r'\bM\(|addMistake|fail\(',line_): kind='錯誤說明'
            if kind=='其他' and re.match(r'\s*const o = \[',line_): kind='選項'
            if dk=='nm' and state=='清單' and kind in ('line','其他'): kind='清單文字'
        if g=='nightmarket' and dk=='nm':
            if state=='購物清單' and kind in ('line','其他'): kind='購物清單'
            elif state=='選攤位畫面' and kind=='其他': kind='位置名稱'
            elif state=='殺價選項' and kind=='其他': kind='選項'
            elif state=='殺價：老闆回應' and re.search(r'\bsay\(\s*$',before): kind='line'
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
        if kind=='LINE訊息': who='房東太太'
        if kind in ('line','台詞'):
            m=SPK.match(zh)
            if m: who=m.group(1).strip('（）'); zh=zh[len(m.group(0)):]; kind='台詞'
            elif zh.startswith('〔客人〕：'): who='客人'; zh=zh[5:]; kind='台詞'
            elif zh.startswith('〔攤販（老闆／老闆娘）〕：'): who='老闆／老闆娘'; zh=zh[len('〔攤販（老闆／老闆娘）〕：'):]; kind='台詞'
            elif g=='bakery' and isSay and not zh.startswith('（'): who='店員'; kind='台詞'
            elif state=='殺價：老闆回應' and re.search(r'\bsay\(\s*$',before): who='老闆／老闆娘'; kind='台詞'
            else: kind='旁白' if zh.startswith('（') else '台詞'
        line=s[s.rfind('\n',0,stt)+1:s.find('\n',stt)]
        if dk=='setup' and kind=='其他' and re.search(r'say: *$',before): kind='台詞'
        if kind=='其他' or zh.startswith(('查看結果','回到地圖','查看排行榜')): continue
        if g=='bakery' and (zh in ('〔變數〕',) or re.fullmatch(r'店員：〔[^〕]*〕',zh) or re.search(r'<(button|div|span)',zh) or zh.strip()=='朗讀'): continue
        if g=='bakery' and zh=='你記得Ami說的：': zh+='〔要加熱。／不用加熱。〕'
        if g=='nightmarket' and (re.search(r'<(button|div|span)',zh) or zh.strip()=='朗讀'): continue   # 程式拼出來的 HTML 片段
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
