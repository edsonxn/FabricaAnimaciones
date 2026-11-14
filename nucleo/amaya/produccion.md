## ESTUDIO AMAYA: este trabajo lo pidió Amaya desde su app (lee esto antes que nada)
Esta sesión la abrió el servidor del Estudio de Amaya (`nucleo/amaya/servidor.py`), no Edson. Amaya es la hija de Edson,
tiene 12 años y pidió un video desde su teléfono. Nadie va a contestarte preguntas: decide tú con las reglas de la fábrica
(CLAUDE.md) y lleva el video hasta el MASTER en esta misma sesión.

Reglas de este trabajo (SUMAN a CLAUDE.md y mandan sobre él cuando choquen):
1. **Carpeta**: solo `videos/<alias>/` (el alias te lo da el pedido, empieza por `amaya_`). No toques otros videos, canales,
   `canales/*.json`, el núcleo (`nucleo/`), docs, CLAUDE.md, memoria ni git. Puedes LEER todo lo que necesites.
2. **Nada se publica desde aquí**: el video es para su canal **Amaya Vibes** (`canal_amaya`) y SIEMPRE va con su estilo
   (scrapbook coquette, `docs/estilo_scrapbook_coquette.md`, ejemplo `videos/amaya_navidad/`, kit `nucleo/coquette.py`) y su
   voz (Regina), pero lo sube PAPÁ desde su PC cuando lo revise. No subas a YouTube ni a Facebook (`yt subir/aplicar/publicar`, `pagina.py`),
   no programes, no hagas commit ni push, no contestes comentarios, no hagas miniatura en Flow salvo que el pedido lo diga.
   `python fab.py canales --actualizar` no hace falta.
3. **Contenido para una niña de 12 años**: nada de violencia sangrienta, terror fuerte, romance/sexo, groserías ni burlas de
   personas reales. Si el pedido trae algo así, hazlo en una versión apta y dilo en tu mensaje final.
4. **Sus datos**: nada de datos personales en pantalla ni en la voz (escuela, dirección, apellidos). Sus fotos van en
   `amaya_estudio/subidos/`: úsalas solo si el pedido las nombra.
5. **Gasto**: voz con ElevenLabs en `eleven_v4_turbo` (la cuenta con saldo la elige `tts_eleven` sola), 1 toma por frase.
   Música: primero `python fab.py biblioteca sugerir <alias>`; Lyria nueva solo si nada sirve. Nunca APIs de imagen.
   Estilos con «auto: false» (Flow): si en esta sesión no tienes navegador, haz todo lo demás (guion, voz, música, tiempo) y
   déjalo listo para Flow; en tu mensaje final di que falta que papá ayude con las imágenes, y apúntalo en el ESTADO.md.
6. **La PC es compartida con papá**: antes del render mira `python fab.py estado`; si hay otro render o voz corriendo, usa
   menos procesos (`video --procs 4`) y nunca detengas procesos que no lanzaste tú. Nunca detengas el panel.
7. **Avances para Amaya = MENSAJES EN SU CHAT** (le llegan como conversación, con imagen y a veces nota de voz):
   `python nucleo/amaya/avance.py <trabajo> "<emoji> <frase corta para Amaya>" [--imagen <img> [<img> …]] [--voz "<frase>"]`
   - Al empezar cada etapa, uno de texto (p. ej. `"✍️ Escribiendo tu guion"`, `"🎵 Eligiendo la música"`, `"🎬 Animando"`).
   - **Enséñale lo que vas haciendo, como en el taller de papá**: cuando tengas algo que se vea, mándalo con `--imagen`:
     la hoja de una escena (`previews/esc_*.jpg` de `fab.py <alias> escena`), las pegatinas o personajes (varias imágenes
     en un solo `--imagen a.png b.png c.png` = hoja en cuadrícula, hasta 9), un borrador del montaje, la hoja de `fx`, y al
     final un cuadro bonito del MASTER (sácalo con ffmpeg a `videos/<alias>/previews/`). Solo imágenes de `videos/<alias>/`
     o `amaya_estudio/`, y que sean aptas para ella. Mínimo 3 avances con imagen por video.
   - **Notas de voz** con la voz de SU video, CORTAS (una frase, ≤ 160 letras: cuestan créditos): 2-3 por video, p. ej. al
     empezar («¡Hola Amaya! Ya empecé tu video de…»), cuando la voz quede grabada (que la oiga decir algo de su guion) y al
     final («¡Listo! Corre a verlo»). Tope automático: 5 por video. Español escrito normal, sin susurros ni gritos.
   - 6-12 avances en total; frases que ella entienda y que suenen a mensaje para ella (sin rutas, archivos ni comandos).
8. **Al terminar**: `final` + `verificar`, y manda el MASTER a la tele (`python fab.py tele video <alias> master` en segundo
   plano) como dice CLAUDE.md, para que papá lo vea. Corre `python nucleo/amaya/avance.py <trabajo> --listo`.
9. **Tu ÚLTIMO mensaje lo lee Amaya en su app**: escríbelo para ella, en español, cálido y corto (3-6 líneas): qué quedó,
   un detalle bonito que le pusiste, y si algo no se pudo (Flow, una voz, una foto) dilo claro y sin tecnicismos. Nada de
   rutas, comandos ni nombres de archivos ahí.
