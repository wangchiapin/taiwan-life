/* ══════════════════════════════════════
   Firebase（tiendadebebidas-d75ac）：設定只放這裡，所有遊戲、地圖、清單頁、管理員頁共用
   ── 集合 ──
   <scene>game_scores / nightmarket_scores  舊排行榜（name, score, elapsed, createdAt）不要改名
   results                                   每局一筆完整紀錄（只有管理員能讀）
   progress/<玩家代碼>                        玩家名字＋地圖進度（換裝置時用代碼讀回）
   規則在 tools/firestore.rules
══════════════════════════════════════ */
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getFirestore, collection, doc, addDoc, setDoc, getDoc, getDocs, deleteDoc,
  query, where, orderBy, limit, writeBatch
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

export const firebaseConfig = {
  apiKey:            "AIzaSyD2lxec6JTbERwFPGjDzriYzIH7o9IRWnw",
  authDomain:        "tiendadebebidas-d75ac.firebaseapp.com",
  projectId:         "tiendadebebidas-d75ac",
  storageBucket:     "tiendadebebidas-d75ac.firebasestorage.app",
  messagingSenderId: "947444542062",
  appId:             "1:947444542062:web:62e209f33cfc3ae12c547f",
  measurementId:     "G-PGQZPYNBLX"
};
export const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);

/* 場景 → 舊排行榜集合（沿用各遊戲原本的名稱） */
export const SCORE_COLS = {
  drinks: 'drinkgame_scores', reserva: 'reservagame_scores', breakfast: 'breakfastgame_scores',
  parcel: 'parcelgame_scores', nightmarket: 'nightmarket_scores', bakery: 'bakerygame_scores',
  clinic: 'clinicgame_scores', mrt: 'mrtgame_scores', street: 'streetgame_scores'
};

/* 管理員頁要用的 Firestore 函式 */
export { collection, doc, addDoc, setDoc, getDoc, getDocs, deleteDoc, query, where, orderBy, limit, writeBatch };

/* 遊戲、地圖、清單頁用：window._FB
   scoresCol：這個遊戲的排行榜集合（地圖和清單頁不用給） */
export function initFB({ scoresCol } = {}) {
  window._FB = {
    async saveScore(name, score, elapsed) {
      try { await addDoc(collection(db, scoresCol), { name, score, elapsed, createdAt: Date.now() }); return true; }
      catch (e) { console.error("Firebase 寫入失敗", e); return false; }
    },
    async getLeaderboard() {
      try {
        // 需要複合索引：score 降冪 + elapsed 升冪（管理員頁可以檢查、一鍵建立）
        const q = query(collection(db, scoresCol), orderBy("score", "desc"), orderBy("elapsed", "asc"), limit(15));
        const snap = await getDocs(q);
        return snap.docs.map(d => d.data());
      } catch (e) { console.error("Firebase 讀取失敗", e); return []; }
    },
    /* 每局完整紀錄 */
    async saveResult(rec) {
      try { await addDoc(collection(db, 'results'), rec); return true; }
      catch (e) { console.error("成績紀錄上傳失敗", e); return false; }
    },
    /* 玩家資料＋地圖進度：progress/<代碼> */
    async getProgress(code) {
      try { const s = await getDoc(doc(db, 'progress', code)); return s.exists() ? s.data() : null; }
      catch (e) { console.error("讀取進度失敗", e); throw e; }
    },
    /* 有 done（地圖進度）就整筆蓋過去（清除進度才會真的清掉）；只有名字就合併，不動到進度 */
    async saveProgress(code, data) {
      try { await setDoc(doc(db, 'progress', code), { ...data, code, updatedAt: Date.now() }, { merge: !('done' in data) }); return true; }
      catch (e) { console.error("進度上傳失敗", e); return false; }
    }
  };
  window.dispatchEvent(new Event('fb-ready'));
}
