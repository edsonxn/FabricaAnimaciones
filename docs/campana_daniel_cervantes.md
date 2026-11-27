# Proyecto «Campaña Daniel Cervantes» (Juchipila, Zac.) — NO es canal de YouTube

Alta: 27-nov-2026. Proyecto de la fábrica fuera de los canales: el usuario y un amigo quieren llevar la **campaña digital** de
**Daniel Cervantes** (PAN, Juchipila, Zacatecas). Los videos se hacen como DEMO para mostrárselos en persona y, si se cierra el
trato, para sus redes. **Nada se publica sin el OK expreso del usuario** (no hay canal, ni `yt subir`, ni panel de
publicación, ni monetización). Se entregan por **Rayo** al celular del usuario.

## Reglas del proyecto
1. **Carpeta:** `videos/campana_dc_<tema>/`, sin canal (`fab.py nuevo` no aplica). Cada video lleva su `ESTADO.md` y su `guion.md` con fuente por dato.
2. **Formato:** VERTICAL 1080×1920 (Reels, TikTok, WhatsApp), ~60–90 s, piden **90 s** (27-nov).
3. **Voz:** la de **Daniel, clonada con su permiso** (él lo pidió). ElevenLabs **cuenta 4**, id `U6S3DHgp2HdE70osCRov`,
   `eleven_v4_turbo`, **sin corchetes de actuación**, estabilidad .65, similarity .8, semilla 11. Guion en **PRIMERA PERSONA**:
   es Daniel proponiendo («Soy Daniel Cervantes… Mi propuesta…»). Solo para esta campaña: nunca en canales ni en Noticias de
   Juchipila (que es anónima).
4. **Privacidad:** `voz_clon/original.ogg` es una conversación PRIVADA de estrategia política: no transcribirla, no citarla, no
   compartirla; está en `.gitignore` (`videos/*/voz_clon/`). Tampoco se suben a git render, fuentes ni salida.
5. **Temas:** problemas reales del pueblo, con datos de fuente oficial (PMD 2024-2027, 1.er Informe, publicaciones del
   Ayuntamiento, INEGI/CONEVAL, CFE, IMSS-Bienestar) y propuesta concreta con el «cómo mejoraría». **Prohibido:** seguridad
   (delicado/peligroso) y «a dónde va tu dinero» / recortes de nómina (compromisos que no se pueden cumplir). No atacar
   personas: los datos hablan.
6. **Estilo:** maqueta de **arcilla 3D** (Blender EEVEE) del valle real (relieve Copernicus + calles/ríos OSM) + escenas de estudio
   con fondo transparente compuestas sobre degradado; cortinilla azul/cian (colores PAN), foto de Daniel en duotono al inicio y al
   cierre, mosca «PROPUESTA · DANIEL CERVANTES», tarjetas de propuesta numeradas. Música: biblioteca (Lyria ya pagada) o Lyria
   nueva si hay saldo en AI Studio; SFX de la biblioteca.
7. **Herramientas (copiar del primer video):** `videos/campana_dc_agua/`: `datos.py` (relieve + OSM → `datos/valle.*`),
   `agua3d.py` (valle con plan JSON: cámara, pozos, tanques, tubos que crecen, fugas, anclas), `casa3d.py`/`pozo3d.py`
   (estudio), `montaje.py` (+ `comp.py`; capas PIL 2× → ffmpeg), `voz.py`, `mezcla.py` (voz +1 s, música agachada, SFX,
   -14 LUFS). Revisión: hojas de cuadros + Whisper sobre la mezcla final.
8. **APP ciudadana de Juchipila (27-nov, pedido del usuario):** la campaña promueve una aplicación para los habitantes donde se
   hacen reportes. En cada propuesta, si encaja, una escena con el celular y la app como servicio extra: alumbrado → reporte con
   FOTO del poste; basura → mapa en tiempo real del camión con GPS (video futuro); apagones → mapa de apagones con los reportes de
   los vecinos. Si no encaja, no se menciona. Mismo diseño de la app en todos los videos.

