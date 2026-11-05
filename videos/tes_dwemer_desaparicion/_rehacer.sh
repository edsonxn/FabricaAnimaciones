cd /c/FabricaAnimaciones
V=tes_dwemer_desaparicion
for a in "088|Skyrim Dwemer ruin 4k" "162|Morrowind Dagoth Ur" "167|Morrowind Yagrum Bagarn" "119|Skyrim Dwemer ruins 4k" "123|Skyrim Tiber Septim statue Solitude" "120|Skyrim Dwemer ruin hall" "117|Skyrim Dwemer automaton" "124|ESO Summerset 4k" "032|Skyrim Dwarven Centurion" "092|Skyrim Katria Arkngthamz" "114|Skyrim Tower of Mzark Drokt" "141|Morrowind Red Mountain 4k" "151|Morrowind Dwemer ruin 4k" "169|Morrowind Mournhold 4k" "182|Skyrim Blackreach 4k" "098|Skyrim Mzulft 4k" "126|Skyrim Time Wound Alduin"; do
  n=${a%%|*}; q=${a#*|}; timeout 400 python fab.py $V bajar $n --q "$q" --rehacer 2>&1 | grep "scene-" | tail -1
done
timeout 1500 python fab.py $V bajar 6,20,23,26,41,47,48,56,57,59,60,122 --rehacer -j 4 2>&1 | grep "scene-\|fallaron" | tail -14
python fab.py $V medios 2>&1 | tail -1
