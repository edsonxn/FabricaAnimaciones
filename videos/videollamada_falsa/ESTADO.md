# La videollamada donde nadie era real — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: logia · PROGRAMADO sáb 10-oct-2026 10:00 CDMX (SNmr4gh5PkY; publishAt 2026-10-10T16:00:00Z, privado hasta la fecha). Ciclo del canal: cada 4-5 días
- estilo: noir → doc de estilo: docs/estilo_noir.md · ejemplo a copiar: videos/ia_noir/ (kit nucleo/noir*.py) + `comun.py` de este video
- etapa: SUBIDO EN PRIVADO a LogIA el 7-oct-2026 → https://youtu.be/SNmr4gh5PkY (MASTER 6:31, CER 0,0006, −14 LUFS; miniatura por código y .srt cargados)
- siguiente: el usuario lo ve y decide fecha → `python fab.py yt publicar logia SNmr4gh5PkY public --programar <ISO UTC>` (el anterior salió el 6-oct; hueco: jue 8 o vie 9, 14:00 CDMX = 20:00 UTC); al aprobarlo: `python fab.py videollamada_falsa limpiar`

## Hecho
- Tema: robo deepfake de Hong Kong (Arup, ene-2024, HK$200 M en 15 transferencias a 5 cuentas). Hechos y fuentes en el docstring de guion.py.
- Guion 53 frases, detective narrador, con CORCHETES de actuación de ElevenLabs (regla nueva: docs/voz.md § Corchetes, CLAUDE.md).
- Voz ElevenLabs «David» (0hh7H4ZVAtaGpm1VZyEN, pedida por el usuario), modelo eleven_v4, stability 0.5: 53/53 frases válidas
  (CER ≤ 0,011), 330,5 s de voz, ~600 créditos. `tiempo` ✓: 391,4 s a 84 BPM, GAP 0,5. Narración suelta: `previews/voz_completa.mp3`.
- Núcleo: `config.FRASES_TTS` (separa etiquetas), `tts_eleven.py` (v3/v4 + `VOZ_POR_FRASE` para personajes), `tts_select.py`, `tts_gen.py`;
  `noir_pers.Frontal` (gafas bien con zoom).
- 12 escenas (`esc_<id>.py`, 3-6 planos cada una): regla, mensaje, llamada, dinero, descubre, truco, manual, victima, sinrostro, senales,
  leccion, cierre. Kit propio en `comun.py`: Hong Kong (`hk_*`), `oficina_hk`, `Llamada` (rejilla con caras → máscaras), `espalda`,
  `monitor`, `luz_rect`, `banda` (rótulo fijo en pantalla, con luz propia), `fijo`. `esc_truco.mascara`, `esc_dinero.tache`.

## Falta
- [ ] que el usuario apruebe la voz (se le mandó voz_completa.mp3)
- [x] SFX de ElevenLabs para el drama (lo pidió el usuario): `fx_audio.py` → 16 sonidos en `sfx/`, 135 golpes en `audio/fx.wav` (437 créditos)
- [x] música Lyria en 3 tramos (`_lyria_segmentos.py todo`), `sfx`, `mezcla`; miniatura por código (`_miniatura.py`, «NADIE ERA REAL»); `youtube.json`
- [ ] opcional (lo ofreció el usuario): otra voz de ElevenLabs para un personaje con `VOZ_POR_FRASE` (añadir la frase al FINAL de una escena)
- [x] `final`, `verificar`, revisión del MASTER (hojas `previews/master_1.jpg` y `master_2.jpg`, un cuadro cada 3 s); se rehicieron
      277-289 s (celda) y 367-378 s (interrogatorio) por oscuros. Flojos conocidos, por si el usuario pide más: bahía sin agua visible
      (regla), lados negros en `senales.p_facial`; ningún clip de Pexels entintado (el estilo pedía ~35 %: aquí todo es dibujado)
- [x] subido en PRIVADO (SNmr4gh5PkY). Falta: que el usuario apruebe voz y video, y diga la fecha
- [ ] Chatterbox (`C:\googleimagenes\chatterbox_server.py --port 7171`) y Applio se cerraron a pedido del usuario para el render: no se relanzaron

## Cómo retomar (comandos)
```
python fab.py estado videollamada_falsa
python videos/videollamada_falsa/_prueba.py <escena> u1 u2 ... [--solo-hoja]   (tiempos locales; hoja previews/p_<escena>.jpg)
python videos/videollamada_falsa/_hoja_global.py 3               (un cuadro cada 3 s de todo el video)
python videos/videollamada_falsa/_parche.py                      (sustituciones exactas en las escenas; NO editar con PowerShell)
python videos/videollamada_falsa/_prueba_voz.py <modelo>         (compara modelos de ElevenLabs con corchetes)
```

## Archivos clave
- `guion.py` (VOZ eleven_v4 + corchetes), `timeline.json`, `escenas.py`, `basen.py`, `comun.py`, `esc_*.py`, `mundos.py`, `props*.py`

## Lecciones de este video (solo lo no obvio)
- eleven_v4 cuesta ~3,6 veces menos que eleven_v3 y también entiende corchetes; multilingual v2 no.
- Con `tomas=1`, `tts_gen.py --seeds 2 3` solo usa la primera semilla: una llamada por semilla.
- «David» es una voz inglesa: «quince» salió «quinze» en 3 de 4 semillas; la semilla 4 pasó.
- La voz salió a ~2,5 palabras/s: el primer guion (640 palabras) daba 4:50; se añadieron las escenas `manual` y `senales`.
- `Set-Content -Encoding UTF8` de PowerShell 5.1 mete BOM y rompe `comprobar` (ast): parches con `_parche.py`; limpiar con `_sin_bom.py`.
- `h.anillo` trabaja en PANTALLA: pasarle `h.tf(P)` y grosor × `h.zoom` (si no, se descuadra con la cámara).
- Rótulos: con empuje de cámara se salían del cuadro y en planos oscuros no se leían → `C.banda` (capa 0 + luz propia).
- `self.w("palabra")` busca desde la frase 0 y por prefijo: «secreto» casó con «secretos» de otra frase; usar `frase=`.
- `h.silueta = ((r, g, b), alfa)`, no un color suelto.
