import os, sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/ubike/index.html')
s=open(P,encoding='utf-8').read()
def rep(old,new,n=1):
    global s
    c=s.count(old)
    if c!=n: print('次數不對（預期 %d，實際 %d）：%s'%(n,c,old[:70])); sys.exit(1)
    s=s.replace(old,new)
def drop_line(prefix,repl):
    global s
    ls=s.split('\n'); idx=[i for i,l in enumerate(ls) if l.strip().startswith(prefix)]
    if len(idx)!=1: print('行數不對',prefix,len(idx)); sys.exit(1)
    ind=ls[idx[0]][:len(ls[idx[0]])-len(ls[idx[0]].lstrip())]
    ls[idx[0]]=ind+repl; s='\n'.join(ls)
# 002 開頭介紹
rep("    Ami 在公園（或圖書館、夜市）等你。你要用 App 找到有車的站，用悠遊卡借 YouBike，騎過去，再找有空位的站還車。<br>",
    "    你常常在路上看到很多人騎YouBike腳踏車，今天你也想試試看騎YouBike去找Ami。趕快找到一台腳踏車，然後出發吧！<br>")
ES2="Es común ver a mucha gente andar en bicicletas YouBike por la calle, y hoy tú también quieres probarlo para ir a buscar a Ami. ¡Encuentra una bicicleta y arranca!"
EN2="You often see lots of people riding YouBike bikes on the street, and today you want to try riding one to meet Ami. Find a bike quickly and set off!"
OLDES="Ami te espera en el parque (o en la biblioteca, o en el mercado nocturno). Usa la app para encontrar una estación con bicis, alquila una YouBike con tu EasyCard, pedalea hasta allá y devuélvela en una estación con espacio libre."
OLDEN="Ami is waiting for you at the park (or the library, or the night market). Use the app to find a station with bikes, borrow a YouBike with your EasyCard, ride over, and return it at a station with a free dock."
rep(OLDES,ES2,2); rep(OLDEN,EN2,1)
# 016 + 017/018（併成一句）
rep("""      L(`Ami：我在${d[0]}等你。你騎 YouBike 過來吧，很快！`, `Estoy esperándote en ${d[1]}. ¡Ven en YouBike, es muy rápido!`, `I'm waiting for you at ${d[2]}. Come by YouBike — it's really quick!`),
      L('Ami：先打開 App，看看哪一個站有車喔。', 'Primero abre la app y mira en qué estación hay bicicletas.', 'First open the app and see which station has bikes.'),
      L('Ami：還車的時候，也要看 App，找有空位的站。', 'Cuando vayas a devolverla, también mira la app y busca una estación con espacio libre.', 'When you return it, check the app too and find a station with a free dock.')
""","""      L(`Ami：我在${d[0]}等你。你剛剛說要騎 YouBike 過來嗎？太好了！可以先看看App，上面會寫哪裡有車，或是哪裡有空位可以停車喔！`, `Te espero en ${d[1]}. ¿Dijiste que vendrías en YouBike? ¡Genial! Primero mira la app: ahí dice dónde hay bicicletas y dónde hay espacio libre para estacionar.`, `I'm waiting for you at ${d[2]}. Did you say you're coming by YouBike? Great! First check the app — it shows where there are bikes and where there's a free dock to park.`)
""")
# 025
rep("（你走到${s.name}，可是車柱都是空的。你只好再回去看 App。）","（你走到${s.name}，可是車柱都是空的。）")
rep("pero todos los anclajes están vacíos. Tienes que volver a mirar la app.)","pero todos los anclajes están vacíos.)")
rep("but all the docks are empty. You have to check the app again.)","but all the docks are empty.)")
# 032 / 033
rep("M('YouBike 不能投硬幣，要用悠遊卡（或 App）借車。', 'En YouBike no se pagan monedas: se alquila con la EasyCard (o con la app).', \"YouBike doesn't take coins — you borrow with your EasyCard (or the app).\")",
    "M('你不知道嗎？YouBike 不能投硬幣，要用悠遊卡（或 App）借車。', '¿No lo sabías? En YouBike no se pagan monedas: se alquila con la EasyCard (o con la app).', \"Didn't you know? YouBike doesn't take coins — you borrow with your EasyCard (or the app).\")")
rep("M('要先用悠遊卡借車，車柱才會打開，不能直接拉。', 'Primero hay que alquilar con la EasyCard; si no, el anclaje no se abre y no se puede jalar la bici.', \"You have to unlock it with your EasyCard first — you can't just pull the bike out.\")",
    "M('車子會被你拉壞啦！要先用嗶卡借車，車柱才會打開。', '¡Vas a romper la bici si la jalas así! Primero hay que alquilar pasando la tarjeta; solo entonces se abre el anclaje.', \"You'll break the bike pulling it like that! Tap your card to borrow it first — only then does the dock open.\")")
