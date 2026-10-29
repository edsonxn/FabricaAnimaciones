"""Hook PostToolUse: corte automático por contexto (el usuario, 29-oct-2026).

Lee del transcrito el uso de la última llamada del hilo principal (entrada + caché) y, al pasar
el umbral (180 000 tokens por defecto), le inyecta a Claude la orden de cerrar el paso en curso,
hacer checkpoint en ESTADO.md y abrir un hilo nuevo con lo que falta. Con la simulación sobre
228 sesiones reales, cortar entre 150 y 200 mil ahorra ~40 % del gasto (docs/sesiones.md §7).

Umbral: variable FAB_CORTE_CONTEXTO (tokens; 0 = apagado). Repite el aviso cada +40 000 si sigue.
Prueba: python nucleo/hook_contexto.py --medir <transcrito.jsonl>
"""
import json
import os
import sys
import tempfile

UMBRAL = int(os.environ.get("FAB_CORTE_CONTEXTO", "180000"))
REPETIR = 40000
ESTADO_DIR = os.path.join(tempfile.gettempdir(), "fab_contexto")


def contexto_actual(path):
    """Tokens de contexto de la última llamada del hilo principal (None si no se encuentra)."""
    try:
        tam = os.path.getsize(path)
    except OSError:
        return None
    with open(path, "rb") as f:
        for bloque in (1 << 20, 8 << 20, 32 << 20):
            f.seek(max(0, tam - bloque))
            lineas = f.read().split(b"\n")
            if tam > bloque:
                lineas = lineas[1:]  # la primera puede venir cortada
            for ln in reversed(lineas):
                if b'"usage"' not in ln or b'"assistant"' not in ln:
                    continue
                try:
                    d = json.loads(ln)
                except ValueError:
                    continue
                if d.get("isSidechain"):
                    continue
                u = (d.get("message") or {}).get("usage")
                total = u and (u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
                               + u.get("cache_read_input_tokens", 0))
                if total:  # los mensajes sintéticos (error, interrupción) traen uso 0
                    return total
            if tam <= bloque:
                break
    return None


def orden(k, repetido):
    insiste = ("SEGUNDO AVISO: sigues trabajando en un hilo que ya pasó el corte. " if repetido else "")
    return (
        f"⚠ CORTE AUTOMÁTICO POR CONTEXTO ({k} mil tokens ≥ {UMBRAL // 1000} mil; regla del usuario del "
        f"29-oct-2026, docs/sesiones.md §7). {insiste}Cada paso de este hilo ya cuesta caro: termina SOLO el paso "
        "que estás haciendo (no empieces piezas nuevas; un render o voz ya lanzado se deja correr) y luego:\n"
        "1. CHECKPOINT: si trabajas en un video, en videos/<v>/ESTADO.md escribe `## En curso` (qué quedó hecho, "
        "archivos tocados, qué falta en orden, comandos lanzados con hora) y pon su fila de «## Sesiones» en "
        "◐ parcial. Si no es un video, deja lo pendiente en el archivo que corresponda (doc, ESTADO, nota).\n"
        "2. HILO NUEVO: carga mcp__ccd_session__start_session (ToolSearch \"select:mcp__ccd_session__start_session\") "
        "y llámala con initiation \"user_asked\" (autorizado de forma permanente por el usuario), context \"fresh\", "
        "use_worktree false, título «Continúa <v> — <siguiente pieza>» y un brief corto: «continúa el video <v>» + "
        "lo que falta en 5-10 líneas + qué leer (solo ESTADO.md y el doc de estilo). Nada de pegar el historial.\n"
        "3. Si la herramienta no existe o la app rechaza el inicio: propón la tarjeta con initiation "
        "\"own_initiative\" si se puede; si no, dile al usuario «abre un chat nuevo y escribe: continúa el video <v>».\n"
        "4. Cierra el turno aquí con un wrap_up breve (enlace a la sesión nueva) sin seguir produciendo en este hilo."
    )


def main():
    try:
        datos = json.load(sys.stdin)
    except ValueError:
        return
    if UMBRAL <= 0 or datos.get("agent_id"):  # apagado, o es un subagente: el corte es del hilo principal
        return
    ctx = contexto_actual(datos.get("transcript_path") or "")
    if ctx is None:
        return
    os.makedirs(ESTADO_DIR, exist_ok=True)
    marca = os.path.join(ESTADO_DIR, f"{datos.get('session_id', 'x')}.json")
    try:
        with open(marca, encoding="utf-8") as f:
            ultimo = json.load(f).get("avisado", 0)
    except (OSError, ValueError):
        ultimo = 0
    if ctx < UMBRAL:
        if ultimo:  # se compactó o se limpió: el siguiente cruce vuelve a avisar
            os.remove(marca)
        return
    if ultimo and ctx < ultimo + REPETIR:
        return
    k = round(ctx / 1000)
    salida = json.dumps({
        "systemMessage": f"Contexto en {k} mil tokens: Claude hace checkpoint y abre un hilo nuevo.",
        "hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": orden(k, bool(ultimo))},
    }, ensure_ascii=False)
    sys.stdout.buffer.write(salida.encode("utf-8"))  # la consola de Windows es cp1252
    sys.stdout.flush()
    with open(marca, "w", encoding="utf-8") as f:  # la marca solo tras avisar de verdad
        json.dump({"avisado": ctx}, f)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--medir":
        print(contexto_actual(sys.argv[2]))
    else:
        main()
