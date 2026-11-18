#!/bin/bash
cd /c/FabricaAnimaciones/videos/cod_villanos
export PYTHONIOENCODING=utf-8
echo "=== ost $(date +%H:%M)"; python armar_musica_ost.py || { echo "FALLO ost"; exit 1; }
cd /c/FabricaAnimaciones
for e in mezcla final verificar; do
  echo "=== $e $(date +%H:%M)"; python fab.py cod_villanos $e || { echo "FALLO $e"; exit 1; }
done
ls -la videos/cod_villanos/salida/
echo "=== FIN $(date +%H:%M)"
