# Baja la OST oficial de los CoD clásicos a <slug>.wav según _catalogo.txt («id slug<TAB>descripción»)
cd "$(dirname "$0")"
while IFS=$'\t' read -r cab desc; do
  id=${cab%% *}; s=${cab#* }
  [ -f "$s.wav" ] && continue
  yt-dlp -q -x --audio-format wav -o "$s.%(ext)s" "https://youtu.be/$id" && echo "ok $s" || echo "x $s"
done < _catalogo.txt
