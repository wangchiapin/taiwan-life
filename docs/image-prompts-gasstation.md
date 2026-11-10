# 加油站 gasstation 的圖片清單與提示詞（給 Gemini 用）

2026-11-10 寫好（第一版草稿，尚未修改）。共 10 張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的（畫風、視角、限制都寫在裡面），整段複製貼上就能用。
遊戲程式在 `games/gasstation/index.html`，圖片放 `games/gasstation/images/`，缺圖時自動顯示表情符號（遊戲照樣能玩）。

## 共通規則

- **一次做一張**：做完一張，Ben 確認，再做下一張，照下面順序。
- **畫風**：和飲料店（games/drinks/images）一樣的 16-bit 像素風插畫、暖色調。**不要拿別的地點、別的遊戲的場景圖當參考圖**（生成器會照抄背景）；只有 Ami 用下面的人物參考圖。
- **Ami 長相要固定**：深棕膚色、波浪長黑髮。先到 `games/drinks/images/call.jpg`，**用它的頭肩裁切**（只留 Ami 的頭和肩膀）當角色參考圖上傳，提示詞已寫「只複製這個人物，忽略背景」。不要只用文字描述 Ami。衣服可以不同。
- **劇情真正發生的地點**：開頭（START）是在 Ami 家門口（手上拿著她的機車鑰匙、手機收到 LINE）；中間所有關卡都在同一個加油站（停在加油機旁的機車、加油員、加油機螢幕、櫃檯／收銀處）；結果與結局圖是 Ami 在自己家門口，旁邊停著她的機車。
- **主角沒有性別**：第一人稱，臉和身體不入鏡，只看得到普通的手（沒有戒指、手錶、手環、指甲油，袖子不要露出）。加油員也不露臉（背影、側後方，或鏡頭把臉裁掉），穿制服、戴帽子。
- **沒有可讀的文字**：招牌、價格、加油機螢幕、發票都畫成空白或抽象線條（遊戲用文字卡片顯示油種和金額）。**不要畫出任何油品牌的商標**。
- **同一個遊戲場景要一致**：同一個加油站，用已確認的 `arrive.jpg` 當底圖，寫成編輯式（keep everything identical, change only X）。
- **檔案規格**：2048×2048 原圖縮成 **720×720、JPG、品質約 84**，檔名小寫，照下表。

## 台灣實景核對（Ben 看過覺得不對請直接說）

- 台灣的加油站：有頂棚，下面一排加油機（每台有兩側加油槍），地面是灰色水泥、有黃色停車線；旁邊有小辦公室／櫃檯。機車常直接騎進加油島，停在加油機旁邊，**客人坐在車上、熄火**，由穿制服的加油員幫忙加油（也有自助加油站，這個遊戲採人工加油）。這是依印象畫的，**待確認**。
- 加油員穿深色或亮色制服、戴帽子，可能戴手套；加油機上有數字顯示（畫成空白）。
- 機車是一般的 125cc 速克達（踏板車），顏色不要太鮮豔，不要品牌標誌。

## 圖片清單

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `arrive.jpg` | ARRIVE（機車停在加油機旁，加油員走過來）— 先做這張，之後都以它為底圖 | 無（文字生圖） |
| 2 | `start.jpg` | START（Ami 家門口，手拿機車鑰匙看手機 LINE） | 無（文字生圖，另一個地點，不要上傳 arrive.jpg） |
| 3 | `order.jpg` | ORDER / CONFIRM（對加油員說要加什麼；加油機螢幕在旁邊） | 上傳已確認的 arrive.jpg（編輯式） |
| 4 | `fill.jpg` | FILL（加油員把油槍伸進油箱，加油機數字在跳） | 上傳已確認的 arrive.jpg（編輯式） |
| 5 | `pay.jpg` | PAY / PAY_FIX / CHANGE（付錢、收找的零錢） | 上傳已確認的 arrive.jpg（編輯式） |
| 6 | `invoice.jpg` | INVOICE（加油員遞發票） | 上傳已確認的 pay.jpg（編輯式） |
| 7 | `leave.jpg` | CLOSE（蓋好油箱蓋，準備離開） | 上傳已確認的 arrive.jpg（編輯式） |
| 8 | `result.jpg` | RESULT（Ami 在家門口收到成果訊息） | 無（文字生圖＋Ami 頭肩參考圖） |
| 9 | `end_good.jpg` | END 好結局（Ami 開心） | 上傳已確認的 result.jpg＋Ami 頭肩參考圖 |
| 10 | `end_bad.jpg` | END 壞結局（Ami 擔心） | 上傳已確認的 end_good.jpg（編輯式） |

---

