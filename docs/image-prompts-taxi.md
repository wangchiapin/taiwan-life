# 計程車 taxi 的圖片清單與提示詞（給 Gemini 用）

2026-11-04 寫好（第一版草稿，尚未修改）。共 11 張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的（畫風、視角、限制都寫在裡面），整段複製貼上就能用。
遊戲程式在 `games/taxi/index.html`，圖片放 `games/taxi/images/`，缺圖時自動顯示表情符號（遊戲照樣能玩）。

## 共通規則

- **一次做一張**：做完一張，Ben 確認，再做下一張，照下面順序。
- **畫風**：和飲料店（games/drinks/images）一樣的 16-bit 像素風插畫、暖色調。**不要拿別的遊戲的場景圖當參考圖**（生成器會照抄背景）；只有 Ami 用下面的人物參考圖。
- **Ami 長相要固定**：深棕膚色、波浪長黑髮。先到 `games/drinks/images/call.jpg`，**用它的頭肩裁切**（只留 Ami 的頭和肩膀）當角色參考圖上傳，提示詞已寫「只複製這個人物，忽略背景」。不要只用文字描述 Ami。衣服可以不同。
- **劇情真正發生的地點**：手機聊天是在台北街頭的人行道（主角站在路邊收到 LINE）；招車在路邊；之後都在計程車後座（司機只拍背影）；結果／結局圖是 Ami 在目的地門口（台北的大型景點入口，不寫字）。
- **主角沒有性別**：第一人稱，臉和身體不入鏡，只看得到普通的手（沒有戒指、手錶、手環、指甲油，袖子不要露出）。司機、乘客、騎士也不露臉（背影、剪影、遠景）。
- **沒有可讀的文字**：招牌、計費表數字、車牌、螢幕都畫成空白或抽象線條（遊戲用文字卡片顯示車資）。
- **同一個遊戲場景要一致**：同一輛計程車後座，用已確認的 `inside.jpg` 當底圖，寫成編輯式（keep everything identical, change only X）。
- **檔案規格**：2048×2048 原圖縮成 **720×720、JPG、品質約 84**，檔名小寫，照下表。

## 台灣實景核對（Ben 看過覺得不對請直接說）

- 台灣計程車是黃色車身（也有其他顏色的，這裡統一用黃色）；司機座旁的儀表板上有計費表；空車時擋風玻璃下有紅色的「空車」燈。這是依印象畫的，**待確認**。
- 乘客坐後座，後座有安全帶；招車是站在路邊伸手招手。
- 路上有很多機車，下車開門要注意後面來的機車。

## 圖片清單

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `start.jpg` | START（站在台北街頭人行道，手機收到 Ami 的 LINE） | 無（文字生圖，第一張先做） |
| 2 | `hail.jpg` | HAIL（站在路邊，看哪台計程車有亮「空車」燈） | 無（文字生圖） |
| 3 | `inside.jpg` | TELL / DEST_CHECK（坐進後座，和司機說話） | 無（文字生圖） |
| 4 | `belt.jpg` | BELT（後座的安全帶） | 上傳已確認的 inside.jpg（編輯式） |
| 5 | `meter.jpg` | METER（前面的計費表） | 上傳已確認的 inside.jpg（編輯式） |
| 6 | `arrive.jpg` | STOP（快到了，路口右邊 Ami 在揮手） | 上傳已確認的 inside.jpg（編輯式） |
| 7 | `pay.jpg` | PAY / PAY_FIX / CHANGE（付錢、找錢） | 上傳已確認的 inside.jpg（編輯式） |
| 8 | `exit.jpg` | EXIT（下車前回頭看後面，後面有機車） | 上傳已確認的 inside.jpg（編輯式） |
| 9 | `result.jpg` | RESULT（Ami 在目的地門口等你，看手機收到成果） | 無（文字生圖＋Ami 頭肩參考圖） |
| 10 | `end_good.jpg` | END 好結局（Ami 開心） | 上傳已確認的 result.jpg＋Ami 頭肩參考圖 |
| 11 | `end_bad.jpg` | END 壞結局（Ami 擔心） | 上傳已確認的 end_good.jpg（編輯式） |

---

