import cProfile, pstats, sys
import estilos
estilos.activar("kurzgesagt")
import kz_mapa
M = kz_mapa.MAPA
M.base((-100.9, 21, 2.2), 0.0)
pr = cProfile.Profile(); pr.enable()
for i in range(3):
    M.base((-100.9 + i*0.1, 21, 2.2), 0.0)
pr.disable()
pstats.Stats(pr).sort_stats('cumulative').print_stats(22)
