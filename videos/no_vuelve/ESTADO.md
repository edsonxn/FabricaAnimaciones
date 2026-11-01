# No vuelve a pasar (corto) + «Bájate de la rueda» (taller HTML sobre el círculo de la violencia, 3.º de secundaria, Jalpa) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: ninguno (taller presencial del Instituto Municipal de las Mujeres en la secundaria de Jalpa, Zac.; no va a YouTube) · sin fecha
- estilo: pegatina_flow → doc: docs/estilo_pegatina_flow.md · ejemplo: videos/la_sena/ (mismo público, misma FICHA, mismo taller HTML)
- etapa: ENTREGADO (22-oct). Taller SOLO presentación (el usuario quitó el corto y luego la historia en láminas):
  `taller/Bajate_de_la_rueda.html` 12,9 MB, 15 diap., todo dentro (imágenes, letras, canción de cuna), probado sin internet
- siguiente: teléfono del IMM de Jalpa (diap. 14); `fab.py no_vuelve limpiar` si el corto ya no se usa

## Sesiones (plan de tramos · «continúa el video no_vuelve» retoma aquí · protocolo docs/sesiones.md)
- alias: no_vuelve, No vuelve a pasar, el del círculo de la violencia, la rueda, Bájate de la rueda, el taller de la rueda
- pedido del usuario (21-oct): «igual que la de Jalpa del hermano mayor… el círculo de la violencia: cómo funciona, cómo prevenirlo, cómo
  darse cuenta si estás dentro… conmover, provocar llanto al final… hazlo todo en esta sesión»
- leer al empezar: este ESTADO.md, PLAN_TALLER.md y docs/estilo_pegatina_flow.md
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 0 | Investigación + historia + guion + prompts | ✅ 21-oct | metáfora: la rueda de la fortuna de la feria; frase: «No vuelve a pasar» |
| 1 | Voz ElevenLabs (41 frases) + Flow (38 prompts x2) + recorte + profundidad | ✅ 21-oct | 76/76 a la 1.ª, 0 puntos; elegidas b: feria_atardecer (marco), cocina_noche (misma cocina), paloma_vuelo (fondo crema) |
| 2 | escenas.py (13 escenas) + Lyria + SFX + mezcla + montaje | ✅ 21-oct | Lyria tramo 1 salió corto (58 s): `_musica_ajuste.py` lo deja sin estirar + cajita de la biblioteca al final de la mesa |
| 3 | render + MASTER + rigor + taller HTML (18 diap.) + empaquetado | ✅ 21-oct | render 26 min; rigor 1 cuadro/3 s → 6 arreglos con `--rehacer`; taller con el corto (98,6 MB) |

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- MASTER v1 (sin los arreglos) movido a C:\FabricaAnimaciones_tmp
o_vuelve_MASTER_v1.mp4 por falta de espacio en E: (borrable)
- voz HECHA: 41/41 CER 0, 145 s de voz, timeline 233,1 s; pista de solo voz en previews/voz_no_vuelve.mp3
- Flow HECHO (21-oct, 18:38-18:50): 76 en 1K en `imagenes/` (15 escenarios) y `hojas/` (23); proyecto
  https://flow.google.com/project/995821c4-6ba6-49e5-8767-922f990ffe13 · contacto en `previews/_contacto_*.jpg`
- escenas.py HECHO (21-oct): revisado con `python _hoja.py previews/x.jpg [t…]` (un cuadro por toma); `fx_audio.py` → audio/fx.wav
  con SFX de la biblioteca (troca al revés = llega; plato roto sintetizado). `fab.py no_vuelve montaje` lanzado
- 2K de las hojas (regla del 21-oct) PENDIENTE: en el Chrome del usuario; el recorte actual es del 1K (sirve para armar escenas)
- Lyria HECHA tras recargar (21-oct): 4 piezas pagadas (tramo 1 dos veces; `_lyria_tramo1_v2.mp3` descartada)
- Biblioteca (21-oct, `fab.py biblioteca sugerir no_vuelve --excluir la_sena jalpa`): para los tramos 1 y 3 casa la cajita de música
  de `wow_darrowshire` (otro público), pero ninguna pieza pasa de 0,45 ni tiene el clímax de intensidad 8 del patio ni el vals de
  feria: para el tramo 3 conviene Lyria nueva; el 1 podría salir de la biblioteca (`wow_darrowshire__lyria_tramo7`, desde ~5 s)
