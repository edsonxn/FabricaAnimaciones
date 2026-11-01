# Las 15 misiones de Skyrim que NUNCA debes hacer — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_tamriel · meta: primer hueco ≥ 96 h tras exploits (18-oct 18:06 UTC) → desde 22-oct 18:06 UTC; ≥ 14 min (el usuario)
- estilo: secuencia_yt (gameplay Skyrim por beat + MG `nucleo/mg_tes.py` + pegatinas) · voz Chatterbox Sarcastica → doc: docs/estilo_secuencia_yt.md § Tamriel
- etapa: ✅ SUBIDO y PROGRAMADO jue 22-oct-2026 12:07 CDMX (2026-10-22T18:07:00Z) · https://youtu.be/R4nzGhWuTmo · MASTER v3 (17:29 con pantalla final) con miniatura
- siguiente: monetización HECHA en Studio (21-oct: anuncios Activada + mid-rolls, cuestionario «Adecuado para anuncios», en «Comprobando») · .srt CARGADO (21-oct, tras reconectar Tamriel con force-ssl; sigue private + publishAt 22-oct 18:07Z) · cierre: hallazgos en docs/estilo_secuencia_yt.md § Tamriel · `limpiar` cuando salga público

## Sesiones (plan de tramos · «continúa el video tes_misiones_nunca» retoma aquí · protocolo docs/sesiones.md)
- alias: misiones que nunca debes hacer, 15 misiones, tamriel 15 misiones · vista previa: NO (como exploits): solo el MASTER al final
- leer al empezar: este ESTADO + docs/estilo_secuencia_yt.md § «Crónicas de Tamriel», § PEGATINAS y § MOTION GRAPHICS NUEVOS; copiar de videos/tes_exploits_rotos/
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion verificado en UESP + FONETICA + voz Chatterbox + seleccionar + tiempo + beats | ✅ 19-oct | 146/146 frases, voz 955,6 s, 1 029 s naturales, 121 beats |
| 2 | busquedas + bajar clips + hojas + pegatinas + 4 MG nuevos en mg_tes + `fx` (Montaje) | ✅ 20-oct | 120 clips (105 videos), 104 FX, 23 SFX |
| 3 | Lyria (9 tramos) + mezcla + render + revisión del MASTER (+ blackdetect) + miniatura propia + subir private/programar | ✅ 21-oct | Lyria 9/9, mezcla, render v1→v3 (10 clips rehechos, logo msi recortado), final, rigor, miniatura Flow, subido R4nzGhWuTmo programado 22-oct 12:07 CDMX |

## Decisiones del episodio (19-oct-2026)
- tema elegido por el usuario entre 3 con datos: misiones que NUNCA debes hacer (ref.: «misiones daédricas PROHIBIDAS» 9 141 en
  5 días, ×4; fuera «NÃO FAÇA ESSA MISSÃO» ×425, SmackerUnknown «Most Hated Quest» ×6,6). Variable que se prueba: sale de lo
  daédrico + 15 puestos/≥ 14 min. 3 sesiones (el usuario). Sin patrocinio. Puente final a misiones daédricas (O2ZsE2AFGYc).
- lista (15→1): piedras de Barenziah · experimento de Arniel · forja de Aetherium · Sangre en el hielo (Calixto) · meadería
  Honningbrew · mina de Cidhna · Eldergleam · faro de Soledad (Icerunner) · cabaña de Astrid · Narfi · Helgi/Laelette (Morthal) ·
  boda de Vittoria Vici · matar al Emperador · destruir la Hermandad · Paarthurnax. Ninguna daédrica (no repite el video del 14-oct).
