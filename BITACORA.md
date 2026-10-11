# Bitácora — Fábrica de Animaciones (resumen; actualizado 2026-10-06, estados verificados contra YouTube)

Solo calendario, decisiones abiertas y estado por canal. **El detalle de cada video vive en `videos/<v>/ESTADO.md`** (`python fab.py estado` los lista todos).
Historial largo de sesiones, métricas y lecciones por video: `docs/historial.md` (no lo leas entero; busca con grep).
Para re-verificar contra YouTube: `python fab.py yt videos <alias>` (los privados programados salen como `private`; la fecha real está en `status.publishAt`).

## 1. Decisiones que esperan respuesta del usuario
1. **Git:** decenas de archivos del núcleo y videos nuevos sin commitear (ver `git status`). Propuesta: un solo commit tras re-verificar que `40mil_anos` no cambia (`python fab.py api` antes).
2. **Bitácora Perdida:** quedan en privado dos subidas viejas de la Independencia (`f4Ipx5rLdmQ` v2 y `1lq_vl0VTGQ` v3): NO publicar; el usuario las borra desde Studio. Siguiente video del canal: `juchipila`.
3. **Sapiens con Wifi:** Neandertales 7-oct y `un_dia_30mil` 14-oct ya programados; después del 14-oct no hay nada.
4. **Cronopapel:** España sale el 7-oct 14:00 y todo se recorrió una semana (Japón 14-oct 13:00, Irán 21-oct 14:00, Egipto 28-oct 11:00). Egipto: arreglar el mapa del inicio y resubir antes del 28.
5. **Edsonxn y LogIA:** sin el siguiente video programado (Edsonxn: Polybius tiene voz, falta lo visual).

## 2. Calendario de publicaciones
| Fecha (CDMX) | Canal | Video (`videos/<v>`) | Estado |
|---|---|---|---|
| 28-sep | Sapiens con Wifi | 10 cosas de hace 40 000 años (`40mil_anos`, Uvg8hX78deo) | Público |
| ~29-sep | Bitácora Perdida | Zacatecas 1546 (`zacatecas_vox`, NwBYB1s0Q3w) | Público |
| 29-sep | Kuriox | ¿Qué pasaría si el Sol se apagara? 8 min (`sol_apagado_8min`, l3JexzfS6-Y) | Público |
| 30-sep | Bitácora Perdida | El tesoro perdido de Moctezuma (`tesoro_moctezuma`, EUXq7-n_i7E) | Público |
| 30-sep 14:00 | Sapiens con Wifi | 7 inventos antiguos (`inventos_antiguos`, ni6FrdYvon0) | Público |
| — | Cronopapel | Historia de China en 3 min (`historia_china`, 4Hc-DNPgiRM) | Público |
| sáb 3-oct 12:00 | Bitácora Perdida | Teotihuacán (`teotihuacan`, riVJpyvvRgg) | Público |
| 3-oct ~19:00 | Edsonxn | Christa Pike: la ejecución que no terminó (`christa_pike`, PGF2sbmC0po) | Público |
| 5-oct | Kuriox | ¿Cómo nació el primer fotón? Short (`primer_foton`, 83T3h3K9gVs) | Público |
| 6-oct ~08:48 | Edsonxn | ¿Quién es Satoshi Nakamoto? El tablero completo (`satoshi_nakamoto`, amA4bPr0aAY) | Público |
| 6-oct ~10:47 | LogIA | Por qué la IA podría DESTRUIR a la humanidad (`ia_noir`, eZlZRGf3VC0) | Público (YouTube aún procesando a mediodía) |
| mié 7-oct 14:00 | Cronopapel | Historia de España en 5 min (`historia_espana`, eSMFJWNy5IA) | Programado |
| mié 7-oct 14:00 | Sapiens con Wifi | Neandertales: 7 mitos (`neandertales`, mlR8vD9ABuw) | Programado |
| jue 8-oct 18:00 | Kuriox | Tu plátano es radiactivo (`platano_radiactivo`, _DJUwuogxeo) | Programado |
| sáb 10-oct 12:00 | Bitácora Perdida | La Independencia de México, completa (`independencia_mx`, dPk9bs6dX0Q) | Programado |
| dom 11-oct 18:00 | Kuriox | La Luna se está yendo (`luna_se_aleja`, Ac5Xv12bllc) | Programado |
| mié 14-oct 13:00 | Cronopapel | Historia de Japón en 5 min (`historia_japon`, EI0c27EY89E) | Programado |
| mié 14-oct 14:00 | Edsonxn | Polybius: el videojuego que nunca existió (`polybius`, 6rqPo_fgz58) | Programado |
| mié 14-oct 14:00 | Sapiens con Wifi | Un día en la vida hace 30.000 años (`un_dia_30mil`, MADQ6aemfZY) | Programado |
| mié 14-oct 18:00 | Kuriox | ¿Cuánto pesa una nube? (`peso_nube`, xYM1mFDrmZs) | Programado |
| sáb 17-oct 18:00 | Kuriox | ¿Por qué se arrugan los dedos? (`dedos_arrugados`, qcdEAcp9r84) | Programado |
| mar 20-oct 18:00 | Kuriox | ¿Por qué el cielo es azul? (`cielo_azul`, kCqZ1Bep07s) | Programado |
| mié 21-oct 14:00 | Cronopapel | Historia de Irán en 5 min (`historia_iran`, CqSg_v6pFjQ) | Programado |
| mié 28-oct 11:00 | Cronopapel | Historia de Egipto en 5 min (`historia_egipto`, 3V_C7ZEj5is) | Programado; PENDIENTE arreglar el mapa del inicio y resubir |
| sin fecha | LogIA | Deepfake: la videollamada donde NADIE era real (`videollamada_falsa`, SNmr4gh5PkY) | Subido en PRIVADO el 7-oct; el usuario decide la fecha |
| vie 9-oct 16:00 UTC | Wild Next Door | Why Spiders "Invade" Your House Every Fall (`aranas_otono`, A0uq0XZgWmI) | Público |
| sáb 10-oct 10:00 | LogIA | Deepfake: la videollamada donde NADIE era real (`videollamada_falsa`, SNmr4gh5PkY) | Programado |
| ~~lun 12-oct~~ **vie 9-oct 01:32 UTC** | Wild Next Door | Never Kill a House Centipede (`ciempies_casa`, 8voZAKYUAkM) | **Público** (salió antes de lo programado; 440 vistas el 11-oct = ganador del canal) |
| dom 18-oct 16:00 UTC | Wild Next Door | Never Kill the Spider in Your Ceiling Corner (`arana_techo`, gG2REwAK54Q) | Programado |
| jue 15-oct 16:00 UTC | Wild Next Door | Where Do All the Bugs Go in Winter? (`bichos_invierno`, AYmaIJedCPc) | Programado |
| mar 3-nov 13:00 | Plastitube | El cilindro vacío que seguía pesando lo mismo (`teflon_sarten`, bQj_Ip4dhEo) | Programado |
| sin fecha | (prueba, sin canal) | Mostacho y el ruido de la cocina, cartoon90 (`gato_cobarde`) | El usuario renderiza escena por escena desde el panel |


