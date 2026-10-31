# Plan para REHACER «Los 40 secretos» (30-oct-2026). Lo pidió el usuario; se AÑADE, no se quita nada

## Lo que pidió el usuario (literal en sustancia)
1. Más motion graphics, sobre todo al inicio (el primero salía en 3:42 y no había otro hasta 13:12) «si el guion lo permite». No sustituir unas capas por otras al añadir reglas nuevas.
2. Lo que dice la voz se tiene que VER. Ej.: Torre Blanca de Cyrodiil, sin foto ni video.
3. Pegatinas: Runil grande, SIN FONDO (solo silueta), media pantalla, cara bien visible, video corriendo detrás. Igual objetos. Variar tamaño, posición y ESTILO; «atrévete a diseñar nuevos tipos», «que no se sienta que todas son iguales».
4. 16:55: clip de otro juego (confirmado: beat 118, «Sinh, the Slumbering Dragon», Dark Souls II).
5. Críticas con burla disfrazada (doc § COMENTARIOS 2c) y todas las reglas vigentes.
6. Al terminar: el usuario lo ve; si aprueba, se resube y se escribe la REGLA DE ORO para Warcraft, Tamriel, Runa y Gaming.

## HECHO
- guion.py: escenas nuevas `cr1` (antes de p25), `cr2` (antes de p8), `camp` (antes de p6), frase `cierre_3`, FONETICA (@jhonfeddis…, @lukelsue4430, kyrim), `ambiente_por` de 8 beats. Copias: `_guion_antes_rehacer.py`, `_efectos_antes_rehacer.py`, `_beats_antes_rehacer.json`. `timeline_beats.json` = timeline viejo (para `reajustar`).
- Voz generada; `seleccionar` dio REGENERAR en cr1_0, cr1_1, cr2_0: casi seguro es solo el CER por @usuario y «kyrim». Lee la transcripción en voz/eval.json; revisa que `voz/textos.json` diga «Kírim» en «kyrim» y «Escairim» en Skyrim (la tabla podría pisarse), y acepta con CER_MAX_POR_FRASE en guion.py o regenera (`fab.py <v> voz --seeds 1 2 3 4 --solo …`).
- Clips cambiados con `bajar --url --desde --rehacer` (ya en medios/): 22 gigante (OGQplWHCCbo), 56/57/58 Neloth (bUQi5nh97zI; 58 dice la frase del Nerevarino), 80/81 Runil (aw-PpcYUCJA).
- Tarjetas de comentario hechas: `com_UgzJYFZJk-eBnw3xQoB4AaABAg` (kyrim) y `com_Ugw36BCPJX6pZT5glDh4AaABAg` (no eres digno).
- Imágenes nuevas en pegatinas/: torre_skyrim (vista real desde Skyrim, ÚSALA a pantalla completa), torre_uesp, montana_roja, nave_extrana, ramati, madre_noche_ob, runil_b (567x985), martinet, alisanne, garnag, sala_falkreath. `trius.png` NO usar (no consta que sea ese Trius); `fuerte_dunstad.png` es mapa, no sirve.
- nucleo/peg_estilos.py (silueta, reliquia, banda, camafeo, legajo, abanico + recorte con rembg): compila, SIN PROBAR. En `silueta` la línea de `out.alpha_composite` quedó enredada: simplifícala y mira el resultado.
- nucleo/mg_tes.py: añadidos barra_vida, deteccion, semana, estrellas, soldados, cronologia: compilan, SIN PROBAR.
- nucleo/chequeo_yt.py + `fab.py <v> chequeo`: densidad contra la mediana del canal y narración ↔ imagen. Probado en este video.

