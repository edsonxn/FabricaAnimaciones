# Guía para escribir las escenas de «Las 1.200» (noir color) en varias conversaciones

Léela entera (es corta) junto con `ESTADO.md`. NO leas los kits completos: usa grep (`grep -n "^def \|^class " archivo`).
Ejemplo completo de escena terminada y revisada: **`esc_tareas.py`** (7 tomas). También `esc_gancho.py` y `esc_encierro.py`.

## Qué se pidió (el usuario, 12-oct-2026)
La voz y la música están bien y NO se tocan. Las escenas viejas (Gemini: fondos quietos con rótulos) eran lentas y aburridas →
se rehacen TODAS en **noir a color**, con propuestas nuevas y mucho dinamismo.

## Reglas de ritmo y calidad (las que hacen que no aburra)
- **Una toma nueva cada 3-5 s**, anclada a palabras del guion: `self.w("palabra")` (inicio) y `self.plano(t, fn, tr=..., dur=..., pal=...)`.
- **Nada quieto**: cámara siempre en deriva/zoom/paneo (`Pista` o `k = smooth(clamp01(u / dur))`), personajes que respiran,
  luces que parpadean, lluvia/humo/motas/niebla, sacudidas (`C.temblor`) en los golpes.
- **La acción narrada la hacen los personajes** (la copia tira de la puerta, el ingeniero suelda, el sello cae en la palabra).
- **Cada escena con sus propios lugares** (no repetir fondo entre escenas; dentro de la misma escena sí, con otra cámara/luz).
- Rótulos de énfasis cortos: `C.banda(h, "TEXTO", x, y, px, t, t0, claro=False|True, acento=False|True)`; lugar/fecha: `C.cinta(...)`.
  Sin subtítulos. Texto sobre papel/pantalla: paralelo y dentro (`N.soporte` / `C.cartel`).
- Transiciones entre tomas variadas: `barrido` (dirx=±1), `empuje` (centro=), `tinta`, `relampago`, `humo`, `fundido`.
- **Revisa con la vista** cada escena: `python videos/sociedad_1200/_lote.py <escena> --procs 4` → `previews/lote_0.jpg`
  (un cuadro por toma) y `_prueba.py <escena> u1 u2 --solo-hoja` para tiempos locales. Lo oscuro es el defecto más común:
  ambiente 0.35-0.55 y luces propias (la pantalla de cada copia ilumina con `luz_radial(..., h.pal["verde"])`).

## Color por acto (paleta POR TOMA con `pal=`)
- `medianoche`: el laboratorio de las copias (actos I y III-sandbagging, V-METR). Acento: verde de las pantallas, rojo piloto.
- `sodio`: el despacho y la calle del detective, San Francisco 2023 (TaskRabbit), Oxford, el bar.  Acento: neón rojo.
- `bourbon`: Facebook 2017 (Bob y Alice), mesas/papeles cálidos.  Colores con nombre: `h.pal["sodio"|"luna"|"neon"|"lampara"|"verde"|"sello"|"tinta"|"papel"]`.

## Kit del video (todo en esta carpeta)
- `basen.py`: `BaseNoir` (heredar; `armar()`, `sonidos()`, `PAL`, `TR_SALIDA`).
- `comun.py` (C): rect, rot, T_obj, ambiente(h, k), banda, cinta, cartel, reflejar (suelo mojado), parpadeo, brasa, temblor, chispas,
  polvo_cae, clip_color (video real teñido), clip_en (video dentro de una pantalla), rejilla_luces (miles de luces baratas).
