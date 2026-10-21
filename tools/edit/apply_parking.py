import os
import sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/parking/index.html')
s=open(P,encoding='utf-8').read()
# 每一筆：(舊字串, 新字串[, 預期出現次數])；找不到就停
# 括號內的編號是線上修改表的列號（rows/parking.json）
R=[
# 003 開頭介紹（中文一次；西文在 data-es 和 span；英文在 data-en）
("Ami 借你她的車，請你開去星光百貨。你要把車停進地下停車場、告訴她你停在哪裡，逛完以後還要繳停車費，再把車開出去。",
 "你跟Ami 開車去星光百貨逛街。Ami已經先去逛了，你要自己把車子停在地下停車場，你知道該怎麼停嗎？", 1),
("Ami te presta su auto para ir al centro comercial Xingguang. Tienes que estacionarlo en el sótano, decirle dónde quedó, y después de las compras pagar el estacionamiento y salir.",
 "Vas con Ami en auto al centro comercial Xingguang. Ami ya se adelantó a pasear; tú tienes que estacionar el auto en el estacionamiento del sótano. ¿Sabes cómo hacerlo?", 2),
("Ami lends you her car to drive to the Starlight department store. You park it in the basement garage, tell her where it is, and after shopping you pay the parking fee and drive out.",
 "You and Ami drive to the Starlight department store to go shopping. Ami has already gone ahead, so you have to park the car in the basement garage yourself. Do you know how?", 1),
# 012 + 013（013 的「不要停愛心專用車位」併進 012，013 整句刪除）
("L(`Ami：${N}，我在三樓的書店等你。你先把車停好。`, `${N}, te espero en la librería del tercer piso. Primero estaciona el auto.`, `${N}, I'll wait at the bookstore on the 3rd floor. Park the car first.`),\n      L('Ami：停車場在地下室。要停一般車位，不要停愛心專用車位喔！', 'El estacionamiento está en el sótano. Usa un espacio normal, ¡no uno reservado «de corazón» para personas con discapacidad!', \"The parking is in the basement. Use a regular space — not a priority \\\"heart\\\" space for people with disabilities!\"),\n",
 "L(`Ami：${N}，我在三樓的書局等你。你先把車停到地下室。不要占用愛心專用車位喔！`, `${N}, te espero en la librería del tercer piso. Primero estaciona el auto en el sótano. ¡No ocupes un espacio reservado «de corazón» para personas con discapacidad!`, `${N}, I'll wait at the bookstore on the 3rd floor. First park the car in the basement. Don't take a priority \"heart\" space!`),\n", 1),
# 015（Ben 寫「停車每小時停車」，重複的「停車」拿掉；「滿一千元折抵兩小時」改成「以此類推」）
("我們大概會逛${NZ(t.h)}個小時。這裡每小時停車${t.rate}元；發票滿五百元折抵一小時，滿一千元折抵兩小時。`,",
 "我們大概會逛${NZ(t.h)}個小時。停車每小時${t.rate}元；不過好像發票滿五百元折抵一小時，以此類推。`,", 1),
("`Vamos a estar unas ${t.h} horas. Aquí se paga ${esM(t.rate)} por hora; un recibo de ${esM(500)} o más descuenta 1 hora, y de ${esM(1000)} o más, 2 horas.`",
 "`Vamos a estar unas ${t.h} horas. El estacionamiento cuesta ${esM(t.rate)} por hora; pero parece que un recibo de ${esM(500)} o más descuenta 1 hora, y así sucesivamente.`", 1),
("`We'll be shopping about ${t.h} hours. Parking is ${enM(t.rate)} per hour; a receipt of ${enM(500)} or more takes off 1 hour, and ${enM(1000)} or more takes off 2 hours.`",
 "`We'll be shopping about ${t.h} hours. Parking is ${enM(t.rate)} per hour; but it seems a receipt of ${enM(500)} or more takes off 1 hour, and so on.`", 1),
# 016
("L('（你開著Ami借你的車，到了星光百貨的停車場入口。手機響了一聲，是Ami傳來的LINE。）', '(Llegas en el auto que te prestó Ami a la entrada del estacionamiento del centro comercial. Tu celular suena: es un LINE de Ami.)', \"(You drive up in the car Ami lent you to the parking entrance of the department store. Your phone buzzes — a LINE from Ami.)\")",
 "L('（你開著車到了星光百貨的停車場入口。手機響了一聲，是Ami傳來的LINE。）', '(Llegas en el auto a la entrada del estacionamiento del centro comercial. Tu celular suena: es un LINE de Ami.)', \"(You drive up to the parking entrance of the department store. Your phone buzzes — a LINE from Ami.)\")", 1),
# 019
("L('（入口的柵欄擋住了路。旁邊有一台機器，上面有一個按鈕。）', '(La barrera te cierra el paso. A un lado hay una máquina con un botón.)', '(A barrier blocks the way. Next to it is a machine with a button.)')",
 "L('（入口柵欄旁邊有一台機器，上面有一個按鈕。）', '(Junto a la barrera de la entrada hay una máquina con un botón.)', '(Next to the entrance barrier is a machine with a button.)')", 1),
# 027：Ben 的「）」是不小心留下的，這句保留原樣（Ben 同意）
# 029
("[L(`（你開到${FL(f)}，每個位子都停了車，只好開回去。）`, `(Bajas al ${FL_ES(f)}: todos los espacios están ocupados, así que subes de nuevo.)`, `(You drive down to ${FL_EN(f)}: every space is taken, so you drive back.)`)]",
 "[L(`（你開到${FL(f)}，好像都停滿了。）`, `(Bajas al ${FL_ES(f)}: parece que todo está lleno.)`, `(You drive down to ${FL_EN(f)}: it looks like everything is full.)`)]", 1),
# 032：保留（Ben 同意，這是 SPOT 畫面上唯一的一句）
# 039 刪除「你把車停好，下了車」
("          Game.thought = [L('（你把車停好，下了車。）', '(Estacionas el auto y bajas.)', '(You park the car and get out.)')];\n          Game.state = 'REMEMBER';",
 "          Game.thought = null;\n          Game.state = 'REMEMBER';", 1),
# 040 刪除「旁邊的柱子上有一個牌子」
("          L('（旁邊的柱子上有一個牌子，寫著這裡的位置。）', '(En el pilar de al lado hay un letrero con la ubicación.)', '(On the pillar next to you is a sign showing where you are.)'),\n", "", 1),
# 048
("ami('好，我知道了！我們逛完就去找車。', '¡Bien, entendido! Después de las compras vamos a buscar el auto.', \"Got it! We'll go find the car after shopping.\")",
 "ami('好，我知道了！', '¡Bien, entendido!', 'Got it!')", 1),
# 059 刪除「你們坐電梯到地下室」
("          L('（你們坐電梯到地下室。）', '(Bajan en el ascensor al sótano.)', '(You take the elevator down to the basement.)'),\n", "", 1),
# 064（拿掉「看任務提示」，西文英文一起拿掉）＋ 065 刪除「你們走到〇〇，那裡沒有Ami的車」
("Game.addMistake(M(`你傳給Ami的訊息是：${Game.locZh()}。（看「任務提示」）`, `Tu mensaje a Ami decía: ${Game.locEs()}. (Mira las «pistas».)`, `Your message to Ami said: ${Game.locEn()}. (Check the hints.)`),\n              [L(`（你們走到${c.slice(1, -1)}，那裡沒有Ami的車。）`, '(Van hasta allá, pero ahí no está el auto de Ami.)', \"(You walk over, but Ami's car isn't there.)\")]);",
 "Game.addMistake(M(`你傳給Ami的訊息是：${Game.locZh()}。`, `Tu mensaje a Ami decía: ${Game.locEs()}.`, `Your message to Ami said: ${Game.locEn()}.`));", 1),
# 067 刪除「你們找到車，上車了」
("          Game.thought = [L('（你們找到車，上車了。）', '(Encuentran el auto y suben.)', '(You find the car and get in.)')];\n          Game.state = 'EXIT';",
 "          Game.thought = null;\n          Game.state = 'EXIT';", 1),
# 075 刪除「柵欄升起來了，你把車開出停車場」（好結局）
("            L('（柵欄升起來了，你把車開出停車場。）', '(La barrera sube y sacas el auto del estacionamiento.)', '(The barrier rises and you drive out of the garage.)'),\n", "", 1),
# 076
("ami(`太好了，${N}，你開車停車都很穩！我們去吃晚餐吧！`,", "ami(`太好了，${N}，你開車停車都很穩喔！我們去吃晚餐吧！`,", 1),
# 079 刪除「你把車開出停車場」（普通結局）
("            L('（你把車開出停車場。）', '(Sacas el auto del estacionamiento.)', '(You drive out of the garage.)'),\n", "", 1),
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
