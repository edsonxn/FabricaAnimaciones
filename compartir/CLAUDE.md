# Fábrica de Animaciones — guía para Claude Code

Pipeline propio (Python, todo local) que produce videos animados 2D con narración, música y efectos sincronizados.
Responde en español. Usa `python fab.py ...` desde la raíz del proyecto. Instalación y primeros pasos: `LEEME.md`.
**Si existe `docs/mis_reglas.md`, léelo: son las reglas propias de este usuario y ganan sobre las de aquí.** Cuando el usuario
te dé una regla nueva («desde ahora…»), anótala ahí con fecha (no en este archivo: se reemplaza en cada `git pull`).

## Canales del usuario
- Sus canales son `canales/<alias>.json` (guía y plantilla en `canales/LEEME.md`). Si no hay ninguno, al primer pedido de
  video pregúntale para qué canal es y créalo (nombre, estilo de la tabla de abajo, horario) antes de producir.
- **Un estilo fijo por canal**: anótalo en `"estilo"` del JSON y respétalo; no cambies de motor por comodidad, pregunta.
- `ejemplos/` NO son proyectos del usuario: es solo el código (guion/escenas, sin medios) de un video de referencia por estilo.
  Léelo para copiar la técnica; nunca reutilices sus escenas tal cual (escenas y utilería propias; solo primitivas del kit).
- Calendario: `python fab.py canales --actualizar` (qué canal se queda antes sin video). Al subir un video regístralo en
  `canales/<alias>.json` → `publicados` (`video`, `id`, `titulo`, `programado`). Nunca dos videos del mismo canal el mismo día
  (`horario.separacion_min_horas`).

## Estilos recomendados (⭐ = los que mejor resultado dan)
| Estilo | `ESTILO_VISUAL` / motor | Copiar de | Doc |
|---|---|---|---|
| ⭐ Kurzgesagt ISOMÉTRICO + mapas con relieve real + retratos reales en marco | `kurzgesagt` | `ejemplos/independencia_mx/` | `docs/estilo_kurzgesagt.md` §A (leer entera) |
| Kurzgesagt con mascota (Shorts verticales, muy dinámico) | `kurzgesagt` | `ejemplos/sol_apagado_8min/`, `ejemplos/historia_60/` | `docs/estilo_kurzgesagt.md` |
| ⭐ Boceto + guache con mapa de relieve (ETOPO1); un dibujo por frase; pegatinas de Flow; ≥ 3 fotos reales/min | `boceto` | `ejemplos/historia_jalisco/` (mapa: `historia_egipto/`; Short vertical: `primer_foton/`) | `docs/estilo_boceto_guache_mapa.md` |
| Doodle / doodle psicodélico / recortes | `doodle` | `ejemplos/neandertales/`, `ejemplos/un_dia_30mil/` | `docs/flujo_produccion.md` |
| Documental de misterio / crimen real con tablero de detective vivo | `documental` | `ejemplos/voynich/` | `docs/estilo_documental.md` |
| ⭐ Noir B/N con medios REALES en tinta (foto real de cada persona pública) | `noir` | `ejemplos/informante_2027/` | `docs/estilo_noir.md` |
| ⭐ Pegatina Flow: Flow pinta escenarios y hojas de personajes; el código los recorta y anima con parallax | `pegatina_flow` | `ejemplos/jalpa/` · noir: `ejemplos/secreto_ia/` | `docs/estilo_pegatina_flow.md` |
| ⭐ Secuencia Flow (plastilina o dibujo animado; no se dibuja por código) | motor `secuencia` | `ejemplos/bichos_invierno/` · dibujo animado: `ejemplos/arana_techo/` | `docs/estilo_secuencia_flow.md` |
| ⭐ Secuencia YT: gameplay real por beat + pegatinas + fichas de la interfaz del juego + motion graphics propios | motor `secuencia` (`nuevo <v> --yt`) | WoW `ejemplos/wow_curiosidades_kalimdor/` · Elden Ring `er_radagon_atrocidades/` · Skyrim `tes_misiones_daedricas/` · Nintendo `banjo_tooie/` · Zelda con fichas translúcidas de su interfaz `majora_mask/` | `docs/estilo_secuencia_yt.md` |
| ⭐ Línea blanca + neón (palabras clave gigantes, un elemento en neón que palpita) | secuencia Flow + FX `neon` | `ejemplos/freno_enojo/` | `docs/estilo_linea_neon.md` |
| Secuencia con efectos tipo Flow | `secuencia_fx` | `ejemplos/guason_fumado/` | `docs/estilo_secuencia_fx.md` |
| Noir a color / feudal | `noir_color` / `noir_feudal` | `ejemplos/sociedad_1200/`, `ejemplos/got_joffrey/` | `docs/estilo_noir_color.md` |
| Rayos X tecno (vertical) | `documental` | `ejemplos/mods_ia_fusion/` | `docs/estilo_rayosx_tecno.md` |
| Terror CRT (cuarto oscuro, gameplay dentro de una tele) | `documental` | `ejemplos/terror_ben_drowned/` | `docs/estilo_terror_crt.md` |
| Acuarela pintada a mano (papel, lavados con borde húmedo, tinta que hierve, chibi, SFX sintetizados) | `documental` (kit `acuarela.py` del ejemplo) | `ejemplos/ballena_estomago/` | `docs/estilo_acuarela_pincel.md` |
| Grabado de peste (tinta y buril en espacio 3D) | `documental` | `ejemplos/wow_tres_noches/` | `docs/estilo_grabado_peste.md` |
| Boceto en bucle | `boceto` | `ejemplos/gota_bucle/` | `docs/estilo_boceto_gota.md` |
| Guache / meme | `guache` | `ejemplos/pelea_meme/` | `docs/estilo_guache_meme.md` |
| Cartoon 90 | `cartoon90` | `ejemplos/gato_cobarde/` | `docs/estilo_cartoon90.md` |
| Análisis táctico de esports (VOD con pausas y telestrador + jugada clave en 3D con three.js, `nucleo/tactica3d`) | `secuencia_yt` | `ejemplos/lol_worlds_2026/` (3D: `j6_3d.py`) | `docs/estilo_analisis_tactico.md` |

