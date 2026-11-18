"""YA APLICADO el 18-nov-2026: NO volver a correrlo (CLAUDE.md ya es el corto; el anexo está en docs/reglas_globales_completas.md).
Genera el ANEXO para docs/reglas_globales_completas.md con el texto ÍNTEGRO
del CLAUDE.md actual, partido en secciones §Rnn / §Cnn (las que cita el CLAUDE.md corto).
Uso: python docs/propuesta_claude_md/generar_anexo.py  (lee CLAUDE.md, escribe anexo_*.md)"""
from pathlib import Path
raiz = Path(__file__).resolve().parents[2]
L = (raiz / "CLAUDE.md").read_text(encoding="utf-8").splitlines()
def tramo(a, b): return "\n".join(L[a-1:b]).strip()

# (id, nombre, primera línea, última línea) — números de línea del CLAUDE.md del 18-nov-2026
SECC = [("R01","TOKENS, plan MAX, corte por cuenta y corte automático a 180 mil",6,10),
        ("R02","«Buenos días» = Claude dirige la orquesta",11,13),
        ("R03","Retomar un video / video nuevo en una sesión hasta el MASTER",14,19)]
nombres = ["REGLA DE ORO tes_secretos_40 (9 puntos)","Mejora continua y corregir al usuario",
 "Promo entre canales propios","Monetización en cada subida","Títulos","Qué canal toca",
 "Panel de canales al empezar y al terminar","Siguiente video con datos","Cierre de video",
 "Sin subtítulos quemados","Miniaturas siempre con Flow","APIs: cada una con un uso",
 "Sonido original del juego","Si la voz nombra un sonido, se oye","Comentarios de la gente",
 "Música de los canales de videojuegos = OST","Música Lyria, biblioteca, SFX y ElevenLabs escritura normal",
 "La voz nunca habla en otro idioma","La voz no cita fuentes","ElevenLabs = corchetes de actuación",
 "Nunca varios videos del mismo canal el mismo día; ciclos y frecuencia","Primero la tele",
 "Avisar al renderizar","Rigor con calidad y detalle","No reciclar escenas entre videos",
 "Campaña de suscripción","Mapas con ruta y SFX del juego","Fotos en el mapa",
 "Cada imagen es de lo que se nombra (identidad)","Promesas visuales comprobadas antes del render",
 "Todo lo que se nombra se muestra","Las escenas importantes se ven en movimiento",
 "Lo que no existe se genera en Flow como captura real","Estilo por canal fijo"]
for i, n in enumerate(nombres):
    SECC.append((f"R{i+4:02d}", n, 21+i, 21+i))
canales = ["Bitácora Perdida","Cronopapel","Sapiens con Wifi","Kuriox","Edsonxn","LogIA","Plastitube",
 "Wild Next Door","Crónicas del gaming",None,"Crónicas de Warcraft","Runa Caída","Crónicas de Tamriel",
 "Gaia Eterna","Cuerpo en Neón","Expediente 141","Crónicas de League of Legends","T Menos Cero",
 "Radio Yermo","Amaya Vibes"]
c = 0
CAN = []
for i, n in enumerate(canales):
    if n is None: continue
    c += 1
    CAN.append((f"C{c:02d}", n, 59+i, 59+i))
FIN = [("R38","Reels de Facebook «Que pasa en Juchipila»",80,80),
       ("R39","Video sin canal: preguntar antes + catálogo de otros estilos",82,82),
       ("R40","Arranque rápido de video dibujado por código",84,86),
       ("R41","Índice de docs",87,89),
       ("R42","Comandos esenciales (lista completa)",90,110),
       ("R43","Disco, git, entorno, entrega y Facebook",111,len(L))]

out = ["", "---", "",
 "# ANEXO 18-nov-2026: texto ÍNTEGRO del CLAUDE.md antes de la poda",
 "<!-- El CLAUDE.md corto del 18-nov-2026 deja cada regla en una línea con fecha y el puntero «RGC §Rnn» o «RGC §Cnn». Aquí está el texto completo, sin cambios. Buscar con: grep -n '### R15' docs/reglas_globales_completas.md -->", ""]
for sid, n, a, b in SECC + FIN[:0]:
    out += [f"### {sid} · {n}", "", tramo(a, b), ""]
out += ["### Cabecera de la tabla de estilos", "", tramo(57, 58), ""]
for sid, n, a, b in CAN:
    out += [f"### {sid} · Canal {n}", "", tramo(57, 58), tramo(a, b), ""]
for sid, n, a, b in FIN:
    out += [f"### {sid} · {n}", "", tramo(a, b), ""]
dest = Path(__file__).with_name("anexo_reglas_globales_completas.md")
dest.write_text("\n".join(out) + "\n", encoding="utf-8")
# Comprobación: cada línea no vacía del CLAUDE.md está en el anexo
txt = dest.read_text(encoding="utf-8")
faltan = [i+1 for i, l in enumerate(L) if l.strip() and l.strip() not in txt]
print("anexo:", dest, "| líneas del CLAUDE.md que NO están en el anexo:", faltan)
