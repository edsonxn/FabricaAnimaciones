# -*- coding: utf-8 -*-
"""Capa de EFECTOS del motor SECUENCIA («secuencia con efectos»): sobre las imágenes y clips de Flow pone cámara dirigida,
golpes de cámara, destellos, viñetas, rótulos de énfasis y una pista de SFX y ambientes de ElevenLabs, todo ANCLADO A LAS
PALABRAS de la narración. Nació del video «Un segundo» (docs/ejemplos/un_segundo/); receta en docs/estilo_secuencia_fx.md.

Todo se declara en videos/<v>/efectos.py (si no existe, el motor arma como siempre):
  CAMARA  = {"scene-003": dict(a=(1.05, 0, 0), b=(1.33, 0, .3))}     (zoom, cx, cy) inicial y final; cx, cy en -1..1
  FUNDIDO = {"scene-006": 0}                                         fundido de entrada de ese beat (0 = corte seco)
  FX      = [dict(tipo="temblor", en="un empujón", amp=34), ...]     ver TIPOS abajo
  ROTULOS = [dict(texto="UN SEGUNDO", en="Un segundo", tam=150, color="crema", y=.16), ...]
  SFX     = {"boom": ("Deep cinematic sub boom hit with a long reverb tail", 4), ...}   prompt en inglés + segundos
  PISTAS  = [dict(sfx="boom", en="Primer final", vol=.55),           un disparo
             dict(sfx="latido", de="En un segundo", a="suelta el golpe|fin", vol=.85)]   bucle entre dos anclas
  PALETA  = {"amarillo": (255, 210, 63)}                             colores con nombre (RGB) para rótulos y efectos

ANCLAS (en / de / a):  12.5 = segundo · "scene-004" = inicio del beat · "scene-004:fin" = su final ·
  "el golpe fue suyo" = cuando EMPIEZA esa frase en la voz · "...|fin" = cuando termina · "...#2" = segunda vez que se dice ·
  ("un empujón", -0.15) = ancla con desfase en segundos.   `beat="scene-004"` = todo ese beat.

TIPOS de FX:  temblor(en, amp, dur) · destello(en, dur, fuerza, color) · zoom(en|de, a, cuanto, entra, sale, cx, cy) ·
  latido(de, a, bpm, zoom, color, fuerza) · vineta(de, a, color, fuerza) · desaturar(de, a, k) · tinte(de, a, color, k) ·
  oscurecer(de, a, k) · sirena(de, a, fuerza) · rec(de, a) · tv(de, a) · abre(en, dur) · cierra(en, dur) ·
  fondo(de, a, centro, borde) · imagen(de, a, ruta, x, y, ancho) ·
  repaso(beat|de+a, partes=["scene-010", ("scene-003", (1.7, .1, .7)), ...], destello) · cortina(beat, desde="scene-009", dur)
  Los de rango aceptan entra= y sale= (segundos de fundido del efecto).

  python fab.py <v> fx            genera los SFX que falten (ElevenLabs, cuesta créditos) y arma audio/fx.wav (lo suma `mezcla`)
  python fab.py <v> fx --seco     no genera nada: lista cada efecto con su segundo y qué SFX faltan
  python fab.py <v> fx hoja       previews/fx_NN.jpg: un cuadro por efecto y rótulo, para revisarlos con la vista
"""
import json
import math
import os
import re
import sys

try:                    # mismo lienzo que el armado: FORMATO = "vertical" en guion.py -> 1080x1920
    import guion as _g
    W, H = (1080, 1920) if getattr(_g, "FORMATO", "horizontal") == "vertical" else (1920, 1080)
except Exception:
    W, H = 1920, 1080
PALETA = dict(amarillo=(255, 210, 63), crema=(255, 244, 224), rosa=(255, 77, 109), tinta=(20, 12, 51), blanco=(255, 255, 255),
              negro=(0, 0, 0), rojo=(255, 20, 60), azul=(40, 90, 255), noche=(20, 10, 30), vino=(74, 42, 156))
