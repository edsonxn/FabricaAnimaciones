#!/bin/bash
cd /c/FabricaAnimaciones
export PYTHONIOENCODING=utf-8
echo "=== regen $(date +%H:%M:%S)"
python fab.py independencia_mx voz --seeds 5 6 7 8 --solo napoleon_4 grito_5 capital_2 cierre_2 > videos/independencia_mx/voz_log2.txt 2>&1
echo "=== sel $(date +%H:%M:%S)"
python fab.py independencia_mx seleccionar > videos/independencia_mx/sel_log2.txt 2>&1
tail -6 videos/independencia_mx/sel_log2.txt
echo "=== listo $(date +%H:%M:%S)"
