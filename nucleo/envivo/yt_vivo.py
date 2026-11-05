# -*- coding: utf-8 -*-
"""Clips de YouTube EN VIVO (el usuario, 4-nov-2026, noche): gameplay del tema actual sin descargar nada.

«¿Se puede no bajar y solo reproducir y pasarlos al stream?» → yt-dlp busca SOLO metadatos (`ytsearch8 … --flat-playlist`),
haiku elige 2-3 por título y duración (fuera tráileres, reacciones, otros juegos y < 2 min), y `yt-dlp -g` da el enlace
directo de googlevideo (solo video, avc1 ≤ 720p) que la pantalla reproduce tal cual en su <video>. Los enlaces caducan
(~6 h) y van atados a la IP pública de la casa (la tele comparte la de la PC). Caché en memoria por tema y tope de llamadas
por minuto; si algo falla, la pantalla usa el clip del disco (biblioteca.py) y nadie lo nota.
RIESGO: en un directo real de YouTube, el gameplay de otros canales puede activar reclamos de derechos de autor.
"""
import json
import random
import re
import subprocess
import threading
import time
from collections import deque

POR_MINUTO = 12           # llamadas a yt-dlp como mucho por minuto (una búsqueda + 3 enlaces = 4 por tema)
CADUCA_S = 3 * 3600       # el enlace de googlevideo dura ~6 h: se pide otro pasadas 3
REFRESCO_S = 20 * 60      # con el mismo tema, otra búsqueda cada 20 min trae clips nuevos
SIN_VENTANA = getattr(subprocess, "CREATE_NO_WINDOW", 0)


