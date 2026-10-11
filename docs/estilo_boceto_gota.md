# Estilo boceto y animaciones en bucle

_Extraído de CLAUDE.md (1-oct-2026). Se lee solo cuando el video lo necesita._

## Estilo boceto y animaciones en bucle (ejemplo: `videos/gota_bucle/`, ~1 min, vertical)
- `ESTILO_VISUAL = "boceto"` + `FORMATO = "vertical"`. Motor propio `nucleo/boceto.py` (NO usa el Lienzo): papel crema,
  tinta que tiembla en 3 fases a 12 cuadros/s (`fase(t)`), crayón en zigzag desfasado, letra manuscrita (Ink Free).
  Cada objeto es un `Dib([T(pts, ancho), R(pts, color), ...])` en coordenadas locales; `dib.dibujar(hoja, x, y, s, rot,
  flip, u=..., fase_=...)`: `u` 0→1 lo DIBUJA trazo a trazo (la pluma avanza y el crayón rellena); `u` 1→0 lo BORRA en
  orden inverso. Otras salidas: `caer` y `encoger` (ver `Mundo.act` en `videos/gota_bucle/escenas.py`).
- Una sola clase `Mundo` dibuja todo en función del tiempo global (como el plano secuencia); una mascota (la gota) viaja
  por "pases" `pase(t0, t1, p0, p1, s0, s1, h)` entre escenas. Subtítulos manuscritos propios (`subs_propios` en el estilo:
  render.py no dibuja los suyos).
- **Bucle:** el estado inicial (C0) se dibuja completo en t=0 y el cierre vuelve a dibujarlo; en el último cuadro
  (`t >= TOTAL - 1.5/30`) el temblor y el parpadeo vuelven a fase 0 → último cuadro = primero (verificado con diff = 0).
  La última frase debe enlazar con la primera. Sin subtítulo ni barra en t=0 ni al final.
- **Ritmo (aprendido de la referencia, 29-sep):** un cambio visual cada ~1,5 s (≥ 1 por frase y varios por frase larga, anclados
  a palabras con `T(id, palabra)`), objetos que entran como boceto de lápiz que la tinta cierra (`lt`), `pop` con rebote,
  `sube`/`izq`/`cae`; salen por `encoger`, `borrar`, `caer`, `baja`. Física: caídas con rebote y aplastamiento (`sq`), lluvia,
  gotas, salpicaduras. **Nada se queda quieto:** todo `Dib` se dibuja con `tv=te` (ondulación + respiración de `boceto.vivir`,
  ciclos enteros en la duración total → el bucle cierra); nube y sol son dinámicos (`O.nube_din`, `O.sol_din`); agua en movimiento.
- **Transformaciones objeto→objeto** (`boceto.morfosis`, en escenas con `M(actor_a, actor_b, t0, dur)`; ~0,5 s), copiadas cuadro a cuadro de
  la referencia (reloj→taza): 1) el crayón del viejo se disuelve en manchas en 1-2 cuadros (`relleno(disolver=)`), 2) sus trazos sobrantes
  se borran, 3) su contorno se deforma en el del nuevo con temblor extra y garabatos de lápiz gris, 4) se dibujan los trazos que solo tiene
  el nuevo (asa…), 5) el crayón nuevo sube en manchas de abajo hacia arriba (`inv=True`). El PRIMER `T` de cada `Dib` debe ser su contorno
  principal (se empareja con el primero del otro). En gota_bucle: planeta→nube, montaña→hielo, hielo→charco, río→grifo, vaso→aliento, sol↔luna.
- **Sonido:** cada actor lleva `sfx=[(nombre, dt, vol, {kw})]` y `Mundo.sonidos` cubre la gota. Sonidos nuevos en `nucleo/sfx.py`:
  plop, gota, papel, lluvia, garabato, glug, chorro, borrar, crece, siseo, ronca. Con ~130 efectos, `MEZCLA sfx≈-24`.
- Prueba rápida sin render: `_prueba.py t1 t2 ...` (hoja de contacto) y `_bucle.py` (compara primer y último cuadro).
  Un cuadro cuesta ~0,45 s (1080x1920); usa varios procesos como siempre.
