# -*- coding: utf-8 -*-
"""Control de calidad de voz: CER contra el guion, similitud de hablante, artefactos."""
import os
import re
import unicodedata

import numpy as np
from rapidfuzz.distance import Levenshtein

UNIDADES = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
            "diez", "once", "doce", "trece", "catorce", "quince", "dieciseis", "diecisiete",
            "dieciocho", "diecinueve", "veinte", "veintiuno", "veintidos", "veintitres",
            "veinticuatro", "veinticinco", "veintiseis", "veintisiete", "veintiocho", "veintinueve"]
DECENAS = {30: "treinta", 40: "cuarenta", 50: "cincuenta", 60: "sesenta", 70: "setenta",
           80: "ochenta", 90: "noventa"}
CENTENAS = {100: "cien", 200: "doscientos", 300: "trescientos", 400: "cuatrocientos",
            500: "quinientos", 600: "seiscientos", 700: "setecientos", 800: "ochocientos",
            900: "novecientos"}


def num_es(n: int) -> str:
    if n < 30:
        return UNIDADES[n]
    if n < 100:
        d, u = divmod(n, 10)
        return DECENAS[d * 10] + ("" if u == 0 else " y " + UNIDADES[u])
    if n < 1000:
        c, r = divmod(n, 100)
        base = "ciento" if c == 1 and r else CENTENAS[c * 100]
        return base + ("" if r == 0 else " " + num_es(r))
    if n < 1_000_000:
        m, r = divmod(n, 1000)
        base = "mil" if m == 1 else num_es(m) + " mil"
        return base + ("" if r == 0 else " " + num_es(r))
    if n < 1_000_000_000_000:
        m, r = divmod(n, 1_000_000)
        base = "un millon" if m == 1 else num_es(m) + " millones"
        return base + ("" if r == 0 else " " + num_es(r))
    return str(n)


_EN_U = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
         "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
_EN_D = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def num_en(n: int, anio=True) -> str:
    """Cifra -> palabras en inglés (para el CER de videos en inglés: Whisper escribe «2009», el guion «two thousand
    nine»). Con `anio`, 1100-1999 y 2010-2099 se leen como años («nineteen ninety eight», «twenty twenty four»)."""
    if anio and (1100 <= n <= 1999 or 2010 <= n <= 2099):
        a, b = divmod(n, 100)
        return num_en(a, False) + (" hundred" if b == 0 else " " + (num_en(b, False) if b >= 10 else "oh " + _EN_U[b]))
    if n < 20:
        return _EN_U[n]
    if n < 100:
        d, u = divmod(n, 10)
        return _EN_D[d] + ("" if u == 0 else " " + _EN_U[u])
    if n < 1000:
        c, r = divmod(n, 100)
        return _EN_U[c] + " hundred" + ("" if r == 0 else " " + num_en(r, False))
    for base, nombre in ((1_000_000_000, " billion"), (1_000_000, " million"), (1000, " thousand")):
        if n >= base:
            m, r = divmod(n, base)
            return num_en(m, False) + nombre + ("" if r == 0 else " " + num_en(r, False))
    return str(n)


_IDIOMA = None


def _idioma():
    """Idioma de la voz del video (guion.py -> VOZ["idioma"]); por defecto español."""
    global _IDIOMA
    if _IDIOMA is None:
        try:
            import guion
            _IDIOMA = str(getattr(guion, "VOZ", {}).get("idioma", "es"))[:2].lower()
        except Exception:
            _IDIOMA = "es"
    return _IDIOMA


ORDINALES = {1: "primero", 2: "segundo", 3: "tercero", 4: "cuarto", 5: "quinto", 6: "sexto", 7: "septimo", 8: "octavo",
             9: "noveno", 10: "decimo"}


def _valor_romano(s: str) -> int:
    v = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
    tot = 0
    for a, b in zip(s, s[1:] + " "):
        tot += -v[a] if b in v and v[b] > v[a] else v[a]
    return tot


def _romanos(t: str) -> str:
    """Whisper escribe 'siglo XX' o 'Rodolfo II': se convierten a palabras (cardinal tras 'siglo', ordinal en los demás casos)."""
    def rep(m):
        ant = t[:m.start()].split()[-1:] or [""]
        n = _valor_romano(m.group(0))
        if ant[0].lower() == "siglo":
            return num_es(n)
        if len(m.group(0)) < 2:
            return m.group(0)
        return ORDINALES.get(n, num_es(n))
    return re.sub(r"\b(?=[IVXLC])(?:X{0,3}(?:IX|IV|V?I{0,3}))(?![a-zA-Z])", lambda m: rep(m) if m.group(0) else "", t)


_ALIAS = None


def _alias():
    """Alias de nombres propios: guion.py -> ALIAS_QA = {"variante que oye Whisper": "como está en el guion"} (en minúsculas y sin tildes)."""
    global _ALIAS
    if _ALIAS is None:
        try:
            import guion
            _ALIAS = {str(k).lower(): str(v).lower() for k, v in getattr(guion, "ALIAS_QA", {}).items()}
        except Exception:
            _ALIAS = {}
    return _ALIAS


