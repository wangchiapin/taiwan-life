/* ══════════════════════════════════════
   台灣情境對話遊戲：所有遊戲共用的程式
   每個遊戲在載入這個檔案前，先寫好 GAME 設定：
     const GAME = {
       scene: 'drinks',              // 資料夾名＝成績紀錄、地圖用的場景 ID
       track: 'drink',               // GA4 事件的 game 參數（沿用舊名稱，報表才接得起來）
       settingsKey: 'drink_settings',// localStorage：這個遊戲的繁簡／西英設定
       timerPrefix: '⏱ ',            // 計時器前面的字（可省略，預設 '⏱ '）
       roles: { 'Ami': { pitch: 1.15 }, … }   // 朗讀角色的音高；male: true 有男聲就用男聲
     };
   遊戲物件用 defineGame({ … }) 建立：會帶入下面 GameCore 的共用功能，遊戲自己寫的同名功能會蓋過共用版。
   遊戲最後呼叫 GameBoot()（從「重新開始」或清單頁回來時直接開始）。
   遊戲自己要寫的：customPinyin、WHO／SPEAKER_RE、VOCAB／VOCAB_OF、Hints、STAGE、NEXT_LABEL、Game（getConfig、render…）、Music.init
   可選的掛勾：Game.onStart()（按開始後、換到遊戲畫面前）、GAME.restartParams(p)（重新開始時多帶的網址參數）
══════════════════════════════════════ */

/* ══════════════════════════════════════
   拼音：台灣讀音（各遊戲自己用 pinyinPro.customPinyin 補讀錯的詞）
══════════════════════════════════════ */
const PY_OPT = { toneType: 'symbol', toneSandhi: true };
const isDigits = seg => /^[零一二三四五六七八九]+$/.test(seg);   // 念號碼：一不變調
function toPinyin(seg, asArray) {
  return pinyinPro.pinyin(seg, { ...PY_OPT, toneSandhi: !isDigits(seg), type: asArray ? 'array' : 'string' });
}

