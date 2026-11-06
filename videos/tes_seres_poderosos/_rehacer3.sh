cd /c/FabricaAnimaciones
V=tes_seres_poderosos
r(){ rm -rf videos/$V/medios/_tmp_scene-*; timeout 400 python fab.py $V bajar $1 "${@:2}" --rehacer < /dev/null 2>&1 | grep "scene-" | tail -1; }
r 19 --q "ESO Summerset official cinematic trailer"
r 23 --q "Daggerfall Unity gameplay no commentary 4k"
r 25 --url https://www.youtube.com/watch?v=Wel4Z0ZI05A --desde 400
r 30 --url https://www.youtube.com/watch?v=Wel4Z0ZI05A --desde 1500
r 42 --url https://www.youtube.com/watch?v=h8Otsnzg-68 --desde 300
r 54 --url https://www.youtube.com/watch?v=Wel4Z0ZI05A --desde 1100
r 60 --url https://www.youtube.com/watch?v=Wel4Z0ZI05A --desde 2000
r 65 --url https://www.youtube.com/watch?v=JV3tKszygTU --desde 600
r 81 --url https://www.youtube.com/watch?v=JV3tKszygTU --desde 1500
r 94 --url https://www.youtube.com/watch?v=Wel4Z0ZI05A --desde 700
r 109 --url https://www.youtube.com/watch?v=h8Otsnzg-68 --desde 900
r 115 --q "Shivering Isles Remastered no commentary 4k"
r 72 --url https://www.youtube.com/watch?v=baSWAT0dt2o --desde 269.4
r 113 --url https://www.youtube.com/watch?v=-_lvLkFEViA --desde 49.3
echo FIN
