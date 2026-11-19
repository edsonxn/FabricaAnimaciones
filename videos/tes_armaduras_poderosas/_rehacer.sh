#!/bin/bash
# Rehace los clips malos de _rehacer.txt con una búsqueda nueva (lo que dice la voz en ese beat). 18-nov-2026, s2.
#   bash _rehacer.sh > _rehacer.log 2>&1      (desde la carpeta del video; SOLO=12,15 bash _rehacer.sh = solo esos)
# OJO: python sin `< /dev/null` se come el heredoc del bucle (pasó el 19-nov: 12 beats saltados).
cd "$(dirname "$0")/../.."
NC=" no commentary"
while IFS='|' read -r id q; do
  [ -z "$id" ] && continue
  if [ -n "$SOLO" ] && ! echo ",$SOLO," | grep -q ",$id,"; then continue; fi
  echo "=== $id  $q"
  python fab.py tes_armaduras_poderosas bajar "$id" --q "$q$NC" < /dev/null 2>&1 | grep -E "scene-|falt|Error|error" | tail -2
done <<'EOF'
1|Skyrim Konahrik dragon priest summoned
4|Skyrim armor showcase vanilla
5|Skyrim iron armor smithing grindstone
9|Skyrim Breath of Nchuak shout
10|Skyrim Breath of Nchuak kill enemies
16|Skyrim Barbas talking dog Falkreath
20|Skyrim Clavicus Vile shrine Barbas reunion
22|Skyrim Eorlund Gray-Mane Skyforge Wuuthrad
25|Skyrim Shield of Ysgramor block
26|Skyrim courier delivers letter
27|Skyrim Bannered Mare bard
30|Skyrim Savior's Hide armor
31|Skyrim Savior's Hide light armor showcase
32|Skyrim Ill Met by Moonlight Sinding
39|Skyrim Vampire Royal Armor showcase
40|Skyrim Castle Volkihar ruins Serana
49|Skyrim brawl fist fight Whiterun
50|Skyrim Ahzidal's armor showcase
57|Skyrim catch fish by hand
63|Skyrim Lord Stone
67|Skyrim Guild Master armor enchantment
78|Skyrim Hag's End Deepwood Redoubt
87|Skyrim Spellbreaker ward dragon breath
88|Skyrim armor mannequin display
90|Skyrim Jagged Crown
92|Skyrim Falmer heavy armor
96|Skyrim Ancano fight Hall of the Elements
97|Skyrim Archmage's Robes
100|Skyrim Nightingale armor vanilla
105|Skyrim Nightingale armor showcase
108|Skyrim Konahrik mask equipped
109|Skyrim Konahrik fire cloak low health
110|Skyrim spectral dragon priest Konahrik
118|Skyrim Miraak's Robes showcase
119|Skyrim Miraak tentacles explosion
120|Skyrim Miraak mask
121|Skyrim Miraak boss fight
125|Skyrim Deathbrand armor showcase
127|Skyrim Deathbrand treasure map chest
129|Skyrim Deathbrand helm
133|Skyrim Gyldenhul Barrow gold
134|Skyrim Ebony Mail showcase
135|Skyrim Ebony Mail Boethiah
136|Skyrim Ebony Mail vs Daedric armor comparison
137|Skyrim Ebony Mail poison cloak
138|Skyrim Ebony Mail smoke effect
139|Skyrim Boethiah's Calling quest
143|Skyrim follower carrying items
146|Skyrim stalhrim deposit mining
147|Skyrim Stalhrim heavy armor
149|Skyrim A New Source of Stalhrim Deor
157|Skyrim Light Armor perk tree
166|Skyrim dragonplate armor smithing
167|Skyrim dragon bone Dawnguard
170|Skyrim Daedric Armor showcase
171|Skyrim Dremora daedra heart
172|Skyrim daedra heart Jorrvaskr
173|Skyrim Atronach Forge
175|Skyrim Atronach Forge daedric armor
177|Skyrim daedric armor full set
180|Skyrim daedric boots glitch
181|Skyrim iron armor
183|Skyrim armor rating explained
184|Skyrim armor rating cap
185|Skyrim iron armor legendary
186|Skyrim giant club smash
188|Skyrim Conditioning perk heavy armor
190|Skyrim iron armor showcase
191|Skyrim Breath of Nchuak dwemer helmet
193|Skyrim armor collection display
EOF
echo REHACER_FIN
