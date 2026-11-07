# Estilo ANIME VIVO (6-nov-2026)

Drama adulto en anime hecho con IMÁGENES de Flow (Nano Banana, 0 puntos) y animación limitada por código. Nació con
`videos/llamada_anime/` (remake de «Llamada de domingo» de LogIA cuando no había puntos de Flow para video). El
usuario aprobó el estilo en la tele («Sí, sigue así»).

## Por qué funciona
El anime de TV/cine ya es animación limitada: dibujos sostenidos, bocas de 2-3 posiciones, parpadeos, paneos sobre
fondos pintados, luz y polvo. Con una imagen por plano + sus ediciones se ve como anime de verdad, no como fotos.

## Receta (kit `nucleo/anime_vivo.py`, ejemplo `videos/llamada_anime/`)
1. **Fase A** — escenarios vacíos y retrato de cada personaje en la ficha anime (`flow_anime.py A`; ingredientes = los
   del proyecto original). FICHA: «Hand-drawn 2D anime feature film still, mature seinen drama…».
2. **Fase B** — un cuadro por plano (x2 variantes), ingredientes = A; «mouth closed in this frame». Elegir por hoja:
   cara grande en los planos con diálogo, ropa/personaje correctos.
3. **Fase E** — por cada toma que habla, 2 ediciones de la MISMA imagen («Edit this exact image… ONLY change: mouth
   open» y «eyes closed»), x2 = dos aperturas. El kit alinea (ECC), saca la máscara de cambio y la intercambia como cel.
4. **`tomas.py`** — una `Toma` por plano: cámara (push/pan), `mov` (respira / cabeceo al hablar / tiembla al llorar),
   efectos por escenario (rayos+polvo en interiores con sol, fluor en hospital, lluvia en autos, brillo de pantallas),
   labios por la envolvente del audio real; 2 hablantes = 2 tomas con corte en el silencio entre frases; videollamadas
   envueltas con la interfaz del original. Render en paralelo: **4 procesos** con 32 GB (6 se quedan sin memoria por x264);
   63 planos de 8-10 s ≈ 45 min. Si el proceso muere, relanzar: salta lo hecho y sobrescribe los `*.tmp.mp4` rotos.
5. **Ensamblar** — tramos por `beats.json`; planos de interfaz recortados del MASTER original; audio final intacto.

## Flow: lo que cambió el 6-nov-2026 (importante)
- Dominio `flow.google.com`; las miniaturas viejas y las del buscador de ingredientes son `/asb/<token>` (piden sesión;
  sin uuid). Las generaciones NUEVAS siguen saliendo en la galería con URL firmada de `flow-content` → `_bajar.py`.
- `img[data-media-id]` de la galería = uuid. Para usar una imagen generada como ingrediente: tile → «Más opciones» →
  «Añadir a la petición» (el buscador no sirve para ellas).
- Orden de la galería = orden de envío (los `Expires` crecen por par). Para ediciones, asignar POR CONTENIDO a su base
  (diferencia a 96×54), no por orden: fallos y reintentos lo desordenan.
- fetch a 127.0.0.1 y el portapapeles no funcionan desde la página; los datos grandes se pegan con javascript_tool.

## Errores a no repetir
- Enviar sin ingrediente (si el helper falla) genera basura y desplaza la cola: comprobar `__ningr()` antes del clic.
- Vestuario fuera de ficha (Lucía de luto salió en uniforme en 071): pedir la ropa en la acción Y en la ficha.
- En un REMAKE de otro estilo, los planos de interfaz (videollamadas, teléfono, laptop) no se recortan del MASTER viejo:
  traen fondos y retratos fotorrealistas que rompen el anime (`llamada_anime`, llamada final de «Papá»). Re-renderizar la
  interfaz con los retratos y fondos anime nuevos.
- Scripts con `print('✓')` y salida redirigida a un log: `sys.stdout.reconfigure(encoding='utf-8')` (cp1252 lo tumba).
