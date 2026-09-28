#!/usr/bin/env bash
# Descarga robusta del modelo T3 de Chatterbox (2.14 GB) en 8 partes paralelas y reanudables,
# verifica su SHA-256 y lo coloca en la caché de HuggingFace. Uso: bash modelos/bajar_t3.sh
URL=https://huggingface.co/ResembleAI/chatterbox/resolve/main/t3_mtl23ls_v3.safetensors
SHA=5abca8321ede76f8e61f1cc0d19aea6c946b28871017ce8726f8a69203f05953
TOTAL=2143989928
N=8
D=/c/FabricaAnimaciones/modelos/_descarga
H=~/.cache/huggingface/hub/models--ResembleAI--chatterbox
mkdir -p "$D"
chunk=$(( (TOTAL + N - 1) / N ))
for i in $(seq 0 $((N - 1))); do
  a=$((i * chunk)); b=$(( (i + 1) * chunk - 1 )); [ $b -ge $TOTAL ] && b=$((TOTAL - 1))
  need=$((b - a + 1))
  (
    while true; do
      have=$(stat -c %s "$D/p$i" 2>/dev/null || echo 0)
      [ "$have" -ge "$need" ] && break
      curl -sS -L --connect-timeout 20 --speed-limit 20000 --speed-time 30 -r $((a + have))-$b "$URL" >> "$D/p$i" || sleep 3
    done
  ) &
done
wait
cat "$D"/p0 "$D"/p1 "$D"/p2 "$D"/p3 "$D"/p4 "$D"/p5 "$D"/p6 "$D"/p7 > "$D/t3.bin"
got=$(sha256sum "$D/t3.bin" | cut -d' ' -f1)
if [ "$got" != "$SHA" ]; then echo "SHA256 NO COINCIDE: $got"; exit 1; fi
mv "$D/t3.bin" "$H/blobs/$SHA"
rm -f "$H"/blobs/$SHA.*.incomplete
snap=$(ls -d "$H"/snapshots/*/ | head -1)
( cd "$snap" && ln -sf "../../blobs/$SHA" t3_mtl23ls_v3.safetensors )
rm -rf "$D"
echo "MODELO LISTO"
