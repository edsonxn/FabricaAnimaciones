# -*- coding: utf-8 -*-
"""Baja SFX REALES de World of Warcraft desde Wowhead (`/sounds/name:<busca>` trae en la página el JSON con files[].url) a
sfx_juego/<alias>.ogg. Uso (desde la carpeta del video): python _bajar_sonidos.py   (solo baja los que faltan).
Copiado de wow_darrowshire y ampliado para la saga de la Crematoria (29-oct-2026). Un 3.er elemento n = baja las n primeras
variantes del sonido como <alias>_01.ogg … <alias>_NN.ogg. Al final escribe sfx_juego/_lista.txt (alias, duración, qué es)."""
import json
import os
import re
import subprocess
import urllib.parse
import urllib.request

# alias: (búsqueda, nombre exacto del sonido en Wowhead[, variantes], "qué es")
SONIDOS = {
    # --- interfaz de misiones
    "mision_acepta": ("QUESTADDED", "QUESTADDED", 1, "interfaz: misión aceptada"),
    "mision_completa": ("QUESTCOMPLETED", "QUESTCOMPLETED", 1, "interfaz: misión completada"),
    "pagina": ("pageturn", "igSpellBokPageTurn", 1, "interfaz: pasar página del libro"),
    # --- la Luz (paladín)
    "luz_sagrada": ("holy", "FX_Holy_Magic_Cast_Large_01", 1, "Luz sagrada: lanzamiento grande"),
    "luz_impacto": ("holy", "FX_Holy_Magic_Impact_Large_01", 1, "Luz sagrada: impacto grande"),
    "luz_clasica": ("holy", "HolyCast", 1, "Luz sagrada: lanzamiento (sonido clásico)"),
    "luz_impacto_clasico": ("holy", "Holy_ImpactDD_Uber_Base", 1, "Luz sagrada: impacto fuerte (clásico)"),
    "luz_sanadora": ("holylight", "HolyLight_Low_Head", 1, "Luz Sagrada (curación de paladín, clásico)"),
    "imposicion_manos": ("layonhands", "LayOnHands_Low_Chest", 1, "Imposición de manos (clásico)"),
    "castigo_sagrado": ("smite", "Spell_PR_Revamp_Smite_Impact", 1, "Castigo sagrado: impacto"),
    "exorcismo": ("exorcism", "Exorcism", 1, "Exorcismo (paladín, clásico)"),
    "consagracion": ("consecration", "SPELL_PA_Consecration_Revamp", 1, "Consagración: suelo sagrado"),
    "escudo_divino": ("divine", "DivineShield", 1, "Escudo divino (burbuja)"),
    "resurreccion": ("resurrect", "Resurrection", 1, "resurrección"),
    # --- sombra, caballero de la muerte y la Plaga
    "sombra": ("shadowbolt", "Spell_6.2HellfireRaid_ShadowBolt_Impact", 1, "sombra: impacto"),
    "sombra_lanzar": ("shadow bolt", "Spell_WL_Revamp_Shadow_Bolt_Cast_01", 1, "sombra: lanzamiento de descarga"),
    "dk_hechizo": ("deathcoil", "Spell_DK_DeathCoil_Cast01", 1, "caballero de la muerte: Espiral de la muerte (lanzar)"),
    "dk_impacto": ("deathcoil", "Spell_DK_Deathcoil_Impact", 1, "caballero de la muerte: Espiral de la muerte (impacto)"),
    "dk_runas": ("runeforge", "SC_RuneForge_01", 1, "caballero de la muerte: forja de runas de Acherus"),
    "dk_golpe_escarcha": ("death knight", "Deathknight_Froststrike1", 1, "caballero de la muerte: Golpe de Escarcha"),
    "dk_presencia_profana": ("unholy", "Deathknight_UnholyPresence", 1, "caballero de la muerte: presencia profana"),
    "dk_atraccion": ("deathgrip", "DK_DeathGrip_Impact", 1, "caballero de la muerte: Atracción letal"),
    "dk_portal": ("deathgate", "Deathknight_Deathgate", 1, "caballero de la muerte: Puerta de la muerte (portal a Acherus)"),
    "destrero_muerte": ("warhorse", "DeathKnight_SummonWarHorse_Impact_Base", 1, "invocar destrero de la muerte (caballo esquelético)"),
    "caballo_no_muerto": ("horse", "UndeadHorseAggro", 1, "caballo no-muerto: relincho"),
    "caballo_no_muerto_invoca": ("horse", "HorseUndeadSummon", 1, "caballo no-muerto: invocación"),
    "necrofago": ("ghoul", "GhoulAggro", 1, "necrófago: aggro (clásico)"),
    "necrofago2": ("ghoul", "NorthrendGhoulAggro2", 1, "necrófago de Rasganorte: aggro"),
    "necrofago_muere": ("ghoul", "GhoulDeath", 1, "necrófago: muerte"),
    "esqueleto": ("skeleton", "MON_OrcSkeleton_Aggro", 1, "esqueleto: aggro"),
    "esqueleto_muere": ("skeleton", "MON_OrcSkeleton_Death", 1, "esqueleto: muerte (huesos)"),
    "abominacion": ("abomination", "MON_AbominationPvG_Aggro", 1, "abominación: aggro"),
    "abominacion_golpe": ("abomination", "MON_AbominationPvG_Attack", 1, "abominación: ataque"),
    "gargola": ("gargoyle", "Spell_DK_SummonGargoyle_GargoyleStrike_Precast", 1, "gárgola de la Plaga: chillido/ataque"),
    # --- escarcha, Kel'Thuzad y el Rey Exánime (hechizos, no voces)
    "escarcha_nova": ("frost nova", "FrostNova", 1, "Nova de Escarcha (clásico): hielo que estalla"),
    "escarcha_lanzar": ("frostbolt", "SPELL_MA_Revamp_Frostbolt_Cast", 1, "Descarga de Escarcha: lanzar"),
    "escarcha_impacto": ("frostbolt", "SPELL_MA_Revamp_FrostBolt_Impact_01", 1, "Descarga de Escarcha: impacto"),
    "hielo_rompe": ("ice", "Spell_Frostfire_Unthaw_Shatter_Ice_cast", 1, "hielo que se rompe"),
    "hielo_cruje": ("ice", "FX_ICE_Cracking_Pond_01", 1, "hielo que cruje (lago helado)"),
    "agonia_rota": ("frostmourne", "FrostMourne_Shatters", 1, "Agonía de Escarcha se hace añicos (ICC)"),
    "agonia_almas": ("frostmourne", "Emitter_IceCrown_FrostMourne_Souls_01", 1, "almas dentro de Agonía de Escarcha (bucle)"),
    # --- portales y campanas
    "portal": ("portal", "GO_7AF_Mage_Portal_Spawn_01", 1, "portal que se abre"),
    "portal_bucle": ("portal", "FX_INSTANCENEWPORTAL_BLUE_ARCANE_LOOP", 1, "portal de estancia (bucle)"),
    "teletransporte": ("teleport", "Teleport", 1, "teletransporte (clásico)"),
    "campana": ("belltoll", "BellTollAlliance", 1, "campana de la Alianza dando la hora (clásico)"),
    "campana_iglesia": ("church", "FX_GO_Boralus_Church_Bell_V2_01", 1, "campana de iglesia"),
    "campanas_lejanas": ("church", "FX_Revendreth_Boralus_Church_Bells_Distant_Stereo_01", 1, "campanas de catedral a lo lejos"),
    "organo_lejano": ("organ", "MUS_80_Drustvar_WaycrestManor_DistantOrgan", 1, "MÚSICA: órgano lejano (mansión Waycrest; mp3 convertido a ogg)"),
    # --- forja de Forjaz
    "yunque": ("blacksmith", "BlackSmithing", 1, "herrería: martillo sobre yunque"),
    "forja_martillo": ("forge", "DalaranForgeArmsHammer7", 1, "martillazos de forja"),
    "fuelle_forjaz": ("forge", "GO_IronforgeBellow_Down", 1, "fuelle de la Gran Fundición de Forjaz"),
    "gran_yunque_fuego": ("anvil", "Emitter_81_DwarfHeritage_Ironforge_GreatAnvil_Fire_Loop", 1, "fuego del Gran Yunque de Forjaz (bucle)"),
    # --- fuego
    "fuego_grande": ("fire", "FX_Fire_Heavy_Loop_01", 1, "fuego grande (bucle)"),
    "fuego_magico": ("fire", "FX_Fire_Magic_Loop_Large_01", 1, "fuego mágico grande (bucle)"),
    "fuego_vil": ("felfire", "FelFireImpact_01", 1, "fuego vil verde: impacto"),
    "fuego_vil_bucle": ("felfire", "SPELL_MKOrderHall_FelFire_Loop", 1, "fuego vil verde (bucle)"),
    "brasero_escarlata": ("scarlet", "ScarletO_Brazier_Fire", 1, "brasero de la Cruzada Escarlata"),
    # --- combate
    "espada_escudo": ("shield", "1h_Sword_CritHit_Shield_Metal_01", 1, "espada contra escudo de metal"),
    "espada_carne": ("flesh", "m2hSwordHitFleshCrit", 1, "espadón que hiere (clásico)"),
    "espada_atraviesa": ("flesh", "2h_Sword_CritHit_Flesh_01", 1, "espadón que atraviesa"),
    "grito_guerra": ("battleshout", "HumanMaleBattleshout", 1, "grito de batalla de humano"),
    "batalla": ("walla", "FX_Walla_Battle_OutsidePOV_Loop_01", 1, "batalla y multitud a lo lejos (bucle)"),
    "victoria_alianza": ("walla", "FX_Walla_Alliance_Battle_Victory", 1, "multitud de la Alianza celebra la victoria"),
    "cascos_nieve": ("footstepshorse", "mFootstepsHorseSnow01", 1, "cascos de caballo sobre nieve"),
    # --- clima y naturaleza
    "lluvia": ("rain", "RainHeavyLoop", 1, "lluvia fuerte (bucle)"),
    "lluvia_ligera": ("rain", "RainLightLoop", 1, "lluvia ligera (bucle)"),
    "trueno": ("weather", "FX_Weather_Thunderstorm_Distant_Thunder_Periodic_05", 1, "trueno lejano"),
    "tormenta": ("weather", "AMB_Weather_Thunderstorm", 1, "tormenta (bucle)"),
    "viento": ("wind", "10.0_Magic_Wind_Howling_Loop_01", 1, "viento que aúlla (bucle)"),
    "ventisca": ("AMB_", "AMB_Weather_Blizzard", 1, "ventisca (bucle, Corona de Hielo)"),
    "rio": ("river", "RiverSlowA", 1, "río lento (Thondroril)"),
    "susurros": ("whisper", "11.0_AMB_Azj-Kahet_Flavor_OldGod_Whispers_01", 1, "susurros oscuros"),
    "susurros_muerte": ("whisper", "FX_Death_Whispers_10", 1, "susurros de muerte"),
    "latido": ("heartbeat", "FX_90_Heartbeat_Slow_02", 1, "latido lento"),
    "crematoria_susurros": ("ashbringer", "Ashbringer Random (01-10)", 10, "susurros de la Crematoria corrupta (VOZ en inglés, frases del objeto)"),
    # --- ambientes de zona
    "amb_peste_dia": ("plaguelands", "PlagueLandsDay", 1, "ambiente: Tierras de la Peste de día"),
    "amb_peste_noche": ("plaguelands", "PlagueLandsNight", 1, "ambiente: Tierras de la Peste de noche"),
    "amb_bosque_apestado": ("AMB_", "AMB_ForestPlagued_Day03", 1, "ambiente: bosque apestado"),
    "amb_tirisfal": ("evilforest", "DayEvilForest01", 1, "MÚSICA de zona clásica «Evil Forest» (Tirisfal/Bosque del Ocaso; mp3 convertido a ogg)"),
    "amb_naxx_caballeros": ("naxxramas", "NaxxramasDeathknightWing", 1, "ambiente: Naxxramas, ala de los caballeros de la muerte (Cuatro Jinetes)"),
    "amb_naxx_entrada": ("naxxramas", "NaxxramasEntrance", 1, "ambiente: Naxxramas, entrada"),
    "amb_forjaz": ("ironforge", "IronForge", 1, "ambiente: Forjaz"),
    "amb_gran_fundicion": ("ironforge", "IronForgeTheGreatForge", 1, "ambiente: la Gran Fundición de Forjaz"),
    "amb_corona_hielo": ("icecrown", "IceCrownGlacier", 1, "ambiente: glaciar de Corona de Hielo"),
}

