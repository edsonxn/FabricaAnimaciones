# mpm_cocacola — «Así se FABRICA la Coca-Cola: 9,553 millones al año» (Mil por Minuto, 2.º video del canal) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: mil_por_minuto · hueco jue 26-nov-2026 15:00 CDMX (2026-11-26T21:00Z; reprogramado el 25-nov desde 18:37, nuevo horario del canal)
- estilo: SECUENCIA YT + kit `nucleo/mg_planta.py` + ESCENAS 3D `nucleo/fabrica3d.py` (arcilla + realista) → `canales/formula/mil_por_minuto.md` · modelo `videos/mpm_takis/`
- etapa: ✅ CERRADO 25-nov — MASTER 1080p 14:53 (732 MB) + .srt + miniatura Flow SUBIDOS → https://youtu.be/BYNSPBgnG_k, privado y programado jue 26-nov 15:00 CDMX (2026-11-26T21:00Z; antes 18:37); no monetizado
- siguiente: medir ≈ 3-dic contra Takis (retención, % TV, sugeridos); A/B de miniatura «FÓRMULA SECRETA» (mini_v3/v4) si el CTR sale bajo; `fab.py mpm_cocacola limpiar` cuando esté aprobado

## Sesiones
- alias: «el video de Coca-Cola», «el siguiente de Mil por Minuto», «mpm_cocacola»
- vista previa: ninguna (regla 5-nov: una sesión, directo al MASTER)
- leer al empezar: este ESTADO, `canales/formula/mil_por_minuto.md`, `videos/mpm_takis/ESTADO.md` (lecciones)
- 24-nov (1): tema, investigación (agente), metraje (agente), guion 90 frases, voz 90/90, 119 beats, clips, 3D (5 estilos → elegidos arcilla + realista), efectos (225), hojas fx 01-12 revisadas, música biblioteca (8 tramos), SFX, chequeo, miniatura Flow, youtube.json, render. Corte de la sesión durante `video --rehacer`.
- 25-nov (2): `video --rehacer 358-376 500-516 && final` (lanzado por la sesión anterior; 1 510 s) → hoja de los dos tramos mirada (contador visible, paneles ya no tapan la etiquetadora) · `verificar` CER 0,39 % (3 frases «altas» = cifras en dígitos), desfase 0 ms · regla 10 con `_sfx_regla10.py` sobre el MASTER: chasquido del gancho −6 dB del total y siseo >5 kHz +19 dB → se oye; `previews/citas_audio.mp3` · avisar · `yt subir` (miniatura + .srt) · publicados, BITÁCORA, panel (`/api/v2/obra`: ya no atrasado). Video cerrado.

## Decisiones (Claude, 24-nov-2026)
- Tema con datos (`fab.py ideas mil_por_minuto`): Coca-Cola se repite en 3 canales (×399, ×356, ×190) y es el n.º 2 de la fórmula.
- Takis a 2 días: 324 vistas, 46,6 % visto, 90 % sugeridos, 74 % TV, 0 comentarios → sin agradecimientos ni críticas.
- 3D (el usuario): «a veces pon el 3 y a veces el 1» → arcilla = general, tapadora, soplado; realista = válvulas, etiquetadora.
- Título «Así se FABRICA la Coca-Cola: 9,553 millones al año» + miniatura «9,553 MILLONES» (Flow); alternativa A/B «FÓRMULA SECRETA».

## Cómo está armado (para arreglos)
- efectos.py = `cat _cab.py _fx_coca.py > efectos.py` → EDITAR `_fx_coca.py`. Placas de procedencia por video en `_PLACAS`; sin placa bajo 3D/mapas (`_SIN_PLACA`).
- Clips: `_escribir_busquedas.py` (inicial) + `bajar N --url … --desde s` (rehechos); archivo 480p con `_archivo.py`; 001 y 011 recortados a mano en cámara lenta (originales en medios/_respaldo/).
- Mapas: `_mapa_base.py` (Natural Earth; estados de EE.UU. con admin-1) + `mapas/lugares.json` (OSM Nominatim) → `mapas/xy.json`.
- 3D: `python nucleo/fabrica3d.py --tomas <abs>/tres_d --estilo arcilla --lista general:13,tapadora:9,soplado:14` y `--estilo realista --muestras 48 --lista valvulas:16,etiquetadora:10` (realista ~8,5 s/cuadro, 1080p).
- Música: biblioteca (guion LYRIA tramos 1-8) → `python ../../nucleo/lyria_tramos.py armar`.

## Lecciones
- Sidel/Danfoss/Krones meten rótulos en inglés a mitad del clip: las hojas `medios` (2 cuadros) no los ven; la hoja fx sí. Mirar también la hoja fx buscando rótulos ajenos.
- Forbes Toluca (zyrzswdZe2g) tiene al reportero (Iván Morales, director de planta) en muchos tramos: usar solo 214-233 y 256-263 tras mirarlo.
- `bajar N --q` NO reemplaza una URL fija: usar `--url`. Un `--desde` mayor que la duración deja un archivo de 261 bytes.
- yt-dlp-ejs 0.8.0 falla el «n challenge»; los formatos HLS 1080p siguen bajando.
- Ruta relativa a Blender = se resuelve contra C:\ (dejó `C:\videos\` suelta: borrarla a mano). Siempre rutas absolutas.
- Regla 10 con un SFX (no una cita hablada): Whisper no sirve; medir `audio/fx.wav` contra la mezcla final en esa ventana (dB respecto al total + banda >5 kHz antes/durante) con `_sfx_regla10.py`. El destapar del cierre (vol .40) queda a −11 dB y casi no se distingue: como esa frase no nombra un sonido no bloquea, pero un SFX de adorno bajo la voz necesita vol ≥ .55 para notarse.
- Tiempos del 3D: el realista en plano general tardó ~15 s/cuadro con Whisper en la GPU; solo ~8,5 s en primer plano con 48 muestras.
