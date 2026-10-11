#!/bin/bash
# uso: ./_pr.sh escena  -> hoja con 9 cuadros repartidos en la escena
cd /c/FabricaAnimaciones/videos/un_dia_30mil
T=$(python - "$1" <<'P'
import json,sys
e={x['id']:x for x in json.load(open('timeline.json',encoding='utf-8'))['escenas']}[sys.argv[1]]
print(' '.join(f"{e['t0']+f*(e['t1']-e['t0']):.2f}" for f in (0.06,0.14,0.22,0.32,0.42,0.52,0.64,0.78,0.92)))
P
)
./run.sh ../../nucleo/prueba_escena.py $1 $T
