# 要補的圖（做完一張刪一行；一次做一張，Ben 確認再下一張）

## 其他（公車，先前記下的）
- [ ] 公車：「別號碼的公車進站」那幾關目前暫用 hail.jpg。

## 冰淇淋店 icecream
- [ ] HANDOVER（店員遞冰淇淋）：暫用 shop.jpg。可選：店員的手遞出冰淇淋（用 shop.jpg 當底圖，編輯式提示詞）。

## 書店 bookstore
- [ ] FIND 書賣完時書架少一本：目前用 HTML 書架顯示，不需新圖。
- [ ] STOCK（問店員有沒有庫存）：暫用 counter.jpg，可選補一張「店員拿著書從倉庫走出來」。

## 停車場 parking
- [ ] PAY_CHECK（繳費機螢幕出現應付金額）：用 machine.jpg + HTML 卡片，不需新圖。

## 菜市場 market
- [ ] CHANGE（找錢）暫用 pay.jpg、CHECK（拿菜）暫用 stall.jpg：可選補「老闆把找的錢放在手上」「老闆遞出一袋菜」兩張（用 stall.jpg 當底圖，編輯式提示詞）。

## 電梯 elevator
- [ ] EARLY（電梯中途停在別的樓層，門開了，外面有人要上電梯）：暫用 hall.jpg。建議補一張「電梯門開，外面是別層走廊，牆上有樓層數字，有人站在門外」。用 elevator.jpg 當底圖，編輯式提示詞。

## 電影院 cinema（2026-10-27 Ben 指定）
- [x] （已完成 10/27）counter_sorry.jpg：售票員被抓到說錯（總價、座位、找錢、票印錯）時的尷尬表情。放進 games/cinema/images/ 就會自動使用；沒有這張圖時自動用 counter.jpg。用 counter.jpg 當底圖，編輯式提示詞（只改表情）。
- [x] （已完成 10/27）snack_sorry.jpg：爆米花櫃台店員給錯爆米花口味被抓到時的尷尬表情（用 snack.jpg 當底圖，只改表情）。沒有圖時自動用 snack.jpg。

## 麵店 noodle、超商 conbini、鹽酥雞 yansuji（2026-10-27）
提示詞全部寫在 `docs/image-prompts-noodle-conbini-yansuji.md`（共 23 張，含順序、底圖、檢查重點）。做完一張勾一張，一次做一張，Ben 確認再下一張。
- [ ] noodle：shop、side、bowl、pay、start、result、end_good、end_bad
- [ ] conbini：counter、shelf、draw、pay、start、result、end_good、end_bad
- [ ] yansuji：stall、bag、pay、start、result、end_good、end_bad

## 關帝廟 guandi（2026-10-29）
提示詞全部寫在 `docs/image-prompts-guandi.md`（共 16 張，含順序、底圖、檢查重點）。做完一張勾一張，一次做一張，Ben 確認再下一張。
- [ ] guandi：gate、exit、start、fire、heaven、main、throw、draw、cabinet、read、desk、amulet、guolu、result、end_good、end_bad

## 服飾店 clothes（2026-10-29）
提示詞已寫好：`docs/image-prompts-clothes.md`（照順序一次做一張）。圖片檔名：start、rack、fittingroom、mirror、mirror_pants、tag、hem、counter、bag、result、end_good、end_bad（共 12 張，720×720）。主角看不到臉、看不出性別（只拍手和鞋子）；沒有 Ami。
- [ ] clothes：start、rack、fittingroom、mirror、mirror_pants、tag、hem、counter、bag、result、end_good、end_bad

## 飯店 hotel（2026-11-01，P-004 草稿：尚未修改）
提示詞：`docs/image-prompts-hotel.md`（照順序一次做一張，Ben 確認再下一張）。圖片檔名：start、desk、room、phone、housekeeper、checkout、result、end_good、end_bad（共 9 張，720×720）。Ami 用 `games/drinks/images/call.jpg` 的頭肩裁切當角色參考圖。
- [ ] hotel：start、desk、room、phone、housekeeper、checkout、result、end_good、end_bad

## 台鐵 train（2026-11-02，P-005 草稿：尚未修改）
提示詞：`docs/image-prompts-train.md`（照順序一次做一張，Ben 確認再下一張）。圖片檔名：start、counter、ticket、gate、platform、aisle、seat、result、end_good、end_bad（共 10 張，720×720）。Ami 用 `games/drinks/images/call.jpg` 的頭肩裁切當角色參考圖。
- [ ] train：start、counter、ticket、gate、platform、aisle、seat、result、end_good、end_bad

## 高鐵 hsr（2026-11-03，P-006 草稿：尚未修改）
提示詞：`docs/image-prompts-hsr.md`（照順序一次做一張，Ben 確認再下一張）。圖片檔名：start、counter、ticket、gate、signs、platform、spot、seat、result、end_good、end_bad（共 11 張，720×720）。Ami 用 `games/drinks/images/call.jpg` 的頭肩裁切當角色參考圖。
- [ ] hsr：start、counter、ticket、gate、signs、platform、spot、seat、result、end_good、end_bad

