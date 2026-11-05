# -*- coding: utf-8 -*-
"""EN VIVO: un directo que se genera y se edita solo mientras se ve, y que cambia de tema cuando se lo piden.

    python fab.py envivo [canal] [--tema "…"] [--modelo sonnet|haiku] [--voz Raul] [--puerto 8790] [--abrir]

- Pantalla (lo que se transmite; en OBS como «Fuente de navegador»): http://127.0.0.1:8790/
- Ventanita de control (cambiar tema, votación, pausa):            http://127.0.0.1:8790/control

Cómo funciona: un hilo «productor» mantiene un búfer de BUFER bloques listos (~20-30 s cada uno): el director
(Claude por `claude -p`, GUIONISTAS a la vez) escribe 4-6 frases y elige pegatina/clip/rótulo de cada una, la voz de Windows las dice y las
imágenes que falten se bajan de la wiki del juego. La pantalla pide el siguiente bloque ~4 s antes de que acabe el
actual. Un cambio de tema tira el búfer (lo ya escrito para el tema viejo) y el siguiente bloque abre con un puente.
Votación: cada bloque trae 3 temas posibles; al pedir el siguiente bloque se cuenta el voto y el ganador manda.
Todo lo dicho queda en _sesiones/<fecha>/guion.jsonl (para cortar después un video o Shorts del directo).
"""
import argparse
import concurrent.futures as cf
import json
import os
import random
import re
import sys
import threading
import time
from collections import deque

from flask import Flask, abort, jsonify, request, send_file, send_from_directory

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
from envivo import chat as chat_mod, director, voz         # noqa: E402
from envivo.yt_vivo import ClipsYT                          # noqa: E402
from envivo.biblioteca import CANALES, VIDEOS, Biblioteca, palabras  # noqa: E402

BUFER = 2           # bloques listos por delante del que está al aire: más = menos riesgo de hueco, más tarda un cambio de tema
GUIONISTAS = 2      # llamadas a `claude -p` a la vez (cada una ~8 s de arranque + ~3 s por frase)


