# 交接包：台灣情境對話遊戲系列（2026-10-14）

## 給新對話的 Claude
- Repo：`wangchiapin/taiwan-life`（GitHub Pages：https://wangchiapin.github.io/taiwan-life/）。先 clone，再讀 `README.md`（共用格式）和這份文件。
- Ben 的固定指示：「請照交接包的「遊戲共用格式」和「主角與世界觀」做，改劇情或圖片前先跟我確認。」
- Ben 常說「先討論，不做任何程式修正，全部確認完再修正」：他這樣說時只討論，等他確認再改。
- Ben 會直接在 GitHub 網頁上傳圖片，所以 push 前一定先 `git pull --rebase origin main`。上傳的大圖要縮成 720×720（麵包 240）。

## 遊戲與頁面
- `index.html` 清單頁，`map/index.html` 地圖模式，`music.html` 音樂試聽。
- `games/<scene>/index.html` + `images/`。scene：drinks、reserva、breakfast、parcel、nightmarket、bakery、clinic、mrt、street。
- 共用機制（詳見 README）：單檔 HTML 狀態機（`getConfig()`、`L(zh,es,en)`、`Game.addMistake`、`Game.good`）、過場 `NEXT_LABEL`、換關時自動收起面板、背景音樂（`Music`，共用 key `taiwan_music`）、嵌入模式 `?embed=1&name=` → `postMessage scene-complete`、清單頁帶 `?again=名字&s=&l=` 免再輸入名字、拼音用 pinyin-pro `customPinyin`（台灣讀音）、簡體用 opencc。
- Firebase（tiendadebebidas-d75ac）排行榜：程式寫好了，但需要 Ben 在 console 建複合索引（score desc、elapsed asc）並檢查 rules；設定裡 messagingSenderId/appId 可能對調了，等 Ben 提供正確設定再修。

## 2026-10-16 改名＋星星（Ben 決定）
- 名稱：**台灣生存日記**（簡：台湾生存日记）· Sobrevive en Taiwán · Survive in Taiwan；標題前面不放圖示。
- 原本的「這週完成」進度條改成**收集星星**（永久，不會每週重算）：0 次錯誤 ★★★、1–5 次 ★★、6 次以上 ★。建築屋頂上緣只顯示星星；進度條右邊顯示「⭐ 星星數 / 27 · 總分」（總分＝每個地點最高分加總，負分算 0）。每個地點分開記最高分和最少錯誤，舊進度直接換算。
- Ami：還有沒去過的地點就推薦下一個；都去過了推薦還沒拿滿星的地點；全滿就稱讚。
- **之後的點子（Ben 說先記著）**：用總分做整張地圖的總排行榜。

## 2026-10-16 改成正式地圖模式（Ben 決定）
- 首頁 `index.html` 就是地圖；原本的遊戲清單頁刪掉；`map/` 舊網址自動轉到首頁；地圖上回清單的按鈕和連結拿掉。
- 單一遊戲網址 `games/<scene>/` 留著（不放連結），給上課直接丟連結用。
- 地圖模式玩完也進排行榜：結果頁 →「查看排行榜」→ 按鈕變成「回到地圖」才送 scene-complete（`shared/game.js` 的 `showLeaderboard`）。smoke.py embed 測試會檢查排行榜有寫、scene-complete 有送。排行榜一出現，遊戲先送 `scene-result`；這時學生按地圖右上角「✕ Salir」也算完成（Ben 決定）。玩到一半按 Salir 不算。
- 第 4 步的檢查清單（https://claude.ai/artifact/EgrTFKHk5Y41FgR1tZML3X，db 集合 `decisions`，文件 id＝項目 id、內容 {choice: 改/不改/再討論, note}）：2026-10-16 已照 Ben 的決定改完（82 項：79 改、3 不改）。統一的決定：連接詞「和」全部念 hàn、「嗯」全部念 ēn（每個遊戲最後一個 customPinyin）；西文對玩家說話不分男女（不用 listo/solo/bienvenido…）；店員招呼用「¡Hola, buenas!」。檢查工具在 `tools/review/`，之後改台詞可以重跑 pinyin_rules.js、pinyin_check.js、vocab_live.py。