- formato a anotar al subir: `lista_15_misiones_nunca_secuencia_yt`
- MG nuevos propuestos (frase ancla): (1) «LA CABAÑA» p7_5/p2_2: cuatro siluetas (3 rehenes + Astrid), una se tacha; vuelve en p2 con
  Astrid tachada en rojo · (2) «EL CARNICERO» p12_4-p12_7: tablero de sospechosos, sello ARRESTADO sobre Wuunferth y giro a Calixto ·
  (3) «LA CADENA DE LA HERMANDAD» p4_8-p3_7: boda → Emperador viene → sopa → doble → traición → santuario en llamas, el último
  eslabón se rompe · (4) «LA BALANZA» p2_5-p2_8: 3 000 monedas contra Shadowmere, 20 000, maestros, armadura, Cicero.

## Hecho
- guion.py con datos verificados en UESP (fuentes en el docstring), FONETICA con "Skyrim": "Eskaai rim"
- voz: 146/146 (22 aceptadas por CER/TAIL/GAP_MAX_POR_FRASE tras leer la transcripción); p1_8 reescrita, p15_0 con 4 tomas
- tiempo: 1 029,3 s naturales (MASTER ≈ 17:30 con pantalla final); los 9 tramos de LYRIA caben (115-131 s; p2 solo, 59 s) · beats: 120
- clips (19-oct): busquedas.json del borrador + 45 correcciones; bajar 96/120 (001-024: «not a bot», bajaron con -j 2); hojas:
  33 rechazados → 4 pasadas, 11 fijados con {url, desde}; creditos.txt completo (títulos de los fijados puestos a mano)
- efectos.py (20-oct): 16 avisos, 16 fichas, 65 pegatinas (16 grandes; imágenes en pegatinas/, fuentes en _fuentes.txt) y 4 MG
  nuevos en mg_tes (6 apariciones): sospechosos p12_3-6, rehenes p7_4-7 y p2_1, cadena p4_7 + p3_2-6, balanza p2_4-7. SFX nuevos:
  sello, cerrojo, cadena, fuego (80 créditos); mision_a/b y monedas copiados de exploits. `fx hoja` cazó 7 clips más (rehechos).

## Falta
- [ ] sesión 3
- [ ] clips flojos aceptados (oscuros pero en tema), mirar en el MASTER: 005 009 012 016 024 038 042 043 063 084 092 107
- [ ] escuchar al menos «Barenziah» (p15_0, Whisper oye «Varencia») y p1_8 antes del render
## Cómo retomar (comandos)
```
python fab.py continuar tes_misiones_nunca
python fab.py tes_misiones_nunca musica      # luego mezcla · video · final (docs/estilo_secuencia_yt.md § Música)
```

## Archivos clave
- `guion.py`, `beats.json`, `busquedas.json`, `fuentes.json`, `efectos.py`, `pegatinas/`, `medios/`, `salida/creditos.txt`

## Lecciones de este video (solo lo no obvio)
- Chatterbox Sarcastica: «te repite» → «telepite» (r entre vocales tras «te»): reescribir la frase, no insistir con semillas.
- Revisión del MASTER (21-oct): 10 clips rechazados que no vieron las hojas de medios; `--q` falló en 6/10 y `--url --desde`
  tras escanear la guía de la misión a 360p acertó 5/5 (detalle en docs/estilo_secuencia_yt.md § Tamriel).
- Skyrim en YouTube: la elección automática cae mucho en MENÚS/inventario/mapa (guías de misión) y en videos de lore
  (fan-art, Legends, Minecraft, UE5, streamer): fijar {url, desde} de un video ya visto bueno, no insistir con --rehacer.

- `final` cortado a mitad del anexo de la pantalla final deja `*_MASTER.mp4.con_pf.mp4` sin «moov atom» (21-oct): borrarlo y
  repetir `final` (usa `video_sin_audio.mp4`, segundos). Separación 96 h se mide contra la hora REAL de salida (18:06:09):
  programar al minuto siguiente, no a la misma hora redonda.

## Cierre (regla del 12-oct-2026)
- [x] subido, miniatura, programado y registrado (`canales/cronicas_tamriel.json` con "formato", BITACORA) — 21-oct
- [ ] HALLAZGOS y mejoras documentados en docs/estilo_secuencia_yt.md § Tamriel
