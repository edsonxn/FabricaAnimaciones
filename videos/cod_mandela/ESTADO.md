# Los efectos Mandela más raros de Call of Duty — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_cod = «Expediente 141» (2.º video) · meta: vie 6-nov-2026 18:00 CDMX (2026-11-07T00:00Z)
- estilo: secuencia_yt (gameplay de YouTube por beat + pegatinas + MG + mapas + sonido original + OST oficial) → doc: docs/estilo_secuencia_yt.md
- etapa: SUBIDO (3-nov): https://youtu.be/XL3MZ4Oj7Ko privado, sale vie 6-nov 18:00 CDMX (2026-11-07T00:00Z); MASTER 14:20 en salida/
- siguiente: visto bueno del usuario; medir a 7 días (% visto ≥ 35, vistas/día) contra MW4; Shorts de 2-3 puestos; `limpiar` y `biblioteca sfx catalogar` al aprobar

## Sesiones (plan de tramos · «continúa el video cod_mandela» retoma aquí · protocolo docs/sesiones.md)
- alias: «el de los efectos Mandela», «cod mandela», «el 2.º de Expediente 141»
- vista previa: solo al final (el usuario, 3-nov): avisar con el MASTER
- leer al empezar: este ESTADO.md · `videos/cod_mw4_secretos/` (plantilla: guion.py, efectos.py, armar_musica_ost.py) · `canales/formula/cronicas_cod.md`
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión (el usuario, 3-nov): investigación → guion → voz → beats/clips → MG/pegatinas → sonido → render → miniatura → subir | ✅ 3-nov (todo en una sesión: guion, voz, 100 clips, 182 MG/pegatinas/fichas, OST, 7 sonidos, render 32 min, Flow, subida) | |

## Decisiones del episodio (preguntadas al usuario, 3-nov-2026)
- tema: «Los efectos Mandela más raros de Call of Duty» (Fellow ×41,6, https://youtu.be/MUHIbSFqEyg) · misma fórmula que MW4, solo cambia el tema
- duración: ~15-17 min · puestos: 20 (cuenta regresiva) · Overgear: aún NO
- voz: Damián de ElevenLabs (`BPwS5yO6aXvwg8auqNwS`), eleven_v4_turbo, sin [whispers]/[excited]
- Comentarios: 0 en el canal (3-nov); el 1.er video salió hoy
- REGLA DE ORO: cada efecto = «lo que recuerdas» contra el clip real EN PANTALLA; ≥ 5 MG y ≥ 5 pegatinas/min; ningún tramo > 4 s con el clip solo; `fab.py cod_mandela chequeo` antes de renderizar

## Hecho
- 3-nov: proyecto creado; investigación (subagente, 32 candidatos); guion 20 puestos; voz Damián (≈ 2 190 créditos de la cuenta 2); tiempo 14:20; 100 beats; 7 sonidos nombrados cortados (−19 a −21 dB)

## Falta
- [ ] investigación · [ ] guion · [ ] voz · [ ] beats/clips · [ ] MG/pegatinas · [ ] sonido/mezcla · [ ] render · [ ] miniatura · [ ] subida

## Archivos clave
- `guion.py`, `investigacion.md`, `beats.json`, `busquedas.json`, `fuentes.json`, `medios/`, `salida/creditos.txt`

## Lecciones de este video (solo lo no obvio)
- El «bad ending» de BO2 que se cita (Menéndez vivo, -P5F8fzG42I) enseña a Menéndez matando a Woods; la tumba de Josefina es OTRA escena (1k6kaGKPkWY). Muestrear el video cada 6-10 s con `yt-dlp -g` + ffmpeg antes de fijar `desde` en escenas de otro video largo.
- `mv88YFoq2rc` (Loose Ends) no tiene ≥ 720p: el remaster `9SRL__ZJgsg` va 4,78 s por detrás; sincronizar alineando con Whisper una palabra común.
- `_bordes.py` (de tes_sentinel_teaser) fallaba con `mg_cod.fallida` (GaussianBlur con np.float64): pasarle `float(u * dur)`.
- «Y el número uno» del puesto 1 casó con la frase del gancho: anclas de puesto con 2-3 palabras más.
- Whisper alucina con metal cantado («115»): Demucs `--two-stems vocals` y Whisper sobre la voz separada da la letra con tiempos.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO (XL3MZ4Oj7Ko, 6-nov 18:00), miniatura Flow y registrado (`canales/cronicas_cod.json`, BITACORA)
- [ ] HALLAZGOS y mejoras documentados en el manual/estilo (ver CLAUDE.md «CIERRE DE VIDEO»)
