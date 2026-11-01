# -*- coding: utf-8 -*-
"""Anclas a la voz (segundos) compartidas por escenas.py (animación) y fx_audio.py (SFX de ElevenLabs): todo cae en SU palabra."""
from pix import FIN, INI, ww

T_ON = 1.05                                  # la tele se enciende (antes de la voz)

# ---- cartucho
a_sep = ww("cartucho", 0, "septiembre")
a_2010 = ww("cartucho", 0, "2010")
a_est = ww("cartucho", 0, "estudiante")
a_car = ww("cartucho", 0, "cartucho")
a_zel = ww("cartucho", 0, "zelda")
a_ven = ww("cartucho", 0, "venta")
a_gar = ww("cartucho", 0, "garaje")
a_par = ww("cartucho", 1, "partida")
a_due = ww("cartucho", 1, "dueño")
a_sell = ww("cartucho", 1, "llamaba")
a_ben1 = ww("cartucho", 1, "ben")
T_INS0 = a_gar + 0.95                        # el cartucho sale del foco y viaja a la consola
T_INS1 = a_par - 0.10                        # entra en la ranura

# ---- falla
T_JUEGO = INI("falla", 0) + 0.15
a_noc = ww("falla", 0, "noche")
a_fal = ww("falla", 0, "fallar")
a_ter = ww("falla", 0, "tercer")
a_sal = ww("falla", 0, "saltaba")
a_fin = ww("falla", 0, "final")
a_pue = ww("falla", 0, "pueblo")
a_vac = ww("falla", 0, "vacío")
a_vend = ww("falla", 1, "vendedor")
a_rei = ww("falla", 1, "reír")
a_est2 = ww("falla", 1, "estatua")
a_mir = ww("falla", 1, "mirada")
T_SALTO = a_fin + 0.45                       # el marcador salta al día 4

# ---- ben
a_rel = ww("ben", 0, "relato")
a_ben2 = ww("ben", 0, "ben")
a_12 = ww("ben", 0, "12")
a_ahog = ww("ben", 0, "ahogado")
a_desde = ww("ben", 0, "desde")
a_hab = ww("ben", 0, "intentaba")
a_fic = ww("ben", 1, "ficción")
a_alex = ww("ben", 1, "alex")
a_jad = ww("ben", 1, "jadusable")

# ---- cierre
a_real = ww("cierre", 0, "real")
a_vid = ww("cierre", 0, "videos")
a_web = ww("cierre", 0, "páginas")
a_men = ww("cierre", 0, "mensajes")
a_mil = ww("cierre", 0, "millones")
a_sab = ww("cierre", 0, "saber")
a_term = ww("cierre", 0, "terminaba")
a_jue = ww("cierre", 0, "juego")
a_des = ww("cierre", 1, "desde")
a_alg = ww("cierre", 1, "algo")
a_alguien = ww("cierre", 1, "alguien")
a_acu = ww("cierre", 1, "acuerda")
a_ben3 = ww("cierre", 1, "ben")
T_NEGRO = FIN("cierre", 0) + 0.25            # apagón entre las dos frases
T_REG = INI("cierre", 1) - 0.1               # vuelve la luz
T_OFF = FIN("cierre", 1) + 0.12              # la tele se apaga
