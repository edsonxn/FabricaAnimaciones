# -*- coding: utf-8 -*-
"""Grabaciones REALES del Robotaller (/v2/vivo, edificio) para euphoria_robots, con la API tapada (robotaller.grabar_real).
Las situaciones se fuerzan con Trapo.prueba / Peligros.prueba (motor c99deb7). Los enemigos-pegatina salen de las piezas de un
video PERMITIDO (PIEZAS_DE, Cronopapel), nunca de Warcraft/Tamriel/Runa/Gaia; además se vacían comentarios, noticias y trofeos.
  python capturas.py <nombre> [...]      graba capturas/<nombre>.mp4      ·  python capturas.py lista
Revisar CADA grabación cuadro a cuadro (hoja) antes de usarla."""
import json
import os
import sys
import urllib.request

sys.path.insert(0, "../../nucleo")
import robotaller as R  # noqa: E402

PIEZAS_DE = "historia_jalisco"
_PIEZAS = json.load(urllib.request.urlopen(f"http://127.0.0.1:8765/api/v2/vivo/mundo?video={PIEZAS_DE}"))["piezas"]
_orig = R._sin_catalogo


def _sin_catalogo(u, datos):
    datos = _orig(u, datos)
    if "/api/v2/vivo/mundo" in u and isinstance(datos, dict):
        datos.update(piezas=_PIEZAS, comentarios=[], noticias=[], trofeos=[])
    return datos


R._sin_catalogo = _sin_catalogo

# preparación: sin director, cámara que sigue, sin peligros al azar ni tumbos al azar (solo los que pedimos)
PREP = ("Taller.ponDir(false);Taller.Cam.sigue=true;Peligros.cada(600000);Trapo.cada(600000,700000);"
        "dispatchEvent(new Event('resize'));")


def fija():
    return "(()=>{const C=Taller.Cam;if(C.tx!=null){C.x=C.tx;C.y=C.ty;C.z=C.tz;}})()"


def prueba(t, que, quien="Peligros"):
    return [dict(t=t, js=f"{quien}.prueba({json.dumps(que)})"), dict(t=t + 0.15, js=fija())]


TOMAS = {
    "prueba": dict(dur=9, acciones=[dict(t=2.5, js=PREP), *prueba(4, "empujon")]),
    "caida": dict(dur=16, acciones=[dict(t=2.5, js=PREP + "Trapo.euforia();"), *prueba(9, "empujon")]),
    "verlet": dict(dur=14, acciones=[dict(t=2.5, js=PREP), *prueba(4, "desmayo", "Trapo"), *prueba(9, "resbalon", "Trapo")]),
    "musculos": dict(dur=14, acciones=[dict(t=2.5, js=PREP), *prueba(4, "tropiezo", "Trapo"), *prueba(9, "ayuda", "Trapo")]),
    "equilibrio": dict(dur=16, acciones=[dict(t=2.5, js=PREP), *prueba(4, "tambalea", "Trapo"), *prueba(10, "tambalea", "Trapo")]),
    "agarre": dict(dur=14, acciones=[dict(t=2.5, js=PREP), *prueba(4, "cadena", "Trapo"), *prueba(9, "mueble")]),
    "mundo": dict(dur=16, acciones=[dict(t=2.5, js=PREP), *prueba(4, "mueble"), *prueba(10, "trampa")]),
    "trampa": dict(dur=14, acciones=[dict(t=2.5, js=PREP), *prueba(4, "trampa")]),
    "enemigo": dict(dur=16, acciones=[dict(t=2.5, js=PREP), *prueba(4, "enemigo")]),
    "puente": dict(dur=12, acciones=[dict(t=2.5, js=PREP), *prueba(4, "puente")]),
    "choque": dict(dur=12, acciones=[dict(t=2.5, js=PREP + "Taller.verTodo&&Taller.verTodo(true);"), *prueba(4, "choque", "Trapo")]),
}

if __name__ == "__main__":
    if sys.argv[1:] == ["lista"] or not sys.argv[1:]:
        print(" ".join(TOMAS))
        sys.exit()
    for n in sys.argv[1:]:
        t = TOMAS[n]
        R.grabar_real(f"capturas/{n}.mp4", "/v2/vivo", t["dur"], t["acciones"], fps=24, w=t.get("w", 1080), h=t.get("h", 1080), escala=1.0, css=R.CSS)
        print("grabada", n, flush=True)