## 2026-10-19 地圖第三條街（Ben 決定）
- 地圖擴充成 20×42（第三條馬路在第 33、34 列），BUILD_SLOTS 0–23。新增維修中的房子：公車(11)、YouBike(14)、理髮店(15)、停車場(16)、冰淇淋店(17)、書店(18)、搭電梯(19)；剩 4 個工地（20–23）。
- 學校、YouBike、公車、理髮店之後要做成真的遊戲（學校＝請假、理髮店含預約、公車跟捷運內容區分）；電影院、停車場、冰淇淋店、書店、菜市場、搭電梯 Ben 之前在本機做過六個遊戲，目前地圖上維持維修中，之後再細修。

## 下一階段（2026-10-15 Ben 確認的計畫，照順序做）
九個遊戲的中文用詞 Ben 已經全部改完（見下面「中文用詞」）。Ben 說之後會自己全部玩一次。接下來照這個順序：

1. **地圖擴充**（`map/index.html`）✅ 2026-10-15 完成：地圖 20×28（第二條橫向馬路在第 19、20 列），畫面跟著玩家捲動；`COMING` 放學校、電影院、菜市場、機場（slot 12、寬 7 格）＋ 3 個工地（Ben 選 3 個就好）；提示顯示「中文＋玩家選的語言」。BUILD_SLOTS 0–15 已全部用完，要再加地點得再往下延伸一塊。
   - 用 A 方案：地圖往下延伸，畫面跟著玩家捲動（現在是 20×14 格、640×448 固定畫布，8 個建築位置已滿）。
   - 新加 4 個地點，先標「🚧 維修中」：學校、機場（**佔兩格寬**）、電影院、菜市場。
   - 另外加 5 個左右的空位，標「建造中」（圍欄、工地），代表之後要擴充的地點。
   - 維修中、建造中都不能進去，走到門口顯示「還在準備中，敬請期待」（中、西、英）。
2. **Firebase 修正 + 每局上傳完整紀錄 + 管理員成績頁** ✅ 2026-10-15 程式完成（`shared/`、`admin/`、`tools/firestore.rules`、`tools/apply_firebase_results.py`）。
   2026-10-15 Ben 已在 console 全部設定好並測試通過：規則、Google 登入、9 個排行榜索引。注意：API 金鑰（Browser key，6/23 建的那把）有限制網站，要允許 `https://tiendadebebidas-d75ac.firebaseapp.com/*`，Google 登入才不會被擋（API_KEY_HTTP_REFERRER_BLOCKED）。
   原本的規則只開放 drinkgame_scores，其他 8 個排行榜一直寫不進去；新規則一起修好。Ben 要在 console：貼規則、開 Google 登入＋授權網域 wangchiapin.github.io、用管理員頁「設定檢查」建 9 個排行榜索引。
   smoke.py 的假 Firebase 改成會記錄寫入，每局檢查「剛好一筆 results、內容和遊戲一致、單機版有寫排行榜」（結果最後一欄 FB✓）。bakery 隨機玩偶爾 timeout 是舊問題（舊版本也會），不是上傳造成的。
   - **firebaseConfig 確定錯位了**：9 個遊戲裡 `messagingSenderId` 放的是 appId、`appId` 放的是 measurementId。Ben 提供的正確值：
     apiKey "AIzaSyD2lxec6JTbERwFPGjDzriYzIH7o9IRWnw"、authDomain "tiendadebebidas-d75ac.firebaseapp.com"、projectId "tiendadebebidas-d75ac"、storageBucket "tiendadebebidas-d75ac.firebasestorage.app"、messagingSenderId "947444542062"、appId "1:947444542062:web:62e209f33cfc3ae12c547f"、measurementId "G-PGQZPYNBLX"。
   - 這個 Firebase 專案只有這系列遊戲在用，可以放心改規則。**Ben 還沒貼目前的 Firestore 規則**，改規則前先跟他要。
   - 排行榜複合索引（score desc、elapsed asc）要請 Ben 在 console 建（寫步驟給他）。
   - 新增統一的成績集合（例如 `results`）：每局一筆，含 playerId（玩家代碼）、名字、scene、score、mistakes、錯在哪裡（每個扣分原因 zh/es/en＋關卡）、elapsed、hintViews、script、lang、embed（地圖或單機）、difficulty（先固定 'normal'）、createdAt。地圖模式也要上傳。舊排行榜集合照舊，不要改名。
   - **玩家代碼（Ben 選 A）**：第一次玩時產生短代碼（例如 `MAR-4821`，名字前三碼＋4 位數），存在 localStorage；換裝置時輸入代碼就能接上。
   - **地圖進度也上傳**（用玩家代碼當 key），換裝置輸入代碼後讀回來。
   - **管理員成績頁** `admin/index.html`：Google 登入，只有 **a2224907@gmail.com** 能讀（Firestore 規則：成績任何人可新增，只有這個帳號可讀、可刪）。內容：總覽（玩家數、局數、近 7 天、最熱門遊戲）、玩家×遊戲最高分表、點玩家看每局紀錄（含錯在哪裡）、點遊戲看最常錯的題目、篩選（日期、遊戲、名字）、匯出 CSV、**可以刪除紀錄**（單筆、整個玩家）。
