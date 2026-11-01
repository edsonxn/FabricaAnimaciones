---
name: actualizar-canales
description: Pone al día el registro de los canales de YouTube de la Fábrica de Animaciones contra lo que hay realmente en YouTube. Úsalo SIEMPRE que el usuario diga "actualiza los canales", "actualiza el canal X", "ya tiene nuevo video", "ya subí/publiqué un video", "pon al día los canales", "qué cambió en los canales" o algo equivalente. Detecta videos nuevos, los que salieron públicos, los reprogramados y los borrados en Studio, los registra en canales/<alias>.json, BITACORA.md y el ESTADO.md del video, y dice qué canal urge y qué videos esperan fecha. Solo lectura sobre YouTube; nunca publica ni programa por su cuenta.
---

# Actualizar los canales

Proyecto `C:\FabricaAnimaciones`. Contexto: el usuario sube, programa, publica o borra videos directamente en
YouTube Studio (o en otra sesión) y el registro local queda atrasado. Este skill lo alinea. **Todo se hace sin
preguntar** porque es solo lectura en YouTube y bookkeeping local; lo que NO se hace sin que él lo pida está en
«Límites».

Alias de canal: `bitacora_perdida`, `cronopapel`, `edsonxn`, `kuriox`, `logia`, `pieza_oculta` (Plastitube),
`sapiens_con_wifi`, `wild_next_door`. Si el usuario nombra un solo canal, trabaja solo ese (`diferencias.py <alias>`).

## Pasos

1. **Datos frescos** (solo lectura, ~15 s):
   `python fab.py canales --actualizar` → tabla con el primer hueco sin video de cada canal y qué hay en producción.
2. **Diferencias YouTube ↔ registro** (solo lectura):
   `python .claude\skills\actualizar-canales\diferencias.py [alias ...] [--dias 14]`
   Imprime por canal:
   | Marca | Significa | Qué registrar |
   |---|---|---|
   | `NUEVO` | subido en los últimos `--dias` días y no está en `publicados` (con la carpeta `videos/<v>` probable) | entrada nueva |
   | `SALIÓ` | ya es público y el registro lo daba por privado/programado | `visibilidad: "public"` + `publicado: <fecha>` |
   | `CAMBIO` | privado/programado con otra fecha, o volvió a privado | alinear `programado`/`visibilidad` |
   | `BORRADO` | id registrado que ya no existe (el usuario lo borró en Studio) | `visibilidad: "borrado"` + nota |
   | `DUPLICADO YA BORRADO` | id de `duplicados_para_borrar` que ya no existe | quitarlo de esa lista |
   | `SIN PROGRAMAR` | privados registrados sin `publishAt` | no se toca: se avisa y se sugiere hueco |
3. **Registrar cada hallazgo** (solo archivos locales):
   - `canales/<alias>.json` → `publicados` (campos: `video`, `id`, `titulo`, `subido` = `snippet.publishedAt`,
     `visibilidad`, `programado`/`publicar` si hay fecha, `publicado` si ya salió, `hueco_sugerido` si está
     privado sin fecha, `formato` si el canal lleva fórmula en `canales/formula/<alias>.md`, `nota`).
     Un mismo id puede aparecer dos veces (subido → programado): manda la **última** entrada.
   - `videos/<v>/ESTADO.md`: id de YouTube, visibilidad, fecha y el **comando exacto** del siguiente paso
     (quita frases viejas como «NO subido»).
   - `BITACORA.md`: §1 (decisiones abiertas si cambió algo), §2 (la fila del calendario: «Programado» → «Público»,
     o fila nueva con el hueco sugerido), §3 (línea del canal) y **una línea con fecha al final** (qué se registró).
   - Un video que solo existe como MASTER local (ESTADO «TERMINADO», sin id en YouTube) NO es «nuevo»: se menciona
     y nada más.
4. **Verificar**: repetir el paso 2 (debe decir «sin diferencias» salvo los `SIN PROGRAMAR`) y
   `python fab.py canales` (el video registrado ya no aparece «en producción»).
5. **Responder corto, en español**: qué cambió (una línea por video con su id), la tabla de canales (cuál urge
   primero y por qué), y los privados sin programar con **hueco sugerido y comando**. Cierra preguntando si los
   programa; no lo hagas tú.

## Hueco sugerido para un privado sin programar
Último programado/publicado del canal + `horario.ciclo_dias` (la columna «Sin video desde» de `fab.py canales`),
a la hora del canal (`horario.utc`, p. ej. Bitácora 20:00 UTC = 14:00 CDMX). Respeta `separacion_min_horas`
(48 h por defecto; LogIA 96, Wild Next Door 72) y la regla de **nunca dos videos del mismo canal el mismo día**.
Comando para el usuario:
`python fab.py yt publicar <alias> <id> private --programar <ISO UTC>`

## Límites (no los cruces sin que el usuario lo pida en esta conversación)
- No publicar, no programar, no cambiar visibilidad, no borrar nada en YouTube. «Súbelo en privado» no incluye fijar
  fecha. Lo único que escribe este skill son archivos locales.
- No lanzar `yt metricas`, `ideas --actualizar` ni `estadisticas --actualizar` (gastan cuota); si el usuario quiere
  el siguiente tema, es otro flujo (`python fab.py ideas <alias>` + `docs/que_funciona.md`).
- No commitear ni hacer push salvo que lo pida (el árbol ya trae muchos cambios sin confirmar).

## Trampas conocidas
- **Formato de los JSON**: casi todos `canales/*.json` están en CRLF (`logia.json` en LF). Para editar varios campos
  usa leer → modificar → `json.dumps(indent=2, ensure_ascii=False)` conservando el fin de línea; una entrada suelta
  se puede con Edit. Después `python -c "import json;json.load(open('canales/<alias>.json',encoding='utf-8'))"`.
- **Campos que cambian de canal a canal**: `visibilidad` (`public`/`private`/`programado`/`privado`), `publicar`,
  `programado`, `publicado` (fecha = ya es público), `estado`. El script ya los normaliza.
- **HTTP 401/410 en un canal** (pasó con LogIA): renovar el token (`canales/tokens/youtube_tokens_<UC…>.json` con
  `expiry_date` en 0) y repetir; un 410 al final de una subida puede ser subida completa.
- **Un video ya público no se puede reprogramar** por API (HTTP 400): ante la duda, privado + programado.
- Un video público antes de su fecha (pasó con el ciempiés) se registra como `SALIÓ` con nota
  («salió antes de lo programado») para que la métrica use la fecha real.
- **Plastitube** es el alias `pieza_oculta`. Wild Next Door va en inglés y lleva `formato` (`never_kill`…).
