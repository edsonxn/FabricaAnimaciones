# -*- coding: utf-8 -*-
"""Biblioteca del EN VIVO: lo que el canal ya tiene en disco y se puede enseñar al instante.

- pegatinas: videos/<prefijo>*/pegatinas/*.png (recortadas, con transparencia) + su nombre de _lista.json
- clips:     videos/<prefijo>*/medios/scene-NNN.mp4 + el texto que la voz decía sobre ese clip (beats.json)
- ost:       pistas de la banda sonora ya bajadas (audio/ost/*.wav) o, si no hay, la música armada del video
- web:       lo que no esté en disco se busca en la wiki del juego (pageimages) y se guarda en caché

Ids: "<carpeta_del_video>/<nombre>" (p. ej. "tes_secretos_40/alduin", "tes_secretos_40/scene-012").
"""
import glob
import hashlib
import json
import os
import random
import re
import unicodedata
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VIDEOS = os.path.join(RAIZ, "videos")
UA = {"User-Agent": "Mozilla/5.0 (FabricaAnimaciones; envivo)"}

# Canales con lo que el en vivo puede reutilizar. «estilo» = cómo habla el narrador.
CANALES = {
    "cronicas_tamriel": {
        "nombre": "Crónicas de Tamriel", "prefijos": ["tes_"], "wiki": "https://elderscrolls.fandom.com/api.php",
        "juego": "The Elder Scrolls (Skyrim, Oblivion, Morrowind)", "tema_inicial": "Los secretos más raros de Skyrim",
        "estilo": "narrador sarcástico e irónico de Crónicas de Tamriel; datos exactos de lore; burla amable al jugador",
    },
    "cronicas_warcraft": {
        "nombre": "Crónicas de Warcraft", "prefijos": ["wow_"], "wiki": "https://warcraft.wiki.gg/api.php",
        "juego": "World of Warcraft", "tema_inicial": "Los objetos más raros de World of Warcraft",
        "estilo": "narrador sarcástico e irónico de Crónicas de Warcraft; lore exacto; burla amable al jugador",
    },
    "runa_caida": {
        "nombre": "Runa Caída", "prefijos": ["er_"], "wiki": "https://eldenring.wiki.fextralife.com/api.php",
        "juego": "Elden Ring", "tema_inicial": "Los jefes que todos ignoran en Elden Ring",
        "estilo": "narrador grave y algo burlón de Runa Caída; lore exacto",
    },
}


