# Estudio Amaya — checkpoint (10-nov-2026; sesión 2 completó los pasos 1-6)

App Android para Amaya (hija de Edson, 12 años, Galaxy S20 Ultra): habla con Claude desde su teléfono para crear videos con la
fábrica. Pedido del usuario: bonita, fácil, «que se note que es para Amaya, hecha por su papá Edson», conectada por
clicknbusiness.com.mx.

## HECHO y probado
- `nucleo/amaya/servidor.py` (127.0.0.1:8795, stdlib): guía = `claude -p` sonnet sin herramientas con `guia.md` + catálogo
  (`--system-prompt-file`, `--system-prompt-snapshot off`, stream-json con imágenes en base64, `--include-partial-messages`);
  producción = `claude -p` completo en la raíz con `--append-system-prompt-file produccion.md`, `--permission-mode
  bypassPermissions`, `--disallowedTools` (DENEGADOS), env `FAB_CORTE_CONTEXTO=0`; cola de 1, tope diario, avisos a papá
  (`fab.py avisar`), versión 720p para el teléfono, portadas, voces de ElevenLabs con saldo (cuenta 2), «Mi frase» con tope,
  estilos propios, favoritos, fotos (Pillow) y audios (faster-whisper small CPU).
- `app.html` (pestañas Crear/Estilos/Voces/Mis videos/Aprende, carta de papá, splash con firma, tarjetas [[estilo:]]/[[voz:]],
  [[opciones:]], [[ficha]] con «🎬 ¡Crear mi video!», grabación de audio con MediaRecorder, fotos achicadas en el cliente).
  PROBADO en el navegador a 375x812: carta, chat con streaming, tarjetas de estilos y voces, ficha. NO probado aún: botón
  Crear (lanza producción real), pestañas Estilos/Voces/Mis videos a fondo, crear estilo propio, Mi frase, audio.
- `estilos.json` (11 estilos con imagen de ejemplo revisada), `voces.json` (28 recomendadas), `guia.md`, `produccion.md`,
  `avance.py`, `icono.py` → `web/icono-192/512.png`, `web/manifest.webmanifest`, `web/estilo_mis_fotos.jpg`.
- Datos de ella en `amaya_estudio/` (raíz; config.json con límites y carta editable por papá). El servidor quedó corriendo
  (lanzado a mano en segundo plano desde la sesión 1).

## HECHO en la sesión 2 (10-nov-2026)
1. `.gitignore`: `amaya_estudio/`, `nucleo/amaya/android/*.apk`.
2. Puerta: `/amaya/…` → 8795 con llave propia `clave_amaya` (cookie `fab_amaya`, solo /amaya/), ping + arranque automático
   del servidor, preflight OPTIONS; página del dominio `clicknbusiness.com.mx/amaya/` (ping con fetch, «la fábrica está dormida»).
3. `python fab.py amaya [--abrir]`.
4. APK `nucleo/amaya/android/amaya.apk` compilada (`construir_apk.py`).
5. Producción inofensiva (`prueba_bypass`): bypassPermissions activo, `fab.py panel` y Write en `nucleo/` BLOQUEADOS,
   avance.py anotado, registro stream-json leído por `leer_log`.
6. Docs: `docs/panel.md` § «Estudio Amaya», línea en CLAUDE.md, memoria `estudio-amaya-app.md`.
Extra: estilos propios sin foto = tarjeta con sus colores y su emoji (antes imagen rota).
Sesión 3 (pedido del usuario): los avances llegan al CHAT como mensajes con imagen (una o una hoja de 2-9), nota de voz
corta con la voz del video (≤ 5 por video) y texto; probado con un trabajo falso (`prueba_chat`, ya borrado).
Sesión 3c (pedido del usuario): chat vacío al empezar (los chats de prueba quedaron en `amaya_estudio/chats_viejos/`),
mini tutorial de 4 láminas tras la carta y botón «Reiniciar la app» en Aprende; probado a 375x812.
Sesión 3b (pedido del usuario): solo 3 pestañas (Crear, Mis videos, Aprende); estilo y voz FIJOS del canal Amaya Vibes
(coquette + Regina), la guía ya no pregunta; los videos los sube papá desde la PC. Guía probada aislada (no ofrece estilos).

## Queda (no bloquea)
- Instalar la APK en el S20 Ultra de Amaya (por Rayo) y probar en el teléfono: fotos, micrófono, descarga.
- La primera producción REAL la debe ver papá (no se lanzó ninguna): mirar que mande ≥ 3 imágenes y 2-3 notas de voz.
- Sin commit (el usuario no lo pidió).
