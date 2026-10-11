cd /c/FabricaAnimaciones
export PYTHONIOENCODING=utf-8
for e in sfx mezcla video final verificar; do
  python fab.py voynich $e > videos/voynich/log3_$e.txt 2>&1 || { echo "FALLO $e" > videos/voynich/resto3_fallo.txt; exit 1; }
done
echo ok > videos/voynich/resto3_ok.txt
