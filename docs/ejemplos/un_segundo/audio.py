# -*- coding: utf-8 -*-
"""Voz y efectos del video «Un segundo» con ElevenLabs (misma clave y voz que usa la Fábrica: Edoardo)."""
import json, os, subprocess, sys, time
import requests

AQUI = os.path.dirname(os.path.abspath(__file__))
CLAVE = open(r"C:\FabricaAnimaciones\canales\tokens\elevenlabs_api_key.txt", encoding="utf-8").read().strip()
URL = "https://api.elevenlabs.io/v1"
H = {"xi-api-key": CLAVE}
VOZ = "YqZLNYWZm98oKaaLZkUA"   # Edoardo

LINEAS = [
    "Jalpa, Zacatecas. Un martes cualquiera, a la hora del recreo.",
    "Diego tiene quince años, y hoy trae la torta que le hizo su mamá.",
    "De pronto, un empujón por la espalda. La torta, al piso. Y todos voltean.",
    "Alguien ya está grabando.",
    "En un segundo, el cuerpo de Diego decide por él. La cara caliente. El corazón a mil. Los puños cerrados.",
    "Primer final. Diego suelta el golpe.",
    "Emiliano cae, y se golpea la cabeza contra la banca. No se levanta.",
    "Diego no quería eso. Pero el video ya está en todos los grupos.",
    "Una ambulancia. La dirección. Sus papás, llegando sin entender nada.",
    "Diego repite: él empezó. Y es cierto. Él empezó. Pero el golpe fue suyo. Y cada quien responde por lo que hace.",
    "Ahora, rebobinemos.",
    "Mismo martes. Mismo empujón. Misma torta en el piso. El mismo calor en la cara.",
    "Pero esta vez, Diego hace algo rarísimo. Nada. Un segundo. Respira.",
    "Y lo dice, fuerte y claro: Oye. Me tiraste mi lonche. No me gustó. Fíjate.",
    "Emiliano, que venía corriendo de otro lado, se queda helado. Perdón, no te vi. Yo te invito otra.",
    "No fue magia. Diego seguía enojado. Y si el empujón hubiera sido a propósito, Emiliano también tendría que responder por él. Porque nadie se salva de las consecuencias de lo que hace.",
    "La diferencia entre las dos historias no fue el empujón. Ni quién tenía la razón.",
    "Fue un segundo.",
    "Ese segundo es tuyo. Nadie te lo puede quitar. ¿Qué vas a hacer con él?",
]

SFX = {
    "patio": ("School courtyard ambience at recess, teenagers chatting and laughing, distant basketball bouncing, birds", 10),
    "empujon": ("Sudden body bump impact with a short male gasp, then a soft object dropping on concrete", 2),
    "latido": ("Tense fast human heartbeat, close and bassy, steady rhythm", 7),
    "golpe": ("Single cinematic punch impact with a fast whoosh before it", 1.5),
    "asombro": ("A crowd of teenagers gasping in shock, then murmurs fading into silence", 4),
    "notif": ("Many smartphone notification dings and vibration buzzes piling up faster and faster", 5),
    "sirena": ("Distant ambulance siren approaching slowly, muffled through a window", 6),
    "rebobinar": ("Fast VHS tape rewind sound effect with squeal, ending in a click", 2.5),
    "respiro": ("One slow deep calm breath in and out, close microphone, quiet room", 4.5),
    "boom": ("Deep cinematic sub boom hit with a long reverb tail", 4),
    "oscuro": ("Dark tense cinematic underscore, low sustained strings and a slow pulsing drone, no melody, no drums", 22),
    "luz": ("Hopeful warm cinematic underscore, gentle piano notes over soft sustained strings, slow, emotional, no drums", 22),
    "inicio": ("Light warm acoustic guitar underscore, relaxed sunny morning, simple and soft", 22),
}


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def pedir(url, body, destino):
    for i in range(4):
        r = requests.post(url, json=body, headers=H, timeout=180)
        if r.status_code == 200:
            open(destino, "wb").write(r.content)
            return int(r.headers.get("character-cost") or 0)
        if r.status_code in (429, 500, 502, 503):
            time.sleep(5 * (i + 1)); continue
        print("ERROR", r.status_code, r.text[:300]); return -1
    return -1


os.makedirs(f"{AQUI}/voz", exist_ok=True); os.makedirs(f"{AQUI}/sfx", exist_ok=True)
gasto = 0
info = []
for n, t in enumerate(LINEAS):
    p = f"{AQUI}/voz/l{n + 1:02d}.mp3"
    if not os.path.exists(p) or f"l{n + 1:02d}" in sys.argv:
        body = dict(text=t, model_id="eleven_multilingual_v2", language_code="es", seed=int(os.environ.get("SEED", 7)) + n,
                    voice_settings=dict(stability=0.42, similarity_boost=0.8, style=0.4, use_speaker_boost=True),
                    previous_text=" ".join(LINEAS[max(0, n - 2):n]), next_text=LINEAS[n + 1] if n + 1 < len(LINEAS) else "")
        c = pedir(f"{URL}/text-to-speech/{VOZ}?output_format=mp3_44100_128", body, p); gasto += max(c, 0)
    info.append(dict(n=n + 1, texto=t, dur=round(dur(p), 2)))
    print(n + 1, info[-1]["dur"], flush=True)
for k, (txt, d) in SFX.items():
    p = f"{AQUI}/sfx/{k}.mp3"
    if not os.path.exists(p) or k in sys.argv:
        c = pedir(f"{URL}/sound-generation", dict(text=txt, duration_seconds=d, prompt_influence=0.45), p); gasto += max(c, 0)
    print(k, round(dur(p), 2) if os.path.exists(p) else "FALTA", flush=True)
json.dump(info, open(f"{AQUI}/voz/lineas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("total voz", round(sum(i["dur"] for i in info), 1), "s · créditos gastados", gasto)
