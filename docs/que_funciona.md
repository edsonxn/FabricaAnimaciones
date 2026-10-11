# Qué está funcionando y por qué (TODOS los canales)

_Pedido del usuario (11-oct-2026): antes de cada video nuevo se revisa qué está funcionando y POR QUÉ, para repetir la
fórmula en los siguientes y mejorar poco a poco. No basta la tabla de `ideas`: hay que llegar a una explicación y
dejarla escrita. Primera aplicación: Wild Next Door (`canales/formula/wild_next_door.md`)._

## Cuándo
- **Antes de proponer el tema de cada video nuevo**, en cualquier canal. Toma ~10 min y ~400 de cuota.
- **A los 7 días de publicar cada video** (y otra vez a los 28): se mide y se anota el resultado en el registro de la
  fórmula del canal.

## Dónde queda: `canales/formula/<alias>.md` (uno por canal, versionado en git)
Es un documento vivo y corto (≤ 80 líneas) con 4 partes. Si no existe, créalo copiando `canales/formula/wild_next_door.md`.
1. **Fórmula vigente:** lo que se repite en cada video (tema, título, miniatura, gancho, estructura, duración), cada punto
   con su evidencia («ciempiés 440 vistas en 2,5 días vs 2-3 de los demás»).
2. **Evitar:** lo que ya se probó y no funcionó, con su evidencia.
3. **Hipótesis a probar:** UNA variable por video (otro tipo de título, una lista, otra duración…).
4. **Registro:** una fila por video: fecha, formato, variable probada, resultado a 7 días (vistas, × mediana, % visto,
   fuente principal) y lectura en una línea.

## Pasos
1. **Lo tuyo.**
   - `python fab.py yt videos <alias>` da las vistas al momento. Las de Analytics llegan con 2-3 días de retraso, así que
     un video de esta semana solo aparece aquí.
   - `python fab.py yt metricas <alias> 90` da el % visto, la curva de retención, las fuentes de tráfico (sugeridos,
     búsqueda, exploración) y las búsquedas que te encontraron.
   - **Compara videos que salieron en las mismas condiciones** (misma semana, mismo estilo, misma voz). Si uno se dispara,
     la diferencia está en el tema o el empaque, no en la producción.
   - Mira la fecha REAL de publicación en `yt videos`: un video puede haber salido antes o después de lo programado.
2. **Fuera.** `python fab.py ideas <alias>` (`--actualizar` si el informe tiene más de una semana). De ahí salen los 3-5
   atípicos con mayor × y que sean replicables (canal chico, mismo nicho).
   - **El mismo tema despegando en ≥ 2 canales distintos = la señal fuerte está en el TEMA.**
   - Un solo canal que lo repite con éxito (p. ej. «Every bug in your X explained» ×5 a ×20) = la señal está en el FORMATO.
3. **Mirar el empaque.** `python nucleo/hoja_miniaturas.py canales/metricas/minis_<alias>.jpg <ids tuyos> <ids de fuera>`
   y mírala con Read. Compara títulos (palabras que se repiten: «Never Kill», «Why you should never…», «Explained»),
   duración y si la miniatura es dibujo o foto, la frase en pantalla, la flecha y cuántos sujetos lleva.
4. **Mirar el gancho y la estructura del mejor atípico.** Usa la transcripción con la herramienta de Nexlev
   `get_video_transcript` (barata; NO la de «watch», que es cara). El resultado sale en un archivo JSON: saca los primeros
   2 min completos y una línea por minuto del resto. Ejemplo en PowerShell: `ConvertFrom-Json` sobre el archivo y luego
   `.transcript | Where-Object { [int]$_.startMs -lt 120000 }`. Fíjate en:
   - Cómo abre: segunda persona, una escena concreta, cuándo llega el giro.
   - Cómo alterna los bloques: consejos, datos raros, mito, cliffhanger.
   - Cómo cierra.
   - La descripción del video suele traer los capítulos y la lista de lo que promete.
5. **Explicar el POR QUÉ en 5 ejes**, cada uno con su evidencia (si un eje no tiene evidencia, dilo):
   - **Tema:** qué sujeto concreto, qué miedo o curiosidad toca.
   - **Empaque:** título y miniatura.
   - **Gancho:** los primeros 20 s.
   - **Estructura:** el ritmo del cuerpo, cuándo se renueva la curiosidad.
   - **Distribución:** de dónde vienen las vistas. Sugeridos = un tema que ya es viral fuera te arrastra. Búsqueda = la
     gente lo pregunta.
6. **Escribirlo** en `canales/formula/<alias>.md`: actualiza la fórmula, lo que hay que evitar y la hipótesis siguiente.
7. **Proponer al usuario** 3 temas que repitan la fórmula, cada uno con su referencia y su ×. Cada propuesta cambia UNA
   sola variable a la vez (si cambias tres, no sabrás cuál funcionó). Las escenas siempre son nuevas, nunca recicladas.
8. **Al subir:** pon `"formato": "<nombre>"` y `"prueba": "<la variable que se probó>"` en `publicados` de
   `canales/<alias>.json`.
9. **A los 7 días:** mide (`yt videos` + `yt metricas`), llena la fila del registro y decide: la hipótesis se queda en la
   fórmula o pasa a «Evitar».

## Cuidados
- **Los canales son chicos:** de 1 a 5 videos son pistas, no leyes. La señal de fuera (varios canales) pesa más que la
  propia, hasta que lo tuyo repita un resultado.
- Compara vistas por día y × de la mediana del canal, no vistas totales. 132 mil vistas en un canal de 480 subs dicen
  más que un millón en uno de 5 millones.
- Analytics llega tarde y no trae datos demográficos con pocas vistas. Para lo reciente usa `yt videos`.
- La conclusión va siempre con su número. Nada de «parece que gusta» sin un dato al lado.
