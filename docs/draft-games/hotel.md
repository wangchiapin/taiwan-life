# 飯店 hotel（P-004）遊戲架構

> **尚未修改（第一版草稿：台詞、拼音、流程待 Ben 審；測試等修改完再寫）**
> 2026-11-01 自動排程產生。**讀音沒有對照 game-kit**（這次排程讀不到 game-kit，見「讀音核對」）。
> 遊戲：`games/hotel/index.html`；排行榜 collection `hotelgame_scores`（Firebase 規則還沒加，所以成績暫時寫不進去，這是預期的）；圖片提示詞：`docs/image-prompts-hotel.md`。
> 還沒放進地圖／後台（沒改首頁 SCENES、admin、music.html、shared/firebase.js、smoke.py、rules）。

## 劇情

Ami 幫主角訂好飯店（用 Ami 的名字訂）。主角到櫃台辦入住 → 房間有兩個隨機的問題（冷氣不冷、沒有熱水、吹風機沒反應、網路連不上，四選二）→ 打房間分機找櫃台、說明問題與房號 → 房務來處理 → 隔天退房，核對迷你吧有沒有被多算或漏算。Ami 用 LINE 交代訂房內容與「房間有問題就打電話給櫃台」。

## 關卡流程（ORDER）

START → DESK（說有訂房、名字是 Ami）→ **DESK_CHECK（櫃台複誦訂房：房型、晚數、含不含早餐，可能說錯一項）** → ROOM（發現問題，怎麼找人）→ REPORT1（說第一個問題）→ REPORT2（說第二個問題）→ ROOMNO（說房號，三個房號選一個）→ **HK_CHECK（櫃台複誦房號與兩個問題，可能說錯一項）** → **HK_DONE（房務說都修好了，房間檢查卡顯示，可能有一項其實還是壞的）** → **CHECKOUT（退房，迷你吧消費可能多算或漏算）** → END → RESULT。

## 對方出錯點與機率

| 關卡 | 錯誤機率 | 怎麼出錯 | 正解 |
|---|---|---|---|
| DESK_CHECK | 45% | 房型／晚數／早餐其中一項說成不一樣的 | 沒錯→「對，沒錯。」；錯→有禮貌說出正確的那一項 |
| HK_CHECK | 45% | 房號加十，或其中一個問題換成沒有發生的問題 | 同上 |
| HK_DONE | 45% | 房務說兩項都好了，但檢查卡有一項顯示「還是…」 | 沒錯→「好，謝謝你。」；錯→指出還沒好的那一項 |
| CHECKOUT | 45% | 你有喝迷你吧的礦泉水但櫃台說沒消費，或沒喝卻說有消費（五十元） | 沒錯→謝謝／付五十元；錯→誠實說出實際情況 |

三個選項固定寫法：①沒錯／謝謝 ②有禮貌指出問題 ③沒禮貌（永遠錯）。選項依玩家實際的情況（`t.drank`、`t.probs`）產生。價錢：只有迷你吧礦泉水五十元（待確認），沒有找零關卡（用零錢付）。

## 正解怎麼判定

- 一般關卡：選錯扣十分並留在原關（共用 `catchState`）；抓到錯誤之後有道歉／重修／改帳的後續。
- 好結局：錯誤 ≤ 2 次。因為 `catchState` 不讓玩家「收下錯誤」往前走，所以最後實際狀況（房間修好、帳單正確）一定和 Ami 的訂單、玩家實際情況一致。
- 房號：`floor×100+號碼`，念法用 `zhDigits`（例如「五零七」）。

## 單字表（VOCAB，共 44 個，每個都在畫面或台詞出現；分數／錯誤／扣分出現在共用的結果頁）

