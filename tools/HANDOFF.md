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

## 目前在做：Ben 自己改中文用詞（一個遊戲一個遊戲）
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
- clinic：已在 `rows2.py` 加 `CONF`（130 句），已發布到線上修改表（預設 clinic），等 Ben 改完再套用。`helpers={'desk':'櫃台','doc':'醫生'}` 處理 `desk(...)`／`doc(...)` 包起來的台詞。叫號螢幕、藥袋、狀況卡標題等 HTML 片段的字（目前看診、你的號碼、藥袋、早中晚睡前…）和 SYM 症狀名、OTHER_CARDS 卡名沒抽出來。
- 線上修改表的 `GAMES` 清單裡已改完的遊戲都標「已完成」
- 接下來：clinic、mrt、street（每個遊戲：先在 `rows2.py` 的 `CONF` 加設定（parcel、breakfast 是範例） → 抽出 → 發布表格 → 等 Ben 改完 → 套用）

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
