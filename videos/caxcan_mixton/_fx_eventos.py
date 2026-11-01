# -*- coding: utf-8 -*-
"""Efectos GRABADOS del Mixtón (sfx/*.mp3: ElevenLabs 21-oct + biblioteca) anclados a la voz; los lee `_fx_ambiente.py`.
AMB2 = bucles [(t0, t1, archivo, vol)] (RMS −20 dBFS × vol) · UNA = golpes [(t, archivo, vol)] (pico −6 dBFS × vol, sin bucle).
Va aparte de escenas.py para poder cambiar el sonido sin tocar el código del render (la firma de las tomas)."""
from escenas import T, F, F1, t0_, t1_

AMB2 = [
    (F("rio", 3) - 0.3, F1("rio", 3) + 0.5, "metate", 0.22),
    (F("fiesta", 1) - 0.2, t1_("fiesta") - 0.3, "multitud_canto", 0.28),
    (F("llegada", 1) - 0.3, F1("llegada", 3) + 0.3, "marcha", 0.38),
    (t0_("hierro") - 0.3, F("hierro", 1) + 0.3, "incendio", 0.45),
    (F("hierro", 2) - 0.25, F("hierro", 3), "incendio", 0.28),
    (T("decision", "amanecer", 3) - 0.2, t1_("decision") + 0.3, "metate", 0.18),
    (F("victoria", 5) - 0.3, t1_("victoria") + 0.3, "multitud_canto", 0.45),
    (F("alvarado", 3) - 0.3, F("alvarado", 8), "tormenta", 0.50),
    (F("alvarado", 9) - 0.3, t1_("alvarado") + 0.3, "tormenta", 0.35),
    (F("guadalajara", 2) - 0.3, F("guadalajara", 3), "batalla", 0.45),
    (F("guadalajara", 2) - 0.3, F("guadalajara", 3), "incendio", 0.35),
    (F("guadalajara", 3) - 0.25, F("guadalajara", 5), "incendio", 0.22),
    (F("guadalajara", 5) - 0.3, F("guadalajara", 6), "batalla", 0.45),
    (F("virrey", 1) - 0.2, F1("virrey", 1) + 0.3, "marcha", 0.42),
    (F("caida", 0) + 0.2, F("caida", 2), "marcha", 0.35),
    (F("caida", 2) - 0.25, F("caida", 3) + 0.5, "batalla", 0.50),
    (t0_("cedula") - 0.3, F("cedula", 1), "galeon", 0.40),
    (F("epilogo", 3) - 0.3, t1_("epilogo") + 0.3, "galeon", 0.40),
    (F("valladolid", 5) - 0.3, t1_("valladolid") + 0.3, "galeon", 0.38),
]

UNA = [
    # llegada: perros, caballos, el muro
    (T("llegada", "perros", 1) - 0.2, "perros", 0.55),
    (T("llegada", "cascos", 1) - 0.3, "caballos", 0.45),
    (T("llegada", "derribaron", 4) - 0.1, "derrumbe", 0.45),
    # el hierro candente
    (T("chirinos", "herradlo", 3) - 0.05, "hierro", 0.60),
    (T("hierro", "hierro", 1) - 0.05, "hierro", 0.55),
    # el río: el bebé que patea, la tormenta de su nacimiento
    (T("rio", "patear", 4) - 0.1, "bebe", 0.50),
    (F("rio", 4) + 0.35, "trueno", 0.45),
    # encomienda: el látigo, la campana de la capilla
    (T("encomienda", "deprisa", 2) - 0.15, "latigo", 0.65),
    (F("encomienda", 4) - 0.3, "campana", 0.45),
    # caracol (en lugar del cuerno procedural)
    (F("tlatol", 3) - 0.1, "caracol", 0.50),
    (F("llamado", 2) - 0.2, "caracol", 0.55),
    (T("penol", "tenamaxtli", 2) - 0.1, "caracol", 0.45),
    (F("penol", 4) + 0.3, "caracol", 0.45),
    (T("victoria", "cayó", 2) - 0.3, "caracol", 0.55),
    (t0_("caida") + 4.3, "caracol", 0.55),
    # «Miles de voces le contestaron» y la victoria
    (T("penol", "miles", 5) - 0.1, "multitud_grito", 0.60),
    (T("victoria", "cayó", 2) + 0.05, "derrumbe", 0.75),
    (T("victoria", "cayó", 2) + 1.4, "multitud_grito", 0.50),
    (F("victoria", 3) - 0.3, "caballos", 0.45),
    (F("victoria", 4) - 0.1, "multitud_grito", 0.40),
    # las armas que tronaban
    (T("noticias", "tronaban", 3) - 0.05, "trueno", 0.50),
    (T("noticias", "armas", 3) + 0.1, "arcabuz", 0.40),
    # consejo del virrey
    (t0_("consejo") + 0.2, "campana", 0.40),
    (F("consejo", 2) + 0.2, "pluma", 0.60),
    # Alvarado
    (t0_("alvarado") + 0.3, "caballos", 0.40),
    (F("alvarado", 3) + 0.4, "trueno", 0.50),
    (T("alvarado", "esperando", 3) - 0.05, "trueno", 0.55),
    (F("alvarado", 4) + 0.3, "caballos", 0.50),
    (T("alvarado", "encima", 5) - 0.2, "caballos", 0.45),
    (T("alvarado", "vencer", 9) - 0.1, "trueno", 0.50),
    # Guadalajara
    (F("guadalajara", 2) + 2.0, "arcabuz", 0.40),
    (F("guadalajara", 5) - 0.2, "caballos", 0.45),
    # el virrey: cañones
    *[(F("virrey", 3) + 0.9 * k, "canonazo", 0.55) for k in range(5)],
    *[(T("virrey", "cañones", 5) + 0.4 + 0.35 * k, "canonazo", 0.70) for k in range(3)],
    # la caída
    (T("caida", "perros", 1) - 0.3, "perros", 0.55),
    (F("caida", 2) + 0.2, "multitud_grito", 0.45),
    # epílogo y Valladolid
    (t0_("epilogo") + 0.3, "campana", 0.40),
    (t0_("valladolid") + 0.1, "campana", 0.35),
    # sustitutos de los procedurales que se quitan (QUITAR, abajo)
    (F("guadalajara", 2) + 0.5, "caracol", 0.50),
    (T("cedula", "siguió", 1) - 0.1, "hierro", 0.55),
    (t0_("cedula") + 0.3, "trueno", 0.40),
]

# procedurales de escenas.SFX que ya tienen versión grabada: `_sfx_filtrado.py` los quita al armar audio/sfx.wav
# (nombre, t_desde, t_hasta); None = en todo el video
QUITAR = [("arena", None, None), ("bebe", None, None), ("cuerno", None, None), ("siseo", None, None), ("trueno", None, None),
          ("ola", None, None), ("lluvia", t0_("alvarado"), t1_("alvarado"))]
