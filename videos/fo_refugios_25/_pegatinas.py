# Baja las pegatinas (imágenes reales de Fallout Wiki) a pegatinas/<slug>.png (RGBA, lado máx. 1000 px).
# URLs de _investigacion_A/B/C.md + las que faltaban, sacadas por la API de la wiki (pageimages / imageinfo).
# Copia de videos/fo_nunca_f4/_pegatinas.py. Las "page:" se piden por pageimages. TODO se mira en
# previews/pegatinas_check_N.jpg (regla de identidad) antes de usarlo.
# --rec  → además recorta sin fondo (rembg) los slugs de RECORTAR como <slug>_rec.png
import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

AQUI = Path(__file__).parent
OUT = AQUI / "pegatinas"
OUT.mkdir(exist_ok=True)
W = "https://static.wikia.nocookie.net/fallout/images/"
# slug: (url | "page:<Página>", qué muestra, juego, refugio)
P = {
    # ---- Refugios 55 / 56 (Biblia de Fallout: sin imagen propia) ----
    "r55_holocinta": (W + "0/01/FO4_Holotape.png", "holocinta (objeto genérico)", "FO4", "55/56"),
    # ---- Refugio 21 (FNV) ----
    "r21_exterior": (W + "2/2c/Vault_21_exterior.jpg", "exterior con el letrero del Refugio 21", "FNV", "21"),
    "r21_atrio": (W + "a/a9/Vault_21_Atrium.png", "atrio con mesas de blackjack", "FNV", "21"),
    "r21_tienda": (W + "c/cb/Vault_21_gift_shop_interior.jpg", "tienda de regalos", "FNV", "21"),
    "r21_sarah": (W + "3/3b/Sarah_Weintraub.jpg", "Sarah Weintraub", "FNV", "21"),
    "r21_doc_mitchell": ("page:Doc Mitchell", "Doc Mitchell", "FNV", "21"),
    "r21_house_pantalla": ("file:FNV Mr House Screen.png", "Mr. House en su pantalla (juego)", "FNV", "21"),
    "r21_house_estasis": (W + "5/56/Mr_House_in_stasis.jpg", "Mr. House real en su cápsula", "FNV", "21"),
    # ---- Refugio 118 (FO4 Far Harbor) ----
    "r118_entrada": (W + "a/a9/FO4-FarHarbor-Vault118-Entrance.jpeg", "entrada (hotel Cliff's Edge)", "FO4 FH", "118"),
    "r118_atrio": (W + "3/35/FO4-FarHarbor-Vault118-Atrium.jpeg", "atrio y escena del crimen", "FO4 FH", "118"),
    "r118_playa": (W + "0/04/FO4-FarHarbor-Vault118-Beach-Beachview.jpeg", "playa artificial", "FO4 FH", "118"),
    "r118_ezra": ("page:Ezra Parker", "Ezra Parker «muerto» (robocerebro)", "FO4 FH", "118"),
    "r118_maxwell": ("page:Maxwell (Far Harbor)", "Maxwell, el Mr. Handy", "FO4 FH", "118"),
    "r118_robocerebro": ("page:Robobrain (Fallout 4)", "robocerebro", "FO4", "118"),
    # ---- Refugio 43 (cómic) ----
    "r43_vineta": (W + "5/51/PA_Vault_43.jpg", "viñeta del Refugio 43 (cómic Penny Arcade)", "cómic oficial", "43"),
    # ---- Refugio 88 (FO4 Vault-Tec Workshop) ----
    "r88_puerta": (W + "c/cd/E3_Fallout4_VaultTecWorkshop_Door.png", "puerta (imagen E3, motor del juego)", "FO4 VW", "88"),
    "r88_sector": (W + "1/10/Vault88-Main-Fallout4.jpg", "sector principal", "FO4 VW", "88"),
    "r88_barstow": (W + "d/dc/FO4VW_Valery_Barstow.png", "supervisora Valery Barstow (necrófaga)", "FO4 VW", "88"),
    "r88_clem": (W + "3/3d/Clem.png", "Clem", "FO4 VW", "88"),
    "r88_powercycle": (W + "1/13/E3_Fallout4_VaultTecWorkshop_Experiment.png", "experimento Power Cycle 1000 (E3)", "FO4 VW", "88"),
    "r88_foropter": ("page:Phoropter", "forópter", "FO4 VW", "88"),
    "r88_tragaperras": ("page:Slot machine", "tragaperras", "FO4 VW", "88"),
    # ---- Refugio 101 (FO3) ----
    "r101_exterior": (W + "d/d1/Vault101.jpg", "exterior: entrada en la roca", "FO3", "101"),
    "r101_atrio": (W + "1/17/Fo3_Atrium_View.png", "atrio", "FO3", "101"),
    "r101_cartel": (W + "1/1c/Vault_101_Thank_you%2C_Over-seer%21.jpg", "cartel «Thank you, Over-seer!»", "FO3", "101"),
    "r101_almodovar": (W + "1/1c/The_Overseer_101_Esc.jpg", "supervisor Alphonse Almodóvar", "FO3", "101"),
    "r101_amata": (W + "6/6b/Amata_TOH.jpg", "Amata", "FO3", "101"),
    "r101_andy": (W + "5/53/Andy_GUF.jpg", "Andy, el Mr. Handy (con la tarta)", "FO3", "101"),
    "r101_jonas": ("page:Jonas Palmer", "Jonas Palmer", "FO3", "101"),
    # ---- Refugio 22 (FNV) ----
    "r22_exterior": (W + "7/73/Vault_22_exterior.jpg", "exterior con flores", "FNV", "22"),
    "r22_atrio": (W + "a/a0/Vault_22_Atrium.jpeg", "atrio invadido por plantas", "FNV", "22"),
    "r22_portador": (W + "a/af/Spore_carrier.png", "portador de esporas", "FNV", "22"),
    "r22_randall": (W + "c/c7/Randall_Clark.jpg", "restos de Randall Clark (Honest Hearts)", "FNV HH", "22"),
    "r22_cartel": (W + "f/fa/The_plants_kill.jpg", "pintada «The plants kill»", "FNV", "22"),
    # ---- Refugio 106 (FO3) ----
    "r106_exterior": (W + "a/a3/Vault_106_exterior.jpg", "exterior (cueva)", "FO3", "106"),
    "r106_atrio": (W + "b/ba/Fo3_Vault_106_LQ_Atrium_Upper_Level.png", "atrio de dormitorios", "FO3", "106"),
    "r106_alucinacion": (W + "0/0f/Vault_106_hallucination.jpg", "alucinación", "FO3", "106"),
    "r106_amata": (W + "8/8b/Vault_106_hallucination_Amata_running.jpg", "alucinación de Amata corriendo", "FO3", "106"),
    "r106_butch": (W + "8/8a/Vault_106_WallyPaulButch_hallucination.jpg", "alucinación de Wally, Paul y Butch", "FO3", "106"),
    "r106_mininuke": (W + "7/72/FO3_Vault_106_mini_nuke.jpg", "mini nuke de la cueva", "FO3", "106"),
    # ---- Refugio 63 (FO76 Skyline Valley) ----
    "r63_puerta": (W + "9/95/F76_Vault_63_Main_Door.png", "puerta reventada", "FO76", "63"),
    "r63_atrio": (W + "0/0c/Vault63_Atrium1.jpeg", "atrio", "FO76", "63"),
    "r63_clima": (W + "d/d9/FO76SV_Vault_63_meteorology_sector_01.png", "sector de meteorología (máquina del clima)", "FO76", "63"),
    "r63_hugo": (W + "f/f7/FO76SV_Hugo_Stolz_Pose.png", "Hugo Stolz", "FO76", "63"),
    "r63_cassidy": (W + "1/1f/FO76SV_Cassidy_Stolz.png", "Cassidy Stolz", "FO76", "63"),
    "r63_lost": (W + "e/ed/Feral_Lost.png", "Lost salvaje", "FO76", "63"),
    # ---- Refugio 81 (FO4) ----
    "r81_puerta": (W + "e/e7/Vault_81door.jpg", "puerta del Refugio 81", "FO4", "81"),
    "r81_secreto": (W + "9/98/Fo4_Vault_81_ext_TV_31.png", "sección secreta", "FO4", "81"),
    "r81_tumbas": (W + "a/a0/Fo4_Vault_81_ext_TV_9.png", "tumbas de la sección secreta", "FO4", "81"),
    "r81_curie": (W + "8/89/Curie.jpg", "Curie (Miss Nanny)", "FO4", "81"),
    "r81_austin": (W + "d/d2/Austin_Engill.png", "Austin Engill", "FO4", "81"),
    "r81_rata_topo": ("page:Mole rat (Fallout 4)", "rata topo", "FO4", "81"),
    # ---- Refugio 108 (FO3) ----
    "r108_entrada": (W + "b/b0/Vault_108_entrance.jpg", "entrada", "FO3", "108"),
    "r108_lab": (W + "6/6b/Vault_108_cloning_lab.jpg", "laboratorio de clonación", "FO3", "108"),
    "r108_gary": (W + "b/b4/Gary_%28clone%29.jpg", "clon de Gary", "FO3", "108"),
    "r108_puerta": (W + "5/5d/FO3_Vault_108_door.jpg", "puerta del Refugio 108", "FO3", "108"),
    "r108_gary_ficha": ("page:Gary (clone)", "Gary (render de la ficha)", "FO3", "108"),
    # ---- Refugio 0 (Fallout Tactics) ----
    "r0_entrada": (W + "3/33/V0_bos0117.jpg", "entrada (cinemática de Tactics)", "Tactics", "0"),
    "r0_calculadora": (W + "a/a0/Calculator_bos0097.jpg", "la Calculadora (cinemática)", "Tactics", "0"),
    "r0_calculadora_juego": (W + "4/41/FoT_Calculator.png", "la Calculadora en el juego", "Tactics", "0"),
    "r0_mapa": (W + "8/81/FoT_Vault_0_map_1.jpg", "mapa del nivel superior", "Tactics", "0"),
    # ---- Refugio 77 (cómic + FO3) ----
    "r77_mono": (W + "5/5f/Vault77Jumpsuit.png", "mono del Refugio 77", "FO3", "77"),
    "r77_sale": (W + "1/1c/Vault77.png", "el hombre de las marionetas sale (cómic)", "cómic oficial", "77"),
    "r77_puerta": (W + "f/f9/Vault77Door.png", "puerta del 77 (cómic)", "cómic oficial", "77"),
    "r77_caja": (W + "4/41/Vault77Crate.png", "caja «PUPPET RATION» (cómic)", "cómic oficial", "77"),
    "r77_vaultboy": (W + "a/a7/77_Vault_Boy_puppet.png", "marioneta de Vault Boy (cómic)", "cómic oficial", "77"),
    "r77_apartamento": (W + "6/6f/Vault77Apartment.png", "interior (cómic)", "cómic oficial", "77"),
    # ---- Refugio 94 (FO76) ----
    "r94_exterior": (W + "c/c6/Vault_94_exterior.png", "exterior", "FO76", "94"),
    "r94_puerta": (W + "1/1c/Vault_94_door.png", "puerta", "FO76", "94"),
    "r94_atrio": (W + "e/ed/F076_Vault_94_Atrium_01.jpeg", "atrio", "FO76", "94"),
    "r94_geck": (W + "9/96/FO76OW_Vault_94_GECK.png", "G.E.C.K. del 94", "FO76", "94"),
    "r94_semillas": (W + "f/ff/F076_Vault_94_Seedbank.jpeg", "banco de semillas", "FO76", "94"),
    # ---- Refugios 68 / 69 (Biblia + cómic) ----
    "r69_vineta": (W + "b/b6/PA_Vault_69.jpg", "viñeta del Refugio 69 (cómic Penny Arcade)", "cómic oficial", "68/69"),
    # ---- Refugio 95 (FO4) ----
    "r95_exterior": (W + "a/a3/Vault95-Fallout4.jpg", "exterior", "FO4", "95"),
    "r95_puerta": (W + "5/55/FO4_Vault_95_door.jpg", "puerta", "FO4", "95"),
    "r95_detox": (W + "d/d2/Vault95-Detox-Fallout4.jpg", "sala de desintoxicación", "FO4", "95"),
    "r95_alijo": (W + "0/03/Vault95-Stash-Fallout4.jpg", "alijo de drogas", "FO4", "95"),
    "r95_cait": (W + "d/d0/Fo4_Cait.jpg", "Cait", "FO4", "95"),
    # ---- Refugio 111 (FO4) ----
    "r111_preguerra": (W + "d/db/Vault_111_pre_war.png", "refugio antes de la guerra", "FO4", "111"),
    "r111_capsulas": (W + "0/05/FO4_V111_Cryopods.png", "cápsulas criogénicas", "FO4", "111"),
    "r111_secuestro": (W + "0/0f/FO4_Kidnapping_Shaun.jpg", "secuestro de Shaun", "FO4", "111"),
    "r111_shaun": (W + "4/44/FO4_Shaun_crib.png", "Shaun bebé en la cuna", "FO4", "111"),
    "r111_kellogg": (W + "d/dc/Conrad_Kellogg_Fallout_4_1.png", "Kellogg", "FO4", "111"),
    "r111_mono": (W + "1/13/Fo4_Vault_111_Jumpsuit.png", "mono del Refugio 111", "FO4", "111"),
    # ---- Refugio 12 (FO1) ----
    "r12_set": (W + "4/40/FO01_NPC_Set_N.png", "Set, cabeza parlante", "FO1", "12"),
    "r12_necropolis": (W + "7/73/Fo1_Necropolis_Watershed.png", "depósito de agua de Necrópolis", "FO1", "12"),
    "r12_chip": (W + "e/e9/Vault_12_water_chip.png", "chip de agua en el Refugio 12", "FO1", "12"),
    "r12_chip_intro": (W + "7/73/Fo1_Intro_Water_chip.png", "chip de agua (intro de FO1)", "FO1", "12"),
    # ---- Refugio 92 (FO3) ----
    "r92_exterior": (W + "8/8b/Vault_92_exterior.jpg", "exterior", "FO3", "92"),
    "r92_estudio": (W + "f/f9/Fo3_Recording_Studio.png", "estudio de grabación", "FO3", "92"),
    "r92_pruebas": (W + "f/f2/Vault_92_sound_testing.jpg", "sala de pruebas de sonido", "FO3", "92"),
    "r92_violin": (W + "4/41/Soil_Stradivarius.png", "violín Soil Stradivarius", "FO3", "92"),
    "r92_malleus": (W + "b/b4/FO3ProfessorMalleus.png", "profesor Malleus", "FO3", "92"),
    "r92_holocinta": (W + "0/0b/Prof_Malleus_audio_log_V92-02.jpg", "holocinta de Malleus V92-02", "FO3", "92"),
    # ---- Refugio 87 (FO3) ----
    "r87_entrada": (W + "7/7f/Vault_87_entrance.jpg", "entrada con barricada", "FO3", "87"),
    "r87_radiacion": (W + "d/d9/Vault_87_peak_radiation.png", "pico de radiación en la entrada", "FO3", "87"),
    "r87_fev": (W + "1/1a/Failed_FEV_experiment_in_Vault_87.jpg", "experimento de FEV fallido", "FO3", "87"),
    "r87_fawkes": (W + "3/3b/Fawkes_cell.jpg", "Fawkes en su celda", "FO3", "87"),
    "r87_centauro": ("page:Centaur (Fallout 3)", "centauro", "FO3", "87"),
    # ---- Refugio 96 (FO76) ----
    "r96_exterior": (W + "5/51/F76_Vault_96_Ext_1.png", "exterior y helipuerto", "FO76", "96"),
    "r96_atrio": (W + "1/12/FO76_V96_Atrium01.jpeg", "atrio helado", "FO76", "96"),
    "r96_crio": (W + "4/4a/FO76_V96_CryoWing02.jpeg", "ala criogénica", "FO76", "96"),
    "r96_camara": (W + "3/3c/FO76_V96_ResearchWingChamber01.jpeg", "cámara de prueba de criaturas", "FO76", "96"),
    "r96_blackburn": (W + "d/d3/FO76SR_Blackburn_smile.png", "Blackburn", "FO76", "96"),
    # ---- Refugio 51 (FO76) ----
    "r51_puerta": (W + "c/c1/Vault51.png", "puerta", "FO76", "51"),
    "r51_zax": (W + "7/76/FO76_Vault_51_ZAX.png", "ZAX 1.3c", "FO76", "51"),
    "r51_atrio": (W + "0/01/Vault51atriumwide.png", "atrio", "FO76", "51"),
    "r51_reuben": (W + "b/b2/FO76_Reuben_Gill.jpg", "Reuben Gill", "FO76", "51"),
    "r51_candidatos": (W + "9/9f/FO76NW-Vault-51-%28candidates%29.jpg", "tablón de candidatos", "FO76", "51"),
    "r51_apuestas": (W + "3/3c/FO76NW_Vault_51_%28betting_machine%29.png", "máquina de apuestas", "FO76", "51"),
    # ---- Refugio 11 (FNV) ----
    "r11_exterior": (W + "7/7d/Vault_11.jpg", "exterior: entrada en la roca", "FNV", "11"),
    "r11_puerta": (W + "0/0b/Vault_11_door.jpg", "puerta del Refugio 11", "FNV", "11"),
    "r11_camara": (W + "e/e1/Vault11_Sacrificial_Chamber.jpg", "cámara del sacrificio", "FNV", "11"),
    "r11_ordenador": (W + "2/27/Vault_11_mainframe_ASR.jpg", "ordenador central de la cámara", "FNV", "11"),
    "r11_cartel1": (W + "2/2a/PosterVault11_01.png", "cartel electoral 01", "FNV", "11"),
    "r11_cartel_kate": (W + "2/2a/PosterVault11_02.png", "cartel «I hate Kate» (Katherine Stone no tiene retrato)", "FNV", "11"),
    "r11_interior": (W + "5/53/Vault_11_Interior.jpeg", "interior", "FNV", "11"),
    # ---- Refugio 75 (FO4) ----
    "r75_entrada": (W + "d/d5/Vault_75_entrance.png", "entrada (Malden Middle School)", "FO4", "75"),
    "r75_atrio": (W + "2/21/Vault75-Atrium-Fallout4.jpg", "atrio", "FO4", "75"),
    "r75_simulacion": (W + "d/d0/Vault75-CombatSimulation2-Fallout4.jpg", "simulación de combate", "FO4", "75"),
    "r75_lab": (W + "d/d7/Vault75-Research-Fallout4.jpg", "laboratorio con cristal en el suelo", "FO4", "75"),
    "r75_esqueleto": (W + "8/89/FO4_Vault_75_skeleton_2.png", "esqueleto esposado en la cocina", "FO4", "75"),
    # ---- Refugio 112 (FO3) ----
    "r112_puerta": (W + "4/44/Vault112.jpg", "puerta del Refugio 112", "FO3", "112"),
    "r112_tumbonas": (W + "b/b3/Vault_112_TQ.jpeg", "sala de tumbonas con el ordenador central", "FO3", "112"),
    "r112_tumbona": (W + "1/14/Tranquility_Lane_in_a_Lounger.jpeg", "tumbona de realidad virtual", "FO3", "112"),
    "r112_braun": (W + "4/48/FO3BraunHeadshotEyesOpen.jpg", "Dr. Braun en su tumbona", "FO3", "112"),
    "r112_betty": (W + "d/d5/Betty_TL.jpg", "Betty (Braun dentro de la simulación)", "FO3", "112"),
    "r112_braun_conectado": (W + "1/12/Braun_in_the_sim.jpg", "Braun conectado en su tumbona", "FO3", "112"),
    "r112_james": (W + "e/e8/Dad_in_the_Sim.jpg", "James (el padre) conectado en su tumbona", "FO3", "112"),
    "r112_mabel": (W + "b/b6/Mabel_Henderson.jpg", "Mabel Henderson", "FO3", "112"),
    "r112_barrio": (W + "f/f8/TL_aerial_view.jpg", "Tranquility Lane vista aérea", "FO3", "112"),
    "r112_invasion": (W + "7/73/Fo3_Simulated_Chinese_invasion.png", "invasión china simulada", "FO3", "112"),
    # ---- Genéricos ----
    "gen_geck": (W + "6/63/GECK_FO3.png", "G.E.C.K.", "FO3", "general"),
    "gen_vaultboy": (W + "c/c0/VaultBoyFO3.png", "Vault Boy (pulgar arriba)", "FO3", "general"),
    "gen_puerta": (W + "7/78/FO3_Vault_door_101_new.jpg", "puerta de engranaje de refugio", "FO3", "general"),
    "gen_pipboy": ("page:Pip-Boy 3000 Mark IV", "Pip-Boy 3000 Mark IV", "FO4", "general"),
    "gen_mono": (W + "8/88/Vault_101_Back.png", "mono de refugio (101, espalda)", "FO3", "general"),
    "gen_logo": (W + "0/06/VaultTecLogo.png", "logo de Vault-Tec", "general", "general"),
}
# personajes/objetos con fondo limpio: se intenta el recorte (se valida a mano en la hoja)
RECORTAR = ["r21_house_pantalla", "r118_robocerebro", "r88_barstow", "r88_clem", "r88_foropter", "r88_tragaperras",
            "r22_portador", "r63_hugo", "r81_rata_topo", "r108_gary_ficha", "r77_mono",  
            "r92_violin", "r92_malleus", "r87_centauro", "r111_mono", "gen_geck", "gen_vaultboy", "gen_pipboy",
            "gen_mono", "r55_holocinta", "r96_blackburn", 
            "r81_austin", "r81_curie", "r95_cait", "r21_doc_mitchell", "r94_geck"]
