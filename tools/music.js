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
    b.title = this.on ? '關掉音樂 · Silenciar música' : '打開音樂 · Activar música';
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
