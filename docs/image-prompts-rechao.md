# 熱炒店 rechao 的圖片清單與提示詞（給 Gemini 用）

2026-11-13 寫好（第一版草稿，尚未修改）。共 9 張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的（畫風、視角、限制都寫在裡面），整段複製貼上就能用。
遊戲程式在 `games/rechao/index.html`，圖片放 `games/rechao/images/`，缺圖時自動顯示表情符號（遊戲照樣能玩）。

## 共通規則

- **一次做一張**：做完一張，Ben 確認，再做下一張，照下面順序。
- **畫風**：和飲料店（games/drinks/images）一樣的 16-bit 像素風插畫、暖色調。**不要拿別的地點、別的遊戲的場景圖當參考圖**（生成器會照抄背景）；只有 Ami 用下面的人物參考圖。
- **Ami 長相要固定**：深棕膚色、波浪長黑髮。先到 `games/drinks/images/call.jpg`，**用它的頭肩裁切**（只留 Ami 的頭和肩膀）當角色參考圖上傳，提示詞已寫「只複製這個人物，忽略背景」。不要只用文字描述 Ami。衣服可以不同。
- **劇情真正發生的地點**：開頭（START）是在熱炒店門口外面（晚上，手機收到 Ami 的 LINE）；中間所有關卡都在同一間熱炒店裡（入口、桌子、菜單、菜、啤酒、櫃檯）；結果與結局圖是 Ami 到了以後，坐在熱炒店的桌子旁看手機。
- **主角沒有性別**：第一人稱，臉和身體不入鏡，只看得到普通的手（沒有戒指、手錶、手環、指甲油，袖子不要露出）。老闆娘和店裡其他客人也不露臉（背影、遠景，或鏡頭把臉裁掉）。
- **沒有可讀的文字**：招牌、菜單、帳單、牆上的菜單板都畫成空白或抽象線條（遊戲用文字卡片顯示菜名和價錢）。**不要畫出任何啤酒品牌的商標**，酒瓶用素色。
- **同一個遊戲場景要一致**：同一間熱炒店，用已確認的 `entrance.jpg` 當底圖，寫成編輯式（keep everything identical, change only X）。
- **檔案規格**：2048×2048 原圖縮成 **720×720、JPG、品質約 84**，檔名小寫，照下表。

## 台灣實景核對（Ben 看過覺得不對請直接說）

- 台灣的熱炒店：開放式的店面，日光燈很亮，鐵製或木頭的圓桌／方桌，塑膠圓凳或椅子；店裡有冰箱放啤酒，桌邊常有一箱箱的啤酒瓶；背景有炒菜的火光（廚房在店面一側）。招牌常是紅底或黃底。這是依印象畫的，**待確認**。
- 菜是一盤一盤端上桌，放在桌子中間；啤酒是玻璃瓶（綠或棕色），配小玻璃杯。
- 結帳在櫃檯，櫃檯上有計算機、一疊單子；老闆娘在櫃檯後面或走動。

## 圖片清單

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `entrance.jpg` | SEAT（走進熱炒店，老闆娘走過來）— 先做這張，之後店內都以它為底圖 | 無（文字生圖） |
| 2 | `start.jpg` | START（熱炒店門口外面，手拿手機看 Ami 的 LINE） | 無（文字生圖，另一個地點，不要上傳 entrance.jpg） |
| 3 | `menu.jpg` | ORDER / BEER / CONFIRM（桌上的菜單，手拿筆，老闆娘在旁邊） | 上傳已確認的 entrance.jpg（編輯式） |
| 4 | `dish.jpg` | SERVE（老闆娘端一盤菜上桌） | 上傳已確認的 entrance.jpg（編輯式） |
| 5 | `table.jpg` | ADD / RETURN（桌上有空酒瓶和一瓶沒開的酒） | 上傳已確認的 dish.jpg（編輯式） |
| 6 | `bill.jpg` | PAY / PAY_FIX / CHANGE（櫃檯結帳，遞鈔票、收零錢） | 上傳已確認的 entrance.jpg（編輯式） |
| 7 | `result.jpg` | RESULT（Ami 到了，坐在桌邊看手機） | 無（文字生圖＋Ami 頭肩參考圖） |
| 8 | `end_good.jpg` | END 好結局（Ami 開心） | 上傳已確認的 result.jpg＋Ami 頭肩參考圖 |
| 9 | `end_bad.jpg` | END 壞結局（Ami 擔心） | 上傳已確認的 end_good.jpg（編輯式） |

---

