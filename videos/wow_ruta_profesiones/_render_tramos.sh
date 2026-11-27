#!/bin/bash
# Render de wow_ruta_profesiones (25-nov-2026; copiado de wow_errores_60): fx → sfx → mezcla → video por tramos de 250 s (el render entero muere por memoria con
# ~250 FX, lección de er_rykard_atrocidades) + concat → final → verificar. UN render a la vez: espera a que no corra otro
# (ni el `video --tramo` de otra sesión ni su _render_tramos.sh entre tramos). Si se corta, relanzarlo: salta los tramos hechos.
cd /c/FabricaAnimaciones
V=wow_ruta_profesiones
D=videos/$V
otro() {
  # otro render, o la voz/selección (GPU) de otra sesión (aviso de la sesión de wow_oro_30_50, 25-nov); sin contarse a sí mismo
  powershell -c "Get-CimInstance Win32_Process | Where-Object { \$_.Name -match 'python' } | Select -Expand CommandLine" 2>/dev/null     | grep -v "$V" | grep -E -q " video$| video --tramo|-m render| final$| mezcla$| voz$| seleccionar$|tts_gen|tts_select"
}
while otro; do sleep 60; done
sleep 30
while otro; do sleep 60; done
echo "INICIO $(date +%H:%M)"
# hoja de efectos para revisarla mientras sigue el render (25-nov: falló dos veces por memoria con otras sesiones corriendo)
# (ya mirada) FAB_FX_FINAL=1 python fab.py $V fx hoja > $D/_prep4.log 2>&1; echo "hoja codigo $? $(date +%H:%M)" >> $D/_prep4.log
# echo hoja
holgura() {   # GB de memoria comprometida libre (la máquina se queda sin commit cuando varias sesiones trabajan a la vez)
  powershell -c "\$o=Get-CimInstance Win32_OperatingSystem; [int](\$o.FreeVirtualMemory/1MB)" 2>/dev/null | tr -d '
'
}
for e in fx sfx mezcla; do
  ok=0
  for intento in 1 2 3 4 5 6; do
    while [ "$(holgura)" -lt 10 ]; do sleep 60; done
    if python fab.py $V $e > $D/_render_$e.log 2>&1; then ok=1; break; fi
    echo "  $e intento $intento falló $(date +%H:%M): $(grep -o 'MemoryError\|Error[^:]*' $D/_render_$e.log | tail -1)"
    sleep 120
  done
  [ $ok = 1 ] || { echo "FALLÓ $e $(date +%H:%M)"; exit 1; }
  echo "$e ok $(date +%H:%M)"
done
# cortes cada 250 s hasta el total del timeline (25-nov: el total cambia al mover la promo y sumar las listas)
T=($(python -c "import json;t=json.load(open('$D/timeline.json',encoding='utf-8'))['total'];c=list(range(0,int(t),250));print(' '.join(map(str,c+[t])))"))
N=$(( ${#T[@]} - 1 ))
: > $D/salida/_lista.txt
for i in $(seq 0 $((N-1))); do
  a=${T[$i]}; b=${T[$((i+1))]}
  f=$(ls $D/salida/ | grep "^tramo_${a}_" | head -1)
  if [ -z "$f" ] || ! /c/ffmpeg/bin/ffprobe -v error -show_entries format=duration -of csv=p=0 "$D/salida/$f" >/dev/null 2>&1; then
    for intento in 1 2 3; do
      while [ "$(holgura)" -lt 10 ]; do sleep 60; done
      python fab.py $V video --tramo $a-$b > $D/_render_video_$i.log 2>&1
      f=$(ls $D/salida/ | grep "^tramo_${a}_" | head -1)
      [ -n "$f" ] && break
      echo "  tramo $a-$b intento $intento falló $(date +%H:%M)"; sleep 120
    done
  fi
  [ -z "$f" ] && { echo "FALLÓ tramo $a-$b $(date +%H:%M)"; exit 1; }
  echo "tramo $a-$b fin $(date +%H:%M) $f $(/c/ffmpeg/bin/ffprobe -v error -show_entries format=duration -of csv=p=0 $D/salida/$f)"
  echo "file '$f'" >> $D/salida/_lista.txt
done
(cd $D/salida && /c/ffmpeg/bin/ffmpeg -y -v error -f concat -safe 0 -i _lista.txt -c copy video_sin_audio.mp4) && echo "CONCAT OK $(date +%H:%M) $(/c/ffmpeg/bin/ffprobe -v error -show_entries format=duration -of csv=p=0 $D/salida/video_sin_audio.mp4)"
python fab.py $V final > $D/_render_final.log 2>&1 && echo "final ok $(date +%H:%M)" || { echo "FALLÓ final"; exit 1; }
python fab.py $V verificar > $D/_render_verificar.log 2>&1; echo "verificar código $? $(date +%H:%M)"
echo "FIN $(date +%H:%M)"
