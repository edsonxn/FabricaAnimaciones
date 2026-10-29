"""Hook PostToolUse: corte automático por contexto (el usuario, 29-oct-2026).

Lee del transcrito el uso de la última llamada del hilo principal (entrada + caché) y, al pasar
el umbral (180 000 tokens por defecto), le inyecta a Claude la orden de cerrar el paso en curso,
hacer checkpoint en ESTADO.md y abrir un hilo nuevo con lo que falta. Con la simulación sobre
228 sesiones reales, cortar entre 150 y 200 mil ahorra ~40 % del gasto (docs/sesiones.md §7).

Desde el 29-oct-2026 (el usuario: «cámbialo») cuenta solo el TRABAJO: los 180 000 van por encima de la base
con la que arranca la sesión (herramientas, memoria, instrucciones: ~100 000), así que corta hacia los ~280 000.
Y un CANDADO por video evita dos continuaciones a la vez (la sesión cortada y la que la lanzó abrían una cada una).

Umbral: variable FAB_CORTE_CONTEXTO (tokens de trabajo; 0 = apagado). Repite el aviso cada +40 000 si sigue.
Prueba: python nucleo/hook_contexto.py --medir <transcrito.jsonl>
Candado: python nucleo/hook_contexto.py candado <v>   → «OK» (abre tú) o «YA …» (otra sesión la abrió; no abras)
"""
import json
import os
import sys
import tempfile
import time

UMBRAL = int(os.environ.get("FAB_CORTE_CONTEXTO", "180000"))
REPETIR = 40000
CANDADO_MIN = 30  # minutos en los que una continuación ya abierta bloquea otra del mismo video
ESTADO_DIR = os.path.join(tempfile.gettempdir(), "fab_contexto")
VIDEOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "videos")


def _uso(ln):
    """Tokens de contexto de una línea del transcrito si es una respuesta del hilo principal con uso; si no, None."""
    if b'"usage"' not in ln or b'"assistant"' not in ln:
        return None
    try:
        d = json.loads(ln)
    except ValueError:
        return None
    if d.get("isSidechain"):
        return None
    u = (d.get("message") or {}).get("usage")
    total = u and (u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
                   + u.get("cache_read_input_tokens", 0))
    return total or None  # los mensajes sintéticos (error, interrupción) traen uso 0


def contexto_inicial(path):
    """Base de la sesión: el contexto de su primera llamada del hilo principal (None si no se encuentra)."""
    try:
        with open(path, "rb") as f:
            for ln in f:
                total = _uso(ln)
                if total:
                    return total
    except OSError:
        pass
    return None


def candado(v):
    """True si esta sesión puede abrir la continuación de <v> (y lo deja apuntado); False si otra ya lo hizo."""
    ruta = os.path.join(VIDEOS, v, ".continuacion.json")
    try:
        with open(ruta, encoding="utf-8") as f:
            hace = (time.time() - json.load(f).get("t", 0)) / 60
        if hace < CANDADO_MIN:
            print(f"YA: otra sesión abrió la continuación de {v} hace {hace:.0f} min; no abras otra.")
            return False
    except (OSError, ValueError):
        pass
    if os.path.isdir(os.path.dirname(ruta)):
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump({"t": time.time(), "cuando": time.strftime("%Y-%m-%d %H:%M")}, f)
    print(f"OK: abre tú la continuación de {v}.")
    return True


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
                total = _uso(ln)
                if total:
                    return total
            if tam <= bloque:
                break
    return None


def orden(k, trabajo, repetido):
    insiste = ("SEGUNDO AVISO: sigues trabajando en un hilo que ya pasó el corte. " if repetido else "")
    return (
        f"⚠ CORTE AUTOMÁTICO POR CONTEXTO ({trabajo} mil tokens de trabajo ≥ {UMBRAL // 1000} mil, {k} mil en total; "
        f"regla del usuario del 29-oct-2026, docs/sesiones.md §7). {insiste}Cada paso de este hilo ya cuesta caro: termina SOLO el paso "
        "que estás haciendo (no empieces piezas nuevas; un render o voz ya lanzado se deja correr) y luego:\n"
        "1. CHECKPOINT: si trabajas en un video, en videos/<v>/ESTADO.md escribe `## En curso` (qué quedó hecho, "
        "archivos tocados, qué falta en orden, comandos lanzados con hora) y pon su fila de «## Sesiones» en "
        "◐ parcial. Si no es un video, deja lo pendiente en el archivo que corresponda (doc, ESTADO, nota).\n"
        "2. HILO NUEVO: primero `python nucleo/hook_contexto.py candado <v>`; si dice «YA», otra sesión ya abrió la "
        "continuación: NO abras otra, dilo en una línea y cierra. Si dice «OK»: carga mcp__ccd_session__start_session (ToolSearch \"select:mcp__ccd_session__start_session\") "
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
            m = json.load(f)
    except (OSError, ValueError):
        m = {}
    base = m.get("base")
    if base is None:  # se mide una vez por sesión: leer el transcrito desde el principio cuesta en los largos
        base = contexto_inicial(datos.get("transcript_path") or "") or 0
        m["base"] = base
    ultimo = m.get("avisado", 0)
    trabajo = ctx - base
    if trabajo < UMBRAL:
        if ultimo:  # se compactó o se limpió: el siguiente cruce vuelve a avisar
            m.pop("avisado")
    elif not (ultimo and ctx < ultimo + REPETIR):
        k = round(ctx / 1000)
        salida = json.dumps({
            "systemMessage": f"Contexto en {k} mil tokens ({round(trabajo / 1000)} mil de trabajo): "
                             "Claude hace checkpoint y abre un hilo nuevo.",
            "hookSpecificOutput": {"hookEventName": "PostToolUse",
                                   "additionalContext": orden(k, round(trabajo / 1000), bool(ultimo))},
        }, ensure_ascii=False)
        sys.stdout.buffer.write(salida.encode("utf-8"))  # la consola de Windows es cp1252
        sys.stdout.flush()
        m["avisado"] = ctx  # la marca solo tras avisar de verdad
    with open(marca, "w", encoding="utf-8") as f:
        json.dump(m, f)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--medir":
        print(f"inicial {contexto_inicial(sys.argv[2])} · actual {contexto_actual(sys.argv[2])}")
    elif len(sys.argv) == 3 and sys.argv[1] == "candado":
        sys.exit(0 if candado(sys.argv[2]) else 1)
    else:
        main()
