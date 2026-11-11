cd /c/FabricaAnimaciones
V=tes_builds_rotas
for T in 0-380 380-760 760-1120; do
  a=${T%-*}; b=${T#*-}
  if ffprobe -v error -show_entries format=duration -of csv=p=0 videos/$V/salida/tramo_${a}_${b}.mp4 >/dev/null 2>&1; then echo "ya $T"; continue; fi
  python fab.py $V video --tramo $T 2>&1 | grep -v "^ *[0-9.]*s /" | tail -3
  echo "tramo $T fin"
done
echo FIN
