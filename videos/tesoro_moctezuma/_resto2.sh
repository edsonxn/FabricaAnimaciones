cd /c/FabricaAnimaciones
export PYTHONIOENCODING=utf-8
V=tesoro_moctezuma
echo "== video $(date +%T)" >> videos/$V/resto_log.txt
python fab.py $V video --procs 8 > videos/$V/log_video2.txt 2>&1 || { echo "FALLO video" >> videos/$V/resto_log.txt; exit 1; }
for e in final verificar; do
  echo "== $e $(date +%T)" >> videos/$V/resto_log.txt
  python fab.py $V $e > videos/$V/log_$e.txt 2>&1 || { echo "FALLO $e" >> videos/$V/resto_log.txt; exit 1; }
done
echo "OK $(date +%T)" > videos/$V/resto_ok.txt
