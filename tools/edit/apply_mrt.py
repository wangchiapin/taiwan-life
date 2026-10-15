import os
import re
import sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/mrt/index.html')
s=open(P,encoding='utf-8').read()
# 每一筆：(舊字串, 新字串[, 預期出現次數])；找不到就停
# 括號內的編號是線上修改表的列號（rows/mrt.json）
R=[
# 003 開頭介紹
("""週六下午，同事 Ami 在藍線的某一站等你。你要從紅線的某一站出發：先把飲料喝完、看悠遊卡有沒有錢、問路、搭紅線、在台北車站轉藍線、聽廣播，最後在對的站下車。""",
 """Ami 在捷運藍線的某站等你。你要從紅線的某站出發：路上會發生很多事情，你要想辦法在對的捷運站下車。""", 1),
# 022、023 Ami 的 LINE
("""      L('Ami：悠遊卡記得先看一下有沒有錢，不夠要先加值喔。',
        'Acuérdate de revisar el saldo de tu EasyCard; si no alcanza, recarga primero.',
        "Remember to check your EasyCard balance. If it's not enough, top it up first."),
      L('Ami：還有，捷運裡面不能吃東西、不能喝飲料，要在進站前喝完。',
        'Y dentro del metro no se puede comer ni beber: termina tu bebida antes de entrar a la estación.',
        "Also, you can't eat or drink inside the MRT, so finish your drink before you go into the station.")""",
 """      L('Ami：你悠遊卡裡面的錢夠吧？',
        'Tienes suficiente saldo en tu EasyCard, ¿verdad?',
        "You've got enough money on your EasyCard, right?"),
      L('Ami：對了，捷運裡面不能吃東西跟喝飲料唷！',
        'Por cierto, ¡dentro del metro no se puede comer ni beber!',
        "By the way, you can't eat or drink inside the MRT!")""", 1),
# 024、025 站務員：025 併進 024
("""      L(`站務員：到${t.dest}站的話，先搭紅線，往${t.rdir}方向，坐${NZ(rn)}站，在台北車站下車。`,
        `Para ir a ${this.destEs()}: primero la línea roja, dirección ${ROM[t.rdir]}, ${rn} ${rn === 1 ? 'parada' : 'paradas'}, y bájese en Taipei Main Station.`,
        `To get to ${t.dest}: take the Red Line toward ${ROM[t.rdir]} for ${rn} ${rn === 1 ? 'stop' : 'stops'} and get off at Taipei Main Station.`),
      L(`站務員：然後轉搭藍線，往${t.dir}方向，坐${NZ(n)}站就到了。`,
        `Luego haga transbordo a la línea azul, dirección ${ROM[t.dir]}; son ${n} ${n === 1 ? 'parada' : 'paradas'}.`,
        `Then transfer to the Blue Line toward ${ROM[t.dir]}; it's ${n} ${n === 1 ? 'stop' : 'stops'}.`)""",
 """      L(`站務員：到${t.dest}站的話，先搭紅線，往${t.rdir}方向，坐${NZ(rn)}站，在台北車站下車。然後轉搭藍線，往${t.dir}方向，坐${NZ(n)}站就到了。`,
        `Para ir a ${this.destEs()}: primero la línea roja, dirección ${ROM[t.rdir]}, ${rn} ${rn === 1 ? 'parada' : 'paradas'}, y bájese en Taipei Main Station. Luego haga transbordo a la línea azul, dirección ${ROM[t.dir]}; son ${n} ${n === 1 ? 'parada' : 'paradas'}.`,
        `To get to ${t.dest}: take the Red Line toward ${ROM[t.rdir]} for ${rn} ${rn === 1 ? 'stop' : 'stops'} and get off at Taipei Main Station. Then transfer to the Blue Line toward ${ROM[t.dir]}; it's ${n} ${n === 1 ? 'stop' : 'stops'}.`)""", 1),
# 032
("""L(`（週六下午，你在${t.origin}站附近。手機響了一聲，是Ami傳來的LINE。你手上還拿著一杯${t.drink[0]}。）`,
            `(Es sábado por la tarde y estás cerca de la estación ${ROM[t.origin]}. Tu celular suena: es un LINE de Ami. En la mano llevas ${t.drink[1]}.)`,
            `(It's Saturday afternoon and you're near ${ROM[t.origin]} Station. Your phone buzzes — a LINE from Ami. You're holding ${t.drink[2]}.)`)""",
 """L(`（你在${t.origin}站附近。手機響了一聲，是Ami傳來的LINE。你手上還拿著一杯${t.drink[0]}。）`,
            `(Estás cerca de la estación ${ROM[t.origin]}. Tu celular suena: es un LINE de Ami. En la mano llevas ${t.drink[1]}.)`,
            `(You're near ${ROM[t.origin]} Station. Your phone buzzes — a LINE from Ami. You're holding ${t.drink[2]}.)`)""", 1),
# 036
("""staff('不好意思，捷運裡面不能吃東西、喝飲料喔。', 'Disculpe, no se puede comer ni beber dentro del metro.', "Excuse me, you can't eat or drink inside the MRT.")""",
 """staff('不好意思，捷運裡面禁止飲食喔。', 'Disculpe, dentro del metro está prohibido comer y beber.', 'Excuse me, eating and drinking are not allowed inside the MRT.')""", 1),
# 040
("""M('捷運裡面不能吃東西、喝飲料，要在進站前喝完。', 'Dentro del metro no se puede comer ni beber: hay que terminar la bebida antes de entrar.', 'You can\\'t eat or drink inside the MRT; finish before entering.')""",
 """M('捷運裡面禁止飲食，要在進站前喝完。', 'Dentro del metro está prohibido comer y beber: hay que terminar la bebida antes de entrar.', 'Eating and drinking are not allowed inside the MRT; finish before entering.')""", 1),
# 043
("""goodFirst('G_DRINK', '在台灣，捷運站內不能吃東西、喝飲料，要在進站前喝完。', 'En Taiwán no se puede comer ni beber en el metro: termina antes de entrar.', "In Taiwan you can't eat or drink in the MRT, so finish before going in.")""",
 """goodFirst('G_DRINK', '你做得很好喔！在台灣，捷運站內不能吃東西、喝飲料。', '¡Lo hiciste muy bien! En Taiwán no se puede comer ni beber dentro del metro.', "Well done! In Taiwan you can't eat or drink inside the MRT.")""", 1),
# 045、046 刪除，047 改
("""          L('（你走到閘門前，把悠遊卡放在感應區。）', '(Llegas al torniquete y apoyas tu EasyCard en la zona de lectura.)', '(You reach the gate and tap your EasyCard on the reader.)'),
          L('（閘門「嗶嗶」響了，沒有打開。螢幕上寫著：餘額不足。）', '(El torniquete pita «bip bip» y no se abre. En la pantalla dice: saldo insuficiente.)', '(The gate beeps and stays shut. The screen says: insufficient balance.)'),
          L(`（你看了一下餘額：只剩${t.bal}元。這趟的票價大概二十多元，不夠。）`, `(Miras el saldo: solo quedan ${esM(t.bal)}. El pasaje cuesta unos veinte y pico dólares, no alcanza.)`, `(You check your balance: only ${enM(t.bal)} left. The fare is roughly twenty-some dollars — not enough.)`)""",
 """          L(`（悠遊卡只剩${t.bal}元，這樣不夠喔。）`, `(A tu EasyCard solo le quedan ${esM(t.bal)}; así no alcanza.)`, `(Your EasyCard only has ${enM(t.bal)} left — that's not enough.)`)""", 1),
# 054 刪除
("""[L('（你走到加值機前，把悠遊卡放在感應區。）', '(Vas a la máquina de recarga y apoyas tu tarjeta en la zona de lectura.)', '(You go to the top-up machine and place your card on the reader.)'),
          L('我：要加多少錢呢？'""", """[L('我：要加多少錢呢？'""", 1),
# 061
("""goodFirst('G_TOP', '你加的錢夠搭好幾趟了。', 'Recargaste lo suficiente para varios viajes.', 'You added enough for several rides.')""",
 """goodFirst('G_TOP', '有先見之明喔！你加的錢夠搭好幾趟了。', '¡Qué previsor! Recargaste lo suficiente para varios viajes.', 'Smart thinking ahead! You added enough for several rides.')""", 1),
# 063 刪除
("""[L('（你不太確定怎麼去，所以走到服務台問站務員。）', '(No estás seguro de cómo llegar y vas a preguntar al mostrador de atención.)', "(You're not sure how to get there, so you go to the service counter and ask.)"),
          staff(""", """[staff(""", 1),
# 065 選項（判斷也一起改）
("""rot([`請問到${t.dest}站要怎麼搭？`,""", """rot([`請問要怎麼搭去${t.dest}站？`,""", 1),
("""if (!c.startsWith(`請問到${t.dest}`)) {""", """if (c !== `請問要怎麼搭去${t.dest}站？`) {""", 1),
# 071
("""goodFirst('S_ASK', '不知道怎麼走，就問站務員。', 'Si no sabes cómo ir, pregunta al personal de la estación.', "If you don't know the way, ask the station staff.")""",
 """goodFirst('S_ASK', '沒錯！不知道怎麼走，就問站務員。', '¡Exacto! Si no sabes cómo ir, pregunta al personal de la estación.', "Exactly! If you don't know the way, ask the station staff.")""", 1),
# 072 刪除
("""dialogue: () => [L('（你刷卡進站，走到紅線的月台。月台上有兩個方向的指示牌。）', '(Pasas la tarjeta y vas al andén de la línea roja. Hay carteles para dos direcciones.)', '(You tap in and walk to the Red Line platform. There are signs for two directions.)')],""",
 """dialogue: () => [],""", 1),
# 077
("""goodFirst('P_RED', '搭捷運要看「往…方向」，也就是終點站的名字。', 'En el metro se mira «dirección…», es decir, el nombre de la terminal.',""",
 """goodFirst('P_RED', '你做得很好！搭捷運要看「往…方向」，也就是終點站的名字。', '¡Muy bien hecho! En el metro se mira «dirección…», es decir, el nombre de la terminal.',""", 1),
("""'On the MRT, look for the "toward…" sign — it\\'s the name of the end station.'""", """'Well done! On the MRT, look for the "toward…" sign — it\\'s the name of the end station.'""", 1),
# 078 廣播（紅線）
("""L(`（車廂廣播：「各位旅客，下一站，${nx}${tpe ? '，可轉乘板南線' : ''}。」）`,
            `(Anuncio del tren: «Estimados pasajeros, la próxima estación es ${ROM[nx]}${tpe ? ', con transbordo a la línea Bannan' : ''}».)`,
            `(Announcement: "Dear passengers, the next stop is ${ROM[nx]}${tpe ? ', with a transfer to the Bannan Line' : ''}.")`)""",
 """L(`（車廂廣播：「下一站，${nx}${tpe ? '，可轉乘板南線' : ''}。」）`,
            `(Anuncio del tren: «Próxima estación: ${ROM[nx]}${tpe ? ', con transbordo a la línea Bannan' : ''}».)`,
            `(Announcement: "Next stop: ${ROM[nx]}${tpe ? ', with a transfer to the Bannan Line' : ''}.")`)""", 1),
# 079 刪除
("""return Game.rstep === 0 ? [L('（列車進站了。你上了車，車廂裡有一點擠。）', '(Llega el tren. Subes; el vagón va un poco lleno.)', '(The train arrives. You get on; the car is a bit crowded.)'), ann] : [ann];""",
 """return [ann];""", 1),
# 087
("""Game.good('你聽懂廣播，知道要在台北車站下車。', 'Entendiste el anuncio y sabes dónde bajar.', 'You understood the announcement and know where to get off.')""",
 """Game.good('聽力很好喔！你聽懂廣播，知道要在台北車站下車。', '¡Muy buen oído! Entendiste el anuncio y sabes que debes bajar en Taipei Main Station.', 'Great listening! You understood the announcement and knew to get off at Taipei Main Station.')""", 1),
# 088 刪除
("""          Game.thought = [L('（你在台北車站下了車。）', '(Bajas en Taipei Main Station.)', '(You get off at Taipei Main Station.)')];
""", "", 1),
# 089 刪除
("""dialogue: () => [L('（台北車站好大，到處都是指標。你要轉搭藍線，也就是板南線。）', '(Taipei Main Station es enorme y hay letreros por todas partes. Debes transbordar a la línea azul, la línea Bannan.)', '(Taipei Main Station is huge, with signs everywhere. You need to transfer to the Blue Line — the Bannan Line.)')],""",
 """dialogue: () => [],""", 1),
# 095
("""goodFirst('X_XFER', '轉乘時，跟著路線的顏色和名字走。', 'En un transbordo, sigue el color y el nombre de la línea.',""",
 """goodFirst('X_XFER', '沒錯！轉乘時，跟著路線的顏色和名字走。', '¡Exacto! En un transbordo, sigue el color y el nombre de la línea.',""", 1),
("""'When transferring, follow the line\\'s color and name.'""", """'Exactly! When transferring, follow the line\\'s color and name.'""", 1),
# 096 刪除
("""dialogue: () => [L('（你來到藍線的月台，這裡也有兩個方向。）', '(Llegas al andén de la línea azul; también hay dos direcciones.)', '(You reach the Blue Line platform — again, two directions.)')],""",
 """dialogue: () => [],""", 1),
# 101
("""goodFirst('P_BLUE', '你看路線圖，選對了方向。', 'Miraste el mapa y elegiste bien la dirección.', 'You checked the map and chose the right direction.')""",
 """goodFirst('P_BLUE', '太棒了！你看路線圖，選對了方向。', '¡Genial! Miraste el mapa y elegiste bien la dirección.', 'Awesome! You checked the map and chose the right direction.')""", 1),
# 103（Ben 後來改成「（你坐在優先席上。）」，單字表 博愛座→慢慢；在 commit 裡直接改）
# 104
("""L(`（這時候，一位${t.elder[0]}慢慢走上車，手裡拿著拐杖，站在你面前。）`, `(Entonces sube lentamente ${t.elder[1]} con un bastón y se queda de pie frente a ti.)`, `(Then ${t.elder[2]} slowly boards with a cane and stands in front of you.)`)""",
 """L(`（一位${t.elder[0]}慢慢走上車，站在你面前。）`, `(Sube lentamente ${t.elder[1]} y se queda de pie frente a ti.)`, `(${t.elder[2][0].toUpperCase() + t.elder[2].slice(1)} slowly boards and stands in front of you.)`)""", 1),
# 108
("""M('博愛座要讓給需要的人，像是老人、孕婦、行動不便的人。',""", """M('優先席是要讓給有需要的人，像是老人、孕婦、行動不便的人。',""", 1),
# 110
("""goodFirst('T_SEAT', '看到需要的人，要主動讓座。', 'Si ves a alguien que lo necesita, ofrece tu asiento.', 'When you see someone who needs the seat, offer it.')""",
 """goodFirst('T_SEAT', '你人真好！看到有需要的人，會主動讓座。', '¡Qué amable eres! Cuando ves a alguien que lo necesita, le ofreces tu asiento.', "How kind of you! When you see someone who needs a seat, you offer yours.")""", 1),
# 112 廣播（藍線）；Ben 的句子少了「）」，補上
("""L(`（車廂廣播：「各位旅客，下一站，${t.stops[Game.step]}。」）`, `(Anuncio del tren: «Estimados pasajeros, la próxima estación es ${ROM[t.stops[Game.step]]}».)`, `(Announcement: "Dear passengers, the next stop is ${ROM[t.stops[Game.step]]}.")`)""",
 """L(`（車廂廣播：「下一站，${t.stops[Game.step]}。」）`, `(Anuncio del tren: «Próxima estación: ${ROM[t.stops[Game.step]]}».)`, `(Announcement: "Next stop: ${ROM[t.stops[Game.step]]}.")`)""", 1),
# 120、121
("""            L(`（你在${t.dest}站下了車，刷卡出站，「嗶」一聲，閘門打開了。）`, `(Bajas en ${Game.destEs()}, pasas la tarjeta y el torniquete se abre con un «bip».)`, `(You get off at ${t.dest}, tap out, and the gate opens with a beep.)`),
            L('（出站以後，你看到Ami在出口等你。）', '(Al salir, ves a Ami esperándote en la salida.)', '(After exiting, you see Ami waiting at the exit.)'),""",
 """            L(`（你在${t.dest}站下了車，刷卡出站，「嗶」一聲。）`, `(Bajas en ${Game.destEs()} y pasas la tarjeta para salir: «¡bip!».)`, `(You get off at ${t.dest} and tap out — beep!)`),""", 1),
# 122、123
("""L(`Ami：哇，${N}，你一個人搭捷運搭得好順喔！我們去吃飯吧！`, `¡Vaya, ${N}, qué bien te manejaste solo en el metro! ¡Vamos a comer!`, `Wow, ${N}, you rode the MRT so smoothly on your own! Let's go eat!`)""",
 """L(`Ami：哇，${N}，你解鎖一個人搭捷運欸！我們去吃飯吧！`, `¡Vaya, ${N}, desbloqueaste el logro de viajar solo en metro! ¡Vamos a comer!`, `Wow, ${N}, you unlocked riding the MRT on your own! Let's go eat!`)""", 1),
("""L('Ami：辛苦了！搭捷運有些地方下次再注意就好。我們去吃飯吧！', '¡Gracias por el esfuerzo! La próxima vez cuida unos detalles del metro. ¡Vamos a comer!', "Thanks for your effort! Just watch a few MRT details next time. Let's go eat!")""",
 """L('Ami：辛苦了！捷運很複雜吧！我們去吃飯吧！', '¡Gracias por el esfuerzo! El metro es complicado, ¿eh? ¡Vamos a comer!', "Thanks for your effort! The MRT is complicated, huh? Let's go eat!")""", 1),
# 單字表（對話裡不再出現的詞換掉）
("""['轉車', 'hacer transbordo', 'transfer'], ['加值', 'recargar', 'top up']],""", """['轉車', 'hacer transbordo', 'transfer'], ['夠', 'alcanzar, ser suficiente', 'be enough']],""", 1),
("""  G_DRINK: [['不能', 'no se puede', "can't, not allowed"],""", """  G_DRINK: [['禁止飲食', 'prohibido comer y beber', 'no eating or drinking'],""", 1),
("""  G_TAP: [['閘門', 'torniquete', 'fare gate'], ['感應區', 'zona de lectura', 'card reader'], ['餘額不足', 'saldo insuficiente', 'insufficient balance'], ['票價', 'tarifa, precio del pasaje', 'fare'], ['加值', 'recargar', 'top up']],""",
 """  G_TAP: [['只剩', 'solo quedar', 'only … left'], ['不夠', 'no alcanzar', 'not enough'], ['再刷一次', 'pasar la tarjeta otra vez', 'tap again'], ['加值機', 'máquina de recarga', 'top-up machine'], ['加值', 'recargar', 'top up']],""", 1),
("""['加值機', 'máquina de recarga', 'top-up machine'], ['加', 'agregar, sumar', 'add'],""", """['票價', 'tarifa, precio del pasaje', 'fare'], ['加', 'agregar, sumar', 'add'],""", 1),
("""['拐杖', 'bastón', 'cane'],""", """['優先席', 'asiento prioritario', 'priority seat'],""", 1),
("""['車門', 'puerta del tren', 'train door'], ['到站', 'llegar a la estación', 'arrive at a station']],""", """['廣播', 'anuncio por altavoz', 'announcement'], ['到站', 'llegar a la estación', 'arrive at a station']],""", 1),
("""  END: [['出站', 'salir de la estación', 'exit the station'], ['出口', 'salida', 'exit'], ['順', 'sin problemas', 'smoothly'],""",
 """  END: [['出站', 'salir de la estación', 'exit the station'], ['解鎖', 'desbloquear (un logro)', 'unlock (an achievement)'], ['複雜', 'complicado', 'complicated'],""", 1),
]
bad=0
for t in R:
    a,b=t[0],t[1]; n=t[2] if len(t)>2 else 1
    c=s.count(a)
    if c!=n: print('COUNT',c,'!=',n,'::',a[:80]); bad+=1; continue
    s=s.replace(a,b)
# 錯誤後的提示旁白刪除：053、076、094、100、109；084/085、117/118（車門快要關了／還沒到）
THOUGHTS=['（對了，Ami說過，餘額不夠要先加值……）','（站務員剛剛說往哪個方向？）','（站務員說，要轉搭哪一條線？）','（站務員剛剛說往哪個方向？看一下任務提示和路線圖。）','（旁邊的人都看著你……）']
for zh in THOUGHTS:
    pat=re.compile(r",\n[ ]*\[L\('"+re.escape(zh)+r"', [^\n]*?\)\]\)")
    ms=pat.findall(s)
    if len(ms)!=1: print('THOUGHT COUNT',len(ms),zh); bad+=1; continue
    s=pat.sub(')',s)
pat=re.compile(r",\n[ ]*\[L\((tpe|isDest) \? '（車門快要關了！）' : '（你看一下路線圖……還沒到。）', [^\n]*?\)\]\)")
if len(pat.findall(s))!=2: print('DOOR COUNT',len(pat.findall(s))); bad+=1
else: s=pat.sub(')',s)
if bad: sys.exit(1)
open(P,'w',encoding='utf-8').write(s); print('ok',len(R)+len(THOUGHTS)+1)
