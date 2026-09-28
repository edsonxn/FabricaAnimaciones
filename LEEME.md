# Fábrica de Animaciones — cómo usarla

## Abrir el proyecto
En la app de Claude (pestaña Code) abre la carpeta **C:\FabricaAnimaciones**. Claude leerá solo
`CLAUDE.md` (la guía) y sabrá cómo reutilizar todo lo construido.

## Cómo pedir un video nuevo (ejemplos)
- "Haz un video de 2 minutos: 7 datos del océano profundo, estilo **neón**, voz de Dan."
- "Video estilo **pizarra** explicando cómo funciona una vacuna, 90 segundos, voz de Gaia."
- "Otro como el de los 40 mil años pero de los egipcios, **doodle psicodélico**, 3 minutos."
- "Short vertical de 45 s estilo **recortes** sobre 3 curiosidades de los gatos."

Conviene decir: tema, duración, estilo, voz (cualquiera de `C:\chatterbox_voices`) y si quieres
escenas a medida (más trabajo y más detalle) o las genéricas (más rápido y barato).

Basta con decir "quiero hacer un video": Claude te preguntará para qué canal, revisará primero las
métricas del canal (qué videos retienen, de dónde llegan las vistas) y te propondrá temas y ajustes.

## YouTube (canal conectado: Sapiens con Wifi)
```
python fab.py yt canales                          # canales conectados
python fab.py yt metricas sapiens_con_wifi 90     # métricas de los últimos 90 días
python fab.py mi_video miniatura                  # miniaturas con el motor del video
python fab.py yt subir mi_video sapiens_con_wifi --publicar 2026-10-02T20:00:00Z   # subir programado (UTC)
python fab.py yt conectar                         # conectar otro canal (inicias sesión en el navegador)
```
Horario por defecto: miércoles a viernes a las 14:00 de CDMX (20:00 UTC), 1-2 videos por semana.
El nombre y la foto de perfil del canal solo se cambian en YouTube Studio.

## Estilos disponibles
| Estilo | Aspecto |
|---|---|
| `doodle_psicodelico` | marcador con stickers sobre fondos psicodélicos (el del video de 40 mil años) |
| `pizarra` | tiza blanca granulada sobre pizarra verde, rellenos pastel |
| `cuaderno` | bolígrafo azul en cuaderno rayado, rellenos acuarela |
| `neon` | contornos de neón brillantes sobre fondos oscuros synthwave |
| `recortes` | papel recortado con borde grueso y sombra, fondo kraft |
| `limpio` | vector plano sin temblor ni grano (explicativo/corporativo) |

## Comandos útiles (los usa Claude; también puedes correrlos tú)
```
python fab.py nuevo mi_video          # crea videos\mi_video desde la plantilla
python fab.py mi_video todo           # todo el pipeline de principio a fin
python fab.py mi_video estilos 12.5   # el mismo cuadro en los 6 estilos
python fab.py 40mil_anos final        # re-exporta el video terminado
```

## Qué hay dentro
- `videos\40mil_anos\salida\` → el video terminado (MASTER 1080p + subtítulos .srt).
- `videos\demo_cerebro\` → video corto de prueba hecho con la plantilla en estilo pizarra.
- `nucleo\` → el motor reutilizable. `API.md` → catálogo de todo lo disponible.
