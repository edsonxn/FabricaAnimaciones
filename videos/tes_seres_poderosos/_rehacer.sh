cd /c/FabricaAnimaciones
V=tes_seres_poderosos
while read -r a; do
  [ -z "$a" ] && continue
  rm -rf videos/$V/medios/_tmp_scene-*; n=${a%%|*}; q=${a#*|}; timeout 400 python fab.py $V bajar $n --q "$q" --rehacer < /dev/null 2>&1 | grep "scene-" | tail -1
done < videos/$V/_rehacer.txt
echo FIN
