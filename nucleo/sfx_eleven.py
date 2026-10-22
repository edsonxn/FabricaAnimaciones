# -*- coding: utf-8 -*-
"""SFX de ElevenLabs (o de la BIBLIOTECA) en los videos dibujados por código (22-oct-2026).

Pedido del usuario: en Cronopapel, Bitácora, Sapiens, Kuriox… «se repiten muchos SFX en varios videos» — el sintetizador de
sfx.py da la MISMA onda en todos (semillas fijas). Ahora cada video declara en guion.py

    SFX_ELEVEN = {
        "pop":     dict(prompt="Soft paper cut-out popping onto a desk, light cardboard tap", seg=0.6, variantes=3),
        "campana": ("Single distant bronze church bell toll, colonial town, light reverb", 3),
        "galope":  dict(prompt="Two horses galloping on a dirt road, passing by", seg=4),
        "tambor":  dict(prompt="…", seg=2, bib=False),      # bib=False: generar siempre (la de la biblioteca no casaba)
    }

y `fab.py <v> sfx`:
  1. por cada nombre (y variante) que falte en sfx/: primero la BIBLIOTECA, descartando lo que el público del canal ya oyó
     (nació en el canal o ya se usó en él); si nada casa, ElevenLabs `sound-generation`;
  2. sfx.py usa esos archivos en vez del sintetizador para TODOS los eventos con ese nombre — también los que emite el kit
     (`snd="pop"`, transiciones `whoosh`…), sin tocar las escenas — rotando las variantes para que un `pop` no suene 172
     veces igual. Un evento con un nombre que no está en el sintetizador pero sí en sfx/<nombre>.mp3 también vale.
`fab.py <v> sfx --seco` dice qué saldría de la biblioteca y qué se generaría, sin copiar ni gastar.
"""
import glob
import os
import re
import sys
from collections import Counter

import numpy as np

UMBRAL_BIB = 0.45          # parecido mínimo (TF-IDF nombre+prompt) para aceptar una pieza de la biblioteca
EXT = (".mp3", ".wav")


def declarados():
    """{nombre: dict(prompt, seg, variantes)} de guion.SFX_ELEVEN (vacío si el video no lo usa)."""
    try:
        import guion
    except ImportError:
        return {}
    return normalizar(getattr(guion, "SFX_ELEVEN", None) or {})


def normalizar(sfx):
    out = {}
    for n, v in sfx.items():
        if isinstance(v, dict):
            out[n] = dict(prompt=v["prompt"], seg=float(v.get("seg", 2)), variantes=int(v.get("variantes", 1)),
                          bib=bool(v.get("bib", True)))
        else:
            out[n] = dict(prompt=v[0], seg=float(v[1]) if len(v) > 1 else 2.0, variantes=int(v[2]) if len(v) > 2 else 1,
                          bib=True)
    return out


def _destinos(nombre, k):
    return [f"sfx/{nombre}.mp3"] if k == 1 else [f"sfx/{nombre}_{i}.mp3" for i in range(1, k + 1)]


def archivos(nombre):
    """Archivos de sfx/ para un nombre: sfx/<nombre>.mp3|wav y/o sus variantes sfx/<nombre>_<n>.*, en orden."""
    fs = [f for f in glob.glob(f"sfx/{glob.escape(nombre)}.*") if f.lower().endswith(EXT)]
    fs += sorted((f for f in glob.glob(f"sfx/{glob.escape(nombre)}_*") if f.lower().endswith(EXT)
                  and re.fullmatch(rf"{re.escape(nombre)}_\d+", os.path.splitext(os.path.basename(f))[0])),
                 key=lambda f: int(re.search(r"_(\d+)\.\w+$", f).group(1)))
    return fs


def resolver(decl, seco=False):
    """Deja en sfx/ todo lo que declara SFX_ELEVEN: biblioteca primero (sin repetir ante el canal), ElevenLabs después."""
    import musica_biblioteca as MB
    decl = normalizar(decl)
    video = os.path.basename(os.getcwd())
    canal = MB.leer_canal(os.getcwd())
    os.makedirs("sfx", exist_ok=True)
    tomadas, generar, de_bib = set(), [], []
    for nombre, d in decl.items():
        faltan = [p for p in _destinos(nombre, d["variantes"]) if not os.path.exists(p)
                  and not os.path.exists(p[:-4] + ".wav")]
        if not faltan:
            continue
        res = MB.sfx_buscar([nombre.replace("_", " "), d["prompt"]], n=12, canal=canal, video=video, salida=False,
                            dur=d["seg"]) if d["bib"] else []
        cand = [k for s, k in res if s >= UMBRAL_BIB and k not in tomadas]
        for p in faltan:
            if cand:
                k = cand.pop(0)
                tomadas.add(k)
                de_bib.append((p, k))
            else:
                generar.append((p, nombre, d))
    print(f"SFX_ELEVEN ({video}, canal {canal or '—'}): {len(de_bib)} de la biblioteca, {len(generar)} por generar")
    for p, k in de_bib:
        print(f"  biblioteca  {p:<28} ← {k}")
    for p, nombre, d in generar:
        print(f"  ElevenLabs  {p:<28} {d['seg']:.1f} s  «{d['prompt'][:70]}»")
    if seco:
        return
    for p, k in de_bib:
        MB.sfx_usar(k, video, os.path.splitext(os.path.basename(p))[0])
    if generar:
        import tts_eleven as E
        gasto = 0
        for p, nombre, d in generar:
            r = E.post("sound-generation", timeout=180,
                       json=dict(text=d["prompt"], duration_seconds=min(max(d["seg"], 0.5), 22), prompt_influence=0.45))
            if r.status_code != 200:
                raise SystemExit(f"ElevenLabs {r.status_code} en «{nombre}»: {r.text[:300]}")
            open(p, "wb").write(r.content)
            gasto += int(r.headers.get("character-cost") or 0)
        print(f"ElevenLabs: {len(generar)} efectos generados, {gasto} créditos (al cerrar el video: biblioteca sfx catalogar)")


def cargar(ruta, sr):
    """Audio de archivo → float64 (2, n) a `sr`, con pico 0,9 como los sintetizados (nrm)."""
    import librosa
    x, _ = librosa.load(ruta, sr=sr, mono=False)
    x = np.atleast_2d(x).astype(np.float64)
    if x.shape[0] == 1:
        x = np.vstack([x, x])
    m = np.abs(x).max()
    return x / m * 0.9 if m > 0 else x


def recortar(x, dur, sr):
    """Si el evento pide `dur` (transiciones) y el archivo es mucho más largo, corta con un fundido de 0,15 s."""
    n = int((dur + 0.4) * sr)
    if dur and x.shape[1] > int(n * 1.3):
        x = x[:, :n].copy()
        f = min(int(0.15 * sr), n)
        x[:, -f:] *= np.linspace(1, 0, f)
    return x


def aviso_repetidos(evs, de_archivo):
    """Avisa de los sonidos sintetizados más usados: son la misma onda en todos los videos del canal."""
    c = Counter(e["nombre"] for e in evs if e["nombre"] not in de_archivo)
    if not c:
        return
    top = ", ".join(f"{n}×{k}" for n, k in c.most_common(10))
    print(f"⚠ {sum(c.values())} eventos con el SINTETIZADOR (suenan igual en todos los videos): {top}"
          f"\n  Declara los principales en guion.py → SFX_ELEVEN (con variantes) para que no se repitan ante el canal.",
          file=sys.stderr)
