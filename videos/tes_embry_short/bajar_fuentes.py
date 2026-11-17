"""Baja info (heatmap «lo más repetido»), subtítulos automáticos en español y comentarios
de los episodios de «Jugando Skyrim con IA» (serie de Embry) del canal Crónicas de Tamriel.
Uso: python bajar_fuentes.py   → fuentes/<id>.info.json, fuentes/<id>.es*.json3
"""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

AQUI = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(AQUI, "fuentes")
os.makedirs(DEST, exist_ok=True)

IDS = """RgBR0rzaDV0 wv96qet_WPs seDaeKwGrEI qf2-ozb7Sp8 IfnJY54veOg dcvtNMAAd4Q TGx-Bx-_nXA WciwTECJhy0
ihNO0fTCAxc 4z0d-aEBmNI p_fKwWhzLAU uWtMXyGcS2k cFSblV1y8A0 Fdqnh0kyhyU QFA-e6ZDutQ vrf77E0kalc
j3Vqdg0Hazg d0wRc1Zbcj0 ahCVWrwObGA zS13gjVUx04 qcbRYZjvzWk R-Lh0iEjiFM y4CqXQp0msU e9lUrKrRa00
cQ7KuDwOuuo zH27CqGlEZw g5yEICMSBFk 498JdFXBkKM BwaoxI4pvak 3mQFSt6URWQ B9hIVA08ha0 yvrmcxodjF4
FiSFtMYufBs hCvOqFnsSqU cNXZ0YpI20g x7-fVqovy0k Qo5zttGSrg0 vcMuOMaLD30 Yle9awlluks 4lF7N5xvyoc
t6fkAD2cvBI fi5FAH8dL00 _27NJXvulUM D5ByCjUVvZg jKE3FrQn5mQ WOdFQkGgfXk gNsJwAOKM6k vdzlv9O9oKY
_23CypM5KPA W-wvqapzn9o qo6aBSc9aBY Ky6z3MNeQj8 jG9LnSPKxPw""".split()


def bajar(vid):
    if os.path.exists(os.path.join(DEST, vid + ".info.json")):
        return vid, "ya"
    cmd = [sys.executable, "-m", "yt_dlp", "--skip-download", "--write-info-json", "--write-auto-subs",
           "--write-subs", "--sub-langs", "es-orig,es", "--sub-format", "json3", "--write-comments",
           "--extractor-args", "youtube:max_comments=200,all,0,0;comment_sort=top",
           "-o", os.path.join(DEST, "%(id)s.%(ext)s"), "https://www.youtube.com/watch?v=" + vid]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return vid, "ok" if r.returncode == 0 else r.stderr[-300:]


if __name__ == "__main__":
    with ThreadPoolExecutor(6) as ex:
        for vid, res in ex.map(bajar, IDS):
            print(vid, res, flush=True)
