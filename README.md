# 台灣生存日記 · Sobrevive en Taiwán（Survive in Taiwan）

> 2026-10-16 起的正式名稱（原「台灣生活地圖」）。飲料店、訂位、早餐店、診所、捷運、夜市、包裹、麵包店、街頭等情境對話遊戲

- **網址：** https://wangchiapin.github.io/taiwan-life/
- **Firebase 專案：** tiendadebebidas-d75ac
- **登入方式：** —（玩家輸入名字）
- **狀態：** 使用中
- **備註：** 排行榜集合為 `<場景>game_scores` 或 `<場景>_scores`，不要改名，否則舊排行榜會消失。

---

# 情境對話遊戲系列（Taiwan Week）

## 結構
```
index.html          首頁＝地圖（2026-10-16 起正式用地圖模式，原本的遊戲清單頁已刪除）：走到建築門口 → iframe 載入 games/<scene>/?embed=1 → 收 scene-complete
map/index.html      舊的地圖網址，自動轉到首頁
                    20×42 格（三條橫向馬路），畫面一次看幾列依螢幕高度自動算（手機約 30 列，電腦約 15 列），跟著玩家上下捲動；手機點地圖走路，沒有方向鍵。
                    星星：每個地點記最好的紀錄（最高分、最少錯誤分開記）；0 次錯誤 ★★★、1–5 次 ★★、6 次以上 ★。
                    上方進度條＝星星總數／（地點數×3）＋總分（每個地點最高分加總，負分算 0）。永久累積，不會每週重算。
                    還不能玩的地點放在 COMING（🚧 維修中／建造中），走到門口只顯示「還在準備中，敬請期待」；開放時搬到 SCENES，slot 不變
games/<scene>/      每個遊戲：index.html + images/（檔名小寫 .jpg）
shared/firebase.js  Firebase 設定（只放這裡）＋ window._FB（排行榜、成績紀錄、地圖進度）
shared/player.js    玩家代碼（TWPlayer）＋每局成績上傳（TWResults）
admin/index.html    管理員成績頁（Google 登入，只有 a2224907@gmail.com 看得到；不放連結）
tools/firestore.rules  Firestore 規則（改了要貼到 console 發布）
```

## 場景 ID（資料夾名 = scene = collection 前綴 = GA4 game 參數）
drinks · reserva · breakfast · nightmarket · parcel · bakery · clinic · mrt · street · school · ubike · bus · barber · cinema · parking · icecream · bookstore · market · elevator · noodle · conbini · yansuji
（共 22 個，與首頁 `SCENES` 一致。`airport`、`site4` 還在 `COMING`（維修中／建造中），沒有資料夾。）

Firestore collection：`<scene>game_scores` 或 `<scene>_scores`（沿用各遊戲現有名稱，不要改，否則舊排行榜會消失）。
排行榜需要複合索引：score 降冪 + elapsed 升冪。
管理員頁「設定檢查」會檢查 22 個排行榜索引（school、ubike、bus、barber、cinema、parking、icecream、bookstore、market、elevator、noodle、conbini、yansuji 新增的要自己建），缺的會給「建立索引」連結。

## 成績紀錄與玩家代碼
- 每局結果頁出現時上傳一筆到 `results`（遊戲裡呼叫 `uploadResult()`）：playerId（玩家代碼）、name、scene、score、mistakes、errors（每個扣分原因 zh/es/en＋關卡 stage/stageEs/stageEn）、elapsed、hintViews、script、lang、embed、difficulty（先固定 'normal'）、createdAt。
- 玩家代碼：例如 `MAR-4821`（名字前三個英文字母＋4 位數；沒有英文字母就隨機）。第一次用某個名字時產生，存在 localStorage `taiwan_player.code` 和 `taiwan_codes`（名字→代碼），並登記到 `progress/<代碼>`。
- 地圖進度存在 `progress/<代碼>` = { code, name, done }；換裝置在地圖的名字畫面輸入代碼就接回來（同一個地方取比較高的分數）。
- 規則：排行榜任何人可看、可新增，不能改；results 任何人可新增，只有管理員能讀、能刪；progress 知道代碼就能讀寫，只有管理員能列出全部、能刪。

## 嵌入模式（給地圖用）
iframe 載入：
```
games/<scene>/index.html?embed=1&name=玩家名&s=simp&l=en
```
- `name`：玩家名字（必填，會跳過登入頁）
- `s`：`simp` 簡體，預設繁體
- `l`：`en` 英文，預設西文
- `code`：玩家代碼（地圖會帶，成績紀錄用）
- 嵌入時不顯示登入頁，直接開始。
- 玩完和單機版一樣：結果頁 →「查看排行榜」（成績寫進那個遊戲的排行榜）→ 排行榜的按鈕變成「回到地圖」。

排行榜出現時先送 `{ type: 'scene-result', scene, score, mistakes }`（地圖先記著；這時按地圖的「✕ Salir」也算完成）。

按「回到地圖」時送出：
```js
parent.postMessage({ type: 'scene-complete', scene: '<scene>', score, mistakes }, '*');
```
地圖收到後關掉 iframe 並記錄成績。

