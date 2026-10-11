# CLAUDE.md — exp-methods-review

## Repo 用途
hai 的「心理學實驗法」每週複習 PWA（手機為主）。骨架仿 `german-review`：單頁 `index.html` ＋ runtime fetch JSON，無 build、無框架。已部署：公開 repo `github.com/Tuanzilee/exp-methods-review`，Pages `tuanzilee.github.io/exp-methods-review`（main 分支根目錄，push 後 1–2 分鐘更新）。`samples/` 試聽檔不進 repo（.gitignore）。

## 檔案結構
```
index.html     ← 全部 UI 與邏輯（首頁、單元重點、概念卡、情境題）
concepts.json  ← 概念卡
quiz.json      ← 情境題（4 選 1，附解析）
units.json     ← 單元（章節）重點摘要與待辦
sw.js / manifest.json / icon-*.png
tools/gen_audio.py ← 產生音檔（雲哲男聲 zh-TW-YunJheNeural，hai 選定）：`~/.venvs/tts/bin/python tools/gen_audio.py`
audio/         ← {概念卡id}.mp3、{題目id}.mp3、Ch{章}.mp3（失敗時退回裝置語音）
check.py       ← 資料檢查（含音檔齊全）：python3 check.py
```
預覽：`.claude/launch.json`（母資料夾）的 `exp-methods-review`，埠 8766。

## 資料 schema（一律以「單元（章節）」分類，畫面只顯示 Ch1–Ch6）
- `concepts.json`：`id`（不要改既有 id，進度綁 id；舊的 E_W1_C01 這類 id 只是歷史命名，不代表週次）、`ch`（章號，必填）、`week`（選填，上課週次，只做追溯、不顯示）、`topic`、`term`、`en`、`def`、`example`、`tags`
- `quiz.json`：`id`、`ch`、`q`、`options`（4 個）、`answer`（options 的索引）、`why`、`concept`（對應概念卡 id；答錯會把該概念加入錯題本）
- `units.json`：每章一筆：`ch`、`key`（Ch1…，音檔檔名）、`label`、`scope`（ch1…）、`say`（朗讀開頭）、`title`、`weeks`（顯示的對應上課週次或「講義」）、`summary`、`points[]`、`todo[]`、`concepts[]`
- 新增內容：新卡片的 id 用 `E_C{章}_C{兩位數}`、題目 `E_C{章}_Q{兩位數}`
- 歸屬原則：看這張卡在講義的哪一章；2026-10-12 hai 要求「以單元分」，把 W1/W2/W4 的卡依主題歸入 Ch1–Ch4

## 介面風格（2026-10-07，hai 參考一款學習 App 的截圖）
暖米色底、深棕字、大圓角（20px）加淡邊框、無陰影；首頁只留一個主行動（今天要複習的卡數＋開始複習）；底部浮動膠囊導覽列＋線條圖示（不用彩色 emoji）；主按鈕有立體底邊。只借設計手法，不複製對方的圖示或文案。連勝／XP 暫不做。德文複習尚未套用。

## 每週新增內容（hai 說「更新實驗法 W{n}」）
1. 讀 `~/Desktop/P. 進行中專案/FJU psy/02_修課/1151/1151_心理學實驗法/` 當週的 `*_W{nn}_Plaud逐字稿.md`（Plaud 摘要區已分好知識點）與講義 PDF
2. **Plaud 轉錄未經核聽**：專有名詞、數字以課本（Morling）與講義校正；不確定處列給 hai 確認
3. 以「一張卡一個概念」追加 concepts.json；情境題用課堂案例改寫；更新 units.json
4. **用自己的話改寫，不要貼講義或課本原文**（日後若公開 repo，需先檢查）
5. 跑 `~/.venvs/tts/bin/python tools/gen_audio.py` 補音檔，再跑 `python3 check.py`；bump `sw.js` 的 `CACHE` 版本號
6. 本機預覽驗證後 commit；**push 前一律先問 hai**（公開 repo，內容不放講義或課本原文）

## 待做
- 期中考範圍＝到 Ch7（hai 確認）；Ch7 講義還沒更新。範圍按鈕「期中範圍（至 Ch7）」目前以 `ch <= 7` 判斷
- 有課堂活動題（如 Ch5 p.149）PPT 沒給答案，不要替它編答案

## 講義來源（2026-10-11）
`心理學實驗法 Ch1–Ch6(1).pdf`（輔大黃揚名老師講義，文字很少、多為圖片，抽文字不夠，要轉圖看）。Ch5、Ch6 的卡片以 PPT 為主；PPT 沒寫定義的詞（尺規四種、雙盲等），只用教科書通用的標準說法，不自己加案例以外的主張。

## 查證紀錄（2026-10-07，Consensus）
- 運動與死亡風險：對應 Gorzelitz 等人 2022（BJSM，PLCO，99,713 人）；32%／41%／9% 吻合，41% 是達有氧建議量＋每週重訓 1–2 次
- 憤怒發洩：對應 Bushman 2002（PSPB）；課堂說「攻擊老闆臉」與原研究（想著激怒者打沙包）不同，以原研究為準
- 臉書情緒研究：Kramer 等人 2014（PNAS）；實際是減少正向或負向貼文；康乃爾 IRB 認定不屬其審查範圍，PNAS 發關注聲明
- 米爾格倫：原始基準約 65% 到 450V（Mazzocco 2025 引述）、全條件約 43.6%（Haslam 2014）；現代重現多停在 150V（Burger 2009）。「預測 0.1%」未查到來源
- 未查證：影響力因子 15.5／Q1、輔大 IRB 不審新藥、塔斯基吉與斯坦福的細節（卡片只寫課堂層級的描述）
