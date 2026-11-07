#!/bin/sh
# nombre vid desde hasta: tramo 1080p H.264 con yt-dlp --download-sections (cuando ffmpeg sobre la URL da 403)
cd /c/FabricaAnimaciones/videos/lol_semana2/medios/_fuente
[ -f "$1.mp4" ] && exit 0
yt-dlp -q --no-warnings --ffmpeg-location /c/ffmpeg/bin -f "bv*[height<=1080][vcodec^=avc1]+ba/bv*[height<=1080]+ba/b" --download-sections "*$3-$4" --force-keyframes-at-cuts --merge-output-format mp4 -o "$1.%(ext)s" "https://youtu.be/$2" 2>&1 | tail -2
ls -la "$1.mp4"
