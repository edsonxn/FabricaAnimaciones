cd /c/FabricaAnimaciones
export PYTHONIOENCODING=utf-8
for e in sfx mezcla video final verificar; do
  python fab.py voynich $e > videos/voynich/log2_$e.txt 2>&1 || { echo "FALLO $e" > videos/voynich/resto2_fallo.txt; exit 1; }
done
echo ok > videos/voynich/resto2_ok.txt
