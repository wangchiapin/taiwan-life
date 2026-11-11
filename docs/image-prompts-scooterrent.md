# 租機車 scooterrent 的圖片清單與提示詞（給 Gemini 用）

2026-11-11 寫好（第一版草稿，尚未修改）。共 12 張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的（畫風、視角、限制都寫在裡面），整段複製貼上就能用。
遊戲程式在 `games/scooterrent/index.html`，圖片放 `games/scooterrent/images/`，缺圖時自動顯示表情符號（遊戲照樣能玩）。

## 共通規則

- **一次做一張**：做完一張，Ben 確認，再做下一張，照下面順序。
- **畫風**：和飲料店（games/drinks/images）一樣的 16-bit 像素風插畫、暖色調。**不要拿別的地點、別的遊戲的場景圖當參考圖**（生成器會照抄背景）；只有 Ami 用下面的人物參考圖。
- **Ami 長相要固定**：深棕膚色、波浪長黑髮。先到 `games/drinks/images/call.jpg`，**用它的頭肩裁切**（只留 Ami 的頭和肩膀）當角色參考圖上傳，提示詞已寫「只複製這個人物，忽略背景」。不要只用文字描述 Ami。衣服可以不同。
- **劇情真正發生的地點**：開頭（START）在主角自己家（客廳，手機收到 Ami 的 LINE）；ARRIVE、LICENSE、ORDER／CONFIRM、INSURE、PAY／CHANGE、HELMET 都在同一間租機車行店內；CHECKBIKE 與 RETURN 在店門口外的人行道（取車、還車都在那裡檢查車子）；RESULT 與結局圖是 Ami 在她家客廳，桌上放著安全帽。
- **主角沒有性別**：第一人稱，臉和身體不入鏡，只看得到普通的手（沒有戒指、手錶、手環、指甲油，袖子不要露出）。店員也不露臉（被螢幕、桌子或鏡頭角度擋住，或背影）。
- **沒有可讀的文字**：招牌、價目表、契約、車況單、手機螢幕都畫成空白或抽象線條（遊戲用文字卡片顯示車種、天數、租金）。**不要畫出任何機車品牌的商標**。
- **同一個遊戲場景要一致**：店內用已確認的 `arrive.jpg` 當底圖，其他店內圖寫成編輯式（keep everything identical, change only X）；門口人行道用已確認的 `check.jpg` 當底圖給 `return.jpg`。
- **檔案規格**：2048×2048 原圖縮成 **720×720、JPG、品質約 84**，檔名小寫，照下表。

## 台灣實景核對（Ben 看過覺得不對請直接說）

- 台灣的機車行：店面小，櫃檯後面常有一兩位店員，牆上掛安全帽，車子停在店門口的人行道或騎樓前；常見的是 125cc 速克達（踏板車）。依印象畫的，**待確認**。
- 取車時店員會拿車況單（畫著車身輪廓）請客人一起把刮痕畫上去，客人用手機拍照存證；這是依消保宣導的建議（取車後立即檢查車況、可拍照存證）。
- 安全帽：開放式或半罩式都有，帶子掛在下面。

## 圖片清單

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `arrive.jpg` | ARRIVE（走進租機車行，店員坐在櫃檯後）— 先做這張，之後店內的圖都以它為底圖 | 無（文字生圖） |
| 2 | `start.jpg` | START（Ami 家裡，主角看手機 LINE） | 無（文字生圖，另一個地點，不要上傳 arrive.jpg） |
| 3 | `license.jpg` | LICENSE（把駕照遞給店員，店員準備影印） | 上傳已確認的 arrive.jpg（編輯式） |
| 4 | `order.jpg` | ORDER / CONFIRM（說要租幾天、哪種車；店員複誦） | 上傳已確認的 arrive.jpg（編輯式） |
| 5 | `contract.jpg` | INSURE（店員把租車契約推過來，要簽名） | 上傳已確認的 order.jpg（編輯式） |
| 6 | `pay.jpg` | PAY / PAY_FIX / CHANGE（付現金、收找的錢） | 上傳已確認的 order.jpg（編輯式） |
| 7 | `helmet.jpg` | HELMET（挑安全帽，看有沒有裂痕、扣帶子） | 上傳已確認的 arrive.jpg（編輯式） |
| 8 | `check.jpg` | CHECKBIKE（取車時檢查刮痕、拍照、畫在車況單上） | 無（文字生圖；店門口外面的人行道） |
| 9 | `return.jpg` | RETURN（還車，店員繞著車子檢查） | 上傳已確認的 check.jpg（編輯式） |
| 10 | `result.jpg` | RESULT（Ami 在家收到成果訊息） | 無（文字生圖＋Ami 頭肩參考圖） |
| 11 | `end_good.jpg` | END 好結局（Ami 開心） | 上傳已確認的 result.jpg＋Ami 頭肩參考圖 |
| 12 | `end_bad.jpg` | END 壞結局（Ami 擔心） | 上傳已確認的 end_good.jpg（編輯式） |

---

