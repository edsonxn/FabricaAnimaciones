# uso: python flow/_clip.py <clave>  → copia al portapapeles el prompt completo de esa hoja
import json, sys, subprocess, os
p = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prompts.json'), encoding='utf-8'))[sys.argv[1]]
subprocess.run(['powershell', '-NoProfile', '-Command', '$input | Set-Clipboard'], input=p.encode('utf-8'), check=True)
print(sys.argv[1], len(p))
