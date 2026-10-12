"""產生「貼進 TTSMaker 網頁」用的文字檔（Lite 方案沒有 API 時用）。
只包含目前缺音檔的項目，項目之間插入 3 秒停頓 ((⏱️=3000))，之後用 tools/split_batch.py 依停頓切回單一音檔。
用法：python3 tools/make_tts_batch.py → 產生 tts_batch/batch.txt 與 tts_batch/order.json"""
import json, os
concepts = json.load(open('concepts.json')); quiz = json.load(open('quiz.json')); units = json.load(open('units.json'))
items = []
for c in concepts: items.append((c['id'], f"{c['term']}。{c['def']}。例如：{c['example']}"))
for q in quiz: items.append((q['id'], q['why']))
for u in units:
    if u['points']: items.append((u['key'], f"{u['say']}，{u['title']}。" + '。'.join(u['points'])))
missing = [(k, t) for k, t in items if not os.path.exists(f'audio/{k}.mp3')]
PAUSE = '((⏱️=3000))'
os.makedirs('tts_batch', exist_ok=True)
text = f'\n{PAUSE}\n'.join(t for _, t in missing)
open('tts_batch/batch.txt', 'w').write(text)
json.dump([{'id': k, 'text': t} for k, t in missing], open('tts_batch/order.json', 'w'), ensure_ascii=False, indent=0)
print(f'缺音檔 {len(missing)} 個，文字約 {len(text)} 字（含停頓標記），停頓 {len(missing)-1} 次')
if len(text) > 10000: print('⚠️ 超過 Lite 單次 10,000 字，要分批貼')
