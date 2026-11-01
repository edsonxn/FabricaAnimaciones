for id in O-TpCNK0iDA jtOfpZqVhok PQJXhyGI96w a23WEJ4Nu6A AGhJTwUG9xc 1TvlihcW6qg 5XTOT4f9Dyw u7xYngIwvjU 2lkFxNv85rg; do
  yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" -o "vid/$id.%(ext)s" --merge-output-format mp4 --no-part --quiet --no-progress "https://youtu.be/$id"
  echo "$id done"; sleep 4
done
echo ALLDONE