3. ✅ 2026-10-15 完成：**共用程式抽成共用檔** `shared/game.js`、`shared/game.css`（用法見 README「共用程式」）。
   - 9 個遊戲都改好；`tools/share_game.py` 逐段比對（忽略註解、空白、遊戲名稱這類參數），完全一樣才刪；不一樣的 function 留在遊戲裡蓋過共用版：breakfast 的 `stageOf`、`Game.maybeTrans`，parcel 的 `restartGame`（多帶 store），reserva 的 `Game.addMistake`、`Game.feedbackHTML`（它的扣分原因可以只有中文）。
   - reserva 先把兩處舊寫法換成新寫法（翻譯視窗的角色名稱改用 WHO／SPEAKER_RE、朗讀男聲改用 malePitch），效果一樣；順手修了英文版錯誤紀錄沒有關卡名稱時會顯示 undefined。
   - CSS：只搬 9 個遊戲完全一樣、而且搬過去不會改變先後順序效果的 59 條；第一次多搬了會造成手機版朗讀／翻譯按鈕變小，已改掉。
   - 驗證：`tools/compare_shots.py` 改之前／改之後逐畫面比對（繁西、簡英＋拼音、手機、嵌入），9 個遊戲約 1,500 張畫面一致（reserva 只有「通話中」閃爍小圓點拍到不同瞬間）；smoke.py 四種測試通過；從地圖進每個遊戲正常。
   - 新增：地圖裡「重新開始」會帶玩家代碼。
   原本的計畫：設定、翻譯、朗讀、拼音、單字抽屜、錯誤紀錄、提示、過場、排行榜、成績上傳、音樂、嵌入模式、重新開始。九個遊戲改成載入共用檔，**之後的新遊戲也用它**。抽完每個遊戲都要跑 smoke.py 四種測試。
4. **九個遊戲全面檢查一次**（共用檔抽完再做，只做一次）：西文、英文翻譯和中文是否一致（這次改過很多句）、拼音台灣讀音（必要時加 `customPinyin`）、單字表（`VOCAB`）的詞是否還出現在對話裡。Ben 會另外找西文母語者看翻譯。
5. **難度設定**：⏸ 2026-10-16 Ben 決定**無限期延後**（成績紀錄的 difficulty 欄位照舊固定 'normal'）。下面是當時的討論，留著備查。
   - 2026-10-16 已提給 Ben 兩個方向，**等 Ben 回答，還沒改任何程式**：
     - 方向 A（建議先做）：台詞不變，只調輔助——簡單＝拼音預設開、要記的資訊一直看得到、朗讀慢一點、錯了少扣；困難＝不能開拼音、翻譯用了扣分或沒有、資訊只出現一次。只改 shared/game.js，9 個遊戲一次到位。
     - 方向 B：不同難度不同台詞（工作量大、每句要 Ben 確認），建議從新遊戲（電影院）開始做。
     - 待 Ben 決定：(1) A／B／A 先做 B 留給新遊戲 (2) 兩級（簡單／普通）或三級（加困難） (3) 誰選難度：學生在開始畫面選／老師給帶難度的連結／兩種都有 (4) 排行榜每個難度分開，或同一榜標難度。
     - 決定後先做畫面樣子給 Ben 看，確認才改。