class Directo:
    def __init__(self, canal, tema, modelo, voz_nombre, velocidad):
        self.canal, self.cfg = canal, CANALES[canal]
        self.modelo, self.voz, self.velocidad = modelo, voz_nombre, velocidad
        self.motor_voz = voz
        if voz_nombre.lower().startswith("chatterbox"):     # --voz chatterbox:Sarcastica = la voz del canal en la GPU (voz_chatterbox.py)
            from envivo import voz_chatterbox
            self.motor_voz, self.voz = voz_chatterbox, (voz_nombre.split(":", 1)[1] if ":" in voz_nombre else "Sarcastica")
        self.carpeta = os.path.join(AQUI, "_sesiones", time.strftime("%Y%m%d_%H%M%S"))
        os.makedirs(self.carpeta, exist_ok=True)
        self.bib = Biblioteca(canal, os.path.join(AQUI, "_cache", canal))
        self.cv = threading.Condition()
        self.tema, self.tema_ver = tema or self.cfg["tema_inicial"], 0
        self.ultimo_tema = None           # tema del último bloque escrito (para saber si toca puente)
        self.cola, self.historial = [], []
        self.al_aire, self.frase_al_aire = None, -1
        self.opciones, self.votos, self.votacion = [], {}, False
        self.pausado, self.estado, self.n = False, "arrancando", 0
        self.anuncio = None
        self.log = deque(maxlen=60)
        self.tiempos = deque(maxlen=10)
        self.seq, self.en_curso, self.listos = 0, {}, {}
        self.enfoques, self.enfoques_ver, self.vers_abiertas = deque(), 0, set()
        self.pedido_por = []              # autores del chat que pidieron el tema actual (para el puente)
        self.en_resp = {}                 # bloques cortos que contestan al chat: van al frente de la cola
        self.bloques = {}                 # id → bloque (para la pantalla espejo del panel)
        # latencia del cambio de tema (el usuario, 4-nov noche): una frase puente sale al aire entre lat_min y lat_max s
        # después del cambio; la frase en curso SIEMPRE se termina (solo una de > 15 s restantes pasado el máximo se recorta)
        self.puente_inmediato, self.lat_min, self.lat_max = True, 3.0, 8.0
        self.cambios = {}                 # tema_ver → {"t", "tema", "origen", "puente": s, "bloque": s} (latencia real medida)
        self.latencias = deque(maxlen=12)
        # voces (el usuario, 4-nov noche): Windows / Chatterbox / 7 de ElevenLabs, relevo visible y discusión entre ellas
        self.voz_clave = self._clave_voz(voz_nombre)
        if self.voz_clave.startswith("eleven:"):
            self.motor_voz, self.voz, _ = self._motor(self.voz_clave)
        self.voz_desde = time.time()
        self.auto_relevo, self.auto_min = False, 5.0      # si una voz lleva > auto_min, entra otra al azar
        self.discusion = []                              # [clave, clave(, clave)]: el director escribe un intercambio
        self.yt = ClipsYT(apunta=self._apunta, al_llegar=self._yt_llego)   # gameplay de YouTube en vivo (yt_vivo.py)
        self.clip_al_aire = None                    # {"fuente": "yt"|"disco", "titulo", "canal"}: lo informa la pantalla
        self.chat = chat_mod.Chat(self)
        self._apunta(f"biblioteca: {len(self.bib.pegatinas)} pegatinas, {len(self.bib.clips)} clips, {len(self.bib.ost)} pistas de OST")
        if self.motor_voz is not voz:                # el modelo se carga antes del primer bloque (~20-40 s)
            t0 = time.time()
            self.motor_voz.preparar(self.voz, canal)
            fon = getattr(self.motor_voz, "_fonetica", None)   # voz_eleven no la tiene (arrancar con --voz eleven:X)
            self._apunta(f"voz «{self.voz}» lista en {time.time() - t0:.0f} s"
                         + (f" ({len(fon)} palabras de FONETICA)" if fon is not None else ""))
        self.yt.pedir(self.tema)
        threading.Thread(target=self._vigila_relevo, daemon=True).start()
        threading.Thread(target=self._productor, daemon=True).start()

    def _apunta(self, txt):
        self.log.append(time.strftime("%H:%M:%S ") + txt)
        print(txt, flush=True)

    # --- control -------------------------------------------------------------------------------
    def cambiar_tema(self, tema, origen="control", conservar=0):
        """Tira el búfer del tema viejo. conservar=1 (votación): deja sonar un bloque más mientras se escribe el ganador,
        así no hay hueco. Desde el control queda 1 bloque de RELLENO (sin marca): la pantalla lo pone solo si el tema
        nuevo aún no está y lo deja a media frase en cuanto llega (el primer bloque nuevo tarda ~25 s en escribirse)."""
        tema = (tema or "").strip()[:120]
        if not tema:
            return
        if self.puente_inmediato:
            conservar = 0                               # la frase puente tapa el hueco: nada del tema viejo por delante
        with self.cv:
            self.cola = [s for s in self.cola if not s.get("inmediato")]     # el puente de un cambio anterior ya no vale
            for s in self.cola[:conservar]:
                s["conservado"] = True                  # la pantalla no lo descarta aunque sea del tema viejo
            quedan = max(conservar, 1)
            # las respuestas al chat ya escritas se quedan (ya marcaron sus comentarios como contestados)
            tirados = [s["id"] for s in self.cola[quedan:] if not s.get("respuesta")]
            for s in self.cola[quedan:]:
                s["conservado"] = s.get("conservado") or s.get("respuesta")
            self.historial = [h for h in self.historial if h[0] not in tirados]
            self.cola[quedan:] = [s for s in self.cola[quedan:] if s.get("respuesta")]
            anterior = self.tema
            self.tema, self.tema_ver = tema, self.tema_ver + 1
            self.anuncio = {"tema": tema, "origen": origen, "t": time.time()}
            self.cambios[self.tema_ver] = {"t": time.time(), "tema": tema, "origen": origen}
            ver = self.tema_ver
            self.cv.notify_all()
        self._apunta(f"TEMA NUEVO ({origen}): {tema}" + (f" · se tiraron {len(tirados)} bloques del búfer" if tirados else ""))
        self.yt.pedir(tema)
        if self.puente_inmediato:
            threading.Thread(target=self._puente, args=(tema, ver, origen, anterior), daemon=True).start()

    # frase puente (el usuario, 4-nov: «debe transicionar naturalmente al nuevo tema, no cortar de tajo»): cierra lo anterior
    # con una muletilla de conversación y ENLAZA con el tema nuevo; suena DESPUÉS de que acabe la frase en curso
    PUENTES = {
        "control": ["Bueno, y dejando {a} por aquí, que da para otro día, vamos con algo que también tiene miga: {t}.",
                    "Y ya que estamos en Tamriel, cambiemos de rincón. Hablemos de {t}.",
                    "Vale, {a} ya dio lo suyo. Ahora, otra historia que les va a gustar: {t}."],
        "panel": ["Bueno, y dejando {a} por aquí, que da para otro día, vamos con algo que también tiene miga: {t}.",
                  "Vale, {a} ya dio lo suyo. Ahora, otra historia que les va a gustar: {t}."],
        "chat": ["Y antes de seguir con {a}, el chat me está pidiendo otra cosa, y aquí se le hace caso: {t}.",
                 "Un momento, que el chat manda. Dejamos {a} y nos vamos a {t}.",
                 "Vale, vale, ya leí el chat. Cerramos {a} aquí y vamos con lo que piden: {t}."],
        "votación": ["Y con esto cerramos {a}, porque la votación ya tiene ganador: {t}.",
                     "Bueno, el chat votó y fue claro. Dejamos {a} y seguimos con {t}."],
    }

    def _puente(self, tema, ver, origen, anterior=None):
        """Frase corta que anuncia el tema nuevo en ~1-3 s (sin Claude): tapa la espera mientras se escribe el bloque."""
        try:
            t0 = time.time()
            a = (anterior or "").strip() or "esto"
            if len(a) > 60 or a.lower() == tema.lower():
                a = "esto"
            texto = random.choice(self.PUENTES.get(origen, self.PUENTES["control"])).format(t=tema, a=a)
            if origen == "chat" and self.pedido_por:
                texto += " Gracias, " + " y ".join(self.pedido_por[:2]) + "."
            sid = f"p{ver:03d}"
            extra = {} if self.motor_voz is voz else {"vigente": lambda: ver == self.tema_ver}
            (wav, dur), = self.motor_voz.sintetizar([texto], self.carpeta, sid, self.voz, self.velocidad, **extra)
            pegs, clips = self.bib.candidatos(tema)
            peg = None
            for clave in list(pegs)[:1]:
                v, slug = clave.split("/", 1)
                e = self.bib.pegatinas[clave]
                if not palabras(tema) & e["pal"]:           # sin parecido, mejor sin imagen que una equivocada
                    break
                peg = {"url": f"/pv/{v}/{slug}.png", "rec": f"/pv/{v}/_rec/{slug}.png" if e["rec"] else None, "nombre": tema}
            clip = list(clips)[0] if clips else self.bib.clip_para(tema)
            seg = {"id": sid, "tema": tema, "titulo": tema, "resumen": "frase puente del cambio de tema", "opciones": [],
                   "frases": [{"texto": texto, "dur": dur, "audio": "/s/" + os.path.basename(wav) if wav else None, "peg": peg,
                               "clip": f"/cv/{clip}.mp4" if clip else None, "rotulo": None, "ficha": None, "com": None}],
                   "proximos": [], "dur": dur + 0.25, "puente": True, "inmediato": True, "ver": ver, "coms": [], "origen": origen}
            with self.cv:
                if ver != self.tema_ver:
                    return
                self.cola.insert(0, seg)
                self.bloques[sid] = seg
                self.cv.notify_all()
            self._apunta(f"{sid}: frase puente lista en {time.time() - t0:.1f} s ({dur:.1f} s de voz)")
        except Exception as e:
            self._apunta(f"frase puente falló: {e!r}")

    # --- voces ------------------------------------------------------------------------------------------
    @staticmethod
    def _clave_voz(nombre):
        n = (nombre or "Raul").strip()
        if ":" in n:
            return n
        from envivo import voz_eleven
        return f"eleven:{n}" if n in voz_eleven.VOCES else f"windows:{n}"

    def _motor(self, clave):
        """clave → (módulo, nombre de la voz, nombre en pantalla)."""
        tipo, _, nombre = clave.partition(":")
        if tipo == "eleven":
            from envivo import voz_eleven
            return voz_eleven, nombre, nombre
        if tipo == "chatterbox":
            from envivo import voz_chatterbox
            return voz_chatterbox, nombre, nombre + " (Chatterbox)"
        return voz, nombre, {"Raul": "Raúl"}.get(nombre, nombre)

    def _perezosa(self):
        return not self.voz_clave.startswith("chatterbox:") and not self.discusion_chatterbox()

    def discusion_chatterbox(self):
        return any(c.startswith("chatterbox:") for c in self.discusion)

    def voces_disponibles(self):
        from envivo import voz_eleven
        vs = [f"eleven:{n}" for n in voz_eleven.VOCES] + ["windows:Raul"]
        cb = sys.modules.get("envivo.voz_chatterbox")
        if cb is not None and getattr(cb, "_modelo", None) is not None:
            vs.append("chatterbox:" + os.path.splitext(os.path.basename(cb._ref or "Sarcastica"))[0])
        return vs

    def _eleven_estado(self):
        from envivo import voz_eleven
        c = getattr(self, "_saldo_cache", None)
        if not c or time.time() - c[0] > 300:        # saldos cada 5 min (lectura gratis)
            s = sum(x for _, x in voz_eleven.saldos() if x)
            c = self._saldo_cache = (time.time(), s)
        return {"saldo": c[1], "gastado": voz_eleven.gastado["creditos"], "sin_saldo": voz_eleven.sin_saldo,
                "poco": c[1] < 3000, "horas": round(c[1] / 13000, 1)}

    def _voces_libres(self):
        """Con poco saldo de ElevenLabs, el azar y el chat solo eligen voces gratis."""
        est = self._eleven_estado()
        vs = self.voces_disponibles()
        return [v for v in vs if not v.startswith("eleven:")] if est["poco"] or est["sin_saldo"] else vs

    def _formato_discusion(self):
        if len(self.discusion) < 2:
            return None
        nombres = [self._motor(c)[2] for c in self.discusion]
        return ("FORMATO: este bloque es una DISCUSIÓN entre " + " y ".join(nombres) + ", los narradores del directo, con el "
                "humor del canal: se llevan la contraria, se interrumpen y se pican (sin insultos). Cada frase lleva \"voz\" "
                "con el nombre EXACTO de quien la dice (" + ", ".join(nombres) + ") y se alternan.")

    @staticmethod
    def _norm_nombre(t):
        import unicodedata
        t = unicodedata.normalize("NFD", str(t or "").lower())
        t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn")
        t = re.sub(r"\(.*?\)|elevenlabs|chatterbox|windows|[^a-z ]", " ", t)
        return re.sub(r"\b(el|la|los|las|don|dona)\b", " ", t).split()

    def _clave_de_nombre(self, quien):
        """«Profeta», «el profeta», «José», «Jose», «Mari Carmen» → su clave. Primero las voces de la discusión, luego todas."""
        q = "".join(self._norm_nombre(quien))
        if not q:
            return None
        for grupo in (list(self.discusion or []), self.voces_disponibles()):
            for c in grupo:
                n = "".join(self._norm_nombre(self._motor(c)[2]))
                if n and (n == q or n.startswith(q) or q.startswith(n)):
                    return c
        return None

    def _voz_de_frase(self, f):
        """La clave de voz de una frase. Se fija al ESCRIBIR el bloque (`clave`): un cambio de voz o de discusión a media cola
        no reasigna las frases que el director ya repartió; solo las que no llevan voz siguen a la voz vigente."""
        if f.get("clave"):
            return f["clave"]
        if f.get("vozde"):
            c = self._clave_de_nombre(f["vozde"])
            if c:
                f["clave"] = c
                return c
        return self.voz_clave

    def _voz_al_salir(self, seg):
        """Sintetiza (o rehace) la voz del bloque que va a sonar: solo se paga lo que se oye y un cambio de voz entra ya."""
        if seg.get("inmediato") or seg.get("relevo"):
            return
        claves = [self._voz_de_frase(f) for f in seg["frases"]]
        if seg.get("voz_hecha") == claves:
            return
        t0 = time.time()
        por_motor = {}
        for i, c in enumerate(claves):
            por_motor.setdefault(c, []).append(i)
        for c, idxs in por_motor.items():
            mod, nombre, _ = self._motor(c)
            if mod.__name__.endswith("voz_chatterbox") and getattr(mod, "_modelo", None) is None:
                mod, nombre, c = voz, "Raul", "windows:Raul"
            res = mod.sintetizar([seg["frases"][i]["texto"] for i in idxs], self.carpeta, f"{seg['id']}_{c.split(':')[1][:6]}",
                                 nombre, self.velocidad)
            for i, (wav, dur) in zip(idxs, res):
                f = seg["frases"][i]
                f["audio"], f["dur"], f["narra"] = ("/s/" + os.path.basename(wav)) if wav else None, dur, self._motor(c)[2]
        seg["dur"] = sum(f["dur"] + 0.25 for f in seg["frases"])
        seg["voz_hecha"] = claves
        self._apunta(f"{seg['id']}: voz {', '.join(sorted(set(self._motor(c)[2] for c in claves)))} en {time.time() - t0:.1f} s"
                     f" ({sum(len(f['texto']) for f in seg['frases'])} caracteres)")

    RELEVO_SALE = ["Hasta aquí llego yo, chat. Les dejo con {n}, que dice que lo hace mejor. Ya veremos.",
                   "Me retiro, que me llaman de Carrera Blanca. El mando es tuyo, {n}.",
                   "Suficiente por hoy para mí. {n}, todo tuyo; no rompas nada."]
    RELEVO_ENTRA = ["Gracias, {v}. Aquí {n}, y vengo a poner orden.", "Tomo el mando. Soy {n}, y {v} dejó todo hecho un desastre.",
                    "Gracias por calentar el asiento, {v}. Sigo yo: {n}."]

    def cambiar_voz(self, clave, origen="panel", pedido_por=()):
        """Relevo visible: la voz vieja se despide y pasa el mando, la nueva se presenta (bloque corto al frente de la cola)."""
        if clave not in self.voces_disponibles() or clave == self.voz_clave:
            return False
        vieja = self.voz_clave
        nv, nn = self._motor(vieja)[2], self._motor(clave)[2]
        textos = [random.choice(self.RELEVO_SALE).format(n=nn), random.choice(self.RELEVO_ENTRA).format(v=nv, n=nn)]
        if pedido_por:
            textos[1] += " Me pidió " + " y ".join("@" + a for a in pedido_por[:2]) + ", así que aquí estoy."
        frases = []
        for i, (c, t) in enumerate(zip((vieja, clave), textos)):
            mod, nombre, pantalla = self._motor(c)
            (wav, dur), = mod.sintetizar([t], self.carpeta, f"v{int(time.time())}_{i}", nombre, self.velocidad)
            frases.append({"texto": t, "dur": dur, "audio": "/s/" + os.path.basename(wav) if wav else None, "peg": None, "clip": None,
                           "rotulo": None, "ficha": None, "com": None, "narra": pantalla, "relevo": "sale" if i == 0 else "entra"})
        sid = f"v{int(time.time()) % 100000:05d}"
        seg = {"id": sid, "tema": self.tema, "titulo": f"{nv} → {nn}", "resumen": "relevo de narrador", "opciones": [], "frases": frases,
               "proximos": [], "dur": sum(f["dur"] + 0.25 for f in frases), "relevo": True, "ver": self.tema_ver, "coms": [],
               "conservado": True}
        with self.cv:
            self.voz_clave, self.voz_desde = clave, time.time()
            mod, self.voz, _ = self._motor(clave)
            self.motor_voz = mod
            self.cola.insert(0, seg)
            self.bloques[sid] = seg
            self.cv.notify_all()
        self._apunta(f"RELEVO ({origen}): {nv} → {nn}")
        return True

    def _vigila_relevo(self):
        while True:
            time.sleep(10)
            if self.auto_relevo and not self.discusion and time.time() - self.voz_desde > self.auto_min * 60:
                otras = [v for v in self._voces_libres() if v != self.voz_clave]
                if otras:
                    self.cambiar_voz(random.choice(otras), "automático")

    def _yt_llego(self, tema):
        """Los clips de YouTube llegaron (~20-30 s tras el cambio): se meten en los bloques del tema que ya esperan."""
        with self.cv:
            for s in self.cola:
                if s.get("tema") == tema:
                    for i, f in enumerate(s["frases"]):
                        if i % 2 == 0 and not f.get("yt"):
                            f["yt"] = self.yt.dar(tema)

    def al_aire_medir(self, seg, dt_pantalla=None):
        """Latencia real: del cambio de tema a la frase puente y al primer bloque escrito, al salir al aire."""
        c = self.cambios.get(seg.get("ver"))
        if not c or seg.get("respuesta"):
            return
        que = "puente" if seg.get("inmediato") else "bloque"
        if que in c:
            return
        c[que] = round(time.time() - c["t"], 1)
        self._apunta(f"LATENCIA {que}: {c[que]} s desde el cambio a «{c['tema']}» ({c['origen']})"
                     + (f" · la pantalla lo vio hace {dt_pantalla} s" if isinstance(dt_pantalla, (int, float)) and dt_pantalla < 600 else ""))
        if "bloque" in c:
            self.latencias.append({"tema": c["tema"], "origen": c["origen"], "puente": c.get("puente"), "bloque": c["bloque"]})

    def votar(self, opcion):
        with self.cv:
            if opcion in self.opciones:
                self.votos[opcion] = self.votos.get(opcion, 0) + 1

    def siguiente(self, espera=20.0):
        """La pantalla pide el próximo bloque. Antes cuenta la votación (si está activa y hubo votos)."""
        if self.votacion and self.votos:
            ganador = max(self.votos, key=self.votos.get)
            self.votos = {}
            if ganador != self.tema:
                self.cambiar_tema(ganador, origen="votación", conservar=1)
        fin = time.time() + espera
        with self.cv:
            while not self.cola and time.time() < fin:
                self.cv.wait(timeout=0.5)
            if not self.cola:
                return {"espera": True, "tema": self.tema, "anuncio": self.anuncio, "estado": self.estado}
            seg = self.cola.pop(0)
        self._voz_al_salir(seg)
        with self.cv:
            self.al_aire, self.frase_al_aire = seg, 0
            if not seg.get("inmediato"):
                self.opciones, self.votos = list(seg.get("opciones", [])), {}
            self.cv.notify_all()
        return seg

    # --- productor -----------------------------------------------------------------------------
    # GUIONISTAS bloques se escriben a la vez: cada bloque propone 2 «proximos» subtemas y cada guionista toma uno
    # (sabe qué escriben los otros para no pisarse). Se entregan a la cola en orden de despacho (seq).
    def _productor(self):
        while True:
            with self.cv:
                while not (self._puede_despachar() or self._puede_responder()):
                    self.cv.wait(timeout=1)
                tema, ver = self.tema, self.tema_ver
                if self._puede_responder():
                    coms = self.chat.para_contestar(2)
                    if coms:
                        self.seq += 1
                        job = {"seq": self.seq, "tema": tema, "ver": ver, "enfoque": None, "t0": time.time(), "coms": coms}
                        self.en_resp[self.seq] = job
                        hist = [h[1] for h in self.historial]
                        threading.Thread(target=self._responder, args=(job, hist), daemon=True).start()
                        continue
                    if not self._puede_despachar():
                        continue
                if self.enfoques_ver != ver:
                    self.enfoques, self.enfoques_ver = deque(), ver
                primero = not any(j["ver"] == ver for j in self.en_curso.values()) and ver not in self.vers_abiertas
                enfoque = self.enfoques.popleft() if self.enfoques else None
                puente = self.ultimo_tema if primero and self.ultimo_tema and self.ultimo_tema != tema else None
                if puente and self.anuncio and self.anuncio.get("origen") == "chat" and self.pedido_por:
                    puente = (puente, self.pedido_por)
                self.vers_abiertas.add(ver)
                paralelo = [j["enfoque"] or j["tema"] for j in self.en_curso.values() if j["ver"] == ver]
                hist = [h[1] for h in self.historial]
                self.seq += 1
                job = {"seq": self.seq, "tema": tema, "ver": ver, "enfoque": enfoque, "t0": time.time()}
                self.en_curso[self.seq] = job
                self.estado = f"escribiendo {len(self.en_curso)} ({self.modelo})"
            # tras un cambio de tema, el primer bloque es corto: el giro llega antes
            n_frases = 4 if primero else 6
            threading.Thread(target=self._trabajo, args=(job, puente, hist, paralelo, n_frases), daemon=True).start()

    def _puede_responder(self):
        """Hay comentarios que contestar y ningún bloque de respuesta en marcha (y el directo ya arrancó)."""
        return (not self.pausado and not self.en_resp and self.ultimo_tema is not None
                and any(c["contestar"] and c["estado"] in ("nuevo", "mostrado") for c in self.chat.comentarios))

    def _responder(self, job, hist):
        """Bloque corto (2-3 frases) que contesta al chat y vuelve al tema; se cuela al frente de la cola."""
        seg = None
        try:
            seg = self._producir(job["tema"], None, hist, job["ver"], n_frases=len(job["coms"]) + 1, sid=f"r{job['seq']:03d}",
                                 comentarios=job["coms"])
        except Exception as e:
            self._apunta(f"error al contestar el chat: {e!r}")
        with self.cv:
            self.en_resp.pop(job["seq"], None)
            if seg and seg["ver"] == self.tema_ver:
                seg["titulo"], seg["respuesta"] = "Leyendo el chat", True
                i = 0
                while i < len(self.cola) and (self.cola[i].get("conservado") or self.cola[i].get("respuesta")):
                    i += 1
                self.cola.insert(i, seg)
                self.bloques[seg["id"]] = seg
                self._guardar(seg)
                self._apunta(f"chat: contestados {', '.join('@' + c['autor'] for c in job['coms'])} en {seg['id']} "
                             f"({time.time() - job['t0']:.0f} s; sale tras el bloque al aire)")
            else:
                self.chat.devolver(job["coms"])
            self.cv.notify_all()

    def _guardar(self, seg):
        with open(os.path.join(self.carpeta, "guion.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(seg, ensure_ascii=False) + "\n")

    def _puede_despachar(self):
        if self.pausado or len(self.en_curso) >= GUIONISTAS:
            return False
        vigentes = [j for j in self.en_curso.values() if j["ver"] == self.tema_ver]
        if len(self.cola) + len(vigentes) >= BUFER + 1:
            return False
        # un segundo guionista solo arranca si hay un subtema para él (si no, escribirían lo mismo)
        return not vigentes or bool(self.enfoques and self.enfoques_ver == self.tema_ver)

    def _trabajo(self, job, puente, hist, paralelo, n_frases):
        seg = None
        try:
            seg = self._producir(job["tema"], puente, hist, job["ver"], enfoque=job["enfoque"], paralelo=paralelo, n_frases=n_frases,
                                 sid=f"b{job['seq']:03d}")
        except Exception as e:                       # nunca se cae el directo: se reintenta
            self._apunta(f"error al producir: {e!r}")
            time.sleep(2)
        with self.cv:
            self.en_curso.pop(job["seq"], None)
            if seg and job["ver"] == self.tema_ver and self.enfoques_ver == job["ver"]:
                for p in seg.get("proximos", []):
                    if len(self.enfoques) < 4:
                        self.enfoques.append(p)
            self.listos[job["seq"]] = seg
            self._entregar()
            self.estado = f"escribiendo {len(self.en_curso)} ({self.modelo})" if self.en_curso else "listo"
            self.cv.notify_all()
        if seg:
            self.tiempos.append(time.time() - job["t0"])
            self._apunta(f"listo {seg['id']} «{seg['titulo']}» ({seg['dur']:.0f} s de voz, hecho en {time.time() - job['t0']:.0f} s"
                         + (f", enfoque «{job['enfoque']}»" if job["enfoque"] else "") + ")")

    def _entregar(self):
        """Pasa a la cola los bloques terminados en orden de despacho (con self.cv tomado)."""
        while True:
            pend = sorted(set(self.listos) | set(self.en_curso))
            if not pend or pend[0] not in self.listos:
                return
            seg = self.listos.pop(pend[0])
            if not seg:
                continue
            if seg["ver"] != self.tema_ver:
                self._apunta(f"bloque «{seg['titulo']}» descartado (cambió el tema mientras se escribía)")
                continue
            self.cola.append(seg)
            self.bloques[seg["id"]] = seg
            for k in list(self.bloques)[:-40]:
                del self.bloques[k]
            nombrado = ", ".join(dict.fromkeys((f["peg"] or {}).get("nombre", "") for f in seg["frases"] if f["peg"]))
            self.historial.append((seg["id"], f"[{seg['tema']}] {seg.get('resumen', '')} (ya enseñado: {nombrado})"))
            self.ultimo_tema = seg["tema"]
            self._guardar(seg)

    def _producir(self, tema, puente, hist, ver=None, enfoque=None, paralelo=(), n_frases=6, sid="b000", comentarios=()):
        pegs, clips = self.bib.candidatos(tema + (" " + enfoque if enfoque else ""))
        catalogo = self.bib.texto_catalogo(pegs, clips)
        t0 = time.time()
        d, crudo = director.escribir(self.cfg, tema, hist, catalogo, transicion_de=puente, modelo=self.modelo,
                                     carpeta=os.path.join(AQUI, "_sesiones", "_claude"),
                                     vigente=lambda: ver is None or ver == self.tema_ver,
                                     enfoque=enfoque, paralelo=paralelo, n_frases=n_frases, comentarios=comentarios,
                                     formato=self._formato_discusion())
        if crudo == "cancelado":
            self._apunta("escritura cortada: cambió el tema")
            return None
        if not d:
            self._apunta("el director no devolvió JSON; reintento: " + (crudo or "")[:120].replace("\n", " "))
            return None
        t_guion = time.time() - t0
        frases = d["frases"][:7]
        coms = {c["id"]: c for c in comentarios}
        with cf.ThreadPoolExecutor(6) as ex:
            extra = {} if self.motor_voz is voz or sid.startswith("r") else {"vigente": lambda: ver is None or ver == self.tema_ver}
            if self._perezosa():                     # se sintetiza al salir de la cola (siguiente): sin gastar en lo que se tira
                f_voz = None
            else:
                f_voz = ex.submit(self.motor_voz.sintetizar, [f["texto"] for f in frases], self.carpeta, sid, self.voz, self.velocidad, **extra)
            f_web = {i: ex.submit(self.bib.buscar_web, f.get("buscar") or f.get("etiqueta"))     # respaldo: la etiqueta
                     for i, f in enumerate(frases) if f.get("pegatina") not in self.bib.pegatinas and (f.get("buscar") or f.get("etiqueta"))}
            audios = f_voz.result() if f_voz else [(None, max(1.5, len(f["texto"]) / 15.0)) for f in frases]
            webs = {i: fu.result() for i, fu in f_web.items()}
        salida, total = [], 0.0
        for i, f in enumerate(frases):
            wav, dur = audios[i]
            peg = None
            if f.get("pegatina") in self.bib.pegatinas:
                v, slug = f["pegatina"].split("/", 1)
                e = self.bib.pegatinas[f["pegatina"]]
                peg = {"url": f"/pv/{v}/{slug}.png", "rec": f"/pv/{v}/_rec/{slug}.png" if e["rec"] else None,
                       "nombre": f.get("etiqueta") or re.sub(r"\s*\(.*?\)", "", e["desc"]) or slug.replace("_", " ")}
            elif webs.get(i):
                peg = {"url": "/web/" + os.path.basename(webs[i]), "rec": None, "nombre": f.get("etiqueta") or f.get("buscar")}
            clip = f.get("clip") if f.get("clip") in self.bib.clips and f.get("clip") not in self.bib.usados[-12:] else self.bib.clip_para(f["texto"])
            if clip:
                self.bib.usar_clip(clip)
            if f.get("pegatina") in self.bib.pegatinas:
                self.bib.peg_usadas.append(f["pegatina"])
            clave = self._clave_de_nombre(f.get("voz")) if f.get("voz") else None
            if f.get("voz") and not clave:
                self._apunta(f"{sid}: voz «{f.get('voz')}» sin reconocer en la frase {i + 1}: va con la vigente")
            salida.append({"texto": f["texto"], "dur": dur, "vozde": f.get("voz"), "clave": clave, "audio": "/s/" + os.path.basename(wav) if wav else None,
                           "peg": peg, "clip": f"/cv/{clip}.mp4" if clip else None,
                           "rotulo": (f.get("rotulo") or None),
                           "ficha": f["ficha"] if isinstance(f.get("ficha"), dict) and f["ficha"].get("nombre") else None,
                           "com": coms.get(f.get("comentario"))})   # el comentario sale en pantalla mientras la voz lo contesta
            if f.get("comentario") in coms:
                self.chat.contestado(f["comentario"])
            total += dur + 0.25
        # gameplay de YouTube del tema en una de cada dos frases (la pantalla cae al clip del disco si no carga en 4 s)
        self.yt.pedir(tema)
        for i, f in enumerate(salida):
            if i % 2 == 0:
                f["yt"] = self.yt.dar(tema)
        t_voz = time.time() - t0 - t_guion
        self._apunta(f"{sid}: guion {t_guion:.0f} s · voz {t_voz:.0f} s para {total:.0f} s · {sum(1 for s in salida if s['peg'])}/{len(salida)} con imagen")
        return {"id": sid, "voz_hecha": None if f_voz is None else [self.voz_clave] * len(salida), "tema": tema, "titulo": d.get("titulo") or tema, "resumen": d.get("resumen", ""),
                "opciones": [o for o in d.get("opciones", []) if isinstance(o, str)][:3], "frases": salida,
                "proximos": [o for o in d.get("proximos", []) if isinstance(o, str)][:2],
                "dur": total, "puente": bool(puente), "ver": ver, "coms": list(comentarios), "origen": (self.anuncio or {}).get("origen") if puente else None}

    def estado_json(self):
        with self.cv:
            al = self.al_aire
            return {"canal": self.cfg["nombre"], "tema": self.tema, "tema_ver": self.tema_ver, "bufer": [s["titulo"] for s in self.cola],
                    "bufer_s": round(sum(s["dur"] for s in self.cola)), "estado": self.estado, "pausado": self.pausado,
                    "votacion": self.votacion, "opciones": self.opciones, "votos": self.votos,
                    "al_aire": {"id": al["id"], "titulo": al["titulo"], "tema": al["tema"],
                                "idx": self.frase_al_aire,
                                "frase": al["frases"][self.frase_al_aire]["texto"] if al and 0 <= self.frase_al_aire < len(al["frases"]) else ""} if al else None,
                    "com_mostrar": self.chat.mostrar, "com_fijado": self.chat.fijado, "proximo_corte": self.chat.proximo_corte,
                    "tiempo_medio": round(sum(self.tiempos) / len(self.tiempos), 1) if self.tiempos else None,
                    "modelo": self.modelo, "anuncio": self.anuncio, "voz": self.voz,
                    "voz_clave": self.voz_clave, "voces": self.voces_disponibles(), "auto_relevo": self.auto_relevo,
                    "auto_min": self.auto_min, "discusion": self.discusion, "voz_lleva_s": round(time.time() - self.voz_desde),
                    "eleven": self._eleven_estado(),
                    "yt_activo": self.yt.activo, "clip_al_aire": self.clip_al_aire,
                    "puente_inmediato": self.puente_inmediato, "lat_min": self.lat_min, "lat_max": self.lat_max,
                    "latencias": list(self.latencias), "guionistas": GUIONISTAS, "en_curso": len(self.en_curso),
                    "bufer_det": [{"titulo": s["titulo"], "dur": round(s["dur"]), "ver": s.get("ver"), "respuesta": bool(s.get("respuesta")),
                                   "inmediato": bool(s.get("inmediato"))} for s in self.cola],
                    "peg_al_aire": ((al["frases"][self.frase_al_aire].get("peg") or {}).get("url")
                                    if al and 0 <= self.frase_al_aire < len(al["frases"]) else None),
                    "voz_factor": round(self.motor_voz.factor(), 2) if getattr(self.motor_voz, "factor", None) and self.motor_voz.factor() else None, "log": list(self.log)[-14:]}


# desde la red de la casa (la tele) solo se puede VER: la pantalla, sus medios y lo que ella pide. Los controles y el chat,
# desde esta PC, desde la puerta con clave del panel remoto (reenvía desde 127.0.0.1) y desde la APP del teléfono en la wifi
# con el CÓDIGO de 4 cifras que enseña la tele al arrancar (cabecera X-Codigo; se guarda en el teléfono).
SOLO_VER_POST = {"/api/progreso"}
PUERTO_UDP = 8792      # la app del teléfono pregunta «ENVIVO?» por broadcast y la PC contesta «ENVIVO1|<puerto>|<canal>»


def codigo_movil():
    ruta = os.path.join(AQUI, "_cache", "codigo_movil.txt")
    try:
        c = open(ruta, encoding="utf-8").read().strip()
        if len(c) == 4 and c.isdigit():
            return c
    except OSError:
        pass
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    c = f"{random.SystemRandom().randrange(10000):04d}"
    open(ruta, "w", encoding="utf-8").write(c)
    return c


CODIGO = codigo_movil()


def responder_udp(puerto, nombre):
    """La app del teléfono encuentra la PC sola en la wifi (como Puente TV): sin IP fija ni túnel."""
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", PUERTO_UDP))
    while True:
        try:
            datos, de = s.recvfrom(256)
            if datos.strip() == b"ENVIVO?":
                s.sendto(f"ENVIVO1|{puerto}|{nombre}".encode("utf-8"), de)
        except OSError:
            time.sleep(1)


def crear_app(d):
    app = Flask(__name__, static_folder=None)

    @app.before_request
    def _solo_ver_desde_la_red():
        if request.remote_addr in ("127.0.0.1", "::1"):
            return None
        if request.headers.get("X-Codigo") == CODIGO:          # la app del teléfono emparejada
            return None
        if request.method == "GET" and request.path not in ("/admin", "/control", "/api/chat"):
            return None
        if request.method == "POST" and request.path in SOLO_VER_POST:
            return None
        abort(403)

    @app.get("/movil")
    def movil():                                    # el control remoto del teléfono (APK en la wifi; por la puerta: /envivo/movil)
        return send_from_directory(AQUI, "movil.html")

    @app.post("/api/tele")
    def api_tele():                                 # poner o quitar el directo en el Google TV desde el teléfono
        accion = (request.get_json(silent=True) or {}).get("accion")
        sys.path.insert(0, os.path.dirname(AQUI))
        import tele as tele_mod
        try:
            if accion == "quitar":
                try:
                    tele_mod.cerrar_web()
                except Exception:
                    pass                            # la tele corta la conexión al cerrar la ventana: no es error
                d._apunta("directo quitado de la tele")
            else:
                url = f"http://{tele_mod.ip_hacia_tele()}:{request.host.split(':')[-1]}/?auto=1&codigo={CODIGO}&v={int(time.time())}"
                tele_mod.web(url)
                d._apunta(f"directo puesto en la tele: {url.split('&')[0]}")
            return jsonify(ok=True)
        except (SystemExit, Exception) as e:
            return jsonify(ok=False, error=str(e)[:200])

    @app.after_request
    def _sin_cache(r):                              # la tele guardaba el pantalla.html viejo: las páginas nunca en caché
        if request.path in ("/", "/movil", "/admin", "/control"):
            r.headers["Cache-Control"] = "no-store"
        return r

    @app.get("/")
    def pantalla():
        return send_from_directory(AQUI, "pantalla.html")

    @app.get("/control")
    def control():
        return send_from_directory(AQUI, "control.html")

    @app.get("/admin")
    def admin():
        return send_from_directory(AQUI, "admin.html")

    @app.post("/api/comentario")
    def api_comentario():
        j = request.get_json(silent=True) or {}
        c = d.chat.recibir(j.get("autor"), j.get("texto"), "panel")
        return jsonify(ok=bool(c), id=c and c["id"])

    @app.get("/api/chat")
    def api_chat():
        return jsonify(d.chat.estado_json())

    @app.post("/api/chat/accion")
    def api_chat_accion():
        j = request.get_json(silent=True) or {}
        return jsonify(ok=d.chat.accion(j.get("id"), j.get("que")))

    @app.post("/api/chat/ajuste")
    def api_chat_ajuste():
        j = request.get_json(silent=True) or {}
        ch = d.chat
        if "cada_min" in j:
            ch.cada_min = max(0.5, min(30.0, float(j["cada_min"])))
            ch.proximo_corte = min(ch.proximo_corte, time.time() + ch.cada_min * 60)
        if "min_pedidos" in j:
            ch.min_pedidos = max(1, int(j["min_pedidos"]))
        if "propuesta" in j:
            ch.propuesta = (j["propuesta"] or "").strip()[:120] or None
        if j.get("decidir"):
            ch.decidir_ya()
        if j.get("quitar_mostrar"):
            ch.mostrar = None
        return jsonify(ok=True)

    @app.get("/api/bloque/<bid>")
    def api_bloque(bid):                            # la pantalla espejo del panel (no consume bloques)
        s = d.bloques.get(bid)
        return jsonify(s) if s else ("", 404)

    @app.get("/api/siguiente")
    def api_siguiente():
        return jsonify(d.siguiente(float(request.args.get("espera", 20))))

    @app.get("/api/estado")
    def api_estado():
        return jsonify(d.estado_json())

    @app.get("/api/ost")
    def api_ost():
        pistas = list(range(len(d.bib.ost)))
        random.shuffle(pistas)
        return jsonify([f"/ost/{i}" for i in pistas])

    @app.post("/api/tema")
    def api_tema():
        d.cambiar_tema((request.get_json(silent=True) or {}).get("tema"))
        return jsonify(ok=True)

    @app.post("/api/votar")
    def api_votar():
        d.votar((request.get_json(silent=True) or {}).get("opcion"))
        return jsonify(ok=True, votos=d.votos)

    @app.post("/api/ajuste")
    def api_ajuste():
        j = request.get_json(silent=True) or {}
        with d.cv:
            if "votacion" in j:
                d.votacion = bool(j["votacion"])
            if "pausado" in j:
                d.pausado = bool(j["pausado"])
            if j.get("modelo") in ("haiku", "sonnet", "opus"):
                d.modelo = j["modelo"]
            if "puente" in j:
                d.puente_inmediato = bool(j["puente"])
            if j.get("voz") and j["voz"] != d.voz_clave:
                threading.Thread(target=d.cambiar_voz, args=(j["voz"], "panel"), daemon=True).start()
            if "auto_relevo" in j:
                d.auto_relevo = bool(j["auto_relevo"])
            if "auto_min" in j:
                d.auto_min = max(1.0, min(60.0, float(j["auto_min"])))
            if "discusion" in j:
                d.discusion = [c for c in (j["discusion"] or []) if c in d.voces_disponibles()][:3]
                if len(d.discusion) < 2:
                    d.discusion = []
            if "yt" in j:
                d.yt.activo = bool(j["yt"])
                if d.yt.activo:
                    d.yt.pedir(d.tema)
            if "lat_min" in j:
                d.lat_min = max(0.0, min(60.0, float(j["lat_min"])))
                d.lat_max = max(d.lat_max, d.lat_min)
            if "lat_max" in j:
                d.lat_max = max(d.lat_min, min(90.0, float(j["lat_max"])))
            d.cv.notify_all()
        return jsonify(ok=True)

    @app.post("/api/progreso")
    def api_progreso():
        j = request.get_json(silent=True) or {}
        if d.al_aire and j.get("id") == d.al_aire["id"]:
            d.frase_al_aire = int(j.get("frase", 0))
            if d.frase_al_aire == 0 and "clip" not in j:
                d.al_aire_medir(d.al_aire, j.get("dt"))
        if isinstance(j.get("clip"), dict) and j["clip"].get("fuente") == "rescate":   # el vigilante de la pantalla
            d.rescates = getattr(d, "rescates", 0) + 1
            d._apunta(f"VIGILANTE: {j['clip'].get('titulo', '')[:80]} → clip del disco (van {d.rescates})")
        elif isinstance(j.get("clip"), dict):       # qué clip está al aire (YouTube o disco)
            d.clip_al_aire = {k: str(j["clip"].get(k, ""))[:120] for k in ("fuente", "titulo", "canal")}
            if d.clip_al_aire["fuente"] == "yt" and d.al_aire:
                d.yt.al_aire(d.al_aire.get("tema"))
        return jsonify(ok=True)

    def _seguro(base, rel):
        ruta = os.path.abspath(os.path.join(base, rel))         # abspath y no realpath: medios/ suele ser junction a D: o E:
        if not ruta.startswith(os.path.abspath(base) + os.sep) or not os.path.isfile(ruta):
            abort(404)
        return ruta

    @app.get("/pv/<v>/<slug>")
    @app.get("/pv/<v>/_rec/<slug>")
    def pegatina(v, slug):
        sub = "_rec" if "/_rec/" in request.path else ""
        return send_file(_seguro(VIDEOS, os.path.join(v, "pegatinas", sub, slug)), max_age=3600)

    @app.get("/fuente/bahnschrift.ttf")
    def fuente():                                   # la letra del kit de Tamriel (mg_tes.fuente): Bahnschrift Condensed
        return send_file(os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts", "bahnschrift.ttf"), max_age=86400)

    @app.get("/cv/<v>/<sc>")
    def clip(v, sc):
        return send_file(_seguro(VIDEOS, os.path.join(v, "medios", sc)), conditional=True, max_age=3600)

    @app.get("/ost/<int:i>")
    def ost(i):
        if not 0 <= i < len(d.bib.ost):
            abort(404)
        return send_file(d.bib.ost[i], conditional=True, max_age=3600)

    @app.get("/s/<nombre>")
    def audio(nombre):
        return send_file(_seguro(d.carpeta, nombre), max_age=3600)

    @app.get("/web/<nombre>")
    def web(nombre):
        return send_file(_seguro(d.bib.cache, nombre), max_age=3600)

    return app


def abrir(puerto):
    import shutil
    import subprocess
    import webbrowser
    webbrowser.open(f"http://127.0.0.1:{puerto}/")
    edge = shutil.which("msedge") or r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(edge):                     # el panel de administración, como app
        subprocess.Popen([edge, f"--app=http://127.0.0.1:{puerto}/admin", "--window-size=1500,920"])
    else:
        webbrowser.open(f"http://127.0.0.1:{puerto}/admin")


def main():
    ap = argparse.ArgumentParser(description="EN VIVO: directo generado y editado en tiempo real")
    ap.add_argument("canal", nargs="?", default="cronicas_tamriel", choices=sorted(CANALES))
    ap.add_argument("--tema", default=None)
    ap.add_argument("--modelo", default="sonnet", help="sonnet (por defecto: mejor lore y sarcasmo, 12-17 s por bloque) | haiku (respaldo)")
    ap.add_argument("--voz", default="Raul", help="voz OneCore de Windows: Raul, Sabina (es-MX), Pablo, Helena, Laura (es-ES) "
                                                  "| chatterbox:<voz de C:\\chatterbox_voices> (GPU, la del canal: chatterbox:Sarcastica)")
    ap.add_argument("--velocidad", type=int, default=1, help="-10..10")
    ap.add_argument("--puerto", type=int, default=int(os.environ.get("PORT", 8790)))
    ap.add_argument("--abrir", action="store_true", help="abre la pantalla y el panel de administración")
    ap.add_argument("--cada-min", type=float, default=3.0, help="cada cuántos minutos el chat puede cambiar el tema")
    ap.add_argument("--chat-youtube", metavar="VIDEO_ID", help="lee el chat del directo de YouTube (gasta cuota: 5 u. por lectura)")
    ap.add_argument("--tele", action="store_true", help="manda la pantalla al Google TV (Puente TV) y abre el servidor a la red de la casa "
                                                       "(desde la red solo se ve; los controles, desde la PC o el teléfono por la puerta)")
    a = ap.parse_args()
    d = Directo(a.canal, a.tema, a.modelo, a.voz, a.velocidad)
    d.chat.cada_min = a.cada_min
    d.chat.proximo_corte = time.time() + a.cada_min * 60
    if a.chat_youtube:
        chat_mod.FuenteYouTube(d.chat, a.canal, a.chat_youtube)
    print(f"EN VIVO · {d.cfg['nombre']} · tema «{d.tema}»\n  pantalla (OBS): http://127.0.0.1:{a.puerto}/?auto=1\n"
          f"  panel:          http://127.0.0.1:{a.puerto}/admin   (ventanita simple: /control)", flush=True)
    if a.abrir:
        threading.Timer(1.0, abrir, args=(a.puerto,)).start()
    import logging
    logging.getLogger("werkzeug").setLevel(logging.ERROR)     # sin una línea por cada petición
    # siempre en la red de la casa: la tele mira y la app del teléfono controla con el código (desde la red, nada más)
    host = "0.0.0.0"
    threading.Thread(target=responder_udp, args=(a.puerto, d.cfg["nombre"]), daemon=True).start()
    print(f"  app del teléfono (wifi de la casa): código {CODIGO}", flush=True)
    if a.tele:
        sys.path.insert(0, os.path.dirname(AQUI))
        import tele as tele_mod

        def a_la_tele():
            try:
                url = f"http://{tele_mod.ip_hacia_tele()}:{a.puerto}/?auto=1&codigo={CODIGO}&v={int(time.time())}"
                tele_mod.web(url)
                d._apunta(f"pantalla enviada a la tele: {url.split('&')[0]}")
            except (SystemExit, Exception) as e:
                d._apunta(f"la tele no la recibió: {e}")
        threading.Timer(2.0, a_la_tele).start()
    crear_app(d).run(host=host, port=a.puerto, threaded=True, use_reloader=False)


if __name__ == "__main__":
    main()
