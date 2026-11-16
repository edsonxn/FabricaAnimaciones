#!/bin/bash
# Render por tramos de 250 s (er_godrick: el render entero muere por memoria) + concat. Espera a que no haya otro render.
cd /c/FabricaAnimaciones
while powershell -c "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Select -Expand CommandLine" 2>/dev/null | grep -q " video$\|-m render"; do
  sleep 60
done
echo "INICIO $(date +%H:%M)"
T=(0 250 500 750 1000 1250 1500 1657.5)
for i in 0 1 2 3 4 5 6; do
  a=${T[$i]}; b=${T[$((i+1))]}
  f=videos/er_sinluz_atrocidades/salida/tramo_${a}_${b}.mp4
  if [ -s "$f" ]; then echo "ya $f"; continue; fi
  python fab.py er_sinluz_atrocidades video --tramo $a-$b > videos/er_sinluz_atrocidades/_render_$i.log 2>&1
  echo "tramo $a-$b fin $(date +%H:%M) $(ls videos/er_sinluz_atrocidades/salida/ | grep tramo_${a}_ | head -1)"
done
echo "FIN $(date +%H:%M)"
