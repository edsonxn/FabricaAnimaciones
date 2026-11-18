# La tele: avisos, avances y decisiones en el Google TV (4-nov-2026)

Pedido del usuario: «que la fábrica pueda enviar videos a la tele, avances, montajes… y yo poder tomar decisiones desde la
tele, con botones, mientras se reproduce el avance o cuando termine».

## Regla (el usuario, 4-nov-2026): PRIMERO LA TELE, si no, la voz
«Cuando cualquier avance necesite mi supervisión o quiera mostrarme algo de la fábrica, que lo mande a la televisión. Y si
no está disponible en la televisión, que me lo mande en voz como era antes.»
- **Disponible** = la tele contesta en el 8730 **y** `"pantalla": true` en `/estado` (en reposo el Chromecast sigue en la
  red, pero nadie lo vería). `tele.disponible()`; `FAB_SIN_TELE=1` hace como si no estuviera.
- **Avance, MASTER, montaje, hoja o algo que revisar** → `fab.py tele video <v> … --pregunta … --esperar 900` (en segundo
  plano) o `tele tablero` / `tele imagen`. Si la tele no está, el comando avisa por voz en la PC («Hay algo de <v> para que
  lo revises… míralo en el panel») y sale con **código 4**: entonces el avance se enseña por el panel/chat como antes.
- **Avisos** → `fab.py avisar "…"`: va a la tele (y ya NO suena en las bocinas); solo si la tele no está, habla la PC
  (ElevenLabs, respaldo voz de Windows). Registro en `panel_avisos/avisar_log.txt` («en la tele: …» o «dicho (…)»).
- Una decisión que llegó por la tele vale como respuesta del usuario para ESE punto (queda en `ESTADO.md` con `--video`).

### Regla (el usuario, 17-nov-2026): los VIDEOS van a la tele SOLO si él lo pide (todos los videos)
«No la mandes a la tele… esa regla quítala… en todos los videos, para ahorrar tiempo… solo si te lo pido que la mandes a la
tele lo haces.» Sustituye la del 5-nov-2026 (todo render a la tele solo y sin preguntar), que queda ANULADA.
- Ni avances, ni montajes, ni el MASTER se mandan por iniciativa propia; tampoco se ofrece. El MASTER pasa de `final` directo a
  `verificar` y a la subida.
- Cuando él lo pida: `fab.py tele video <v> [avance|master|montaje]`. Un MASTER de > 1 GB la tele lo corta (WinError 10054,
  cod_villanos 17-nov): mandar una copia 720p (`ffmpeg -vf scale=1280:-2 -crf 27`) con `tele video <ruta.mp4>`.
- Avisos (`fab.py avisar`) y decisiones sin video siguen yendo a la tele como antes.

## Skill global «avisar-y-decidir» (4-nov-2026, CUALQUIER proyecto)
Pedido del usuario: todo aviso, información, imagen, video o decisión → a la tele si la está viendo (pantalla prendida);
si no, por las bocinas. `C:\Users\jaire\.claude\skills\avisar-y-decidir\SKILL.md` (los skills `avisar-por-voz` y
`avisar-por-tv` remiten a él). Se llama por ruta absoluta `python C:\FabricaAnimaciones\fab.py tele …` desde cualquier
cwd: `fab.py` pasa la carpeta de origen en `FAB_CWD` y las rutas relativas se leen desde ahí; fuera de la fábrica los
textos del respaldo por voz son genéricos («te lo dejo en la computadora», con la pregunta y sus opciones).
- **Decisiones**: `tele preguntar … --esperar 900` en segundo plano Y la misma pregunta en el chat; gana lo primero. Si
  contesta en el chat → `tele cerrar`: la app (1.261104.1317+) marca «cerrada» la pregunta quitada sin contestar y la
  espera de la PC suelta en segundos con código 3.
- `tele disponible` imprime sí/no (código 0/4). `preguntar --video <ruta.mp4>` acepta un archivo suelto.
- Probado el 4-nov desde `D:\Escaner`: disponible (sí; no con `FAB_SIN_TELE=1`), aviso, pregunta contestada en la tele
  (`RESPUESTA: Sí`) y pregunta cerrada desde la PC (código 3 en 3 s).
- Respaldo cuando la tele no está = **bocinas de la PC**, no WhatsApp (confirmado por el usuario el 4-nov-2026).