## 1. arrive.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), just inside the glass front door of a small Taiwan scooter rental shop, looking straight ahead at a plain wooden service counter about 3 meters away. Behind the counter sits a clerk in a plain polo shirt, seen from the front but with the face cropped by a computer monitor and the top edge of the counter; behind them a wall rack with plain colored helmets on hooks and a blank key board. On the left through the window, two plain scooters (no logos) parked on the sidewalk. Bright daylight, grey tile floor. One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) hangs at the lower right of the frame holding the door handle. No faces of any person, no readable text, no brand logos anywhere. Signs and posters are blank or abstract lines.
```

## 2. start.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at seated eye height (about 1.2 m) in a small Taipei apartment living room, daytime, looking down at a low wooden coffee table beside a sofa. One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a smartphone in the lower middle of the frame; the phone screen shows only abstract blank chat-bubble shapes. On the table a glass of water and a small plant. Soft window light from the left. No faces of any person, no readable text, no brand logos anywhere.
```

## 3. license.jpg

```
Edit the attached image (the confirmed scooter rental shop). Keep the shop, colors, 16-bit pixel art style, camera height and viewing direction completely identical. Change only this: the viewer now stands right at the counter; One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds out a plain blank ID-card-sized card (abstract, no photo, no text) over the counter toward the clerk, whose hand (no face, cropped by the monitor) reaches to take it; a small desktop copier sits on the right end of the counter. No faces of any person, no readable text, no brand logos anywhere.
```

## 4. order.jpg

```
Edit the attached image (the confirmed scooter rental shop). Keep the shop, colors, 16-bit pixel art style, camera height and viewing direction completely identical. Change only this: the viewer stands at the counter; the clerk (face still hidden behind the monitor) holds a blank rental form on a clipboard and a pen, tilting the head slightly as if listening; on the counter lies a blank laminated price card with abstract grey lines and two small plain scooter pictograms. One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) rests on the counter. No faces of any person, no readable text, no brand logos anywhere.
```

## 5. contract.jpg

```
Edit the attached image (the confirmed counter scene). Keep the shop, colors, 16-bit pixel art style, camera height and viewing direction completely identical. Change only this: a two-page paper rental contract (only abstract grey text lines and one blank signature box, no readable words) now lies in the middle of the counter, with a plain pen on it; the clerk's hand pushes it toward the viewer, and One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds the edge of the page. The price card is gone. No faces of any person, no readable text, no brand logos anywhere.
```

## 6. pay.jpg

```
Edit the attached image (the confirmed counter scene). Keep the shop, colors, 16-bit pixel art style, camera height and viewing direction completely identical. Change only this: the clerk's open palm holds a few plain coins and plain banknotes (abstract, no numbers) as change, held out toward the viewer; One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) is held out at the lower right to receive them, and a larger plain banknote lies on the counter. The rental form is on the counter, blank. No faces of any person, no readable text, no brand logos anywhere.
```

## 7. helmet.jpg

```
Edit the attached image (the confirmed scooter rental shop). Keep the shop, colors, 16-bit pixel art style, camera height and viewing direction completely identical. Change only this: the viewer now stands facing the wall helmet rack (the clerk is out of frame). Two plain, ordinary bare hands (no ring, no watch, no bracelet, no nail polish, no sleeve visible) hold a plain open-face helmet up in front of the viewer, turning it to check the shell, with the chin strap hanging down; other plain helmets stay on the hooks. No faces of any person, no readable text, no brand logos anywhere.
```

## 8. check.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at crouching height (about 0.9 m) on a Taiwan sidewalk outside the scooter rental shop, daytime, looking at the left side of a parked plain-colored scooter (no logo) from about 1.5 meters away. A short thin light scratch line is visible on the left body panel. One plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a smartphone toward the scratch as if taking a photo (screen shows only an abstract blank frame); a clerk's hand with a clipboard holding a blank sheet with an abstract car-side outline drawn on it appears at the right edge, the clerk's body cropped out of the frame. No faces of any person, no readable text, no brand logos anywhere.
```

## 9. return.jpg

```
Edit the attached image (the confirmed sidewalk scene). Keep the shop front, sidewalk, the scooter, colors, 16-bit pixel art style and viewing direction identical. Change only this: the viewer now stands upright at eye height (about 1.6 m), and the clerk (seen from behind, plain polo shirt, face not visible) walks around the scooter pointing at its left side with one finger while holding the blank clipboard sheet in the other hand; the scratch line on the left panel is the same thin old one. The viewer's one plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds the phone down at the side. No faces of any person, no readable text, no brand logos anywhere.
```

## 10. result.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image. Copy ONLY the character from the attached reference image (a woman named Ami: dark brown skin, long wavy black hair) and ignore its background. Ami sits on the sofa of her own small Taipei apartment living room, daytime, medium shot from the waist up at eye level, looking down at her smartphone with a calm, curious expression; a plain helmet sits on the coffee table in front of her. Plain casual clothes (a simple light T-shirt), no logos. Soft window light. No readable text anywhere (the phone screen shows only abstract blank shapes), no brand logos.
```

## 11. end_good.jpg

```
Edit the attached image (result.jpg), and use the attached reference image only for Ami's face and hair (dark brown skin, long wavy black hair), ignoring its background. Keep the room, helmet, composition and 16-bit pixel art style identical. Change only this: Ami looks up from her phone with a big happy smile and gives a thumbs-up with one hand. No readable text, no brand logos anywhere.
```

## 12. end_bad.jpg

```
Edit the attached image (end_good.jpg). Keep the room, helmet, composition, Ami's appearance (dark brown skin, long wavy black hair) and the 16-bit pixel art style identical. Change only this: Ami's expression becomes worried and a little disappointed, one hand rests on her cheek, eyebrows slightly raised, the thumbs-up is gone and her other hand holds the phone. No readable text, no brand logos anywhere.
```
