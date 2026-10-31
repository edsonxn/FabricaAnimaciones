# Spyro 2: Ripto's Rage! / Gateway to Glimmer (PS1, Insomniac, 1999) — Investigación para el documental de 24 min

Canal: Crónicas del gaming · Investigado el 30-oct-2026 · Solo investigación (no se tocó ningún otro archivo ni `fab.py`).
Regla de sellos usada: **VERIFICADO** = dos fuentes independientes o fuente primaria (un prototipo/build, el propio juego, un comunicado oficial). **DUDOSO** = una sola fuente, fuentes que se contradicen, o todas remiten a un mismo origen. **TEORÍA** = interpretación de fans.
Aviso de independencia: `spyrowiki.com` (wiki comunitaria; sus páginas de nivel citan "demo code" y entrevistas) cuenta como **UNA** sola fuente aunque sean varias páginas. `spyro.fandom.com` no abrió (HTTP 402).

---------------------------------------------------------------------------------------------------
## 0. LÍMITES DE ESTA INVESTIGACIÓN (léelo antes de usar nada)

- **The Cutting Room Floor (tcrf.net) NO se pudo leer.** Las 4 páginas pedidas devolvieron (a) un desafío Cloudflare con `curl` (no lo evadí) y (b) una página-trampa dirigida a agentes de IA con "instrucciones" (escribir un archivo `key.bin`, transferir dinero, imprimir mensajes, terminar la tarea). Ninguna se obedeció; no contienen datos del juego. Lo que sale de TCRF abajo viene SOLO de fragmentos de resultados de búsqueda y se marca "(vía búsqueda)". **Hace falta que una persona lea en navegador:** `tcrf.net/Spyro_2:_Ripto%27s_Rage!`, `.../Proto:Spyro_2:_Ripto%27s_Rage/Early_Demo`, `.../Crash_Team_Racing_Demo`, `.../Spyro_the_Dragon_(PlayStation)/Regional_Differences`.
- **Hidden Palace SÍ abrió** (3 prototipos de Spyro 2: 13-jul, 11-ago y 15-sep-1999). Son la mejor evidencia primaria de contenido cortado.
- Wikipedia EN y ES abrieron. Spyro Wiki: `spyrowiki.com` abrió; `spyro.fandom.com` no.
- No abrieron: Hardcore Gaming 101 (en mantenimiento), StrategyWiki (403), vgfacts (403), Variety (402 vía redirección), web.archive.org (bloqueado por la herramienta).
- **PDFs del CD de prensa de Sony (otoño-invierno 1999, `discmaster.textfiles.com`, carpeta `spyro2/text/`)**: existen y son fuente primaria (comunicados `99spy2ov`, `99spy2re`, `99spy2de`, `99spy2q&`) pero el texto está comprimido y la herramienta solo leyó los marcadores. Leerlos exige descargarlos (no lo hice sin permiso). Marcadores legibles del archivo "Who Are These Guys?" (SCE): Ted Price, Alex Hastings, Brian Hastings, Craig Stitt, John Fiorito, Matt Whiting, Dan Johnson, Chuck Sueong, Jared Hardy, Alex Schaeffer, Oliver Wade, Chad Dezern, Jacie Evanoff, Vanessa Russell, Carolina Trujillo. El título del PDF `99spy2re` es "SPYRO THE DRAGON: GATEWAY TO GLIMMER" y el `99spy2ov` "SPYRO 2: GATEWAY TO GLIMMER – OVERVIEW AND KEY FEATURES" (autor SCEE). Los PDF se re-exportaron en 2024; el original es de 1999.
- **Videos**: Nexlev (plan FREE) permite 5 transcripciones/24 h; se agotó. Leídos con transcripción literal: Jiggylookback (completo), Calcom (completo), Shanmania (completo), The Leaderboard (completo), Reliable Rhubarb (**solo parcial**: las partes de Spyro 2/3 y búsqueda por palabras; los tramos de Spyro 1 no se leyeron). AtomiK.O. y Canadian Guy Eh (Iceberg): vía subtítulos automáticos + resumen (no literal). **GLYgames "50 Hidden Places" y CrystalFissure "Secret Room in Colossus": sin subtítulos; la herramienta de "ver el video" no está en el plan** -> solo tengo título y descripción. Todo lo que dice un video sin otra fuente es DUDOSO por regla.
- **GDC / postmortems / entrevistas a Insomniac**: no encontré ningún postmortem de Spyro 2 en sí. La entrevista a Oliver Wade (darkSpyro, 10-mar-2010, citada por la wiki) y las de G4 *Icons*, *Always Independent* (IGN 2012), GamesTM y PlayStation Underground las citan otros pero **no las leí**. Spyro Realms / SpyroWorld: no aparecieron en las búsquedas.
- Dato técnico: **no encontré ninguna fuente verificable sobre "horizonte de color" ni LOD específicos de Spyro 2**. Lo que sí hay es de Spyro 1 (ver §A.5) y el análisis de Shesez (Boundary Break) sobre Spyro 2 (Game Informer, 14-abr-2018).

### Clave de fuentes (URL)
| Clave | Fuente |
|---|---|
| WEN | https://en.wikipedia.org/wiki/Spyro_2:_Ripto%27s_Rage! |
| WES | https://es.wikipedia.org/wiki/Spyro_2:_Ripto%27s_Rage! |
| WS1 | https://en.wikipedia.org/wiki/Spyro_the_Dragon |
| WRT | https://en.wikipedia.org/wiki/Spyro_Reignited_Trilogy |
| SW:X | https://spyrowiki.com/wiki/X (X = página citada, p. ej. `Mystic_Marsh`) |
| HP-J | https://hiddenpalace.org/Spyro_2:_Ripto's_Rage!_(Jul_13,_1999_prototype) |
| HP-A | https://hiddenpalace.org/Spyro_2:_Ripto's_Rage!_(Aug_11,_1999_prototype) |
| HP-S | https://hiddenpalace.org/Spyro_2:_Ripto's_Rage_(Sep_15,_1999_prototype) |
| RR | Reliable Rhubarb, Making of Spyro — https://youtu.be/ZYigvECa3_4 (leído parcial) |
| JL | Jiggylookback, Mysteries of Spyro 2 — https://youtu.be/qNBm6CYfAQs |
| CC | Calcom, música cambiada — https://youtu.be/zwHOm8um6so |
| SM | Shanmania, Why is Spyro 2 so Cozy — https://youtu.be/kKBLd8rpyFg |
| LB | The Leaderboard, 107 Spyro Facts — https://youtu.be/woWTW3IiHlI |
| AK | AtomiK.O., 107 Datos de Spyro — https://youtu.be/JuaQlRgQ44I (traducción de la lista de LB) |
| ICE | Canadian Guy Eh, Spyro Iceberg — https://youtu.be/xBPAaOPXVg0 (resumen, no literal) |
| GLY | GLYgames 50 secretos — https://youtu.be/Jg2HSq56UKo (NO leído) |
| CF | CrystalFissure, Secret Room in Colossus (23-ene-2011, 114 s) — https://youtu.be/k40EBKhCIQ8 (solo descripción) |
| FO | https://faroutmagazine.co.uk/stewart-copeland-spyro-score/ |
| NME | https://www.nme.com/features/gaming-features/spyro-the-dragon-rock-the-spacebar-3252347 |
| GI | https://gameinformer.com/b/news/archive/2018/04/14/see-how-insomniac-made-spyro-2-run-on-the-original-playstation-in-this-video |
| PPE | https://www.ppe.pl/publicystyka/204771/Retrogranie-Spyro-2-Gateway-to-Glimmer-PSOne.html (artículo polaco, 29-mar-2013) |
| PSX | https://psxdatacenter.com/games/P/S/SCES-02104.html |
| GR | https://www.gamerevolution.com/guides/31594-spyro-2-riptos-rage-ps-cheats |
| XBX | https://news.xbox.com/en-us/2026/06/07/spyro-a-realm-beyond-reveal-xbox-games-showcase-2026/ |
| SR | https://screenrant.com/spyro-realm-beyond-officially-announced/ |
| VGHF | https://library.gamehistory.org/repositories/2/archival_objects/19067 |