## 1. arrive.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at seated eye height on a scooter (about 1.2 m), looking forward-left at a Taiwan gas station under a flat roof canopy: a gas pump island with one pump directly to the left of the front wheel, grey concrete ground with yellow lines, a small service office with a glass window in the background on the right. A gas station attendant in a plain dark uniform and cap walks toward the viewer from the pump, seen from three-quarter back, face cropped out of the frame. Two plain, ordinary bare hands (no ring, no watch, no bracelet, no nail polish, no sleeve visible) rest on the scooter handlebars at the lower part of the frame. The pump display is a blank dark rectangle. No faces of any person, no readable text, no brand logos anywhere.
```

## 2. start.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), outside the front door of a small Taipei apartment building entrance, daytime. A parked scooter (plain colors, no logo) stands at the lower right. One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a smartphone in the lower middle of the frame; the phone screen shows only abstract blank chat-bubble shapes; the other hand holds a small scooter key on a plain keyring. Soft daylight. No faces of any person, no readable text, no brand logos anywhere.
```

## 3. order.jpg

```
Edit the attached image (the confirmed gas station). Keep the gas station, scooter, colors, 16-bit pixel art style, camera height and viewing direction completely identical. Change only this: the attendant now stands right beside the pump next to the scooter, holding the pump nozzle in a hanging position, turned slightly toward the viewer (cap brim covering the face, no face visible), one gloved hand raised slightly as if listening; the pump's blank display is in clear view at the left. Two plain, ordinary bare hands (no ring, no watch, no bracelet, no nail polish, no sleeve visible) rest on the handlebars. No faces of any person, no readable text, no brand logos anywhere.
```

## 4. fill.jpg

```
Edit the attached image (the confirmed gas station). Keep the gas station, scooter, colors, 16-bit pixel art style, camera height and viewing direction completely identical. Change only this: the scooter's seat is lifted open at the viewer's left side and the attendant (seen from the back, cap, no face) bends over the fuel opening, inserting the pump nozzle; the hose runs back to the pump whose blank display glows. The viewer's two plain, ordinary bare hands (no ring, no watch, no bracelet, no nail polish, no sleeve visible) stay on the handlebars. No faces of any person, no readable text, no brand logos anywhere.
```

## 5. pay.jpg

```
Edit the attached image (the confirmed gas station). Keep the gas station, scooter, colors, 16-bit pixel art style, camera height and viewing direction completely identical. Change only this: the nozzle is back on the pump; the attendant (three-quarter back view, cap, no face) stands beside the scooter and holds out a flat open palm with a few plain coins and small plain banknotes (abstract, no numbers) toward the viewer. One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) is held out at the lower right to receive them; a plain larger banknote lies in the other hand. No faces of any person, no readable text, no brand logos anywhere.
```

## 6. invoice.jpg

```
Edit the attached image (the confirmed payment scene at the gas station). Keep everything identical (gas station, scooter, attendant without a face, colors, 16-bit pixel art style, camera). Change only this: the attendant now holds out a small white paper receipt strip (blank, only abstract grey lines, no readable numbers) between two fingers toward the viewer; one plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) reaches for it. No faces of any person, no readable text, no brand logos anywhere.
```

## 7. leave.jpg

```
Edit the attached image (the confirmed gas station). Keep the gas station, colors, 16-bit pixel art style, camera height and viewing direction completely identical. Change only this: the pump nozzle hangs back on the pump, the attendant is walking away toward the office (back view, cap, no face), the scooter's fuel cap is closed and the seat is down. One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) tucks a small folded white paper receipt (blank) into a pocket at the lower right while the other hand rests on the handlebar. No faces of any person, no readable text, no brand logos anywhere.
```

## 8. result.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image. Copy ONLY the character from the attached reference image (a woman named Ami: dark brown skin, long wavy black hair) and ignore its background. Ami stands at the front door of her own small Taipei apartment, daytime, medium shot from the waist up at eye level, looking down at her smartphone with a calm, curious expression; her scooter is parked beside the door behind her. Plain casual clothes (a simple light T-shirt), no logos. Soft daylight. No readable text anywhere (the phone screen shows only abstract blank shapes), no brand logos.
```

## 9. end_good.jpg

```
Edit the attached image (result.jpg), and use the attached reference image only for Ami's face and hair (dark brown skin, long wavy black hair), ignoring its background. Keep the location, scooter, composition and 16-bit pixel art style identical. Change only this: Ami looks up from her phone with a big happy smile and gives a thumbs-up with one hand. No readable text, no brand logos anywhere.
```

## 10. end_bad.jpg

```
Edit the attached image (end_good.jpg). Keep the location, scooter, composition, Ami's appearance (dark brown skin, long wavy black hair) and the 16-bit pixel art style identical. Change only this: Ami's expression becomes worried and a little disappointed, one hand rests on her cheek, eyebrows slightly raised, the thumbs-up is gone and her other hand holds the phone. No readable text, no brand logos anywhere.
```
