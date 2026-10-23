# Los Duos — anuncio vertical 45 s — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: ninguno (cliente: grupo musical Los Duos) · se publica en Facebook/Instagram Reels + estados de WhatsApp
- estilo: anuncio vertical con VIDEOS REALES del grupo + motion graphics por CÓDIGO (Mundo(Escena), como duo_promo) → docs/estilo_app_promo.md
- etapa: v2 verificada — esperando revisión del usuario (sin Juchipila; 3 pausas de 9-10 s con el grupo cantando + 5 s de canto al final; 86 s)
- siguiente: cambios que pida el usuario (`video --rehacer t0-t1` + `final`); al aprobar: `limpiar`, catalogar SFX, commit

## Sesiones (plan de tramos · «continúa el video duos_promo» retoma aquí · protocolo docs/sesiones.md)
- alias: Los Duos, anuncio de Los Duos, duos_promo
- vista previa: el guion antes de la voz
- leer al empezar: este ESTADO.md
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | material revisado, decisiones, muestras de voz | ✅ 22-oct | 6 voces de locutor; eligió la 2 (Zabra) |
| 3 | v2: frase de zona nueva (35 créditos), guion.PAUSA, popurrí con canto en pausas, ecualizador, mapa solo Ags → render (6,5 min) → final → verificar | ✅ 22-oct | MASTER 86 s 167 MB + WHATSAPP 19 MB |
| 2 | guion → voz (Zabra, 327 créditos) → clips → kit + escenas → popurrí Demucs → SFX → mezcla → render (11 min) → final → verificar | ✅ 22-oct | MASTER 56 s 105 MB + WHATSAPP 720p 11 MB; rigor: hoja cada 2,8 s y cambios de escena sin bloqueos |

## Decisiones (preguntadas al usuario el 22-oct-2026)
- duración: 45 s · vertical 1080x1920 · profesional, con narrador y PRECIO POR HORA en pantalla
- imagen: los 4 clips reales de fiestas (baja resolución 360-476 px: escalar, corregir color, fondo desenfocado, marcos y textos animados)
- música: SOLO las canciones grabadas por el grupo (audios de WhatsApp en `material/`), nada de Lyria: **varios tramos de las distintas piezas** (popurrí, ver Falta)
- voz: ElevenLabs **Zabra** `9XaoraKgpXhItOQktYsV` (locutor joven de radio comercial mexicana), `eleven_v4` con corchetes
- entregas: MASTER 1080x1920 + copia liviana para estados de WhatsApp (`comprimir-video`)

## Material (`E:\FabricaAnimaciones\videos\duos_promo\material\`, copia de Downloads\LosDuos)
- Audio 10.43.31 (3:18) cumbia «La indita» · 10.43.54 (6:09) sin letra clara · 10.44.13 (2:50) corrido de Teodora («vestido entallado») · 10.44.33 (4:28) sin letra clara
- Video 10.45.14 (53 s) salón con globos, gente bailando, tecladista Yamaha PSR · 10.45.15 (69 s) salón grande con mesas, mucha gente
- Video 10.45.16 (40 s) terraza con columnas amarillas, parejas bailando, tecladista Yamaha de camisa oscura · 10.45.17 (51 s) patio de noche, señoras bailando
- `muestras_voz/`: las 6 muestras (558 créditos, cuenta 3)

## Datos del cliente (usuario + post de Facebook, 22-oct-2026)
- Se vende como **TECLADISTA Y DOS VOCES** (el usuario, 22-oct; el póster dice percusionista) · **1 200 MXN la hora** (sin mínimo, pero NO decirlo en el anuncio) · WhatsApp **449 306 5431**
- Facebook: «Grupo Los Duos» https://www.facebook.com/profile.php?id=61578884111497
- Géneros: cumbias, norteño, zapateado, banda, balada, grupera, balada pop, mariachi, rock · eventos: privados, fiestas, bodas, XV años, cumpleaños, reuniones familiares
- Zona: **Aguascalientes y municipios a la redonda + Juchipila, Zacatecas, y alrededores** (el usuario, 22-oct)
- Logo: NO hay archivo original (el póster de Facebook es IA) → rehacer «Los Duos» por código en cursiva dorada
- Lemas: «Música que alegra tus momentos» · «La música hace mejores momentos» · identidad del póster: negro + dorado, logo «Los Duos» en cursiva dorada, iconos de colores

## Plan visual por escena (guion en guion.py, ~110 palabras)
- gancho: clip de baile (patio de noche / salón) con cámara que empuja + «¿TIENES FIESTA?» gigante; golpe de percusión
- grupo: tecladista con su Yamaha (video 10.45.16, final) en marco dorado + rótulo «TECLADISTA + 2 VOCES»
- generos: ráfaga de píldoras con icono por género (como el póster) sobre clips de baile cortados a ritmo
- eventos: 3 cortes rápidos (salón con globos, salón grande con mesas, terraza) con rótulo por evento
- zona: mapa con relieve real (ETOPO1, como Cronopapel) de Aguascalientes → Juchipila con pines dorados que se encienden
- precio: fondo negro/dorado, «$1,200» gigante que cae con destellos + «POR HORA» (sin «sin mínimo»)
- contacto: icono WhatsApp + 449 306 5431 grande, botón que palpita
- cierre: logo «Los Duos» dorado + lema; la canción del grupo sube al terminar la voz

## Falta
- [ ] aprobación del guion → `python fab.py duos_promo voz`
- [ ] música = **popurrí de VARIOS tramos de las 4 piezas del grupo** (el usuario, 22-oct): elegir tramos con ritmo (sin letra encima de la voz o muy bajos), unirlos con cortes a tempo/golpe de percusión en los cambios de escena (p. ej. un tramo por bloque: gancho+grupo, géneros, eventos, precio+contacto, cierre con la pieza más festiva subiendo)
- [ ] logo rehecho por código (cursiva dorada, notas musicales)

## Entregables
- v2: `salida/los_duos_anuncio_MASTER.mp4` (1080x1920, 86 s, -14 LUFS) · `salida/los_duos_anuncio_WHATSAPP.mp4` (720x1280, 19 MB)

## Lecciones de este video (solo lo no obvio)
- Anuncio de grupo musical: el cliente quiere OÍR al grupo → pausas de 7-10 s sin narrador con una frase cantada completa; la escena anterior lleva el instrumental de la misma pieza para que el canto entre sin corte (`guion.PAUSA` + `post` en la escena).
- Canciones del cliente con voz bajo el locutor: Demucs `--two-stems vocals` (ya instalado, GPU, ~1 min por 4 canciones) → instrumental bajo la narración y la mezcla completa entra al callar el locutor.
- La mezcla del núcleo exige 48 kHz en audio/musica.wav y audio/fx.wav.
- Zona segura de Reels: nada importante debajo de y ≈ 1550 ni arriba de y ≈ 200 (descripción y botones de la app).
- El mapa ETOPO1 (1') a escala de municipios se ve pixelado: suavizar la altitud (σ 4,5 px) y sombreado fuerte + curvas de nivel doradas lo vuelve «estilo» en vez de defecto.
- Búsqueda de voces: `GET /v1/shared-voices` con `language=es&gender=male` (+`accent=mexican` / `use_cases=advertisement`); el parámetro `sort` la deja vacía.