UA = {"User-Agent": "Mozilla/5.0"}


def url_de(v):
    if v.startswith("file:"):
        t = urllib.parse.quote("File:" + v[5:])
        q = f"https://fallout.fandom.com/api.php?action=query&prop=imageinfo&iiprop=url&format=json&titles={t}"
        d = json.load(urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=30))
        for p in d["query"]["pages"].values():
            return p["imageinfo"][0]["url"]
    if not v.startswith("page:"):
        return v
    t = urllib.parse.quote(v[5:])
    q = f"https://fallout.fandom.com/api.php?action=query&prop=pageimages&piprop=original&redirects=1&format=json&titles={t}"
    d = json.load(urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=30))
    for p in d["query"]["pages"].values():
        return p.get("original", {}).get("source")


def bajar():
    fuentes = {}
    fp = OUT / "_fuentes.txt"
    if fp.exists():
        for ln in fp.read_text(encoding="utf-8").splitlines():
            if " | " in ln:
                s, u = ln.split(" | ", 1)
                fuentes[s] = u
    for slug, (v, *_r) in P.items():
        dst = OUT / f"{slug}.png"
        if dst.exists() and "--todo" not in sys.argv:
            continue
        try:
            u = url_de(v)
            raw = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read()
            im = Image.open(io.BytesIO(raw)).convert("RGBA")
            im.thumbnail((1000, 1000), Image.LANCZOS)
            im.save(dst)
            fuentes[slug] = u
            print("ok", slug, im.size)
        except Exception as e:
            print("FALLO", slug, e)
    fp.write_text("\n".join(f"{s} | {fuentes[s]}" for s in P if s in fuentes) + "\n", encoding="utf-8")


