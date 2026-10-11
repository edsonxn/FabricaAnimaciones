cd /c/FabricaAnimaciones
export PYTHONIOENCODING=utf-8
V=tesoro_moctezuma
for e in comprobar musica sfx mezcla video final verificar; do
  echo "== $e $(date +%T)" >> videos/$V/resto_log.txt
  python fab.py $V $e > videos/$V/log_$e.txt 2>&1 || { echo "FALLO $e" >> videos/$V/resto_log.txt; exit 1; }
done
echo "OK $(date +%T)" > videos/$V/resto_ok.txt
