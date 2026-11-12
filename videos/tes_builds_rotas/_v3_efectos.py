# -*- coding: utf-8 -*-
"""v3 (12-nov-2026): efectos.py al guion nuevo (sin «UESP» en la voz ni en pantalla; el Profeta narra, la banca se pelea)."""
import io, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
s = io.open("efectos.py", encoding="utf-8").read()
R = [
    ('ficha("Todo comprobado en UESP", "Fuentes", "Cada dato con su enlace de *UESP*", "En la descripción", dur=3.2)',
     'ficha("Cada una, probada", "Probadas", "Cada build, *en partida*", "Fuentes en la descripción", dur=3.2)'),
    ('("Todo comprobado", .1)', '("Cada una, probada", .1)'),
    ('"Hoy: 1 narrador + 2 de visita"', '"Narra el ganador: el Profeta"'),
    ('ficha("Están en un menú de pausa", "Cinco voces", "En *pausa*, mirando la pared", "Inmersión total"',
     'ficha("en la banca, peleándose", "La banca", "*Tres* voces peleando por un dato", "Johnny · MariCarmen · Hope"'),
    ('(P("altmer"), "UESP", ["Solo duplica la regeneración"', '(P("altmer"), "La verdad", ["Solo duplica la regeneración"'),
    ('"Y aquí, un mito", ("el doble de debilidad", .4), ["La pantalla de carga dice", "Según UESP", "el doble de debilidad"]',
     '"Este mito lo desmiento yo", ("el doble de debilidad", .4), ["La pantalla de carga dice", "Falso: solo duplica", "el doble de debilidad"]'),
    ('mis("Hace terapia de grupo", "Terapia de grupo", "Muy mala"', 'mis("Hace terapia de grupo", "Terapia de grupo", "Pregúntenle a la banca"'),
    ('    narra("Gracias, Johnny. Según UESP", "MariCarmen", "De visita · un dato", dur=5.0),\n', ''),
    ('    narra("Y otro dato de UESP", "Johnny", "Narrador", dur=3.0),\n', ''),
    ('unidad=" ejércitos", remate=("Potencialmente ilimitados", 3)),\n       "Y si te quitas la corona", ("potencialmente ilimitados", .4),\n'
     '       ["Y si te quitas la corona", "puedes usar la Ritual otra vez", "UESP lo resume", "potencialmente ilimitados"]',
     'unidad=" ejércitos", remate=("Sin límite", 3)),\n       "Y si te quitas la corona", ("de no muertos, sin límite", .4),\n'
     '       ["Y si te quitas la corona", "puedes usar la Ritual otra vez", "Ejércitos de no", "de no muertos, sin límite"]'),
    ('    narra("Los muertos únicos conservan", "el Profeta", "De visita · un dato", dur=4.6),\n', ''),
    ('    narra("Gracias, Profeta. Y ojo", "Johnny", "Narrador", dur=3.0),\n', ''),
    ('"UESP · Damage"', '"Dificultad Legendario"'),
    ('"El código (UESP)"', '"El código del juego"'),
    ('"Y otro mito. Todos dicen"', '"Todos dicen que la Navaja"'),
    ('(P("altmer"), "UESP", ["≈ ×9,33"', '(P("altmer"), "La cuenta real", ["≈ ×9,33"'),
    ('"UESP lo calculó"', '"Haz la cuenta"'),
    ('"UESP · Spell Absorption"', '"Todo lo que no sea físico"'),
    ('ficha("El tercero es un error"', 'ficha("Es un error: un vampiro"'),
    ('"UESP lo midió", ("El número sigue subiendo", .3), ["UESP lo midió"', '"Lo medí yo", ("El número sigue subiendo", .3), ["Lo medí yo"'),
    ('"El procedimiento, literal"', '"El procedimiento es así"'),
    ('    narra("Los Barbas Grises entrenan", "el Profeta", "De visita · un dato", dur=4.4),\n', ''),
    ('    narra("Gracias otra vez, Profeta", "Johnny", "Narrador", dur=3.0),\n', ''),
    ('"UESP · Fortify Destruction"', '"Congelación mata dragones"'),
    ('rel("el de hueso de dragón, de Dawnguard"', 'rel("El arco de hueso de dragón, de Dawnguard"'),
    ('ficha("eso no cuenta como crimen"', 'ficha("no lo cuenta como crimen"'),
    ('cam("Serana. La única novia"', 'cam("la única novia que"'),
    ('("Estaba escrito.|fin", .1)', '("Contra sus propios soldados.|fin", .1)'),
]
for a, b in R:
    n = s.count(a)
    assert n == 1, (n, a[:70])
    s = s.replace(a, b)

ANEXO = '''
# ---- v3 (el usuario, 12-nov-2026): GANÓ EL PROFETA → narra 8 de cada 10 datos y se burla desde arriba; la BANCA (Johnny, MariCarmen,
# Hope, empate a 2 votos) se pelea por el resto. Placa en cada relevo (sale de guion.NARRA) + papeleta del resultado y del cierre.
import re as _re  # noqa: E402
import guion as _G  # noqa: E402

_LEMA = {"el Profeta": "Ganador de la votación"}
_robados, _prev, PLACAS = {}, None, []
for _e in _G.ESCENAS:
    for _i, _tx in enumerate(_e["frases"]):
        _v = _G.NARRA[f"{_e['id']}_{_i}"]
        if _v != _prev and _prev is not None:
            _limpio = _re.sub(r"\\[[^\\]]*\\]\\s*", "", _tx)
            _ancla = " ".join(_limpio.split()[:5]).rstrip(",.:;¡!¿?")
            if _v == "el Profeta":
                PLACAS.append(narra(_ancla, "el Profeta", _LEMA[_v], dur=2.6))
            else:
                _robados[_v] = _robados.get(_v, 0) + 1
                PLACAS.append(narra(_ancla, _v, f"En la banca · dato robado n.º {_robados[_v]}", dur=3.6))
        _prev = _v
PLACAS += [
    mg(T.votacion("Resultado de la votación", ["el Profeta · 9", "Johnny · 2", "MariCarmen · 2", "Hope · 2"],
                  remate=("Narra el ganador", 4)),
       "Ustedes votaron, y ganó", ("Es lo justo", .4),
       ["Ustedes votaron, y ganó", "Así que narro yo", "Los tres empatados", "se pelean por las migajas", "Es lo justo"],
       "votación resultado", y=.42),
    mg(T.votacion("¿Quién de la banca habla más?", ["Johnny", "MariCarmen", "Hope"], remate=("No va a pasar", 3)),
       "vota en los comentarios", ("Nos vemos en Tamriel", .2),
       ["vota en los comentarios", "vota en los comentarios", "vota en los comentarios", "No va a pasar"], "votación banca", y=.42),
]
FX = FX + PLACAS
'''
s = s.rstrip() + "\n" + ANEXO
io.open("efectos.py", "w", encoding="utf-8").write(s)
print("efectos.py v3 OK")
