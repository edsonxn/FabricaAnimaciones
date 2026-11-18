#!/bin/bash
# Render completo + audio + final + verificar, esperando a que no haya otros procesos pesados (regla 11-nov). Para en el primer error.
cd /c/FabricaAnimaciones
export PYTHONIOENCODING=utf-8
python videos/t1_blg_caida/esperar_libre.py --max 10800 --cada 20 || { echo "ESPERA AGOTADA"; exit 3; }
for e in video fx ambiente; do
  echo "=== $e $(date +%H:%M)"; python fab.py cod_villanos $e || { echo "FALLO $e"; exit 1; }
done
echo "=== ost $(date +%H:%M)"; python videos/cod_villanos/armar_musica_ost.py || { echo "FALLO ost"; exit 1; }
for e in mezcla final verificar; do
  echo "=== $e $(date +%H:%M)"; python fab.py cod_villanos $e || { echo "FALLO $e"; exit 1; }
done
ls -la videos/cod_villanos/salida/
echo "=== FIN $(date +%H:%M)"
