# Polybius: el videojuego que nunca existió — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: edsonxn · PROGRAMADO mié 14-oct-2026 14:00 CDMX (https://youtu.be/6rqPo_fgz58; publishAt 2026-10-14T20:00:00Z, privado hasta la fecha, con miniatura por código y .srt)
- estilo: documental → docs/estilo_documental.md (§ «Tablero de detective VIVO») · ejemplo copiado: videos/satoshi_nakamoto/ + kit propio `arcade.py` · voz Faraon · Lyria · SIN subtítulos
- etapa: MASTER 5:16 (1,43 GB, CER medio 0,0015, −14 LUFS), revisado cada 3 s · subido y programado el 7-oct-2026
- siguiente: opcional: miniatura IA (Flow; `prompt_miniatura.md` sigue siendo el de Satoshi, hay que reescribirlo) y aplicarla con `python fab.py yt aplicar polybius edsonxn 6rqPo_fgz58`; mover salida/ y segmentos/ a E: (`python nucleo/mover_pesados.py`); al aprobar: `limpiar`

## Hecho
- Guion de 30-sep (8 escenas, 52 frases, 718 palabras), hechos con fuente en el docstring de `guion.py`. `ALIAS_QA` para lo que oye Whisper («Rothberg», «Hipolibius» = «Y Polybius»).
- Un solo plano secuencia sobre el corcho: centro = polaroid «POLYBIUS · ¿EXISTIÓ?» (portal `busqueda`: almacén a oscuras con linterna; al final la cabina se enciende).
  Zonas: gancho arriba-izq. · leyenda arriba · casos derecha · gobierno abajo-der. · pruebas abajo · origen abajo-izq. · por qué izquierda.
- KIT NUEVO `arcade.py` (pintor `mg.P`): `cabina` (frente) y `cabina_lado` (perfil), pantallas vectoriales propias `pant_formas / pant_asteroides / pant_tunel / pant_tanque`,
  `salon` (pared con neones, fila de cabinas vivas, moqueta), `jugador`, `luz_cara` (borde de luz de pantalla), `neon`, `moqueta`.
- 18 portales (`portales.py`, `portales2.py`, base `portal_base.py`): salon, fascinados, pesadilla, hombres, vacio, maraton, migrana, redada (exterior → interior), corazon,
  tanque, prueba, hemeroteca (microfilm), web2000 (monitor de tubo), viaje (mapa Natural Earth), padres, mente, recreacion, busqueda.
- Piezas (`piezas.py`): `anio_card`, `vacia_card` («NINGUNA»), `icono_card` (tele, música, mando, placa…), `revista` genérica, `hoja_vector`, `recorte`, `tarjeta_cita`, `relleno`.
- Fotos reales (Commons, con crédito en pantalla): estación de Portland dic-1981, cabina de Asteroids, logo de Tempest, cabina de Battlezone, captura del simulador militar, busto y edición de 1548 de Polibio.
  NO se muestra ninguna «foto de Polybius»; pantallas, web del año 2000, periódicos y revista van rotulados como recreación (también en los créditos y la descripción).

## Falta
- [x] `final`, `verificar` (solo «Polybius» → «Bolivius» en una frase, es Whisper), revisión del MASTER
- [ ] mover lo pesado a E: (`python nucleo/mover_pesados.py`; `salida/` y `segmentos/` se crearon en C: porque el video es anterior a los junctions)
- [x] subido en privado y programado (miniatura por código `_miniatura.py`: «NUNCA EXISTIÓ ¿O SÍ?»)
- [ ] miniatura IA si el usuario la quiere

## Cómo retomar (comandos)
```
python fab.py estado polybius
cd videos/polybius ; $env:PYTHONPATH="C:\FabricaAnimaciones\videos\polybius;C:\FabricaAnimaciones\nucleo"
python _hoja_rec.py a        (a..h: cuadros clave del recorrido -> previews/rec_a.jpg;  `t 12.5 30` = tiempos sueltos)
python _hoja_portal.py salon:1,5 redada      (portales sueltos)      python _hoja_arc.py   (kit arcade)
python _barrido.py 3         (un cuadro cada 3 s de todo el video)   python _parche.py     (sustituciones exactas)
python _render_despierto.py 6   (render sin que el PC se suspenda)
```

## Lecciones de este video (solo lo no obvio)
- Siluetas oscuras sobre salón oscuro NO se leen: subir el fondo (pared 0.05–0.12) y dar borde de luz (`luz_cara`); el filtro `cine` oscurece, por eso
  `portal_base.portal` multiplica la escena por 1,22.
- `mg_obj.lupa` pinta el cristal opaco (parece una bola blanca): dibujar aro + mango a mano.
- Anclas: `_n()` conserva la ñ («año», «señalado», «migra») y `ww` busca por PREFIJO («no» casa con «nombre», «una» no casa con «unos»): pasar `nth`.
- Texto de pregunta `Q`: el «?» rojo sube ~250 px sobre la primera línea; dejar aire (cámara más abierta o pieza más arriba).
- PowerShell rompe los `python -c` con comillas: parches en `_parche.py`. `Remove-Item` dentro de un comando compuesto puede bloquear TODO el comando.
- Chatterbox dejó la voz a medias el 30-sep (22/52) y `estado` lo mostraba como «voz hecha»: mirar `seleccionar` antes de fiarse.
- El clic de la chincheta (`pin`) sonaba 67 veces en 5 min y el usuario pidió quitarlo: `tablero.Pieza` ya no lo registra y el papel va a 0,14. YouTube no deja cambiar el audio: hubo que resubir (la subida vieja QMrTGVJXIEg quedó en privado SIN fecha; la borra el usuario).