/* ══════════════════════════════════════
   小工具
══════════════════════════════════════ */
const CN = ['零','一','二','三','四','五','六','七','八','九','十'];
const L = (zh, es, en) => ({ zh, es, en });                 // 一行台詞＋翻譯
const M = (zh, es, en) => ({ zh, es, en });                 // 扣分原因
const pick = arr => arr[Math.floor(Math.random() * arr.length)];
const shuffle = arr => { const a = [...arr]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function track(name, params) { try { gtag('event', name, params || {}); } catch (e) {} }

/* ══════════════════════════════════════
   網址參數：嵌入模式（給「台灣一週」地圖用）
   ?embed=1&name=玩家名字（&s=simp&l=en）
══════════════════════════════════════ */
const QS = new URLSearchParams(location.search);
const EMBED = QS.get('embed') === '1';
if (EMBED && QS.get('name')) document.body.classList.add('embed-boot');

/* ══════════════════════════════════════
   設定：中文字體（繁／簡）、說明語言（西／英）
   遊戲內部一律用繁體判斷答案，只在顯示時轉成簡體；拼音一律用台灣讀音（由繁體算出）
══════════════════════════════════════ */
const Settings = { script: 'trad', lang: 'es' };
try {
  const saved = JSON.parse(localStorage.getItem(GAME.settingsKey) || '{}');
  if (saved.script === 'simp') Settings.script = 'simp';
  if (saved.lang === 'en') Settings.lang = 'en';
} catch (e) {}
(() => {   // 從「重新開始」回來時，沿用這一局的設定
  const q = new URLSearchParams(location.search);
  if (q.get('s') === 'simp' || q.get('s') === 'trad') Settings.script = q.get('s');
  if (q.get('l') === 'es' || q.get('l') === 'en') Settings.lang = q.get('l');
})();
const X = (es, en) => Settings.lang === 'en' ? en : es;     // 依語言選西文或英文
let _t2s = null;                                            // 繁→簡轉換器（選簡體時才載入）
const Z = s => (Settings.script === 'simp' && _t2s) ? _t2s(String(s)) : String(s);
function loadT2S() {
  if (_t2s) return Promise.resolve();
  return new Promise(res => {
    const sc = document.createElement('script');
    sc.src = 'https://cdn.jsdelivr.net/npm/opencc-js@1.4.2/dist/umd/t2cn.js';
    sc.onload = () => { try { _t2s = OpenCC.Converter({ from: 'tw', to: 'cn' }); } catch (e) {} res(); };
    sc.onerror = () => res();
    document.head.appendChild(sc);
  });
}
/* 登入畫面以外的文字，一出現就轉成簡體（逐行轉換，保留詞的上下文） */
function convertNode(root) {
  if (Settings.script !== 'simp' || !_t2s) return;
  const walk = n => {
    if (n.nodeType === 3) {
      if (!/[一-鿿]/.test(n.nodeValue)) return;
      const el = n.parentElement;
      if (!el || el.closest('#login-screen, script, style, rt')) return;
      const v = _t2s(n.nodeValue);
      if (v !== n.nodeValue) n.nodeValue = v;
    } else if (n.nodeType === 1) n.childNodes.forEach(walk);
  };
  walk(root);
}
const simpObserver = new MutationObserver(muts => {
  muts.forEach(m => {
    if (m.type === 'characterData') convertNode(m.target);
    else m.addedNodes.forEach(convertNode);
  });
});
function applyLang() {
  document.querySelectorAll('[data-es]').forEach(el => {
    el.textContent = (el.dataset.zh ? el.dataset.zh + ' ' : '') + el.dataset[Settings.lang];
  });
  document.documentElement.lang = Settings.script === 'simp' ? 'zh-Hans' : 'zh-Hant';
  document.querySelectorAll('[data-script]').forEach(b => b.setAttribute('aria-pressed', b.dataset.script === Settings.script));
  document.querySelectorAll('[data-lang]').forEach(b => b.setAttribute('aria-pressed', b.dataset.lang === Settings.lang));
  convertLogin();
}
/* 開始畫面：選了简体就馬上轉換，按回繁體就換回原文（「繁體｜简体」按鈕本身不轉） */
const _loginOrig = new WeakMap();
function convertLogin() {
  const walk = n => {
    if (n.nodeType === 3) {
      if (!_loginOrig.has(n)) { if (!/[一-鿿]/.test(n.nodeValue)) return; _loginOrig.set(n, n.nodeValue); }
      const o = _loginOrig.get(n);
      const v = (Settings.script === 'simp' && _t2s) ? _t2s(o) : o;
      if (v !== n.nodeValue) n.nodeValue = v;
    } else if (n.nodeType === 1 && !n.hasAttribute('data-script')) n.childNodes.forEach(walk);
  };
  walk(document.getElementById('login-screen'));
  const inp = document.getElementById('player-name-input');
  if (!inp.dataset.ph) inp.dataset.ph = inp.placeholder;
  inp.placeholder = (Settings.script === 'simp' && _t2s) ? _t2s(inp.dataset.ph) : inp.dataset.ph;
}
function saveSettings() { try { localStorage.setItem(GAME.settingsKey, JSON.stringify(Settings)); } catch (e) {} }
/* ══════════════════════════════════════
   翻譯小視窗：可拖曳、可關閉，選了選項就全部關掉
══════════════════════════════════════ */
const Tr = {
  z: 30,
  open(item, btn) {
    const pop = document.createElement('div');
    pop.className = 'tr-pop';
    pop.setAttribute('role', 'dialog');
    const m = item.zh.match(SPEAKER_RE);
    const who = m ? (m[1] === '我' ? [Game.N, Game.N] : WHO[m[1]]) : null;
    const li = Settings.lang === 'en' ? 1 : 0;
    pop.innerHTML = `<div class="tr-head"><span>翻譯 · ${X('Traducción', 'Translation')}</span><button class="tr-close" aria-label="關閉 Cerrar">✕</button></div>
      <div class="tr-body">
        <div class="tr-row"><span class="tr-lang">${li ? 'EN' : 'ES'}</span><span>${who ? `<b>${esc(who[li])}:</b> ` : ''}${esc(li ? item.en : item.es)}</span></div>
      </div>`;
    document.body.appendChild(pop);
    const r = btn.getBoundingClientRect(), w = pop.offsetWidth, h = pop.offsetHeight;
    let x = Math.min(Math.max(8, r.right - w), innerWidth - w - 8);
    let y = r.bottom + 8 + h > innerHeight ? r.top - h - 8 : r.bottom + 8;
    pop.style.left = x + 'px'; pop.style.top = Math.max(8, y) + 'px';
    pop.style.zIndex = ++Tr.z;
    pop.querySelector('.tr-close').onclick = () => pop.remove();
    pop.addEventListener('pointerdown', () => { pop.style.zIndex = ++Tr.z; });
    // 拖曳：抓標題列移動
    const head = pop.querySelector('.tr-head');
    head.addEventListener('pointerdown', e => {
      if (e.target.closest('.tr-close')) return;
      const sx = e.clientX - pop.offsetLeft, sy = e.clientY - pop.offsetTop;
      head.setPointerCapture(e.pointerId);
      const move = ev => {
        pop.style.left = Math.min(Math.max(0, ev.clientX - sx), innerWidth - 60) + 'px';
        pop.style.top = Math.min(Math.max(0, ev.clientY - sy), innerHeight - 40) + 'px';
      };
      const up = () => { head.removeEventListener('pointermove', move); head.removeEventListener('pointerup', up); };
      head.addEventListener('pointermove', move); head.addEventListener('pointerup', up);
    });
  },
  closeAll() { document.querySelectorAll('.tr-pop').forEach(p => p.remove()); }
};
const SPK_ICON = '<svg viewBox="0 0 20 20" width="14" height="14" aria-hidden="true"><path d="M3 7.5h3l4-3.5v12l-4-3.5H3z" fill="currentColor"/><path d="M13 7a4 4 0 0 1 0 6M15.5 4.5a7.5 7.5 0 0 1 0 11" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>';
const TR_ICON = '<svg viewBox="0 0 20 20" width="14" height="14" aria-hidden="true"><circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M2 10h16M10 2c-2.6 2.4-2.6 13.6 0 16M10 2c2.6 2.4 2.6 13.6 0 16" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>';

/* ══════════════════════════════════════
   背景音樂：程式即時合成的 8-bit 小曲，不需要音檔
   🎵 按鈕開關（所有遊戲和地圖共用設定）；中文朗讀時自動變小聲；切到別的分頁就暫停
══════════════════════════════════════ */
const Music = {
  KEY: 'taiwan_music', VOL: 0.12,
  on: true, ctx: null, master: null, timer: null, step: 0, nextT: 0, song: null, ducked: false, events: null,
  init(song) {
    this.song = song;
    try { if (localStorage.getItem(this.KEY) === 'off') this.on = false; } catch (e) {}
    this.events = song.tracks.map(tr => this.parse(tr.notes));
    this.paint();
    const go = () => { if (this.on) this.start(); };
    addEventListener('pointerdown', go, { once: true }); addEventListener('keydown', go, { once: true });
    document.addEventListener('visibilitychange', () => { if (this.ctx) document.hidden ? this.ctx.suspend() : (this.on && this.timer && this.ctx.resume()); });
  },
  /* 一個字代表一個八分音符：C5、F#4、Bb3＝音；-＝延長；.＝休止；k s h＝大鼓、小鼓、鈸 */
  parse(str) {
    const tk = str.split(/\s+/).filter(x => x && x !== '|'), ev = [];
    const SEMI = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
    tk.forEach((x, i) => {
      if (x === '-' || x === '.') return;
      let len = 1; while (tk[i + len] === '-') len++;
      const m = x.match(/^([A-G])([#b]?)(\d)$/);
      ev[i] = m ? { midi: 12 * (+m[3] + 1) + SEMI[m[1]] + (m[2] === '#' ? 1 : m[2] === 'b' ? -1 : 0), len } : { drum: x, len };
    });
    ev.n = tk.length; return ev;
  },
  start() {
    if (!this.ctx) {
      const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return;
      this.ctx = new AC(); this.master = this.ctx.createGain(); this.master.gain.value = 0; this.master.connect(this.ctx.destination);
      const len = this.ctx.sampleRate * 0.3, buf = this.ctx.createBuffer(1, len, this.ctx.sampleRate), d = buf.getChannelData(0);
      for (let i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
      this.noise = buf;
    }
    this.ctx.resume();
    this.fade(this.ducked ? 0.15 : 1);
    if (!this.timer) { this.step = 0; this.nextT = this.ctx.currentTime + 0.1; this.timer = setInterval(() => this.tick(), 60); }
  },
  stop() { if (!this.ctx) return; this.fade(0); clearInterval(this.timer); this.timer = null; },
  toggle() {
    this.on = !this.on;
    try { localStorage.setItem(this.KEY, this.on ? 'on' : 'off'); } catch (e) {}
    this.on ? this.start() : this.stop(); this.paint();
  },
  duck(d) { this.ducked = d; if (this.ctx && this.on && this.timer) this.fade(d ? 0.15 : 1); },
  fade(x) { const g = this.master.gain, t = this.ctx.currentTime; g.cancelScheduledValues(t); g.setTargetAtTime(x * this.VOL, t, 0.12); },
  paint() {
    const b = document.getElementById('btn-music'); if (!b) return;
    b.textContent = this.on ? '🎵' : '🔇';
    b.title = this.on ? '關掉音樂 · Silenciar música' : '打開音樂 · Activar música'; b.setAttribute('aria-label', b.title);
  },
  tick() {
    const s = this.song, d = 60 / s.bpm / 2;
    while (this.nextT < this.ctx.currentTime + 0.3) {
      s.tracks.forEach((tr, k) => { const ev = this.events[k], e = ev[this.step % ev.n]; if (e) this.play(tr, e, this.nextT, d); });
      this.nextT += d; this.step++;
    }
  },
  play(tr, e, t, d) {
    const c = this.ctx, g = c.createGain(); g.connect(this.master);
    const v = tr.vol ?? 0.5;
    if (e.drum) {
      if (e.drum === 'k') {
        const o = c.createOscillator(); o.frequency.setValueAtTime(140, t); o.frequency.exponentialRampToValueAtTime(40, t + 0.12);
        g.gain.setValueAtTime(v * 1.4, t); g.gain.exponentialRampToValueAtTime(0.001, t + 0.15); o.connect(g); o.start(t); o.stop(t + 0.16);
      } else {
        const n = c.createBufferSource(), f = c.createBiquadFilter(); n.buffer = this.noise;
        f.type = 'highpass'; f.frequency.value = e.drum === 'h' ? 7000 : 1800;
        const dur = e.drum === 'h' ? 0.04 : 0.1;
        g.gain.setValueAtTime(v * (e.drum === 'h' ? 0.35 : 0.7), t); g.gain.exponentialRampToValueAtTime(0.001, t + dur);
        n.connect(f); f.connect(g); n.start(t); n.stop(t + dur + 0.01);
      }
      return;
    }
    const o = c.createOscillator(), len = e.len * d * 0.92;
    o.type = tr.wave || 'square'; o.frequency.value = 440 * Math.pow(2, (e.midi - 69) / 12);
    g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(v, t + 0.01);
    g.gain.setValueAtTime(v * 0.7, t + Math.min(0.08, len * 0.5)); g.gain.exponentialRampToValueAtTime(0.001, t + len);
    o.connect(g); o.start(t); o.stop(t + len + 0.02);
  }
};

/* ══════════════════════════════════════
   朗讀：用裝置內建的中文語音（優先台灣國語 zh-TW），不用網路、不用錄音
══════════════════════════════════════ */
const Speech = {
  ok: 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window,
  voice: null,
  pickVoice() {
    const vs = speechSynthesis.getVoices();
    const zh = vs.filter(v => /^(zh|cmn)/i.test(v.lang));
    const mando = zh.filter(v => !/HK|yue/i.test(v.lang));
    const tw = mando.filter(v => /TW|Hant/i.test(v.lang));
    const pool = tw.length ? tw : mando;
    const isMale = v => /Zhiwei|Kangkang|Yunyang|Yunxi|Yunjian|Yunxia|Li-?mu|male|男/i.test(v.name) && !/female|女/i.test(v.name);
    this.voice = pool.find(v => !isMale(v)) || pool[0] || null;    // 主要聲音（女聲優先）
    this.male = pool.find(isMale) || null;                        // 裝置上有男聲才用
    this.hasList = vs.length > 0;
  },
  /* 角色的音高寫在各遊戲的 GAME.roles：女性角色用女聲調音高；male: true 的角色有男聲就用男聲，沒有就壓低音高 */
  get ROLE() { return GAME.roles || {}; },
  speak(text, btn, who) {
    if (!this.ok) return;
    this.stop();
    if (!this.voice) this.pickVoice();
    if (this.hasList && !this.voice) {
      Game.toast(Z('這台裝置沒有中文語音。') + ' ' + X('Este dispositivo no tiene voz en chino.', 'This device has no Chinese voice.'));
      return;
    }
    const u = new SpeechSynthesisUtterance(text.replace(/[（）()]/g, ''));
    const role = this.ROLE[who] || {};
    const useMale = role.male && this.male;
    const v = useMale ? this.male : this.voice;
    u.lang = v ? v.lang : 'zh-TW';
    if (v) u.voice = v;
    u.pitch = useMale ? role.malePitch : (role.pitch || 1);
    u.rate = 0.9;
    if (btn) { btn.classList.add('speaking'); this._btn = btn; }
    u.onend = u.onerror = () => { Music.duck(false); if (btn) btn.classList.remove('speaking'); };
    Music.duck(true);
    speechSynthesis.speak(u);
    track('tts', { game: GAME.track, state: Game.state });
  },
  stop() {
    if (!this.ok) return;
    speechSynthesis.cancel();
    if (this._btn) this._btn.classList.remove('speaking');
  }
};
if (Speech.ok) { Speech.pickVoice(); speechSynthesis.onvoiceschanged = () => Speech.pickVoice(); }
const spkBtn = (i, label) => Speech.ok ? `<button class="tr-btn spk" data-spk="${i}" aria-label="${label}">${SPK_ICON}</button>` : '';

/* ══════════════════════════════════════
   本關單字
══════════════════════════════════════ */
const Vocab = {
  open: false,
  toggle(force) {
    this.open = force ?? !this.open;
    if (this.open) { Hints.toggle(false); Log.toggle(false); }
    document.getElementById('vocab').classList.toggle('open', this.open);
    document.getElementById('vocab-tab').setAttribute('aria-expanded', this.open);
  },
  render(state) {
    const list = VOCAB[state] || [];
    document.getElementById('vocab-count').textContent = list.length;
    document.getElementById('vocab-tab').hidden = !list.length;
    document.getElementById('side-tabs').hidden = false;
    document.getElementById('vocab-list').innerHTML = list.map(([zh, es, en]) => {
      const py = toPinyin(zh, false);
      return `<li><div class="v-word"><span class="v-zh">${esc(Z(zh))}</span>${spkBtn(zh, '朗讀')}</div><div class="v-py">${esc(py)}</div>
        <div class="v-tr">${esc(X(es, en))}</div></li>`;
    }).join('');
    document.querySelectorAll('#vocab-list [data-spk]').forEach(btn => { btn.onclick = () => Speech.speak(btn.dataset.spk, btn); });
  }
};
document.getElementById('vocab-tab').onclick = () => Vocab.toggle();
document.getElementById('vocab-close').onclick = () => Vocab.toggle(false);
/* ══════════════════════════════════════
   錯誤紀錄：整局累積、即時更新、最新的在上面、標出關卡（關卡名稱 STAGE 寫在各遊戲）
══════════════════════════════════════ */
function stageOf() { const s = STAGE[Game.state]; return s ? [s[0], s[1], s[2]] : [Game.state, Game.state, Game.state]; }

const Log = {
  open: false,
  toggle(force) {
    this.open = force ?? !this.open;
    if (this.open) { Vocab.toggle(false); Hints.toggle(false); this.render(); }
    document.getElementById('log').classList.toggle('open', this.open);
    document.getElementById('log-tab').setAttribute('aria-expanded', this.open);
  },
  render() {
    const list = Game.log;
    document.getElementById('log-count').textContent = list.length;
    const body = document.getElementById('log-body');
    if (!list.length) { body.innerHTML = `<div class="l-empty">目前沒有錯誤，加油！<br>${X('¡Sin errores por ahora!', 'No mistakes so far!')}</div>`; return; }
    body.innerHTML = list.slice().reverse().map(m => {
      const st = m.stage || ['', '', ''];
      return `<div class="l-item${m.visit === Game.visit ? ' now' : ''}">
        <div class="l-stage">−10 · ${esc(st[0])}｜${esc(X(st[1], st[2]))}</div>
        <div class="l-es">${esc(X(m.es, m.en))}</div><div class="l-zh">${Game.ruby(m.zh)}</div></div>`;
    }).join('');
  }
};
document.getElementById('log-tab').onclick = () => Log.toggle();
document.getElementById('log-close').onclick = () => Log.toggle(false);

/* ══════════════════════════════════════
   登入
══════════════════════════════════════ */
function startGame() {
  const input = document.getElementById('player-name-input');
  const name = input.value.trim();
  if (!name) {
    document.getElementById('name-error').textContent = '請輸入你的名字 ' + X('Escribe tu nombre', 'Enter your name');
    input.focus(); return;
  }
  if (Settings.script === 'simp' && !_t2s) { loadT2S().then(() => { if (!_t2s) Settings.script = 'trad'; startGame(); }); return; }
  saveSettings(); applyLang();
  if (Settings.script === 'simp') { simpObserver.observe(document.body, { childList: true, subtree: true, characterData: true }); convertNode(document.body); }
  Game.playerName = name;
  Game.setup();
  document.getElementById('player-badge').textContent = '玩家：' + name;
  if (Game.onStart) Game.onStart();
  document.getElementById('login-screen').classList.remove('active');
  document.getElementById('game-window').classList.add('active');
  track('game_start', { game: GAME.track, script: Settings.script, lang: Settings.lang, embed: EMBED ? 1 : 0 });
  Game.render();
}
document.getElementById('player-name-input').addEventListener('keydown', e => { if (e.key === 'Enter') startGame(); });
document.querySelectorAll('[data-script]').forEach(b => b.onclick = () => {
  Settings.script = b.dataset.script; applyLang();
  if (Settings.script === 'simp' && !_t2s) loadT2S().then(applyLang);
});
document.querySelectorAll('[data-lang]').forEach(b => b.onclick = () => { Settings.lang = b.dataset.lang; applyLang(); });
applyLang();
if (Settings.script === 'simp' && !_t2s) loadT2S().then(applyLang);   // 上次選了简体：開始畫面也先轉好

/* 重新開始：保留名字和語言設定，整局重來（重新出題、分數與時間歸零）；中途放棄的不寫入排行榜 */
function restartGame(skipConfirm) {
  if (!skipConfirm && !confirm(Z('確定要重新開始嗎？這一局的分數不會保留。') + '\n' + X('¿Seguro que quieres empezar de nuevo? Perderás el puntaje de esta partida.', 'Start over? Your score for this round will be lost.'))) return;
  track('game_restart', { game: GAME.track, state: Game.state });
  const p = new URLSearchParams();
  if (EMBED) { p.set('embed', '1'); p.set('name', Game.playerName); if (QS.get('code')) p.set('code', QS.get('code')); }
  else p.set('again', Game.playerName);
  p.set('s', Settings.script); p.set('l', Settings.lang);
  if (GAME.restartParams) GAME.restartParams(p);
  location.replace(location.pathname + '?' + p.toString());
}

/* 嵌入模式：玩完把成績交給地圖，由地圖關掉這一關 */
function finishEmbed() {
  Tr.closeAll(); Speech.stop();
  try { parent.postMessage({ type: 'scene-complete', scene: GAME.scene, score: Game.score, mistakes: Game.mistakes }, '*'); } catch (e) {}
}

/* 每局完整紀錄：結果頁出現時上傳到 results（管理員成績頁看得到）；一局只傳一次 */
function uploadResult() {
  if (Game._sent) return; Game._sent = true;
  try {
    TWResults.send({ scene: GAME.scene, name: Game.playerName, code: QS.get('code'), score: Game.score, mistakes: Game.mistakes,
      log: Game.log, elapsed: Game.elapsedTime, hintViews: Game.hintViews, script: Settings.script, lang: Settings.lang, embed: EMBED });
  } catch (e) { console.error('成績紀錄上傳失敗', e); }
}

/* ══════════════════════════════════════
   排行榜
══════════════════════════════════════ */
async function showLeaderboard() {
  // 地圖模式：看完排名，按鈕改成「回到地圖」（成績交給地圖、地圖關掉這一關）
  if (EMBED) {
    const back = document.querySelector('#leaderboard-screen .btn-restart');
    if (back) { back.dataset.zh = '回到地圖'; back.dataset.es = 'Volver al mapa'; back.dataset.en = 'Back to the map'; back.textContent = '回到地圖 ' + X('Volver al mapa', 'Back to the map'); back.onclick = finishEmbed; }
    // 先告訴地圖成績（學生直接按地圖右上角「✕ Salir」離開，也算完成）
    try { parent.postMessage({ type: 'scene-result', scene: GAME.scene, score: Game.score, mistakes: Game.mistakes }, '*'); } catch (e) {}
  }
  Tr.closeAll(); Speech.stop(); Vocab.toggle(false); Hints.toggle(false); Log.toggle(false);
  document.getElementById('side-tabs').hidden = true;
  document.getElementById('game-window').classList.remove('active');
  document.getElementById('leaderboard-screen').classList.add('active');
  const myName = Game.playerName, myScore = Game.score, myElapsed = Game.elapsedTime;

  if (window._FB) await window._FB.saveScore(myName, myScore, myElapsed);
  const rows = window._FB ? await window._FB.getLeaderboard() : [];

  document.getElementById('lb-loading').style.display = 'none';
  document.getElementById('lb-table').style.display = 'table';
  const medals = ['🥇','🥈','🥉'];
  const myRank = rows.findIndex(r => r.name === myName && r.score === myScore && r.elapsed === myElapsed) + 1;

  document.getElementById('rank-banner').innerHTML = myRank
    ? `<div class="congrats-banner">${medals[myRank - 1] || '🎉'} 恭喜 ${esc(myName)}！你是第 ${myRank} 名！<br><small>${X(`¡Felicidades! Quedaste en el puesto #${myRank}`, `Congratulations! You're #${myRank}`)}</small></div>`
    : `<div class="no-rank-banner">可惜，${esc(myName)}，這次沒進前 15 名，再試一次吧！<br><small>${X('No entraste al top 15. ¡Inténtalo otra vez!', "You didn't make the top 15. Try again!")}</small></div>`;

  const body = document.getElementById('lb-body');
  body.innerHTML = rows.length ? '' : `<tr><td colspan="4">還沒有紀錄 ${X('Sin registros', 'No records yet')}</td></tr>`;
  rows.forEach((r, i) => {
    const tr = document.createElement('tr');
    if (i + 1 === myRank) tr.classList.add('highlight-row');
    tr.innerHTML = `<td>${medals[i] || '#' + (i + 1)}</td><td>${esc(String(r.name))}</td><td>${r.score} 分</td><td>${r.elapsed} 秒</td>`;
    body.appendChild(tr);
  });
}

/* ══════════════════════════════════════
   遊戲物件的共用功能（計時、扣分、回饋卡、拼音、圖片、過場）
   用 defineGame({ … }) 建立遊戲物件；遊戲自己寫的同名功能會蓋過這裡
══════════════════════════════════════ */
const GameCore = {
  get N() { return this.playerName; },
  startTimer() {
    this.startTime = Date.now();
    this.timerInterval = setInterval(() => {
      this.elapsedTime = Math.floor((Date.now() - this.startTime) / 1000);
      const m = Math.floor(this.elapsedTime / 60), s = String(this.elapsedTime % 60).padStart(2, '0');
      document.getElementById('timer-display').textContent = `${GAME.timerPrefix ?? '⏱ '}${m}:${s}`;
    }, 1000);
  },
  stopTimer() { clearInterval(this.timerInterval); },
  addMistake(r, thought) {
    this.score -= 10; this.mistakes += 1; this.mistakeLog.push(r.zh + ' ' + r.es);
    this.log.push({ ...r, stage: stageOf(), visit: this.visit });
    if (this.state !== 'END') this.feedback.push({ type: 'bad', ...r });
    document.getElementById('score-badge').textContent = this.score + ' 分';
    track('mistake', { game: GAME.track, state: this.state });
    if (thought) this.thought = thought;
    Log.render();
    if (this.mistakes >= 10 && this.state !== 'END') {
      setTimeout(() => { alert(Z('錯太多次了，從頭再來一次！') + ' ' + X('Demasiados errores. ¡Empieza otra vez!', 'Too many mistakes. Start over!')); restartGame(true); }, 300);
    }
  },
  good(zh, es, en) { this.feedback.push({ type: 'good', zh, es, en }); },
  feedbackHTML() {
    return this.feedback.map(f => `<div class="fb ${f.type}">
      <div class="fb-head">${f.type === 'bad' ? '✗ −10 分' : '✓ ' + X('¡Bien!', 'Nice!') + ' 做得好'}</div>
      <div class="fb-es">${esc(X(f.es, f.en))}</div><div class="fb-zh">${this.ruby(f.zh)}</div></div>`).join('');
  },
  toast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg; t.classList.add('show');
    clearTimeout(this._toastTimer);
    this._toastTimer = setTimeout(() => t.classList.remove('show'), 3600);
  },
  togglePinyin() {
    this.showPinyin = !this.showPinyin;
    document.getElementById('btn-pinyin').setAttribute('aria-pressed', this.showPinyin);
    this.render();
    if (Hints.open) Hints.render();
  },
  toggleList() {
    this.showList = !this.showList;
    document.getElementById('btn-list').setAttribute('aria-pressed', this.showList);
    this.render();
  },
  ruby(str) {
    if (!this.showPinyin) return esc(Z(str));
    return String(str).split(/([一-鿿]+)/).map(seg => {
      if (!/^[一-鿿]+$/.test(seg)) return esc(seg);
      const py = toPinyin(seg, true);                 // 台灣讀音由繁體算
      const shown = [...Z(seg)], orig = [...seg];
      const chars = shown.length === orig.length ? shown : orig;
      return chars.map((c, i) => `<ruby>${c}<rt>${py[i] || ''}</rt></ruby>`).join('');
    }).join('');
  },
  missing: new Set(),
  imageMissing() {
    const img = document.getElementById('npc-avatar'), ph = document.getElementById('scene-placeholder');
    const cur = img.getAttribute('src');
    if (cur) this.missing.add(cur);
    // 輪流圖的第二張不存在：回到第一張，不要跳成 emoji
    if (this._anim && cur === this._anim.alt) { this.stopAnim(); if (this._anim0 && !this.missing.has(this._anim0)) { img.setAttribute('src', this._anim0); return; } }
    img.style.display = 'none'; ph.style.display = 'grid';
  },
  stopAnim() { clearInterval(this._animTimer); this._anim = null; },
  closePanels() {
    for (const k of ['showList', 'showPhone']) if (this[k]) { this[k] = false; const b = document.getElementById(k === 'showList' ? 'btn-list' : 'btn-phone'); if (b) b.setAttribute('aria-pressed', 'false'); }
    Hints.toggle(false); Vocab.toggle(false); Log.toggle(false);
  },
  get st0() { return this.state === '_TRANS' && this._trans ? this._trans.to : this.state; },
  transLabel() {
    const t = this._trans, f = NEXT_LABEL[t.to];
    return (typeof f === 'function' ? f(t.from, this.task) : f) || NEXT_LABEL._default || '繼續';
  },
  maybeTrans(before, extra) {
    if (this.state === before && !extra) return;
    this.closePanels();
    if ((this.thought || this.feedback.length) && this.state !== 'RESULT') {
      this._trans = { from: before, to: this.state };
      this.state = '_TRANS';
    }
  }
};
/* 合併時保留 get（例如 get N()、get total()），不能用 {...} 展開 */
function defineGame(own) {
  const g = {};
  Object.defineProperties(g, Object.getOwnPropertyDescriptors(GameCore));
  Object.defineProperties(g, Object.getOwnPropertyDescriptors(own));
  return g;
}

/* 從「重新開始」或清單頁回來：直接用原本的名字開新的一局（遊戲最後呼叫） */
function GameBoot() {
  const again = EMBED ? QS.get('name') : QS.get('again');
  if (!again) return;
  if (!EMBED) history.replaceState(null, '', location.pathname);
  document.getElementById('player-name-input').value = again;
  startGame();
}
