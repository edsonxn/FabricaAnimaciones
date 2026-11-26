"""Hook PreCompact (26-nov-2026): lo que imprime se vuelve instrucciones para el resumen de la compactación.

Desde el 26-nov Claude Code compacta hacia los 350 mil tokens (`autoCompactWindow` en .claude/settings.json),
así que en un video largo compacta 1-2 veces antes del MASTER. Esto le dice qué no puede perder.
Nunca bloquea: siempre sale con 0. Detalle: docs/sesiones.md §8.
"""
import sys

print("""Al resumir esta sesión de la Fábrica de Animaciones, conserva SIEMPRE, con nombres y rutas exactos:
1. El alias del video en curso (videos/<v>/), su canal y el paso exacto del flujo en que va (voz, montaje, render, subida...).
2. Lo que falta para llegar al MASTER y subirlo, en orden, y la sección «## En curso» de su ESTADO.md si se tocó.
3. Las decisiones y correcciones que dio el usuario en esta sesión, con sus palabras cuando importen.
4. Procesos lanzados que siguen corriendo (render, Flow, subidas): qué son, dónde escriben y cómo saber que acabaron.
5. Archivos creados o editados en esta sesión y errores ya resueltos (para no repetirlos).
No copies contenido de documentos ni salidas de comandos: basta la ruta del archivo para releerlo.""")
sys.exit(0)
