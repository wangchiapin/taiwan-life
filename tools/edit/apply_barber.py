import os
import sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/barber/index.html')
s=open(P,encoding='utf-8').read()
# 每一筆：(舊字串, 新字串[, 預期出現次數])；找不到就停
# 括號內的編號是線上修改表的列號（rows/barber.json）
R=[
# 003 開頭介紹（中文一次；西文在 data-es 和 span；英文在 data-en）
('''了。你要先打電話預約，選對時間、說對電話號碼，到店說「有預約」，說明怎麼剪，水太燙要有禮貌地說，最後付錢、算找錢。''',
 '''了，要找時間去剪頭髮。對了，你有自己去剪頭髮過嗎？''', 1),
('''Ami dice que tienes el pelo muy largo. Reserva primero por teléfono, elige bien el horario y di tu número; en la tienda di que tienes cita, explica el corte, pide con cortesía que enfríen el agua y al final paga y revisa el cambio.''',
 '''Ami dice que tienes el pelo muy largo y que tienes que buscar un momento para cortártelo. Por cierto, ¿alguna vez has ido a cortarte el pelo por tu cuenta?''', 2),
('''Ami says your hair is too long. Book by phone first — pick the right time and give your number — then say you have an appointment, explain the cut, politely ask for cooler water, and finally pay and check your change.''',
 '''Ami says your hair is too long and you should find time to get it cut. By the way, have you ever gone for a haircut on your own?''', 1),
# 019、020（Ben 把 020 併進 019，020 刪除）
('''      L('Ami：你頭髮太長了，去剪一剪吧！先預約比較不用等喔。', 'Tienes el pelo muy largo, ¡ve a cortártelo! Es mejor reservar primero para no esperar.', 'Your hair is too long — go get it cut! Booking first means less waiting.'),
      L(`Ami：你這個${t.want.slice(0, 3)}下午${t.hr === 2 ? '兩' : CN[t.hr]}點有空，對吧？`, `Tienes libre ese día a las ${t.hr} de la tarde, ¿verdad?`, `You're free that day at ${t.hr} p.m., right?`),
''',
 '''      L(`Ami：你頭髮太長了，去剪一剪吧！你這個${t.want.slice(0, 3)}下午${t.hr === 2 ? '兩' : CN[t.hr]}點有空，對吧？先預約比較不用等喔。`, `Tienes el pelo muy largo, ¡ve a cortártelo! Tienes libre ese día a las ${t.hr} de la tarde, ¿verdad? Es mejor reservar primero para no esperar.`, `Your hair is too long — go get it cut! You're free that day at ${t.hr} p.m., right? Booking first means less waiting.`),
''', 1),
# 021
('''L(`Ami：剪到${l[0]}就好，瀏海${t.bang[0]}。`, `Cortar hasta ${l[1]} es suficiente; flequillo: ${t.bang[1]}.`, `Cut it to ${l[2]}; bangs: ${t.bang[2]}.`)''',
 '''L(`Ami：我覺得你剪到${l[0]}就好，瀏海${t.bang[0]}。`, `Creo que cortar hasta ${l[1]} es suficiente; flequillo: ${t.bang[1]}.`, `I think cutting it to ${l[2]} is enough; bangs: ${t.bang[2]}.`)''', 1),
# 022
('''L('（你的頭髮太長了。手機響了一聲，是 Ami 傳來的 LINE。）', '(Tienes el pelo muy largo. Tu celular suena: es un LINE de Ami.)', '(Your hair is too long. Your phone buzzes — a LINE from Ami.)')''',
 '''L('（手機響了一聲，是 Ami 傳來的 LINE。）', '(Tu celular suena: es un LINE de Ami.)', '(Your phone buzzes — a LINE from Ami.)')''', 1),
# 025（Ben 的問題：這一關不是在店門口；改成在手機上找到店家資訊；026 保留）
('''L('（你找到一間理髮店，門口貼著：「歡迎預約，電話 0900-000-000」。）', '(Encuentras una peluquería. En la puerta dice: «歡迎預約»: se aceptan reservas por teléfono.)', '(You find a salon. A sign on the door reads 歡迎預約 — reservations welcome.)')''',
 '''L('（你在手機上找到一間理髮店，上面寫著：「歡迎預約，電話 0900-000-000」。）', '(Encuentras una peluquería en tu celular. Dice: «歡迎預約»: se aceptan reservas por teléfono.)', '(You find a salon on your phone. It says 歡迎預約 — reservations welcome.)')''', 1),
# 031
('''M('頭髮太長了，現在就預約吧。',''', '''M('頭髮太長了啦，現在就預約吧。',''', 1),
# 036
('''M(`你${t.want.slice(0, 3)}下午${t.hr === 2 ? '兩' : CN[t.hr]}點才有空，要選「${t.want}」。`, `Solo estás libre el día indicado a las ${t.hr} de la tarde: elige «${t.want}».`, `You're only free at ${t.hr} p.m. on that day: pick "${t.want}".`)''',
 '''M(`想清楚一點，你${t.want.slice(0, 3)}下午${t.hr === 2 ? '兩' : CN[t.hr]}點才有空，要選「${t.want}」。`, `Piénsalo bien: solo estás libre el día indicado a las ${t.hr} de la tarde; elige «${t.want}».`, `Think it through: you're only free at ${t.hr} p.m. on that day — pick "${t.want}".`)''', 1),
# 039 刪除「老闆在電腦上打字」
('''L('（老闆在電腦上打字，等你說電話號碼。）', '(El dueño teclea en la computadora, esperando tu número.)', '(The owner types on a computer, waiting for your number.)'), ''', '', 1),
# 041
('''M(`你的電話是 ${t.phone}。要看清楚每個數字。`, `Tu número es ${t.phone}. Revisa bien cada dígito.`, `Your number is ${t.phone}. Check every digit.`)''',
 '''M(`你的電話是 ${t.phone}。怎麼會忘記了呢？`, `Tu número es ${t.phone}. ¿Cómo pudiste olvidarlo?`, `Your number is ${t.phone}. How could you forget?`)''', 1),
# 043、044（044 刪除「預約的日子到了。你走進理髮店」；過場按鈕本來就寫「預約的日子到了，走進理髮店」）
('''[boss(`好，${t.want}，我們等你。`, `Bien, ${t.want}; te esperamos.`, `OK, ${t.want} — we'll see you then.`), L('（預約的日子到了。你走進理髮店。）', '(Llega el día de tu cita. Entras a la peluquería.)', '(The day arrives. You walk into the salon.)')]''',
 '''[boss(`好，${t.want}，謝謝。`, `Bien, ${t.want}; gracias.`, `OK, ${t.want} — thank you.`)]''', 1),
# 045 刪除「店裡有幾個客人在等」
('''L('（店裡有幾個客人在等。設計師看到你走進來。）', '(Hay varios clientes esperando. El estilista te ve entrar.)', '(Several customers are waiting. The stylist sees you come in.)'), ''', '', 1),
# 055
('''M(`Ami 說剪到${t.len[0]}就好。`, `Ami dijo que bastaba con cortar hasta ${t.len[1]}.`, `Ami said to cut it to ${t.len[2]}.`)''',
 '''M(`Ami 建議剪到${t.len[0]}就好，聽她的建議吧！`, `Ami sugirió cortar hasta ${t.len[1]}: ¡hazle caso!`, `Ami suggested cutting it to ${t.len[2]} — take her advice!`)''', 1),
# 056
('''goodFirst('STYLE_LEN', '你說得很清楚！',''', '''goodFirst('STYLE_LEN', '你說得很清楚唷！',''', 1),
# 059
('''M(`Ami 說瀏海${t.bang[0]}。`, `Ami dijo: flequillo, ${t.bang[1]}.`, `Ami said the bangs: ${t.bang[2]}.`)''',
 '''M(`Ami 建議瀏海${t.bang[0]}，聽她的建議吧！`, `Ami sugirió: flequillo, ${t.bang[1]}. ¡Hazle caso!`, `Ami suggested the bangs: ${t.bang[2]} — take her advice!`)''', 1),
# 062
('''L('（助理幫你洗頭。水太燙了！）', '(Una asistente te lava el cabello. ¡El agua está demasiado caliente!)', '(An assistant washes your hair. The water is scalding!)')''',
 '''L('（水太燙了！）', '(¡El agua está demasiado caliente!)', '(The water is scalding!)')''', 1),
# 064、066
('''options: () => rot(['不好意思，水有點燙，可以冷一點嗎？', '沒關係，我忍一下。', '啊！好燙！你想燙死我嗎？']),''',
 '''options: () => rot(['不好意思，水有點燙。', '沒關係，我忍一下。', '媽的！好燙！你想燙死我嗎？']),''', 1),
# 067、068、069（Ben 同意：正解縮短後，答錯說明和綠卡一起改）
('''M('水太燙會受傷，要說出來。用「不好意思…可以…嗎？」很有禮貌。', 'El agua muy caliente puede lastimar: hay que decirlo. «不好意思…可以…嗎？» es muy cortés.', 'Scalding water can hurt — speak up. 不好意思…可以…嗎？ is very polite.')''',
 '''M('水太燙要說，不然會燙傷！', '¡Si el agua está muy caliente, hay que decirlo; si no, te quemas!', 'If the water is too hot, say so — or you will get burned!')''', 1),
('''M('不要生氣，禮貌地說就好：「不好意思，水有點燙，可以冷一點嗎？」', 'No te enojes; di con cortesía: «不好意思，水有點燙，可以冷一點嗎？».', "Don't get angry — just say politely: 不好意思，水有點燙，可以冷一點嗎？")''',
 '''M('不要生氣，禮貌地說就好：「不好意思，水有點燙。」', 'No te enojes; di con cortesía: «不好意思，水有點燙».', "Don't get angry — just say politely: 不好意思，水有點燙。")''', 1),
('''goodFirst('WASH', '很有禮貌！「不好意思，可以…嗎？」很好用。', '¡Muy cortés! «不好意思，可以…嗎？» es muy útil.', '很有禮貌！「不好意思，可以…嗎？」 is a very handy pattern.');''',
 '''goodFirst('WASH', '很有禮貌！說「不好意思」就不會讓人不舒服。', '¡Muy cortés! Decir «不好意思» evita que la otra persona se sienta incómoda.', 'Very polite! Saying 不好意思 keeps things comfortable for everyone.');''', 1),
# 070（Ben 同意：助理那句改成真正的對話）
('''[L('（助理說：「好的，這樣可以嗎？」水剛剛好。洗好了，你回到座位，設計師開始剪。）', '(La asistente dice: «Claro, ¿así está bien?». El agua queda perfecta. Terminan de lavarte y el estilista empieza a cortar.)', '(The assistant says, "Sure — is this OK?" The water is just right. You return to your seat and the stylist begins cutting.)')]''',
 '''[L('助理：好的，這樣可以嗎？', 'Claro, ¿así está bien?', 'Sure — is this OK?'), L('（洗好了，你回到座位，設計師開始剪。）', '(Terminan de lavarte y vuelves a tu asiento; el estilista empieza a cortar.)', '(You are done washing and return to your seat; the stylist begins cutting.)')]''', 1),
# 076
('''M('你覺得後面還有點長，現在就要說。設計師不會知道你在想什麼。',''', '''M('你覺得後面還有點長就要說，不然設計師不知道你在想什麼。',''', 1),
# 091
('''rot(['算一算，沒錯，收下，謝謝',''', '''rot(['沒錯，謝謝',''', 1),
# 098
('''L(`Ami：哇，${N}，剪得很好看欸！預約真的很方便吧！我們去走走吧！`, `¡Vaya, ${N}, qué bien te quedó! ¡Reservar es muy práctico, ¿verdad? ¡Vamos a dar una vuelta!`, `Wow, ${N}, it looks great! Booking really is convenient, right? Let's go for a stroll!`)''',
 '''L(`Ami：哇，${N}，剪得很好看欸！很帥喔！我們去走走吧！`, `¡Vaya, ${N}, qué bien te quedó! ¡Te ves genial! ¡Vamos a dar una vuelta!`, `Wow, ${N}, it looks great! You look awesome! Let's go for a stroll!`)''', 1),
]
for r in R:
    old,new=r[0],r[1]
    n=r[2] if len(r)>2 else 1
    c=s.count(old)
    if c!=n:
        print('次數不對（預期 %d，實際 %d）：%s'%(n,c,old[:70])); sys.exit(1)
    s=s.replace(old,new)
open(P,'w',encoding='utf-8').write(s)
print('OK，共 %d 筆'%len(R))
