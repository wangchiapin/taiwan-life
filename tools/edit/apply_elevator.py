import os
import sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/elevator/index.html')
s=open(P,encoding='utf-8').read()
# 每一筆：(舊字串, 新字串[, 預期出現次數])；找不到就停
# 括號內的編號是線上修改表的列號（rows/elevator.json）
R=[
# 003 開頭介紹
("Ami 住在公寓大樓。今天你要去她家，要搭電梯上樓。電梯裡有按鈕，還會遇到鄰居，要用客氣的話。",
 "你今天要去Ami家，她住在一棟大樓，所以你要搭電梯上樓。搭電梯可能會遇到Ami的鄰居，說話的時候要客氣一點。", 1),
("Ami vive en un edificio de apartamentos. Hoy vas a su casa y tienes que subir en ascensor: hay botones que presionar y vecinos con quienes ser cortés.",
 "Hoy vas a la casa de Ami. Ella vive en un edificio, así que tienes que subir en ascensor. En el ascensor puedes encontrarte con vecinos de Ami; sé cortés al hablar.", 2),
("Ami lives in an apartment building. Today you visit her and take the elevator up. There are buttons to press and neighbors to be polite to.",
 "Today you're going to Ami's home. She lives in a tall building, so you take the elevator up. You may meet Ami's neighbors in the elevator, so speak politely.", 1),
# 011 地點名稱
("shop: ['🏢', '公寓大樓', 'Edificio', 'Apartment building', '']",
 "shop: ['🏢', '大樓', 'Edificio', 'Building', '']", 1),
# 013 刪除 Ami 第二句 LINE
("""      L(`Ami：${N}，我住在${t.n}樓。大樓門口進來就有電梯，你自己上來。`, `${N}, vivo en el piso ${t.n}. El ascensor está justo al entrar; sube tú solo.`, `${N}, I live on floor ${t.n}. The elevator is right inside the entrance — come up on your own.`),
      L('Ami：電梯裡面可能會遇到鄰居，要有禮貌喔！', 'Quizá te encuentres con algún vecino en el ascensor; ¡sé cortés!', 'You may meet a neighbor in the elevator — be polite!')
    ];""",
 """      L(`Ami：${N}，我住在${t.n}樓。大樓門口進來就有電梯，你自己上來。`, `${N}, vivo en el piso ${t.n}. El ascensor está justo al entrar; sube tú solo.`, `${N}, I live on floor ${t.n}. The elevator is right inside the entrance — come up on your own.`)
    ];""", 1),
# 014
("L('（你走到Ami住的公寓大樓。手機響了一聲，是Ami傳來的LINE。）', '(Llegas al edificio de Ami. Tu celular suena: es un LINE de Ami.)', '(You arrive at Ami’s apartment building. Your phone buzzes — a LINE from Ami.)')",
 "L('（你到Ami住的地方了。手機響了一聲，是Ami傳來的LINE。）', '(Llegas al lugar donde vive Ami. Tu celular suena: es un LINE de Ami.)', '(You arrive at Ami’s place. Your phone buzzes — a LINE from Ami.)')", 1),
# 017 刪除一樓大廳旁白
("dialogue: () => [L('（你在一樓大廳，電梯門前有兩個按鈕：▲和▼。）', '(Estás en el vestíbulo del primer piso; frente al ascensor hay dos botones: ▲ y ▼.)', '(You are in the first-floor lobby. There are two buttons by the elevator: ▲ and ▼.)'), L(`我：Ami住在${t.n}樓，我要按哪一個？`,",
 "dialogue: () => [L(`我：Ami住在${t.n}樓，我要按哪一個？`,", 1),
# 022
("M(`Ami住在${t.n}樓，在一樓要往上。`,", "M(`Ami住在${t.n}樓，在一樓要往上啦。`,", 1),
# 024 刪除「電梯來了，門打開了」
("          Game.thought = [L('（電梯來了，門打開了。你走進去。）', '(Llega el ascensor y se abre la puerta. Entras.)', '(The elevator arrives and the door opens. You step in.)')];\n", "", 1),
# 030
("M('鄰居在跑，要按「開門」等他。', 'El vecino viene corriendo: hay que presionar «abrir» y esperarlo.', 'The neighbor is running — press \"open\" and wait.')",
 "M('鄰居要來了，要好心一點幫他按著「開」。', 'El vecino ya viene: sé amable y mantén presionado el botón «abrir» para él.', 'The neighbor is coming — be kind and hold the \"open\" button for them.')", 1),
# 033 刪除電梯裡的按鈕旁白
("dialogue: () => [L('（電梯裡有一排樓層按鈕。）', '(En el ascensor hay una fila de botones de piso.)', '(There is a row of floor buttons in the elevator.)'), L(`我：Ami住在${t.n}樓。`,",
 "dialogue: () => [L(`我：Ami住在${t.n}樓。`,", 1),
# 036
("M(`Ami住在${t.n}樓。`, `Ami vive en el piso ${t.n}.`, `Ami lives on floor ${t.n}.`)",
 "M(`你記錯了喔！Ami住在${t.n}樓。`, `¡Te equivocaste! Ami vive en el piso ${t.n}.`, `You got it wrong! Ami lives on floor ${t.n}.`)", 1),
# 038、039（兩處：FLOOR 的過場和 HELP 的對話）
("nb(`不好意思，我到${t.m}樓，麻煩你幫我按。`,",
 "nb(`不好意思，我要到${t.m}樓，麻煩你幫我按一下。`,", 2),
# 042 選項文字；判斷「不會」改成「不好」
("'我不會說中文。']", "'我中文不好。']", 1),
("c.includes('不會')", "c.includes('不好')", 1),
# 043
("M('鄰居只是請你幫忙按一個鈕，很簡單。', 'El vecino solo te pide presionar un botón; es fácil.', 'The neighbor only asks you to press a button — easy.')",
 "M('鄰居只是請你幫忙按一個鈕，應該不難吧！', 'El vecino solo te pide presionar un botón; ¡no debería ser difícil!', 'The neighbor only asks you to press a button — it shouldn\\'t be hard!')", 1),
# 044
("M(`鄰居要到${t.m}樓。`, `El vecino va al piso ${t.m}.`, `The neighbor is going to floor ${t.m}.`)",
 "M(`聽清楚一點，鄰居要到${t.m}樓。`, `Escucha con más atención: el vecino va al piso ${t.m}.`, `Listen more carefully: the neighbor is going to floor ${t.m}.`)", 1),
# 046
("L(`（電梯往上，在${t.m}樓停了，門打開。）`, `(El ascensor sube, se detiene en el piso ${t.m} y se abre la puerta.)`, `(The elevator goes up, stops at floor ${t.m} and the door opens.)`)",
 "L(`（電梯向上，在${t.m}樓的時候電梯停了下來。）`, `(El ascensor sube y se detiene en el piso ${t.m}.)`, `(The elevator goes up and stops at floor ${t.m}.)`)", 1),
# 052
("M('鄰居要下電梯，可以說「慢走」。', 'El vecino se baja: puedes decir «慢走».', 'The neighbor is leaving — you can say \"慢走\".')",
 "M('鄰居要出電梯了，可以禮貌地說「慢走」。', 'El vecino va a salir del ascensor: puedes decirle «慢走» con cortesía.', 'The neighbor is getting out — you can politely say \"慢走\".')", 1),
# 053
("goodFirst('STOP', '「慢走」是跟離開的人說的客氣話。', '«慢走» es una frase cortés para quien se va.', '\"慢走\" is a polite thing to say to someone leaving.');",
 "goodFirst('STOP', '你學會了！「慢走」是跟離開的人說的客氣話。', '¡Lo aprendiste! «慢走» es una frase cortés para quien se va.', 'You learned it! \"慢走\" is a polite thing to say to someone leaving.');", 1),
# 054
("L(`（電梯繼續往上，到${t.n}樓了。門口站了很多人，你前面有人擋著。）`, `(El ascensor sigue subiendo y llega al piso ${t.n}. Hay gente delante de ti, bloqueando la salida.)`, `(The elevator continues up to floor ${t.n}. There are people in front of you, blocking the way.)`)",
 "L(`（電梯繼續往上，到${t.n}樓了。）`, `(El ascensor sigue subiendo y llega al piso ${t.n}.)`, `(The elevator continues up to floor ${t.n}.)`)", 1),
# 055（Ben 同意：保留「前面站著人」，借過才有原因）
("L(`（${t.n}樓到了，門開了。可是前面有人站著。）`,",
 "L(`（${t.n}樓到了，門開了。前面站著人。）`,", 1),
# 060
("M('要出去時，客氣地說「借過一下」。', 'Para salir, di cortésmente «借過一下».', 'To get out, politely say \"借過一下\".')",
 "M('要出去時，客氣地說「借過一下」比較好喔！', 'Para salir, es mejor decir cortésmente «借過一下».', 'To get out, it\\'s better to politely say \"借過一下\".')", 1),
# 062
("L(`（你走到Ami家門口，按了電鈴。）`,", "L(`（你到Ami家門口，按了電鈴。）`,", 1),
# 063
("L(`Ami：${N}，你來了！電梯很好搭吧？歡迎歡迎！`, `¡${N}, llegaste! ¿Fue fácil el ascensor? ¡Bienvenido!`, `${N}, you made it! The elevator was easy, right? Welcome!`)",
 "L(`Ami：${N}，你來了！搭電梯不難吧？歡迎歡迎！`, `¡${N}, llegaste! ¿Verdad que subir en ascensor no fue difícil? ¡Qué bueno que viniste!`, `${N}, you made it! Taking the elevator wasn't hard, right? Welcome!`)", 1),
# 064
("L(`Ami：${N}，你終於來了！剛剛好像有點不順利？沒關係，進來吧！`, `¡${N}, por fin llegaste! ¿Parece que hubo problemas? No pasa nada, ¡pasa!`, `${N}, you're finally here! Looks like it didn't go smoothly? No worries — come in!`)",
 "L(`Ami：${N}，你終於來了！用中文搭電梯還順利嗎？沒關係，進來吧！`, `¡${N}, por fin llegaste! ¿Cómo te fue subiendo en ascensor en chino? No pasa nada, ¡pasa!`, `${N}, you're finally here! How did taking the elevator in Chinese go? No worries — come in!`)", 1),
# 單字表：對話裡已經沒有的詞，換成畫面上有出現的詞
("['公寓', 'edificio de apartamentos', 'apartment building'], ['鄰居', 'vecino(a)', 'neighbor']]",
 "['大樓', 'edificio', 'building'], ['住在', 'vivir en', 'live at']]", 1),   # START：公寓→大樓；鄰居（013 刪除後 START 沒有）→住在
("[['大廳', 'vestíbulo', 'lobby'], ['按鈕', 'botón', 'button'], ['往上', 'hacia arriba', 'up'], ['往下', 'hacia abajo', 'down']]",
 "[['按', 'presionar', 'press'], ['哪一個', '¿cuál?', 'which one?'], ['往上', 'hacia arriba', 'up'], ['往下', 'hacia abajo', 'down']]", 1),   # LOBBY：017 刪除後大廳、按鈕沒有出現
("['按', 'presionar', 'press'], ['幾樓', '¿qué piso?', 'which floor?']]",
 "['按', 'presionar', 'press'], ['住在', 'vivir en', 'live at']]", 1),   # FLOOR：幾樓（原本就沒出現）→住在
("[['按電鈴', 'tocar el timbre', 'ring the doorbell'],", "[['電鈴', 'timbre', 'doorbell'],", 1),   # END：句子是「按了電鈴」，原本的「按電鈴」對不上
# 拼音（台灣讀音）：新句子用到 著、喔、啦、沒關係、還
("pinyinPro.customPinyin({ '和': 'hàn', '嗯': 'ēn' });",
 "pinyinPro.customPinyin({ '和': 'hàn', '嗯': 'ēn' });\npinyinPro.customPinyin({ '著': 'zhe', '喔': 'ō', '啦': 'la', '關係': 'guān xi', '還順利': 'hái shùn lì' });", 1),
]
for r in R:
    old,new=r[0],r[1]
    n=r[2] if len(r)>2 else 1
    c=s.count(old)
    if c!=n:
        print('次數不對（預期 %d，實際 %d）：%s'%(n,c,old[:60])); sys.exit(1)
    s=s.replace(old,new)
open(P,'w',encoding='utf-8').write(s)
print('OK，共 %d 筆'%len(R))