## Videos
| Video | Tema | Estado |
|---|---|---|
| `campana_dc_agua` | ¿De dónde viene tu agua? pozos → tanques → red; fugas y pozos sin luz; propuesta tubería + respaldo eléctrico | MASTER 59.6 s entregado 27-nov (voz Juan Pablo; se puede renarrar con la de Daniel) |
| `campana_dc_basura` | Rutas sin horario (3 camiones: 04 contenedor, 63 centro, 26 = 20+ comunidades; 8 lugares 1×/semana), basurero a cielo abierto, río → camión compactador nuevo + horario oficial por colonia + aviso al celular + basurero separado | MASTER 27-nov (Rayo), sin publicar |
| `campana_dc_superdaniel` | Cómico, todo en Flow: Daniel se pone un traje azul con el PAN (tipo armadura), vuela sobre Juchipila y arregla el alumbrado; «Juchipila, con luz.» | MASTER 26.7 s 27-nov (Flow ~35 pts, voz clonada por STS), sin publicar |
| `campana_dc_lowpoly` | Prueba de 15 s estilo PS1 (receta de un TikTok, sin Blender a mano): Daniel low poly (~300 triángulos, cara de 64 px con 9 gestos de Flow que cambian con su voz) en la plaza; el camión abre la caja y sale el reloj 8:15 | MASTER 16.8 s 27-nov (Rayo), sin publicar |
| `campana_dc_alumbrado` | «Juchipila, con luz»: 2,980 luminarias (censo CFE) → todas a LED en 3 años; Tlaltenango −57.7 % (CONUEE); el ahorro paga el cambio; poste con número + WhatsApp + 72 h + mapa público (sin «60 años»: el 1.er Informe reporta ~200 LED) | MASTER 81.5 s 27-nov, sin publicar |
| `campana_dc_apagones` | «Que la tormenta pase y la luz se quede»: apagones en las casas (viento/lluvia), refri, aparatos quemados, pozos sin luz; El Tejano 26-jun-2026 (NTR); Bajío 51 min por apagón vs 44.5 nacional (CFE CAIDI 2024). Red = CFE → 1 poda preventiva con la CFE, 2 **app «Mapa de apagones»** (reportes → datos para exigir a la CFE cambiar transformadores/líneas), 3 plantas de respaldo en los pozos, + ayuda para reclamar aparatos quemados (cláusula 25.ª) | MASTER 93.0 s 27-nov, sin publicar |
| `campana_dc_topes` | SÁTIRA PS1 con groserías (30 s): Daniel maldice los topes (vocho que vuela, barra «SUSPENSIÓN» y K.O., berrinche con cara roja) y su «primera orden como presidente» es tirarlos todos; con un pisotón salen volando. Versión con pitidos aparte | MASTER 33.3 s 27-nov (Rayo, normal + pitidos), sin publicar |
| `campana_dc_salud` | **Low poly PS1** (pedido): fiebre a las 3 a. m.; hospital comunitario para ~20 mil de 4 municipios; 2 médicos por mil vs 3 estatal; casi 3 de 10 sin acceso a salud (CONEVAL); 2 h o más a un especialista; dengue 19 de 27 casos del estado → 1 unidad médica móvil con día y hora fijos, 2 brigadas contra el dengue todo el año, 3 jornadas de especialistas aquí, + app (próxima visita y reporte de criadero con foto) | MASTER 90.0 s 27-nov (Rayo), sin publicar |

Pendiente aparte: PDF de servicios de marketing digital para la campaña (el usuario elige de las 16 propuestas).

## Datos ya investigados (con fuente)
- **Basura:** tabla oficial «Rutas de aseo público» (FB del Ayuntamiento, 22-nov-2026; `campana_dc_basura/fuente/rutas_aseo.json`): solo días, **sin horario**. PMD: basurero de 9,356.84 m², distribución inadecuada; Informe: maquinaria para sepultar basura expuesta «para prevenir incendios»; drenaje con descarga al Río Juchipila (Cantera, Mezquitera Sur). Inventario 2021: un solo compactador (International 2013) + Ford 2008 de contenedores; número actual oficial de unidades NO publicado. Compactador nuevo 21 yd ≈ $1.9–2.8 millones (anuncios, no licitación); la SAMA pone la mitad en 2025-2026 (Sombrerete, Loreto…, Concepción del Oro, Ojocaliente); Calera compró 3 y «ya no hemos tenido problemas» (NTR 26-nov-2026). Río: limpieza Conagua + Ayuntamiento 15-nov-2026 sacó 30 bolsas grandes y un volteo de basura; planta de lagunas 17.8 L/s activa. **OJO:** los «9 incendios en 4 días» (NTR abr-2026) fueron pastizales, NO el basurero: no usarlo.
- **Alumbrado:** censo CFE 2015 = 2,980 luminarias; ~50 cambios a LED por año; 600 mantenimientos/año por $261 mil.
- **Salud:** Hospital Comunitario IMSS-Bienestar atiende ~20 mil personas de Juchipila, Moyahua, Mezquital del Oro y Apozol, 9 especialistas; 25 médicos = 2 por mil (estatal 3); 69.5 % sin seguridad social; 27.9 % sin acceso a salud; dengue: 19 casos en Juchipila de 27 en el estado (SSZ, 27-nov-2026; el 17 era de NTR, más viejo); 6 unidades médicas (PMD); Informe 2025: 204 traslados gratis a citas fuera.
- **Contexto político:** presidente municipal actual «Profe Chema» Castro Félix (PT); 2024: PAN 27.2 % vs PT 46.6 %.