其他 Ben 的決定：刪掉旁白後只剩選項的頁面，Ben 自己玩過再決定要不要補；麵包圖的畫風不用改；reserva、breakfast 之後補 oracle（正解測試）。

## 中文用詞（已完成）的流程與紀錄
流程：
1. 用 `tools/edit/rows2.py <game>` 從遊戲抽出所有中文（產生 `tools/edit/site/rows/<game>.json` 和 `tools/edit/priv/priv_<game>.json`，priv 存原始程式字串和位置）。新遊戲要先在 rows2.py 的 `CONF` 加設定（參考 reserva、breakfast）。
2. 把 `tools/edit/site/index.html` 和 rows 發布到線上修改表：https://claude.ai/artifact/WBeNojoGuKyvoHHyjVY8G7（db 集合 `edits`，文件 `edits/<rowId>` = `{game, id, text, updatedAt}`）。在 `GAMES` 加遊戲、預設 `S.game`。
3. Ben 說改好了 → 用 ArtifactData 讀 `edits`（where game == X），對照 rows/priv 列出舊→新。
4. 寫 `tools/edit/apply_<game>.py`（精確字串取代，找不到就停），同步改：西文/英文翻譯、依選項文字判斷的程式（`c === '...'`、`startsWith`、vocab）、〔佔位〕還原成原本的 `${...}`。明顯錯字（例如「旺季」→「忘記」）直接修，但要跟 Ben 說。寫「（這句話刪除）」= 整句刪掉。
5. 檢查新句子的拼音（必要時加 `customPinyin`），跑測試，commit + push，跟 Ben 報告你自己改了哪些地方。

套用時的經驗（breakfast、parcel）：
- `apply_<game>.py` 是 `(舊字串, 新字串[, 預期次數])` 的清單，次數不對就停。同一句出現在兩個關卡會是兩列（parcel 的 099/121、110/117），Ben 通常兩列改成一樣，次數寫 2。
- 改選項文字時，程式裡判斷選項的地方（`c.startsWith(...)`、`ch === '...'`）和 `tools/oracles/<game>.py` 都要一起改（parcel：「我要加值悠遊卡。」）。
- Ben 把兩句併成一句（另一句寫「（這句刪除）」）時，併進去的內容要保留原本的條件（parcel 結局：「我自己的包裹還沒到」只有 `!t.yourArrived` 才出現）。
- 半形標點（`!`、`:`）改成全形，句尾缺句號就補，這種小事做了要告訴 Ben。
- 新句子的拼音用 `node` 配 `tools/.npm/node_modules/pinyin-pro` 檢查；套件讀錯的字加進該遊戲的 `customPinyin`（parcel：還需→hái xū、欸→ēi；breakfast：還加→hái jiā）。
- 單字（`VOCAB`）：對話裡已經不出現的詞換成新出現的詞（breakfast：煎台→點單機、買菜→交給；parcel：插→櫃台、結局加油飯）。
- 發布表格：`Artifact` publish，`url` 用上面那個，`file_path=tools/edit/site/index.html`，`files={'rows/<game>.json': 路徑}`（已發布的其他 rows 會保留）；publish 前要先用 `Artifact read` 讀過那個 url。新的類別名要加進 `index.html` 的 `KIND_ORDER`，不然上面的類別按鈕不會出現。
- `rows2.py` 重跑會重新編號、重算位置，已套用完的遊戲不要再跑。
- parcel 的 `CONF` 是最新範例（`phone` 區塊、`簡訊`/`LINE訊息`/`手機標題`/`結尾包裹說法` 類別）；手機畫面上的寄件標籤（「房東太太」「簡訊（房東太太轉傳）」）和包裹標籤（收件人／寄件人）沒抽出來。

