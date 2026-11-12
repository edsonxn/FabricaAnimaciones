#!/bin/bash
# 12-nov: podio del cierre (1.º puesto salía al irse) → solo tramo 800-1182 + concat + final + verificar
cd /c/FabricaAnimaciones
V=tes_builds_rotas
f=videos/$V/salida/tramo_800_1182.mp4
rm -f "$f.ok"
python fab.py $V video --tramo 800-1182 2>&1 | grep -v "^ *[0-9.]*s /" | tail -3
/c/ffmpeg/bin/ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" || exit 1
touch "$f.ok"
cd videos/$V/salida
/c/ffmpeg/bin/ffmpeg -y -loglevel error -f concat -safe 0 -i _concat.txt -c copy video_sin_audio.mp4 && echo "concat OK"
cd /c/FabricaAnimaciones
FAB_CONSERVAR=1 python fab.py $V final 2>&1 | tail -4
python fab.py $V verificar 2>&1 | grep -v "^ *stream" | tail -6
echo "$(date +%H:%M) FIN"
