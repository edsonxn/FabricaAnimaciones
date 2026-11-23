# -*- coding: utf-8 -*-
"""Tarjetas de comentarios de «Los 25 ERRORES al llegar al nivel 60 en WoW Forever» (22-nov-2026).
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
    "ia2025": ("UgwCpRYjHXvV7q", "gracias1", "gracias"),
    "torrikus": ("UgwZUKSlIX0G0U", "gracias1", "gracias"),
    "andresbece": ("Ugx2Ok2UrrbmK7", "gracias1", "gracias"),
    "teniente_dandadan": ("Ugy94JCmN25DRd", "gracias2", "gracias"),
    "zargues": ("Ugz3H92TNyfHda", "gracias2", "gracias"),
    "alejandro_quevedo": ("UgwvWM26naEQ54", "burla0", "burla"),
    "jclothus": ("UgyEdMM72NU_Rk", "burla1", "burla"),
    "rafael_veliz": ("UgzE0AsihdnWag", "burla2", "burla"),
    "gespexp": ("UgwomMA4pr1XaV", "correc", "corrección"),
    "aztero": ("UgxUxdSofA9jxe", "correc", "corrección"),
    "sastakai": ("Ugy7L_WmgIGtiC", "correc", "corrección"),
}

SALTOS = {"ia2025": "SE VE QUE LE PONES MUCHO CARIÑO\nY EMPEÑO A LOS VIDEOS.\nNUEVO SEGUIDOR. SALUDOS."}


def main():
    cs = json.load(open(os.path.join(RAIZ, "canales", "comentarios", "cronicas_warcraft.json"), encoding="utf-8"))["comentarios"]
    filas = ["# Tarjetas de comentarios (22-nov-2026) · archivo → autor → id completo → escena del guion → tipo → fecha · texto",
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
    open(os.path.join(AQUI, "pegatinas", "_comentarios.txt"), "w", encoding="utf-8").write("\n".join(filas) + "\n")


if __name__ == "__main__":
    main()
