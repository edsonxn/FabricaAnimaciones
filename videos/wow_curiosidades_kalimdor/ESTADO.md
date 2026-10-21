# 30 curiosidades de Kalimdor que casi nadie conoce (World of Warcraft Classic → Forever) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_warcraft · ~16 min · hueco dom 25-oct-2026 09:00 CDMX (15:00 UTC; `canales --actualizar` del 21-oct)
- estilo: secuencia_yt (gameplay de YouTube por beat + apoyos + pegatinas + pantallas + MG nuevos; SIN Overgear) → doc: docs/estilo_secuencia_yt.md
- etapa: ✅ SUBIDO y PROGRAMADO dom 25-oct-2026 09:00 CDMX (lE1SS7xJc_4) · miniatura + .srt + monetización activada
- siguiente: tras procesar la SD, Studio > Monetización: comprobar tipos de anuncio (pre/mid/post); medir a los 7 días (1-nov) contra Reinos del Este; luego `limpiar`

## Sesiones (plan de tramos · «continúa el video kalimdor» retoma aquí · protocolo docs/sesiones.md)
- alias: kalimdor, curiosidades de kalimdor, 30 curiosidades
- vista previa: NO (el usuario, 21-oct: «lo hago entero»); revisión con el rigor de siempre y aviso al subir
- leer al empezar: este ESTADO.md + `docs/estilo_secuencia_yt.md` (sin § Overgear) + de modelo `videos/wow_curiosidades_reinos_este/`
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | Investigación + guion (30 curiosidades, ~2 600 palabras) | ✅ 21-oct | 30 datos verificados en Wowpedia (docstring de `guion.py`); 2 679 palabras ≈ 16 min; ninguna frase > 200 c ni ≤ 4 palabras; FONETICA ~95 entradas |
| 2 | voz Applio + seleccionar + tiempo + beats + busquedas.json | ✅ 21-oct | 126/126 tomas (33 con CER_MAX por nombres; 10 frases con nombres oficiales es-MX de Wowhead; 1 reescrita); voz 835,7 s; video 926,9 s (15:27, +20,6 s de pantalla final); 108 beats |
| 3 | bajar todos los clips + revisar hojas `medios` | ✅ 21-oct | 108/108; 54 rehechos en 6 vueltas (webcams, marcas DCARR/Noob2Boss/Twitch, mapas quietos, WC3 ×3, Turtle WoW, retail «Midnight Falls», guía con recuadro); `recorte_por` 104; cámara en 101 |
| 4 | apoyos + pegatinas + pantallas + 2-4 MG nuevos (`fx hoja`) | ✅ 21-oct | 122 efectos + 4 rótulos; 7 hojas fx revisadas: 8 choques arreglados (pegatinas encimadas, linaje con panel vacío) |
| 5 | música original de WoW (zonas de Kalimdor) → mezcla → render → final → rigor MASTER → miniatura → subir y programar | ✅ 21-oct | -14,08 LUFS; MASTER v1 con 1 negro (013) y franjas (061) → rehechos → MASTER v2 limpio (blackdetect 0) 15:47; subido lE1SS7xJc_4 |

## Decisiones del episodio (preguntadas al usuario el 21-oct-2026)
- tema: «30 CURIOSIDADES de Kalimdor que casi nadie conoce (WoW Classic)» — secuela de Reinos del Este; la variable que cambia es la DURACIÓN (31 → 16 min)
- **SIN Overgear** (el usuario, 21-oct)
- **MÚSICA = bandas sonoras ORIGINALES de WoW de zonas de Kalimdor con yt-dlp (3-4 temas), NO Lyria** (el usuario, 21-oct; igual que Reinos del Este)
- orden: 30-28 rarísimas · 27-5 alternando poco conocida / popular · 4-1 rarísimas, la n.º 1 la más rara
- enfoque: Kalimdor de CLASSIC tal como llega a WoW Forever (4-nov-2026); Cataclysm solo para contrastar

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- (nada en curso)

## Hecho
- 4 MG nuevos en `nucleo/mg_wow.py`: runas, linaje, cadena, consola (documentados en docs/estilo_secuencia_yt.md)
- `nuevo --yt` (21-oct) · `canales --actualizar` (21-oct): antes que Warcraft se quedan sin video Cuerpo en Neón (vie 23) y Wild Next Door (sáb 24)

## Cómo retomar (comandos)
```
python fab.py estado wow_curiosidades_kalimdor
python fab.py wow_curiosidades_kalimdor voz | seleccionar | tiempo | beats | busquedas
python fab.py wow_curiosidades_kalimdor bajar           (rehacer: bajar 12,15 --rehacer | --q "otra búsqueda")
python fab.py wow_curiosidades_kalimdor medios          hojas previews/medios_NN.jpg (MÍRALAS)
```

## Archivos clave
- `guion.py`, `beats.json`, `busquedas.json`, `fuentes.json` (de dónde sale cada clip), `medios/`, `salida/creditos.txt`

## Lecciones de este video (solo lo no obvio)
- 16 min = 2 680 palabras con Applio (0,358 s/palabra de video incluidas pausas): el primer borrador salió de 3 215 (19 min).
- Nombres oficiales es-MX de Wowhead ANTES de la voz (Anaia Correalba, Cerellean Zarpablanca, Karna Tripirrem, kombobulador kodo).
- 50 % de clips rechazados: WC3, retail, Turtle WoW, gráficos de videos de lore, webcams, mapas abiertos; ver docs/estilo_secuencia_yt.md.
- Un plano de ambiente fijo se salva con CAMARA (acercamiento lento) en efectos.py (scene-061, scene-101).
- «Temas delicados» del cuestionario NO aplica a este video (no hay suicidio/abuso/autolesiones): responder por el contenido real.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO dom 25-oct 09:00 CDMX (lE1SS7xJc_4), miniatura y .srt; registrado en `canales/cronicas_warcraft.json` y BITACORA
- [x] HALLAZGOS documentados: docs/estilo_secuencia_yt.md (rechazos, nombres es-MX, CAMARA, MG nuevos, alfa en PIL), docs/publicacion.md (monetización)
