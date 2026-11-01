# -*- coding: utf-8 -*-
"""SFX de ElevenLabs de «Tres noches»: cada sonido se genera UNA vez en sfx/<nombre>.mp3 (cuesta créditos) y se arma audio/fx.wav
con cada golpe anclado a la MISMA palabra que la animación (anclas.py). `mezcla` suma audio/fx.wav (MEZCLA["fx"] en guion.py).
Regla «SFX repetidos no»: cada sonido suena pocas veces y con volúmenes distintos; los ambientes son largos y suaves.

    python fx_audio.py --seco     lista los sonidos y sus segundos, no genera nada
    python fx_audio.py            genera lo que falte y escribe audio/fx.wav
"""
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)

import librosa  # noqa: E402
import numpy as np  # noqa: E402
import requests  # noqa: E402
import soundfile as sf  # noqa: E402

import anclas as A  # noqa: E402
from grabado import TOTAL  # noqa: E402

SFX = {                                    # nombre: (prompt en inglés, segundos)
    "campana": ("A single distant cold church bell toll at night, long reverberant decay, eerie", 5.0),
    "viento": ("Night wind blowing through an old graveyard, soft howling, dry leaves, distant, eerie ambience", 10.0),
    "cuervos": ("A few crows cawing in the distance at night, sparse, eerie", 3.0),
    "fantasma": ("Ghostly whoosh passing by, airy spectral swoosh with a faint moan", 2.0),
    "coro": ("Short eerie angelic choir swell, ethereal, cold reverb, rising then fading", 4.0),
    "almas": ("Many distant ghostly moans and sighs echoing, a procession of lost souls, faint", 6.0),
    "lapida": ("Heavy stone slab grinding up out of the earth, gravel and dirt falling, short", 1.6),
    "hundir": ("Stone tombstones sinking into the ground, low rumble and grinding, short", 1.6),
    "vela": ("A candle wick igniting with a soft whoosh and crackle, close", 1.2),
    "apagar": ("A candle flame being snuffed out, short hiss and a puff of smoke", 1.0),
    "tinta": ("Thick liquid ink splashing and spreading, wet viscous whoosh, dark", 1.6),
    "selva": ("Night jungle ambience, insects, distant frogs and strange birds, humid and threatening", 10.0),
    "tambor": ("Three slow deep tribal war drum hits in a jungle temple, reverberant", 3.0),
    "fuego": ("Several torches igniting in sequence, fire whoosh and crackling", 2.5),
    "siseo": ("Huge serpent hissing, deep and menacing, long hiss with reverb in a stone chamber", 3.0),
    "gotas": ("Thick drops of blood dripping onto stone floor, slow, echoing", 3.0),
    "reloj": ("Sand pouring fast through an hourglass, granular trickle, close", 2.5),
    "lobo": ("A wolf growling low and menacing, close", 2.0),
    "jaula": ("Small iron cage door creaking and clanking shut, metallic", 1.2),
    "multitud": ("Medieval crowd murmuring in a large stone hall, a forge crackling in the background", 8.0),
    "ataque": ("Wolf snarling and lunging, then people screaming in panic in a stone hall", 3.0),
    "caida": ("A body collapsing to the ground and bones rattling onto stone", 1.4),
    "espada": ("A sword being drawn from a sheath, metallic ring", 1.2),
    "huesos": ("Skeletons dancing, wooden bones clacking and rattling rhythmically, macabre", 4.0),
    "nieve": ("Cold wind howling over snowy mountains, blowing snow, desolate ambience", 10.0),
    "campanilla": ("A hand bell ringing urgently as a warning, outdoors in cold air", 2.0),
    "sanacion": ("Soft holy healing spell chime with a warm shimmer", 2.0),
    "madera": ("Wooden barricade slammed down into the ground, heavy wooden thud", 1.2),
    "risa": ("Distorted creepy manic laughter of a man running, echoing, horror", 2.5),
    "gritos": ("Crowd of people screaming and fleeing in panic, outdoors", 3.0),
    "templo": ("Deep dark drone rumble inside an ancient stone temple, ominous low hum", 6.0),
    "latido": ("Slow deep heartbeat thumping, dark and tense, three beats", 3.0),
    "susto": ("Sudden loud horror jumpscare: violent impact boom with a monstrous serpent shriek, cinematic", 2.5),
    # tramos 6-7 (15-oct-2026)
    "tinta2": ("Ink drop falling into water and blooming outward, deep muffled whoosh, dark", 1.6),
    "fuego_aldea": ("A village burning in the distance at night, roaring fire and crackling timber, faint screams", 6.0),
    "papel": ("Old parchment letter unfolding and rustling, close", 1.5),
    "pluma": ("Quill pen scratching quickly on parchment, writing", 3.0),
    "libro": ("Heavy old leather book dropped open on a wooden table, dust", 1.2),
    "globo": ("Old wooden globe spinning on its creaking stand", 2.0),
    "olas": ("Night harbor ambience: gentle waves lapping against a wooden pier, creaking ropes and ship timbers", 10.0),
    "caja": ("Wooden crate lid pried open with a creak and a sickly hiss of gas escaping", 2.0),
    "gas": ("Sickly poison gas hissing and bubbling, wet and toxic", 2.5),
    "tictac": ("Loud clock ticking, relentless countdown, close and dry", 4.0),
    "necrofago": ("Undead ghoul snarling and groaning, wet raspy zombie growl", 2.5),
    "mordisco": ("Zombie bite: flesh tearing and a short muffled scream", 1.5),
    "calle_caos": ("Medieval city at night in chaos: zombies groaning, people screaming, alarm bells far away", 10.0),
    "monedas": ("Many gold coins spilling and scattering across cobblestones", 2.0),
    "portal": ("Magic portal humming and swirling, deep arcane drone with a shimmering whoosh", 4.0),
    "cruzar": ("Rushing whoosh of passing through a magic portal, wind and arcane shimmer", 1.5),
    "susto_necrofago": ("Sudden loud horror jumpscare: violent impact boom with a ghoul's screeching snarl right in your "
                        "face, cinematic", 2.5),
    "amanecer": ("Dawn breaking over a desolate field: cold wind, a distant rooster, then a soft warm choir swell", 6.0),
    "ceniza": ("Bodies crumbling into dust and ash, dry hissing disintegration", 2.5),
    "agua_termal": ("Hot spring bubbling softly in a snowy forest, gentle steam hiss, cold wind", 10.0),
    "pasos_nieve": ("Many people walking slowly in deep snow, quiet crunching footsteps, no voices", 5.0),
    "carga": ("A war band charging downhill: battle cries, armor clanking, running footsteps in snow", 4.0),
    "hechizo": ("A frost bolt and a fireball spell whooshing past and impacting", 1.5),
    "golpes_espada": ("Swords striking, bodies falling into snow, a short cry", 3.0),
    "susto_carga": ("Sudden loud horror jumpscare: violent impact boom with a sword slash and a war cry right at the "
                    "camera, cinematic", 2.5),
    "teclado": ("Old computer: mouse clicks and fast keyboard typing, a short dial-up modem screech", 3.0),
    "murmullo": ("Quiet city plaza at night: soft murmur of mourners, candles, a distant church bell", 6.0),
    "losa": ("Heavy stone slab sliding closed over a grave, grinding then a deep thud", 2.0),
    "caja_musica": ("Eerie old music box melody slowly winding down, lonely", 4.0),
    "susto_angel": ("Sudden loud horror jumpscare: violent impact boom with a choir shriek and a sharp whispered gasp, "
                    "cinematic", 2.5),
}
PISTAS = [                                  # (sonido, segundo, volumen)
    ("viento", 0.0, .55), ("campana", 0.15, .8), ("cuervos", 4.2, .45), ("fantasma", A.g_fantasma - 0.6, .7),
    ("coro", A.g_yo - 0.25, .6), ("almas", A.g_millones - 1.2, .5), ("viento", 12.0, .45),
    ("lapida", A.g_salto - 0.35, .75), ("lapida", A.g_jefe - 0.35, .6), ("lapida", A.g_apuesta - 0.35, .7),
    ("hundir", A.g_tres - 0.75, .6), ("vela", A.g_tres, .7), ("vela", A.g_tres2 - 0.25, .6), ("vela", A.g_olvido, .75),
    ("viento", 24.0, .4), ("apagar", A.g_tu + 0.05, .9),
    ("tinta", A.TR_ZG - 0.8, .7), ("selva", A.TR_ZG, .55), ("tambor", A.z_13 - 0.2, .7), ("fuego", A.z_blizzard, .6),
    ("tambor", A.z_zg - 0.1, .8), ("tinta", A.T_ENTRA - 0.45, .5),
    ("templo", A.T_ENTRA, .5), ("siseo", A.z_hakkar - 0.1, .85), ("gotas", A.z_sangre - 0.1, .7),
    ("templo", A.z_enfermedad, .45), ("siseo", A.z_drenaba, .5), ("reloj", A.z_durar - 0.2, .7),
    ("lobo", A.z_mascotas - 0.1, .85), ("jaula", A.m_pelea, .7),
    ("tinta", A.TR_FORJAZ - 0.45, .55), ("multitud", A.TR_FORJAZ, .6), ("jaula", A.m_llamaban - 0.1, .6),
    ("ataque", A.m_salio - 0.25, .9), ("multitud", A.m_salio + 4.0, .35),
    ("caida", A.c_instante, .8), ("espada", A.c_espada - 0.25, .8), ("latido", A.c_muerte - 0.4, .6),
    ("huesos", A.c_cientos - 0.3, .6), ("huesos", A.c_cientos + 3.6, .5), ("caida", A.c_blanco, .5),
    ("almas", A.c_fantasmas - 0.4, .6), ("tinta", A.TR_CEM - 0.5, .55), ("viento", A.TR_CEM, .45),
    ("coro", A.c_resucitaba - 0.2, .45),
    ("tinta", A.TR_CAMPO - 0.7, .55), ("nieve", A.TR_CAMPO, .55), ("nieve", A.TR_CAMPO + 11.0, .5),
    ("campanilla", A.h_avisando - 0.3, .7), ("sanacion", A.h_sanadores - 0.2, .6), ("nieve", A.TR_CAMPO + 22.0, .45),
    ("madera", A.h_puso - 0.1, .8), ("risa", A.h_corrian - 0.2, .75), ("gritos", A.h_huir - 0.2, .8),
    ("tinta", A.TR_HAKKAR - 0.5, .6), ("templo", A.TR_HAKKAR, .6), ("siseo", A.h_hakkar, .6), ("latido", A.h_falta - 0.2, .8),
    ("susto", A.T_SUSTO - 0.03, 1.0),
    # ---- tramo 6: gabinete → Bahía del Botín → Ventormenta → Villadorada → torre de los magos
    ("tinta2", A.TR_ESTUDIO - 0.2, .45), ("fuego_aldea", A.d_quema - 0.3, .55), ("campana", A.d_reinicio, .45),
    ("papel", A.d_centros - 0.3, .6), ("pluma", A.d_escribieron, .5), ("libro", A.d_lancet - 0.15, .7),
    ("globo", A.d_mundo - 0.3, .55), ("coro", A.d_ensayado - 0.4, .35),
    ("tinta", A.TR_MUELLE - 0.5, .5), ("olas", A.TR_MUELLE, .55), ("vela", A.k_segunda - 0.2, .55),
    ("viento", A.k_rey - 0.3, .4), ("olas", A.TR_MUELLE + 9.5, .45), ("fuego", A.k_halloween - 0.2, .4),
    ("madera", A.k_aparecieron - 0.2, .5), ("olas", A.TR_MUELLE + 19.0, .4), ("caja", A.k_abrieron - 0.1, .8),
    ("gas", A.k_abrieron + 0.5, .55), ("tictac", A.r_cuenta - 0.2, .6), ("reloj", A.r_diez, .5), ("olas", A.TR_MUELLE + 28.5, .35),
    ("caida", A.r_cero, .55), ("necrofago", A.r_levantabas - 0.2, .75), ("mordisco", A.r_mordia - 0.1, .8),
    ("tictac", A.r_siguiente, .45), ("reloj", A.r_cinco - 0.2, .45), ("tictac", A.r_dos, .55), ("reloj", A.r_uno - 0.1, .6),
    ("tinta2", A.TR_CALLE - 0.45, .5), ("calle_caos", A.TR_CALLE, .45), ("mordisco", A.n_vendedores - 0.1, .6),
    ("mordisco", A.n_subastadores - 0.1, .45), ("necrofago", A.n_vuelo - 0.3, .5), ("mordisco", A.n_guardias - 0.1, .7),
    ("calle_caos", A.n_ciudades - 0.5, .4), ("campanilla", A.n_ciudades + 0.5, .4), ("monedas", A.n_economia - 0.2, .7),
    ("tinta", A.TR_VILLA - 0.4, .4), ("gritos", A.TR_VILLA + 0.2, .5), ("necrofago", A.n_muertos - 0.2, .7),
    ("tinta2", A.TR_TORRE - 0.45, .45), ("portal", A.TR_TORRE, .55), ("huesos", A.p_zombis - 0.3, .5),
    ("risa", A.p_zombis + 0.3, .45), ("necrofago", A.p_hordas - 0.2, .45), ("portal", A.p_portales, .45),
    ("latido", A.p_escondian - 0.2, .55), ("cruzar", A.p_portal - 0.1, .8), ("necrofago", A.p_esperando, .6),
    ("susto_necrofago", A.T_SUSTO2 - 0.03, 1.0),
    # ---- tramo 7: amanecer → aguas termales → la carga → el cementerio → la plaza → la promesa → la selección
    ("pluma", A.u_escribian - 0.3, .45), ("amanecer", A.u_alba - 0.8, .6), ("ceniza", A.u_cura, .65),
    ("ceniza", A.u_apago - 0.2, .45), ("viento", A.u_rey - 0.3, .4), ("huesos", A.u_eligen - 0.2, .4),
    ("risa", A.u_plaga2 - 0.2, .35),
    ("tinta", A.TR_TERMALES - 0.6, .45), ("agua_termal", A.TR_TERMALES, .5), ("nieve", A.TR_TERMALES + 2.0, .3),
    ("vela", A.f_tercera - 0.2, .6), ("campana", A.f_illidan, .5), ("apagar", A.f_murio + 0.4, .6),
    ("pasos_nieve", A.f_companeros - 0.3, .45), ("agua_termal", A.f_companeros + 1.0, .4), ("papel", A.f_foros - 0.3, .5),
    ("viento", A.f_cualquiera2, .45), ("pasos_nieve", A.i_llegaron - 0.4, .5), ("agua_termal", A.i_llegaron + 3.0, .35),
    ("coro", A.i_silencio, .3), ("cuervos", A.i_atacar - 0.2, .4), ("latido", A.i_verdad - 0.3, .6),
    ("susto_carga", A.T_SUSTO3 - 0.03, 1.0),
    ("carga", A.T_VUELVE3 - 0.3, .75), ("hechizo", A.e_armas, .7), ("hechizo", A.e_armas + 1.0, .5),
    ("golpes_espada", A.e_mataron - 0.2, .8), ("caida", A.e_todos, .55), ("gritos", A.e_dolientes, .35),
    ("caida", A.e_defendio - 0.2, .4), ("tinta2", A.TR_CEM2 - 0.5, .5), ("almas", A.TR_CEM2, .5), ("campana", A.e_funeral, .55),
    ("teclado", A.v_subieron - 0.3, .5), ("pluma", A.v_correos - 0.2, .4), ("almas", A.v_videos, .3),
    ("tinta", A.TR_PLAZA - 0.45, .4), ("murmullo", A.TR_PLAZA, .5), ("tinta2", A.TR_CEM3 - 0.45, .4),
    ("viento", A.TR_CEM3, .4), ("vela", A.o_error - 0.2, .65), ("vela", A.o_plaga - 0.2, .5), ("vela", A.o_funeral - 0.2, .7),
    ("lapida", A.o_ustedes - 0.4, .5), ("coro", A.o_prometido, .35), ("losa", A.o_cerraste - 0.1, .75),
    ("tinta", A.TR_SELECCION - 0.6, .45), ("caja_musica", A.TR_SELECCION, .5), ("latido", A.o_sabe - 0.2, .5),
    ("susto_angel", A.T_SUSTO4 - 0.03, 1.0), ("caja_musica", A.T_CIERRE + 0.2, .35), ("apagar", A.T_NEGRO - 1.2, .6),
]
# (apagón, golpe) de cada jumpscare → audio/sustos.json: `mezcla` apaga todo entre ambos y saca el golpe al frente. Los «susto*»
# van aparte en audio/fx_sustos.wav (no en fx.wav, que entra a MEZCLA["fx"] y lo enterraba bajo la música).
SUSTOS_T = [(A.T_APAGON, A.T_SUSTO), (A.T_APAGON2, A.T_SUSTO2), (A.T_APAGON3, A.T_SUSTO3), (A.T_APAGON4, A.T_SUSTO4)]


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
    if "--seco" in sys.argv:
        for n, t, v in sorted(PISTAS, key=lambda x: x[1]):
            print(f"{t:7.2f}  {n:10s} {v}")
        from collections import Counter
        print(len(PISTAS), "golpes;", Counter(n for n, _, _ in PISTAS).most_common(5))
        print("faltan:", [n for n in SFX if not os.path.exists(f"sfx/{n}.mp3")],
              "≈", sum(d for n, (_, d) in SFX.items() if not os.path.exists(f"sfx/{n}.mp3")), "s")
        return
    generar()
    from sinte import SR
    N = int(TOTAL * SR)
    out, golpes, cache = np.zeros((2, N), np.float32), np.zeros((2, N), np.float32), {}
    for n, t, v in PISTAS:
        if n not in cache:
            x, _ = librosa.load(f"sfx/{n}.mp3", sr=SR, mono=False)
            x = np.vstack([x, x]) if x.ndim == 1 else x[:2]
            ini = int(np.argmax(np.abs(x).max(0) > 0.02 * np.abs(x).max()))
            x = x[:, ini:] / (np.abs(x).max() + 1e-9) * 0.7
            f = min(int(0.25 * SR), x.shape[1])
            x[:, -f:] *= np.linspace(1, 0, f, dtype=np.float32)
            cache[n] = x.astype(np.float32)
        x = cache[n]
        i = max(0, int(t * SR))
        x = x[:, :max(0, N - i)] * v
        (golpes if n.startswith("susto") else out)[:, i:i + x.shape[1]] += x
    os.makedirs("audio", exist_ok=True)
    for pista, ruta in ((out, "audio/fx.wav"), (golpes, "audio/fx_sustos.wav")):
        pico = float(np.abs(pista).max())
        if pico > 0.95:
            pista *= 0.95 / pico
        sf.write(ruta, pista.T, SR, subtype="PCM_16")
    with open("audio/sustos.json", "w", encoding="utf-8") as f:
        json.dump([[round(a, 3), round(b, 3)] for a, b in SUSTOS_T], f)
    print(f"audio/fx.wav: {len(PISTAS)} golpes en {TOTAL:.1f} s (pico {np.abs(out).max():.2f}); "
          f"audio/fx_sustos.wav + sustos.json: {len(SUSTOS_T)} susto(s)")


if __name__ == "__main__":
    main()
