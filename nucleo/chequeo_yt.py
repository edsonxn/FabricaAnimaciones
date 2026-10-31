# -*- coding: utf-8 -*-
"""Chequeo de capas del motor SECUENCIA YT (el usuario, 30-oct-2026: «no debes sustituir una cosa con otra» y «lo que se ve debe
reflejar lo que dice la narración»). No renderiza ni gasta nada; solo avisa, nunca bloquea.
  1. DENSIDAD: fichas, MG, mapas, pegatinas y comentarios por minuto contra la mediana de los últimos videos del canal.
  2. NARRACIÓN ↔ IMAGEN: frases que nombran algo o prometen algo visible y que ni el clip ni un efecto enseñan.
  3. CLIP DE OTRO JUEGO: títulos de fuentes.json sin el nombre del juego o con el de otro (habría cazado «Sinh, the Slumbering
     Dragon», Dark Souls II, en tes_secretos_40); los «(fijado a mano)» salen como revisar.
       python fab.py <v> chequeo        (también corre solo antes de `video`; salida completa en previews/chequeo_narracion.md)
Receta: docs/estilo_secuencia_yt.md § LISTA DE CONTROL. La pista es de texto: lo que marca se revisa a mano, no es un veredicto.
"""

import glob
import importlib.util
import json
import os
import re
import statistics
import sys

import secuencia_fx as F

CAPAS = ("fichas", "mg", "mapas", "pegatinas", "comentarios")   # los avisos «Secreto · número N» no cuentan: son numeración
UMBRAL = .75                                                    # por debajo del 75 % de la mediana del canal = aviso
N_REF = 6
PROMETE = re.compile(r"\b(se ve|se ven|se alcanza a ver|alcanzas a ver|puedes ver|podrás ver|verás|mira|miren|fíjate|fijate|"
                     r"aquí está|ahí está|aparece|aparecen|como ves|así se ve|esta es|este es)\b", re.I)


OTROS = re.compile(r"(dark souls|elden ring|sekiro|bloodborne|witcher|baldur|dragon age|dragon's dogma|dragons dogma|fallout|starfield|"
                   r"minecraft|genshin|monster hunter|god of war|diablo|runescape|final fantasy)", re.I)
ALIAS = {"skyrim": ("skyrim", "tesv", "elder scrolls", "dovahkiin", "dawnguard", "dragonborn", "tamriel", "solstheim"),
         "world of warcraft": ("warcraft", "wow", "azeroth"), "elden ring": ("elden ring", "shadow of the erdtree", "erdtree")}


def clase(d):
    """Capa a la que pertenece un FX, o None si no es gráfico (temblor, destello…)."""
    if d.get("tipo") not in ("mg", "pantalla"):
        return None
    n = (d.get("nombre") or "").lower()
    for pref, c in (("aviso", "avisos"), ("pegatina com_", "comentarios"), ("pegatina", "pegatinas"), ("mapa", "mapas"),
                    ("pantalla", "pantallas"), ("ficha", "fichas")):
        if n.startswith(pref):
            return c
    return "mg"


def contar(carpeta):
    """{capa: por minuto} de un video, o None si su efectos.py no carga."""
    previo = os.getcwd()
    try:
        os.chdir(carpeta)
        sys.path.insert(0, carpeta)
        total = json.load(open("timeline.json", encoding="utf-8"))["total"]
        sp = importlib.util.spec_from_file_location("efectos_ref", "efectos.py")
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        cuenta = {}
        for d in getattr(m, "FX", []):
            c = clase(d)
            if c:
                cuenta[c] = cuenta.get(c, 0) + 1
        return {c: cuenta.get(c, 0) / (total / 60) for c in CAPAS}
    except (Exception, SystemExit):
        return None
    finally:
        sys.path.remove(carpeta)
        os.chdir(previo)


def canal_de(estado):
    m = re.search(r"^- canal:\s*(\w+)", open(estado, encoding="utf-8").read(), re.M)
    return m.group(1) if m else None


def referencia(carpeta):
    """Mediana por capa de los últimos videos del mismo canal."""
    estado = os.path.join(carpeta, "ESTADO.md")
    canal = canal_de(estado) if os.path.exists(estado) else None
    if not canal:
        return None, 0
    otros = []
    for e in glob.glob(os.path.join(os.path.dirname(carpeta), "*", "ESTADO.md")):
        c = os.path.dirname(e)
        if c != carpeta and "_plantilla" not in c and canal_de(e) == canal and os.path.exists(os.path.join(c, "efectos.py")):
            otros.append(c)
    otros.sort(key=lambda c: os.path.getmtime(os.path.join(c, "efectos.py")), reverse=True)
    filas = [f for f in (contar(c) for c in otros[:N_REF]) if f]
    if not filas:
        return None, 0
    return {c: statistics.median(f[c] for f in filas) for c in CAPAS}, len(filas)


def densidad(carpeta):
    este = contar(carpeta)
    if not este:
        print("  (efectos.py no carga: sin chequeo de densidad)")
        return
    ref, n = referencia(carpeta)
    print(f"DENSIDAD (por minuto; canal = mediana de sus últimos {n} videos)")
    for c in CAPAS:
        r = ref[c] if ref else 0
        baja = bool(ref) and r > 0 and este[c] < r * UMBRAL
        print(f"  {c:12s} {este[c]:4.1f}   canal {r:4.1f}" + (f"   ⚠ BAJÓ {100 - este[c] / r * 100:.0f} %" if baja else ""))


