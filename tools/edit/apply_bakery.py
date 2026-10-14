import os
import re
import sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/bakery/index.html')
s=open(P,encoding='utf-8').read()
# 每一筆：(舊字串, 新字串[, 預期出現次數])；找不到就停
# 括號內的編號是線上修改表的列號（rows/bakery.json）
R=[
# 003 開頭介紹（西文在 data-es 和 span 各一次）
(r"""週六早上，你跟同事 Ami 約好，一起去她家附近的麵包店買早餐。Ami 在外面講電話，你先進去：自己拿托盤和夾子，夾麵包、結帳，還要幫 Ami 訂一個生日蛋糕。小心，Ami 對堅果過敏！""",
 r"""你跟Ami一起去麵包店買麵包，Ami臨時接到電話，要你先進去買。除了買麵包，還要幫Ami訂一個生日蛋糕喔！小心，Ami 對堅果過敏！""", 1),
(r"""Es sábado por la mañana y quedaste con tu compañera Ami para desayunar en una panadería cerca de su casa. Ami está afuera hablando por teléfono, así que entras tú primero: tomas la bandeja y las pinzas, eliges el pan, pagas y además encargas un pastel de cumpleaños para Ami. ¡Ojo: Ami es alérgica a los frutos secos!""",
 r"""Vas con Ami a la panadería a comprar pan, pero a Ami le entra una llamada de última hora y te pide que entres tú primero. ¡Además del pan, tienes que encargar un pastel de cumpleaños para Ami! ¡Ojo: Ami es alérgica a los frutos secos!""", 2),
(r"""It's Saturday morning, and you and your coworker Ami are going to a bakery near her place for breakfast. Ami is outside on a phone call, so you go in first: take a tray and tongs, pick the bread, pay, and also order a birthday cake for Ami. Careful — Ami is allergic to nuts!""",
 r"""You and Ami go to a bakery to buy bread, but Ami suddenly gets a phone call and asks you to go in first. Besides the bread, you also need to order a birthday cake for Ami! Careful — Ami is allergic to nuts!""", 1),
# 016
(r"""      L(`Ami：${N}，你先進去，我在外面接個電話，馬上進來！`,
        `${N}, entra tú primero; estoy contestando una llamada afuera y entro enseguida.`,
        `${N}, go in first. I'm taking a phone call outside and I'll be right in!`),""",
 r"""      L(`Ami：${N}，你先進去，我接個電話。`,
        `${N}, entra tú primero; voy a contestar una llamada.`,
        `${N}, go in first. I'm going to take a call.`),"""),
# 017 + 018（018 併入 017）
(r"""      L(`Ami：我要${nz}個${bz}。你自己也選一個別種的，但是不要有堅果的，我對堅果過敏，我們可能會分著吃。`,
        `Quiero ${t.n} ${BREAD_ES[t.bread]}. Tú elige también uno de otro tipo, pero sin frutos secos: soy alérgica y quizás lo compartamos.`,
        `I want ${t.n} ${BREAD_EN[t.bread]}. Pick one of a different kind for yourself, but nothing with nuts — I'm allergic, and we might share.`),
      L(`Ami：還要一條吐司，請店員幫忙切成${sz}片。`,
        `También una barra de pan de molde: pídele a la dependienta que la corte en ${t.slice} rebanadas.`,
        `Also one loaf of sandwich bread. Ask the clerk to slice it into ${t.slice} slices.`),""",
 r"""      L(`Ami：我要${nz}個${bz}。你看你另外要吃什麼，但是不要買有堅果的喔！我也想吃你買的。對了！再買一條吐司，請店員切成${sz}片。`,
        `Quiero ${t.n} ${BREAD_ES[t.bread]}. Mira qué otro pan quieres tú, pero ¡no compres nada con frutos secos! Yo también quiero probar lo que compres. ¡Ah, y también una barra de pan de molde: pídele a la dependienta que la corte en ${t.slice} rebanadas!`,
        `I want ${t.n} ${BREAD_EN[t.bread]}. Pick whatever else you'd like, but don't buy anything with nuts! I want to eat what you buy too. Oh, and get one loaf of sandwich bread — ask the clerk to slice it into ${t.slice} slices.`),"""),
# 020
(r"""      L('Ami：還有，店員如果問要不要辦會員，不用辦喔。',
        'Y si la dependienta pregunta si quieres hacerte miembro, no hace falta.',
        "And if the clerk asks whether you want to sign up for a membership, no need.")""",
 r"""      L('Ami：還有，不需要辦會員喔。',
        'Y no hace falta que te hagas miembro.',
        "Also, no need to sign up for a membership.")"""),
# 022
(r"""      L(`Ami：${N}，麻煩你順便去櫃台幫我訂一個蛋糕，是我朋友${t.friend}的生日蛋糕！`,
        `${N}, de paso, ¿puedes pedir un pastel en el mostrador? Es el pastel de cumpleaños de mi amiga ${t.friend}.`,
        `${N}, while you're there, could you order a cake at the counter? It's for my friend ${t.friend}'s birthday!`),""",
 r"""      L(`Ami：${N}，幫我訂一個生日蛋糕，要給我朋友${t.friend}的！`,
        `${N}, ¿puedes encargar un pastel de cumpleaños por mí? ¡Es para mi amiga ${t.friend}!`,
        `${N}, could you order a birthday cake for me? It's for my friend ${t.friend}!`),"""),
# 023 + 024 + 025（024、025 併入 023；「要要」筆誤改成一個「要」）
(r"""      L(`Ami：${t.friend}家有${NZ(t.people)}個人要吃，口味要${t.flavor}的，我也要吃，所以不要堅果。`,
        `En casa de ${t.friend} van a comer ${t.people} personas; el sabor, de ${fl[0]}. Yo también voy a comer, así que sin frutos secos.`,
        `There are ${t.people} people eating at ${t.friend}'s place, and the flavor should be ${fl[1]}. I'll eat some too, so no nuts.`),
      L(`Ami：蠟燭要${NZ(t.candles)}根，巧克力片寫「${t.friend}，生日快樂」。`,
        `Las velas: ${t.candles}. En la plaquita de chocolate, escribe «${t.friend}, feliz cumpleaños».`,
        `${t.candles} candles, and on the chocolate plaque write "${t.friend}, happy birthday".`),
      L(`Ami：我們${t.pickup}來拿。`, `Vendremos a recogerlo ${PICKUP_ES[t.pickup]}.`, `We'll come pick it up ${PICKUP_EN[t.pickup]}.`)""",
 r"""      L(`Ami：有${NZ(t.people)}個人要吃，${t.flavor}口味的，因為我也會吃，所以不要有堅果的。跟店員要${NZ(t.candles)}根蠟燭，巧克力片寫「${t.friend}，生日快樂」。我們${t.pickup}來拿。`,
        `Van a comer ${t.people} personas, de sabor ${fl[0]}; como yo también voy a comer, que no lleve frutos secos. Pídele a la dependienta ${t.candles} velas, y que en la plaquita de chocolate escriba «${t.friend}, feliz cumpleaños». Vendremos a recogerlo ${PICKUP_ES[t.pickup]}.`,
        `${t.people} people will eat it, ${fl[1]} flavor, and since I'll eat some too, no nuts. Ask the clerk for ${t.candles} candles, and have the chocolate plaque say "${t.friend}, happy birthday". We'll pick it up ${PICKUP_EN[t.pickup]}.`)"""),
# 031 刪除（蛋糕清單沒有這句了）＋ 036
(r"""      rule = L('蛋糕訂好之前，要確認店員寫的對不對。', 'Antes de terminar, comprueba que lo que anotó la dependienta sea correcto.', 'Before you finish, check that what the clerk wrote down is correct.');""",
 r"""      rule = null;"""),
(r"""      rule = L('我對堅果過敏，所以不要買有堅果的。', 'Soy alérgica a los frutos secos: no compres nada que los lleve.', "I'm allergic to nuts, so don't buy anything with nuts.");""",
 r"""      rule = L('Ami對堅果過敏。', 'Ami es alérgica a los frutos secos.', 'Ami is allergic to nuts.');"""),
(r"""    const all = [...rows, rule];""", r"""    const all = rule ? [...rows, rule] : rows;"""),
(r"""      `<div class="rule">${r(rule.zh)}</div></div>`;""", r"""      (rule ? `<div class="rule">${r(rule.zh)}</div>` : '') + '</div>';"""),
# 039 開場旁白刪除
(r"""          L('（週六早上，你跟Ami約好，一起去她家附近的麵包店買早餐。）',
            '(Es sábado por la mañana. Quedaste con Ami para comprar el desayuno en la panadería cerca de su casa.)',
            '(It\'s Saturday morning. You and Ami are going to a bakery near her place to buy breakfast.)'),
          ...Game.amiLines(),""",
 r"""          ...Game.amiLines(),"""),
# 044
(r"""L('（前面的客人拿起夾子，先「喀喀」空夾了兩下，才去夾麵包。）', '(El cliente de delante toma las pinzas y las cierra dos veces en el aire —clic, clic— antes de ir por el pan.)', '(The customer ahead picks up the tongs and clicks them twice in the air — click, click — before reaching for the bread.)')""",
 r"""L('（喀喀喀！是什麼聲音呢？）', '(¡Clic, clic, clic! ¿Qué será ese ruido?)', "(Click, click, click! What's that sound?)")"""),
# 047 綠卡
(r"""Game.good('在台灣，很多人拿夾子會先「喀喀」空夾兩下，再去夾麵包。', 'En Taiwán muchas personas cierran las pinzas dos veces en el aire (clic, clic) antes de tomar el pan.', 'In Taiwan, many people click the tongs twice in the air before picking up bread.')""",
 r"""Game.good('你越來越像台灣人了喔！在台灣，很多人拿夾子會先「喀喀」空夾兩下，再去夾麵包。', '¡Cada vez te pareces más a un taiwanés! En Taiwán muchas personas cierran las pinzas dos veces en el aire (clic, clic) antes de tomar el pan.', "You're becoming more and more like a Taiwanese person! In Taiwan, many people click the tongs twice in the air before picking up bread.")"""),
# 048
(r"""L('（喀喀！你空夾了兩下，覺得自己好像在地人了。）', '(¡Clic, clic! Sientes que ya pareces un local.)', '(Click, click! You feel like a local already.)')""",
 r"""L('（喀喀！你空夾了兩下，覺得自己好像變成台灣人了。）', '(¡Clic, clic! Sientes que te has vuelto un poco taiwanés.)', '(Click, click! You feel like you\'ve become a bit Taiwanese.)')"""),
# 049 沒空夾的提示話刪除
(r"""          } else {
            Game.thought = [L('（你拿起夾子，走向麵包架。）', '(Tomas las pinzas y vas hacia los estantes de pan.)', '(You pick up the tongs and head to the bread shelves.)')];
          }""",
 r"""          }"""),
# 050 麵包區沒有旁白了
(r"""dialogue: () => [L('（架上的麵包都有標籤，寫著名字、價錢，有些還寫了成分。）', '(Cada pan tiene una etiqueta con nombre y precio; algunos indican sus ingredientes.)', '(Each bread has a label with its name and price, and some list ingredients.)')],""",
 r"""dialogue: () => [],"""),
# 060 綠卡
(r"""Game.good('你看清楚清單和標籤，沒有買到堅果。', 'Leíste bien la lista y las etiquetas: no compraste frutos secos.', 'You read the list and labels carefully and avoided nuts.')""",
 r"""Game.good('很棒！你記得Ami說過的，沒有買到堅果。', '¡Muy bien! Recordaste lo que dijo Ami: no compraste frutos secos.', 'Great! You remembered what Ami said and avoided nuts.')"""),
# 062
(r"""M(`標籤寫「含${it.nut}」，Ami對堅果過敏。`, `La etiqueta dice «contiene ${it.nutEs}»; Ami es alérgica a los frutos secos.`, `The label says it contains ${it.nutEn}; Ami is allergic to nuts.`)""",
 r"""M(`你買的麵包含${it.nut}，Ami對堅果過敏。`, `El pan que compraste contiene ${it.nutEs}; Ami es alérgica a los frutos secos.`, `The bread you bought contains ${it.nutEn}; Ami is allergic to nuts.`)"""),
# 066 櫃台旁白刪除
(r"""          L('（你把托盤拿到櫃台。）', '(Llevas la bandeja al mostrador.)', '(You carry the tray to the counter.)'),
""", r""""""),
# 075 綠卡
(r"""Game.good('你記得吐司要切幾片。', 'Recordaste en cuántas rebanadas cortar el pan.', 'You remembered how many slices to cut.')""",
 r"""Game.good('不錯喔！你記得吐司要切幾片。', '¡Bien! Recordaste en cuántas rebanadas cortar el pan.', 'Nice! You remembered how many slices to cut.')"""),
# 080 + 081
(r"""M(t.heat ? 'Ami想吃熱的，麵包要加熱。' : 'Ami說不用加熱，他們要去公園吃。', t.heat ? 'Ami quería comerlo caliente: había que calentar el pan.' : 'Ami dijo que no hacía falta calentarlo: lo comerán en el parque.', t.heat ? 'Ami wanted it warm, so the bread should be heated.' : 'Ami said no heating — they\'re eating at the park.')""",
 r"""M(t.heat ? 'Ami說麵包要加熱。' : 'Ami說麵包不用加熱。', t.heat ? 'Ami dijo que había que calentar el pan.' : 'Ami dijo que no hacía falta calentar el pan.', t.heat ? 'Ami said the bread should be heated.' : 'Ami said the bread doesn\'t need heating.')"""),
# 083 綠卡
(r"""Game.good('你記得Ami說的：' + (t.heat ? '要加熱。' : '不用加熱。'), 'Recordaste lo que dijo Ami sobre calentar el pan.', 'You remembered what Ami said about heating the bread.')""",
 r"""Game.good('讚喔！你記得Ami說的：' + (t.heat ? '要加熱。' : '不用加熱。'), '¡Genial! Recordaste lo que dijo Ami sobre calentar el pan.', 'Awesome! You remembered what Ami said about heating the bread.')"""),
# 097 綠卡
(r"""Game.good('你禮貌地拒絕了辦會員。', 'Rechazaste con educación hacerte miembro.', 'You politely declined the membership.')""",
 r"""Game.good('很好！你禮貌地拒絕了辦會員。', '¡Muy bien! Rechazaste con educación hacerte miembro.', 'Well done! You politely declined the membership.')"""),
# 107
(r"""L('（你走到蛋糕櫃台。）', '(Vas al mostrador de pasteles.)', '(You walk to the cake counter.)')""",
 r"""L('（你走到櫃台。）', '(Vas al mostrador.)', '(You walk to the counter.)')"""),
# 114 綠卡
(r"""Game.good('你用人數選對了蛋糕的大小。', 'Elegiste bien el tamaño según el número de personas.', 'You chose the right size for the number of people.')""",
 r"""Game.good('厲害喔！你用人數選對了蛋糕的大小。', '¡Genial! Elegiste bien el tamaño según el número de personas.', 'Impressive! You chose the right size for the number of people.')"""),
# 118
(r"""M(`Ami說口味要${t.flavor}的。`""", r"""M(`Ami說要${t.flavor}口味的。`"""),
# 133 綠卡
(r"""Game.good('你記得朋友的名字。', 'Recordaste el nombre de la amiga/o.', 'You remembered the friend\'s name.')""",
 r"""Game.good('很好！你記得Ami朋友的名字。', '¡Muy bien! Recordaste el nombre de la amiga/o de Ami.', 'Well done! You remembered Ami\'s friend\'s name.')"""),
# 147
(r"""M('店員複誦的都是對的。', 'Todo lo que repitió la dependienta era correcto.', 'Everything the clerk repeated was correct.')""",
 r"""M('店員確認的都是對的。', 'Todo lo que confirmó la dependienta era correcto.', 'Everything the clerk confirmed was correct.')"""),
# 155 綠卡
(r"""Game.good('你聽出來店員講錯了！', '¡Notaste que la dependienta se equivocó!', 'You caught the clerk\'s mistake!')""",
 r"""Game.good('厲害喔！你聽出來店員講錯了！', '¡Impresionante! ¡Notaste que la dependienta se equivocó!', 'Impressive! You caught the clerk\'s mistake!')"""),
# 157
(r"""sayK('好，請問怎麼稱呼？我要寫一下取貨人的名字。', 'Bien, ¿cómo se llama? Necesito anotar el nombre de quien recogerá el pedido.', 'OK, what\'s your name? I need to write down who\'s picking it up.')""",
 r"""sayK('好，請問怎麼稱呼？', 'Bien, ¿cómo se llama?', 'OK, what\'s your name?')"""),
# 164（補上句尾的「）」）
(r"""L('（蛋糕訂好了。這時候，Ami講完電話，走進麵包店。）', '(El pastel está encargado. En ese momento, Ami termina su llamada y entra a la panadería.)', '(The cake is ordered. Just then, Ami finishes her call and walks into the bakery.)')""",
 r"""L('（蛋糕訂好了，Ami也剛好講完電話，走進麵包店。）', '(El pastel está encargado, y Ami también termina justo su llamada y entra a la panadería.)', '(The cake is ordered, and Ami also happens to finish her call and walks into the bakery.)')"""),
# 166（Ben 同意：空夾過才稱讚夾子；沒空夾的玩家用一般的稱讚）
(r"""              ? L(`Ami：哇，${N}，你好厲害！連夾子都夾得像台灣人！我們去公園吃吧！`, `¡Vaya, ${N}, qué bien! ¡Hasta usas las pinzas como un taiwanés! ¡Vamos a comer al parque!`, `Wow, ${N}, you're great! You even handle the tongs like a Taiwanese person! Let's go eat at the park!`)""",
 r"""              ? (Game.clickedTongs
                ? L(`Ami：哇，${N}，你好厲害！連拿夾子的時候都變成台灣人的樣子了！我們去公園吃吧！`, `¡Vaya, ${N}, qué bien! ¡Hasta cuando usas las pinzas pareces un taiwanés! ¡Vamos a comer al parque!`, `Wow, ${N}, you're great! Even the way you handle the tongs makes you look Taiwanese! Let's go eat at the park!`)
                : L(`Ami：哇，${N}，你好厲害！我們去公園吃吧！`, `¡Vaya, ${N}, qué bien! ¡Vamos a comer al parque!`, `Wow, ${N}, you're great! Let's go eat at the park!`))"""),
# 167
(r"""L('Ami：辛苦了！有些地方下次再注意就好。我們去公園吃吧！', '¡Gracias por el esfuerzo! La próxima vez cuida unos detallitos. ¡Vamos a comer al parque!', "Thanks for your hard work! Just watch a few details next time. Let's go eat at the park!")""",
 r"""L('Ami：感謝你！下次買麵包再給你練習一次吧！我們去公園吃吧！', '¡Gracias! La próxima vez que compremos pan, ¡te dejo practicar otra vez! ¡Vamos a comer al parque!', "Thank you! Next time we buy bread, I'll let you practice again! Let's go eat at the park!")"""),
# 單字：對話裡已經沒有的詞，換成新出現的詞
(r"""['順便', 'de paso', 'while you are at it'],""", r"""['朋友', 'amigo/a', 'friend'],"""),
(r"""['複誦', 'repetir lo dicho', 'repeat back'],""", r"""['這樣對嗎', '¿es correcto?', 'is that right?'],"""),
(r"""['取貨人', 'quien recoge el pedido', 'person picking up'],""", r"""['朋友', 'amigo/a', 'friend'],"""),
]
bad=0
for r in R:
    a,b=r[0],r[1]; want=r[2] if len(r)>2 else None
    n=s.count(a)
    if n<1 or (want is not None and n!=want): print('MISSING/COUNT:',n,want,a[:90]); bad+=1; continue
    s=s.replace(a,b)
# 旁白提示話刪除（錯誤卡不再帶提示話）：把「),\n   [L('（…）', …)]);」改成「));」
THOUGHTS=['（看一下清單，Ami要幾個？）','（吐司呢？Ami說要一條。）','（Ami說，你自己選一個別種的。）','（Ami說要切幾片？）','（Ami說麵包要不要加熱？）',
 '（Ami說要不要分開裝？）','（Ami說會員要不要辦？）','（朋友家有幾個人要吃？）','（Ami傳的訊息，口味是什麼？）','（朋友叫什麼名字？）',
 '（Ami說什麼時候來拿？）','（再核對一次Ami的訊息……都對耶。）','（再聽一次店員剛剛說的……）']
for zh in THOUGHTS:
    pat=re.compile(r",\n[ ]*\[L\('"+re.escape(zh)+r"', [^\n]*?\)\]\)")
    ms=pat.findall(s)
    if len(ms)!=1: print('THOUGHT COUNT',len(ms),zh); bad+=1; continue
    s=pat.sub(')',s,count=1)
if bad: sys.exit(1)
open(P,'w',encoding='utf-8').write(s); print('ok',len(R)+len(THOUGHTS))
