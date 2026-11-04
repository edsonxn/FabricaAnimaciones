# EN VIVO: directo generado y editado en tiempo real (idea del usuario, 4-nov-2026)

Formato nuevo para Crónicas de Tamriel (y luego Warcraft/Runa): un directo que no se acaba. El usuario da un tema y la
fábrica genera video en tiempo real (clips del canal, pegatinas reales, avisos y fichas del kit del canal, narrador) con un
búfer por delante; desde una ventanita se cambia el tema y el video gira hacia él. Meta: en un directo de YouTube el público
vota el tema de los minutos siguientes. **Regla del usuario: debe parecer lo más posible un video del propio canal** (letra,
avisos, fichas y pegatinas del kit de Tamriel, no un estilo genérico). Voz por ahora: **voz de Windows** (OneCore Raúl
es-MX), nada de ElevenLabs para no gastar créditos.

```
python fab.py envivo [canal] [--tema "…"] [--modelo haiku|sonnet] [--voz Raul] [--abrir]
  pantalla (OBS: fuente de navegador, ?auto=1): http://127.0.0.1:8790/     control: http://127.0.0.1:8790/control
```
En el panel de vista previa: `.claude/launch.json` → «envivo».

## Cómo funciona (nucleo/envivo/)
- `servidor.py` Flask + despachador con **`GUIONISTAS = 2` llamadas a la vez** y búfer de `BUFER = 2` bloques (+1 en
  escritura). Cada bloque propone 2 `proximos` subtemas; cada guionista toma uno y sabe qué escriben los otros («EN
  PARALELO… no lo toques»). Los bloques entran a la cola en orden de despacho (`seq`). Cambio de tema desde el control =
  tira el búfer menos 1 bloque de **relleno** y corta las escrituras en curso; por votación = conserva 1 bloque marcado
  `conservado`. El primer bloque de un tema nuevo (o del arranque) es corto (4 frases) para que llegue antes. Todo lo
  dicho queda en `_sesiones/<fecha>/guion.jsonl` (para cortar después un video o Shorts del directo).
- `director.py` escribe cada bloque (6 frases, ~35-48 s de voz) con `claude -p` (suscripción, sin API de pago) desde carpeta
  vacía, sin MCP/hooks/CLAUDE.md, `MAX_THINKING_TOKENS=0` y `--effort low`; **sonnet por defecto** (ver «Medido»). Elige por
  frase: pegatina del disco o `buscar` en la wiki (Fandom), clip, etiqueta en español, aviso (`rotulo`) y 1 ficha de
  inventario con **negritas**. Opciones de votación. Nunca se despide ni vuelve a saludar (el directo no se acaba).
- `biblioteca.py` reutiliza lo que el canal ya tiene: `videos/tes_*/pegatinas` (+ `_rec` recortadas), `medios/scene-*.mp4`
  con el texto de `beats.json`, OST de `audio/ost`. Las pegatinas usadas salen del catálogo un rato (evita repetir).
- `voz.py` SAPI + voces OneCore (Raúl), un .wav por frase; su duración marca el cambio de imagen.
- `pantalla.html` canvas 1920×1080 con el kit de `mg_tes.py`: Bahnschrift Condensed (servida en `/fuente/`), humo negro
  difuminado, separadores con rombo, hueso/gris/sangre; avisos tipo «misión iniciada» arriba al centro; ficha de inventario
  arriba a la derecha; pegatinas carta / silueta / camafeo / legajo / grande (media pantalla; las fotos anchas se encierran
  dentro del cuadro); OST con ducking; votación abajo a la derecha. **Cambio de tema:** cada bloque lleva `ver`; lo precargado
  del tema viejo pasa a `relleno` (suena solo si el nuevo aún no está, nunca pantalla de espera) y en cuanto llega el
  bloque nuevo se salta a él en el siguiente cambio de frase. `control.html` = la ventanita (tema, sugerencias, votación
  simulada, pausa, guionista, registro).

## Probado (4-nov-2026)
Arranque, clips, pegatinas de los 5 estilos, fichas, votación (aviso «EL CHAT ELIGIÓ» → bloque conservado → «EL CHAT
DECIDIÓ», sin hueco). **Cambio manual verificado en pantalla** (traza de `seg/idx/siguiente` en el navegador): el bloque
precargado viejo pasa a relleno, el viejo sigue sonando sin hueco y el nuevo entra en el siguiente cambio de frase
(15:51:38 cambio → 15:52:05 listo → 15:52:06 al aire con haiku; desde la ventanita y con sonnet: 15 s). Acentos bien desde
`/control` y urllib (curl de Git Bash los manda mal).

## Medido (4-nov-2026)
- `claude -p` cuesta **~8 s solo de arranque**; con un guionista, 6 frases tardaban 23-35 s (haiku) para ~37 s de voz y el
  búfer se vaciaba (0 s). Con 2 guionistas en paralelo: **búfer 90-127 s** en régimen.
- **sonnet vs haiku** (mismo tema, sin «pensar»): sonnet 12-17 s por bloque (haiku 23-35 s) y **mucho mejor guion**: lore
  correcto y el sarcasmo del canal («un héroe nórdico con más fama que pruebas, como todo buen héroe»). Haiku metía errores
  (Paarthurnax en Alto Hrothgar; «en Skyrim no se pueden domar dragones», cuando Dragonborn deja montarlos; Numinex/Numidium)
  y se despedía a mitad del directo. → **sonnet por defecto**, haiku de respaldo. Ojo: gasta más plan (~1 llamada por bloque).

## En curso / pendiente
1. Probarlo con el usuario (OBS: fuente de navegador `http://127.0.0.1:8790/?auto=1`, 1920×1080; control en `/control`).
2. Directo de YouTube con votos del chat: leer el chat en vivo (`liveChatMessages.list` con el `liveChatId` del directo;
   ojo, gasta cuota) y contar «1/2/3» → `d.votar()`. Anotado en `docs/ideas_guardadas.md`.
3. Los subtemas en paralelo a veces se pisan (dos bloques sobre Numinex): el prompt ya pide personajes que no salgan en el
   bloque; vigilar.
4. Voz: OneCore Raúl por ahora; si el directo funciona, valorar una voz del canal.
