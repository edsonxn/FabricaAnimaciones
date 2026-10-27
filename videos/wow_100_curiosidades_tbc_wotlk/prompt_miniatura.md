# Miniatura de «100 curiosidades de Burning Crusade y Wrath» (Flow, Nano Banana 2.1 · 16:9 · x2; 27-oct-2026) — 2/2 bien, elegida v1

Regla del canal: Flow COMBINANDO imagen REAL del juego (memoria «miniaturas Warcraft = ingredientes reales»), UN protagonista,
texto pintado por Nano Banana a la izquierda (receta de `wow_curiosidades_reinos_este/prompt_miniatura.md`, v3/v4).

**Ingrediente:** la miniatura OFICIAL del tráiler cinemático de Wrath (`https://i.ytimg.com/vi/BCr7y4SLhck/maxresdefault.jpg`,
copia en `miniatura_ing/2_yt_trailer_wotlk.jpg`): el Rey Exánime con Agonía de Escarcha a la derecha y cielo oscuro a la izquierda.
**Cómo llegó a Flow:** el navegador integrado BLOQUEA `http://127.0.0.1` (ERR_BLOCKED_BY_CLIENT; el servidor local de
ingredientes no sirve), pero `i.ytimg.com` tiene CORS abierto: `fetch` → `File` → `ClipboardEvent('paste')` sintético en
`.ProseMirror`. Cualquier miniatura de YouTube del juego sirve así de ingrediente sin subir nada nuestro a internet.

## Prompt
YouTube thumbnail, 16:9, SIMPLE and CLEAN with very little visual clutter, one single subject. Use the reference image, the real World of Warcraft Wrath of the Lich King cinematic frame of the Lich King holding the runeblade Frostmourne in a snowstorm, keeping the original Blizzard cinematic look without redrawing his face, helmet or armor. Place the Lich King big in the right half of the frame, sharp, his glowing icy blue eyes and the frost-covered sword blade the brightest elements, a few drifting snowflakes and cold blue rim light. The left half is a calm dark night sky with soft falling snow, slightly blurred, so the text reads clearly. Big bold title text on the left third: "100" huge in white with a thick black outline, and right under it the word "CURIOSIDADES" in bright yellow #FFE21E with a thick black outline, chunky fantasy game font, perfectly spelled, no other words. Strong contrast, slight vignette, keep the bottom-left corner fairly dark and empty. No interface, no watermark, no border, no extra text, no logos.

Resultado: `salida/miniatura_flow/mini_lich_v1.png` (elegida, texto más grande) y `_v2.png` → `salida/miniatura.jpg` (1280x720).
