#!/bin/bash
cd /c/FabricaAnimaciones
export PYTHONIOENCODING=utf-8
python videos/t1_blg_caida/esperar_libre.py --max 10800 --cada 20 || { echo "ESPERA AGOTADA"; exit 3; }
for e in video final verificar; do
  echo "=== $e $(date +%H:%M)"; python fab.py cod_villanos $e || { echo "FALLO $e"; exit 1; }
done
ls -la videos/cod_villanos/salida/
echo "=== FIN $(date +%H:%M)"
