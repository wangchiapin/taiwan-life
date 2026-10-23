import os, sys
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../games/school/index.html')
s=open(P,encoding='utf-8').read()
def rep(old,new,n=1):
    global s
    c=s.count(old)
    if c!=n: print('次數不對（預期 %d，實際 %d）：%s'%(n,c,old[:70])); sys.exit(1)
    s=s.replace(old,new)
def line(prefix,fn):
    """依行首找唯一一行，fn(縮排, 原行) 回傳新行（None＝刪掉整行）"""
    global s
    ls=s.split('\n'); idx=[i for i,l in enumerate(ls) if l.strip().startswith(prefix)]
    if len(idx)!=1: print('行數不對',prefix,len(idx)); sys.exit(1)
    i=idx[0]; ind=ls[i][:len(ls[i])-len(ls[i].lstrip())]
    r=fn(ind,ls[i])
    if r is None: del ls[i]
    else: ls[i]=r
    s='\n'.join(ls)
# 003 開頭介紹
rep("你今天（或明天、後天）不能去上課。你要用 LINE","你好像有一天沒辦法去上課。你要用 LINE")
rep("Hoy (o mañana, o pasado mañana) no puedes ir a clase.","Parece que un día no puedes ir a clase.",2)
rep("You can't go to class today (or tomorrow, or the day after).","It looks like there's a day you can't go to class.")
# 說話的人：我
rep("    const xm = (zh, es, en) => L(`小美：${zh}`, es, en);","    const xm = (zh, es, en) => L(`小美：${zh}`, es, en);\n    const me = (zh, es, en) => L(`我：${zh}`, es, en);")
# 021
line("dialogue: () => [L('（你打開跟老師的 LINE 聊天室。",lambda i,l:i+"dialogue: () => [me('第一句要怎麼說呢？', '¿Cómo empiezas el mensaje?', 'How do you start the message?')],")
rep(", ['聊天室', 'chat', 'chat room']","")
# 036
rep("M(`你要請的是「${lv.time}」的假。`, `Tienes que pedir permiso para: ${lv.timeEs}.`, `The time you need is: ${lv.timeEn}.`)",
    "M(`不對吧！你是要請「${lv.time}」的假。`, `¡No es eso! Lo que quieres pedir es permiso para: ${lv.timeEs}.`, `That's not right! You need to ask for leave for: ${lv.timeEn}.`)")
# 042 / 043
rep("M('老師同意了，要說「謝謝老師」，這樣比較有禮貌。', 'La profesora aceptó: hay que decir «謝謝老師» (gracias), es más cortés.', 'The teacher agreed, so say 謝謝老師 (thank you) — it\\'s more polite.')",
    "M('要當個有禮貌的學生！要說「謝謝老師」！', '¡Hay que ser cortés! ¡Debes decir «謝謝老師» (gracias, profesora)!', 'Be a polite student! Say 謝謝老師 (thank you, teacher)!')")
rep("M('請假單是學校的規定，用 LINE 請假以後，回學校還是要補交。', 'El formulario es una regla de la escuela: aunque pidas permiso por LINE, igual hay que entregarlo al volver.', \"The leave form is a school rule: even if you ask by LINE, you still hand it in when you're back.\")",
    "M('請假單是學校的規定，我們都要遵守規定！', 'El formulario es una regla de la escuela: ¡todos tenemos que cumplir las reglas!', 'The leave form is a school rule — we all have to follow the rules!')")
# 045
rep("L('（你傳出去了。第二天，你回到學校。）', '(Envías el mensaje. Al día siguiente, vuelves a la escuela.)', '(You send it. The next day, you go back to school.)')",
    "L('（你把訊息傳出去了。）', '(Envías el mensaje.)', '(You send the message.)')")
