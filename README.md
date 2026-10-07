# 情境對話遊戲系列（Taiwan Week）

## 結構
```
index.html          遊戲選單（之後換成「台灣一週」地圖）
map/                地圖專用檔案（之後新增）
games/<scene>/      每個遊戲：index.html + images/（檔名小寫 .jpg）
```

## 場景 ID（資料夾名 = scene = collection 前綴 = GA4 game 參數）
drinks · reserva · breakfast · thsr · gas · nightmarket · parcel · bakery

Firestore collection：`<scene>game_scores` 或 `<scene>_scores`（沿用各遊戲現有名稱，不要改，否則舊排行榜會消失）。
排行榜需要複合索引：score 降冪 + elapsed 升冪。

## 嵌入模式（給地圖用）
iframe 載入：
```
games/<scene>/index.html?embed=1&name=玩家名&s=simp&l=en
```
- `name`：玩家名字（必填，會跳過登入頁）
- `s`：`simp` 簡體，預設繁體
- `l`：`en` 英文，預設西文
- 嵌入時不顯示登入頁和排行榜，直接開始。

遊戲結束時（結果頁按「回到地圖」）送出：
```js
parent.postMessage({ type: 'scene-complete', scene: '<scene>', score, mistakes }, '*');
```
地圖收到後關掉 iframe 並記錄成績。

## 不帶 embed=1
就是單機版：有登入頁、排行榜，連結可以直接發給學生。

## 新增遊戲
複製現有遊戲的共用區塊（設定、翻譯、朗讀、單字、錯誤紀錄、排行榜、重新開始），只換遊戲專屬部分；詳見交接包。
