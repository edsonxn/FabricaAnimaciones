---
name: analizar-uso-panel
description: Analiza cómo el usuario usa el panel de la Fábrica de Animaciones (clics, filtros, scroll, pestañas, controles que nunca toca) a partir de la bitácora de uso y propone una versión nueva de la interfaz mejor organizada. Úsalo SIEMPRE que el usuario diga "analiza mi uso del panel", "revisa cómo uso el panel", "mejora el panel con mi uso", "rediseña el panel", "propón una versión nueva del panel", "revisión de uso del panel" o algo equivalente. Lee nucleo/datos/uso_panel/, diagnostica con números, escribe una propuesta en nucleo/propuestas_panel/ (nunca pisa panel.html sin permiso) y la deja probable en el propio panel.
---

# Analizar el uso del panel y proponer una versión nueva

Proyecto `C:\FabricaAnimaciones`. El panel (`nucleo/panel.py` + `nucleo/panel.html`) lleva una **bitácora de interacción**
(`nucleo/panel_uso.js` → `POST /api/uso` → `nucleo/datos/uso_panel/AAAA-MM-DD.jsonl`, privada, fuera de git). Este skill la
lee, saca conclusiones con números y propone una interfaz mejor. Responde en español.

Qué registra la bitácora: clics (control, posición, pestaña, video/canal, **clics muertos** = sin nada interactivo bajo el
cursor), cambios de filtros/selects/buscador, atajos de teclado (nunca letras sueltas), scroll (profundidad, tarjetas
visibles, ida y vuelta), cambios de pestaña, **atención real** por pestaña (15 s por latido, solo con ventana visible y
actividad), e **inventario** de controles (para saber cuáles existen y nunca se tocan). Cada evento lleva `ui` = versión de la
interfaz (`<meta name="ui-version">` de panel.html), lo que permite comparar antes/después.

## Pasos

1. **¿Hay datos suficientes?** `python nucleo/uso_panel.py estado`. Con menos de ~3 días de uso o ~300 clics, dilo y
   pregunta si seguir de todos modos (las conclusiones serían débiles). Si dice «Sin datos», el panel no se reinició con el
   registrador: pedir al usuario cerrar su ventana de consola del panel y `python fab.py panel --abrir`
   (**nunca detener el panel tú**).
2. **Informe**: `python nucleo/uso_panel.py resumen --dias 14` (o `--json` para cifras exactas; `--ui v2` para una sola versión).
3. **Contexto**: lee `docs/panel_ui_versiones.md` (versiones anteriores, qué cambió y qué métrica debía mejorar; si existe, y si la
   versión anterior ya tiene datos, **compara** `--ui vN` contra la previa: ¿mejoró lo que se prometió?). Del código del panel
   mira solo lo necesario: `grep -n` en `nucleo/panel.html` (80 KB; no lo leas entero) y el bloque de la zona que vayas a mover.
4. **Diagnóstico con evidencia** (cada hallazgo lleva su cifra del informe). Busca:
   - **Lo que se usa** (controles top, filtros que se aplican siempre → deben ser el valor por defecto o quedar a la vista),
     **lo que se estorba** (controles nunca tocados ocupando sitio → plegar a un menú, NO borrar sin avisar).
   - **Fricción**: clics muertos concentrados en un sitio (el usuario espera que eso sea clicable), clics repetidos rápido
     (control lento o que no confirma), scroll de ida y vuelta (algo que busca no está a mano), `profundidad_media` alta con
     tarjetas que nunca se miran, pestañas con poca atención o con mucho vaivén entre dos.
   - **Ritmo**: horas y duración de las sesiones (¿lo abre para ver un render? → resumen arriba), tamaño de pantalla (`pantalla`).
   - **Mapa de calor**: zonas calientes → controles frecuentes ahí o cerca del pulgar/mouse; frías → contenido secundario.
5. **Propuesta**. Escribe `nucleo/propuestas_panel/panel_vN.html` (N = siguiente versión; copia de `panel.html` modificada, con
   `<meta name="ui-version" content="vN">`). **Nunca sobrescribas `nucleo/panel.html` en este paso.** Reglas:
   - Conserva los `id`, `data-*` y funciones JS que el panel ya usa (el HTML se relee solo; el servidor de `panel.py` no cambia).
   - Mantén el registrador: `<script src="/uso.js"></script>` al final (así el uso de la propuesta también queda registrado).
   - Cambia organización y controles según la evidencia: atajos a lo frecuente, defaults de filtros, secciones plegadas,
     densidad, orden de pestañas, resumen arriba de lo que está en marcha. Lo no usado se agrupa en «Más…», no se elimina.
   - Calidad visual (regla de rigor del proyecto): mírala con el navegador integrado, a tamaño completo, tema claro y oscuro,
     con datos reales, antes de entregarla. La propuesta se abre en el panel en marcha: `http://127.0.0.1:8765/propuesta/panel_vN.html`
     (ruta de `panel.py`; usa la misma API, así que muestra el estado real).
6. **Entrega** (corto): 5-8 hallazgos con su cifra; la lista de cambios, cada uno con la métrica que debería mover
   (p. ej. «clics muertos en tarjetas: 40 → <10»); el enlace de la propuesta. Pregunta con AskUserQuestion si **adoptarla**
   (recomendado: probarla unos días con el enlace antes, porque su uso queda registrado como `vN`), ajustarla o descartarla.
7. **Si la adopta**: copia `panel.html` actual a `nucleo/propuestas_panel/panel_v<N-1>.html` (respaldo), copia la propuesta a
   `nucleo/panel.html`, y añade una entrada a `docs/panel_ui_versiones.md` (fecha, versión, datos base —días, clics, sesiones—,
   cambios, métricas esperadas, cómo volver atrás). El HTML se relee solo: basta recargar la pestaña. Commit en español solo si
   el usuario lo pide.
8. **Cierre**: dile cuándo conviene volver a correr el análisis (≥ 1 semana de uso de la versión nueva) y la frase exacta:
   «analiza mi uso del panel».

## Límites
- Solo lees la bitácora y escribes en `nucleo/propuestas_panel/`, `docs/panel_ui_versiones.md` y (con permiso) `nucleo/panel.html`.
- La bitácora es privada: no la subas a git (`nucleo/datos/uso_panel/` está en `.gitignore`), ni cites búsquedas o nombres de
  video fuera de esta conversación.
- `python nucleo/uso_panel.py borrar --antes AAAA-MM-DD` solo si el usuario lo pide.
- Si el registrador mismo necesita cambios (más eventos), edita `nucleo/panel_uso.js` + `nucleo/uso_panel.py`
  (campos permitidos en `CAMPOS`) y avisa que hay que recargar el panel (JS) o reiniciarlo (`panel.py`).
