# Dos formas de fusionar videojuegos con IA — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: SIN CANAL (prueba; el usuario decide dónde va) · sin fecha
- estilo: documental → «rayos X tecno» VERTICAL (animación por código + video real en ventanas) → doc: docs/estilo_rayosx_tecno.md · ejemplo: este video
- etapa: MASTER hecho y verificado (7-oct-2026): `salida/mods_ia_fusion_MASTER.mp4`, 1080x1920, 112,0 s, CER 0, 0 ms de desfase, −14,25 LUFS; revisado con la vista cada 3 s (`previews/master_hoja.jpg`)
- siguiente: que el usuario lo vea y lo OIGA (voz, música, nivel de efectos); con sus cambios: editar escena → `video --rehacer t0-t1` → `final`. Si le gusta: decidir canal, título y créditos

## Hecho
- Guion verificado (fuentes en el docstring de `guion.py`): SkyCraft = dos procesos + memoria compartida; recompilar vs. decompilar; Skate 3 en Rust/Bevy tras más de dos años de ingeniería inversa a mano.
- Voz ElevenLabs «Ginyin» (`nMPrFLO7QElx9wTR0JGo`): 23/23 frases CER 0, 99,2 s de narración (`puente_5` necesitó la semilla 5).
- Escenas en plano secuencia: gancho → puente → límite (`esc_a.py`); reescritura → la verdad → cierre (`esc_b.py`).
- Extractos reales en `clips/`: `skycraft_a` (Hi5M0F0, FL_UzGZraT8) y `skate_rust` (chasm, osiMnevjhZM, primeros 240 s), con crédito en pantalla.
- SFX: 12 sonidos de ElevenLabs en `sfx/`, 109 golpes anclados a palabras (`fx_audio.py` → `audio/fx.wav`).
- Música: Lyria candidato 1 (`audio/lyria_1.mp3` → `audio/musica.wav`). Mezcla −14,25 LUFS, −1,05 dBTP, voz 10,8 dB sobre el fondo.

## Falta
- [x] Render + `final` + `verificar`. El usuario avisó (viendo el avance) de que el clip del gancho quedaba corrido fuera de su ventana: corregido y re-renderizado.
- [ ] Que el usuario lo vea y lo OIGA (voz, música y nivel de efectos no se pueden juzgar sin escuchar).
- [ ] Si se publica: decidir canal, título/descripción con créditos de los clips, y aviso de riesgo de derechos por los extractos de gameplay.

## Cómo retomar (comandos)
```
python fab.py estado mods_ia_fusion
python videos/mods_ia_fusion/_hoja.py 2.6 31.5 71.5 -f --out prueba     hoja de cuadros (previews/prueba.jpg; -f = tamaño completo)
python videos/mods_ia_fusion/fx_audio.py [--seco]                       SFX → audio/fx.wav; luego `python fab.py mods_ia_fusion mezcla`
python fab.py mods_ia_fusion video --rehacer 40-46                      tras cambiar una escena; luego `final`
```

## Archivos clave
- `guion.py` (guion, VOZ, LYRIA, MEZCLA, TRANSICIONES continuas) · `escenas.py` (`Mundo`, `cuadro(t)`)
- `pix.py` (pintor, fondo, acabado, clips, anclas) · `comp.py` (ventana, memoria, mundo de bloques, rótulos, iconos)
- `esc_a.py` / `esc_b.py` (coreografía anclada a palabras) · `fx_audio.py` · `_hoja.py` · `_voces.py` · `_ref_voz.py`

## Lecciones de este video (solo lo no obvio)
- El video real funciona mejor DENTRO de una ventana del diagrama que a pantalla completa: 720p estirado a 1920 de alto se ve borroso, y como ventana pasa a ser parte de la explicación.
- Con `fx=-7` los efectos tapaban la voz (2,3 dB); `fx=-17` y `musica=-24` la dejan en 10,8 dB.
- `lyria.py` necesita `PYTHONPATH` con la carpeta del video y `nucleo` (si no: «No module named guion»).
- `p.cam(z, cx, cy)` CENTRA el punto (cx, cy) en la pantalla aunque z = 1: para un zoom que no desplace, `p.pivote(x, y, z)`. Ese error dejó el clip del gancho 180 px fuera de su ventana.
- Editar el código de una escena invalida TODOS los segmentos (firma del código): `video --rehacer` volvió a renderizar los 38 (~9 min con 6–8 procesos).
- Hojas de prueba a 360x640 detectan huecos de composición; la nitidez del texto solo se juzga a tamaño completo (`-f`).
