#!/bin/bash
# Render de wow_ruta_profesiones (25-nov-2026; copiado de wow_errores_60): fx → sfx → mezcla → video por tramos de 250 s (el render entero muere por memoria con
# ~250 FX, lección de er_rykard_atrocidades) + concat → final → verificar. UN render a la vez: espera a que no corra otro
# (ni el `video --tramo` de otra sesión ni su _render_tramos.sh entre tramos). Si se corta, relanzarlo: salta los tramos hechos.
cd /c/FabricaAnimaciones
V=wow_ruta_profesiones
D=videos/$V
otro() {
  powershell -c "Get-CimInstance Win32_Process | Where-Object { \$_.Name -match 'python|bash' } | Select -Expand CommandLine" 2>/dev/null \
    | grep -v "$V" | grep -q " video$\| video --tramo\|-m render\|_render_tramos.sh\| final$\| mezcla$"
}
while otro; do sleep 60; done
sleep 30
while otro; do sleep 60; done
echo "INICIO $(date +%H:%M)"
for e in fx sfx mezcla; do
  python fab.py $V $e > $D/_render_$e.log 2>&1 || { echo "FALLÓ $e $(date +%H:%M)"; exit 1; }
  echo "$e ok $(date +%H:%M)"
done
T=(0 250 500 750 1000 1250 1500 1750 1878.75)
: > $D/salida/_lista.txt
for i in 0 1 2 3 4 5 6 7; do
  a=${T[$i]}; b=${T[$((i+1))]}
  f=$(ls $D/salida/ | grep "^tramo_${a}_" | head -1)
  if [ -z "$f" ] || ! /c/ffmpeg/bin/ffprobe -v error -show_entries format=duration -of csv=p=0 "$D/salida/$f" >/dev/null 2>&1; then
    python fab.py $V video --tramo $a-$b > $D/_render_video_$i.log 2>&1
    f=$(ls $D/salida/ | grep "^tramo_${a}_" | head -1)
  fi
  [ -z "$f" ] && { echo "FALLÓ tramo $a-$b $(date +%H:%M)"; exit 1; }
  echo "tramo $a-$b fin $(date +%H:%M) $f $(/c/ffmpeg/bin/ffprobe -v error -show_entries format=duration -of csv=p=0 $D/salida/$f)"
  echo "file '$f'" >> $D/salida/_lista.txt
done
(cd $D/salida && /c/ffmpeg/bin/ffmpeg -y -v error -f concat -safe 0 -i _lista.txt -c copy video_sin_audio.mp4) && echo "CONCAT OK $(date +%H:%M) $(/c/ffmpeg/bin/ffprobe -v error -show_entries format=duration -of csv=p=0 $D/salida/video_sin_audio.mp4)"
python fab.py $V final > $D/_render_final.log 2>&1 && echo "final ok $(date +%H:%M)" || { echo "FALLÓ final"; exit 1; }
python fab.py $V verificar > $D/_render_verificar.log 2>&1; echo "verificar código $? $(date +%H:%M)"
echo "FIN $(date +%H:%M)"