## 1. start.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), facing along a busy Taipei city sidewalk, slightly looking down at the phone. A pair of plain, ordinary bare hands (no ring, no watch, no bracelet, no nail polish, no sleeves visible) holds a smartphone in the lower part of the frame; the phone screen shows only abstract blank chat-bubble shapes. Far ahead: a road with a few cars and yellow taxis, shop awnings with blank signs, scooters parked at the curb, a few pedestrians seen from behind and far away. No faces of any person, no readable text anywhere.
```

## 2. hail.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), standing on the sidewalk at the curb and facing the road, looking slightly to the left at yellow Taiwan taxis driving toward the viewer. The nearest taxi has a small red lit panel under its windshield (abstract red rectangle, no characters) meaning it is vacant; the next one has no light and a passenger silhouette inside. One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) is raised at the right edge of the frame, waving toward the road. The drivers and passengers are only dark silhouettes behind tinted glass. No faces of any person, no readable text anywhere.
```

## 3. inside.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera seated in the back seat of a yellow Taiwan taxi, at seated eye height (about 1.2 m), centered behind the front seats, looking straight forward through the windshield at a city street. The driver is seen only from behind (back of the head and shoulders, plain shirt, no face), the dashboard has a small taxi meter box with a dark blank display, a plain rear-view mirror with no reflection of any face. One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) rests on the back-seat cushion at the lower edge. No faces of any person, no readable text anywhere.
```

## 4. belt.jpg

```
Edit the attached image (the confirmed taxi back seat). Keep the taxi interior, the driver seen from behind, colors, 16-bit pixel art style and camera position completely identical. Change only this: look slightly to the right and down so that the back-seat seat belt fills the right half of the frame, with one plain bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) pulling the belt across toward the buckle. No faces, no readable text.
```

## 5. meter.jpg

```
Edit the attached image (the confirmed taxi back seat). Keep the taxi interior, the driver seen from behind (no face), colors, 16-bit pixel art style and camera height completely identical. Change only this: move the camera slightly forward and zoom in on the taxi meter on the dashboard so it takes up the center of the frame; its display is a dark rectangle with only abstract blank red segment shapes (no digits, no letters). The city street is blurred through the windshield. No hands, no faces, no readable text.
```

## 6. arrive.jpg

```
Edit the attached image (the confirmed taxi back seat). Keep the taxi interior, the driver seen from behind (no face), colors, 16-bit pixel art style and camera position completely identical. Change only what is seen through the windshield: a street corner on the right with a small, distant figure waving (tiny, no facial details, long wavy black hair, dark brown skin), a blank-signed building behind her. No readable text.
```

## 7. pay.jpg

```
Edit the attached image (the confirmed taxi back seat). Keep the taxi interior, colors, 16-bit pixel art style and camera position completely identical. Change only this: the driver (seen from behind, no face) holds out one hand toward the back seat with a few abstract paper bills and coins (blank, no numbers); in the lower foreground one plain bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a banknote. No faces, no readable text.
```

## 8. exit.jpg

```
Edit the attached image (the confirmed taxi back seat). Keep the taxi interior, colors, 16-bit pixel art style and the seat height completely identical. Change only this: the camera now looks sideways over the shoulder through the rear window at a scooter approaching slowly on the roadside (rider seen only as a dark silhouette, no face), while one plain bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) rests on the inside door handle at the lower edge. No readable text.
```

## 9. result.jpg

```
Use the attached reference image ONLY for the character: copy only this person (the woman with dark brown skin and long wavy black hair), ignore its background completely. 16-bit pixel art illustration, warm muted colors, square 1:1 image. Camera at eye level, facing the character from the front, medium shot from the waist up. The character stands on the sidewalk at the entrance of a large Taipei landmark building on a sunny afternoon, looking at her smartphone with a happy, curious expression; she wears a different outfit from the reference (a plain light-blue jacket over a white top) and a small shoulder bag. Behind her: a wide building entrance with a blank sign with no letters, a yellow taxi pulling away at the curb, a few trees. The phone screen shows only abstract blank chat bubbles. No readable text anywhere.
```

## 10. end_good.jpg

```
Use the attached reference image ONLY for the character: copy only this person (the woman with dark brown skin and long wavy black hair), ignore its background completely. Same entrance scene, camera angle and 16-bit pixel art style as the confirmed result.jpg. Change only this: she smiles broadly, holds her phone up to the camera with one hand and waves with the other. Keep everything else identical. No readable text.
```

## 11. end_bad.jpg

```
Edit the attached image (the confirmed end_good.jpg). Keep the entrance scene, camera angle, outfit, 16-bit pixel art style and the character's appearance (dark brown skin, long wavy black hair) completely identical. Change only her expression and pose: she looks worried, brows slightly raised, one hand holding the phone down at her chest, the other hand resting on her cheek. No readable text.
```
