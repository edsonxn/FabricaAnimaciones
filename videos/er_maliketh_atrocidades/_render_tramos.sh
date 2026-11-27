#!/bin/bash
# Render por tramos de 250 s (el render entero muere por memoria con ~250 FX) + concat. Espera a que no haya otro render.
cd /c/FabricaAnimaciones
V=er_maliketh_atrocidades
while powershell -c "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Select -Expand CommandLine" 2>/dev/null | grep -q " video$\| video --tramo\|-m render"; do
  sleep 60
done
echo "INICIO $(date +%H:%M)"
T=(0 250 500 750 1000 1250 1455)
: > videos/$V/salida/_lista.txt
for i in 0 1 2 3 4 5; do
  a=${T[$i]}; b=${T[$((i+1))]}
  f=$(ls videos/$V/salida/ | grep "^tramo_${a}_" | head -1)
  if [ -z "$f" ]; then
    python fab.py $V video --tramo $a-$b > videos/$V/_render_$i.log 2>&1
    f=$(ls videos/$V/salida/ | grep "^tramo_${a}_" | head -1)
  fi
  echo "tramo $a-$b fin $(date +%H:%M) $f"
  echo "file '$f'" >> videos/$V/salida/_lista.txt
done
cd videos/$V/salida && /c/ffmpeg/bin/ffmpeg -y -v error -f concat -safe 0 -i _lista.txt -c copy video_sin_audio.mp4 && echo "CONCAT OK $(date +%H:%M)"
/c/ffmpeg/bin/ffmpeg -v error -i video_sin_audio.mp4 -f null - && echo "COMPROBADO"
echo "FIN $(date +%H:%M)"
