# Versiones de la interfaz del panel

Historial que lee el skill `analizar-uso-panel` (`.claude/skills/analizar-uso-panel/`). Una entrada por versión:
fecha, datos en los que se basó, cambios, métrica que debía mejorar, cómo volver atrás.

## v1 — 12-oct-2026 · interfaz original
- Tres pestañas (Proyectos · Estilos · Canales), filtros por estado/canal/estilo, buscador, tarjetas por proyecto con 14-17 etapas.
- Sin datos de uso: es el punto de partida. La bitácora (`nucleo/panel_uso.js`) empieza a registrarse con esta versión.
- Para comparar: `python nucleo/uso_panel.py resumen --ui v1`.

## v2-lienzo — 21-oct-2026 · panel en lienzo (convive con v1; no lo sustituye)
- Pedido del usuario a partir de MiniMax Design: ver y reproducir en un canvas todo lo producido, con CPU/RAM/GPU/discos/procesos arriba.
- `http://127.0.0.1:8765/v2` (`nucleo/panel_v2.html` + `nucleo/panel_v2.py`). Detalle: `docs/panel.md` § «Panel v2 "Lienzo"».
- Montaje, Vista previa y Muestra son los diálogos de v1 incrustados (`/?embed=…`): no hay dos versiones que mantener.
- Para comparar: `python nucleo/uso_panel.py resumen --ui v2-lienzo`. Volver atrás: basta con usar `/` (v1 sigue igual).
