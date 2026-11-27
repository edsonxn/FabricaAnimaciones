# -*- coding: utf-8 -*-
"""Segundos de cada clip (ajustados con las hojas de contacto previews/c_*.jpg, 26-nov)."""
SEG = {
    # --- draco (39.4 s): la última imagen (franja de rocas arriba + rojo) entra a los 34.4 y queda fija hasta el final
    "draco_ultimo": 34.45,   # primer cuadro de la última imagen incompleta (34.3 = última foto completa)
    "draco_gancho": 27.45,   # Dimorphos pequeño creciendo → superficie → última imagen
    "draco_fin": 22.45,      # Didymos sale por la esquina, Dimorphos se acerca; rocas desde ~28
    "draco_ini": 0.0,        # el clip NO tiene «dos puntos»: arranca con Didymos ya visible + Dimorphos como punto
    # --- apl_festejo (15.9 s): NO son ingenieros, es otra secuencia DRACO de aproximación (0-16 s)
    "festejo": 0.0,          # sin festejo en este clip; alternativa: apl_sala 92.5-100
    # --- hera_llegada (67.4 s): punto desde ~15, crece hasta ~28, gira con su luna hasta 53.3; 53.5+ negro/logo ESA
    "llegada_gancho": 17.5,  # 17.5-30.9 (vel 2): punto → Didymos con Dimorphos
    "didymos_cerca": 49.8,   # 49.8-53.3 (vel 0.5): Didymos lo más grande, con Dimorphos debajo
    "llegada": 15.0,         # punto apenas visible
    "llegada_vel": 5.0,      # 15.0 + 7.6*5 = 53.0 ≤ llegada_fin
    "llegada_fin": 53.3,     # último cuadro antes del fundido a negro / logo
    # --- hera_sur (29 s): útil 0-22.8 (luego negro + logo ESA)
    "sur": 0.0,              # cubre 7 s y 17.8 s (hasta 17.8)
    # --- hera_norte (23 s): útil 0-16.8
    "norte": 6.5,            # 6.5-13.6: la luna rodea a Didymos y cruza por delante
    # --- dart_lanz (120 s): T-0 en ~32.3, ignición/humo 33.5-35, sale de cuadro de llamas ~38
    "lanz": 32.5,            # 32.5-38.0 (de noche; el cohete casi no se ve, es el destello)
    "despl": 63.0,           # dart_despl (105 s, re-descargado): DART se separa de la 2.ª etapa ~62-66
    # antes: clip dart_despl FALLÓ al descargar → queda el defecto (10.0). Hera se separa en hera_lanz 169.6-177.8
    # --- nasa_sala (160 s): todo es la emisión con la DART cam grande y la sala SOLO en un recuadro pequeño
    "sala_ini": 102.0,       # 102-108.6 sin cintillo ni insignia «Primary/Opportunity»
    # --- apl_sala (140 s): señal perdida (rojo) 87-93, corte a la sala a las 93.0
    "sala_festejo": 91.5,    # 1.5 s de pantalla roja → aplausos y brazos arriba (93-99.3)
    "sala_final": 106.0,     # 106-113.7 abrazos (insignia IMPACT pequeña; cintillo desde ~114)
    # --- hubble_x3 (3.07 s): tres cuadros fijos +22 min / +5 h / +8.2 h
    "x3_fin": 2.95,
    # --- hubble_aft (162 s): imágenes reales de Hubble 29.2-41.3 y tríptico 141.5-150.3 (los dos con subtítulo quemado)
    "aft": 29.6,             # 29.6-40.5 eyecta de Hubble (subtítulo abajo hasta ~37.7)
    "aft2": 142.0,           # 142.0-150.1 tríptico +22 min/+5 h/+8.2 h (frase arriba hasta ~147.7); logo NASA 150.5
    # --- hera_trailer (100.8 s): Hera visible 44.8-47.3 (cerca de la Tierra) y pequeña frente al asteroide 47.5-50
    "trailer": 44.8,         # 44.8-50.3 sin texto
    # --- hera_lanz (250 s): T-0 126, despega 128.5, corte a plano lejano 133
    "hera_lanz": 124.3,      # 124.3-133.0
    # --- hera_marte (141 s): Deimos (disco oscuro) cruzando Marte 68.5-82; rótulo «297 km» 77-81.5
    "marte": 72.5,           # 72.5-76.5 sin rótulo (imagen cuadrada con barras laterales)
    # --- esa_intro (150 s): 0-81 tráiler, 82-137 presentador en atril, 137.5-150 plano general del escenario
    "berlin": 137.6,         # 137.6-146.8 plano general (pantalla «DOUBLE IMPACT», presentadores); sin dinosaurios
    "dino": 95.0,            # NO hay dinosaurios en el clip: 95-121.6 = presentador con fondo de asteroide (tramo largo)
    # --- esa_hoy (245 s): imagen a pantalla 18-33.3; antes/después 37.5-52.3, 98.5-149.5, 214-232 (ocupa solo el tercio de arriba)
    "hoy": 21.0,             # 21.0-23.7 «Dimorphos today» (imagen sola)
    "tres": 39.0,            # 39.0-45.5 antes/después lado a lado
    "igual": 105.0,          # 105-118 la misma comparación, otro tramo
    # --- esa_10m (50 s): nunca a pantalla completa; plano general con la foto proyectada 0-15.5 y 30-48
    "diez": 6.0,             # 6.0-9.5 escenario con la imagen en la pantalla
    # --- esa_puro (60 s): imagen en la pantalla del escenario 6-60 (sobreexpuesta), nunca a pantalla completa
    "puro": 18.0,            # 18.0-24.5 dos vistas de Dimorphos con el cráter
    # --- esa_rocas (70 s): imagen a pantalla completa 10.5-20.7 (muy oscura)
    "rocas": 11.5,           # 11.5-18.4 Didymos/Dimorphos con las rocas/estelas alrededor
    # --- esa_estafeta (40 s): plano general 6-12.5; orador con el tubo/estafeta 13-40
    "estafeta": 24.5,        # 24.5-27.6 tiende el tubo hacia el compañero (alt. 6.5 plano general)
    # --- esa_tiri (60 s): imagen térmica (rosa/morado) en la pantalla del escenario 10-28.5
    "tiri": 15.0,            # 15.0-21.7
    # --- chel_dash (48.6 s): bola de fuego 20.5-26.5, estela 26.5-46
    "chel": 20.0,            # 20.0-28.0 aparece, destello máximo ~25, se parte
}
