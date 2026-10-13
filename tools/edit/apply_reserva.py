import os
import sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/reserva/index.html')
s=open(P,encoding='utf-8').read()
R=[
# 002 intro
("Ami 要你幫大家打電話訂位。記住她說的每一個細節！","Ami 要你幫忙打電話訂位。要仔細聽喔！"),
('data-es="Ami te pide que reserves una mesa por teléfono. ¡Recuerda todos los detalles!" data-en="Ami asks you to book a table by phone. Remember every detail!">Ami te pide que reserves una mesa por teléfono. ¡Recuerda todos los detalles!',
 'data-es="Ami te pide que reserves una mesa por teléfono. ¡Escucha con atención!" data-en="Ami asks you to book a table by phone. Listen carefully!">Ami te pide que reserves una mesa por teléfono. ¡Escucha con atención!'),
# 004 / 031 傳單→廣告單
("DIAL: '再看一次傳單'","DIAL: '再看一次廣告單'"),
("L('（冰箱上有一張餐廳的傳單。","L('（冰箱上有一張餐廳的廣告單。"),
("['傳單', 'folleto', 'flyer']","['廣告單', 'folleto publicitario', 'flyer']"),
# 022 greet
("L('店員：您好，好味道餐廳，請問有什麼需要？', 'Buenas, restaurante Hao Weidao, ¿en qué le puedo ayudar?', 'Hello, Hao Weidao restaurant, how can I help you?')",
 "L('店員：您好，這裡是好味道餐廳，請問有什麼可以為您服務的嗎？', 'Buenas, aquí el restaurante Hao Weidao, ¿en qué puedo servirle?', 'Hello, this is Hao Weidao restaurant. How may I help you?')"),
# 024 + 025
("""L(`Ami：${N}，${t.day}（${dateStr(t.date)}）我們要去好味道餐廳聚餐，你可以幫我打電話訂位嗎？`,
            `${N}, el ${DAY_ES[t.day]} (${esDate(t.date)}) vamos a comer al restaurante Hao Weidao. ¿Puedes llamar para reservar una mesa?`,
            `${N}, on ${DAY_EN[t.day]} (${enDate(t.date)}) we're having dinner at Hao Weidao. Can you call and book a table?`),
          L('Ami：你幫我打吧，剛好讓你練習中文！',
            'Llama tú, ¡así practicas chino!',
            "You make the call. It's good Chinese practice for you!"),""",
 """L(`Ami：${N}，我們${dateStr(t.date)}${t.day}要去好味道餐廳聚餐，你可以幫我打電話訂位嗎？順便練習你的中文！`,
            `${N}, el ${DAY_ES[t.day]} ${esDate(t.date)} vamos a comer al restaurante Hao Weidao. ¿Puedes llamar para reservar una mesa? ¡Así practicas chino!`,
            `${N}, on ${DAY_EN[t.day]}, ${enDate(t.date)}, we're having dinner at Hao Weidao. Can you call and book a table? Good Chinese practice for you!`),"""),
# 028
("Ami：對了，我朋友小美吃素。還有，不要太貴的位子！","Ami：對了，我朋友小美吃素。還有，不要選太貴的位子！"),
# 033
("'號碼撥錯了，打到別人家。Marcaste mal el número.'","'打錯號碼了，打到別人家。Marcaste mal el número.'"),
# 045 (typo 還→還有)
("L('店員：好的……請問還有別的事嗎？', 'Bueno… ¿necesita algo más?', 'OK… is there anything else?')",
 "L('店員：好的……請問還有什麼可以為您服務的嗎？', 'Bueno… ¿puedo ayudarle en algo más?', 'OK… is there anything else I can help you with?')"),
# 055
("Game.good('你發現店員說錯日期了！', '¡Notaste que","Game.good('讚喔！你發現店員說錯日期了', '¡Bien! Notaste que"),
# 058
("L('我：不好意思，我說錯了，我重新說。', 'Perdón, me equivoqué, lo digo otra vez.', 'Sorry, I misspoke, let me say it again.')",
 "L('我：不好意思，我說錯了，再跟您確認一次。', 'Perdón, me equivoqué; se lo confirmo otra vez.', 'Sorry, I misspoke; let me confirm again.')"),
# 068/079/165 option
("'請稍等，我問一下朋友。'","'等一下喔……我確認一下。'"),
("c.startsWith('請稍等')","c.startsWith('等一下喔')"),
("opt.startsWith('請稍等')","opt.startsWith('等一下喔')"),
("['請稍等', 'un momento, por favor', 'one moment, please'], ['問一下', 'preguntar un momento', 'quickly ask']",
 "['等一下', 'un momento', 'one moment'], ['確認', 'confirmar, verificar', 'check, confirm']"),
# 072
("Game.good('人數正確，有把小朋友算進去。', 'Número correcto","Game.good('很棒欸！人數正確，有把小朋友算進去。', '¡Muy bien! Número correcto"),
# 073 (typo 旺季→忘記)
("'忘了把小朋友也算進去。Olvidaste","'忘記把小朋友也算進去。Olvidaste"),
# 081
("L('店員：好的。還有其他需要嗎？', 'Bien. ¿Necesita algo más?', 'OK. Anything else?')",
 "L('店員：好的。還有其他需求嗎？', 'Bien. ¿Necesita algo más?', 'OK. Anything else?')"),
# 090
("Game.good('兒童椅和素食都問了！', '¡Pediste","Game.good('太好了！兒童椅和素食都有問！', '¡Muy bien! Pediste"),
# 108
("'店員複述時說錯了，你沒發現。El empleado repitió algo mal y no lo notaste.'","'店員要確認時說錯了，你沒發現。El empleado se equivocó al confirmar y no lo notaste.'"),
# 117
("Game.good('你發現店員複述錯了！', '¡Notaste el error del empleado al repetir!', 'You caught the mistake in the read-back!')",
 "Game.good('你發現店員說錯了！', '¡Notaste el error del empleado!', 'You caught the employee\\'s mistake!')"),
# 120
("""L('店員：好的，訂好了！位子只保留十分鐘，遲到超過十分鐘就會取消喔。',
          '¡Listo, reservado! Guardamos""","""L('店員：好的，訂好了！提醒您，位子只保留十分鐘，遲到超過十分鐘就會取消喔。',
          '¡Listo, reservado! Le recuerdo que guardamos"""),
("\"All set! We only hold","\"All set! Just a reminder: we only hold"),
# 125
("'回答太冷淡，可以說謝謝。Tu respuesta fue muy seca; podías dar las gracias.'","'太冷淡了啦！可以說聲謝謝。¡Muy seco! Podías dar las gracias.'"),
# 128
("""L(`Ami：還有，可以改成${timeStr(t.ask2)}嗎？大家都要坐在一起喔！`, `Y, ¿se puede cambiar a ${esTime(t.ask2)}? ¡Todos tenemos que sentarnos juntos!`, `Also, can we change it to ${enTime(t.ask2)}? We all need to sit together!`)""",
 """L(`Ami：還有，可以改成${timeStr(t.ask2)}嗎？我們要坐在一起，不要分桌喔！`, `Y, ¿se puede cambiar a ${esTime(t.ask2)}? ¡Queremos sentarnos juntos, no en mesas separadas!`, `Also, can we change it to ${enTime(t.ask2)}? We want to sit together, not at separate tables!`)"""),
# 130
("options: ['我想修改訂位。', '我想訂位。', '我想取消訂位。']","options: ['你好，我剛剛有打電話訂位，我想要更正一下。', '我想訂位。', '我想取消訂位。']"),
("if (c === '我想修改訂位。')","if (c.startsWith('你好，我剛剛有打電話訂位'))"),
# 145
("或是改成大廳兩張桌子併在一起，也可以分開坐兩桌。`","或是改成兩張桌子併在一起，也可以分開坐兩桌。`"),
("También puedo juntar dos mesas en el salón principal","También puedo juntar dos mesas"),
("Or we can push two tables together in the main hall,","Or we can push two tables together,"),
# 177
("L('店員：好的，幫您改好了。謝謝您的來電！'","L('店員：好的，幫您改好了。感謝您的來電！'"),
# 185
("沒位子了，要維持${timeStr(t.t1)}，還是改到${timeStr(t.alt2)}？`","沒位子了，要原本的${timeStr(t.t1)}，還是改到${timeStr(t.alt2)}？`"),
# 186
("小朋友會想睡覺。維持${timeStr(t.t1)}吧！`","小朋友會想睡覺。原本的${timeStr(t.t1)}吧！`"),
# 187 (趕來不及→來不及)
("L(`Ami：${timeStr(t.t1)}阿哲趕不到，改${timeStr(t.alt2)}好了。`","L(`Ami：${timeStr(t.t1)}阿哲來不及，改${timeStr(t.alt2)}好了。`"),
# 189
("Game.good('先問 Ami 是好主意。', 'Preguntarle a Ami fue una buena idea.', 'Asking Ami first was a good idea.')",
 "Game.good('聰明喔！知道要先問 Ami。', '¡Muy listo! Sabías que primero había que preguntarle a Ami.', 'Smart! You knew to ask Ami first.')"),
# 191
("[`日期訂成${dateStr(b.date)}，可是是${dateStr(t.date)}才對！`, `¡Reservaste para el ${esDate(b.date)}, pero era el ${esDate(t.date)}!`",
 "[`你怎麼訂到${dateStr(b.date)}，是${dateStr(t.date)}才對！`, `¿Por qué reservaste para el ${esDate(b.date)}? ¡Era el ${esDate(t.date)}!`"),
("`You booked ${enDate(b.date)}, but it should be ${enDate(t.date)}!`","`Why did you book ${enDate(b.date)}? It should be ${enDate(t.date)}!`"),
# 192
("[`時間是${timeStr(b.time)}？我們說好${timeStr(t.finalTime)}的！`, `¿A ${esTime(b.time)}? ¡Quedamos a ${esTime(t.finalTime)}!`, `${enTime(b.time)}? We agreed on ${enTime(t.finalTime)}!`]",
 "[`${timeStr(b.time)}？我跟你說${timeStr(t.finalTime)}欸！`, `¿A ${esTime(b.time)}? ¡Te dije a ${esTime(t.finalTime)}!`, `${enTime(b.time)}? I told you ${enTime(t.finalTime)}!`]"),
# 193
("[`位子只有${cn(b.people)}個人的，我們有${cn(t.finalPeople)}個人耶！`, `¡La mesa es para ${b.people}, pero somos ${t.finalPeople}!`, `The table is for ${b.people}, but there are ${t.finalPeople} of us!`]",
 "[`你只有訂${cn(b.people)}個人，我們有${cn(t.finalPeople)}個人耶！`, `¡Solo reservaste para ${b.people}, pero somos ${t.finalPeople}!`, `You only booked for ${b.people}, but there are ${t.finalPeople} of us!`]"),
# 195
("['分兩桌？我說大家要坐在一起耶！', '¿En dos mesas? ¡Dije que todos juntos!', 'Two tables? I said we all sit together!']",
 "['為什麼要分兩桌？我說大家要坐在一起耶！', '¿Por qué en dos mesas? ¡Dije que todos juntos!', 'Why two tables? I said we all sit together!']"),
# 196
("[`兒童椅要${cnCount(t.kids)}張，你訂了${b.chairs ? cnCount(b.chairs) + '張' : '零張'}。`, `Necesitábamos ${esN(t.kids, 'silla para niños', 'sillas para niños')} y reservaste ${b.chairs}.`, `We needed ${t.kids} high chair${t.kids > 1 ? 's' : ''}, you booked ${b.chairs}.`]",
 "[`應該是${cnCount(t.kids)}張兒童座椅吧？你怎麼訂了${b.chairs ? cnCount(b.chairs) + '張' : '零張'}？`, `¿No eran ${esN(t.kids, 'silla para niños', 'sillas para niños')}? ¿Por qué reservaste ${b.chairs}?`, `Shouldn't it be ${t.kids} high chair${t.kids > 1 ? 's' : ''}? Why did you book ${b.chairs}?`]"),
# 197
("['你沒問素食，小美要吃什麼？', 'No preguntaste por comida vegetariana, ¿qué va a comer Xiaomei?', \"You didn't ask about vegetarian food, what will Xiaomei eat?\"]",
 "['你沒問素食，那小美要吃什麼？', 'No preguntaste por comida vegetariana, ¿y entonces qué va a comer Xiaomei?', \"You didn't ask about vegetarian food, so what will Xiaomei eat?\"]"),
# 200
("L(`Ami：太棒了，${N}！謝謝你，那天我請你吃飯！`, `¡Genial, ${N}! Gracias, ¡ese día te invito a comer!`, `Awesome, ${N}! Thanks, dinner's on me that day!`)",
 "L(`Ami：太棒了，${N}！謝謝你，你的中文不錯嘛！`, `¡Genial, ${N}! Gracias, ¡tu chino está muy bien!`, `Awesome, ${N}! Thanks, your Chinese is pretty good!`)"),
# 205 hint
("item(`${cn(t.adults)}個大人，還有${cnCount(t.kids)}個小朋友，小朋友要坐兒童椅。`","item(`${cn(t.adults)}個大人，${cnCount(t.kids)}個小孩，小孩要坐兒童椅。`"),
# 209/210
("item(`問 Ami：${timeStr(t.T - 0.5)}還沒下班","item(`Ami：${timeStr(t.T - 0.5)}還沒下班"),
("item('問 Ami：包廂太貴了","item('Ami：包廂太貴了"),
# 211
("${r('Ami 回電說的')}","${r('Ami 打電話補充的')}"),
# 215/216
("item(`問 Ami：${timeStr(t.alt2)}太晚了，維持${timeStr(t.t1)}。`, `Ami: ${esTime(t.alt2)} es muy tarde; mantener ${esTime(t.t1)}.`, `Ami: ${enTime(t.alt2)} is too late; keep ${enTime(t.t1)}`)",
 "item(`Ami：${timeStr(t.alt2)}太晚了，維持原來的${timeStr(t.t1)}。`, `Ami: ${esTime(t.alt2)} es muy tarde; mantener la hora original, ${esTime(t.t1)}.`, `Ami: ${enTime(t.alt2)} is too late; keep the original ${enTime(t.t1)}`)"),
("item(`問 Ami：阿哲${timeStr(t.t1)}趕不到，改${timeStr(t.alt2)}。`","item(`Ami：阿哲${timeStr(t.t1)}來不及，改成${timeStr(t.alt2)}。`"),
]
bad=0
for a,b in R:
    n=s.count(a)
    if n<1: print('MISSING:',a[:90]); bad+=1; continue
    s=s.replace(a,b)
if bad: sys.exit(1)
open(P,'w',encoding='utf-8').write(s); print('ok',len(R))
