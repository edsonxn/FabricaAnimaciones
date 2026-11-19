#!/bin/bash
# Baja cada clip de _efectos_vivos.txt en su segundo exacto (el efecto FUNCIONANDO, regla del 19-nov-2026). Log: _efectos_vivos.log
cd "$(dirname "$0")/../.."
grep -v '^#' videos/tes_armaduras_poderosas/_efectos_vivos.txt | while IFS='|' read -r id url desde que; do
  [ -z "$id" ] && continue
  echo "=== $id @$desde  $que"
  python fab.py tes_armaduras_poderosas bajar "$((10#$id))" --url "$url" --desde "$desde" < /dev/null 2>&1 | grep -E "scene-|falt|Error|error" | tail -2
done
echo VIVOS_FIN
