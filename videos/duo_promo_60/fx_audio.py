# -*- coding: utf-8 -*-
"""SFX de ElevenLabs del anuncio de 60 s (sonidos de interfaz suaves y de juego, como los de la app; nada de golpes de tráiler).
Genera cada sonido una sola vez en sfx/<nombre>.mp3 (cuesta créditos; usa `tts_eleven.post`, que salta a la cuenta de respaldo
si una se queda sin saldo) y arma audio/fx.wav con los sonidos anclados a las MISMAS palabras que la animación (se importan de
los e_*.py). `mezcla` suma audio/fx.wav (nivel: MEZCLA["fx"] en guion.py).
Regla «SFX repetidos no»: los frecuentes tienen variantes (_a/_b/_c) y van bajitos.

    python fx_audio.py --seco     lista los sonidos, sus segundos y cuántas veces suena cada uno; no genera nada
    python fx_audio.py            genera lo que falte y escribe audio/fx.wav
"""
import collections
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)

import librosa  # noqa: E402
import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402

import e_ciclo as C  # noqa: E402
import e_hogar as Ho  # noqa: E402
import e_intro as I  # noqa: E402
import e_juegos as J  # noqa: E402
import e_medida as M  # noqa: E402
from duo import TOTAL  # noqa: E402

SFX = {                                    # nombre: (prompt en inglés, segundos)
    "cojin": ("Person flopping down onto a soft couch cushion, gentle fabric thump, tired", 0.6),
    "pila": ("Low battery warning blip, two soft descending electronic beeps, phone, quiet", 0.7),
    "scroll_a": ("Soft finger swipe scrolling on a phone screen, light glass flick, short", 0.4),
    "scroll_b": ("Quick light thumb flick on smartphone glass, subtle swipe, short", 0.4),
    "tictac": ("Fast soft clock ticking speeding up, time passing, gentle", 1.6),
    "vibra": ("Phone vibrating on a couch cushion, short soft buzz buzz", 0.8),
    "aviso": ("Soft two-note phone notification chime, warm and friendly, clean", 1.0),
    "deslizar": ("Soft fabric slide of two people scooting closer on a couch, gentle swish", 0.7),
    "magia": ("Magical sparkle shimmer swell rising into a warm soft chime, logo reveal, romantic", 2.0),
    "confeti": ("Party popper pop with paper confetti fluttering, festive, short", 1.4),
    "whoosh_a": ("Soft airy swoosh transition, smooth and light, short", 0.7),
    "whoosh_b": ("Gentle quick whoosh pass by, airy and clean, short", 0.6),
    "sube": ("Smooth soft whoosh of a phone sliding up into view, airy, short", 0.9),
    "aparece": ("Very soft UI swish of cards appearing one after another, light and subtle", 0.7),
    "tarjeta": ("Soft paper card flip pop, friendly UI, short", 0.5),
    "toque": ("Phone screen tap, soft finger click on glass, short", 0.4),
    "brillo_a": ("Small magical sparkle twinkle, short bright chime, cute", 0.7),
    "brillo_b": ("Tiny glittery ding with soft bells, magical UI, short", 0.7),
    "switch": ("Toggle switch flicked on in a mobile app, soft satisfying click with a tiny chime", 0.5),
    "cartas": ("Cards swiping away and new cards sliding in, soft paper swish, UI", 0.8),
    "llamada": ("Video call connecting tone, soft friendly ascending blips", 1.0),
    "plato": ("Ceramic plate set down gently on a table with a fork clink", 0.6),
    "colgar": ("Video call ending soft descending blip", 0.6),
    "pestana": ("Soft UI tab switch click, smooth, short", 0.4),
    "ficha_a": ("Cute bouncy boing hop, playful game token jump, short", 0.5),
    "ficha_b": ("Soft springy bloop jump, cartoon hop, short", 0.5),
    "sin_red": ("Soft gentle error blip, low two-note, mobile app, quiet", 0.5),
    "pasa": ("Quick soft UI swipe, page slides sideways in an app, short", 0.4),
    "pasa_b": ("Light paper-like swish of a screen sliding sideways, mobile app, short", 0.4),
    "correcto": ("Bright correct answer chime, cheerful quiz game, short", 0.8),
    "lapiz": ("Pencil quickly sketching on paper, drawing scribbles", 1.2),
    "teclas": ("Soft phone keyboard typing four taps", 0.6),
    "correcto2": ("Cheerful success jingle with a soft pluck, teamwork win, mobile game, short", 0.9),
    "grua": ("Small toy crane motor whirring back and forth, cute mechanical", 1.0),
    "bloque": ("Wooden toy block dropping onto a stack, solid soft clack", 0.5),
    "ficha_c4": ("Plastic disc dropping into a connect four board, clacky plastic slide", 0.5),
    "victoria": ("Short bright victory fanfare, mobile game win, celebratory chimes", 1.6),
    "resortera": ("Rubber slingshot band stretching, creaky elastic pull", 0.8),
    "lanza": ("Slingshot release twang with a quick whoosh", 0.6),
    "choque": ("Wooden fort crashing apart with glass breaking, cartoon game destruction, short", 1.2),
    "monedas": ("Shower of coins jingling and bouncing, video game reward", 1.2),
    "cerdito": ("Cute cartoon pig oink, playful, short", 0.6),
    "isla": ("Magical rising whoosh with soft wind chimes, floating island appears", 1.2),
    "caen": ("Many gold coins pouring into a pile, sparkly video game cash in", 1.5),
    "ding": ("Cash register soft ding, coin counter, cute game", 0.6),
    "mueble_a": ("Furniture piece dropping onto a wooden floor with a soft bouncy thud, cozy game", 0.5),
    "mueble_b": ("Soft cushioned plop of an object landing, cute building game, short", 0.5),
    "mueble_c": ("Light wooden knock of furniture placed down, cozy game, short", 0.5),
    "dia_noche": ("Magical time lapse swirl, wind and twinkling chimes rising and falling", 1.3),
    "brote_a": ("Tiny plant sprouting pop, cute soft plink", 0.4),
    "brote_b": ("Little bubbly growth pop, cute garden game, short", 0.4),
    "marchita": ("Sad cartoon descending slide whistle, soft and short", 0.9),
    "boton": ("Soft rubbery game button press, satisfying", 0.4),
    "gotas": ("Water droplets falling into soil, a few gentle drips and a splash", 1.0),
    "florece": ("Plants blooming sparkle, magical bright chimes ascending, cozy garden game", 1.2),
    "fase_a": ("Soft warm marimba note chime, gentle UI change", 0.6),
    "fase_b": ("Soft glockenspiel note, gentle UI change, short", 0.6),
    "fase_c": ("Soft kalimba pluck, gentle UI change, short", 0.6),
    "pagina": ("Magazine page turning, crisp paper flip", 0.6),
    "latido": ("Soft warm heartbeat, two gentle thumps", 1.2),
    "pop_a": ("Soft bubble pop, cute UI icon appearing, short", 0.3),
    "pop_b": ("Light airy pop with a tiny chime, UI, short", 0.3),
    "final": ("Bright sparkle chime success sting, uplifting, clean ending", 1.5),
}