## 單一遊戲的網址（不帶 embed=1）
就是單機版：有登入頁、排行榜。畫面上已經沒有連結，但網址留著（Ben 決定）：上課想直接丟一個遊戲給學生時用，以前發出去的連結也不會壞。
`?again=名字&s=…&l=…` 會跳過名字頁直接開始（「重新開始」用），網址參數會自動清掉。

## 共用程式（shared/game.js、shared/game.css）
9 個遊戲共用：設定（繁簡、西英）、翻譯小視窗、背景音樂、朗讀、拼音、單字抽屜、錯誤紀錄、開始畫面、重新開始、地圖嵌入、成績上傳、排行榜，
以及遊戲物件的共用功能（計時、扣分、回饋卡、拼音、圖片、過場）。改這兩個檔案會影響全部遊戲。

每個遊戲的 index.html 裡留下的：
1. 載入順序：`shared/player.js` → Firebase（`initFB`）→ `<link shared/game.css>` → 自己的 `<style>`（顏色變數和自己的樣式）→ 畫面 HTML → `const GAME = {…}` → `shared/game.js` → 自己的程式。
2. `GAME = { scene, track, settingsKey, timerPrefix?, roles }`：場景 ID、GA4 的 game 名稱（沿用舊名）、存設定的 localStorage 名稱、計時器前面的字（預設 ⏱）、朗讀角色的音高。可選 `restartParams(p)`。
3. 自己的程式：`pinyinPro.customPinyin`、資料、`WHO`／`SPEAKER_RE`、`VOCAB`／`VOCAB_OF`、`Hints`、`STAGE`、`NEXT_LABEL`、`const Game = defineGame({ … })`（`setup`、`getConfig`、`render`、`handleChoice`、`formatText`、`setPlace`、`setImage`…；同名功能會蓋過共用版；開始時要多做的事寫在 `onStart()`）、最後 `GameBoot();` 和 `Music.init({…})`。

## 新增遊戲
複製一個現有遊戲（建議 mrt 或 street，最新），只改上面第 2、3 點的遊戲專屬部分，共用的不用複製。
改完跑 `tools/smoke.py` 四種測試。改共用檔時，可以用 `tools/compare_shots.py <遊戲> <舊檔>` 逐畫面比對改之前／改之後。

## 關卡設計原則（2026-10-27，Ben 決定；新遊戲、改舊遊戲都照這個）
新做的遊戲曾經太簡單：對方永遠不會錯，玩家只要照 Ami 的話選就對。原本的九個遊戲不是這樣。每個遊戲至少要有：
1. **對方會出錯（隨機）**：店員／老闆報的價錢、複誦的時間、找的錢、印出來的票、拿給你的東西，有一部分機率是錯的。玩家要自己核對，不能一律「好，謝謝」。
2. **「抓錯」和「沒錯」都要做成正解的可能**：對方說對時，「不對，我要的是…」是錯誤選項（要換成別的內容，不能跟對的一樣）；對方說錯時，「好，謝謝」才是錯誤選項。
3. **三個選項的固定寫法**：①沒錯／謝謝 ②有禮貌地指出問題（含具體正確數字或時間；對方其實沒錯時，數字是錯的）③罵人或沒禮貌的說法（永遠是錯誤選項）。
4. **抓到錯誤之後要有後續**：對方道歉、補錢、重印、重做，不能一句話就結束；必要時多一關確認（例如理髮店 CHANGE_FIX、電影院 TICKET_CHECK）。
5. **綠卡**：做對才出現，放在下一頁對話上方，不另外多一個過場頁。
6. **測試要覆蓋兩種情況**：每個遊戲的 `tools/oracles/<遊戲>.py` 要能依照「對方有沒有出錯」給出正解，`smoke.py perfect` 多跑幾次（隨機）都要 100 分。
7. **新增了要補圖的關卡**，先記在 `docs/image-todo.md`，最後一起做圖。

## 新遊戲：麵店 noodle、超商購物 conbini、鹽酥雞 yansuji（2026-10-27）
地圖 slot 20、21、22（原本的工地 site1～3），`gated: true`＝預設維修中，管理員頁「地圖開關」打開才能玩。排行榜 `noodlegame_scores`、`conbinigame_scores`、`yansujigame_scores`。
三個都照上面的「關卡設計原則」做：對方（老闆／店員）會出錯，錯誤是隨機的，玩家要自己核對。

- **麵店**：點麵（乾麵／湯麵／餛飩麵／牛肉麵）→ 大碗小碗 → 辣不辣 → 蔥 → 小菜（滷蛋、豆干、海帶、燙青菜，一樣一樣問）→ 內用外帶 → **老闆複誦（可能說錯一項）** → **麵端上來（可能有一項不對）** → 報價（可能多算）→ 付錢 → 找錢（可能找錯）。
- **超商購物**：兩種泡麵各有優惠（第二件6折、半價、兩件85折、兩件特價……），要算哪個兩份比較便宜 → 便當加熱 → 買酒要滿十八歲、出示證件（沒買啤酒時沒有這關）→ 手機載具條碼 → **店員複誦條碼（可能唸錯一個字）** → 按按鈕抽折扣 → 報價（可能多掃一次，或抽中折扣卻沒打折）→ 付錢 → 找錢。
- **鹽酥雞**：一樣一樣點（雞排一定有，其他的數量可能是兩份）→ 雞排切不切 → 辣不辣 → 蔥、蒜、洋蔥各要不要（三選一組合）→ **老闆複誦（數量、切不切、辣度、蔥蒜洋蔥其中一項可能說錯）** → **打開袋子核對（同樣可能有一項不對）** → 報價（可能多算沒點的東西）→ 付錢 → 找錢。

