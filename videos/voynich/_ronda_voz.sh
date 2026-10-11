cd /c/FabricaAnimaciones
export PYTHONIOENCODING=utf-8
python fab.py voynich voz > videos/voynich/voz_log3.txt 2>&1
python fab.py voynich voz --seeds 5 6 7 8 --solo duenos_1 duenos_3 intentos_0 cierre_0 > videos/voynich/voz_log4.txt 2>&1
python fab.py voynich seleccionar > videos/voynich/sel_log3.txt 2>&1
echo RONDA_LISTA > videos/voynich/ronda_ok.txt
