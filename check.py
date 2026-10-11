"""資料檢查：python3 check.py"""
import json, sys
concepts = json.load(open('concepts.json'))
quiz = json.load(open('quiz.json'))
units = json.load(open('units.json'))
errors = []
ids = [c['id'] for c in concepts] + [q['id'] for q in quiz]
dup = {i for i in ids if ids.count(i) > 1}
if dup: errors.append(f'重複 id：{dup}')
cids = {c['id'] for c in concepts}
for c in concepts:
    if not c.get('ch'): errors.append(f"{c['id']}：缺 ch")
    for k in ('id', 'topic', 'term', 'en', 'def', 'example'):
        if not c.get(k): errors.append(f"{c.get('id')}：缺 {k}")
for q in quiz:
    if q['concept'] not in cids: errors.append(f"{q['id']}：concept {q['concept']} 不存在")
    if len(q['options']) != 4: errors.append(f"{q['id']}：選項不是 4 個")
    if not 0 <= q['answer'] < len(q['options']): errors.append(f"{q['id']}：answer 超出範圍")
    if len(set(q['options'])) != len(q['options']): errors.append(f"{q['id']}：選項重複")
    if not q.get('why'): errors.append(f"{q['id']}：缺 why")
for w in units:
    for cid in w['concepts']:
        if cid not in cids: errors.append(f"{w['key']}：概念 {cid} 不存在")
import os
for k in cids | {q['id'] for q in quiz} | {w['key'] for w in units if w['points']}:
    if not os.path.exists(f'audio/{k}.mp3'): errors.append(f'缺音檔 audio/{k}.mp3（跑 tools/gen_audio.py）')
print(f'概念卡 {len(concepts)}、情境題 {len(quiz)}、單元 {len(units)}')
print('\n'.join(errors) if errors else '✅ 全部通過')
sys.exit(1 if errors else 0)
