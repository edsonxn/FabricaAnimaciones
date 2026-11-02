# -*- coding: utf-8 -*-
"""Voz con ElevenLabs (alternativa de pago a Chatterbox). Lo llama tts_gen.py cuando guion.py trae VOZ["motor"] = "elevenlabs".

guion.py:  VOZ = dict(motor="elevenlabs", voice_id="...", modelo="eleven_multilingual_v2", idioma="es",
                      referencia="<mp3 de muestra de esa voz>",   # para la similitud de voz de tts_select
                      tomas=1, stability=0.45, similarity_boost=0.8, style=0.35)
Clave en canales/tokens/elevenlabs_api_key.txt (no versionada). Cuentas de RESPALDO (20-oct-2026): elevenlabs_api_key_2.txt,
_3.txt…; cuando una cuenta se queda sin saldo (401/402) se sigue con la siguiente sin parar. `python nucleo/tts_eleven.py` = saldo
de cada cuenta. Cada toma cuesta créditos: por defecto 1 toma por frase;
tts_select marca las que fallan y `voz --seeds 5 --solo <keys>` las rehace con otra semilla.
Se envían la frase anterior y la siguiente (previous_text/next_text) para que la entonación fluya entre frases.
Registro de créditos gastados: voz/eleven_log.json.
Voz con actuación (docs/voz.md § «Corchetes»): modelo="eleven_v4_turbo" (POR DEFECTO desde el 26-oct-2026: mitad de créditos que
eleven_v4; ver modelo()) y etiquetas en inglés dentro de las frases del guion,
p. ej. "[sighs] Nadie lo sabía. [short pause] Ni yo."; config.py las quita para todo lo demás (Whisper, timeline, .srt).
Voz CLONADA en varias cuentas (2-nov-2026; p. ej. el clon de la voz Applio de Warcraft, docs/voz.md): cada cuenta le da otro
voice_id al mismo clon → VOZ["por_cuenta"] = {2: "<id en la 2>", 3: "<id en la 3>"}; post() pone el id de la cuenta en uso y
salta las que no lo tienen. Sirve como narrador o en VOZ_POR_FRASE (lleva su propio puntero de cuenta: no saca al narrador
de la cuenta 1). VOZ_POR_FRASE = "applio" no pasa por aquí: lo genera tts_applio (tts_gen.py).
Etiquetas que NO van con una voz: VOZ["sin_etiquetas"] = ("whisper", "excit") → se quita toda [..] que contenga ese texto.
"""
import io
import json
import os
import re
import time

import librosa
import requests
import soundfile as sf

try:
    import config
except ImportError:   # sin video activo (`python nucleo/tts_eleven.py` solo para ver saldos)
    config = None

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = os.path.join(RAIZ, "canales", "tokens")
CLAVE = os.path.join(TOKENS, "elevenlabs_api_key.txt")   # cuenta 1; respaldo: elevenlabs_api_key_2.txt, _3.txt…
URL = "https://api.elevenlabs.io/v1"
_activa = 0   # índice en cuentas() de la cuenta en uso; post() pasa a la siguiente cuando esta se queda sin saldo
_activa_clon = 0   # lo mismo para las frases con una voz de VOZ["por_cuenta"]


def cuentas():
    """[(n, clave)] en orden de uso: n=1 la principal, n≥2 las de respaldo (elevenlabs_api_key_<n>.txt)."""
    rutas = [(1, CLAVE)] + [(n, os.path.join(TOKENS, f"elevenlabs_api_key_{n}.txt")) for n in range(2, 10)]
    cs = [(n, open(p, encoding="utf-8").read().strip()) for n, p in rutas if os.path.exists(p)]
    if not cs:
        raise SystemExit(f"ElevenLabs: falta la clave en {CLAVE}")
    return cs


def clave():
    return cuentas()[_activa][1]


def saldo(k=None):
    d = requests.get(f"{URL}/user/subscription", headers={"xi-api-key": k or clave()}, timeout=30).json()
    return d["character_limit"] - d["character_count"]


def saldos():
    """[(n, saldo)] de cada cuenta; saldo None si la clave no responde (inválida, bloqueada)."""
    out = []
    for n, k in cuentas():
        try:
            out.append((n, saldo(k)))
        except (KeyError, ValueError, requests.RequestException):
            out.append((n, None))
    return out