- ElevenLabs: cuenta 2 con ~172 créditos tras la voz (899 + 15); cuenta 1 marca 0 → SFX desde la biblioteca de `videos/*/sfx/`
- taller (21-oct): nombres de pieza corregidos con el mapa real (patas = utileria_feria/04, flor del chat = utileria_casa/06,
  diap. 5 sin los bancos propios); diap. 4, 5 y 12 arregladas. Vista previa: launch.json «taller-no-vuelve» (puerto 8772)

## Decisiones con el usuario (21-oct-2026)
- (22-oct) «Quita la historia de la presentación»: 15 diapositivas sin Diego; carta «para alguien de 8 años», preguntas
  generales; violentómetro con los 3 niveles completos y un ejemplo por nivel.
- «No me gustó mucho el video»: el taller va SIN el corto; la historia en láminas (narración en cursiva, diálogos con nombre,
  una frase por clic). «¿Amor o control?» con frases CAPCIOSAS (lo que parece cariño es control y al revés).
- Imágenes SOLO en Flow (navegador); NUNCA por la API de Google. ElevenLabs: 2 cuentas en la API con saldo.
- Mismo formato que «La seña»: corto pegatina Flow a la mitad de una presentación HTML con el mismo estilo.

## Hecho
- Investigación (CNDH 4 fases, violentómetro IPN, ENDIREH Zacatecas, Safe Dates/Fourth R, teléfonos verificados): PLAN_TALLER.md §5.
- guion.py (14 escenas, 41 frases, 1 812 caracteres; voces nuevas, distintas a La seña) · _prompts.py → prompts.json (38) · _bundle.js.

## Falta
- [ ] Teléfono del Instituto Municipal de las Mujeres de Jalpa (no está en línea) para la diap. 17
- [ ] Que el usuario apruebe las voces

## Lecciones de este video (solo lo no obvio)
- Dos renders a la vez (otra sesión con caxcan_mixton) llenaron E: a mitad del `--rehacer` (No space left on device): poner el
  render en cola con `Wait-Process` y mirar el espacio libre de E: antes de `final` (MASTER ~1 GB + video_sin_audio ~1 GB).
- La rueda de la fortuna la arma el código (`rueda()` en escenas.py): rueda de Flow SIN góndolas ni patas + patas en A + 8 góndolas
  que cuelgan del aro (ancla arriba) y se mecen; las góndolas con gente son otra hoja. Con el tono nocturno azul la rueda se veía
  lila: su propio tono cálido (RUEDA_N), la ilumina su luz.
- Pieza que trae mesa (el papá sentado): sentarlo en la cabecera de la mesa PINTADA y restaurar el fondo en el rectángulo de la mesa
  bajo la cubierta (`papa_mesa`): las manos quedan encima y la mesita propia desaparece.
- Pieza que trae banco (Diego y Fer en el jardín): encuadre de la cintura para arriba con los pies FUERA de cuadro.
- Coordenadas leídas de la rejilla a ojo fallan (el frasco salió 0,12 corrido): en un plano con zoom, x = cx + (x_pantalla − 0,5)/z_rel.
- Corchetes con COMA («[angry, shouting]») no los quitaba `config._ETIQUETA` → Whisper comparaba contra el texto con la etiqueta y
  rechazaba tomas buenas (CER 0,26-0,52). Arreglado en nucleo/config.py el 21-oct (la coma entra en la clase).
- Whisper oye «leer el clima» como «el Tima» (dos tomas iguales) y «Fer» como «Fair»: ALIAS_QA, no regenerar.

## Archivos clave
- `PLAN_TALLER.md` (guion + diapositivas + fuentes) · `_prompts.py` → `prompts.json` · `guion.py` · `taller/` (index.html, _materiales.py, empaquetar.py)
