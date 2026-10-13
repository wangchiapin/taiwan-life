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

進度：
- drinks ✅、reserva ✅（43 處，已上線）
- breakfast：表格已上線（102 行，新類別「老樣子說法」），**等 Ben 改完**
- 接下來：parcel、nightmarket、bakery、clinic、mrt、street

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
