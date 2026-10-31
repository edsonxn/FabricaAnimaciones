# Los 40 SECRETOS de Skyrim que nadie te contó — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_tamriel · PROGRAMADO mié 11-nov-2026 12:08 CDMX (2026-11-11T18:08:00Z) · https://youtu.be/-o9sopVzR0o (privado)
- estilo: secuencia_yt (gameplay Skyrim por beat + MG `nucleo/mg_tes.py` + pegatinas + mapas tema `tes`) · voz Chatterbox Sarcastica · música OST oficial de Skyrim → doc: docs/estilo_secuencia_yt.md § Tamriel
- etapa: RESUBIDO y programado 31-oct con la voz Chatterbox (MASTER 18:42, aprobado por el usuario) · REGLA DE ORO escrita · el viejo nlMINAT_6UI queda privado sin fecha · pruebas de voz Johnny (ElevenLabs) en `prueba_voz_eleven/`
- siguiente: monetización en Studio de -o9sopVzR0o (con el OK del usuario) y el usuario borra nlMINAT_6UI en Studio

## Sesiones (plan de tramos · «continúa el video tes_secretos_40» retoma aquí · protocolo docs/sesiones.md)
- alias: 40 secretos, secretos de Skyrim · vista previa: ninguna (el usuario: 🎞 Montaje y aviso al tener el MASTER)
- leer al empezar: docs/estilo_secuencia_yt.md § Crónicas de Tamriel; docs/voz.md antes de `voz`
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión (el usuario, 30-oct): UESP + guion + voz + beats + clips + pegatinas + MG + mapas + OST + mezcla + render + miniatura + subida | ✅ 30-oct | 17:42 con pantalla final; subido nlMINAT_6UI |
| 2 | REHACER con críticas del usuario: **`_plan_rehacer.md`** (voz, beats, clips, pegatinas nuevas, MG, fichas, render, aviso) | ✅ 31-oct | MASTER 18:42 aprobado; chequeo sin ⚠ de densidad (fichas 1,7 · MG 1,4 · mapas 0,7 · pegatinas 3,1/min); resubido -o9sopVzR0o con capítulos y créditos al día |

## Decisiones del episodio (30-oct-2026)
- 18 min pedidos por el usuario; tema elegido entre 3 con datos: «40 SECRETOS» (Choa ×86, Syrric ×4,6; misma lista larga, cambia el tema).
- ~148 frases: gancho 7, cierre 5, ~3-4 frases por secreto (~25 s). Formato `lista_40_secretos_secuencia_yt`.
- Comentarios (89 en 21 d, 4 nuevos): quejas de datos («revisa tus fuentes», «Nazeem sí pisa el palacio») → todo verificado en UESP;
  «¿voz IA?» / acento → se reporta al usuario, no se cambia. Pendiente elegir capturas: ≥ 4 de agradecimiento.
- Disco: E: con 3 GB libres → carpetas pesadas de ESTE video como carpetas reales en C: (28 GB libres); nada de junctions.
- Campaña de suscripción (el usuario, 30-oct, después de grabar la voz): docs/estilo_secuencia_yt.md § CAMPAÑA. Si aún no hay render, añadir el tramo: frases nuevas (~75 %) y su MG; el enlace de la descripción ya sale solo al subir.

## Revisión del MASTER (sin arreglar: decide el usuario)
- Negro 0,6 s en 2:17 y 1,1 s en 15:23 (dentro de clips, finales de los beats 16 y 107). Congelados > 2,5 s en 14:29 y 14:47 (clip de Lydia y mapa).
- `verificar` sin bloqueos; stream de video 1062,07 s con pantalla final incluida.

## Rehacer (hecho el 30-oct, plan en `_plan_rehacer.md`)
- Comentarios críticos contestados (2): @jhonfeddiszabalamoreno9056 «kyrim» (6:00) y @lukelsue4430 «no eres digno» (12:58). Los 2 contestados con burla disfrazada; agradecimientos: 7 tarjetas.

## Hecho
- `nuevo --yt`, panel de canales actualizado · 48 secretos verificados en UESP (`_investigacion_A/B/C.md`, con URL y lo que no casó)
- guion.py final: 42 escenas, 146 frases, 2 708 palabras (21:40 → recortado a ~18 min) · FONETICA · ayudantes copiados de imperdibles (`_pegatinas`, `_coords_uesp`, `_hoja_clips`, `_chequeo_clips`, `_rigor`, `_sonido_original`, `_bajar_ost`, `armar_musica_ost`, `_prueba_mg`, `_prueba_mapas`, `_capitulos`, `_fallidas`) · `mapas/skyrim.jpg` · 50 pegatinas + 8 tarjetas

## Falta
- [x] Miniatura de Flow aplicada (30-oct, el usuario aceptó el aviso de derechos): `prompt_miniatura.md`
- [ ] Monetización en Studio de -o9sopVzR0o
- [ ] El usuario borra nlMINAT_6UI en Studio

## Lecciones de este video (solo lo no obvio)
- Detalle en docs/estilo_secuencia_yt.md § Tamriel y § REGLA DE ORO.
- Al añadir una regla nueva, medir las demás capas: los mapas se comieron las fichas sin que nadie lo viera. `chequeo` lo avisa ahora.
- Resubir tras rehacer: regenerar capítulos y créditos de youtube.json; el tiempo de cada puesto cambia y los clips nuevos deben salir en créditos.
- `Sarcastica` es Johnny de ElevenLabs (docs/voz.md); el usuario decidió subir este con Chatterbox.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/<alias>.json`, BITACORA)
- [x] HALLAZGOS y mejoras documentados en el manual/estilo (ver CLAUDE.md «CIERRE DE VIDEO»)
