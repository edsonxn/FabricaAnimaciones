import sys, numpy as np, cv2
import boceto as B, mapa as M
from obj_base import *
import obj_p as P
import obj_b as Bb
M.cargar()
cam = M.Cam(50, 31, 1.3)
img = M.fondo_base(); M.pintar_tierra(img, cam, 0)
h = B.Hoja(); h.limpiar(); h.fondo = img
lista = sys.argv[1] if len(sys.argv) > 1 else 'a'
if lista == 'a':
    D = [P.montanas(), P.tablilla(), P.qanat(0), P.cilindro(), P.columna(), P.carta(), P.gota_oro(), P.altar_fuego(1), P.tablero_ajedrez(), P.arco_ctesifonte(),
         P.libro(), P.mezquita()]
else:
    D = [P.alfombra(), P.trono_pavo(), P.torre_petroleo(1), P.barril(), P.parlamento(), P.haft_sin(), P.pancarta(), P.estandarte_persa(),
         persona(P.PURPURA, PIEL_OSC, "tiara", "serio", (20, 110), barba=NEGRO, traje="tunica", faja=ORO, cuello=ORO),
         persona(ROJO_CH, PIEL_OSC, "corona_sasanida", "serio", (20, 110), barba=NEGRO, traje="tunica", faja=ORO),
         persona(ROJO_OSC, PIEL_OSC, "casco_griego", "enojo", (20, 140), acc_d="espada", traje="armadura"),
         persona(CREMA, PIEL_OSC, "kufiya", "serio", (20, 40), barba=NEGRO),
         persona(P.AZUL_TILE, PIEL_OSC, "taj", "feliz", (30, 100), bigote=True),
         persona(NEGRO, PIEL_CL, "turbante_negro", "serio", (20, 20), barba=(235, 235, 240)),
         persona(MORADO, PIEL_OSC, "kolah", "normal", (20, 20), bigote=True, barba=NEGRO),
         persona((150, 140, 108), PIEL, "gorra_oficial", "serio", (20, 20), bigote=True, traje="corta")]
for i, d in enumerate(D):
    x = 160 + (i % 6) * 320; y = 520 + (i // 6) * 430
    d.dibujar(h, x, y, 0.6 if lista == 'a' else 0.7, 0.0, False, 1.0, 0, i + 1, peg=True)
out = np.clip(h.componer(), 0, 1)
cv2.imwrite(f'previews/_o_{lista}.jpg', (out[..., ::-1] * 255).astype(np.uint8))
