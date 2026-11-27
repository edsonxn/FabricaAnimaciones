#!/bin/bash
# Cierra el render de wow_ruta_profesiones (26-nov): espera a que acabe _render_tramos.sh, rehace los tramos que no abran
# (tramo_750_1000 quedó sin «moov atom») y luego concat → final → verificar.
cd /c/FabricaAnimaciones
V=wow_ruta_profesiones; D=videos/$V
holgura() { powershell -c "\$o=Get-CimInstance Win32_OperatingSystem; [int](\$o.FreeVirtualMemory/1MB)" 2>/dev/null | tr -dc '0-9'; }
echo "sigue $(date +%H:%M)"
T=($(python -c "import json;t=json.load(open('$D/timeline.json',encoding='utf-8'))['total'];c=list(range(0,int(t),250));print(' '.join(map(str,c+[t])))"))
N=$(( ${#T[@]} - 1 ))
: > $D/salida/_lista.txt
for i in $(seq 0 $((N-1))); do
  a=${T[$i]}; b=${T[$((i+1))]}
  for intento in 1 2 3; do
    f=$(ls $D/salida/ | grep "^tramo_${a}_" | head -1)
    dur=$([ -n "$f" ] && /c/ffmpeg/bin/ffprobe -v error -show_entries format=duration -of csv=p=0 "$D/salida/$f" 2>/dev/null)
    [ -n "$dur" ] && python -c "import sys;sys.exit(0 if float('$dur') > ($b - $a) - 1 else 1)" && break
    dur=""
    [ -n "$f" ] && rm -f "$D/salida/$f"
    while [ "$(holgura)" -lt 10 ]; do sleep 60; done
    echo "rehago tramo $a-$b (intento $intento) $(date +%H:%M)"
    python fab.py $V video --tramo $a-$b > $D/_render_video_${i}_b.log 2>&1
  done
  [ -z "$dur" ] && { echo "FALLÓ tramo $a-$b"; exit 1; }
  echo "tramo $a-$b ok $dur"
  echo "file '$f'" >> $D/salida/_lista.txt
done
(cd $D/salida && /c/ffmpeg/bin/ffmpeg -y -v error -f concat -safe 0 -i _lista.txt -c copy video_sin_audio.mp4) && echo "CONCAT OK $(/c/ffmpeg/bin/ffprobe -v error -show_entries format=duration -of csv=p=0 $D/salida/video_sin_audio.mp4)"
python fab.py $V final > $D/_render_final.log 2>&1 && echo "final ok $(date +%H:%M)" || { echo "FALLÓ final"; exit 1; }
python fab.py $V verificar > $D/_render_verificar.log 2>&1; echo "verificar código $? $(date +%H:%M)"
echo FIN
