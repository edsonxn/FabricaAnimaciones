# Plan de efectos.py con el kit nuevo `nucleo/mg_lol.py` (para retomar en otra cuenta, 27-oct-2026)

## Por qué (el usuario, 27-oct, al ver la vista previa 0-5:26)
- «esas tarjetas se ven muy básicas, poco impresionantes» (las píldoras `mg_tactica.chip` / `lista`).
- «los primeros 30-45 segundos deben tener más motion graphics, más vistoso, que enganche desde el inicio».
- «usa pegatinas, imágenes, animaciones en general».
- «aprende cómo se editan los videos de Warcraft, Tamriel, Runa Caída para que los hagas mucho más dinámicos».
  Método de esos canales (videos/wow_100_curiosidades_tbc_wotlk/efectos.py, docs/estilo_secuencia_yt.md § PEGATINAS y
  § MOTION GRAPHICS NUEVOS): pegatina real casi en cada frase (chicas abajo-izq. x .17 y .62 tam ~420; ~1 de 5 GRANDE a
  media pantalla x .25/.75 y .50 tam 560-620), MG propios del guion que entran por partes con `marcas` = palabras de la voz,
  tarjetas a la derecha (x .72), nada quieto > 2 s. Anclas por TEXTO: `de=("frase exacta", offset)`, `marcas=["palabra", ...]`.

## Ya hecho (en disco)
- `nucleo/mg_lol.py` (kit nuevo, compila, probado en `previews/mg_lol_hoja.jpg`): `tarjeta`, `pegatina`, `resultados`,
  `caida` (con `vive` y `sello`), `eliminado`, `apertura`, `versus`, `menu`, `suiza`. Prueba: scratchpad `prueba_mg_lol.py`
  (copiar a `videos/lol_worlds_2026/_prueba_mg_lol.py` si hace falta repetirla).
- Recursos: `iconos/equipos/<COD>.png` (19 logos oficiales, static.lolesports.com por HTTPS; API pública getTeams),
  `pegatinas/jugadores/<Nombre>.png` (43 fotos oficiales recortadas), `splash/<Campeón>.jpg` y `splash/<Campeón>_carga.jpg`
  (Data Dragon: Jax, Kaisa, Renata, XinZhao, Annie, Kalista, Anivia, Camille, Pantheon, LeeSin, Olaf, Nocturne, Akali,
  MissFortune, Orianna, JarvanIV), `iconos/<Campeón>.png` (cuadros).

## Falta: reescribir efectos.py 0-323 s (y luego todo el video con el mismo nivel)
Helpers nuevos en efectos.py (import mg_lol as L): `tar(de, a, titulo, sub, color, logo=COD, icono=, dato=, x=.72, y=.74)`,
`peg(en, jugador, nombre, color, logo, sub, dur=4, x=.17, y=.55, tam=420, gris=False)`, `gran(...)` (tam 560, x .25/.75),
`mg(fn, de, a, marcas, x=.5, y=.45)`. Quitar `chip`/`lista` de mg_tactica en todo el video.

GANCHO (0-50):
- 0-3.3 `apertura("WORLDS 2026", "Todo lo que ha pasado · al 27 de octubre")`.
- 3.3-9.0 `eliminado(AL, "Anyone's Legend", "Campeón de China 2026")`, marcas [6.0 «se fueron», 7.8 «partida»].
- 9.0-16.2 pegatinas GRISES de Tarzan (x .2), Shanks (x .8), Hope (x .5, y .3) entrando 9.4/10.4/11.3 + `tarjeta("Primer
  sembrado del LPL", dato="0-3")` en 12.3; sello «0-3» en «cero a tres» (13.2).
