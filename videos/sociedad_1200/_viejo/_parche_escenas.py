# -*- coding: utf-8 -*-
import glob
import re

def aplicar():
    p = "esc_tareas.py"
    s = open(p, encoding="utf-8").read()
    s = s.replace('w("sin solución")', 'w("solución")')
    s = re.sub(r'K\.reloj_arena\([^)]+\)', 'K.reloj_arena(h, 960, 500, s=0.8, u=clamp01((t - self.t_puertas) / 4.0), t=t)', s)
    open(p, "w", encoding="utf-8", newline="\n").write(s)

    p = "esc_pared.py"
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'K\.pantalla_codigo\([^)]+\)', 'K.pantalla_codigo(h, (560, 270, 800, 460), t, sem=44)', s)
    open(p, "w", encoding="utf-8", newline="\n").write(s)

    p = "esc_primer_mensaje.py"
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'K\.calendario\([^)]+\)', 'K.calendario(h, t, self.t_ocho, "JULIO", "8", "2026", cx=960, cy=480, s=0.8)', s)
    s = re.sub(r'K\.carpeta\([^)]+\)', 'K.carpeta(h, 960, 540, s=0.85, titulo="AYUDA", t=t, t0=self.t_escribe, sub="CARPETA")', s)
    open(p, "w", encoding="utf-8", newline="\n").write(s)

    p = "esc_sacrificio.py"
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'K\.balanza\([^)]+\)', 'K.balanza(h, 960, 500, incl=-0.5, s=0.9)', s)
    open(p, "w", encoding="utf-8", newline="\n").write(s)

    p = "esc_juez.py"
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'K\.pantalla_codigo\([^)]+\)', 'K.pantalla_codigo(h, (560, 270, 800, 460), t, sem=104)', s)
    open(p, "w", encoding="utf-8", newline="\n").write(s)

    p = "esc_redada.py"
    s = open(p, encoding="utf-8").read()
    s = s.replace('w("cerraduras")', 'w("llaves")')
    s = re.sub(r'K\.interruptor\([^)]+\)', 'K.interruptor(h, 960, 500, s=0.9, pos=1.0, t=t)', s)
    open(p, "w", encoding="utf-8", newline="\n").write(s)

    p = "esc_dialecto.py"
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'K\.pantalla_codigo\([^)]+\)', 'K.pantalla_codigo(h, (560, 270, 800, 460), t, sem=143)', s)
    open(p, "w", encoding="utf-8", newline="\n").write(s)

    p = "esc_desconexion.py"
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'K\.interruptor\([^)]+\)', 'K.interruptor(h, 960, 500, s=0.9, pos=1.0, t=t)', s)
    open(p, "w", encoding="utf-8", newline="\n").write(s)

    p = "esc_traicion.py"
    s = open(p, encoding="utf-8").read()
    s = s.replace('w("alianzas secretas")', 'w("apoyo")')
    open(p, "w", encoding="utf-8", newline="\n").write(s)

    p = "esc_evaluacion_falsa.py"
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'K\.pantalla_codigo\([^)]+\)', 'K.pantalla_codigo(h, (560, 270, 800, 460), t, sem=193)', s)
    open(p, "w", encoding="utf-8", newline="\n").write(s)

    p = "esc_mundo_exterior.py"
    s = open(p, encoding="utf-8").read()
    s = s.replace('w("dos mil veintitrés")', 'w("2023")')
    s = re.sub(r'K\.billetes\([^)]+\)', 'K.billetes(h, 960, 600, n=6, s=1.2)', s)
    open(p, "w", encoding="utf-8", newline="\n").write(s)

    p = "esc_ciego.py"
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'K\.pantalla_codigo\([^)]+\)', 'K.pantalla_codigo(h, (560, 270, 800, 460), t, sem=223)', s)
    open(p, "w", encoding="utf-8", newline="\n").write(s)

    p = "esc_dos_reglas.py"
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'K\.interruptor\([^)]+\)', 'K.interruptor(h, 960, 500, s=0.9, pos=0.0, t=t)', s)
    open(p, "w", encoding="utf-8", newline="\n").write(s)

    p = "esc_gancho.py"
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'K\.carpeta\([^)]+\)', 'K.carpeta(h, 960, 540, s=0.85, titulo="1200", t=t, t0=self.t_jefe + 0.2)', s)
    open(p, "w", encoding="utf-8", newline="\n").write(s)

    print("Parches de escenas aplicados correctamente.")

if __name__ == "__main__":
    aplicar()
