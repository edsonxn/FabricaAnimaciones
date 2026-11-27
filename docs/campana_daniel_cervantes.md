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

## Videos
| Video | Tema | Estado |
|---|---|---|
| `campana_dc_agua` | ¿De dónde viene tu agua? pozos → tanques → red; fugas y pozos sin luz; propuesta tubería + respaldo eléctrico | MASTER 59.6 s entregado 27-nov (voz Juan Pablo; se puede renarrar con la de Daniel) |
| `campana_dc_basura` | Rutas sin horario (3 camiones: 04 contenedor, 63 centro, 26 = 20+ comunidades; 8 lugares 1×/semana), basurero a cielo abierto, río → camión compactador nuevo + horario oficial por colonia + aviso al celular + basurero separado | MASTER 27-nov (Rayo), sin publicar |
| `campana_dc_superdaniel` | Cómico, todo en Flow: Daniel se pone un traje azul con el PAN (tipo armadura), vuela sobre Juchipila y arregla el alumbrado; «Juchipila, con luz.» | MASTER 26.7 s 27-nov (Flow ~35 pts, voz clonada por STS), sin publicar |
| `campana_dc_alumbrado` | Alumbrado LED (2,980 luminarias viejas; 50 LED/año ≈ 60 años) | pendiente |
| `campana_dc_salud` | Salud (hospital comunitario para 4 municipios, 2 médicos por mil, dengue) | pendiente |

Pendiente aparte: PDF de servicios de marketing digital para la campaña (el usuario elige de las 16 propuestas).

## Datos ya investigados (con fuente)
- **Basura:** tabla oficial «Rutas de aseo público» (FB del Ayuntamiento, 22-nov-2026; `campana_dc_basura/fuente/rutas_aseo.json`): solo días, **sin horario**. PMD: basurero de 9,356.84 m², distribución inadecuada; Informe: maquinaria para sepultar basura expuesta «para prevenir incendios»; drenaje con descarga al Río Juchipila (Cantera, Mezquitera Sur). Inventario 2021: un solo compactador (International 2013) + Ford 2008 de contenedores; número actual oficial de unidades NO publicado. Compactador nuevo 21 yd ≈ $1.9–2.8 millones (anuncios, no licitación); la SAMA pone la mitad en 2025-2026 (Sombrerete, Loreto…, Concepción del Oro, Ojocaliente); Calera compró 3 y «ya no hemos tenido problemas» (NTR 26-nov-2026). Río: limpieza Conagua + Ayuntamiento 15-nov-2026 sacó 30 bolsas grandes y un volteo de basura; planta de lagunas 17.8 L/s activa. **OJO:** los «9 incendios en 4 días» (NTR abr-2026) fueron pastizales, NO el basurero: no usarlo.
- **Alumbrado:** censo CFE 2015 = 2,980 luminarias; ~50 cambios a LED por año; 600 mantenimientos/año por $261 mil.
- **Salud:** Hospital Comunitario IMSS-Bienestar atiende ~20 mil personas de Juchipila, Moyahua, Mezquital del Oro y Apozol, 9 especialistas; 25 médicos = 2 por mil (estatal 3); 69.5 % sin seguridad social; 27.9 % sin acceso a salud; 17 casos de dengue (nov-2026).
- **Contexto político:** presidente municipal actual «Profe Chema» Castro Félix (PT); 2024: PAN 27.2 % vs PT 46.6 %.
