# Ideas guardadas (banco de ideas del usuario)

Ideas que el usuario dicta para producir más adelante. Al empezar un video de un canal, revisa aquí si hay alguna asignada a ese canal. Al producirla, marca la fila como ✅ con el alias del video.

| Fecha | Idea | Canal | Estado |
|---|---|---|---|
| 20-oct-2026 | El destino final de toda civilización: drenar su estrella para dormir en una simulación | **Kuriox** (`kuriox`), versión oscura | 💡 guardada · estilo por confirmar |
| 27-oct-2026 | **Pedidas en los comentarios** de «La niña que sigue esperando a su padre» (mismo formato de historia de misión): corcel temible de Xoroth, el héroe caído de la Horda, la Espada de Linken, la redención de Tirion (@silentsword2786 `Ugyz_Et1c5gL3OBTXv94AaABAg`, la que más quiere: Xoroth) · cadenas tétricas del Bosque del Ocaso (@nicomedi93 `UgzuVYsEUGvOPOa9PTB4AaABAg`) · el tauren paladín y sus becerritos (@cuco1399 `UgzBwIGbix0r1-rx7Td4AaABAg`) · el Jinete sin Cabeza y la familia Mograine (@zainzzgustavo `UgwJ8uvwTqUR0shT0uR4AaABAg`) · Morladim (@Vikussss `UgyzVXDx3mhBxlpONQ94AaABAg`) · Cerellean Zarpablanca y su misión (@DASagent `Ugyz-pgJV3l7Nev8pLl4AaABAg`, 28-oct). Enseñar el comentario de quien lo pidió (`yt comentario`) | **Crónicas de Warcraft** (`cronicas_warcraft`) | 💡 guardada |
| 28-oct-2026 | **Pedidas en los comentarios de Tamriel:** la lista de mods gráficos del canal (@Gamer-Legend-1G `UgxnAZ623RKI6iO_jlt4AaABAg`, 0 ♥) · Paarthurnax también es villano, lore de los dragones (@Knox8386 `UgzXyBrJs7uH5lwToEV4AaABAg`). Candidatos con datos (formula 28-oct): «Los 40 SECRETOS de Skyrim…» y «Las 10 builds más ROTAS» | **Crónicas de Tamriel** (`cronicas_tamriel`) | 💡 guardada |
| 26-oct-2026 | **Worlds 2026 de League of Legends: resumen de ~18 min** desde los primeros partidos (play-in, 15-oct) hasta hoy: las mejores jugadas analizadas y el panorama general (quién va, quién cayó, favoritos) | sin canal todavía (preguntar) · estilo **análisis táctico** (`docs/estilo_analisis_tactico.md`) | ▶ en producción desde el 27-oct-2026: `videos/lol_worlds_2026/` (22 min) |

---

## 26-oct-2026 · «Worlds 2026: todo lo que ha pasado» (título de trabajo)

**Lo que pidió el usuario:** un video de **18 minutos** que resuma todo lo que ha pasado en la Worlds desde sus primeros
juegos hasta ahora, viendo las mejores jugadas y cómo va el panorama en general. Se hace COMPLETO el 27-oct-2026.

**Formato:** el de la prueba `videos/lol_worlds_tl_al/` (aprobado como prueba el 26-oct): clips del VOD con pausas,
telestrador, mapa táctico 3D (`nucleo/mg_tactica.py`, ya optimizado: ~60 ms/cuadro). Para 18 min: render en tramos
paralelos (`video --tramo a-b`, ver el doc del estilo). Voz ElevenLabs con `FONETICA` de nombres en inglés («Liquid» → «Lícuid»).

