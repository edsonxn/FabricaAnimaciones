# Estilo «terror CRT» — terror de videojuegos en 2D oscuro (horizontal 16:9)

_Nació en `videos/terror_ben_drowned/` (12-oct-2026, 67 s, 1920x1080, sin canal: prueba de estilo para un canal de terror y sucesos
raros en videojuegos). Pedido del usuario: «estilo oscuro 2D de terror; usaremos yt-dlp para gameplays, así que el video real debe
combinar con el estilo: mostrarse en una tele vieja hecha en 2D o de formas distintas, siempre»._

## Idea
- **El cuarto y la pantalla.** Cuarto a oscuras cuya ÚNICA luz es una tele CRT dibujada en 2D; delante, la silueta de espaldas de quien
  juega. El video real del juego (yt-dlp) **nunca va suelto**: vive dentro de la tele (curvatura, scanlines, tracking de VHS,
  aberración cromática, grano). Cuando hay que mostrar «algo que no es del juego» (marcador, foro, agua) también es una pantalla dibujada
  dentro de la tele.
- **La luz sale de la pantalla.** El cuarto se dibuja «sin luz» (`cuarto_albedo`) y `iluminar()` lo multiplica por la luz de la tele; su
  color y su brillo salen del color medio de la propia pantalla (`color_medio`): lo que pasa en el juego tiñe el cuarto.
- **Plano secuencia.** La cámara (`camara(t)` con fotogramas clave) va del cuarto entero a «dentro de la pantalla» (z≈2.75, el tubo
  llena el cuadro) y vuelve. La corrupción del juego se sale de la tele (tiras aditivas, tarjetas de video/web/chat que flotan afuera,
  pantallitas de lectores en la pared) y el cierre es siempre en el cuarto: **algo entró al cuarto** (aquí, la silueta de la estatua
  detrás del jugador, que gira la cabeza).
- **Color con significado:** frío verde-azulado = tele/mundo real; rojo sangre (`SANGRE`) = SOLO lo que está mal (marcador del día 4,
  «VACÍO», el nombre del niño); hueso (`HUESO`) = rótulos. Todo lo demás, casi negro.
- Reglas de la casa: sin subtítulos quemados (los rótulos «SEPTIEMBRE 2010», «JADUSABLE», «MILLONES» son énfasis, en serifa `Baskervville`);
  voz ElevenLabs con corchetes (`[whispers]`, `[serious]`…); música Lyria de terror incómodo; SFX de ElevenLabs anclados a las palabras.

## Dónde vive el kit (promovido a `nucleo/` el 13-oct-2026)
Los videos NUEVOS no copian nada: `import terror_crt as T` · `import terror_pc as X` (monitor de PC) · `from terror_pix import ...`
(y `anclas.py` + `fx_audio.py` propios de cada video). `nucleo/terror_pix.py` = `pix.py` de Ben (mismas funciones) · `terror_crt.py` =
`terror.py` de Ben · `terror_pc.py` = extensión PC de Sonic.exe (ver § «Variante monitor de PC»). `videos/terror_ben_drowned/` conserva
sus copias locales (video cerrado; no tocar). Las anclas `ww/INI/FIN` leen el `timeline.json` del cwd: siempre se importa desde el video.

## Archivos del kit original de Ben (copiados en `videos/terror_ben_drowned/`; para videos nuevos usa los de `nucleo/`)
- `pix.py` — pintor de `mods_ia_fusion` con `P(w, h)` (búfer de cualquier tamaño: la pantalla de la tele es un `P(1216, 912)`), `ww` (anclas por palabra), `acabado` (bloom, aberración, glitch, viñeta), `Clip` (extractos de `clips/*.mp4`).
- `terror.py` — el kit:
  - **CRT:** `crt(img, t, glitch, tono)` (remap de curvatura, tracking, bandas corridas, scanlines, bloom, grano, viñeta), `ruido_tv`, `color_medio`.
  - **Pantallas dibujadas** (búfer `SWxSH`): `pant_archivo` (selección de archivo con el nombre «BEN»), `pant_hud_dia` (marcador que salta al día 4), `pant_agua` (niño que se hunde), `pant_foro` (tablero en verde de terminal), `pant_clip` (video real a 4:3 en bucle).
  - **Cuarto:** `cuarto_albedo`, `iluminar`, `ventana` (luna + cortinas), `tele` (caja, antena, mesa, LED), `consola` + `cartucho`, `cartel_garaje`, `luz_suelo`, `polvo`.
  - **Siluetas** (casi negras con luz de borde): `jugador` (de espaldas, gira la cabeza), `estatua` (figura de capucha puntiaguda, ojos que brillan).
  - **Cierre:** `tarjeta` (video/web/chat que salen de la tele), `pared_pantallas`.