## Niveles, bandeja, sala de revisión y tablero (4-nov-2026, tarde)
Pedido del usuario: «controlar el nivel de notificaciones en la tele, por capas, y no molestar para ver una película»;
«revisar los videos marcando momentos con el control»; «cuando no use la tele, la fábrica y CNB como protector».
- **Modo de la tele** (lo elige él en Puente TV › Avisos; `fab.py tele modo` lo lee o cambia): 🔔 Todo · ⭐ Normal (por
  defecto) · 🚨 Solo urgentes · 🌙 No molestar (hasta que lo quite / 2 h / mañana 8:00; «urgentes en la esquinita» opcional).
  Cada aviso trae `nivel` (urgente | importante | info) y `origen` (fabrica | cnb | claude | puente) y la tele decide:
  **completo** (pausa + robot), **banner** (esquina, sin pausar, 8 s) o **bandeja** (en silencio). Tabla en `Ajustes.kt`
  (y copia en `tele._entrega_probable`, para no pedir voz a ElevenLabs si no va a sonar). Por origen: normal / más bajito /
  silencio. `fab.py avisar` manda `importante` (= banner en Normal). **Bandeja = no se repite en las bocinas.**
- **Preguntas** salen en Todo y Normal; en los otros modos quedan en la bandeja y `tele preguntar`/`revisar` salen con
  **código 5 (POSPUESTA)**: preguntar en el chat. No se sube el video si va a posponerse.
- **Sala de revisión**: `fab.py tele revisar <v> [avance|master|montaje] [--esperar 3600]` o `--archivo x.mp4`. En la
  tele: OK pausa, ◀ ▶ 10 s, ▼ marca (Error, Audio, Imagen, Texto, Cortar, Me gusta), ▲ lista (saltar/borrar), Atrás o el
  final = resumen con veredicto. Deja `videos/<v>/revision/REVISION_<fecha>.md` + `marca_*.jpg` (un cuadro por marca)
  y una línea en `ESTADO.md`. Si no se esperó: `tele revisar-resultado <id> <v>`.
- **Tablero** (protector de pantalla): `Tablero` (DreamService) en la tele con la página que manda la PC por
  `POST /tablero {"url"}` (servidor `D:\PuenteTV\tablero`, puerto 8741). Puesto por ADB el 4-nov:
  `settings put secure screensaver_components com.puente.tv/.Tablero` (antes: `com.google.android.apps.tv.dreamx/.service.Backdrop`;
  para volver al de Google, poner ese). Sin root no se puede forzar a arrancar: `fab.py tele tablero --vivo` lo abre a
  pantalla completa (Atrás sale). Sin página, respaldo con reloj y bandeja.
- **Sin protector mientras algo suena** (1.261104.1939, 4-nov noche): Xuper y otras apps reproducen sin pedir pantalla
  encendida y a los minutos entraba el protector. `PuenteService.mantenerDespierta()` revisa cada 20 s: si otra app está
  en PLAYING (sesión multimedia) o suena audio, y la tele está prendida, sostiene un wake lock de pantalla (vence en
  60 s, `ON_AFTER_RELEASE`). `/estado` → `"sin_protector": true` mientras lo sostiene.
- **CNB** (`C:\CNB\scratch\alarma.py`): los avisos del vigilante van primero a la tele con `origen: cnb` y la voz de la tele
  (no ElevenLabs); cliente = importante, señal de compra/pago/precio = urgente, respuesta automática = info.
- API nueva: `GET/POST /modo`, `GET /bandeja`, `POST /bandeja?accion=vistos|vaciar`, `GET/POST /tablero`,
  `POST /tablero/ver`, `POST /pregunta` con `"modo":"revision"` (la respuesta trae `marcas[]`); `/estado` agrega `modo`,
  `no_molestar_hasta`, `bandeja`, `tablero`, `tablero_activo`.

## Piezas
- **Tele**: Google TV «Cuarto Zyan y Edson» (Chromecast con Google TV, 192.168.0.187) con la app **Puente TV**
  (`D:\PuenteTV\tv`, Kotlin). Servidor HTTP en el **8730**; la PC la encuentra sola por UDP en el 8731 («PUENTE?»).
  Encima de lo que se vea dibuja un robot que habla, pausa YouTube/Netflix y lo reanuda al terminar.
- **App de la PC** `D:\PuenteTV\pc` (PuenteTV.exe, bandeja): ventana para mandar avisos a mano y **actualiza la tele sola**.
- **Fábrica**: `nucleo/tele.py` (`python fab.py tele …`) le habla a la tele DIRECTO (no necesita PuenteTV.exe); la voz sale
  de ElevenLabs (Alberto Rodríguez, `eleven_v4_turbo`, cuentas de `tts_eleven`, caché `panel_avisos/tele_*.mp3`); sin
  saldo, habla la voz de la tele. IP recordada en `nucleo/datos/tele.json`.

