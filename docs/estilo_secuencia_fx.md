# Secuencia CON EFECTOS (videos sin canal; ideas para Plastitube y Wild Next Door)

_Creado el 7-oct-2026. Origen: el corto «Un segundo» (taller «Hablemos para entendernos», 2 min), hecho fuera de la Fábrica
en `C:\googleimagenes\scratch\taller_hablemos\video` y que al usuario le gustó «por cómo maneja los SFX, la voz y los efectos».
Su código original quedó en `docs/ejemplos/un_segundo/` (`armar.py`, `audio.py`, `prompts_video.txt`). Aquí está convertido
en parte del motor SECUENCIA: `nucleo/secuencia_fx.py` + `videos/<v>/efectos.py`._

Es el mismo motor de `docs/estilo_secuencia_flow.md` (imágenes y clips de Google Flow, uno por beat; **leer ese doc para
generar en Flow**), más una capa que hace que la imagen fija «actúe» lo que dice la voz.

## Qué tenía «Un segundo» que funcionó (la receta)
1. **Una imagen por frase**, y la imagen ilustra esa frase exacta (17 imágenes para 19 líneas en 2 min; ~5-7 s cada una).
2. **Cámara dirigida, no aleatoria**: cada toma dice de dónde a dónde va (entra de detalle a general, o empuja hacia la cara).
3. **Golpes sincronizados a la palabra**: en «un empujón» la cámara tiembla, salta un destello blanco y se acerca de golpe;
   en «el corazón a mil» la imagen late con viñeta roja; en «rebobinemos» pasan las imágenes anteriores al revés con rayas de TV.
4. **Color como emoción**: desaturar y viñeta oscura en lo grave, tinte cálido en la salida, sirena roja/azul en la ambulancia.
5. **Rótulos solo de énfasis** (regla global: sin subtítulos): 2-4 palabras enormes que entran con rebote («EL GOLPE FUE SUYO»,
   «UN SEGUNDO»), cápsula de lugar y hora al abrir, y tarjeta final con el título.
6. **Recursos de montaje baratos**: repaso (ráfaga de imágenes ya vistas), cortina diagonal «antes | después», REC parpadeando.
7. **Sonido en tres capas, todo de ElevenLabs** (`/sound-generation`, prompt en inglés + segundos):
   - *camas* de 22 s en bucle que cambian con el acto (guitarra tranquila → cuerdas oscuras → piano esperanzador), vol 0,30-0,50;
   - *ambientes* (patio de recreo) y *bucles dramáticos* (latido) entre dos frases;
   - *disparos* exactos en la palabra (empujón, golpe, asombro, notificaciones, sirena, rebobinado, respiro) y un **«boom»
     grave reutilizado** en cada rótulo o giro (5 veces en 2 min).
8. **Pausas escritas a mano** entre líneas (0,5 a 1,8 s): el silencio largo va antes del giro. En la Fábrica: `"pre"`/`"post"` por
   escena y `GAP` en guion.py; para una pausa larga, corta la escena ahí.
9. Voz ElevenLabs «Edoardo» (`VOZ = dict(motor="elevenlabs", voice_id="YqZLNYWZm98oKaaLZkUA", stability=0.42, style=0.4)`),
   frases cortas, con `previous_text`/`next_text` (ya lo hace `nucleo/tts_eleven.py`).

## Flujo
```
python fab.py nuevo <v> --secuencia        (la plantilla trae efectos.py de ejemplo)
python fab.py <v> voz | seleccionar | tiempo      o AUDIO EXTERNO: solo `tiempo` (abajo)
python fab.py <v> beats                    SECUENCIA: video_s=0, img_s=5-6 (una imagen por frase); comedia: img_s≈3 y fundido=0
   prompts.json -> python fab.py <v> prompts -> generar en Flow (servir + extensión; docs/estilo_secuencia_flow.md)
   escribir efectos.py
python fab.py <v> fx --seco                lista cada efecto/rótulo/sonido con su segundo (revisa anclas sin gastar)
python fab.py <v> fx                       genera los SFX que falten (ElevenLabs) -> sfx/*.mp3 y arma audio/fx.wav
python fab.py <v> fx hoja                  previews/fx_NN.jpg: un cuadro por efecto y rótulo (MIRARLA)
python fab.py <v> video [--tramo a-b]      aplica cámara, efectos y rótulos
python fab.py <v> mezcla | final           `mezcla` suma audio/fx.wav (música procedural y `sfx` clásico son opcionales: sin ellos no suenan)
```
Costo de SFX: ~40 créditos por segundo pedido (23 efectos, 2 camas de 22 s incluidas = 975 créditos el 7-oct-2026).
Un SFX ya generado no se vuelve a pedir; para rehacer uno, borra `sfx/<nombre>.mp3`. También puedes copiar ahí un mp3 propio.

