# -*- coding: utf-8 -*-
"""Remake ANIME de «Llamada de domingo»: una Toma de anime_vivo por plano clip/llamada/img → medios/scene-NNN.mp4.
  python tomas.py                 todos los planos que falten (en paralelo, N procesos)
  python tomas.py scene-005 …     solo esos (rehace)
  python tomas.py hoja scene-005  hoja de cuadros (previews/_tomas/<scene>.jpg)
  python tomas.py ensamblar       85 tramos (ui = recortes del MASTER original) + audio final del original → MASTER
Labios: audio del plano del original (../llamada_domingo/medios/scene-NNN.mp4). Planos llamada: interfaz de ui.py."""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(AQUI, "..", "llamada_domingo")
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
import anime_vivo as AV  # noqa: E402

FF = r"C:\ffmpeg\bin\ffmpeg.exe"
MED = os.path.join(AQUI, "medios")
TMP = os.path.join(AQUI, "flow", "_render")      # en C: (E: falla a ratos)
BEATS = {b["id"]: b for b in json.load(open(os.path.join(ORIG, "beats.json"), encoding="utf-8"))}
ELEG = dict(l.split() for l in open(os.path.join(AQUI, "flow", "_elegidasB.txt")) if l.strip())
COPIA = {"scene-001": "puerta_dia", "scene-026": "plaza", "scene-040": "cocina", "scene-059": "hospital_ext",
         "scene-068": "puerta"}
SEGUNDO = {"scene-014": "scene-014b", "scene-032": "scene-032b", "scene-069": "scene-069b"}
LLORA = {"scene-074", "scene-077", "scene-073", "scene-053"}


def _g():
    import importlib.util
    s = importlib.util.spec_from_file_location("g", os.path.join(ORIG, "guion.py"))
    g = importlib.util.module_from_spec(s)
    s.loader.exec_module(g)
    return g


G = _g()
PL = {f"scene-{i + 1:03d}": p for i, p in enumerate(G.PLANOS)}


def base(k):
    if k in COPIA:
        return os.path.join(AQUI, "flow", "a", f"esc_{COPIA[k]}_a.jpg")
    return os.path.join(AQUI, "flow", "b", f"{k}_{ELEG[k]}.jpg")


def var(k, t):
    r = [os.path.join(AQUI, "flow", "e", f"{k}_{t}_{v}.jpg") for v in (0, 1)]
    return [x for x in r if os.path.exists(x)]


def fx_de(esc, k):
    n = int(k[6:9])
    if esc in ("taller", "taller_perfecto", "perfecto"):
        return [("rayos", dict(origen=(0.95, -0.05), ang=125)), ("polvo", dict(caja=(0.5, 0.0, 1.0, 0.8)))]
    if esc in ("pasillo", "hospital"):
        return [("fluor", dict())]
    if esc in ("oficina", "depto"):
        return [("brillo", dict(pos=(0.5, 0.7), r=0.25, color=(150, 200, 255), op=0.12))]
    if esc in ("plaza", "porche", "puerta_dia"):
        return [("polvo", dict(caja=(0.0, 0.0, 1.0, 0.7), color=(255, 240, 200), op=0.4))]
    if esc in ("taxi", "auto_lucia"):
        return [("lluvia", dict(caja=(0.0, 0.0, 1.0, 0.6), n=120, op=0.2))]
    if esc == "cocina":
        return [("brillo", dict(pos=(0.45, 0.15), r=0.2, op=0.18))]
    return [("polvo", dict(n=40, op=0.3))] if n % 2 else []


def cam_de(k, habla):
    n = int(k[6:9]) + (7 if k.endswith("b") else 0)
    tipos = [dict(z0=1.0, z1=1.12, c0=(0.5, 0.5), c1=(0.52, 0.42)),
             dict(z0=1.1, z1=1.02, c0=(0.48, 0.42), c1=(0.5, 0.5)),
             dict(z0=1.04, z1=1.1, c0=(0.42, 0.48), c1=(0.58, 0.45)),
             dict(z0=1.04, z1=1.1, c0=(0.58, 0.48), c1=(0.42, 0.45))]
    c = dict(tipos[n % 4])
    if habla:
        c["z1"] = c["z1"] + 0.04
    return c


def toma(k, esc, habla, seed):
    mov = "tiembla" if k[:9] in LLORA else ("cabeceo" if habla else "respira")
    return AV.Toma(base(k), bocas=var(k, "boca"), ojos=var(k, "ojos"), cam=cam_de(k, habla), fx=fx_de(esc, k), mov=mov,
                   personaje=bool(PL[k[:9]].get("personajes")), seed=seed)


def corte_dialogo(audio, dur, frac):
    """Instante del silencio entre la 1.ª y la 2.ª frase (el más cercano a dur*frac)."""
    env = AV.envolvente(audio, dur)
    fps = AV.FPS
    hab = env > 0.12
    huecos, i = [], 0
    while i < len(hab):
        if not hab[i]:
            j = i
            while j < len(hab) and not hab[j]:
                j += 1
            if j - i >= int(0.18 * fps) and i > 0 and j < len(hab):
                huecos.append((i + j) / 2 / fps)
            i = j
        else:
            i += 1
    if not huecos:
        return dur * frac
    return min(huecos, key=lambda t: abs(t - dur * frac))


