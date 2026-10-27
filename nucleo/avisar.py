# -*- coding: utf-8 -*-
"""Aviso por voz AUTÓNOMO (sin servidor, sin puerto 3000).

    python fab.py avisar "Ya terminó el render"          (o: python nucleo/avisar.py "texto")

POR DEFECTO (el usuario, 27-oct-2026: «para no gastar CPU ni GPU, siempre ElevenLabs»): ELEVENLABS en la nube (voz Alberto
Rodríguez, eleven_v4_turbo, ~0,2 créditos/carácter; las cuentas de respaldo de tts_eleven.post) con caché de WAV por texto;
sin red o sin saldo cae a la VOZ DE WINDOWS. Motivo: un aviso con Chatterbox se quedó colgado 45 min ocupando la GPU junto a
un `verificar`. `--chatterbox` vuelve al camino viejo (lo de abajo).

Por defecto se DESPRENDE: devuelve el control de inmediato y un proceso aparte sintetiza y habla (puede tardar de unos
segundos a ~1 min la primera vez que carga el modelo). `--esperar` bloquea hasta que termine de sonar.
Voz y parámetros salen de panel_config.json (por defecto Faraon, como los avisos del panel); la caché de WAV
(panel_avisos/) es la misma del panel: un aviso repetido suena al instante. Avisos en fila: un candado de archivo
los serializa, nunca se empalman. Si Chatterbox no puede (GPU ocupada por un render, error, sin modelo) cae a la voz
de Windows en español, para que el aviso SIEMPRE se oiga. Registro: panel_avisos/avisar_log.txt.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import avisos  # noqa: E402  (solo se usan sus funciones: config y texto hablado; no arranca el panel)

DIR = avisos.DIR
LOG = os.path.join(DIR, "avisar_log.txt")
CANDADO = os.path.join(DIR, "avisar.lock")
MIN_LIBRE_GB = 3.0          # VRAM libre mínima para intentar Chatterbox; con menos (render en marcha) va directo a la voz de Windows
SIN_VENTANA = getattr(subprocess, "CREATE_NO_WINDOW", 0)
ELEVEN_VOZ = "l1zE9xgNpUTaQCZzpNJa"   # Alberto Rodríguez (latino neutro, la de Cronopapel)
ELEVEN_MODELO = "eleven_v4_turbo"


def log(msg):
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")
    except OSError:
        pass


def texto_hablado(texto):
    t = re.sub(r"https?://\S+", "", texto)                   # los links no se dictan
    t = re.sub(r"[A-Za-z]:[\\/][^\s,;]*", "", t)             # ni las rutas de archivo
    t = t.replace("*", "").replace("`", "").replace("#", "")
    return avisos.hablar(t)


def sintetizar(hablado, cfg, ruta):
    """Chatterbox en este mismo proceso. True si dejó el WAV en `ruta`."""
    import torch
    if not torch.cuda.is_available():
        log("sin CUDA: voz de Windows")
        return False
    libre = torch.cuda.mem_get_info()[0] / 2**30
    if libre < MIN_LIBRE_GB:
        log(f"VRAM libre {libre:.1f} GB < {MIN_LIBRE_GB}: voz de Windows")
        return False
    import torchaudio as ta
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    t0 = time.time()
    modelo = ChatterboxMultilingualTTS.from_pretrained(device="cuda", t3_model="v3")
    modelo.prepare_conditionals(cfg["voz"], exaggeration=cfg["exaggeration"])
    torch.manual_seed(7)
    wav = modelo.generate(hablado, language_id="es", exaggeration=cfg["exaggeration"],
                          cfg_weight=cfg["cfg_weight"], temperature=cfg["temperature"]).detach().cpu()
    wav = wav / (float(wav.abs().max()) or 1.0) * 0.9        # volumen parejo entre avisos
    tmp = ruta + ".tmp.wav"
    ta.save(tmp, wav, modelo.sr, encoding="PCM_S", bits_per_sample=16)
    os.replace(tmp, ruta)                                    # la caché nunca queda con un WAV a medias
    log(f"Chatterbox OK en {time.time() - t0:.0f}s ({wav.shape[-1] / modelo.sr:.1f}s de audio)")
    return True


def tocar_wav(ruta):
    ps = f"(New-Object Media.SoundPlayer '{ruta}').PlaySync()"
    subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps], timeout=300, creationflags=SIN_VENTANA)


def voz_windows(hablado):
    ps = ("Add-Type -AssemblyName System.Speech; $s=New-Object System.Speech.Synthesis.SpeechSynthesizer; "
          "$v=$s.GetInstalledVoices() | Where-Object {$_.VoiceInfo.Culture.Name -like 'es-*'} | Select-Object -First 1; "
          "if($v){$s.SelectVoice($v.VoiceInfo.Name)}; $s.Speak($env:AVISO_TEXTO)")
    subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps], timeout=180, creationflags=SIN_VENTANA,
                   env=dict(os.environ, AVISO_TEXTO=hablado))


class Candado:
    """Exclusión entre procesos (msvcrt): los avisos hablan uno tras otro."""
    def __enter__(self):
        import msvcrt
        os.makedirs(DIR, exist_ok=True)
        self.f = open(CANDADO, "a+")
        fin = time.time() + 900
        while True:
            try:
                self.f.seek(0)
                msvcrt.locking(self.f.fileno(), msvcrt.LK_NBLCK, 1)
                return self
            except OSError:
                if time.time() > fin:
                    return self                              # no bloquear para siempre: habla igual
                time.sleep(0.5)

    def __exit__(self, *_):
        import msvcrt
        try:
            self.f.seek(0)
            msvcrt.locking(self.f.fileno(), msvcrt.LK_UNLCK, 1)
        except OSError:
            pass
        self.f.close()


def eleven(hablado, ruta):
    """ElevenLabs en la nube (cero GPU, casi cero CPU): PCM 24 kHz → WAV en `ruta`. True si quedó."""
    import wave
    import tts_eleven
    body = dict(text=hablado, model_id=ELEVEN_MODELO, language_code="es", voice_settings=dict(stability=0.5))
    r = tts_eleven.post(f"text-to-speech/{ELEVEN_VOZ}?output_format=pcm_24000", json=body, timeout=60)
    if r.status_code != 200 or len(r.content) < 2000:
        log(f"ElevenLabs {r.status_code}: {r.text[:200] if r.status_code != 200 else 'audio vacío'}")
        return False
    tmp = ruta + ".tmp.wav"
    with wave.open(tmp, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(24000)
        w.writeframes(r.content)
    os.replace(tmp, ruta)
    log(f"ElevenLabs OK ({r.headers.get('character-cost', '?')} créditos)")
    return True


def decir(texto, chatterbox=False):
    hablado = texto_hablado(texto)
    if not hablado:
        return
    if not chatterbox:                                   # por defecto (27-oct): ElevenLabs; sin red/saldo → voz de Windows
        ruta = os.path.join(DIR, "eleven_" + hashlib.sha1((hablado + ELEVEN_VOZ).encode("utf-8")).hexdigest()[:16] + ".wav")
        with Candado():
            ok = os.path.isfile(ruta) and os.path.getsize(ruta) > 2000
            if not ok:
                try:
                    ok = eleven(hablado, ruta)
                except (Exception, SystemExit) as e:     # sin red, sin clave, sin saldo: nunca quedarse mudo
                    log(f"ElevenLabs falló: {str(e)[:200]}")
                    ok = False
            if ok:
                tocar_wav(ruta)
            else:
                voz_windows(hablado)
        log(f"dicho ({'ElevenLabs' if ok else 'voz de Windows'}): {hablado[:80]}")
        return
    cfg = avisos.leer_config()
    clave = hashlib.sha1((hablado + cfg["voz"] + str(cfg["exaggeration"])).encode("utf-8")).hexdigest()[:16]
    ruta = os.path.join(DIR, f"{clave}.wav")          # misma clave que el Locutor del panel
    with Candado():
        ok = os.path.isfile(ruta) and os.path.getsize(ruta) > 2000
        if not ok:
            try:
                ok = sintetizar(hablado, cfg, ruta)
            except Exception as e:                       # OOM, modelo, voz inexistente...: nunca quedarse mudo
                log(f"Chatterbox falló: {str(e)[:200]}")
                ok = False
        if ok:
            tocar_wav(ruta)
        else:
            voz_windows(hablado)
        log(f"dicho ({'Chatterbox' if ok else 'voz de Windows'}): {hablado[:80]}")


def main():
    ap = argparse.ArgumentParser(description="Aviso por voz autónomo (ElevenLabs; respaldo voz de Windows; Chatterbox con --chatterbox)")
    ap.add_argument("texto", nargs="+")
    ap.add_argument("--esperar", action="store_true", help="bloquea hasta que termine de sonar")
    ap.add_argument("--chatterbox", action="store_true", help="voz Chatterbox (usa la GPU); por defecto, ElevenLabs")
    ap.add_argument("--hijo", action="store_true", help=argparse.SUPPRESS)
    a = ap.parse_args()
    texto = " ".join(a.texto)
    os.makedirs(DIR, exist_ok=True)
    if a.esperar or a.hijo:
        decir(texto, a.chatterbox)
        return
    flags = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | SIN_VENTANA
    salida = open(LOG, "a", encoding="utf-8")
    subprocess.Popen([sys.executable, os.path.abspath(__file__), "--hijo", texto] + (["--chatterbox"] if a.chatterbox else []),
                     stdin=subprocess.DEVNULL,
                     stdout=salida, stderr=salida, creationflags=flags, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    print("Aviso en marcha (se oirá en unos segundos).")


if __name__ == "__main__":
    main()