## 計程車 taxi（2026-11-04，P-007 草稿：尚未修改）
提示詞：`docs/image-prompts-taxi.md`（照順序一次做一張，Ben 確認再下一張）。圖片檔名：start、hail、inside、belt、meter、arrive、pay、exit、result、end_good、end_bad（共 11 張，720×720）。Ami 用 `games/drinks/images/call.jpg` 的頭肩裁切當角色參考圖。
- [ ] taxi：start、hail、inside、belt、meter、arrive、pay、exit、result、end_good、end_bad

## 藥局 pharmacy（2026-11-05，P-008 草稿：尚未修改）
提示詞：`docs/image-prompts-pharmacy.md`（照順序一次做一張，Ben 確認再下一張）。圖片檔名：start、inside、box、label、counter、result、end_good、end_bad（共 8 張，720×720）。Ami 用 `games/drinks/images/call.jpg` 的頭肩裁切當角色參考圖。
- [ ] pharmacy：start、inside、box、label、counter、result、end_good、end_bad

## 銀行 bank（2026-11-06，P-009 草稿：尚未修改）
提示詞：`docs/image-prompts-bank.md`（照順序一次做一張，Ben 確認再下一張）。圖片檔名：start、lobby、ticket、table、counter、cash、result、end_good、end_bad（共 9 張，720×720）。Ami 用 `games/drinks/images/call.jpg` 的頭肩裁切當角色參考圖。
- [ ] bank：start、lobby、ticket、table、counter、cash、result、end_good、end_bad

## 電信行 telecom（2026-11-07，P-010 草稿：尚未修改）
提示詞：`docs/image-prompts-telecom.md`（照順序一次做一張，Ben 確認再下一張）。圖片檔名：start、shop、counter、plan、pay、sim、nosignal、result、end_good、end_bad（共 10 張，720×720）。Ami 用 `games/drinks/images/call.jpg` 的頭肩裁切當角色參考圖。
- [ ] telecom：start、shop、counter、plan、pay、sim、nosignal、result、end_good、end_bad

## 自助洗衣店 laundry（2026-11-08，P-011 草稿：尚未修改）
提示詞：`docs/image-prompts-laundry.md`（照順序一次做一張，Ben 確認再下一張）。圖片檔名：start、shop、coins、washer、wait、dryer、result、end_good、end_bad（共 9 張，720×720）。Ami 用 `games/drinks/images/call.jpg` 的頭肩裁切當角色參考圖。
- [ ] laundry：start、shop、coins、washer、wait、dryer、result、end_good、end_bad

## 租屋看房 rental（2026-11-09，P-012 草稿：尚未修改）
提示詞：`docs/image-prompts-rental.md`（照順序一次做一張，Ben 確認再下一張）。圖片檔名：start、building、room、meter、table、result、end_good、end_bad（共 8 張，720×720）。Ami 用 `games/drinks/images/call.jpg` 的頭肩裁切當角色參考圖。
- [ ] rental：start、building、room、meter、table、result、end_good、end_bad

## 加油站 gasstation（2026-11-10，P-013 草稿：尚未修改）
提示詞：`docs/image-prompts-gasstation.md`（照順序一次做一張，Ben 確認再下一張）。圖片檔名：arrive、start、order、fill、pay、invoice、leave、result、end_good、end_bad（共 10 張，720×720）。Ami 用 `games/drinks/images/call.jpg` 的頭肩裁切當角色參考圖。
- [ ] gasstation：arrive、start、order、fill、pay、invoice、leave、result、end_good、end_bad

## 租機車 scooterrent（2026-11-11，P-014 草稿：尚未修改）
提示詞：`docs/image-prompts-scooterrent.md`（照順序一次做一張，Ben 確認再下一張）。圖片檔名：arrive、start、license、order、contract、pay、helmet、check、return、result、end_good、end_bad（共 12 張，720×720）。Ami 用 `games/drinks/images/call.jpg` 的頭肩裁切當角色參考圖。
- [ ] scooterrent：arrive、start、license、order、contract、pay、helmet、check、return、result、end_good、end_bad

## 垃圾車倒垃圾 trash（2026-11-12，P-015 草稿：尚未修改）
提示詞：`docs/image-prompts-trash.md`（照順序一次做一張，Ben 確認再下一張）。圖片檔名：start、lobby、home、wait、truck、throw、oil、result、end_good、end_bad（共 10 張，720×720）。Ami 用 `games/drinks/images/call.jpg` 的頭肩裁切當角色參考圖。
- [ ] trash：start、lobby、home、wait、truck、throw、oil、result、end_good、end_bad
