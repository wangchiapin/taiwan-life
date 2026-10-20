import os
import sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/icecream/index.html')
s=open(P,encoding='utf-8').read()
# 每一筆：(舊字串, 新字串[, 預期出現次數])；找不到就停
# 括號內的編號是線上修改表的列號（rows/icecream.json）
R=[
# 003 開頭介紹（Ben 寫「他有很多要求」「!」，我改成「她」「！」）
("Ami 想吃冰淇淋，請你去冰淇淋店幫她買。要幾球、什麼口味、杯子還是甜筒、加不加配料、內用還是外帶，都要照她說的點。",
 "Ami 請你去冰淇淋店幫她買冰淇淋。她有很多要求喔！記得都要照她說的點，Ami才不會生氣。", 1),
("Ami quiere un helado y te pide que lo compres. Tienes que pedirlo exactamente como ella dijo: cuántas bolas, de qué sabores, en vaso o en cono, con o sin topping, para comer ahí o para llevar.",
 "Ami te pide que vayas a la heladería a comprarle un helado. ¡Tiene muchas peticiones! Recuerda pedirlo todo tal como ella dijo, para que Ami no se enoje.", 2),
("Ami wants ice cream and asks you to buy it. Order it exactly as she said: how many scoops, which flavors, cup or cone, toppings or not, for here or to go.",
 "Ami asks you to go to the ice cream shop and buy her some ice cream. She has a lot of requests! Remember to order everything exactly as she said, so Ami won't get upset.", 1),
# 011
("幫我買一個冰淇淋，好嗎？`,", "幫我買冰淇淋，好嗎？`,", 1),
("Could you buy me an ice cream?`", "Could you buy me some ice cream?`", 1),
# 031
("M(`Ami要${t.vessel.zh}。`, `Ami lo quiere ${t.vessel.es}.`, `Ami wants it ${t.vessel.en}.`)",
 "M(`你記錯了啦！Ami要${t.vessel.zh}。`, `¡Te equivocaste! Ami lo quiere ${t.vessel.es}.`, `You got it wrong! Ami wants it ${t.vessel.en}.`)", 1),
# 035
("M(`第${CN[Game.k + 1]}球，Ami要的是${f.zh}。`, `Para la bola ${Game.k + 1}, Ami pidió ${f.es}.`, `For scoop ${Game.k + 1}, Ami asked for ${f.en}.`)",
 "M(`不對不對！第${CN[Game.k + 1]}球Ami要的是${f.zh}。`, `¡No, no! Para la bola ${Game.k + 1}, Ami pidió ${f.es}.`, `No, no! For scoop ${Game.k + 1}, Ami asked for ${f.en}.`)", 1),
# 036
("L(`（店員把${f.zh}冰淇淋放在${Game.vessel.zh}裡。）`,", "L(`（店員把${f.zh}的冰淇淋放在${Game.vessel.zh}裡。）`,", 1),
# 037 刪除「店員把〇〇放在最上面」
("          Game.thought = [L(`（店員把${f.zh}放在最上面。）`, `(La persona pone el de ${f.es} arriba de todo.)`, `(The staff puts the ${f.en} on top.)`)];\n          Game.state = 'TOPPING';",
 "          Game.thought = null;\n          Game.state = 'TOPPING';", 1),
# 038（西文、英文原本就是「每一種」）
("配料一種十元。'", "配料每種十元。'", 1),
# 039、040
("M(`Ami要加${t.top.zh}。`, `Ami quiere ${t.top.es}.`, `Ami wants ${t.top.en}.`)",
 "M(`拜託～Ami要加的是${t.top.zh}。`, `¡Por favor! Ami quiere ${t.top.es}.`, `Come on! Ami wants ${t.top.en}.`)", 1),
("M('Ami說不要加配料。', 'Ami dijo que no quería topping.', 'Ami said no toppings.')",
 "M('你完蛋了！Ami說不要加配料。', '¡Estás frito! Ami dijo que no quería topping.', \"You're doomed! Ami said no toppings.\")", 1),
# 042 刪除「店員在冰淇淋上面加了配料」
("          Game.thought = t.top ? [L(`（店員在冰淇淋上面加了${t.top.zh}。）`, `(La persona agrega ${t.top.es} al helado.)`, `(The staff adds ${t.top.en} on top.)`)] : null;\n",
 "          Game.thought = null;\n", 1),
# 044
("M(`Ami${t.eat === 'here' ? '已經在店裡面坐好了，要內用' : '在公園等你，要外帶'}。`, `Ami ${t.eat === 'here' ? 'ya está sentada en la tienda: es para comer aquí' : 'te espera en el parque: es para llevar'}.`, `Ami ${t.eat === 'here' ? \"is already seated in the shop — it's for here\" : \"is waiting in the park — it's to go\"}.`)",
 "M(`不對喔！Ami${t.eat === 'here' ? '已經在店裡面坐好了，要內用' : '在公園等你，要外帶'}。`, `¡No! Ami ${t.eat === 'here' ? 'ya está sentada en la tienda: es para comer aquí' : 'te espera en el parque: es para llevar'}.`, `No! Ami ${t.eat === 'here' ? \"is already seated in the shop — it's for here\" : \"is waiting in the park — it's to go\"}.`)", 1),
# 045 刪除「你有一張一百元和一張兩百元」：付錢畫面改顯示店員說的總價（Ben 同意）；
# 原本放在過場的那句移到付錢畫面，避免連續出現兩次
("          Game.thought = [Game.priceLine()];\n          Game.state = 'PAY';", "          Game.state = 'PAY';", 1),
("dialogue: () => [L('（你有一張一百元和一張兩百元。）', '(Tienes un billete de cien y uno de doscientos dólares.)', '(You have a 100-dollar bill and a 200-dollar bill.)')],",
 "dialogue: () => [Game.priceLine()],", 1),
# 048、049
("M(`一共是${t.total}元，一百元不夠。`,", "M(`一共是${t.total}元，一百元不夠啦。`,", 1),
("M('買東西要先付錢，不能賒帳。', 'Hay que pagar primero: no se compra a crédito.', \"You have to pay first — no buying on credit.\")",
 "M('這樣不行喔！買東西要先付錢，不能賒帳。', '¡Así no se puede! Hay que pagar primero: no se compra a crédito.', \"That won't do! You have to pay first — no buying on credit.\")", 1),
# 053、054 刪除「你把冰淇淋拿給Ami」「你走到公園，把冰淇淋拿給Ami」
("            L(here ? '（你把冰淇淋拿給Ami。）' : '（你走到公園，把冰淇淋拿給Ami。）', here ? '(Le llevas el helado a Ami.)' : '(Caminas al parque y le das el helado a Ami.)', here ? '(You bring the ice cream to Ami.)' : '(You walk to the park and hand Ami the ice cream.)'),\n", "", 1),
# 單字表：END 的「拿給」（053、054 刪除後沒有出現）換成結局店員說的「請慢用」
("['拿給', 'entregar a', 'hand to']]", "['請慢用', 'buen provecho', 'enjoy']]", 1),
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
