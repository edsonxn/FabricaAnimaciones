# Fábrica de Animaciones — instalación y primer video

Pipeline en Python, todo local, que produce videos animados 2D con narración, música y efectos sincronizados.
Tú hablas con **Claude Code** (app de Claude, pestaña Code) dentro de esta carpeta: él escribe el guion, dibuja las escenas
con el motor, genera la voz, la música y el render. Tú revisas y decides.

## 1. Requisitos de la PC
- Windows 10/11, **GPU NVIDIA con 8 GB o más** (voz y Whisper), 16 GB de RAM o más, ~50 GB libres por video largo en curso.
- **Git**, **Python 3.10 (64 bits)** marcado «Add to PATH».
- **ffmpeg** en `C:\ffmpeg\bin` (descarga «release full» de gyan.dev, descomprime ahí y añade `C:\ffmpeg\bin` al PATH).

## 2. Bajar el proyecto
```
git clone <url que te pasaron> C:\FabricaAnimaciones
cd C:\FabricaAnimaciones
```
Clónalo en **`C:\FabricaAnimaciones`**: algunas rutas del motor la dan por hecha.

## 3. Librerías
```
pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
pip install chatterbox-tts
playwright install chromium
```

## 4. Voces (Chatterbox, gratis y local)
Pon muestras limpias de 10-20 s (`.mp3` o `.wav`, una persona, sin música) en **`C:\chatterbox_voices\<Nombre>.mp3`**.
En el guion se elige con `VOZ = dict(referencia="C:/chatterbox_voices/<Nombre>.mp3", ...)`. Solo usa voces que tengas
derecho a usar (la tuya o una con licencia). Detalle: `docs/voz.md`.

## 5. Claves de API (opcionales, cada una con un solo uso — `docs/apis.md`)
Van en `canales/tokens/` (git las ignora; nunca las compartas):
- `elevenlabs_api_key.txt` — voz de ElevenLabs (de pago, la de mejor actuación).
- `google_ai_studio.txt` — **solo** música Lyria (de pago por pieza).
- Imágenes: **Google Flow** en el navegador (Claude lo maneja con el navegador integrado de la app), nunca por API.

## 6. Tus canales
Lee `canales/LEEME.md`. En corto: dile a Claude «crea mi canal *Nombre*, estilo *X*» y aparece en el panel.

## 7. Panel
```
python fab.py panel --abrir
```
Muestra el avance de **tus** videos y canales (http://127.0.0.1:8765).

## 8. Tu primer video
Abre la carpeta en Claude Code y escribe, por ejemplo:
> Quiero hacer un video de 3 minutos para mi canal *Nombre*, estilo Kurzgesagt isométrico, sobre *tema*.

Claude crea `videos/<video>/`, propone el guion y lo lleva por las etapas (`docs/flujo_produccion.md`).

## 9. Actualizaciones
Cuando el autor mejore el motor o un estilo:
```
git pull
```
Tus canales, tus videos y `BITACORA.md` están ignorados por git: el `pull` nunca los toca. No hagas `push` a este repo.
Tus reglas propias (las que le vayas dando a Claude) van en `docs/mis_reglas.md`.
