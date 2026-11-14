"""Comprime un video a una copia más liviana SIN tocar el original.

Uso:
  python .claude/skills/comprimir-video/comprimir.py <archivo.mp4 | carpeta | alias_de_video> [opciones]

  <alias_de_video>  p. ej. historia_egipto  -> busca videos/historia_egipto/salida/*_MASTER.mp4
  <carpeta>         comprime los *_MASTER.mp4 que tenga (o todos los .mp4 si no hay MASTER)

Opciones:
  --perfil P        ligero (defecto) | compartir | minimo | archivo   (ver PERFILES)
  --mb N            tamaño objetivo en MB (dos pasadas; ignora la CRF del perfil)
  --res N           lado corto en px (1080, 720, 480...). Vale igual para horizontal y vertical.
                    Nunca agranda.
  --codec C         h264 | h265
  --crf N           calidad (menor = mejor y más pesado)
  --audio K         kbps de audio AAC
  --gpu             NVENC (RTX 4060): 5-10x más rápido, algo más pesado a igual calidad
  --sufijo S        defecto _ligero  (X_MASTER.mp4 -> X_ligero.mp4; nunca coincide con *_MASTER.mp4)
  --sobrescribir    rehace la copia si ya existe

Salida: junto al original. Si la copia no baja al menos 5 % se borra y se avisa.
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
FFMPEG_DIR = r"C:\ffmpeg\bin"
FFMPEG = shutil.which("ffmpeg") or os.path.join(FFMPEG_DIR, "ffmpeg.exe")
FFPROBE = shutil.which("ffprobe") or os.path.join(FFMPEG_DIR, "ffprobe.exe")

# codec, crf, preset x264/x265, lado corto (None = igual), audio kbps
PERFILES = {
    "ligero":    dict(codec="h264", crf=23, preset="slow",   res=None, audio=128),  # mismo aspecto, ~1/3 del peso
    "compartir": dict(codec="h264", crf=25, preset="slow",   res=720,  audio=96),   # WhatsApp/correo/revisión
    "minimo":    dict(codec="h265", crf=30, preset="medium", res=720,  audio=64),   # lo más chico que aún se ve bien
    "archivo":   dict(codec="h265", crf=22, preset="medium", res=None, audio=160),  # guardar en disco casi sin pérdida
}


def mb(n):
    return n / (1024 * 1024)


def sondear(ruta):
    out = subprocess.run([FFPROBE, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", ruta],
                         capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    a = any(s["codec_type"] == "audio" for s in d["streams"])
    if v is None:
        sys.exit(f"✗ {ruta} no tiene pista de video")
    return dict(dur=float(d["format"]["duration"]), w=int(v["width"]), h=int(v["height"]),
                kbps=int(d["format"].get("bit_rate", 0)) // 1000, codec=v["codec_name"], audio=a)


def resolver_entradas(arg, sufijo):
    if os.path.isfile(arg):
        return [os.path.abspath(arg)]
    carpeta = arg
    if not os.path.isdir(carpeta):
        cand = os.path.join(RAIZ, "videos", arg, "salida")
        if os.path.isdir(cand):
            carpeta = cand
        else:
            sys.exit(f"✗ No encuentro «{arg}» (ni como archivo, ni carpeta, ni videos/{arg}/salida)")
    elif os.path.isdir(os.path.join(carpeta, "salida")):
        carpeta = os.path.join(carpeta, "salida")
    vids = sorted(glob.glob(os.path.join(carpeta, "*_MASTER.mp4")))
    if not vids:
        vids = sorted(p for p in glob.glob(os.path.join(carpeta, "*.mp4"))
                      if not os.path.splitext(p)[0].endswith(sufijo))
    if not vids:
        sys.exit(f"✗ No hay .mp4 en {carpeta}")
    return [os.path.abspath(p) for p in vids]


def nombre_salida(ruta, sufijo):
    base, _ = os.path.splitext(ruta)
    if base.endswith("_MASTER"):
        base = base[: -len("_MASTER")]
    return base + sufijo + ".mp4"


def filtro_escala(info, res):
    if not res or min(info["w"], info["h"]) <= res:
        return None
    return f"scale=-2:{res}:flags=lanczos" if info["w"] >= info["h"] else f"scale={res}:-2:flags=lanczos"


def args_video(cfg, gpu, vkbps, pasada):
    """Argumentos de codificación de video. vkbps = objetivo (modo --mb) o None (modo calidad)."""
    h265 = cfg["codec"] == "h265"
    if gpu:
        a = ["-c:v", "hevc_nvenc" if h265 else "h264_nvenc", "-preset", "p7", "-tune", "hq",
             "-rc", "vbr", "-multipass", "fullres", "-spatial-aq", "1", "-temporal-aq", "1"]
        if vkbps:
            a += ["-b:v", f"{vkbps}k", "-maxrate", f"{int(vkbps * 1.5)}k", "-bufsize", f"{vkbps * 2}k"]
        else:
            a += ["-cq", str(cfg["crf"] + (1 if h265 else 0)), "-b:v", "0"]
    else:
        a = ["-c:v", "libx265" if h265 else "libx264", "-preset", cfg["preset"]]
        if vkbps:
            a += ["-b:v", f"{vkbps}k"]
            if h265:
                # rutas relativas: el «:» de C:\ rompe -x265-params (ffmpeg corre con cwd = temporal)
                a += ["-x265-params", f"pass={pasada}:stats=x265_2pass.log:log-level=error"]
            else:
                a += ["-pass", str(pasada), "-passlogfile", "x264_2pass"]
        else:
            a += ["-crf", str(cfg["crf"])]
            if h265:
                a += ["-x265-params", "log-level=error"]
    if h265:
        a += ["-tag:v", "hvc1"]  # para que lo abran QuickTime/iPhone
    return a + ["-pix_fmt", "yuv420p"]


def correr(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd)
    if r.returncode != 0:
        sys.exit(f"✗ ffmpeg falló (código {r.returncode})")


def comprimir(ruta, cfg, gpu, mb_obj, sufijo, sobrescribir):
    salida = nombre_salida(ruta, sufijo)
    if os.path.exists(salida) and not sobrescribir:
        print(f"• Ya existe {os.path.basename(salida)} ({mb(os.path.getsize(salida)):.0f} MB); usa --sobrescribir")
        return
    info = sondear(ruta)
    peso0 = os.path.getsize(ruta)
    print(f"\n▶ {os.path.basename(ruta)}  {mb(peso0):.0f} MB · {info['w']}x{info['h']} {info['codec']} · "
          f"{info['dur']:.0f} s · {info['kbps']} kbps")

    vf = filtro_escala(info, cfg["res"])
    comunes = ["-map", "0:v:0", "-map", "0:a?", "-map_metadata", "0"] + (["-vf", vf] if vf else [])
    audio = ["-c:a", "aac", "-b:a", f"{cfg['audio']}k"] if info["audio"] else []

    vkbps = None
    if mb_obj:
        total = mb_obj * 8 * 1024 * 1024 / info["dur"] / 1000 * 0.97  # 3 % de margen del contenedor
        vkbps = int(total - (cfg["audio"] if info["audio"] else 0))
        if vkbps < 150:
            sys.exit(f"✗ {mb_obj} MB es demasiado poco para {info['dur']:.0f} s (saldría a {vkbps} kbps de video)")

    tmp = tempfile.mkdtemp(prefix="comprimir_")
    parcial = os.path.join(tmp, "salida.mp4")
    t0 = time.time()
    try:
        base = [FFMPEG, "-hide_banner", "-loglevel", "error", "-stats", "-y", "-i", ruta]
        if vkbps and not gpu:  # dos pasadas reales con x264/x265
            correr(base + comunes + args_video(cfg, gpu, vkbps, 1) + ["-an", "-f", "null", "NUL"], tmp)
            correr(base + comunes + args_video(cfg, gpu, vkbps, 2) + audio
                   + ["-movflags", "+faststart", parcial], tmp)
        else:
            correr(base + comunes + args_video(cfg, gpu, vkbps, 0) + audio
                   + ["-movflags", "+faststart", parcial], tmp)
        peso1 = os.path.getsize(parcial)
        if peso1 >= peso0 * 0.95:
            print(f"✗ La copia pesaría {mb(peso1):.0f} MB (≥ 95 % del original): no vale la pena, no se guarda.")
            return
        shutil.move(parcial, salida)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    i1 = sondear(salida)
    print(f"✓ {salida}\n  {mb(peso0):.0f} MB → {mb(peso1):.0f} MB  (−{100 * (1 - peso1 / peso0):.0f} %) · "
          f"{i1['w']}x{i1['h']} {i1['codec']} · {i1['kbps']} kbps · {time.time() - t0:.0f} s de proceso")
    if abs(i1["dur"] - info["dur"]) > 0.5:
        print(f"  ⚠ duración distinta: {info['dur']:.2f} s → {i1['dur']:.2f} s")


def main():
    # que los mensajes salgan en orden con la barra de ffmpeg y sin romper la consola de Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    ap = argparse.ArgumentParser(description="Comprime videos a una copia liviana (el original no se toca).")
    ap.add_argument("entrada")
    ap.add_argument("--perfil", choices=PERFILES, default="ligero")
    ap.add_argument("--mb", type=float)
    ap.add_argument("--res", type=int)
    ap.add_argument("--codec", choices=["h264", "h265"])
    ap.add_argument("--crf", type=int)
    ap.add_argument("--audio", type=int)
    ap.add_argument("--gpu", action="store_true")
    ap.add_argument("--sufijo", default="_ligero")
    ap.add_argument("--sobrescribir", action="store_true")
    a = ap.parse_args()

    cfg = dict(PERFILES[a.perfil])
    for k in ("res", "codec", "crf", "audio"):
        if getattr(a, k) is not None:
            cfg[k] = getattr(a, k)
    print(f"Perfil {a.perfil}: {cfg['codec']} " + (f"objetivo {a.mb:g} MB" if a.mb else f"CRF {cfg['crf']}")
          + f" · {'original' if not cfg['res'] else str(cfg['res']) + 'p'} · audio {cfg['audio']} kbps"
          + (" · GPU NVENC" if a.gpu else ""))
    for ruta in resolver_entradas(a.entrada, a.sufijo):
        comprimir(ruta, cfg, a.gpu, a.mb, a.sufijo, a.sobrescribir)


if __name__ == "__main__":
    main()
