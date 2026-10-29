# 服飾店 clothes 的圖片清單與提示詞（給 Gemini 用）

2026-10-29 寫好。共 12 張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的（畫風、視角、限制都寫在裡面），整段複製貼上就能用。
遊戲程式在 `games/clothes/index.html`，圖片放 `games/clothes/images/`，缺圖時自動顯示表情符號（遊戲照樣能玩）。

## 共通規則

- **一次做一張**：做完一張，Ben 確認，再做下一張，照下面順序。
- **底圖規則**：寫著「上傳已確認的 xxx.jpg（編輯式）」的，把那張圖一起上傳再貼提示詞；只拿同一個遊戲的圖當底圖，不要拿別的遊戲的圖。
- **這個遊戲沒有 Ami、沒有 LINE**：玩家自己去買衣服，圖裡不要畫 Ami 或手機訊息。
- **主角沒有性別**：第一人稱，臉和身體不入鏡，只看得到普通的手（沒有戒指、手錶、手環、指甲油、袖子）或鞋子。店員也不露臉（背影、剪影、或在脖子處切掉）。
- **沒有可讀的文字**：招牌、吊牌、價錢、螢幕都畫成空白或抽象線條（遊戲用文字卡片顯示內容）。
- **檔案規格**：2048×2048 原圖縮成 **720×720、JPG、品質約 84**，檔名照下表。

## 台灣實景核對（Ben 看過覺得不對請直接說）

- 台灣服飾店常在騎樓下，玻璃門＋櫥窗，櫥窗裡放無頭人台；店內日光燈加暖色燈，木紋地板。
- 試衣間是一排小隔間（木百葉門或布簾），門口店員會給**號碼牌**（依拿進去的件數）。
- 衣服掛著小**吊牌**（尺寸、價錢）；襯衫常用 S／M／L／XL，長褲用腰圍（英寸，例如三十腰）。
- 收銀台有收銀機、發票機、零錢盤；袋子是紙袋或塑膠提袋。
- 改褲管：店員用軟尺量、用別針固定，店裡常有縫紉機，等約三十分鐘。

## 圖片清單

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `start.jpg` | START（站在服飾店門口，想買新衣服） | 無（文字生圖，第一張先做） |
| 2 | `rack.jpg` | SIZE（在衣架前找尺寸） | 無（文字生圖） |
| 3 | `fittingroom.jpg` | ROOM_TAG（試衣間門口，店員給號碼牌） | 無（文字生圖） |
| 4 | `mirror.jpg` | FIT_SHIRT / FIT_WAIST（在試衣間照鏡子，試穿襯衫與腰） | 無（文字生圖） |
| 5 | `mirror_pants.jpg` | FIT_LENGTH（照鏡子看褲長） | 上傳已確認的 mirror.jpg（編輯式） |
| 6 | `tag.jpg` | SHIRT_SWAP（店員拿來另一個尺寸，看吊牌） | 無（文字生圖） |
| 7 | `hem.jpg` | HEM（站著讓店員量褲長、別別針） | 無（文字生圖） |
| 8 | `counter.jpg` | PAY / PAY_FIX / CHANGE（櫃台結帳） | 無（文字生圖） |
| 9 | `bag.jpg` | PICKUP（拿到袋子，確認改好的褲子） | 無（文字生圖） |
| 10 | `result.jpg` | RESULT（結算畫面） | 無（文字生圖） |
| 11 | `end_good.jpg` | END 好結局（買好衣服，開心走出店） | 無（文字生圖） |
| 12 | `end_bad.jpg` | END 壞結局（買錯東西，垂頭走出店） | 上傳已確認的 end_good.jpg（編輯式） |

---

## 1. `start.jpg` — START（站在服飾店門口，想買新衣服）

底圖：無（文字生圖，第一張先做）

