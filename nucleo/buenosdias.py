"""«Buenos días»: datos mínimos para que Claude proponga el plan del día sin explorar el proyecto.

  python fab.py buenosdias [--actualizar]                      tablero del día (canales, tramos pendientes, feedback, uso)
  python fab.py buenosdias --uso <cuenta> <semanal%> <5h%> <resetsAt ISO>   anota el uso de tokens de una cuenta (get_usage)
  python fab.py buenosdias --feedback <video> <aprobado|ajustes|rehacer> "<nota>"   anota el veredicto del usuario

Protocolo completo: docs/buenos_dias.md. Archivos: canales/uso_tokens.csv y docs/feedback_videos.md.
"""
import csv
import datetime as dt
import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USO = os.path.join(RAIZ, "canales", "uso_tokens.csv")
FEED = os.path.join(RAIZ, "docs", "feedback_videos.md")
CABECERA_FEED = "# Feedback del usuario sobre videos (lo escribe Claude tras la encuesta)\n\n| fecha | video | veredicto | nota |\n|---|---|---|---|\n"


def correr(*args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, *args], cwd=RAIZ, env=env, capture_output=True, text=True, encoding="utf-8")
    return (r.stdout or "") + (r.stderr if r.returncode else "")


def anotar_uso(cuenta, semanal, cinco, resets):
    fin = dt.datetime.fromisoformat(resets.replace("Z", "+00:00"))
    if fin.tzinfo is None:  # fecha sola (p. ej. 2026-10-20): se toma como UTC
        fin = fin.replace(tzinfo=dt.timezone.utc)
    ahora = dt.datetime.now(dt.timezone.utc)
    transcurrida = max(0.0, min(100.0, (1 - (fin - ahora).total_seconds() / (7 * 86400)) * 100))
    nuevo = not os.path.exists(USO)
    with open(USO, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(["fecha", "cuenta", "semanal_pct", "semana_transcurrida_pct", "cinco_h_pct", "reinicio_semanal"])
        w.writerow([dt.date.today().isoformat(), cuenta, semanal, round(transcurrida), cinco, fin.date().isoformat()])
    ritmo = float(semanal) / max(transcurrida, 1)
    print(f"{cuenta}: {semanal}% usado con {transcurrida:.0f}% de la semana → ritmo ×{ritmo:.1f} del sostenible")


def anotar_feedback(video, veredicto, nota):
    if not os.path.exists(FEED):
        with open(FEED, "w", encoding="utf-8") as f:
            f.write(CABECERA_FEED)
    with open(FEED, "a", encoding="utf-8") as f:
        f.write(f"| {dt.date.today().isoformat()} | {video} | {veredicto} | {nota.replace('|', '/')} |\n")
    print("Anotado en docs/feedback_videos.md")


def _suspendido(alias):
    """El canal lleva `"suspendido"` en canales/<alias>.json (el usuario lo pausó): no entra en el tablero."""
    try:
        return bool(json.load(open(os.path.join(RAIZ, "canales", alias + ".json"), encoding="utf-8")).get("suspendido"))
    except (OSError, ValueError):
        return False


def tablero(extra):
    print(f"=== BUENOS DÍAS · {dt.date.today():%A %d-%m-%Y} ===\n")
    print(correr(os.path.join(RAIZ, "nucleo", "estadisticas.py"), "calendario", *extra).strip())
    print("\n--- Videos con tramos pendientes ---")
    for linea in correr(os.path.join(RAIZ, "nucleo", "estado.py"), "continuar").splitlines()[1:]:
        if not linea.strip().startswith("_plantilla"):
            print(linea.split("  (alias")[0])
    print("\n--- Informe de ideas (edad) ---")
    carpeta = os.path.join(RAIZ, "canales", "metricas", "ideas")
    if os.path.isdir(carpeta):
        for n in sorted(os.listdir(carpeta)):
            if n.endswith(".md") and not _suspendido(n[:-3]):
                dias = (dt.datetime.now() - dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(carpeta, n)))).days
                print(f"  {n[:-3]:<18} hace {dias} d" + ("  ← refrescar (--actualizar)" if dias > 7 else ""))
    if os.path.exists(FEED):
        print("\n--- Últimos veredictos del usuario ---")
        print("".join(open(FEED, encoding="utf-8").readlines()[4:][-6:]).rstrip() or "  (ninguno)")
    if os.path.exists(USO):
        print("\n--- Uso de tokens (últimas filas) ---")
        print("".join(open(USO, encoding="utf-8").readlines()[-6:]).rstrip())


def main():
    a = sys.argv[1:]
    if a[:1] == ["--uso"] and len(a) == 5:
        anotar_uso(*a[1:])
    elif a[:1] == ["--feedback"] and len(a) >= 4:
        anotar_feedback(a[1], a[2], " ".join(a[3:]))
    else:
        tablero([x for x in a if x == "--actualizar"])


if __name__ == "__main__":
    main()
