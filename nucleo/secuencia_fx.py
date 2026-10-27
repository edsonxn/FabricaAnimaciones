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
  oscurecer(de, a, k) · neon(de, a, fuerza, vel, radio, sat, val) — lo saturado y brillante de la imagen (neón amarillo, ojos
    rojos) brilla con halo y palpita/parpadea como tubo de neón; estilo «línea blanca + neón» (docs/estilo_linea_neon.md) ·
  sirena(de, a, fuerza) · rec(de, a) · tv(de, a) · abre(en, dur) · cierra(en, dur) ·
  fondo(de, a, centro, borde) · imagen(de, a, ruta, x, y, ancho, alto, anim="slide"|"fade") ·
  video(de, a, ruta, desde, x, y, ancho, croma, recorte) — otro video encima (sin ancho = cuadro entero; croma=True quita la
    pantalla verde; recorte=0.03 quita esa fracción por lado, p. ej. el marco de un clip de Flow; vel=0.9 lo frena o acelera;
    con desde= y el mismo clip del beat se salta un tramo malo (un negro de transición); congela su último cuadro si sobra
    rango; su audio NO entra en la mezcla) · mg(de, a, fn, marcas, x, y) — motion graphic por código:
    fn(dt, dur, marcas) -> imagen BGRA; marcas = anclas de la voz, llegan como s desde el inicio (kit nucleo/mg_wow.py) ·
  pantalla(de, a, fn) — como `mg` pero se dibuja DEBAJO de tarjetas y pegatinas: imagen real a cuadro entero con movimiento
    lento (`mg_wow.pantalla`), para cuando el clip no enseña lo que la curiosidad necesita ver ·
  repaso(beat|de+a, partes=["scene-010", ("scene-003", (1.7, .1, .7)), ...], destello) · cortina(beat, desde="scene-009", dur) ·
  vivo(beat, anim="respira"|"baile"|"flota"|"balanceo"|"parallax", capa=None|0|[0, 1], amp=1.0, par=16, escala=1.04,
    modelo, pivote="pies"|"centro") — IMAGEN VIVA (nucleo/vivo.py): el personaje (o 2-3, o un objeto) recortado con rembg se
    mueve encima de su fondo rellenado, con pivote en los pies y un 4 % más grande para tapar el hueco; el fondo lleva parallax
    2.5D por profundidad. capa = qué recortes se mueven (números de previews/vivo_NN.jpg; None = todos). Con en=/de= la
    animación entra suave en esa palabra. Antes: `python fab.py <v> vivo` (caché medios/capas/ + candidatos + hoja).
  VIVO_AUTO = 12  (variable aparte, no en FX): parallax suave de 12 px en TODAS las imágenes sin FX vivo (necesita la
    profundidad: `python fab.py <v> vivo preparar --solo-prof`; sin ella la imagen va como siempre).
  Los de rango aceptan entra= y sale= (segundos de fundido del efecto). ancho/alto <= 1 = fracción del cuadro.
APOYOS = [dict(en="...", wowhead=5060 | tarjeta={...} | web=URL | img=ruta), ...]   tooltips y tarjetas encima del gameplay
  (nucleo/apoyos.py: `python fab.py <v> apoyos` genera los PNG); aquí se vuelven FX `imagen` con entrada deslizada.