def normal(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def palabras(s):
    return {w for w in re.findall(r"[a-z0-9]+", normal(s)) if len(w) >= 4}


def _leer_json(ruta):
    try:
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        try:
            with open(ruta, encoding="latin-1") as f:
                return json.load(f)
        except Exception:
            return None


class Biblioteca:
    def __init__(self, canal, cache):
        self.canal = canal
        self.cfg = CANALES[canal]
        self.cache = cache
        os.makedirs(cache, exist_ok=True)
        self.pegatinas = {}     # id -> {"ruta", "desc", "pal"}
        self.clips = {}         # id -> {"ruta", "texto", "pal"}
        self.ost = []
        self.usados = []        # clips ya puestos (para no repetir pronto)
        self.peg_usadas = []    # pegatinas ya enseñadas: salen del catálogo un buen rato, así el director cuenta cosas nuevas
        self._indexar()

    def _carpetas(self):
        for pre in self.cfg["prefijos"]:
            for d in sorted(glob.glob(os.path.join(VIDEOS, pre + "*"))):
                if os.path.isdir(d):
                    yield d

    def _indexar(self):
        for d in self._carpetas():
            v = os.path.basename(d)
            lista = _leer_json(os.path.join(d, "pegatinas", "_lista.json")) or {}
            for png in glob.glob(os.path.join(d, "pegatinas", "*.png")):
                slug = os.path.splitext(os.path.basename(png))[0]
                if slug.startswith("_") or slug.startswith("com_"):     # comentarios de gente: no van al en vivo
                    continue
                e = lista.get(slug)
                desc = e if isinstance(e, str) else (e or {}).get("archivo", "") if isinstance(e, dict) else ""
                desc = re.sub(r"\.(png|jpe?g|webp)$", "", str(desc)).replace("_", " ")
                rec = os.path.join(d, "pegatinas", "_rec", slug + ".png")     # ya recortada sin fondo (peg_estilos.recorte)
                self.pegatinas[f"{v}/{slug}"] = {"ruta": png, "desc": desc, "rec": rec if os.path.exists(rec) else None,
                                                 "pal": palabras(slug.replace("_", " ") + " " + desc)}
            beats = _leer_json(os.path.join(d, "beats.json")) or []
            textos = {b.get("id"): b.get("texto", "") for b in beats if isinstance(b, dict)}
            for mp4 in glob.glob(os.path.join(d, "medios", "scene-*.mp4")):
                sid = os.path.splitext(os.path.basename(mp4))[0]
                if os.path.getsize(mp4) < 200_000:
                    continue
                t = textos.get(sid, "")
                if "@" in t:                                            # beats de comentarios: no
                    continue
                self.clips[f"{v}/{sid}"] = {"ruta": mp4, "texto": t, "pal": palabras(t)}
            self.ost += glob.glob(os.path.join(d, "audio", "ost", "*.wav")) + glob.glob(os.path.join(d, "audio", "ost", "*.mp3"))
        if not self.ost:
            for d in self._carpetas():
                m = os.path.join(d, "audio", "musica.wav")
                if os.path.exists(m):
                    self.ost.append(m)
        vistos, unicos = set(), []
        for o in self.ost:                                              # la misma pista bajada en varios videos
            k = os.path.basename(o)
            if k not in vistos:
                vistos.add(k)
                unicos.append(o)
        self.ost = unicos

    # --- para el prompt del director ---------------------------------------------------------
    def candidatos(self, texto, n_peg=45, n_clip=16):
        """Pegatinas y clips más parecidos al tema (sin las ya enseñadas), con algo de azar para que cada bloque traiga cosas nuevas."""
        p = palabras(texto)

        def orden(d):
            puntos = [(len(p & e["pal"]), random.random(), k) for k, e in d.items()]
            puntos.sort(reverse=True)
            return [k for s, _, k in puntos]
        pegs = [k for k in orden(self.pegatinas) if k not in self.peg_usadas[-40:]][:n_peg]
        clips = [k for k in orden(self.clips) if k not in self.usados[-30:]][:n_clip]
        return pegs, clips

    def texto_catalogo(self, pegs, clips):
        lp = [f"{k} = {self.pegatinas[k]['desc'] or k.split('/')[-1].replace('_', ' ')}" for k in pegs]
        lc = [f"{k} = {self.clips[k]['texto'][:110]}" for k in clips]
        return "PEGATINAS (imagen real recortada):\n" + "\n".join(lp) + "\n\nCLIPS DE GAMEPLAY (lo que se ve, según la frase que lo acompañó):\n" + "\n".join(lc)

    def clip_para(self, frase):
        """El clip cuyo texto más se parece a la frase; si no hay parecido, uno al azar que no se haya usado hace poco."""
        p = palabras(frase)
        libres = [k for k in self.clips if k not in self.usados[-40:]] or list(self.clips)
        mejor = max(libres, key=lambda k: (len(p & self.clips[k]["pal"]), random.random())) if libres else None
        return mejor

    def usar_clip(self, k):
        self.usados.append(k)

    # --- imágenes de la wiki -----------------------------------------------------------------
    def buscar_web(self, consulta):
        """Primera imagen de página de la wiki del juego para «consulta». Devuelve ruta local o None."""
        if not consulta:
            return None
        h = hashlib.md5((self.canal + consulta.lower()).encode()).hexdigest()[:12]
        for ext in (".jpg", ".png", ".webp"):
            r = os.path.join(self.cache, h + ext)
            if os.path.exists(r):
                return r
        try:
            q = urllib.parse.urlencode({"action": "query", "generator": "search", "gsrsearch": consulta, "gsrlimit": 3,
                                        "gsrnamespace": 0, "prop": "pageimages", "pithumbsize": 800, "format": "json"})
            req = urllib.request.Request(self.cfg["wiki"] + "?" + q, headers=UA)
            data = json.load(urllib.request.urlopen(req, timeout=8))
            paginas = sorted((data.get("query") or {}).get("pages", {}).values(), key=lambda x: x.get("index", 99))
            url = next((pg["thumbnail"]["source"] for pg in paginas if pg.get("thumbnail")), None)
            if not url:
                return None
            ext = ".png" if ".png" in url.lower() else ".webp" if ".webp" in url.lower() else ".jpg"
            ruta = os.path.join(self.cache, h + ext)
            req = urllib.request.Request(url, headers=UA)
            with open(ruta, "wb") as f:
                f.write(urllib.request.urlopen(req, timeout=10).read())
            return ruta
        except Exception:
            return None
