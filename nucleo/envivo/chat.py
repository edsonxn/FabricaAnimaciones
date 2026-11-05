# -*- coding: utf-8 -*-
"""Chat del EN VIVO (el usuario, 4-nov-2026): la IA lee los comentarios, los clasifica, contesta los buenos en la
narración, enseña en pantalla los que valen la pena y, cada N minutos, cambia el tema a lo que más pide la gente.

- Los comentarios entran por `recibir()` (panel /admin = espectador simulado; o la fuente de YouTube, apagada por defecto).
- «1», «2», «3» con la votación activa cuentan como voto y no pasan por la IA.
- Un hilo clasifica en tandas con haiku (sin «pensar»): pedido / pregunta / agradecimiento / crítica / comentario /
  fuera (no es del juego) / spam / tóxico, más el tema pedido ya normalizado para poder contarlo.
- Cada `cada_min` minutos se cuentan los pedidos de la ventana: si uno llega a `min_pedidos`, ese es el tema nuevo
  (origen «chat», conserva 1 bloque para no dejar hueco). Si no, manda la propuesta del panel o se sigue igual.
- Reglas de CLAUDE.md § COMENTARIOS: nunca inventar ni retocar el texto; la crítica exagerada se contesta con burla
  disfrazada (del comentario, nunca de la persona); spam y tóxicos ni se enseñan ni se contestan.
"""
import json
import os
import re
import subprocess
import threading
import time
from collections import Counter, deque

from envivo import director

TIPOS = ("pedido", "pregunta", "agradecimiento", "critica", "comentario", "fuera", "spam", "toxico")

PROMPT = """Moderas el chat de un directo de YouTube del canal «{canal}» sobre {juego}. Tema actual del directo: «{tema}».
Temas que el chat ya pidió (si un comentario pide lo mismo, usa EXACTAMENTE ese texto en "tema"): {pedidos}

Clasifica cada comentario:
- "tipo": pedido (pide un tema o que hablemos de algo de {juego}) · pregunta (sobre {juego}) · agradecimiento (valora el
  directo o el canal) · critica (queja del directo, el narrador, el canal) · comentario (charla normal del juego) ·
  fuera (no tiene que ver con {juego}: otros juegos, política, ventas…) · spam (enlaces, autopromoción, repetir) ·
  toxico (insultos, odio, acoso).
- "tema": solo si es pedido: el tema como título corto en español (máx. 7 palabras, p. ej. «Los dragones de Skyrim»).
  Si pide algo que NO es de {juego}, entonces es "fuera" y sin tema.
- "mostrar": true si vale la pena enseñarlo en pantalla (aporta, es gracioso, agradece, pregunta algo bueno del juego);
  nunca fuera, spam ni tóxico.
- "contestar": true si el narrador debería contestarlo de viva voz: preguntas buenas del juego, agradecimientos, y la
  crítica EXAGERADA o sin razón (se contesta con burla disfrazada). Una crítica justa también se contesta, con humildad.
  Un pedido de tema NO se contesta (false): el chat lo decide en el corte y ahí se nombra a quien lo pidió.
- "nota": por qué, máx. 8 palabras.

Comentarios:
{lista}

Responde SOLO JSON: {{"c": [{{"id": "...", "tipo": "...", "tema": null, "mostrar": false, "contestar": false, "nota": "..."}}]}}"""


