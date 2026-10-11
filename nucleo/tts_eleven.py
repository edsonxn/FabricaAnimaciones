# -*- coding: utf-8 -*-
"""Voz con ElevenLabs (alternativa de pago a Chatterbox). Lo llama tts_gen.py cuando guion.py trae VOZ["motor"] = "elevenlabs".

guion.py:  VOZ = dict(motor="elevenlabs", voice_id="...", modelo="eleven_multilingual_v2", idioma="es",
                      referencia="<mp3 de muestra de esa voz>",   # para la similitud de voz de tts_select
                      tomas=1, stability=0.45, similarity_boost=0.8, style=0.35)
Clave en canales/tokens/elevenlabs_api_key.txt (no versionada). Cada toma cuesta créditos: por defecto 1 toma por frase;
tts_select marca las que fallan y `voz --seeds 5 --solo <keys>` las rehace con otra semilla.
Se envían la frase anterior y la siguiente (previous_text/next_text) para que la entonación fluya entre frases.
Registro de créditos gastados: voz/eleven_log.json.
Voz con actuación (docs/voz.md § «Corchetes»): modelo="eleven_v4" (o eleven_v3) y etiquetas en inglés dentro de las frases del guion,
p. ej. "[sighs] Nadie lo sabía. [short pause] Ni yo."; config.py las quita para todo lo demás (Whisper, timeline, .srt).
"""
import io
import json
import os
import time

import librosa
import requests
import soundfile as sf

import config

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAVE = os.path.join(RAIZ, "canales", "tokens", "elevenlabs_api_key.txt")
URL = "https://api.elevenlabs.io/v1"


def clave():
    return open(CLAVE, encoding="utf-8").read().strip()


def saldo():
    d = requests.get(f"{URL}/user/subscription", headers={"xi-api-key": clave()}, timeout=30).json()
    return d["character_limit"] - d["character_count"]


def es_v3():
    """Modelos expresivos (eleven_v3, eleven_v4 y sus variantes): entienden etiquetas entre corchetes."""
    return any(v in config.VOZ.get("modelo", "") for v in ("_v3", "_v4"))


def voz_de(key):
    """Voz de una frase: guion.VOZ_POR_FRASE = {"escena_i": "<voice_id>"} da otra voz a un personaje (el estafador, un testigo);
    las demás frases usan VOZ["voice_id"] (el narrador)."""
    import guion
    return getattr(guion, "VOZ_POR_FRASE", {}).get(key) or config.VOZ["voice_id"]


def tts(texto, seed, prev="", sig="", voice_id=None):
    v = config.VOZ
    if es_v3():
        # eleven_v3 / eleven_v4: entienden etiquetas entre corchetes; stability solo 0.0 (creativa) / 0.5 (natural) / 1.0 (robusta)
        # y no se les manda previous_text/next_text
        body = dict(text=texto, model_id=v["modelo"], seed=int(seed), voice_settings=dict(stability=v.get("stability", 0.5)))
        prev = sig = ""
    else:
        body = dict(text=texto, model_id=v.get("modelo", "eleven_multilingual_v2"), seed=int(seed),
                    voice_settings=dict(stability=v.get("stability", 0.45), similarity_boost=v.get("similarity_boost", 0.8),
                                        style=v.get("style", 0.35), use_speaker_boost=True))
    if v.get("idioma"):
        body["language_code"] = v["idioma"]
    if prev:
        body["previous_text"] = prev
    if sig:
        body["next_text"] = sig
    for intento in range(4):
        r = requests.post(f"{URL}/text-to-speech/{voice_id or v['voice_id']}?output_format=mp3_44100_128", json=body,
                          headers={"xi-api-key": clave()}, timeout=120)
        if r.status_code == 200:
            return r.content, int(r.headers.get("character-cost") or 0)
        if r.status_code in (429, 500, 502, 503):
            time.sleep(4 * (intento + 1))
            continue
        raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:300]}")
    raise SystemExit("ElevenLabs no respondió tras 4 intentos")


def generar(frases, seeds, solo, out):
    seeds = seeds[:config.VOZ.get("tomas", 1)]
    textos = [t for _, _, t in frases]
    pend = []
    for n, (esc, idx, texto) in enumerate(frases):
        key = f"{esc}_{idx}"
        if solo and key not in solo:
            continue
        for seed in seeds:
            path = f"{out}/{key}_s{seed}.wav"
            if not os.path.exists(path):
                pend.append((n, key, texto, seed, path))
    if not pend:
        print("ElevenLabs: nada pendiente")
        return
    chars = sum(len(p[2]) for p in pend)
    disp = saldo()
    print(f"ElevenLabs: {len(pend)} tomas, {chars} caracteres; saldo {disp} créditos", flush=True)
    log_p = "voz/eleven_log.json"
    log = json.load(open(log_p, encoding="utf-8")) if os.path.exists(log_p) else []
    gasto = 0
    for n, key, texto, seed, path in pend:
        prev = " ".join(textos[max(0, n - 2):n])
        sig = textos[n + 1] if n + 1 < len(textos) else ""
        if es_v3():
            texto = config.FRASES_TTS.get(key, texto)   # con las etiquetas [..] que config quitó del guion
        mp3, costo = tts(texto, seed, prev, sig, voice_id=voz_de(key))
        y, sr = librosa.load(io.BytesIO(mp3), sr=None, mono=True)
        sf.write(path, y, sr)
        gasto += costo
        log.append(dict(key=key, seed=seed, chars=len(texto), costo=costo, t=time.strftime("%Y-%m-%d %H:%M")))
        print(path, round(len(y) / sr, 2), f"costo {costo}", flush=True)
    json.dump(log, open(log_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"ElevenLabs: gastados {gasto} créditos en esta ronda; saldo ≈ {disp - gasto}")