## 3. Estado por canal (una línea cada uno; detalle en historial.md §3-§5)
- **Bitácora Perdida** (`bitacora_perdida`): Kurzgesagt SIEMPRE. Los de ~2:40 rinden mejor. Teotihuacán ya público. Independencia completa programada sáb 10-oct 12:00 (dPk9bs6dX0Q). **Siguiente: `juchipila`** (voz hecha, escenas por hacer en el panel).
- **Sapiens con Wifi** (`sapiens_con_wifi`): 10 suscriptores. Neandertales 7-oct; `un_dia_30mil` programado 14-oct (MADQ6aemfZY). Miniaturas del canal: POR CÓDIGO (`miniaturas.py`), confirmado por el usuario el 6-oct. Siguiente: sin video en producción.
- **Cronopapel** (`cronopapel`): 44 subs. Cubierto hasta el 28-oct (España 7, Japón 14, Irán 21, Egipto 28).
- **Kuriox** (`kuriox`): 68 subs. Shorts programados hasta el 20-oct (verificado); después, nada. Sol 1 min (`sol_apagado`) sigue con el termómetro mal renderizado.
- **Edsonxn** (`edsonxn`): 1660 subs. Christa Pike (3-oct) y Satoshi (6-oct) públicos. **Siguiente: Polybius** (o una noticia viva).
- **LogIA** (`logia`): 6 subs. `ia_noir` publicado 6-oct (estilo noir). `videollamada_falsa` (robo deepfake de Hong Kong, 6:31; voz ElevenLabs «David» con corchetes de actuación + SFX de ElevenLabs) subido en PRIVADO el 7-oct (SNmr4gh5PkY), sin fecha.
- Plan semanal acordado (30-sep): 1 video por semana por canal, 5-8 min; no pasar de 15 min sin datos de retención.

