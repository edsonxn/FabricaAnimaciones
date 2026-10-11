import sys, importlib
import estilos
estilos.activar("kurzgesagt")
m = importlib.import_module(sys.argv[1])
print({k: round(getattr(m, k), 2) for k in sys.argv[2:]})
