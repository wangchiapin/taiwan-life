# 新增遊戲：設定與邏輯（給之後做新遊戲的 Claude 看）

> 2026-10-29 重新彙整。**這份是「做新遊戲該照什麼做」的唯一總檔**，其他文件只放細節，規則有衝突時以這份為準。
> 做之前先跟 Ben 確認劇情、圖片、流程；他說「推」才推（他說「做好直接推」就做完直接推）。

## 文件分工

| 檔案 | 放什麼 |
|---|---|
| **docs/new-game-guide.md（這份）** | 做新遊戲一定要照的規則：共用檔有什麼、自己要寫什麼、關卡設計、畫面、圖片、測試、登記、推之前 |
| **game-kit repo（wangchiapin/game-kit）** | 所有遊戲共同的標準：13 項新遊戲檢查表、讀音標準（GoodTeacher）、總字庫、共用零件原稿、Firebase 規則說明。**這裡沒有的內容在 game-kit，見第 12 節** |
| README.md | 專案結構、場景 ID 清單、成績與玩家代碼、嵌入模式、地圖開關、圖片規格、音樂、手機瀏覽器備註，以及每個遊戲各自的流程說明 |
| docs/icecream-logic-notes.md | 冰淇淋店的完整邏輯範例（多分支結局、店員放錯球、配料）；要做類似的複雜遊戲時參考 |
| docs/image-todo.md、docs/image-prompts-*.md | 要補的圖與做圖提示詞 |
| docs/revision-checklist.md | 台詞審查表（Ben 審稿用） |
| tools/HANDOFF.md | 歷史決定與當時的交接記錄（查「為什麼這樣做」才看） |

---

## 1. 先做什麼

1. 複製一個最新的遊戲當範本：`games/noodle`（有「對方出錯」和付錢找錢）；簡單一點的流程可以看 `games/mrt`、`games/street`。
2. 複製後**只改遊戲自己的部分**（見第 3 節）。共用檔已經有的功能（見第 2 節）不要留一份在遊戲裡；如果範本裡看到跟共用檔同名或同功能的東西，用共用的，把副本刪掉。
   - 重複定義會直接出錯：共用檔已經宣告的名字（例如 `zhNum`、`NZ`、`zhDigits`、`esM`），遊戲不能再用 `const` 宣告一次，整個遊戲會打不開。
3. 做新遊戲前，先看第 12 節「要對照 game-kit 的項目」。
4. 先把劇情流程寫給 Ben 看，確認後才寫程式。台詞和拼音第一版是草稿，Ben 會審。

## 2. 共用檔已經有的（不要自己寫）

`shared/game.js`、`shared/game.css`、`shared/player.js`、`shared/firebase.js`，改它們會影響全部遊戲。

- **功能**：設定（繁簡、西英、拼音）、翻譯小視窗、朗讀、單字抽屜（`Vocab`）、錯誤紀錄（`Log`）、提示面板、開始畫面、重新開始、嵌入模式、成績上傳（`uploadResult`）、排行榜、背景音樂（`Music`）。
- **遊戲物件的共用功能（`GameCore`）**：計時、扣分 `addMistake`、綠卡 `good`、回饋卡 `feedbackHTML`、圖片 `setImage`（支援備用 emoji 和輪流出現的第二張圖）、文字格式 `formatText`、過場 `maybeTrans`。遊戲自己寫同名的，會蓋過共用版；只有真的需要不同做法才蓋，並在遊戲檔裡註明原因。
- **小工具**：`L(中, 西, 英)`、`M(…)`（扣分原因）、`CN`（零到十）、`pick`、`shuffle`、`esc`、`money`、`esM`、`enM`。
- **念數字**（不要自己再寫）：
  - `zhNum(n)`：念一個數字，2 單獨念「二」，200 念「兩百」，20000 念「兩萬」，可以念到兆；金額、日期、時間、人數、號碼牌、樓層都用它。
  - `NZ(n)`：後面要接量詞時用，2 念「兩」（兩個、兩球、兩張），其他和 `zhNum` 一樣（十二片、兩萬個）。
  - `zhDigits(s)`：一個一個數字念（電話、號碼、西元年），其他字（`-`、`，`、空格）原樣保留。`zhDigits('02-4967-2308')` 念成「零二-四九六七-二三零八」，`zhDigits(2026)` 念成「二零二六」。0 念「零」、1 念「一」（不念「幺」）。要分組念（例如手機 4-3-3、中間停頓）就自己先切好，每一組各呼叫一次再用「，」接起來（barber 的電話就是這樣做）。
