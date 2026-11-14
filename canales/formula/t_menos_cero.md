# T Menos Cero (`t_menos_cero`) — fórmula

## Alta del 14-nov-2026 (canal nuevo, 0 subs)
- **Hueco con datos (NexLev, 13-nov):** en español no hay explicadores animados de cohetes de calidad (tipo Primal Space / The Space Race).
  Referencias: Control de Misión «Artemis II» 3,6 M (7,1×), «Soyuz 11» 2,6 M (5,1×), «Losetas de Starship» 57 K en un canal de 2,3 K subs (23×);
  en inglés The Space Race «The Real Reason Starship Has 33 Engines» 1,9 M (4×), CNET recap del vuelo 14 de Starship 2,2 M (25×).
- **Títulos que ganan:** «La verdadera razón por la que…», «¿Qué pasó EXACTAMENTE…?», «Todo lo que necesitas saber…», cohete/misión con nombre + 1 palabra en MAYÚSCULAS.
- **Duración:** 9-22 min en los que rinden; arranque con ~12 min.
- **Ejes:** (1) noticia de un vuelo explicada en 3D a los 3-5 días (mayor multiplicador); (2) explicadores atemporales (motores, escudo térmico, reentrada);
  (3) historias de fallos (Apolo 13, Challenger, explosiones).
- **Formato visual:** kit LÍNEA 3D + video real de la misión con capas encima + diagramas; a veces 3D solo. Ejemplo corto: `videos/cohete_crs30/`.
- **Nombre:** «T Menos Cero» (@TMenosCero): la cuenta regresiva, igual que el reloj T+ del HUD. «Ignición» y «Telemetría» ya estaban tomados.

## Registro a 7 días
- `starship_vuelo15` TJvawxDLQnE (10:10), publicado 14-nov ~17:30 CDMX a mano por el usuario. Medir el 21-nov.

## Revisión del usuario del 1.er video (14-nov-2026)
«Estuvo bien el video.» Mejora para TODOS los siguientes: más VIDEO REAL (la explosión del B22 en el mar, las capturas anteriores
cuando la voz las menciona) y fotos/pegatinas como en Tamriel/Warcraft/Runa pero con el kit de línea 3D. Regla en `docs/estilo_linea3d.md` § «REGLA: más video real».

## En curso (14-nov-2026, 11:40 CDMX): 1.er video = vuelo 15 de Starship (~12 min), alias propuesto `starship_vuelo15`
- Hecho: modelos 3D en `nucleo/linea3d_starship.py` (super_heavy 33 motores/3 aletas, nave con flaps y escudo, pila, torre_captura con
  palillos `apertura`/`z_brazos`, mesa_lanzamiento); prueba en una hoja (la vista de la nave desde abajo sale revuelta: arreglar al hacer las tomas).
- Datos comprobados (Wikipedia «Starship flight 15», tabla de SpaceX): despegue 13-nov 22:47:36 UTC desde Pad 2 de Starbase; B22 + Ship 42
  «Don't Panic», Block 3; 26 Starlink V3; Max Q T+58 s, MECO T+2:19, hot staging T+2:21, boostback T+2:26-3:02 (27 de 28 motores),
  quema de aterrizaje T+6:10-6:35, captura del booster ABORTADA (desvío al mar por poco combustible según Musk; el texto dice GNC) y
  pérdida de integridad antes del agua; SECO T+8:09; órbita ~275 km, 30,5°, ~14 vueltas; deorbit T+21:35:57; captura de la nave
  planeada T+22:32:34 (≈ 21:17-21:20 UTC del 14-nov = 15:17-15:20 CDMX). Fuentes en space.com (live 14-nov) y Wikipedia.
- Falta, en orden: (1) tras las 15:45 CDMX buscar el resultado de la captura de la nave; (2) `python fab.py nuevo starship_vuelo15`;
  (3) guion de ~12 min según el resultado (alternar 3D puro / diagramas / video real de SpaceX con capas / combinado; reloj T+ con
  la tabla oficial); (4) voz Alberto, video real con yt-dlp, MASTER, miniatura Flow, subir a `t_menos_cero` (ya conectado y verificado).

## Siguiente video (propuesto el 14-nov-2026, hueco sáb 21-nov)
Sin lanzamiento grande del 18 al 25-nov (solo Ariane 6 Leo NET 23-nov). Explicadores atemporales montados en la ola del vuelo 15 (`fab.py ideas`):
1. **«¿Por qué Starship NO tiene patas? La verdadera razón de los palillos»**: ref. Everyday Astronaut «The Genius Reason Why SpaceX
   Deleted A Grid Fin» 1,34 M (×2,9) + The Space Race «The Real Reason Starship Has 33 Engines» 1,99 M (×2,0); clips de TODAS las capturas
   (B12 vuelo 5, B13, B14…, S42) y de las patas del Falcon 9. (Recomendado.)
2. **«Todas las veces que Starship EXPLOTÓ… y qué aprendió SpaceX»**: ref. Scientia Plus «Booster Collapse» ×10,6, HotCut corto ×2,6; casi todo video real.
3. **«18 000 losetas: cómo Starship sobrevive a 1 400 °C»**: ref. «Losetas de Starship» 57 K en canal de 2,3 K subs (×23, en español).
