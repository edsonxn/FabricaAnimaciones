# Las 5 peores atrocidades de Malenia QUE IGNORASTE — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: runa_caida · PROGRAMADO jue 29-10-2026 10:00 CDMX (2026-10-29T16:00:00Z) · https://youtu.be/3qrJnRE6ol4
- estilo: secuencia_yt (gameplay de Elden Ring por beat + PEGATINAS + imágenes a pantalla + MG NUEVOS `nucleo/mg_er.py`; sin patrocinio) · voz Chatterbox Faraon → doc: docs/estilo_secuencia_yt.md § Runa Caída
- etapa: programado (subido private el 23-oct con miniatura; .srt sin cargar)
- siguiente: .srt a mano en Studio · a los 7 días (5-nov) métricas vs Miquella/Ranni · si llega reclamo de Content ID por el OST, anotarlo en la fórmula

## Sesiones (plan de tramos · «continúa el video malenia» retoma aquí · protocolo docs/sesiones.md)
- alias: malenia, atrocidades de malenia
- vista previa: como Miquella (el usuario, 18-oct): MASTER directo, revisado con hojas de cuadros + barrido de negros/quietos
- leer al empezar: este ESTADO.md · `videos/er_miquella_atrocidades/guion.py` (estructura) · docs/estilo_secuencia_yt.md § Runa Caída
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion + voz Faraon + seleccionar + tiempo | ✅ 22/23-oct | 121 frases, voz 1 139 s, video 19:14 (+ pantalla final) |
| 2 | beats, búsquedas, clips, pegatinas, pant(), mapas, fichas/MG mg_er NUEVOS | ✅ 23-oct | 134 clips (37 rehechos en 3 rondas), 129 efectos |
| 3 | música OST, SFX, mezcla, render, revisión, miniatura, subida private + programar | ✅ 23-oct | MASTER 2 (19:34) sin negros ni quietos; CER 0,76 % |

## Decisiones del episodio (22-oct-2026, elegidas por el usuario)
- tema: Malenia (gemela de Miquella; sigue del video que explotó: 4 786 vistas en 2 días ≈ ×48 de la mediana del canal)
- duración ~20 min como Miquella (copia del ganador cambiando UNA variable: el sujeto)
- NO repetir lo ya contado: Aeonia vs Radahn + Yelmo del joven león (Miquella p3), «espada de Miquella», esperó al pie del
  capullo, perdió brazo/pierna/ojos (Miquella p1b), «hijos de un solo dios» y la Gran Runa «debió ser la más sagrada» (Radagon)
- gancho de comentarios del Miquella: «¿Malenia también estaba hechizada por Miquella?» (responderlo en el video)
- VOZ: nombres propios que Whisper escriba mal (Miqueya, Moj) = error REAL, regenerar (lección del 22-oct)

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- (nada: video cerrado el 23-oct)

## Hecho
- MASTER 1 → 2: negro de 0,3 s (scene-113 Maiko @300 → @318) y 3,9 s quietos al final del mapa de Finlay (cortado); p2_1 «mi Isent» →
  toma s1 «Millicent» (cambiar_toma: misma duración, x1,014) · subido https://youtu.be/3qrJnRE6ol4 · música: audio/ost/ + armar_musica_ost.py
- proyecto creado (`nuevo --yt`), canal corregido a runa_caida
- guion.py: 121 frases, 3 157 palabras (≈ 1 090 s de voz ≈ 19:30), 12 escenas pN/pNb; citas verificadas (lista en el docstring)
  · puestos: 5 invicta (Godrick, robo de vida, Gran Runa) · 4 sus caballeros (armadura, O'Neil, Finlay, parientes) · 3 Caelid
  (monumento, Aeonia escarlata, Gideon, Jerren) · 2 Millicent y hermanas (Gowry, «como hizo tu madre», la aguja) · 1 la tercera
  flor + respuesta al comentario del hechizo («no estaba hechizada: estaba de acuerdo»)
- voz: 242 tomas (semillas 1-2) + 6 de Radahn (3-5); 50 marcadas, 20 errores reales apartados en voz/_descartes/
  (ver comentario en guion.py); umbrales por frase para el resto; ninguna toma viva con «Miqueya/Malemia/Ladan»
- clips: url+segundo fijados a mano (SourceSpy91 Caelid/Haligtree/Elphael/Redmane, pelea de Malenia, Kelvyn Acevedo para Millicent);
  rechazados: Gamerpillar (rótulos «STEP N» en TODO), menús, «LOST GRACE DISCOVERED», DRAKULUS; recorte .09 Shirrako y ClipPlayTru
- efectos.py: ~60 pegatinas, 30 fichas, 11 pantallas, MG nuevos `juramento/contagio/floraciones/repudio` (mg_er), mapas mundo
  (viaje de Finlay) y Caelid (ventana, pantano de Aeonia), 5 SFX nuevos, cámara lenta en 7 diálogos quietos

## Falta
- [x] mapas reales (Finlay en el mundo; Aeonia en Caelid). La ruta de Millicent NO: sin coordenadas fiables de iglesia/choza

## Lecciones de este video (solo lo no obvio)
- clips: Gamerpillar («Millicent Full Questline») trae rótulos «STEP N» en TODOS sus clips → descartado entero; para Millicent sirvió
  Kelvyn Acevedo (G9M10gpYQnY, sin comentarios) y SourceSpy91 Part 20 Caelid (capítulos: O'Neil en 9225). Mirar capítulos con
  `yt-dlp --print "%(chapters)j"` antes de fijar segundos: ahorra rondas.
- revisión MASTER 1: un fundido a negro de 0,3 s DENTRO del video de origen (Maiko @300, cinemática → pelea) y 3,9 s quietos al final
  del mapa de ruta (la cámara del mapa casi no se mueve cuando la ruta ya llegó: cortar el mapa ~1,5 s tras la última marca).
- en Git Bash, ffmpeg sin `-nostdin` se queda colgado esperando la entrada (parecían clips «dañados»): usar `-nostdin` o PowerShell.
- Faraon con FONETICA: «Mikuéla» → Whisper «Mikuela/Miquela» (bien); «Rádan» tras «a»/«de» a veces sale «Ladan/arladan»:
  regenerar con otras semillas; una CER baja (0,019) puede esconder «carme/escalata» si la otra toma pasa: buscar con regex
- esperar «GPU libre» mirando procesos: `fx` (`-m secuencia_fx`) y `bajar` NO usan GPU; mirar `nvidia-smi` (VRAM) en vez de nombres
- `nuevo --yt` deja la plantilla de Warcraft (Applio, Overgear, canal cronicas_warcraft): para Runa Caída copiar config de Miquella

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/<alias>.json`, BITACORA)
- [x] HALLAZGOS y mejoras documentados en el manual/estilo (ver CLAUDE.md «CIERRE DE VIDEO») → docs/estilo_secuencia_yt.md (Malenia, MÚSICA OST), mg_er (4 MG), CLAUDE.md
