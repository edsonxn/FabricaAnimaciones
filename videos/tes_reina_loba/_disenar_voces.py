# -*- coding: utf-8 -*-
"""Voces DISEÑADAS para los personajes de La Reina Loba (el usuario, 12-nov-2026: las de la biblioteca suenan encerradas/con eco).
ElevenLabs Voice Design en la cuenta 2: POST /v1/text-to-voice/design → 3 previews por rol (mp3 en panel_voces/voz/d_<rol>_<n>.mp3,
ids en panel_voces/disenadas.json). Guardar la elegida: `python _disenar_voces.py guardar <rol> <n>` → POST /v1/text-to-voice.
Uso: python _disenar_voces.py [rol ...]   (sin roles = todos los que falten)
"""
import base64, json, os, re, sys
import requests

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(RAIZ, "..", "..", "nucleo"))
import tts_eleven  # noqa: E402

URL = "https://api.elevenlabs.io/v1"
KEY = dict(tts_eleven.cuentas())[2]
OUT = os.path.join(RAIZ, "panel_voces", "voz")
JS = os.path.join(RAIZ, "panel_voces", "disenadas.json")

LIMPIO = ("Studio-quality recording: close microphone, completely dry, no reverb, no echo, no room sound, no background noise, "
          "crisp and present like a professional dubbing booth. Speaks neutral Latin American Spanish (doblaje latino), "
          "no Spain accent.")

ROLES = {
    "pelagio": ("Pelagius III, the Mad Emperor: an aristocratic man around 30, high-strung and paranoid, nervous fast speech that "
                "jumps between giggly charm and sudden panic, slightly nasal, refined but unhinged, theatrical. ",
                "¡Más vino! ¡Más vino! ¡Vino! Oh, no podría, me pasa directo. Además, tengo tantas cosas que hacer. "
                "Tantos indeseables. ¡Mi verdugo lleva tres días sin dormir!"),
    "sheogorath": ("A whimsical fantasy trickster god: a middle-aged man with a flamboyant, theatrical, whimsical voice, "
                   "playful and unpredictable, sing-song cadence, mischievous, an eccentric gentleman host serving tea. ",
                   "¿Más té, Pelly, querido? Bienvenido a la engañosamente verde mente del emperador Pelagio Tercero. "
                   "Sí, así es. Estás dentro de la cabeza de un emperador muy, muy peculiar. ¿Queso? ¿No? Más para mí."),
    "corte": ("A medieval court nobleman and necromancer ritual master, around 50, deep resonant baritone, grave and solemn, "
              "measured cadence, commanding, dark and serious, epic fantasy. ",
              "Reina Loba. Escucha nuestra llamada y despierta. ¡Invocamos a Potema! Has dormido mucho tiempo el sueño "
              "sin sueños de la muerte. Ya no."),
    "pelagio2": ("Emperor Pelagius II: an old cold calculating monarch around 65, dry and stern, low voice, unhurried, "
                 "speaks of his daughter as a political asset, authoritative and unemotional. ",
                 "Tiene trece años. Edad suficiente para casarse. El rey de Soledad necesita una esposa, y el Imperio "
                 "necesita a Soledad. Eso es todo."),
    "mensajera": ("A young female court messenger around 25, warm alto voice, trembling with grief and fear, breaking news of a "
                  "death to a queen, sincere and emotional but clear. ",
                  "Majestad... Tu hijo está muerto. Lo quemaron dentro de su carruaje, camino a Ichidag. "
                  "Lo siento tanto. Está muerto."),
    "potema": ("Potema, the Wolf Queen of Solitude: a mature regal woman around 45, low velvety contralto, cold, cunning and "
               "imperious, quiet menace, every word controlled, a dark fantasy villain queen. ",
               "Hijos míos. He visto juego sucio, puñaladas por la espalda, salvajadas crueles y gratuitas. "
               "Y me complacen igual. Pero hoy, no os equivoquéis... hoy sois la guerra."),
    "uriel": ("Uriel III: a young ambitious nobleman around 25, clear confident tenor, proud and determined, "
              "a usurper crowning himself emperor, intense but controlled. ",
              "Desde esta noche, soy Uriel Septim Tercero. Emperador de Tamriel. Y el que diga lo contrario "
              "puede decírselo a mi madre."),
    "kintyra": ("Empress Kintyra II: a young woman around 20, proud and dignified, bright clear soprano with steel underneath, "
                "an imprisoned empress defiant and furious. ",
                "Tu presencia en la ceremonia no será bienvenida. Eso es todo. Adiós, tía. ¡Maldita seas, mírame! "
                "¡Soy tu emperatriz!"),
    "viejo": ("An elderly emperor and old priest around 75, deep gravelly weathered voice, wise, slow and sardonic, "
              "warm but authoritative, old age texture without being weak. ",
              "¿Sabías que los hechizos de encanto, incluso los más poderosos, duran poco? Un buen sueldo motiva más. "
              "En el futuro, querida Reina Loba, no pongas dos veces la misma trampa."),
}


def cargar():
    return json.load(open(JS, encoding="utf-8")) if os.path.exists(JS) else {}


def disenar(rol):
    desc, texto = ROLES[rol]
    r = requests.post(f"{URL}/text-to-voice/design", headers={"xi-api-key": KEY},
                      params={"output_format": "mp3_44100_192"},
                      json=dict(voice_description=desc + LIMPIO, text=texto, model_id="eleven_ttv_v3",
                                guidance_scale=5, loudness=0.5), timeout=180)
    if r.status_code != 200:
        raise SystemExit(f"{rol}: {r.status_code} {r.text[:400]}")
    d = r.json()
    ids = []
    for i, p in enumerate(d["previews"], 1):
        open(os.path.join(OUT, f"d_{rol}_{i}.mp3"), "wb").write(base64.b64decode(p["audio_base_64"]))
        ids.append(p["generated_voice_id"])
    return ids


def guardar(rol, n):
    j = cargar()
    gid = j[rol]["ids"][n - 1]
    nombre = f"ReinaLoba {rol} {n}"
    r = requests.post(f"{URL}/text-to-voice", headers={"xi-api-key": KEY}, timeout=120,
                      json=dict(voice_name=nombre, voice_description=(ROLES[rol][0] + LIMPIO)[:1000], generated_voice_id=gid))
    if r.status_code != 200:
        raise SystemExit(f"guardar {rol} {n}: {r.status_code} {r.text[:400]}")
    vid = r.json()["voice_id"]
    j[rol].setdefault("guardadas", {})[str(n)] = vid
    json.dump(j, open(JS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(rol, n, "→", vid)
    return vid


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "guardar":
        guardar(sys.argv[2], int(sys.argv[3]))
        sys.exit()
    j = cargar()
    roles = sys.argv[1:] or [r for r in ROLES if r not in j]
    for rol in roles:
        antes = tts_eleven.saldo(KEY)
        ids = disenar(rol)
        j[rol] = dict(ids=ids)
        json.dump(j, open(JS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{rol}: {len(ids)} previews · costo {antes - tts_eleven.saldo(KEY)} créditos", flush=True)
