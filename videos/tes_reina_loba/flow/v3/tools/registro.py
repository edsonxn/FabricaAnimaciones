# escribe flow/escenas_v3.md (checkpoint) y exporta pegatinas/flow3_<id>.png de las elegidas
import sys, json, glob, os
sys.path.insert(0, 'flow/v3'); import prompts as p
from PIL import Image
L = {r['id']: r for r in json.load(open('flow/v3/lista.json', encoding='utf-8'))}
el = json.load(open('flow/v3/elegidas.json', encoding='utf-8'))
fall = json.load(open('flow/v3/fallidas.json', encoding='utf-8')) if os.path.exists('flow/v3/fallidas.json') else {}
exp = '--exportar' in sys.argv
filas = []; hechas = []
for i in p.E:
    fs = sorted(glob.glob(f'flow/v3/crudo/flow3_{i}_*'))
    if not fs: continue
    k = el.get(i, 1); src = fs[min(k, len(fs)) - 1]
    dst = f'pegatinas/flow3_{i}.png'
    if exp and (not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src) or '--forzar' in sys.argv):
        im = Image.open(src).convert('RGB')
        if im.width < 1920: im = im.resize((1920, round(im.height * 1920 / im.width)), Image.LANCZOS)
        im.save(dst)
    t, ing = p.prompt(i)
    hechas.append(i)
    filas.append(f"| {i} | `{dst}` (cand. {k}/{len(fs)}) | {t.replace('|','/')} | {', '.join('`'+x+'`' for x in ing)} |")
pend = [i for i in p.E if i not in hechas]
md = ["# Escenas de Flow v3 — tes_reina_loba (13-nov-2026)",
      "Sustituyen clips de gameplay que no encajaban (`previews/revision_v3_clips.md`, filas «Flow:») + 18 añadidos por el coordinador.",
      "Proyecto de Flow: «Reina Loba v3». Nano Banana 2.1, 16:9, x2 (razonamiento Alto, 0 puntos). Salida 1376x768 → LANCZOS a 1920 px → `pegatinas/flow3_<id>.png`.",
      "Brutos en `flow/v3/crudo/flow3_<id>_<n>.jpg` (las 2 candidatas); elección en `flow/v3/elegidas.json`; prompts en `flow/v3/prompts.py` (cola servida con `flow/v3/tools/servir.py`).",
      "Ingredientes reales: `flow/ingred/ob_*` = cuadros de Oblivion 2006 original (YouTube, recortados sin HUD/subtítulos), `sk_*` = Skyrim vanilla; más retratos de `pegatinas/`. Lo que se pegó en Flow fueron copias ligeras JPG ≤1280 px (`flow/ingred/peg_<nombre>.jpg`, `*_l.jpg`; las PNG de 2-3 MB colgaban la pestaña), generadas por `flow/v3/tools/cola.py`.",
      "", f"**Hechas: {len(hechas)} / {len(p.E)}** · pendientes: {', '.join(pend) if pend else 'ninguna'}", ""]
if fall: md += ["## Fallidas / rechazadas", ""] + [f"- {k}: {v}" for k, v in fall.items()] + [""]
md += ["| id | archivo | prompt | ingredientes |", "|---|---|---|---|"] + filas
open('flow/escenas_v3.md', 'w', encoding='utf-8').write('\n'.join(md) + '\n')
print('hechas', len(hechas), 'pendientes', len(pend))