_cache = {}


def pagina(q):
    if q not in _cache:
        req = urllib.request.Request("https://www.wowhead.com/sounds/name:" + urllib.parse.quote(q),
                                     headers={"User-Agent": "Mozilla/5.0"})
        _cache[q] = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
    return _cache[q]


def urls(q, nombre):
    """URLs (.ogg/.mp3) del sonido con ese nombre exacto (la 1.ª entrada que coincida)."""
    for m in re.finditer(r'\{"id":\d+,"type":\d+,"name":"([^"]+)","popularity":\d+,"files":\[(.*?)\]\}', pagina(q), re.S):
        if json.loads('"' + m.group(1) + '"') == nombre:
            return [u.replace("\\/", "/") for u in re.findall(r'"url":"([^"]+)"', m.group(2))]
    return []


def duracion(f):
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                           capture_output=True, text=True, timeout=30)
        return float(r.stdout.strip())
    except Exception:
        return 0.0


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs("sfx_juego", exist_ok=True)
    faltan = []
    for alias, (q, nombre, n, _) in SONIDOS.items():
        dsts = [f"sfx_juego/{alias}.ogg"] if n == 1 else [f"sfx_juego/{alias}_{k:02d}.ogg" for k in range(1, n + 1)]
        if all(os.path.exists(d) for d in dsts):
            continue
        us = urls(q, nombre)
        if not us:
            print("NO", alias, nombre)
            faltan.append(alias)
            continue
        for dst, url in zip(dsts, us):
            if not os.path.exists(dst):
                urllib.request.urlretrieve(url, dst)
                print(alias, os.path.getsize(dst), url.rsplit("/", 1)[-1])
    # lista con duración (ffprobe) de todo lo que hay
    filas = []
    for alias, (q, nombre, n, que) in SONIDOS.items():
        fs = [f"{alias}.ogg"] if n == 1 else [f"{alias}_{k:02d}.ogg" for k in range(1, n + 1)]
        for f in fs:
            p = os.path.join("sfx_juego", f)
            if os.path.exists(p):
                d = duracion(p)
                filas.append(f"{f[:-4]:<26} {d:6.2f} s  {que}  [{nombre}]" + ("  ⚠ VACÍO/ILEGIBLE" if d <= 0 else ""))
    with open("sfx_juego/_lista.txt", "w", encoding="utf-8") as fh:
        fh.write("SFX reales de World of Warcraft (Wowhead, wow.zamimg.com/sound-ids). Bajados con _bajar_sonidos.py.\n")
        fh.write("alias                      duración  qué es  [nombre en Wowhead]\n")
        fh.write("\n".join(filas) + "\n")
        if faltan:
            fh.write("\nNO ENCONTRADOS: " + ", ".join(faltan) + "\n")
    print(len(filas), "archivos;", "faltan:", faltan)
