import os
import sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/cinema/index.html')
s=open(P,encoding='utf-8').read()
# 每一筆：(舊字串, 新字串[, 預期出現次數])；找不到就停
# 括號內的編號是線上修改表的列號（rows/cinema.json）
R=[
# 003 開頭介紹（中文一次；西文在 data-es 和 span；英文在 data-en）
("你先到電影院：看看板、買票、選座位、買爆米花，還要找到對的廳。", "你提早先到電影院，要幫大家買票。", 1),
("Llegas primero: miras la cartelera, compras las entradas, eliges los asientos, compras palomitas y buscas la sala correcta.",
 "Llegas temprano y tienes que comprar las entradas para todos.", 2),
("You get there first: check the board, buy the tickets, pick seats, buy popcorn, and find the right theater.",
 "You arrive early and have to buy the tickets for everyone.", 1),
# 023
("（你走到售票櫃台，上面的電子看板列出今晚的電影。）", "（你走到售票櫃台，上面的螢幕列出今晚的電影。）", 1),
# 025、026
("M(`Ami說的是${Game.timeZh()}那一場。`, `Ami dijo la función de las ${t.time.es}.`, `Ami said the ${t.time.en} showing.`)",
 "M(`你記錯了啦！Ami說的是${Game.timeZh()}那一場。`, `¡Te equivocaste! Ami dijo la función de las ${t.time.es}.`, `You got it wrong! Ami said the ${t.time.en} showing.`)", 1),
("M(`Ami要看的是《${t.movie.zh}》。`, `Ami quiere ver «${t.movie.es}».`, `Ami wants to see \"${t.movie.en}\".`)",
 "M(`Ami要看的是《${t.movie.zh}》欸。`, `Ami quiere ver «${t.movie.es}», ¿eh?`, `Ami wants to see \"${t.movie.en}\", you know.`)", 1),
# 033
("M('你和Ami不是學生，要買全票。', 'Tú y Ami no son estudiantes: tienen que comprar entrada completa.', \"You and Ami aren't students, so you need full-price tickets.\")",
 "M('你和Ami已經不是學生了，要買全票。', 'Tú y Ami ya no son estudiantes: tienen que comprar entrada completa.', \"You and Ami aren't students anymore, so you need full-price tickets.\")", 1),
# 036
("staff('這是座位表，灰色的位子已經賣掉了。請選位子。', 'Este es el plano de asientos; los grises ya están vendidos. Elija sus asientos, por favor.', 'Here is the seat map; the gray seats are already sold. Please choose your seats.')",
 "staff('這是座位表，灰色的位子已經賣掉了。你看你想坐哪裡。', 'Este es el plano de asientos; los grises ya están vendidos. Mire dónde le gustaría sentarse.', \"Here is the seat map; the gray seats are already sold. Take a look at where you'd like to sit.\")", 1),
# 039（Ben 同意：提醒 Ami 說的是「連在一起」，再說同一排）
("M('要坐在同一排。', 'Tienen que sentarse en la misma fila.', 'You need to sit in the same row.')",
 "M('你忘記Ami說座位要連在一起嗎？要坐在同一排。', '¿Olvidaste que Ami dijo que los asientos fueran juntos? Tienen que sentarse en la misma fila.', 'Did you forget Ami said the seats should be together? You need to sit in the same row.')", 1),
# 050 刪除「售票員把電影票和零錢放在桌上」：找錢畫面改顯示售票員那句「收你…找你…」（Ben 同意）；
# 原本放在過場的那句移到找錢畫面，避免連續出現兩次
("          Game.thought = [staff(`收你${zhNum(t.bills * 1000)}元，找你${zhNum(Game.given)}元。`, `Recibo ${esM(t.bills * 1000)}; le doy ${esM(Game.given)} de cambio.`, `I've got ${enM(t.bills * 1000)} — here's ${enM(Game.given)} change.`)];\n          Game.state = 'CHANGE';",
 "          Game.state = 'CHANGE';", 1),
("dialogue: () => [L('（售票員把電影票和零錢放在桌上。）', '(La persona de la taquilla pone las entradas y el cambio sobre el mostrador.)', '(The ticket seller puts the tickets and the change on the counter.)')],",
 "dialogue: () => [staff(`收你${zhNum(t.bills * 1000)}元，找你${zhNum(Game.given)}元。`, `Recibo ${esM(t.bills * 1000)}; le doy ${esM(Game.given)} de cambio.`, `I've got ${enM(t.bills * 1000)} — here's ${enM(Game.given)} change.`)],", 1),
# 055、057 刪除「你收好電影票和零錢」
("          Game.thought = right\n            ? [L('（你收好電影票和零錢。）', '(Guardas las entradas y el cambio.)', '(You put away the tickets and the change.)')]\n            : [staff(`啊，不好意思！這裡是${zhNum(t.change)}元。`, `¡Ay, disculpe! Aquí tiene ${esM(t.change)}.`, `Oh, sorry! Here's ${enM(t.change)}.`), L('（你收好電影票和零錢。）', '(Guardas las entradas y el cambio.)', '(You put away the tickets and the change.)')];",
 "          Game.thought = right\n            ? null\n            : [staff(`啊，不好意思！這裡是${zhNum(t.change)}元。`, `¡Ay, disculpe! Aquí tiene ${esM(t.change)}.`, `Oh, sorry! Here's ${enM(t.change)}.`)];", 1),
# 062
("M('Ami要吃爆米花，只買可樂不夠。', 'Ami quiere palomitas: solo la cola no basta.', 'Ami wants popcorn — just a cola is not enough.')",
 "M('Ami還要吃爆米花，只買可樂不夠。', 'Ami también quiere palomitas: solo la cola no basta.', 'Ami wants popcorn too — just a cola is not enough.')", 1),
# 073
("L('驗票員：好，沒問題。請進，祝你們看得開心！', 'Muy bien, todo en orden. Pasen; ¡que disfruten la película!', 'Alright, no problem. Go on in — enjoy the movie!')",
 "L('驗票員：好，沒問題。請進！', 'Muy bien, todo en orden. Pasen.', 'Alright, no problem. Go on in!')", 1),
# 074 刪除「電影院裡有好幾個廳，每個門口都寫著廳號」
("          L('（電影院裡有好幾個廳，每個門口都寫著廳號。）', '(Hay varias salas en el cine y cada puerta tiene el número de sala.)', '(The cinema has several theaters, and each door shows its number.)'),\n", "", 1),
# 086
("M('票上有位子，要坐票上的位子（對號入座），不能隨便讓給別人。',", "M('票上有位子，要對號入座，不要隨便讓給別人。',", 1),
# 099 刪除「電影結束了，燈亮起來」（好結局）
("            L('（電影結束了，燈亮起來。）', '(Termina la película y se encienden las luces.)', '(The movie ends and the lights come up.)'),\n", "", 1),
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