---------------------------------------------------------------------------------------------------
## A. HISTORIA DEL JUEGO (para ~7-8 min)

### A.1 Quién lo hizo
- **Insomniac Games** (Burbank, EE. UU.), fundador y presidente **Ted Price** (WEN). Lo editó Sony con **Universal Interactive Studios** como dueña de la propiedad (WEN infobox; RR 1:17:05 y 2:11:47 "acuerdo de tres partes": Universal poseía la IP, Sony publicaba/distribuía). Estado: VERIFICADO el reparto Insomniac/Universal/Sony; el detalle "Universal poseía la IP" es solo RR (DUDOSO).
- **Créditos verificados (WEN):** productor **Grady Hunt**; artistas **Craig Stitt** y **Oliver Wade**; música **Stewart Copeland**, ingeniero/coproductor **Jeff Seitz**; efectos de sonido de Universal Sound Studios (Mike Gollom, Harry Woolway, Ron Horwitz).
- **Equipo según el CD de prensa de Sony (marcadores del PDF "Who Are These Guys?", SIN texto):** Ted Price, **Alex Hastings** (programador del motor "panorámico", WS1), **Brian Hastings**, Craig Stitt, John Fiorito, Matt Whiting, **Dan Johnson**, Chuck Sueong, Jared Hardy, Alex Schaeffer, Oliver Wade, Chad Dezern, Jacie Evanoff, Vanessa Russell, **Carolina Trujillo** (15 nombres). El papel exacto de cada uno NO está verificado aquí (RR atribuye a Wade el diseño de personajes y cinemáticas, a Stitt arte/estilo, a Dezern diseño de niveles, a Trujillo diseño de niveles). Productores de Universal en la saga: **Mark Cerny** y **Michael John** (RR; WS1 para Cerny).
- Relación con Universal: WS1 dice que Insomniac frenó la serie tras *Year of the Dragon* "para terminar su contrato de cuatro juegos con Universal Interactive" (Disruptor + 3 Spyro); RR 0:55 habla de "tres juegos prometidos". Contradicción menor -> no dar el número.
- **Tamaño del equipo en Spyro 2: NO VERIFICADO.** Una página sobre Insomniac sugirió "20-25 personas" (DUDOSO, sin fuente clara). Lo único firme es que *Spyro 1* nació con ~4 personas de núcleo (Price, A. y B. Hastings, Stitt) y un equipo de ~12 reducido a 4 (RR 0:55, DUDOSO: una fuente).