def normaliza(t: str) -> str:
    t = _romanos(t.strip()).lower()
    t = re.sub(r"\ba\.\s?c\b\.?", " antes de cristo ", t)           # "221 a.C." = "doscientos veintiuno antes de Cristo"
    t = re.sub(r"\bd\.\s?c\b\.?", " despues de cristo ", t)
    # Whisper abrevia "Número seis: ..." como "6. ..."
    t = re.sub(r"^(\d+)\.(\s|$)", r"numero \1 ", t)
    t = t.replace("%", " percent" if _idioma() == "en" else " por ciento")
    # unidades que Whisper abrevia ("30 km por segundo", "-18 °C")
    t = re.sub(r"(\d)\s*km\b", r"\1 kilómetros", t)
    t = re.sub(r"(\d)\s*°\s*c\b", r"\1 grados", t)
    # 40.000 / 40,000 -> 40000
    while re.search(r"(\d)[\.,](\d{3})\b", t):                            # 1.100.000 -> 1100000 (varios grupos)
        t = re.sub(r"(\d)[\.,](\d{3})\b", r"\1\2", t)
    if _idioma() == "en":                                                  # inglés: «$37 million» / «1950s»
        t = re.sub(r"\$\s*([\d.]+)\s*(million|billion|thousand)?", r"\1 \2 dollars", t)
        t = re.sub(r"(\d)s\b", r"\1 s", t)
        t = re.sub(r"\d+", lambda m: " " + num_en(int(m.group())) + " ", t)
    else:
        t = re.sub(r"\d+", lambda m: " " + num_es(int(m.group())) + " ", t)
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^a-z0-9ñ ]+", " ", t)
    # los números escritos con cifras salen en masculino ("3700" -> setecientos): igualar el género
    t = re.sub(r"cientas\b", "cientos", t)
    # equivalencias fonéticas que Whisper escribe distinto
    t = t.replace("a d n", "adn").replace("self ie", "selfie").replace("wi fi", "wifi")
    t = t.replace("knockout", "nocaut").replace("knock out", "nocaut")      # el TTS dice "nocaut" a la inglesa
    t = " ".join(t.split())
    for var, canon in _alias().items():                                      # alias por video (nombres propios que Whisper escribe a su manera)
        t = re.sub(r"\b" + re.escape(var) + r"\b", canon, t)
    return t


def cer(ref: str, hyp: str) -> float:
    r, h = normaliza(ref).replace(" ", ""), normaliza(hyp).replace(" ", "")
    return Levenshtein.distance(r, h) / max(1, len(r))


def wer(ref: str, hyp: str) -> float:
    r, h = normaliza(ref).split(), normaliza(hyp).split()
    return Levenshtein.distance(r, h) / max(1, len(r))


class SpeakerSim:
    """Similitud coseno ECAPA (speechbrain) contra la voz de referencia."""

    def __init__(self, ref_path, device="cuda"):
        import torch
        import librosa
        from speechbrain.inference.speaker import EncoderClassifier
        self.torch, self.librosa = torch, librosa
        self.enc = EncoderClassifier.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modelos", "ecapa"),
            run_opts={"device": device})
        self.ref = self.embed_file(ref_path)

    def embed(self, wav16k: np.ndarray):
        x = self.torch.tensor(wav16k, dtype=self.torch.float32).unsqueeze(0)
        e = self.enc.encode_batch(x).squeeze()
        return e / e.norm()

    def embed_file(self, path):
        y, _ = self.librosa.load(path, sr=16000)
        return self.embed(y)

    def sim(self, wav, sr):
        y = self.librosa.resample(np.asarray(wav, dtype=np.float32), orig_sr=sr, target_sr=16000)
        return float((self.embed(y) * self.ref).sum())


def artefactos(wav: np.ndarray, sr: int) -> dict:
    """Métricas de salud de la toma: silencios internos largos, clipping, cola ruidosa."""
    import librosa
    y = np.asarray(wav, dtype=np.float32)
    iv = librosa.effects.split(y, top_db=40, frame_length=1024, hop_length=256)
    gaps = [(iv[i + 1][0] - iv[i][1]) / sr for i in range(len(iv) - 1)]
    peak = float(np.abs(y).max())
    # energía en el último 10% vs el cuerpo: detecta murmullos/ruido al final
    n = len(y)
    body = y[int(n * 0.1): int(n * 0.85)]
    tail = y[int(n * 0.92):]
    rms = lambda a: float(np.sqrt(np.mean(a ** 2)) + 1e-9)
    return {
        "gap_max": max(gaps) if gaps else 0.0,
        "peak": peak,
        "tail_ratio": rms(tail) / rms(body) if len(body) else 0.0,
        "speech_dur": float((iv[-1][1] - iv[0][0]) / sr) if len(iv) else 0.0,
    }


def silenciar_arranque(wav: np.ndarray, sr: int, max_bloque=0.35, min_hueco=0.20, min_resto=1.0):
    """Chatterbox a veces suelta un sonido ininteligible (0,1-0,4 s, «como un error») ANTES de la primera palabra, separado de ella por
    un silencio. Whisper lo ignora (CER 0), pero se oye (historia_espana, gancho_0: «Fe… Fenicios»). Si el primer bloque de voz es corto,
    el hueco siguiente es de >= min_hueco y después queda voz de sobra, lo silencia. Conserva la duración (los tiempos no cambian).
    Devuelve (wav, segundos silenciados); 0.0 si no hay nada que quitar. Úsalo sobre la toma ya recortada, antes de normalizar."""
    import librosa
    iv = librosa.effects.split(np.asarray(wav, dtype=np.float32), top_db=40, frame_length=1024, hop_length=256)
    if len(iv) < 2:
        return wav, 0.0
    bloque, hueco, resto = (iv[0][1] - iv[0][0]) / sr, (iv[1][0] - iv[0][1]) / sr, (iv[-1][1] - iv[1][0]) / sr
    if bloque > max_bloque or hueco < min_hueco or resto < min_resto:
        return wav, 0.0
    fin = iv[1][0] - int(0.05 * sr)                  # 50 ms de silencio antes de la palabra real
    out = np.array(wav, copy=True)
    out[:fin] = 0.0
    return out, fin / sr
