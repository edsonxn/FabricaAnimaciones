# Estilo ACUARELA PINTADA A MANO POR CÓDIGO (4-nov-2026)

Nació en `videos/ballena_estomago/` (Short de Kuriox «¿Qué pasaría si una ballena te tragara?», 75 s, vertical, 24 fps). Pedido
del usuario: animación procedural, cada cuadro dibujado por código, con el estilo y la forma de animar de un corto de
@mablesjoseph en X (25-sep-2026), y SFX hechos por Claude (síntesis propia, sin ElevenLabs ni bibliotecas).

## Qué lo hace reconocible
- **Papel** con grano y viñeta cálida (`terminar(im, t)` al final de cada cuadro).
- **Lavados** de acuarela que multiplican como pigmento, con moteado y **borde húmedo** más oscuro (`lavado`, `forma(..., humedo=)`).
- **Tinta a pincel** de grosor variable y puntas afiladas que **hierve a 12 fps** (re-dibujada en dos a 24 fps: `boil(t)`).
- **Chibi**: cabezones, ojos con caras por nombre (`normal`, `susto`, `apretados`, `mareo`, `feliz`, `triste`…).
- **Iconos de emoción** del lenguaje de la referencia: `!`, `?`, nubecita con lluvia, destellos, corazones, gotas de sudor, mareo.
- **Transición = la acuarela se desborda** (`comun.desborde(A, B, u, cx, cy, borde)`): B entra como una gota que se expande con
  borde húmedo; nada de cortes secos (plano secuencia).
- **Rótulos pintados** (LuckiestGuy + contorno de tinta) solo para énfasis: «¡ATORADO!», «37°C», «×100», «¡BLAAAGH!».
- **Lugares oscuros**: `oscuridad(im, nivel, luces, conos)` con la linterna del personaje (cono que barre) y la mascota como
  lámpara. Regla aprendida: el HUD (termómetro, manómetro, rótulos, lupas) se pinta DESPUÉS de la oscuridad y se vuelve a pintar
  a la mascota encima para que brille; nivel ≤ 0,85 o el cuadro queda negro.

## Archivos (copiar de `videos/ballena_estomago/`)
| Archivo | Qué es |
|---|---|
| `acuarela.py` | el kit: `forma`, `lavado`, `linea`, `cinta`, `curva`, `elipse`, `rrect`, `brillo`, `oscuridad`, `rayos`, `rotulo`, `terminar`, easings |
| `personajes.py` | buzo chibi (poses por parámetros, `apretado`, `guante_roto`, otro traje), Kuri, cachalote, calamar, pez, alga, iconos |
| `utileria.py` | jorobada con boca que se abre (+ `dentro`), pico de calamar, manómetro, termómetro, flecha pintada, bombilla, calavera, O₂, vapor |
| `comun.py` | anclas a la voz `ww(esc, frase, palabra)`, `fondo_agua` cacheado, `corte`, `desborde` |
| `plano_*.py` | un plano por tramo con `T_INI` y `cuadro(t)`; `escenas.py` despacha por tiempo (un solo `Mundo`) |
| `_hoja.py` | `python _hoja.py nombre t1 t2 …` → `previews/hoja_<nombre>.jpg` (3 columnas): MÍRALA tras cada plano |
| `sfx_proc.py` + `sonidos_resto.py` | SFX 100 % sintetizados (numpy/scipy) anclados a las mismas palabras → `audio/fx.wav` |

## Flujo
1. Guion + voz (ElevenLabs de Kuriox) + `tiempo` → `timeline.json` con palabras.
2. Planos con anclas `ww()`; cada uno revisado en hoja (`_hoja.py`) a 3-4 tiempos por frase. ~0,5-1,5 s/cuadro a 1080x1920.
3. SFX: cada sonido es una función (osciladores, ruido filtrado, envolventes): burbuja Minnaert, campanita, boing, bip de Kuri,
   canto de ballena, trago, latido, whoosh, rotulador, chirrido de goma, clics de cachalote, sorbido, «wah-wah», tripas, crujido,
   chisporroteo de ácido, ping de sonar, tic de manómetro, alarma, siseo, acorde de veneno, «ding» de idea, arcada, clac, olas,
   gaviota. `python sfx_proc.py` (avisa del pico) → `fab.py <v> mezcla` (fx a −9 dB).
4. Render con pocos procesos (render.py los limita por RAM; aquí 2): ~2,5 min por segmento de 3,75 s.
5. Miniatura Flow 9:16 con UN CUADRO DEL PROPIO VIDEO como ingrediente (WebP 360x640 pegado): copia el estilo y los personajes
   a la primera (`videos/ballena_estomago/prompt_miniatura.md`).

## Errores a no repetir (de este video)
- Un objeto que entra en la boca de un animal grande se dibuja DELANTE del animal hasta que entra (si no, queda tapado).
- Iconos (nube, `!`) a ≥ 120 px del borde superior: se salen del cuadro.
- Personajes ≥ 1,3 de escala en planos verticales: con 1,0 el cuadro se ve vacío.
- Un detalle diminuto (un dedo) se enseña con una LUPA (círculo de papel con el detalle grande), no a escala real.

## Lecciones del 2.º video (`videos/arenas_movedizas/`, 4-nov-2026, 73 s)
- Los módulos propios del video llevan sufijo (`fondos_arena.py`, `personajes_arena.py`): `fondos.py` choca con `nucleo/fondos.py`
  (el núcleo va primero en `sys.path`) y se importa el equivocado sin error.
- Charco/pozo en perspectiva: el labio delantero es media elipse que TAPA lo hundido; ≥ 210 px de alto bajo la superficie o asoman las botas.
- Agua que sube alrededor de alguien: una capa DETRÁS (toda la playa) y otra DELANTE solo hasta el pecho; una sola capa encima le tapa la cara.
- Una película dentro del video (galán sepia que se hunde) se pinta en una copia y se recorta al fotograma, o el cuerpo se sale del marco.
- Corte a vista lateral bajo tierra (granos, flechas de empuje, línea «CINTURA») explica la física mejor que la vista de la playa.
- Render: 20 segmentos en ~6 min con 3-4 procesos (~0,5 s/cuadro; mucho más rápido que la ballena).
- Miniatura: un cuadro del video como WebP 180x320 (6 KB) cabe en UN `javascript_tool` en base64; el canvas lo sube a 720x1280.
  Salió 2/2 bien con título de 2 líneas y tildes deletreadas; se elige la de título más grande (se lee a tamaño de celular).
  En el navegador integrado `computer type` SÍ escribe en el `.ProseMirror` aunque la captura tarde en mostrarlo: no repetir con
  `execCommand('insertText')` sin mirar antes `innerText.length` (se duplica el prompt).
- Dos Shorts del mismo canal: `yt subir` exige 48 h entre ellos (12 h solo frente a un largo).
