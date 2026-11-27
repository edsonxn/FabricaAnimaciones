# Investigación: «15 FARMEOS de ORO del 30 al 50 en WoW Forever»

Hecha el **25-nov-2026** (21 días después del lanzamiento de WoW Forever, 4-nov-2026). Canal: Crónicas de Warcraft. ~28 min, cuenta regresiva 15 → 1, sale el **4-dic-2026**. Patrocinador: Overgear.
Video de **LUGARES CONCRETOS** (qué matar o recoger, dónde, a qué nivel, cuánto rinde y a quién venderlo), no de trucos de subasta. No repite los puestos del video anterior «30 trucos de ORO» ([ORO]) salvo uno marcado **YA USADO + novedad**.

## Cómo leer la confianza
- **OFICIAL** = notas de hotfix de Blizzard (página única que Blizzard amplía; leída hoy, ya titulada «November 25, 2026»).
- **DATOS** = datos del cliente de Forever leídos hoy en Wowhead Forever: tooltips de PNJ (nivel, tipo y **puntos de aparición en % de la zona**), tooltips de objetos (ícono, **precio de vendedor**, carga máxima), tooltips de misiones, y el mapa mundial (rótulos de subzona, nodos de recolección y pesca, vendedores). Nombres es-MX del mismo sitio (`locale=11` y mapa `/forever/mx/`).
- **GUÍAS** = guías escritas para Forever (Conquest Capped, actualizada hoy con escaneo EU del 15-nov).
- **JUGADORES** = creadores de YouTube o foros jugando en el cliente en vivo (cifra de una persona, un servidor, un día).
- **CLÁSICO-sin confirmar** = vale en Classic; ninguna fuente de Forever lo confirma.
- Muchas cifras de oro por hora son de **una sola prueba de 30-60 min** en un servidor: decirlas como «a un jugador le salieron…» y con fecha. Los precios de subasta cambian por servidor y por día.

## Método (para repetirlo)
- **Transcripciones:** la herramienta de Nexlev devolvió «límite semanal agotado (50/50)», así que los subtítulos de YouTube se leyeron con `yt-dlp --write-auto-subs --skip-download` (solo texto) y la fecha exacta de subida con `%(upload_date)s`. 26 videos revisados; 22 leídos completos.
- **Ids, íconos y precios de vendedor:** `https://www.wowhead.com/forever/search/suggestions-template?q=<nombre>` → id; `https://nether.wowhead.com/forever/tooltip/<item|npc|quest>/<id>?locale=0` (inglés, ícono, «Sell Price») y `?locale=11` (es-MX). Si Forever no trae el nombre traducido (sale entre corchetes), se probó `nether.wowhead.com/classic/tooltip/...?locale=11` y se marca «(es-MX de Wowhead Classic)».
- **Coordenadas de criaturas:** el tooltip de PNJ de Wowhead Forever trae el campo `map` con todos los puntos de aparición ya en % de la zona. Se da el **centro de la casilla de 5 % con más puntos** (n = puntos en esa casilla) y el total de puntos. **Rótulos de subzona, vetas y bancos de peces:** mapa mundial `nether.wowhead.com/forever/data/world-map`, convertidos con el rectángulo de la zona (mismo método que [RUTA]; error ±0.5).
- **Comprobaciones cruzadas:** los coyotes de Claros del Río (tooltip, 54.5, 86.9 y 54.4, 67.6) caen **al sur del Cortijo de Wheeler** (rótulo 54.8, 75.8), justo donde los dibujan Studen y Solheim. El raro Lo'Grosh (tooltip, 52.7, 47.3) cae en la **misma casilla** que la mayor concentración de vetas de Alterac según el mapa (52.8, 47.1, 38 vetas). La Cazadora llanagreste (58.7, 52.8) cae «justo debajo de Rog'mar» (rótulo 59.6, 45.9), como dice Studen.

## Nombres en español (comprobados hoy)
- **Zonas y subzonas (mapa es-MX de Wowhead Forever):** Tierras Inhóspitas (Badlands), Las Tierras Devastadas (Blasted Lands), Pantano de las Penas, Marjal Revolcafango, Las Mil Agujas, **El Desierto de Sal** (The Shimmering Flats), **Claros del Río** (Riverglades), Montañas de Alterac, Desolace, Vega de Tuercespina, Tanaris, Feralas, Tierras Altas de Arathi, Tierras del Interior. Subzonas: **Dominios de los Aplastacresta** (Crushridge Hold), **Barranco Lethlor**, Kargath, Excavación de Piemartillo, Explanada del Espejismo, Fortaleza de Angor, Valle de los Colmillos, **Cortijo de Wheeler**, **Puerto Polvomecha** (Powderfuse Port), Rog'mar, Avanzada de Terral, **Rocal** (Stonard), Cueva Stagalbog, Puesto Juncobruma, Tinieblas de las Penas, **Cueva Niebla Negra** (Darkmist Cavern), Poblado Murohelecho, Isla Theramore, **Poblado Magram**, Aldea Cazasombras, **Arenas Abisales**, Gadgetzan, Los Dos Colosos, Campamento Mojache, Bastión Plumaluna, Castillo de Nethergarde, Serpiente Enroscada, Alto de los Rapiñadores, Puesto Machacamiedo, Campamento Grom'Gol, Bahía del Botín, Valle del Velo de Bruma, Lago Nazferiti, Cráter de la Comadreja, Circuito del Espejismo, Sentencia (Hammerfall), Refugio de la Zaga (Refuge Pointe), Cañón Mostacho Seco.
- **Criaturas y objetos:** en cada ficha, con id. Destacan: **Destripador negro** (Black Slayer), **Molleja de buitre**, **Ogro / Tosco Aplastacresta**, **Valija reforzada con mitril** (Mithril Bound Trunk), **Elemental de roca inferior / superior**, **Coyote de las llanuras**, **Merodeador coyote**, **Cazadora llanagreste**, **Jaguar del pantano**, **Cola blanda larga**, **Bigote de cerdas**, **Cola tupida suave**, **Melena espesa**, **Tronador Groddoc**, **Patriarca Cueracero**, **Hiena Llagapata**, **Múrloc de marisma**, **Almeja de boca grande**, **Reptador de arena**, **Carne de cangrejo tierna**, **Glándula de llamas pequeña**, **Vástago oscuro**, **Mordedor brillavalva**, **Fragmento de caparazón moteado**, **Gorila Velo de Bruma**, **Colmillo de gorila**, **Araña / Ermitaña Niebla Negra**, **Seda de araña espesa**, **Retador / Cazavientos Magram**, **Expositor de pesca** (Fishing Rack), **Ají aliento de dragón** (ojo: en [ORO] pusimos «Chile aliento de dragón»; manda Wowhead mx).
- **Sin nombre es-MX en Wowhead (decir en inglés o describirlo):** Scalding Whelp (la cría de Tierras Inhóspitas), Sootfur (el coyote raro de Claros del Río), las misiones «Coyote Huntin'», «Rescue Roundup» y «A Feast for Buzzards», Luremaster (talento de Legado).

