import os
import re
import sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/clinic/index.html')
s=open(P,encoding='utf-8').read()
# 每一筆：(舊字串, 新字串[, 預期出現次數])；找不到就停
# 括號內的編號是線上修改表的列號（rows/clinic.json）
R=[
# 003 開頭介紹（西文、英文在 data-es/data-en 和 span 裡）
("""你已經不舒服好幾天了，同事 Ami 要你去看醫生。你一個人去診所""", """你生病了，Ami 要你去看醫生。你一個人去診所""", 1),
("""Llevas varios días sintiéndote mal y tu compañera Ami te pide que vayas al médico.""", """Estás enfermo y Ami te pide que vayas al médico.""", 2),
("""You've felt unwell for several days, and your coworker Ami tells you to see a doctor.""", """You're sick, and Ami tells you to see a doctor.""", 1),
# 004
("""    這個遊戲是中文練習，不是醫療建議。<br>""", """    注意！這個遊戲是中文練習，不是醫療建議。<br>""", 1),
("""Este juego es práctica de chino, no un consejo médico.""", """¡Atención! Este juego es práctica de chino, no un consejo médico.""", 2),
("""This game is Chinese practice, not medical advice.">""", """Please note! This game is Chinese practice, not medical advice.">""", 1),
# 021–024 Ami 的 LINE：022、023 併進 021
("""      L(`Ami：${N}，你看起來不太舒服，去看醫生吧！我今天要開會，不能陪你去。`,
        `${N}, no te ves bien: ¡ve al médico! Hoy tengo una reunión y no puedo acompañarte.`,
        `${N}, you don't look well — go see a doctor! I have a meeting today, so I can't go with you.`),
      L('Ami：公司旁邊有一家診所，感冒掛家醫科就可以了。',
        'Hay una clínica al lado de la oficina; para un resfriado basta con registrarte en medicina familiar.',
        "There's a clinic next to the office. For a cold, just register with family medicine."),
      L('Ami：記得帶健保卡，第一次去要填初診單。',
        'Acuérdate de llevar tu tarjeta del seguro de salud; la primera vez tienes que llenar un formulario de primera consulta.',
        "Remember to bring your NHI card. If it's your first time, you need to fill out a new-patient form."),
      L('Ami：看醫生的時候，要說清楚哪裡不舒服、幾天了。有對藥物過敏，也要跟醫生說喔。',
        'Con el médico, explica bien qué te duele y desde hace cuántos días. Si eres alérgico a algún medicamento, también díselo.',
        "When you see the doctor, explain clearly what's wrong and for how many days. If you're allergic to any medicine, tell the doctor too.")""",
 """      L(`Ami：${N}，你生病好幾天了，去看醫生吧！附近有一家診所，感冒掛家醫科就可以了。記得帶健保卡喔，第一次去要填初診單。`,
        `${N}, llevas varios días enfermo: ¡ve al médico! Hay una clínica cerca; para un resfriado basta con registrarte en medicina familiar. Acuérdate de llevar tu tarjeta del seguro de salud: la primera vez tienes que llenar un formulario de primera consulta.`,
        `${N}, you've been sick for several days — go see a doctor! There's a clinic nearby; for a cold, just register with family medicine. Remember to bring your NHI card: on your first visit you need to fill out a new-patient form.`),
      L('Ami：看醫生的時候，要說清楚哪裡不舒服、不舒服幾天了，有沒有藥物過敏也要跟醫生說喔。',
        'Con el médico, explica bien qué te molesta y desde hace cuántos días, y dile también si tienes alergia a algún medicamento.',
        "When you see the doctor, explain clearly what's wrong and for how many days, and tell the doctor whether you're allergic to any medicine.")""", 1),
# 任務提示：Ami 的重點現在在第一句，提示要列出全部
("""Game.amiLines().slice(1).map(item)""", """Game.amiLines().map(item)""", 1),
# 027
("""L('醫生：你對止痛藥過敏，我會開別的藥給你。', 'Eres alérgico a los analgésicos; te recetaré otros medicamentos.', "You're allergic to painkillers, so I'll prescribe something else.")""",
 """L('醫生：你說你對止痛藥過敏，我會開別的藥給你。', 'Dices que eres alérgico a los analgésicos; te recetaré otros medicamentos.', "You said you're allergic to painkillers, so I'll prescribe something else.")""", 1),
# 042
("""          L('（你已經不舒服好幾天了。這時候，手機響了，是Ami傳來的LINE。）',
            '(Llevas varios días sintiéndote mal. Entonces suena tu celular: es un LINE de Ami.)',
            '(You\\'ve felt unwell for several days. Just then your phone buzzes — a LINE message from Ami.)'),""",
 """          L('（你生病了，感覺很不舒服。手機響了，是Ami傳來的LINE。）',
            '(Estás enfermo y te sientes muy mal. Suena tu celular: es un LINE de Ami.)',
            '(You\\'re sick and feel awful. Your phone buzzes — a LINE message from Ami.)'),""", 1),
# 045 刪除
("""          L('（你走進診所，櫃台有一位護理師。）', '(Entras a la clínica; en el mostrador hay una enfermera.)', '(You walk into the clinic. A nurse is at the front desk.)'),
""", "", 1),
# 051
("""Game.good('掛號要先給櫃台看健保卡。', 'Para registrarte, primero muestras la tarjeta NHI.', 'To register, you first show your NHI card.')""",
 """Game.good('你記得沒錯喔！掛號要先給櫃台看健保卡。', '¡Lo recordaste bien! Para registrarte, primero muestras la tarjeta NHI.', 'You remembered right! To register, you first show your NHI card.')""", 1),
# 055（西文、英文原本就沒有提 Ami）
("""M('Ami說這是你第一次來這家診所。',""", """M('你是第一次來這家診所。',""", 1),
# 058 刪除（初診單旁白）
(""",
            L('（你在初診單上寫了名字、生日和電話。）', '(Escribes tu nombre, fecha de nacimiento y teléfono en el formulario.)', '(You write your name, birth date and phone number on the form.)')];""", "];", 1),
# 063
("""M('Ami說感冒掛家醫科。', 'Ami dijo que para un resfriado hay que registrarse en medicina familiar.', 'Ami said to register with family medicine for a cold.')""",
 """M('感冒應該要掛家醫科。', 'Para un resfriado hay que registrarse en medicina familiar.', 'For a cold you should register with family medicine.')""", 1),
# 065
("""Game.good('你記得感冒要掛家醫科。', 'Recordaste que""", """Game.good('不錯唷！你記得感冒要掛家醫科。', '¡Nada mal! Recordaste que""", 1),
("""'You remembered that a cold goes to family medicine.'""", """'Not bad! You remembered that a cold goes to family medicine.'""", 1),
# 073
("""Game.good('你聽到叫號，輪到自己才進去。', 'Escuchaste el llamado y entraste cuando fue tu turno.', 'You listened for the call and went in when it was your turn.')""",
 """Game.good('很好！你聽到叫號，輪到自己才進去。', '¡Muy bien! Escuchaste el llamado y entraste cuando fue tu turno.', 'Very good! You listened for the call and went in when it was your turn.')""", 1),
# 074
("""M('輪到你了，要馬上進診間，不要錯過。', 'Ya es tu turno: hay que entrar enseguida para no perderlo.', "It's your turn — go in right away so you don't miss it.")""",
 """M('輪到你了，要馬上進診間，不然會過號。', 'Ya es tu turno: hay que entrar enseguida o se pasarán a otro número.', "It's your turn — go in right away, or they'll skip your number.")""", 1),
# 078 刪除
("""[L('（你走進診間，醫生坐在桌子後面。）', '(Entras al consultorio; el doctor está sentado detrás del escritorio.)', '(You enter the exam room. The doctor sits behind the desk.)'),
          doc(""", """[doc(""", 1),
# 081
("""Game.good('你把症狀和天數都說清楚了。', 'Explicaste claramente los síntomas y los días.', 'You described your symptoms and the number of days clearly.')""",
 """Game.good('很棒喔！你把症狀和天數都說清楚了。', '¡Excelente! Explicaste claramente los síntomas y los días.', 'Great job! You described your symptoms and the number of days clearly.')""", 1),
# 090（半形問號改全形）
("""doc('有沒有對什麼藥物過敏？', '¿Es alérgico a algún medicamento?', 'Are you allergic to any medicine?')""",
 """doc('吃藥會過敏嗎？', '¿Le dan alergia los medicamentos?', 'Are you allergic to any medicine?')""", 1),
# 096
("""Game.good('有藥物過敏，一定要跟醫生說。', 'Si tienes alergia a un medicamento, siempre díselo al doctor.', 'If you have a drug allergy, always tell the doctor.')""",
 """Game.good('沒錯！有藥物過敏，一定要跟醫生說。', '¡Exacto! Si tienes alergia a un medicamento, siempre díselo al doctor.', 'Exactly! If you have a drug allergy, always tell the doctor.')""", 1),
# 098 刪除
("""next: () => { Game.thought = [L('（你拿著單子，回到櫃台。）', '(Tomas tu receta y vuelves al mostrador.)', '(You take your slip and go back to the front desk.)')]; Game.state = 'P_PAY'; }""",
 """next: () => { Game.state = 'P_PAY'; }""", 1),
# 118
("""Game.good('你記得藥什麼時候吃。', 'Recordaste cuándo tomar cada medicina.', 'You remembered when to take each medicine.')""",
 """Game.good('不錯喔！你記得藥什麼時候吃。', '¡Bien hecho! Recordaste cuándo tomar cada medicina.', 'Nice! You remembered when to take each medicine.')""", 1),
# 119
("""L('（吃完藥，你坐在位子上休息。過一會兒，Ami傳來訊息。）', '(Tomas la medicina y descansas en tu asiento. Poco después, Ami te escribe.)', '(You take the medicine and rest at your desk. A little later, Ami texts you.)')""",
 """L('（剛剛吃完藥，你正在休息。Ami傳來訊息。）', '(Acabas de tomar la medicina y estás descansando. Ami te escribe.)', '(You\\'ve just taken your medicine and are resting. Ami texts you.)')""", 1),
# 120
("""L('Ami：怎麼樣？醫生怎麼說？藥要吃幾天？', '¿Cómo te fue? ¿Qué dijo el doctor? ¿Cuántos días tienes que tomar la medicina?', 'How did it go? What did the doctor say? How many days do you take the medicine?')""",
 """L('Ami：怎麼樣？醫生怎麼說？他給你幾天的藥？', '¿Cómo te fue? ¿Qué dijo el doctor? ¿Para cuántos días te dio medicina?', 'How did it go? What did the doctor say? How many days of medicine did he give you?')""", 1),
# 127
("""Game.good('你聽懂醫生說的話，也能告訴朋友。', 'Entendiste al doctor y pudiste contárselo a tu amiga.', 'You understood the doctor and could tell your friend.')""",
 """Game.good('中文不錯喔！你聽得懂醫生說的話，也能清楚告訴朋友。', '¡Tu chino va muy bien! Entendiste al doctor y pudiste contárselo claramente a tu amiga.', 'Your Chinese is pretty good! You understood the doctor and could tell your friend clearly.')""", 1),
# 128
("""趕快好起來喔！`, `¡Qué bien!""", """趕快好起來喔！這樣才可以繼續學中文喔！`, `¡Qué bien!""", 1),
("""¡Bebe agua, duerme temprano y mejórate pronto!`""", """¡Bebe agua, duerme temprano y mejórate pronto! ¡Así podrás seguir estudiando chino!`""", 1),
("""Drink water, sleep early and get well soon!`""", """Drink water, sleep early and get well soon! That way you can keep studying Chinese!`""", 1),
# 單字表
("""  START: [['看醫生', 'ir al médico', 'see a doctor'],""", """  START: [['生病', 'enfermarse, estar enfermo', 'be sick'], ['看醫生', 'ir al médico', 'see a doctor'],""", 1),
("""['繼續', 'continuar', 'continue']],""", """['繼續', 'continuar', 'continue'], ['過號', 'perder el turno (se pasa tu número)', 'miss your number (it gets skipped)']],""", 1),
("""['止痛藥', 'analgésico', 'painkiller'], ['有沒有', '¿tiene o no?', 'do you have or not?']],""", """['止痛藥', 'analgésico', 'painkiller'], ['吃藥', 'tomar medicina', 'take medicine']],""", 1),
]
bad=0
for t in R:
    a,b=t[0],t[1]; n=t[2] if len(t)>2 else 1
    c=s.count(a)
    if c!=n: print('COUNT',c,'!=',n,'::',a[:70]); bad+=1; continue
    s=s.replace(a,b)
# 錯誤後的提示旁白刪除（083/089/095「看一下我的身體狀況卡」、117、126）：「,\n   [L('（…）', …)]); return;」改成「); return;」
THOUGHTS=[('（看一下我的身體狀況卡。）',3),('（藥師剛剛怎麼說？看一下藥袋。）',1),('（再想一下，醫生剛剛怎麼說？看一下任務提示。）',1)]
for zh,n in THOUGHTS:
    pat=re.compile(r",\n[ ]*\[L\('"+re.escape(zh)+r"', [^\n]*?\)\]\)")
    ms=pat.findall(s)
    if len(ms)!=n: print('THOUGHT COUNT',len(ms),zh); bad+=1; continue
    s=pat.sub(')',s)
if bad: sys.exit(1)
open(P,'w',encoding='utf-8').write(s); print('ok',len(R)+len(THOUGHTS))