class Chat:
    def __init__(self, directo, cada_min=3.0, min_pedidos=2, modelo="haiku"):
        self.d, self.cfg = directo, directo.cfg
        self.cada_min, self.min_pedidos, self.modelo = cada_min, min_pedidos, modelo
        self.comentarios, self.n = [], 0
        self.por_id = {}
        self.proximo_corte = time.time() + cada_min * 60
        self.desde = time.time()                 # inicio de la ventana que se cuenta
        self.propuesta = None                    # tema propuesto desde el panel para el próximo corte
        self.mostrar = None                      # tarjeta grande al aire: {id, autor, texto, t, dur}
        self.fijado = None
        self.ultimo_auto = 0
        self.clasificando = False
        self.decisiones = deque(maxlen=20)
        threading.Thread(target=self._bucle, daemon=True).start()

    # --- entrada ----------------------------------------------------------------------------------
    def recibir(self, autor, texto, fuente="panel"):
        autor, texto = (autor or "Espectador").strip()[:40], (texto or "").strip()[:300]
        if not texto:
            return None
        with self.d.cv:
            self.n += 1
            c = {"id": f"c{self.n:04d}", "autor": autor, "texto": texto, "t": time.time(), "fuente": fuente,
                 "tipo": None, "tema": None, "mostrar": False, "contestar": False, "nota": "", "estado": "nuevo"}
            if re.fullmatch(r"\s*[123]\s*", texto) and self.d.votacion and self.d.opciones:
                i = int(texto) - 1
                if i < len(self.d.opciones):
                    self.d.votos[self.d.opciones[i]] = self.d.votos.get(self.d.opciones[i], 0) + 1
                c.update(tipo="voto", nota=f"voto por «{self.d.opciones[i]}»" if i < len(self.d.opciones) else "voto")
            self.comentarios.append(c)
            self.por_id[c["id"]] = c
            del self.comentarios[:-500]
        try:                                         # llegó alguien: si el directo estaba callado, despierta y lo saluda
            self.d.actividad(autor, fuente)
        except Exception as e:
            self.d._apunta(f"chat: error al avisar actividad {e!r}")
        return c

    # --- acciones del panel -----------------------------------------------------------------------
    def accion(self, cid, que):
        c = self.por_id.get(cid)
        if not c:
            return False
        with self.d.cv:
            if que == "mostrar":
                self.mostrar = self._tarjeta(c, 9)
                c["estado"] = "mostrado"
            elif que == "fijar":
                self.fijado = None if self.fijado and self.fijado["id"] == cid else self._tarjeta(c, 0)
            elif que == "ocultar":
                c["estado"] = "oculto"
                c["mostrar"] = c["contestar"] = False
                if self.mostrar and self.mostrar["id"] == cid:
                    self.mostrar = None
                if self.fijado and self.fijado["id"] == cid:
                    self.fijado = None
            elif que == "contestar":
                c["contestar"], c["estado"] = True, "nuevo"
                c["prioridad"] = True
        return True

    def _tarjeta(self, c, dur):
        return {"id": c["id"], "autor": c["autor"], "texto": c["texto"], "tipo": c["tipo"], "t": time.time(), "dur": dur}

    def para_contestar(self, n=2):
        """Saca (y marca) hasta n comentarios para que el director los conteste en el bloque que va a escribir."""
        with self.d.cv:
            cand = [c for c in self.comentarios if c["contestar"] and c["estado"] in ("nuevo", "mostrado")
                    and time.time() - c["t"] < 600]
            cand.sort(key=lambda c: (not c.get("prioridad"), -c["t"]))
            elegidos = cand[:n]
            for c in elegidos:
                c["estado"] = "en guion"
        return [{"id": c["id"], "autor": c["autor"], "texto": c["texto"], "tipo": c["tipo"]} for c in elegidos]

    def devolver(self, coms):
        """El bloque se tiró (cambio de tema): esos comentarios vuelven a la fila."""
        with self.d.cv:
            for x in coms:
                if x["id"] in self.por_id and self.por_id[x["id"]]["estado"] == "en guion":
                    self.por_id[x["id"]]["estado"] = "nuevo"

    def contestado(self, cid):
        if cid in self.por_id:
            self.por_id[cid]["estado"] = "contestado"

    def decidir_ya(self):
        self.proximo_corte = time.time()

    # --- hilo: clasificar, enseñar y decidir el tema ---------------------------------------------
    def _bucle(self):
        while True:
            time.sleep(2)
            try:
                pend = [c for c in self.comentarios if c["tipo"] is None]
                if pend and not self.clasificando:
                    self.clasificando = True
                    threading.Thread(target=self._clasificar, args=(pend[:25],), daemon=True).start()
                self._auto_mostrar()
                if time.time() >= self.proximo_corte:
                    self._decidir()
            except Exception as e:                  # el chat nunca tumba el directo
                self.d._apunta(f"chat: error {e!r}")

    def _clasificar(self, lote):
        try:
            pedidos = sorted({c["tema"] for c in self.comentarios if c.get("tema")})
            lista = "\n".join(f'{c["id"]} · @{c["autor"]}: «{c["texto"]}»' for c in lote)
            prompt = PROMPT.format(canal=self.cfg["nombre"], juego=self.cfg["juego"], tema=self.d.tema,
                                   pedidos=("; ".join(f"«{p}»" for p in pedidos) or "ninguno"), lista=lista)
            t0 = time.time()
            txt = _llamar(prompt, self.modelo)
            m = re.search(r"\{.*\}", txt or "", re.S)
            res = json.loads(m.group(0)).get("c", []) if m else []
            vistos = set()
            with self.d.cv:
                for r in res:
                    c = self.por_id.get(r.get("id"))
                    if not c or c["tipo"] is not None:
                        continue
                    tipo = r.get("tipo") if r.get("tipo") in TIPOS else "comentario"
                    malo = tipo in ("fuera", "spam", "toxico")
                    c.update(tipo=tipo, tema=(r.get("tema") or None) if tipo == "pedido" else None,
                             mostrar=bool(r.get("mostrar")) and not malo, contestar=bool(r.get("contestar")) and not malo,
                             nota=(r.get("nota") or "")[:80])
                    vistos.add(c["id"])
                for c in lote:                   # lo que la IA no devolvió no se queda colgado
                    if c["id"] not in vistos and c["tipo"] is None:
                        c.update(tipo="comentario", nota="sin clasificar")
            self.d._apunta(f"chat: {len(lote)} comentarios clasificados en {time.time() - t0:.0f} s")
        finally:
            self.clasificando = False

    def _auto_mostrar(self):
        """La IA enseña sola los comentarios buenos: uno a la vez, como mucho cada 20 s."""
        ahora = time.time()
        if self.mostrar and ahora - self.mostrar["t"] < self.mostrar["dur"] + 1:
            return
        if ahora - self.ultimo_auto < 20:
            return
        for c in self.comentarios:
            if c["mostrar"] and c["estado"] == "nuevo" and not c["contestar"] and ahora - c["t"] < 180:
                with self.d.cv:
                    self.mostrar = self._tarjeta(c, 8)
                    c["estado"] = "mostrado"
                self.ultimo_auto = ahora
                return

    def ranking(self):
        cuenta = Counter(c["tema"] for c in self.comentarios if c.get("tema") and c["t"] >= self.desde and c["estado"] != "oculto")
        return cuenta.most_common(5)

    def _decidir(self):
        rk = self.ranking()
        tema, origen, motivo = None, None, ""
        if rk and rk[0][1] >= self.min_pedidos and rk[0][0] != self.d.tema:
            tema, origen, motivo = rk[0][0], "chat", f"{rk[0][1]} pedidos"
        elif self.propuesta and self.propuesta != self.d.tema:
            tema, origen, motivo = self.propuesta, "panel", "propuesta del panel (el chat no pidió nada claro)"
        if tema:
            if origen == "chat":                 # el puente del tema nuevo nombra a quienes lo pidieron
                self.d.pedido_por = list(dict.fromkeys(c["autor"] for c in self.comentarios
                                                       if c.get("tema") == tema and c["t"] >= self.desde))[:4]
            self.d.cambiar_tema(tema, origen=origen, conservar=1)
            self.propuesta = None
        self.decisiones.append({"t": time.time(), "tema": tema, "motivo": motivo or "sin demanda clara: sigue el tema",
                                "ranking": rk})
        self.d._apunta(f"chat: corte de {self.cada_min:g} min → " + (f"«{tema}» ({motivo})" if tema else "sigue el tema")
                       + (f" · ranking {rk}" if rk else ""))
        self.desde = time.time()
        self.proximo_corte = time.time() + self.cada_min * 60

    def estado_json(self):
        return {"comentarios": [{k: c.get(k) for k in ("id", "autor", "texto", "t", "fuente", "tipo", "tema", "mostrar", "contestar",
                                                       "nota", "estado")} for c in self.comentarios[-120:]],
                "mostrar": self.mostrar, "fijado": self.fijado, "proximo_corte": self.proximo_corte,
                "cada_min": self.cada_min, "min_pedidos": self.min_pedidos, "ranking": self.ranking(),
                "propuesta": self.propuesta, "clasificando": self.clasificando,
                "decisiones": list(self.decisiones)[-5:]}


