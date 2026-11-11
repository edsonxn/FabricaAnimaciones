# -*- coding: utf-8 -*-
"""Corta a mano los clips que `bajar` no pudo (videos viejos sin 1080p): baja el video entero a _dl/ y corta el beat
(1920x1080 recortado, 30 fps, sin audio). python _manual.py scene-039 scene-041 ..."""
import glob, json, subprocess, sys
b = {x['id']: x for x in json.load(open('beats.json', encoding='utf-8'))}
q = json.load(open('busquedas.json', encoding='utf-8'))
for s in sys.argv[1:]:
    d = b[s]['t1'] - b[s]['t0']
    v = q[s]['url'].split('v=')[1]; ss = q[s]['desde']
    if not glob.glob(f'_dl/{v}.*'):
        subprocess.run(['yt-dlp', '-q', '-f', 'bv*', '-o', f'_dl/{v}.%(ext)s', 'https://youtu.be/' + v])
    src = glob.glob(f'_dl/{v}.*')[0]
    vf = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30"
    r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(ss), '-i', src, '-t', f'{d:.3f}', '-an', '-vf', vf,
                        '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', f'medios/{s}.mp4'])
    print(s, v, ss, r.returncode)
