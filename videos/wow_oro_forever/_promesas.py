# -*- coding: utf-8 -*-
"""PROMESAS VISUALES (regla 5-nov-2026): cuadro real (clip + capa de efectos) en el segundo en que la voz dice cada frase.
previews/promesas_NN.jpg (12 por hoja). Las frases y lo que debería verse: PROMESAS de abajo (copiadas a promesas.md).
    python _promesas.py            (desde la carpeta del video)"""
import os
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)   # el efectos.py del video, no nucleo/efectos.py
import secuencia_fx as SF  # noqa: E402

PROMESAS = [   # (frase ancla, + s, qué debería verse)
    ('y tienes cuarenta y dos de oro', 0.4, 'rótulo 42 DE ORO + instructor/bolsa'),
    ('La equitación cuesta cien', 1.0, 'MG factura del 60'),
    ('Son más de mil quinientos', 1.2, 'factura TOTAL'),
    ('Hoy te traigo treinta trucos', 1.0, 'banda 30 trucos'),
    ('Cada vez que vas al instructor', 2.0, 'clip ventana del instructor'),
    ('El brujo la consigue con Strahad Farsan', 1.5, 'mapa Trinquete + Strahad'),
    ('La equitación de aprendiz baja de cien', 3.0, 'MG Honorable 100/90'),
    ('el instructor humano es Randal Hunter', 1.0, 'mapa Elwynn + Randal'),
    ('En la Horda, Kildar', 1.0, 'mapa Orgrimmar + Kildar'),
    ('Y aquí, un mensaje de Ehren', 2.0, 'comentario Ehren'),
    ('Viajero frecuente hace que tus vuelos', 1.0, 'tarjeta Legado / vuelo'),
    ('Jorge nos escribió', 2.0, 'comentario Jorge'),
    ('Porque reespecializar cuesta uno de oro', 3.0, 'MG escalera'),
    ('Un jugador confesó que se gastó dieciocho', 2.0, 'rótulo 23 / clip subasta arma'),
    ('pero mucha gente mata y sigue de largo', 1.0, 'clip desollar'),
    ('El cuero ligero lo paga el vendedor', 2.0, 'MG cuero'),
    ('Es un add-on de subasta que ya tiene versión', 1.0, 'pegatina Auctionator'),
    ('Un ejemplo real: la carne de tortuga', 2.5, 'MG balanza'),
    ('Un jugador vio cómo una perla de oro', 2.5, 'MG día/noche'),
    ('En los foros de Forever ya hay quejas', 2.0, 'clip subasta'),
    ('Alan nos dijo que va despacio', 2.0, 'comentario Alan'),
    ('Un personaje de nivel bajo aparcado junto al buzón', 2.0, 'tarjeta banco / clip buzón'),
    ('En Los Baldíos hay una élite nueva', 2.0, "mapa Chol'aruk + pegatina"),
    ('Y este va para Rafael', 2.0, 'comentario Rafael'),
    ('la Bolsa de paño mágico roja tiene catorce', 1.0, 'pegatinas bolsa roja / caja feria'),
    ('La próxima Feria vuelve en diciembre', 1.5, 'mapa Mulgore + Gelvas'),
    ('con paño de seda haces vendas', 1.0, 'pegatinas seda / venda'),
    ('Y aquí, Vincent, que comentó', 2.0, 'comentario Vincent'),
    ('Las verdes colinas de Tuercespina es esa misión', 1.5, 'página de Tuercespina'),
    ('Y en mar abierto, frente a los Páramos', 2.0, 'clip pesca mar abierto + tarjeta baúl'),
    ('sale de las trampas de marisco', 1.5, 'mapa Desolace trampas'),
    ('Es un robot que viaja con la caravana', 1.5, 'Supervendedor 680 + mapa'),
    ('Caen de los Exiliados de las Tierras Altas', 2.0, 'mapa Arathi 3 puntos'),
    ('Ardientes, del trueno y blasonados', 0.8, '3 talismanes'),
    ('En la costa de la Vega de Tuercespina', 2.0, 'mapa Arrecife + almeja'),
    ('Ojo con el precio', 2.5, 'MG perla azul cae'),
    ('Jonathan nos dijo que el video', 1.5, 'comentario Jonathan'),
    ('En Gadgetzan hay una misión de cocina', 2.0, 'mapa Tanaris Gadgetzan/rocs'),
    ('Pero mira lo que pasó', 4.0, 'MG desplome huevos'),
    ('En Feralas, los hipogrifos', 1.5, 'mapa Feralas + pico/hueso'),
    ('los granjeros sueltan horcas', 0.5, 'clip Trabalomas granjeros'),
    ('En la costa sur de Tanaris hay unas tortugas', 1.5, 'mapa tortugas + planoleador'),
    ('Son cajas interceptadas que caen', 1.5, 'tarjeta Waylaid Crate / clip caja'),
    ('Se entregan en el campamento de Three Corners', 1.5, 'mapa Crestagrana'),
    ('Forever trae más de seiscientas recetas', 1.5, 'tarjeta recetas'),
    ('CaneAttack nos escribió', 2.0, 'comentario CaneAttack'),
    ('entre ellas la Guarida de Onyxia', 0.8, 'Onyxia'),
    ('Un jugador compró unos dos mil cardoveloces', 1.0, 'cardoveloz'),
    ('Los Adornos brillantes se compran', 1.0, 'Adornos brillantes'),
    ('el libro de pesca de experto te lo vende el Viejo Heming', 1.0, 'mapa Bahía del Botín + Heming'),
    ('Y el de artesano, Nat Pagle', 1.0, 'mapa Marjal + Nat Pagle'),
    ('Los sátiros Jadefire de Frondavil', 1.5, 'mapa Frondavil + sátiro'),
    ('en Las Estepas Ardientes hay vetas de torio ricas', 1.5, 'mapa Estepas vetas'),
    ('Los vendió a unos nueve de oro', 2.0, 'MG techo cristal'),
    ('Mister Graphed vende el Cristal Arcano', 1.0, 'Mister Graphed'),
    ('solo una de cada cuatro misiones', 2.0, 'MG misiones 1 de 4'),
    ('solo con las misiones del Monte Hyjal', 1.0, 'mapa Hyjal'),
    ('No pagues lo que no usas', 1.0, 'banda cierre'),
]


