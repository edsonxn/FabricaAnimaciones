# Espera a que termine el `voz` en curso (guion viejo) y lanza la ronda completa con el guion nuevo (`voz` reutiliza las tomas ya hechas).
import os, subprocess, sys, time
os.chdir(r"C:\FabricaAnimaciones")
while True:
    out = subprocess.run(["powershell", "-Command", "Get-CimInstance Win32_Process -Filter \"name='python.exe'\" | Where-Object { $_.CommandLine -match 'fab.py tesoro_moctezuma voz|tts_gen' } | Measure-Object | Select-Object -ExpandProperty Count"],
                         capture_output=True, text=True).stdout.strip()
    if out == "0":
        break
    time.sleep(15)
subprocess.run([sys.executable, "videos/tesoro_moctezuma/_ronda.py"], env=dict(os.environ, PYTHONIOENCODING="utf-8"))
