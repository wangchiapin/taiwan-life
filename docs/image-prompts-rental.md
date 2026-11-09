# 租屋看房 rental 的圖片清單與提示詞（給 Gemini 用）

2026-11-09 寫好（第一版草稿，尚未修改）。共 8 張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的（畫風、視角、限制都寫在裡面），整段複製貼上就能用。
遊戲程式在 `games/rental/index.html`，圖片放 `games/rental/images/`，缺圖時自動顯示表情符號（遊戲照樣能玩）。

## 共通規則

- **一次做一張**：做完一張，Ben 確認，再做下一張，照下面順序。
- **畫風**：和飲料店（games/drinks/images）一樣的 16-bit 像素風插畫、暖色調。**不要拿別的遊戲的場景圖當參考圖**（生成器會照抄背景）；只有 Ami 用下面的人物參考圖。
- **Ami 長相要固定**：深棕膚色、波浪長黑髮。先到 `games/drinks/images/call.jpg`，**用它的頭肩裁切**（只留 Ami 的頭和肩膀）當角色參考圖上傳，提示詞已寫「只複製這個人物，忽略背景」。不要只用文字描述 Ami。衣服可以不同。
- **劇情真正發生的地點**：手機聊天是在玩家家裡（桌上筆電／手機看租屋網站）；見房東在老舊大樓一樓門口；看房、問租金、談價都在三樓套房裡；問電費在套房門口的電表旁；談押金、看合約、付錢在大樓一樓管理室旁的小桌；結果／結局圖是 Ami 在自己家門口。
- **主角沒有性別**：第一人稱，臉和身體不入鏡，只看得到普通的手（沒有戒指、手錶、手環、指甲油，袖子不要露出）。房東也不露臉（背影、側後方，或鏡頭把臉裁掉）。
- **沒有可讀的文字**：招牌、價格、螢幕、合約、信箱的字都畫成空白或抽象線條（遊戲用文字卡片顯示金額）。
- **同一個遊戲場景要一致**：同一棟大樓、同一間套房，用已確認的圖當底圖，寫成編輯式（keep everything identical, change only X）。
- **檔案規格**：2048×2048 原圖縮成 **720×720、JPG、品質約 84**，檔名小寫，照下表。

## 台灣實景核對（Ben 看過覺得不對請直接說）

- 台灣常見的出租套房：老舊公寓或大樓的小套房，磁磚地板、白牆，一張單人床、書桌、衣櫃、分離式或窗型冷氣、獨立衛浴（有熱水器）、有的有小洗衣機放陽台。這是依印象畫的，**待確認**。
- 大樓一樓：鐵門、電梯、一排信箱、樓梯間；電表通常在樓梯間或每層的電表箱（有的套房門口外面有電表）。待確認。
- 簽約通常在房間或一樓管理室的桌子，桌上有紙本合約、印章盒、計算機。待確認。

## 圖片清單

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `start.jpg` | START（在家用手機看租屋網站，收到 Ami 的 LINE） | 無（文字生圖，第一張先做） |
| 2 | `building.jpg` | MEET（老舊大樓一樓門口，房東在電梯旁，背影） | 無（文字生圖） |
| 3 | `room.jpg` | LOOK／RENT／NEGO（三樓套房內部：冷氣、書桌、床、洗衣機位置） | 無（文字生圖） |
| 4 | `meter.jpg` | UTIL（套房門口外牆的電表） | 上傳已確認的 room.jpg（編輯式） |
| 5 | `table.jpg` | DEPOSIT／CONTRACT／PAYWAY（一樓小桌，合約、計算機、印章盒） | 上傳已確認的 building.jpg（編輯式） |
| 6 | `result.jpg` | RESULT（Ami 在家門口收到成果訊息） | 無（文字生圖＋Ami 頭肩參考圖） |
| 7 | `end_good.jpg` | END 好結局（Ami 開心） | 上傳已確認的 result.jpg＋Ami 頭肩參考圖 |
| 8 | `end_bad.jpg` | END 壞結局（Ami 擔心） | 上傳已確認的 end_good.jpg（編輯式） |