def recortar():
    from rembg import remove
    for slug in RECORTAR:
        src = OUT / f"{slug}.png"
        dst = OUT / f"{slug}_rec.png"
        if not src.exists() or (dst.exists() and "--todo" not in sys.argv):
            continue
        im = remove(Image.open(src).convert("RGBA"))
        bb = im.getchannel("A").point(lambda a: 255 if a > 20 else 0).getbbox()
        if bb:
            im = im.crop(bb)
        im.save(dst)
        print("rec", slug, im.size)


def hoja():
    """previews/pegatinas_check_N.jpg: miniatura + slug + qué es + juego (20 por hoja). Los _rec sobre damero."""
    from PIL import ImageDraw, ImageFont
    try:
        f1 = ImageFont.truetype("arialbd.ttf", 17)
        f2 = ImageFont.truetype("arial.ttf", 14)
    except OSError:
        f1 = f2 = ImageFont.load_default()
    items = []
    for slug, (v, que, juego, ref) in P.items():
        for suf in ("", "_rec"):
            fp = OUT / f"{slug}{suf}.png"
            if fp.exists():
                items.append((fp, slug + suf, que, f"{juego} · R{ref}"))
    C, F, TW, TH = 5, 4, 340, 230
    prev = AQUI / "previews"
    for n in range(0, len(items), C * F):
        S = Image.new("RGB", (C * TW, F * (TH + 50)), (40, 40, 40))
        d = ImageDraw.Draw(S)
        for i, (fp, slug, que, jr) in enumerate(items[n:n + C * F]):
            x, y = (i % C) * TW, (i // C) * (TH + 50)
            im = Image.open(fp).convert("RGBA")
            im.thumbnail((TW - 10, TH - 6))
            if slug.endswith("_rec"):
                bg = Image.new("RGB", im.size, (255, 0, 255))
                bg.paste(im, (0, 0), im)
                im = bg.convert("RGBA")
            S.paste(im, (x + (TW - im.width) // 2, y + 3), im)
            d.text((x + 4, y + TH + 2), slug, fill=(255, 230, 0), font=f1)
            d.text((x + 4, y + TH + 24), f"{que[:38]} | {jr}", fill=(220, 220, 220), font=f2)
        out = prev / f"pegatinas_check_{n // (C * F) + 1}.jpg"
        S.save(out, quality=88)
        print(out)


if __name__ == "__main__":
    if "--hoja" not in sys.argv or "--bajar" in sys.argv:
        bajar()
    if "--rec" in sys.argv:
        recortar()
    if "--hoja" in sys.argv:
        hoja()
