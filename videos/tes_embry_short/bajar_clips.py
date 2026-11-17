"""Baja ventanas de 60 s (1080p) alrededor de cada candidato y las transcribe con Whisper
(palabra por palabra) para cortar exacto. â†’ segmentos/clips/<clave>.mp4 + <clave>.words.json
Uso: python bajar_clips.py [clave ...]
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

AQUI = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(AQUI, "segmentos", "clips")
os.makedirs(DEST, exist_ok=True)

# clave: (id, segundo del candidato)
CAND = {
    "pareja":     ("jG9LnSPKxPw", 6 * 60 + 45),
    "tiktok":     ("498JdFXBkKM", 42 * 60 + 15),
    "alcohol":    ("498JdFXBkKM", 2 * 60 + 35),
    "potencial":  ("498JdFXBkKM", 20 * 60 + 48),
    "pan":        ("4lF7N5xvyoc", 32 * 60 + 24),
    "hijas":      ("BwaoxI4pvak", 4 * 60 + 41),
    "dorthe":     ("dcvtNMAAd4Q", 4 * 60 + 50),
    "bolillo":    ("e9lUrKrRa00", 9 * 60 + 1),
    "parientes":  ("IfnJY54veOg", 13 * 60 + 13),
    "yelmo":      ("p_fKwWhzLAU", 8 * 60 + 20),
    "sombrero":   ("cFSblV1y8A0", 9 * 60 + 18),
    "diego":      ("Qo5zttGSrg0", 3 * 60 + 12),
    "fantasmas":  ("WOdFQkGgfXk", 36 * 60 + 0),
    "dormir":     ("qo6aBSc9aBY", 10 * 60 + 53),
    "prefieres":  ("qo6aBSc9aBY", 17 * 60 + 35),
    "orca":       ("vdzlv9O9oKY", 4 * 60 + 40),
    "trio":       ("vdzlv9O9oKY", 5 * 60 + 50),
    "computadora": ("_27NJXvulUM", 2 * 60 + 18),
    "dignidad":   ("TGx-Bx-_nXA", 7 * 60 + 39),
    "alfalfa":    ("gNsJwAOKM6k", 4 * 60 + 43),
    "roniosos":   ("Ky6z3MNeQj8", 0 * 60 + 21),
    "caldo":      ("vcMuOMaLD30", 40 * 60 + 33),
    "fracaso":    ("qf2-ozb7Sp8", 14 * 60 + 54),
    "pajaro":     ("x7-fVqovy0k", 22 * 60 + 59),
    "autografo":  ("vrf77E0kalc", 21 * 60 + 22),
}
ANTES, DESPUES = 28, 32


def bajar(clave):
    vid, t = CAND[clave]
    out = os.path.join(DEST, clave + ".mp4")
    if not os.path.exists(out):
        a, b = max(0, t - ANTES), t + DESPUES
        cmd = [sys.executable, "-m", "yt_dlp", "-f", "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080]",
               "--download-sections", "*%d-%d" % (a, b), "--force-keyframes-at-cuts", "--merge-output-format", "mp4",
               "-o", out, "https://www.youtube.com/watch?v=" + vid]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            return clave, "ERROR " + r.stderr[-300:]
    return clave, "ok"


def transcribir(claves):
    from faster_whisper import WhisperModel
    m = WhisperModel("medium", device="cuda", compute_type="int8_float16")
    for c in claves:
        js = os.path.join(DEST, c + ".words.json")
        if os.path.exists(js):
            continue
        segs, _ = m.transcribe(os.path.join(DEST, c + ".mp4"), language="es", word_timestamps=True,
                               vad_filter=True)
        out = []
        for s in segs:
            out.append({"a": round(s.start, 2), "b": round(s.end, 2), "t": s.text.strip(),
                        "w": [[round(w.start, 2), round(w.end, 2), w.word] for w in s.words]})
        json.dump(out, open(js, "w", encoding="utf-8"), ensure_ascii=False)
        print("transcrito", c, flush=True)


if __name__ == "__main__":
    claves = sys.argv[1:] or list(CAND)
    with ThreadPoolExecutor(5) as ex:
        for c, r in ex.map(bajar, claves):
            print(c, r, flush=True)
    transcribir([c for c in claves if os.path.exists(os.path.join(DEST, c + ".mp4"))])

