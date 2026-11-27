#!/bin/bash
# Tras _render_tramos.sh (FIN en _render.log): concat → FAB_CONSERVAR=1 final → verificar → avisar. 26-nov-2026. Log: _tras_render.log
cd /c/FabricaAnimaciones/videos/tes_pierdes_siempre
until grep -q "^FIN" _render.log; do sleep 30; done
for T in 0_415 415_830 830_1240; do ffprobe -v error -show_entries format=duration -of csv=p=0 salida/tramo_$T.mp4 || { echo "FALTA tramo $T"; exit 1; }; done
printf "file 'tramo_0_415.mp4'\nfile 'tramo_415_830.mp4'\nfile 'tramo_830_1240.mp4'\n" > salida/_tramos.txt
ffmpeg -y -v error -f concat -safe 0 -i salida/_tramos.txt -c copy salida/video_sin_audio.mp4 && echo CONCAT_OK
cd /c/FabricaAnimaciones
FAB_CONSERVAR=1 python fab.py tes_pierdes_siempre final 2>&1 | tail -4
python fab.py tes_pierdes_siempre verificar 2>&1 | tail -8
python fab.py avisar "Listo el MASTER de las 15 cosas que pierdes para siempre en Skyrim, para Crónicas de Tamriel. Ya está verificado; sigue la miniatura y la subida." 2>&1 | tail -1
echo TRAS_FIN
