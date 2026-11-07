#!/bin/bash
# Reintenta cada 90 s: (a) G2 en 480p del VOD de Twitch (VOD 5900-10899) -> vod_g2_480.mp4 ; (b) si sale antes el VOD de
# YouTube de LoL Esports (canal UC-I8d_BjKP6MMsYjZhAtjIA, «CFO vs KC … GAME 2»), lo baja entero en 480p -> vod_g2_yt480.mp4 (+ id en vod_g2_yt.txt)
cd "$(dirname "$0")"
for i in $(seq 1 80); do
  if yt-dlp -q --download-sections "*5900-10899" -f "480p/480p30/best[height<=480]" --ffmpeg-location C:/ffmpeg/bin \
      -o "vod_g2_480.%(ext)s" https://www.twitch.tv/videos/2914166111 > bajar_g2.log 2>&1; then
    echo "OK twitch $(date)"; exit 0; fi
  ID=$(yt-dlp --flat-playlist --playlist-end 4 --print "%(id)s %(title)s" "https://www.youtube.com/channel/UC-I8d_BjKP6MMsYjZhAtjIA/videos" 2>/dev/null | grep -i "CFO vs KC.*GAME 2" | cut -d' ' -f1)
  if [ -n "$ID" ]; then
    echo "$ID" > vod_g2_yt.txt
    yt-dlp -q -f "bv*[height<=480]+ba/b[height<=480]" --merge-output-format mp4 --ffmpeg-location C:/ffmpeg/bin -o "vod_g2_yt480.%(ext)s" "https://www.youtube.com/watch?v=$ID" >> bajar_g2.log 2>&1 && { echo "OK youtube $ID $(date)"; exit 0; }
  fi
  sleep 90
done
echo "FALLO"; exit 1
