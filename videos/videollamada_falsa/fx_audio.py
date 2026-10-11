# -*- coding: utf-8 -*-
"""SFX de ElevenLabs para el DRAMA (lo pidió el usuario): impactos, subidas, truenos, la señal que se rompe, tonos de llamada…
Se generan una sola vez en sfx/<nombre>.mp3 (cuesta créditos) y se arman en audio/fx.wav con cada golpe anclado a la MISMA palabra
que la animación (los tiempos salen de los `t_*` de cada escena). `mezcla` suma audio/fx.wav (nivel: MEZCLA["fx"] en guion.py).

    python fx_audio.py --seco     lista los sonidos y sus segundos, no genera nada
    python fx_audio.py            genera lo que falte y escribe audio/fx.wav
"""
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]

import librosa  # noqa: E402
import numpy as np  # noqa: E402
import requests  # noqa: E402
import soundfile as sf  # noqa: E402

import escenas as S  # noqa: E402

TL = json.load(open("timeline.json", encoding="utf-8"))
TOTAL = TL["total"]
IDS = [e["id"] for e in TL["escenas"]]
E = {e["id"]: S.CLASES[e["id"]](e, IDS.index(e["id"])) for e in TL["escenas"]}

SFX = {                                    # nombre: (prompt en inglés, segundos)
    "impacto": ("Deep dark cinematic bass impact hit with a long low reverberant tail, film noir thriller trailer", 3.0),
    "impacto2": ("Short dry low orchestral hit, timpani and low piano cluster, noir suspense sting", 2.0),
    "subida": ("Tense dark cinematic riser, strings and reversed cymbal building up and cutting off abruptly", 3.0),
    "glitch": ("Digital video signal glitch, data corruption stutter and static burst, short", 1.2),
    "trueno": ("Close heavy thunder crack with long rolling rumble in the rain", 5.0),
    "conecta": ("Video conference call connecting chime, soft modern join-meeting notification sound", 1.5),
    "correo": ("Single soft email notification ding on a computer, clean", 1.0),
    "cuelga": ("Video call ending, short descending disconnect tone followed by silence", 1.5),
    "linea": ("Old telephone line ringing tone heard through the earpiece, two rings, slightly distorted", 4.0),
    "latido": ("Slow tense human heartbeat, low and close, four beats, suspense", 4.0),
    "zumbido": ("Low ominous dark drone swell, uneasy, sub bass and distant metallic resonance, noir mystery", 5.0),
    "bip": ("Short soft digital bank transfer confirmation beep, single", 0.5),
    "reloj": ("Fast frantic clock ticking accelerating, tense", 4.0),
    "celda": ("Heavy iron prison cell door slamming shut with reverberant clang", 2.5),
    "susurro": ("Eerie breathy ghostly whisper whoosh passing by, unintelligible, haunting", 2.5),
    "dinero": ("Rapid counting of paper banknotes by a money counting machine, fast flutter", 3.0),
}


