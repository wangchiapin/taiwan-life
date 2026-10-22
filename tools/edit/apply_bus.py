import os
import sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/bus/index.html')
s=open(P,encoding='utf-8').read()
# 每一筆：(舊字串, 新字串[, 預期出現次數])；找不到就停
# 括號內的編號是線上修改表的列號（rows/bus.json）
R=[
# 003 開頭介紹（Ben 寫「找他」，Ami 是女生，改成「找她」）
('''Ami 在某一站等你。你要看站牌、看電子看板、對公車招手，上車刷卡，問司機，在對的站按下車鈴，下車再刷一次卡。''',
 '''Ami 在某個公車站等你。你要搭公車過去找她，搭公車要注意的事情你都知道嗎？''', 1),
('''Ami te espera en una parada. Lee el letrero de la parada y el tablero electrónico, hazle señas al autobús, pasa tu tarjeta al subir, pregunta al conductor, presiona el timbre en la parada correcta y vuelve a pasar la tarjeta al bajar.''',
 '''Ami te espera en una parada de autobús. Tienes que ir a buscarla en autobús. ¿Sabes todo lo que hay que tener en cuenta al tomar el autobús?''', 2),
('''Ami is waiting at a stop. Read the bus stop sign and the electronic board, wave down the bus, tap your card on boarding, ask the driver, press the bell at the right stop, and tap off when you get out.''',
 '''Ami is waiting at a bus stop. You need to take the bus to meet her. Do you know everything you should watch out for when riding the bus?''', 1),
# 017、018（Ben 把 018 併進 017，018 刪除）、019
('''      L(`Ami：你搭${t.route[1]}路公車，往${t.dir}方向。`, `Toma el autobús ${t.route[0]}, en dirección a ${d[0]}.`, `Take bus ${t.route[0]}, toward ${d[1]}.`),
      L(`Ami：在${t.dest}站下車。`, `Bájate en la parada ${t.dest}.`, `Get off at ${t.dest} Stop.`),
      L('Ami：上車要刷悠遊卡，下車也要刷喔。', 'Pasa tu EasyCard al subir, y también al bajar.', 'Tap your EasyCard when you get on, and again when you get off.')''',
 '''      L(`Ami：你搭${t.route[1]}路公車，往${t.dir}方向，在${t.dest}站下車。`, `Toma el autobús ${t.route[0]}, en dirección a ${d[0]}, y bájate en la parada ${t.dest}.`, `Take bus ${t.route[0]}, toward ${d[1]}, and get off at ${t.dest} Stop.`),
      L('Ami：記得，上車要刷悠遊卡，下車也要刷喔。', 'Recuerda: pasa tu EasyCard al subir, y también al bajar.', 'Remember: tap your EasyCard when you get on, and again when you get off.')''', 1),
# 024 刪除「我要在哪一邊等車呢？」
(''', L('我：我要在哪一邊等車呢？', '¿De qué lado espero el autobús?', 'Which side should I wait on?')]''', ''']''', 1),
# 028、029、030
('''M(`你要去${t.dir}那個方向，要在「往${t.dir}」的站牌等。`, `Tu destino queda en dirección a ${dEs[0]}: hay que esperar en la parada «往${t.dir}».`, `You're heading toward ${dEs[1]}, so wait at the "往${t.dir}" stop.`)''',
 '''M(`走錯了啦！你要去${t.dir}那個方向，要在「往${t.dir}」的站牌等。`, `¡Te equivocaste de lado! Tu destino queda en dirección a ${dEs[0]}: hay que esperar en la parada «往${t.dir}».`, `Wrong side! You're heading toward ${dEs[1]}, so wait at the "往${t.dir}" stop.`)''', 1),
('''M('要先看站牌，確定公車往哪個方向。', 'Primero hay que mirar el letrero de la parada para saber hacia dónde va el autobús.', 'Check the bus stop sign first to make sure which way the bus goes.')''',
 '''M('要先看站牌，才可以確定公車往哪個方向。', 'Primero hay que mirar el letrero de la parada para poder saber hacia dónde va el autobús.', 'Check the bus stop sign first so you can be sure which way the bus goes.')''', 1),
('''goodFirst('STOP', '你看對站牌了！搭公車要看「往…」，確定方向。', '¡Leíste bien el letrero! Al tomar el autobús hay que fijarse en «往…» para confirmar la dirección.', 'You read the sign right! When taking a bus, check the "往…" (toward…) to confirm the direction.');''',
 '''goodFirst('STOP', '你看對站牌了！搭公車要看往哪裡，確定方向。', '¡Leíste bien el letrero! Al tomar el autobús hay que fijarse hacia dónde va para confirmar la dirección.', 'You read the sign right! When taking a bus, check where it is heading to confirm the direction.');''', 1),
# 031 刪除「站牌旁邊有一個電子看板」
('''L('（站牌旁邊有一個電子看板，寫著公車幾分鐘後到。）', '(Junto a la parada hay un tablero electrónico que indica en cuántos minutos llega cada autobús.)', '(Beside the stop there is an electronic board showing how many minutes until each bus arrives.)'), ''', '', 1),
# 034
('''不是${b.r[1]}路。`, `Tienes que tomar''', '''不是${b.r[1]}路喔。`, `Tienes que tomar''', 1),
# 036
('''L(`（你等了${b0(t)}分鐘。遠遠地，公車開過來了！）`, `(Esperas ${b0(t)} minutos. A lo lejos viene el autobús.)`, `(You wait ${b0(t)} minutes. The bus comes down the road!)`)''',
 '''L(`（你等了${b0(t)}分鐘，公車終於來了！）`, `(Esperas ${b0(t)} minutos y por fin llega el autobús.)`, `(You wait ${b0(t)} minutes, and the bus finally comes!)`)''', 1),
# 037、038（038 刪除「要怎麼辦呢？」）
('''L(`（車頭的螢幕寫著：${t.route[0]}，往${t.dir}。是你要搭的公車！）`, `(La pantalla del frente dice: ${t.route[0]}, hacia ${dEs[0]}. ¡Es tu autobús!)`, `(The sign on the front reads: ${t.route[0]}, toward ${dEs[1]}. It's your bus!)`), L('我：要怎麼辦呢？', '¿Qué hago?', 'What should I do?')]''',
 '''L(`（公車上面寫：${t.route[0]}，往${t.dir}。）`, `(El autobús dice: ${t.route[0]}, hacia ${dEs[0]}.)`, `(The bus says: ${t.route[0]}, toward ${dEs[1]}.)`)]''', 1),
# 042、043、044
('''M('在台灣，要對公車招手，司機才知道你要搭車。', 'En Taiwán hay que hacerle señas al autobús para que el conductor sepa que quieres subir.', 'In Taiwan you wave at the bus so the driver knows you want to board.')''',
 '''M('要對公車招手，司機才知道你要搭車。', 'Hay que hacerle señas al autobús para que el conductor sepa que quieres subir.', 'Wave at the bus so the driver knows you want to board.')''', 1),
('''M('不可以走到馬路中間，很危險。要在站牌旁邊招手。', 'No se debe caminar al medio de la calle: es muy peligroso. Haz señas desde la parada.', "Never step into the road — it's dangerous. Wave from beside the stop sign.")''',
 '''M('不可以走到馬路中間，很危險。', 'No se debe caminar al medio de la calle: es muy peligroso.', "Never step into the road — it's dangerous.")''', 1),
('''goodFirst('HAIL', '做得好！在台灣，要對公車招手，公車才會停。', '¡Bien hecho! En Taiwán hay que hacer señas para que el autobús se detenga.', 'Well done! In Taiwan you have to wave to make the bus stop.');''',
 '''goodFirst('HAIL', '做得好！要對公車招手，公車才會停。', '¡Bien hecho! Hay que hacer señas para que el autobús se detenga.', 'Well done! You have to wave to make the bus stop.');''', 1),
# 045 刪除「公車停下來，車門打開了」
('''Game.thought = [L('（公車停下來，車門打開了。）', '(El autobús se detiene y se abre la puerta.)', '(The bus stops and the door opens.)')];''', '''Game.thought = null;''', 1),
# 046（牌子現在寫「上下車刷卡」）、050
('''L('（你上車了。前面有一台刷卡機，旁邊的牌子寫著：「上車刷卡，下車刷卡」。）', '(Subes. Delante hay un lector de tarjetas y un letrero que dice: «上車刷卡，下車刷卡» —pasar la tarjeta al subir y al bajar—.)', '(You board. There\\'s a card reader at the front with a sign: "上車刷卡，下車刷卡" — tap on and tap off.)')''',
 '''L('（「上下車刷卡」。）', '(El letrero dice: «上下車刷卡» —pasar la tarjeta al subir y al bajar—.)', '(The sign reads: "上下車刷卡" — tap on and tap off.)')''', 1),
('''M('牌子寫「上車刷卡，下車刷卡」，上車的時候就要刷，下車還要再刷一次。', 'El letrero dice «上車刷卡，下車刷卡»: se pasa la tarjeta al subir y otra vez al bajar.', 'The sign says 上車刷卡，下車刷卡: tap when you board, and tap again when you get off.')''',
 '''M('牌子寫「上下車刷卡」，上車的時候就要刷，下車還要再刷一次。', 'El letrero dice «上下車刷卡»: se pasa la tarjeta al subir y otra vez al bajar.', 'The sign says 上下車刷卡: tap when you board, and tap again when you get off.')''', 1),
# 054、055
('''所以你問司機。）`, `(No estás seguro de que este autobús llegue a la parada ${t.dest}, así que le preguntas al conductor.)`, `(You're not sure this bus goes to ${t.dest} Stop, so you ask the driver.)`)''',
 '''所以你想問問看司機。）`, `(No estás seguro de que este autobús llegue a la parada ${t.dest}, así que quieres preguntarle al conductor.)`, `(You're not sure this bus goes to ${t.dest} Stop, so you want to ask the driver.)`)''', 1),
('''rot([`司機，請問這台公車有到${t.dest}站嗎？`,''', '''rot([`司機大哥，請問這台公車有到${t.dest}站嗎？`,''', 1),
# 058、059
('''不可以叫司機開快一點，這樣不禮貌，也不安全。你要問的是：這台車有沒有到你要去的站。', 'No se le pide al conductor que maneje más rápido: es descortés y poco seguro. Lo que debes preguntar es si este autobús llega a tu parada.', "Don't tell the driver to go faster — it's rude and unsafe. What you need to ask is whether this bus goes to your stop.")''',
 '''不可以叫司機開快一點，這樣不禮貌，也不安全。', 'No se le pide al conductor que maneje más rápido: es descortés y poco seguro.', "Don't tell the driver to go faster — it's rude and unsafe.")''', 1),
('''你才剛上車，還不用下車。你要先問司機有沒有到你要去的站。''', '''你才剛上車，還不用下車。可以先問問司機有沒有到你要去的站。''', 1),
('''Primero pregunta al conductor si el autobús llega a tu parada.''', '''Puedes preguntar primero al conductor si el autobús llega a tu parada.''', 1),
('''First ask the driver whether the bus goes to your stop.''', '''You can first ask the driver whether the bus goes to your stop.''', 1),
# 061 刪除「你找了一個位子坐下來」
('''Game.thought = [Game.driverLine(), L('（你找了一個位子坐下來。）', '(Buscas un asiento y te sientas.)', '(You find a seat and sit down.)')];''', '''Game.thought = [Game.driverLine()];''', 1),
# 067 刪除「你按了下車鈴……公車慢慢停下來」
('''Game.thought = [L('（你按了下車鈴，「叮咚」一聲，車上的燈亮了。公車慢慢停下來。）', '(Presionas el timbre: «¡ding-dong!» y se enciende la luz. El autobús se detiene poco a poco.)', '(You press the bell — ding-dong! — and the light comes on. The bus slowly stops.)')];''', '''Game.thought = null;''', 1),
# 068
('''L(`（公車到${next}站了，沒有人下車。）`, `(El autobús llega a ${next}; nadie baja.)`, `(The bus reaches ${next}; nobody gets off.)`)''',
 '''L(`（公車到站：${next}。）`, `(El autobús llega a la parada: ${next}.)`, `(The bus reaches the stop: ${next}.)`)''', 1),
# 069 刪除「公車停了，車門打開」；070「要下車了」留著當這一關的問題（Ben 同意）
('''L('（公車停了，車門打開。）', '(El autobús se detiene y se abre la puerta.)', '(The bus stops and the door opens.)'), ''', '', 1),
# 074（牌子現在寫「上下車刷卡」）
('''M('牌子寫「下車刷卡」，下車也要刷悠遊卡。', 'El letrero decía «下車刷卡»: al bajar también hay que pasar la EasyCard.', 'The sign said 下車刷卡: you tap your EasyCard when you get off, too.')''',
 '''M('你忘記了嗎？牌子寫「上下車刷卡」，下車也要刷悠遊卡。', '¿Lo olvidaste? El letrero decía «上下車刷卡»: al bajar también hay que pasar la EasyCard.', 'Did you forget? The sign said 上下車刷卡: you tap your EasyCard when you get off, too.')''', 1),
# 079（Ben 照他的寫法；西文、英文用不分性別的說法）
('''L(`Ami：哇，${N}，你很會搭公車欸！公車很方便吧！我們去走走吧！`, `¡Vaya, ${N}, qué bien tomas el autobús! ¡Es muy práctico, ¿verdad? ¡Vamos a dar una vuelta!`, `Wow, ${N}, you're really good at taking the bus! It's so convenient, right? Let's go for a stroll!`)''',
 '''L(`Ami：哇，${N}，解鎖自己搭公車欸！公車很方便吧！我們去走走吧！`, `¡Vaya, ${N}, desbloqueaste el logro de tomar el autobús por tu cuenta! ¡Es muy práctico, ¿verdad? ¡Vamos a dar una vuelta!`, `Wow, ${N}, you unlocked taking the bus on your own! It's so convenient, right? Let's go for a stroll!`)''', 1),
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
