cd /c/FabricaAnimaciones
export PYTHONIOENCODING=utf-8
python fab.py tesoro_moctezuma voz > videos/tesoro_moctezuma/rb_voz.txt 2>&1
python fab.py tesoro_moctezuma seleccionar > videos/tesoro_moctezuma/rb_sel.txt 2>&1
echo hecho > videos/tesoro_moctezuma/rb_ok.txt