rep("dialogue: () => [tch(`早安，${N}！`","dialogue: () => [L('（第二天，你回到學校。）', '(Al día siguiente, vuelves a la escuela.)', '(The next day, you go back to school.)'), tch(`早安，${N}！`")
# 049
rep("M('老師關心你，要有禮貌地回答，還要說「謝謝老師關心」。', 'La profesora se preocupa por ti: responde con cortesía y di «謝謝老師關心» (gracias por preguntar).', 'The teacher is showing concern: answer politely and say 謝謝老師關心 (thanks for asking).')",
    "M('不要忽略了老師的關心，要有禮貌。', 'No ignores la preocupación de la profesora: responde con cortesía.', \"Don't ignore the teacher's concern — be polite.\")")
# 052 刪、054 改
line("L('（你坐下來，旁邊是同學小美。）'",lambda i,l:None)
rep("L(`（你想到，${lv.note}你還沒有。）`, `(Te acuerdas de que todavía no tienes ${lv.noteEs}.)`, `(You realize you don't have ${lv.noteEn} yet.)`)",
    "L(`（你突然想到你沒有${lv.note}。）`, `(De pronto recuerdas que no tienes ${lv.noteEs}.)`, `(You suddenly realize you don't have ${lv.noteEn}.)`)")
# 058 / 059
rep("M('不能請同學幫你寫功課；你可以請同學把筆記借你拍照。', 'No se le pide a un compañero que te haga la tarea; puedes pedirle que te preste los apuntes para fotografiarlos.', \"Don't ask a classmate to do your homework; ask to borrow their notes and take a photo.\")",
    "M('不能請同學幫你寫功課，自己寫！', 'No le pidas a un compañero que te haga la tarea: ¡hazla tú!', \"Don't ask a classmate to do your homework — do it yourself!\")")
rep("M('「筆記給我」太直接了，要說「不好意思，可以請你……嗎？」。', '«筆記給我» («dame los apuntes») es demasiado directo; di «不好意思，可以請你……嗎？».', '\"Give me the notes\" is too blunt; say 不好意思，可以請你……嗎？ (\"Excuse me, could you…?\").')",
    "M('你說得太直接了啦！有禮貌一點！', '¡Eso suena demasiado directo! ¡Sé más cortés!', 'That was too blunt! Be more polite!')")
# 062
line("dialogue: () => [L('（下課了。你拿到一張請假單",lambda i,l:i+"dialogue: () => [me('要填哪一種假別？', '¿Qué «tipo de licencia» debo llenar?', 'Which type of leave should I fill in?')],")
# 068 刪
line("L('（你把請假單填好，走到辦公室。）'",lambda i,l:None)
# 073
rep("M('你要交的是請假單，不是作業。', 'Lo que tienes que entregar es el formulario de ausencia, no la tarea.', \"What you're handing in is the leave form, not homework.\")",
    "M('你要交的是請假單，不是作業唷！', '¡Lo que tienes que entregar es el formulario de ausencia, no la tarea!', \"What you're handing in is the leave form, not homework!\")")
# 076 刪、077/078
line("L('（老師收下請假單，說：",lambda i,l:None)
line("? xm(`哇，${N}，你已經會用中文請假了！",lambda i,l:i+"? me('哇，我已經會用中文請假了！', '¡Vaya, ya sé pedir permiso en chino!', 'Wow, I can already ask for leave in Chinese!')")
line(": xm('辛苦了！請假的事情很麻煩吧！",lambda i,l:i+": me('唉，用中文請假還是有點麻煩。', 'Uf, pedir permiso en chino sigue siendo un poco complicado.', 'Ugh, asking for leave in Chinese is still a bit of a hassle.')")
rep("END: [['收到', 'recibir', 'receive'], ['午餐', 'almuerzo', 'lunch'], ['辛苦了', 'gracias por el esfuerzo', 'thanks for your effort']]",
    "END: [['請假', 'pedir permiso (para faltar)', 'ask for leave'], ['已經', 'ya', 'already'], ['麻煩', 'complicado, molesto', 'troublesome']]")
open(P,'w',encoding='utf-8').write(s)
print('OK')