_DIR_FUENTES = [os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts"), "C:/Windows/Fonts"]
FUENTES = dict(black=("Poppins-Black.ttf", "seguibl.ttf"), xbold=("Poppins-ExtraBold.ttf", "segoeuib.ttf"),
               semi=("Poppins-SemiBold.ttf", "seguisb.ttf"))
INSTANTE = dict(temblor=0.45, destello=0.2, abre=0.8)          # efectos de un instante: duración por defecto
ORDEN = ("fondo", "zoom", "latido", "temblor", "desaturar", "tinte", "tv", "vineta", "sirena", "oscurecer", "rec", "imagen",
         "destello")                                            # los rótulos van después; abre/cierra, al final

clamp = lambda u: max(0.0, min(1.0, u))
ease = lambda u: u * u * (3 - 2 * u)
_norm = lambda w: re.sub(r"[\W_]+", "", w.lower())


def pop(dt, dur=0.35):
    """Escala con rebote (entra pasándose un poco y se asienta)."""
    if dt <= 0:
        return 0.0
    u = dt / dur
    return 1.0 if u >= 1.6 else 1 - math.exp(-6 * u) * math.cos(9 * u)


def cargar():
    """La capa de efectos del video (carpeta actual), o None si no tiene efectos.py."""
    if not os.path.exists("efectos.py"):
        return None
    import importlib
    return Capa(importlib.import_module("efectos"))


class Capa:
    def __init__(self, mod):
        import secuencia as S
        self.S, self.mod = S, mod
        self.bs = S.cargar_beats()
        self.por_id = {b["id"]: b for b in self.bs}
        tl = json.load(open("timeline.json", encoding="utf-8"))
        self.total = self.bs[-1]["t1"]
        self.pal = [(_norm(w["w"]), w["s"], w["e"]) for e in tl["escenas"] for fr in e["frases"] for w in fr["words"]]
        self.pal = [p for p in self.pal if p[0]]
        self.paleta = dict(PALETA)
        self.paleta.update(getattr(mod, "PALETA", {}))
        self.camaras = dict(getattr(mod, "CAMARA", {}))
        self.fundidos = dict(getattr(mod, "FUNDIDO", {}))
        for i in list(self.camaras) + list(self.fundidos):
            self._beat(i)
        self.fx = [self._rango(dict(d), "FX") for d in getattr(mod, "FX", [])]
        self.rot = [self._rango(dict(d), "ROTULOS") for d in getattr(mod, "ROTULOS", [])]
        self.pistas = [self._rango(dict(d), "PISTAS") for d in getattr(mod, "PISTAS", [])]
        self.sfx = dict(getattr(mod, "SFX", {}))
        for d in self.fx:
            if d["tipo"] not in ORDEN + ("abre", "cierra", "repaso", "cortina"):
                raise SystemExit(f"efectos.py: tipo de FX desconocido «{d['tipo']}»")
        self.fx.sort(key=lambda d: ORDEN.index(d["tipo"]) if d["tipo"] in ORDEN else 99)
        self._rot_cache, self._img_cache, self._mallas = {}, {}, None

    # ------------------------------------------------------------ anclas
    def _beat(self, i):
        if i not in self.por_id:
            raise SystemExit(f"efectos.py: no existe el beat «{i}» (hay {self.bs[0]['id']}…{self.bs[-1]['id']})")
        return self.por_id[i]

    def ancla(self, x):
        if isinstance(x, (int, float)):
            return float(x)
        if isinstance(x, (tuple, list)):
            return self.ancla(x[0]) + float(x[1])
        m = re.fullmatch(r"(scene-\d{3,})(:fin)?", x)
        if m:
            return self._beat(m.group(1))["t1" if m.group(2) else "t0"]
        m = re.fullmatch(r"(.*?)(?:#(\d+))?(\|fin)?", x, re.S)
        aguja = [_norm(w) for w in m.group(1).split()]
        aguja = [w for w in aguja if w]
        vez, visto = int(m.group(2) or 1), 0
        for i in range(len(self.pal) - len(aguja) + 1):
            if all(self.pal[i + j][0] == aguja[j] for j in range(len(aguja))):
                visto += 1
                if visto == vez:
                    return self.pal[i + len(aguja) - 1][2] if m.group(3) else self.pal[i][1]
        raise SystemExit(f"efectos.py: la voz no dice «{m.group(1)}»" + (f" {vez} veces" if vez > 1 else "")
                         + " (el ancla debe copiar palabras seguidas del guion, tal como las transcribió `tiempo`)")

    def beat_en(self, t):
        return next((b for b in self.bs if b["t0"] <= t < b["t1"]), self.bs[-1])

    def _rango(self, d, lista):
        """Resuelve en/de/a/beat a segundos: deja d['de'] y d['a']."""
        b = self._beat(d["beat"]) if "beat" in d else None
        de = self.ancla(d["en"]) if "en" in d else self.ancla(d["de"]) if "de" in d else (b["t0"] if b else None)
        if de is None:
            raise SystemExit(f"efectos.py ({lista}): falta en=, de= o beat= en {d}")
        tipo = d.get("tipo", "")
        if "a" in d:
            a = self.ancla(d["a"])
        elif tipo == "cierra":                         # se queda en negro hasta el final
            a = self.total + 1
        elif "dur" in d and tipo not in ("cortina",) and lista != "PISTAS":
            a = de + float(d["dur"])
        elif tipo in INSTANTE:
            a = de + INSTANTE[tipo]
        elif tipo == "cierra" or (lista == "PISTAS" and "de" not in d):
            a = self.total
        else:
            a = b["t1"] if b else self.beat_en(de + 1e-3)["t1"]
        d["de"], d["a"] = de, max(a, de + 0.03)
        return d

    def color(self, c):
        """Nombre de la paleta o (R, G, B) -> BGR."""
        r, g, b = self.paleta[c] if isinstance(c, str) else c
        return (b, g, r)

    def fundido(self, i, por_defecto):
        return float(self.fundidos.get(i, por_defecto))

    # ------------------------------------------------------------ fuentes compuestas (reemplazan la imagen del beat)
    def envolver(self, act, b):
        for d in self.fx:
            if d["tipo"] in ("repaso", "cortina") and d["de"] < b["t1"] and d["a"] > b["t0"]:
                act = (_Repaso if d["tipo"] == "repaso" else _Cortina)(act, d, self, b)
        return act

    def fija(self, i, t0, t1, cam):
        """La imagen de otro beat (o el cuadro central de su clip) como fuente con su propia cámara."""
        r = self.S.medio_de(self._beat(i))
        if r is None:
            raise SystemExit(f"efectos.py: {i} no tiene medio todavía (lo pide un repaso o una cortina)")
        return self.S.Imagen(r, dict(id=i, t0=t0, t1=t1), 0, cam)

    # ------------------------------------------------------------ cuadro
    def _malla(self):
        if self._mallas is None:
            import numpy as np
            yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
            rad = np.clip((np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)) - .45) / .75, 0, 1)[..., None]
            self._mallas = (xx, yy, rad, ((yy.astype(int) // 4) % 2)[..., None].astype(np.float32))
        return self._mallas

    @staticmethod
    def _env(d, t):
        e, s = d.get("entra", 0), d.get("sale", 0)
        k = ease(clamp((t - d["de"]) / e)) if e > 0 else 1.0
        return k * (ease(clamp((d["a"] - t) / s)) if s > 0 else 1.0)

    def aplicar(self, f, t):
        import cv2
        import numpy as np
        act = [d for d in self.fx if d["de"] <= t < d["a"]]
        if not act and not any(d["de"] <= t < d["a"] for d in self.rot):
            return f
        xx, yy, RAD, TV = self._malla()
        vin = lambda f, col, k: (f * (1 - RAD * k) + np.float32(col) * RAD * k).astype(np.uint8)
        esc, sx, sy, cx, cy = 1.0, 0.0, 0.0, 0.0, 0.0
        for d in act:                                  # lo geométrico se junta en una sola transformación
            dt = t - d["de"]
            if d["tipo"] == "zoom":
                d.setdefault("entra", 0.25)
                esc += d.get("cuanto", 0.25) * self._env(d, t)
                cx, cy = d.get("cx", cx), d.get("cy", cy)
            elif d["tipo"] == "latido":
                d["_p"] = max(0.0, math.sin(t * 2 * math.pi * d.get("bpm", 138) / 60)) ** 6 * self._env(d, t)
                esc += d.get("zoom", 0.035) * d["_p"]
            elif d["tipo"] == "temblor":
                k = d.get("amp", 30) * (1 - dt / (d["a"] - d["de"]))
                sx, sy = sx + k * math.sin(dt * 95), sy + k * math.cos(dt * 71)
        if esc != 1.0 or sx or sy:
            ox, oy = W / 2 + cx * W * 0.5 * (1 - 1 / esc), H / 2 + cy * H * 0.5 * (1 - 1 / esc)
            M = np.float32([[esc, 0, W / 2 - esc * ox + sx], [0, esc, H / 2 - esc * oy + sy]])
            f = cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        for d in act:
            tipo, e, dt = d["tipo"], self._env(d, t), t - d["de"]
            if tipo == "fondo":                        # tarjeta: degradado radial que tapa la imagen
                r = np.clip(1 - np.hypot((xx - W * .5) / W, (yy - H * .2) / H) * 1.5, 0, 1)[..., None]
                g = np.float32(self.color(d.get("borde", "tinta"))) * (1 - r) + np.float32(self.color(d.get("centro", "vino"))) * r
                f = (f * (1 - e) + g * e).astype(np.uint8)
            elif tipo == "desaturar":
                k = d.get("k", 0.5) * e
                f = (f * (1 - k) + cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)[..., None] * k).astype(np.uint8)
            elif tipo == "tinte":
                k = d.get("k", 0.25) * e
                f = (f * (1 - k) + f.astype(np.float32) * np.float32(self.color(d.get("color", "crema"))) / 255 * k).astype(np.uint8)
            elif tipo == "tv":                         # cinta rebobinando: rayas, salto horizontal, banda brillante
                f = np.roll(f, int(60 * math.sin(t * 50)), axis=1)
                f = (f * (.72 + .28 * TV)).astype(np.uint8)
                y = int((t * 900) % H)
                f[y:y + 40] = np.clip(f[y:y + 40].astype(np.int16) + 70, 0, 255).astype(np.uint8)
                f = (f * .5 + cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)[..., None] * .5).astype(np.uint8)
            elif tipo == "vineta":
                f = vin(f, self.color(d.get("color", "noche")), d.get("fuerza", 0.5) * e)
            elif tipo == "latido":
                f = vin(f, self.color(d.get("color", "rojo")), d.get("fuerza", 0.35) * e + 0.4 * d["_p"])
            elif tipo == "sirena":
                s = .5 + .5 * math.sin(t * d.get("vel", 7))
                f = vin(f, (255 * (1 - s), 30, 255 * s), d.get("fuerza", 0.28) * e)
            elif tipo == "oscurecer":
                f = (f * (1 - d.get("k", 0.55) * e)).astype(np.uint8)
            elif tipo == "rec":
                f = np.ascontiguousarray(f)
                if int(t * 2) % 2 == 0:
                    cv2.circle(f, (150, 120), 26, (60, 40, 255), -1, cv2.LINE_AA)
                self._pegar(f, self._rotulo("REC", 60, "crema", "black", None), 260, 122)
            elif tipo == "imagen":
                self._pegar(f, self._imagen(d["ruta"], d.get("ancho", 1400)), d.get("x", .5) * W, d.get("y", .83) * H, 1,
                            clamp(dt / d.get("entra", 0.6)) if d.get("entra", 0.6) > 0 else 1)
            elif tipo == "destello":
                k = (1 - dt / (d["a"] - d["de"])) * d.get("fuerza", 0.8)
                f = cv2.addWeighted(f, 1 - k, np.full_like(f, self.color(d.get("color", "blanco")), np.uint8), k, 0)
        for d in self.rot:
            if not (d["de"] <= t < d["a"]) or (d.get("parpadea") and int(t * d["parpadea"] * 2) % 2):
                continue
            f = np.ascontiguousarray(f)
            r = self._rotulo(d["texto"], d.get("tam", 150), d.get("color", "crema"), d.get("fuente", "black"), d.get("caja"))
            s = d.get("sale", 0.3)
            self._pegar(f, r, d.get("x", .5) * W, d.get("y", .5) * H, pop(t - d["de"], d.get("pop", 0.4)) if d.get("pop", 0.4) else 1,
                        clamp((d["a"] - t) / s) if s > 0 else 1)
        for d in act:
            if d["tipo"] == "abre":
                f = (f * clamp((t - d["de"]) / (d["a"] - d["de"]))).astype(np.uint8)
            elif d["tipo"] == "cierra":
                f = (f * (1 - clamp((t - d["de"]) / d.get("dur", 0.6)))).astype(np.uint8)
        return np.ascontiguousarray(f)

    # ------------------------------------------------------------ rótulos e imágenes pegadas
    def _rotulo(self, texto, tam, color, fuente, caja):
        key = (texto, tam, str(color), fuente, str(caja))
        if key not in self._rot_cache:
            import numpy as np
            from PIL import Image, ImageDraw, ImageFont
            ruta = next((os.path.join(c, n) for n in FUENTES.get(fuente, (fuente,)) for c in _DIR_FUENTES
                         if os.path.exists(os.path.join(c, n))), "C:/Windows/Fonts/segoeuib.ttf")
            fnt = ImageFont.truetype(ruta, tam)
            x0, y0, x1, y1 = fnt.getbbox(texto)
            w, h = x1 - x0, y1 - y0
            px, py = (int(tam * .7), int(tam * .35)) if caja else (16, 16)
            im = Image.new("RGBA", (w + 2 * px + 24, h + 2 * py + 24), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            rgb = lambda c: tuple(self.color(c)[::-1])
            if caja:                                   # cápsula de color con el texto dentro
                d.rounded_rectangle((0, 0, w + 2 * px, h + 2 * py), radius=(h + 2 * py) // 2, fill=rgb(caja) + (255,))
            else:                                      # texto suelto: sombra dura para leerse sobre cualquier imagen
                d.text((px - x0 + max(3, tam // 25), py - y0 + max(4, tam // 19)), texto, font=fnt, fill=(8, 4, 24, 190))
            d.text((px - x0, py - y0), texto, font=fnt, fill=rgb(color) + (255,))
            self._rot_cache[key] = np.array(im)[..., [2, 1, 0, 3]].copy()
        return self._rot_cache[key]

    def _imagen(self, ruta, ancho):
        if (ruta, ancho) not in self._img_cache:
            import cv2
            import numpy as np
            im = cv2.imdecode(np.fromfile(ruta, np.uint8), cv2.IMREAD_UNCHANGED)
            if im is None:
                raise SystemExit(f"efectos.py: no pude leer la imagen {ruta}")
            if im.shape[2] == 3:
                im = np.dstack([im, np.full(im.shape[:2], 255, np.uint8)])
            self._img_cache[(ruta, ancho)] = cv2.resize(im, (ancho, round(ancho * im.shape[0] / im.shape[1])), interpolation=cv2.INTER_AREA)
        return self._img_cache[(ruta, ancho)]

    @staticmethod
    def _pegar(f, r, cx, cy, escala=1.0, alfa=1.0):
        import cv2
        import numpy as np
        if alfa <= 0 or escala <= 0.02:
            return
        if abs(escala - 1) > .005:
            r = cv2.resize(r, None, fx=escala, fy=escala, interpolation=cv2.INTER_LINEAR)
        h, w = r.shape[:2]
        x, y = int(cx - w / 2), int(cy - h / 2)
        x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
        if x1 <= x0 or y1 <= y0:
            return
        rr = r[y0 - y:y1 - y, x0 - x:x1 - x]
        a = rr[..., 3:4].astype(np.float32) / 255 * alfa
        f[y0:y1, x0:x1] = (f[y0:y1, x0:x1] * (1 - a) + rr[..., :3] * a).astype(np.uint8)

    # ------------------------------------------------------------ listado
    def lista(self):
        f = lambda d: f"{d['de']:7.2f}-{d['a']:7.2f}  {self.beat_en(d['de'] + 1e-3)['id']}"
        ev = [(d["de"], f"{f(d)}  FX      {d['tipo']}") for d in self.fx]
        ev += [(d["de"], f"{f(d)}  RÓTULO  «{d['texto']}»") for d in self.rot]
        ev += [(d["de"], f"{f(d)}  SONIDO  {d['sfx']}{' (bucle)' if d.get('bucle', 'en' not in d) else ''}  vol {d.get('vol', 1.0)}")
               for d in self.pistas]
        for _, linea in sorted(ev):
            print(linea)
        print(f"{len(self.fx)} efectos · {len(self.rot)} rótulos · {len(self.pistas)} sonidos · {len(self.camaras)} cámaras dirigidas")


class _Repaso:
    """Durante [de, a] el beat muestra una ráfaga de imágenes de OTROS beats (recuento, rebobinado), con destello en cada corte."""

    def __init__(self, base, d, capa, b):
        self.base, self.de, self.a, self.fl = base, max(d["de"], b["t0"]), min(d["a"], b["t1"]), d.get("destello", 0.5)
        partes = [(p, None) if isinstance(p, str) else p for p in d["partes"]]
        self.dp = (self.a - self.de) / len(partes)
        self.im = []
        for k, (i, cam) in enumerate(partes):
            z, cx, cy = cam or (1.12, 0, 0)
            self.im.append(capa.fija(i, self.de + k * self.dp, self.de + (k + 1) * self.dp, dict(a=(z, cx, cy), b=(z + .08, cx, cy))))

    def cuadro(self, t):
        if not (self.de <= t < self.a):
            return self.base.cuadro(t)
        import cv2
        import numpy as np
        k = min(int((t - self.de) / self.dp), len(self.im) - 1)
        f = self.im[k].cuadro(t)
        fl = clamp(1 - ((t - self.de) / self.dp - k) * self.dp / .12) * self.fl
        return cv2.addWeighted(f, 1 - fl, np.full_like(f, 255), fl, 0) if fl > 0 else f


class _Cortina:
    """El beat arranca con la imagen de otro beat y una cortina diagonal la barre hasta dejar la propia (antes | después)."""

    def __init__(self, base, d, capa, b):
        self.base, self.d, self.t0 = base, d, b["t0"]
        self.otra = capa.fija(d["desde"], b["t0"], b["t1"], d.get("cam") or dict(a=(1.2, 0, 0), b=(1.3, 0, 0)))
        self.xx, self.yy = capa._malla()[:2]
        self.borde = capa.color(d.get("color", "crema"))

    def cuadro(self, t):
        import cv2
        import numpy as np
        d = self.d
        a, b = self.otra.cuadro(t), self.base.cuadro(t)
        k = d.get("desaturar", 0.5)
        if k:
            a = (a * (1 - k) + cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)[..., None] * k).astype(np.uint8)
        corte = W * (1.25 - (1.25 - d.get("hasta", 0.5)) * ease(clamp((t - self.t0) / d.get("dur", 0.7))))
        linea = self.xx - (corte - (self.yy - H / 2) * d.get("inclinacion", 0.22))
        m = np.clip(linea / 3 + .5, 0, 1)[..., None]
        f = (a * (1 - m) + b * m).astype(np.uint8)
        return np.where((np.abs(linea) < d.get("borde", 7))[..., None], np.uint8(self.borde), f).astype(np.uint8)


# ---------------------------------------------------------------- sonido
def _generar(capa, seco):
    """Pide a ElevenLabs los SFX que falten en sfx/<nombre>.mp3. Devuelve los que siguen faltando."""
    usados = {d["sfx"] for d in capa.pistas}
    sin_def = [n for n in usados if n not in capa.sfx and not os.path.exists(f"sfx/{n}.mp3")]
    if sin_def:
        raise SystemExit(f"efectos.py: PISTAS usa sonidos sin definir en SFX ni en sfx/: {sin_def}")
    faltan = [n for n in capa.sfx if not os.path.exists(f"sfx/{n}.mp3")]
    if seco or not faltan:
        return faltan
    import time
    import requests
    import tts_eleven as E
    os.makedirs("sfx", exist_ok=True)
    gasto = 0
    for n in faltan:
        txt, dur = capa.sfx[n]
        for intento in range(4):
            r = requests.post(f"{E.URL}/sound-generation", headers={"xi-api-key": E.clave()}, timeout=180,
                              json=dict(text=txt, duration_seconds=min(float(dur), 22), prompt_influence=0.45))
            if r.status_code == 200:
                open(f"sfx/{n}.mp3", "wb").write(r.content)
                gasto += int(r.headers.get("character-cost") or 0)
                print(f"  sfx/{n}.mp3  {dur} s", flush=True)
                break
            if r.status_code not in (429, 500, 502, 503):
                raise SystemExit(f"ElevenLabs {r.status_code} en «{n}»: {r.text[:300]}")
            time.sleep(5 * (intento + 1))
    print(f"ElevenLabs: {len(faltan)} efectos generados, {gasto} créditos")
    return [n for n in capa.sfx if not os.path.exists(f"sfx/{n}.mp3")]


def audio(seco=False):
    import librosa
    import numpy as np
    import soundfile as sf
    from sinte import SR
    capa = cargar()
    if capa is None:
        raise SystemExit("Este video no tiene efectos.py (plantilla: videos/_plantilla_secuencia/efectos.py)")
    capa.lista()
    faltan = _generar(capa, seco)
    if seco:
        print("SFX por generar:", " ".join(faltan) if faltan else "ninguno")
        return
    N = int(capa.total * SR)
    out, cache = np.zeros((2, N), np.float32), {}
    for d in capa.pistas:
        if d["sfx"] not in cache:
            x, _ = librosa.load(f"sfx/{d['sfx']}.mp3", sr=SR, mono=False)
            cache[d["sfx"]] = np.vstack([x, x]) if x.ndim == 1 else x[:2]
        x = cache[d["sfx"]]
        n = int((d["a"] - d["de"]) * SR)
        if d.get("bucle", "en" not in d):              # ambiente o música de fondo: se repite con empalme suave
            c = min(int(0.5 * SR), x.shape[1] // 4)
            v = np.linspace(0, 1, c, dtype=np.float32)
            vuelta = np.concatenate([x[:, :c] * v + x[:, -c:] * (1 - v), x[:, c:-c]], axis=1)
            x = np.tile(vuelta, (1, n // vuelta.shape[1] + 1))[:, :n].copy()
            fi, fo = min(int(d.get("entra", 1.2) * SR), n // 2), min(int(d.get("sale", 1.8) * SR), n // 2)
        else:
            x = x[:, :n].copy()
            fi, fo = 0, min(int(d.get("sale", 0.05) * SR), x.shape[1])
        if fi:
            x[:, :fi] *= np.linspace(0, 1, fi, dtype=np.float32)
        if fo:
            x[:, -fo:] *= np.linspace(1, 0, fo, dtype=np.float32)
        i = max(0, int(d["de"] * SR))
        x = x[:, :N - i] * float(d.get("vol", 1.0))
        out[:, i:i + x.shape[1]] += x
    os.makedirs("audio", exist_ok=True)
    sf.write("audio/fx.wav", out.T, SR, subtype="PCM_16")
    print(f"audio/fx.wav: {len(capa.pistas)} sonidos en {capa.total:.1f} s (pico {np.abs(out).max():.2f}); `mezcla` lo suma a la voz")


def hoja():
    """Un cuadro por efecto y por rótulo (en su momento más visible), con su etiqueta: para revisar con la vista."""
    import cv2
    import numpy as np
    capa = cargar()
    if capa is None:
        raise SystemExit("Este video no tiene efectos.py")
    S = capa.S
    ev = [(d["de"] + min(0.12 if d["tipo"] in ("temblor", "destello") else 0.7, (d["a"] - d["de"]) * .6), d["tipo"]) for d in capa.fx]
    ev += [(d["de"] + min(0.8, (d["a"] - d["de"]) * .6), d["texto"][:22]) for d in capa.rot]
    ev += [((b["t0"] + b["t1"]) / 2, "cámara") for b in capa.bs if b["id"] in capa.camaras]
    ev.sort()
    os.makedirs("previews", exist_ok=True)
    minis = []
    for t, nombre in ev:
        k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
        b = capa.bs[k]
        f = capa.aplicar(capa.envolver(S._fuente(b, k, True, capa), b).cuadro(t), t)
        m = cv2.resize(f, (480, 270), interpolation=cv2.INTER_AREA)
        cv2.rectangle(m, (0, 244), (480, 270), (20, 18, 18), -1)
        cv2.putText(m, f"{t:.1f}s {b['id'][6:]} {nombre}".encode("ascii", "replace").decode(), (6, 263), cv2.FONT_HERSHEY_SIMPLEX, .55,
                    (90, 214, 255), 1, cv2.LINE_AA)
        minis.append(m)
    for h in range(0, len(minis), 20):
        g = minis[h:h + 20] + [np.zeros_like(minis[0])] * (-len(minis[h:h + 20]) % 4)
        ruta = f"previews/fx_{h // 20 + 1:02d}.jpg"
        cv2.imwrite(ruta, np.vstack([np.hstack(g[i:i + 4]) for i in range(0, len(g), 4)]))
        print(ruta)
    capa.lista()


if __name__ == "__main__":
    if "hoja" in sys.argv[1:]:
        hoja()
    else:
        audio(seco="--seco" in sys.argv[1:])
