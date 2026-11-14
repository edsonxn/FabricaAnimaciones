# Los SECRETOS del teaser de The Elder Scrolls VI: Sentinel — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_tamriel · se sube PRIVADO sin fecha: el usuario lo ve y lo publica él (3-nov-2026; movió el video de hoy al 6)
- estilo: secuencia_yt (gameplay Skyrim/ESO/teaser por beat + MG `nucleo/mg_tes.py` + pegatinas + mapas tema `tes`) · SIETE voces ElevenLabs que compiten (Johnny, Edoardo, Hope, José, Mario, MariCarmen, el Profeta) + el Humano tras el Telón (voz clonada del usuario); el público vota · OST oficial → doc: docs/estilo_secuencia_yt.md § Tamriel + § REGLA DE ORO
- etapa: SUBIDO PRIVADO sin fecha el 3-nov: https://youtu.be/TM5ivAWiF0o (MASTER 22:18, 153 beats, 228 FX); falta el visto bueno del usuario
- siguiente: el usuario lo revisa y lo publica; a los 7 días contar en los comentarios qué voz gana y decírselo; `fab.py tes_sentinel_teaser limpiar` al aprobar

## Sesiones (plan de tramos · «continúa el video tes_sentinel_teaser» retoma aquí · protocolo docs/sesiones.md)
- alias: sentinel, elder scrolls 6, teaser de TES VI · vista previa: ninguna (aviso al tener el MASTER y subida en privado)
- leer al empezar: docs/estilo_secuencia_yt.md § REGLA DE ORO y § Crónicas de Tamriel; docs/voz.md § Johnny
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión (el usuario, 3-nov): UESP + guion + voz + beats + clips + pegatinas + MG + mapas + OST + mezcla + render + miniatura Flow + subida PRIVADA | ✅ 3-nov | 3 cortes por contexto: s1 guion + voz; s2 beats, clips, efectos.py; s3 siete voces (muestras → elección del usuario), Humano tras el Telón, comentarios ≤ 10 días, cierre → 15 armas, bordes (`_bordes.py`), `_remapear.py` v1→v4, MASTER 22:18 y subida privada TM5ivAWiF0o |

## Decisiones del episodio (3-nov-2026, el usuario)
- Tema elegido entre 3: «Los 15 SECRETOS del teaser de Elder Scrolls 6: Sentinel» (noticia del día; IGN 121 k en horas).
- **≥ 16 min**: si falta, relleno con lore, curiosidades y easter eggs de Hammerfell, Sentinel y los Pergaminos.
- **Voz nueva: Johnny** (ElevenLabs `HMCmDsbKeaSZp5LMOYKR`, turbo). Saldos 3-nov: c1 5 555 · c2 35 005 · c3 1 195.
- **≥ 3 críticas contestadas con burla disfrazada** (el usuario; más que el 1-2 de la regla), no usadas antes:
  `UgyR2Rnl7yIODqxw1z14AaABAg` «Puto video hecho con IA» (armas) · `UgyRNHW2x-zACQueNkF4AaABAg` «Dile a la IA que revise sus fuentes»
  · `UgyYrD3Rsm_VnW1DviV4AaABAg` «Están mejor los vídeos del Gerber» (El Gerber también cubre Sentinel).
- «Puto»: NO afecta a la monetización si va una vez dentro del video (YouTube solo castiga título/miniatura o uso frecuente;
  desde jul-2025 ni en los primeros 7 s) → se dice y se ve sin censura; nunca en título, miniatura ni descripción.
- ≥ 4 agradecimientos + campaña de suscripción (~75 %, 6 450 → meta 10 000) + mapa de Hammerfell/Sentinel con ruta.
- Material del teaser en `_ref/` (teaser 64,7 s `mFu8t9735IY`, transcripción del video de 40 años `SlB27bu6XGE` en `aniv.txt`).

## Hecho
- MASTER 22:18 + `.srt`, subido privado `TM5ivAWiF0o` con miniatura Flow y descripción ≤ 5 000 bytes (37 fuentes + créditos); registrado en `canales/cronicas_tamriel.json` y BITACORA; docs/voz.md § VARIAS VOCES y docs/estilo_secuencia_yt.md (bordes, clip de otro tema)
- `nuevo --yt`, candado, `canales --actualizar` (Tamriel BIEN; Bitácora URGENTE hoy) · comentarios leídos (3 nuevos)

## Falta
- [ ] visto bueno del usuario y publicación (él) · Studio: monetización · a 7 días: recuento de votos por voz

## Lecciones de este video (solo lo no obvio)
- **Nunca mandar a un video que todavía no está público** (el usuario, 3-nov): el cierre citaba los 40 secretos (sale el 11-nov); mirar `canales/<alias>.json` → publicados antes de recomendar.
- Comentarios en pantalla: solo de ≤ 10 días (`nucleo/comentarios.py` `MAX_DIAS`).
- Cambiar la voz con el video montado: `_remapear.py` conserva los clips por texto (ver docs/voz.md § VARIAS VOCES).
- La descripción de YouTube se mide en BYTES: `_youtube.py` `_cabe()` recorta fuentes (≥ 30) y créditos; sin `salida/creditos.txt`, créditos = canales de `fuentes.json`.
- Un clip de búsqueda puede ser un meme con escenas de series (081, Breaking Bad): mirar SIEMPRE `previews/final_hoja.jpg`.
