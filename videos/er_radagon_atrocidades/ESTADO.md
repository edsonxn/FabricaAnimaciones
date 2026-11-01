# Las 5 peores atrocidades de Radagon QUE IGNORASTE — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: runa_caida · PUBLICADO (público) mié 14-oct-2026 11:18 CDMX (https://youtu.be/L0HTszG4ycM)
- estilo: secuencia_yt (gameplay de Elden Ring por beat; sin patrocinio) · voz Chatterbox Faraon → doc: docs/estilo_secuencia_yt.md
- etapa: publicado
- siguiente: subir salida/er_radagon_atrocidades.srt a mano en Studio · a las 48 h: `python fab.py yt metricas runa_caida 90` (retención vs Márika)

## Sesiones (plan de tramos · «continúa el video radagon» retoma aquí · protocolo docs/sesiones.md)
- alias: radagon, atrocidades de radagon, runa caída
- vista previa: NO (el usuario, 14-oct): MASTER directo, revisado con hojas de cuadros
- leer al empezar: docs/estilo_secuencia_yt.md (§ Tamriel = misma receta con Chatterbox), canales/formula/runa_caida.md
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | todo: guion, voz, clips, MG, Lyria, mezcla, render, revisión, miniatura, subida | ✅ 14-oct | el usuario pidió 1 sola sesión; MASTER 7:42 revisado 2 veces |

## Decisiones del episodio (14-oct-2026)
- duración ~6 min como Márika (×24,6, 5:54), NO el piso viejo de 12 min · 5 puestos · sin patrocinio
- voz Chatterbox `Faraon.mp3` (la de Edsonxn) · gema del canal · puente final a «Las 5 peores atrocidades de Márika» (KKxhcwon2kg)
- no repetir lo del video de Márika (exilio de Sinluz, gigantes, Morgott/Mohg, Cornudos, Cuchillos Negros)
- puestos: 5 invasión de Liurnia + pelo rojo de gigante · 4 Espadón de la Orden Áurea (era el de Rennala) ·
  3 gemelos «hijos de un solo dios» · 2 Radagon es Márika (bigamia, martillo) · 1 abandono de Rennala (huevo de ámbar, lobo rojo)

## Hecho
- guion verificado en Fextralife (lista de fuentes en el docstring de guion.py) · 1 227 palabras, 56 frases
- voz 56/56 (409 s; 5 frases reescritas porque «Radagon» al inicio salía «Dradagón»; intro_2 con toma 3 a mano) · 51 beats · video 7:22
- kit nuevo `nucleo/mg_er.py` · efectos.py (6 rótulos, 13 fichas con íconos reales, 3 MG) · 4 SFX (150 créditos)
- 51 clips: 14 rehechos tras las hojas (menús, guías con texto, mando de Xbox, miniatura de otro canal, 2 negros);
  estatua de Leyndell fijada en pHksdpT9Nyo@93/107 (se ve el mensaje «Radagon is Marika»)
- Lyria 3 tramos · mezcla −14,0 LUFS, voz/fondo 14,3 dB
- MASTER 7:42 (442,5 s + pantalla final) · CER medio 0,47 % · sin negros ni quietos (barrido a 2 fps) · miniatura Flow v1
- 2.º render tras revisar el 1.º: negro en 6:39 (clip 046 fundía a negro), mapa en 6:03 (042), «rota»→«Grota» (p1_11 reescrita)
- subido private con miniatura (L0HTszG4ycM) · registrado en canales/runa_caida.json (formato lista_5_atrocidades_que_ignoraste) y BITACORA

## Falta
- [ ] subtítulos: subir salida/er_radagon_atrocidades.srt en Studio (o `python fab.py yt conectar` con force-ssl)
- [ ] a los 7 días: comparar con Márika ×24,6 (1 081 vistas, 55 % visto) · `limpiar` cuando ya no haga falta

## Archivos clave
- `guion.py`, `beats.json`, `busquedas.json`, `fuentes.json`, `medios/`, `salida/creditos.txt`

## Lecciones de este video (solo lo no obvio)
- `while read … done <<EOF` con `fab.py bajar` dentro: yt-dlp/python se comen el stdin y la 2.ª vuelta lee basura como id →
  `bajar --q` sin ids rehízo LOS 51 beats. Se restauró todo desde medios/_respaldo/. Motor arreglado (--q/--url sin ids = error);
  en bucles usa `< /dev/null`.
- «Radagon» al inicio de frase sale «Dradagón»; «rota» tras coma salió «Grota»: palabra con R inicial tras pausa = riesgo.
- clips de cinemáticas/peleas pueden fundir a negro dentro del tramo: barrer el MASTER a 2 fps (media < 12) además de las hojas.
- tras `reajustar`, un beat que CRECE puede quedarse más largo que su clip: volver a bajar ese beat.

## Cierre (regla del 12-oct-2026)
- [x] subido (private), miniatura y registrado (`canales/runa_caida.json`, BITACORA) · [x] publicado por el usuario 14-oct 11:18 CDMX
- [x] HALLAZGOS documentados (docs/estilo_secuencia_yt.md § Runa Caída, CLAUDE.md tabla, memoria runa-caida-duracion-y-voz)
- Montaje con efectos exportado el 19-oct-2026 (`fab.py er_radagon_atrocidades fx montaje`: 19 tramos, 0 apoyos; panel 🎞 Montaje)
