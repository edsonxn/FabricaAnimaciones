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
1|Skyrim Konahrik spectral dragon priest summon vanilla
4|Skyrim Dragonborn daedric armor walking gameplay vanilla
5|Skyrim blacksmith forge crafting armor vanilla
10|Skyrim Visage of Mzund Breath of Nchuak ragdoll
20|Skyrim Masque of Clavicus Vile headless bug
30|Skyrim Ill Met by Moonlight Hircine reward Savior's Hide
31|Skyrim Savior's Hide vanilla
40|Skyrim Dawnguard Chasing Echoes Volkihar ruins Serana
57|Skyrim Ahzidal's Boots of Waterwalking walking on water
63|Skyrim The Lord Stone activate
87|Skyrim Spellbreaker ward block destruction spell
96|Skyrim Ancano boss fight Eye of Magnus
108|Skyrim Konahrik mask wearing vanilla
110|Skyrim Konahrik dragon priest ally fight
120|Skyrim Miraak's Robes tentacles
125|Skyrim Deathbrand armor vanilla
134|Skyrim Haknir's Shoal Deathbrand chest
135|Skyrim Ebony Mail vanilla showcase
136|Skyrim Ebony Mail heavy armor gameplay
138|Skyrim Ebony Mail poison cloak effect
143|Skyrim Lydia follower carry burdens
146|Skyrim Stalhrim armor vanilla
147|Skyrim stalhrim deposit Solstheim mining
157|Skyrim Dragon Armor perk smithing tree
166|Skyrim dragonplate armor vanilla showcase
170|Skyrim Daedric armor vanilla showcase
171|Skyrim daedric armor red glow vanilla
173|Skyrim daedra heart location Jorrvaskr
177|Skyrim heavy armor perks max armor rating daedric
181|Skyrim daedric boots no glow bug
183|Skyrim mage casting fire at warrior heavy armor
184|Skyrim armor rating 567 cap
185|Skyrim tempering armor grindstone legendary
186|Skyrim iron armor legendary tempered
190|Skyrim heavy armor Conditioning perk
191|Skyrim daedric armor Dragonsreach vanilla
193|Skyrim armor mannequins Breezehome display
EOF
echo REHACER_FIN
