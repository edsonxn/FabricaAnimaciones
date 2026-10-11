#!/bin/bash
# Render con reintentos: el render reanuda los segmentos ya terminados; si un worker muere por falta de memoria virtual se vuelve a lanzar.
cd /c/FabricaAnimaciones
for i in $(seq 1 6); do
  echo "=== intento $i $(date +%H:%M:%S) ===" >> videos/independencia_mx/render_v3_log.txt
  python fab.py independencia_mx video --procs 6 >> videos/independencia_mx/render_v3_log.txt 2>&1
  if [ -f videos/independencia_mx/salida/video_sin_audio.mp4 ]; then echo "LISTO $(date +%H:%M:%S)" >> videos/independencia_mx/render_v3_log.txt; break; fi
  sleep 10
done
