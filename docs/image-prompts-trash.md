# 垃圾車倒垃圾 trash 的圖片清單與提示詞（給 Gemini 用）

2026-11-12 寫好（第一版草稿，尚未修改）。共 10 張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的（畫風、視角、限制都寫在裡面），整段複製貼上就能用。
遊戲程式在 `games/trash/index.html`，圖片放 `games/trash/images/`，缺圖時自動顯示表情符號（遊戲照樣能玩）。

## 共通規則

- **一次做一張**：做完一張，Ben 確認，再做下一張，照下面順序。
- **畫風**：和飲料店（games/drinks/images）一樣的 16-bit 像素風插畫、暖色調。**不要拿別的地點、別的遊戲的場景圖當參考圖**（生成器會照抄背景）；只有 Ami 用下面的人物參考圖。
- **Ami 長相要固定**：深棕膚色、波浪長黑髮。先到 `games/drinks/images/call.jpg`，**用它的頭肩裁切**（只留 Ami 的頭和肩膀）當角色參考圖上傳，提示詞已寫「只複製這個人物，忽略背景」。不要只用文字描述 Ami。衣服可以不同。Ami 只出現在 result、end_good、end_bad（她在自己家客廳）。
- **劇情真正發生的地點**：START 在主角自己的新家客廳（手機收到 LINE）；BOARD、ASK 在公寓一樓大廳（公佈欄、遇到阿姨）；HOME 在主角家廚房；ARRIVE、TRUCK、THROW、ASKOIL、OIL 都在公寓外巷口（傍晚，垃圾車來）；RESULT 與結局是 Ami 在她家客廳。
- **主角沒有性別**：第一人稱，臉和身體不入鏡，只看得到普通的手（沒有戒指、手錶、手環、指甲油，袖子不要露出）。阿姨、清潔隊員等其他人也不露臉（背影或被物品擋住）。
- **沒有可讀的文字**：公告、招牌、垃圾袋、桶子、手機螢幕都畫成空白或抽象線條（遊戲用文字卡片顯示公告內容）。**不要畫出任何品牌商標**。
- **同一個遊戲場景要一致**：巷口用已確認的 `wait.jpg` 當底圖給 `truck.jpg`，`truck.jpg` 再當底圖給 `throw.jpg`、`oil.jpg`；Ami 家用已確認的 `result.jpg` 當底圖給結局圖。每個編輯式提示詞開頭都寫了「Edit the attached image」，上傳底圖時要一起上傳。
- **檔案規格**：2048×2048 原圖縮成 **720×720、JPG、品質約 84**，檔名小寫，照下表。

## 台灣實景核對（Ben 看過覺得不對請直接說）

- 台灣的垃圾車是定時定點來的，居民在車子到之前拿著垃圾下樓等，音樂響起（常見是〈給愛麗絲〉或〈少女的祈禱〉）；後面有清潔隊員收垃圾，旁邊有資源回收車或桶子、廚餘桶。（來源見 docs/draft-games/trash.md「查證來源」）
- 台北市、新北市的一般垃圾要用「專用垃圾袋」（藍色，各縣市顏色與規格不同，**待確認**），所以圖裡用藍色無字的袋子；黑色塑膠袋是「錯誤示範」。
- 資源回收車與桶子的外觀、廚餘桶的樣子各縣市不同，依印象畫，**待確認**。