def main():
    capa = SF.cargar()
    S = capa.S
    minis = []
    mw, mh = 480, 270
    filas = []
    for frase, dt, que in PROMESAS:
        try:
            t = capa.ancla(frase) + dt
        except Exception as e:
            print("NO ENCONTRADA:", frase, e)
            continue
        k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
        b = capa.bs[k]
        f = capa.aplicar(capa.envolver(S._fuente(b, k, True, capa), b).cuadro(t), t)
        m = cv2.resize(f, (mw, mh), interpolation=cv2.INTER_AREA)
        cv2.rectangle(m, (0, mh - 26), (mw, mh), (20, 18, 18), -1)
        txt = f"{int(t // 60)}:{t % 60:04.1f} {b['id'][6:]} {que}"
        cv2.putText(m, txt.encode("ascii", "replace").decode(), (6, mh - 7), cv2.FONT_HERSHEY_SIMPLEX, .5, (90, 214, 255), 1,
                    cv2.LINE_AA)
        minis.append(m)
        filas.append((frase, t, b["id"], que))
    cols, n = 4, 12
    for h in range(0, len(minis), n):
        g = minis[h:h + n] + [np.zeros_like(minis[0])] * (-len(minis[h:h + n]) % cols)
        ruta = f"previews/promesas_{h // n + 1:02d}.jpg"
        cv2.imwrite(ruta, np.vstack([np.hstack(g[i:i + cols]) for i in range(0, len(g), cols)]))
        print(ruta)
    for frase, t, bid, que in filas:
        print(f"{int(t // 60)}:{t % 60:04.1f}\t{bid}\t{frase}\t{que}")


if __name__ == "__main__":
    main()
