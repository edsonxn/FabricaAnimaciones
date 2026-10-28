# python lp_txt.py Pagina salida.txt  -> texto renderizado de Liquipedia (API parse)
import json, sys, urllib.request, urllib.parse, re, html, gzip
p, out = sys.argv[1], sys.argv[2]
u = "https://liquipedia.net/leagueoflegends/api.php?action=parse&format=json&formatversion=2&prop=text&page=" + urllib.parse.quote(p)
r = urllib.request.Request(u, headers={"User-Agent": "FabricaAnimaciones-research/1.0", "Accept-Encoding": "gzip"})
raw = urllib.request.urlopen(r, timeout=30).read()
try: raw = gzip.decompress(raw)
except Exception: pass
d = json.loads(raw)
h = d["parse"]["text"]
open(out.replace(".txt", ".html"), "w", encoding="utf-8").write(h)
h = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", h, flags=re.S)
h = re.sub(r"<img[^>]*alt=\"([^\"]*)\"[^>]*>", r" [\1] ", h)
h = re.sub(r"<(br|/tr|/p|/li|/h\d|/div)[^>]*>", "\n", h)
h = re.sub(r"</t[dh]>", " | ", h)
t = html.unescape(re.sub(r"<[^>]+>", "", h))
t = re.sub(r"[ \t]+", " ", t)
t = re.sub(r"\n\s*\n+", "\n", t)
open(out, "w", encoding="utf-8").write(t)
print(out, len(t))
