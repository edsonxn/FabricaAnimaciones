# -*- coding: utf-8 -*-
"""Pegatinas de «Los 25 ERRORES al llegar al nivel 60 en WoW Forever» (22-nov-2026; adaptado de wow_ruta_forever/_pegatinas.py
y wow_errores_30_60/_pegatinas.py). Una por cosa que NOMBRA la voz; identidad = id de Wowhead Forever o archivo concreto de la wiki.
- o_<slug> = ÍCONO de objeto/hechizo: id de objeto/hechizo de la investigación (videos/_investigacion_wow_errores_60.md, «En pantalla»)
  → API de tooltips de Wowhead FOREVER (nether.wowhead.com/forever/tooltip/<item|spell>/<id>, locale=6 da el nombre es-ES para
  comprobar) → wow.zamimg.com/images/wow/icons/large/<icon>.jpg (56 px, ampliado a 320: solo rel/cam/ficha, nunca PE.banda).
  ICONO_DIRECTO = íconos genéricos por nombre (profesiones, oro, reparar…), comprobados con HEAD.
- PNJ con pin en el mapa mundial de Wowhead Forever (nether.wowhead.com/forever/data/world-map, campo «model» del PNJ):
  modelo 3D de Wowhead Forever (webthumb classicplus).
- Jefes, lugares, mazmorras: ARCHIVO CONCRETO de warcraft.wiki.gg (capturas oficiales de Forever «Raid_*», «Dungeon_*», «Zones_*»;
  pantallas de carga de Classic; capturas del juego). Nada de Hearthstone, TCG, arte de fans ni Retail nuevo.
python _pegatinas.py → pegatinas/<slug>.png (≤ 900 px) + pantallas/<slug>.jpg (1920, si el original es ≥ 1000) + previews/pegatinas_hoja.jpg
NO toca los com_*.png (tarjetas de comentarios: _com_tarjetas.py)."""
import io
import json
import os
import sys
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
PEG, PAN = os.path.join(D, "pegatinas"), os.path.join(D, "pantallas")
for c in (PEG, PAN, os.path.join(D, "previews")):
    os.makedirs(c, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (FabricaAnimaciones)"}
WIKI_API = "https://warcraft.wiki.gg/api.php"
PRENSA = "Blizzard, capturas oficiales de Forever (blizzard.gamespress.com/wowforeverreveal)"

# slug: (archivo de warcraft.wiki.gg, recorte, qué es / identidad, escena(s))
#   recorte: None · "carga_classic" (800x600 / 1280x1024 con marco y logo) · "carga_forever" (bandas de madera)
WIKI = {
    # --- las tres bandas del 9-dic (intro, c08, c13, c18, c17)
    "guarida_onyxia": ("Onyxia's Lair loading screen.jpg", "carga_classic", "pantalla de carga de la Guarida de Onyxia (Classic)", "intro c23 c10 c08"),
    "cima_hyjal": ("Raid Hyjal 085.jpg", None, "«Raid in Mount Hyjal» (galería de Forever) = Cima Hyjal", "intro c18 c13 c08"),
    "cima_hyjal_2": ("Raid Hyjal 086.jpg", None, "«Raid in Mount Hyjal» (galería de Forever) = Cima Hyjal", "c18"),
    "cavernas_tumulo": ("Raid BarrowDeeps 082.jpg", None, "«Raid in Barrow Deeps» (galería de Forever) = Cavernas del Túmulo", "intro c17 c08"),
    "cavernas_tumulo_2": ("Raid BarrowDeeps 077.jpg", None, "«Raid in Barrow Deeps» (galería de Forever)", "c17"),
    "cavernas_tumulo_3": ("Raid BarrowDeeps 104.jpg", None, "«Raid in Barrow Deeps» (galería de Forever)", "c17 c03"),
    "monte_hyjal": ("Zones Hyjal 025.png", None, "Mount Hyjal (galería de Forever; página Mount Hyjal (Forever))", "c18 c06"),
    "monte_hyjal_2": ("Zones Hyjal 032.jpg", None, "Mount Hyjal (galería de Forever)", "c06"),
    "nordrassil": ("Nordrassil above pre-cata.jpg", None, "página Nordrassil: el Árbol del Mundo visto desde arriba, antes de Cataclysm", "c18 c06"),
    "archimonde": ("Archimonde-BC.jpg", None, "páginas Archimonde y Archimonde (tactics): el jefe de la Cima Hyjal de The Burning Crusade", "c18"),
    # --- Onyxia (c23, c10, c09)
    "onyxia": ("Onyxia.jpg", None, "archivo «Onyxia» (captura del juego, Guarida)", "c23 c09"),
    "cria_onyxia": ("Onyxian Whelp.jpg", None, "Onyxian Whelp (licencia Mob, categoría Onyxia's Lair mobs) = cría de Onyxia", "c23"),
    # --- JcJ (c24, c21)
    "garganta_grito_guerra": ("Warsong Gulch loading screen.jpg", "carga_classic", "pantalla de carga de la Garganta Grito de Guerra (Classic)", "c24"),
    "valle_alterac": ("Alterac Valley loading screen.jpg", "carga_classic", "pantalla de carga del Valle de Alterac (Classic)", "c21"),
    "islas_lanza_negra": ("Darkspear Islands loading screen.jpg", "carga_blanca", "«Darkspear Islands (battleground) loading screen in Forever»", "c21"),
    # --- c19
    "espiritu": ("Spirit Healer.jpg", None, "página Spirit Healer (ángel de la resurrección, captura del juego)", "c19"),
    # --- Cavernas / Bastión / Cuna (c17, c16, c12)
    "bastion_faucenegra": ("Dungeon TimbermawHold 057.jpg", None, "Blizzard lo llamó «Timbermaw Hold dungeon»; la wiki lo usa en «Blackmaw Hold (instance)»", "c17 c16 c12"),
    "cuna_invierno": ("Everlook.jpg", None, "imagen de la página Everlook (Vista Eterna, Cuna del Invierno)", "c17"),
    "profundidades_roca_negra": ("Blackrock Depths loading screen.jpg", "carga_classic", "pantalla de carga de Profundidades de Roca Negra (Classic)", "c16"),
    # --- Bancal del Creador (c15, c05)
    "bancal_creador": ("Dungeon ShaperTerrace 068.jpg", None, "«Shaper Terrace dungeon» (galería de Forever) = Bancal del Creador", "c15 c05"),
    "ungoro": ("Un'Goro Crater.jpg", None, "página Un'Goro Crater (captura vieja)", "c15"),
    "refugio_mariscales": ("Marshals Refuge.jpg", None, "página Marshal's Refuge (Refugio de los Mariscales, captura de Classic)", "c15"),
    # --- Roca Negra (c11, c04, c05)
    "cumbre_superior": ("Upper Blackrock Spire loading screen.jpg", "carga_classic", "pantalla de carga de la Cumbre de Roca Negra superior (Classic)", "c11 c04"),
    "drakkisath": ("General Drakkisath.jpg", None, "archivo «General Drakkisath» (captura del juego)", "c04 c01"),
    "rend": ("Rend.jpg", None, "archivo «Rend» de la página Dal'rend Blackhand (Jefe de Guerra Rend en la Cumbre)", "c04 c02"),
    "valthalak": ("Lord Valthalak.jpg", None, "archivo «Lord Valthalak» (página Lord Valthalak)", "c04 c01"),
    "vaelan": ("Vaelan.jpg", None, "«Vaelan in human form» (página Vaelastrasz): el que empieza el Lacre en la Cumbre inferior", "c04"),
    "brasaliza": ("Emberstrife.jpg", None, "archivo «Emberstrife» (página Emberstrife = Brasaliza)", "c04"),
    # --- c05 / c01
    "stratholme": ("Stratholme loading screen.jpg", "carga_classic", "pantalla de carga de Stratholme (Classic)", "c05 c01"),
    "scholomance": ("Scholomance loading screen.jpg", "carga_classic", "pantalla de carga de Scholomance (Classic)", "c05 c01"),
    "gandling": ("DarkmasterGandling.jpg", None, "archivo «DarkmasterGandling» (Maestro oscuro Gandling, Scholomance)", "c01"),
    "osahendido": ("Rivendare2.jpg", None, "archivo «Rivendare2» (usado en Baron Rivendare (Classic)) = Barón Osahendido en Stratholme", "c01"),
    # --- c06
    "tiala": ("Tiala Whitemane.jpg", None, "imagen de la página Tiala Whitemane (Tiala Melenablanca, Monte Hyjal)", "c06"),
    # --- c02
    "la_masacre": ("Dire Maul loading screen.jpg", "carga_classic", "pantalla de carga de La Masacre (Classic)", "c02"),
    "feria_luna_negra": ("Darkmoon.jpg", None, "archivo «Darkmoon» (Feria de la Luna Negra, captura vieja)", "c02"),
}
# Modelos 3D de Wowhead FOREVER: displayId del mapa mundial (nether.wowhead.com/forever/data/world-map, campo «model» del PNJ)
MODELOS = {
    "pix_xizzix": (121329, "Pix Xizzix (npc 227853), vendedor del cambio de anillos (Bahía del Botín en el mapa de Forever)", "c25"),
    "nara_wildmane": (4513, "Nara Wildmane / Nara Melena Salvaje (npc 5770), Cima del Trueno: 1.ª misión del Bastión (H)", "c16"),
    "mathrengyl": (2261, "Mathrengyl Bearwalker / Mathrengyl Caminaosos (npc 4217), Darnassus: 1.ª misión del Bastión (A)", "c16"),
    "mux": (15998, "Mux Manascrambler / Mux Malamaná (npc 16014), Gadgetzan: detector de fantasmas del conjunto 0.5", "c01"),
    "deliana": (15965, "Deliana (npc 16013), Forjaz: empieza la cadena del conjunto 0.5 (A)", "c01"),
    "mokvar": (15966, "Mokvar (npc 16012), Orgrimmar: empieza la cadena del conjunto 0.5 (H)", "c01"),
    "anthion": (15968, "Anthion Harmon (npc 16016), Stratholme: carrera de 45 min", "c01"),
    "bodley": (15994, "Bodley (npc 16033), fantasma de la Montaña Roca Negra (cadena 0.5)", "c01"),
}
# Íconos: slug: (tipo, id, qué dice la voz, escena)
ICONOS = {
    "o_anillo_canalizador": ("item", 272406, "Anillo de canalizador", "c25"),
    "o_sortija_luz": ("item", 272407, "Sortija de la Luz bendita", "c25"),
    "o_marca_garganta": ("item", 20558, "Marca de Honor de la Garganta Grito de Guerra (tareas semanales)", "c24"),
    "o_barrido_cola": ("spell", 15847, "Barrido de cola de Onyxia (el coletazo)", "c23"),
    "o_bola_fuego_onyxia": ("spell", 18392, "Bola de Fuego de Onyxia (fase 2)", "c23"),
    "o_aliento_onyxia": ("spell", 17086, "Respiración = aliento de Onyxia (fase 2)", "c23"),
    "o_lacre_muneca": ("item", 275240, "Lacre de muñeca envalentonado de gran calidad (rango 8)", "c22"),
    "o_lacre_cabeza": ("item", 275241, "Lacre de cabeza envalentonado de gran calidad (rango 13)", "c22"),
    "o_marca_lanza_negra": ("item", 274895, "Marca de honor de las Islas Lanza Negra", "c21"),
    "o_marca_alterac": ("item", 20560, "Marca de Honor del Valle de Alterac", "c21"),
    "o_pocion_fuego": ("item", 13457, "Poción de protección de Fuego superior", "c20 c09"),
    "o_pocion_mana": ("item", 13444, "Poción de maná sublime", "c20"),
    "o_pocion_curacion": ("item", 13446, "Poción de curación sublime", "c20"),
    "o_elixir_mangosta": ("item", 13452, "Elixir de la mangosta", "c20"),
    "o_bolas_masa": ("item", 20452, "Bolas de masa del desierto ahumadas (comida con +5 % de experiencia)", "c20"),
    "o_arma_inutil": ("item", 274560, "Arma inútil de la Cima Hyjal", "c18"),
    "o_moneda_sonya": ("item", 286300, "Moneda de oro de Sonya Sombrasanto", "c17"),
    "o_cristal_rojo": ("item", 11186, "Cristal de poder rojo (Cinder)", "c15"),
    "o_cristal_amarillo": ("item", 11188, "Cristal de poder amarillo (Bolt)", "c15"),
    "o_cristal_azul": ("item", 11184, "Cristal de poder azul (Snowtalon)", "c15"),
    "o_cristal_verde": ("item", 11185, "Cristal de poder verde (Vitrix)", "c15"),
    "o_equitacion": ("spell", 33391, "Oficial jinete (equitación del 60)", "c14"),
    "o_montura_epica": ("item", 18776, "Palomino veloz (una montura épica racial de vendedor)", "c14"),
    "o_lacre_ascension": ("item", 12344, "Lacre de Ascensión (Seal of Ascension; +10 res. Fuego/Naturaleza/Escarcha en Forever)", "c11 c09 c04"),
    "o_amuleto_pirodraco": ("item", 16309, "Amuleto Pirodraco (+15 res. Fuego en Forever)", "c10 c09"),
    "o_capa_onyxia": ("item", 15138, "Capa de escamas de Onyxia", "c09"),
    "o_escama_onyxia": ("item", 15410, "Escama de Onyxia", "c09"),
    "o_yelmo_forjaluz": ("item", 16727, "Yelmo Forjaluz (casco del Conjunto de mazmorra, paladín; lo suelta Gandling)", "c09 c01"),
    "o_quijotes_forjaluz": ("item", 16728, "Quijotes Forjaluz (piernas del Conjunto de mazmorra; Barón Osahendido)", "c01"),
    "o_peto_forjaluz": ("item", 16726, "Peto Forjaluz (peto del Conjunto de mazmorra; Drakkisath)", "c01"),
    "o_esencia_maleable": ("item", 274030, "Esencia maleable de la Naturaleza", "c07 c03"),
    "o_tabardo_guardianes": ("item", 274025, "Tabardo de los Guardianes de Hyjal", "c06"),
    "o_vaina_semilla": ("item", 274379, "Vaina de semilla reanimadora", "c06"),
    "o_baston_montana": ("item", 267079, "Bastón de la montaña (cadena de Tiala)", "c06"),
    "o_lacre_sin_adornar": ("item", 12219, "Lacre de ascensión sin adornar", "c04"),
    "o_gema_espina_ahumada": ("item", 12335, "Gema de Espina Ahumada (general Omokk… gemas de los generales)", "c04"),
    "o_gema_cumbrerroca": ("item", 12336, "Gema de Cumbrerroca (gemas de los generales)", "c04"),
    "o_gema_hacha_sangre": ("item", 12337, "Gema de Hacha de Sangre (gemas de los generales)", "c04"),
    "o_desencantar": ("spell", 13262, "Desencantar", "c03"),
    "o_berrido": ("spell", 22888, "Berrido de convocación del matadragones (beneficio de la cabeza de Onyxia)", "c02"),
    "o_cabeza_onyxia": ("item", 18423, "Cabeza de Onyxia", "c02"),
    "o_cabeza_rend": ("item", 12630, "Cabeza de Rend Puño Negro", "c02"),
    "o_serenata": ("spell", 15366, "Serenata Cantaflor (Frondavil)", "c02"),
    "o_poderio_ventormenta": ("spell", 460939, "Poderío de Ventormenta", "c02"),
    "o_bendicion_jefe": ("spell", 16609, "Bendición del Jefe de Guerra", "c02"),
    "o_reubicador": ("item", 184937, "Reubicador cronológico", "c02"),
    "o_brasero_sagrado": ("item", 22014, "Brazal Sagrado (= brasero; pide Alba Argenta Honorable)", "c01"),
}
ICONO_DIRECTO = {   # slug: (nombre del ícono en zamimg, qué es, escena)
    "o_herreria": ("trade_blacksmithing", "ícono de la profesión Herrería", "c07"),
    "o_peleteria": ("trade_leatherworking", "ícono de la profesión Peletería", "c07"),
    "o_sastreria": ("trade_tailoring", "ícono de la profesión Sastrería", "c07"),
    "o_encantamiento": ("trade_engraving", "ícono de la profesión Encantamiento (el encantador)", "c07 c03"),
    "o_interrogacion": ("inv_misc_questionmark", "ícono de objeto desconocido (botín oculto)", "c13"),
    "o_oro": ("inv_misc_coin_01", "ícono de monedas de oro", "c19 c14 c12"),
    "o_reparar": ("ability_repair", "ícono de reparar", "c19"),
    "o_reloj": ("inv_misc_pocketwatch_01", "ícono de reloj (tope de 5 por hora)", "c05"),
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def wiki_info(nombres):
    out = {}
    for i in range(0, len(nombres), 20):
        q = urllib.parse.urlencode(dict(format="json", action="query", prop="imageinfo|fileusage", iiprop="url|size",
                                        fulimit=50, titles="|".join("File:" + n for n in nombres[i:i + 20])))
        for p in json.loads(get(WIKI_API + "?" + q))["query"]["pages"].values():
            ii = (p.get("imageinfo") or [{}])[0]
            out[p["title"][5:]] = dict(url=ii.get("url"), w=ii.get("width"), h=ii.get("height"),
                                       usado_en=[x["title"] for x in p.get("fileusage", [])])
    return out


def recortar(im, modo):
    W, H = im.size
    if modo == "carga_classic":   # marco de pergamino + logo de WoW arriba (las de 5:4, 1280x1024, tienen el marco más alto)
        abajo = 0.79 if H / W > 0.78 else 0.825
        return im.crop((int(W * 0.015), int(H * 0.25), int(W * 0.985), int(H * abajo)))
    if modo == "carga_blanca":    # pantalla de carga de Forever en boceto sepia con bandas blancas arriba y abajo
        return im.crop((0, int(H * 0.17), W, int(H * 0.83)))
    if modo == "carga_forever":   # bandas de madera arriba y abajo
        return im.crop((0, int(H * 0.135), W, int(H * 0.865)))
    return im


ACLARAR = {"monte_hyjal_2", "cavernas_tumulo", "cavernas_tumulo_2", "cavernas_tumulo_3", "bastion_faucenegra"}


def aclarar(im):
    a = im.getchannel("A") if im.mode == "RGBA" else None
    rgb = im.convert("RGB").point(lambda v: round(255 * (v / 255) ** 0.6))
    if a:
        rgb.putalpha(a)
    return rgb


def guardar(slug, im):
    if slug in ACLARAR:
        im = aclarar(im)
    if max(im.size) >= 1000:
        g = im.convert("RGB")
        g.thumbnail((1920, 1920), Image.LANCZOS)
        g.save(os.path.join(PAN, slug + ".jpg"), quality=92)
    if max(im.size) < 400:  # íconos y modelos pequeños: ampliar
        f = 320 / max(im.size) if slug.startswith("o_") else 2
        im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
    im.thumbnail((900, 900), Image.LANCZOS)
    im.save(os.path.join(PEG, slug + ".png"))
    return im.size


def icono_url(nombre):
    return f"https://wow.zamimg.com/images/wow/icons/large/{nombre}.jpg"


def main(solo=None):
    credf = os.path.join(PEG, "_creditos.json")
    cred = json.load(open(credf, encoding="utf-8")) if solo and os.path.isfile(credf) else {}
    quiere = (lambda s: s in solo) if solo else (lambda s: True)
    w = {k: v for k, v in WIKI.items() if quiere(k)}
    info = wiki_info(sorted({v[0] for v in w.values()})) if w else {}
    for slug, (arch, modo, que, esc) in w.items():
        ii = info.get(arch) or info.get(arch.replace("_", " "))
        if not ii or not ii["url"]:
            print("FALTA", slug, arch)
            continue
        im = recortar(Image.open(io.BytesIO(get(ii["url"]))).convert("RGBA"), modo)
        tam = guardar(slug, im)
        cred[slug] = dict(fuente="warcraft.wiki.gg", archivo="File:" + arch, url=ii["url"].split("?")[0],
                          pagina_archivo="https://warcraft.wiki.gg/wiki/File:" + urllib.parse.quote(arch.replace(" ", "_")),
                          identidad=que, usado_en=ii["usado_en"], escena=esc, original=f"{ii['w']}x{ii['h']}", recorte=modo,
                          aclarada=slug in ACLARAR, pegatina=f"{tam[0]}x{tam[1]}",
                          autor=PRENSA if arch.startswith(("Zones ", "Dungeon ", "Raid ")) else "captura/arte de Blizzard en la wiki")
        print(slug, tam)
    for slug, (did, que, esc) in MODELOS.items():
        if not quiere(slug):
            continue
        url = f"https://wow.zamimg.com/modelviewer/classicplus/webthumbs/npc/{did % 256}/{did}.webp"
        im = Image.open(io.BytesIO(get(url))).convert("RGBA")
        caja = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        if caja:
            m = int(0.04 * max(im.size))
            im = im.crop((max(0, caja[0] - m), max(0, caja[1] - m), min(im.width, caja[2] + m), min(im.height, caja[3] + m)))
        tam = guardar(slug, im)
        cred[slug] = dict(fuente="Wowhead Forever (modelo 3D)", url=url, identidad=que + f"; displayId {did} (mapa mundial de Wowhead Forever)",
                          escena=esc, pegatina=f"{tam[0]}x{tam[1]}")
        print(slug, tam)
    for slug, (tipo, i, que, esc) in ICONOS.items():
        if not quiere(slug):
            continue
        j = json.loads(get(f"https://nether.wowhead.com/forever/tooltip/{tipo}/{i}?locale=0"))
        es = json.loads(get(f"https://nether.wowhead.com/forever/tooltip/{tipo}/{i}?locale=6")).get("name")
        url = icono_url(j["icon"])
        tam = guardar(slug, Image.open(io.BytesIO(get(url))).convert("RGBA"))
        cred[slug] = dict(fuente="Wowhead Forever (ícono)", url=url, tooltip=f"https://www.wowhead.com/forever/{tipo}={i}",
                          identidad=f"{tipo} {i}: {j.get('name')} / es-ES «{es}» — {que}", escena=esc, pegatina=f"{tam[0]}x{tam[1]}")
        print(slug, j.get("name"), "|", es)
    for slug, (n, que, esc) in ICONO_DIRECTO.items():
        if not quiere(slug):
            continue
        url = icono_url(n)
        tam = guardar(slug, Image.open(io.BytesIO(get(url))).convert("RGBA"))
        cred[slug] = dict(fuente="Wowhead (ícono genérico por nombre)", url=url, identidad=que, escena=esc, pegatina=f"{tam[0]}x{tam[1]}")
        print(slug, n)
    json.dump(dict(sorted(cred.items())), open(credf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    hoja()


def hoja():
    fs = sorted(f for f in os.listdir(PEG) if f.endswith(".png") and not f.startswith("com_"))
    col, cw, ch = 7, 300, 230
    h = Image.new("RGB", (col * cw, ((len(fs) + col - 1) // col) * ch), (40, 40, 40))
    d = ImageDraw.Draw(h)
    fnt = ImageFont.truetype("arialbd.ttf", 17)
    for n, f in enumerate(fs):
        im = Image.open(os.path.join(PEG, f)).convert("RGBA")
        tam = im.size
        im.thumbnail((cw - 10, ch - 42))
        x, y = (n % col) * cw + 5, (n // col) * ch + 5
        h.paste(im, (x, y), im)
        d.text((x, y + ch - 36), f[:-4][:28], fill=(255, 220, 80), font=fnt)
        d.text((x + 240, y + ch - 36), f"{tam[0]}", fill=(180, 180, 180), font=fnt)
    h.save(os.path.join(D, "previews", "pegatinas_hoja.jpg"), quality=85)
    print("hoja:", len(fs))


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
