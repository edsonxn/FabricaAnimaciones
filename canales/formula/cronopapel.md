# Fórmula de Cronopapel — qué funciona y por qué
_Documento vivo (procedimiento: `docs/que_funciona.md`). Última revisión: 17-oct-2026, antes de `historia_mexico`._

## Fórmula vigente (repetir en cada video)
- **Tema:** la historia completa de un país o imperio muy buscado en español (España, México, Rusia, Israel, Roma, Egipto), contada de principio a fin sin saltarse épocas. Evidencia propia: `historia_espana` (309 vistas, ×1,28 de la mediana del canal, 46 % visto a 10 días) frente a `historia_china` (174 vistas, ×0,72, 55 % visto). Evidencia de fuera: «La Historia de México en 10 Minutos» (CRONOVIVO, 26 subs, 2.034 vistas = **×17,61**), «2000 Años de Historia de Israel en 10 Minutos» (Historia Animada Studio, 991 subs, 142.777 vistas = **×512,66**), «RUSIA de vikingos a Putin en 1000 años» (**×61,41**), «La Historia de España en 2 Minutos» (En Resumen TV, **×63,2**).
- **Título:** «La historia de <PAÍS> en 5 minutos» (directo, con promesa de tiempo corto y palabra clave al inicio). Evidencia: España en 5 min (×1,28 propio) y el patrón «Historia de X en N minutos» que se repite en 4 canales chicos distintos (Historia Animada Studio, CRONOVIVO, Cronaria, En Resumen TV).
- **Miniatura:** mapa pintado a guache del país con relieve, 2-3 personajes icónicos de distintas épocas enfrentados o flanqueando el mapa, y rótulo grande («5 MINUTOS» / «3.000 AÑOS») en alto contraste. Evidencia: `historia_espana` y `historia_egipto` v2 (miniaturas por código sobre el propio motor de boceto+guache).
- **Gancho (primeros 20 s):** contraste geográfico y civilizatorio inmediato sobre el mapa en movimiento (un territorio por el que pasaron imperios o donde chocaron dos mundos + una cifra o legado que llega hasta hoy + «Esta es la historia de X, en cinco minutos» con cronómetro y estampado del país).
- **Estructura y estilo visual (`docs/estilo_boceto_guache_mapa.md` v2.1):** plano secuencia continuo sobre mapa Mercator con relieve real NOAA ETOPO1, ríos de Natural Earth, territorios translúcidos que crecen/fracturan (Voronoi o fronteras reales) y **alta densidad**: al menos un dibujo de boceto nuevo y movimiento en cada frase (ningún tramo > 1,5 s con el mapa solo), contador de años arriba a la izquierda, sellos de época con emblema dibujado arriba a la derecha y barridos procedurales (`trans.py`) entre épocas. Voz: Dan (`Chatterbox`) + música Lyria instrumental épica + SFX puntuales con sentido.
- **Distribución:** búsqueda + sugeridos en el nicho hispanohablante (México y España son los dos países con mayor volumen de búsqueda en español).

- **Dibujos = pegatinas de Flow (desde 22-oct-2026, aprobado por el usuario con `historia_jalisco`)**: hojas por época con los dibujos del kit como ingrediente; mismo trazo, mucho más rápido y con más detalle. Ejemplo a copiar: `videos/historia_jalisco/`.

## Evitar
- Videos demasiado cortos (< 3:30) o con poca densidad visual: `historia_china` (3:11, ×0,72) tuvo menos alcance que `historia_espana` (5:13, ×1,28), y `historia_egipto` v1 fue rechazada en revisión por tramos con el mapa solo y bordes rectos.
- Sonidos «pop» automáticos en cada pegatina (saturaban la mezcla; desde `historia_egipto` v2 los SFX se ponen solo donde significan algo).

## Hipótesis a probar (una por video)
1. `historia_mexico` (subida en privado 17-oct; hueco lun 26-oct 14:00 CDMX): **tema del país principal de la audiencia del canal (México, `pais: MX`)** manteniendo intacta la fórmula v2.1 de 5-6 min (`historia_espana` / `historia_egipto` v2: relieve ETOPO1, ~150 dibujos, 14 escenas, sellos por época). Referencia externa: CRONOVIVO (26 subs) logró **×17,61** (2.034 vistas) con «La Historia de México en 10 Minutos». Si supera las 309 vistas de España a 7 días, confirma que los países hispanos lideran la tracción del canal.
2. Siguiente: «La historia de Rusia en 5 minutos» (×61,41 en Historia Animada Studio y ×13,52 en Animated History Español) o «La historia de Roma en 5 minutos» (×10,5 en CRONOVIVO; ya tenemos `historia_roma` listo para programar tras México).

## Registro (llenar a los 7 días con `yt videos` + `yt metricas`)
| video | publicado | formato | variable probada | 7 días | lectura |
|---|---|---|---|---|---|
| `historia_china` (4Hc-DNPgiRM) | 30-sep | historia_pais_3m | base 3 min | 174 vistas (×0,72), 55 % visto | buen % visto, pero 3 min queda corto frente a 5 min |
| `historia_espana` (eSMFJWNy5IA) | 7-oct | **historia_pais_5m** | duración 5 min + relieve v2 | **309 vistas (×1,28), 46 % visto** | **supera a China (+78 % vistas); formato base** |
| `historia_japon` (EI0c27EY89E) | 14-oct | historia_pais_5m | país asiático en 5 min | medir el 21-oct | en maduración |
| `historia_iran` (CqSg_v6pFjQ) | 18-oct (prog.) | historia_pais_5m | Persia/Irán 5 min | medir el 25-oct | |
| `historia_egipto` (R1LQTkRiwzI) | 22-oct (prog.) | historia_pais_5m | densidad v2.1 (~150 dibujos) | medir el 29-oct | |
| `historia_mexico` (BZd71Z5BIrk) | 17-oct (privado) | historia_pais_5m | país propio de la audiencia (MX) | pendiente (tras publicar) | |
| `historia_jalisco` (SiA13ZlBK5A) | 3-nov (prog.) | historia_pais_5m | estado de MX + pegatinas de Flow (4:30) | medir el 10-nov | aprobado por el usuario el 22-oct |
