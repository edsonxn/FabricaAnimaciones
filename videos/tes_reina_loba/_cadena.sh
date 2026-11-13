#!/bin/bash
# Cadena final de tes_reina_loba: espera a que no haya OTRO render (regla «un render a la vez»), luego fx → ambiente → mezcla →
# render por tramos → final → verificar. Log: _cadena.log
cd /c/FabricaAnimaciones
otro() {
  powershell -NoProfile -Command "(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -like '*secuencia video*' -or \$_.CommandLine -like '*fab.py * video*' -or \$_.CommandLine -like '*fab.py * final*' } | Where-Object { \$_.CommandLine -notlike '*tes_reina_loba*' }).Count"
}
while [ "$(otro | tr -d '\r ')" != "0" ]; do echo "$(date +%H:%M) espero otro render"; sleep 120; done
echo "$(date +%H:%M) arranca"
set -e
export PYTHONIOENCODING=utf-8
python fab.py tes_reina_loba fx 2>&1 | grep -v "^ *[0-9.]*s / " | tail -3
echo "$(date +%H:%M) fx ok"
python fab.py tes_reina_loba ambiente 2>&1 | tail -2
python fab.py tes_reina_loba mezcla 2>&1 | tail -3
echo "$(date +%H:%M) mezcla ok"
bash videos/tes_reina_loba/_render_tramos.sh
echo "$(date +%H:%M) tramos ok"
FAB_CONSERVAR=1 python fab.py tes_reina_loba final 2>&1 | tail -4
python fab.py tes_reina_loba verificar 2>&1 | tail -8
echo "$(date +%H:%M) CADENA FIN"
