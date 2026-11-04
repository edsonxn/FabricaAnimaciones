# ¿Qué pasaría si cayeras en arenas movedizas? — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: kuriox (Short vertical, 73 s) · hueco: Kuriox ATRASADO desde el 31-oct (la ballena sale el 4-nov 14:00) → el siguiente hueco libre
- estilo: ACUARELA PINTADA A MANO POR CÓDIGO → docs/estilo_acuarela_pincel.md · kit copiado de videos/ballena_estomago/
- etapa: ✅ SUBIDO y PROGRAMADO vie 6-nov-2026 14:00 CDMX (20:00 UTC): https://youtu.be/wWscQjByyxE (privado → público solo)
- siguiente: nada; medir a 7 días (`yt metricas kuriox`) y comparar con la ballena; `fab.py arenas_movedizas limpiar` cuando el usuario lo apruebe

## Sesiones (plan de tramos · «continúa el video arenas» retoma aquí · protocolo docs/sesiones.md)
- alias: arenas, arenas_movedizas, el short de las arenas movedizas
- vista previa: NO (el usuario, 4-nov: directo al MASTER) · 1 sesión
- leer al empezar: este ESTADO.md · `guion.py` (datos) · `escenas.py` (mapa de planos)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | todo: guion, voz, planos, SFX, Lyria, mezcla, render, miniatura, subir | ✅ 4-nov | elegido por el usuario entre 6 opciones de terror (opción 2); MASTER 73 s, CER 0, desfase 0; miniatura Flow 2/2 (elegida la de título grande); 48 h tras la ballena |

## Hecho
- guion (datos verificados: Khaldoun et al., Nature 437, 635, 2005; Engber, Slate 2010) · voz ElevenLabs de Kuriox 66,1 s, CER 0 en 12/12
- planos: plano_a (0-28), plano_b (28-48,3), plano_c (48,3-73), revisados en hoja (previews/hoja_a, b, b2, c, c2) · ~0,5 s/cuadro
- render 20 segmentos en ~6 min · `final` + `verificar` (CER 0, sin desfase) · hoja `previews/final_hoja.jpg` sin bloqueos
- miniatura Flow «¿TE HUNDES? LAS PELÍCULAS MINTIERON» → salida/arenas_movedizas_mini_flow.jpg · subido wWscQjByyxE, registrado en kuriox.json y BITACORA
- SFX 100 % sintetizados: `sonidos_arena.py` (68 eventos) → audio/fx.wav · Lyria nueva (la biblioteca no tenía nada: 0,15) · mezcla −14 LUFS, voz +13,1 dB

## Plan de planos (voz → imagen)
- 0-9,7 orilla: camina → «el suelo se traga tus piernas» (succión, salpicón, salacot que salta) → «¡ARENAS MOVEDIZAS!»
- 9,7-20,6 cine: «AÑOS 60», 35 rollos (uno rojo, «1 DE CADA 35») → película sepia: el galán se hunde hasta la cabeza → sello «¡MENTIRA!»
- 20,6-28 balanza «PESA ×2» (cubeta de arena vs explorador) → corte: hasta la «CINTURA» → «¡FLOTAS!» (flechas de empuje)
- 28-35,4 corte: patalea, los granos se cierran → bloque gris «¡COMO CEMENTO!» · 35,4-40,5 Kuri tira de la cuerda; burbuja «= 1 COCHE»
- 40,5-48,3 playa: reloj «HORAS», el sol baja a la tarde, la marea sube hasta el pecho, «¡LA MAREA!»
- 48,3-54,6 «¡NO TIRES!» (tache) → se echa atrás; burbuja: flotando en una alberca · 54,6-60,2 corte: piernas en círculos, «DESPACIO…», hilos de agua «+ AGUA»
- 60,2-63 se desliza fuera, «¡PLOP!», la bota se queda · 63-73 sentado y embarrado con Kuri; Kuri hunde un rollo de película; «¡NO ENTRES EN PÁNICO!»

## Lecciones de este video (solo lo no obvio)
- `fondos.py` choca con `nucleo/fondos.py` (el núcleo va primero en sys.path): los módulos propios del video llevan sufijo (`fondos_arena.py`).
- Charco en perspectiva: el labio delantero es media elipse que TAPA lo hundido; alto ≥ 210 px bajo la superficie o asoman las botas.
- Agua que sube alrededor de alguien: una capa DETRÁS (toda la playa) y otra DELANTE solo hasta el pecho; una sola capa encima le tapa la cara.
- Lo que pasa dentro de una película se pinta en una copia y se recorta al cuadro (si no, el cuerpo que se hunde se sale del fotograma).
