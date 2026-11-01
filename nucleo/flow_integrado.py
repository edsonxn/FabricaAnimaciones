# -*- coding: utf-8 -*-
"""Flow SIN extensión de Chrome: lote de IMÁGENES desde el navegador integrado de la app (o cualquier navegador donde el JS
pueda escribir en el editor de Flow) y descarga directa desde Python. Creado el 11-oct-2026 en `cinco_bichos` cuando Claude in
Chrome se desconectó; Flow marcaba 0 puntos y las imágenes de «Nano Banana 2 Lite» siguieron saliendo gratis.

Por qué funciona (todo probado):
- El editor de prompts de Flow es ProseMirror: `document.execCommand('insertText')` escribe en él. El botón de enviar IGNORA clics
  sintéticos: el envío es con la tecla Return real (herramienta `computer` key Return del navegador integrado).
- Cada imagen aparece como <img src="https://flow-content.google/image/<uuid>?Expires=…&KeyName=labs-flow-prod-cdn-key&Signature=…">:
  URL firmada que se baja con curl SIN cookies. El navegador integrado NO puede hacer fetch a 127.0.0.1 (no hay puente), por eso
  el JS solo imprime «uuid expires firma» y Python las baja (`bajar`).
- Los mosaicos nuevos entran SIEMPRE arriba (más reciente primero) aunque terminen en otro orden; el colector marca lo ya visto
  y devuelve los nuevos en orden de envío.

Uso (desde C:\\FabricaAnimaciones):
  python nucleo/flow_integrado.py paquete <video>        escribe videos/<v>/_bundle.js (prompts.json comprimido con la FICHA)
  python nucleo/flow_integrado.py bajar <video> < lineas   «N uuid expires firma» por línea → medios/scene-NNN.jpg
Receta completa de la sesión del navegador: docs/manual_wild_next_door.md § «Imágenes sin extensión».
"""
import importlib
import json
import os
import re
import subprocess
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _guion(v):
    d = os.path.join(RAIZ, "videos", v)
    sys.path.insert(0, d)
    os.chdir(d)
    return importlib.import_module("guion"), d


def paquete(v):
    g, d = _guion(v)
    P = json.load(open("prompts.json", encoding="utf-8"))
    F = g.FICHA
    ks = sorted(P)
    E = F["estilo"] + ". "
    C = " " + F["cierre"]
    # fichas largas -> @A@, @B@…; se reconstruye idéntico (se verifica abajo)
    fuentes = [v_ for v_ in list(F.get("personajes", {}).values()) + [F.get("objeto", ""), F.get("epoca", "")] if len(v_) > 25]
    # frases repetidas ≥3 veces y ≥50 caracteres en los cuerpos (marcos, «unlabeled», etc.)
    cuerpos = [P[k][len(E):] for k in ks if P[k].startswith(E)]
    conteo = {}
    for c in cuerpos:
        for frag in re.split(r",\s+|\.\s+", c):
            if len(frag) >= 50:
                conteo[frag] = conteo.get(frag, 0) + 1
    fuentes += [f for f, n in conteo.items() if n >= 3]
    fuentes = sorted(set(fuentes), key=len, reverse=True)
    letras = ([chr(65 + i) for i in range(26)] + [chr(97 + i) for i in range(26)])[:len(fuentes)]
    toks = dict(zip(letras, fuentes))
    items, cierres = [], []
    for k in ks:
        t = P[k]
        assert t.startswith(E), k
        t = t[len(E):]
        cola = ""
        m = re.search(r"( No text.*| The only text.*)$", t)  # cierre entero hasta el final (19-oct: antes solo 1 frase)
        if m:
            cola = m.group(1)
            t = t[:m.start()]
        if cola not in cierres:
            cierres.append(cola)
        for tk, val in toks.items():
            t = t.replace(val, "@" + tk + "@")
        items.append([cierres.index(cola), t])
    js = ("window.__T=" + json.dumps(toks, ensure_ascii=False) + ";window.__E=" + json.dumps(E) + ";window.__C=" +
          json.dumps(cierres, ensure_ascii=False) + ";window.__I=" + json.dumps(items, ensure_ascii=False) + ";")
    js += ("window.__P=(i)=>{const [c,t]=window.__I[i];return window.__E+t.replace(/@([A-Za-z])@/g,(m,x)=>window.__T[x])+window.__C[c]};"
           "window.__ins=async(i)=>{await new Promise(r=>setTimeout(r,3500));const ed=document.querySelector('.ProseMirror');ed.focus();"
           "document.execCommand('selectAll');document.execCommand('delete');document.execCommand('insertText',false,window.__P(i));return ed.innerText.length};"
           "window.__seen=new Set([...document.querySelectorAll('img')].filter(i=>i.src.includes('flow-content')).map(i=>i.src.split('?')[0]));"
           "window.__col=async(n)=>{const t0=Date.now();let o=[];while(Date.now()-t0<55000){o=[...document.querySelectorAll('img')]"
           ".filter(i=>i.src.includes('flow-content')).map(i=>i.src).filter(u=>!window.__seen.has(u.split('?')[0]));if(o.length>=n)break;"
           "await new Promise(r=>setTimeout(r,2000));}o.reverse();o.forEach(u=>window.__seen.add(u.split('?')[0]));"
           "return o.map(u=>{const m=u.match(/image\\/([0-9a-f-]+)\\?Expires=(\\d+)&KeyName=[^&]+&Signature=(.+)$/);return m?m[1]+' '+m[2]+' '+m[3]:u}).join('\\n')};")
    # verificación: reconstruir cada prompt
    for i, k in enumerate(ks):
        c, t = items[i]
        rec = E + re.sub(r"@([A-Za-z])@", lambda m: toks[m.group(1)], t) + cierres[c]
        assert rec == P[k], k
    open("_bundle.js", "w", encoding="utf-8").write(js)
    print(f"{d}\\_bundle.js: {len(ks)} prompts, {len(js)} caracteres, {len(toks)} fichas")


def bajar(v):
    g, d = _guion(v)
    dst = os.path.join(d, "medios")
    os.makedirs(dst, exist_ok=True)          # sin la carpeta curl responde «200 0» (secreto_ia, 21-oct-2026)
    ok = mal = 0
    for ln in sys.stdin:
        p = ln.lstrip("﻿").split()          # la tubería de PowerShell 5.1 antepone un BOM (20-oct-2026)
        if len(p) < 2:
            continue
        url = p[1] if p[1].startswith("http") else (
            f"https://flow-content.google/image/{p[1]}?Expires={p[2]}&KeyName=labs-flow-prod-cdn-key&Signature={p[3]}")
        f = os.path.join(dst, f"scene-{int(p[0]):03d}.jpg")
        r = subprocess.run(["curl", "-s", "-m", "60", "-o", f, "-w", "%{http_code} %{size_download}", url],
                           capture_output=True, text=True)
        code, size = (r.stdout.split() + ["0", "0"])[:2]
        if code == "200" and int(size) > 50000:
            ok += 1
        else:
            mal += 1
            print("FALLO", p[0], code, size)
    print(f"descargadas {ok}, fallos {mal}")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("paquete", "bajar"):
        print(__doc__)
        sys.exit(1)
    {"paquete": paquete, "bajar": bajar}[sys.argv[1]](sys.argv[2])
