#!/bin/bash
# Cola de voz: genera y selecciona tomas, un video tras otro (la GPU no se comparte: voz y Whisper nunca a la vez)
cd /c/FabricaAnimaciones
export PYTHONIOENCODING=utf-8
for v in "$@"; do
  echo "=== $v voz $(date +%H:%M:%S)"
  python fab.py $v voz > videos/$v/voz_log.txt 2>&1
  echo "=== $v seleccionar $(date +%H:%M:%S)"
  python fab.py $v seleccionar > videos/$v/sel_log.txt 2>&1
  echo "=== $v listo $(date +%H:%M:%S)"
  tail -5 videos/$v/sel_log.txt
done
echo "=== COLA TERMINADA $(date +%H:%M:%S)"
