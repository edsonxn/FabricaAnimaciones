"""2-nov: aplica las hojas de Flow regeneradas con la foto real como ingrediente (aprobadas por el usuario).

Respalda hojas/<nom>_a|b.jpg y piezas/<nom>/ en `_respaldo_2nov/`, copia la variante elegida de hojas_reales/ como
hojas/<nom>_a.jpg (recortar usa la _a) y quita la fila de nombres impresos de la hoja de Magni.
Isillien JOVEN entra como hoja nueva h31_isillien_joven (código IJ): la vieja h14 sigue para el Gran Inquisidor.
Uso: python _aplicar_hojas_reales.py   (luego `python nucleo/pegaflow.py recortar gaia_crematoria <hojas>`)
"""
import os
import shutil

from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
ELEGIDAS = {"h01_alexandros_hoja": "b", "h03_renault_hoja": "b", "h08_tirion_joven": "b", "h11_taelan_hoja": "a",
            "h13_eitrigg_hoja": "b", "h15_villanos_hoja": "a", "h16_consejo_hoja": "b", "h17_magni_hoja": "b"}
NUEVAS = {"h31_isillien_joven": ("h14_isillien_hoja", "b")}      # hoja nueva ← (hoja de hojas_reales, variante)
RESP_H = os.path.join(D, "hojas", "_respaldo_2nov")
RESP_P = os.path.join(D, "piezas", "_respaldo", "2nov")


def _real(nom, var):
    f = os.path.join(D, "hojas_reales", f"{nom}_{var}.jpg")
    return f if os.path.exists(f) else os.path.join(D, "hojas_reales", f"{nom[:-5]}_{var}.jpg")


def _sin_texto(f):
    """Magni: Flow imprimió los nombres bajo los pies → blanco desde el hueco entre pies y texto."""
    im = Image.open(f).convert("RGB")
    w, h = im.size
    y0 = int(0.825 * h)
    im.paste((255, 255, 255), (0, y0, w, h))
    im.save(f, quality=95)


def main():
    os.makedirs(RESP_H, exist_ok=True)
    os.makedirs(RESP_P, exist_ok=True)
    for nom, var in ELEGIDAS.items():
        for s in ("a", "b"):
            f = os.path.join(D, "hojas", f"{nom}_{s}.jpg")
            if os.path.exists(f) and not os.path.exists(os.path.join(RESP_H, os.path.basename(f))):
                shutil.copy2(f, RESP_H)
        p = os.path.join(D, "piezas", nom)
        if os.path.isdir(p) and not os.path.isdir(os.path.join(RESP_P, nom)):
            shutil.copytree(p, os.path.join(RESP_P, nom))
        dst = os.path.join(D, "hojas", f"{nom}_a.jpg")
        shutil.copy2(_real(nom, var), dst)
        if nom == "h17_magni_hoja":
            _sin_texto(dst)
        print("ok", nom, var)
    for nom, (src, var) in NUEVAS.items():
        shutil.copy2(_real(src, var), os.path.join(D, "hojas", f"{nom}_a.jpg"))
        print("nueva", nom, "<-", src, var)


if __name__ == "__main__":
    main()
