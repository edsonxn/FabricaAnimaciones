#!/bin/bash
# Rehace los clips malos de _rehacer.txt (revisión de hojas 26-nov). bash _rehacer.sh > _rehacer.log 2>&1
cd "$(dirname "$0")/../.."
while IFS="|" read -r id mot q; do
  id=$(echo $id); q=$(echo $q); [ -z "$id" ] && continue
  echo "=== $id  $q"
  python fab.py tes_pierdes_siempre bajar "${id#scene-}" --q "$q no commentary" < /dev/null 2>&1 | grep -E "scene-|falt|Error|error" | tail -2
done < videos/tes_pierdes_siempre/_rehacer.txt
echo REHACER_FIN
