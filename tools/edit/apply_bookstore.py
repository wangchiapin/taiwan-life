import os
import sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/bookstore/index.html')
s=open(P,encoding='utf-8').read()
# 每一筆：(舊字串, 新字串[, 預期出現次數])；找不到就停
# 括號內的編號是線上修改表的列號（rows/bookstore.json）
R=[
# 003 開頭介紹（中文一次；西文在 data-es 和 span；英文在 data-en）
("Ami 的朋友要過生日，她想送一本書。請你去書店幫她買：找到對的書區、對的書，順便買書籤，還要請店員包裝。",
 "Ami 想送她朋友一本書當作生日禮物，所以請你去書店幫她買，要買到Ami指定的書，需要注意很多事喔！", 1),
("Se acerca el cumpleaños de una amiga de Ami y quiere regalarle un libro. Ve a la librería: encuentra la sección y el libro correctos, compra también un marcapáginas y pide que lo envuelvan.",
 "Ami quiere regalarle un libro a una amiga por su cumpleaños, así que te pide que vayas a la librería a comprarlo. Tienes que comprar el libro que Ami indicó, ¡y hay que fijarse en muchas cosas!", 2),
("Ami's friend has a birthday soon and she wants to give her a book. Go to the bookstore: find the right section and book, buy a bookmark too, and ask for gift wrapping.",
 "Ami wants to give her friend a book as a birthday gift, so she asks you to buy it at the bookstore. You need to get the exact book Ami wants, and there are a lot of things to watch out for!", 1),
# 011
("L(`Ami：${N}，下禮拜是我朋友的生日，我想買一本書當禮物。`, `${N}, la semana que viene es el cumpleaños de una amiga y quiero regalarle un libro.`, `${N}, my friend's birthday is next week and I want to give her a book.`)",
 "L(`Ami：${N}，下禮拜是我朋友的生日，我想買一本書當禮物，你覺得怎麼樣？`, `${N}, la semana que viene es el cumpleaños de una amiga y quiero regalarle un libro. ¿Qué te parece?`, `${N}, my friend's birthday is next week and I want to give her a book. What do you think?`)", 1),
# 012
("L(`Ami：她喜歡看${t.sec.zh}，所以去${t.sec.zh}書區找。書名是《${t.book[0]}》。`, `Le gusta leer ${t.sec.es}, así que busca en la sección de ${t.sec.es}. El título es «${t.book[0]}».`, `She likes ${t.sec.en}, so look in the ${t.sec.en} section. The title is \"${t.book[0]}\".`)",
 "L(`Ami：你可以幫我買一下嗎？她喜歡看${t.sec.zh}，所以去${t.sec.zh}書區找。書名是《${t.book[0]}》。`, `¿Puedes comprarlo por mí? Le gusta leer ${t.sec.es}, así que busca en la sección de ${t.sec.es}. El título es «${t.book[0]}».`, `Could you buy it for me? She likes ${t.sec.en}, so look in the ${t.sec.en} section. The title is \"${t.book[0]}\".`)", 1),
# 013
("L('Ami：還要買一個書籤，然後請店員幫我們包裝。', 'También compra un marcapáginas y pide que lo envuelvan.', 'Also buy a bookmark, and ask the staff to wrap it.')",
 "L('Ami：對了！再買一個書籤好了，然後請店員幫忙包裝。', '¡Ah, cierto! Compra también un marcapáginas y pide al personal que lo envuelva.', 'Oh, right! Let’s also get a bookmark, and ask the staff to wrap it.')", 1),
# 017 刪除旁白（書店裡有很多書區）；018 保留當作這一關的問題（Ben 同意）
("dialogue: () => [L('（書店裡有很多書區。招牌上寫著不同的分類。）', '(La librería tiene muchas secciones; los letreros indican las categorías.)', '(The bookstore has many sections, with signs for each category.)'), L('我：Ami的朋友喜歡看什麼書？我要去哪一區？',",
 "dialogue: () => [L('我：Ami的朋友喜歡看什麼書？我要去哪一區？',", 1),
# 020
("M(`Ami說朋友喜歡看${t.sec.zh}。`, `Ami dijo que a su amiga le gusta leer ${t.sec.es}.`, `Ami said her friend likes ${t.sec.en}.`)",
 "M(`你記錯了喔！Ami說朋友喜歡看${t.sec.zh}。`, `¡Te equivocaste! Ami dijo que a su amiga le gusta leer ${t.sec.es}.`, `You got it wrong! Ami said her friend likes ${t.sec.en}.`)", 1),
# 022 刪除「你走到〇〇書區」
("          Game.thought = [L(`（你走到${t.sec.zh}書區。）`, `(Caminas a la sección de ${t.sec.es}.)`, `(You walk to the ${t.sec.en} section.)`)];\n          Game.state = 'FIND';",
 "          Game.thought = null;\n          Game.state = 'FIND';", 1),
# 023 刪除旁白（書架上有三本書）；024 保留當作這一關的問題（Ben 同意）
("dialogue: () => [L('（書架上有三本書。書名都很像，要看清楚。）', '(Hay tres libros en el estante; hay que leer bien los títulos.)', '(Three books on the shelf — read the titles carefully.)'), L('我：Ami要的是哪一本？',",
 "dialogue: () => [L('我：Ami要的是哪一本？',", 1),
# 026
("M(`書名是《${t.book[0]}》。`, `El título es «${t.book[0]}».`, `The title is \"${t.book[0]}\".`)",
 "M(`要吃銀杏了喔！Ami說書名是《${t.book[0]}》。`, `¡Hay que comer ginkgo (para la memoria)! Ami dijo que el título es «${t.book[0]}».`, `Time to eat some ginkgo (for your memory)! Ami said the title is \"${t.book[0]}\".`)", 1),
# 028 刪除「你拿到書了。接下來要找書籤」
("          Game.thought = [L('（你拿到書了。接下來要找書籤。）', '(Tienes el libro. Ahora falta el marcapáginas.)', '(You have the book. Next, the bookmark.)')];\n          Game.state = 'ASK';",
 "          Game.thought = null;\n          Game.state = 'ASK';", 1),
# 029
("L('（你找不到書籤。你看到一位店員走過來。）', '(No encuentras los marcapáginas. Ves a un empleado acercarse.)', \"(You can't find the bookmarks. A staff member walks by.)\")",
 "L('（你找不到書籤在哪裡。）', '(No encuentras dónde están los marcapáginas.)', \"(You can't find where the bookmarks are.)\")", 1),
# 032、033 選項文字（正解「請問書籤在哪裡？」不變）
("['請問書籤在哪裡？', '請問書籤幾點下班？', '請問這本書好看嗎，書籤呢？']", "['請問書籤在哪裡？', '請問簽書會在哪裡？', '書籤很貴嗎？']", 1),
# 034（Ben 同意改成：搞錯了啦！你要找的是書籤，要問位置，就說「書籤在哪裡」。）
("M('要問位置，就說「在哪裡」。', 'Para preguntar la ubicación se dice «在哪裡».', 'To ask where something is, say \"在哪裡\".')",
 "M('搞錯了啦！你要找的是書籤，要問位置，就說「書籤在哪裡」。', '¡Te equivocaste! Lo que buscas es el marcapáginas; para preguntar la ubicación, di «書籤在哪裡».', 'Oops! You are looking for the bookmark; to ask where it is, say \"書籤在哪裡\".')", 1),
# 042
("M('Ami說要請店員包裝，這是禮物。', 'Ami dijo que lo envuelvan: es un regalo.', 'Ami asked for gift wrapping — it is a present.')",
 "M('哎呀！Ami說要請店員包裝，這是禮物欸。', '¡Ay! Ami dijo que lo envuelvan: ¡es un regalo!', 'Oops! Ami asked for gift wrapping — it is a present!')", 1),
# 048
("M(`一共是${t.total}元，兩百元不夠。`, `El total es ${esM(t.total)}: doscientos no alcanzan.`, `The total is ${enM(t.total)} — 200 isn't enough.`)",
 "M(`你算錯了吧！一共是${t.total}元，兩百元不夠。`, `¡Calculaste mal! El total es ${esM(t.total)}: doscientos no alcanzan.`, `You miscalculated! The total is ${enM(t.total)} — 200 isn't enough.`)", 1),
# 049
("M('買東西要先付錢，不能賒帳。', 'Hay que pagar primero: no se compra a crédito.', 'You have to pay first — no buying on credit.')",
 "M('這樣不行喔！買東西要先付錢，不能賒帳。', '¡Así no se puede! Hay que pagar primero: no se compra a crédito.', \"That won't do! You have to pay first — no buying on credit.\")", 1),
# 053 刪除「你回去找Ami，把禮物拿給她」
("            L('（你回去找Ami，把禮物拿給她。）', '(Vuelves con Ami y le das el regalo.)', '(You go back to Ami and hand her the gift.)'),\n", "", 1),
# 055
("L('Ami：謝謝你！不過你花了好多時間……下次要快一點喔！', '¡Gracias! Pero tardaste mucho… ¡la próxima vez más rápido!', 'Thanks! But it took a while… faster next time!')",
 "L('Ami：謝謝你！好像遇到一些狀況……至少是買到書了啦……', '¡Gracias! Parece que hubo algunos problemas… pero al menos conseguiste el libro…', 'Thanks! Looks like there were some problems… but at least you got the book…')", 1),
# 單字表：旁白刪除後畫面上不再出現的詞，換成還在畫面上的詞
("['招牌', 'letrero', 'sign']]", "['喜歡', 'gustar', 'like']]", 1),      # SECTION：招牌（017 刪除）→ 喜歡（018 的問題裡有）
("['書架', 'estante', 'bookshelf'], ['找到', 'encontrar', 'find']]", "['拿', 'tomar, coger', 'take'], ['找到', 'encontrar', 'find']]", 1),   # FIND：書架（023 刪除）→ 拿（選項「拿《書名》」）
("END: [['喜歡', 'gustar', 'like'], ['禮物', 'regalo', 'gift'], ['謝謝', 'gracias', 'thanks']]", "END: [['喜歡', 'gustar', 'like'], ['包好', 'ya envuelto', 'wrapped'], ['謝謝', 'gracias', 'thanks']]", 1),   # END：禮物（053 刪除）→ 包好（店員那句）
# 拼音（台灣讀音）：怎麼樣 念 zěn me yàng
("'書店': 'shū diàn', '書籤': 'shū qiān',", "'書店': 'shū diàn', '怎麼樣': 'zěn me yàng', '書籤': 'shū qiān',", 1),
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
