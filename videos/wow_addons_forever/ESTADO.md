# Los 20 ADD-ONS que necesitas en WoW Forever (y uno que hicimos nosotros) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_warcraft · lun 9-nov-2026 09:00 CDMX (fecha Overgear, enlace `overgear.s.gy/CRONICAS/5`)
- estilo: secuencia_yt (gameplay por beat + pegatinas + MG + mapas + Overgear con fondo de marca + grabaciones propias de OBS) → doc: docs/estilo_secuencia_yt.md
- etapa: SUBIDO ✅ privado, se publica lun 9-nov 09:00 CDMX (https://youtu.be/WpOLrmRm2h8) · MASTER 22:06
- siguiente: poner enlaces PayPal y CurseForge en youtube.json (sustituir [ENLACE … PENDIENTE]) → `yt aplicar`; Studio: monetización + cuestionario

## Sesiones (UNA sesión directo al MASTER, regla 5-nov; relevo si corta a 180 mil)
- alias: los add-ons, 20 add-ons, el del 9-nov
- vista previa: no; render a la tele solo (regla 5-nov)
- leer al empezar: este ESTADO.md · `canales/formula/cronicas_warcraft.md` § «PENDIENTE para el SIGUIENTE video nuevo (… 7-nov)» · copiar de `videos/wow_errores_forever/` (Overgear, mapas, MG, placas de narrador, musica_wow.py)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación + guion + voz + tiempo | ✅ 7-nov | voz 183/183 (Applio + 16 ElevenLabs), tiempo, beats (152, 21:46) |
| 2 | beats + búsquedas + bajar + pegatinas + grabaciones OBS + efectos + promesas + chequeo | ✅ 7-nov | 152 clips, 135 efectos, 5 MG nuevos, promesas y chequeo |
| 3 | OST + SFX + mezcla + render + final + verificar + miniatura Flow + subir 9-nov | ✅ 7-nov | MASTER, miniatura Flow, subido WpOLrmRm2h8 |

## Decisiones del episodio (el usuario, 7-nov-2026)
- Tema: «Los 20 ADD-ONS que necesitas en WoW Forever» (opción 1 de 3; ref. Bellular «The Addons We're Using on Day 1 of Forever» ×3,1). **~24 min.** Igual de Forever que los 25 errores (que arrancó fuerte: 1 688 vistas en ~4 h).
- **Mini categoría «add-ons de INMERSIÓN» (≥ 5) dentro del top**, explicando que a él le gusta jugar inmersivo (oír el lore y las misiones). Ahí entran SUS dos add-ons (WoW Forever Voces + Necesidades), hacia el **30 %** del video, con sus grabaciones de OBS (`D:\wowForeverVoces\grabaciones_obs\`, 5 clips, 3:55 en total; hojas `previews/grab_1..5.jpg`): gratis, pocas misiones (Villanorte/Villadorada), **llamado a donar por PayPal desde un mínimo** para doblar todo el juego, preguntar si quieren que siga (sobre todo el de voces) → comentarios. Descarga: **CurseForge** (zips y fichas en `D:\wowForeverVoces\curseforge\`). Enlaces PayPal y CurseForge: _pendientes del usuario_ (bloquean la subida).
- **Voces:** Remy (Applio) narra (ganó la votación de los 25 errores: «la voz de siempre») + **la voz clonada del usuario (el Humano tras el Telón)** presenta sus add-ons. Agradecer los votos.
- Overgear: 9-nov → `/CRONICAS/5`, fondo de marca, logo blanco, promoción pagada; NUNCA hablar mal de comprar oro/boosts.
- `wow_pistas_futuro` (uETB9GOW4hk) MOVIDO al dom 15-nov 09:00 CDMX (7-nov, registrado en canales/cronicas_warcraft.json).
- Comentarios (7-nov): 21 nuevos, casi todos votan la voz de siempre; ♥6 @zatherion1 elogia la voz real del usuario. Candidatos: gracias @zatherion1 @pirlo2106 @AlexAnder-z1i7l @666nibelheim666 @quemaloscalor @santislpslp1595; burla @FenrirMorningstar («las demás son kaka… Hope suena bien»).
- Gracia: en la grabación 5 el PNJ se llama **Remy «Dos Veces»** (como el narrador).

## Pendiente tras subir (7-nov ~16:10)
- Enlaces de PayPal.Me y CurseForge (pedidos a la sesión madre): en youtube.json → `python fab.py yt aplicar wow_addons_forever cronicas_warcraft`.
- Studio (navegador): monetización + cuestionario; video relacionado de Shorts.
- Tele apagada al terminar: el MASTER no se mandó (aviso por voz hecho).

## Lecciones (7-nov)
- Applio habla rápido: 183 frases dieron 21:46, no 24 min (≈ 7,1 s por frase).
- `CER_MAX` 0,012 rechazó 45 frases por nombres de add-ons que Whisper escribe distinto: `CER_MAX_POR_FRASE` tras revisarlas (y oír la dudosa con `initial_prompt`).
- El `post` de una escena cae en el beat de la SIGUIENTE: el sonido nombrado va mejor como PISTA `voz=True` con el tramo audible recortado (`sfx/oye_*.mp3`) y el clip alineado; `ambiente_por` suena en todo el beat.
- Videos de creadores con minuto: 33 de 152 rehechos (mascota de We Ding Again, webcam de SignsOfKelani/Scottejaye/Bigbillygames, cara de Bellular).
- Anclas: `|fin` = fin de la última palabra del ancla (no de la frase); `_anclas.py` revisa todas antes de `fx`. ROTULOS solo con colores de PALETA (no hay «verde»).
- Flow: el navegador integrado no hace `fetch` a 127.0.0.1 ni recibe Ctrl+V del sistema; en Chrome, un `paste` de un File traído de un servidor local con CORS mete el ingrediente, y los resultados se guardan con POST al mismo servidor.
## Hecho
- proyecto, canales, comentarios, métricas, pistas_futuro movido, hojas de las grabaciones.

## Falta
- [ ] guion → voz → tiempo → beats → busquedas → bajar → pegatinas → efectos (grabaciones OBS como `pant`/medios propios) → promesas → chequeo → OST → SFX → mezcla → video → final → tele → verificar → miniatura Flow → subir `--publicar 2026-11-09T15:00:00Z` → registrar → canales → commit
