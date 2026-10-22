# Biblioteca de música (y de efectos) — reutilizar lo ya pagado (21-oct-2026)

Pedido del usuario (21-oct-2026): «hemos creado mucha música con Google, música que podemos reciclar para otros videos… crea una
biblioteca de toda la música que hemos hecho con etiquetas, para que la puedas reutilizar a futuro y no estar dependiendo todo el
tiempo de la API». Regla de cuándo usarla: `docs/apis.md` §2. Kit: `nucleo/musica_biblioteca.py`.

## Qué hay
- **Audio:** `E:\FabricaAnimaciones\musica_biblioteca\<id>.mp3` (copia de cada pieza de Lyria; los .wav pasan a mp3 320k) y
  `E:\FabricaAnimaciones\sfx_biblioteca\<id>.mp3` (los SFX de ElevenLabs de `videos/*/sfx/`). La copia sobrevive aunque se limpie
  o se borre el video de origen. Una pieza repetida en dos videos (mismo md5) es UN registro con `copias`.
- **Fichas:** `nucleo/datos/musica_biblioteca.json` y `nucleo/datos/sfx_biblioteca.json` (en git). Por pieza: id `<video>__<archivo>`,
  video, canal, estilo, tramo y escenas que cubría, el **prompt exacto** (de `audio/prompt_tramoN.txt` o del `LYRIA` de guion.py),
  secciones con intensidad, **etiquetas en español** (instrumentos, ánimo, género), medidas (duración, tempo, volumen, brillo,
  curva de energía en 12 puntos, huecos de silencio > 1,5 s), si es variante (`_b`, `corto`, `prueba`) y sus **usos**.
- **Catálogo legible:** `docs/musica_biblioteca_catalogo.md` (se regenera con `catalogar`; no se edita a mano).

## Comandos (`python fab.py biblioteca …` = `python nucleo/musica_biblioteca.py …`)
```
catalogar [--procs 8]                         solo lo nuevo: copia, mide, etiqueta y rehace el catálogo
reetiquetar                                   tras cambiar las tablas de etiquetas del kit (sin copiar ni medir)
buscar tierno piano cuna [--min 60] [--max 120] [--canal logia] [--excluir la_sena] [-n 12]
ver <id>                                      prompt completo, secciones, curva ▁▃▆█, huecos y usos
sugerir <video> [--excluir la_sena jalpa]     por cada tramo de LYRIA del video: las 5 que mejor casan (texto + duración + intensidad)
usar <id> <video> <tramo> [--desde 12.5]      deja videos/<v>/audio/lyria_tramoN.mp3 a la medida del tramo y anota el uso
sfx catalogar | sfx buscar plato roto | sfx usar <id> <video> [--nombre plato]
```
- `buscar` entiende español e inglés (tierno → tender gentle, cuna → lullaby, feria → fair waltz…; tabla `ES_EN` del kit).
- `usar` corta la pieza al largo del tramo + 3 s de cruce (con fundido de 2,5 s) o, si es corta, la repite con cruce de 3 s; la vieja
  `lyria_tramoN.*` queda como `_antes_lyria_tramoN.*`. `prompt_tramoN.txt` empieza con `BIBLIOTECA: <id>`. Luego
  `python ../../nucleo/lyria_tramos.py armar` (desde la carpeta del video) ajusta con `atempo` ±12 % y une los tramos como siempre.
- `--desde` elige otra parte de la pieza (mirar la curva de `ver`: si el tramo empieza tranquilo y la pieza arranca fuerte, entrar
  donde la curva está baja).

## Estado al crearla (21-oct-2026)
- **245 piezas · 476 min** de Lyria de 56 videos (+ 4 del sistema viejo en `D:\videosnuevos\cuentas_pendientes`) · 707 MB.
- **401 SFX** de ElevenLabs · 19 MB. Faltan, por ejemplo, un plato que se ROMPE (solo hay uno que se apoya): generarlo y catalogarlo.
- Etiquetas: se quitan antes el texto fijo de la plantilla de Lyria («keep the middle frequencies calm»…) y las frases negadas
  («No drum kit» no es percusión). «cálido» y «tenso» salen en muchas piezas porque los prompts los usan mucho: afinar con la curva.

## SFX en los videos dibujados por código: `SFX_ELEVEN` (el usuario, 22-oct-2026)
«Se repiten muchos SFX en varios videos» (Cronopapel, Bitácora, Sapiens, Kuriox…): el sintetizador de `nucleo/sfx.py` da la
MISMA onda en todos los videos (semillas fijas; `pop` sonaba 173 veces igual en historia_espana). Regla para TODO video nuevo
por código, en cualquier canal:
- En `guion.py`, `SFX_ELEVEN = {"pop": dict(prompt="…en inglés…", seg=0.6, variantes=3), "campana": ("…", 3), …}`. Cada
  nombre sustituye al sintetizado en TODOS sus eventos (también los que emite el kit: `snd="pop"`, transiciones `whoosh`),
  sin tocar las escenas; las variantes se turnan evento a evento. Un nombre nuevo que no exista en el sintetizador también vale.
- `python fab.py <v> sfx --seco` muestra qué sale de la BIBLIOTECA y qué se genera, y avisa (⚠) de los sintetizados más usados:
  declara al menos los que salgan ahí arriba. Sin `--seco`: copia de la biblioteca (anota el uso), genera el resto con
  ElevenLabs (`sound-generation`) y arma `audio/sfx.wav` como siempre (mismo LUFS y ducking en la mezcla).
- **No repetir ante el mismo público:** la biblioteca descarta lo que nació en el canal del video o ya se usó en él
  (`usos` con canal). Si una pieza elegida no casa con la escena, borrar el archivo de `sfx/` y poner `bib=False` en ese nombre.
- Al cerrar el video: `biblioteca sfx catalogar` (también lee los prompts de `SFX_ELEVEN` y arregla el canal de las fichas).
- Kit: `nucleo/sfx_eleven.py` (umbral de parecido 0,45). `sfx buscar … --canal <alias>` filtra igual que la producción.

## Criterio para elegir
1. Que el **ánimo y la intensidad** de las secciones casen con las escenas del tramo (la curva importa más que el instrumento).
2. Que el **largo** esté dentro de ±12 % (sin bucle ni recorte), o que sobre (se recorta) antes que falte (bucle).
3. **Sin huecos** de silencio internos (Lyria a veces los deja: `huecos` en la ficha).
4. **Público:** no repetir ante quien ya la oyó (`docs/apis.md` §2): `--excluir` los videos del mismo público; en el mismo canal, ni
   las piezas de sus últimos 5 videos ni el motivo reconocible de un video.
5. Si ninguna pasa de ~0,25 en `sugerir`, mejor Lyria nueva (con saldo) que una pieza que no cuenta la escena.
