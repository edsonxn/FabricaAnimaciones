#!/bin/bash
# REANUDAR (14-nov 13:12, pausado por el usuario): fx+ambiente+mezcla YA hechos y tramo_0_700 listo; sigue tramos 700-2109 → final → verificar → tele.
# render por tramos → final → verificar. Log: _cadena.log
cd /c/FabricaAnimaciones
otro() {
  powershell -NoProfile -Command "(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -like '*secuencia video*' -or \$_.CommandLine -like '*fab.py * video*' -or \$_.CommandLine -like '*fab.py * final*' -or \$_.CommandLine -like '*fab.py * seleccionar*' } | Where-Object { \$_.CommandLine -notlike '*tes_reina_loba*' }).Count"
}
while [ "$(otro | tr -d '\r ')" != "0" ]; do echo "$(date +%H:%M) espero otro render"; sleep 120; done
echo "$(date +%H:%M) arranca"
set -e
export PYTHONIOENCODING=utf-8
bash videos/tes_reina_loba/_render_tramos.sh
echo "$(date +%H:%M) tramos ok"
FAB_CONSERVAR=1 python fab.py tes_reina_loba final 2>&1 | tail -4
python fab.py tes_reina_loba verificar 2>&1 | tail -8
# V3 (14-nov): copia ligera para la tele (el MASTER de 2 GB corta la conexión) y a la tele
cd videos/tes_reina_loba
ffmpeg -loglevel error -y -i salida/tes_reina_loba_MASTER.mp4 -c:v h264_nvenc -preset p5 -b:v 3200k -maxrate 4500k -bufsize 9000k -c:a aac -b:a 160k -movflags +faststart previews/tes_reina_loba_TELE_ligero.mp4 && echo "$(date +%H:%M) copia tele ok"
cd /c/FabricaAnimaciones
python fab.py tele video videos/tes_reina_loba/previews/tes_reina_loba_TELE_ligero.mp4 2>&1 | tail -2
echo "$(date +%H:%M) CADENA FIN"