## Comandos
```
python fab.py tele                                   ¿está la tele? qué se ve, permisos, espejo
python fab.py tele disponible                        sí/no (código 0/4): contesta y la pantalla está prendida
python fab.py tele aviso "texto" --titulo T --estilo info|importante|urgente|listo [--no-pausar] [--sin-voz]
python fab.py tele video <v> [avance|master|montaje|escena <id>]     sin nada = lo más nuevo (MASTER > AVANCE_ligero > AVANCE > montaje)
python fab.py tele video <v> avance --pregunta "¿Lo subo?" --opciones "Sí, súbelo|Rehacer el gancho|Después" --momento final --esperar 900
python fab.py tele preguntar "¿Qué tema sigue?" --opciones "A|B|C" --mensaje "…" [--video <v>|<ruta.mp4>] --esperar 900
python fab.py tele tablero                           foto de los videos en curso (canal, etapa, voz/mezcla/MASTER/YouTube, qué sigue)
python fab.py tele imagen hoja.jpg --segundos 15 --titulo "Hoja del gancho"
python fab.py tele respuestas | cerrar
```
- **montaje** = el «🎞 Montaje» del panel hecho video: cada escena de `timeline.json` (escena fluida o borrador de
  `fab.py <v> montaje`, negro si falta) a su duración, en orden, con `audio/final.wav` (o la voz) encima →
  `previews/montaje/_tele.mp4` 720p (se rehace solo si algo cambió). Así el usuario lo ve con audio, como pide la regla.
- **Preguntas**: `--momento final` = ve el video entero (OK pausa, ◀ ▶ 10 s, Atrás salta a la pregunta) y al final el robot
  dice la pregunta con botones + «Ver otra vez»; `durante`/`siempre` = barra abajo con ⏪ ⏯ ⏩ y los botones mientras se ve.
  Atrás en la pregunta = «después» (estado `cerrada`); sin respuesta en 15 min se cierra sola.
- **Respuesta**: `--esperar N` bloquea y devuelve código 0 con `RESPUESTA: <opción>` (3 = sin respuesta). Lánzalo en
  segundo plano (`run_in_background`) y sigue trabajando: la notificación llega cuando el usuario contesta. Queda en
  `nucleo/datos/tele_respuestas.jsonl` y, con `--video <v>`, una línea `- tele: … → **opción**` al final de su `ESTADO.md`.
- **`fab.py avisar`** manda el aviso a la tele si está disponible y entonces no suena en la PC (`"espejo_avisar"` en
  `nucleo/datos/tele.json`; `"pausar_avisos": true` = pausa lo que se ve, elegido por el usuario el 4-nov-2026).

## Cuándo usarla (Claude)
- Avance o MASTER listo para revisión → `tele video <v> avance --pregunta … --esperar 900` en segundo plano además del aviso.
- Decisiones cortas (tema, subir sí/no, qué rehacer): 2-4 opciones de 1-4 palabras; nunca preguntas abiertas.
- No saturar: una pregunta a la vez (se encolan), nada de madrugada, nada por detalles menores.
- Videos > ~700 MB tardan en subir por wifi: preferir `*_AVANCE_ligero.mp4` o el montaje.

## API de la tele (para otras herramientas)
`GET /estado` · `POST /aviso` (JSON: titulo, mensaje, estilo, pausar, audio_b64, voz_tv, duracion) ·
`POST /video?nombre=x.mp4` (binario) o JSON `{"url"}` · `POST /imagen?segundos=&titulo=` ·
`POST /archivo?nombre=x.mp4` → `{"archivo":"archivo_0.mp4"}` · `POST /pregunta` (JSON: id, titulo, mensaje, opciones[],
estilo, momento, archivo, audio_b64, voz_tv, espera) · `GET /respuesta?id=` → `{estado: pendiente|mostrando|respondida|cerrada,
opcion, indice}` · `GET /respuestas` · `POST /cerrar[?todo=1]` · `POST /control?accion=pausar|reanudar` · `POST /actualizar` (APK).

## Cambiar la app de la tele
`cd D:\PuenteTV\tv` → `JAVA_HOME="/c/Program Files/Android/Android Studio/jbr" ./gradlew assembleRelease` → copiar
`app\build\outputs\apk\release\app-release.apk` a **`D:\PuenteTV\PuenteTV.apk`**: PuenteTV.exe ve el cambio y se lo manda;
la tele se instala sola en ~15 s (`GET /estado` → `version` nueva). No actualizar mientras la tele muestra una pregunta
(la app se reinicia y la pregunta se pierde).
