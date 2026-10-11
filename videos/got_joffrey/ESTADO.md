# ¿Quién envenenó al rey? La Boda Púrpura — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: — (sin canal, prueba del estilo con guion y voz; 11-oct-2026). Tema de Game of Thrones: el envenenamiento de Joffrey
- estilo: noir_feudal → doc docs/estilo_noir_color.md § Variante FEUDAL · kit nucleo/noir_color.py + noir_feudal.py + noir_corte.py (nuevo)
- etapa: MASTER hecho y revisado (salida/got_joffrey_MASTER.mp4, 3:12, 1080p, −14,1 LUFS, voz/fondo 11,3 dB, CER 0,003) + .srt corregido
- siguiente: que el usuario lo vea; si aprueba: `python fab.py got_joffrey limpiar` (segmentos ~1 GB). Si pide cambios: `video --rehacer t0-t1` + `final`

## Hecho
- Guion (9 escenas, 26 frases, 366 palabras, corchetes de actuación): el pesquisidor narra la Boda Púrpura como un caso. Hechos y
  pronunciación en el docstring de `guion.py` (voz «Yófrey/Tirion/Sérsei/Olena» → en pantalla y .srt Joffrey/Tyrion/Cersei/Olenna).
- Voz ElevenLabs «David» (eleven_v4): 26/26 válidas, 151 s de voz, 252 créditos; video de 192,1 s (3:12).
- Kit NUEVO del núcleo `nucleo/noir_corte.py`: BustoCorte (perfil con corona/diadema/toca/collar/ahogo), Cortesano (cuerpo entero,
  enano, bufón, bastón, caer), comensales; rampas purpura/azul/armino. Estilo `noir_feudal` registrado en `nucleo/estilos.py`.
- Propio del video: `reparto.py` (rasgos de cada personaje), `mundos_j1/j2/j3.py` (ciudad en fiesta, gran salón, pared de tapices,
  estrado, losas, mazmorra, botica, jardín, terraza, rosaleda, contaduría, puerto, cubierta, torre de día, puerta al alba, mantel,
  terciopelo, tablero), `props_j.py` (cáliz, empanada y palomas, espada, jarra, músicos, cristales, frasco, puño, collar, cofre,
  ballesta, saeta, barca, rosas, monedas, rollo), `comun.py` (banda, cartela de pergamino, reflejar), `esc_*.py` (9 escenas).
- Música Lyria en 2 tramos (`_lyria_segmentos.py todo` → audio/musica.wav). SFX ElevenLabs `fx_audio.py` → audio/fx.wav
  (40 golpes; 6 nuevos = 215 créditos; 7 genéricos copiados de informante_2027).
- Sin fotos ni escudos de la serie: personajes y emblemas propios (sol, llave).

## Falta
- [x] Revisión por planos (`_lote.py`) y del MASTER cada 3 s (`previews/master_0..5.jpg`); 6 defectos corregidos y re-renderizados por tramos
- [x] .srt corregido con `_srt.py` (Joffrey, Tyrion, Cersei, Olenna)
- [ ] Opcional si se publica: miniatura, youtube.json; flojos conocidos: el cofre abierto no enseña la tapa; el cristal que se
      disuelve es pequeño; muchas tomas son oscuras por diseño (noir)

## Cómo retomar (comandos)
```
python fab.py estado got_joffrey
python videos/got_joffrey/_lote.py [escena ...] [--fr 0.3,0.8] --procs 4     (un cuadro por plano → previews/lote_*.jpg)
python videos/got_joffrey/_prueba.py <escena> u1 u2 ...                       (tiempos locales → previews/p_<escena>.jpg)
python videos/got_joffrey/_ver_corte.py · _ver_mundos.py j1|j2|j3 · _ver_props.py   (hojas del reparto, mundos y utilería)
python videos/got_joffrey/_reg.py                                             (regenera escenas.py)
```

## Lecciones de este video
- Los cuadros salen lentos (10-15 s el salón con 36 invitados) y ×10 si otro render ocupa la CPU: probar con pocos cuadros.
- `NC.pegar` con `dx` grande deja ver el borde replicado del Lienzo (rayas verticales): desplazar poco o pintar más ancho.
- El ancla del primer corte va en «delante», no en «Nunca»: la grúa de la ciudad necesita ~5 s.
- `video --rehacer` tras editar código (sobre todo del núcleo) DESCARTA todos los segmentos con firma vieja y rehace el video entero
  (pasó aquí: 65 en vez de 22). Antes: «conservar» en el panel, o asumir el render completo.
