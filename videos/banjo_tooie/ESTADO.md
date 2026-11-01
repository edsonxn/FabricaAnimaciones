# Banjo-Tooie: su historia y los 10 secretos QUE IGNORASTE — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_gaming · meta: ANTES del 30-oct-2026 (gancho = Evercade del 30-oct; si sale después, «sale» → «salió» en intro/p1)
- estilo: secuencia_yt (gameplay por beat + pegatinas + fichas + MG `nucleo/mg_gaming.py`) · **voz ElevenLabs Hope** (`tnSpp4vdxKPjI9w0GnoV`, eleven_v4 + corchetes; antes Chatterbox Sarcastica) → doc: docs/estilo_secuencia_yt.md
- etapa: ✅ PUBLICADO 20-oct-2026 ~14:00 UTC (público al momento, a pedido del usuario): https://youtu.be/HxURLhWv1Vs (15:07, voz Hope). El 1.er upload (zJkKmdBzlpE, Chatterbox) quedó PRIVADO → `retirados` de cronicas_gaming.json
- siguiente: .srt a mano en Studio si se quiere (la API no lo subió) · registro a 7 días en canales/formula/cronicas_gaming.md (27-oct) · al aprobar: `fab.py banjo_tooie limpiar` · el usuario puede borrar zJkKmdBzlpE en Studio

## Voz Hope (19-oct-2026, el usuario: «dice mal Tooie y Kazooie» → ElevenLabs, voz de mujer)
- Muestras en previews/voces_mujer*/ (eligió 05_Hope); FONETICA solo B.O.B.→Bob y Hag 1→Hag One (ElevenLabs dice el inglés nativo);
  la de Chatterbox quedó como FONETICA_CHATTERBOX. Respaldo completo de la versión Chatterbox en `voz/_chatterbox/` (cands, final,
  eval, beats/timeline/busquedas/fuentes/youtube.json, final.wav, fx.wav) y `guion_chatterbox.py.bak`; Lyria vieja en audio/_lyria_chatterbox/.
- Hope habla ~14 % más despacio: el usuario eligió velocidad natural (15:06) → 80 clips rebajados con la misma url/desde (busquedas.json
  sincronizado con fuentes.json: 015, 075, 076, 086), 051 y 089 movidos (negro al final). Lyria: 8 tramos nuevos a la medida.
- Falsas alarmas de Whisper con Hope: «Chito», «Tui/Kazui», «Greg Males», «Hellfire», «Banjo 3» → CER_MAX_POR_FRASE en guion.py.
- MASTER revisado (26 hojas, 1 cuadro/3 s): único negro = iris de pieza de puzle del propio juego en 9:12 (scene-057), aceptado.
- Costo: ~5 500 créditos de ElevenLabs (voz + muestras); saldo ≈ 17 000.

## Sesiones (plan de tramos · «continúa el video banjo_tooie» retoma aquí · protocolo docs/sesiones.md)
- alias: banjo tooie, banjo, video de banjo · vista previa: solo el MASTER al final
- leer al empezar: este ESTADO + docs/estilo_secuencia_yt.md; hojas de búsqueda en previews/scan_*.jpg (segundo exacto de cada parte)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion verificado + FONETICA + kit mg_gaming + pegatinas + voz + seleccionar + tiempo + beats | ✅ 19-oct | 86 frases, voz 750 s, 801,9 s naturales (13:22), 93 beats |
| 2 | busquedas (todas url+desde) · bajar · hojas medios · recorte_por | ✅ 19-oct | 93/93; ~40 rehechos en 4 rondas (menús, negros, SD) |
| 3 | Lyria 8 tramos · SFX 7 (210 créditos) · mezcla (-14 LUFS, 13,7 dB) · Montaje (52 tramos) · video · final · verificar (CER 1,4 %) · miniatura Flow v1 | ✅ 19-oct | 2 renders: el 1.º tenía 5 clips con negro/oscuro (créditos, fundidos) |

## Decisiones del episodio (19-oct-2026, el usuario)
- El canal VUELVE a Nintendo/retro (deja el terror CRT) con la fórmula de Warcraft/Tamriel/Runa. Voz Chatterbox Sarcastica. ~12 min.
- Ángulo: historia del desarrollo + lore + sobre todo secretos (lista de 10). Formato a anotar: `historia_y_10_secretos_secuencia_yt`.
- MG nuevos (`nucleo/mg_gaming.py`): `linea_tiempo` ×3, `swop` ×2, `jinjos`, `concurso` + `puesto`/`ficha`.
- REGLA nueva del usuario (19-oct): el Montaje del panel enseña SIEMPRE MG/pegatinas/fichas → `fx` exporta la capa (docs/panel.md).

## Fuentes de clips (todas `{"url","desde"}` en busquedas.json)
- Banjo-Tooie: serie Ninbanyan Switch Online 1080p60 (Partes 1-44; ids en el docstring de la conversación → busquedas.json).
  Escenas de video en 4:3 dentro del marco de NSO (gris + «P1») → `recorte_por` .145 (medido por código).
- Cartuchos vivos / llave / Mega-Glowbo / dragón: illustrious rocket GBbMKjMwpsw (720p). Bottles' Revenge: SonicGhost kv6zEbFBvuc.
  Evercade Nexus: GameXplain Kjn3GzEv4kA@452. Final y fotos de Mumbo de BK: Ninbanyan BK Parte 23 (-D8NxmVqjqI); menú
  Stop 'n' Swop: BK Parte 25 (6dYbihMz0AA@1166). NO sirven (< 720p): KaiLightDark, ChrisPTY507, LerakoLanche, N64 Database.

## Falta
- [ ] clips pendientes (reintento cada 5 min: `python %TEMP%\bt\reintentar.py`, o a mano `fab.py banjo_tooie bajar <ids> -j 2 --rehacer`)
- [ ] canal SIN `pantalla_final` en canales/cronicas_gaming.json: preguntar al usuario cuál usa
- [x] subido en privado y programado 19-oct 18:00 CDMX (registrado en cronicas_gaming.json y BITACORA)

## Lecciones de este video
- Sesión nacida en worktree sin el motor actual: los videos se producen en C:\FabricaAnimaciones.
- «Rare» al inicio de frase suena «Drane/Drare» (como Radagon): ponerlo tras vocal («La idea de Rare…», «los de Rare…»).
- Whisper escribe «Toye/Kasoye/Miles/Yigis»: falsas alarmas; leer eval.json y fijar tolerancias a la toma buena.
- Hojas de contacto propias (OpenCV, un cuadro cada 6-25 s) de cada parte a 360p = segundo exacto sin adivinar.
- El marco de Switch Online no es negro: medirlo por columnas que no cambian en el tiempo, no por oscuridad.
- ~110 descargas en la sesión → 429 y luego «not a bot»: reintento automático cada 5 min.