進度：
- drinks ✅、reserva ✅（43 處）、breakfast ✅（34 處）、parcel ✅（30 句＋旁白刪 3 句，已上線）、nightmarket ✅（Ben 改 26 句，已套用：019/020/024/049/130 刪除並併入前一句，087/093 的提示話拿掉）、bakery ✅（Ben 改 48 句，已套用並推上去；`apply_bakery.py`）
- clinic ✅（Ben 改 31 句，已套用並推上去；`apply_clinic.py`）。`rows2.py` 的 clinic 設定用 `helpers={'desk':'櫃台','doc':'醫生'}` 處理 `desk(...)`／`doc(...)` 包起來的台詞。叫號螢幕、藥袋、狀況卡標題等 HTML 片段和 SYM 症狀名、OTHER_CARDS 卡名沒抽出來。
- 線上修改表的 `GAMES` 清單裡已改完的遊戲都標「已完成」
- mrt ✅（Ben 改 46 句，已套用並推上去；`apply_mrt.py`）。103 Ben 改成「（你坐在優先席上。）」。`rows2.py` 的 mrt 設定用 `helpers={'staff':'站務員'}`；站名、DRINKS、阿嬤／阿公、路線圖和加值機畫面的字沒抽出來。
- street ✅（Ben 改 44 句，全部已套用並推上去；`apply_street.py`，016 後來 Ben 改成「（行人號誌是紅燈。路上沒什麼車，所以旁邊有兩個人直接走過去了。）」）。CONF 用 `statere` 抓 `E_xxx: mk(` 當關卡；新類別「選錯後的反應」（`th`）。號誌、問路小卡畫面的字和 WHOS／先生小姐／地標資料沒抽出來。

### parcel 的旁白（錯誤後的提示話）：Ben 已決定
- 刪除：086（驗算）、067（房東太太的名字）、141（加值金額）；已從遊戲拿掉。
- 保留：063（是誰的號碼）、094、098（房東先生的末三碼、名字只在電話裡說）。
- 這 3 句保留的旁白不要再動。parcel 全部完成。

## 延後的事
- 難度分級（簡單／普通，NPC 台詞依難度不同）：Ben 說「以後再說」。
- 地圖的七天結構。
- 麵包圖是照片風，可以考慮重畫成像素風（提示詞加上 "in pixel art style, not a photo"）。

## 測試工具（tools/）
- 先安裝相依套件：`cd tools && npm i pinyin-pro opencc-js --prefix .npm`（`.npm/` 已加入 gitignore）；另外要有 Python Playwright 和 Chromium。
- `python3 tools/smoke.py perfect|mixed|embed|trans [games...]`：perfect 是照正解玩（應該 100 分），mixed 是隨機玩，embed 是嵌入模式，trans 會列出過場。正解 oracle 放在 `tools/oracles/`，drinks 的寫在 smoke.py 的 `EXTRA` 裡；reserva、breakfast 沒有 oracle，只能隨機玩。
- `tools/songs.py`、`tools/music.js`：背景音樂的來源。

## 圖片提示詞文件
- MRT：https://claude.ai/code/artifact/1e13584c-6b11-4dd1-9b34-41f702f93e79
- 街頭事件：https://claude.ai/code/artifact/5b761cac-74b3-4101-87d2-7f54557e9f99
- 麵包／吃藥／小綠人：https://claude.ai/code/artifact/e5a7c9c9-f02c-427d-820e-84c923bcf9f9

### nightmarket 套用時的決定（Ben 確認）
- 020（「再看看」提示）Ben 決定刪除；018 保留「殺價的時候要有技巧喔」，單字表 START 換成 技巧、敢，CALL 換成 變胖（原本 長高）。
- 結局「衣服和髮夾，我殺價省了…」併進上一句，仍只在 `Game.saved > 0` 時出現。
- `rows2.py` 的 nightmarket 設定有 `nm` 區塊（amiLines、listHTML、殺價引擎等函式內的字串）可當範例。

