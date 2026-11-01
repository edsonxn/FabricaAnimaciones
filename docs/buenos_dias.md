# «Buenos días»: Claude dirige la orquesta (el usuario, 12-oct-2026)

El usuario arranca cada día con «buenos días». Claude propone el plan del día (canal, tema, qué tramo, en qué cuenta) y lo ejecuta; el usuario mira los videos y da su veredicto. Objetivo: más videos buenos con menos tokens.

## 1. Al recibir «buenos días» (una sola sesión de gestión, barata)
1. `get_usage` → `python fab.py buenosdias --uso <cuenta> <semanal%> <5h%> <resetsAt>` (cuenta = parte local del correo del usuario de esa sesión).
2. `python fab.py buenosdias` (añade `--actualizar` si los datos de canales tienen > 1 día). No leas más archivos salvo el `ESTADO.md` del video elegido.
3. Responde con el plan en ≤ 12 líneas:
   - **Canal urgente** (ATRASADO o el primer hueco) y **qué hacer**: terminar un video en producción antes que empezar otro.
   - **Tema** si hay que empezar uno: los 3 candidatos salen de `canales/metricas/ideas/<alias>.md` + `canales/formula/<alias>.md` (no los inventes; si el informe tiene > 7 días, `fab.py ideas <alias> --actualizar`).
   - **Tramos del día** (cuántas sesiones, cuál primero) y **en qué cuenta** (la que tenga más margen semanal la producción pesada; la más gastada solo gestión).
   - **Qué necesito de ti** (mirar un video, una decisión, cerrar programas para el render).
   - Una línea de tokens: ritmo ×N del sostenible y la recomendación.
4. Pide el visto bueno con AskUserQuestion (plan recomendado primero) y arranca. Cada tramo de producción en **su propia sesión** («continúa el video X»), no en la de buenos días.

## 2. Encuesta tras cada video que el usuario revisa
Cuando el usuario ve un render (avance o MASTER), AskUserQuestion de 2-3 preguntas, nunca más:
- **Veredicto:** aprobado / ajustes menores / rehacer partes / rehacer todo.
- **Qué falló** (multiSelect): gancho o ritmo · calidad del dibujo/imagen · voz · música o sonido · tema/guion · nada.
- **Qué te gustó** (multiSelect, opcional, solo si aprobado o ajustes).
Luego: `python fab.py buenosdias --feedback <video> <aprobado|ajustes|rehacer> "<fallos; gustos; nota libre>"`. Si un mismo fallo sale 2 veces en un estilo, va a «hallazgos» de su `docs/estilo_*.md`.
Una vez por semana (lunes), 1 pregunta extra de estrategia: qué canal le importa más esta semana.

## 3. Las 3 cuentas Pro y el gasto
- Cada cuenta tiene su cupo semanal y de 5 h; `get_usage` solo ve la cuenta de la sesión. Anota cada cuenta el día que se use (`--uso`).
- **Cuenta agotada a mitad de tramo (13-oct-2026):** el usuario cambia de cuenta y escribe «continúa el video X»; la sesión nueva concilia con `fab.py continuar` (aviso «TRABAJO SIN REGISTRAR»). Anota la cuenta agotada con `--uso <cuenta> 100 <5h%> <resetsAt>` y reparte el plan del día con las otras (protocolo: `docs/sesiones.md` §6).
- Ritmo = semanal% / % de semana transcurrida. > 1,3 → aviso y solo lo urgente; < 0,7 en las 3 → hay margen ocioso.
- **Revisión mensual (día 1):** con `canales/uso_tokens.csv`, si el promedio de fin de semana de las 3 cuentas queda < ~60 %, proponer bajar a 2 cuentas; si 2 o más llegan a 100 % antes del reinicio, mantener 3 (o comparar con un plan mayor: precios actuales en claude.ai, no de memoria).
- Ahorros de proceso que siempre aplican: una tarea por sesión; no sesiones en paralelo sin necesidad; cerrar las terminadas; correcciones en lote; renders sin vigilancia (`avisar-por-voz`).
