# -*- coding: utf-8 -*-
"""Etapa final: salida/video_sin_audio.mp4 + audio/final.wav ->
   salida/<titulo>_MASTER.mp4 (video sin recomprimir, AAC 320k),
   salida/<titulo>.srt  (+ salida/<titulo>_WHATSAPP.mp4 720p solo si FAB_WHATSAPP=1)"""
import json
import os
import re
import subprocess
import unicodedata

import config

TL = json.load(open("timeline.json", encoding="utf-8"))


def slug(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")[:60] or "video"


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def srt(ruta):
    def ts(x):
        h, r = divmod(x, 3600)
        m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"
    if not any(e["frases"] for e in TL["escenas"]):   # SIN_VOZ (novela): sin narrador; el .srt sale de Whisper y no se pisa
        if not os.path.exists(ruta):
            open(ruta, "w", encoding="utf-8").close()
        return
    n = 0
    with open(ruta, "w", encoding="utf-8") as f:
        for e in TL["escenas"]:
            for fr in e["frases"]:
                n += 1
                f.write(f"{n}\n{ts(fr['t0'])} --> {ts(fr['t1'])}\n{fr['texto']}\n\n")


def pantalla_final():
    """Clip de salida del canal (13-oct-2026): PANTALLA_FINAL en guion.py (None/"" = sin) o «pantalla_final» de
    canales/<alias>.json, con el alias de la línea «- canal:» del ESTADO.md. Lleva su propio audio."""
    import guion
    if hasattr(guion, "PANTALLA_FINAL"):
        r = guion.PANTALLA_FINAL
    else:
        r, alias = None, None
        if os.path.exists("ESTADO.md"):
            m = re.search(r"^- canal:\s*([\w-]+)", open("ESTADO.md", encoding="utf-8").read(), re.M)
            alias = m and m.group(1)
        ficha = os.path.join("..", "..", "canales", f"{alias}.json")
        if alias and os.path.exists(ficha):
            r = json.load(open(ficha, encoding="utf-8")).get("pantalla_final")
    if r and not os.path.exists(r):
        print(f"AVISO: no existe la pantalla final {r} (¿E: desconectado?): el MASTER sale sin ella")
        return None
    return r or None


def sondear(ruta):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate,profile,color_primaries", "-of", "json", ruta],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)["streams"][0]


def anexar_pantalla(master, pf):
    """MASTER + pantalla final sin recomprimir el video: la pantalla se codifica con los parámetros del render
    (libx264 medium crf 18 yuv420p, mismo tamaño, fps y perfil) y se une con el concat demuxer."""
    v = sondear(master)
    w, h, fps = v["width"], v["height"], v["r_frame_rate"]
    col = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"] if v.get("color_primaries") == "bt709" else []
    pf_tmp, lst, out = master + ".pf.mp4", master + ".lista.txt", master + ".con_pf.mp4"
    ff("-i", pf, "-vf", f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,fps={fps},format=yuv420p",
       "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", (v.get("profile") or "high").lower(), *col,
       "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2", "-shortest", pf_tmp)
    with open(lst, "w", encoding="utf-8") as f:
        f.write(f"file '{os.path.abspath(master)}'\nfile '{os.path.abspath(pf_tmp)}'\n".replace("\\", "/"))
    ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", out)
    os.replace(out, master)
    for x in (pf_tmp, lst):
        os.remove(x)
    print(f"pantalla final anexada: {os.path.basename(pf)}")


def main():
    titulo = TL.get("titulo") or os.path.basename(os.getcwd())
    base = os.path.join("salida", config.ARCHIVO or slug(titulo))
    master, wa = base + "_MASTER.mp4", base + "_WHATSAPP.mp4"
    # fuente de video: el render sin audio; si ya se limpió, la pista de video del MASTER anterior
    fuente = "salida/video_sin_audio.mp4"
    if not os.path.exists(fuente):
        if not os.path.exists(master):
            raise SystemExit("Falta salida/video_sin_audio.mp4: corre antes 'python fab.py <video> video'")
        fuente = base + "_video_previo.mp4"
        os.replace(master, fuente)
    tmp = master + ".tmp.mp4"
    dur = TL["total"]
    # -t: si la fuente es un MASTER anterior, ya traía la pantalla final; se corta para no anexarla dos veces
    ff("-i", fuente, "-i", "audio/final.wav", "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-t", f"{dur:.3f}",
       "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-metadata", f"title={titulo}", tmp)
    os.replace(tmp, master)
    if fuente.endswith("_video_previo.mp4"):
        os.remove(fuente)
    pf = pantalla_final()
    if pf:
        anexar_pantalla(master, pf)
    if not os.environ.get("FAB_WHATSAPP"):
        wa = None
    vbr = int(max(700, min(3500, (52 * 8 * 1024 * 1024 / dur - 128_000) / 1000)))
    log = os.path.join("salida", "wa2pass")
    comun = [] if wa is None else ["-i", master, "-vf", "scale=1280:720:flags=lanczos", "-c:v", "libx264", "-preset", "slow", "-b:v", f"{vbr}k"]
    if wa is not None:
        ff(*comun, "-pass", "1", "-passlogfile", log, "-an", "-f", "mp4", os.devnull)
    if wa is not None:
        ff(*comun, "-maxrate", f"{int(vbr * 1.5)}k", "-bufsize", f"{vbr * 3}k", "-pass", "2", "-passlogfile", log,
       "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
       "-movflags", "+faststart", wa)
    for x in os.listdir("salida"):
        if x.startswith("wa2pass"):
            os.remove(os.path.join("salida", x))
    srt(base + ".srt")
    for r in [x for x in (master, wa, base + ".srt") if x]:
        print(f"{r}  {os.path.getsize(r) / 1e6:.1f} MB")
    # video_sin_audio.mp4 se borra (el concat de segmentos lo rehace en segundos). segmentos/ se CONSERVA (desde
    # 2026-10-04) para corregir una toma sin re-renderizar todo: `fab.py <v> video --rehacer 270-280` + `final`.
    # Se borran con `fab.py <v> limpiar` cuando el video está aprobado/subido (o FAB_LIMPIAR=1 aquí mismo).
    if os.path.exists("salida/video_sin_audio.mp4") and not os.environ.get("FAB_CONSERVAR"):
        os.remove("salida/video_sin_audio.mp4")
    if os.path.isdir("segmentos"):
        if os.environ.get("FAB_LIMPIAR"):
            import shutil
            shutil.rmtree("segmentos", ignore_errors=True)
            print("segmentos/ borrados; el MASTER conserva el video")
        else:
            mb = sum(os.path.getsize(os.path.join("segmentos", x)) for x in os.listdir("segmentos")) / 1e6
            print(f"segmentos/ conservados ({mb:.0f} MB) para arreglos por tramos (`video --rehacer t0-t1`); "
                  f"bórralos con `python fab.py <video> limpiar` cuando el video esté aprobado")


if __name__ == "__main__":
    main()