- `reparto.py` (RP): `Copia(sem, num, grande=False)` → `.perfil(h, dict(x, y, s, d, andar, paso=RP.fase_paso(dist, s), sentado,
  brazos="bracea|teclea|carga|alza", mano=(lx, ly), mano2, mano_bob, cara=dict(expr, mira, mira_y, texto=[..], t0, cps, apagado),
  gabardina, gafas, baston, brazal, inclina))`, `.frente(h, dict(x, y, s, manos=[(lx,ly),(lx,ly)], cara, brazal))`,
  `.cabeza(h, cx, cy, s, cara, d)`, `RP.espalda(h, x, y, s, t, sentado, timer="00:12:30")`, `RP.copia_mini(...)`, `RP.cabeza_mini(...)`.
  Expresiones: neutro feliz triste astuto miedo sorpresa linea error carga pregunta off texto alarma; `apagado` 0..1 = apagón de tubo.
  Mano a un punto del mundo: `local(x, y, s, d, wx, wy)` (copiar de esc_tareas.py).
- Personajes humanos: `noir_pers.Detective / Busto / Figura / Frontal` y `kit27.caminante` (camina sin patinar), `kit27.persona`.
- `props_s.py` (P): ver la cabecera del archivo (candado, llavero, ganzúa, regalo, carpeta_tab, sobre, caja, reloj, periodico,
  palanca, enchufe, capsula, tubo_neumatico, punto_en, contador, mazo, portatil, chat, captcha, tarjeta, hilo, chincheta, mano,
  vaso, servilleta, boton_off, ficha_juego, pieza_ajedrez, busto_ciceron, juez, robot_mesa, cinta_policial, silueta_tiza,
  lampara_mesa, telefono, cadena, papeles). `kit27` (K): calendario, carpeta, hoja, balanza, reloj_arena, medidor, barra, puerta,
  interruptor, pantalla_codigo, multitud, mano_alzada. `noir_feudal` (NF): llama, vela, lacre. `noir_real` (R): retrato_noir.
- Lugares: `mundos_base.py` (piezas: muro, suelo, ventana, puerta, reja, barandilla, tuberias, estanteria, archivador, servidor,
  cartel, lampara, cielo, ciudad, agua, colinas + `superficie(tipo, sem)` para planos cerrados). Cada bloque escribe SU archivo
  `mundos_<n>.py` con funciones `@mundo` (caché común; no usar lru_cache). Ver lugares: `_ver_mundos.py mundos_<n>`.
  Pegar con color: `NC.pegar(M.lugar(), h, prof, rampa="ladrillo|piedra|madera|papel|lejos|cielo|asfalto|vino|tela_verde",
  emis=1.0, col_emis=h.pal["verde"], bruma=0.2)`.
- Sonido: en `sonidos()` con `self.ev(t, "nombre", vol, pan, dur=...)`; nombres = funciones `s_*` de `nucleo/sfx_noir.py`
  (grep). No repetir el mismo efecto por cada pieza que aparece.

## Medios reales (regla LogIA)
Fotos en `imagenes/`: sam_altman (ya usada en encierro), clement_delangue (usar en redada: «Hugging Face denunció el ataque»),
yann_lecun (caso_2017: «laboratorios de Facebook», leyenda «IA DE FACEBOOK · 2017»), nick_bostrom (filosofia_peligro: «Nick
Bostrom»). `R.retrato_noir(h, "nombre", x, y, ancho, t, t0, rotulo="...", leyenda="...")` dentro de `with h.capa(0.0):`.
Clips Pexels en `clips/` (servidores_1/5, cables_2, codigo_3, gotas_vidrio_0/5, humo_3/4, maquina_0/4): `C.clip_color` o `C.clip_en`.
No poner a Zuckerberg ni a Altman como autores de decisiones que el guion no les atribuye.

## Reparto del trabajo
Los tramos y su estado están en la sección «## Sesiones» de `ESTADO.md` (la lee `python fab.py continuar las 1200`).
Cada tramo escribe SU archivo de lugares (`mundos_<n>.py`); al terminar: `python _reg.py`, revisar lotes y cerrar el tramo en
`ESTADO.md` (protocolo `docs/sesiones.md`).

Las propuestas de tomas de cada escena están en `PLAN_TOMAS.md` (seguirlas, mejorarlas si hace falta).