## 圖片清單

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `start.jpg` | START（主角在新家客廳看 Ami 的 LINE） | 無（文字生圖） |
| 2 | `lobby.jpg` | BOARD / ASK（公寓一樓，公佈欄和鄰居阿姨） | 無（文字生圖） |
| 3 | `home.jpg` | HOME（在家整理要倒的東西） | 無（文字生圖，另一個地點，不要上傳 lobby.jpg） |
| 4 | `wait.jpg` | ARRIVE（傍晚在巷口等垃圾車） | 無（文字生圖，另一個地點，不要上傳前面的圖） |
| 5 | `truck.jpg` | TRUCK（垃圾車停下，隊員在收垃圾） | 上傳已確認的 wait.jpg（編輯式） |
| 6 | `throw.jpg` | THROW（把廚餘倒進廚餘桶、垃圾丟進車） | 上傳已確認的 truck.jpg（編輯式） |
| 7 | `oil.jpg` | ASKOIL / OIL（拿著沾了油的披薩盒，問旁邊的阿姨） | 上傳已確認的 truck.jpg（編輯式） |
| 8 | `result.jpg` | RESULT（Ami 在家收到成果訊息） | 無（文字生圖＋Ami 頭肩參考圖） |
| 9 | `end_good.jpg` | END 好結局（Ami 開心） | 上傳已確認的 result.jpg＋Ami 頭肩參考圖 |
| 10 | `end_bad.jpg` | END 壞結局（Ami 擔心） | 上傳已確認的 end_good.jpg（編輯式） |

---

## 1. start.jpg

用在：START（主角在新家客廳看 Ami 的 LINE）；底圖：無（文字生圖）

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at seated eye height (about 1.2 m) in the living room of a small, newly moved-in Taipei apartment, evening light, looking down at a low coffee table beside a sofa; a few unopened cardboard moving boxes stacked against the wall in the background. One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a smartphone in the lower middle of the frame; the screen shows only abstract blank chat-bubble shapes. A glass of water on the table. No faces of any person, no readable text, no brand logos anywhere. Signs, notices and screens are blank or abstract lines.
```

---

## 2. lobby.jpg

用在：BOARD / ASK（公寓一樓，公佈欄和鄰居阿姨）；底圖：無（文字生圖）

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), inside the small ground-floor lobby of an older Taiwan apartment building, looking straight ahead at a cork notice board on the wall about 2 meters away with a few blank sheets of paper pinned on it (one larger blank sheet in the middle, only abstract gray lines instead of text). To the left, a row of metal mailboxes and the stairwell door; polished stone tile floor, a fluorescent ceiling light. On the right edge of the frame, the back of a middle-aged neighbor in a plain cardigan carrying a plastic grocery bag walks in through the glass door (seen from behind, no face). One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) hangs at the lower right edge of the frame. No faces of any person, no readable text, no brand logos anywhere. Signs, notices and screens are blank or abstract lines.
```

---

## 3. home.jpg

用在：HOME（在家整理要倒的東西）；底圖：無（文字生圖，另一個地點，不要上傳 lobby.jpg）

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.5 m) in the small kitchen of a Taipei apartment, looking down toward the floor beside the counter. On the floor: one plain official-style blue trash bag tied shut (no text or logo), one plain black plastic bag, a rinsed empty plastic bottle, a flattened cardboard box, and a greasy open pizza box (grease stains drawn as dark translucent patches). A small bowl of leftover vegetables on the counter. One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) reaches into the lower right of the frame to pick up the blue bag. Warm evening light from the window. No faces of any person, no readable text, no brand logos anywhere. Signs, notices and screens are blank or abstract lines.
```

---

## 4. wait.jpg

用在：ARRIVE（傍晚在巷口等垃圾車）；底圖：無（文字生圖，另一個地點，不要上傳前面的圖）

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m) at the corner where a quiet Taipei residential alley meets a small street, dusk with the sky turning orange and street lamps just turned on, looking down the alley. A convenience store with a blank glowing sign on the right side (no logo), a few parked scooters, apartment buildings with air-conditioner units. In the distance at the end of the alley, a small garbage truck with its headlights on is approaching (small and far away, no driver visible). A few residents stand along the sidewalk seen only from behind, holding bags. One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a tied blue trash bag at the lower right of the frame. No faces of any person, no readable text, no brand logos anywhere. Signs, notices and screens are blank or abstract lines.
```

---

## 5. truck.jpg

用在：TRUCK（垃圾車停下，隊員在收垃圾）；底圖：上傳已確認的 wait.jpg（編輯式）

