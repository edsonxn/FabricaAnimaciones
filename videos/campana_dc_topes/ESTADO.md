# campana_dc_topes — «¡A la verga los topes!» (Campaña Daniel Cervantes, sátira PS1)

Pedido del usuario (27-nov-2026): video estilo PlayStation, ~30 s, sátira tipo caricatura para adultos: Daniel maldice los topes
de Juchipila (cabrón, pinche, verga, putos…) y promete que su primera orden como presidente será tirarlos todos; movimientos
rápidos y cómicos. Proyecto, NO canal (`docs/campana_daniel_cervantes.md`): nada se publica sin OK; entrega por Rayo.
Guion y lo que se ve: `guion.md`. Es sátira: sin datos (no se inventa cuántos topes hay).

## Estado
- ✔ MASTER 27-nov-2026: `salida/topes_daniel_MASTER.mp4` (sin censura) y `salida/topes_daniel_PITIDOS_MASTER.mp4` (groserías
  con pitido de 1 kHz) — 1080×1920, 33.3 s, 30 fps, −14.2 LUFS, pico −0.8 dBFS. Mandados por Rayo. **Sin publicar.**
- Whisper sobre la mezcla FINAL: texto completo correcto; en la de pitidos no se oye ninguna grosería.
- Hojas: `previews/hoja_master.jpg` (1 cuadro/s), `previews/inicio.jpg` (0–4.5 s).

## Piezas
| Archivo | Qué hace |
|---|---|
| `voz.py` | 8 frases con la voz CLONADA (cuenta 4, eleven_v4_turbo, sin corchetes; estabilidad .45 para el enojo), `/with-timestamps` → tiempo de cada palabra; atempo ×1.1 (ritmo de caricatura, cabe en 30 s) |
| `plan.py` | tiempos compartidos (de `voz/tiempos.json`): cada «tope» de la voz = un golpe del carro verde; mofle, suspensión, patada, pisotón |
| `tex_topes.py` | texturas 64 px a 15 bits: empedrado, tope amarillo/negro, banqueta, 5 fachadas, letrero TORTILLERÍA, cantera rosa, cara y piel ROJAS de coraje |
| `topes3d.py` | Blender 4.2 EEVEE 270×480 a 15 cps: el Daniel de `campana_dc_lowpoly` v3 (malla continua, 9 gestos de Flow) con 20 poses de rebote (18 % de sobretiro); calle con 9 topes, parroquia y cerros; vocho rojo (voltereta), verde (rebota, mofle, llanta, se hunde, sale volando), blanco (pasa liso); vapor, polvo, onda del pisotón; cámara con cortes y sacudida en cada golpe; temblor PS1 |
| `post.py` | rótulos sin suavizado, HUD «SUSPENSIÓN» + «TOPES: n» + K.O., escala ×4 vecino más cercano, chiptune sintetizado + música `robotaller_4apps__lyria_tramo2` (desde 20 s) agachada; dos mezclas |

Rehacer: `python voz.py` → `python tex_topes.py` → `"C:/Program Files/Blender Foundation/Blender 4.2/blender.exe" -b --factory-startup --python topes3d.py -- --salida render` → `python post.py` (`--solo-audio` rehace solo la mezcla). Render completo ≈ 6 min.

## Lecciones
- `with-timestamps` de ElevenLabs da el tiempo por carácter: sincronizar golpes con palabras sin Whisper. Descontar el recorte
  (`librosa.effects.trim` devuelve el índice) y dividir entre el atempo.
- Un carro que arranca detrás de la cámara sale como un bloque gigante en el cuadro 0: arrancarlo ya delante (y ≥ −1.5 con la
  cámara en −4.7).
- `PYTHONIOENCODING=utf-8` para correr `post.py` desde bash (consola cp1252).

## Sesiones
- 27-nov-2026: guion, voz, escena, render, post, dos MASTER, Rayo. Para seguir: «continúa el video campana_dc_topes».
