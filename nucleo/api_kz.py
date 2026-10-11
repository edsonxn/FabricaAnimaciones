# -*- coding: utf-8 -*-
"""Genera docs/api_kz.md: catálogo compacto (firma + primera línea del docstring) del kit Kurzgesagt isométrico/mapas
(nucleo/kz_*.py) y de las utilidades de videos/independencia_mx (util.py, mundos*.py).  Uso:  python nucleo/api_kz.py
Se consulta con grep (`grep -n "def casa" docs/api_kz.md`) en vez de leer los módulos."""
import ast
import glob
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTES = sorted(glob.glob(os.path.join(RAIZ, "nucleo", "kz_*.py"))) + [os.path.join(RAIZ, "nucleo", "plano.py")] + \
    [os.path.join(RAIZ, "videos", "independencia_mx", "util.py")] + sorted(glob.glob(os.path.join(RAIZ, "videos", "independencia_mx", "mundos*.py")))


def firma(f):
    a = f.args
    partes = []
    defs = [None] * (len(a.args) - len(a.defaults)) + list(a.defaults)
    for arg, d in zip(a.args, defs):
        partes.append(arg.arg if d is None else f"{arg.arg}={ast.unparse(d)}")
    if a.vararg:
        partes.append("*" + a.vararg.arg)
    for arg, d in zip(a.kwonlyargs, a.kw_defaults):
        partes.append(arg.arg if d is None else f"{arg.arg}={ast.unparse(d)}")
    if a.kwarg:
        partes.append("**" + a.kwarg.arg)
    return ", ".join(partes)


def main():
    out = ["# Catálogo del kit Kurzgesagt (generado por `python nucleo/api_kz.py`; no editar a mano)\n",
           "Formato: `def nombre(args)` — primera línea del docstring. Busca con grep; abre el módulo solo para el rango que necesites.\n"]
    for ruta in FUENTES:
        if not os.path.exists(ruta):
            continue
        src = open(ruta, encoding="utf-8").read()
        arbol = ast.parse(src)
        doc = (ast.get_docstring(arbol) or "").split("\n")[0]
        rel = os.path.relpath(ruta, RAIZ).replace("\\", "/")
        out.append(f"\n## {rel} — {doc}\n")
        for n in arbol.body:
            if isinstance(n, ast.FunctionDef) and not n.name.startswith("_"):
                d = (ast.get_docstring(n) or "").split("\n")[0]
                out.append(f"- `def {n.name}({firma(n)})`" + (f" — {d}" if d else ""))
            elif isinstance(n, ast.ClassDef) and not n.name.startswith("_"):
                d = (ast.get_docstring(n) or "").split("\n")[0]
                out.append(f"- `class {n.name}`" + (f" — {d}" if d else ""))
                for m in n.body:
                    if isinstance(m, ast.FunctionDef) and not m.name.startswith("_"):
                        dm = (ast.get_docstring(m) or "").split("\n")[0]
                        out.append(f"    - `.{m.name}({firma(m)})`" + (f" — {dm}" if dm else ""))
    destino = os.path.join(RAIZ, "docs", "api_kz.md")
    open(destino, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(destino, len("\n".join(out)), "bytes")


if __name__ == "__main__":
    main()
