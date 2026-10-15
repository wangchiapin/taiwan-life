import os
import sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/street/index.html')
s=open(P,encoding='utf-8').read()
# 每一筆：(舊字串, 新字串[, 預期出現次數])；找不到就停
# 括號內的編號是線上修改表的列號（rows/street.json）
R=[
# 003 開頭介紹（中文一次；西文、英文在 data-es/data-en 和 span）
("週六下午，Ami 在前面路口的咖啡店等你。你走在路上，會遇到各種突發的事：紅燈、機車喇叭、有人跌倒、阿嬤過馬路、有人問路、掉錢包、下雨、發傳單……每次遊戲會遇到其中五件。",
 "Ami 在咖啡店等你。你走在路上，會遇到各種突發事件，你可以順利到達咖啡店嗎？", 1),
("Es sábado por la tarde y Ami te espera en una cafetería de la esquina. Por el camino te pasarán cosas imprevistas: semáforo en rojo, bocinazos de motos, alguien que se cae, una abuelita cruzando, alguien que pregunta una dirección, una billetera caída, lluvia, volantes… En cada partida te tocan cinco.",
 "Ami te espera en una cafetería. Por el camino te pasarán todo tipo de imprevistos. ¿Podrás llegar a la cafetería sin problemas?", 2),
("It's Saturday afternoon and Ami is waiting at a café at the next intersection. On the way you'll run into all kinds of surprises: a red light, scooter horns, someone falling, a grandma crossing, someone asking directions, a dropped wallet, rain, flyers… Each round gives you five of them.",
 "Ami is waiting for you at a café. On the way you'll run into all kinds of surprises. Can you make it to the café?", 1),
# 008–010 Ami 的 LINE（010 刪除）
("""      L(`Ami：${N}，我在前面路口的咖啡店等你，你走過來吧！`,
        `${N}, te espero en la cafetería de la esquina de enfrente. ¡Ven caminando!`,
        `${N}, I'm waiting at the café at the next intersection. Come on over!`),
      L('Ami：路上人多車也多，要小心喔。',
        'Hay mucha gente y muchos autos en la calle; ten cuidado.',
        "There are lots of people and cars out there, so be careful."),
      L('Ami：如果路上有什麼事，先處理一下，我可以等你。',
        'Si pasa algo en el camino, ocúpate primero; yo puedo esperarte.',
        "If something happens on the way, deal with it first — I can wait.")""",
 """      L(`Ami：${N}，我在咖啡店等你，你趕快過來吧！`,
        `${N}, te espero en la cafetería. ¡Ven rápido!`,
        `${N}, I'm waiting for you at the café. Hurry on over!`),
      L('Ami：路上小心喔！',
        '¡Ten cuidado por el camino!',
        'Be careful on the way!')""", 1),
# 018
("{ t: '沒有車，我也直接走過去。',", "{ t: '沒有車，直接闖過去。',", 1),
# 024、025
("good: ['在台灣，要等小綠人亮了才過馬路。', 'En Taiwán se cruza solo cuando se enciende el hombrecito verde.', 'In Taiwan you cross only when the little green man lights up.'],",
 "good: ['遵守交通規則，不要當馬路三寶。', 'Respeta las normas de tráfico: no seas un peligro en la calle.', \"Follow the traffic rules — don't be a road menace.\"],", 1),
("after: [sc('（小綠人亮了，你慢慢走過斑馬線。）', '(Se enciende el hombrecito verde y cruzas con calma por el paso de cebra.)', '(The little green man lights up and you walk across the crosswalk.)')]",
 "after: [sc('（小綠人走起來了！很可愛吧！）', '(¡El hombrecito verde echa a andar! ¿A que es lindo?)', \"(The little green man starts walking! Cute, isn't it?)\")]", 1),
# 026
("""dialogue: () => [sc('（你走進一條小巷，巷子很窄，沒有人行道。後面突然傳來「嗶！嗶！」的喇叭聲，一台機車想要過去。）', '(Entras en un callejón estrecho, sin acera. De pronto suena «¡bip, bip!» detrás de ti: una moto quiere pasar.)', '(You walk into a narrow alley with no sidewalk. Suddenly you hear "beep, beep!" behind you — a scooter wants to get past.)')],""",
 """dialogue: () => [sc('（叭！叭！）', '(¡Piii, piii!)', '(Honk! Honk!)')],""", 1),
# 028、029
("{ t: '站在原地不動，回頭看他。', m: M('機車按喇叭，是請你讓一下。往旁邊靠比較安全。', 'Si la moto toca la bocina, te pide que te apartes. Hazte a un lado: es más seguro.', 'When a scooter honks, it is asking you to move over. Step aside to be safe.')",
 "{ t: '站在原地不動，回頭瞪他。', m: M('機車按喇叭，你可以先讓一下，保護自己的安全。', 'Si una moto toca la bocina, puedes apartarte primero para protegerte.', 'When a scooter honks, you can step aside first to keep yourself safe.')", 1),
# 034、036
("good: ['小巷子裡聽到喇叭聲，要往旁邊靠，讓車先過。', 'Si oyes una bocina en un callejón, apártate y deja pasar al vehículo.', 'If you hear a horn in a narrow alley, step aside and let the vehicle pass.'],",
 "good: ['雖然可能不是你的問題，但是你很有禮貌喔！', 'Quizá no era culpa tuya, ¡pero fuiste muy educado!', \"It may not have been your fault, but that was very polite of you!\"],", 1),
("sc('（機車慢慢地從你旁邊騎過去。）', '(La moto pasa despacio a tu lado.)', '(The scooter slowly rides past you.)')",
 "sc('（機車慢慢地從你旁邊騎過去，跟你點點頭感謝。）', '(La moto pasa despacio a tu lado y el conductor te agradece con la cabeza.)', '(The scooter slowly rides past you, and the rider nods in thanks.)')", 1),
# 037
("sc(`（前面有一位${fw[0]}在人行道上跌倒了，坐在地上，沒有站起來。）`, `(Delante, ${fw[1]} se ha caído en la acera y sigue sentado en el suelo.)`, `(Ahead, ${fw[2]} has fallen on the sidewalk and is still sitting on the ground.)`)",
 "sc(`（前面有一位${fw[0]}跌倒了，坐在地上！）`, `(Delante, ¡${fw[1]} se ha caído y está sentado en el suelo!)`, `(Ahead, ${fw[2]} has fallen and is sitting on the ground!)`)", 1),
# 040
("{ t: '趕快用力把他拉起來。',", "{ t: '用力把他拉起來。',", 1),
# 044
("m: M('看到有人跌倒，要先關心他。', 'Si ves a alguien caerse, primero interésate por él.', 'If you see someone fall, check on them first.')",
 "m: M('看到有人跌倒，我們可以關心他一下，世界會更美好。', 'Si ves a alguien caerse, puedes preguntarle cómo está: el mundo será un poco mejor.', 'If you see someone fall, you can check on them — the world will be a little better.')", 1),
# 046、047（047 刪除：after 拿掉，選對時直接進下一步）
("""        good: ['看到有人跌倒，先問「您還好嗎？」。', 'Si ves a alguien caerse, pregunta primero «¿Está bien?».', 'When someone falls, first ask "Are you OK?".'],
        after: [sc('（你蹲下來，輕輕地問他。）', '(Te agachas y le preguntas con suavidad.)', '(You crouch down and ask gently.)')],""",
 """        good: ['你很善良喔！看到有人跌倒會上前關心。', '¡Qué buena persona! Cuando alguien se cae, te acercas a ver cómo está.', 'How kind! When someone falls, you go over to check on them.'],""", 1),
# 049（選項只看 ok，不用改判斷）
("{ t: '您先別動，我幫您打119。', ok: true },", "{ t: '您先別動，我幫您叫救護車。', ok: true },", 1),
# 056、057
("""        good: ['在台灣，需要救護車就打119。', 'En Taiwán, si hace falta una ambulancia, se llama al 119.', 'In Taiwan, call 119 when you need an ambulance.'],
        after: [sc('（你打了119，十幾分鐘後，救護車來了。）', '(Llamas al 119 y, unos diez minutos después, llega la ambulancia.)', '(You call 119, and about ten minutes later the ambulance arrives.)'), L(""",
 """        good: ['沒錯！在台灣，需要救護車就打119。', '¡Exacto! En Taiwán, si hace falta una ambulancia, se llama al 119.', 'Exactly! In Taiwan, call 119 when you need an ambulance.'],
        after: [L(""", 1),
# 059
("sc(`（綠燈亮了。一位${ew[0]}拿著菜籃慢慢過馬路，走到一半，小綠人開始閃了。）`, `(Se pone verde. ${ew[1][0].toUpperCase() + ew[1].slice(1)} cruza despacio con una cesta de verduras y, a mitad de camino, el hombrecito verde empieza a parpadear.)`, `(The light turns green. ${ew[2][0].toUpperCase() + ew[2].slice(1)} slowly crosses with a basket of vegetables, and halfway across, the little green man starts to flash.)`)",
 "sc(`（綠燈亮了。一位${ew[0]}慢慢過馬路。）`, `(Se pone verde. ${ew[1][0].toUpperCase() + ew[1].slice(1)} cruza la calle despacio.)`, `(The light turns green. ${ew[2][0].toUpperCase() + ew[2].slice(1)} slowly crosses the street.)`)", 1),
# 062
("m: M('長輩走得慢，看到了要幫忙。', 'Los mayores caminan despacio: si lo ves, ayúdalo.', 'Elderly people walk slowly — if you see it, help.')",
 "m: M('長輩走得慢，可以的話要幫忙一下。', 'Los mayores caminan despacio: si puedes, échales una mano.', 'Elderly people walk slowly — if you can, give them a hand.')", 1),
# 064、065
("{ t: '「快一點！綠燈要沒有了！」', m: M('這樣催長輩很不禮貌，應該陪他慢慢走。', 'Apurar a un mayor es de mala educación: acompáñalo despacio.', \"Rushing an elderly person is rude — walk with them slowly.\")",
 "{ t: '「走快一點！快要紅燈了！」', m: M('這樣催長輩很不禮貌。', 'Apurar así a un mayor es de mala educación.', 'Rushing an elderly person like that is rude.')", 1),
# 067、069
("""        good: ['看到長輩過馬路，主動陪他走。', 'Si ves a un mayor cruzando, acompáñalo por iniciativa propia.', 'When you see an elderly person crossing, offer to walk with them.'],
        after: [L(`${ew[0]}：謝謝你啊，好心的年輕人！`, '¡Gracias, joven de buen corazón!', 'Thank you, kind young one!'), sc('（你陪他走到對面，小綠人剛好變成紅燈。）', '(Lo acompañas al otro lado justo cuando el semáforo cambia a rojo.)', '(You walk with them to the other side just as the signal turns red.)')]""",
 """        good: ['你真是大好人！看到長輩過馬路，主動陪他走。', '¡Eres un sol! Al ver a un mayor cruzando, lo acompañaste por iniciativa propia.', 'What a good person! You saw an elderly person crossing and offered to walk with them.'],
        after: [L(`${ew[0]}：謝謝你啊，好心的年輕人！`, '¡Gracias, joven de buen corazón!', 'Thank you, kind young one!')]""", 1),
# 070
("""dialogue: () => [sc('（一位路人拿著手機走過來。）', '(Un transeúnte se te acerca con el celular en la mano.)', '(A passer-by walks up holding a phone.)'),
          L('路人：""", """dialogue: () => [L('路人：""", 1),
# 076
("good: ['問路時，說「直走、第幾個路口、左轉或右轉、在哪裡旁邊」。', 'Para dar indicaciones: «todo recto, la … esquina, gira a…, al lado de…».', 'When giving directions: \"go straight, the Nth intersection, turn left/right, next to…\".'],",
 "good: ['你已經不是那個只會問路的人了，可以幫忙指路了唷！', '¡Ya no eres solo quien pregunta el camino: ahora también puedes indicarlo!', \"You're no longer the one who can only ask for directions — now you can give them too!\"],", 1),
# 078
("sc(`（前面一位${ww[0]}從口袋拿手機的時候，錢包掉在地上了。他沒發現，繼續往前走。）`, `(Delante, ${ww[1]} saca el celular del bolsillo y se le cae la billetera. No se da cuenta y sigue caminando.)`, `(Ahead, ${ww[2]} pulls a phone from a pocket and drops a wallet. They don't notice and keep walking.)`)",
 "sc(`（前面一位${ww[0]}從口袋拿手機的時候，錢包掉在地上了。）`, `(Delante, ${ww[1]} saca el celular del bolsillo y se le cae la billetera al suelo.)`, `(Ahead, ${ww[2]} pulls a phone from a pocket and drops a wallet on the ground.)`)", 1),
# 084
("m: M('看到別人的東西掉了，要叫住他。', 'Si ves que a alguien se le cae algo, llámalo.', 'If you see someone drop something, call out to them.')",
 "m: M('看到別人的東西掉了，最好提醒他一下。', 'Si ves que a alguien se le cae algo, lo mejor es avisarle.', \"If you see someone drop something, it's best to let them know.\")", 1),
# 086
("good: ['東西掉了的人還沒發現，要出聲叫他。', 'Si alguien no se da cuenta de que perdió algo, avísale en voz alta.', \"If someone hasn't noticed they dropped something, call out to them.\"],",
 "good: ['你人真好！提醒別人東西掉了。', '¡Qué amable! Le avisaste de que se le cayó algo.', 'How kind! You let them know they dropped something.'],", 1),
# 088、089
("sc(`（天空突然下起大雨，你沒有帶傘。旁邊有${rw[0]}撐著傘，對你說話。）`,", "sc(`（天空突然下起大雨，你沒有帶傘。旁邊有一個${rw[0]}撐著傘，跟你說話。）`,", 1),
("L('路人：你也是往前面走嗎？來，一起撐吧！', '¿Tú también vas hacia allá? ¡Ven, compartamos el paraguas!', \"Are you going that way too? Come on, let's share the umbrella!\")",
 "L('路人：你也是往前面走嗎？要不要一起撐？', '¿Tú también vas hacia allá? ¿Quieres compartir el paraguas?', 'Are you going that way too? Want to share my umbrella?')", 1),
# 091、094
("{ t: '你的傘借我，你自己跑吧。',", "{ t: '你的傘直接給我吧。',", 1),
("{ t: '不要，我不認識你。',", "{ t: '不要，你是誰？我不認識你。',", 1),
# 097、099
("""        good: ['別人好心幫忙，可以說「謝謝，麻煩你了」。', 'Si alguien te ayuda de buena fe, puedes decir «gracias, qué molestia».', 'When someone kindly helps, you can say "Thanks, sorry to trouble you."'],
        after: [L('路人：不會不會，雨很大，慢慢走。', 'No hay problema; llueve fuerte, vamos despacio.', "No problem — it's raining hard, so let's walk slowly."), sc('（你們一起撐著傘，走到前面的路口。）', '(Compartiendo el paraguas, llegan juntos a la esquina de enfrente.)', '(Sharing the umbrella, you walk to the next intersection together.)')]""",
 """        good: ['沒錯！我們要感謝別人的好心！', '¡Exacto! Hay que agradecer la amabilidad de los demás.', "Exactly! We should be grateful for other people's kindness!"],
        after: [L('路人：不會不會，雨很大，慢慢走。', 'No hay problema; llueve fuerte, vamos despacio.', "No problem — it's raining hard, so let's walk slowly.")]""", 1),
# 100
("sc('（路口有一個人在發傳單，他把一張傳單遞到你面前。你還要趕去找Ami。）', '(En la esquina alguien reparte volantes y te extiende uno. Aún tienes que llegar a donde está Ami.)', '(Someone at the corner is handing out flyers and holds one out to you. You still need to hurry to Ami.)')",
 "sc('（路口有人在發傳單。）', '(En la esquina alguien reparte volantes.)', '(Someone at the corner is handing out flyers.)')", 1),
# 106
("{ t: '「不要！走開！」',", "{ t: '滾開啦！',", 1),
# 109
("good: ['不想要傳單，可以客氣地說「不用了，謝謝」。', 'Si no quieres el volante, di cortésmente «no hace falta, gracias».', \"If you don't want a flyer, politely say \\\"No need, thanks.\\\"\"],",
 "good: ['你做得對！客氣地拒絕就可以了！', '¡Bien hecho! Basta con rechazarlo con amabilidad.', 'Well done! A polite no is all it takes!'],", 1),
# 111–113 結局
("""            sc('（你終於走到路口的咖啡店，Ami坐在窗邊，看到你就揮手。）', '(Por fin llegas a la cafetería de la esquina. Ami está junto a la ventana y te saluda con la mano.)', '(You finally reach the café at the intersection. Ami is by the window and waves when she sees you.)'),
""", "", 1),
("L(`Ami：${N}，你來啦！路上都還順利嗎？你一個人處理得真好！`, `¡${N}, ya llegaste! ¿Todo bien por el camino? ¡Lo manejaste muy bien tú solo!`, `${N}, you made it! Was everything OK on the way? You handled it all so well on your own!`)",
 "L(`Ami：${N}，你來啦！路上都還順利嗎？你已經不需要其他人陪你一起出門了嘛！`, `¡${N}, ya llegaste! ¿Todo bien por el camino? ¡Ya no necesitas que nadie te acompañe para salir!`, `${N}, you made it! Was everything OK on the way? You don't need anyone to go out with you anymore!`)", 1),
("L('Ami：你來啦！辛苦了，路上遇到不少事情吧？下次我們再慢慢練習。', '¡Llegaste! Debió de pasarte de todo en el camino, ¿no? La próxima vez seguimos practicando.', 'You made it! A lot happened on the way, huh? We can keep practicing next time.')",
 "L('Ami：你來啦！感覺路上遇到很多事情，有這次的經驗下次可以處理得更好！', '¡Llegaste! Parece que te pasaron muchas cosas por el camino; con esta experiencia, ¡la próxima vez lo harás aún mejor!', \"You made it! Sounds like a lot happened on the way — with this experience, you'll handle it even better next time!\")", 1),
# 單字表
("START: [['路口', 'esquina, cruce', 'intersection'], ['咖啡店', 'cafetería', 'café'], ['小心', 'tener cuidado', 'be careful'], ['處理', 'ocuparse de, resolver', 'deal with']],",
 "START: [['咖啡店', 'cafetería', 'café'], ['趕快', 'rápido, date prisa', 'hurry'], ['小心', 'tener cuidado', 'be careful'], ['路上', 'por el camino', 'on the way']],", 1),
("['闖紅燈', 'saltarse el semáforo en rojo', 'run a red light'], ['斑馬線', 'paso de cebra', 'crosswalk']],",
 "['闖紅燈', 'saltarse el semáforo en rojo', 'run a red light'], ['交通規則', 'normas de tráfico', 'traffic rules'], ['三寶', '(jerga) conductor o peatón imprudente', '(slang) reckless road user']],", 1),
("E_honk: [['小巷', 'callejón', 'alley'], ['人行道', 'acera', 'sidewalk'],",
 "E_honk: [['瞪', 'mirar mal, fulminar con la mirada', 'glare at'], ['點頭', 'asentir con la cabeza', 'nod'],", 1),
("['菜籃', 'cesta de la compra', 'shopping basket'], ['閃', 'parpadear', 'flash'],",
 "['催', 'meter prisa, apurar', 'rush (someone)'], ['紅燈', 'luz roja', 'red light'],", 1),
("['叫住', 'llamar a alguien para que se detenga', 'call out to stop someone'],", "['提醒', 'avisar, recordar', 'remind, let someone know'],", 1),
("['介紹', 'presentar, explicar', 'introduce, explain']],", "['介紹', 'presentar, explicar', 'introduce, explain'], ['拒絕', 'rechazar', 'refuse, turn down']],", 1),
("END: [['順利', 'sin problemas', 'smoothly'], ['處理', 'ocuparse de', 'deal with'],", "END: [['順利', 'sin problemas', 'smoothly'], ['處理', 'ocuparse de', 'deal with'], ['經驗', 'experiencia', 'experience'],", 1),
]
bad=0
for t in R:
    a,b=t[0],t[1]; n=t[2] if len(t)>2 else 1
    c=s.count(a)
    if c!=n: print('COUNT',c,'!=',n,'::',a[:80]); bad+=1; continue
    s=s.replace(a,b)
if bad: sys.exit(1)
open(P,'w',encoding='utf-8').write(s); print('ok',len(R))
