# Las 15 armas más PODEROSAS de Skyrim — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_tamriel · meta: hueco vie 30-oct-2026 12:08 CDMX (96 h tras cosas_inutiles) · ~15 min (el usuario) → 16:33 con pantalla final
- estilo: secuencia_yt (gameplay Skyrim por beat + MG `nucleo/mg_tes.py` + pegatinas + mapas tema `tes`) · voz Chatterbox Sarcastica · música OST oficial de Skyrim → doc: docs/estilo_secuencia_yt.md § Tamriel
- etapa: ✅ SUBIDO y PROGRAMADO vie 30-oct-2026 12:08 CDMX (2026-10-30T18:08:00Z) · https://youtu.be/m6Pk4FLQGuc · miniatura + .srt + monetización activada
- siguiente: a los 7 días (6-nov) métricas vs cosas_inutiles/misiones_nunca → `canales/formula/cronicas_tamriel.md` · `limpiar` cuando salga público

## Sesiones (plan de tramos · «continúa el video tes_armas_poderosas» retoma aquí · protocolo docs/sesiones.md)
- alias: armas poderosas, 15 armas, tamriel armas · vista previa: 🎞 Montaje del panel, sin render parcial
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión (el usuario, 23-oct): investigación UESP + guion + voz + beats + clips + pegatinas + MG + mapas + OST + mezcla + render + rigor + miniatura + subida + Studio | ✅ 23-oct | 130 frases, 113 clips (56 rehechos en 5 vueltas), 58 pegatinas, 4 MG nuevos + 3 del kit, 7 mapas; subido m6Pk4FLQGuc |

## Decisiones del episodio (23-oct-2026)
- tema elegido por Claude (el usuario: «tú elige el tema»): lo que el jugador USA gana en el canal (objetos ×4,2, hechizos ×3,8);
  últimos 3 = misiones nunca / exploits / inútiles → cambia UNA variable: el tema pasa a ARMAS (15 puestos, misma fórmula).
- lista (15→1): Viento Cortante · Wabbajack · Espada de Sangreskal · Maza de Molag Bal · Hacha rúnica de la Guardia del Alba ·
  Volendrung · Hoja de ébano · Bastón de Magnus · Quebrantadora del amanecer · Hoja de Ruiseñor · Espada de Miraak · Azote de
  dragones · Desgarradora gélida · Arco de Auriel · la Daga de hueso de dragón que forjas tú (gema: ×30 con Hoja del asesino +
  Guantes etéreos = 1 980 por puñalada). Fichas y fuentes UESP en `investigacion.md`.
- formato: `lista_15_armas_secuencia_yt` · sin patrocinio · música OST (12 pistas NO usadas en cosas_inutiles, `armar_musica_ost.py`)
- MG nuevos en mg_tes: ruleta (Wabbajack), niveles (trampa del nivel: Ruiseñor y Azote), golpes (dragón ancestral 38/38 → 38/52),
  barras (daño base de espadas; «Una sola puñalada» con líneas de salud de dragones) + `_icono` (armas largas tumbadas). Del kit:
  traiciones (Hoja de ébano), rejilla (26 %), receta (la daga), contadores (hacha rúnica).
- mapas (tema tes, con foto): el Katariah, Laberintia, Monte Kilkreath, Cauce Boscoso → Refugio Celestial, Riften, Cueva de Sima
  Negra, ruta del forjador (Carrera Blanca → Falkreath).

## Hecho
- voz 130/130 (24 aceptadas por CER/GAP/TAIL tras leer cada transcripción) · tiempo 974,0 s · 113 beats
- clips: 1.ª hoja propia de 2 cuadros/clip → 40 rechazados; 2.ª vuelta 9; `fx hoja` 4; MASTER v1 9; MASTER v2 1 (069 acababa en el
  menú de la forja a los 12 s) → tramos 575-600 y 755-772 con `video --tramo` insertados por cuadro en video_sin_audio + `final`
- mezcla -14 LUFS, voz +12,9 dB · verificar CER medio 1,08 % · sin negros ni congelados (solo el paso a la pantalla final)
- registrado: canales/cronicas_tamriel.json (publicados, formato), BITACORA, `canales --actualizar` (Tamriel hasta lun 02-11)
- E: dio NTFS 130 (20:32): segmentos/ y salida/ de este video son carpetas REALES en C: (respaldo salida/_MASTER_v2_respaldo.mp4: borrar)

## Falta
- [ ] métricas a los 7 días · [ ] `python fab.py tes_armas_poderosas limpiar` cuando salga público (borra también _MASTER_v2_respaldo)
- [x] anuncios intermedios (mid-roll automáticos) activados en Studio tras el procesado SD (23-oct); anuncios «Comprobando»

## Cómo retomar (comandos)
```
python fab.py continuar tes_armas_poderosas
```

## Lecciones de este video (solo lo no obvio)
- Las anclas y MARCAS se buscan en TODO el video, primera aparición: «La Desgarradora gélida» casó con el aviso del n.º 3 y «tiene
  un error» con otro puesto → usar un trozo que solo exista ahí («Desgarradora gélida en la misma», «sin parches tiene un error»).
- «… no HUD» en las búsquedas salió limpio casi siempre (13 de 14 a la primera); «no commentary» todavía trae menús.
- Un beat largo (13 s) necesita mirar más allá de 6 s: el 069 acababa en un menú. `_hoja_clips.py` mira 1 s y 6 s.
- No empalmar sobre el MASTER (pierde la pantalla final): reconstruir video_sin_audio con los tramos y volver a pasar `final`. Si
  `final` truena con PermissionError, el panel tiene abierto el MASTER: renombrar a mano el .tmp.mp4 y repetir `final`.
- Flow en el navegador INTEGRADO no llega a 127.0.0.1 (ERR_BLOCKED_BY_CLIENT): ingredientes desde URL públicas (wiki, i.ytimg.com),
  uno cada ~6 s (receta en prompt_miniatura.md).
