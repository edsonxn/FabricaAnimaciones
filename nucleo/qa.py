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
    return str(n)


def normaliza(t: str) -> str:
    t = t.strip().lower()
    # Whisper abrevia "Número seis: ..." como "6. ..."
    t = re.sub(r"^(\d+)\.(\s|$)", r"numero \1 ", t)
    t = t.replace("%", " por ciento")
    # unidades que Whisper abrevia ("30 km por segundo", "-18 °C")
    t = re.sub(r"(\d)\s*km\b", r"\1 kilómetros", t)
    t = re.sub(r"(\d)\s*°\s*c\b", r"\1 grados", t)
    # 40.000 / 40,000 -> 40000
    t = re.sub(r"(\d)[\.,](\d{3})\b", r"\1\2", t)
    t = re.sub(r"\d+", lambda m: " " + num_es(int(m.group())) + " ", t)
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^a-z0-9ñ ]+", " ", t)
    # equivalencias fonéticas que Whisper escribe distinto
    t = t.replace("a d n", "adn").replace("self ie", "selfie").replace("wi fi", "wifi")
    return " ".join(t.split())


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
