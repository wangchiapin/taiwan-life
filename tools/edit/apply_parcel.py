import os
import sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/parcel/index.html')
s=open(P,encoding='utf-8').read()
# 每一筆：(舊字串, 新字串[, 預期出現次數])；找不到就停
# 旁白提示：086 已刪（Ben 決定，見 apply_parcel_086.py 的做法：addMistake 不帶 thought）；067、141 也已刪（Ben 決定，同樣把 addMistake 的提示話拿掉）；063 094 098 保留
R=[
# 003 開頭介紹（半形「!」改全形）
("你租了房東太太家的一個房間，已經住一陣子了。今天早上，房東太太出門上班前，請你去巷口的超商幫忙領包裹。看清楚簡訊再去！",
 "房東太太傳訊息給你，請你去超商幫忙領包裹，要看清楚訊息內容喔！"),
("Llevas un tiempo viviendo en una habitación de la casa de tu casera. Esta mañana, antes de irse al trabajo, ella te pide que recojas unos paquetes en la tienda de conveniencia de la esquina. ¡Lee bien el mensaje antes de ir!",
 "La casera te manda un mensaje y te pide que vayas a la tienda de conveniencia a recoger unos paquetes. ¡Lee bien el contenido del mensaje!", 2),
("You've been renting a room in your landlady's home for a while. This morning, before leaving for work, she asks you to pick up some parcels at the convenience store on the corner. Read the text message carefully before you go!",
 "Your landlady sends you a message asking you to pick up some parcels at the convenience store. Read the message carefully!", 1),
# 017 住處→小窩（開始畫面的位置列＋之後的位置名稱）
('<div class="who" id="place-who">住處</div>','<div class="who" id="place-who">小窩</div>'),
("home:   ['🏠', '住處',","home:   ['🏠', '小窩',"),
# 022 + 023（023 刪除，併入 022）
("""      L(`我的包裹到了，幫我去${t.store}拿，是取貨付款，錢在桌上。`,
        `Llegó mi paquete. Ve a recogerlo a ${stES(t.store)}; es de pago al recoger y el dinero está en la mesa.`,
        `My parcel has arrived. Please pick it up at ${stEN(t.store)}; it's pay-on-pickup, and the money is on the table.`),
      L(`取件人是我，${t.momName}，手機末三碼${t.momTail}。`,
        `La destinataria soy yo, ${rom(t.momName)}, y los últimos tres dígitos de mi celular son ${sp(t.momTail)}.`,
        `The recipient is me, ${rom(t.momName)}, and the last three digits of my phone number are ${sp(t.momTail)}.`),
""",
"""      L(`可以麻煩你幫我去${t.store}拿包裹嗎？是取貨付款，錢在桌上。取件人是我，${t.momName}，手機末三碼${t.momTail}。`,
        `¿Podrías ir a recoger mi paquete a ${stES(t.store)}? Es de pago al recoger y el dinero está en la mesa. La destinataria soy yo, ${rom(t.momName)}, y los últimos tres dígitos de mi celular son ${sp(t.momTail)}.`,
        `Could you please go pick up my parcel at ${stEN(t.store)}? It's pay-on-pickup, and the money is on the table. The recipient is me, ${rom(t.momName)}, and the last three digits of my phone number are ${sp(t.momTail)}.`),
"""),
# 024
("""      L(`順便幫我的悠遊卡加值${t.cardTop}元。家裡塑膠袋太多了，不要再買袋子喔！`,
        `De paso, recarga mi EasyCard con ${esM(t.cardTop)}. En casa hay demasiadas bolsas de plástico: ¡no compres más bolsas!`,
        `While you're there, please top up my EasyCard with ${enM(t.cardTop)}. We have too many plastic bags at home, so don't buy any more bags!`)""",
"""      L(`順便幫我加值一下悠遊卡，加${t.cardTop}元。對了，家裡很多塑膠袋了，不要再買袋子喔！`,
        `De paso, recárgame un poco la EasyCard: ${esM(t.cardTop)}. Ah, y en casa ya hay muchas bolsas de plástico: ¡no compres más bolsas!`,
        `While you're there, please top up my EasyCard, ${enM(t.cardTop)}. Oh, and we already have a lot of plastic bags at home, so don't buy any more!`)"""),
# 042
("""          L('（今天早上，房東太太出門上班前傳了LINE給你，你的手機也收到了一則簡訊。）',
            '(Esta mañana, antes de irse al trabajo, la casera te mandó un mensaje de LINE, y tu celular también recibió un SMS.)',
            '(This morning, before leaving for work, your landlady sent you a LINE message, and your phone also got a text message.)'),""",
"""          L('（今天早上，房東太太傳LINE給你。另外，你還收到了一封簡訊。）',
            '(Esta mañana, la casera te mandó un mensaje de LINE. Además, recibiste un SMS.)',
            '(This morning, your landlady sent you a LINE message. You also got a text message.)'),"""),
# 043
("""L('（上面的「看手機」按鈕，隨時可以再打開來看。）',
            '(Puedes volver a abrir el botón «Ver celular» de arriba cuando quieras.)',""",
"""L('（上面的「看手機」按鈕，可以隨時打開來看。）',
            '(Puedes abrir el botón «Ver celular» de arriba en cualquier momento.)',"""),
# 050
("L('（看一下簡訊上的取件門市……）', '(Mira la tienda de recogida en el mensaje…)', '(Check the pickup store in the text message…)')",
 "L('（看一下是哪一間取件門市……）', '(Mira cuál es la tienda de recogida…)', '(Check which store is the pickup store…)')"),
# 051
("Game.good('你先看了簡訊，去對了門市。', 'Leíste el mensaje primero y fuiste a la tienda correcta.', 'You checked the text message first and went to the right store.')",
 "Game.good('還好你有確認，先看了簡訊，去對了門市。', 'Menos mal que confirmaste: leíste el mensaje primero y fuiste a la tienda correcta.', 'Good thing you checked: you read the text message first and went to the right store.')"),
# 074
("Game.good('你發現包裹上的名字不對。', 'Notaste que el nombre del paquete no era el correcto.', 'You noticed the name on the parcel was wrong.')",
 "Game.good('哇！你發現包裹上的名字不對欸！', '¡Wow! ¡Notaste que el nombre del paquete no era el correcto!', 'Wow! You noticed the name on the parcel was wrong!')"),
# 079
("M('簡訊上寫「取貨付款」，要現在付。'","M('簡訊上寫「取貨付款」，要現在付錢。'"),
# 084
("`少找了錢，應該找${money(Game._change)}。`","`少找錢了，應該找${money(Game._change)}。`"),
# 087
("Game.good('你發現店員少找錢，還說出來了！', 'Notaste que el cambio estaba mal y lo dijiste.', 'You noticed the wrong change and spoke up!')",
 "Game.good('很棒喔！你發現店員少找錢！', '¡Muy bien! ¡Notaste que el cambio estaba mal!', 'Great job! You noticed the clerk gave you too little change!')"),
# 099 / 121（兩處同句）
("L('店員：這個已經付過款了，麻煩在螢幕上按「確認取貨」。',","L('店員：這個已經付過了，麻煩在螢幕上按「確認取貨」。',", 2),
# 104 / 126
("L('店員：好了。還有其他需要嗎？', 'Listo. ¿Necesita algo más?', 'All done. Anything else?')","L('店員：好了。還需要什麼嗎？', 'Listo. ¿Necesita algo más?', 'All done. Anything else?')"),
("L('店員：還有其他需要嗎？', '¿Necesita algo más?', 'Anything else?')","L('店員：還需要什麼嗎？', '¿Necesita algo más?', 'Anything else?')"),
# 110 / 117（兩處同句）
("Game.good('你看了簡訊，知道包裹還沒到。', 'Leíste el mensaje y supiste que tu paquete aún no llegaba.', 'You read the text and knew your parcel hadn\\'t arrived yet.')",
 "Game.good('聰明喔！你有再看一次簡訊，知道包裹還沒到。', '¡Qué listo! Volviste a leer el mensaje y supiste que tu paquete aún no llegaba.', 'Smart! You read the text again and knew your parcel hadn\\'t arrived yet.')", 2),
# 118
("L('店員：沒關係，到了會再傳簡訊給您。', 'No hay problema; cuando llegue le mandarán un mensaje.', \"No problem, you'll get a text when it arrives.\")",
 "L('店員：沒關係，到了應該會傳簡訊給您。', 'No hay problema; cuando llegue, seguramente le mandarán un mensaje.', \"No problem, you should get a text when it arrives.\")"),
# 127（選項＋判斷）
("'我要幫悠遊卡加值。'","'我要加值悠遊卡。'"),
("c.startsWith('我要幫')","c.startsWith('我要加值')"),
# 130 / 131
("M('房東太太還請你幫悠遊卡加值。'","M('房東太太還有請你幫忙加值悠遊卡。'"),
("L('（等等，房東太太還交代了一件事……）'","L('（等等，房東太太還有說一件事……）'"),
# 145（錯誤選項）
("'把卡插進收銀機'","'把卡放在櫃台上'"),
# 單字：選項裡不再有「插」，換成「櫃台」；結局新增「油飯」
("['插', 'insertar', 'insert']","['櫃台', 'mostrador', 'counter']"),
("['習慣', 'acostumbrarse', 'get used to']","['習慣', 'acostumbrarse', 'get used to'], ['油飯', 'yóufàn (arroz glutinoso con aceite)', 'oil rice (savory sticky rice)']"),
# 新字的台灣讀音：還需要（hái）、欸（ēi）
("'還好': 'hái hǎo', '還多': 'hái duō',","'還好': 'hái hǎo', '還需': 'hái xū', '欸': 'ēi', '還多': 'hái duō',"),
# 154
("Game.good('你記得房東太太說不要再買袋子。', 'Recordaste que la casera dijo que no compraras más bolsas.', 'You remembered the landlady said not to buy more bags.')",
 "Game.good('太好了！你記得房東太太說不要買袋子。', '¡Muy bien! Recordaste que la casera dijo que no compraras bolsas.', 'Great! You remembered the landlady said not to buy bags.')"),
# 155
("const zhItems = ['您的包裹',","const zhItems = ['你的包裹',"),
# 159 + 160（160 刪除，併入 159；沒到才加這句，跟原本一樣）
("""            L(`我：房東太太，${zhItems.join('、')}都拿回來了，悠遊卡也加值了${t.cardTop}元。`,
              `Casera, ya traje ${joinEs(esItems)}, y también recargué la EasyCard con ${esM(t.cardTop)}.`,
              `Landlady, I brought back ${joinEn(enItems)}, and I topped up the EasyCard with ${enM(t.cardTop)}.`)
          ];
          if (!t.yourArrived) lines.push(L(`我：我的包裹還沒到，簡訊說${md(2)}才會到。`, `Mi paquete aún no llega; el mensaje dice que llegará el ${md(2)}.`, `My parcel hasn't arrived yet; the text says it will arrive on ${md(2)}.`));
""",
"""            L(`我：房東太太，${zhItems.join('、')}都拿回來了，悠遊卡也加值了${t.cardTop}元。${t.yourArrived ? '' : '結果我自己的包裹還沒到，' + md(2) + '才會到。'}`,
              `Casera, ya traje ${joinEs(esItems)}, y también recargué la EasyCard con ${esM(t.cardTop)}.${t.yourArrived ? '' : ' Al final, mi propio paquete aún no llega; llegará el ' + md(2) + '.'}`,
              `Landlady, I brought back ${joinEn(enItems)}, and I topped up the EasyCard with ${enM(t.cardTop)}.${t.yourArrived ? '' : " As it turns out, my own parcel hasn't arrived yet; it will arrive on " + md(2) + '.'}`)
          ];
"""),
# 162
("L(`房東太太：哇，${N}，你真厲害！以後包裹都靠你了！`, `¡Vaya, ${N}, eres genial! ¡De ahora en adelante los paquetes quedan en tus manos!`, `Wow, ${N}, you're amazing! From now on, I'll leave the parcels to you!`)",
 "L(`房東太太：哇，${N}，你真厲害！那，這個油飯給你！很好吃喔！`, `¡Vaya, ${N}, eres genial! Entonces, ¡este yóufàn (arroz glutinoso con aceite) es para ti! ¡Está muy rico!`, `Wow, ${N}, you're amazing! Then this oil rice (yóufàn) is for you! It's really tasty!`)"),
# 163
("L('房東太太：謝謝你！有些小地方要再注意，慢慢就習慣了。', '¡Gracias! Hay unos detallitos que cuidar, pero poco a poco te acostumbrarás.', \"Thank you! There are a few small things to watch out for, but you'll get used to it.\")",
 "L('房東太太：謝謝你！中文很難吼，慢慢就習慣了啦。', '¡Gracias! El chino es difícil, ¿verdad? Poco a poco te acostumbrarás.', \"Thank you! Chinese is hard, huh? You'll get used to it little by little.\")"),
]
bad=0
for r in R:
    a,b=r[0],r[1]; want=r[2] if len(r)>2 else None
    n=s.count(a)
    if n<1 or (want is not None and n!=want): print('MISSING/COUNT:',n,want,a[:90]); bad+=1; continue
    s=s.replace(a,b)
if bad: sys.exit(1)
open(P,'w',encoding='utf-8').write(s); print('ok',len(R))
