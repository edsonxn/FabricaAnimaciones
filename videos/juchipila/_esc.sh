#!/bin/bash
# uso: ./_esc.sh escena [n]  -> previews/esc_<escena>.jpg
cd /c/FabricaAnimaciones/videos/juchipila
T=$(python _t.py $1 ${2:-9})
./run.sh _prueba.py esc_$1 $T 2>&1 | tail -3
