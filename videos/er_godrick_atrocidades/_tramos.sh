#!/bin/bash
cd /c/FabricaAnimaciones
for t in 500-750 750-1000 1000-1250 1250-1476; do
  a=${t%-*}; b=${t#*-}
  f=videos/er_godrick_atrocidades/salida/tramo_${a}_${b}.mp4
  if [ -f "$f" ] && /c/ffmpeg/bin/ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" >/dev/null 2>&1; then echo "ya $t"; continue; fi
  echo "=== $t $(date +%H:%M)"
  python fab.py er_godrick_atrocidades video --tramo $t > videos/er_godrick_atrocidades/_tramo_$a.log 2>&1
  echo "salida $t codigo $? $(date +%H:%M)"
  tail -2 videos/er_godrick_atrocidades/_tramo_$a.log
done
echo FIN