- **抓錯關卡與付錢三關（2026-10-30 已進共用檔，見第 5 節）**：`POLITE`、`rotOf(t, 選項)`、`catchState()`、`payStates()`、`stdShortBill`。遊戲不能再用 `const` 宣告這幾個名字，否則整個遊戲打不開。`billFor()`（你給的鈔票）金額每個遊戲不同，仍寫在遊戲裡。
- **共用樣式（`shared/game.css`，2026-10-30 又搬進 8 條）**：地點列的 `.clock`、`.icon`、`.who`，清單框裡的 `.done`、`.rule`、`.t .grow`，以及紅色成交按鈕 `.opt.deal`（含滑過去變色）。新遊戲不要再自己寫這幾條。地點列和清單框的底色、邊框、電話列顏色、按鈕上拼音的顏色，各遊戲有刻意的差異，仍寫在各遊戲裡。
- **付錢欄位與加總（2026-10-30 已進共用檔）**：`initPay(t, total, extras)`（算出真正總價、對方報價有沒有多算、鈔票、找零、找錯的錢；鈔票金額用遊戲自己的 `billFor()`）和 `sum(陣列)`。遊戲不能再用 `const`／`function` 宣告這兩個名字，否則整個遊戲打不開；遊戲自己要用不同做法的加總，請取別的名字（早餐店用 `sumPrice`）。關帝廟的鈔票固定是一千元，付錢欄位自己寫，不用 `initPay`。

## 3. 遊戲自己要寫的

每個遊戲的 `index.html` 只留這些（詳細載入順序見 README「共用程式」）：

- `GAME = { scene, track, settingsKey, roles }`：場景 ID、GA4 名稱、存設定的 localStorage 名稱、朗讀角色的音高（可選 `timerPrefix`、`restartParams(p)`）。
- `pinyinPro.customPinyin`（台灣讀音）、資料、`WHO`／`SPEAKER_RE`、`VOCAB`／`VOCAB_OF`、`Hints`、`STAGE`、`NEXT_LABEL`。
- `const Game = defineGame({ … })`：`setup`、`getConfig`、`render`、`handleChoice`、`setPlace`…；開始時要多做的事寫在 `onStart()`。
- 最後一行 `GameBoot();` 和 `Music.init({…})`。

## 4. 每個遊戲都要有的設定

- 場景 ID：資料夾名 = `scene` = 排行榜前綴。排行榜 collection 叫 `<scene>game_scores`，**不能改名**。
- 三種語言：台詞一律用 `L(中文, 西文, 英文)`。繁體／簡體、西文／英文由玩家設定決定。
- 拼音用台灣讀音，多音字照 GoodTeacher（共用檔已內建，見第 12 節）。GoodTeacher 沒有規則、又讀錯的詞，才加進該遊戲的 `customPinyin`。統一：「和」念 hàn、「嗯」念 ēn。
- 分數：100 分起，每個錯誤 −10。`Game.addMistake()` 扣分、`Game.good()` 出綠卡。
- 結局：錯誤 ≤ 2 次是好結局，否則壞結局（冰淇淋店另有更多條件）。結局後進結果頁，呼叫 `uploadResult()` 上傳成績。
- **好壞結局看「最後實際拿到的東西」是否符合 Ami 的訂單**，不是看過程中選了什麼。
- 星星（地圖用）：0 次錯誤 ★★★、1–5 次 ★★、6 次以上 ★。
- 背景音樂：**不能跟別的遊戲同一首**。

