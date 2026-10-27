# Zelda Ocarina of Time REMAKE: los 15 CAMBIOS frente al ORIGINAL de N64 — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_gaming · hueco lun 2-nov-2026 18:00 CDMX · gancho = el remake sale el 5-nov-2026
- estilo: secuencia_yt + fichas TRANSLÚCIDAS con la interfaz de N64 + comparativas N64/Switch 2 · voz ElevenLabs Hope (`eleven_v4_turbo`) · música = OST oficial de Ocarina → doc: docs/estilo_secuencia_yt.md § Crónicas del gaming
- etapa: SUBIDO en privado (https://youtu.be/1wDyy-FJrBg), programado lun 2-nov-2026 18:00 CDMX · MASTER 12:06 · miniatura ✅
- siguiente: visto bueno del usuario; al aprobar: `fab.py oot_remake_cambios limpiar`, `biblioteca sfx catalogar`, hallazgos al doc de estilo

## Sesiones (plan de tramos · «continúa el video oot_remake» retoma aquí · protocolo docs/sesiones.md)
- alias: oot remake, remake de ocarina, cambios del remake, oot_remake_cambios
- vista previa: ninguna; directo al MASTER y aviso (el usuario, 26-oct)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión (el usuario, 26-oct) | ✅ 27-oct | guion 93 frases · voz turbo · clips · OST · FX · miniatura · render 693 s · subido 1wDyy-FJrBg (2-nov 18:00) |

## Decisiones del episodio (26-oct-2026, el usuario)
- Tema elegido entre 3 con datos (OoT remake / auge y caída de Rare / Mario 64): OoT remake, variable = SOLO el ángulo.
- Una sesión; sin vista previa: MASTER y aviso.
- Voz: ElevenLabs con 2 683 créditos → muestras Chatterbox (Hope clonada, Sarcastica) y `eleven_v4_turbo`; el usuario: «suena
  perfecto… el default debe ser turbo» → turbo por defecto en todo el núcleo (`tts_eleven.modelo()`); recargó 50 000 créditos.

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- 26-oct ~20:30: guion escrito (93 frases, 9 853 caracteres ≈ 1 970 créditos). Lanzando la voz.
- Hojas de contacto del remake (escanear.py: DEMO, OVR, DIR, JUN, NLIFE) → previews/_scan/. N64 = serie ZeldaCentral
  catalogada en videos/zelda_oot/mapa_clips.md (marco NSO 0,131).

- 27-oct (conciliado): la sesión del 26-oct se cortó tras la mezcla (20:58) sin anotar. En disco: voz 93/93, beats, 87 clips en
  medios/, pegatinas/, OST + ambiente + fx.wav, efectos.py (hojas fx_01-05), audio/final.wav, youtube.json. Sin render (salida/ y
  segmentos/ vacíos). Miniatura: ingredientes 1-5 en miniatura_ing/ y prompt en prompt_miniatura.md; NO generada (Chrome colgado
  con la CPU al 100 % por los renders de Warcraft y LoL). El usuario: «haz miniatura solamente, más tarde lo continuamos».
- 27-oct (tarde): el usuario: «render, final, verificar y súbelo programado al 2-nov 18:00». py_compile ok, hojas fx ok →
  `fab.py oot_remake_cambios video` lanzado. Si se corta: mirar segmentos/ y relanzar (retoma lo hecho).

## Hecho
- muestras de voz en muestras/ (Chatterbox ×2, turbo con y sin corchetes)
- voz · seleccionar · tiempo · beats · busquedas · bajar · medios · pegatinas · OST · ambiente · fx · mezcla · youtube.json

## Falta
- [x] miniatura Flow (27-oct, 15:30, con la PC libre): variante B (`miniatura_ing/mini_b.jpg` → `salida/miniatura.jpg` 1280x720);
  la A repintó el logo en rojo y redibujó al Link del remake. Proyecto Flow «oct 27 - 15:28» (flow.google.com).
- [x] video · final · verificar (27-oct: CER 0,32 %; 3 frases > 2 % solo por nombres —Aonuma, Skulltula, Kakariko—; desfase 0 ms;
  el negro de ~0,5 s en 199 s es el fundido del propio juego al entrar a la Ciudadela = el cambio n.º 13, no un error)
- [x] subir y programar 2-nov 18:00 (1wDyy-FJrBg, miniatura aplicada) · Facebook NO (canal gaming) · registrado en canales/BITACORA
- [ ] visto bueno del usuario · limpiar · catalogar SFX · hallazgos a docs/estilo_secuencia_yt.md
