# La historia de Aguascalientes — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronopapel · **PROGRAMADO sáb 7-nov-2026 14:00 CDMX** (https://youtu.be/VTdzWTuzrLg, publishAt 2026-11-07T20:00:00Z) · Facebook «Historias Perdidas de México» PUBLICADO 22-oct (fb 980974675052533)
- estilo: boceto → doc de estilo: docs/estilo_boceto_guache_mapa.md § «Dibujos en Flow» · ejemplo a copiar: videos/historia_jalisco/
- etapa: subido (privado programado; miniatura y .srt cargados) + publicado en Facebook
- siguiente: a los 7 días de publicado medir con `yt metricas cronopapel` y anotar en canales/formula/cronopapel.md (prueba: voz ElevenLabs + 13 min + lugares); al aprobarlo, `python fab.py historia_aguascalientes limpiar`

## Sesiones (plan de tramos · «continúa el video aguascalientes» retoma aquí · protocolo docs/sesiones.md)
- alias: aguascalientes, historia de Aguascalientes
- vista previa: NO render parcial; el usuario revisa por escenas en el 🎞 Montaje del panel (`fab.py historia_aguascalientes montaje`)
- encadenado: el usuario eligió seguir de corrido en una sesión (plan MAX), con checkpoints aquí tras cada tramo
- leer al empezar: `_hechos.md` (fuentes, [HECHO]/[LEYENDA], fotos de Commons), `guion.py` (FOTOS, SFX_ELEVEN)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion + voz + tiempo + kit (mapa Ags) + hojas Flow + fotos | ✅ 22-oct | encadenado en una sesión |
| 2 | coreografía (4 tramos en paralelo) + montaje | ✅ 22-oct | |
| 3 | (fusionado con 2) | ✅ | |
| 4 | sfx → música → mezcla → render → rigor (1 arreglo, 76-87 s) → miniatura → YouTube → Facebook | ✅ 22-oct | MASTER CER 0,08 % |

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- 22-oct ~12:00: voz ✅ 98/98 (ElevenLabs Alberto, 740,9 s, ~4 200 créditos; saldo cuenta 3 ≈ 28 000) · timeline ✅ 785,4 s (13:05)
- kit copiado; MAPA lo adapta un subagente (mapa.py, datos/, `_mapa_notas.md` al terminar) · FOTOS ✅ (`fotos/`, `foto_peg.py`, `fotos/LEEME.md`;
  sustituir en guion.FOTOS: colonia_1 → Fachada_de_la_Catedral_de_Aguascalientes_01.jpg, siglo20_3 → El_Cristo_Roto,_San_José_de_Gracias,…jpg)
- Flow ✅ 14/14 hojas, 2K en `hd/` (1K en `hojas/`), recortadas en `piezas/` (MAPA ✅ por subagente: `_mapa_notas.md`; escenas.py umbral z 2,2-5,5).
  Piezas (NN): 01 chichimecas 0 arquero guachichil·1 guamar lanza·2 madre·3 cazador venado·4 sacerdote gigante·5 fogata·6 nopal+mezquite·7 roca pintada
  | 02 plata 0 carreta plata·1 soldado arcabuz·2 presidio·3 mula·4 minero·5 jinete chichimeca·6 rueda flechas·7 plata
  | 03 fundación 0 oidor·1 colono·2 colona·3 carta sello·4 poza termal·5 jacal·6 cruz·7 estandarte Virgen
  | 04 colonia 0 catedral·1 palacio·2 San Marcos·3 cura·4 novios·5 mina·6 túnel agua·7 Cristo columna·8 vaca·9 vacas·10 vaquero
  | 05 xix 0 Santa Anna·1 dama·2 caballero·3 baños·4 tina·5 cadena·6 escudo labios·7 puesto feria·8 jardín balaustrada
  | 06 arte 0 grabador·1 prensa·2 catrina·3 calavera baila·4 hoja volante·5 pintor·6 cuadro diosa·7 cempasúchil
  | 07 porfiriato 0 locomotora·1 humo·2 humo·3 ferrocarrilero·4 taller·5 fundición·6 escoria·7 teatro·8 templo S.Antonio·9 arquitecto
  | 08 revolución 0 Villa·1 Obregón·2 zapatista·3 bandera firmada·4 discuten·5 adelita·6 Eulalio·7 tribuna
  | 09 s.XX 0 presa·1 campanario inundado·2 Cristo Roto·3 lancha·4 uvas·5 barrica·6 guayabas·7 guayabo·8 motor·9 coche·10 INEGI
  | 10 turismo 0 turista·1 familia globo·2 tina pato·3 mariachi·4 rueda fortuna·5 charro·6 letrero·7 autobús
  | ciclos: 11 chichimeca corre (8) · 12 soldado marcha (8) · 13 carreta camina (6; pieza 6 = jacal suelto) · 14 villa galope (6)

