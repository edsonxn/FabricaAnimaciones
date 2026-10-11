#!/bin/bash
# uso: ./run.sh script.py args...   (PYTHONPATH de este video + núcleo, como hace fab.py)
export PYTHONPATH='C:\FabricaAnimaciones\videos\independencia_mx;C:\FabricaAnimaciones\nucleo'
export PYTHONIOENCODING=utf-8
cd /c/FabricaAnimaciones/videos/independencia_mx
python "$@"