def _llamar(prompt, modelo):
    carpeta = os.path.join(director.AQUI, "_sesiones", "_claude")
    os.makedirs(carpeta, exist_ok=True)
    mcp = os.path.join(carpeta, "mcp_vacio.json")
    if not os.path.exists(mcp):
        with open(mcp, "w") as f:
            f.write('{"mcpServers":{}}')
    cmd = [director._claude(), "-p", "--model", modelo, "--strict-mcp-config", "--mcp-config", mcp,
           "--setting-sources", "", "--tools", "", "--effort", "low"]
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8", cwd=carpeta, timeout=90,
                       env=dict(os.environ, MAX_THINKING_TOKENS="0"), creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    return r.stdout


class FuenteYouTube:
    """Lee el chat de un directo de YouTube y lo mete en el Chat. APAGADA por defecto (`--chat-youtube <id del video>`).

    Cuota: cada `liveChatMessages.list` cuesta 5 unidades y el proyecto tiene 10 000 al día. Se respeta
    `pollingIntervalMillis`, con un mínimo de `MIN_S` s: a 15 s son ~1 200 unidades por hora (≈ 8 h de directo al día
    sin contar las subidas). Se para sola al llegar a `TOPE` unidades.
    """
    MIN_S, TOPE = 15, 6000

    ESPECTADORES_S = 60                              # videos.list = 1 unidad: 60 por hora

    def __init__(self, chat, canal, video_id):
        import youtube as yt
        self.yt, self.chat, self.vid = yt, chat, video_id
        self.cid = yt.resolver_canal(canal)
        self.gastado, self.activa = 0, True
        threading.Thread(target=self._bucle, daemon=True).start()
        threading.Thread(target=self._espectadores, daemon=True).start()

    def _espectadores(self):
        """Espectadores concurrentes del directo (modo sin público, 5-nov): `liveStreamingDetails.concurrentViewers`."""
        while self.activa and self.gastado < self.TOPE:
            try:
                r = self.yt.api(self.cid, "GET", "/videos", params={"part": "liveStreamingDetails", "id": self.vid})
                self.gastado += 1
                det = (r.get("items") or [{}])[0].get("liveStreamingDetails") or {}
                if "concurrentViewers" in det:
                    n = int(det["concurrentViewers"])
                    if n != self.chat.d.espectadores_yt:
                        self.chat.d._apunta(f"YouTube: {n} espectador(es) ahora")
                    self.chat.d.espectadores_yt = n
                elif det.get("actualEndTime"):
                    self.chat.d.espectadores_yt = 0
            except Exception as e:
                self.chat.d._apunta(f"YouTube espectadores: error {e!r}")
            time.sleep(self.ESPECTADORES_S)

    def _bucle(self):
        r = self.yt.api(self.cid, "GET", "/videos", params={"part": "liveStreamingDetails", "id": self.vid})
        self.gastado += 1
        live = ((r.get("items") or [{}])[0].get("liveStreamingDetails") or {}).get("activeLiveChatId")
        if not live:
            self.chat.d._apunta("chat YouTube: ese video no tiene chat en vivo activo")
            return
        token = None
        while self.activa and self.gastado < self.TOPE:
            p = {"liveChatId": live, "part": "snippet,authorDetails", "maxResults": 200}
            if token:
                p["pageToken"] = token
            r = self.yt.api(self.cid, "GET", "/liveChat/messages", params=p)
            self.gastado += 5
            for m in r.get("items", []):
                s = m.get("snippet", {})
                if s.get("type") == "textMessageEvent":
                    self.chat.recibir((m.get("authorDetails") or {}).get("displayName"), s.get("displayMessage"), "youtube")
            token = r.get("nextPageToken")
            time.sleep(max(self.MIN_S, r.get("pollingIntervalMillis", 15000) / 1000))
        self.chat.d._apunta(f"chat YouTube: parado ({self.gastado} unidades gastadas)")
