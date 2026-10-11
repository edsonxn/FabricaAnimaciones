cd /c/FabricaAnimaciones
export PYTHONIOENCODING=utf-8
V=tesoro_moctezuma
rm -f videos/$V/resto_ok.txt
for e in sfx mezcla final verificar; do
  python fab.py $V $e > videos/$V/log_$e.txt 2>&1 || { echo "FALLO $e" > videos/$V/resto_fallo.txt; exit 1; }
done
echo OK > videos/$V/resto_ok.txt