共用寫法（每個遊戲的 index.html 裡各有一份，改的時候三個要一起看）：
- `catchState()`：一關「①沒錯／謝謝 ②有禮貌指出問題 ③沒禮貌」，由 `wrong()` 決定對方這次有沒有出錯；抓到錯誤之後有道歉／重做的後續。
- `payStates()`：報價（PAY）、重算後真的付錢（PAY_FIX）、找錢（CHANGE）三關。付的鈔票由 `billFor()` 決定（一百、兩百、五百）。
- 正解在 `tools/oracles/noodle.py`、`conbini.py`、`yansuji.py`；`tools/smoke.py` 已加入名單。
- 圖片檔 `games/<遊戲>/images/*.jpg` 還沒有，缺圖時自動顯示 emoji。
- 台詞和拼音是第一版草稿，需要 Ben 審。

## 冰淇淋店 icecream（2026-10-28 更新）
流程（程式裡的 `ORDER`）：START → SCOOPS（幾球）→ CONTAINER（杯子或甜筒）→ FLAVOR（每球口味）→ SCOOP_CHECK（店員做好，核對口味）→ TOPPING（配料）→ EAT（內用外帶）→ ORDER_CHECK（店員複誦，一次只會說錯一項）→ PICKUP → HANDOVER → PAY（報價）→ PAY_FIX（算錯時重算）→ END → RESULT。
價目：一球 60、兩球 110、三球 150 元；配料每種 10 元。

照「關卡設計原則」，店員會隨機出錯，玩家要自己核對：
- **口味放錯**：店員做好的冰淇淋有約 45% 機率某一球口味放錯，放錯的口味不會和玩家點的一樣；是否算錯，以玩家**實際點的口味**為準。玩家可以指出「第 N 球我要的是…」，也可以收下（Ami 的台詞會加上「我要的是…」）。
- **價錢**：以實際做出來的配料計算（含玩家真的點的配料），不是以任務原本寫的配料。店員報價可能多算一份配料，玩家要算對再重付。
- **結局好壞**：看最後拿到的口味與配料，是不是真的符合 Ami 的訂單，不是看過程中選了什麼。
- 杯裝的冰淇淋球會沉進杯子裡（杯口畫在球的前面）。

## 圖片規格
情境圖：正方形 .jpg，**720×720**、品質約 84（每張約 100–150 KB）。遊戲最大只顯示 360px 寬，720 已足夠高解析螢幕。
Gemini 畫出來的 2048×2048 原圖請先縮小再上傳（原圖保留在自己電腦）。

## 過場（換關卡時）
選完一關後，如果有結果要顯示（對方的回答、綠卡／紅卡），會先出現一頁「過場」，按下面的情境句才進下一關。
情境句寫在每個遊戲的 `NEXT_LABEL`（key 是下一關的名字；沒寫的顯示 `_default` 或「繼續」）。
換關卡時會自動收起清單和右側分頁。

## 背景音樂
程式即時合成（Web Audio），沒有音檔。每個遊戲最後一行 `Music.init({...})` 就是那首曲子：
每個字是一個八分音符，`C5`＝音、`-`＝延長、`.`＝休止、`k s h`＝大鼓、小鼓、鈸。
🎵 按鈕開關，設定存在 localStorage `taiwan_music`（所有遊戲和地圖共用）；朗讀中文時音樂會自動變小聲。
試聽全部：`music.html`。

## 地圖開關
新遊戲在 SCENES 加 `gated: true` ＝ 預設維修中；管理員頁「地圖開關・連結」可改成開啟（存 Firestore `settings/map`），也有每個遊戲的試玩連結。
同一頁的「地圖效果」可設定日夜（跟手機時間／一直夜晚／一直白天）和節慶（跟日期／關閉／直接開啟某個節日），存在同一份 `settings/map`（`night`、`fest`）；網址的 `?night=`、`?fest=` 優先。

## 手機瀏覽器備註：捲動後回不到頂端（2026-10-24）
iPhone 版 Chrome 上，頁面可以捲動時，往下捲之後有時回不到最上面（Safari 正常）。
處理方式（已套用在本遊戲）：
- `<meta name="viewport">` 設 `maximum-scale=1`，不使用 `viewport-fit=cover`。
- `<html>` 加 `html{color-scheme:light}`。

兩項一起改後，手機 Chrome 測試恢復正常；尚未分開測是哪一項有效。新增頁面請照這個寫。

（範圍：首頁、music.html，以及 games/ 底下全部小遊戲；admin、map、tools 沒動。）
