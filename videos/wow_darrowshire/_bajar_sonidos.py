# -*- coding: utf-8 -*-
"""Baja SFX REALES de World of Warcraft desde Wowhead (`/sounds/name:<busca>` trae en la página el JSON con files[].url) a
sfx_juego/<alias>.ogg. Uso (desde la carpeta del video): python _bajar_sonidos.py   (solo baja los que faltan)."""
import os
import re
import urllib.request

# alias: (búsqueda, nombre exacto del sonido en Wowhead)
SONIDOS = {
    "luz_sagrada": ("holy", "FX_Holy_Magic_Cast_Large_01"),
    "luz_impacto": ("holy", "FX_Holy_Magic_Impact_Large_01"),
    "dk_hechizo": ("deathcoil", "Spell_DK_DeathCoil_Cast01"),
    "dk_impacto": ("deathcoil", "Spell_DK_Deathcoil_Impact"),
    "reloj_arena": ("hourglass", "GO_FOAHourglass_Close"),
    "cofre": ("chest", "GO_6IH_IRONHORDE_CHEST01_OPEN"),
    "latido_juego": ("heartbeat", "FX_90_Heartbeat_Slow_02"),
    "susurros": ("whisper", "11.0_AMB_Azj-Kahet_Flavor_OldGod_Whispers_01"),
    "sombra": ("shadowbolt", "Spell_6.2HellfireRaid_ShadowBolt_Impact"),
    "pagina": ("pageturn", "igSpellBokPageTurn"),
    "resurreccion": ("resurrect", "Resurrection"),
    "mundo_espiritus": ("spirithealer", "SpiritHealerLoop"),
}


def pagina(q):
    req = urllib.request.Request(f"https://www.wowhead.com/sounds/name:{q}", headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")


if __name__ == "__main__":
    os.makedirs("sfx_juego", exist_ok=True)
    cache = {}
    for alias, (q, nombre) in SONIDOS.items():
        dst = f"sfx_juego/{alias}.ogg"
        if os.path.exists(dst):
            continue
        if q not in cache:
            cache[q] = pagina(q)
        m = re.search(r'"name":"' + re.escape(nombre) + r'".*?"url":"(https:\\/\\/wow\.zamimg\.com[^"]+)"', cache[q], re.S)
        if not m:
            print("NO", alias, nombre)
            continue
        url = m.group(1).replace("\\/", "/")
        urllib.request.urlretrieve(url, dst)
        print(alias, os.path.getsize(dst), url.rsplit("/", 1)[-1])
