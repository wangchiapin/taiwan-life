# 台灣情境對話遊戲系列（Taiwan Week）

> 飲料店、訂位、早餐店、診所、捷運、夜市、包裹、麵包店、街頭等情境對話遊戲

- **網址：** https://wangchiapin.github.io/taiwan-life/
- **Firebase 專案：** tiendadebebidas-d75ac
- **登入方式：** —（玩家輸入名字）
- **狀態：** 使用中
- **備註：** 排行榜集合為 `<場景>game_scores` 或 `<場景>_scores`，不要改名，否則舊排行榜會消失。

---

# 情境對話遊戲系列（Taiwan Week）

## 結構
```
index.html          遊戲選單（之後換成「台灣一週」地圖）
map/index.html      地圖模式（測試版）：走到建築門口 → iframe 載入 games/<scene>/?embed=1 → 收 scene-complete
                    20×28 格，畫面一次看 20×14 格，跟著玩家上下捲動。
                    還不能玩的地點放在 COMING（🚧 維修中／建造中），走到門口只顯示「還在準備中，敬請期待」；開放時搬到 SCENES，slot 不變
games/<scene>/      每個遊戲：index.html + images/（檔名小寫 .jpg）
shared/firebase.js  Firebase 設定（只放這裡）＋ window._FB（排行榜、成績紀錄、地圖進度）
shared/player.js    玩家代碼（TWPlayer）＋每局成績上傳（TWResults）
admin/index.html    管理員成績頁（Google 登入，只有 a2224907@gmail.com 看得到；不放連結）
tools/firestore.rules  Firestore 規則（改了要貼到 console 發布）
```

## 場景 ID（資料夾名 = scene = collection 前綴 = GA4 game 參數）
drinks · reserva · breakfast · thsr · gas · nightmarket · parcel · bakery · clinic · mrt · street

Firestore collection：`<scene>game_scores` 或 `<scene>_scores`（沿用各遊戲現有名稱，不要改，否則舊排行榜會消失）。
排行榜需要複合索引：score 降冪 + elapsed 升冪。
管理員頁「設定檢查」會檢查 9 個排行榜索引，缺的會給「建立索引」連結。

## 成績紀錄與玩家代碼
- 每局結果頁出現時上傳一筆到 `results`（遊戲裡呼叫 `uploadResult()`）：playerId（玩家代碼）、name、scene、score、mistakes、errors（每個扣分原因 zh/es/en＋關卡 stage/stageEs/stageEn）、elapsed、hintViews、script、lang、embed、difficulty（先固定 'normal'）、createdAt。
- 玩家代碼：例如 `MAR-4821`（名字前三個英文字母＋4 位數；沒有英文字母就隨機）。第一次用某個名字時產生，存在 localStorage `taiwan_player.code` 和 `taiwan_codes`（名字→代碼），並登記到 `progress/<代碼>`。
- 地圖進度存在 `progress/<代碼>` = { code, name, done }；換裝置在清單頁或地圖輸入代碼就接回來（同一個地方取比較高的分數）。
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
- 嵌入時不顯示登入頁和排行榜，直接開始。

遊戲結束時（結果頁按「回到地圖」）送出：
```js
parent.postMessage({ type: 'scene-complete', scene: '<scene>', score, mistakes }, '*');
```
地圖收到後關掉 iframe 並記錄成績。

## 從清單頁進遊戲（不用再輸入名字）
清單頁（index.html）和地圖共用玩家資料：localStorage `taiwan_player` = { name, script, lang }。
清單頁有填名字時，點遊戲會開 `games/<scene>/index.html?again=名字&s=…&l=…`，遊戲跳過名字頁直接開始（單機版，有排行榜），網址參數會自動清掉。
沒填名字，或直接用網址進遊戲，遊戲照常先問名字。

## 不帶 embed=1
就是單機版：有登入頁、排行榜，連結可以直接發給學生。

## 新增遊戲
複製現有遊戲的共用區塊（設定、翻譯、朗讀、單字、錯誤紀錄、排行榜、重新開始），只換遊戲專屬部分；詳見交接包。

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