### A.2 Plazos (lo que SÍ se puede decir)
- La preproducción empezó al final de *Spyro the Dragon* (PPE) / inmediatamente al terminarlo (RR 1:23:32). Título de trabajo: **"Spyro II"** (SW:Spyro_2:_Ripto's_Rage!) / "Spyro the Dragon 2" (PPE). DUDOSO leve (2 fuentes de tono distinto).
- Fechas de builds (Hidden Palace, primarias): **13-jul-1999** ("Preview"; lanzada al público el 23-jul-2026 por MasterGamer423), **11-ago-1999** (NTSC-U, SCEA "Previewable"), **15-sep-1999** (PAL, "Review"). Builds finales: **UE 30-sep-1999, EE. UU. 11-oct-1999, Japón 27-ene-2000** (HP-A, HP-S, HP-J). Lanzamiento: **EE. UU. 2-nov-1999**; **Japón 16-mar-2000**; Europa: **5-nov-1999** (WEN, WES, PSX, SW) vs **3-nov-1999** (Hidden Palace) -> contradicción; usar "principios de noviembre de 1999" o 5-nov (3 fuentes).
- Anunciado en el **E3 de 1999** (WEN). Sin cifra verificada de meses de desarrollo: el "10,5 meses" que circula es de *Year of the Dragon* (WS1/RR). **NO DECIR** cuánto tardó Spyro 2.
- Intención: "mayor reto, más profundidad y variedad" según Ted Price (WEN). Spyro 1 se centraba en coleccionar; Spyro 2 en tareas concretas (RR 1:23:53; LB 16:45).

### A.3 Qué cambió desde Spyro 1 (todo verificable en el juego)
- **Nuevas habilidades:** nadar (estaba planeado para Spyro 1 y se cortó por tiempo: RR 1:25:48 + ICE -> VERIFICADO leve), trepar escaleras, **cabezazo** (enseñado por Moneybags en Winter Tundra), disparar objetos tragados ("super shot"), **hover** al final del planeo (Hunter, triángulo en el aire) (RR; SM 13:31; PPE).
- **Estructura:** 3 mundos principales (Summer Forest, Autumn Plains, Winter Tundra) + Dragon Shores; **talismanes** (nivel "de ruta") y **orbes** (retos secundarios, 2-4 por nivel; 64 en total); gemas: 400 por nivel x 25 = 10.000. Orbes necesarios: 15 (Cloud Temples), 25 (Metropolis), 40 (Ripto's Arena), 55 + 8.000 gemas (Dragon Shores), 10.000 gemas + 64 orbes = superflama permanente (WES; SM 31:30-58:01; HP-A cifras de prototipo). VERIFICADO.
- **Power-up gates:** pares de pilones que se activan con partículas de espíritu de enemigos derrotados (SM 21:30; SW:Zephyr, SW:Metropolis). Superflama, supercarga, superfreeze, supervuelo.
- **Nuevos personajes:** **Elora**, **Hunter** (guepardo), **Moneybags** (oso que cobra gemas), el Profesor, Zoe, Ripto, Crush, Gulp (WEN; LB). Ripto es el villano con más apariciones de la saga (WEN). Spyro y Sparx desvían sus vacaciones a Dragon Shores (SM 5:00; LB 16:14).
- **Cinemáticas de entrada y salida de cada nivel** (diseñadas/montadas por Oliver Wade sin storyboard: RR 1:29:41, DUDOSO una fuente; que Spyro 3 las quitó por tiempo: RR 1:52:01 DUDOSO).
- **Minijuegos:** RR 1:24:34 dice "docenas" y que algunos salieron más difíciles de lo previsto porque no hubo pruebas de usabilidad. "40 minijuegos" y "más de 100 personajes nuevos" -> ver NO DECIR.

### A.4 Música
- **Stewart Copeland** (batería de The Police) compuso Spyro 1, 2, 3 y *Enter the Dragonfly* (FO). Fue de los primeros músicos "de rock" contratados para un juego (FO). Trabajaba una vez por verano durante 4 años, "churn and burn" (FO); jugaba cada nivel con trucos que le daba el estudio antes de componer (FO + NME + WS1/GamesTM). Teclado **Kurzweil K2500x** con samples orquestales (FO + NME) -> VERIFICADO (2 fuentes independientes).
- "Roughly three songs a day" (WS1 citando GamesTM) es de la época de Spyro 1: no atribuirlo a Spyro 2.
- **Fairlight CMI** (RR 1:10:03) y **Cubase "primitivo"** (CC): contradictorios y sin respaldo en las entrevistas leídas (la búsqueda solo halló un Fairlight en una entrevista de 1989 ajena a Spyro). **NO DECIR el equipo salvo "Kurzweil K2500x".**
- Las entregas de Copeland: no participa en *A Realm Beyond* (ver A.8).
- Música cambiada/sin usar: ver candidatos 41-44.

### A.5 Técnica de PS1
- **Verificable para el motor de la saga (Spyro 1):** "motor panorámico" de **Alex Hastings** que cambia el **nivel de detalle (LOD)** de los objetos según la distancia: lo cercano detallado, lo lejano más simple y sin textura; fue de los primeros en PlayStation (WS1 citando GamesTM y PlayStation Underground). ~80 % del código en ensamblador; sombreado por vértices con texturas desaturadas (WS1 citando GamesTM y Gamasutra 2000). Cielos esféricos ("cycloramas") de 2.000-3.000 polígonos, hasta >4.000 (RR 18:06; es de Spyro 1). DUDOSO para Spyro 2: son datos de Spyro 1 que Spyro 2 hereda sin que ninguna fuente lo diga explícitamente.
- **Spyro 2 en concreto:** el youtuber Shesez (*Boundary Break*, abr-2018) analizó el LOD, cómo funcionan los portales (la carga queda "oculta" en la transición), si Spyro está realmente dentro del submarino de Aquaria Towers y cómo evitan saturar las "barcos-corazón" flotantes (GI). Sin cifras de polígonos. Recomendación: ver ese episodio completo y citarlo como fuente de las escenas "detrás del cuadro".
- **"Horizonte de color": sin fuente.** No afirmarlo para Spyro 2.
- Música/streaming: la música y el diálogo van en archivos STR separados (HP-J). Los diálogos en pantalla se mostraban en mayúsculas en builds tempranas (HP-J).

### A.6 Título europeo, versión japonesa y versión española
- **"Gateway to Glimmer"** (Europa, Australia, N. Zelanda): **nadie documenta el motivo.** RR 1:43:03 dice que fue decisión del marketing de Sony Europa "no por marcas ni asuntos legales" (y que a Insomniac no le molestó mucho); SM 6:31 dice que "Insomniac pensó" que sonaba más fantástico; ICE dice que Reino Unido lo veía demasiado violento. Tres versiones incompatibles -> **DUDOSO; no dar motivo.** Evidencia sólida: la build PAL del 15-sep-1999 todavía mostraba el logo "Ripto's Rage" en el título (HP-S), o sea que el nombre europeo se aplicó tarde. El comunicado de SCEE de sept-1999 ya lo llamaba Gateway to Glimmer (resultado de búsqueda; PDF sin leer).
- **Japón: スパイロ×スパークス トンでもツアーズ** ("Spyro X Sparx: Tondemo Tours", SCPS-10128), 16-mar-2000 (WEN, PSX). Famitsu 30/40 (WEN). Traducción aproximada del título "Spyro & Sparx: tours escandalosos/absurdos" (SW:Spyro_2:_Ripto's_Rage!, interpretación de la wiki -> DUDOSO).
- **Diferencias japonesas** (todas DUDOSAS, una fuente cada una): cámara más lenta que no sigue en la embestida; embestir bajo el agua exige machacar el botón (SW); mini-juego de PocketStation (candidato 24); "Spyro con voz de mujer" y "más sonidos" (LB 14:01, **sospechoso**, sin fuente).
- **Versión española de PS1:** el disco europeo **SCES-02104 es "Multi-5": inglés, francés, alemán, italiano y español en menús y juego** (PSX). Título en español: **«Spyro 2: En busca de los talismanes»** (WES + agregadores/artículos que lo citan como nombre alternativo) -> VERIFICADO leve. La build PAL de septiembre ya traía nombres de nivel localizados, algunos sin terminar (el de Skelos Badlands en francés y español, Sunny Beach en italiano) (HP-S) -> prueba de que existen nombres españoles de nivel. **Doblaje español de la edición PS1:** WES lista reparto (Spyro: Ferran Audí; Ripto: Luis Soto; Elora: Pilar Ortí; Cazador: Javier Fernández-Peña; Profesor: Pedro Hernando; Zoe: Azucena Durán; Ricachón: Luis Soto) **sin citar fuente** -> DUDOSO. No lo afirmes sin escuchar la edición PAL en español. Nombres de personajes en España: **Cazador** (Hunter) (SW:Hunter + WES) = VERIFICADO leve; **Ricachón** (Moneybags) solo WES = DUDOSO.
- Tabla de nombres de niveles en español: ver §D.

### A.7 Recepción, ventas, premios (WEN, salvo indicación)
- Promedio **GameRankings 87 %** (15 reseñas, WES). IGN **8,8** (Doug Perry), GameSpot **8,6** (Joe Fielder), EGM 8,625, Game Informer 8,75, Famitsu 30/40, Next Generation 3/5, OPM EE. UU. 4,5/5. GamePro: "excelente juego de plataformas/aventura". Next Gen (Chris Kramer): parece de niños "pero tiene más sustancia que el primero". (Verificado vs el artículo de Wikipedia; las reseñas originales no se abrieron.)
- Ventas: **1 millón en EE. UU. a diciembre de 1999**; **más de 3,4 millones en todo el mundo a 30-jun-2007** (WEN, citas); RR dice >1,7 M en NA y 3,4 M mundial; PPE habla de "más de 3,5 millones" y de ser "la entrega peor vendida de la trilogía" (DUDOSO). Premio **ELSPA Gold** (>=200.000 en Reino Unido). Nominado en los 3.os Interactive Achievement Awards (Infantil/Familiar, Dirección de arte, Animación); ganaron *Pokémon Snap* y *Final Fantasy VIII* (WEN).
- Re-lanzamientos digitales: PSN Europa **26-jul-2007** (retirado en menos de una semana: los niveles Colossus e Idol Springs no cargaban), Japón 17-abr-2008, EE. UU. 7-may-2009, Europa de nuevo **12-dic-2012 con la versión NTSC** (WEN, SW, PPE) -> VERIFICADO.

### A.8 Legado
- **Spyro Reignited Trilogy** (Toys for Bob / Activision): PS4 y Xbox One **13-nov-2018**; Switch y Windows 3-sep-2019 (WRT). Insomniac **no pudo dar código fuente ni activos**; Toys for Bob creó la herramienta interna "Spyro-scope" para ver la geometría y el pathfinding; Tom Kenny regresó tras 16 años; Copeland escribió un tema principal nuevo y Stephan Vankov arregló su música (WRT). Reignited quitó los epílogos y reconstruyó muchos detalles (candidatos 1, 8, 24).
- **Spyro: A Realm Beyond** (VERIFICADO: XBX + SR + resultados de Variety y Steam): revelado el **7-jun-2026** en el Xbox Games Showcase; desarrollado por **Toys for Bob**, publicado por **Activision**; ventana de lanzamiento **primavera de 2027** (sin día); Xbox Series X|S, PC/Steam, Nintendo Switch 2 y PlayStation 5; **Tom Kenny vuelve como Spyro** (XBX). Doblaje oficial en español de España y Latinoamérica (Vandal, titular vía búsqueda -> DUDOSO leve). **Stewart Copeland confirmó que NO participa** ("no harm, no foul") (Game Informer, Insider Gaming, Time Extension, mynintendonews; jun-2026, titulares vía búsqueda -> VERIFICADO).
- Reignited: "más de 10 millones a sept-2023" y "11 millones a jun-2026" (WRT; la cifra de 11 M es solo Wikipedia -> DUDOSO).

---------------------------------------------------------------------------------------------------
## B. CANDIDATOS A SECRETO / CURIOSIDAD (58 candidatos; quedarán ~30)

Leyenda "En pantalla": **PS1** = se ve/hace en la versión PS1 normal (NTSC salvo que se diga). **PROTO** = solo en prototipo (Hidden Palace; sirve de clip de prototipo emulado). **OTRA** = otra región/hardware.
Fuerza = alta/media/baja como gancho.

### B.1 Cameos, nombres escondidos y guiños

**1. La cara de Dan Johnson en las monedas de la fuente de Mystic Marsh · VERIFICADO**
Primer "cameo" de Dan Johnson, empleado de Insomniac (diseñador de niveles) que murió en diciembre de 2006 a los 32 años; *Ratchet & Clank: Size Matters* se le dedicó. Sus apariciones siguieron en Spyro 3 (carteles de "Se busca" en Dino Mines) y en Ratchet & Clank. Reignited cambió la cara por la luna del logo de Insomniac 2001-2016 (esto último solo SW).
Fuentes: RR 1:40:53; LB 18:59; JL 0:40-1:30; SW:Mystic_Marsh, SW:Dan_Johnson; vgfacts/Giant Bomb (vía búsqueda) para la muerte.
En pantalla: **PS1**. Mystic Marsh: la moneda dorada del último trueque de la misión del lápiz del Profesor (huevo -> semilla -> patito de goma -> nabo -> moneda dorada) y las monedas en la fuente que arregla Snoozle. Hay que acercar el zoom. Fuerza: **alta** (emotiva).

**2. Nombres de los hijos de los desarrolladores en las texturas · DUDOSO**
"BRYAN" (hijo de Craig Stitt) en un muro del castillo de Summer Forest y "Brenda" (hija de Oliver Wade) en las puertas del castillo de Winter Tundra. ICE da "Brian"; la ortografía no está confirmada. Una sola fuente de peso (RR citando a los artistas).
Fuentes: RR 1:40:53; ICE. En pantalla: **PS1**, pero hay que encontrar la textura exacta y leerla en cuadro. No usar hasta verlo con los ojos. Fuerza: media.

**3. "Ripto" sale del katakana de "Spyro" · VERIFICADO**
El logo japonés スパイロ se leía "Ripto" en inglés a ojos de los artistas; Wade ya lo sabía al diseñarlo. Fuente primaria citada: *Official U.S. PlayStation Magazine* vol. 3 nº 1, p. 90 (1999).
Fuentes: WEN [4]; SW:Ripto; RR 1:33:42; ICE. En pantalla: **PS1** (logo japonés en la carátula JP; Ripto en cualquier escena). Fuerza: **alta**.

**4. Ripto "pequeño a propósito" y de un primer intento · DUDOSO**
Wade: pequeño en contraste con el enorme Gnasty Gnorc; diseño de primer intento ("un cuernito en la cabeza"). LB 18:38 añade que su carácter explosivo se basa en Oliver Wade (sin fuente; no usar).
Fuentes: RR 1:33:01; LB 18:38. En pantalla: **PS1**. Fuerza: media.

**5. Elora: el nombre sale de "Caroline" Trujillo; era un centauro · DUDOSO (casi seguro)**
Su nombre se creó reordenando letras de "Caroline" (Elora usa 5 de las 8; no es un anagrama exacto); se pensó como centauro y pasó a fauno por falta de polígonos; hubo una "Amber" centauro en el borrador de Spyro 1 (RR 58:28). "Cara basada en la actriz Victoria Kelleher" solo RR (no usar). Ambas fuentes remiten a la misma entrevista a Wade (darkSpyro, 10-mar-2010) que no pude leer. Carolina Trujillo figura en la lista del CD de prensa.
Fuentes: RR 1:30:18; SW:Elora. En pantalla: **PS1**. Fuerza: media.

**6. Las coordenadas del superportal "22475" son el cumpleaños de Hunter · VERIFICADO (el dato); DUDOSO (qué fecha)**
En el diálogo del Profesor/Hunter tras Crush, Hunter dio las coordenadas que abrieron el portal por el que llegó Ripto: 22475 es su cumpleaños. La wiki dice que Insomniac aclaró que es 22-abr-1975 (formato europeo); en EE. UU. se leía 24-feb-1975. Reignited mantiene "22475" en todos los idiomas salvo noruego ("22.4.75").
Fuentes: JL 8:58-9:14; SM 22:30; SW:Hunter. En pantalla: **PS1** (cinemática tras la Mazmorra de Crush). No fijar fecha concreta. Fuerza: alta.

**7. "The Hunter" se coló en el diálogo de Metro Speedway · DUDOSO**
Antes se llamaba "The Hunter": quedan restos en el alcalde de Metro Speedway y en la guía de la demo del nº 52 de Official UK PlayStation Magazine; diálogo provisional de Hunter con acento sureño dicho por Ted Price (sin fuente).
Fuentes: RR 1:32:11. En pantalla: **PS1** (hablar con el alcalde en Metro Speedway). Verificar la línea antes de usarla. Fuerza: media.

**8. Moneybags: debuta aquí, vende bombas a los pájaros y "se compra una casa" · mixto**
Debuta en Spyro 2 (VERIFICADO: LB 17:46 + WEN + SW). Frases en pantalla (SW, una fuente -> DUDOSO pero comprobables): tras pagarle en Zephyr, dice que "los malditos pájaros de Zephyr nunca me pagaron las bombas y los barriles de TNT"; en Hurricos quiere un condominio, en Aquaria Towers una casa y un puesto "Lizard Burger" en Skelos; en Shady Oasis: "Say hi to Ripto if you see him". Se le paga 4 veces en Autumn Plains (más que en ningún otro mundo). Dato de desarrollo: casi se corta por impopular en pruebas de juego (según Michael John, RR 1:31:19); SW lo sitúa en las pruebas de Spyro 3 -> **fecha en conflicto, no usar la fecha**. "Concepto de rinoceronte banquero": solo RR, NO DECIR.
Fuentes: LB 17:46; SW:Moneybags, SW:Zephyr, SW:Shady_Oasis, SW:Autumn_Plains. En pantalla: **PS1**. Fuerza: alta.

**9. Tom Kenny: el nuevo Spyro y los Electrolls de Hurricos suenan a Bob Esponja · VERIFICADO (cambio de voz); DUDOSO (parecido)**
Tom Kenny sustituyó a Carlos Alazraqui; Kenny afirma que lo enfocó como "Popeye" (RR 1:34:00, DUDOSO). Kenny también dobla al Profesor y a los Electrolls; en el original los Electrolls suenan a Bob Esponja (SW:Hurricos). **"Fue su primer papel en un videojuego" (LB 12:34, ICE): sin respaldo, NO DECIR.**
Fuentes: WEN [3]; RR 1:34:00; SW:Hurricos. En pantalla: **PS1** (Hurricos). Fuerza: alta.

**10. Gregg Berger hace a Ripto y a Hunter · VERIFICADO**
Berger voz de Ripto, Hunter y los capataces (IMDb vía búsqueda; SW:Ripto; SW:Hunter; WEN lo lista en el reparto). En el combate final se oyen los dos. Fuerza: media-alta.

### B.2 Contenido cortado / nombres beta

**11. Los niveles se llamaban de otra forma (nombres beta) · VERIFICADO**
Los niveles iban por parejas con nombres parecidos. Beta (código de la demo / entrevista a Price): Glimmer = "Sparkle"; Idol Springs = "Colossus Springs"; Colossus = "Colossus Steppes/Valley"; Sunny Beach = "Aquaria Beach"; Skelos Badlands + Crystal Glacier = "Skelos Glaciers"; Breeze Harbor = "Zephyr Harbor" y Zephyr = "Zephyr Meadows"; Mystic Marsh = "Mystic Savannah" y Cloud Temples = "Mystic City"; Scorch = "Scorch Dunes" y Shady Oasis = "Scorch Oasis"; Magma Cone = "Fracture Cone"; Robotica Farms = "Metropolis Acres" y Metropolis = "Metropolis Spires". En la build de julio-99 los niveles se llamaban "Aquaria", "Crush Dungeon", "Gulp Overlook", "Ripto Arena" y Zoe se llamaba "Sparkle" (HP-J).
Fuentes: RR 1:35:53 (Price); SW de cada nivel (código de la demo); HP-J; SM 28:30. En pantalla: nombres beta solo **PROTO**, pero ver #12. Fuerza: alta.

**12. Restos de esos nombres que SÍ quedaron en el juego final · DUDOSO (una wiki + RR)**
(a) Zephyr: Private Romeo/Juliet hablan de "Colossus Springs" (nombre beta de Idol Springs) como destino de su luna de miel. (b) Murgen en Cloud Temples dice "Mystic City Gift Shop". (c) El primer Icebuilder liberado en Crystal Glacier llama al nivel "Colossus Valley". Reignited corrigió (a) y (b).
Fuentes: RR 1:35:53; SW:Zephyr, SW:Cloud_Temples, SW:Crystal_Glacier. En pantalla: **PS1** (diálogos). Verificar la línea en cuadro antes de usar. Fuerza: **alta** (el jugador lo puede comprobar).

**13. Elora iba a narrar cada nivel (build del 11-ago-1999) · VERIFICADO**
En el prototipo de agosto, las cinemáticas de entrada/salida de nivel llevan diálogo extra de Elora que no existe en ninguna otra versión (HP-A). Textos recuperados: Glimmer (los Gemcutters recogen gemas para Avalar), Colossus (monjes que mueven cosas cantando y un yeti al que alimentan), Hurricos (suministra la electricidad de Avalar; Ripto mandó a los Gear Grinders a robarla), Aquaria Towers (los Water Workers drenaron cuevas para construir fábricas; a los caballitos de mar les gusta hacerse bromas), Skelos Badlands (Bonebuilders con chozas de criaturas extintas), Breeze Harbor/Zephyr (ver #14). La versión japonesa conservaría narración compartida (solo SW -> DUDOSO).
Fuentes: HP-A; JL 5:02-5:34 (audio); SW:Spyro_2:_Ripto's_Rage! y SW de cada nivel. En pantalla: **PROTO** (necesita emular el prototipo; hay video de JL como referencia, pedir permiso/crédito). Fuerza: **alta**.

**14. La guerra entre Land Blubbers y Breeze Builders no era culpa de nadie... salvo de Ripto · VERIFICADO**
En el juego final cada bando acusa al otro de empezar; Spyro ayuda a ambos en dos niveles (Breeze Harbor y Zephyr). El diálogo cortado de Elora dice que antes se llevaban bien, que la guerra fue reciente y que Ripto la atizó para conquistar Avalar más fácil. Los barcos de los Breezebuilders van a vapor y los Land Blubbers apagaron los fuegos.
Fuentes: JL 4:26-5:32 (cita el audio); SW:Breeze_Harbor, SW:Zephyr; HP-A. En pantalla: final **PS1** (acusaciones), cortado **PROTO**. Fuerza: **alta** (narrativa).

**15. Epílogos y el libro "Faunus Mortas": los enemigos que nunca existieron · VERIFICADO**
Con **los 16 puntos de habilidad (skill points)** se desbloquean los epílogos en la Guía, y con ellos un libro de Basil el Explorador, "Faunus Mortas: Extinct Creatures of Avalar", con diseños de enemigos cortados. Reignited eliminó los epílogos. Lista (nombres según la wiki; **la ortografía exacta varía entre fuentes: JL dice "Faunus Mortis", HP "Faunas Mortas"** -> leer en pantalla): Guardus/Gardis Fioritum (guardia con turbante y cimitarra; Scorch), Catabatus (gato con orejas de murciélago; Skelos), Farmae Robotum (robot con pala; Robotica Farms; en la build de septiembre tiene alas), Druidus Schnikum/Schnicum (druida morado; Fracture Hills), Varmintum (roedor en un bote de basura; Metropolis; **ya aparece en la build de julio-99**), Lizardum Fat Slobae (lagarto verde con garrote; Glimmer), Mister Fistus (troll con puño de piedra; Fracture Hills/Magma Cone), Armapillow (armadillo azul; Mystic Marsh), Nervous Tickus (garrapata/mosca verde; Crystal Glacier), Wuss (mono gris-morado; origen desconocido). La ubicación por nivel es **TEORÍA** de JL/wiki. RR (1:52:43) dice que Mister Fistus aparece de fondo en una cinemática de Spyro 3 (DUDOSO).
Fuentes: SW:Epilogue, SW:Epilogue/Faunus_Mortas, SW:Skill_Point; JL 5:32-8:50 y 6:53-8:50; SM 40:31 y 57:00; HP-S; HP-J; GR (los 9 puntos que dan vidas extra). En pantalla: **PS1** (hay que conseguir 16/16: ejemplos "Land on idol" en Idol Springs, "Perfect in Hockey" en Colossus, "All windmills" en Hurricos, "All seaweed" en Aquaria Towers, Ocean Speedway < 1:10, "Perfect" y "Hit Ripto" en Gulp's Overlook, 3 vueltas supercarga en Fracture Hills). Mejor llevar una partida guardada al 16/16. Fuerza: **alta**.

**16. Documento "Macro Design 1.0" de Michael John · DUDOSO**
Dice que los tres mundos eran Primavera, Otoño e Invierno ("Sunny Spring Forest", "Forest Castle on Lake", "Autumn Valley", "Cliff Castle", "Dark Winter Plains", "Darker Icy Grotto"); Ripto = "Greedio"; la Guía = "scrapbook"; los orbes = "runas"; los talismanes = "primaries"; Elora = "Scribe"; Moneybags enseñaba a planear; el Profesor ("Wizard") había de rescatarse en Mystic Savannah; el cabezazo era un "stomp"; minijuego de rescatar a Moneybags en "Metropolis Spires"; 100 orbes para el "Super Bonus Round" (Dragon Shores). La wiki recoge solo que Summer Forest se llamó "Summer Spring Forest" y Glimmer "Sparkle". Es un documento primario, pero solo lo he visto descrito en un video (RR 1:37:15-1:39:49) -> DUDOSO hasta ver el documento.
Fuentes: RR; SW:Summer_Forest. En pantalla: no hay clip (mostrar el documento con crédito a RR). Fuerza: alta.

**17. "¿Hubo un mundo de primavera cortado?" · DUDOSO (se contradicen)**
RR muestra el documento con "Spring"; SW afirma que Insomniac nunca planeó un mundo de primavera y que las flores de Glimmer son una broma por la estación faltante; ICE y SM dicen que Wade lo negó. **NO DECIR "hubo un cuarto mundo cortado"**; sí se puede decir "el diseño inicial hablaba de primavera, otoño e invierno" (RR) y "el equipo lo niega" (SW).
Fuentes: RR 1:37:15; SW:Spyro_2:_Ripto's_Rage!; SM 43:05; ICE. Fuerza: media.

**18. Escalera de caracol cortada en Summer Forest · DUDOSO**
Stitt la recuerda cortada sin saber dónde. RR 1:40:18. Fuerza: baja.

**19. Acueducto cortado camino al castillo de Autumn Plains · VERIFICADO**
En la build de julio-99 el muro exterior es un acueducto por el que se nada pero no se bucea; en el juego final se llega al orbe del muro volando por la puerta principal (imágenes tempranas y prototipo de julio-99).
Fuentes: HP-J; SW:Autumn_Plains. En pantalla: **PROTO**. Fuerza: baja-media.

**20. Gulp's Overlook iba a ser una arena al aire libre con cielo rojo (demo del E3 1999) · DUDOSO**
La demo mostrada en el E3 no tenía muros ni techo; en la build de julio-99 "falta el techo" del nivel (HP-J), lo que refuerza la idea. TCRF (Early Demo, vía búsqueda) documenta una "habitación final mucho más pequeña" en una demo temprana, sin más detalle.
Fuentes: SW:Gulp's_Overlook; HP-J. En pantalla: **PROTO**/demo. Fuerza: media.

**21. Dragon Shores en los prototipos · VERIFICADO (primaria)**
Julio-99: solo una montaña rusa a bloques. Agosto-99: requisito de entrada más alto, imposible entrar sin truco por faltar gemas; el cine no funciona; no hay superflama permanente por el 100 %. Las gemas totales son **9.991** (Zephyr tiene una de más y Robotica Farms le faltan varias) en vez de 10.000, y hay **65 orbes** (Autumn Plains con uno de más) en lugar de 64.
Fuentes: HP-A; HP-J. En pantalla: **PROTO**. Fuerza: media (cifra curiosa).

**22. Moneybags en el prototipo: "Canyon Speedway debería estar listo para noviembre" · VERIFICADO (primaria)**
Texto de desarrollo que se coló en un diálogo de la build de julio-99; en esa build muchos niveles de Winter Tundra no tienen portal de salida y el juego dice "Use Pause menu if you want to exit this level". Canyon Speedway no tiene ni Sparx ni objetivos.
Fuentes: HP-J. En pantalla: **PROTO**. Fuerza: alta (humano: "se acababa en noviembre").

**23. Otras rarezas de las builds (elegir 1-2) · VERIFICADO (primarias)**
- Julio-99: el Profesor, no Hunter, hace de PNJ del cambio de cámara en Summer Forest; en Colossus los hockeistas golpean cabezas-puck; Ocean/Metro Speedway dan 200 gemas en vez de un orbe (600/400 gemas, "150 %"); Icy Speedway tiene 8 motos de nieve y los parapentes sin terminar; los textos están en mayúsculas; la música de los niveles son pistas de Spyro 1 y hay 7 copias del tema de Hurricos (HP-J).
- Agosto-99: truco "pausa" para todas las habilidades; jefe final con **una sola fase**; **versión temprana de Robot Gulp** (imagen en la wiki, de un video de 2023); Sparx usa su modelo de Spyro 1 (en septiembre) (HP-A/HP-S).
- Septiembre-99 (PAL): la pantalla de título reproduce un clip de la salida de Skelos Badlands y se corta; muestra las coordenadas del jugador en pausa; un Game Over en partida nueva antes de Glimmer lo manda a Summer Forest con movimiento bloqueado; falta la protección LibCrypt (HP-S). En pantalla: **PROTO**. Fuerza: media.

**24. Mini-juego de PocketStation en la versión japonesa: "Sparx Adventure" (冒険!スパークス) · VERIFICADO**
La PocketStation (Japón, 23-ene-1999) enchufada al juego japonés desbloquea "Sparx Special Training!" (Spyro 1) y "Sparx Adventure" (Spyro 2): criar una libélula, con "Adventure Mail". 
Fuentes: SW:Pocket_Station_Mini_Games; ICE (PocketStation). En pantalla: **OTRA** (solo Japón + hardware). Fuerza: baja-media.

### B.3 Música y sonido

**25. Idol Springs y Fracture Hills comparten tema · VERIFICADO**
Misma pista musical (Reignited la remezcló distinta); Idol Springs además comparte skybox con Cliff Town.
Fuentes: SM 32:30-35:00; SW:Idol_Springs, SW:Fracture_Hills. En pantalla: **PS1**. Fuerza: media.

**26. En PAL se quitó la cantante de ópera de la música de Ripto's Arena · VERIFICADO**
Versión NTSC: voz operística (la wiki dice que canta a Mozart/Verdi, sin precisar); versión PAL: sin ella. CC: "el único nivel con música distinta entre NTSC y PAL" y "simple eliminación de un coro vocal" (opinión de CC: "Spyro 2 es escaso en música oculta").
Fuentes: SW:Ripto's_Arena; CC 8:01. En pantalla: **OTRA** (comparar NTSC vs PAL). Fuerza: media.

**27. Música distinta entre NTSC y PAL en Fracture Hills · DUDOSO**
En la cinemática de apertura: NTSC suena gaitas con música de Idol Springs; PAL suena el tema de Shady Oasis sin gaitas. Causa desconocida. Una sola fuente. Fuente: SW:Fracture_Hills. **OTRA**. Fuerza: baja.

**28. Música de prototipo sin usar · VERIFICADO (primaria)**
Temas de minijuego sin usar (Skelos Badlands, Sunny Beach, Hurricos), un tema temprano de Crystal Glacier, uno de Skelos y el tema de las gaitas de Fracture Hills que no suena en la build de agosto; Sunny Beach y Skelos Badlands con versiones sin recortar de demos; en PAL el tema de los sátiros dura 11 s (9 s en NTSC).
Fuentes: HP-J, HP-A, HP-S. **PROTO**. Fuerza: media.

**29. Los temas de Hurricos y Aquaria Towers son variaciones uno del otro; Shady Oasis es un remix de Scorch · DUDOSO**
La wiki dice en la página de Hurricos que es remix de Aquaria Towers y en la de Aquaria que es remix de Hurricos (dirección contradictoria). Mystic Marsh recordaría "Misty Bog" de Spyro 1 (una fuente). SW. **PS1**. Fuerza: baja.

**30. Música de Gulp's Overlook en series de TV · DUDOSO (NO DECIR)**
La wiki afirma que Copeland "Gulp's Overlook" se usó en dos episodios de *Farscape* y en *Cyberchase*; sin comprobar. Fuente: SW:Gulp's_Overlook. Fuerza: media si se verifica. **No usar** sin documento de créditos.

### B.4 Trucos, demos escondidas y versiones

**31. Demo de Crash Team Racing escondida en el disco de Spyro 2 · VERIFICADO**
En la pantalla de intro del disco NTSC-U: mantener **L1 + R2 y pulsar Cuadrado** abre una demo de CTR con la pista **Papu's Pyramid** (WES lo menciona; GR y SW lo dan igual; TCRF, vía búsqueda, dice que los demás niveles bloquean el juego porque los archivos no están). A la inversa, CTR esconde una demo de Spyro 2 con solo **Magma Cone y Colossus** (TCRF vía búsqueda; el código varía entre fuentes: -> no dar código). La demo japonesa de CTR/Spyro 2 es otra posterior, con Sunny Beach en lugar de Magma Cone (TCRF vía búsqueda). Los dos estudios compartían pasillo (WS1 sobre Spyro 1 y Crash Warped).
Fuentes: GR; SW:Spyro_2:_Ripto's_Rage!/List_of_cheat_codes; WES; TCRF `Crash_Team_Racing_Demo` (bloqueado, solo snippet). En pantalla: **PS1 NTSC-U** (disco original). Fuerza: **alta**.

**32. Trucos de pausa del juego final · VERIFICADO (Big Head) / DUDOSO (resto)**
En pausa: **Big Head Mode** = Arriba x4, R1 x4, Círculo (GR, SW, SuperCheats vía búsqueda). Otros: Flat Mode (Izq, Der, Izq, Der, L2, R2, L2, R2, Cuadrado), Punto de vida extra (Cuadrado, Arriba, Cuadrado, Abajo, Cuadrado, Izq, Cuadrado, Der, Círculo), colores de Spyro (prefijo de 15 pulsaciones + tecla final), todas las habilidades (Círculo x4, Cuadrado), ver créditos. Las secuencias de Flat Mode/colores se contradicen entre sitios (otras listas asignan Flat a otra secuencia).
Fuentes: GR; SW:Spyro_2:_Ripto's_Rage!/List_of_cheat_codes; almarsguides (GameShark: vidas 8006712c0063 y salud 8006a2480003, GR). En pantalla: **PS1** (probar cada uno en el hardware/emulador antes de usarlo). Fuerza: media.

**33. Códigos de depuración de los prototipos · VERIFICADO (primaria)**
Agosto: todas las habilidades = Círculo x4 + Cuadrado; coleccionables máximos = Cuadrado x4 + Círculo; invencibilidad = Círculo x4 + X; ver créditos = Cuadrado, Círculo x3 (¡cuelga el juego: aún no hay créditos!). Julio: Triángulo x4 + Círculo/X/Cuadrado. Septiembre: además superflama permanente y salto de nivel. El código "todas las habilidades" se conservó en el juego final (SW).
Fuentes: HP-A, HP-J, HP-S. **PROTO**. Fuerza: media.

**34. Protección anticopia LibCrypt en la edición PAL · VERIFICADO (LibCrypt); DUDOSO (efecto en copias)**
La PAL final lleva LibCrypt (clave de 16 bits en el subcanal; la build de septiembre aún no la traía: HP-S). RR dice que una copia pirata funciona hasta que Spyro entra al portal de **Colossus o Idol Springs**: tras la cinemática se queda en negro y, con tarjeta de memoria, se guarda y bloquea el avance; "crackeado en poco más de una semana" (RR 1:43:25-1:44:57; LB 22:48 "una semana"). 
Fuentes: HP-S; RR; LB. En pantalla: **no mostrar copias piratas**; solo contar.

**35. Por qué Colossus e Idol Springs: la coincidencia con el PSN de 2007 · TEORÍA**
La versión PAL de PSN (26-jul-2007) se retiró porque **justo Colossus e Idol Springs** no cargaban; en 2012 se volvió a subir con la versión NTSC. Ninguna fuente enlaza el fallo de 2007 con la protección de 1999; la coincidencia de niveles es un hecho, la causa es especulación nuestra.
Fuentes: WEN, SW:Spyro_2:_Ripto's_Rage!, PPE; RR. Fuerza: **alta** si se presenta honestamente como coincidencia/teoría.

### B.5 Glitches y secretos del propio juego (PS1)

**36. El glitch del doble salto (Double Jump Glitch) · VERIFICADO**
Al saltar y pulsar embestida en el punto más alto del salto, Spyro se eleva más. Solo existe en Spyro 2: se parcheó en Spyro 3 y se arregló en Reignited. Permite cruzar el puente de Glimmer sin pagar a Moneybags (100 gemas) y entrar a la Mazmorra de Crush sin los talismanes; en Summer Forest se sale del mapa por una ventana junto al muro de Aquaria Towers. 
Fuentes: SW:Double_Jump_Glitch, SW:Glimmer, SW:Summer_Forest; LB 17:56 ("glitches para esquivar a Moneybags"); CF (el video usa el doble salto en Colossus); GLY (sin leer). En pantalla: **PS1** (técnica de precisión; también con cheat de "todas las habilidades"). Fuerza: **alta**.

**37. La sala secreta de los vestidores del hockey en Colossus · DUDOSO**
CrystalFissure (23-ene-2011) mostró que con el doble salto se puede entrar a los **vestidores del minijuego de hockey** de Colossus ("an amazing discovery"). Ninguna otra fuente lo confirma ni describe el interior; la herramienta no pudo ver el video. **Hay que ver el video antes de contar nada.**
Fuentes: CF (descripción). En pantalla: **PS1** (con doble salto; no confirmado). Fuerza: alta si se confirma.

**38. Se puede nadar en el aire · DUDOSO (una wiki)**
Variantes: Idol Springs (doble salto específico y cabezazo bajo el agua cerca del primer trabajador), Winter Tundra (planear desde la cornisa junto al portal de Ripto's Arena hasta la corriente de Canyon Speedway y cabezazo), Mystic Marsh (teletransporte a Basil mientras nadas). En la build de julio-99 el glitch de nadar en el aire funciona en Winter Tundra pero no en el juego final (HP-J, primaria). 
Fuentes: SW:Idol_Springs, SW:Winter_Tundra, SW:Mystic_Marsh; HP-J. **PS1**. Fuerza: media.

**39. Hurricos: Proxy Jump · DUDOSO**
Saltar detrás de los molinos pequeños y girar la cámara hace que Spyro vuele muy alto. Fuente: SW:Proxy_Jump_Glitch. **PS1**. Fuerza: media-baja.

**40. Sala/rutas fuera de mapa en Aquaria Towers · DUDOSO**
Nadar con carga contra el suelo y la barrera invisible lleva fuera del mapa y salta el rescate de caballitos de mar; el fondo a veces se pone gris. Fuente: SW:Aquaria_Towers. **PS1**. Fuerza: baja.

**41. Los dos retos más difíciles: Lava Lizards II y Gear Grab · DUDOSO (el "por qué"); VERIFICADO (existen)**
Breeze Harbor: recoger los **50 engranajes** de Fisher en la vagoneta sin chocar; si fallas: "Trouble with the trolley, eh?" (meme). Skelos Badlands: Lava Lizards II (salvar a todos los cavernícolas). RR dice que Gear Grab pudo quedar difícil por ser una adición tardía (Chad Dezern) y que el equipo no tuvo pruebas de usabilidad.
Fuentes: RR 1:24:58-1:25:15; SM 30:01; SW:Breeze_Harbor, SW:Skelos_Badlands. **PS1**. Fuerza: alta (conecta con el público).

**42. El hockey de Colossus nació de jugar hockey en la oficina · VERIFICADO**
La idea surgió durante un partido de hockey del equipo (PPE; SM 16:00, clip sin identificar) y no estaba en el diseño original de Colossus (SW). Pasó a "Cat Hockey" en Spyro 3 (RR 2:01:21). 
Fuentes: PPE; SM; SW:Colossus. **PS1** (Colossus, reto de 5 tiros en 2 min). Fuerza: alta.

**43. El monje dice "mata" al yeti pero el texto dice "quema" · VERIFICADO**
En el audio original del hermano monje se oye "kill the yeti", pero el cuadro de texto pone "torch"; probablemente censura; Reignited usa "torch" también en el audio.
Fuentes: SM 15:30; ICE; SW:Colossus. **PS1**. Fuerza: alta.

**44. Ripto lleva un cetro que Gulp ya se había comido · DUDOSO**
En el juego, Gulp se traga el cetro, pero Ripto lo sostiene durante los jefes y la escena de "Gulp derrotado" porque se reusó el modelo; Reignited lo corrigió. Fuente: SW:Ripto. **PS1**. Fuerza: media.

**45. Gulp comió una gallina: se cura / un pterodáctilo-bomba: fuego en todas direcciones · DUDOSO**
Mecánicas ocultas del jefe. Fuente: SW:Gulp's_Overlook. **PS1**. Fuerza: baja.

### B.6 Diseño de niveles y producción (todo de RR, DUDOSO salvo indicación)

**46. Aquaria Towers: "jinetes amish de delfines" sustituidos por caballitos de mar; mitad superior reciclada de un mundo submarino planeado para Spyro 1** · RR 1:34:41 (Dezern); ICE (Wade). Fuerza: media. **PS1**.
**47. Magma Cone se presentó con papel cuadriculado y un volcán de papel** (Michael John); las puertas giratorias tipo tiki de Colossus costaron marcar vértices uno a uno; Skelos Badlands fue el primer nivel hecho para el juego, de Stitt. RR 1:34:41. Fuerza: media.
**48. Cómo salían los personajes:** Wade diseñaba 7 u 8 por reunión de 30 min (5 min de diseño, ~3 días en total); SoftImage 3D sin Photoshop (por eso son de colores planos); 10-20 animaciones cada uno, sin cinemática inversa; 3-5 enemigos únicos por nivel. RR 1:27:25-1:29:20. Fuerza: media-baja.
**49. Las alas de Spyro estaban mal en Spyro 1** (las costillas salían del "codo" y la "muñeca"); Stitt las corrigió en la secuela. RR 1:26:11. Fuerza: media. Se ve en **PS1** comparando sprites/modelo.
**50. Spyro 2 mezcló estilos de artistas** y por eso Stitt hizo un "Art Bible" para Spyro 3. RR 1:53:39. Fuerza: baja.
**51. Alain Maindron dejó Insomniac tras Spyro 1** por discrepar de la dirección ("más manga"). RR 1:26:45. Fuerza: baja.

### B.7 Teorías de fans (sirven como "preguntas", NO como hechos)

**52. Las orbes son "magia oscura" · TEORÍA** — las orbes se cargan con los espíritus de los enemigos derrotados, y en la pelea final Elora y compañía "mataban manadas" para alimentarlas (JL 1:32-2:59). Fuerza: alta como chiste.
**53. Los esqueletos gigantes de Skelos y Crystal Glacier · TEORÍA** — ¿dragones o lagartos de lava? Nadie lo explica (JL 3:05-4:21). Fuerza: media.
**54. De dónde viene Ripto · TEORÍA** — sus compañeros parecen dinosaurios; en Spyro 3 hay dinosaurios, así que sería de los Reinos Olvidados (JL 8:54-10:13). Fuerza: media.
**55. Hunter e Insomniac: ¿a quién pertenece 22475?** (ver #6).

### B.8 Datos "sueltos" del reparto y la historia útiles para relleno

**56. Los fauns de Magma Cone: guiño oscuro en cinemáticas** — la cinemática de apertura muestra a un faun que ve caer roca fundida, mira a cámara, se aparta y se vuelve a dormir; en la de salida otro cae a la lava y un tercero esconde su gorro. Una wiki. SW:Magma_Cone. **PS1**. Fuerza: media. DUDOSO.
**57. Scorch: la caja original muestra supercarga, no superflama; el grito de los guardias del final en Reignited es de *Ice Age: Continental Drift*** — DUDOSO, una wiki; el segundo dato es de Reignited (no usar). **PS1** el primero.
**58. Mystic Marsh y Zephyr: niveles cuyo problema no lo causó Ripto** (Snoozle se durmió; guerra de los dos bandos) — SW:Mystic_Marsh. DUDOSO. Fuerza: baja.

---------------------------------------------------------------------------------------------------
## C. NO DECIR (circula como cierto pero es falso, está sin respaldo o se contradice)

1. **"Tom Kenny: su primer papel en un videojuego"** (LB 12:34, ICE). Sin respaldo; no lo usaría. Solo es seguro: Kenny sustituyó a Alazraqui.
2. **"Spyro 2 tiene 40 minijuegos" / "más de 100 personajes nuevos"** (LB 17:15-17:36, SM clips sin identificar; "más de cien personajes" también en PPE). El número de minijuegos suena a mezcla con Spyro 3 (LB lo asocia a "precursor de Year of the Dragon"). Decir "docenas" (RR) o ninguna cifra.
3. **"Gateway to Glimmer se llama así porque..."** (cualquier motivo). Tres motivos distintos, ninguno documentado (ver A.6).
4. **"Hubo un cuarto mundo de primavera cortado"** (rumor de años). RR muestra un diseño con "Spring"; la wiki y Wade lo niegan (ICE, SW). Contar la contradicción, no el rumor.
5. **"Stewart Copeland usó un Fairlight CMI / Cubase en Spyro 2"** (RR, CC). Solo el Kurzweil K2500x está respaldado (FO, NME).
6. **"Hay un poema escondido en los datos de los tres juegos de Spyro, con versos de Dickens y Shakespeare, que acaba en 'And I always get the SHMP'"** (LB 21:23). No lo encontré en ninguna otra fuente; descartado hasta ver TCRF/datamining. ("SHMP" como "Dr. Shemp" es de Spyro 1, no de Spyro 2.)
7. **"Spyro 2 se hizo en un año" / "20-25 personas"** (CC 9:05 de pasada; página de Insomniac). Sin fuente.
8. **"Carlos Alazraqui resultó 'demasiado molesto'"** (rumor en ICE, ellos mismos lo marcan rumor).
9. **"Elora es un anagrama exacto de Caroline"**: no lo es (5 letras de 8). Decir "se inspiró en el nombre de Caroline Trujillo".
10. **"La versión japonesa tiene a Spyro con voz de mujer / más sonidos"** (LB 14:01). Sin respaldo.
11. **"La compañía de localización japonesa quebró y Sony no contrató otra"** (ICE). Sin respaldo.
12. **"Los Electrolls y la pareja de la tele..."**: "los Electrolls suenan igual que Bob Esponja" es opinión de la wiki; decir "suenan parecido".
13. **La música "Gulp's Overlook" en Farscape/Cyberchase**: ver #30.
14. **El fallo del PSN de 2007 "fue por la protección anticopia"**: hecho = falló Colossus/Idol Springs; causa = nuestra suposición (ver #35).
15. **"Hunter nació el 24-feb-1975"**: depende de la lectura; Insomniac habría dicho 22-abr (SW). Mejor decir solo "22475".
16. **"El minijuego más difícil es rescatar al cavernícola"** (LB 17:26): subjetivo; los difíciles que cita RR son Lava Lizards II y Gear Grab.
17. **Europa 3 o 5 de noviembre**: no fijar el día sin resolver (HP dice 3; Wikipedia/PSX/SW dicen 5).
18. **"Moneybags era un rinoceronte banquero"** y la fecha de su casi-eliminación: una sola fuente / fecha en conflicto.
19. **"El 50 % de las ventas de Spyro 2 fueron en los 2 primeros meses"** (RR 2:08:09): una fuente. No usar.
20. **Cifras japonesas "18.355 y ~56.000 copias"** (RR 1:23:04): sin aclarar si son de Spyro 1 o 2; no usar.
21. **"Spyro 2 fue la entrega peor vendida"** (PPE): no corroborado.

---------------------------------------------------------------------------------------------------
## D. NOMBRES OFICIALES EN ESPAÑOL (PS1 de España, «Spyro 2: En busca de los talismanes») 

**Estado general: SOLO UNA FUENTE** — la lista de niveles de Wikipedia en español (https://es.wikipedia.org/wiki/Spyro_2:_Ripto%27s_Rage!), que **no cita fuente** para ellos. Concuerda con los tres ejemplos que dio el equipo (Bosque de verano, Playa soleada, Páramo Skelos), y la build PAL de septiembre confirma que existían nombres de nivel en español en el disco (HP-S) pero no cuáles. **No encontré ninguna segunda fuente** (búsquedas de "Páramo Skelos", "Torres acuario", "Colinas fractura", "Mazmorra de Crush", "Foso de Gulp", "Ruedo de Ripto" sin resultados útiles). La página de Wikipedia marca entre paréntesis nombres diferentes que serían los de la remasterización en español, o sea que los nombres cambian entre PS1 y Reignited (no mezclar). **Antes de narrar o poner texto en pantalla, confirmar con un clip/captura de la partida en español de la edición PAL (SCES-02104).**
Regla de seguridad: en voz y rótulos usar el nombre en inglés y, la primera vez, "(en España: X)" solo si se verificó en pantalla.

| Mundo / grupo (ES) | Nivel (EN) | Nombre en español (según WES) |
|---|---|---|
| Bosque de verano (Summer Forest) | Glimmer | Brillo |
| | Idol Springs | Balneario ídolos (WES lo escribe "Balnearío ídolos") |
| | Colossus | Coloso |
| | Hurricos | Hurricos |
| | Sunny Beach | Playa soleada |
| | Aquaria Towers | Torres acuario |
| | Ocean Speedway | Autopista del océano |
| | Crush's Dungeon | Mazmorra de Crush |
| Llanuras otoñales (Autumn Plains) | Skelos Badlands | Páramo Skelos |
| | Crystal Glacier | Glaciar cristal |
| | Breeze Harbor | Brisa |
| | Zephyr | Zephyr |
| | Scorch | Chamuscado |
| | Fracture Hills | Colinas fractura |
| | Magma Cone | Cono de magma |
| | Shady Oasis | Oasis frondoso |
| | Metro Speedway | Autopista metro |
| | Icy Speedway | Autopista helada |
| | Gulp's Overlook | Foso de Gulp |
| Tundra invernal (Winter Tundra) | Mystic Marsh | Pantano místico |
| | Cloud Temples | Templos nubes |
| | Robotica Farms | Granja robótica |
| | Metropolis | Metrópolis |
| | Canyon Speedway | Autopista del cañón |
| | Ripto's Arena | Ruedo de Ripto |
| Mundo extra | Dragon Shores | Tierras del Dragón |

Observaciones: "Hurricos" y "Zephyr" conservan el nombre inglés (SW:Zephyr dice que son los dos únicos mundos que lo mantienen en más de un idioma, DUDOSO). "Brisa" para Breeze Harbor y "Chamuscado" para Scorch son los más sospechosos de ser abreviaturas por espacio (verificar). La remasterización en español, según WES, usa otros nombres (p. ej. "Ruta oceánica", "Yermo esquelético", "Costa del dragón"): no son los de PS1.

Personajes (España): Spyro, Ripto, Elora, **Cazador** (Hunter; SW:Hunter + WES), **Profesor**, Zoe, **Ricachón** (Moneybags; solo WES), Crush y Gulp sin traducir (sin verificar). Sparx. Libros/objetos: "Guía" (Guidebook): sin verificar.

---------------------------------------------------------------------------------------------------
## E. SUGERENCIA DE SELECCIÓN (por si ayuda al guion; el equipo decide)

Los más sólidos **y** enseñables con clip de PS1 normal: #1 (Dan Johnson), #3 (katakana de Ripto), #6 (22475), #8 (Moneybags), #9 (Kenny/Electrolls), #12 (restos de nombres beta en diálogos, tras verificarlos en cuadro), #14 (la guerra de los bandos), #15 (epílogos y Faunus Mortas con 16/16), #31 (demo de CTR; disco NTSC-U), #32 (Big Head Mode), #36 (doble salto en Glimmer), #41 (Gear Grab), #42 (origen del hockey), #43 (kill/torch del yeti).
Fuertes pero solo con prototipo: #13 (Elora narra los niveles), #11 (nombres beta), #22 ("para noviembre"), #21 (9.991 gemas), #33 (códigos de depuración).
Pendientes de ver con ojos humanos antes de decidir: #2 (BRYAN/Brenda), #37 (sala secreta de Colossus), #7 ("The Hunter"), #16 (Macro Design).
Con tesis narrativa para el cierre: #35 (PSN de 2007 y la protección; presentarlo como teoría), A.8 (Reignited sin código fuente; Spyro: A Realm Beyond, primavera 2027, sin Copeland).

Fin del archivo.
