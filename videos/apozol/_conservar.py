import os, sys
sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import cache_escenas as C
car = os.getcwd()
nuc = r"C:\FabricaAnimaciones\nucleo"
firma = C.firma_codigo(car, nuc)
n = C.conservar(car, range(0, 100), firma)
print(n, "segmentos reanotados con la firma actual", firma)
