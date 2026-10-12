"""把 TTSMaker 轉出的長音檔，依 3 秒停頓切回單一音檔。
用法：python3 tools/split_batch.py <下載的 mp3 路徑>
會檢查切出的段數＝order.json 的項目數，不符就不寫入任何檔案。"""
import hashlib, json, re, subprocess, sys, os
src = sys.argv[1]
order = json.load(open('tts_batch/order.json'))
VOICE = 'zh-TW-YunJheNeural'  # 讓 gen_audio.py 不要把這些檔案當成需要重錄
out = subprocess.run(['ffmpeg', '-i', src, '-af', 'silencedetect=noise=-40dB:d=2.0', '-f', 'null', '-'], capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', out)]
ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', out)]
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.strip())
# 只取長停頓（≥2.5 秒）當分隔，句內的短停頓不算
gaps = [(s, e) for s, e in zip(starts, ends) if e - s >= 2.5]
segs, prev = [], 0.0
for s, e in gaps:
    segs.append((prev, s)); prev = e
segs.append((prev, dur))
print(f'偵測到 {len(segs)} 段，預期 {len(order)} 段')
if len(segs) != len(order):
    sys.exit('❌ 段數不符，沒有寫入任何檔案。請確認貼上的文字與停頓都完整，或告訴我這個訊息。')
idx = json.load(open('audio/index.json')) if os.path.exists('audio/index.json') else {}
for (a, b), item in zip(segs, order):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{max(a-0.05,0):.2f}', '-to', f'{b+0.15:.2f}', '-i', src, '-ac', '1', '-b:a', '64k', f"audio/{item['id']}.mp3"], check=True)
    idx[item['id']] = hashlib.md5((VOICE + item['text']).encode()).hexdigest()
json.dump(idx, open('audio/index.json', 'w'), indent=0)
print('✅ 已切出並寫入', len(order), '個音檔')