def nombres(frases):
    """Nombres propios del guion: mayúscula a media oración (al inicio solo si también sale a media oración en otra parte)."""
    medios, veces = set(), {}
    for fr in frases:
        for m in re.finditer(r"(?<![.!?…:¿¡]\s)(?<!^)\b[A-ZÁÉÍÓÚÑ][\wáéíóúñü'-]{2,}", fr["texto"]):
            medios.add(F._norm(m.group()))
    for fr in frases:
        for w in set(F._norm(x) for x in re.findall(r"[\wáéíóúñü'-]+", fr["texto"])):
            if w in medios:
                veces[w] = veces.get(w, 0) + 1
    return {w for w in medios if w and veces.get(w, 0) <= max(4, len(frases) * .06)}   # lo que sale a cada rato (Skyrim) no dice nada


def narracion(carpeta):
    capa = F.cargar()
    if not capa:
        print("  (sin efectos.py: sin chequeo de narración)")
        return
    tl = json.load(open("timeline.json", encoding="utf-8"))
    frases = [fr for e in tl["escenas"] for fr in e["frases"]]
    propios = nombres(frases)
    fuentes = json.load(open("fuentes.json", encoding="utf-8")) if os.path.exists("fuentes.json") else {}
    graficos = [d for d in capa.fx if clase(d) not in (None, "avisos")]
    promete, sueltos = [], []
    for fr in frases:
        ini, fin = fr["t0"], fr["t1"]
        medio = (ini + fin) / 2
        beat = next((b for b in capa.bs if b["t0"] <= medio <= b["t1"]), capa.bs[-1])
        fu = fuentes.get(beat["id"], {}) if isinstance(fuentes.get(beat["id"]), dict) else {}
        activos = [d.get("nombre") or "" for d in graficos if d["de"] <= fin and d["a"] >= ini]
        visto = set(F._norm(w) for w in re.findall(r"[\wáéíóúñü'-]+", " ".join(activos + [fu.get("q", ""), fu.get("titulo", "")]).replace("_", " ")))
        faltan = sorted({w for w in (F._norm(x) for x in re.findall(r"[\wáéíóúñü'-]+", fr["texto"])) if w in propios} - visto)
        if not faltan:
            continue
        fila = (ini, beat["id"], fr["texto"], faltan, fu.get("q", ""), activos)
        (promete if PROMETE.search(fr["texto"]) else sueltos).append(fila)
    salida = os.path.join("previews", "chequeo_narracion.md")
    os.makedirs("previews", exist_ok=True)
    with open(salida, "w", encoding="utf-8") as f:
        f.write("# Narración ↔ imagen: revisar a mano (pista de texto, no veredicto)\n")
        for tit, filas in (("La voz PROMETE algo visible", promete), ("Nombre sin pegatina ni clip que lo diga", sueltos)):
            f.write(f"\n## {tit} ({len(filas)})\n")
            for t, b, tx, fa, q, ac in filas:
                f.write(f"- {int(t // 60)}:{int(t % 60):02d} {b} · falta: {', '.join(fa)}\n  voz: {tx}\n  clip: {q or '?'} · efectos: {', '.join(ac) or 'ninguno'}\n")
    print(f"NARRACIÓN ↔ IMAGEN: {len(promete)} frases prometen algo visible y {len(sueltos)} nombran algo sin apoyo → {salida}")
    for t, b, tx, fa, q, ac in promete[:10]:
        print(f"  ⚠ {int(t // 60)}:{int(t % 60):02d} {b} [{', '.join(fa)}] clip «{q or '?'}»: {tx[:90]}")


def otro_juego():
    """Beats cuyo clip viene de un video que no parece del juego. Solo avisa: hay que mirar el clip."""
    if not os.path.exists("fuentes.json"):
        return
    import guion
    sufijo = ((getattr(guion, "SECUENCIA", {}) or {}).get("yt") or {}).get("sufijo", "").lower()
    if not sufijo:
        return
    nombres_ = ALIAS.get(sufijo, (sufijo,))
    fuentes = json.load(open("fuentes.json", encoding="utf-8"))
    beats = {b["id"] for b in json.load(open("beats.json", encoding="utf-8"))}
    otros, a_mano = [], []
    for k in sorted(fuentes):
        r = fuentes[k]
        if k not in beats or not isinstance(r, dict):
            continue
        t = r.get("titulo", "")
        if t == "(fijado a mano)":
            a_mano.append(k)
        elif OTROS.search(t) or not any(n in t.lower() for n in nombres_):
            otros.append((k, r.get("video", ""), t))
    print(f"CLIP DE OTRO JUEGO: {len(otros)} títulos sin «{sufijo}» o de otro juego · {len(a_mano)} fijados a mano por revisar")
    for k, v, t in otros:
        print(f"  ⚠ {k} {v}: {t[:80]}")
    if a_mano:
        print("  a mano: " + " ".join(k[6:] for k in a_mano))


def main():
    carpeta = os.getcwd()
    densidad(carpeta)
    narracion(carpeta)
    otro_juego()
    print("Lista completa de capas: docs/estilo_secuencia_yt.md § LISTA DE CONTROL")


if __name__ == "__main__":
    main()
