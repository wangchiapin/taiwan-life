/* ══════════════════════════════════════
   玩家代碼＋成績上傳（所有遊戲、地圖、清單頁共用；一般 <script>，要在遊戲程式前面載入）
   ── 玩家代碼 ──
   第一次用某個名字玩時產生，例如 MAR-4821（名字的前三個英文字母＋4 位數；
   名字沒有英文字母，例如「小明」，前三碼就隨機給）。
   localStorage：taiwan_player = { name, script, lang, code }（清單頁、地圖共用）
                 taiwan_codes  = { 小寫名字: 代碼 }（同一台裝置上不同名字各有自己的代碼）
   換裝置：在清單頁或地圖輸入代碼 → 讀 progress/<代碼> 接回名字和地圖進度
══════════════════════════════════════ */
const TWPlayer = {
  KEY: 'taiwan_player', CODES: 'taiwan_codes',
  load() { try { return JSON.parse(localStorage.getItem(this.KEY) || '{}') || {}; } catch (e) { return {}; } },
  save(p) { try { localStorage.setItem(this.KEY, JSON.stringify(p)); } catch (e) {} },
  codes() { try { return JSON.parse(localStorage.getItem(this.CODES) || '{}') || {}; } catch (e) { return {}; } },
  saveCodes(c) { try { localStorage.setItem(this.CODES, JSON.stringify(c)); } catch (e) {} },
  key: name => String(name || '').trim().toLowerCase(),

  /* 名字 → 代碼前三碼 */
  makeCode(name) {
    const AZ = 'ABCDEFGHJKLMNPQRSTUVWXYZ';      // 隨機補的字母不用 I、O（容易和 1、0 搞混）
    let p = String(name || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toUpperCase().replace(/[^A-Z]/g, '').slice(0, 3);
    while (p.length < 3) p += AZ[Math.floor(Math.random() * AZ.length)];
    return p + '-' + String(Math.floor(Math.random() * 10000)).padStart(4, '0');
  },
  /* 使用者輸入的代碼 → 標準格式（大寫、補 -），不合格式回傳 '' */
  normCode(s) {
    const t = String(s || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
    return /^[A-Z]{3}[0-9]{4}$/.test(t) ? t.slice(0, 3) + '-' + t.slice(3) : '';
  },
  /* 這個名字的代碼（沒有就產生一個並登記到 Firebase）；given：網址帶來的代碼（地圖嵌入時） */
  codeFor(name, given) {
    const k = this.key(name); if (!k) return '';
    const codes = this.codes(), g = this.normCode(given);
    if (g) { if (codes[k] !== g) { codes[k] = g; this.saveCodes(codes); } return g; }
    if (codes[k]) return codes[k];
    const p = this.load();
    if (p.code && this.key(p.name) === k) { codes[k] = p.code; this.saveCodes(codes); return p.code; }
    const c = this.makeCode(name);
    codes[k] = c; this.saveCodes(codes);
    this.register(c, name);
    return c;
  },
  /* 記住「名字 ↔ 代碼」（換裝置讀回代碼時用） */
  remember(name, code) { const codes = this.codes(); codes[this.key(name)] = code; this.saveCodes(codes); },
  /* 新代碼登記到 progress/<代碼>；萬一和別人的代碼撞號，就換一個 */
  register(code, name, tries = 0) {
    TWFB.when(async fb => {
      let d = null;
      try { d = await fb.getProgress(code); } catch (e) { return; }
      if (d && this.key(d.name) !== this.key(name) && tries < 5) {
        const n = this.makeCode(name), codes = this.codes();
        codes[this.key(name)] = n; this.saveCodes(codes);
        const p = this.load(); if (p.code === code) { p.code = n; this.save(p); }
        return this.register(n, name, tries + 1);
      }
      if (!d) fb.saveProgress(code, { name: String(name).slice(0, 30) });
    });
  }
};

/* 等 Firebase（shared/firebase.js 是 module，會比較晚載入）準備好再做事；離線就算了 */
const TWFB = {
  when(fn) {
    if (window._FB) return fn(window._FB);
    window.addEventListener('fb-ready', () => fn(window._FB), { once: true });
  }
};

/* 每局完整紀錄 → results（只有管理員能讀） */
const TWResults = {
  send({ scene, name, code, score, mistakes, log, elapsed, hintViews, script, lang, embed }) {
    const rec = {
      playerId: TWPlayer.codeFor(name, code) || '',
      name: String(name || '').slice(0, 30),
      scene, score, mistakes,
      errors: (log || []).slice(0, 50).map(m => {
        const st = m.stage || [];
        return { zh: String(m.zh || ''), es: String(m.es || ''), en: String(m.en || ''),
                 stage: String(st[0] || ''), stageEs: String(st[1] || ''), stageEn: String(st[2] || '') };
      }),
      elapsed: elapsed || 0, hintViews: hintViews || 0,
      script, lang, embed: !!embed,
      difficulty: 'normal',          // 之後做難度設定時再改
      createdAt: Date.now()
    };
    TWFB.when(fb => fb.saveResult(rec));
    return rec;
  }
};