```
Warm-toned 16-bit pixel art illustration, square 1:1 composition, soft cozy lighting, clean readable shapes. First-person point of view: the protagonist's face and body are NOT visible; if hands appear they are plain bare hands (no rings, no watch, no bracelet, no nail polish, no sleeves visible), gender-neutral. No people's faces anywhere (any other person is only a back view, a silhouette, or cropped at the neck). No readable text anywhere: all signs, price tags, labels and screens are blank or abstract lines. Camera: eye level, standing on the sidewalk about two meters in front of a small Taiwanese clothing shop, looking straight at the entrance. The shop has a glass front door and a big display window with two mannequins (headless torsos) wearing a plain shirt and plain trousers; a blank rectangular signboard above the door; a few hanging blank sale banners (red, no text). Sidewalk with an arcade overhang typical of Taiwan, a scooter parked at the curb. The protagonist's two plain bare hands are visible at the bottom edge, one holding a small folded paper shopping bag handle, relaxed. Mood: about to go in and buy new clothes.
```

檢查點：視角對、沒有臉、沒有可讀文字、手是普通的手。

## 2. `rack.jpg` — SIZE（在衣架前找尺寸）

底圖：無（文字生圖）

```
Warm-toned 16-bit pixel art illustration, square 1:1 composition, soft cozy lighting, clean readable shapes. First-person point of view: the protagonist's face and body are NOT visible; if hands appear they are plain bare hands (no rings, no watch, no bracelet, no nail polish, no sleeves visible), gender-neutral. No people's faces anywhere (any other person is only a back view, a silhouette, or cropped at the neck). No readable text anywhere: all signs, price tags, labels and screens are blank or abstract lines. Camera: eye level, standing in front of a long clothing rack inside a Taiwanese clothing shop, close view. Rows of folded shirts on a shelf (white, blue, light gray) on the left, and a hanging rack of trousers (dark gray, khaki, black) on the right. Each garment has a small blank paper hang tag. One plain bare hand reaches in from the bottom right, lifting a hang tag to look at it (tag blank, no numbers). Bright fluorescent-plus-warm lighting, light wood floor, a sale poster on the wall (blank red shapes, no text). Quiet shop, no customers visible.
```

檢查點：視角對、沒有臉、沒有可讀文字、手是普通的手。

## 3. `fittingroom.jpg` — ROOM_TAG（試衣間門口，店員給號碼牌）

底圖：無（文字生圖）

```
Warm-toned 16-bit pixel art illustration, square 1:1 composition, soft cozy lighting, clean readable shapes. First-person point of view: the protagonist's face and body are NOT visible; if hands appear they are plain bare hands (no rings, no watch, no bracelet, no nail polish, no sleeves visible), gender-neutral. No people's faces anywhere (any other person is only a back view, a silhouette, or cropped at the neck). No readable text anywhere: all signs, price tags, labels and screens are blank or abstract lines. Camera: eye level, standing in front of a row of fitting rooms at the back of a Taiwanese clothing shop. Three narrow cubicles with light wooden louvered doors and a curtain-free frame; one door slightly open showing a mirror inside. A clerk's arm in a plain dark apron, cropped at the shoulder (no face), holds out a small plastic number tag toward the viewer; the tag shows only abstract dots, no digits. At the bottom, the protagonist's plain bare hands hold a folded shirt and a pair of trousers on a hanger. A small blank sign above the cubicles.
```

檢查點：視角對、沒有臉、沒有可讀文字、手是普通的手。

## 4. `mirror.jpg` — FIT_SHIRT / FIT_WAIST（在試衣間照鏡子，試穿襯衫與腰）

底圖：無（文字生圖）

```
Warm-toned 16-bit pixel art illustration, square 1:1 composition, soft cozy lighting, clean readable shapes. First-person point of view: the protagonist's face and body are NOT visible; if hands appear they are plain bare hands (no rings, no watch, no bracelet, no nail polish, no sleeves visible), gender-neutral. No people's faces anywhere (any other person is only a back view, a silhouette, or cropped at the neck). No readable text anywhere: all signs, price tags, labels and screens are blank or abstract lines. Camera: eye level inside a small fitting room, looking into a full-length mirror on the wall. The mirror reflection shows only a torso from the neck down (face cropped out of the frame) wearing a new button-up shirt, buttons done up, and trousers; the person is gender-neutral, plain build. Plain bare hands rest at the sides, one hand pinching the loose waistband slightly. Small hook on the wall with a hanger, a stool in the corner, warm ceiling light, wooden panel walls.
```

檢查點：視角對、沒有臉、沒有可讀文字、手是普通的手。