## 5. 關卡設計原則（Ben 10/27 決定，一定要照）

新遊戲不能只是「照 Ami 的話選就對」。每個遊戲至少要有：

1. **對方會隨機出錯**：報價、複誦、找錢、拿給你的東西、印出來的票，一部分機率是錯的（約 40–50%），玩家要自己核對。
2. **抓錯和沒錯都要做成正解**：對方說對時，「不對，我要的是…」是錯誤選項（要換成別的內容，不能跟對的一樣）；對方說錯時，「好，謝謝」才是錯誤選項。
3. **三個選項的固定寫法**：①沒錯／謝謝　②有禮貌地指出問題（含具體正確的數字或內容；對方其實沒錯時，數字是錯的）　③罵人或沒禮貌的說法（永遠是錯誤選項）。
4. **抓到錯誤之後要有後續**：對方道歉、補錢、重做、重印，不能一句話結束；必要時多一關確認。
5. **綠卡**：做對才出現，放在下一頁對話上方，不另外多一個過場頁。
6. **選了什麼先記下來，最後才判定**：玩家每一次實際選的東西都要記下來，選錯也照樣記，不擋住、不當場提示；錯誤在結局統一說明。例外：對方出錯的地方要在關卡中出現（讓玩家有機會抓）。
7. **選項文字依「玩家實際選的內容」產生**，不可以依 Ami 的正確答案產生。選項順序用 `rot()` 或 `shuffle()` 隨機排。
8. **價錢照實際做出來的算**：不要用 Ami 訂單的總價。對方報的價和實際應收的價要分開記（例如 `real()`／`said()`），付錢與找零的對話用它們。
9. **新增需要補的圖**，先記在 `docs/image-todo.md`，最後一起做。

共用寫法（在 `shared/game.js`，改它會影響麵店、超商、鹽酥雞、關帝廟、服飾店，改完要比對這五個遊戲）：
- `catchState()`：一關「①沒錯／謝謝 ②有禮貌指出 ③沒禮貌」，由 `wrong()` 決定這次對方有沒有出錯。
- `payStates()`：報價（PAY）、重算後付錢（PAY_FIX）、找錢（CHANGE）三關。付的鈔票由 `billFor()` 決定（一百、兩百、五百；服飾店、關帝廟的金額不同，各自改）。
  - 選用參數 `finish(G, t)`：付完錢／找完錢之後要做的事，預設是停表、進 END。服飾店用它換成「有改褲管就先等三十分鐘去拿褲子」。
  - 選用參數 `shortBill(n)`：給「一定不夠的那張鈔票」，預設 20～500 元（`stdShortBill`）。服飾店金額較大，自己帶一個。
  - 關帝廟只用 `catchState()`，付錢流程是自己寫的；它的「一定不夠的鈔票」直接用共用的 `stdShortBill(n)`。

複雜遊戲（多個出錯點、多種結局）的完整做法，看 `docs/icecream-logic-notes.md`。

## 6. 玩家角色與語氣

- 玩家是「主角」，名字由玩家輸入。西文對玩家說話不分男女（不用 listo／solo／bienvenido 這類有性別的字）。
- 畫面上主角看不出性別、看不到臉（手可以）。
- Ami 是固定的朋友，會用 LINE 交代任務（服飾店例外：沒有 Ami）。店員招呼用「¡Hola, buenas!」。
- 台詞要是台灣人真的會講的說法，流程要符合 2026 年台灣現場（悠遊卡、LINE Pay、發票、載具、叫號）。
- 中文價錢報「一百五十元」這種念法；數字一律用 `zhNum`／`NZ`（量詞前的 2 念「兩」）。

## 7. 畫面規則

