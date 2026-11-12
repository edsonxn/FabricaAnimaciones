#!/bin/bash
# v3 (12-nov-2026): espera a que no corra NINGÚN otro render (regla «un render a la vez», 11-nov) y renderiza por tramos → final → verificar
cd /c/FabricaAnimaciones
V=tes_builds_rotas
otro() {
  powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | ForEach-Object { \$_.CommandLine }" 2>/dev/null \
    | grep -E "fab.py [a-z0-9_]+ (video|final)" | grep -v "$V" | head -1
}
while [ -n "$(otro)" ]; do echo "$(date +%H:%M) esperando: $(otro)"; sleep 120; done
echo "$(date +%H:%M) sin otros renders: empiezo"
for T in 0-400 400-800 800-1182; do
  a=${T%-*}; b=${T#*-}
  f=videos/$V/salida/tramo_${a}_${b}.mp4
  if [ -f "$f.ok" ]; then echo "ya $T"; continue; fi
  for i in 1 2 3; do
    python fab.py $V video --tramo $T 2>&1 | grep -v "^ *[0-9.]*s /" | tail -3
    /c/ffmpeg/bin/ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" >/dev/null 2>&1 && { touch "$f.ok"; break; }
    echo "reintento $T"
  done
  echo "$(date +%H:%M) tramo $T fin"
done
cd videos/$V/salida
printf "file 'tramo_0_400.mp4'\nfile 'tramo_400_800.mp4'\nfile 'tramo_800_1182.mp4'\n" > _concat.txt
/c/ffmpeg/bin/ffmpeg -y -loglevel error -f concat -safe 0 -i _concat.txt -c copy video_sin_audio.mp4 && echo "concat OK"
cd /c/FabricaAnimaciones
FAB_CONSERVAR=1 python fab.py $V final 2>&1 | tail -4
python fab.py $V verificar 2>&1 | tail -6
echo "$(date +%H:%M) FIN"