def pistas():
    r, m, l, d, x, tr, ma, v, s, se, le, c = (E[k] for k in IDS)
    P = [
        # regla
        ("trueno", r.t_regla - 0.5, .5), ("zumbido", r.t_fiate, .5), ("trueno", r.rayos[0], .8), ("trueno", r.rayos[1], .6),
        ("conecta", r.t_emp + 0.6, .6), ("subida", r.t_nadie - 2.6, .7), ("glitch", r.t_nadie + 0.1, .7), ("glitch", r.t_nadie + 0.9, .7),
        ("glitch", r.t_real - 0.5, .8), ("impacto", r.t_real - 0.15, 1.0), ("latido", r.t_excepto, .7),
        # mensaje
        ("correo", m.t_mensaje - 0.25, .8), ("impacto2", m.t_urgente, .8), ("zumbido", m.t_ynuestro, .5), ("impacto2", m.t_engano, .7),
        ("susurro", m.t_pero - 0.2, .7), ("zumbido", m.t_pero + 0.5, .6), ("conecta", m.t_reunion, .6), ("impacto", m.t_camara, .9),
        # llamada
        ("conecta", l.t_conecta, .8), ("impacto2", l.t_director, .5), ("susurro", l.t_duda, .5), ("latido", l.t_porque, .6),
        ("subida", l.t_ojos - 2.4, .6), ("impacto", l.t_ojos, .9), ("cuelga", l.t_termino - 0.2, .9),
        # dinero
        ("latido", d.t_semana, .5), ("dinero", d.t_dosc, .7), ("subida", d.t_mas - 2.8, .7), ("impacto", d.t_mas, 1.0),
        ("impacto2", d.t_pistola + 0.25, .6), ("impacto2", d.t_pasa + 0.25, .6), ("impacto2", d.t_forzar + 0.25, .6),
        ("zumbido", d.t_botin - 0.2, .6), ("impacto", d.t_sello, .9),
        # descubre
        ("linea", x.t_llamo, .8), ("susurro", x.t_otro, .5), ("latido", x.t_nadie, .8), ("zumbido", x.t_nohabia - 0.3, .7),
        ("impacto2", x.t_nohabia + 0.25, .6), ("impacto2", x.t_noreu + 0.25, .6), ("impacto", x.t_jamas, 1.0),
        ("trueno", x.t_veinti + 0.2, .5), ("celda", x.t_para - 0.1, .7), ("impacto", x.t_noestaba - 0.2, 1.0),
        # truco
        ("susurro", tr.t_como, .8), ("zumbido", tr.t0 + 0.3, .7), ("susurro", tr.t_fant - 0.3, .7), ("impacto2", tr.t_hipo - 0.3, .6),
        ("glitch", tr.t_voces, .6), ("subida", tr.t_deep - 2.7, .7), ("impacto", tr.t_deep, 1.0), ("glitch", tr.t_mascara, .7),
        ("glitch", tr.t_mascara + 0.6, .5), ("impacto2", tr.t_hoy, .7),
        # manual
        ("zumbido", ma.t_otra, .6), ("impacto", ma.t_aut - 0.15, .8), ("zumbido", ma.t_quien, .6), ("impacto", ma.t_secreto - 0.15, .8),
        ("susurro", ma.t_oper, .6), ("impacto", ma.t_prisa - 0.15, .8), ("reloj", ma.t_prisa + 0.2, .8), ("latido", ma.t_cuando, .7),
        ("impacto", ma.t_grupo - 0.15, .8), ("subida", ma.t_quieneres - 2.2, .5), ("impacto2", ma.t_quieneres + 0.6, .6),
        ("impacto", ma.t_siglo - 0.3, .9),
        # victima
        ("impacto2", v.t_nombre - 0.2, .6), ("subida", v.t_confirmo - 2.9, .6), ("impacto", v.t_confirmo, 1.0), ("impacto2", v.t_era + 0.5, .8),
        ("zumbido", v.t_misma - 0.3, .5), ("impacto2", v.t_nadie, .6), ("impacto2", v.t_ninguna, .7), ("susurro", v.t_noeng - 0.2, .6),
        ("subida", v.t_persona - 2.9, .6), ("impacto", v.t_persona - 0.2, 1.0),
        # sinrostro
        ("trueno", s.t0 + 0.6, .5), ("impacto", s.t_nopuedo, 1.0), ("celda", s.t_hasta - 0.2, .8), ("impacto2", s.t_deten - 0.1, .7),
        ("impacto2", s.t_nombres, .7), ("impacto2", s.t_dinero, .7), ("zumbido", s.t_esel - 0.3, .7), ("impacto", s.t_ladr, .9),
        ("susurro", s.t_usaron, .7),
        # senales
        ("trueno", se.t0 + 0.4, .5), ("impacto2", se.t_senales - 0.5, .7), ("celda", se.t_meses, .9), ("impacto", se.t_seis, .9),
        ("dinero", se.t_noventa - 0.2, .5), ("impacto2", se.t_cinc, .6), ("glitch", se.t_usaban, .7), ("bip", se.t_rostro + 0.5, .9),
        ("zumbido", se.t_misma - 0.3, .7), ("impacto2", se.t_maquina, .7), ("impacto", se.t_hombre, .9),
        # leccion
        ("subida", le.t_aviso - 2.8, .7), ("impacto", le.t_aviso, 1.0), ("glitch", le.t_voz, .6), ("glitch", le.t_cara, .6),
        ("impacto2", le.t_internet - 0.3, .8), ("zumbido", le.t_asi, .5), ("impacto", le.t_nueva - 0.5, .9), ("cuelga", le.t_cuelga - 0.1, .9),
        ("impacto2", le.t_cuelga, .7), ("linea", le.t_llama + 0.4, .6), ("impacto2", le.t_clave - 0.2, .7), ("susurro", le.t_clave + 0.2, .6),
        ("impacto2", le.t_ydesc + 0.2, .7), ("reloj", le.t_prisa, .5),
        # cierre
        ("zumbido", c.t0 + 0.2, .6), ("latido", c.t_temblaba - 0.4, .8), ("subida", c.t_suya - 2.9, .6), ("impacto", c.t_suya, .9),
        ("trueno", c.t_ver - 0.2, .5), ("impacto2", c.t_pues, .7), ("impacto", c.t_alcanza - 0.5, .8), ("impacto", c.t_caso + 0.25, 1.0),
        ("trueno", c.t_caso + 0.5, .8),
    ]
    dur = max(2.0, d.t_hk + 1.2 - d.t_quince)                  # los quince envíos: un bip al llegar cada uno
    P += [("bip", d.t_quince + q * dur / 16.0 + 0.75, .55) for q in range(15)]
    return P


