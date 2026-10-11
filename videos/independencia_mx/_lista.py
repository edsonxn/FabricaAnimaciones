import sys
sys.stdout.reconfigure(encoding='utf-8')
import estilos
estilos.activar("kurzgesagt")
import escenas as S
from escena_base import TL
esc = TL['escenas']
print("TOTAL", TL['total'], "n_shots", len(S.SHOTS))
for e in esc:
    print(f"{e['id']:16s} {e['t0']:7.1f} {e['t1']:7.1f}  frases={len(e.get('frases',[]))}")
print()
for i, d in enumerate(S.SHOTS):
    print(f"{i:3d} {d['t0']:7.2f} {d['t1']:7.2f} {d['t1']-d['t0']:5.1f}s {d['nombre']:28s} {d['ent']}")