### bakery 套用時的決定（Ben 確認）
- 031（蛋糕清單的規則提示）刪除：`rule = null`，清單渲染對 null 安全；036 規則改成「Ami對堅果過敏。」。
- 結局 166：只有 `Game.clickedTongs` 才稱讚夾子，否則「Ami：哇，${N}，你好厲害！我們去公園吃吧！」。
- 017 是 Ben 自己改的（「你看你另外要吃什麼，但是不要買有堅果的喔！…」）；107 用「櫃台」；PICK 的 dialogue 改成空陣列；錯誤卡片後的提示旁白（054、056、059、074、082、089、096、113、119、132、139、148、154）全部移除。
- 單字表：K_GREET 順便→朋友，K_CONFIRM 複誦→這樣對嗎，K_NAME 取貨人→朋友。
- 我順手修的：023 的「要要」、164 缺的「）」。
- `rows2.py` 的 bakery 設定示範了 `ternary=True`（「A／B」三元運算式）、`fnmap`（函式內字串的類別名）、`first`。資料常數（SHELF 麵包名、FLAVORS、PICKUP 選項、托盤／清單標題）不在表格裡。

### clinic 套用時的決定（Ben 改的）
- Ami 的 LINE：022、023 併進 021（「我今天要開會，不能陪你去」拿掉，「公司旁邊」→「附近」）。因為重點都在第一句，任務提示改成列出全部 Ami 的話（原本 `slice(1)` 跳過第一句）。
- 刪除的旁白：045 走進診所、058 填初診單、078 走進診間（098「拿著單子，回到櫃台」Ben 決定保留，過場頁也保留）；錯誤後的提示旁白（083/089/095 看狀況卡、117 看藥袋、126 看任務提示）全部移除。
- 綠卡說明前面都加了稱讚語（很好！、不錯唷！、沒錯！…）。
- 單字表：START 加 生病，W_WAIT 加 過號，D_ALLERGY 的 有沒有 → 吃藥。
- 我順手修的：090「吃藥會過敏嗎?」半形問號改全形；customPinyin 加 聽得懂 → tīng de dǒng。

### mrt 套用時的決定（Ben 改的）
- 025 併進 024（站務員一句講完整條路線）；Ami 的 022、023 改短，不再交代「不夠要先加值」。
- 刪掉的旁白：045/046（刷卡、嗶嗶）、054、063、072（紅線月台）、079、088（在台北車站下車）、089（台北車站好大）、096（藍線月台）、121（Ami 在出口）。P_RED、X_XFER、P_BLUE 現在沒有旁白，只有路線圖和選項。
- 錯誤後的提示旁白（053、076、084/085、094、100、109、117/118）全部移除。
- 選項 065 改成「請問要怎麼搭去〔目的地〕站？」，判斷和 `tools/oracles/mrt.py` 一起改。
- 103、108 用「優先席」；單字表 T_SEAT 博愛座→慢慢。
- 單字表：START 加值→夠；G_DRINK 不能→禁止飲食；G_TAP 換成 只剩／不夠／再刷一次／加值機／加值；G_TOP 加值機→票價；T_SEAT 拐杖→優先席；T_BLUE 車門→廣播；END 出口、順→解鎖、複雜。
- 我順手修的：112 Ben 的句子少了「）」補上；customPinyin 加 路上→lù shàng、名字→míng zi。

### street 套用時的決定（Ben 改的）
- Ami 的 LINE：010 刪除，008/009 改短。
- 刪除：047（蹲下來問他：E_fall 的 `after` 整個拿掉，選對才有綠卡過場）、057（救護車來了）、069、070、099、111（結局旁白，Ami 直接說話）。
- 026 機車那關只剩「（叭！叭！）」；037、059、078、088、100 旁白改短。
- 選項：049 改「我幫您叫救護車」（`tools/oracles/street.py` 一起改；判斷看 `ok`，不看文字）、018、028、040、064、091、094、106。
- 單字表：START 路口、處理→趕快、路上；E_light 斑馬線→交通規則、三寶；E_honk 小巷、人行道→瞪、點頭；E_elder 菜籃、閃→催、紅燈；E_wallet 叫住→提醒；E_flyer 加 拒絕；END 加 經驗。
- 我順手修的：customPinyin 加 路上、走得、處理得、慢慢地、客氣地、認識。
