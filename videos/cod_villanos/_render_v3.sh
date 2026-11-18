cd /c/FabricaAnimaciones
for e in video final verificar; do python fab.py cod_villanos $e || { echo "FALLO $e"; exit 1; }; done
echo LISTO
