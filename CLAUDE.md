# CLAUDE.md — exp-methods-review

## Repo 用途
hai 的「心理學實驗法」每週複習 PWA（手機為主）。骨架仿 `german-review`：單頁 `index.html` ＋ runtime fetch JSON，無 build、無框架。已部署：公開 repo `github.com/Tuanzilee/exp-methods-review`，Pages `tuanzilee.github.io/exp-methods-review`（main 分支根目錄，push 後 1–2 分鐘更新）。`samples/` 試聽檔不進 repo（.gitignore）。

## 檔案結構
```
index.html     ← 全部 UI 與邏輯（首頁、每週重點、概念卡、情境題）
concepts.json  ← 概念卡
quiz.json      ← 情境題（4 選 1，附解析）
weeks.json     ← 每週重點摘要與待辦
sw.js / manifest.json / icon-*.png
tools/gen_audio.py ← 產生音檔（雲哲男聲 zh-TW-YunJheNeural，hai 選定）：`~/.venvs/tts/bin/python tools/gen_audio.py`
audio/         ← {概念卡id}.mp3、{題目id}.mp3、W{週}.mp3（失敗時退回裝置語音）
check.py       ← 資料檢查（含音檔齊全）：python3 check.py
```
預覽：`.claude/launch.json`（母資料夾）的 `exp-methods-review`，埠 8766。

## 資料 schema
- `concepts.json`：`id`（E_W{週}_C{兩位數}，不要改既有 id，進度綁 id）、`week`、`topic`、`term`、`en`、`def`、`example`、`tags`（含「期中」會進期中範圍）
- `quiz.json`：`id`（E_W{週}_Q{兩位數}）、`week`、`q`、`options`（4 個）、`answer`（options 的索引）、`why`、`concept`（對應概念卡 id；答錯會把該概念加入錯題本）
- `weeks.json`：`week`、`date`、`title`、`summary`、`points[]`、`todo[]`、`concepts[]`。W3 放假沒上課，保留一筆說明

## 每週新增內容（hai 說「更新實驗法 W{n}」）
1. 讀 `~/Desktop/P. 進行中專案/FJU psy/02_修課/1151/1151_心理學實驗法/` 當週的 `*_W{nn}_Plaud逐字稿.md`（Plaud 摘要區已分好知識點）與講義 PDF
2. **Plaud 轉錄未經核聽**：專有名詞、數字以課本（Morling）與講義校正；不確定處列給 hai 確認
3. 以「一張卡一個概念」追加 concepts.json；情境題用課堂案例改寫；更新 weeks.json
4. **用自己的話改寫，不要貼講義或課本原文**（日後若公開 repo，需先檢查）
5. 跑 `~/.venvs/tts/bin/python tools/gen_audio.py` 補音檔，再跑 `python3 check.py`；bump `sw.js` 的 `CACHE` 版本號
6. 本機預覽驗證後 commit；**push 前一律先問 hai**（公開 repo，內容不放講義或課本原文）

## 待做
- 期中考範圍＝到 Ch7（hai 確認）。`SCOPES` 的「期中範圍」目前以 `week <= 7` 近似，等老師公布章節與週次對應後改成精確章節；`tags` 的「期中」已不再使用

## 查證紀錄（2026-10-07，Consensus）
- 運動與死亡風險：對應 Gorzelitz 等人 2022（BJSM，PLCO，99,713 人）；32%／41%／9% 吻合，41% 是達有氧建議量＋每週重訓 1–2 次
- 憤怒發洩：對應 Bushman 2002（PSPB）；課堂說「攻擊老闆臉」與原研究（想著激怒者打沙包）不同，以原研究為準
- 臉書情緒研究：Kramer 等人 2014（PNAS）；實際是減少正向或負向貼文；康乃爾 IRB 認定不屬其審查範圍，PNAS 發關注聲明
- 米爾格倫：原始基準約 65% 到 450V（Mazzocco 2025 引述）、全條件約 43.6%（Haslam 2014）；現代重現多停在 150V（Burger 2009）。「預測 0.1%」未查到來源
- 未查證：影響力因子 15.5／Q1、輔大 IRB 不審新藥、塔斯基吉與斯坦福的細節（卡片只寫課堂層級的描述）
