# Las 5 peores atrocidades de Morgott QUE IGNORASTE — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: runa_caida · meta: hueco del canal dom 08-11-2026 10:00 CDMX (ciclo nuevo de 3 días, 5-nov)
- estilo: secuencia_yt (gameplay de Elden Ring por beat + PEGATINAS + pant() + MG NUEVOS `nucleo/mg_er.py` + mapas; sin patrocinio) · voz Chatterbox Faraon → doc: docs/estilo_secuencia_yt.md § Runa Caída
- etapa: SUBIDO y PROGRAMADO dom 8-nov-2026 10:00 CDMX (https://youtu.be/fMBEJI5FjaY, 21:07, privado con miniatura Flow)
- siguiente: el usuario lo revisa · .srt a mano en Studio (token sin force-ssl) · medir a 7 días · `limpiar` al aprobar

## Sesiones (plan de tramos · «continúa el video morgott» retoma aquí · protocolo docs/sesiones.md)
- alias: morgott, atrocidades de morgott
- vista previa: MASTER directo, UNA sesión (regla 5-nov); avance reproducible y MASTER a la tele sin preguntar
- leer al empezar: este ESTADO + docs/estilo_secuencia_yt.md § Runa Caída; plantilla de todo: videos/er_radahn_atrocidades/
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion + voz Faraon + seleccionar + tiempo | ✅ 6-nov | hecho |
| 2 | beats, plan de clips, pegatinas, pant(), mapas, MG NUEVOS mg_er | ✅ 6-nov | hecho |
| 3 | OST, SFX del juego, mezcla, chequeo, render, tele, miniatura Flow, subida private + programar | ✅ 6-nov | MASTER 21:07, subido fMBEJI5FjaY |

## Decisiones del episodio (5-nov-2026)
- tema: Morgott (elegido por el usuario de 4: Morgott, Mohg, Godfrey, Rennala); duración: AL MENOS 20 min (pedido del usuario)
- frecuencia del canal: ciclo 4 → 3 días (pedido del usuario), separación mínima 90 → 66 h
- Comentarios (yt-dlp; el token sigue sin force-ssl → 403): 53 nuevos guardados en canales/comentarios/runa_caida.json.
  Pidió el tema @ConkerLord22 (dos veces: 28-oct y 5-nov «ansioso por el de morgott»). Agradecen que se corrigiera «Micuela»
  (@mr.hunter2348 ♥5, @pablofernandez893). Quejas de la voz IA: ~4 (@pablofernandez893 ♥7, @manuelramos7867, @thegoyco93, @huevason)
  → se le reportan al usuario. Corrección: @xAntithesis7x (Blaidd «sick» = impresionante, no asco). Piden: Godfrey/Godwyn
  (@JohnMaldonado), Rennala (@CristianGustavoLara), Llama Frenética (@barialfx) → apuntar. Crítica para burla disfrazada:
  @manuelramos7867 «Que mal que un buen video decaiga tanto por usar la ia» (sin mentir: la voz ES IA).
  Tarjetas hechas (pegatinas/com_<id>.png, 11): Conker ×2, mr.hunter, pablo, cpachon9, luisgonzalez, juancamilo, elimputable,
  manuelramos, xAntithesis, barialfx.
- Campaña de suscripción: 90 d → 2 248 vistas de suscritos de 62 479 = 3,6 % («de cada cien, menos de cuatro»); subs 456 → meta 500 → 1 000

## Hecho el 6-nov-2026 (antes «En curso»)
- Clips 145/145 (035, 047 y 132 rehechos por negros/corrupto), música OST armada, fx (pegatinas con peg_anim.variado; títulos de puesto
  2-4 acortados porque se salían), mezcla (−14 LUFS, voz +14,5 dB), chequeo (pegatinas «clásicas» 1,6/min: cuenta solo peg(); con
  silueta/reliquia/camafeo/abanico/legajo son ~70). youtube.json listo (capítulos, créditos de 18 canales).
- LANZADO: `video && final` (log E:/…/er_morgott_atrocidades/render_log.txt). Después: `tele video er_morgott_atrocidades master` en
  2.º plano → verificar → `yt subir er_morgott_atrocidades runa_caida private --publicar 2026-11-08T16:00:00Z` → registrar en
  canales/runa_caida.json + BITACORA → `canales --actualizar` → cierre (lecciones, docs) → commit.
- Pendiente opcional: ambiente_por (voz de Godfrey en scene-131) no se hizo.
- MINIATURA HECHA (Flow, a la primera): salida/miniatura.jpg (prompt_miniatura.md).
- HECHO en esta sesión: 5 MG NUEVOS en nucleo/mg_er.py (`dos_nombres`, `pila`, `subsuelo`, `trono_vacio`, `cadena`, probados
  en hoja); `efectos.py` COMPLETO (167 FX: pegatinas con silueta/reliquia/camafeo/banda/legajo/abanico, 11 com_, fichas §7,
  mapas limgrave/altus/mundo, `cien` 3 de 100 + meta 456→500→1 000); `_anclas.py` (0 anclas que fallen; correrlo tras cambiar
  efectos); `armar_musica_ost.py` con SECCIONES de Morgott (margit, leyndell, godfrey, mohg, frenesi, morgott, mesa, tema).
- FALTA, en orden: (voz+seleccionar) → `tiempo` → `beats` → `python asignar_clips.py` → `bajar -j 4` → medir_brillo.py →
  hojas `medios` (mirar: menús, Shirrako, YOU DIED, jugador casi desnudo) → rehacer → `ambiente_por` en beats con diálogo/muerte
  de Margit/Morgott/Godfrey (sonido original) y SFX del juego → `fx --seco` (huecos > 4 s) → `fx hoja` (mirar) → `python _bordes.py`
  (copiar de videos/tes_sentinel_teaser/) → armar_musica_ost.py → mezcla → `chequeo` → video → final → `tele video
  er_morgott_atrocidades master` en 2.º plano → verificar → miniatura Flow (receta videos/er_radahn_atrocidades/prompt_miniatura.md,
  personaje Morgott: ingredientes ref_marika de Radahn + pantallas/morgott_jefe.jpg + morgott_render.jpg) → `yt subir
  er_morgott_atrocidades runa_caida private --publicar 2026-11-08T16:00:00Z` → registrar + BITACORA + `canales --actualizar` + cierre.
- Al avisar del MASTER: reportar al usuario las ~4 quejas de la voz IA (no se cambia sola) y la crítica contestada (@manuelramos7867).

## Hecho
- canales --actualizar (Runa URGENTE: hueco dom 8-nov 10:00) · carpeta (`nuevo --yt`) · candado
- OST oficial en audio/ost/ (bajar_ost.py: Margit = Tsukasa Saitoh - Topic, Godfrey = Tai Tomisawa - Topic; morgott/leyndell/
  mohg/rennala/frenesi/gigante/tema/mesa copiados de Melina/Radahn)
- mapas/ limgrave, altus, cumbres (+ rejillas) y mundo · scripts auxiliares copiados de Radahn (por adaptar)

## Lecciones de este video (solo lo no obvio)
- Voz: 4 semillas = ~5 h para 107 frases → `--seeds 1 2`; `_revisar_voz.py` (mejor toma + diff) separa en minutos las falsas alarmas.
- Marcas de MG: se resuelven a su 1.ª aparición en TODO el guion → `_anclas.py` avisa «FUERA» y propone `#n` (30 arregladas).
- `peg()` con `PA.variado` quita «se sienten repetidas»; la densidad de `chequeo` solo cuenta `peg()` clásico.
- Tele: la app cortó las 3 subidas (MASTER 1,5 GB y copia 720p de 423 MB): fallo de Puente TV, no del tamaño.
- Quieto 3,7 s a los 3:56 (`dos_nombres` esperando su marca sobre un clip casi fijo): menor, sin re-render; decide el usuario.
- `_bordes.py`: MemoryError con 21 min y poca RAM: saltado.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/runa_caida.json`, BITACORA)
- [x] HALLAZGOS documentados → docs/estilo_secuencia_yt.md § Runa Caída, canales/formula/runa_caida.md
