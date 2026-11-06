cd /c/FabricaAnimaciones
V=tes_seres_poderosos
r(){ rm -rf videos/$V/medios/_tmp_scene-*; timeout 400 python fab.py $V bajar $1 "${@:2}" --rehacer < /dev/null 2>&1 | grep "scene-\|Error" | tail -1; }
r 123 --url https://www.youtube.com/watch?v=JV3tKszygTU --desde 2500
r 135 --url https://www.youtube.com/watch?v=NqddXGavHN0 --desde 40
r 144 --url https://www.youtube.com/watch?v=Wel4Z0ZI05A --desde 2600
r 147 --url https://www.youtube.com/watch?v=Wel4Z0ZI05A --desde 3000
r 151 --q "Skyrim Night Mother coffin Dark Brotherhood no HUD"
r 152 --url https://www.youtube.com/watch?v=JV3tKszygTU --desde 3300
r 158 --url https://www.youtube.com/watch?v=JV3tKszygTU --desde 4000
r 113 --url https://www.youtube.com/watch?v=-_lvLkFEViA --desde 49.3
echo FIN