SALTOS = [J.j_tur, J.j_tur + 0.55, J.j_aun + 0.1, J.j_con, J.j_tie]
PISTAS = [                                  # (sonido, segundo, volumen)
    # gancho: la sala de noche
    ("cojin", 0.42, .5), ("cojin", 0.55, .4), ("pila", I.g_cans + .1, .4),
    *[("scroll_a" if k % 2 else "scroll_b", I.g_cada + 0.42 * k, .28) for k in range(6)],
    ("tictac", I.g_pierde - .1, .3), ("vibra", I.h_hasta - .05, .55), ("aviso", I.h_hasta + .05, .65),
    ("deslizar", I.h_prob - .1, .5), ("magia", I.h_duo - .15, .75), ("confeti", I.h_duo + .2, .5), ("whoosh_a", I.T_VUELA, .45),
    # misiones a la medida y a distancia
    ("sube", 7.55, .55), ("aparece", M.m_cada + .2, .45), ("tarjeta", M.m_seg + .05, .5), ("tarjeta", M.m_seg + .4, .4),
    ("toque", M.m_cont, .6), ("toque", M.m_cont + .15, .5), ("brillo_a", M.m_quien + .15, .55), ("brillo_b", M.m_quien + .35, .55),
    ("switch", M.l_lej, .7), ("whoosh_b", M.l_lej + .05, .45), ("cartas", M.l_camb, .5), ("plato", M.l_cenar, .5),
    ("plato", M.l_cenar + .12, .4), ("llamada", M.l_vid - .25, .5), ("colgar", M.T_SALE - .1, .4),
    # juegos
    ("pestana", J.j_hay, .6), ("aparece", J.j_jue, .4),
    *[("ficha_a" if k % 2 else "ficha_b", s, .4) for k, s in enumerate(SALTOS)], ("sin_red", J.j_con, .35),
    *[("pasa" if k % 2 else "pasa_b", s, .45) for k, s in enumerate((J.S_QTMC, J.S_DIB, J.S_TOR, J.S_C4, J.S_SG))],
    ("correcto", J.k_con + .45, .6),
    ("lapiz", J.S_DIB + .2, .45), ("teclas", J.k_dib + .2, .45), ("correcto2", J.k_dib + .65, .55),
    ("grua", J.S_TOR + .1, .35), ("bloque", J.k_cie + .38, .6),
    ("ficha_c4", J.C4_B[2] + .08, .5), ("ficha_c4", J.c_cua + .1, .6), ("victoria", J.c_lin, .6), ("aviso", J.c_deb - .05, .55),
    ("toque", J.T_REV, .6), ("resortera", J.r_rev, .5), ("lanza", J.r_asa, .6), ("choque", J.T_IMP, .7),
    ("monedas", J.T_IMP + .1, .5), ("cerdito", J.T_IMP + .2, .55),
    # hogar y huerto
    ("whoosh_a", J.T_SALE, .45), ("isla", Ho.T_ENTRA, .5), ("caen", Ho.o_gan + .1, .5), ("ding", Ho.o_mis + .6, .5),
    *[(("mueble_a", "mueble_b", "mueble_c")[i % 3], Ho.t_mueble(i) + .33, .45) for i in range(len(Ho.MUEBLES))],
    ("pestana", Ho.u_hue - .2, .5), ("whoosh_b", Ho.u_hue, .4), ("dia_noche", Ho.u_cre - .05, .45),
    ("brote_a", Ho.u_cre + .3, .35), ("brote_b", Ho.u_cre + .6, .35), ("brote_a", Ho.u_si - .2, .3),
    ("marchita", Ho.u_si + .1, .45), ("boton", Ho.T_RIEGO - .25, .55), ("gotas", Ho.T_RIEGO - .15, .55), ("florece", Ho.T_RIEGO + .5, .5),
    # ciclo y guía
    ("sube", 44.05, .5), ("aparece", 44.6, .35),
    *[(("fase_a", "fase_b", "fase_c")[i - 1], C.T_FASES[i], .5) for i in range(1, 4)],
    ("whoosh_b", C.g_mi - .15, .45), ("pagina", C.g_guia - .2, .55), ("brillo_a", C.g_guia, .45),
    ("pasa", C.g_emb - .35, .45), ("latido", C.g_emb, .45),
    # cierre
    ("whoosh_a", C.T_CAE, .45), ("magia", C.c_duo - .15, .75), ("confeti", C.c_duo + .08, .45),
    *[("pop_a" if k % 2 else "pop_b", C.c_duo + .15 + .1 * k, .3) for k in range(6)],
    ("toque", C.d_desc + .35, .65), ("pop_a", C.d_jue - .1, .4), ("pop_b", C.d_hoy - .15, .4), ("final", C.d_hoy + .3, .6),
]


