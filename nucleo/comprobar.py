# -*- coding: utf-8 -*-
"""Comprobación rápida ANTES del render largo (segundos, no minutos):
  1) nombres sin definir en escenas.py (errores tipo NameError que solo saltarían a mitad del render)
  2) todas las anclas de palabras resuelven (self.w) y cada escena tiene clase
  3) un cuadro de cada fase de cada escena se dibuja sin excepciones
Uso: python fab.py <video> comprobar"""
import ast
import builtins
import io
import json
import traceback

import escena_base
import escenas as S
from motor import Lienzo

errores = 0
# 1) análisis estático
arbol = ast.parse(io.open("escenas.py", encoding="utf-8").read())
disponibles = set(dir(escena_base)) | set(dir(builtins)) | set(dir(S))
locales = {a.arg for n in ast.walk(arbol) if isinstance(n, (ast.FunctionDef, ast.Lambda))
           for a in n.args.args + n.args.kwonlyargs + n.args.posonlyargs
           + ([n.args.vararg] if n.args.vararg else []) + ([n.args.kwarg] if n.args.kwarg else [])}
locales |= {t.id for n in ast.walk(arbol) for t in ast.walk(n) if isinstance(t, ast.Name) and isinstance(t.ctx, ast.Store)}
locales |= {n.name for n in ast.walk(arbol) if isinstance(n, (ast.FunctionDef, ast.ClassDef))}          # también anidadas
locales |= {(a.asname or a.name).split(".")[0] for n in ast.walk(arbol) if isinstance(n, (ast.Import, ast.ImportFrom))
            for a in n.names}                                                                          # imports locales
usados = {n.id for n in ast.walk(arbol) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
faltan = sorted(usados - disponibles - locales)
if faltan:
    errores += 1
    print("✗ nombres sin definir en escenas.py:", faltan)
else:
    print("✓ sin nombres indefinidos")

# 2) anclas y clases
TL = json.load(open("timeline.json", encoding="utf-8"))
objs = []
for i, e in enumerate(TL["escenas"]):
    try:
        objs.append(S.CLASES[e["id"]](e, i))
    except Exception as ex:
        errores += 1
        print(f"✗ escena {e['id']}: {ex}")
print(f"✓ {len(objs)}/{len(TL['escenas'])} escenas con anclas válidas, {sum(len(o.sfx) for o in objs)} efectos de sonido")

# 3) un cuadro por fase
lz = Lienzo()
for o in objs:
    ts = [o.t0 + 0.8, (o.t0 + o.t1) / 2, o.t1 - 0.4]
    if hasattr(o, "B"):
        ts = [o.t0 + 0.8, o.B + 0.6, (o.B + o.C) / 2, o.C + 0.6, (o.C + o.t1) / 2, o.t1 - 0.4]
    for t in ts:
        try:
            o.render(lz, t)
        except Exception:
            errores += 1
            print(f"✗ escena {o.id} en t={t:.2f}:")
            print(traceback.format_exc(limit=3))
            break
print("✓ todas las fases se dibujan" if not errores else f"✗ {errores} problema(s): corrígelos antes de renderizar")
raise SystemExit(1 if errores else 0)