| 關卡 | 單字 |
|---|---|
| START | 飯店（hotel）、訂房（reservar una habitación）、房間（habitación）、櫃台（recepción）、退房（hacer el check-out） |
| DESK | 歡迎光臨（bienvenido(a)）、入住（hacer el check-in）、訂房（reservar una habitación） |
| DESK_CHECK | 單人房（habitación individual）、雙人房（habitación doble）、晚（noche）、含早餐（con desayuno incluido）、確認（confirmar）、不好意思（disculpe） |
| ROOM | 房卡（tarjeta de la habitación）、冷氣（aire acondicionado）、熱水（agua caliente）、吹風機（secador de pelo）、網路（internet）、分機（extensión (teléfono interno)）、房務（personal de limpieza） |
| REPORT1 | 沒有熱水（no hay agua caliente）、連不上（no se puede conectar）、沒有反應（no responde）、不冷（no enfría） |
| ROOMNO | 房號（número de habitación）、幾號房（¿qué número de habitación?） |
| HK_CHECK | 同仁（compañero(a) de trabajo (formal)）、處理（encargarse de, resolver）、對嗎（¿es correcto?） |
| HK_DONE | 修好（arreglar）、還是（todavía, aun así）、試試看（probar）、房務員（personal de limpieza de habitaciones） |
| CHECKOUT | 退房（hacer el check-out）、迷你吧（minibar）、礦泉水（agua mineral）、消費（consumo, gasto）、零錢（monedas, cambio suelto） |
| END | 舒服（cómodo）、下次（la próxima vez） |
| RESULT | 分數（puntos）、錯誤（error）、扣分（restar puntos） |

## 讀音核對

- **這次沒有對照 game-kit**：add_repo 工具在這個排程的環境裡不能用，直接 clone 私人 repo 也被拒（需要登入）。所以沒有讀到 game-kit 的 readings.txt、rules.csv、classes.txt、gt_compare.js 和讀音待處理清單。依【3-1】第 6 點，進度檔寫「完成（讀音待核對）」。
- 實際做法：用共用檔 `shared/game.js` 內建的 GoodTeacher 規則（由 `tools/build_gt_rules.js` 產生，不手改）算拼音，用 Playwright 把遊戲 30 次隨機局中顯示的中文詞（共約 260 條）逐一印出人工檢查。
- 發現與處理：pinyin-pro 預設讀錯的詞，放進遊戲自己的 `customPinyin`：怎麼 zěn me、舒服 shū fu、還舒服 hái shū fu、住得 zhù de、連得上 lián de shàng。其餘飯店詞（櫃台、房務、退房、迷你吧…）也加了讀音以防萬一。
- **GoodTeacher 尚未涵蓋的詞**：沒辦法判斷（沒對照）。上面 5 條需要 Ben 或下一次有 game-kit 時確認：是 GoodTeacher 已有規則（那就該照它、移掉 customPinyin），還是尚未涵蓋。
- 已知維持原讀音的詞（飯店裡沒用到）：東西 dōng xi（有用到，已設定）。

## 查證來源

- 找到的資料很少：交通部觀光署與臺北市旅館業管理自治條例（<https://laws.gov.taipei/law/LawSearch/LawPrint/FL021703?type=0>）只是旅館業的一般規定，沒有寫客房設備壞掉怎麼處理。
- 世界日報〈入住飯店別只拿房卡 先問這6件事〉（<https://www.worldjournal.com/wj/story/121471/9671328>）主要是美國情況，只參考「迷你吧可能有感應計費」。
- 其他（辦入住說訂房人名字、櫃台複誦訂房、房間分機撥「0」或櫃台分機、房務到房間處理、退房還房卡並結迷你吧）**都是憑常見做法，標待確認**。

## 待確認

1. 台灣飯店客房電話找櫃台是撥「0」還是「9」、各家不同；遊戲只寫「撥分機找櫃台」。
2. 辦入住是否要出示護照／證件、押金（遊戲沒有做；外國旅客入住通常要登記證件）。
3. 迷你吧礦泉水價錢（暫定五十元）、退房時間與是否當場結算迷你吧。
4. 房務員稱呼（用「房務」／「房務員」）與櫃台說「房務同仁」是否自然。
5. 共用檔 GoodTeacher 規則和 game-kit 是否一致（本次沒對照）。
6. 圖片全部還沒做（缺圖時顯示 emoji）。
