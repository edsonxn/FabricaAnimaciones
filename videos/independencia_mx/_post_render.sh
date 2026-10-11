#!/bin/bash
# espera a que exista salida/video_sin_audio.mp4 (fin del render) y luego hace final + verificar (log: post_render_log.txt)
cd /c/FabricaAnimaciones
LOG=videos/independencia_mx/post_render_log.txt
until [ -f videos/independencia_mx/salida/video_sin_audio.mp4 ]; do sleep 60; done
sleep 20
echo "=== render listo $(date +%H:%M:%S) ===" >> $LOG
python fab.py independencia_mx final >> $LOG 2>&1
echo "=== final terminado $(date +%H:%M:%S) ===" >> $LOG
python fab.py independencia_mx verificar >> $LOG 2>&1
echo "=== POST_RENDER_OK $(date +%H:%M:%S) ===" >> $LOG