class ClipsYT:
    def __init__(self, juego="skyrim", apunta=print, al_llegar=None):
        self.juego, self.apunta, self.al_llegar = juego, apunta, al_llegar
        self.activo = True
        self.cache = {}                          # tema → {"t", "clips": [...], "i"}
        self.trabajando = set()
        self.llamadas = deque()
        self.cv = threading.Lock()
        self.medidas = {}                        # tema → instante del pedido (para medir hasta el primer clip al aire)

    # --- límites -----------------------------------------------------------------------------------
    def _turno(self):
        while True:
            with self.cv:
                ahora = time.time()
                while self.llamadas and ahora - self.llamadas[0] > 60:
                    self.llamadas.popleft()
                if len(self.llamadas) < POR_MINUTO:
                    self.llamadas.append(ahora)
                    return
            time.sleep(2)

    def _ytdlp(self, args, timeout=40):
        self._turno()
        r = subprocess.run(["yt-dlp", "--no-warnings", *args], capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout, creationflags=SIN_VENTANA)
        if r.returncode != 0 and ("429" in r.stderr or "Sign in to confirm" in r.stderr):
            self.apunta("YouTube frenó a yt-dlp: clips del disco un rato")
            with self.cv:                          # 2 min sin pedir nada
                self.llamadas.extend([time.time() + 60] * POR_MINUTO)
        return r.stdout

    # --- pedir y dar -------------------------------------------------------------------------------
    def pedir(self, tema):
        """Busca en segundo plano si no hay clips frescos para el tema (no bloquea)."""
        if not self.activo or not tema:
            return
        with self.cv:
            c = self.cache.get(tema)
            if tema in self.trabajando or (c and time.time() - c["t"] < REFRESCO_S):
                return
            self.trabajando.add(tema)
            self.medidas.setdefault(tema, time.time())
        threading.Thread(target=self._buscar, args=(tema,), daemon=True).start()

    def dar(self, tema):
        """El siguiente clip del tema (o None: la pantalla usa el del disco)."""
        if not self.activo:
            return None
        with self.cv:
            c = self.cache.get(tema)
            vivos = [x for x in (c or {}).get("clips", []) if time.time() - x["t"] < CADUCA_S]
            if not vivos:
                return None
            c["i"] = (c["i"] + 1) % len(vivos)
            x = vivos[c["i"]]
            return {"url": x["url"], "dur": x["dur"], "titulo": x["titulo"], "canal": x["canal"], "id": x["id"],
                    "desde": round(x["dur"] * random.uniform(0.10, 0.85), 1)}

    def al_aire(self, tema):
        """La pantalla avisa que salió el primer clip de YouTube: latencia desde el pedido."""
        t = self.medidas.pop(tema, None)
        if t:
            self.apunta(f"LATENCIA clip YouTube: {time.time() - t:.1f} s desde el cambio a «{tema}»")

    # --- la búsqueda -------------------------------------------------------------------------------
    def _buscar(self, tema):
        t0 = time.time()
        try:
            consulta = self._consulta(tema)
            crudo = self._ytdlp([f"ytsearch8:{self.juego} {consulta} gameplay no commentary", "--flat-playlist", "-j"])
            cands = []
            for l in crudo.splitlines():
                try:
                    d = json.loads(l)
                except ValueError:
                    continue
                titulo, dur = d.get("title") or "", d.get("duration") or 0
                if dur < 120 or re.search(r"trailer|tráiler|react|reacci|review|top \d+|#shorts", titulo, re.I):
                    continue
                cands.append({"id": d["id"], "titulo": titulo, "dur": dur, "canal": d.get("channel") or d.get("uploader") or ""})
            elegidos = self._elegir(tema, cands)[:3]
            clips = []
            for c in elegidos:
                url = self._ytdlp(["-g", "-f", "bv*[height<=480][vcodec^=avc1]/18", f"https://www.youtube.com/watch?v={c['id']}"]).strip()
                url = url.splitlines()[0] if url else ""
                if url.startswith("http"):           # cada clip se usa en cuanto llega su enlace (no espera a los 3)
                    clips.append({**c, "url": url, "t": time.time()})
                    with self.cv:
                        self.cache[tema] = {"t": time.time(), "clips": list(clips), "i": -1}
                    if self.al_llegar:
                        self.al_llegar(tema)
            self.apunta(f"YouTube «{tema}»: {len(clips)} clip(s) en {time.time() - t0:.0f} s"
                        + (" · " + " | ".join(c["titulo"][:40] for c in clips) if clips else " (se quedan los del disco)"))
        except Exception as e:
            self.apunta(f"YouTube «{tema}» falló: {e!r} (se quedan los del disco)")
        finally:
            with self.cv:
                self.trabajando.discard(tema)

    def _consulta(self, tema):
        """El tema en inglés, corto, para buscar (haiku sin pensar; si falla, el tema tal cual)."""
        from envivo import chat
        try:
            r = chat._llamar(f"Traduce al inglés como búsqueda de YouTube de 2-5 palabras, sin comillas ni nada más, "
                             f"el tema de {self.juego}: {tema}", "haiku").strip().splitlines()
            return re.sub(r"[\"'«»]", "", r[0])[:60] if r and r[0] else tema
        except Exception:
            return tema

    def _elegir(self, tema, cands):
        if len(cands) <= 2:
            return cands
        from envivo import chat
        lista = "\n".join(f"{i}. {c['titulo']} ({c['dur'] // 60} min) — {c['canal']}" for i, c in enumerate(cands))
        try:
            r = chat._llamar(f"Tema del directo de {self.juego}: «{tema}». De estos videos de YouTube, elige los 3 que MEJOR "
                             f"enseñen gameplay de ese tema EN {self.juego} (nada de tráileres, reacciones, otros juegos ni "
                             f"compilaciones de memes). Contesta solo los números separados por comas.\n{lista}", "haiku")
            idx = [int(n) for n in re.findall(r"\d+", r or "")]
            elegidos = [cands[i] for i in dict.fromkeys(idx) if 0 <= i < len(cands)]
            return elegidos or cands
        except Exception:
            return cands