```
Edit the attached image (the confirmed alley-corner scene). Keep the buildings, convenience store, scooters, street lamps, colors, 16-bit pixel art style, camera height and viewing direction completely identical. Change only this: the garbage truck is now stopped right in front of the viewer, about 3 meters away, seen from the rear-side, with its rear hopper open; one sanitation worker in a plain high-visibility vest and cap stands beside it, seen from behind or cropped so no face is visible. Next to the truck on the sidewalk stand two plain colored recycling bins. One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) still holds the tied blue trash bag at the lower right. No faces of any person, no readable text, no brand logos anywhere. Signs, notices and screens are blank or abstract lines.
```

---

## 6. throw.jpg

用在：THROW（把廚餘倒進廚餘桶、垃圾丟進車）；底圖：上傳已確認的 truck.jpg（編輯式）

```
Edit the attached image (the confirmed stopped-garbage-truck scene). Keep the alley, buildings, truck, colors, 16-bit pixel art style, camera height and viewing direction completely identical. Change only this: move the camera slightly closer so that a plain food-waste bucket with its lid open (no label, no text) stands at the center beside the truck; One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) tips a small bowl of leftover vegetables into the bucket from the right side of the frame. The tied blue trash bag is held up in the other hand and does not touch the ground. The sanitation worker stays in the background with no face. No faces of any person, no readable text, no brand logos anywhere. Signs, notices and screens are blank or abstract lines.
```

---

## 7. oil.jpg

用在：ASKOIL / OIL（拿著沾了油的披薩盒，問旁邊的阿姨）；底圖：上傳已確認的 truck.jpg（編輯式）

```
Edit the attached image (the confirmed stopped-garbage-truck scene). Keep the alley, buildings, truck, colors, 16-bit pixel art style, camera height and viewing direction completely identical. Change only this: One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a flattened pizza box with obvious dark grease stains at the lower center of the frame; at the right side stands a middle-aged neighbor in a plain cardigan seen from behind, half turned toward the viewer so that no face is visible, holding her own tied bag. The worker stays in the background. No faces of any person, no readable text, no brand logos anywhere. Signs, notices and screens are blank or abstract lines.
```

---

## 8. result.jpg

用在：RESULT（Ami 在家收到成果訊息）；底圖：無（文字生圖＋Ami 頭肩參考圖）

```
Attached is a character reference image: a head-and-shoulders crop of Ami taken from the drinks game (dark brown skin, long wavy black hair). Copy ONLY this person's face, skin tone and hair; ignore its background completely. 16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at seated eye height in Ami's cozy living room, looking at Ami sitting on a sofa holding her smartphone, smiling, seen from the front in a three-quarter view (Ami is a fixed recurring character so her face is shown; she wears a plain light-green hoodie). A small potted plant and a low table with a mug beside her. The phone screen shows only abstract chat bubbles. No other people, no readable text, no brand logos.
```

---

## 9. end_good.jpg

用在：END 好結局（Ami 開心）；底圖：上傳已確認的 result.jpg＋Ami 頭肩參考圖

```
Attached is a character reference image: a head-and-shoulders crop of Ami taken from the drinks game (dark brown skin, long wavy black hair). Copy ONLY this person's face, skin tone and hair; ignore its background completely. Edit the attached image (the confirmed result scene). Keep the living room, sofa, plant, mug, 16-bit pixel art style and camera completely identical, and keep Ami's face, skin tone, long wavy black hair and clothes identical. Change only this: Ami has a big happy smile and raises one hand in a thumbs-up, and the phone screen shows a few abstract sparkle shapes. No readable text, no brand logos.
```

---

## 10. end_bad.jpg

用在：END 壞結局（Ami 擔心）；底圖：上傳已確認的 end_good.jpg（編輯式）

```
Edit the attached image (the confirmed good-ending scene). Keep the living room, sofa, plant, mug, 16-bit pixel art style and camera completely identical, and keep Ami's face, skin tone, long wavy black hair and clothes identical. Change only this: Ami looks worried with a slight frown and one hand on her cheek, looking at the phone; remove the thumbs-up and the sparkles. No readable text, no brand logos.
```