def post(ruta, **kw):
    """POST a ElevenLabs con la cuenta activa: reintenta 429/5xx y, si la cuenta se queda sin saldo o la rechaza (401/402),
    sigue con la siguiente cuenta de respaldo. Devuelve la última respuesta (200 o el error que ya no tiene salida)."""
    global _activa, _activa_clon
    cs = cuentas()
    clones = (config.VOZ.get("por_cuenta") or {}) if config else {}
    # el mismo clon tiene otro voice_id en cada cuenta: sus frases llevan su PROPIO puntero de cuenta, para que una frase con
    # un clon (VOZ_POR_FRASE, en las cuentas 2-3) no arrastre al narrador fuera de la cuenta 1
    vid = next((v for v in clones.values() if v in ruta), None)
    i = _activa_clon if vid else _activa
    while True:
        n, k = cs[i]
        if vid and n not in clones:   # esta cuenta no tiene el clon: se salta sin pedir nada
            if i + 1 < len(cs):
                i += 1
                continue
            raise SystemExit(f"ElevenLabs: ninguna cuenta restante tiene el clon (VOZ['por_cuenta'] = {clones})")
        url = ruta.replace(vid, clones[n]) if vid else ruta
        for intento in range(4):
            r = requests.post(f"{URL}/{url}", headers={"xi-api-key": k}, **kw)
            if r.status_code not in (429, 500, 502, 503):
                break
            time.sleep(4 * (intento + 1))
        # 404 voice_not_found: una voz CLONADA solo vive en la cuenta donde se creó (la narradora de Gaia Eterna, en la 2)
        sin_voz = r.status_code in (400, 404) and "voice_not_found" in r.text
        if (r.status_code in (401, 402) or sin_voz) and i + 1 < len(cs):
            i += 1
            print(f"ElevenLabs: la cuenta {n} ya no puede ({r.status_code}: {r.text[:150]}); sigo con la cuenta "
                  f"{cs[i][0]}", flush=True)
            continue
        if vid:
            _activa_clon = i
        else:
            _activa = i
        return r


# Modelo por defecto desde el 26-oct-2026 (el usuario: «suena perfecto… el default debe ser turbo»): eleven_v4_turbo entiende los
# corchetes igual que eleven_v4 y cobra la MITAD (0,20 créditos/carácter frente a 0,40, medido con `character-cost`).
MODELO_DEFECTO = "eleven_v4_turbo"
TASA = {"eleven_v4_turbo": 0.20, "eleven_v4": 0.40, "eleven_v3": 0.40, "eleven_multilingual_v2": 0.40}
LOG = "voz/eleven_log.json"


def modelo():
    """Modelo de este video. Un guion que dice "eleven_v4" (copiado de un video viejo) pasa a eleven_v4_turbo, salvo que el video ya
    tenga tomas hechas con v4 (registro sin `modelo` = anterior al 26-oct = v4): así no cambia la voz a media obra.
    Para forzar v4 en un video nuevo: VOZ["modelo_fijo"] = True."""
    m = config.VOZ.get("modelo") or MODELO_DEFECTO
    if m != "eleven_v4" or config.VOZ.get("modelo_fijo"):
        return m
    log = json.load(open(LOG, encoding="utf-8")) if os.path.exists(LOG) else []
    if any(d.get("modelo", "eleven_v4") == "eleven_v4" for d in log):
        return "eleven_v4"
    return MODELO_DEFECTO


def es_v3():
    """Modelos expresivos (eleven_v3, eleven_v4 y sus variantes, turbo incluido): entienden etiquetas entre corchetes."""
    return any(v in modelo() for v in ("_v3", "_v4"))


def voz_de(key):
    """Voz de una frase: guion.VOZ_POR_FRASE = {"escena_i": "<voice_id>"} da otra voz a un personaje (el estafador, un testigo);
    las demás frases usan VOZ["voice_id"] (el narrador)."""
    import guion
    return getattr(guion, "VOZ_POR_FRASE", {}).get(key) or config.VOZ["voice_id"]


def sin_etiquetas(texto):
    """Quita las etiquetas que esta voz no lleva (VOZ["sin_etiquetas"]: trozos de texto, p. ej. "whisper" quita [whispers])."""
    malas = config.VOZ.get("sin_etiquetas") or ()
    if not malas:
        return texto
    limpio = re.sub(r"\[([^\]]+)\]\s*", lambda m: "" if any(x in m.group(1).lower() for x in malas) else m.group(0), texto)
    if limpio != texto:
        print(f"  (etiquetas quitadas por VOZ['sin_etiquetas']: {texto[:60]}…)", flush=True)
    return limpio.strip()


