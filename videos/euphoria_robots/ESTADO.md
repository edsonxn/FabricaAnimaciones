# Le enseñé a mis robots a caerse: el motor tipo Euphoria (Edsonxn, vertical ~2 min) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: edsonxn · vertical 1080x1920 · ~2 min · video nuevo del 5-nov-2026 (pedido del usuario vía la sesión del Robotaller)
- estilo: NUEVO «Disección en vivo» (kit nucleo/diseccion.py) + reglas del canal → doc: docs/estilo_diseccion.md · docs/estilo_jefe_robots.md
- etapa: SUBIDO Y PROGRAMADO (5-nov): Short https://youtu.be/YlFnxL8coVg, privado, sale mié 18-nov 19:00 CDMX (2026-11-19T01:00:00Z)
- siguiente: cuando sea público (18-nov): Studio «Vídeo relacionado» = un largo público del canal; medir a 7 días (retención, subs, comentarios) → canales/formula/edsonxn.md

## Cierre (5-nov-2026, sesión de subida — manda)
- Miniatura Flow 9:16, 2/2 bien: `salida/miniatura.jpg` (B, El Jefe mira al robot volando, «32 > 21 ¡SALIÓ VOLANDO!») + respaldo `miniatura_b.jpg`; `prompt_miniatura.md`.
- `youtube.json` (título con #Shorts, contenido_sintetico, .srt); `filtro_canal`: limpio. `yt subir … private --publicar 2026-11-19T01:00:00Z` → **YlFnxL8coVg**.
- Studio: «Uso de IA» = Sí (ya lo marcó la API). Pendiente: «Vídeo relacionado» cuando sea público.
- Registrado en canales/edsonxn.json (`"short": true`) + BITACORA; `canales --actualizar` (Edsonxn BIEN hasta sáb 21-11); `biblioteca catalogar`
  (7 errores de memoria en mp3 ajenos y en audio/lyria_tramo1.mp3, que es copia de `arana_amarilla__lyria_tramo1`, ya catalogada) + `sfx catalogar` (30 nuevos).

## En curso (5-nov-2026, 1.ª sesión)
HECHO: `nuevo` (carpetas pesadas en E: por junction; E: sin errores de disco en 3 días) · `canales --actualizar` (Edsonxn: hueco mar 10-11 11:24,
pero `robotaller_4apps` está al 53 % para ese canal: este video va DESPUÉS de ese, ciclo 7 d) · `ideas edsonxn` (datos viejos del canal de misterio: no aplican) ·
`yt comentarios edsonxn`: 0 comentarios en 21 d (la junta directiva aún no vota; si alguien comenta antes de subir, el cierre lo enseña).
Kit `nucleo/diseccion.py`: `Sim` = mismo modelo que panel_vivo_ragdoll.js (7 puntos, masas, huesos min/max, 180 Hz, g 820) + músculos + equilibrio
por punto de captura + reflejo; escenarios trapo / rigido / leve / fuerte / vuela / arreglado (hoja `previews/_sim_hoja.jpg`).
escenas.py: momentos gancho, verlet, musculos, equilibrio, error_vuela (hoja `previews/hoja_estilo.jpg`, con RESPALDO de robotaller_n64 en el monitor).
timeline.json es PROVISIONAL (sin voz; 163 s a 2,6 palabras/s): se pisa con `tiempo`.
Doc del estilo + CLAUDE.md (fila Edsonxn) + compartir.py + compartir/CLAUDE.md + galeria.json: hechos.

## Avance 5-nov (tarde)
- Motor verificado contra c99deb7 (datos en el docstring de guion.py). El `Sim` del diagrama se queda con su controlador simple (con 0,2 s / 170 ms exactos se vuelve
  inestable); la voz cita las cifras del motor real. Anotado en docs/estilo_diseccion.md.
- Voz: `voz` → `seleccionar` → `tiempo` lanzados en 2.º plano (log `_voz.log`, termina con FIN). Jefe = `pedido_1` (cuenta 3).
- capturas.py: grabar_real de /v2/vivo a 1080x1080, 24 fps, taller a pantalla completa (css=R.CSS), API tapada; enemigos-pegatina = piezas de
  `historia_jalisco` (Cronopapel, permitido); comentarios/noticias/trofeos vacíos. Prueba OK (`previews/_cap_prueba.jpg`: «¡CLANG!», «¡CATAPLÁN!»).
  Tomas en marcha (log `_cap.log`): caida verlet musculos equilibrio agarre mundo trampa enemigo puente choque. REVISAR hojas cuadro a cuadro.

## En curso (5-nov, VISTO BUENO — manda)
- **El usuario, en el chat de esta sesión (5-nov): «Sí, súbelo».** Vertical de 2:35 = SHORT para YouTube (≤ 3 min): título con «#Shorts», `"short": true`
  en publicados, no ocupa hueco semanal. 4apps va sáb 14-nov 10:00. Este: **mié 18-nov 19:00 CDMX = 2026-11-19T01:00:00Z** (Shorts 18-21 h; nadie más ese día).
- FALTA: miniatura Flow 9:16 (Nano Banana 2.1, x2; ingredientes Token = cuadro del taller/MASTER + `propios/jefe_limpio.png`; receta
  `../robotaller_mes1/prompt_miniatura.md`; texto «32 > 21» o «0 ANIMACIONES», escrito como lo dice el video) → `salida/miniatura.jpg` + `prompt_miniatura.md`;
  `youtube.json` desde `descripcion.txt` (plantilla `../robotaller_n64/youtube.json`, contenido_sintetico true, subtítulos salida/euphoria_robots.srt);
  filtro_canal; `python fab.py yt subir euphoria_robots edsonxn private --publicar 2026-11-19T01:00:00Z`; Studio «Contenido alterado» = Sí;
  «Video relacionado» = un largo público del canal (cuando el Short sea público); publicados + BITACORA + `canales --actualizar`;
  `biblioteca catalogar` + `biblioteca sfx catalogar`; commit SOLO de lo de este video + kit/doc del estilo (ojo: compartir/CLAUDE.md tiene cambios ajenos).

## En curso (5-nov, cierre)
- MASTER hecho con tomas del motor 96c3052+323d045 y rótulo de costo 0,3-0,6 ms (9b2a840). Hoja `previews/_master_hoja.jpg` revisada.
- `tele video … master` en 2.º plano (`_tele.log`): opciones Sí | Cambios | Regrabar con patas largas (ed95ac3 alargó las piernas DESPUÉS de las tomas).
- NO SUBIR sin su sí (video entre los 5 primeros). Con el sí: miniatura en Flow, youtube.json desde descripcion.txt con contenido_sintetico,
  hueco DESPUÉS de robotaller_4apps (ciclo 7 d), `yt subir`, Studio «Contenido alterado» = Sí, publicados + BITACORA, `biblioteca catalogar` / `sfx catalogar`, commit.
- Para renderizar: `--procs 2` (con más procesos `cv2.merge` revienta por memoria).

## En curso (5-nov, noche, 3.ª parte)
- Render completo relanzado (`_render2.log`; el 1.º falló en un segmento por memoria con 42/52 hechos). Al terminar: rótulo de mundo_2
  «por cuadro (medido: 0,2 ms)» → «medido: 0,3-0,6 ms» (motor 9b2a840: cuerpo SIEMPRE simulado, mediana 0,3 ms solo Token / 0,6 ms toda la fábrica,
  p95 1,3) y `video --rehacer 111-118` + `final` + `verificar`. Luego hoja del MASTER, filtro, tele con «¿Lo subo?».

## En curso (5-nov, noche, 2.ª parte)
- El motor cambió tras mis grabaciones: 96c3052 (controladores, manos al punto de impacto, golpes graduados) y 323d045 (caminan a 150 px/s).
  Render detenido. Frase equilibrio_3 corregida («meto las manos donde voy a caer»); `caida` usa Trapo.euforia(). REGRABANDO las 10 tomas (`_cap2.log`),
  luego voz de equilibrio_3 + seleccionar + tiempo, hoja `_pruebas/hoja_t.py`, y otra vez mezcla → video → final → verificar.

## En curso (5-nov, noche — manda sobre lo de abajo)
- Voz recortada OK: 25/25, timeline 154,8 s (2:35; ~10 s son compases de música entre bloques). Si el usuario lo quiere más corto: recortar frases.
- escenas.py + esc_cola.py: los 13 momentos y el PLAN anclado a la voz (hoja `previews/hoja_t.jpg` revisada, grabaciones reales, El Jefe con su voz).
- Música: biblioteca `arana_amarilla__lyria_tramo1` (WND, otro público) → audio/musica.wav. SFX: `SFX_ELEVEN` (9 nombres, 23 eventos; 92 créditos, cuenta 1 agotada → cuenta 2).
- `chequeo`: no aplica (sin efectos.py). Lanzado en 2.º plano: mezcla → video → final → verificar (`_render.log`, termina con FIN).
- SIGUE: mirar `_render.log`, hoja del MASTER cada ~10 s (privacidad), filtro_canal, MASTER a la tele con «¿Lo subo?», y NO subir sin su sí.

## FALTA (en orden)
1. Motor en main: `git log --oneline -10`, bloque «Muñeco de trapo» y «Peligros» de docs/panel.md, `nucleo/panel_vivo_ragdoll.js`, `panel_vivo_peligros.js`.
   Comprobar cada dato del guion (docstring de guion.py; lo marcado [VERIFICAR]) y re-copiar constantes al `Sim` si cambiaron (tambalea, paso de recuperación,
   manos a la cabeza, agarrarse del mueble, choques entre muñecos, trampas entre pisos, costo ≤ 1 ms). Añadir errores nuevos si los hubo.
2. Guion: recortar a ~2:00 (hoy ~330 palabras; Token habla ~2,8/s → ~300). La línea del Jefe (`pedido_1`, texto de su pedido del 5-nov) se le enseña antes.
3. `python nucleo/filtro_canal.py euphoria_robots` → `fab.py euphoria_robots voz` (cuenta 3 para el Jefe) → `seleccionar` → `tiempo`.
4. Grabar el taller (`robotaller.grabar`, cuadro a cuadro, viewport ≈ 1080x1080 o 1600x900 recortado) forzando `Trapo.prueba(...)` / `Peligros.prueba(...)`:
   capturas/caida, verlet, musculos, equilibrio, mundo (muebles, trampa entre pisos, enemigo con chancla), errores. Sesión de un video PERMITIDO
   (no Warcraft/Tamriel/Runa/Gaia: los enemigos-pegatina salen de las piezas del video en curso). Revisar cuadro a cuadro.
   Idea: exportar `Trapo.estado()` por cuadro para dibujar el esqueleto real sobre el barrido.
5. Momentos que faltan: pedido (El Jefe `jefe_canadiense`), problema (animación repetida vs Euphoria), mundo, error_puente, cierre (junta directiva);
   PLAN anclado a palabras; SFX (`SFX_ELEVEN`, sin repetir lo del canal) + música (biblioteca → Lyria) ; `chequeo`.
6. `video` → `final` → `verificar` → filtro → `tele video euphoria_robots master --pregunta "¿Lo subo?" --opciones "Sí|Cambios" --esperar 900` → NO subir sin su sí.
7. Miniatura en Flow (navegador integrado; Token + El Jefe, cifra gigante «32 > 21» o «0 ANIMACIONES»), descripción, youtube.json con contenido_sintetico, subir, registrar.

## Sesiones
- alias: euphoria_robots · motor del taller: sesión «Robotaller — muebles, caídas entre pisos y Euphoria» (local_cbbfccc3-38eb-404d-b946-d6f9e55ee904)
- ✅ 5-nov-2026: estilo nuevo, guion verificado, voz, 10 grabaciones (motor 96c3052), MASTER verificado, visto bueno del usuario
- ✅ 5-nov-2026 (subida): miniatura Flow 9:16, youtube.json, filtro, subido y programado (YlFnxL8coVg, mié 18-nov 19:00), registro y catálogo
