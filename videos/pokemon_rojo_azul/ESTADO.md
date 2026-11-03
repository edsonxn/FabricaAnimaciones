# Pokémon Rojo y Azul: su historia y los 20 secretos QUE IGNORASTE — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_gaming · SUBIDO privado y PROGRAMADO vie 20-nov-2026 18:00 CDMX (2026-11-21T00:00:00Z): https://youtu.be/7B0KBuT4WEg
- estilo: secuencia_yt (gameplay por beat + pegatinas reales + fichas translúcidas con la interfaz de Game Boy + mapas de Kanto con ruta + OST oficial, voz ElevenLabs Hope, sin Overgear) → doc: docs/estilo_secuencia_yt.md § Crónicas del gaming
- etapa: CERRADO (MASTER 15:34 + miniatura Flow + subido y programado, 3-nov-2026)
- siguiente: esperar el visto bueno del usuario sobre el MASTER (se arregla con `video --rehacer t0-t1` + `final` + resubir si pide algo); medir a 7 días (`yt metricas cronicas_gaming`); al aprobar: `fab.py pokemon_rojo_azul limpiar`

## Sesiones (plan de tramos · «continúa el video pokemon» retoma aquí · protocolo docs/sesiones.md)
- alias: pokemon, pokémon rojo azul, pokemon_rojo_azul
- vista previa: NO (elegido por el usuario el 3-nov): directo al MASTER, aviso al terminar
- leer al empezar: este ESTADO.md + docs/estilo_secuencia_yt.md (§ Crónicas del gaming, § REGLA DE ORO) + videos/majora_mask/ como modelo
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación (fuentes verificables) + guion.py + `voz` + `tiempo` | ✅ 3-nov | 107 frases, 1 453 créditos ElevenLabs, 12 falsas alarmas de Whisper aceptadas (CER_MAX_POR_FRASE); 20 puestos, gancho = 30 años de Pokémon (2026); MissingNo, camión de Mew, Mew de Morimoto (300 bytes), Jynx, betas/Capsule Monsters, Game Freak casi en quiebra |
| 2 | beats → búsquedas → bajar clips (OST/sonido original) → pegatinas → MG nuevos + fichas Game Boy + mapas de Kanto | ✅ 3-nov | 3 sesiones (la 2.ª cortada por contexto); kit nuevo nucleo/mg_pokemon.py; 228 efectos (fichas 1,0/min, MG 6,6, pegatinas 5,0, mapas 0,3); OST GB 35 pistas; 59 SFX del juego; mezcla −14,3 LUFS; youtube.json listo |
| 3 | render → final → verificar → miniatura Flow → subir y programar | ✅ 3-nov | render 1 283 s; MASTER 304,8 MB, CER 0,0026, desfase 0; hoja final sin bloqueos; miniatura Flow «20 SECRETOS» (variante A de 2); usuario avisado por voz; subido 7B0KBuT4WEg programado 21-nov 00:00 UTC |

## Decisiones del episodio (preguntadas al usuario al empezar, 3-nov-2026)
- duración total: 12-15 min · puestos de la lista: 20 secretos (+ historia) · Overgear: no (canal sin patrocinio)
- tema elegido entre 3 (Pokémon / GoldenEye / Conker); variable que cambia respecto a banjo_tooie: SOLO el juego
- Comentarios (3-nov): 0 nuevos, sin quejas ni sugerencias
- REGLA DE ORO: leer docs/estilo_secuencia_yt.md § REGLA DE ORO antes de `efectos.py` (todas las capas suman); `fab.py <v> chequeo` antes de renderizar

## Hecho
- 3-nov (tramo 3): `video` → `final` → `verificar`; miniatura Flow con ingredientes reales (prompt_miniatura.md, `miniatura_ing/`); `yt subir … private --publicar 2026-11-21T00:00:00Z`; registrado en canales/cronicas_gaming.json + BITACORA
- 3-nov (tramo 2): clips rehechos y revisados en hojas, efectos.py, mapas de Kanto, OST (bajar_ost + armar_musica_ost), SFX (bajar_sfx), fx + ambiente + mezcla, chequeo, youtube.json
- 3-nov: `nuevo --yt`, tema y duración elegidos, panel de canales actualizado; investigacion.md (fuentes); guion.py final; voz Hope turbo 107/107 (855 s); `tiempo` = 929 s

## Falta
- [x] guion + voz · [x] beats/clips · [x] MG/pegatinas/mapas · [x] sonido/mezcla · [x] MASTER · [x] miniatura Flow · [x] subir · [ ] visto bueno del usuario

## Cómo retomar (comandos)
```
python fab.py estado pokemon_rojo_azul
python fab.py pokemon_rojo_azul video --rehacer 270-280   arreglo por tramos (segmentos/ conservados) → final → resubir
python fab.py pokemon_rojo_azul limpiar                   al aprobar
```

## Archivos clave
- `guion.py`, `beats.json`, `busquedas.json`, `fuentes.json` (de dónde sale cada clip), `medios/`, `salida/creditos.txt`, `prompt_miniatura.md`

## Lecciones de este video (solo lo no obvio)
- Gritos de los 151 (Kvn3kHJFKuI): ni una fórmula lineal ni la energía del audio sirven (los gritos van pegados); el CAMBIO DE
  SPRITE del video da los 151 tiempos exactos (bajar_sfx.py; grito() = 0,6 + (n-1)·1,23 solo para elegir clip).
- Puntos de mg_mapa con foto: (x, y, nombre, tipo, foto), sin cadena vacía en medio (`fx hoja` revienta con «meta»).
- Los tutoriales de glitches en español (Zhecare) meten rótulos («PASO 4», «REQUISITOS») entre tomas limpias: revisar cuadro a cuadro.
- `fx` completo (montaje) cazó un fallo que `fx --seco` y `fx hoja` no ven: rebote negativo en mg_pokemon.sprite (arreglado).
- `chequeo`: los clips «fijado a mano» salen como clip «?» y dan avisos de narración falsos; comprobar en la hoja fx.
- `chequeo` «sonido nombrado» avisa en la frase que NOMBRA la música (10:19) aunque el tramo audible esté 3 beats después (scene-077, 6 s con voz callada): falsa alarma.
- Flow: pegar los ingredientes de uno en uno (en un bucle solo entra el primero); en.wikipedia da portadas/sprites con `generator=images`.
- Whisper oye «Victory Bell» (Victreebel) y «EMU» (Mew) en `verificar`: falsas alarmas, la voz está bien.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/<alias>.json`, BITACORA)
- [x] HALLAZGOS y mejoras documentados en el manual/estilo (docs/publicacion.md § MINIATURAS = FLOW: ingredientes de uno en uno)