def tts(texto, seed, prev="", sig="", voice_id=None):
    v = config.VOZ
    if es_v3():
        # eleven_v3 / eleven_v4: entienden etiquetas entre corchetes; stability solo 0.0 (creativa) / 0.5 (natural) / 1.0 (robusta)
        # y no se les manda previous_text/next_text
        body = dict(text=texto, model_id=modelo(), seed=int(seed), voice_settings=dict(stability=v.get("stability", 0.5)))
        prev = sig = ""
    else:
        body = dict(text=texto, model_id=modelo(), seed=int(seed),
                    voice_settings=dict(stability=v.get("stability", 0.45), similarity_boost=v.get("similarity_boost", 0.8),
                                        style=v.get("style", 0.35), use_speaker_boost=True))
    if v.get("idioma"):
        body["language_code"] = v["idioma"]
    if prev:
        body["previous_text"] = prev
    if sig:
        body["next_text"] = sig
    r = post(f"text-to-speech/{voice_id or v['voice_id']}?output_format=mp3_44100_128", json=body, timeout=120)
    if r.status_code == 200:
        return r.content, int(r.headers.get("character-cost") or 0)
    raise SystemExit(f"ElevenLabs {r.status_code} (cuenta {cuentas()[_activa][0]}): {r.text[:300]}")


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
    global _activa
    chars = sum(len(p[2]) for p in pend)
    log_p = LOG
    log = json.load(open(log_p, encoding="utf-8")) if os.path.exists(log_p) else []
    mod = modelo()
    tasa = TASA.get(mod, 0.40)   # créditos por carácter de ese modelo (medidos con character-cost)
    sal = saldos()
    clones = config.VOZ.get("por_cuenta") or {}
    if config.VOZ["voice_id"] in clones.values():   # el NARRADOR es el clon: solo cuentan las cuentas que lo tienen
        sal = [(n, s if n in clones else 0) for n, s in sal]
    disp = sum(s for _, s in sal if s)
    _activa = next((i for i, (_, s) in enumerate(sal) if s), 0)   # empieza por la primera cuenta con saldo
    if mod != config.VOZ.get("modelo"):
        print(f"ElevenLabs: guion.py dice {config.VOZ.get('modelo')!r}; se usa {mod} (por defecto desde el 26-oct-2026, mitad de "
              f"créditos; VOZ['modelo_fijo']=True para no cambiarlo)", flush=True)
    print(f"ElevenLabs ({mod}): {len(pend)} tomas, {chars} caracteres (≈ {round(chars * tasa)} créditos); saldo "
          + " · ".join(f"cuenta {n}: {'?' if s is None else s}" for n, s in sal), flush=True)
    if chars * tasa > disp:
        print(f"  ⚠ no alcanza: faltan ≈ {round(chars * tasa - disp)} créditos; se genera lo que se pueda", flush=True)
    gasto = 0
    try:
        for n, key, texto, seed, path in pend:
            prev = " ".join(textos[max(0, n - 2):n])
            sig = textos[n + 1] if n + 1 < len(textos) else ""
            if es_v3():
                texto = sin_etiquetas(config.FRASES_TTS.get(key, texto))   # con las etiquetas [..] que config quitó del guion
            mp3, costo = tts(texto, seed, prev, sig, voice_id=voz_de(key))
            y, sr = librosa.load(io.BytesIO(mp3), sr=None, mono=True)
            sf.write(path, y, sr)
            gasto += costo
            cta = cuentas()[_activa_clon if voz_de(key) in clones.values() else _activa][0]
            log.append(dict(key=key, seed=seed, chars=len(texto), costo=costo, cuenta=cta, modelo=mod,
                            t=time.strftime("%Y-%m-%d %H:%M")))
            print(path, round(len(y) / sr, 2), f"costo {costo}", flush=True)
    finally:   # el registro se guarda aunque todas las cuentas se queden sin saldo a media ronda
        json.dump(log, open(log_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"ElevenLabs: gastados {gasto} créditos en esta ronda; saldo ≈ {disp - gasto}")


if __name__ == "__main__":
    for n, s in saldos():
        print(f"cuenta {n}: {'clave rechazada o sin respuesta' if s is None else f'{s} créditos'}")