# 035 刪除、043、051 刪除
drop_line("Game.thought = [L('（「嗶」一聲，螢幕寫著「借車成功」","Game.thought = null;")
rep("（你把車拉出來，牽到旁邊，坐上去。座墊太低，腳伸不直，騎起來不舒服。）","（座墊好像太低了，騎起來不舒服。）")
rep("(Sacas la bici, la llevas a un lado y te subes. El asiento está demasiado bajo y no puedes estirar las piernas: es incómodo.)","(El asiento parece demasiado bajo; es incómodo para pedalear.)")
rep("(You pull the bike out, wheel it aside and climb on. The seat is too low — you can't straighten your legs, and it's uncomfortable.)","(The seat seems too low — it's uncomfortable to ride.)")
drop_line("Game.thought = [L('（你調好座墊，騎上路了。","Game.thought = null;")
# 064 / 065
rep("M('紅燈要停下來，行人正在過馬路，很危險。', 'Con luz roja hay que detenerse; hay peatones cruzando y es muy peligroso.', 'Stop at a red light — pedestrians are crossing and it\\'s dangerous.')",
    "M('紅燈要停下來，而且行人正在過馬路，不然很危險！', '¡Con luz roja hay que detenerse, y además hay peatones cruzando; si no, es muy peligroso!', \"Stop at a red light — pedestrians are crossing, otherwise it's dangerous!\")")
rep("M('不能騎上人行道繞過去，紅燈要停下來等。', 'No se puede rodear por la acera: con luz roja se espera.', \"You can't ride around on the sidewalk — wait at the red light.\")",
    "M('不能騎上人行道繞過去喔，紅燈要停下來等欸！', '¡No se puede rodear por la acera! Con luz roja hay que esperar.', \"You can't ride around on the sidewalk! You have to wait at the red light.\")")
# 070 / 071
rep("M(`${s.name}「可還 0 位」，沒有空位可以還車，要去有空位的站。`","M(`${s.name}「可還 0 位」，沒有空位可以還車了，要去有空位的站。`")
rep("（你騎到${s.name}，可是車柱都滿了，沒辦法還車。你只好再看 App。）","（你騎到${s.name}，可是車柱都滿了，沒辦法還車。）")
rep("y no puedes devolver la bici. Tienes que volver a mirar la app.)","y no puedes devolver la bici.)")
rep("so you can't return the bike. You have to check the app again.)","so you can't return the bike.)")
# 078 / 079
rep("M('車要推進車柱才算還車，只放在旁邊，費用會一直算下去。'","M('車要推進車柱才算還車，只放在旁邊的話，費用會一直算下去喔。'")
rep("M('YouBike 不能鎖在欄杆上，要推進車柱還車。'","M('YouBike 不能鎖在欄杆上啦，要推進車柱還車。'")
# 083
rep("""L(`Ami：哇，${N}，你很會騎 YouBike 欸！很方便吧！我們去走走吧！`, `¡Vaya, ${N}, qué bien manejas la YouBike! ¡Es muy práctica, ¿verdad? ¡Vamos a dar una vuelta!`, `Wow, ${N}, you're really good at riding a YouBike! It's so convenient, right? Let's go for a stroll!`)""",
    """L(`Ami：哇，${N}，騎 YouBike 很方便吧！我們去走走吧！`, `¡Vaya, ${N}, qué práctico es andar en YouBike, ¿verdad? ¡Vamos a dar una vuelta!`, `Wow, ${N}, riding a YouBike is so convenient, right? Let's go for a stroll!`)""")
# 單字
rep("['很快', 'muy rápido', 'very quickly']]","['空位', 'espacio libre', 'free dock / space']]")
rep("PULL: [['借車成功', 'alquiler exitoso', 'rental successful'], ['綠燈', 'luz verde', 'green light'], ['紅燈', 'luz roja', 'red light'], ['車柱', 'poste/anclaje de la bicicleta', 'bike dock post'], ['拉出', 'sacar (jalando)', 'pull out']],",
    "PULL: [['綠燈', 'luz verde', 'green light'], ['紅燈', 'luz roja', 'red light'], ['拉出', 'sacar (jalando)', 'pull out'], ['亮', 'encenderse (una luz)', 'light up (be lit)'], ['自己', 'uno mismo, solo', 'by itself / yourself']],")
open(P,'w',encoding='utf-8').write(s)
print('OK')