PISTAS con voz=True (p. ej. el tramo intacto del creativo de un patrocinio) van a audio/fx_voz.wav: `mezcla` las pone a
  nivel de voz y agacha la música debajo, como con la narración.

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
ORDEN = ("fondo", "zoom", "latido", "temblor", "desaturar", "tinte", "neon", "tv", "vineta", "sirena", "oscurecer", "rec", "video",
         "pantalla", "imagen", "mg", "destello")                            # los rótulos van después; abre/cierra, al final

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
        for k, ap in enumerate(getattr(mod, "APOYOS", [])):     # tooltips/tarjetas (nucleo/apoyos.py) = FX imagen deslizada
            import apoyos
            tam = ap.get("size", apoyos.TAM[apoyos.tipo(ap)])
            self.fx.append(self._rango(dict(tipo="imagen", ruta=apoyos.ruta(ap), en=ap["en"], dur=ap.get("dur", 4.5),
                                            x=ap.get("x", .5 if tam > .45 else .78), y=ap.get("y", .48), ancho=tam,
                                            alto=ap.get("alto", .84), anim=ap.get("anim", "slide"), entra=.35, sale=.3,
                                            apoyo=k + 1), "APOYOS"))
        for d in self.fx:                                       # mg: momentos en que la voz dice cada ancla (s desde su inicio)
            if d["tipo"] in ("mg", "pantalla"):
                d["_marcas"] = [self.ancla(m) - d["de"] for m in d.get("marcas", [])]
        self.rot = [self._rango(dict(d), "ROTULOS") for d in getattr(mod, "ROTULOS", [])]
        self.pistas = [self._rango(dict(d), "PISTAS") for d in getattr(mod, "PISTAS", [])]
        self.sfx = dict(getattr(mod, "SFX", {}))
        for d in self.fx:
            if d["tipo"] not in ORDEN + ("abre", "cierra", "repaso", "cortina", "vivo"):
                raise SystemExit(f"efectos.py: tipo de FX desconocido «{d['tipo']}»")
        self.fx.sort(key=lambda d: ORDEN.index(d["tipo"]) if d["tipo"] in ORDEN else 99)
        self._rot_cache, self._img_cache, self._mallas, self._vids = {}, {}, None, {}
        self.vivo_auto = float(getattr(mod, "VIVO_AUTO", 0) or 0)      # parallax suave en todas las imágenes (px)
        self._sin_prof = []

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
        if isinstance(act, self.S.Imagen):             # imágenes vivas (nucleo/vivo.py): recorte animado o parallax
            import vivo
            d = next((d for d in self.fx if d["tipo"] == "vivo" and d["de"] < b["t1"] and d["a"] > b["t0"]), None)
            if d is not None:
                act = vivo.Vivo(act, b, d)
            elif self.vivo_auto:
                v = vivo.auto(act, b, self.vivo_auto)
                if v is None and b["id"] not in self._sin_prof:
                    self._sin_prof.append(b["id"])
                    print(f"  (vivo) {b['id']} sin profundidad: va quieta. python fab.py <v> vivo preparar --solo-prof", flush=True)
                act = v or act
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
        # copia: el cuadro de un Clip es su búfer de lectura, que se reutiliza (clip de 24 fps en video de 30, cuadro congelado,
        # `prev` de la transición). Pegar encima sin copiar dejaba estelas y fantasmas de rótulos/apoyos/MG (13-oct-2026).
        f = f.copy()
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
            elif tipo == "neon":                       # halo de neón sobre lo saturado y brillante, con pulso y parpadeo
                q = 4
                pq = cv2.resize(f, (W // q, H // q), interpolation=cv2.INTER_AREA)
                hsv = cv2.cvtColor(pq, cv2.COLOR_BGR2HSV)
                m = ((hsv[..., 1] > d.get("sat", 90)) & (hsv[..., 2] > d.get("val", 110)))[..., None].astype(np.float32)
                src = pq.astype(np.float32) * m
                r = d.get("radio", 9)
                halo = cv2.GaussianBlur(src, (0, 0), r) * 1.6 + cv2.GaussianBlur(src, (0, 0), r * 3) * 1.2
                v = d.get("vel", 1.3)
                pulso = .78 + .22 * math.sin(t * 2 * math.pi * v * .5) + .08 * math.sin(t * 2 * math.pi * v * 2.7)
                if (math.sin(t * 17.3) * math.sin(t * 5.1 + 1) > .93):   # chisporroteo raro del tubo
                    pulso *= .55
                halo = cv2.resize(halo, (W, H), interpolation=cv2.INTER_LINEAR) * (d.get("fuerza", 0.9) * e * pulso)
                f = np.clip(f.astype(np.float32) + halo, 0, 255).astype(np.uint8)
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
                ent, anim = d.get("entra", 0.6), d.get("anim")
                u = clamp(dt / ent) if ent > 0 else 1.0
                if anim:                               # apoyos: entra deslizándose desde la derecha (o solo funde) y sale fundiendo
                    s = d.get("sale", 0)
                    alfa = ease(u) * (ease(clamp((d["a"] - t) / s)) if s > 0 else 1.0)
                    dx = (1 - u) ** 3 * W * .09 if anim == "slide" else 0.0
                else:
                    alfa, dx = u, 0.0
                self._pegar(f, self._imagen(d["ruta"], d.get("ancho", 1400), d.get("alto")), d.get("x", .5) * W + dx,
                            d.get("y", .83) * H, 1, alfa)
            elif tipo == "video":
                v = self._video(d).cuadro(dt)
                if d.get("zoom"):                      # acercamiento animado (27-oct-2026, análisis táctico): zoom=(z, cx, cy) final,
                    v = _zoom_video(v, d, dt)          # zoom0 inicial (por defecto 1, centro), zoom_en/zoom_dur en s del FX
                if d.get("recorte"):                   # fracción por lado (quita el marco de viñeta de un clip de Flow)
                    ry, rx = int(v.shape[0] * d["recorte"]), int(v.shape[1] * d["recorte"])
                    v = v[ry:v.shape[0] - ry, rx:v.shape[1] - rx]
                if d.get("ancho"):                     # recuadro encima (con croma: solo lo que no es verde)
                    an = d["ancho"] * W if d["ancho"] <= 1 else d["ancho"]
                    v = cv2.resize(v, (int(an), round(an * v.shape[0] / v.shape[1])), interpolation=cv2.INTER_AREA)
                else:                                  # cuadro entero
                    import secuencia as S
                    v = cv2.resize(S._cubrir(v, W, H), (W, H), interpolation=cv2.INTER_LINEAR)
                if d.get("croma"):
                    v = _croma(v)
                elif d.get("ancho"):
                    v = np.dstack([v, np.full(v.shape[:2], 255, np.uint8)])
                else:
                    f = (f * (1 - e) + v * e).astype(np.uint8) if e < 1 else v.copy()
                    continue
                f = np.ascontiguousarray(f)
                self._pegar(f, v, d.get("x", .5) * W, d.get("y", .5) * H, 1, e)
            elif tipo in ("mg", "pantalla"):           # motion graphic por código: fn(dt, dur, marcas) -> BGRA
                f = np.ascontiguousarray(f)
                self._pegar(f, d["fn"](dt, d["a"] - d["de"], d["_marcas"]), d.get("x", .5) * W, d.get("y", .5) * H, 1, e)
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

    def _imagen(self, ruta, ancho, alto=None):
        """La imagen con ese ancho (px, o fracción del cuadro si <= 1); si pasa de `alto`, se achica para caber."""
        if (ruta, ancho, alto) not in self._img_cache:
            import cv2
            import numpy as np
            if not os.path.exists(ruta):
                raise SystemExit(f"efectos.py: falta la imagen {ruta}" + (" (genera los apoyos: python fab.py <v> apoyos)"
                                                                          if ruta.startswith("apoyos") else ""))
            im = cv2.imdecode(np.fromfile(ruta, np.uint8), cv2.IMREAD_UNCHANGED)
            if im is None:
                raise SystemExit(f"efectos.py: no pude leer la imagen {ruta}")
            if im.ndim == 2:
                im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
            if im.shape[2] == 3:
                im = np.dstack([im, np.full(im.shape[:2], 255, np.uint8)])
            an = ancho * W if ancho <= 1 else ancho
            if alto:
                an = min(an, (alto * H if alto <= 1 else alto) * im.shape[1] / im.shape[0])
            an = int(round(an))
            self._img_cache[(ruta, ancho, alto)] = cv2.resize(im, (an, round(an * im.shape[0] / im.shape[1])),
                                                              interpolation=cv2.INTER_AREA if an < im.shape[1] else cv2.INTER_CUBIC)
        return self._img_cache[(ruta, ancho, alto)]

    def _video(self, d):
        if id(d) not in self._vids:
            if not os.path.exists(d["ruta"]):
                raise SystemExit(f"efectos.py: falta el video {d['ruta']}")
            self._vids[id(d)] = _VideoFx(d["ruta"], d.get("desde", 0.0), d.get("vel", 1.0))
        return self._vids[id(d)]

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
        if rr.shape[0] * rr.shape[1] > 65536:          # capa grande (MG a cuadro entero): solo su recuadro visible (26-oct-2026,
            bx, by, bw, bh = cv2.boundingRect(np.ascontiguousarray(rr[..., 3]))      # mg_tactica: 70 -> ~10 ms por capa)
            if bw == 0:
                return
            rr = rr[by:by + bh, bx:bx + bw]
            x0, y0, x1, y1 = x0 + bx, y0 + by, x0 + bx + bw, y0 + by + bh
            if alfa >= 1 and cv2.minMaxLoc(np.ascontiguousarray(rr[..., 3]))[0] == 255:   # opaca (tablero, pantalla): copia
                f[y0:y1, x0:x1] = rr[..., :3]
                return
        a = rr[..., 3].astype(np.float32) * (alfa / 255)
        f[y0:y1, x0:x1] = cv2.blendLinear(np.ascontiguousarray(rr[..., :3]), np.ascontiguousarray(f[y0:y1, x0:x1]), a, 1 - a)

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


class _VideoFx:
    """Lector de un video externo para el FX `video`: cuadro en `desde + dt`; se queda en el último si el rango sobra."""

    def __init__(self, ruta, desde, vel=1.0):
        import cv2
        self.cap = cv2.VideoCapture(ruta)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.n = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.desde, self.vel, self.i, self.ult = desde, vel, -1, None

    def cuadro(self, dt):
        import cv2
        obj = min(int(round((self.desde + max(0.0, dt) * self.vel) * self.fps)), self.n - 1)
        if obj < self.i or obj > self.i + 90:          # salto (la hoja de revisión va y viene): reposiciona
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, obj)
            self.i = obj - 1
        while self.i < obj:
            ok, f = self.cap.read()
            if not ok:
                break
            self.i, self.ult = self.i + 1, f
        if self.ult is None:
            raise SystemExit("efectos.py: no pude leer el video del FX `video`")
        return self.ult


def _zoom_video(v, d, dt):
    """Recorte que se acerca de `zoom0` a `zoom` (z, cx, cy; cx, cy = centro en fracción del cuadro fuente) con ease-in-out.
    Lo que dibuje la pizarra encima se mide sobre el cuadro YA acercado (hoja: previews/cuadros con el mismo recorte)."""
    import cv2
    import numpy as np
    z1, cx1, cy1 = d["zoom"]
    z0, cx0, cy0 = d.get("zoom0", (1.0, .5, .5))
    dur = d.get("zoom_dur", .6)
    p = ease(clamp((dt - d.get("zoom_en", 0.0)) / dur)) if dur > 0 else 1.0
    z, cx, cy = z0 + (z1 - z0) * p, cx0 + (cx1 - cx0) * p, cy0 + (cy1 - cy0) * p
    if z <= 1.001:
        return v
    h, w = v.shape[:2]
    cw, ch = w / z, h / z
    x0 = min(max(cx * w - cw / 2, 0), w - cw)
    y0 = min(max(cy * h - ch / 2, 0), h - ch)
    m = np.float32([[z, 0, -x0 * z], [0, z, -y0 * z]])
    return cv2.warpAffine(v, m, (w, h), flags=cv2.INTER_LINEAR)


def _croma(v):
    """Quita la pantalla verde (assets de patrocinios): BGRA con borde suave y sin halo verde."""
    import cv2
    import numpy as np
    b, g, r = (v[..., i].astype(np.int16) for i in range(3))
    m = np.maximum(r, b)
    a = 1 - np.clip((g - m - 28) / 52.0, 0, 1)
    a = cv2.GaussianBlur(a.astype(np.float32), (3, 3), 0)
    g = np.minimum(g, m + 12)                           # despill
    return np.dstack([b, g, r, a * 255]).clip(0, 255).astype(np.uint8)


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
    import tts_eleven as E
    os.makedirs("sfx", exist_ok=True)
    gasto = 0
    for n in faltan:
        txt, dur = capa.sfx[n]
        # E.post reintenta 429/5xx y pasa a la cuenta de respaldo si la activa se queda sin saldo
        r = E.post("sound-generation", timeout=180,
                   json=dict(text=txt, duration_seconds=min(float(dur), 22), prompt_influence=0.45))
        if r.status_code != 200:
            raise SystemExit(f"ElevenLabs {r.status_code} en «{n}»: {r.text[:300]}")
        open(f"sfx/{n}.mp3", "wb").write(r.content)
        gasto += int(r.headers.get("character-cost") or 0)
        print(f"  sfx/{n}.mp3  {dur} s", flush=True)
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
    out_voz = np.zeros((2, N), np.float32)            # PISTAS con voz=True: a nivel de voz y con la música agachada
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
        (out_voz if d.get("voz") else out)[:, i:i + x.shape[1]] += x
    os.makedirs("audio", exist_ok=True)
    sf.write("audio/fx.wav", out.T, SR, subtype="PCM_16")
    if np.abs(out_voz).max() > 0:
        sf.write("audio/fx_voz.wav", out_voz.T, SR, subtype="PCM_16")
        print("audio/fx_voz.wav: pistas a nivel de voz (voz=True)")
    elif os.path.exists("audio/fx_voz.wav"):
        os.remove("audio/fx_voz.wav")
    print(f"audio/fx.wav: {len(capa.pistas)} sonidos en {capa.total:.1f} s (pico {np.abs(out).max():.2f}); `mezcla` lo suma a la voz")


def hoja():
    """Un cuadro por efecto y por rótulo (en su momento más visible), con su etiqueta: para revisar con la vista."""
    import cv2
    import numpy as np
    capa = cargar()
    if capa is None:
        raise SystemExit("Este video no tiene efectos.py")
    S = capa.S
    ev = [(d["de"] + min(0.12 if d["tipo"] in ("temblor", "destello") else d.get("ver", 0.7), (d["a"] - d["de"]) * .6),
           f"apoyo {d['apoyo']}" if d.get("apoyo") else d.get("nombre", d["tipo"])) for d in capa.fx]
    ev += [(d["de"] + min(0.8, (d["a"] - d["de"]) * .6), d["texto"][:22]) for d in capa.rot]
    ev += [((b["t0"] + b["t1"]) / 2, "cámara") for b in capa.bs if b["id"] in capa.camaras]
    ev.sort()
    os.makedirs("previews", exist_ok=True)
    minis = []
    mw, mh, cols, letra = 480, 270, 4, .55
    for t, nombre in ev:
        k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
        b = capa.bs[k]
        f = capa.aplicar(capa.envolver(S._fuente(b, k, True, capa), b).cuadro(t), t)
        if f.shape[0] > f.shape[1]:          # Short/reel vertical: mini 9:16 (antes se aplastaba a 16:9, 21-oct-2026)
            mw, mh, cols, letra = 216, 384, 6, .42
        m = cv2.resize(f, (mw, mh), interpolation=cv2.INTER_AREA)
        cv2.rectangle(m, (0, mh - 26), (mw, mh), (20, 18, 18), -1)
        cv2.putText(m, f"{t:.1f}s {b['id'][6:]} {nombre}".encode("ascii", "replace").decode(), (6, mh - 7), cv2.FONT_HERSHEY_SIMPLEX, letra,
                    (90, 214, 255), 1, cv2.LINE_AA)
        minis.append(m)
    n = cols * 5
    for h in range(0, len(minis), n):
        g = minis[h:h + n] + [np.zeros_like(minis[0])] * (-len(minis[h:h + n]) % cols)
        ruta = f"previews/fx_{h // n + 1:02d}.jpg"
        cv2.imwrite(ruta, np.vstack([np.hstack(g[i:i + cols]) for i in range(0, len(g), cols)]))
        print(ruta)
    capa.lista()


def _sig(o, prof=0):
    """Firma estable (texto) de un FX: dicts/listas por contenido; las fn de los kits por su código y las variables que
    capturan (ruta de la pegatina, título, puntos del mapa…), sin direcciones de memoria."""
    import re
    if prof > 6:
        return "…"
    if isinstance(o, dict):
        return "{" + ",".join(f"{k}:{_sig(v, prof + 1)}" for k, v in sorted(o.items(), key=lambda kv: str(kv[0]))) + "}"
    if isinstance(o, (list, tuple)):
        return "[" + ",".join(_sig(v, prof + 1) for v in o) + "]"
    if callable(o) and hasattr(o, "__code__"):
        cel = []
        for c in (o.__closure__ or ()):
            try:
                cel.append(_sig(c.cell_contents, prof + 1))
            except ValueError:                         # celda vacía
                cel.append("∅")
        import hashlib
        return f"fn:{o.__qualname__}:{hashlib.sha1(o.__code__.co_code).hexdigest()[:12]}(" + ",".join(cel) + ")"
    if hasattr(o, "shape"):                            # arrays / imágenes cacheadas dentro de un closure
        return f"arr{getattr(o, 'shape', '')}"
    if isinstance(o, str) and os.path.exists(o) and os.path.isfile(o):
        return f"{o}:{os.path.getmtime(o):.0f}"        # una pegatina/mapa cambiada en disco rehace su tramo
    return re.sub(r" at 0x[0-9a-fA-F]+", "", repr(o))


def montaje(forzar=False):
    """Para la vista «Montaje» del panel: previews/montaje_fx.json (apoyos con su momento y lugar, y tramos con efectos) y un
    mp4 de 960 px por tramo con motion graphics o videos encima (mismo armado que el render: clips, transiciones y toda la
    capa), con el audio de efectos de ese tramo (p. ej. el creativo de un patrocinio). Tramos a < 1,2 s se juntan."""
    import subprocess
    import time
    import secuencia as S
    capa = cargar()
    if capa is None:
        raise SystemExit("Este video no tiene efectos.py")
    car = os.path.join("previews", "montaje_fx")
    os.makedirs(car, exist_ok=True)
    nuc = os.path.dirname(os.path.abspath(__file__))
    # 26-oct-2026: firma POR TRAMO con su contenido (los FX que pisa, con los parámetros de sus fn, y sus clips), no la fecha de
    # efectos.py/kits: antes, tocar una pegatina rehacía los ~200 tramos de un video de 50 min (horas sin ver nada en el panel)
    import hashlib
    base = "|".join(f"{os.path.getmtime(r):.0f}" for r in ["beats.json", "timeline.json", os.path.join(nuc, "secuencia.py"),
                                                             os.path.join(nuc, "vivo.py")] if os.path.exists(r))
    rfir = os.path.join(car, "_firmas.json")
    try:
        firmas = json.load(open(rfir, encoding="utf-8"))
    except (OSError, ValueError):
        firmas = {}
    apoyos =[dict(n=d["apoyo"], de=round(d["de"], 3), a=round(d["a"], 3), x=d.get("x", .5), y=d.get("y", .5), ancho=d["ancho"],
                   alto=d.get("alto"), anim=d.get("anim"), archivo=os.path.basename(d["ruta"])) for d in capa.fx if d.get("apoyo")]
    rangos = sorted((d["de"], d["a"], d.get("nombre", d["tipo"])) for d in capa.fx if d["tipo"] in ("mg", "video", "pantalla"))
    juntos = []
    for de, a, n in rangos:
        if juntos and de - juntos[-1][1] < 1.2:
            juntos[-1][1] = max(juntos[-1][1], a)
            juntos[-1][2].append(n)
        else:
            juntos.append([de, a, [n]])
    _bs = S.cargar_beats()
    plan = []
    for de, a, ns in juntos:
        f0, f1 = int(max(0.0, de - .4) * S.FPS), int(min(capa.total, a + .4) * S.FPS)
        de, a = f0 / S.FPS, f1 / S.FPS
        nombre = f"fx_{f0:06d}_{f1:06d}.mp4"
        # y los clips de los beats que pisa el tramo (19-oct-2026: un clip rebajado no rehacía su tramo)
        clips = [f"{m}:{os.path.getmtime(m):.0f}" for bb in _bs if bb["t1"] > de and bb["t0"] < a
                 for m in [S.medio_de(bb)] if m and os.path.exists(m)]
        dentro = sorted(_sig({k: v for k, v in d.items() if k not in ("_marcas",)}) for d in capa.fx
                        if d["de"] < a and d["a"] > de)
        sig = hashlib.sha1("\n".join([base] + clips + dentro).encode("utf-8", "replace")).hexdigest()
        plan.append((de, a, ns, nombre, sig))

    tramos = []

    def _guardar(hechos):
        json.dump(dict(apoyos=apoyos, tramos=hechos, hecho=time.time()),
                  open("previews/montaje_fx.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        json.dump(firmas, open(rfir, "w", encoding="utf-8"), indent=0)

    def _al_dia(nombre, sig):
        return not forzar and os.path.exists(os.path.join(car, nombre)) and firmas.get(nombre) == sig

    # 26-oct-2026: el panel ve el avance; primero lo que ya está al día y luego cada tramo en cuanto se pinta
    listos = {p[3] for p in plan if _al_dia(p[3], p[4])}
    pend = len(plan) - len(listos)
    print(f"montaje: {len(plan)} tramos, {pend} por pintar", flush=True)
    _guardar([dict(de=round(p[0], 4), a=round(p[1], 4), archivo=p[3], que=" + ".join(p[2])) for p in plan if p[3] in listos])
    hechos_n = 0
    for de, a, ns, nombre, sig in plan:
        ruta = os.path.join(car, nombre)
        if nombre not in listos:
            hechos_n += 1
            print(f"montaje [{hechos_n}/{pend}]: tramo {de:.1f}-{a:.1f} s ({', '.join(ns)})", flush=True)
            tmp = os.path.join(car, "_tmp.mp4")
            S.video(["--tramo", f"{de + 1e-4:.4f}-{a + 1e-4:.4f}", "--salida", tmp, "--ancho", "960", "--preset", "veryfast"])
            pistas = [r for r in ("audio/fx_voz.wav", "audio/fx.wav") if os.path.exists(r)]
            cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", tmp]
            for r in pistas:
                cmd += ["-ss", f"{de:.3f}", "-t", f"{a - de:.3f}", "-i", r]
            if pistas:
                mezcla = "".join(f"[{k + 1}:a]" for k in range(len(pistas))) + f"amix=inputs={len(pistas)}:normalize=0[a]"
                cmd += ["-filter_complex", mezcla, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest"]
            else:
                cmd += ["-c", "copy"]
            subprocess.run(cmd + ["-movflags", "+faststart", ruta], check=True)
            os.remove(tmp)
            firmas[nombre] = sig
            listos.add(nombre)
            _guardar([dict(de=round(p[0], 4), a=round(p[1], 4), archivo=p[3], que=" + ".join(p[2])) for p in plan
                      if p[3] in listos])
        tramos.append(dict(de=round(de, 4), a=round(a, 4), archivo=nombre, que=" + ".join(ns)))
    for r in os.listdir(car):                          # vistas viejas que ya no corresponden a ningún tramo
        if r.endswith(".mp4") and r not in {t["archivo"] for t in tramos}:
            os.remove(os.path.join(car, r))
            firmas.pop(r, None)
    _guardar(tramos)
    print(f"previews/montaje_fx.json: {len(apoyos)} apoyos · {len(tramos)} tramos con efectos (ábrelos en el panel: 🎞 Montaje)")


if __name__ == "__main__":
    if "hoja" in sys.argv[1:]:
        hoja()
    elif "montaje" in sys.argv[1:]:
        montaje(forzar="--forzar" in sys.argv[1:])
    else:
        audio(seco="--seco" in sys.argv[1:])
        # REGLA (el usuario, 19-oct-2026): en todo video SECUENCIA YT (Warcraft, Tamriel, Runa Caída, Crónicas del gaming) el
        # Montaje del panel enseña SIEMPRE los MG, pegatinas, fichas y pantallas: `fx` exporta también la capa del Montaje
        # (solo rehace los tramos que cambiaron). Docs: docs/panel.md § Montaje y docs/estilo_secuencia_yt.md.
        if "--seco" not in sys.argv[1:] and "--sin-montaje" not in sys.argv[1:]:
            import config
            if config.ESTILO_VISUAL == "secuencia_yt" and os.path.isdir("medios"):
                montaje()
