# APIs y saldos: qué se usa para qué (REGLA del usuario, 21-oct-2026)

Origen: en el taller «No vuelve a pasar» (`videos/no_vuelve/`) la sesión no tenía navegador y Claude probó a pintar una imagen por la
API de Google AI Studio (Nano Banana). El usuario: «Nunca hagas fotos en Google AI; las fotos son en Flow… no se debe usar el saldo
en imágenes». Ese mismo día pidió la biblioteca de música para «no estar dependiendo todo el tiempo de la API».

## 1. Cada recurso tiene UN uso
| Recurso | Para qué SÍ | Para qué NUNCA | Si no hay saldo o no está disponible |
|---|---|---|---|
| **Flow** (Google Labs, en el navegador integrado de la app o en Claude in Chrome) | TODAS las imágenes: escenarios, hojas de pegatinas, utilería, miniaturas; y los clips de video (Nano Banana 2.1 · x2 = 0 puntos) | — | Si la sesión no tiene herramientas de navegador, **pedirle al usuario que lo active** y seguir con lo que no depende de imágenes (guion, voz, taller). No buscar otra vía de pago. |
| **Google AI Studio** (clave en `canales/tokens/google_ai_studio.txt`) | **Solo Lyria** (música): `nucleo/lyria.py`, `nucleo/lyria_tramos.py` · 0,08 US$ por pieza | **Imágenes** (Nano Banana, `gemini-*-image`, Imagen…), aunque el modelo salga en la lista de la clave; texto o TTS de Gemini | 402 = crédito agotado → **biblioteca de música** (§2). Si nada encaja, avisar al usuario (recargar en ai.studio/projects o generarla a mano en AI Studio, que ya no es gratis). |
| **ElevenLabs** (3 cuentas en la API: `elevenlabs_api_key.txt`, `_2.txt` y `_3.txt`, la 3.ª desde el 21-oct-2026) | Voz `eleven_v4_turbo` con corchetes (≈ 0,20 créditos por carácter; por defecto desde el 26-oct-2026, `eleven_v4` cobra 0,40) y SFX que no estén en la biblioteca; **avisos por voz** (`fab.py avisar` y el locutor del panel, desde el 27-oct-2026: ~10-20 créditos por aviso, caché por texto; respaldo voz de Windows) | — | `tts_eleven.post()` salta sola a la siguiente cuenta (401/402). Saldos: `python nucleo/tts_eleven.py` (31-oct: cuenta 1 = 0, cuenta 2 = 7 815, cuenta 3 = 2 538; un video de 18 min ≈ 3 200 créditos). Mira los saldos antes de una voz larga; si todas bajan de lo que pide la ronda, avisar al usuario. |
| **YouTube Data API** | subir, programar, métricas | — | Cuota agotada: registrar la subida en `canales/<alias>.json` → `publicados` igual (regla del 13-oct). |

## 2. Orden antes de gastar (música y efectos)
1. **Música:** `python fab.py biblioteca sugerir <video>` (lee los tramos de `LYRIA` y el `timeline.json`) → si una pieza casa con el
   tramo (texto, duración, intensidad) → `python fab.py biblioteca usar <id> <video> <tramo>` → `lyria_tramos.py armar` como siempre.
   **Lyria nueva solo** para lo que la biblioteca no cubre (un motivo propio del guion, una estructura muy concreta) o si el usuario la pide.
2. **No repetir música ante el mismo público:** `--excluir` los videos que ya vio esa audiencia (el taller de la rueda excluye
   `la_sena` y `jalpa`) y, dentro de un mismo canal, no reutilizar una pieza de sus últimos 5 videos ni el motivo reconocible de un
   video (el silbido de «La seña»). Entre canales distintos, sí.
3. **Efectos:** `python fab.py biblioteca sfx buscar plato roto` → `sfx usar <id> <video>`; ElevenLabs solo para lo que falte.
4. **Imágenes:** Flow, siempre.
5. **Al cerrar un video** con música o efectos nuevos: `python fab.py biblioteca catalogar` y `python fab.py biblioteca sfx catalogar`
   (solo procesa lo nuevo) para que entren a la biblioteca.

## 3. Prohibido
- Probar una API de pago «para ver si funciona» sin preguntar. Primero el camino gratis (Flow, biblioteca); si exige al usuario
  (activar el navegador), pedírselo.
- Abrir o listar los archivos de `canales/tokens/` (credenciales): se usan solo a través de los módulos (`lyria.clave()`, `tts_eleven`).
- Pagar una alternativa cuando lo único que falta es que el usuario active algo.

## 4. Anotar lo gastado
- En el `ESTADO.md` del video: créditos de ElevenLabs (lo imprime `voz`) y piezas de Lyria (0,08 US$ c/u) o «biblioteca: <id>».
- `prompt_tramoN.txt` de una pieza reutilizada empieza con `BIBLIOTECA: <id>`; el uso queda en `nucleo/datos/musica_biblioteca.json`.
