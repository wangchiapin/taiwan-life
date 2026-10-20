import os
import sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/market/index.html')
s=open(P,encoding='utf-8').read()
# 每一筆：(舊字串, 新字串[, 預期出現次數])；找不到就停
# 括號內的編號是線上修改表的列號（rows/market.json）
R=[
# 003 開頭介紹（中文一次；西文在 data-es 和 span；英文在 data-en）
("Ami 想在家煮晚餐，請你去傳統市場買菜。每種東西的量詞不一樣，還可以試試看殺價。",
 "Ami 說今天想要自己煮晚餐，請你去傳統市場買菜。每種東西的量詞不一樣，還可以試試看殺價唷！", 1),
("Ami quiere cocinar la cena en casa y te manda al mercado tradicional.",
 "Ami dice que hoy quiere cocinar la cena ella misma y te manda al mercado tradicional.", 2),
("Ami wants to cook dinner at home and sends you to the traditional market.",
 "Ami says she wants to cook dinner herself today and sends you to the traditional market.", 1),
# 010
("L(`Ami：${N}，我今天晚上要在家煮飯，你可以幫我去菜市場買菜嗎？`, `${N}, esta noche cocino en casa. ¿Puedes ir al mercado a comprar?`, `${N}, I'm cooking at home tonight. Could you buy groceries at the market?`)",
 "L(`Ami：${N}，我今天晚上要在家煮飯，你來我家一起吃吧！不過，你可以幫我去菜市場買菜嗎？`, `${N}, esta noche cocino en casa: ¡ven a mi casa a cenar conmigo! Pero antes, ¿puedes ir al mercado a comprar?`, `${N}, I'm cooking at home tonight — come over and eat with me! But first, could you buy groceries at the market?`)", 1),
# 012
("L('Ami：記得帶我的環保袋，不要拿塑膠袋。還有，可以問問看能不能算便宜一點喔！', 'Lleva mi bolsa reutilizable, no aceptes bolsa de plástico. ¡Y pregunta si te pueden hacer un descuento!', \"Take my reusable bag — don't take a plastic one. And ask if they can give you a discount!\")",
 "L('Ami：記得帶環保袋，不要拿塑膠袋。還有，可以問問看能不能算便宜一點喔！', 'Lleva una bolsa reutilizable, no aceptes bolsa de plástico. ¡Y pregunta si te pueden hacer un descuento!', \"Bring a reusable bag — don't take a plastic one. And ask if they can give you a discount!\")", 1),
# 019
("M(`${it.zh}的量詞是「${it.m}」。`, `El clasificador de ${it.es} es «${it.m}».`, `The measure word for ${it.en} is \"${it.m}\".`)",
 "M(`記住！${it.zh}的量詞是「${it.m}」。`, `¡Recuerda! El clasificador de ${it.es} es «${it.m}».`, `Remember! The measure word for ${it.en} is \"${it.m}\".`)", 1),
# 022 刪除「我：Ami說可以問問看……」
("dialogue: () => [Game.priceLine(), L('我：Ami說可以問問看……', 'Ami dijo que podía preguntar…', 'Ami said I could try asking…')],",
 "dialogue: () => [Game.priceLine()],", 1),
# 026
("M('客氣地問「可以算便宜一點嗎？」。', 'Se pide con amabilidad: «可以算便宜一點嗎？».', 'Ask politely: \"可以算便宜一點嗎？\".')",
 "M('客氣一點問「可以算便宜一點嗎？」，會比較有禮貌喔！', 'Pregunta con más amabilidad: «可以算便宜一點嗎？». ¡Es más cortés!', 'Ask more politely: \"可以算便宜一點嗎？\" — it sounds more courteous!')", 1),
# 027
("goodFirst('BARGAIN', '問得很客氣！在菜市場常常可以這樣問。', '¡Muy cortés! En el mercado se suele preguntar así.', 'Very polite! At the market this is a common question.');",
 "goodFirst('BARGAIN', '不錯喔！問得很客氣！', '¡Muy bien! ¡Qué cortés!', 'Nice! Very polite!');", 1),
# 029 刪除「你只有一張五百元」：付錢畫面改顯示老闆的價錢（Ben 同意）；原本放在過場的老闆那句移到付錢畫面，避免連續出現兩次
("          Game.thought = [vend(`好啦，算你${zhNum(t.final)}元。`, `Está bien, se lo dejo en ${esM(t.final)}.`, `Alright, I'll make it ${enM(t.final)}.`)];\n          Game.state = 'PAY';",
 "          Game.state = 'PAY';", 1),
("dialogue: () => [L('（你只有一張五百元。）', '(Solo tienes un billete de quinientos dólares.)', '(You only have a 500-dollar bill.)')],",
 "dialogue: () => [vend(`好啦，算你${zhNum(t.final)}元。`, `Está bien, se lo dejo en ${esM(t.final)}.`, `Alright, I'll make it ${enM(t.final)}.`)],", 1),
# 034
("M('買東西要先付錢，不能賒帳。', 'Hay que pagar primero: no se compra a crédito.', 'You have to pay first — no buying on credit.')",
 "M('不行啦！買東西要先付錢，不能賒帳。', '¡No se puede! Hay que pagar primero: no se compra a crédito.', 'No way! You have to pay first — no buying on credit.')", 1),
# 035
("goodFirst('PAY', '沒錯！五百元夠了。', '¡Exacto! Quinientos alcanzan.', 'Right! 500 is enough.');",
 "goodFirst('PAY', '沒錯！五百元就夠了。', '¡Exacto! Con quinientos alcanza.', 'Right! 500 is enough.');", 1),
# 042
("M('Ami說不要拿塑膠袋，要用環保袋。', 'Ami dijo que no tomaras bolsa de plástico y usaras la reutilizable.', 'Ami said no plastic bags — use the reusable one.')",
 "M('Ami說不要拿塑膠袋，要用環保袋。保護地球！', 'Ami dijo que no tomaras bolsa de plástico y usaras la reutilizable. ¡Cuida el planeta!', 'Ami said no plastic bags — use the reusable one. Protect the planet!')", 1),
# 043
("goodFirst('BAG', '很好！「不用，我有……」可以客氣地拒絕。', '¡Muy bien! «不用，我有…» es una forma amable de rechazar.', 'Good! \"不用，我有…\" is a polite way to decline.');",
 "goodFirst('BAG', '很好！「不用，我有……」可以很客氣地拒絕。', '¡Muy bien! «不用，我有…» es una forma muy amable de rechazar.', 'Good! \"不用，我有…\" is a very polite way to decline.');", 1),
# 045 刪除「你提著環保袋回家」
("            L('（你提著環保袋回家，把菜拿給Ami。）', '(Vuelves a casa con la bolsa reutilizable y le das las compras a Ami.)', '(You go home with the reusable bag and give the groceries to Ami.)'),\n", "", 1),
# 046
("L(`Ami：哇，菜都好新鮮，還省了錢！謝謝你，${N}！今天晚餐會很好吃。`, `¡Guau, todo está muy fresco y además ahorraste! ¡Gracias, ${N}! La cena estará riquísima.`, `Wow, everything is so fresh and you even saved money! Thanks, ${N}! Dinner will be great.`)",
 "L(`Ami：哇，菜都好新鮮唷，還省了不少錢！謝謝你，${N}！我來煮好吃的給你吃。`, `¡Guau, todo está muy fresco y además ahorraste bastante! ¡Gracias, ${N}! Yo cocino algo rico para ti.`, `Wow, everything is so fresh, and you saved quite a bit! Thanks, ${N}! I'll cook something delicious for you.`)", 1),
# 047
("L('Ami：謝謝你！不過好像買錯了一些東西……下次要看清楚喔！',", "L('Ami：謝謝你！不過好像有一些東西買錯了……下次要看清楚喔！',", 1),
# 拼音（台灣讀音）：新句子「還可以試試看殺價」「還省了不少錢」的「還」念 hái
("'殺價': 'shā jià', '歡迎光臨': 'huān yíng guāng lín'\n",
 "'殺價': 'shā jià', '歡迎光臨': 'huān yíng guāng lín', '還可以': 'hái kě yǐ', '還省': 'hái shěng'\n", 1),
# 單字表：END 的「晚餐」在 046 改掉後沒有出現，換成新句子裡有的「好吃」
("['晚餐', 'cena', 'dinner']]", "['好吃', 'rico / delicioso', 'delicious']]", 1),
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