- `anclas.py` — todos los `a_*` (segundos de cada palabra) en un sitio: lo importan `escenas.py` y `fx_audio.py`.
- `escenas.py` — una sola clase `Mundo(Escena)`; `pantalla(t)` decide qué hay en la tele en cada tramo; `cuadro(t)` arma cuarto + cámara + rótulos. `guion.TRANSICIONES = [("continua", 0.5)] * n`.
- `fx_audio.py` — `SFX` (prompts) + `PISTAS` (sonido, segundo, volumen) → `audio/fx.wav`. `_hoja.py` — hoja de cuadros (`python _hoja.py 8 28.6 34.6 -f --out h`).

## Video real (yt-dlp)
- Elegir con hoja de contacto de ffmpeg (`fps=1/2,scale=320:-1,tile=6x3`) y anotar el tramo en `pant_clip(nombre, seg, ini, fin)`. **Mirar el tramo de verdad antes de anclarlo a una palabra** (el clip «elegía» resultó ser solo un logo; se tiró).
- Siempre ≤ ~8 s por uso, con el crédito del autor (`clips/creditos_clips.json`), y avisar al usuario del riesgo de derechos de los extractos de YouTube.
- Recorte 4:3: un 16:9 pierde los lados; el HUD del juego queda en los bordes. Los juegos de 4:3 (N64/PS1) llenan la tele sin recorte.
- La traba (`seg` cuantizado) + `glitch` + `golpe` dan la sensación de «el juego falla» sin tocar el clip.

## Mezcla y cifras de la prueba
- Render ~1 s/cuadro (pantalla 1216x912 con `remap` + bloom + cuarto 1920x1080 con iluminación).
- `MEZCLA = dict(musica=-20, sfx=-24, fx=-17)`; relación voz/fondo 13,1 dB; −14 LUFS.
- Costos ElevenLabs: voz 95 créditos + 1 regeneración (12); 15 efectos 322 créditos.

## Errores a no repetir / mejoras
- Flash de pantalla completa > 0,15 deja el cuadro gris y lava el negro (el terror vive en el negro): usar ≤ 0,15 salvo golpes de 0,2 s.
- El `glitch` global de `acabado` corre filas fuera de la tele: dejarlo en `gl*0.18`; el glitch fuerte va DENTRO de la pantalla (`crt`).
- Texto dentro de la tele con glitch alto se vuelve ilegible (letras del diálogo): bajar el glitch donde haya texto que leer.
- Escenas oscuras (agua) se comen el contraste con el CRT: subir la paleta del búfer antes de pasarlo por `crt`.
- Pendiente: promover el kit a `nucleo/`, segunda pantalla (monitor de PC / consola portátil / arcade) para variar el empaque entre videos, siluetas de más personajes y una estatua mejor dibujada.

## Miniatura (Crónicas del gaming = Flow, Nano Banana 2.1 CON el texto dentro; el usuario, 13-oct-2026)
- **La miniatura del canal se hace en Flow, no por código**, y el **título lo pinta el propio modelo**: Nano Banana 2.1 escribe
  texto en español muy bien (en `sonic_exe` salió «NUNCA EXISTIÓ» con tilde, bien a la primera en las 2 imágenes, y además
  «SONIC.EXE» a rotulador sobre el CD). No hace falta sobreponer Impact con PIL.
- Por qué no el cuadro del video: los cuadros del terror CRT son casi negros a propósito; subidos de niveles se queman y pierden
  la identidad del personaje (la cara del demonio quedó naranja genérico). La de código (`miniaturas.py`) queda solo de respaldo.
- Receta (navegador integrado, sesión de la cuenta Edsonxn; si pide iniciar sesión, pedírselo al usuario): proyecto nuevo →
  dejar el chip por defecto **Imagen · 16:9 · Nano Banana 2.1 · x2** (consumió 0 puntos) → `execCommand('insertText')` + `Return`
  real → ~35 s → bajar las URLs `flow-content.google/image/...` con curl (1376x768) → recorte centrado a 16:9 → 1280x720 →
  mirar también a 320x180.
