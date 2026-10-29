# La Crematoria: dos padres, dos hijos y una espada — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: gaia_eterna (alta 29-oct-2026; falta `yt conectar` con la cuenta de la esposa) · sábado 10:00 CDMX, primer hueco tras el MASTER
- estilo: pegatina_flow (formato «Pamela») → docs/estilo_pegatina_flow.md § 8 · ejemplo: videos/wow_darrowshire/ · mapas: nucleo/mg_mapa.py tema "wow"
- etapa: voz ✅ · OST ✅ · Flow 192 imágenes ✅ · recorte ✅ · reales/mapas/SFX ✅ · escenas (plan.py, ~300 tomas) ✅ · mezcla ✅ · RENDER en marcha (10:14, 865 segmentos) · miniatura ✅ · youtube.json ✅
- siguiente: al acabar el render → `fab.py gaia_crematoria final` → `verificar` → aviso al usuario → `yt conectar` (cuenta de la esposa) → subir y programar

## Sesiones (plan de tramos · «continúa el video gaia_crematoria» retoma aquí · protocolo docs/sesiones.md)
- alias: gaia_crematoria, la Crematoria, el de Gaia Eterna, el de Tirion y los Mograine, el de la Ashbringer
- vista previa: 🎞 Montaje del panel con audio completo conforme salen las escenas (pendiente de confirmar con el usuario)
- leer al empezar: este ESTADO.md, `fuentes_lore.md`, docs/estilo_pegatina_flow.md § 8 y videos/wow_darrowshire/ESTADO.md
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | Alta del canal + casting de voces + lore con fuentes + guion 40-50 min | ✅ 29-oct | canal ✅, voz narradora ✅, casting ✅ (elegido en casting.html), lore ✅, guion ✅ ~44 min |
| 2 | Voz (narradora + personajes) + seleccionar + tiempo + OST | ✅ 29-oct | 367 frases (~6 000 créditos); 1 bloqueada por el filtro (reescrita); 8 regeneradas; 43:14; OST 15 pistas |
| 3 | Flow (escenarios + hojas con ciclos + utilería) + recorte + profundidad + reales + mapas + SFX del juego | ✅ 29-oct | 96 prompts x2 (proyecto Flow «oct 29 - 09:33»), 30 hojas, 37 reales + 8 iconos + 8 medallones, 10 mapas, 93 SFX |
| 4-6 | Escenas por actos + sfx + mezcla | ✅ 29-oct | MOTOR POR DATOS: `escenas.py` dibuja y `plan.py` describe ~300 tomas; muestras cada 40 s revisadas (`_muestras.py`) |
| 7 | Render → MASTER → aviso al usuario → miniatura → youtube.json | pendiente | render ≈ 2,5 h (13:30 = 45 min) |
| 8 | Subir (tras `yt conectar`) + registro + cierre | pendiente | |


- `audio/` pasado a carpeta REAL en C: (E: dio Ntfs 55 el 28-oct; ver memoria disco-e-fallando). `voz/` sigue en E:.

## En curso (29-oct, tramo 7) — el usuario: «termina todo en esta sesión hasta tener el MASTER»
- `fab.py gaia_crematoria video` LANZADO 10:14 (log `render_log.txt`); solo 5-6 procesos: la memoria virtual está corta porque C: tiene
  8,6 GB libres (el pagefile no crece). Segmentos y salida en E: (0 errores de disco en 3 h). Si se corta: borrar `seg_*.tmp.mp4` y relanzar.
- Hecho y listo para el cierre: `salida/miniatura.jpg` (`_miniatura.py`), `youtube.json` (título, capítulos, fuentes), eco de ultratumba
  (`_ultratumba.py`, 26 frases; originales en voz/final_orig), `audio/fx.wav` (`_sfx_juego.py`, 174 sonidos), `audio/final.wav`.

## Decisiones con el usuario (29-oct-2026)
- Canal: Gaia Eterna (de su esposa). Narradora = su voz clonada (probadas 19 emociones con corchetes: «suenan bien»).
- Tema elegido entre 3 propuestas con datos (`canales/formula/gaia_eterna.md`): La Crematoria, terror + heroísmo, 40 min MÍNIMO.
- Pedido: mapas reales con ruta en algunas escenas, VARIAS VOCES de ElevenLabs para los personajes con emociones, SFX DEL JUEGO.

## Voces
- Narradora: `BwV6RplmLHPGm7QVf6II` («Zyan gameplay 2», clonada, SOLO cuenta 2; `tts_eleven.post` ya salta de cuenta con
  `voice_not_found`). eleven_v4_turbo, stability 0,5. Pruebas: `videos/gaia_prueba_voz/`.
- Casting (`_prueba_personajes.py`, `muestras_personajes/todas.mp3`, 2 candidatos por personaje, 350 créditos):
  Alexandros salvatore/elder · Tirion arturo/elder · Renault enrique/antonio · Darion alejandro/david · Taelan david/antonio ·
  Isillien murdock/odran · Kel'Thuzad ivan/mordred · Rey Exánime miguel/final_boss · Eitrigg ragnar/ludovico (todas en español).