- 16.3-20.1 `versus(TLAW, AL, "Team Liquid elimina a AL", "Día 4", ganador=0)`, marca [18.0].
- 20.2-22.4 tarjeta grande centro «Y NO FUE LA ÚNICA SORPRESA».
- 22.4-26.7 `caida("China en el día 1", AL/BLG/TES/IG, "0-4")`, marcas [22.5, 23.3, 24.2, 24.7, 25.4, 25.9].
- 26.7-28.4 `gran` Smash + pegatina `splash/Kaisa_carga.jpg` + tarjeta «PENTAKILL · SMASH» dato «5».
- 28.5-30.8 `versus(DK, T1, "DK remonta a T1", ganador=0)`, marca [30.2].
- 30.9-35.5 `versus(LYON, GEN, "LYON le gana una partida a Gen.G", "Día 3 · partida 1", ganador=0)` marca [33.8] + peg Inspired.
- 36.0-49.6 `menu([Kaisa splash «Las jugadas», Smash «Los jugadores», GEN «Los equipos», T1 «Lo que viene»])`, marcas
  [41.5, 44.9, 46.3, 47.7]; antes (36-41) tarjeta «¿NO VISTE NADA?».
FORMATO (50-135): tarjeta «EL FORMATO» 50.8 · `caida("Play-in · Los Ángeles", KC(vive)/C9/FUR/MVK, sello="FUERA")` 56.1-63
marcas [56.3, 60.7, 61.2, 61.6] · `suiza()` 63.5-88, marcas [64.0, 66.9, 68.5, 69.5, 72.2, 85.0] · Fearless (88-99.6): tarjeta
grande arriba + pegatina del cuadro de Lee Sin con sello «YA USADO» en 95.5 · 100-106: tarjetas «8 A CUARTOS» y «FINAL 14 NOV
· BARCLAYS CENTER» · 106.7-115.6 tarjetas del lema e himno · 116-123 «CYANIDE» · 123.7-134: `gran` Faker x .25 + tarjeta T1 «TRICAMPEÓN»
dato «3» + «¿EL CUARTO SEGUIDO?» en 131.9.
PLAY-IN (135-172): tarjeta «PLAY-IN · 15-18 OCT» · tarjeta KC (logo) 139.4 + peg Yike 141.8 · `versus(KC, C9, "3-2", ganador=0)`
146.4-151.5 · `versus(KC, MVK, "3-0 y 3-0")` 153.5-159.5 · `caida("Fuera en el play-in", C9/FUR/MVK)` 160.5-164.5 · `versus(KC, AL,
"Su estreno: el campeón de China")` 165.6-172.
DÍA 1 (172-212): tarjeta grande «DÍA 1 · 23 OCT» · `resultados("Día 1 · ronda 1", GEN>IG, HLE>TES, MKOI>BLG, KC>AL)`
182-196.4 marcas [182.3, 184.5, 187.8, 193.4] · pegatinas grises Knight/Rookie/Tarzan/TheShy en fila 196.6 + sello «NUNCA HABÍA
PASADO» 199.6 · 205.3 `gran` Canna x .25 + peg Busio x .75 · 212 tarjeta «EN VIVO» corta (el vivo 209.7-263.8 sin más FX).
JUGADA 1 (263.8-323): el rebobinado, J() y las pizarras quedan; cambiar las chips por: pegatinas `_carga` de Olaf/Nocturne/
Akali/MissFortune en fila (x .2/.4/.6/.8, y .45, tam 300) en sus palabras · peg Busio (foto) x .82 en 274.7 · tarjetas con
`icono` para Renata/Orianna/Jarvan (x .25, y .3/.45/.6) · peg Canna x .2 + `_carga` de Jax x .8 en 294.8 · tarjeta grande
«¡CUÁDRUPLE!» dato «4» en 301.1 · tarjetas «BARÓN PARA KC» / «4.º NEXO CHINO EN 4 PARTIDAS» · lección con 3 tarjetas apiladas.
Después: `fx` → `mezcla` (PISTAS: pop2 en cada pieza nueva) → `video --hasta 326` → hoja → avisar.
Y documentar el kit en docs/estilo_analisis_tactico.md (§ «Gráficos de transmisión: mg_lol») + `nucleo/datos/galeria.json`.