## 5. `mirror_pants.jpg` — FIT_LENGTH（照鏡子看褲長）

底圖：上傳已確認的 mirror.jpg（編輯式）

```
Warm-toned 16-bit pixel art illustration, square 1:1 composition, soft cozy lighting, clean readable shapes. First-person point of view: the protagonist's face and body are NOT visible; if hands appear they are plain bare hands (no rings, no watch, no bracelet, no nail polish, no sleeves visible), gender-neutral. No people's faces anywhere (any other person is only a back view, a silhouette, or cropped at the neck). No readable text anywhere: all signs, price tags, labels and screens are blank or abstract lines. Edit the uploaded image: keep the fitting room, mirror, lighting and pixel-art style exactly the same. Change the camera to look slightly downward at the mirror's lower half and the floor: the reflected trousers now reach down and bunch up over the top of the shoes, the cuffs resting on the floor. A pair of plain sneakers is visible, and the trouser hems are slightly too long and folding. No face, no readable text. Plain bare hands optional and not required.
```

檢查點：視角對、沒有臉、沒有可讀文字、手是普通的手。 其餘部分要和底圖一致。

## 6. `tag.jpg` — SHIRT_SWAP（店員拿來另一個尺寸，看吊牌）

底圖：無（文字生圖）

```
Warm-toned 16-bit pixel art illustration, square 1:1 composition, soft cozy lighting, clean readable shapes. First-person point of view: the protagonist's face and body are NOT visible; if hands appear they are plain bare hands (no rings, no watch, no bracelet, no nail polish, no sleeves visible), gender-neutral. No people's faces anywhere (any other person is only a back view, a silhouette, or cropped at the neck). No readable text anywhere: all signs, price tags, labels and screens are blank or abstract lines. Camera: close-up, looking down at the protagonist's plain bare hands holding a new shirt by its collar so a small blank paper hang tag dangles in front of the camera; the tag has only a few abstract lines and a barcode-like stripe, no digits or letters. In the soft blurred background a clerk's torso in a dark apron is walking away between clothing racks (back view, no face). Fitting room doors blurred behind.
```

檢查點：視角對、沒有臉、沒有可讀文字、手是普通的手。

## 7. `hem.jpg` — HEM（站著讓店員量褲長、別別針）

底圖：無（文字生圖）

```
Warm-toned 16-bit pixel art illustration, square 1:1 composition, soft cozy lighting, clean readable shapes. First-person point of view: the protagonist's face and body are NOT visible; if hands appear they are plain bare hands (no rings, no watch, no bracelet, no nail polish, no sleeves visible), gender-neutral. No people's faces anywhere (any other person is only a back view, a silhouette, or cropped at the neck). No readable text anywhere: all signs, price tags, labels and screens are blank or abstract lines. Camera: eye level, slightly below, looking down at the lower legs in a fitting-room corner. The protagonist stands straight in the new trousers and plain sneakers (only the lower legs and shoes visible). A clerk crouches beside them in a dark apron, seen only from the shoulders down and cropped at the neck (no face), holding a yellow tape measure at the trouser hem and a few pins; one pin is already in the folded cuff. A small pincushion on the floor. Soft warm light, wooden floor.
```

檢查點：視角對、沒有臉、沒有可讀文字、手是普通的手。

## 8. `counter.jpg` — PAY / PAY_FIX / CHANGE（櫃台結帳）

底圖：無（文字生圖）

```
Warm-toned 16-bit pixel art illustration, square 1:1 composition, soft cozy lighting, clean readable shapes. First-person point of view: the protagonist's face and body are NOT visible; if hands appear they are plain bare hands (no rings, no watch, no bracelet, no nail polish, no sleeves visible), gender-neutral. No people's faces anywhere (any other person is only a back view, a silhouette, or cropped at the neck). No readable text anywhere: all signs, price tags, labels and screens are blank or abstract lines. Camera: eye level, standing at the checkout counter of a Taiwanese clothing shop, facing the counter. On the counter: a folded shirt and trousers, a small cash register with a blank screen (abstract lines only), a small tray with coins and a few banknotes (blank, plain colored), a receipt printer with a blank receipt. The clerk is a torso in a dark apron seen from the chest down, cropped at the neck, hands tapping the register. At the bottom, the protagonist's plain bare hands hold out a banknote. Hanging blank sale banner behind the counter.
```

