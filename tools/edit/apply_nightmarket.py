import os
import sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/nightmarket/index.html')
s=open(P,encoding='utf-8').read()
# 每一筆：(舊字串, 新字串[, 預期出現次數])；找不到就停
# 括號內的編號是線上修改表的列號（rows/nightmarket.json）
R=[
# 002 開頭介紹（中文＋西文／英文，西文在 data-es 和 span 各一次）
(r"""晚上，你和同事 Ami、Ami 的奶奶一起逛夜市。Ami 帶奶奶去洗手間，把一千塊交給你，請你幫忙買東西。會殺價，就能省下錢！""",
 r"""你和Ami、Ami 的奶奶一起去逛夜市。Ami 帶奶奶去上廁所，所以她把一千塊給你，請你幫忙買東西。敢殺價，就能省下錢！""", 1),
(r"""Por la noche paseas por el mercado nocturno con tu compañera Ami y su abuela. Ami lleva a su abuela al baño y te deja mil dólares para que compres unas cosas. ¡Si sabes regatear, ahorras!""",
 r"""Paseas por el mercado nocturno con Ami y su abuela. Ami lleva a su abuela al baño, así que te da mil dólares y te pide que compres unas cosas. ¡Si te atreves a regatear, ahorras!""", 2),
(r"""In the evening you wander the night market with your coworker Ami and her grandma. Ami takes her grandma to the restroom and hands you NT$1,000 to buy a few things. If you can haggle, you save money!""",
 r"""You're strolling the night market with Ami and her grandma. Ami takes her grandma to the restroom, so she gives you NT$1,000 and asks you to buy a few things. If you dare to haggle, you save money!""", 1),
# 018 + 019 + 020（019 併入 018；020 刪除，Ben 決定）
(r"""      L(`Ami：${N}，我帶奶奶去洗手間，這一千塊先給你，幫我們買東西，好不好？`,
        `${N}, voy a llevar a mi abuela al baño. Te dejo estos mil dólares: ¿puedes comprar unas cosas por nosotras?`,
        `${N}, I'm taking my grandma to the restroom. Here's NT$1,000 for now. Can you buy a few things for us?`),
      L('Ami：要買的我都寫在清單上了。衣服和飾品可以殺價，但是吃的不要殺價喔，老闆會不高興。',
        'Todo lo que hay que comprar está en la lista. En la ropa y los accesorios se puede regatear, pero la comida no: al vendedor no le gusta.',
        "Everything we need is on the list. You can haggle for clothes and accessories, but not for food — the vendors won't like it."),
      L('Ami：還有，殺價的時候，如果你說要「再看看」，老闆常常就會降價了！',
        'Y además, cuando regatees, si dices que vas a «mirar un poco más», ¡el vendedor suele bajar el precio!',
        'Also, when you haggle, if you say you\'ll "look around a bit more," the vendor will often lower the price!')
    ];""",
 r"""      L(`Ami：${N}，我帶奶奶去上廁所，錢先給你，你先去幫我買東西。要買的我都寫在清單上了。衣服和飾品可以殺價，殺價的時候要有技巧喔！但是，吃的不要殺價喔，老闆會不高興！`,
        `${N}, voy a llevar a mi abuela al baño. Te dejo el dinero primero y tú ve a comprarme unas cosas. Todo lo que hay que comprar está en la lista. En la ropa y los accesorios se puede regatear, ¡pero hay que tener maña! Eso sí, la comida no se regatea: al vendedor no le gusta.`,
        `${N}, I'm taking my grandma to the restroom. I'll give you the money first, so go ahead and buy a few things for me. Everything we need is on the list. You can haggle for clothes and accessories, but you need some technique! Just don't haggle for food, because the vendors won't like it.`)
    ];"""),
# 049 開場旁白刪除
(r"""          L('（週末晚上，你和Ami、Ami的奶奶一起逛夜市，人好多，好熱鬧！）',
            '(Es una noche de fin de semana y paseas por el mercado nocturno con Ami y su abuela. ¡Hay mucha gente y mucho ambiente!)',
            '(It\'s a weekend night, and you\'re strolling the night market with Ami and her grandma. It\'s crowded and lively!)'),
          ...Game.amiLines(),""",
 r"""          ...Game.amiLines(),"""),
# 023 + 024（024 併入 023；長高→變胖）
(r"""      L(`Ami：${N}，東西買好了嗎？我弟弟剛剛傳訊息給我，他說他最近長高了，${t.tSize}號可能太小了！`,
        `${N}, ¿ya compraste todo? Mi hermano acaba de escribirme: dice que creció últimamente y que la talla ${t.tSize} quizá le quede pequeña.`,
        `${N}, did you get everything? My little brother just texted me. He says he's grown taller lately, so size ${t.tSize} might be too small!`),
      L(`Ami：可以幫他換${t.bigSize}號嗎？拜託拜託！`,
        `¿Puedes cambiársela por la talla ${t.bigSize}? ¡Por favor, por favor!`,
        `Could you exchange it for a size ${t.bigSize}? Please, please!`)
    ];""",
 r"""      L(`Ami：${N}，東西買好了嗎？我突然想到我弟最近變胖了，${t.tSize}號可能太小了！可以幫他換${t.bigSize}號嗎？拜託拜託！`,
        `${N}, ¿ya compraste todo? De repente me acordé de que mi hermano ha engordado últimamente y que la talla ${t.tSize} quizá le quede pequeña. ¿Puedes cambiársela por la talla ${t.bigSize}? ¡Por favor, por favor!`,
        `${N}, did you get everything? I just remembered my little brother has gained some weight lately, so size ${t.tSize} might be too small! Could you exchange it for a size ${t.bigSize}? Please, please!`)
    ];"""),
# 039 綠卡（再看看）
(r"""this.good('你說了「再看看」，老闆就降價了！', 'Dijiste «mirar un poco más» y el vendedor bajó el precio.', 'You said you\'d look around some more, and the vendor dropped the price!')""",
 r"""this.good('聰明喔！你說了「再看看」，老闆就降價了！', '¡Qué lista! Dijiste «mirar un poco más» y el vendedor bajó el precio.', 'Smart! You said you\'d look around some more, and the vendor dropped the price!')"""),
# 046 任務提示標題
(r"""r('Ami 在夜市說的話')""", r"""r('Ami 說的話')"""),
# 061
(r"""[L('（等等，清單上寫的是什麼顏色？）', '(Espera, ¿de qué color decía la lista?)', '(Wait, what color does the list say?)')]""",
 r"""[L('（等等，Ami說要買什麼顏色的衣服？）', '(Espera, ¿de qué color de ropa dijo Ami que comprara?)', '(Wait, what color of clothes did Ami say to buy?)')]"""),
# 065（喔→啦）
(r"""三個比較划算喔！`,""", r"""三個比較划算啦！`,""", 1),
# 075
(r"""[L('（等等，清單上寫一個就好……）', '(Espera, la lista dice que basta con uno…)', '(Wait, the list says just one…)')]""",
 r"""[L('（等等，Ami說買一個就好……）', '(Espera, Ami dijo que con uno basta…)', '(Wait, Ami said just one is enough…)')]"""),
# 076 綠卡
(r"""Game.good('你看清單，只買一個。', 'Miraste la lista y compraste solo uno.', 'You checked the list and bought just one.')""",
 r"""Game.good('還好你有確認過清單，只買一個。', 'Menos mal que revisaste la lista: compraste solo uno.', 'Good thing you checked the list: you bought just one.')"""),
# 086 + 087（087 提示話刪除）
(r"""            Game.addMistake(M(`清單上寫${CN[t.chicken]}份。`, `La lista decía ${t.chicken} porciones.`, `The list said ${t.chicken} servings.`),
              [L('（看一下清單，要幾份？）', '(Mira la lista: ¿cuántas porciones?)', '(Check the list: how many servings?)')]); return;""",
 r"""            Game.addMistake(M(`Ami說${CN[t.chicken]}份。`, `Ami dijo ${t.chicken} porciones.`, `Ami said ${t.chicken} servings.`)); return;"""),
# 093 旁白刪除
(r"""            Game.addMistake(M('奶奶不吃辣，要一份不要辣。', 'La abuela no come picante: una porción sin picante.', "Grandma doesn't eat spicy food: one serving without spice."),
              [L('（清單上寫奶奶的那份……）', '(La lista dice algo sobre la porción de la abuela…)', "(The list says something about grandma's serving…)")]); return;""",
 r"""            Game.addMistake(M('奶奶不吃辣，要一份不要辣。', 'La abuela no come picante: una porción sin picante.', "Grandma doesn't eat spicy food: one serving without spice.")); return;"""),
# 094 綠卡
(r"""Game.good('你記得奶奶不吃辣。', 'Recordaste que la abuela no come picante.', "You remembered grandma doesn't eat spicy food.")""",
 r"""Game.good('很棒喔！你記得奶奶不吃辣。', '¡Muy bien! Recordaste que la abuela no come picante.', "Great job! You remembered grandma doesn't eat spicy food.")"""),
# 098
(r"""M('清單上寫要切。', 'La lista decía que lo cortaran.', 'The list said to have it cut up.')""",
 r"""M('Ami說要切。', 'Ami dijo que lo cortaran.', 'Ami said to have it cut up.')"""),
# 105 老闆的回應
(r"""[L('老闆：吃的不能殺價啦，我們賺很少耶！', '¡La comida no se regatea, ganamos muy poco!', "You can't haggle over food — we barely make anything!")]""",
 r"""[L('老闆：不要這樣啦，現在雞肉很貴欸！', '¡No hagas eso, ahora el pollo está carísimo!', "Come on, don't do that — chicken is really expensive these days!")]"""),
# 108 綠卡
(r"""Game.good('吃的東西不殺價，你直接付錢了。', 'No regateaste por la comida: pagaste directamente.', "You didn't haggle over food — you just paid.")""",
 r"""Game.good('讚喔！你記得Ami說吃的東西不要殺價！', '¡Genial! ¡Recordaste que Ami dijo que no se regatea la comida!', "Awesome! You remembered Ami said not to haggle over food!")"""),
# 126 綠卡
(r"""Game.good('你記得老闆說每個尺寸都一樣價錢。', 'Recordaste que el vendedor dijo que todas las tallas cuestan igual.', 'You remembered the vendor said every size costs the same.')""",
 r"""Game.good('太好了！你記得老闆說每個尺寸都一樣價錢。', '¡Qué bien! Recordaste que el vendedor dijo que todas las tallas cuestan igual.', 'Great! You remembered the vendor said every size costs the same.')"""),
# 127（拿掉「不用加錢」，西英文跟著改）
(r"""[L('老闆：哈哈，被你發現了！好啦好啦，直接換給你，不用加錢。', '¡Jaja, me descubriste! Está bien, te la cambio directamente, sin cobrarte más.', "Haha, you caught me! Fine, fine — I'll just swap it, no extra charge.")]""",
 r"""[L('老闆：哈哈，被你發現了！好啦好啦，直接換給你啦！', '¡Jaja, me descubriste! Está bien, está bien, ¡te la cambio directamente!', "Haha, you caught me! Fine, fine — I'll just swap it for you!")]"""),
# 129 + 130（130 併入 129；沒省到錢就不加這句，跟原本一樣）
(r"""            L(`我：Ami，東西都買好了！一共花了${spent}元，還剩${Game.cash}元。`, `¡Ami, ya compré todo! Gasté ${esM(spent)} en total y sobraron ${esM(Game.cash)}.`, `Ami, I got everything! I spent ${enM(spent)} in total, and ${enM(Game.cash)} is left.`)
          ];
          if (Game.saved > 0) lines.push(L(`我：衣服和髮夾，我殺價省了${Game.saved}元！`, `¡En la ropa y el pasador regateé y ahorré ${esM(Game.saved)}!`, `I haggled on the shirt and the hairpin and saved ${enM(Game.saved)}!`));
""",
 r"""            L(`我：Ami，東西都買好了！一共花了${spent}元，還剩${Game.cash}元。${Game.saved > 0 ? '衣服和髮夾，我殺價省了' + Game.saved + '元！' : ''}`,
              `¡Ami, ya compré todo! Gasté ${esM(spent)} en total y sobraron ${esM(Game.cash)}.${Game.saved > 0 ? ' ¡En la ropa y el pasador regateé y ahorré ' + esM(Game.saved) + '!' : ''}`,
              `Ami, I got everything! I spent ${enM(spent)} in total, and ${enM(Game.cash)} is left.${Game.saved > 0 ? ' I haggled on the shirt and the hairpin and saved ' + enM(Game.saved) + '!' : ''}`)
          ];
"""),
# 131
(r"""L(`Ami：哇，${N}，你比我還會殺價耶！下次逛夜市都帶你來！`, `¡Vaya, ${N}, regateas mejor que yo! ¡La próxima vez que vayamos al mercado nocturno te traigo!`, `Wow, ${N}, you're better at haggling than I am! I'll bring you every time we go to the night market!`)""",
 r"""L(`Ami：哇，${N}，你比我還會殺價耶！看來中文學得不錯喔！`, `¡Vaya, ${N}, regateas mejor que yo! ¡Parece que estás aprendiendo muy bien el chino!`, `Wow, ${N}, you're better at haggling than I am! Looks like your Chinese is coming along well!`)"""),
# 132
(r"""L('Ami：辛苦了！有些地方下次再注意就好。', '¡Gracias por el esfuerzo! La próxima vez cuida unos detallitos y listo.', "Thanks for your hard work! Just watch out for a few things next time.")""",
 r"""L('Ami：辛苦了！我們下次再一起來夜市試試看。', '¡Gracias por el esfuerzo! La próxima vez volvamos a venir juntas al mercado nocturno a intentarlo otra vez.', "Thanks for your hard work! Let's come to the night market together again next time and give it another try.")"""),
# 單字：對話裡已經沒有的詞，換成新出現的詞
(r"""START: [['同事', 'compañero de trabajo', 'coworker'],""", r"""START: [['技巧', 'técnica, maña', 'technique, knack'],"""),
(r"""['再看看', 'mirar un poco más', 'look around some more']],
  MAP:""", r"""['敢', 'atreverse', 'dare']],
  MAP:"""),
(r"""CALL: [['長高', 'crecer en estatura', 'grow taller'],""", r"""CALL: [['變胖', 'engordar', 'gain weight'],"""),
(r"""['排', 'hacer fila', 'line up']],""", r"""['排', 'hacer fila', 'line up'], ['貴', 'caro', 'expensive']],"""),
]
bad=0
for r in R:
    a,b=r[0],r[1]; want=r[2] if len(r)>2 else None
    n=s.count(a)
    if n<1 or (want is not None and n!=want): print('MISSING/COUNT:',n,want,a[:90]); bad+=1; continue
    s=s.replace(a,b)
if bad: sys.exit(1)
open(P,'w',encoding='utf-8').write(s); print('ok',len(R))