**Arranque (datos a confirmar el mismo día, la fase suiza sigue):** play-in en Los Ángeles (15-18 oct, ganó Karmine Corp);
fase suiza en Allen, Texas (23-31 oct); a 26-oct: Gen.G y Dplus KIA 3-0 (en cuartos); Team Secret Whales y Anyone's Legend
eliminados 0-3 (la peor salida de un primer sembrado del LPL desde LGD en 2015); ronda 4 desde el 28-oct (KOI vs T1).
Cuartos 3-6 nov y semis 7-8 nov en Allen; final el 14-nov en el Barclays Center (Nueva York). Fuentes: Wikipedia
«2026 League of Legends World Championship», GosuGamers, Leaguepedia (402 por WebFetch), resúmenes de LoL Esports / OPLOLReplay /
Onivia en YouTube; VOD completos de EpicSkillshot (los resúmenes se saltan tramos).

**Estructura propuesta (a decidir con el usuario):** gancho (la jugada más loca) → el formato y los favoritos → play-in →
cada ronda suiza con 1-2 jugadas analizadas (telestrador) → las sorpresas (AL fuera, el LPL sin ganar el día 1) →
tablero de clasificación animado → quién llega a cuartos y qué viene → pregunta a la audiencia.

---

## 20-oct-2026 · «El último sueño de la humanidad» (título de trabajo)

**Tono:** oscuro, inquietante, especulativo («¿y si…?»).

**La idea del usuario (tal cual la planteó):** la humanidad cree que su destino es explorar el espacio, pero tal vez el objetivo para el que está «hecho» un sistema solar con vida es otro: aprovechar su propia estrella como combustible, con una esfera de Dyson, y drenar toda su energía para convertirla en alimento directo para la humanidad y en la energía que mantiene una simulación donde todos dormimos viviendo los sueños y las vidas que siempre quisimos. Ese sería el final de **cualquier** civilización: encerrar su estrella y entrar en el mundo simulado.

**El giro que lo hace oscuro:** eso explicaría por qué no vemos a nadie allá afuera (paradoja de Fermi): no se extinguieron ni se fueron; se encerraron a soñar. Y cuando la estrella se agote, el sueño se apaga con ella.

**Ciencia y conceptos reales en los que se apoya** (verificar fuentes al escribir el guion; DOI con Crossref):
- Esfera / enjambre de Dyson (Freeman Dyson, 1960, *Science*).
- Escala de Kardashev (1964): civilización tipo II = usa toda la energía de su estrella.
- Cerebro Matrioshka (Robert Bradbury): capas de computación alrededor de una estrella.
- Argumento de la simulación (Nick Bostrom, 2003).
- Hipótesis de la transcensión (John Smart, 2012): las civilizaciones avanzadas se van «hacia adentro», no hacia afuera.
- Hipótesis de la estivación (Sandberg, Armstrong y Ćirković, 2017): civilizaciones que «duermen» esperando un universo más frío para computar mejor.
- Estrella de Tabby (KIC 8462852): la vez que se especuló con una megaestructura (al final, polvo).

**Posible estructura:** 1) el sueño de las estrellas (cohetes, Marte, colonias) → 2) el silencio del universo → 3) la alternativa: no salir, encerrar la estrella → 4) la simulación perfecta: cada quien su vida soñada → 5) la conclusión inquietante: quizá ya estamos dentro… y quizá nuestro Sol ya está siendo drenado.

**Canal (el usuario, 20-oct-2026): Kuriox**, con el estilo del canal (mascota Kuri, muy dinámico) pero en su **lado oscuro**.
**Estilo: POR CONFIRMAR.** El usuario quiere usar el estilo híbrido nuevo, Kuriox + secuencias de Flow, el mismo de `videos/asteroide_invisible/` («El asteroide que no vimos venir»). Lo confirmará cuando vea la vista previa de ese video: **no empezar la producción hasta que lo apruebe.** Si no lo aprueba, la otra opción es el Kurzgesagt por código del canal (`sol_apagado_8min/`).
Antes de producir: `python fab.py ideas kuriox`, `canales/formula/kuriox.md` y las lecciones de `asteroide_invisible/ESTADO.md`.