檢查點：視角對、沒有臉、沒有可讀文字、手是普通的手。

## 9. `bag.jpg` — PICKUP（拿到袋子，確認改好的褲子）

底圖：無（文字生圖）

```
Warm-toned 16-bit pixel art illustration, square 1:1 composition, soft cozy lighting, clean readable shapes. First-person point of view: the protagonist's face and body are NOT visible; if hands appear they are plain bare hands (no rings, no watch, no bracelet, no nail polish, no sleeves visible), gender-neutral. No people's faces anywhere (any other person is only a back view, a silhouette, or cropped at the neck). No readable text anywhere: all signs, price tags, labels and screens are blank or abstract lines. Camera: close view from above at a slight angle, on the counter. A paper shopping bag with rope handles (plain, no logo) is open; the protagonist's plain bare hands are lifting out folded trousers to check the hem, which is neatly sewn. A neat receipt and a small pin cushion at the edge of the counter. In the background, a sewing machine on a shelf, soft warm light.
```

檢查點：視角對、沒有臉、沒有可讀文字、手是普通的手。

## 10. `result.jpg` — RESULT（結算畫面）

底圖：無（文字生圖）

```
Warm-toned 16-bit pixel art illustration, square 1:1 composition, soft cozy lighting, clean readable shapes. First-person point of view: the protagonist's face and body are NOT visible; if hands appear they are plain bare hands (no rings, no watch, no bracelet, no nail polish, no sleeves visible), gender-neutral. No people's faces anywhere (any other person is only a back view, a silhouette, or cropped at the neck). No readable text anywhere: all signs, price tags, labels and screens are blank or abstract lines. Camera: eye level, looking at the shop entrance from inside, with warm sunset light shining through the glass door. On a bench near the door, a paper shopping bag and a folded shirt sit neatly; the open sign is blank. A scoreboard-like blank wooden board on the wall with abstract star shapes (no numbers or text). Peaceful ending mood.
```

檢查點：視角對、沒有臉、沒有可讀文字、手是普通的手。

## 11. `end_good.jpg` — END 好結局（買好衣服，開心走出店）

底圖：無（文字生圖）

```
Warm-toned 16-bit pixel art illustration, square 1:1 composition, soft cozy lighting, clean readable shapes. First-person point of view: the protagonist's face and body are NOT visible; if hands appear they are plain bare hands (no rings, no watch, no bracelet, no nail polish, no sleeves visible), gender-neutral. No people's faces anywhere (any other person is only a back view, a silhouette, or cropped at the neck). No readable text anywhere: all signs, price tags, labels and screens are blank or abstract lines. Camera: eye level, just outside the shop door, looking back at the entrance from the sidewalk, bright warm daylight. The protagonist's plain bare hands hold a full paper shopping bag with rope handles; a clerk's arm (cropped at the shoulder, no face) waves from the doorway. The street behind has a small convenience-store sign (blank) and a scooter. Cheerful, satisfied mood, a few sparkle pixels.
```

檢查點：視角對、沒有臉、沒有可讀文字、手是普通的手。

## 12. `end_bad.jpg` — END 壞結局（買錯東西，垂頭走出店）

底圖：上傳已確認的 end_good.jpg（編輯式）

```
Warm-toned 16-bit pixel art illustration, square 1:1 composition, soft cozy lighting, clean readable shapes. First-person point of view: the protagonist's face and body are NOT visible; if hands appear they are plain bare hands (no rings, no watch, no bracelet, no nail polish, no sleeves visible), gender-neutral. No people's faces anywhere (any other person is only a back view, a silhouette, or cropped at the neck). No readable text anywhere: all signs, price tags, labels and screens are blank or abstract lines. Edit the uploaded image: keep the shop, street and style the same, but change the lighting to a dim, cloudy late afternoon. The paper shopping bag now hangs low from one plain bare hand, a trouser leg too long sticks out of the bag and drags slightly; the waving arm is gone and the door is closed. Subdued, a little disappointed mood, no faces, no readable text.
```

檢查點：視角對、沒有臉、沒有可讀文字、手是普通的手。 其餘部分要和底圖一致。