## 4. Motor y repositorio (pendientes)
- [ ] `python fab.py api` (API.md desactualizado) y re-verificar `videos/40mil_anos`.
- [ ] Commit de lo nuevo (`nucleo/` y videos) — esperando decisión §1.1. Nunca subir tokens, secrets, métricas ni voz/audio/render.
- [ ] Disco C: los MASTER de 400-700 MB se acumulan; el 1-oct otra sesión limpió voz/render de videos viejos (`40mil_anos`, `sol_apagado_8min`…).
- [ ] Estilo `vox` y optimizaciones de render aún no documentados en `docs/`.

## 5. Cómo mantener esto
Al terminar un video o sesión: actualiza `videos/<v>/ESTADO.md` (etapa + siguiente paso exacto), y aquí solo el calendario (§2) si cambió algo publicable. Nada de narrativa larga en este archivo.
- 3-oct-2026 · Edsonxn: «Christa Pike: la ejecución que no terminó» (8:15, documental de noticia, motion graphics propios) subido en PRIVADO https://youtu.be/PGF2sbmC0po con miniatura IA («SOBREVIVIÓ A SU EJECUCIÓN») y .srt. Lo publica el usuario desde Studio; revisar «Derechos de autor» (extractos de WBIR, France 24, NBC, ABC, NewsChannel 5) y las noticias del día.
- 5-oct-2026: Short «¿Cómo nació el primer fotón?» publicado en Kuriox (83T3h3K9gVs), video primer_foton.
- 5-oct-2026: 5 Shorts de ciencia (boceto+guache vertical) para Kuriox, uno cada 3 días 18:00 CDMX: platano_radiactivo 8-oct (_DJUwuogxeo), luna_se_aleja 11-oct (Ac5Xv12bllc); pendientes peso_nube 14-oct, dedos_arrugados 17-oct, cielo_azul 20-oct.
- 5-oct-2026: programados en Kuriox (18:00 CDMX): platano_radiactivo 8-oct, luna_se_aleja 11-oct, peso_nube 14-oct (xYM1mFDrmZs), dedos_arrugados 17-oct (qcdEAcp9r84), cielo_azul 20-oct (kCqZ1Bep07s).
- 6-oct-2026: estados verificados contra YouTube: Christa Pike y Satoshi (Edsonxn) e ia_noir (LogIA) ya públicos; China y Teotihuacán públicos; Cronopapel reprogramado por el usuario (Japón 7-oct 13:00, Irán 14-oct, Egipto 21-oct 11:00); Independencia sigue privada sin programar.
- 6-oct-2026: Bitácora Perdida: «Independencia de México: la historia completa» v5 subida y PROGRAMADA sáb 10-oct 12:00 CDMX (dPk9bs6dX0Q) con miniatura IA de Google Flow y .srt; las subidas viejas f4Ipx5rLdmQ y 1lq_vl0VTGQ quedan privadas para que el usuario las borre en Studio.
- 6-oct-2026: Cronopapel: «Historia de España en 5 minutos» subida y PROGRAMADA mié 7-oct 14:00 CDMX (eSMFJWNy5IA) con miniatura por código y .srt; Japón, Irán y Egipto recorridos una semana (14, 21 y 28-oct) a pedido del usuario. `un_dia_30mil` (Sapiens): la voz ya estaba completa; `tiempo` hecho (3:30), falta revisar escenas y renderizar.
- 6-oct-2026: Sapiens con Wifi: «Un Día en la Vida Hace 30.000 Años» (3:30, doodle) subido y PROGRAMADO mié 14-oct 14:00 CDMX (MADQ6aemfZY) con miniatura por código (se probó una de Flow y el usuario pidió volver a la de código) y .srt; las 9 escenas se corrigieron antes del render (huecos vacíos, rótulos encimados, figuras montadas).

