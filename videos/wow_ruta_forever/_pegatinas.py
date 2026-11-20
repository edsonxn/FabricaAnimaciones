# -*- coding: utf-8 -*-
"""Pegatinas de «La RUTA del 1 al 60 en WoW Forever» (19-nov-2026; copiado y adaptado de wow_oro_forever/_pegatinas.py).
- Lugares, mazmorras, PNJ: ARCHIVO CONCRETO de warcraft.wiki.gg (identidad = la página que lo usa / su pie de foto, ver pegatinas/_creditos.json).
  Las de Forever son las capturas oficiales de Blizzard (blizzard.gamespress.com/wowforeverreveal, «Zones_*», «Dungeon_*», «Raid_*»,
  con su pie en la galería de la página «World of Warcraft: Forever») y las subidas a la wiki desde el lanzamiento (Farholde, Bolder'ok…).
  Las de zonas viejas son capturas de Classic (o de antes de Cataclysm, mismo aspecto). Nada de Hearthstone, TCG, arte de fans ni Retail nuevo.
- Pantallas de carga: se recorta el marco (y el logo de WoW de las de Classic) → solo la ilustración.
- PNJ sin foto: modelo 3D de Wowhead FOREVER (webthumb classicplus; displayId del mapa mundial de Wowhead Forever).
- o_ = ícono de 64 px ampliado (solo para ficha/tarjeta).
python _pegatinas.py → pegatinas/<slug>.png (≤ 900 px) + pantallas/<slug>.jpg (1920, si el original es ≥ 1000) + previews/pegatinas_check.jpg
NO toca los com_*.png (tarjetas de comentarios)."""
import io
import json
import os
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