---

## 1. start.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at seated eye height (about 1.2 m), sitting at a small desk in a Taipei apartment, looking slightly downward at an open laptop whose screen shows only abstract blank listing cards and gray photo rectangles (no readable text). One plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a smartphone at the lower right; the phone screen shows only abstract blank chat bubbles. A mug and a notebook with blank pages on the desk, soft daylight from a window on the left. No faces of any person, no readable text anywhere.
```

## 2. building.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), standing just inside the open metal gate of an older Taiwan apartment building entrance on the ground floor, looking straight ahead at the lobby: a row of mailboxes on the left wall with blank labels, an elevator with closed doors in the center, a staircase on the right, worn light-gray terrazzo floor. A landlord in a plain polo shirt stands next to the elevator, seen from the back or cropped at the chin, no face visible. Daylight from the entrance behind the camera. One plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a smartphone at the lower right. No faces of any person, no readable text anywhere.
```

## 3. room.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), standing just inside the doorway of a small Taiwan studio apartment on the third floor, looking toward the window on the opposite wall. Light tile floor, white walls, a single bed with plain bedding on the left, a wooden desk and chair under the window on the right, a split-type air conditioner mounted high on the left wall, a small bathroom door beside the entrance, and in the right corner an empty washing-machine spot with a visible water connection and no machine. A landlord in a plain polo shirt stands by the bed, seen from the back, no face visible. Bright daylight through the window. One plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a smartphone at the lower right. No faces of any person, no readable text anywhere.
```

## 4. meter.jpg

```
Edit the attached image (the confirmed studio apartment). Keep the building style, colors and 16-bit pixel art style identical. Change only this: the camera now stands in the corridor just outside the studio's front door, at standing eye height (about 1.6 m), looking at the corridor wall next to the door where a small gray electricity meter box with a round window and tiny blank dials is mounted; the studio's open door is visible at the left edge. One plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) points at the meter from the lower right. No faces of any person, no readable text anywhere.
```

## 5. table.jpg

```
Edit the attached image (the confirmed building.jpg). Keep the building lobby style, colors and 16-bit pixel art style identical. Change only this: the camera now sits at a small square wooden table in the corner of the ground-floor lobby, at seated eye height (about 1.2 m), looking across the table at a landlord in a plain polo shirt seen from the front but cropped at the chin, no face visible. On the table: a stack of blank paper contract pages (abstract lines only), a pen, a desk calculator with a blank display, and a small red stamp-pad box. One plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a pen over the paper at the lower right. No faces of any person, no readable text anywhere.
```

## 6. result.jpg

```
Use the attached reference image ONLY for the character: copy only this person (the woman with dark brown skin and long wavy black hair), ignore its background completely. 16-bit pixel art illustration, warm muted colors, square 1:1 image. Camera at eye level, facing the character from the front, medium shot from the waist up. She stands in the doorway of her apartment in Taipei, wearing a plain teal cardigan over a white top, holding her smartphone in one hand and reading it with a calm, pleased expression. Behind her: a tidy entryway with a shoe cabinet and shoes, warm afternoon light. The phone screen shows only abstract blank chat bubbles. No readable text anywhere.
```

## 7. end_good.jpg

```
Use the attached reference image ONLY for the character: copy only this person (the woman with dark brown skin and long wavy black hair), ignore its background completely. Same doorway scene, camera angle and 16-bit pixel art style as the confirmed result.jpg. Change only this: she smiles warmly and gives a thumbs-up with her free hand while holding the phone with the other; a small ordinary door key hangs on a plain ring from her phone hand's fingers. Keep everything else identical. No readable text.
```

## 8. end_bad.jpg

```
Edit the attached image (the confirmed end_good.jpg). Keep the doorway scene, camera angle, outfit, 16-bit pixel art style and the character's appearance (dark brown skin, long wavy black hair) completely identical. Change only her expression and pose: she looks worried, brows slightly raised, the phone held down at her chest, the other hand resting on her cheek; remove the key. No readable text.
```