- Prompt que funcionó (entero en `videos/sonic_exe/prompt_miniatura.md`): (1) «YouTube thumbnail, cinematic
  horror illustration, 16:9»; (2) el empaque del video: cuarto a oscuras cuya única luz es el monitor/tele CRT, que ocupa el
  **60 % derecho**; (3) el monstruo en primerísimo plano DENTRO de la pantalla, mirando al espectador, con el rasgo icónico
  (ojos negros que sangran, pupila roja, sonrisa); (4) el objeto del relato en primer plano abajo-izquierda con su rótulo
  (el CD-R «SONIC.EXE», el cartucho…); (5) el título: «a huge two-line title in heavy condensed bold sans-serif capitals with
  a thick black outline…: first line the word X in white, second line the word Y in bright blood red, spelled exactly
  E-X-I-S-T-I-Ó with an acute accent on the final O», «fully inside the frame… does not overlap the monitor screen»;
  (6) «No other text, no logos, no watermark, no border».
- Personaje con marca: describirlo («corrupted cartoon blue hedgehog video game mascot»), no nombrarlo; el nombre solo va como
  rótulo del objeto. Elegir la variante donde la cara NO se corta por el borde (una de las dos lo hacía).
- Texto: 2 palabras, blanco + rojo sangre, y que diga lo que el título no dice (título «Sonic.exe: el CD maldito…» → «NUNCA EXISTIÓ»).

## Variante monitor de PC (`terror_pc.py`, Sonic.exe, 13-oct-2026, 224 s, 1920x1080)
Cuándo: el relato es de PC (CD-R, .exe, wiki, foro), no de consola. Mismo plano secuencia: escritorio de 2011 a oscuras, el CD viaja al
lector, la cámara entra en el monitor, la corrupción sale al cuarto y el cierre vuelve al cuarto con algo nuevo (Sonic de pie detrás).
- **Utilería:** `cuarto_pc` (cama, escritorio, teclado, torre), `torre_luces` (LED y bandeja del lector), `monitor_pc` (caja beige),
  `jugador_pc` (silla giratoria, `giro` 0..1), `sonic_sil` (de pie o peluche; `ojos`, `sangre`), `cd_disco` (`u_texto` escribe «SONIC.EXE»
  a mano), `nota_arrugada`, `cama_luna`, `encendido`/`apagado` del tubo.
- **Pantallas dibujadas (búfer `SWxSH`):** `pant_escritorio`, `pant_titulo` (título real de Sonic 1 que se corrompe por capas: cielo
  ceniza `p_cielo`, emblema oxidado `p_oxid`, 1991→666 `p_666`, agua roja `p_roja`), `pant_clip43`, `pant_wiki` (`u_elim` borra el
  relato y deja el sello; `u_s1/u_s2` sellos «MAL ESCRITO»/«CLICHÉS»), `pant_captura` (original vs. retocada), `pant_exe` (con `t0` el
  cursor recorre la ventana hasta «Ejecutar»), `pant_doc`, `pant_web` (`'gj'`, `'video'`, `'blog'`, `'broma'`). Las marcas reales (Sega,
  Windows, GameJolt, YouTube) van SOLO como texto, sin logos.
- **Lecciones:**
  1. Con fuentes verificadas un relato de ~200 s dura 3:45: decide pronto si alargas (escena nueva con fuentes) o lo dejas corto.
  2. Tras «start» el monitor NO cae a negro (2,5 s de cuadro oscuro = bloqueo de rigor): ruido que se enrojece, banda de tracking que sube
     y dos cuadros subliminales del demonio justo antes de la primera pantalla de nivel.
  3. Una página fija > 6 s (wiki «ELIMINADO», ventana .exe) necesita vida atada a palabras: sellos que caen o el cursor que recorre.
  4. Un cierre de ~27 s en el MISMO cuarto necesita un evento por frase: el CD que aparece y se deshace en polvo («un disco real»), la
     captura retocada en el monitor, el texto de la wiki, `pared_pantallas` con el cuarto atenuado («mucha gente mirando») y el CD
     nuevo sobre el escritorio («sin carátula»); la cámara cambia de plano entre eventos (1.0 ↔ 1.4).
  5. Para mover un kit sin romper un video: guardar cuadros de ~13 tiempos antes y compararlos después (el render es determinista).
