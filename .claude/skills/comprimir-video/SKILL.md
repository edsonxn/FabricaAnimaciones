---
name: comprimir-video
description: Comprime un video (un MASTER de la Fábrica u otro .mp4 cualquiera) a una copia más liviana sin tocar el original. Úsalo SIEMPRE que el usuario diga "comprime este video", "hazlo más liviano", "bájale el peso", "que pese menos", "para mandarlo por WhatsApp/correo", "reduce el tamaño", "achica el video" o algo equivalente, y también cuando haga falta liberar disco guardando los MASTER en H.265. Acepta un archivo, una carpeta o el alias de un video (busca videos/<v>/salida/*_MASTER.mp4).
---

# Comprimir video

Proyecto `C:\FabricaAnimaciones`, ffmpeg en `C:\ffmpeg\bin`. El script crea una **copia** junto al original
(`X_MASTER.mp4` → `X_ligero.mp4`); el MASTER nunca se toca ni se borra, y el nombre de la copia no coincide con
`*_MASTER.mp4`, así que `verificar`, el panel y `yt subir` siguen usando el MASTER.

## Paso único

```
python .claude\skills\comprimir-video\comprimir.py <archivo | carpeta | alias> [--perfil P] [--mb N] [--res N] [--gpu]
```

Lánzalo con `run_in_background` (un video de 5-6 min a 1080p tarda unos minutos en CPU) y no lo vigiles:
espera la notificación. Al terminar imprime `antes → después (−%)`, resolución, kbps y tiempo.

| Perfil | Qué hace | Para qué |
|---|---|---|
| `ligero` (defecto) | H.264 CRF 23, misma resolución, audio 128 k | copia general que se ve igual (SSIM ≈ 0,98); −55 % sobre un MASTER de ~10 Mbps |
| `compartir` | H.264 CRF 25, 720p, audio 96 k | WhatsApp, correo, mandar a revisión |
| `minimo` | H.265 CRF 30, 720p, audio 64 k | lo más chico que aún se ve bien |
| `archivo` | H.265 CRF 22, misma resolución, audio 160 k | guardar masters en disco casi sin pérdida |

- **Tamaño exacto** (p. ej. límite de 100 MB de WhatsApp/Discord): `--mb 95` → dos pasadas que apuntan a ese peso.
  Si el usuario pide un peso concreto y pequeño, haz la cuenta antes: kbps totales ≈ MB × 8390 / segundos.
  Por debajo de ~2 Mbps usa `--perfil minimo --mb N` (H.265 720p): a 1080p H.264 se ve en bloques, sobre
  todo con texturas (guache, grano noir). Ej.: Egipto, 5:40 → `--perfil minimo --mb 45` (~1,1 Mbps):
  428 → 44 MB (−90 %), SSIM 0,964 a 720p; líneas y textos intactos, solo se suaviza el grano del papel.
  Noir con grano (Las 1.200, 15:47 → `--mb 125`): 4037 → 122 MB (−97 %), SSIM 0,91: líneas y textos bien,
  pero el grano de película desaparece y las sombras quedan lisas; si el grano importa, dale ~2× MB.
  Tarda ~5 min por cada 5 min de video (x265 dos pasadas); no lances dos a la vez (se frenan a 0,3×).
- **Verificar** (barato): SSIM de 30 s contra el MASTER escalado a la misma resolución
  (`ffmpeg -ss 120 -t 30 -i copia -ss 120 -t 30 -i MASTER -lavfi "[1:v]scale=1280:720[r];[0:v][r]ssim" -f null NUL`;
  ≥ 0,98 no se distingue, ≥ 0,95 aceptable) y un recorte lado a lado de 960x360 si es a peso fijo.
  Usa `--sufijo _<N>mb` para no pisar la copia `_ligero`.
- `--res 720` = lado corto (sirve igual para Shorts verticales: 720x1280). Nunca agranda.
- `--gpu` usa NVENC: 5-10× más rápido, un poco más pesado a igual calidad. **No con un render ni Chatterbox
  corriendo** (comparten la RTX 4060); sin `--gpu` solo usa CPU.
- `--codec`, `--crf`, `--audio`, `--sufijo`, `--sobrescribir` para ajustar a mano.
- Si la copia no baja al menos 5 % (el original ya estaba comprimido), no se guarda y lo avisa.

## Qué decirle al usuario

Ruta de la copia (como enlace), peso antes → después y el perfil usado. Si es para subir a YouTube, recuérdale que
**a YouTube se sube el MASTER** (YouTube recomprime; cuanto mejor la fuente, mejor queda), la copia ligera es para
compartir/revisar/archivar.

## Límites

- No borrar ni reemplazar el MASTER aunque la copia se vea igual; si el usuario pide liberar espacio, que confirme
  qué original se borra (borrar = preguntar).
- No comprimir mientras corre un render largo de `fab.py` (compiten por CPU); el panel nunca se detiene.
- Las copias no van a git (`videos/*/salida` ya es pesado y está fuera).
