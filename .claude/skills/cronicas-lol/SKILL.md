---
name: cronicas-lol
description: Estilo «Crónicas de League of Legends» (también «Crónicas de ligoleyen») = ANÁLISIS TÁCTICO de esports de la Fábrica de Animaciones. Úsalo SIEMPRE que pidan un video de League of Legends / LoL / Worlds / LEC / LCK / esports, un video «estilo Crónicas de League of Legends», «como los de la Worlds», «analiza las jugadas de este partido», «como en la NFL con flechas, pausas y 3D», un resumen de un torneo o de una semana, la previa de un partido o las jugadas clave de una serie. Dice qué motor, qué kit (nucleo/mg_tactica.py, nucleo/mg_lol.py, nucleo/tactica3d) y qué ejemplo copiar, y las reglas que no se negocian.
---

# Crónicas de League of Legends (estilo análisis táctico)

Proyecto: la raíz de este repo (`python fab.py ...`). Responde en español.

## Lo primero (en este orden)
1. Lee `docs/estilo_analisis_tactico.md` § «GUÍA RÁPIDA PARA OTRO AGENTE» (motor, formatos, kit, flujo y reglas).
   El resto del doc se lee por secciones cuando toque (grep por el título del §).
2. Elige el formato y abre su ejemplo (en la copia compartida los ejemplos viven en `ejemplos/<v>/` en vez de `videos/<v>/`):
   - Resumen de torneo o semana (20-30 min, el que mejor funciona): `lol_semana2` (completo) y `lol_worlds_2026` (jugada en 3D: `j6_3d.py`).
   - Previa de un partido (12-15 min): `ig_lyon_worlds`.
   - Jugadas clave de un partido ya jugado, sin spoiler (15-18 min): `cfo_kc_jugadas`.
   Lee del ejemplo `guion.py` (estructura, `FONETICA`, voz) y `efectos.py` (la gramática del montaje: `J`, `CLIP`, `P`,
   `REBX`, `LENTA`, `MESA`, `V3`, `RUTA`, `VIVO`, anclas `T0`/`T1`/`W`/`NX`). Cópialos y adáptalos; no reescribas el kit.
3. `python fab.py nuevo <v> --yt` y sigue el flujo de la guía rápida.

## Motor y kit (no cambiarlos)
- `MOTOR = "secuencia"`, `ESTILO_VISUAL = "secuencia_yt"`; todo el cuadro sale del FX `video` del clip del VOD
  (`vel` 1/0/negativa/lenta, `zoom`).
- Telestrador 2D: `nucleo/mg_tactica.py` · gráficos de transmisión: `nucleo/mg_lol.py` · 3D (three.js local):
  `nucleo/tactica3d/render3d.py` (Grieta 3D) y `nucleo/tactica3d/sobre_video.py` (capas 3D sobre el VOD).
- Voz ElevenLabs de comentarista con corchetes, `eleven_v4_turbo`, sin `[excited]` ni `[whispers]`; nombres en inglés en `FONETICA`.

## Reglas que no se negocian
- Cero datos inventados: marcador, kill feed, retratos del HUD, feed oficial `livestats` y narración del VOD completo (no el resumen).
- Anillos en los PIES medidos en un cuadro con rejilla; rutas solo con puntos medidos en la misma toma de cámara.
- La acción a x1 o más lenta, nunca acelerada; cada tramo sigue en el cuadro exacto de la pausa; nunca cortar la voz a media palabra.
- Sin spoiler (título, miniatura, gancho) si el partido ya se jugó; fechas por nombre de día.
- Alternar VOD y 3D por frases (nunca 30 s de 3D seguidos); nada quieto > 2 s; gancho cargado de gráficos `mg_lol`;
  durante una jugada, gráficos chicos en los bordes para no tapar la acción.
- Antes de entregar: hoja de cuadros revisada a mano (anillos bien puestos, textos sin chocar) y `python fab.py <v> chequeo` si existe.
