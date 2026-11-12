#!/bin/bash
# 12-nov (v3b): tarjeta «Top 10 Slo-Mo Bow Kills» en el 2:07 (scene-015) + recorte sobre negro y MG cortado en 16:10 (scene-113)
# → espera a que no corra otro render, rehace tramos 0-400 y 800-1182 → concat → final → verificar
cd /c/FabricaAnimaciones
V=tes_builds_rotas
otro() {
  powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | ForEach-Object { \$_.CommandLine }" 2>/dev/null \
    | grep -E "fab.py [a-z0-9_]+ (video|final)" | grep -v "$V" | head -1
}
while [ -n "$(otro)" ]; do echo "$(date +%H:%M) esperando: $(otro)"; sleep 120; done
for T in 0-400 800-1182; do
  a=${T%-*}; b=${T#*-}; f=videos/$V/salida/tramo_${a}_${b}.mp4
  rm -f "$f.ok"
  for i in 1 2 3; do
    python fab.py $V video --tramo $T 2>&1 | grep -v "^ *[0-9.]*s /" | tail -2
    /c/ffmpeg/bin/ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" >/dev/null 2>&1 && { touch "$f.ok"; break; }
    echo "reintento $T"
  done
  echo "$(date +%H:%M) tramo $T fin"
done
cd videos/$V/salida
/c/ffmpeg/bin/ffmpeg -y -loglevel error -f concat -safe 0 -i _concat.txt -c copy video_sin_audio.mp4 && echo "concat OK"
cd /c/FabricaAnimaciones
FAB_CONSERVAR=1 python fab.py $V final 2>&1 | tail -3
python fab.py $V verificar 2>&1 | grep -v "^ *stream" | tail -6
echo "$(date +%H:%M) FIN"
