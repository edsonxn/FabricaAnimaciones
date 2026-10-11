# Los jardines y el parque de Juchipila (reel) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: ninguno (reel de la página de Facebook «Que pasa en Juchipila», E:\PaginaFace) · publicar desde allá, no a YouTube
- estilo: secuencia con efectos, VERTICAL 9:16, imágenes de Flow (ilustración) → docs/estilo_secuencia_fx.md + estilo_secuencia_flow.md § Formato vertical
- etapa: voz en curso (8-oct-2026 16:30: `python fab.py jch_parque voz`, 4 semillas por frase)
- siguiente: `seleccionar` → `tiempo` → `beats` → escribir prompts.json (un prompt por beat) → `prompts` → Flow (pedir a Edson su Chrome con flowscrap en un proyecto NUEVO de Flow)

## Decisiones (Edson, 8-oct-2026)
- tema: historia del parque de Juchipila → eligió «el centro completo en una línea de tiempo» (Jardín Madero/Plazuela Segovia → Jardín Juárez 1943 → Parque Municipal, primera piedra 18-may-1949)
- registro informativo/histórico · duración 1 min (~172 palabras, Dan ≈ 3,3 palabras/s) · voz Chatterbox Dan · música Lyria · SOLO imágenes de Flow (video_s=0, img_s=3.0)
- efectos como «Un segundo»: cámara dirigida, golpes, rótulos de énfasis (años) y SFX de ElevenLabs (~20 s en total, ~800 créditos)

## Hecho
- Investigación y fuentes: están en el docstring de guion.py (Plan Municipal de Desarrollo 2021-2024 + documento de patrimonio de Zacatecas). Dato corregido: una nota de Imagen Zacatecas (2018) dice «1929»; vale 1949 (Alemán presidente 1946-52).
- guion.py (texto final, FICHA, LYRIA) escrito.

## Falta
- [ ] voz → seleccionar → tiempo → beats → prompts.json → Flow → medios (mirar hojas) → efectos.py → fx --seco/fx/fx hoja → video → Lyria (`python ..\..\nucleo\lyria_tramos.py` desde la carpeta del video) → mezcla → final → verificar
- [ ] Copiar el MASTER a `E:\PaginaFace\posts\...` (`pagina.py nuevo <slug> --tipo reel --categoria historia`), texto.txt, fuentes, créditos («ilustraciones generadas con IA»)
- [ ] Edson aprueba ANTES de `aprobar`/`programar`. Primer reel: programarlo solo y verificarlo en Business Suite.

## Lecciones de este video (solo lo no obvio)
- «El parque» en Juchipila es ambiguo: Parque Municipal (2.7 ha, 1949) vs Jardín Juárez (plaza del kiosco, 1943) vs Jardín Madero (antes panteón). Se cubrieron los tres.
- No se afirma: fecha de inauguración del parque, autor del kiosco, qué había antes de 1943, año del templo (la fecha 1627 no se pudo confirmar).
