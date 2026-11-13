cd /c/FabricaAnimaciones
V=tes_reina_loba
for T in 0-700 700-1400 1400-2109; do
  a=${T%-*}; b=${T#*-}
  if ffprobe -v error -show_entries format=duration -of csv=p=0 videos/$V/salida/tramo_${a}_${b}.mp4 >/dev/null 2>&1; then echo "ya $T"; continue; fi
  python fab.py $V video --tramo $T 2>&1 | grep -v "^ *[0-9.]*s /" | tail -3
  echo "tramo $T fin"
done
# `final` lee salida/video_sin_audio.mp4: SIN este paso usa el render viejo (pasó el 13-nov-2026)
cd videos/$V/salida
printf "file 'tramo_0_700.mp4'\nfile 'tramo_700_1400.mp4'\nfile 'tramo_1400_2109.mp4'\n" > _concat.txt
ffmpeg -v error -y -f concat -safe 0 -i _concat.txt -c copy video_sin_audio.mp4 && echo "unido: $(ffprobe -v error -show_entries format=duration -of csv=p=0 video_sin_audio.mp4) s"
echo FIN