## Fuentes (claves usadas en las fichas)
- **[OFI-HF]** Blizzard, «WoW: Forever Hotfixes» (del 5 al **25-nov**), leída hoy: https://worldofwarcraft.blizzard.com/en-gb/news/24315281/
- **[CC-FARM]** Conquest Capped, «WoW Forever Gold Farming» (**actualizada el 25-nov**; tabla de valor por muerte con **escaneo de subasta EU del 15-nov**): https://conquestcapped.com/guides/wow-forever/wow-forever-gold-farming/
- **[WHF-NPC] / [WHF-TT] / [WHF-Q]** Wowhead Forever, tooltips de PNJ / objeto / misión (ver Método), leídos hoy: `https://nether.wowhead.com/forever/tooltip/npc/<id>` · `.../item/<id>` · `.../quest/<id>`; página: `https://www.wowhead.com/forever/npc=<id>` · `.../item=<id>`.
- **[WHF-MAP]** Wowhead Forever, mapa mundial (datos `https://nether.wowhead.com/forever/data/world-map` y `.../forever/mx/data/world-map`), leído hoy.
- **YouTube (transcripción leída completa; fecha = día de subida exacto; vistas al 25-nov):**
  - **[HASTE]** Haste, «I Made 20g in 30 Minutes With This WoW Forever Gold Farm» (**23-nov**, 17,6 k) — https://www.youtube.com/watch?v=5Pq0vfd4M84
  - **[RAGE21]** RageGaming, «This OP Gold Farm is Better Than Ever - 50 Gold An Hour While Leveling» (**21-nov**, 168 k) — https://www.youtube.com/watch?v=i5mudUrqOks
  - **[ZEZ]** zezsigaming, «WoW Forever Gold Farms ACTUALLY Tested» (**20-nov**, 34 k) — https://www.youtube.com/watch?v=DUmEhAy-e2Y
  - **[SOL]** Solheim Gaming, «Get Your Level 40 Mount EASY in WoW Forever With These Goldfarms!» (**20-nov**, 26 k) — https://www.youtube.com/watch?v=JGG5LBZzAWg
  - **[STUR]** SturnusGaming, «Insane Level 40+ Raw Gold Farm in WoW Forever!» (20-nov, 8,5 k) — https://www.youtube.com/watch?v=5BzoO8JZnFo
  - **[MMOU]** MMO Unlocked, «This Level 40 Murloc Farm Drops INSANE Gold & Epics!» (**22-nov**, 28 k) — https://www.youtube.com/watch?v=uXfShCrgYBU
  - **[STU5]** Studen Albatroz, «Top 5 Goldfarms For lvl 40 Mount In WoW Forever» (**18-nov**, 71 k) — https://www.youtube.com/watch?v=LcqaK7fZSCg
  - **[STU-HY]** Studen Albatroz, «WoW Forever INSANE Steady Goldfarm!» (**23-nov**, 67 k; hienas y rocs de Tanaris) — https://www.youtube.com/watch?v=WXVN4WqJlj0
  - **[STU-FER]** Studen Albatroz, «WoW Forever AMAZING Raw Gold Farm!» (**19-nov**, 24 k; Feralas) — https://www.youtube.com/watch?v=mcZZ2kihk0A
  - **[STU-WH]** Studen Albatroz, «WoW Forever INSANE Gold & XP Grind» (9-nov, 48 k; crías de Tierras Inhóspitas) — https://www.youtube.com/watch?v=ZZs52VIR1-k
  - **[STU-40]** Studen Albatroz, «Goldfarm lvl 40 Mount! RAW GOLD» (8-nov, 41 k) — https://www.youtube.com/watch?v=kZnOXnZvqhM
  - **[NOHIT]** NOHITJEROME, «This Turns Leveling Into a GOLD FARM in WoW Forever» (15-nov, 187 k) — https://www.youtube.com/watch?v=rQuvT137PLo
  - **[KARG]** Kargoz, «Don't Hit Level 40 BROKE! 5 BEST Gold Farms in WoW Forever» (12-nov, 248 k) — https://www.youtube.com/watch?v=LStkmcnFTCg
  - **[CYN]** Cynara, «NEW Gold Farms (WoW Forever)» (12-nov, 85 k) — https://www.youtube.com/watch?v=G3VrXE5Zsu8
  - **[FROST40]** Frostadamus, «How I Made 100 Gold FAST for Mount at Level 40» (11-nov, 111 k) — https://www.youtube.com/watch?v=ANA932N3edk
  - **[KHY]** Khylen WoW, «Consigue tu Montura con estos Farmeos de ORO! WoW Forever» (14-nov, 35 k, **en español**) — https://www.youtube.com/watch?v=rxlcQoz2Dsk
  - **[SERL]** SerllinoGG, «30 de ORO por HORA, Como farmear ORO en WoW Forever» (13-nov, 18 k, **en español**) — https://www.youtube.com/watch?v=KNxjGp2yMAs
  - **[NOKZU]** Nokzu, «Cómo ganar ORO siendo nivel bajo | WoW Forever» (9-nov, 7 k, **en español**) — https://www.youtube.com/watch?v=PvYaSHdRxxE — trata de niveles 1-20 (bolsas de componentes de lino y de lana, Liquen con volantes → Tinte cerúleo); no aporta lugares del 30 al 50.
  - **Descartados tras leerlos:** TheAllianceFootman «THE BEST Early-Game Gold Farm» (https://youtu.be/iA6y8mF5mzg) y «This WoW Forever Gold Farm CANNOT Be Nerfed» (https://youtu.be/WkLT1B8ZfH8): **son Shorts de 67 y 91 s subidos el 6 y el 14-oct, en la BETA**, de nivel 8 (trolls Escarcha de Dun Morogh, receta que se vende a ~20 s; ~3 g en 30 min) y nivel 15 (isla de reptiles de Loch Modan, ~9 g en 1 h con desuello). Fuera de rango y con insultos en la voz: no usar. Corealis (24-nov, https://www.youtube.com/watch?v=LEkgX7Wpjdg), Studen «Hyperspawn» (25-nov, https://www.youtube.com/watch?v=paQ1yIrQMns) y «Raw Goldfarm» (24-nov, https://www.youtube.com/watch?v=JROZhiA6ReY): niveles 55-60 (Frondavil, Silithus, Hyjal, Un'Goro). Grindilow (17-nov, https://www.youtube.com/watch?v=4L6fEX8cXPE): un farmeo de mazmorra al 60 ya parcheado; no usar. CaptnCanes «Maraudon Solo Farm: Prot Paladin! 20-40 Gold Per Hour» (25-nov, https://www.youtube.com/watch?v=WSrfInDlUCs): de una clase concreta y con Zabibas diciendo el mismo día lo contrario (https://www.youtube.com/watch?v=5kqmV1F4h-0): fuera.
- **Foros de Blizzard (US):** [F-GOLD] «The Gold Issue in Forever» (21-nov, 460+ respuestas) https://us.forums.blizzard.com/en/wow/t/the-gold-issue-in-forever/2424791 · [F-APPR] «So what is the Blizzard-approved method of farming gold?» (22-nov) https://us.forums.blizzard.com/en/wow/t/so-what-is-the-blizzard-approved-method-of-farming-gold/2425675 · [F-STOP] «Are we really trying to stop all gold farms?» (22-nov) https://us.forums.blizzard.com/en/wow/t/are-we-really-trying-to-stop-all-gold-farms/2426162 · [F-TOPIC] «On the topic of farming gold» (23-nov) https://us.forums.blizzard.com/en/wow/t/on-the-topic-of-farming-gold/2426615
- **Reddit:** la búsqueda de r/wowforever devolvió una página de bloqueo (sin JSON); no hay citas de Reddit nuevas.
- **Ya investigado en el canal:** [ORO] `_investigacion_wow_oro_forever.md` (15-nov; los 30 trucos) · [PROF] `_investigacion_wow_ruta_profesiones.md` (método de datos de Wowhead) · [RUTA] `_investigacion_wow_ruta_forever.md` (conversión del mapa).

---

## AVISO PARA EL GUION
- **Patrocinador (Overgear):** siempre «WoW Forever» (varias fuentes dicen «Classic»: no copiarlo); Forever **no** es temporada; nada contra comprar oro, boosts ni servicios; nada de «mejor clase», «la clase que más farmea», tier lists (varios videos dicen «con mago o paladín de área es mejor»: no repetirlo; decir «cualquier clase puede, unas matan más rápido que otras»); nada de «sáltate el grind».
- **Nada de exploits ni de baneos.** Contexto que NO va en la voz: el 17-nov estalló en los foros el farmeo de «Blackmaw Hold» (botín mal puesto en una mazmorra, corregido por Blizzard, con quejas de baneos); el 20-nov Blizzard bajó a **5 entradas por hora** el tope de mazmorras (antes 10) [OFI-HF] y el 23-nov cambió el botín del Centinela de obsidiana de Uldaman [OFI-HF]; jugadores dicen que los farmeos de Zul'Farrak, La Masacre Este y Uldaman «están muertos» [F-TOPIC]. **Lo que sí puede decir la voz:** «las mazmorras ahora tienen tope de cinco por hora, así que el oro del 30 al 50 está en el mundo abierto». Por eso el video es 100 % de mundo abierto.
- **Tampoco** se recomienda el add-on de «cambio de capa» (layer swap): RageGaming lo usa y dice que lo desactivarán en una semana; Corealis dice que Blizzard restringirá esa parte de la API. No lo nombramos.
- **No citar fuentes en la voz.** Las cifras de jugadores: «a un jugador le salieron…», con la fecha.
- **Ya contado en [ORO] (no repetir como «nuevo»):** talismanes de Arathi (#12), perlas azules (#11), huevos gigantes (#10), grises de Feralas Frayfeather / Trabalomas / basiliscos de Desolace (#9), tortugas de Tanaris (#8, Planeadores de oleaje), pesca con Adornos brillantes y restos flotantes (#4), sátiros (#3), torio/Cristal Arcano (#2), misiones 48+ (#1), trampas de marisco de Desolace (#14). En este video, los rocs y huevos aparecen solo como **complemento** de las hienas (#8) y la pesca entra **una vez** como «YA USADO + novedad» (#3).

## VERIFICACIONES

### Hotfixes posteriores al 15-nov que tocan el oro del 30 al 50 [OFI-HF]
- **25-nov:** Desolace, los centauros del Poblado Magram ahora reaparecen más rápido → base del #15. Además: los paladines y brujos reciben la Equitación de oficial gratis con sus misiones de montura épica (no afecta al rango 30-50).
- **23-nov:** Uldaman, el Centinela de obsidiana vuelve a soltar el botín «previsto» (cierra un farmeo de mazmorra; no se nombra). Las recetas de almeja (Almejas hervidas, Sopa de almejas…) pasan a la categoría de comida de aguante: la **Carne de almeja sabrosa** de los múrlocs (#9) sigue teniendo uso.
- **20-nov:** cada mazmorra se puede reiniciar y entrar como máximo **5 veces por hora** (antes 10).
- **19-nov:** Claros del Río, arreglan que el raro Mosh'gra nunca soltara botín raro (Mosh'gra, npc 259801, nivel 41, raro, 62.2, 36.0 [WHF-NPC]). Arreglos de Cultivo del tauren (hierbas).
- **17-nov:** los desolladores ya no pueden desollar «algunas criaturas» que normalmente no se desuellan (sin lista; ninguno de nuestros 15 farmeos depende de eso). Hierro espectral más abundante (Shen'dralas, nivel 50+).
- **16-nov:** el **Expositor de pesca** (Fishing Rack, objeto de campamento, Pesca 140) ahora da señuelos a todos, y los peces especiales que saca tienen más probabilidad y botín ajustado → novedad para el #3. Sube la probabilidad de los «Blood Red Bandanas» (misión).
- **Anteriores, pero nunca usados en el canal:** **13-nov** Tierras Inhóspitas, los **Elementales de roca inferiores aparecen más seguido** (base del #5), y en Tuercespina aparecen más seguido los tigres, panteras y raptores.
- **No hay** ningún hotfix que baje el precio de vendedor de los grises que farmeamos ni que cambie el botín de nuestras 15 criaturas.

### Lo que cuesta llegar al 40 (contexto del gancho)
- Equitación de aprendiz **100 g** (90 con Honorable) + doble especialización **50 g** = **140 g con descuento** [NOHIT 4:00; ORO]. Khylen dice «100 de equitación y 20 la montura» [KHY 0:20]: la contradicción de [ORO] (¿montura incluida?) sigue abierta. Kargoz: «unos 90 de oro» [KARG 15:07].
- Un jugador del foro (21-nov) recuerda que en el Vanilla original se llegaba al 40 con 40-60 g y que Forever añadió los 50 g de la doble especialización sin subir los ingresos [F-GOLD].
- Sin farmear: zezsigaming midió **~3 g/h** solo con misiones y desuello (7 g contando recompensas y verdes) en Claros del Río al 39-40 [ZEZ 2:43].

### Los videos que pidió el encargo
- **TheAllianceFootman:** son Shorts de la beta (ver Fuentes); no entran.
- **RageGaming «The BIG Secret to Easy Fast Gold Early»** ya es [RAGE] de [ORO]. Su video NUEVO del 21-nov [RAGE21] es la novedad del #3.
- **Khylen** (español): leído completo; apoya el #2 (cuevas de ogros de Alterac con minería), el #6 (jaguares del Pantano de las Penas) y aporta zonas de reserva (cocodrilos de Desolace y de una cueva de Tuercespina, tortugas del río de Trabalomas y de la costa de Dalaran).
- **Nokzu** (español): niveles bajos; nada del 30 al 50.
- **Frostadamus:** su video del 11-nov [FROST40] es el #2. **GrayMaine:** no tiene video nuevo de oro después del 14-nov (el «7 Farms» ya está en [ORO]).

---

## LOS 28 CANDIDATOS → elegidos 15
| # | Candidato | Zona (nivel) | Cifra | Estado |
|---|---|---|---|---|
| A | Destripadores negros → Molleja de buitre | Las Tierras Devastadas (46-48) | ~41 g/h (30 min medidos, 23-nov) | **#1** |
| B | Cuevas de ogros Aplastacresta + minería | Montañas de Alterac (34-38) | ~30 g/h con montura; 20-25 sin ella | **#2** |
| C | Pesca de Valijas reforzadas con mitril | Vega de Tuercespina (25+, Pesca 150) | 170 g en 3 h 30 (21-nov) | **#3 YA USADO + novedad** |
| D | Coyotes de Claros del Río | Claros del Río (36-40) | 13-14 g/h (20-nov) | **#4** |
| E | Elementales de roca | Tierras Inhóspitas (37-44) | ~10 g/h + Tierra elemental | **#5** |
| F | Jaguares del pantano (+ Cazadora llanagreste) | Pantano de las Penas (36-37) / Claros del Río (38-39) | +10 g/h (huntress) | **#6** |
| G | Gorilas Groddoc y osos Cueracero | Feralas norte (48-50) | grises de 5-15 s | **#7** |
| H | Hienas Llagapata (+ rocs) | Tanaris, Arenas Abisales (41-45) | grises 8-9 s; huevo ~20 s | **#8** |
| I | Múrlocs de marisma (almejas y perlas) | Pantano de las Penas (41-45) | Perla de oro ~1 g 30 s (22-nov) | **#9** |
| J | Crías de Tierras Inhóspitas (Scalding Whelp) | Barranco Lethlor (41-43) | ~30 000 XP/h + Glándulas | **#10** |
| K | Reptadores de arena → Carne de cangrejo tierna | Claros del Río (36-37) / Tuercespina sur (40-41) | 14 s c/u, 40 % (12-nov) | **#11** |
| L | Tortugas brillavalva | El Desierto de Sal (30-35) | ~4 s por muerte (15-nov) | **#12** |
| M | Gorilas Velo de Bruma → Colmillo de gorila | Tuercespina (32-41) | 5-6 g/h (12-nov) | **#13** |
| N | Arañas Niebla Negra (seda) | Marjal Revolcafango (35-37) | sin g/h; grises 5-6 s | **#14** |
| O | Centauros Magram (reaparecen más rápido) | Desolace (32-38) | sin cifra; hotfix de HOY | **#15** |
| P | Búhos de Tierras del Interior (huevos) | Tierras del Interior (42-47) | **~6 g/h** el 20-nov (era ~13) [ZEZ] | reserva: «lo que todos farmean se hunde» |
| Q | Elementales de Arathi (talismanes + Aire elemental) | Tierras Altas de Arathi (38-39) | ~12,6 g/h (20-nov) [ZEZ] | YA USADO (#12 de [ORO]) |
| R | Vórtice espiral → Aire elemental 13 % | Las Mil Agujas (33-34) | ~3 s por muerte (15-nov) [CC-FARM] | reserva |
| S | Kóbolds Mostacho Seco → Mena de sangrita inferior | Arathi, Cañón Mostacho Seco (35-38) | vendedor 25 c; 10 vetas | reserva (sin precio de subasta) |
| T | Coyotes y pumas de Excavación de Piemartillo | Tierras Inhóspitas (35-39) | 40 g del 38 al 40 [SOL] | reserva (misma zona que #5) |
| U | Basiliscos al norte del Arrecife Vil | Tuercespina (33+) | sin cifra [SOL] | reserva |
| V | Tortugas Fangorroca | Marjal Revolcafango (42-43) | ~6 s por muerte [CC-FARM] | reserva (alternativa del #12) |
| W | Aullador Dientelargo → Carne de lobo tierna 37 % | Feralas (43-44) | ~6 s por muerte [CC-FARM] | reserva |
| X | Déspota Machacaduna → Paño de tejido mágico 73 % | Tanaris (46-47) | ~4 s por muerte [CC-FARM] | reserva |
| Y | Raptores Cienorrojo → Piel de raptor lisa | Marjal Revolcafango (35-36) | gris 7 s 13 c [SERL] | reserva |
| Z | Mordedores Mandíbula de acero (tortugas) | Tanaris norte (42-45) | ~7 s por muerte [CC-FARM; STUR] | descartado (= tortugas de Tanaris de [ORO]) |
| AA | Alga estranguladora / Musgo de tumba | varias | Musgo de tumba 3 s 38 c (EU 15-nov) | reserva (recolección barata) |
| AB | Trampas de marisco de Aldea Cazasombras → pez de 2,5 g (Horda) | Desolace | 2,5 g (12-nov) [CYN] | YA USADO el lugar (#14 de [ORO]); dato anterior al 15-nov |
| — | Fuera de rango o descartados | — | — | Frostmane/Loch Modan (beta, nivel 8-15), Vul'Gol de Bosque del Ocaso (24-26), sátiros, Pellejo vil de Hyjal, raptores de Un'Goro, Silithus; farmeos de mazmorra (cerrados o de una clase) |

---

## LOS 15 FARMEOS (cuenta regresiva 15 → 1)

### 15. Centauros Magram: Blizzard los acaba de acelerar (Desolace)
- **Qué es en Forever:** el Poblado Magram es un campamento grande de centauros humanoides (monedas y tela). **Hoy, 25-nov, Blizzard publicó que sus centauros ahora reaparecen más rápido** [OFI-HF]: más centauros por hora para quien hace sus misiones o se queda farmeando. No hay prueba de oro por hora todavía.
- **Nivel recomendado:** 33-38 (los centauros son 32-35; las hienas Zarpósea 37-38).
- **Cuánto da:** **sin cifra de Forever**. Lo que se sabe: humanoides de nivel 32-35 → monedas y tela (paño de seda; el tejido mágico empieza alrededor del 35). La tabla de botín no se pudo comprobar (las páginas de Wowhead dan 403; el tooltip no trae botín). Paño de seda: vendedor **1 s 50 c** [WHF-TT].
- **Lugar (coordenadas):** Desolace, **Poblado Magram** (rótulo 70.8, 76.8 [WHF-MAP]). Puntos de aparición [WHF-NPC]: Retador Magram 67.8, 73.1 (n=17 de 72) · Cazavientos Magram 67.6, 72.5 (n=22 de 78) · Corremanadas Magram 67.2, 76.2 · Avanzado Magram 67.5, 72.3 · Explorador Magram 67.3, 72.4. Segundo grupo en 71-72, 67-68 y tercero en 72, 76.7.
- **Qué se farmea:** Paño de seda · `forever/4306` · ícono `inv_fabric_silk_01` · vendedor 1 s 50 c. Paño de tejido mágico · `forever/4338` · `inv_fabric_mageweave_01` · vendedor 2 s 50 c (probable a este nivel, sin tabla comprobada).
- **Criaturas (npc):** Retador Magram / Magram Wrangler `npc 4640` (33-34) · Cazavientos Magram / Magram Windchaser `npc 4641` (33-34) · Corremanadas Magram / Magram Pack Runner `npc 4643` (34-35) · Avanzado Magram / Magram Outrunner `npc 4639` (32-33) · Explorador Magram / Magram Scout `npc 4638` (32-33) · Zarpósea Magram / Magram Bonepaw `npc 4662` (37-38, hiena).
- **En pantalla:** centauros reapareciendo en el Poblado Magram; nota del hotfix del 25-nov; Paño de seda. YouTube: «Magram Village Desolace» / «Desolace centaur grind».
- **Fuentes:** [OFI-HF] 25-nov · [WHF-NPC] · [WHF-TT] · [WHF-MAP]
- **Confianza:** OFICIAL (reaparición) · DATOS (lugar, ids) · CLÁSICO-sin confirmar (botín).

### 14. Arañas Niebla Negra: seda que piden los sastres (Marjal Revolcafango)
- **Qué es en Forever:** arañas débiles y muy juntas fuera y dentro de la Cueva Niebla Negra, al lado de los múrlocs del norte del marjal. Sueltan dos grises que se apilan y **dos sedas de fabricación**: Seda de araña espesa y Seda de las Sombras (esta última va en piezas de sastrería con daño de Sombras). Hay un raro dentro de la cueva que suelta un verde ligado al equiparse. Vendedor de la Horda al lado (Poblado Murohelecho) [KARG 12:58-14:23].
- **Nivel recomendado:** 35-38.
- **Cuánto da:** sin oro por hora medido. Precios de vendedor [WHF-TT]: Mandíbula de araña chorreando **5 s 83 c**, Punta de pata de araña dura **4 s 91 c**, Seda de araña espesa **7 s 50 c**, Seda de las Sombras **10 s**. Kargoz: «muy valiosos» y los sastres los usan para subir [KARG].
- **Lugar (coordenadas):** Marjal Revolcafango, **Cueva Niebla Negra** (rótulo 33.3, 22.8 [WHF-MAP]). Arañas [WHF-NPC]: Araña Niebla Negra 34.0, 21.8 (n=10 de 21) y 35.4, 22.3; Ermitaña Niebla Negra 34.0, 21.8 (n=9 de 19). Vendedores: Poblado Murohelecho (rótulo 36.3, 31.4) para la Horda; Isla Theramore (65.0, 47.1) para la Alianza.
- **Qué se farmea:** Mandíbula de araña chorreando · `forever/4585` · `inv_misc_monsterspidercarapace_01` · 5 s 83 c · Punta de pata de araña dura · `forever/1074` · `inv_misc_monsterspidercarapace_01` · 4 s 91 c · Seda de araña espesa · `forever/4337` · `spell_nature_web` · 7 s 50 c · Seda de las Sombras · `forever/10285` · `spell_nature_web` · 10 s.
- **Criaturas (npc):** Araña Niebla Negra / Darkmist Spider `npc 4376` (35-36) · Ermitaña Niebla Negra / Darkmist Recluse `npc 4378` (36-37). Pocas apariciones en total (40): con competencia, entrar a la cueva.
- **En pantalla:** entrada de la cueva; arañas en grupo; las dos sedas. YouTube: «Darkmist Cavern spiders» / «Dustwallow spider farm».
- **Fuentes:** [KARG] · [WHF-NPC] · [WHF-TT] · [WHF-MAP]
- **Confianza:** JUGADORES (valor) · DATOS (lugar, precios de vendedor, ids).

### 13. Gorilas Velo de Bruma: los colmillos que nadie quiere farmear (Vega de Tuercespina)
- **Qué es en Forever:** los gorilas del norte de Tuercespina **no tienen misión de matar ni para la Alianza ni para la Horda**, así que están casi siempre vivos y sin competencia. Sueltan pelo de gorila (gris para el vendedor) y **Colmillo de gorila**, que se vende en la subasta porque lo usa la misión «La fiebre de Tuercespina» (invocar a Mokk el Salvaje en oleadas): quien la intenta solo suele fallar y compra los colmillos otra vez [CYN 1:42-2:43].
- **Nivel recomendado:** 32-35 (norte) o 40-41 (los ancianos del sur).
- **Cuánto da:** **5-6 g/h** a precios del 12-nov solo matando gorilas [CYN 2:43]. Colmillo de gorila: vendedor 67 c [WHF-TT] (el valor está en la subasta; sin precio citado).
- **Lugar (coordenadas):** Gorila Velo de Bruma: **37.7, 17.1** (13 de sus 14 apariciones; al oeste del Lago Nazferiti, rótulo 40.8, 16.0) [WHF-NPC]. Gorila Velo de Bruma anciano: **32.5, 66.8** y 33.1, 62.3 (Valle del Velo de Bruma, rótulo 33.0, 66.2). Misión: Médico brujo Unbagwa 35.2, 60.5 → Fin Fizqueta 27.6, 76.8 (Bahía del Botín) [WHF-NPC].
- **Qué se farmea:** Colmillo de gorila · `forever/2799` · `inv_misc_monsterfang_01` · vendedor 67 c · carga 20. Pelo de gorila burdo · `forever/4096` · `inv_misc_monstertail_03` · 6 s 8 c (no comprobé cuál de los dos pelos sueltan estos gorilas).
- **Criaturas (npc):** Gorila Velo de Bruma / Mistvale Gorilla `npc 1108` (32-33) · Gorila Velo de Bruma anciano / Elder Mistvale Gorilla `npc 1557` (40-41). Misión «La fiebre de Tuercespina» / Stranglethorn Fever `quest 348`; Médico brujo Unbagwa `npc 1449`; Fin Fizqueta `npc 2486`.
- **En pantalla:** gorilas en la selva; Colmillo de gorila; Mokk el Salvaje en la misión. YouTube: «Stranglethorn gorilla farm» / «Mistvale Valley gorillas».
- **Fuentes:** [CYN] · [WHF-NPC] · [WHF-TT] · [WHF-Q]
- **Confianza:** JUGADORES (cifra, uso del colmillo) · DATOS (lugar, ids). Ojo: solo 14 apariciones de los del norte: rinde si estás solo.

### 12. Tortugas brillavalva del Desierto de Sal: el gris de 9 platas
- **Qué es en Forever:** tortugas lentas que no pegan fuerte. Sueltan el **Fragmento de caparazón moteado** (gris que se apila de 5 y el vendedor paga 9 s) en **alrededor de un tercio** de las muertes, más Carne de tortuga y cola escamosa. NOHITJEROME: «unas cuantas tardes de tortugas» y tienes la montura [NOHIT 7:06, 9:09]. Es **otra zona y otro nivel** que las tortugas de Tanaris del #8 de [ORO].
- **Nivel recomendado:** 30-36.
- **Cuánto da:** Conquest Capped: **4 s 5 c por muerte** del Mordedor brillavalva (escaneo EU del 15-nov; Carne de tortuga 32 %, Fragmento 32 %, Cola escamosa espesa 33 %) → a ~100 muertes por hora, ~4 g de botín más monedas [CC-FARM]. La Carne de tortuga se compra para una misión de cocina de Laderas de Trabalomas: ~5 s c/u en la subasta según Cynara (12-nov) [CYN 3:24].
- **Lugar (coordenadas):** Las Mil Agujas, **El Desierto de Sal** (rótulo 70.8, 76.7). Mordedor brillavalva **82.7, 56.2** (n=11 de 64) y 86.7, 61.3; Tortuga brillavalva 73.2, 57.3 (n=15 de 71) y 71.3, 67.5 [WHF-NPC]: al este de las salinas, junto al Cráter de la Comadreja (78.8, 62.5) y el Campamento Roca de Hierro (67.7, 64.1). Vendedores en el Circuito del Espejismo (80.4, 77.5).
- **Qué se farmea:** Fragmento de caparazón moteado · `forever/4556` · `inv_misc_monsterscales_07` · **9 s 3 c** · carga 5 · Cola escamosa espesa · `forever/4555` · `inv_misc_monsterscales_04` · 1 s 55 c · Carne de tortuga · `forever/3712` · `inv_misc_food_70` · 87 c.
- **Criaturas (npc):** Mordedor brillavalva / Sparkleshell Snapper `npc 4143` (34-35) · Tortuga brillavalva / Sparkleshell Tortoise `npc 4142` (30-31).
- **En pantalla:** tortugas sobre la sal blanca; Fragmento de caparazón moteado; venta al PNJ. YouTube: «Shimmering Flats turtles» / «Sparkleshell Snapper farm».
- **Fuentes:** [CC-FARM] · [NOHIT] · [CYN] · [WHF-NPC] · [WHF-TT] · [WHF-MAP]
- **Confianza:** GUÍAS (valor por muerte) · JUGADORES · DATOS. Alternativa de más nivel: Cavapozos Fangorroca (`npc 4399`, 42-43) del Marjal Revolcafango, 58.4, 61.7, ~6 s por muerte con almejas [CC-FARM; WHF-NPC].

### 11. Reptadores de arena: la carne que piden las misiones nuevas (Claros del Río)
- **Qué es en Forever:** los cangrejos de la costa de **Claros del Río** (zona nueva de Forever) sueltan **Carne de cangrejo tierna** en el **40 %** de las muertes según Cynara; en la subasta valía **14 s c/u** (12-nov) porque la gente la compra para cocinar en vez de farmearla. Los reptadores de más nivel del sur de Tuercespina sueltan además **Almejas de boca grande** (perlas) [CYN 0:00-1:42]. En el mismo puerto hay misión con cangrejos: **«Sabores de mar»** (12 Ojos de múrloc de agua salada + 6 Carne de reptador de arena para Fimbo Grasapuños) [WHF-Q].
- **Nivel recomendado:** 36-41.
- **Cuánto da:** 14 s por carne (12-nov, Cynara); vendedor solo 1 s 12 c [WHF-TT] → **no venderla al PNJ**. Cynara: si tienes Cocina 200, ~25 s de ganancia por cada guiso vendido [CYN 1:42].
- **Lugar (coordenadas):** Claros del Río: Reptador de arena **71.6, 67.5** (n=14 de 85), 73.2, 63.1 y 76.8, 61.9 [WHF-NPC], al sur de **Puerto Polvomecha** (rótulo 78.9, 55.2). Fimbo Grasapuños: 79.0, 54.2. Vega de Tuercespina: Reptador de las arenas del sur 33.6, 76.3 y 35.6, 71.3 (cerca de Bahía del Botín) [WHF-NPC].
- **Qué se farmea:** Carne de cangrejo tierna · `forever/12206` · `inv_misc_food_51` · vendedor 1 s 12 c · Carne de reptador de arena (objeto de misión) · `forever/268345` · `inv_misc_food_126_clammeat` · Almeja de boca grande · `forever/7973` · `inv_misc_shell_03` · 46 c (solo los del sur de Tuercespina, según Cynara).
- **Criaturas (npc):** Reptador de arena / Sand Crawler `npc 255901` (36-37, Claros del Río; ojo, hay otro «Sand Crawler» `npc 830` de nivel 13-14 en Páramos de Poniente) · Reptador de las arenas del sur / Southern Sand Crawler `npc 2544` (40-41, es-MX de Wowhead Classic). Fimbo Grasapuños `npc 259962`; misión «Sabores de mar» / A Taste of the Sea `quest 95121`.
- **En pantalla:** cangrejos en la playa de Claros del Río con el Puerto Polvomecha detrás; Carne de cangrejo tierna. YouTube: «Riverglades sand crawlers» / «Tender Crab Meat farm».
- **Fuentes:** [CYN] · [WHF-NPC] · [WHF-TT] · [WHF-Q] · [WHF-MAP]
- **Confianza:** JUGADORES (40 %, 14 s) · DATOS (lugar, misión, ids). Ver Dudoso: la Carne de cangrejo tierna **no es nueva** (es un objeto de Classic) y no encontré la misión de los 10 guisos.

### 10. Las crías del Barranco Lethlor: Glándulas de llamas y una mascota (Tierras Inhóspitas)
- **Qué es en Forever:** crías de dragón (son dragonantes, así que sueltan monedas) con dos cosas propias: la **Glándula de llamas pequeña**, que va en el **Ají aliento de dragón** (la comida que escupe fuego, muy usada en mazmorras), y la mascota **Vástago oscuro**. Hay una misión que pide el **Corazón de draco negro** con 1-2 % de probabilidad: la gente mata más de cien. Vetas de mitril alrededor [STU-WH 1:26-4:30]. Unas **30 000 XP por hora** al 40 [STU-WH 5:10].
- **Nivel recomendado:** 40-44.
- **Cuánto da:** sin oro por hora medido. Glándula de llamas pequeña: vendedor **2 s 50 c** [WHF-TT]; ~10 s en la subasta el 14-nov (GrayMaine, en [ORO]). Vástago oscuro: vendedor 25 s (la subasta paga más; Studen cree que las mascotas valdrán más en Forever por los logros).
- **Lugar (coordenadas):** Tierras Inhóspitas, este: Scalding Whelp **82.5, 32.2** (n=21 de 110), 82.2, 38.0 y 77.7, 62.8 [WHF-NPC], alrededor del **Barranco Lethlor** (rótulo 79.2, 53.9). Studen avisa de élites en medio del barranco.
- **Qué se farmea:** Glándula de llamas pequeña · `forever/4402` · `inv_misc_organ_06` · 2 s 50 c · carga 5 · Vástago oscuro · `forever/10822` · `inv_misc_head_dragon_black` · 25 s · Corazón de draco negro (misión) · `forever/4612` · `inv_misc_organ_01` · Ají aliento de dragón · `forever/12217` · `inv_drink_17`.
- **Criaturas (npc):** Scalding Whelp `npc 2725` (41-43; **sin nombre es-MX** en Wowhead Forever ni Classic: decir «las crías del Barranco Lethlor»).
- **En pantalla:** crías escupiendo fuego en el barranco; Vástago oscuro de mascota; Glándula de llamas. YouTube: «Badlands whelp farm» / «Scalding Whelp Badlands».
- **Fuentes:** [STU-WH] · [ORO] (precio 14-nov) · [WHF-NPC] · [WHF-TT] · [WHF-MAP]
- **Confianza:** JUGADORES (XP, botín) · DATOS (lugar, ids, precios de vendedor). La misión del corazón: sin nombre comprobado.

### 9. Múrlocs del Pantano de las Penas: almejas con Perla de oro
- **Qué es en Forever:** cuatro tipos de múrlocs en toda la mitad sur de la playa y en una cueva llena. Todos pueden soltar **Almeja de boca grande**: siempre da 1-3 Carne de almeja sabrosa y a veces una perla, hasta la **Perla de oro**. Sueltan además 1-6 s en monedas, Serviola moteada cruda «de a varias», aceite de pescado, verdes, azules y épicas ligadas al equiparse de nivel 30-40. Los Oráculos sueltan la receta nueva **Té soleado** [MMOU 0:42-9:41].
- **Nivel recomendado:** 41-45 (playa a los 40; la cueva tiene demasiados juntos).
- **Cuánto da:** precios del **22-nov** [MMOU]: Perla de oro **~1 g 30 s**, Perla negra ~12 s, Perla iridiscente ~8 s, Perla lustrosa pequeña ~2 s 45 c, Carne de almeja sabrosa ~90 c, Serviola moteada cruda ~1 s 50 c. Una épica (Botas de evasión) se le vendió a **~13 g**. Conquest Capped: Oráculo/Comecarnes = Almeja de boca grande 55 %, **2 s 76 c por muerte** (EU 15-nov) [CC-FARM]. Vendedor: Almeja de boca grande 46 c, Perla de oro 1 g [WHF-TT].
- **Lugar (coordenadas):** Pantano de las Penas, sureste. Playa: Múrloc de marisma **82.4, 92.1** (n=22) y 86.4, 82.1; cerca del Puesto Juncobruma (81.5, 80.7). Grupo grande de Oráculos y Comecarnes **62.7, 87.2** (n=19) y 63.1, 82.4 [WHF-NPC], hacia la Cueva Stagalbog (66.1, 77.3).
- **Qué se farmea:** Almeja de boca grande · `forever/7973` · `inv_misc_shell_03` · 46 c · Perla de oro · `forever/13926` · `inv_misc_gem_pearl_04` · 1 g · Perla negra · `forever/7971` · `inv_misc_gem_pearl_01` · 10 s · Perla iridiscente · `forever/5500` · `inv_misc_gem_pearl_02` · 7 s 50 c · Perla lustrosa pequeña · `forever/5498` · `inv_misc_gem_pearl_03` · 2 s · Carne de almeja sabrosa · `forever/7974` · `inv_misc_food_51` · 50 c · Serviola moteada cruda · `forever/4603` · `inv_misc_fish_01` · Receta: té soleado · `forever/249883` · `inv_scroll_03` · 18 s 75 c (ligada al recogerla; Cocina 200).
- **Criaturas (npc):** Múrloc de marisma / Marsh Murloc `npc 747` (41-42) · Vomitatintas de marisma / Marsh Inkspewer `npc 750` (42-43) · Comecarnes de marisma / Marsh Flesheater `npc 751` (43-44) · Oráculo de marisma / Marsh Oracle `npc 752` (44-45). Nombres es-MX de Wowhead Classic (Forever no los trae).
- **En pantalla:** múrlocs en la playa; almeja abierta con una Perla de oro; Té soleado. YouTube: «Swamp of Sorrows murlocs» / «Marsh Oracle farm».
- **Fuentes:** [MMOU] · [CC-FARM] · [WHF-NPC] · [WHF-TT]
- **Confianza:** JUGADORES (precios 22-nov) · GUÍAS · DATOS.

### 8. Hienas Llagapata de las Arenas Abisales (y los rocs de paso) (Tanaris)
- **Qué es en Forever:** en las Arenas Abisales hay tantos Rocs de fuego (de misión) como hienas; casi nadie mata las hienas. Hienas: **Melena espesa** (8 s) y **Pata de trofeo grande** (9 s) para el vendedor, cuero grueso y pesado, Carne de lobo rojo y **Carne de lobo tierna** (la piden las guías de cocina). Rocs: grises parecidos y **Huevo gigante**. Ruta en triángulo por los tres esqueletos de dinosaurio [STU-HY 1:24-4:32].
- **Nivel recomendado:** 44-46.
- **Cuánto da:** Studen (23-nov): «un par de oro en unos pocos grupos» solo en grises; la Carne de lobo tierna «casi 1 g el montón» en la subasta y la de lobo rojo casi medio oro el montón (contra 17 s al vendedor); **Huevo gigante a poco más de 20 s** (la vez anterior vendió 32 a 41 s de media) [STU-HY 2:05-3:28]. Conquest Capped (EU 15-nov): Roc/Roc de fuego 10 s 49 c por muerte (Huevo 33 %) [CC-FARM].
- **Lugar (coordenadas):** Tanaris, **Arenas Abisales** (rótulo 45.4, 42.9). Hiena Llagapata **44.4, 38.7** (n=7), 63.1, 43.1 (n=8) y 61.0, 47.5 · Roc de fuego **48.6, 43.1** (n=9) y 47.5, 36.9 · Roc 51.7, 31.2 (n=9) [WHF-NPC]. Gadgetzan (51.2, 27.5) para vender, neutral.
- **Qué se farmea:** Melena espesa · `forever/4583` · `inv_misc_pelt_bear_01` · **8 s 12 c** · Pata de trofeo grande · `forever/4584` · `inv_misc_monsterclaw_04` · **9 s 37 c** · Carne de lobo tierna · `forever/12208` · `inv_misc_food_14` · 1 s 50 c · Carne de lobo rojo · `forever/12203` · `inv_misc_food_71` · 87 c · Huevo gigante · `forever/12207` · `inv_egg_03` · 1 s 50 c · Cuero grueso · `forever/4304` · `inv_misc_leatherscrap_08` · 3 s.
- **Criaturas (npc):** Hiena Llagapata / Blisterpaw Hyena `npc 5426` (44-45; es-MX de Wowhead Classic) · Roc de fuego / Fire Roc `npc 5429` (43-45; es-MX Classic) · Roc `npc 5428` (41-43).
- **En pantalla:** hienas entre los huesos de dinosaurio; Melena espesa y Pata de trofeo; huevo. YouTube: «Tanaris hyena farm» / «Abyssal Sands Tanaris».
- **Fuentes:** [STU-HY] · [CC-FARM] · [WHF-NPC] · [WHF-TT] · [WHF-MAP]
- **Confianza:** JUGADORES (precios 23-nov) · GUÍAS · DATOS. Huevos/rocs: YA USADO en [ORO] #10; aquí solo como complemento (precio nuevo: ~20 s el 23-nov, vs 15-18 s el 13-15-nov).

### 7. Gorilas y osos del norte de Feralas: grises de hasta 15 platas
- **Qué es en Forever:** «cerca de los 50». Tronadores Groddoc (gorilas) y Patriarcas Cueracero (osos) del norte de Feralas, en la misma zona; los gorilas son de la misión previa del Templo Sumergido, así que tienen reaparición dinámica. **No hace falta profesión** [STU-FER 1:24-3:06].
- **Nivel recomendado:** 47-50 (alternativa del 41-43: Simios Groddoc y Osos Cueracero del centro).
- **Cuánto da:** sin oro por hora; grises que paga el vendedor [WHF-TT]: **Hueso de oso grande 14 s 84 c** (cuenta como maza gris), **Mechón de pelo de gorila 11 s 31 c**, Mandíbula de oso 8 s 98 c, Pelo de gorila burdo 6 s 8 c, Garra de oso indómito 5 s 78 c, Costillar de oso 5 s 3 c. Studen da las mismas cifras redondeadas (19-nov) [STU-FER 2:26-3:06].
- **Lugar (coordenadas):** Feralas norte: Tronador Groddoc **42.1, 21.9** (n=7 de 29), 45.9, 25.7 y 49.3, 33.3 · Patriarca Cueracero **42.9, 22.1** (n=11 de 44), 47.8, 27.3 y 48.5, 36.7 [WHF-NPC], alrededor de Los Dos Colosos (rótulo 45.0, 22.7). Del 41-43: Simio Groddoc 57.0, 53.9; Oso Cueracero 57.8, 56.8. Vender: Campamento Mojache (Horda, 75.2, 43.8) o Bastión Plumaluna (Alianza, 31.1, 44.6).
- **Qué se farmea:** Hueso de oso grande · `forever/11411` · `inv_misc_bone_01` · 14 s 84 c · Mechón de pelo de gorila · `forever/4099` · `inv_misc_pelt_03` · 11 s 31 c · Mandíbula de oso · `forever/11408` · `inv_misc_bone_09` · 8 s 98 c · Pelo de gorila burdo · `forever/4096` · `inv_misc_monstertail_03` · 6 s 8 c · Garra de oso indómito · `forever/11410` · `inv_misc_monsterclaw_03` · 5 s 78 c · Costillar de oso · `forever/11409` · `inv_misc_food_13` · 5 s 3 c.
- **Criaturas (npc):** Tronador Groddoc / Groddoc Thunderer `npc 5262` (49-50) · Patriarca Cueracero / Ironfur Patriarch `npc 5274` (48-49) · Simio Groddoc / Groddoc Ape `npc 5260` (42-43) · Oso Cueracero / Ironfur Bear `npc 5268` (41-42).
- **En pantalla:** gorila Groddoc golpeándose el pecho; montón de huesos y pelo en la bolsa; venta al PNJ. YouTube: «Feralas gorilla farm» / «Groddoc Thunderer Feralas».
- **Fuentes:** [STU-FER] · [WHF-NPC] · [WHF-TT] · [WHF-MAP]
- **Confianza:** JUGADORES · DATOS (precios exactos del vendedor, lugar, ids). Distinto de los grifos Frayfeather del #9 de [ORO] (sur de Feralas).

### 6. Jaguares del Pantano de las Penas (y las Cazadoras llanagreste de Claros del Río)
- **Qué es en Forever:** «probablemente el farmeo de montura más común», ya famoso en 2019 [STU5 7:33-8:15]. Felinos que sueltan **Cola blanda larga** (8 s al vendedor) y **Bigote de cerdas** (7 s), cuero y carne; con desuello y herboristería rinde más (Kargoz sube Herboristería del 180 al 300 en este pantano) [KARG 5:48-7:30; SERL 0:22]. En Claros del Río, las **Cazadoras llanagreste** sueltan lo mismo, **más de 10 g/h**, y si hay gente en una zona vas a la otra [STU5 6:10-7:12].
- **Nivel recomendado:** 36-39.
- **Cuánto da:** Studen: «justo por encima de 10 g/h» en las Cazadoras (18-nov) [STU5 6:50]. SerllinoGG estima «unos 30 g/h si lo haces eficiente» (13-nov; **sin medir**) [SERL 3:25]. Vendedor [WHF-TT]: Cola blanda larga **8 s 6 c**, Bigote de cerdas **7 s 33 c**.
- **Lugar (coordenadas):** Pantano de las Penas: Jaguar del pantano **42.2, 42.4** (n=20 de 184), 37.3, 47.7 y 22.2, 42.4 [WHF-NPC]; vendedores en **Rocal** (Horda, rótulo 46.0, 53.8). Kargoz avisa a la Alianza de que patrullan guardias que la marcan para JcJ. Claros del Río: Cazadora llanagreste **58.7, 52.8** (n=10) y 58.5, 56.3; Patriarca llanagreste 58.6, 52.9, al sur de Rog'mar (59.6, 45.9) [WHF-NPC].
- **Qué se farmea:** Cola blanda larga · `forever/1688` · `inv_misc_monstertail_01` · 8 s 6 c · carga 5 · Bigote de cerdas · `forever/1686` · `inv_misc_monstertail_03` · 7 s 33 c · carga 10 · Cuero pesado · `forever/4234` · `inv_misc_leatherscrap_07` · 1 s 50 c.
- **Criaturas (npc):** Jaguar del pantano / Swamp Jaguar `npc 767` (36-37) · Cazadora llanagreste / Wildplains Huntress `npc 259055` (38-39) · Patriarca llanagreste / Wildplains Patriarch `npc 259054` (38-39).
- **En pantalla:** jaguar en el pantano con niebla; Cola blanda larga y Bigote de cerdas; desuello. YouTube: «Swamp Jaguar farm» / «Swamp of Sorrows skinning».
- **Fuentes:** [STU5] · [KARG] · [SERL] · [KHY] · [WHF-NPC] · [WHF-TT]
- **Confianza:** JUGADORES · DATOS. Ver Dudoso: Conquest Capped atribuye el Bigote de cerdas a los tigres de Tuercespina, no a los jaguares.

### 5. Elementales de roca de Tierras Inhóspitas (Blizzard puso más)
- **Qué es en Forever:** el clásico de los mid-30 a mid-40: elementales que sueltan grises de piedra que el vendedor paga bien y **Tierra elemental** [STU5 1:42-3:45; KARG 2:22-4:04; STU-40 4:31]. El **13-nov** Blizzard hizo que los **Elementales de roca inferiores aparezcan más seguido** [OFI-HF]. NOHITJEROME: con ellos «te garantizas la montura»; el único problema es la gente [NOHIT 7:47-8:28]. Kargoz: la Tierra elemental vale poco al principio de un servidor y mucho cuando empiezan las bandas (piedras de afilar elementales, pociones de protección).
- **Nivel recomendado:** 37-44 (tres franjas: inferiores 37-39, normales 39-40, superiores 42-44).
- **Cuánto da:** **~10 g/h solo en grises** (Studen, 18-nov) [STU5 1:42]; más si vendes la Tierra elemental o sale un verde/azul. Conquest Capped: Elemental de roca **7 s 19 c por muerte** (Trozo de piedra dentado 35 %, Piedra inerte 48 %, Tierra elemental 10 %; EU 15-nov) [CC-FARM]. Tierra elemental **~14 s** en la subasta (12-nov; Cynara la recomienda como inversión) [CYN 7:12]. Vendedor [WHF-TT]: Trozo de piedra lisa 5 s 30 c, Trozo de piedra dentado 4 s 11 c, Piedra inerte 3 s 60 c, Tierra elemental 4 s, Sal de roca 2 s 50 c, Piedra sólida 1 s.
- **Lugar (coordenadas):** Tierras Inhóspitas [WHF-NPC]: Elemental de roca inferior **17.6, 41.9** (n=16), 21.9, 46.6 y 21.3, 43.9 (al lado de **Kargath**, vendedores de la Horda, rótulo 4.3, 47.4) · Elemental de roca **43.1, 82.4** (n=17), 41.2, 77.7 y 37.2, 76.4 (sur, junto a la Explanada del Espejismo 37.7, 72.0) · Elemental de roca superior **2.8, 82.0** (n=18) y 14.0, 87.2 (suroeste). Kargoz: la Alianza vende en los campamentos goblin del centro (sin coordenada comprobada).
- **Qué se farmea:** Tierra elemental · `forever/7067` · `inv_ore_iron_01` · 4 s · Trozo de piedra lisa · `forever/4552` · `inv_stone_10` · 5 s 30 c · carga 10 · Trozo de piedra dentado · `forever/4553` · `inv_stone_13` · 4 s 11 c · Piedra inerte · `forever/4784` · `inv_stone_10` · 3 s 60 c · Sal de roca · `forever/8150` · `inv_misc_dust_02` · 2 s 50 c · Piedra sólida · `forever/7912` · `inv_stone_10` · 1 s.
- **Criaturas (npc):** Elemental de roca inferior / Lesser Rock Elemental `npc 2735` (37-39) · Elemental de roca / Rock Elemental `npc 92` (39-40) · Elemental de roca superior / Greater Rock Elemental `npc 2736` (42-44; es-MX de Wowhead Classic).
- **En pantalla:** elementales de roca en el desierto rojo; la nota del hotfix del 13-nov; Tierra elemental. YouTube: «Badlands rock elementals» / «Lesser Rock Elemental farm».
- **Fuentes:** [OFI-HF] 13-nov · [STU5] · [KARG] · [NOHIT] · [STU-40] · [CC-FARM] · [WHF-NPC] · [WHF-TT] · [WHF-MAP]
- **Confianza:** OFICIAL (más apariciones) · JUGADORES (10 g/h) · GUÍAS · DATOS.

### 4. Los coyotes de Claros del Río: la zona nueva que reaparece sola
- **Qué es en Forever:** en **Claros del Río**, la zona nueva de Forever (36-44), los coyotes del sur del Cortijo de Wheeler «reaparecen a lo loco»: Solheim calcula que siempre tiene que haber unos 4 vivos, así que matas, das la vuelta y ya están otra vez; hasta se puede farmear en grupo con botín libre [SOL 3:53-8:20]. Sueltan **Cola tupida suave** (7 s al vendedor; es objeto de la Feria de la Luna Negra) y **Melena espesa** (8 s), Carne de lobo rojo, colmillos y cuero [STU5 4:06-6:10; ZEZ 7:11]. Hay un coyote con nombre, **Sootfur**, de la misión «Coyote Huntin'» de Benjy Wheeler. Desde Claros del Río se pasa a Tierras Inhóspitas (#5) y hay barco de Puerto Polvomecha a Tanaris [SOL; STUR 8:33].
- **Nivel recomendado:** 36-40 (Merodeadores de las llanuras 39-40 al noreste).
- **Cuánto da:** zezsigaming, **prueba de 30 min el 20-nov: 6 g 84 s → «13 a 14 g por hora»** (48 s en grises + el resto en subasta) [ZEZ 7:11-8:12]. Studen: «fácilmente más de 10 g/h» [STU5 5:08]. Solheim, al 60: ~1 g en 3-4 min; Carne de lobo rojo 33 s y Colmillos grandes 4,5 s en la subasta [SOL 8:41].
- **Lugar (coordenadas):** Claros del Río [WHF-NPC]: Coyote de las llanuras **54.5, 86.9** (n=9) y 54.1, 83.5 · Merodeador coyote **54.4, 67.6** y 55.2, 70.7 · Sootfur 54.5, 86.2 · Merodeador de las llanuras 72.0, 37.1 (n=20 de 47). **Cortijo de Wheeler** (rótulo 54.8, 75.8); Benjy Wheeler 54.8, 73.0. Studen: «debajo del Cortijo de Wheeler, una cuevita y todo hasta el último árbol».
- **Qué se farmea:** Cola tupida suave · `forever/4582` · `inv_misc_monstertail_02` · **7 s 45 c** · carga 5 · Melena espesa · `forever/4583` · `inv_misc_pelt_bear_01` · **8 s 12 c** · Carne de lobo rojo · `forever/12203` · `inv_misc_food_71` · 87 c · Colmillo grande · `forever/5637` · `inv_misc_bone_08` · 75 c · Cuero pesado · `forever/4234` · 1 s 50 c.
- **Criaturas (npc):** Coyote de las llanuras / Plains Coyote `npc 259267` (36-37) · Merodeador coyote / Coyote Prowler `npc 259263` (36-37) · Merodeador de las llanuras / Plains Prowler `npc 268831` (39-40) · Sootfur `npc 258522` (38; sin es-MX). Misión «Coyote Huntin'» `quest 94617` (sin es-MX); Benjy Wheeler `npc 258317`.
- **En pantalla:** coyotes reapareciendo uno tras otro junto al Cortijo de Wheeler; Cola tupida suave; mapa de la zona nueva. YouTube: «Riverglades coyote farm» / «WoW Forever Riverglades».
- **Fuentes:** [ZEZ] · [STU5] · [SOL] · [STUR] · [WHF-NPC] · [WHF-TT] · [WHF-Q] · [WHF-MAP]
- **Confianza:** JUGADORES (13-14 g/h medidos) · DATOS (lugar, ids, precios de vendedor).

### 3. Pesca de Valijas reforzadas con mitril en Tuercespina — YA USADO + novedad
- **YA USADO:** [ORO] #4 contó la pesca de nivel alto con Adornos brillantes en los restos flotantes. **Novedad (21-nov):** RageGaming lo midió de verdad y encontró cómo **duplicarlo**: (1) el talento de Legado **Luremaster** (2 rangos; según él hay que poner antes 5 puntos en Cosecha abundante u Horas extra = 7 puntos) da 50 % de sacar un pez extra con señuelo, **también valijas**, y puede encadenarse: sacó **4 valijas en un solo lance**; (2) los **bancos de Anguila escama pétrea** también dan valijas; (3) el **Jarabe de caminar sobre el agua** (20-40 s) deja pescar lejos de la orilla sin que te ataquen, desde el nivel 20 [RAGE21 0:42-13:56]. **Hotfix 16-nov:** el Expositor de pesca del campamento da señuelos a todos [OFI-HF].
- **Nivel recomendado:** 25+ con Pesca 150 (Adornos brillantes +75 la llevan a lo que piden los restos).
- **Cuánto da:** **170 g en 3 h 30 min** subiendo la Pesca del 150 al 225 (≈ 49 g/h) con Luremaster; cada valija vale **~0,7 g de media**; sin Luremaster ~15 valijas por hora (≈ 10 g/h), con él ~40 [RAGE21 2:05-4:34, 12:14]. Dentro: tejido mágico, cuero grueso y basto, paño rúnico, **bolsas de 14**, verdes de 30 s a 3 g al vendedor y recetas [RAGE21 1:44].
- **Lugar (coordenadas):** Vega de Tuercespina, costa oeste. Ruta de RageGaming: salir del **Campamento Grom'Gol** (rótulo 31.9, 28.4), bajar por toda la costa hasta **Bahía del Botín** (27.2, 75.6), doblar la esquina hasta las ruinas y volver; abrir valijas y mandar todo por el buzón de Grom'Gol. **Restos flotantes: sin coordenada** (no están en los datos de Wowhead). Bancos de Anguila escama pétrea [WHF-MAP]: **27.4, 83.4** (8 bancos, junto a Bahía del Botín), 31.9, 81.3, 23.3, 57.2 y 27.1, 42.9.
- **Qué se farmea:** Valija reforzada con mitril · `forever/21228` · `inv_box_02` · vendedor 2 c (se abre) · Valija reforzada con hierro (nivel menor) · `forever/21150` · `inv_box_01` · Anguila escama pétrea · `forever/13422` · `inv_misc_fish_11` · 10 s · Adornos brillantes · `forever/6532` · `inv_misc_gem_variety_02` · Jarabe de caminar sobre el agua · `forever/8827` · `inv_potion_15` · Expositor de pesca · `forever/279965` · `inv_misc_2h_draenorfishingpole_a_01` · Paño de tejido mágico · `forever/4338` · Paño rúnico · `forever/14047` · `inv_fabric_purplefire_01` · Cuero grueso · `forever/4304`.
- **Criaturas (npc):** ninguna (pesca).
- **En pantalla:** corcho en los restos flotantes; cuatro valijas en el botín de un lance; personaje caminando sobre el agua. YouTube: «Mithril Bound Trunk fishing» / «Stranglethorn floating wreckage».
- **Fuentes:** [RAGE21] · [OFI-HF] 16-nov · [ORO] #4 · [WHF-TT] · [WHF-MAP]
- **Confianza:** JUGADORES (cifras, una persona) · OFICIAL (Expositor) · DATOS (ids, bancos). **No** contar su truco del add-on de cambio de capa.

### 2. Las cuevas de ogros de Alterac: ogros + vetas de cinco minerales
- **Qué es en Forever:** junto a los **Dominios de los Aplastacresta** (la fortaleza élite) hay ogros normales y **dos cuevas, una al norte y otra al sur**, con vetas de hierro, mitril, veraplata, oro y plata que reaparecen rápido: se puede subir Minería casi hasta el torio [FROST40 0:20-1:24; KARG 4:04-5:27; KHY 15:14]. Los ogros sueltan plata, paño de seda, grises y verdes. Un **vendedor gnomo en una jaula** permite vaciar bolsas sin irse. Hay un raro, **Lo'Grosh**, con una maza de nivel 32 que vale mucho en la subasta (a Frostadamus no le cayó en 2 muertes) [FROST40 5:10]. Frostadamus lo encontró **vacío porque las guías de subida no mandan ahí** [FROST40 0:41].
- **Nivel recomendado:** 34-38 (evitar los Aplastadores y Magos, que son élite, cerca de la fortaleza).
- **Cuánto da:** Frostadamus (11-nov), con Minería, montura y +15 % de velocidad en botas: **~30 g/h**; «sin montura ni botas, 20 a 25 g, o menos». Llenó bolsas de 12 casillas en una hora. Precios escaneados en hora punta (los más bajos) [FROST40 4:08-4:49]. Vendedor [WHF-TT]: Mena de oro 5 s, Mena de veraplata 5 s, Mena de mitril 2 s 50 c, Mena de hierro 1 s 50 c, Paño de seda 1 s 50 c.
- **Lugar (coordenadas):** Montañas de Alterac, **Dominios de los Aplastacresta** (rótulo 51.2, 42.0). Ogros [WHF-NPC]: Ogro Aplastacresta **47.8, 36.6** (norte), **47.4, 61.6** (sur) y 52.8, 53.1 (111 apariciones) · Tosco Aplastacresta 47.8, 37.2, 52.1, 46.8 y 47.7, 57.9. Vetas [WHF-MAP]: **52.8, 47.1 = 38 vetas en una casilla de 5 %** (11 de oro, 8 de hierro, 7 de plata, 6 de mitril, 6 de veraplata) y **48.0, 33.2 = 27 vetas**. Lo'Grosh **52.7, 47.3** (misma casilla de las vetas). Vendedor **Rizz Tornillosuelto** («Engineering Supplies») **47.3, 35.3**. Élites: Aplastador 42.1, 47.2; Mago 41.0, 43.0.
- **Qué se farmea:** Mena de oro · `forever/2776` · `inv_ore_gold_01` · 5 s · Mena de veraplata · `forever/7911` · `inv_ore_truesilver_01` · 5 s · Mena de mitril · `forever/3858` · `inv_ore_mithril_02` · 2 s 50 c · Mena de hierro · `forever/2772` · `inv_ore_iron_01` · 1 s 50 c · Paño de seda · `forever/4306` · `inv_fabric_silk_01` · 1 s 50 c. La maza de Lo'Grosh: **nombre no comprobado** (Wowhead no da botín en el tooltip).
- **Criaturas (npc):** Ogro Aplastacresta / Crushridge Ogre `npc 2252` (34-35) · Tosco Aplastacresta / Crushridge Brute `npc 2253` (35-36) · Aplastador Aplastacresta `npc 2254` (36-37, élite) · Mago Aplastacresta `npc 2255` (37-38, élite) · **Lo'Grosh** `npc 2453` (39, raro) · Rizz Tornillosuelto / Rizz Loosebolt `npc 2684` (vendedor).
- **En pantalla:** entrada de la cueva con vetas brillando; ogro Aplastacresta; Rizz en su jaula; Lo'Grosh. YouTube: «Alterac ogre caves» / «Crushridge Hold mining».
- **Fuentes:** [FROST40] · [KARG] · [KHY] · [WHF-NPC] · [WHF-TT] · [WHF-MAP]
- **Confianza:** JUGADORES (30 g/h, una prueba) · DATOS (vetas, ogros, vendedor, raro, ids).

### 1. Los Destripadores negros de Las Tierras Devastadas: casi 90 platas por muerte
- **Qué es en Forever:** buitres de nivel 46-48 que sueltan **Molleja de buitre** en un **40 %** de las muertes según Haste; la molleja valía **más de 2 g** en la subasta (23-nov) porque la piden las misiones de Las Tierras Devastadas: **«El vigor del buitre»** (10 mollejas + 2 Papadas de hiena risitas) y **«El golpe decisivo»** (2 mollejas + 3 Pinzas de scorpok + 1 pulmón de jabalí) [HASTE 0:41-1:22; WHF-Q]. Su herramienta de valor por muerte dice que es **el bicho que más paga por muerte del juego, casi el triple que el segundo** [HASTE 1:01]. Se puede esperar en un punto (un cráter negro con una aparición cada 1-6 min) o hacer una ruta por varios puntos si la capa está vacía. De paso: Aguijoneros Scorpok (~27 s por muerte) e Hienas risitas famélicas, ambos desollables [HASTE 2:03-3:43].
- **Nivel recomendado:** 46-50 (los Aguijoneros son 50-51).
- **Cuánto da:** prueba medida de 30 min (23-nov): **92 objetos ≈ 21 g → ~41 g/h** antes del 5 % de la subasta; **6 mollejas = la mitad del oro**; con los precios más bajos del día ~35 g/h y con los más altos ~55; **sin ninguna molleja, ~17 g/h** [HASTE 4:05-4:46]. Valor esperado: **~90 s por muerte**.
- **Lugar (coordenadas):** Las Tierras Devastadas [WHF-NPC]: Destripador negro **56.2, 36.5** (n=8 de 32), 62.4, 26.8 (n=5) y 46.5, 19.1 (n=4) — entre el Alto de los Rapiñadores (48.0, 29.1) y la Serpiente Enroscada (63.9, 33.6). Solo **32 puntos de aparición**: hay competencia y gana quien está encima. Misiones: Maga sangrienta Lynnore 50.6, 14.4 y Mago sangriento Drazial 50.5, 14.2 (cerca del Bastión Machacamiedo). Llegar: Alianza, vuelo al **Castillo de Nethergarde** (65.9, 18.7); Horda, desde el vuelo del Pantano de las Penas [HASTE 1:43].
- **Qué se farmea:** **Molleja de buitre** · `forever/8396` · ícono `inv_misc_organ_05` · carga 20 · el tooltip no trae precio de vendedor (su valor es la subasta) · Papada de hiena risitas · `forever/8391` · `inv_misc_food_16` · Pinza de scorpok · `forever/8393` · `inv_misc_birdbeck_02`.
- **Criaturas (npc):** **Destripador negro / Black Slayer `npc 5982`** (46-48, bestia carroñera; nombre es-MX de Wowhead Classic, Forever no lo trae) · Aguijonero Scorpok / Scorpok Stinger `npc 5988` (50-51) · Hiena risitas famélica / Starving Snickerfang `npc 5984` (45-46, es-MX Classic). Misiones: «El vigor del buitre» / Vulture's Vigor `quest 2603` (Maga sangrienta Lynnore `npc 7506`) · «El golpe decisivo» / The Decisive Striker `quest 2585` (Mago sangriento Drazial `npc 7505`).
- **En pantalla:** cráter negro de Las Tierras Devastadas; el buitre apareciendo; Molleja de buitre con su tooltip; el oro sumando. YouTube: «Black Slayer Blasted Lands» / «Vulture Gizzard farm».
- **Fuentes:** [HASTE] · [WHF-NPC] · [WHF-TT] · [WHF-Q] · [WHF-MAP]
- **Confianza:** JUGADORES (una prueba medida de 30 min, un servidor; el 40 % es suyo) · DATOS (criatura, nivel, lugar, misiones, ids). Ver Dudoso: el precio de 2 g depende del servidor y puede caer como los huevos.

---

## DUDOSO / NO CONFIRMADO
- **Molleja de buitre a 2 g:** un solo creador, un servidor, 23-nov. Los buffs de sus misiones eran muy buscados en Classic; no confirmé qué dan en Forever. Si todos van, bajará (la lección de los huevos gigantes: de 1 g a 15-18 s en una semana [ORO; CC-FARM]). Decir «a un jugador le salieron unos 40 de oro por hora; sin mollejas, 17».
- **El 40 % de mollejas:** dato de Haste (Wowhead no muestra probabilidades en el tooltip).
- **Pesca:** 170 g y 4 valijas en un lance son de una persona. Su ruta usaba el add-on de cambio de capa: él dice que solo suma ~15 %. Luremaster: «2 rangos, 25 % por rango» en [PROF]/Warcraft Tavern y «50 % con 2/2» en RageGaming: coinciden. El requisito de 5 puntos previos es suyo.
- **Carne de cangrejo tierna «nueva»:** Cynara la llama nueva, pero es un objeto de Classic (`forever/12206`, nivel 40). La misión de Claros del Río que encontré («Sabores de mar») pide **Carne de reptador de arena** (otro objeto, de misión). La misión de cocina de «10 guisos en el puerto» que menciona: **no la encontré**. Contar solo el precio (14 s el 12-nov) y que sale de los reptadores.
- **Bigote de cerdas en los jaguares:** Studen lo da en jaguares y cazadoras; Conquest Capped lo da en los tigres y panteras de Tuercespina y la Cola blanda larga en los jaguares. Decir «colas y bigotes de felino».
- **30 g/h de SerllinoGG:** estimación, no prueba.
- **Kóbolds de Arathi que sueltan talismanes del oleaje** (Kargoz): sin comprobar. La **Mena de sangrita inferior** es objeto de misión (Wowhead) y hay 10 vetas en el Cañón Mostacho Seco (84.0, 32.4 [WHF-MAP]); no encontré cuál misión de Bahía del Botín la pide.
- **Crías del Pantano de las Penas** (Kargoz las pone «al oeste» del pantano): no aparecen en los datos de Wowhead; las crías con Glándula comprobadas son las de Tierras Inhóspitas (#10).
- **Mosh'gra** (raro de Claros del Río, botín raro arreglado el 19-nov): no sé qué suelta.
- **Montura del 40:** ¿100 g con montura o 100 + 20? (Khylen: 100 + 20; [ORO]: contradicción ya anotada).
- **Barco de Puerto Polvomecha a Tanaris** «cada ~10 min» (SturnusGaming): sin confirmar en otra fuente.
- **Maza de Lo'Grosh** («nivel 32, velocidad 4.0», Frostadamus): nombre sin comprobar.
- **Farmeos de mazmorra** (Maraudón en solitario 20-40 g/h de un paladín protección vs «no vale la pena» el mismo día; Uldaman, Zul'Farrak, La Masacre): fuera del video.
- **Coordenadas:** las de criaturas son puntos de aparición registrados por Wowhead Forever (pueden faltar algunos); las de rótulos, vetas y bancos llevan ±0.5. Dibujarlas sobre el mapa de cada zona antes del render (regla del canal).

## ANÉCDOTAS REALES (foros y jugadores; contadas, no citadas)
1. **«Soy nivel 40 y no me alcanza para la montura»:** Frostadamus abre su video diciendo que esa frase no paraba de salir en su directo; como paladín la tuvo gratis, así que se retó a farmear su precio en un par de horas. Pasando por Alterac para una misión vio las cuevas de ogros **vacías**, porque las guías de subida no mandan ahí, y sacó unos 30 g/h minando [FROST40 0:00-4:08].
2. **Nivel 39 con 67 de oro:** zezsigaming se propuso llegar a 100 antes del 40 probando cada farmeo 30 minutos con cronómetro. Los huevos gigantes, que la semana anterior valían 1 g, le dieron 6 g/h; los coyotes de Claros del Río, 13-14 [ZEZ].
3. **Cuatro valijas de un solo lance:** RageGaming cuenta que con el talento Luremaster le salieron cuatro Valijas reforzadas con mitril en una sola pesca, «unos 4 de oro por sacar un pez», y que así pagó la montura y la doble especialización al llegar al 40 [RAGE21 3:27-3:49, 0:21].
4. **Nivel 46 y todo pagado:** en el hilo más grande del foro sobre el oro en Forever (21-nov, 460+ respuestas), un jugador de nivel 46 cuenta que ya tiene la doble especialización y la equitación a base de hierbas, mena, desuello y elementales; otro recuerda que en el juego original llevaba dos profesiones de recolección mientras subía y solo al final elegía las principales [F-GOLD].
5. **«¿Cuál es el método aprobado?»:** un jugador (22-nov) se queja de que las mazmorras tienen tope de 5 por hora y que hasta el Loto negro se vende por unos 5 de oro; otro, de nivel 48, pide que dejen farmear mientras no sea un exploit [F-APPR; F-STOP]. Sirve para el gancho del «mundo abierto».

## 5+ PRECIOS REALES DE SUBASTA (con fecha y fuente)
1. **Molleja de buitre:** **más de 2 g** c/u (23-nov, servidor de Haste) [HASTE 0:41].
2. **Perlas y almejas (22-nov):** Perla de oro ~1 g 30 s · Perla negra ~12 s · Perla iridiscente ~8 s · Perla lustrosa pequeña ~2 s 45 c · Carne de almeja sabrosa ~90 c · Serviola moteada cruda ~1 s 50 c. Épicas: Botas de evasión ~13 g (vendidas), Bastón de Jordan ~75 g [MMOU]. (Perla de oro el 15-nov: 2 g 70-5 g en un reino EU [CC-FARM]; Perla iridiscente: 1 g el 9-nov → 8 s el 13-nov [NOHIT 0:40].)
3. **Aire elemental ~84 s** c/u y **Talismán del trueno 27 s** (20-nov, servidor de zezsigaming) [ZEZ 5:07].
4. **Cuero pesado 2 s · Cuero grueso 6 s · Escamas de dragón 5 s** (20-nov) [ZEZ 1:41].
5. **Huevo gigante «poco más de 20 s»** (23-nov; la vez anterior vendió 32 a 41 s de media) [STU-HY 3:08]; ~15 s el 15-nov en EU, con más de 3000 publicados [CC-FARM].
6. **Carne de lobo tierna «casi 1 g el montón»** y **Carne de lobo rojo «casi medio oro el montón»** (contra 17 s al vendedor) (23-nov) [STU-HY 2:26].
7. **Tierra elemental ~14 s** (12-nov) — Cynara en su consejo de inversión (en Classic Era vale 8-10 g, dice) [CYN 7:12-7:32].
8. **Jarabe de caminar sobre el agua 20-40 s** según la hora (21-nov) [RAGE21 9:46].
9. **Carne de cangrejo tierna 14 s** (12-nov) [CYN 0:20] · **Fuego elemental 31 s** (13-nov, reino PvP Horda de Norteamérica) [SERL 5:30].
10. **Escaneo EU del 15-nov:** Solea 12 s 88 c · Mena de veraplata 12 s 63 c · Flor de fuego 9 s 98 c · Mena de oro 9 s 87 c · Mena de mitril 9 s 74 c · Espina de oro 6 s 17 c · Pálida (Fadeleaf) 5 s 19 c · Musgo de tumba 3 s 38 c · talismanes ~22-23 s · Perla azul ~14 s [CC-FARM].
11. **Loto negro «unos 5 g»** (22-nov, foro) [F-APPR] (el mercado negro lo vende a 50 g fijos [ORO]: dato curioso para el guion).

## Para el guion
- **Gancho (segunda persona, escena concreta):** «Llegas al nivel 40. Entras corriendo donde el instructor de equitación, abres la bolsa… y tienes 61 de oro. La montura cuesta 100. Y tu instructor de clase te recuerda que la doble especialización son otros 50. Te faltan casi 90 de oro. Mientras tanto, en un cráter negro de Las Tierras Devastadas, cada pocos minutos aparece un buitre que, en promedio, deja casi una moneda de oro cada vez que lo matas. Hoy: quince lugares concretos del 30 al 50, qué matar, dónde y cuánto da, del que menos rinde al que más.» (El 61 es ilustrativo: decirlo como «pongamos que tienes…» o usar el 67 real de zezsigaming: «un jugador llegó al 39 con 67 de oro».)
- **Cifra más fuerte:** **~41 g/h** (Destripadores negros, prueba de 30 min, 23-nov; 35-55 según el precio del día; 17 g/h sin mollejas). Segunda: **170 g en 3 h 30** pescando valijas (21-nov). Tercera medida: **13-14 g/h** con los coyotes de Claros del Río (20-nov).
- **Datos oficiales para dar peso:** hoy (25-nov) los centauros Magram reaparecen más rápido; 13-nov, más Elementales de roca inferiores; 16-nov, el Expositor de pesca da señuelos a todos; 20-nov, tope de 5 mazmorras por hora (por eso, mundo abierto).
- **Variedad del orden:** Kalimdor (Desolace, Marjal Revolcafango, Las Mil Agujas, Tanaris, Feralas) y Reinos del Este (Tuercespina, Claros del Río, Tierras Inhóspitas, Pantano de las Penas, Alterac, Las Tierras Devastadas). Puntos de venta de las dos facciones en cada ficha. Tipos: monstruos con grises (12, 10, 8, 7, 6, 5, 4, 1), recolección (2: minería), pesca (3), objetos de misión que se venden (13, 11, 1), materiales de fabricación (14, 9, 5).
- **Frases útiles (sin citar fuentes):** «Lo que todos farmean se hunde en días: los huevos gigantes pasaron de un oro a quince platas en una semana.» · «Las criaturas de misión reaparecen solas: si hay gente, mejor.» · «El vendedor nunca te baja el precio.» · «Si no tienes desuello, igual rinde; si lo tienes, rinde más.»
- **Patrocinio (Overgear) sin chocar:** el video enseña a farmear; la integración puede decir que si no tienes tiempo de farmear, Overgear tiene oro y coaching. Nunca «no compres oro».
- **3 ideas de miniatura (algo que se vea del juego):**
  1. **El buitre del cráter:** un Destripador negro posado sobre el cráter negro de Las Tierras Devastadas, una **Molleja de buitre** enorme brillando en primer plano y monedas de oro cayendo; texto «40 ORO/H».
  2. **Bolsa vacía vs montura:** tu personaje frente al instructor de equitación con la bolsa abierta y vacía; detrás, un mapa con 15 marcadores rojos sobre Azeroth; texto «15 FARMEOS».
  3. **La valija que sale del agua:** una **Valija reforzada con mitril** saliendo del mar en Tuercespina con el corcho al lado y Bahía del Botín al fondo, rebosando paño y una bolsa de 14; texto «DEL 30 AL 50».
- **Comprobar antes de grabar:** dibujar las coordenadas sobre cada mapa de zona; mirar en el cliente el nombre en español de las crías del Barranco Lethlor (Wowhead no lo tiene); no mostrar la interfaz del add-on de cambio de capa en ningún clip de RageGaming; los clips deben ser de Forever (ventana de profesiones con tecla K, ranura de bolsa de componentes).