def hacer(k):
    p = PL[k]
    b = BEATS[k]
    dur = b["t1"] - b["t0"]
    audio = os.path.join(ORIG, "medios", k + ".mp4")
    a_t0 = 0.0
    if not os.path.exists(audio):                    # planos img: el original era un .jpg → audio final del tramo
        audio, a_t0 = os.path.join(ORIG, "audio", "final.wav"), b["t0"]
    habla = bool(p.get("dialogo")) and p["tipo"] in ("clip", "llamada")
    esc = p.get("esc") or COPIA.get(k, "")
    tms = [(0.0, toma(k, esc, habla, int(k[6:9])))]
    if k in SEGUNDO and len(p["dialogo"]) >= 2:
        l1, l2 = len(p["dialogo"][0][1]), sum(len(d[1]) for d in p["dialogo"][1:])
        tc = corte_dialogo(audio, dur, l1 / (l1 + l2))
        tms.append((tc, toma(SEGUNDO[k], esc, True, int(k[6:9]) + 50)))
    llam = p["tipo"] == "llamada"
    os.makedirs(MED, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    sal = os.path.join(TMP, k + "_crudo.mp4") if llam else os.path.join(MED, k + ".mp4")
    AV.render(tms, dur, sal, audio=audio, audio_t0=a_t0, mux_audio=True, seed=int(k[6:9]))
    if llam:
        envolver_llamada(k)
    return k


def envolver_llamada(k):
    sys.path.insert(0, ORIG)
    import ui
    from PIL import Image
    ui.MEDIOS = MED
    ui.PREV = TMP
    ui.CACHE = os.path.join(TMP, "ui_cache")
    os.makedirs(os.path.join(TMP, "originales"), exist_ok=True)
    os.replace(os.path.join(TMP, k + "_crudo.mp4"), os.path.join(TMP, "originales", k + "_crudo.mp4"))

    def cara(quien):
        im = Image.open(os.path.join(AQUI, "flow", "a", f"pj_{quien.split('_')[0]}_a.jpg")).convert("RGB")
        w, h = im.size
        return im.crop(((w - h) // 2, 0, (w + h) // 2, h))
    ui.cara = cara
    ui.llamada(k)


def hacer_seguro(k):
    try:
        return "✓ " + hacer(k)
    except Exception as e:  # noqa: BLE001
        return f"✗ {k}: {e}"


def planos():
    return [k for k, p in PL.items() if p["tipo"] in ("clip", "llamada", "img")]


def hoja(k):
    p = PL[k]
    dur = BEATS[k]["t1"] - BEATS[k]["t0"]
    t = toma(k, p.get("esc") or COPIA.get(k, ""), bool(p.get("dialogo")), 1)
    os.makedirs(os.path.join(AQUI, "flow", "_tomas"), exist_ok=True)
    AV.cuadros([(0, t)], dur, [0.5, dur * 0.35, dur * 0.65, dur - 0.5], os.path.join(AQUI, "flow", "_tomas", k + ".jpg"),
               audio=os.path.join(ORIG, "medios", k + ".mp4"))


def ensamblar():
    """Concatena los 85 tramos a 30 fps exactos y pone el audio final del original."""
    master_o = os.path.join(ORIG, "salida", "llamada_de_domingo_MASTER.mp4")
    lst = os.path.join(TMP, "concat.txt")
    seg = os.path.join(TMP, "seg")
    os.makedirs(seg, exist_ok=True)
    lineas = []
    for k in sorted(BEATS):
        b = BEATS[k]
        dur = b["t1"] - b["t0"]
        dst = os.path.join(seg, k + ".mp4")
        if PL[k]["tipo"] == "ui":
            cmd = [FF, "-y", "-v", "error", "-ss", f"{b['t0']:.3f}", "-i", master_o, "-t", f"{dur:.3f}"]
        else:
            cmd = [FF, "-y", "-v", "error", "-i", os.path.join(MED, k + ".mp4"), "-t", f"{dur:.3f}"]
        cmd += ["-an", "-vf", f"scale=1920:1080:flags=lanczos,fps=30,tpad=stop_mode=clone:stop_duration=1",
                "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", dst]
        subprocess.run(cmd, check=True)
        lineas.append(f"file '{dst}'")
    open(lst, "w").write("\n".join(lineas).replace("\\", "/"))
    v = os.path.join(TMP, "video.mp4")
    subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", v], check=True)
    out = os.path.join(AQUI, "salida", "llamada_de_domingo_anime_MASTER.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run([FF, "-y", "-v", "error", "-i", v, "-i", os.path.join(ORIG, "audio", "final.wav"), "-map", "0:v",
                    "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags",
                    "+faststart", out], check=True)
    print(out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # el log redirigido es cp1252 y «✓» lo tumbaba
    a = sys.argv[1:]
    if a and a[0] == "hoja":
        for k in a[1:]:
            hoja(k)
    elif a and a[0] == "ensamblar":
        ensamblar()
    else:
        todo = a or [k for k in planos() if not os.path.exists(os.path.join(MED, k + ".mp4"))]
        n = int(os.environ.get("PROCS", "6"))
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(n) as ex:
            for r in ex.map(hacer_seguro, todo):
                print(r, flush=True)