**Toda lámina con profundidad** (≥ 3 planos, luz, capas), nunca paneles planos sobre un fondo: «parece página web».
Video sin canal o estilo no dicho → pregunta (AskUserQuestion) qué estilo de la tabla quiere.

## Cómo se hace un video
1. `python fab.py nuevo <v>` (`--secuencia` para Flow, `--yt` para gameplay) y escribe `videos/<v>/panel.json` con
   `{"canal": "<alias>"}` para que el panel lo ponga en su canal. Lee el doc del estilo y el ejemplo.
2. Guion en `videos/<v>/guion.py` → `voz` → `seleccionar` → `tiempo` → escenas → `musica` → `sfx` → `mezcla` → `video` → `final` → `verificar`.
   Detalle: `docs/flujo_produccion.md`; voz: `docs/voz.md` (léelo ANTES de `voz`).
3. Videos largos en tramos (varias sesiones): estado en `videos/<v>/ESTADO.md`; retomar con `python fab.py continuar <v>` (`docs/sesiones.md`).
4. Pregunta si quiere ver el principio renderizado (`video --hasta <s>`), siempre con audio completo (voz + música + SFX + mezcla).
5. Entrega: `videos/<v>/salida/*_MASTER.mp4` (1080p) + `.srt`. Publicar: `docs/publicacion.md` (`python fab.py yt subir <v> <alias> private --publicar <ISO>`).

## Reglas de producción
- **Sin subtítulos quemados**: texto en pantalla solo para énfasis; el `.srt` se genera aparte.
- **Rigor**: un video no está terminado porque renderizó. Revisa a tamaño completo un cuadro cada ~3 s y uno por fase.
  Bloquean la entrega: escenario vacío, mismo fondo en escenas distintas, mapa sin geografía real, figuras mal hechas o
  flotando, texto que choca o se sale, cuadros negros, algo quieto > 2 s, personajes diminutos. Lista de errores:
  `docs/estilo_kurzgesagt.md` § «ERRORES A NO REPETIR». Entre tardar más y entregar flojo: tardar más.
- **APIs, cada una con UN uso** (`docs/apis.md`): imágenes SOLO en Google Flow (navegador); la clave de Google AI Studio es
  solo para música Lyria; ElevenLabs para voz (con corchetes de actuación: `"[sighs] Esa regla murió. [short pause] En Hong Kong."`).
  Nunca probar una API de pago «a ver si funciona» ni abrir `canales/tokens/`.
- **Música**: Lyria apegada al guion (`LYRIA` en guion.py). Antes de pedir música nueva, mira la biblioteca propia
  (`python fab.py biblioteca sugerir <v>`); al cerrar cada video `biblioteca catalogar`. Doc: `docs/musica_biblioteca.md`.
- **SFX** por código (`SFX_ELEVEN` en guion.py), sin repetir los mismos efectos ante el mismo público.
- Fonética (`FONETICA` en guion.py) solo para Chatterbox/Applio; ElevenLabs con escritura normal.
- Si el usuario critica la calidad, arregla también el estilo (kit + doc) y anota la lección en el doc del estilo.

## Disco y entorno
- Un video de 3 min ≈ 1,5 GB temporales. `FAB_PESADOS=<disco>\FabricaAnimaciones` manda las carpetas pesadas a otro disco.
- Voz (Chatterbox) y render NO a la vez (GPU). Comandos largos (> ~8 KB) fallan en Windows: escribe archivos con Write/Edit.
- ffmpeg en `C:\ffmpeg\bin`, voces en `C:\chatterbox_voices`.
- Git: este repo es de solo lectura para el usuario (recibe mejoras con `git pull`); sus canales, videos y BITACORA.md están
  ignorados. No hagas `push`.

## Comandos esenciales
```
python fab.py estado [v] | continuar [texto] | canales [--actualizar] | ideas [<canal>] [--actualizar]
python fab.py <v> voz | seleccionar | tiempo | comprobar | musica | sfx | mezcla | video | final | verificar | todo
python fab.py <v> escena <id> t1 t2 ...   hoja de prueba (previews/esc_<id>.jpg; MÍRALA)
python fab.py <v> montaje                  borradores por escena para el 🎞 Montaje del panel
python fab.py <v> video --hasta <s> | --rehacer 270-280   luego `final`
python fab.py nuevo <v> [--secuencia|--yt]  |  <v> fx [--seco|hoja]  |  <v> limpiar (al aprobar)
python fab.py biblioteca sugerir <v> | buscar <texto> | catalogar | sfx buscar <texto>
python fab.py yt conectar | canales | metricas <alias> 90 | videos <canal> | subir <v> <canal> private
python fab.py panel --abrir
```
Índice de docs: `docs/flujo_produccion.md` (núcleo, etapas, render) · `docs/voz.md` · `docs/apis.md` · `docs/musica_biblioteca.md`
· `docs/publicacion.md` · `docs/sesiones.md` · `docs/panel.md` · `docs/api_kz.md` (kit Kurzgesagt) · `docs/estilo_*.md` · `API.md` (catálogo; solo con grep).