- COREOGRAFÍA: `coreo_1.py` ✅ revisado 0-203 s (previews/c1a…c1f) · `coreo_3.py` ✅ 420-641 s (rev_c3_*; pendiente rigor: 466-469 s algo vacío; SFX `balazos` añadido) · `coreo_4.py` ✅ 641-785 s (rev_c4_*; SFX fabrica/terremoto añadidos).
  DATO CORREGIDO: Ags tiene 11 municipios (no 12): frase siglo20_10 regenerada (56 créditos), timeline igual 785,4 s, música rearmada.
  `coreo_2.py` ✅ 204-419 s (rev_c2_*). SFX ✅ 214/247 eventos con efectos propios (43 ElevenLabs ≈ 700 créditos + 7 biblioteca; saldo ≈ 26 500).
  Flechas → ← no existen en la fuente: quitadas. Nota: la Presa Calles se ve como agua en el mapa base también antes de 1927 (menor). `coreo_2/3/4.py` los terminan 3 subagentes (brief `_brief_coreo.md`;
  se cortaron por el límite a las ~13:00 y se reanudaron): al recibirlos, `py_compile`, hoja `./run.sh _hojas.py 3 204 785`, revisar, y añadir
  a SFX_ELEVEN los SFX nuevos que pidan. `escenas.py` carga cada coreo con try/except; `_prueba.py --out=<nombre>`.
- MÚSICA ✅ `audio/musica.wav` 785,4 s: 6 tramos (LYRIA en guion.py); 1-3 de la BIBLIOTECA (apozol_tramo2, juchipila_tramo4, juchipila_1;
  usos anotados), 4-6 Lyria nueva (≈ 0,24 US$). Al cerrar: `biblioteca catalogar`.
- Después: `fab.py historia_aguascalientes montaje` (el usuario revisa en 🎞 Montaje) → sfx --seco → Lyria (biblioteca sugerir) → mezcla → render.

## Hecho
- Investigación con fuentes en `_hechos.md` (34 fotos de Commons con licencia comprobada).
- Guion: 14 escenas, historia en orden + curiosidades + lugares visitables + ruta final; 22 FOTOS reales asignadas por frase.

## Falta
- [ ] voz, seleccionar, tiempo · [ ] kit + mapa de Aguascalientes · [ ] hojas Flow (épocas: chichimecas, colonia, s. XIX, Porfiriato, Revolución, s. XX) · [ ] fotos bajadas
- [ ] coreografía 14 escenas · [ ] SFX_ELEVEN completo · [ ] Lyria (biblioteca sugerir) · [ ] render + rigor · [ ] miniatura · [ ] subir

## Lecciones de este video (solo lo no obvio)
- Primer Cronopapel con voz ElevenLabs (Alberto Rodríguez) y con SFX_ELEVEN.
- No afirmar: túneles de la capital (sin fuente), El Ocote y Museo Nacional de la Muerte como visitables, fecha exacta del Teatro Morelos.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO (7-nov), miniatura, registrado en canales/cronopapel.json y BITACORA; Facebook publicado
- [x] HALLAZGOS en docs/estilo_boceto_guache_mapa.md § «historia_aguascalientes»
- [x] `biblioteca catalogar` y `biblioteca sfx catalogar`