def generar():
    import tts_eleven as TE
    os.makedirs("sfx", exist_ok=True)
    gasto = 0
    for n, (txt, dur) in SFX.items():
        if os.path.exists(f"sfx/{n}.mp3"):
            continue
        r = TE.post("sound-generation", timeout=180,
                    json=dict(text=txt, duration_seconds=max(0.5, float(dur)), prompt_influence=0.5))
        if r.status_code != 200:
            raise SystemExit(f"ElevenLabs {r.status_code} en «{n}»: {r.text[:300]}")
        open(f"sfx/{n}.mp3", "wb").write(r.content)
        gasto += int(r.headers.get("character-cost") or 0)
        print(f"  sfx/{n}.mp3  {dur} s", flush=True)
    print(f"ElevenLabs: {gasto} créditos en efectos")


def main():
    if "--seco" in sys.argv:
        for n, t, v in sorted(PISTAS, key=lambda x: x[1]):
            print(f"{t:7.2f}  {n:10s} {v}")
        print(len(PISTAS), "sonidos;", dict(collections.Counter(n for n, _, _ in PISTAS).most_common(6)))
        print("sin usar:", [n for n in SFX if n not in {x[0] for x in PISTAS}])
        print("faltan:", [n for n in SFX if not os.path.exists(f"sfx/{n}.mp3")])
        return
    generar()
    from sinte import SR
    N = int(TOTAL * SR)
    out, cache = np.zeros((2, N), np.float32), {}
    for n, t, v in PISTAS:
        if n not in cache:
            x, _ = librosa.load(f"sfx/{n}.mp3", sr=SR, mono=False)
            x = np.vstack([x, x]) if x.ndim == 1 else x[:2]
            ini = int(np.argmax(np.abs(x).max(0) > 0.02 * np.abs(x).max()))     # sin silencio inicial: cae en su palabra
            x = x[:, ini:] / (np.abs(x).max() + 1e-9) * 0.7
            f = min(int(0.08 * SR), x.shape[1])
            x[:, -f:] *= np.linspace(1, 0, f, dtype=np.float32)
            cache[n] = x.astype(np.float32)
        x = cache[n]
        i = max(0, int(t * SR))
        x = x[:, :max(0, N - i)] * v
        out[:, i:i + x.shape[1]] += x
    os.makedirs("audio", exist_ok=True)
    sf.write("audio/fx.wav", out.T, SR, subtype="PCM_16")
    print(f"audio/fx.wav: {len(PISTAS)} sonidos en {TOTAL:.1f} s (pico {np.abs(out).max():.2f})")


if __name__ == "__main__":
    main()
