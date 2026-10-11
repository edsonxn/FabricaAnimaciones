# El informante que le puso fecha al final (AI 2027) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: logia · PROGRAMADO mié 14-oct-2026 14:00 CDMX (https://youtu.be/5D-kQtNWF4w, versión corregida que sustituye a eHIxoZLpbMc; publishAt 2026-10-14T20:00:00Z, privado hasta la fecha, con miniatura y .srt)
- estilo: noir → doc de estilo: docs/estilo_noir.md · ejemplo a copiar: este video (20 escenas, kit `kit27.py` + `mundos27.py` + `comite.py`)
- etapa: MASTER REHECHO y verificado el 8-oct-2026 (texto paralelo a las hojas, caminatas corregidas): `salida/informante_2027_MASTER.mp4` (10:32, 1080p, 3,1 GB, CER 0,0008, −14 LUFS, voz/fondo 11,4 dB) + `.srt` + `salida/miniatura.jpg` + `youtube.json`
- siguiente: el USUARIO borra el video anterior eHIxoZLpbMc en Studio (mismo hueco); comprobar en Studio que terminó de procesar en HD; cuando el usuario lo apruebe: `python fab.py informante_2027 limpiar` (libera 3 GB de segmentos)

## Hecho
- Tema elegido por métricas (8-oct-2026): en LogIA lo que más retiene son las predicciones con fecha («cine en 2027», «cerebro PRONTO»);
  en el nicho, outliers «AI whistleblower warns» (18x) y «The world in 2027» (34x). Hechos y fuentes: docstring de `guion.py`.
- Guion: 20 escenas, 84 frases, 1304 palabras, detective narrador, corchetes de actuación. Voz «David» eleven_v4: 84/84 válidas,
  632,1 s en total (10:32), ~970 créditos. En la voz el apellido va «Kokotailo»; en pantalla «KOKOTAJLO».
- Escenas `esc_<id>.py` (3-7 planos cada una): gancho, cliente, profecia, renuncia, precio, escandalo, expediente, agentes, robo,
  ejercito, afuera, mentira, filtracion, voto, carrera, freno, dudas, marcador, plan, cierre. `escenas.py` lo genera `_reg.py`.
- Kit nuevo: `kit27.py` (calendario, carpeta, billetes, casa, balanza, interruptor, reloj_arena, puerta, mano_alzada, multitud,
  robot, pantalla_codigo, medidor 0-100 %, `caminante` = cuerpo entero con ciclo de paso), `mundos27.py` (laboratorio, sala_comite,
  capitolio, fabrica, redaccion, despacho), `comite.py` (los diez del comité + `jardin` = la casa de la familia).
- Sonido: `sfx` del núcleo (496 eventos), `fx_audio.py` → `audio/fx.wav` (91 golpes, 12 sonidos de ElevenLabs; 10 reutilizados de
  `videollamada_falsa/sfx`, 2 nuevos: mazo, apagon), música Lyria en 5 tramos (`_lyria_segmentos.py todo`).
- Miniatura por código (`_miniatura.py`: la máquina con careta y la sombra con ojos, «2027 LO AVISÓ»); `youtube.json` (`_youtube.py`).

## Falta
- [x] `mezcla`, `final`, `verificar`; MASTER revisado en hojas `previews/master_1..4.jpg` (un cuadro cada 3 s): sin cuadros negros ni saltos
- [x] `.srt` corregido («Kokotajlo»)
- [ ] flojos conocidos, por si el usuario pide más (ANTES de `--rehacer`, «conservar» en el panel): la hoja de la carta queda en blanco ~3 s
      (1:41-1:44, `renuncia.p_carta`); `profecia.p_razona` (1:15) y `freno.p_apagan` (7:51) son tomas sobrias y oscuras; render 49 min con 10-11 procesos
- [x] **CÓDIGO CORREGIDO, MASTER REHECHO Y RESUBIDO el 8-oct-2026** (5D-kQtNWF4w, con `--forzar` por ser reemplazo; sin revisión visual del MASTER, a pedido del usuario) (el usuario vio en YouTube: texto torcido respecto a la hoja, renglones
      que no caben en el cristal de `freno`, caminatas «hacia atrás»). Arreglado en `nucleo/noir.py` (`soporte`, `ang`, `ancho_max`),
      `nucleo/noir_pers.py` (`pierna_paso`, `cadera_paso`, `avance_paso`), `kit27.py` (`hoja`, `carpeta`, `caminante`, `fase_paso`) y
      escenas afuera/cliente/cierre/freno/renuncia. Afecta a ~14 de 20 escenas: toca render completo + `final` + subir de nuevo
      (YouTube no reemplaza el archivo: video nuevo con el mismo `publishAt` y borrar el viejo).
- [x] subido y programado el 8-oct-2026 (la subida dio 401 al iniciar y 410 en el último trozo, pero el archivo llegó completo; luego `yt aplicar`
      tras forzar la renovación del token: poner `expiry_date` a 0 en `canales/tokens/youtube_tokens_<canal>.json`)
- [ ] opcional: insertos de video real entintado (`clip_noir`): este video es 100 % dibujado

## Cómo retomar (comandos)
```
python fab.py estado informante_2027
python videos/informante_2027/_prueba.py <escena> u1 u2 ... [--solo-hoja]   (tiempos locales; hoja previews/p_<escena>.jpg)
python videos/informante_2027/_lote.py esc1 esc2 ... --n 8                   (8 cuadros por escena → previews/lote_<k>.jpg)
python videos/informante_2027/_hoja_global.py 3                              (un cuadro cada 3 s de todo el video)
python videos/informante_2027/_ver.py mundos|props                           (hoja de los mundos y la utilería nuevos)
python videos/informante_2027/_reg.py                                        (regenera escenas.py tras añadir un esc_*.py)
```

## Archivos clave
- `guion.py`, `timeline.json`, `escenas.py`, `basen.py`, `comun.py`, `kit27.py`, `mundos27.py`, `comite.py`, `esc_*.py`, `props*.py`

## Lecciones de este video (solo lo no obvio)
- La luz multiplica: una silueta oscura sobre pared oscura NO se ve. O contraluz (puerta encendida detrás) o luz radial que la siga.
- `K.persona` (bolo sin piernas) solo vale para multitudes lejanas; para un personaje que camina, `K.caminante` (piernas con rodilla).
- Empuje de cámara: `1 + 0.012..0.02 * u`; con 0.05 un plano de 7 s acaba al 135 % y recorta papeles y rótulos.
- Ningún plano debe arrancar vacío: lo que «cae» o «se escribe» empieza con el plano, no con la palabra (se ancla el remate, no la entrada).
- Papeles cenitales: tazas y objetos también cenitales (`K.taza_arriba`); la taza de perfil sobre un escritorio visto desde arriba chirría.
- `N.sello` (tinta con huecos) no se lee encima de otro texto: para rematar, `C.banda` (sólida).
- La torre de cristal de `MU.medio()` llega a y≈-1150 en su capa (prof 0.6): para verla, cámara en cy≈-1900 con zoom 0,9.
- Comandos de más de ~8 KB fallan en este Windows aunque sean heredocs: los parches largos van a un .py con Write.
- `CER_MAX_POR_FRASE` en guion.py para homófonos que Whisper escribe distinto (rebela/revela, apellidos).