- **任務提示**面板：只放畫面上沒有的資訊。固定有 Ami 的 LINE，和「我的狀況」（身上的錢、手上的東西）；NPC 的話只留答題需要的數字（價錢、路線、天數），客套話不放。
- **過場頁**順序：圖 → 綠色回饋卡 → 旁白 → 過場按鈕。旁白要對得上圖。按鈕文字寫在 `NEXT_LABEL`（key 是下一關的名字）。
- 不要放「📝 Mi situación」按鈕（內容已在任務提示裡）。
- 沒有圖時自動顯示 emoji，所以先寫程式、圖之後補都可以。
- 小字典 `VOCAB`：每個詞都必須在該關畫面或台詞裡真的出現，先 grep 確認；LINE 裡的詞歸在 START；同一關有兩種台詞（例如內用／外帶）時，兩種都要列。
- 手機：`<meta viewport>` 要有 `maximum-scale=1`，不要 `viewport-fit=cover`；`<html>` 加 `html{color-scheme:light}`。

## 8. 圖片

- 正方形 `.jpg`，**720×720**，品質約 84，檔名小寫，放 `games/<scene>/images/`。麵包店的物品小圖是 240。
- 常用檔名：`start`、`end_good`、`end_bad`、`result`，加每關自己的圖。對方出錯被抓到的尷尬表情用 `*_sorry.jpg` 或 `*_oops.jpg`（沒有就自動用原圖）。
- 做圖提示詞：一次一張，Ben 確認才做下一張；每個提示詞都要完整、可直接複製；寫清楚鏡頭方向、高度、角度；Ami 長相要跟飲料店的 Ami 一樣；場景要符合劇情真正發生的地點。

## 9. 測試

- 每個遊戲要有 `tools/oracles/<遊戲>.py`：依「對方有沒有出錯」給出正解。
- `python3 tools/smoke.py perfect <遊戲>` 照正解玩，多跑幾次（隨機）都要 100 分；另外跑 `mixed`、`embed`、`trans`（共四種）。
- 改共用檔時，用 `tools/compare_shots.py <遊戲> <舊檔>` 逐畫面比對改之前／改之後（用法和限制寫在檔案最上面）。改完要比對**所有用到的遊戲**，包含新遊戲。
- 測試要覆蓋：對方出錯、對方沒錯、玩家抓到、玩家沒抓到、付錯錢、順序錯。
- 每次測試確認：頁面沒有 pageerror；結局台詞與玩家實際選擇一致；價錢與實際內容一致。

## 10. 做完要登記的地方（新遊戲才有）

1. `index.html`：`SCENES` 加一筆（`gated: true`＝預設維修中、`slot`＝地圖位置），並補 `ZHS`（簡體名稱）、`SUGGEST`。
2. `shared/firebase.js`、`admin/index.html`（`SCENES`、`GATED`）、`music.html`、`tools/smoke.py`（遊戲名單）。
3. `tools/tiendadebebidas-d75ac.rules.txt`（`scoreCols`、`scenes`）。
4. 推上去之後 Ben 要做：把 `tools/tiendadebebidas-d75ac.rules.txt` 貼到 Firebase console 發布；管理員頁「設定檢查」建新排行榜的複合索引（score 降冪＋elapsed 升冪）；「地圖開關」打開遊戲。
5. 最後更新 README.md 的場景 ID 清單，和這個遊戲自己的那一段說明。

## 11. 推上去之前

- 先 `git pull --rebase origin main`（Ben 常直接在 GitHub 網頁上傳圖片，也可能有別的對話框同時在改）。
- 推之前確認沒有遊戲重複宣告共用檔的名字（例如 `grep -rn "const zhNum\|const NZ\|const zhDigits\|const POLITE\|const rotOf\|function catchState\|function payStates\|const sum \|function initPay" games`）。
- 改到 Firestore 的資料結構（collection、欄位、儲存方式）時，要提醒 Ben 更新 Apps Script 同步腳本。
- Ben 說「推」才推。

## 12. 要對照 game-kit 的項目

game-kit 是 Ben 所有遊戲共用的標準庫（私人 repo，要用 `add_repo` 加進來才讀得到）。taiwan-life 的共用檔已經內建設定、語音提示、靜音、版權說明、遊玩紀錄、排行榜前 10 名，這些**不用另外做**。下面幾項要**主動對照**：

