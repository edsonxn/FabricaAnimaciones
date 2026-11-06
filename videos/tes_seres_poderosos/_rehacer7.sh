cd /c/FabricaAnimaciones
V=tes_seres_poderosos
r(){ rm -rf videos/$V/medios/_tmp_scene-*; timeout 400 python fab.py $V bajar $1 "${@:2}" --rehacer < /dev/null 2>&1 | grep "scene-\|Error" | tail -1; }
r 152 --url https://www.youtube.com/watch?v=Uw12GYeN6a0 --desde 63
