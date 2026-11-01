# -*- coding: utf-8 -*-
"""Efectos de sonido del plano secuencia «gravedad 5 s» (sintetizados por nucleo/sfx.py).
Variedad de timbres sin que ninguno tape las palabras iniciales de frase."""
from anclas import A, Z1, Z2, Z3, Z4
from estado import T_GRAV_OFF, T_GRAV_ON, T_IMPACTO


def registrar(e):
    ev = e.ev
    # ---- intro
    ev(A.pequeno + 0.15, "boing", 0.32, -0.2)
    ev(A.suelo + 0.05, "golpe_suave", 0.35, -0.2)
    ev(Z1[0] + 0.1, "zoom_whoosh", 0.45, dur=2.2)
    ev(A.desaparece, "apagon", 0.35, dur=1.0)
    for k in range(5):
        ev(A.cinco_i + 0.35 * k, "tick", 0.24, 0.25, tono=1.0 + 0.05 * k)
    ev(A.volando, "whoosh", 0.32, 0.2)
    ev(A.cohetes, "error", 0.32, 0.3)
    ev(A.depende, "pop", 0.30, 0.3)
    ev(A.apagues, "pluck", 0.32, 0.3, tono=0.9)
    ev(Z2[0], "zoom_whoosh", 0.45, dur=2.0)

    # ---- version_a
    ev(A.suave, "ding", 0.32, -0.3)
    ev(A.cero_a - 0.08, "campana", 0.30, tono=1.15)
    ev(T_GRAV_OFF + 0.1, "burbujas", 0.28, -0.2, dur=0.9)
    ev(A.flotas, "brillo", 0.28, -0.2)
    ev(A.impulso, "boing", 0.30, -0.1, tono=1.1)
    ev(A.arriba_a, "crece", 0.28, dur=1.1)
    ev(A.arbol, "pop", 0.28, 0.2)
    ev(A.perros, "pop", 0.25, -0.2, tono=1.0)
    ev(A.bicicletas, "clink", 0.25, 0.1)
    ev(A.tazas, "gota", 0.28, 0.3)
    ev(A.aire_a, "viento", 0.30, dur=1.4)

    # ---- viento_mar
    ev(A.dos_v - 0.08, "campana", 0.30, tono=1.0)
    ev(A.aplasta, "golpe_suave", 0.30, 0.2)
    ev(A.rebota_v, "whoosh", 0.38, 0.2, tono=0.85)
    ev(A.resorte, "boing", 0.30, 0.3, tono=0.9)
    ev(A.golpe_v, "puf", 0.35, 0.2)
    ev(A.oidos + 0.15, "golpe_suave", 0.42)
    ev(A.viento, "viento", 0.38, dur=2.4)
    ev(A.olas, "chapuzon", 0.34, 0.3)
    ev(A.burbujas, "burbujas", 0.34, 0.3, dur=1.3)
    ev(A.gira, "espiral_zap", 0.28, dur=1.1)
    ev(A.recta_v, "whoosh", 0.32, 0.4)

    # ---- caida_a
    ev(A.cinco_ca - 0.08, "campana", 0.34, tono=1.25)
    ev(T_GRAV_ON, "whoosh", 0.42, tono=0.75)
    ev(T_IMPACTO, "trueno", 0.45)
    ev(A.golpean + 0.1, "chapuzon", 0.35, 0.3)
    ev(A.durisimo, "bonk", 0.30, -0.2)
    ev(A.sobreviviria, "bling", 0.36)
    ev(Z3[0], "zoom_whoosh", 0.45, dur=2.1)

    # ---- version_b
    ev(A.total - 0.1, "gong", 0.35, tono=0.85)
    ev(A.cero_b - 0.08, "campana", 0.30, tono=0.95)
    ev(A.brutal, "crece", 0.30, dur=1.0)
    ev(A.rebota_b, "explosion", 0.42, tono=0.8)
    ev(A.rompe, "crujido", 0.40, dur=0.9)
    ev(A.lava, "fuego", 0.35, dur=1.5)
    ev(A.tres_b - 0.08, "campana", 0.30, tono=1.05)
    ev(A.orbita, "whoosh", 0.32, -0.2)
    ev(A.sol_b, "amanecer", 0.32, 0.3, dur=1.4)
    ev(A.hincha, "crece", 0.34, 0.3, dur=1.1)
    ev(A.nuclear, "apagon", 0.38, 0.3, dur=1.2)
    ev(A.cinco_b - 0.08, "campana", 0.35, tono=1.25)
    ev(A.desploma, "canonazo", 0.45)
    ev(A.funde, "fuego", 0.36, dur=1.6)

    # ---- cierre
    ev(A.suerte, "amanecer", 0.34, dur=1.8)
    ev(A.interruptor, "clink", 0.30, 0.3)
    ev(A.forma, "revelar", 0.32)
    ev(A.materia, "estrellitas", 0.28)
    ev(Z4[0], "zoom_whoosh", 0.42, dur=2.0)
    ev(A.piso_c + 0.05, "clink", 0.32, -0.1)
    ev(A.tiron, "brillo", 0.30)
    ev(A.estrellas, "bling", 0.32)
