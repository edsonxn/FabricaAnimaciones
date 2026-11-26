# -*- coding: utf-8 -*-
"""Tarjetas de comentarios de «La RUTA de PROFESIONES del 1 al 300 en WoW Forever» (25-nov-2026).
Datos REALES de canales/comentarios/cronicas_warcraft.json (autor, texto, avatar, fecha, me gusta) dibujados con
nucleo/comentarios.tarjeta (la misma de `fab.py ... comentario`). Nombre = com_<autor_corto>.png (encargo del 22-nov);
la lista archivo → autor → id → escena queda en pegatinas/_comentarios.txt.
OJO: el control «ningún comentario dos veces» de comentarios.pegatina() busca com_<id>.png; aquí el id va en _comentarios.txt.
    python _com_tarjetas.py"""
import datetime as dt
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "nucleo"))
import comentarios as C  # noqa: E402

# corto: (prefijo del id de YouTube, escena del guion, tipo)
LISTA = {
    "jesus_izquierdo": ("UgwTWxWEaiIybLp", "gracias1", "gracias"),
    "oscar_anv": ("UgwJAeIjUJcoaQ0", "gracias1", "gracias"),
    "steven": ("Ugwl80s3Ezg4AXR", "gracias1", "gracias"),
    "baron_rata": ("UgzbEMkWklafqFG", "gracias2", "gracias"),
    "julsikakku": ("UgxpNvAExPzF9ew", "gracias2", "gracias (minero y herrero)"),
    "soyoyos": ("UgypokiddmmmYmw", "burla0", "burla"),
    "crisisx94": ("UgyPYj291d_Qi_5", "burla1", "burla"),
    "goca912": ("UgznH1uJzF2Xkbk", "burla2", "burla"),
}

SALTOS = {"julsikakku": "… estoy de chill poco a poco 2 3 horas al dia .. 25 en 5 dias con mineria 145 i herreria 120 .. a mi ritmo ."}   # tramo final del MISMO comentario (lo de las profesiones)


def main():
    cs = json.load(open(os.path.join(RAIZ, "canales", "comentarios", "cronicas_warcraft.json"), encoding="utf-8"))["comentarios"]
    filas = ["# Tarjetas de comentarios (25-nov-2026) · archivo → autor → id completo → escena del guion → tipo → fecha · texto",
             "# en efectos.py: com(<ancla>, \"<corto>\")  (el helper añade «com_»)"]
    for corto, (pref, escena, tipo) in LISTA.items():
        c = next(x for x in cs if x["id"].startswith(pref))
        dias = (dt.date.today() - dt.date.fromisoformat(c["fecha"])).days
        assert dias <= C.MAX_DIAS, (corto, dias)
        if corto in SALTOS:   # MAYÚSCULAS: 44 caracteres por línea se salen de la tarjeta → saltos a mano (mismo texto)
            c = dict(c, texto=SALTOS[corto])
        sal = C.tarjeta(c, os.path.join(AQUI, "pegatinas", f"com_{corto}.png"))
        filas.append(f"com_{corto}.png → {c['autor']} → {c['id']} → {escena} → {tipo} → {c['fecha']} ({c['likes']} me gusta) · "
                     + c["texto"].replace("\n", " ")[:160])
        print(sal)
        import shutil; shutil.copy(sal, os.path.join(AQUI, "pegatinas", f"com_{c['id']}.png"))   # control de repetidos
    open(os.path.join(AQUI, "pegatinas", "_comentarios.txt"), "w", encoding="utf-8").write("\n".join(filas) + "\n")


if __name__ == "__main__":
    main()