# slug: (archivo de warcraft.wiki.gg, recorte, qué es / identidad comprobada, era)
#   recorte: None · "carga_classic" (800x600 con logo) · "carga_forever" (1920x1080 con bandas de madera)
WIKI = {
    # --- Parada 1: los 7 inicios + cielonatos
    "abadia_villanorte": ("Northshireabbey.jpg", None, "página Northshire Abbey", "aspecto de Classic (edificio sin cambios)"),
    "kharanos": ("Kharanos.jpg", None, "imagen principal de la página Kharanos", "aspecto de Classic"),
    "dolanaar": ("Dolanaar.jpg", None, "imagen principal de la página Dolanaar", "aspecto de Classic"),
    "cerrotajo": ("Razor Hill Watchtower.jpg", None, "archivo «Razor Hill Watchtower» (atalaya de Cerrotajo)", "Classic/antes de Cataclysm"),
    "pezuna_sangre": ("Bloodhoof Village.jpg", None, "imagen principal de la página Bloodhoof Village", "aspecto de Classic"),
    "remol": ("Brill.jpg", None, "página Brill (versión de antes de Cataclysm; hay otra «Post Cataclysm»)", "Classic"),
    "zephras_isla": ("Zones Zephras 047.jpg", None, "Zephras Isle (pie en la galería de Forever; imagen de la página Zephras Isle)", "Forever"),
    "zephras_pueblo": ("Zones Zephras 042.jpg", None, "Zephras Isle (galería de Forever). Un pueblo de la isla: NO consta que sea Aldea Shen'dar", "Forever"),
    "zephras_torre": ("Zones Zephras 046.jpg", None, "Zephras Isle (galería de Forever)", "Forever"),
    "zephras_lago": ("Zones Zephras 049.jpg", None, "Zephras Isle (galería de Forever)", "Forever"),
    "zephras_valanaar": ("Valanaar Port Authority.png", None, "archivo «Valanaar Port Authority» (Valanaar, Isla Zephras)", "Forever"),
    "zephras_carga": ("Zephras Isle loading screen.jpg", "carga_forever", "pantalla de carga de la Isla Zephras en Forever", "Forever"),
    "cielonato": ("Skyborne Customization 096.jpg", None, "página Skyborne (playable): personalización de cielonatos", "Forever"),
    "cielonato_2": ("Skyborne Customization 060.png", None, "galería de Forever «Skyborne customization»", "Forever"),
    "cima_trueno_dirigible": ("Zones Mulgore 022.jpg", None, "Mulgore (galería de Forever): Cima del Trueno con un dirigible", "Forever"),
    "hogger": ("Hogger.jpg", None, "página Hogger (licencia Mob; modelo viejo de gnoll)", "Classic"),
    "fuerte_bandarion": ("Bandarion Keep.jpg", None, "imagen de la página Bandarion Keep (categoría Forever)", "Forever"),
    # --- Parada 2-3
    "salon_senores_feudales": ("Dungeon HallOfThanes 053.jpg", None, "«Hall of Thanes dungeon» (galería de Forever)", "Forever"),
    "salon_senores_feudales_carga": ("Hall of Thanes loading screen.jpg", "carga_forever", "pantalla de carga del Hall of Thanes en Forever", "Forever"),
    "ruinas_lordaeron": ("Dungeon Lordaeron 046.png", None, "«Dungeon in Lordaeron» (galería de Forever; página Ruins of Lordaeron (instance))", "Forever"),
    "ruinas_lordaeron_carga": ("Ruins of Lordaeron loading screen Forever.jpg", "carga_forever", "pantalla de carga de Ruins of Lordaeron en Forever", "Forever"),
    "minas_muerte": ("The Deadmines loading screen.jpg", "carga_classic", "pantalla de carga de Las Minas de la Muerte (Classic)", "Classic"),
    "cuevas_lamentos": ("Wailing Caverns loading screen.jpg", "carga_classic", "pantalla de carga de las Cuevas de los Lamentos (Classic)", "Classic"),
    "villa_del_lago": ("Lakeshire.jpg", None, "página Lakeshire (captura vieja)", "Classic"),
    # --- Parada 4-5
    "puerto_menethil": ("Menethil Harbor.jpg", None, "página Menethil Harbor (la de antes del Cataclismo; hay otra «after Cataclysm»)", "Classic"),
    "colmillo_oscuro": ("Shadowfang Keep loading screen.jpg", "carga_classic", "pantalla de carga del Castillo de Colmillo Oscuro", "Classic"),
    "brazanegra": ("Blackfathom Deeps entrance.jpg", None, "página Blackfathom Deeps: la entrada", "Classic"),
    "viento_libre": ("Freewind Post.jpg", None, "página Freewind Post (seco, antes de la inundación de Cataclysm)", "Classic"),
    "excavacion_humedales": ("Dungeon ExcavationSite 055.jpg", None, "«Excavation Site dungeon» (galería de Forever; página Excavation Site: Wetlands)", "Forever"),
    "excavacion_humedales_carga": ("Wetlands Dig Site loading screen.jpg", "carga_forever", "pantalla de carga del Sitio de Excavación en Forever", "Forever"),
    # --- Parada 6
    "dalaran": ("Zones Dalaran 021.jpg", None, "Dalaran (galería de Forever; página Dalaran)", "Forever"),
    "dalaran_mazmorra": ("Dungeon Dalaran 073.jpg", None, "«Dalaran dungeon» (galería de Forever; página City of Dalaran)", "Forever"),
    "dalaran_mazmorra_2": ("Dungeon Dalaran 074.jpg", None, "«Dalaran dungeon» (galería de Forever)", "Forever"),
    "dalaran_carga": ("Dalaran loading screen.jpg", "carga_forever", "pantalla de carga de Dalaran en Forever", "Forever"),
    "refugio_zaga": ("Refuge Pointe2.jpg", None, "página Refuge Pointe (campamento)", "aspecto de Classic (MEDIA)"),
    "sentencia": ("Hammerfall.jpg", None, "página Hammerfall (vista aérea, la empalizada de siempre)", "Classic"),
    "stromgarde": ("Stromgarde.jpg", None, "página Stromgarde Keep (vista aérea)", "Classic"),
    # --- Parada 7
    "bahia_botin": ("Booty Bay.jpg", None, "página Booty Bay (intacta; la dañada es «Post Cata»)", "aspecto de Classic"),
    "bahia_botin_2": ("Old Port Authority pre-Cata.jpg", None, "página Booty Bay: «Old Port Authority pre-Cata»", "Classic"),
    "gromgol": ("Grom'Gol Base Camp beach side.jpg", None, "página Grom'gol Base Camp (lado de la playa, con el zepelín)", "Classic"),
    "arena_gurubashi": ("Gurubashi Arena.jpg", None, "página Gurubashi Arena", "Classic"),
    "theramore": ("Theramore.jpg", None, "página Theramore Isle (intacta, antes de su destrucción)", "Classic"),
    "kargath": ("Kargath.jpg", None, "página Kargath (usada en «Badlands (Classic)»)", "Classic"),
    "ciudad_anegada": ("Dungeon DrownedCity 064.jpg", None, "«Drowned City dungeon» (galería de Forever; página Drowned City)", "Forever"),
    "ciudad_anegada_2": ("Dungeon DrownedCity 062.jpg", None, "«Drowned City dungeon» (galería de Forever)", "Forever"),
    "ciudad_anegada_3": ("Dungeon DrownedCity 060.jpg", None, "«Drowned City dungeon» (galería de Forever)", "Forever"),
    # --- Parada 8: Claros del Río
    "claros_rio": ("Zones Riverglades 035.jpg", None, "Riverglades (galería de Forever; imagen de la página Riverglades)", "Forever"),
    "claros_rio_2": ("Zones Riverglades 037.jpg", None, "Riverglades (galería de Forever)", "Forever"),
    "claros_rio_3": ("Zones Riverglades 039.jpg", None, "Riverglades (galería de Forever): pueblo humano con estatua ecuestre", "Forever"),
    "claros_rio_4": ("Zones Riverglades 040.jpg", None, "Riverglades (galería de Forever): el río", "Forever"),
    "farholde": ("Farholde Keep.jpg", None, "imagen de la página Farholde Keep", "Forever"),
    "polvomecha": ("Powderfuse Port.jpg", None, "imagen de la página Powderfuse Port", "Forever"),
    "pedregok": ("Bolder'ok.jpg", None, "imagen de la página Bolder'ok (= Pedreg'ok en es-MX)", "Forever"),
    "kroldok": ("Dungeon KrolDokStronghold 071.jpg", None, "«Krol Dok Stronghold dungeon» (galería de Forever; página Krol'dok Stronghold)", "Forever"),
    "avanzada_terral": ("Terral's Watch.jpg", None, "imagen de la página Terral's Watch (Claros del Río)", "Forever"),
    "cortijo_wheeler": ("Wheeler's Grange.jpg", None, "imagen de la página Wheeler's Grange (Claros del Río)", "Forever"),
    # --- Parada 9: Shen'dralas
    "shendralas": ("Zones Shendralas 024.jpg", None, "Shen'dralas (galería de Forever)", "Forever"),
    "valle_huesos": ("Valley of Bones east entrance old.jpg", None, "página Valley of Bones: entrada este, versión vieja", "Classic"),
    "orgrul": ("Orgrul.jpg", None, "imagen de la página Orgrul (centauro, PNJ de Forever)", "Forever"),
    # --- Parada 10
    "gadgetzan": ("Gadgetzan.jpg", None, "página Gadgetzan (captura vieja)", "Classic"),
    "plumaluna": ("Feathermoon Stronghold.jpg", None, "archivo «Feathermoon Stronghold» (la isla vieja; la nueva es «New-feathermoon»)", "Classic"),
    "mojache": ("Camp Mojache.jpg", None, "página Camp Mojache", "Classic"),
    "pico_nidal": ("Aerie Peak.jpg", None, "página Aerie Peak (estatua del grifo)", "aspecto de Classic"),
    "jinthaalor": ("Jintha'Alor.jpg", None, "página Jintha'Alor", "Classic"),
    "zulfarrak": ("Zul'Farrak loading screen.jpg", "carga_classic", "pantalla de carga de Zul'Farrak (Classic)", "Classic"),
    # --- Parada 11
    "alcaz": ("Dungeon AlcazPrison 066.jpg", None, "«Alcaz Prison dungeon» (galería de Forever; página Alcaz Prison)", "Forever"),
    "ungoro": ("Un'Goro Crater.jpg", None, "página Un'Goro Crater (captura vieja)", "Classic"),
    "atal_hakkar": ("Temple of Atal'Hakkar loading screen.jpg", "carga_classic", "pantalla de carga del Templo de Atal'Hakkar (Classic)", "Classic"),
    # --- Parada 12
    "vigilia_morgan": ("Morgan's Vigil.jpg", None, "imagen de la página Morgan's Vigil (campamento con tiendas)", "Classic? (MEDIA)"),
    "penasco_llamarada": ("Flame Crest.jpg", None, "imagen de la página Flame Crest", "Classic"),
    "profundidades_roca_negra": ("Blackrock Depths loading screen.jpg", "carga_classic", "pantalla de carga de Profundidades de Roca Negra (Classic)", "Classic"),
    "franclorn": ("Franclorn Forgewright.jpg", None, "página Franclorn Forgewright («NPC screenshot (Blackrock Mountain)»: el fantasma)", "Classic"),
    "o_oso_espectral": ("Inv bearmountblizzard.png", None, "ícono de la página «Reins of the Spectral Bear» (montura de Forever)", "Forever (ícono)"),
    # --- Parada 13
    "vista_eterna": ("Everlook.jpg", None, "imagen de la página Everlook", "aspecto de Classic"),
    "fuerte_cenarion": ("Cenarion Hold.jpg", None, "imagen de la página Cenarion Hold (800x600, captura vieja)", "Classic"),
    "capilla_esperanza": ("Light's hope.jpg", None, "página Light's Hope Chapel (cielo de la peste, sin la estatua de Legion)", "Classic"),
    "bastion_faucenegra": ("Dungeon TimbermawHold 057.jpg", None, "Blizzard lo llamó «Timbermaw Hold dungeon»; la wiki lo usa en «Blackmaw Hold (instance)» (furbolgs)", "Forever"),
    # --- Parada 14
    "monte_hyjal": ("Zones Hyjal 025.png", None, "Mount Hyjal (galería de Forever; página Mount Hyjal (Forever))", "Forever"),
    "monte_hyjal_2": ("Zones Hyjal 030.jpg", None, "Mount Hyjal (galería de Forever)", "Forever"),
    "bancal_creador": ("Dungeon ShaperTerrace 068.jpg", None, "«Shaper Terrace dungeon» (galería de Forever)", "Forever"),
    "cavernas_tumulo": ("Raid BarrowDeeps 082.jpg", None, "«Raid in Barrow Deeps» (galería de Forever)", "Forever"),
    "cavernas_tumulo_2": ("Raid BarrowDeeps 077.jpg", None, "«Raid in Barrow Deeps» (galería de Forever)", "Forever"),
    "cumbre_hyjal": ("Raid Hyjal 085.jpg", None, "«Raid in Mount Hyjal» (galería de Forever) = Cumbre Hyjal", "Forever"),
    "guarida_onyxia": ("Onyxia's Lair loading screen.jpg", "carga_classic", "pantalla de carga de la Guarida de Onyxia (Classic)", "Classic"),
}
# Modelos 3D de Wowhead FOREVER: displayId del mapa mundial (nether.wowhead.com/forever/data/world-map, campo «model» del PNJ)
MODELOS = {
    "nerlokh": (9422, "Nerlokh (npc 253177), PNJ de la Horda en Shen'dralas"),
    "orgrul_modelo": (9433, "Orgrul (npc 253136), PNJ de la Horda en Shen'dralas"),
    "shari_stilwell": (129943, "Shari Stilwell (npc 246152), Rémol: cadena del Fuerte de Bandarion"),
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def wiki_info(nombres):
    out = {}
    for i in range(0, len(nombres), 20):
        q = urllib.parse.urlencode(dict(format="json", action="query", prop="imageinfo|fileusage", iiprop="url|size",
                                        fulimit=10, titles="|".join("File:" + n for n in nombres[i:i + 20])))
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
    if modo == "carga_forever":   # bandas de madera arriba y abajo
        return im.crop((0, int(H * 0.135), W, int(H * 0.865)))
    return im


# Capturas de prensa muy oscuras: se aclaran (gamma 0.6) para que se lean en pantalla; el resto, tal cual
ACLARAR = {"alcaz", "cavernas_tumulo", "salon_senores_feudales", "dalaran_mazmorra_2", "bastion_faucenegra"}


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


def main():
    cred = {}
    info = wiki_info(sorted({v[0] for v in WIKI.values()}))
    for slug, (arch, modo, que, era) in WIKI.items():
        ii = info.get(arch) or info.get(arch.replace("_", " "))
        if not ii or not ii["url"]:
            print("FALTA", slug, arch)
            continue
        im = recortar(Image.open(io.BytesIO(get(ii["url"]))).convert("RGBA"), modo)
        tam = guardar(slug, im)
        cred[slug] = dict(fuente="warcraft.wiki.gg", archivo="File:" + arch, url=ii["url"].split("?")[0],
                          pagina_archivo="https://warcraft.wiki.gg/wiki/File:" + urllib.parse.quote(arch.replace(" ", "_")),
                          identidad=que, usado_en=ii["usado_en"], era=era, original=f"{ii['w']}x{ii['h']}",
                          recorte=modo, aclarada=slug in ACLARAR, pegatina=f"{tam[0]}x{tam[1]}",
                          autor=PRENSA if arch.startswith(("Zones ", "Dungeon ", "Raid ", "Skyborne Customization")) else "captura de la wiki (licencia Blizzard)")
        print(slug, tam)
    for slug, (did, que) in MODELOS.items():
        url = f"https://wow.zamimg.com/modelviewer/classicplus/webthumbs/npc/{did % 256}/{did}.webp"
        im = Image.open(io.BytesIO(get(url))).convert("RGBA")
        caja = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        if caja:
            m = int(0.04 * max(im.size))
            im = im.crop((max(0, caja[0] - m), max(0, caja[1] - m), min(im.width, caja[2] + m), min(im.height, caja[3] + m)))
        tam = guardar(slug, im)
        cred[slug] = dict(fuente="Wowhead Forever (modelo 3D)", url=url, identidad=que + f"; displayId {did}", era="Forever", pegatina=f"{tam[0]}x{tam[1]}")
        print(slug, tam)
    json.dump(cred, open(os.path.join(PEG, "_creditos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
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
        d.text((x + 200, y + ch - 36), f"{tam[0]}", fill=(180, 180, 180), font=fnt)
    h.save(os.path.join(D, "previews", "pegatinas_check.jpg"), quality=85)
    print("hoja:", len(fs))


if __name__ == "__main__":
    main()