## efectos.py (todo es opcional; formato completo en el encabezado de `nucleo/secuencia_fx.py`)
```python
CAMARA  = {"scene-003": dict(a=(1.05, 0, 0), b=(1.33, 0, .3))}        # (zoom, cx, cy); cx/cy -1..1 (1 = borde derecho/abajo)
FUNDIDO = {"scene-006": 0}                                            # corte seco al entrar a ese beat
FX      = [dict(tipo="temblor", en="un empujón", amp=34),
           dict(tipo="latido", de="En un segundo", a="suelta el golpe|fin"),
           dict(tipo="desaturar", beat="scene-007", k=.55, entra=1.2)]
ROTULOS = [dict(texto="UN SEGUNDO", en="Un segundo", tam=150, color="crema", y=.16),
           dict(texto="JALPA, ZACATECAS", en=1.5, a=6, tam=64, color="tinta", caja="amarillo", x=.2, y=.81)]
SFX     = {"boom": ("Deep cinematic sub boom hit with a long reverb tail", 4)}
PISTAS  = [dict(sfx="boom", en="Primer final", vol=.55),              # disparo
           dict(sfx="latido", de="En un segundo", a="suelta el golpe|fin", vol=.85)]   # bucle
```
- **Anclas**: segundo (`12.5`), beat (`"scene-004"`, `"scene-004:fin"`), **palabras de la voz** (`"el golpe fue suyo"` = cuando
  empieza; `"...|fin"` = cuando termina; `"...#2"` = segunda vez), con desfase `("un empujón", -0.15)`. Las palabras son las de
  `timeline.json` (lo que transcribió Whisper): si el ancla no existe, el comando lo dice y no arma nada.
- **Tipos de FX**: `temblor`, `destello`, `zoom`, `latido`, `vineta`, `desaturar`, `tinte`, `oscurecer`, `sirena`, `rec`, `tv`,
  `abre`, `cierra`, `fondo` (tarjeta de color), `imagen` (logo PNG), `repaso` (ráfaga de otros beats), `cortina` (antes | después).
- Rebobinado = `repaso` (beats anteriores en orden inverso) + `tv` + rótulo con `parpadea=2.5`.
- Tarjeta final = dar `"post": 7` a la última escena y poner `fondo` + rótulos + `imagen` en ese tramo.
- Nivel: `MEZCLA = dict(fx=-6.0)` en guion.py (dB de recorte de toda la pista). Meta: `mezcla` debe decir
  «relación voz/(música+sfx)» ≥ ~10 dB. Camas 0,14-0,20; disparos 0,4-0,9.

## Audio externo (animar un audio que ya existe)
`AUDIO_EXTERNO = "fuente/archivo.mp4"` en guion.py (audio o video) y `ESCENAS = [{"id": "audio", "frases": []}]`.
`python fab.py <v> tiempo` lo convierte, lo transcribe palabra por palabra (`voz/transcripcion.json`; corrige ahí a mano y
repite `tiempo`) y arma el timeline; `mezcla` usa el audio tal cual. No se corre `voz`, `seleccionar` ni `verificar`.
Si la GPU de voz está ocupada (`voz_gpu.lock`), espera: Whisper comparte la GPU.
Ejemplo: `videos/guason_fumado/` (sketch de 3 min, 56 dibujos).

## Estilo «animación fumada / sin presupuesto» (pedido del usuario, 7-oct-2026)
Dibujos exagerados y MAL HECHOS a propósito, como las parodias de Dragon Ball «sin presupuesto». Prompt de estilo que funcionó
(Nano Banana 2 Lite): *«Intentionally terrible low-budget parody cartoon frame, drawn in MS Paint with a computer mouse by an
amateur: wobbly uneven thick black outlines, crooked anatomy, wildly exaggerated ugly-funny facial expressions, off-model
characters, lazy flat color fills that miss the lines, plain almost empty flat-colored background…»*.
- No escribir «white paper look»: dibuja un marco blanco alrededor. Pedir «background color fills the entire image edge to edge».
- Personajes de marca: describirlos (traje, colores, rasgos) con un apodo en mayúsculas en vez del nombre.
- `fundido=0` (corte seco), `img_s≈3.2`, muchos `temblor` + `destello` en los gritos, SFX de caricatura (boing, mazazo,
  pedorreta, trombón triste, rayón de disco, grillos en los silencios) y una cama boba de pizzicato muy baja.
- Chistes subidos de tono: se sugieren (cara, estrella de impacto, rótulo «CENSURADO»), no se dibujan.

## Ideas para aplicar en Plastitube y Wild Next Door (no cambian su estilo; se suman con efectos.py)
- **Boom + rótulo de 1-3 palabras** en el gancho, en el cliffhanger de mitad de video y en la cifra clave.
- **Camas por acto** con ElevenLabs en vez de (o bajo) la música procedural: una por tramo emocional; el sonido propio de los
  clips de Flow (`ambiente`) se conserva.
- **Disparos por beat** en la zona de imagen, donde hoy no hay sonido propio: zumbido, crujido de hielo, engranes, vapor.
- **Cámara dirigida** en los beats importantes (empujar hacia el objeto estrella, abrir de detalle a general) y `latido`/`vineta`
  en los momentos de riesgo; `repaso` para recapitular antes del cierre circular.
- Probar primero en un tramo: `python fab.py <v> video --tramo 0-40`.