## 1. entrance.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), just inside the open front of a lively Taiwanese stir-fry restaurant (rechao shop) at night, looking straight ahead into the shop: bright fluorescent lights, round and square tables with red plastic stools, groups of diners seen only from far away or from behind, crates of plain green beer bottles beside some tables, a glowing open kitchen with flames on the right side, a plain counter with a cash register at the back left. A woman owner in an apron walks toward the viewer, seen from three-quarter front but her face cropped out of the frame (only her apron and arms visible). Signs and the wall menu board are blank colored rectangles. No faces of any person, no readable text, no brand logos anywhere.
```

## 2. start.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), on a Taipei street at night right outside the entrance of a stir-fry restaurant: the bright open shop front with tables and blurred diners far inside (no faces), a plain red blank signboard above, scooters parked along the curb at the lower left. One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a smartphone in the lower middle of the frame; the phone screen shows only abstract blank chat-bubble shapes. Warm light spilling from the shop. No faces of any person, no readable text, no brand logos anywhere.
```

## 3. menu.jpg

```
Edit the attached image (the confirmed stir-fry restaurant). Keep the restaurant, colors, 16-bit pixel art style, camera height and lighting completely identical. Change only this: the camera is now seated at a round table near the front; on the table in front of the viewer lies a paper menu sheet with blank colored lines (no readable text) and a plain pen; two plain, ordinary bare hands (no ring, no watch, no bracelet, no nail polish, no sleeve visible) rest on the table, one holding the pen. The woman owner stands beside the table in her apron, her face cropped out of the frame, holding a small blank notepad. No faces of any person, no readable text, no brand logos anywhere.
```

## 4. dish.jpg

```
Edit the attached image (the confirmed stir-fry restaurant). Keep the restaurant, colors, 16-bit pixel art style, camera height and lighting completely identical. Change only this: the camera is now seated at a round table; the woman owner in her apron (face cropped out of the frame, only arms and apron visible) is setting a steaming plate of stir-fried food in the middle of the table, with two empty small plates, chopsticks and a few small beer glasses around it. Two plain, ordinary bare hands (no ring, no watch, no bracelet, no nail polish, no sleeve visible) rest on the table edge. No faces of any person, no readable text, no brand logos anywhere.
```

## 5. table.jpg

```
Edit the attached image (the confirmed dish-on-table scene). Keep the restaurant, table, colors, 16-bit pixel art style, camera height and lighting completely identical. Change only this: the table now holds several plates with only leftovers, and a group of plain empty green glass beer bottles stands on the table, with one single full unopened plain green bottle (cap still on) standing apart on the right; the woman owner is no longer in the frame. Two plain, ordinary bare hands (no ring, no watch, no bracelet, no nail polish, no sleeve visible) rest on the table edge. No faces of any person, no readable text, no brand logos anywhere.
```

## 6. bill.jpg

```
Edit the attached image (the confirmed stir-fry restaurant entrance). Keep the restaurant, colors, 16-bit pixel art style, camera height and lighting completely identical. Change only this: the camera now stands at the plain counter at the back of the shop; the woman owner in her apron (face cropped out of the frame) holds a small white paper bill (blank, only abstract grey lines, no readable numbers) in one hand and a calculator on the counter; one plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) is held out at the lower right with a few plain banknotes (abstract, no numbers) and a few plain coins lie on the counter. No faces of any person, no readable text, no brand logos anywhere.
```

## 7. result.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image. Copy ONLY the character from the attached reference image (a woman named Ami: dark brown skin, long wavy black hair) and ignore its background. Ami sits at a round table in a lively Taiwanese stir-fry restaurant at night, medium shot from the waist up at eye level, looking down at her smartphone with a calm, curious expression; on the table are a few plates and plain green beer bottles, and far in the background blurred diners seen from behind (no faces). Plain casual clothes (a simple light T-shirt), no logos. No readable text anywhere (the phone screen shows only abstract blank shapes), no brand logos.
```

## 8. end_good.jpg

```
Edit the attached image (result.jpg), and use the attached reference image only for Ami's face and hair (dark brown skin, long wavy black hair), ignoring its background. Keep the location, table, composition and 16-bit pixel art style identical. Change only this: Ami looks up from her phone with a big happy smile and gives a thumbs-up with one hand. No readable text, no brand logos anywhere.
```

## 9. end_bad.jpg

```
Edit the attached image (end_good.jpg). Keep the location, table, composition, Ami's appearance (dark brown skin, long wavy black hair) and the 16-bit pixel art style identical. Change only this: Ami's expression becomes worried and a little disappointed, one hand rests on her cheek, eyebrows slightly raised, the thumbs-up is gone and her other hand holds the phone. No readable text, no brand logos anywhere.
```
