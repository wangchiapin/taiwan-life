import os
p=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/drinks/index.html'); s=open(p,encoding='utf8').read()
R=[
("    同事 Ami 請你去樓下的飲料店幫她買一杯飲料，也別忘了你自己要喝什麼！<br>","    同事 Ami 要你去飲料店幫她買一杯飲料，別忘了買一杯你自己的！<br>"),
('Tu compañera Ami te pide que le compres una bebida en la tienda de abajo. ¡Y no olvides la tuya!','Tu compañera Ami te pide que vayas a la tienda de bebidas a comprarle una. ¡No olvides comprar una para ti!'),
("Your coworker Ami asks you to buy her a drink at the shop downstairs. And don't forget your own!","Your coworker Ami asks you to go to the drink shop and buy her a drink. Don't forget to buy one for yourself!"),
("['樓下', 'abajo (en el edificio)', 'downstairs']","['飲料店', 'tienda de bebidas', 'drink shop']"),
("TYPE_1: '好，重新點一次。'","TYPE_1: '好，重點一次。'"),
("TYPE_2: '接著點第二杯', TOPPING_2: '接著選加料'","TYPE_2: '繼續點第二杯', TOPPING_2: '選擇加什麼料'"),
("L(`Ami：${N}，我好渴喔！可以幫我去樓下買一杯${zhOrder(t)}嗎？我要加椰果。`,","L(`Ami：${N}，我好渴喔！可以幫我去買一杯${zhOrder(t)}嗎？我要加椰果。`,"),
("options: ['去樓下的飲料店'],","options: ['去飲料店'],"),
("L('（你走到樓下的飲料店，店員在櫃台後面。你要先點誰的飲料？）', '(Llegas a la tienda de bebidas de abajo; el empleado está detrás del mostrador. ¿De quién pides primero?)', \"(You reach the drink shop downstairs; the staff member is behind the counter. Whose drink will you order first?)\")",
 "L('（你到飲料店了，你要先點誰的飲料？）', '(Ya llegaste a la tienda de bebidas. ¿De quién pides primero?)', \"(You've arrived at the drink shop. Whose drink will you order first?)\")"),
("M('店員念錯了，你卻說對。', 'El empleado repitió mal tu pedido y dijiste que sí.'","M('店員說錯了，你卻說是對的。', 'El empleado dijo mal tu pedido y tú dijiste que estaba bien.'"),
("L('Benjamin：咦？等一下，這好像不是您剛剛點的……我們重新點一次吧！', 'Eh, espera, creo que eso no es lo que pediste… Vamos a pedirlo otra vez.', \"Huh? Wait, that's not what you ordered… Let's start over.\")",
 "L('Benjamin：咦？等一下，這好像不是您剛剛點的……我們再點一次吧！', 'Eh, espera, creo que eso no es lo que pediste… Vamos a pedirlo otra vez.', \"Huh? Wait, that's not what you ordered… Let's order it again.\")"),
("Game.good('你發現店員念錯了！', '¡Notaste que el empleado repitió mal tu pedido!', 'You caught the mistake in the read-back!')","Game.good('讚喔！你發現店員說錯了！', '¡Genial! Notaste que el empleado dijo mal tu pedido.', 'Nice! You noticed the staff got your order wrong!')"),
("M('店員念的是對的，你卻說不對。', 'El empleado repitió bien tu pedido y dijiste que no.'","M('店員說的是對的，你卻說不對。', 'El empleado dijo bien tu pedido y tú dijiste que no.'"),
("L('Benjamin：嗯？我念的就是您剛剛點的耶……'","L('Benjamin：嗯？我說的就是您剛剛點的耶……'"),
("L('Benjamin：嗯……我們從頭再點一次好了。', 'Mmm… mejor lo pedimos otra vez desde el principio.', \"Hmm… let's just order again from the start.\")","L('Benjamin：嗯……我們再點一次好了。', 'Mmm… mejor lo pedimos otra vez.', \"Hmm… let's just order it again.\")"),
("['請稍等，我問一下朋友。',","['等一下，我問一下我朋友。',"),
("if (c.startsWith('請稍等')) { Game.state = 'CALL_AMI'; return; }","if (c.startsWith('等一下，我問')) { Game.state = 'CALL_AMI'; return; }"),
("(opt.startsWith('請稍等') ? ' call' : '')","(opt.startsWith('等一下，我問') ? ' call' : '')"),
("Game.good('先打電話問 Ami 是好主意。', 'Llamar a Ami primero fue una buena idea.', 'Calling Ami first was a good idea.')","Game.good('你有先打電話問 Ami ，很棒喔！', 'Llamaste primero a Ami, ¡muy bien!', 'You called Ami first — great job!')"),
("Game.good('你發現店員找錯錢了！', '¡Notaste que el cambio estaba mal!', 'You noticed the change was wrong!')","Game.good('讚欸！你發現店員找錯錢了！', '¡Genial! Notaste que el cambio estaba mal.', 'Nice! You noticed the change was wrong!')"),
("options: ['沒關係，謝謝。', '你到底會不會算啊？'],","options: ['沒關係，謝謝。', '幹！你到底會不會算啊？'],"),
("L(`Ami：咦？${N}，這杯不對吧！我要的是","L(`Ami：咦？${N}，不對吧！我要的是"),
("L(`（你自己不是要${zhOrder(me)}嗎？好像也買錯了……）`, `(¿Tú no querías ${esOrder(me)}? Parece que la tuya también está mal…)`, `(Didn't you want ${enOrder(me)}? Looks like yours is wrong too…)`)",
 "L(`（你不是要喝${zhOrder(me)}嗎？買錯了吧……）`, `(¿No querías tomar ${esOrder(me)}? Creo que te equivocaste…)`, `(Didn't you want ${enOrder(me)}? Looks like you got it wrong…)`)"),
]
for a,b in R:
    n=s.count(a); assert n>=1,(n,a[:60]); s=s.replace(a,b)
s=s.replace("pinyinPro.customPinyin({\n","pinyinPro.customPinyin({\n  '重點': 'chóng diǎn', '重點一次': 'chóng diǎn yí cì',\n",1)
open(p,'w',encoding='utf8').write(s)
print('applied',len(R))
