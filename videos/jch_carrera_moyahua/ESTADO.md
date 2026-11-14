# ¿Cerrar la carretera por una carrera de motos? (reel vertical) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: ninguno · Facebook, perfil de Juchipila de Edson (lo sube él; o la página «Que pasa en Juchipila» SOLO con su aprobación) · antes del dom 15-nov-2026
- estilo: SECUENCIA YT en VERTICAL (clips reales por beat, recorte 9:16) + kit propio `kit_jch.py` + pegatinas + rótulos · formato DEBATE neutral
- etapa: ✅ MASTER listo (salida/jch_carrera_moyahua_MASTER.mp4, 3:00, −14 LUFS) · enviado al celular por Rayo y recibido · esperando el visto bueno de Edson para Facebook (salida/post_facebook.md) · 10-nov-2026
- siguiente: Edson lo revisa (tele) → si aprueba, publicar en su perfil o en «Que pasa en Juchipila» con salida/post_facebook.md (NUNCA sin su OK) → `fab.py jch_carrera_moyahua limpiar`

## Sesiones
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación, guion, voces, voz, tiempo, beats, mapa + kit | ◐ parcial 10-nov | corte por contexto a 180 mil |
| 2 | clips, efectos, música, render, MASTER | ✅ 10-nov | busquedas.json + medios revisados + efectos.py (kit_jch) + SFX + música de biblioteca + MASTER + texto del post |

## Decisiones (Edson, 10-nov-2026)
- tema: CAIN Road Race México 2026 (13-15 nov; CARRERA dom 15 desde el mediodía; km 78 Jesús María → km 105 Moyahua; 27.5 km, 97 curvas) y la polémica del cierre de la federal 23 (3-4 h)
- **EL NARRADOR NO TOMA POSTURA** (Edson): solo plantea los dos lados con datos; las opiniones las dicen las voces de postura (cintillo «POSTURA · EN CONTRA/A FAVOR» = `kit_jch.postura()`); el cierre pregunta. La balanza oscila sin decidirse.
- voces (todas mexicanas, elegidas por Edson): narrador Enrique M. Nieto `gbTn1bmCvNgk0QEAVyfM`; EN CONTRA Gabiyoya `iBGVhgcEZS6A5gTOjqSJ` (frases contra_0, contra_7); A FAVOR Marto `ojGau167OE7nUATM1xDa` (favor_0, 5, 6, 8). Muestras en audio/muestras_voces/.
- fotos/videos REALES de las curvas y bikers con crédito chico «Video: <canal>» (`kit_jch.credito`) en cada clip; caída = «imagen de archivo» (no es la del piloto de la nota)
- duración 3:00 (Edson pidió 2-3 min) · vertical para Facebook · fuentes en el docstring de guion.py

## Hecho
- guion.py (fuentes, neutralidad, VOZ_POR_FRASE, LYRIA), voz (ElevenLabs cuenta 2, ~1 300 créditos en total), seleccionar, tiempo, beats
- mapas/canon_base.png (OpenTopoMap z13) + _ruta.json (OSRM, tramo 27.2 km) + kit_jch.py: mapa_ruta() [marcas = inicio y fin del trazo], postura(lado), ficha(titulo, items ✓/✗), cifra(num, texto, sub), balanza(), credito(texto), hoja() de prueba. Probado en hojas.

## Clips (revisados en hojas 360p del scratchpad; usar en busquedas.json como {"url": "https://youtu.be/ID", "desde": s})
- 9nQiFRaa_Bs SanMykol onboard Jesús María–Moyahua (49-900 s, todo el tramo) · _2HqpvYxpQ0 Alice Reyes onboard (rótulos de curvas 112 «La Herradura», 273 «Las Palmas», velocímetro 600-750)
- iEVShIFfAxQ Las Rutas del Chris (piloto de cuero 73-120, grupo 255-270) · HOanpy2EGo8 (grupo 120-560; Los Burritos con motos 912-980)
- QlVO3wmW0co DD on the road (Los Burritos de Moyahua 765-850, DRON con decenas de motos 804-805) · 7DzxoV41Hik CASTA HRC 4K onboard curvas
- QtKiqBaPpcs INFO TV 9 rueda de prensa (Le Roy Barragán 45-106, Jorge Quiñones 116-207, mapa de la ruta 228-268, foto final 288)
- rCZEUvXwl8Y CAIN oficial Concordia (motos 9-15, banderas 21, público en curva 39-51, Guardia Nacional 70, curva 76, rodilla al piso 100, público 106, ambulancia/paramédicos 124, multitud 149-170) · BtEGl7aYdiU videoclip (curvas 64, 189)
- bE9qxBdOQtk Natanael (caída real 706-790, gente ayudando, sin heridos a la vista) · d-OqU-t6pME Rosy Rosy (Juchipila llena de motos y gente 200-340, 590-720)
- Reparto sugerido: gancho = onboard + rugido (ambiente_por); «que» = prensa/Concordia/mapa_ruta (FX pantalla en que_2-que_3, marcas «Jesús María» y «Moyahua»); contra = accidente, ficha hospital ✗, cifra 4 ambulancias, cifra 3/semana; favor = marshals/GN/ambulancia Concordia, ficha equipo ✓, cifra 15 000 espectadores, Burritos, Juchipila llena; balanza() en balanza; consejos con ficha; cierre con rótulo «¿DE QUÉ LADO ESTÁS?»

## Lecciones de este video
- E: estaba al 100 % (5 GB libres): copias de revisión al scratchpad en C:, en 1080p solo los tramos usados. No dejes fuentes enteras en E:.
- Whisper escribe «Moyagua»/«Aposol»: CER_MAX_POR_FRASE en guion.py (no es error de la voz).
- tts_eleven.cuentas() devuelve tuplas (n, clave).
- rCZEUvXwl8Y (Paul Desing Cain, no es el canal oficial) solo existe en 360p: sus 8 beats van en VENTANA 16:9 sobre el mismo video desenfocado (script en el scratchpad de la sesión 2, `ventana360.py`); BtEGl7aYdiU e iEVShIFfAxQ traen franjas negras: se quitan con cropdetect antes del recorte 9:16.
- Rótulos en vertical: «A / B» = dos líneas y `_ajusta()` de efectos.py los achica a 960 px; las fichas del kit crecen con cada dato (sin caja vacía).
- Música: Lyria sin saldo (402) → biblioteca: tramo 1 `lol_semana2__lyria_tramo10`, tramo 2 `arana_amarilla__lyria_tramo4` (se descartaron jalpa/apozol/juchipila: mismo público de Facebook). `ig_lyon_worlds__lyria_tramo1` era corta (8 s de silencio).
- Pendiente opcional: foto real del Hospital Comunitario de Juchipila y del hotel sede (Paraíso Caxcán, Apozol): hoy van con ficha y rótulo.