1. **讀音**：標準是教育部國語辭典，**多音字以 GoodTeacher 規則為準**（`game-kit/bank/gt/` 的 readings.txt、rules.csv、classes.txt；比對工具 `bank/gt_compare.js`）。輕聲不標，「和」念 hàn。待處理的字詞清單在 `讀音與字詞待處理.md`。
   - **已經內建（2026-10-29，Ben 決定全部照 GoodTeacher）**：`shared/game.js` 的 `toPinyin` 會先用 pinyin-pro 算，再套 GoodTeacher「要改」的規則（多音字、一／不、輕聲、個…）。規則資料在 `GT-RULES-BEGIN／END` 之間，由 `tools/build_gt_rules.js` 產生，**不要手改**。
   - **GoodTeacher 更新規則之後**：把 game-kit 更新到最新，在 taiwan-life 跑 `node tools/build_gt_rules.js`，所有遊戲一起更新；再跑 smoke 四種模式，並把改前改後的拼音差異列給 Ben 看。
   - **新遊戲**：不用再為 GoodTeacher 已有規則的字補 `customPinyin`（例如排行榜、音樂、名字、對不起、算一算）。GoodTeacher 沒有規則、pinyin-pro 又讀錯的詞，才加進該遊戲的 `customPinyin`，並告訴 Ben。
   - 已知和日常口語不太一樣的地方（照 GoodTeacher 的結果）：「接個電話」念 gè（口語常是 ge）、「對不起、能不能」的「不」念 bù（口語常是輕聲）。如果 Ben 想例外，再加。
   - 聲調偵探是刻意用本調的例外，不是錯誤。
2. **分享連結預覽（檢查表第 13 項）**：每個遊戲 `<head>` 要有 `og:type`、`og:site_name`、`og:title`、`og:description`、`og:url`、`og:image`（含寬高）。**把遊戲連結交給 Ben 之前，先確認並告訴他：遊戲名稱（og:title）、縮圖（og.jpg）是什麼、存不存在、網址對不對。** 範例看 game-kit 檢查表提到的吃字小籠包。taiwan-life 目前只有首頁有，各遊戲頁還沒加（縮圖由 Ben 另一個對話框處理）。
3. **字詞一致性**：`game-kit/tests/word_consistency_check.js` 檢查跨遊戲同一個詞的寫法／讀音是否一致，但**目前不涵蓋台灣生存日記**。
   - **待辦（2026-10-29 Ben 決定先不做，先記著）**：要納入的是各遊戲的單字抽屜 `VOCAB`（劇本台詞不納入）。試算結果：1,333 筆、885 個詞，135 個詞出現在兩個以上遊戲，其中 106 處西文／英文寫法不同（例如內用 para comer aquí／ahí、吐司 pan de molde／pan tostado、不好意思 disculpe／disculpa；也有本來就該不同的，如「點」pedir／hora）。nightmarket、parcel、school 的 VOCAB 是動態產生，檢查程式要先改才讀得到。
   - 做法（建議，Ben 還沒確認）：先把 106 處分成「該統一／兩個意思／補充長短不同」三類，只讓 Ben 看第一類；統一以 game-kit 其他 6 個遊戲的寫法為標準；統一後再改 game-kit 的檢查程式，第二類寫進例外清單。
4. **共用零件有更新時**（`game-kit/parts/` 的 settings、voicehint、mute、copyright、plays）：taiwan-life 是把這些內嵌在 `shared/game.js` 裡（plays 可改寫 `HGPlays.gameFn`），game-kit 改了要回頭看這邊要不要跟著改。靜音那段目前文字和 game-kit 不完全一樣，尚未逐行確認。
5. **Firebase 規則**：taiwan-life 用 `tiendadebebidas-d75ac`，規則檔留在本 repo 的 `tools/tiendadebebidas-d75ac.rules.txt`，不要搬去 game-kit（見 `game-kit/firebase-rules/README.md`）。
6. **省額度方法**：`game-kit/省額度下指令方法.md`。