## FALTA, en orden
1. Voz: resolver cr1_0, cr1_1, cr2_0; luego `fab.py <v> tiempo` y `fab.py <v> reajustar` (no renumera beats).
2. Beats nuevos: tras `reajustar`, en beats.json parte el tiempo de cr1, cr2, camp y cierre_3 en beats propios con id nuevo (scene-122…125; comprueba que nada asuma ids seguidos) y bájales clip (`busquedas.json` + `bajar`). cr1 y cr2: clip tranquilo; camp: tienda/casa de Skyrim. Los beats vecinos no deben quedar más largos que su clip.
3. Clips que faltan: beat 118 → `bajar 118 --url https://youtu.be/g-x-4hZXQFM --desde 1385 --rehacer` (Paarthurnax, video de 117; míralo). Rebaja con audio los de ambiente_por que no cambiaron, mismo video y segundo: 16 D17874c2Ykc 281.2 · 23 (ver fuentes.json) · 59 etQHLLWAeXY 810.3 · 62 Vp6V6VDTAwE 335.2 · 96 Wh17Z3hd7vo 713.9 · 115 SGhk197hhzc 102.2; luego `python _sonido_original.py habla` y `nivel`. Mira qué sale en 57 si sigue el Vergil.
4. Probar los 6 estilos y los 6 MG: `_prueba_mg.py` de ejemplo, hojas a 640x360. Silueta: rostros nítidos. Fotogramas de calidad: Delphine = medios/scene-095.mp4 a 4 s (1080p, primer plano); Neloth = bUQi5nh97zI a 70 s; Cicerón = eknUh5vJdnc a 300 s; Runil = h4.jpg (aw-PpcYUCJA 68-96 s) o runil_b; Erik, Ulfric, Tullius, Esbern, Paarthurnax ya son ≥ 1000 px. Guarda los fotogramas en pegatinas/ con nombre propio. Si rembg arrastra a otro personaje, recorta antes.
5. efectos.py, añadiendo sin quitar:
   - **MG** (objetivo ≥ 0,8/min y reparto parejo):
     - gancho `T.rejilla("Cuarenta secretos", 40, 40, ("Todos comprobados", 2))` en «Hoy te traigo cuarenta secretos»
     - 38 `T.barras` con alto_elfo/bretona/khajiit (1,08 · 1,03 · 0,95) y cambia el texto de su ficha para no duplicar datos
     - 34 `T.barra_vida`; 26 `T.deteccion` (sybille); cr1 `T.mision("Objetivo fallido", "Saber de Kyrim")`
     - 24 `T.semana` (rieklings, Arvak, Señor de los vampiros, adopción, casa; tachado: mayordomo esqueleto)
     - 22 `T.estrellas` (Escorpio y Cruz del Sur, formas reconocibles)
     - 16 `T.sospechosos` u otro para el giro sacerdote/vampiro; 10 `T.soldados(…, 40)`
     - 5 `T.cronologia` Erik (2009 diagnóstico · Make-A-Wish · 11 mayo 2011 · 11 nov 2011 Skyrim), sin sarcasmo
     - 4 `T.cadena` de Brand-Shei
     - camp: `T.rejilla("De cada 100 que ven este canal", 100, 14, ("Solo 14 están suscritos", 2))` + `T.mision("Misión nueva", "Suscríbete a Crónicas de Tamriel")` + `T.mision("Siguiente objetivo", "7 000 suscriptores")`
   - **Fichas** (objetivo ≥ 1,6/min, ~28; solo datos del guion, sin pisar mapas a pantalla completa): 39, 36 hombre lobo, 35 mamut (5 flechas + 1 virote), 32 Margret, 30 vampiro = otra raza, 27 cerraduras (0 ganzúas), 25 nave, 22 borra efectos, 20 Neloth, 19 Falx (~200 años), 18 muestra gratis, 17 misión cortada, 13 mil monedas × 4, 12 Alduin, 10 cuarenta soldados, 7 Delphine (3 atentados), 4 Lymdrenn, 3 trece años.
   - **Narración ↔ imagen:** 54 pantalla `torre_skyrim` en toda la frase de la Torre; 52-53 `montana_roja` grande + foto en el punto Morrowind del mapa; 43-44 `nave_extrana`; 74 `martinet`; 88 `ramati`; 106-107 `madre_noche_ob`, `alisanne`, `garnag`; 23 `karan_diario`; 11 bretona/khajiit/alto_elfo; revisa `previews/chequeo_narracion.md` entero.
   - **Pegatinas variadas:** al menos 1 de cada 3 en estilo nuevo, reparto por todo el video. Silueta: Runil (pedido), Neloth, Delphine, Cicerón, Erik, Ulfric, Paarthurnax. Reliquia: Estrella de Azura, Arco de Auriel, Martillo largo, amuleto de Talos, sopa. Banda: Delphine, Paarthurnax, Alduin. Camafeo: menciones rápidas (Bolund, Galathil, Urag). Legajo: Sybille, Margret. Abanico: enumeraciones (24, 37). Varía también tamaño, posición y giro de las normales.
   - Comentarios: cr1, cr2 con `com()`; `chequeo` debe dar fichas y MG sin ⚠.
6. `armar_musica_ost.py`: SECCIONES tiene tiempos fijos, muévelos con el timeline nuevo; `ambiente`, `fx`, `sfx`, `mezcla`, `video`, `final`, `verificar`. Render ~20 min. Mira C: (11 GB libres) y E: (1,6 GB). Beats 2:17 y 15:23 tenían negro; 14:29 y 14:47, congelados: corrígelos si caen a mano.
7. `python fab.py avisar "…"` + mensaje al usuario con qué comentarios críticos salieron. NO resubir ni tocar el video viejo nlMINAT_6UI hasta su visto bueno (ver abajo).
8. Mejoras de herramienta pendientes: en nucleo/chequeo_yt.py añadir una sección «clip de otro juego» (título/canal de fuentes.json sin el nombre del juego `yt.sufijo` o con títulos de otros juegos: habría cazado «Sinh, the Slumbering Dragon»; los «(fijado a mano)» salen como revisar) y correrlo solo antes de `video` completo en fab.py para `fuente="yt"` (sin bloquear). El docstring ya lo promete.

## Al aprobarlo el usuario
Subir el nuevo a la misma fecha (11-nov 12:08 CDMX), retirar el viejo con su OK (borrar es irreversible: pregúntale) y escribir la REGLA DE ORO: CLAUDE.md, `docs/estilo_secuencia_yt.md` (sección «LISTA DE CONTROL» arriba del todo con TODAS las capas), `videos/_plantilla_yt/ESTADO.md` y `efectos.py`, memoria, `yt subir`, panel de canales. Contenido: las reglas SUMAN, nunca sustituyen; lo que dice la voz se ve (todos los canales); ningún clip de otro juego; pegatinas variadas (`peg_estilos`, ampliar TEMAS a wow/er/gaming); MG repartidos desde el gancho; `fab.py <v> chequeo` antes de renderizar.