- ELEGIDAS por el usuario (29-oct, página `casting.html` en `localhost:8773`, launch «casting-crematoria»):
  Alexandros Salvatore `t3eeeqhBjrUqcrPvDqUn` (eligió Elder para los dos padres; el usuario dejó Elder a Tirion) · Tirion Elder
  `gSYqSbtMajxq5LUT0bNl` · Renault Enrique Mondragón
  `iDEmt5MnqUotdwCIVplo` · Darion Alejandro `byWOh4ohcovt7I8koF2I` · Taelan Antonio `htFfPSZGJwjBv1CL0aMD` · Isillien Murdock
  `OLmSqlYzB06EIKJRy5b0` · Kel'Thuzad Mordred `UFO0Yv86wqRxAt1DmXUu` · Rey Exánime Miguel `k8cFOyAg7B9qwBlDDNTC` · Eitrigg Ludovico
  `GTY55jD77hLBRrnQOhNk`.

## Guion (29-oct)
- `guion.py` aplana `actos_1/2/3.py` (cada frase str = narradora, tupla (personaje, texto) = VOZ_POR_FRASE con `VOCES`); `plan` de
  cada acto = imagen/mapa/SFX para el tramo de escenas. Lectura para el usuario: `guion_lectura.md` (regenerar si se edita).
- Canon = cómic «Ashbringer» + Chronicle 3 + misiones; lo de Classic desplazado se cuenta como «lo que vivieron los jugadores».
  Diálogos = adaptaciones (las líneas oficiales en español no se pudieron verificar). Voces con eco en la mezcla: Kel'Thuzad y el Rey.
- Música: BANDA SONORA OFICIAL de WoW (el usuario, 29-oct) → `armar_musica_ost.py` (secciones por escena; lista de pistas en su docstring).

## Tiempos (timeline.json, 29-oct)
- gancho 0 · bienvenida 80 · elena 109 · orbe 178 · mano_plata 233 · costasur 316 · forja 382 · eitrigg 466 · juicio 556 ·
  plaga 709 · complot 796 · traicion 873 · testigo 978 · naxxramas 1040 · susurros 1142 · culpa 1178 · cta_mitad 1240 ·
  darion_busca 1269 · monasterio 1356 · misterio 1436 · ermitano 1505 · taelan_hijo 1589 · recuerdos 1676 · en_suenos 1778 ·
  capilla_1 1909 · acherus 2044 · alba 2102 · epilogo 2389 · cierre 2542 → 2594,5
- `audio/` es carpeta REAL en C: (E: dio Ntfs 55 el 28-oct); `voz/` sigue en E: (pasarla a C: antes del render).

## Lecciones de este video (solo lo no obvio)
- 43 min de pegatina Flow en UNA sesión: en vez de escribir tomas a mano (Darrowshire: 3 200 líneas para 13 min), un MOTOR
  por datos (`escenas.py`) + `plan.py` (una línea por toma: escenario, cámara, luz, actores con códigos de 2 letras, ambiente, reales,
  iconos, rótulos, mapas, SFX). La PLACA de quien habla (medallón + nombre en oro) sale sola de PERSONAJE_POR_FRASE.
- El navegador integrado NO comparte el portapapeles de Windows: el paquete de Flow se inyecta directo en `javascript_tool`.
  Enviar con clic por código al botón «Iniciar generación» NO envía: hace falta la tecla Enter real.
- Columnas de luz recortadas de Flow se ven como papel: rayos procedurales aditivos (`columnas_luz`).
- `_muestras.py --rango` debe pasar `float` (np.float64 en `t` vuelve float64 los mapas de cv2.remap y truena).
- `fab.py nuevo --help` CREA un video llamado «--help» (borrado: junctions primero con rmdir).
- Whisper oye «Lord Dairon» por Lordaeron y «Mugrain/Mowgrain» por Mograine → ALIAS_QA.
- 1.ª `seleccionar`: 78 «fallos» y casi todos eran NOMBRES (Tyrion Badin, Eitrig, Renaud, Balnazar, Rivalimpia, Thailand…):
  ALIAS_QA con claves YA normalizadas (sin tildes ni apóstrofos) y `seleccionar` otra vez (reusa `voz/eval.json`, no gasta).
  Solo 8 eran tropiezos reales («caudeada», «abuelada», «volvieron a Vlad», «Uy» por «Hoy») → otra semilla (~170 créditos).
- Filtro de ElevenLabs (403 content_against_policy): «Si he de morir, quiero morir de pie, contigo» (Darion joven) → reescrita.

## Cierre (regla del 12-oct-2026)
- [ ] subido y PROGRAMADO en el hueco del canal, miniatura y registrado (`canales/gaia_eterna.json`, BITACORA)
- [ ] HALLAZGOS documentados (docs/estilo_pegatina_flow.md, canales/formula/gaia_eterna.md)
