# Tus canales

Cada canal es un archivo `canales/<alias>.json` (alias en minúsculas con guion bajo, p. ej. `historia_rapida.json`).
El panel, el calendario (`python fab.py canales --actualizar`) y las ideas (`python fab.py ideas <alias>`) salen de aquí:
en cuanto existe el archivo con su `"nombre"`, el canal aparece solo.

**Crear un canal:** pídeselo a Claude («crea mi canal X, estilo Y») o copia `plantilla_canal.json.ejemplo` a `<alias>.json`
y rellena `nombre`, `estilo`, `canal_id` (YouTube Studio → Configuración → Canal → Configuración avanzada) y `horario`.

**Conectar YouTube** (para subir y leer métricas): crea un proyecto en Google Cloud con la *YouTube Data API v3* y la
*YouTube Analytics API*, descarga el cliente OAuth de escritorio como `canales/youtube_client_secrets.json` y corre
`python fab.py yt conectar` (inicias sesión en el navegador). Los tokens quedan en `canales/tokens/`.

Todo lo de esta carpeta (salvo esta guía y la plantilla) es tuyo y git lo ignora: un `git pull` del motor nunca lo toca.