- 6-oct-2026 · **Wild Next Door** (canal nuevo en la Fábrica, inglés, motor secuencia/Google Flow): «What Happens to Wasps When Winter Comes?» publicado en público, https://youtu.be/sHqcDnMrQTU (`videos/avispas_invierno`).
- 7-oct-2026 · **Wild Next Door**: «Why Spiders "Invade" Your House Every Fall (They Don't)» publicado en público, https://youtu.be/9E9j5ZWxZHo (`videos/aranas_otono`, 4:37, todo imagen de Flow).
- 7-oct-2026 · **Wild Next Door**: «Never Kill a House Centipede. Here's Why» publicado en público, https://youtu.be/oFi5HDkClVE (`videos/ciempies_casa`, 4:23, todo imagen).
- 7-oct-2026 · **Wild Next Door**: «Where Do All the Bugs Go in Winter?» publicado en público, https://youtu.be/mqHB3cK7RF8 (`videos/bichos_invierno`, 8:39; primeros 70 s en 7 clips de Flow 360p reescalados, 2 escenas por clip).
- 7-oct-2026 · **Wild Next Door, CORRECCIÓN**: publicar los tres de arriba el mismo día fue un error. Pasados a PRIVADO (9E9j5ZWxZHo, oFi5HDkClVE, mqHB3cK7RF8); solo queda público el de avispas (6-oct). Regla nueva: un video cada 2-3 días por canal, nunca varios el mismo día (CLAUDE.md, `docs/publicacion.md`, freno en `nucleo/youtube.py`). Pendiente: republicarlos espaciados (no se pueden programar por API porque ya fueron públicos: o se hacen públicos a mano el día que toque, o se resuben y se programan).
- 7-oct-2026 · **Plastitube** (alias `pieza_oculta`, antes «La Pieza Oculta»; canal pasado a español): primer video hecho en la Fábrica, «El cilindro vacío que seguía pesando lo mismo» (teflón), subido en PRIVADO sin fecha, https://youtu.be/bQj_Ip4dhEo (`videos/teflon_sarten`, 6:10, 89 imágenes de Flow, música Lyria por tramos). El canal tiene ocupados 13, 20 y 27-oct 19:00 UTC. Falta el .srt (el token no tiene permiso de subtítulos).
- 7-oct-2026 · **Ciclos fijados por el usuario:** LogIA cada 4-5 días; Wild Next Door cada 3 días; Plastitube sigue su ciclo semanal (martes 19:00 UTC). Programados: LogIA `videollamada_falsa` sáb 10-oct 16:00 UTC (SNmr4gh5PkY); Wild Next Door RESUBIDOS (un video que ya fue público no se deja programar: HTTP 400) y programados 16:00 UTC: arañas 9-oct (A0uq0XZgWmI), ciempiés 12-oct (8voZAKYUAkM), bichos 15-oct (AYmaIJedCPc); las subidas viejas 9E9j5ZWxZHo, oFi5HDkClVE y mqHB3cK7RF8 quedan en privado para que el usuario las borre en Studio. Plastitube `teflon_sarten` mar 3-nov 19:00 UTC (bQj_Ip4dhEo). Siguientes huecos: LogIA 14/15-oct, Wild Next Door 18-oct, Plastitube 10-nov.
- 7-oct-2026 · Edsonxn: «Polybius: el videojuego que nunca existió» (5:16, tablero de detective vivo + 18 escenas dibujadas, kit `arcade.py`) subido y PROGRAMADO mié 14-oct 14:00 CDMX (6rqPo_fgz58) con miniatura por código y .srt. Siguiente hueco del canal: 21-oct.
- 7-oct-2026 · Edsonxn: Polybius RESUBIDO sin el clic repetido de las chinchetas (6rqPo_fgz58, misma fecha 14-oct 14:00 CDMX). La subida anterior QMrTGVJXIEg quedó en privado sin programar: el usuario la borra en Studio.
- 8-oct-2026: LogIA, video nuevo `informante_2027` («Qué pasará con la IA en 2027: la advertencia del que renunció a OpenAI», 10:32, noir) con MASTER hecho. SUBIDO en privado y PROGRAMADO mié 14-oct-2026 14:00 CDMX (eHIxoZLpbMc; publishAt 2026-10-14T20:00:00Z), con miniatura y .srt. Ojo: LogIA dio 401 en escrituras hasta forzar la renovación del token (expiry_date=0).
- 8-oct-2026: LogIA, `informante_2027` REHECHO (texto paralelo a las hojas, caminatas) y resubido en privado: 5D-kQtNWF4w, programado mié 14-oct-2026 14:00 CDMX (publishAt 2026-10-14T20:00:00Z). Sustituye a eHIxoZLpbMc, que el usuario borra en Studio.
- 11-oct-2026: Bitácora Perdida, «Juchipila: el pueblo de las flores y la guerra» (8:18) SUBIDO en privado: UHZ9sXW0D1g (miniatura Flow «FLORES Y GUERRA»), SIN programar; usuario decidió subir el render actual con defectos documentados en docs/estilo_kurzgesagt.md. Hueco sugerido: jue 15-oct 14:00 CDMX (20:00 UTC).
- 11-oct-2026: Juchipila (UHZ9sXW0D1g) PROGRAMADO jue 15-oct-2026 14:00 CDMX (publishAt 2026-10-15T20:00:00Z): ciclo de 5 días desde Independencia (10-oct).
