import os
import sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/breakfast/index.html')
s=open(P,encoding='utf-8').read()
# 每一筆：(舊字串, 新字串[, 預期出現次數])；找不到就停
R=[
# 002 開頭介紹
("你在陳姐的早餐店打工一陣子了。今天陳姐去市場，陳大哥在後面做早餐，櫃台交給你。聽懂客人要什麼！",
 "你在陳姐的早餐店打工，陳姐說她要去市場買東西，請你幫忙先顧店，櫃台交給你，做早餐的工作就交給陳大哥。"),
("Llevas un tiempo trabajando a medio tiempo en el desayunador de la señora Chen. Hoy ella va al mercado y el señor Chen cocina atrás: tú atiendes el mostrador. ¡Entiende lo que piden los clientes!",
 "Trabajas a medio tiempo en el desayunador de la señora Chen. Ella dice que va al mercado a comprar unas cosas y te pide que cuides la tienda un rato: el mostrador queda a tu cargo y el señor Chen se encarga de preparar el desayuno.", 2),
("You've been working part-time at Ms. Chen's breakfast shop for a while. Today she's going to the market and Mr. Chen is cooking in the back, so you're running the counter. Understand what the customers order!",
 "You work part-time at Ms. Chen's breakfast shop. She says she's going to the market to buy a few things and asks you to watch the shop for a while: the counter is yours, and Mr. Chen takes care of making the breakfast.", 1),
# 005-010 過場按鈕
("HEAR: '聽客人說', PICKUP: '聽客人說'","HEAR: '聽客人點餐', PICKUP: '聽客人點餐'"),
("ORDER: '寫點單'","ORDER: '點餐'"),
("DINE: '接著問客人'","DINE: '繼續問客人'"),
("BYE: '把早餐交給客人'","BYE: '把早餐給客人'"),
# 018/020/023/026 一位→一個
("L('（一位穿西裝的先生急急忙忙走進來。）'","L('（一個穿西裝的先生急急忙忙走進來。）'"),
("L('（一位伯伯慢慢走進來，跟你揮揮手。）'","L('（一個伯伯慢慢走進來，跟你揮揮手。）'"),
("L('（一位媽媽帶著小朋友走進來。）'","L('（一個媽媽帶著小朋友走進來。）'"),
("L('（一位小姐一邊看手機一邊走進來。）'","L('（一個小姐一邊看手機一邊走進來。）'"),
# 027 林小姐
("L('林小姐：你好，我是林小姐，我有打電話訂早餐。', 'Hola, soy la señorita Lin. Pedí el desayuno por teléfono.', \"Hi, I'm Ms. Lin. I ordered breakfast by phone.\")",
 "L('林小姐：你好，我有打電話訂早餐，我姓林。', 'Hola, pedí el desayuno por teléfono; mi apellido es Lin.', \"Hi, I ordered breakfast by phone. My last name is Lin.\")"),
# 029 + 030（030 刪除，併入 029）
("""          L(`陳姐：${N}，早安！我要去市場買菜，大概一個小時回來。`,
            `¡Buenos días, ${N}! Voy al mercado a hacer las compras; vuelvo en más o menos una hora.`,
            `Good morning, ${N}! I'm going to the market; I'll be back in about an hour.`),
          L('陳姐：陳大哥在後面煎台做早餐，櫃台就交給你囉！',
            'El señor Chen va a cocinar atrás en la plancha; ¡el mostrador queda a tu cargo!',
            "Mr. Chen will be cooking at the griddle in the back. The counter is all yours!"),
""",
"""          L(`陳姐：${N}，早安！我要去一下市場，大概一個小時後回來。櫃台就先交給你囉！`,
            `¡Buenos días, ${N}! Voy un momento al mercado; vuelvo en más o menos una hora. ¡Por ahora el mostrador queda en tus manos!`,
            `Good morning, ${N}! I'm heading to the market for a bit; I'll be back in about an hour. I'm leaving the counter to you for now!`),
"""),
# 031
("""          L('陳姐：客人點什麼，你就在點單上點。客人常常說簡稱：「大冰奶」就是大杯冰奶茶，「中冰紅」就是中杯冰紅茶，「中熱奶」就是中杯熱奶茶。',
            'Marca en la comanda lo que pidan los clientes. Muchas veces usan abreviaturas: «dà bīng nǎi» es un té con leche frío grande, «zhōng bīng hóng» es un té negro frío mediano y «zhōng rè nǎi» es un té con leche caliente mediano.',
            'Mark whatever customers order on the order slip. They often use short names: "dà bīng nǎi" is a large iced milk tea, "zhōng bīng hóng" is a medium iced black tea, and "zhōng rè nǎi" is a medium hot milk tea.'),
""",
"""          L('陳姐：客人要點什麼，你就在點單機上點。你還記得大杯冰奶茶我們會說成什麼吧？「大冰奶」啦！「中冰紅」就是中杯冰紅茶，自己多學一下啦！',
            'Lo que pidan los clientes, lo marcas en la máquina de pedidos. ¿Te acuerdas de cómo decimos «té con leche frío grande», verdad? ¡«dà bīng nǎi»! Y «zhōng bīng hóng» es un té negro frío mediano. ¡Aprende un poco más por tu cuenta!',
            'Whatever customers order, you enter it on the ordering machine. You remember what we call a large iced milk tea, right? "Dà bīng nǎi"! And "zhōng bīng hóng" is a medium iced black tea. Pick up a bit more on your own!'),
"""),
# 032 + 033（033 刪除，併入 032）
("""          L('陳姐：鐵板麵今天賣完了，記得跟客人說。', 'Hoy se acabaron los fideos a la plancha; acuérdate de avisar a los clientes.', 'The griddle noodles are sold out today; remember to tell the customers.'),
          L(`陳姐：還有，王伯伯每天都會來，他說「老樣子」就是${this.usual.say}。`,
            `Además, el tío Wang viene todos los días. Cuando dice «lo de siempre», es ${this.usual.es}.`,
            `Also, Uncle Wang comes every day. When he says "the usual," it means ${this.usual.en}.`),
""",
"""          L(`陳姐：啊對了！鐵板麵已經賣完了，有客人點的話要先跟他說喔。還有，我今天還沒看到王伯伯，他每天都會來，如果他說「老樣子」就是${this.usual.say}。`,
            `¡Ah, cierto! Los fideos a la plancha ya se acabaron; si algún cliente los pide, avísale primero. Y todavía no he visto al tío Wang hoy; viene todos los días, y si dice «lo de siempre», es ${this.usual.es}.`,
            `Oh, right! The griddle noodles are sold out; if a customer orders them, tell them first. Also, I haven't seen Uncle Wang yet today. He comes every day, and if he says "the usual," it means ${this.usual.en}.`),
"""),
# 034
("L('陳姐：電話訂餐的單子我貼在收銀機上了。拜託你囉！', 'Pegué los pedidos por teléfono en la caja registradora. ¡Cuento contigo!', \"I stuck the phone orders on the cash register. I'm counting on you!\")",
 "L('陳姐：剛剛有電話點餐的，單子我貼在收銀機上了。拜託你囉！', 'Hace un momento hubo un pedido por teléfono; pegué la nota en la caja registradora. ¡Cuento contigo!', \"We just got a phone order; I stuck the slip on the cash register. I'm counting on you!\")"),
# 046
("Game.good('你記得告訴客人鐵板麵賣完了。', 'Te acordaste de avisar que se acabaron los fideos a la plancha.', 'You remembered to say the griddle noodles are sold out.')",
 "Game.good('記憶力很好喔！有記得告訴客人鐵板麵賣完了。', '¡Qué buena memoria! Te acordaste de avisar que se acabaron los fideos a la plancha.', 'Great memory! You remembered to say the griddle noodles are sold out.')"),
# 057
("L('（點單做好了。）', '(La comanda está lista.)', '(The order slip is ready.)')",
 "L('（早餐做好了。）', '(El desayuno está listo.)', '(The breakfast is ready.)')"),
# 062
("Game.good('王伯伯沒說內用還是外帶，你記得問了。', 'El tío Wang no dijo si era para comer aquí o para llevar, y tú preguntaste.', \"Uncle Wang didn't say for here or to go, and you asked.\")",
 "Game.good('王伯伯沒說內用還是外帶，還好你有問。', 'El tío Wang no dijo si era para comer aquí o para llevar, y menos mal que preguntaste.', \"Uncle Wang didn't say for here or to go; good thing you asked.\")"),
# 077 下一位！→下一位點餐！（選項兩處＋判斷一處）
("'下一位！'","'下一位點餐！'", 3),
# 084/085
("'老樣子，還多一個薯餅。'","'老樣子，還加一個薯餅。'"),
("'老樣子，還多一個鐵板麵。'","'老樣子，還加一份鐵板麵。'"),
("'還多': 'hái duō',","'還多': 'hái duō', '還加': 'hái jiā',"),
# 088
("Game.good('你記得王伯伯點了什麼。', 'Recordaste el pedido del tío Wang.', \"You remembered Uncle Wang's order.\")",
 "Game.good('很棒喔！你記得王伯伯點了什麼。', '¡Muy bien! Recordaste el pedido del tío Wang.', \"Great job! You remembered Uncle Wang's order.\")"),
# 089
("L('陳姐：好，我九點以前回去，有事再打給我！', 'Bien, vuelvo antes de las nueve. ¡Si pasa algo, llámame!', \"OK, I'll be back before nine. Call me if anything comes up!\")",
 "L('陳姐：好，我很快就回去，有事再打給我！', 'Bien, vuelvo pronto. ¡Si pasa algo, llámame!', \"OK, I'll be back soon. Call me if anything comes up!\")"),
# 090
("L('（八點，陳姐提著菜回來了。）', '(A las ocho, la señora Chen vuelve con las compras.)', '(At eight, Ms. Chen comes back with the groceries.)')",
 "L('（八點，陳姐回來了。）', '(A las ocho, la señora Chen vuelve.)', '(At eight, Ms. Chen comes back.)')"),
# 092（「我去出去」→「我出去」，已跟 Ben 說）
("L(`陳姐：${N}，你做得太好了！以後我去市場，櫃台都交給你！`, `¡${N}, lo hiciste genial! De ahora en adelante, cuando vaya al mercado, el mostrador es tuyo.`, `${N}, you did great! From now on, whenever I go to the market, the counter is yours!`)",
 "L(`陳姐：${N}，你好棒喔！以後我出去，櫃台都交給你！`, `¡${N}, qué bien lo hiciste! De ahora en adelante, cuando salga, el mostrador es tuyo.`, `${N}, you're awesome! From now on, whenever I go out, the counter is yours!`)"),
# 095
("item('陳大哥在後面做早餐，你負責櫃台：點單、收錢、找錢。', 'El señor Chen cocina atrás; tú atiendes el mostrador: comandas, cobrar y dar el cambio.', 'Mr. Chen cooks in the back; you run the counter: order slips, taking money and giving change.')",
 "item('陳大哥負責做早餐，你負責櫃台：點單、收錢、找錢。', 'El señor Chen se encarga de preparar el desayuno; tú atiendes el mostrador: comandas, cobrar y dar el cambio.', 'Mr. Chen takes care of the cooking; you run the counter: order slips, taking money and giving change.')"),
# 096
("item('鐵板麵今天賣完了，要跟客人說。', 'Hoy se acabaron los fideos a la plancha: hay que avisar a los clientes.', 'The griddle noodles are sold out today: tell the customers.')",
 "item('鐵板麵已經賣完了。', 'Los fideos a la plancha ya se acabaron.', 'The griddle noodles are sold out.')"),
# 097（半形冒號改全形）
("item(`王伯伯說「老樣子」，就是${u.say}。`, `Cuando el tío Wang dice «lo de siempre», es ${u.es}.`, `When Uncle Wang says \"the usual,\" it means ${u.en}.`)",
 "item(`王伯伯「老樣子」：${u.say}。`, `El tío Wang, «lo de siempre»: ${u.es}.`, `Uncle Wang's \"the usual\": ${u.en}.`)"),
# 098（補句號）
("item('電話訂餐的單子貼在收銀機上。', 'Los pedidos por teléfono están pegados en la caja registradora.', 'The phone orders are stuck on the cash register.')",
 "item('電話點餐的單子在收銀機上。', 'La nota del pedido por teléfono está en la caja registradora.', 'The phone order slip is at the cash register.')"),
# 099
("${r('客人常說的簡稱')}","${r('常用的簡稱')}"),
# 100-102
("""      item('大冰奶＝大杯冰奶茶', 'té con leche frío grande', 'large iced milk tea') +
      item('中冰紅＝中杯冰紅茶', 'té negro frío mediano', 'medium iced black tea') +
      item('中熱奶＝中杯熱奶茶', 'té con leche caliente mediano', 'medium hot milk tea');""",
"""      item('大冰奶＝大杯冰奶茶；中熱奶＝中杯熱奶茶', 'té con leche frío grande; té con leche caliente mediano', 'large iced milk tea; medium hot milk tea');"""),
# 單字（開場）：對話裡不再出現「煎台」「買菜」，換成這次新出現的詞
("['煎台', 'plancha', 'griddle']","['點單機', 'máquina de pedidos', 'ordering machine']"),
("['買菜', 'comprar comida (verduras, carne)', 'buy groceries']","['交給', 'dejar a cargo de', 'leave (it) to']"),
]
bad=0
for r in R:
    a,b=r[0],r[1]; want=r[2] if len(r)>2 else None
    n=s.count(a)
    if n<1 or (want is not None and n!=want): print('MISSING/COUNT:',n,want,a[:90]); bad+=1; continue
    s=s.replace(a,b)
if bad: sys.exit(1)
open(P,'w',encoding='utf-8').write(s); print('ok',len(R))