def generar():
    clave = open(os.path.join(AQUI, "..", "..", "canales", "tokens", "elevenlabs_api_key.txt"), encoding="utf-8").read().strip()
    os.makedirs("sfx", exist_ok=True)
    gasto = 0
    for n, (txt, dur) in SFX.items():
        if os.path.exists(f"sfx/{n}.mp3"):
            continue
        for intento in range(4):
            r = requests.post("https://api.elevenlabs.io/v1/sound-generation", headers={"xi-api-key": clave}, timeout=180,
                              json=dict(text=txt, duration_seconds=max(0.5, float(dur)), prompt_influence=0.5))
            if r.status_code == 200:
                open(f"sfx/{n}.mp3", "wb").write(r.content)
                gasto += int(r.headers.get("character-cost") or 0)
                print(f"  sfx/{n}.mp3  {dur} s", flush=True)
                break
            if r.status_code not in (429, 500, 502, 503):
                raise SystemExit(f"ElevenLabs {r.status_code} en «{n}»: {r.text[:300]}")
            time.sleep(5 * (intento + 1))
    print(f"ElevenLabs: {gasto} créditos en efectos")


def main():
    P = pistas()
    if "--seco" in sys.argv:
        for n, t, v in sorted(P, key=lambda x: x[1]):
            print(f"{t:7.2f}  {n:10s} {v}")
        print(len(P), "golpes;", "faltan:", [n for n in SFX if not os.path.exists(f"sfx/{n}.mp3")],
              "| segundos a generar:", sum(d for n, (_, d) in SFX.items() if not os.path.exists(f"sfx/{n}.mp3")))
        return
    generar()
    SR = 48000
    N = int(TOTAL * SR)
    out, cache = np.zeros((2, N), np.float32), {}
    for n, t, v in P:
        if n not in cache:
            x, _ = librosa.load(f"sfx/{n}.mp3", sr=SR, mono=False)
            x = np.vstack([x, x]) if x.ndim == 1 else x[:2]
            ini = int(np.argmax(np.abs(x).max(0) > 0.02 * np.abs(x).max()))     # sin silencio inicial: el golpe cae en su palabra
            x = x[:, ini:] / (np.abs(x).max() + 1e-9) * 0.7
            f = min(int(0.15 * SR), x.shape[1])
            x[:, -f:] *= np.linspace(1, 0, f, dtype=np.float32)
            cache[n] = x.astype(np.float32)
        x = cache[n]
        i = max(0, int(t * SR))
        x = x[:, :max(0, N - i)] * v
        out[:, i:i + x.shape[1]] += x
    os.makedirs("audio", exist_ok=True)
    sf.write("audio/fx.wav", out.T, SR, subtype="PCM_16")
    print(f"audio/fx.wav: {len(P)} golpes en {TOTAL:.1f} s (pico {np.abs(out).max():.2f})")


if __name__ == "__main__":
    main()
