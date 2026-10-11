# Une partes/p1..p4 en escenas.py
import os
s = "".join(open(f"partes3/p{i}.py", encoding="utf-8").read() for i in (1, 2, 3, 4))
open("escenas.py", "w", encoding="utf-8").write(s)
import ast; ast.parse(s); print("escenas.py", len(s.splitlines()), "líneas, sintaxis ok")
