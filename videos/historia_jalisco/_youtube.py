# -*- coding: utf-8 -*-
"""youtube.json de «La historia de Jalisco en 5 minutos» con los capítulos tomados del timeline.json real. python _youtube.py"""
import json

TL = json.load(open("timeline.json", encoding="utf-8"))
CAP = {
    "gancho": "Tequila, mariachi y charros: una sola tierra",
    "origenes": "Xalisco, los Guachimontones y las tumbas de tiro",
    "conquista": "Nuño de Guzmán, la Nueva Galicia y la guerra del Mixtón",
    "guadalajara": "Guadalajara en Atemajac, la catedral, el tequila y el Hospicio Cabañas",
    "independencia": "El Amo Torres, Hidalgo y la abolición de la esclavitud, Puente de Calderón",
    "federalismo": "1823: el Estado Libre de Jalisco, cuna del federalismo",
    "reforma": "1858: «Los valientes no asesinan»",
    "porfiriato": "El ferrocarril llega a Guadalajara (1888)",
    "cristiada": "La Guerra Cristera en Los Altos (1926-1929)",
    "siglo20": "Cine de oro, Mundiales, la tragedia de 1992 y el Silicon Valley mexicano",
    "actualidad": "Jalisco hoy y el Mundial de 2026",
}


def mmss(t):
    t = int(t)
    return f"{t // 60}:{t % 60:02d}"


caps = "\n".join(f"{mmss(0 if e['id'] == 'gancho' else e['t0'])} {CAP[e['id']]}" for e in TL["escenas"] if e["id"] in CAP)
desc = f"""Más de dos mil años de historia de Jalisco sobre un mapa con relieve real: los Guachimontones de la tradición Teuchitlán y las tumbas de tiro, caxcanes, tecuexes, cocas y wixárikas, la llegada de Nuño de Guzmán y la Nueva Galicia, la guerra del Mixtón y la muerte de Pedro de Alvarado, las cuatro fundaciones de Guadalajara, el tequila de 1795 y el Hospicio Cabañas, Hidalgo y la abolición de la esclavitud en 1810, Puente de Calderón, el Estado Libre de Jalisco de 1823, Juárez y Guillermo Prieto, el ferrocarril, la Guerra Cristera, el mariachi y el charro del cine de oro, la tragedia de 1992 y el Jalisco del Mundial 2026.

⏱️ CAPÍTULOS
{caps}

📚 FUENTES
• INAH (Guachimontones, tradición Teuchitlán, catedral de Guadalajara) · El Colegio de Michoacán (Weigand)
• IIEG Jalisco y Gaceta de Guadalajara (fundaciones de Guadalajara, 1532-1542) · Congreso de Jalisco (Tonalá, 1530)
• Revistas del INAH y de la UdeG (guerra del Mixtón, Pedro de Alvarado, Real Universidad de 1792, ferrocarril de 1888)
• UNAM, Instituto de Investigaciones Históricas (Puente de Calderón, 1811) · INAH (Estado Libre de Jalisco, 1823)
• Memórica / Gobierno de México (Guerra Cristera y arreglos de 1929)
• UNESCO (Hospicio Cabañas 1997, Paisaje agavero de Tequila 2006, mariachi 2011)
• INEGI, Censo 2020 (8 348 151 habitantes) · FIFA (sedes del Mundial 2026)
• Relieve: NOAA ETOPO1; costas, ríos, lagos y límites estatales: Natural Earth (dominio público). Los territorios históricos son aproximaciones animadas.

Ilustraciones creadas con ayuda de IA (Google Flow) a partir de nuestros propios dibujos y animadas sobre el mapa; personajes y edificios son recreaciones artísticas.

Mira también:
• «Historia de México en 5 minutos» → https://youtu.be/BZd71Z5BIrk
• «Historia de España en 5 minutos» → https://youtu.be/m7b-pKda8BM

¿Qué estado de México quieres ver después? Te leo en los comentarios 👇

#HistoriaDeJalisco #Jalisco #HistoriaEnMinutos"""
Y = dict(
    titulo="La historia de Jalisco en 5 minutos",
    titulos_alternativos=["Historia de Jalisco en 5 minutos", "Jalisco en 5 minutos: de los Guachimontones al Mundial"],
    descripcion=desc,
    etiquetas=["historia de jalisco", "jalisco", "historia de guadalajara", "guadalajara", "jalisco en 5 minutos", "guachimontones",
               "guerra del mixton", "nueva galicia", "hospicio cabañas", "tequila", "mariachi", "guerra cristera", "puente de calderon",
               "federalismo", "historia de mexico", "historia en minutos", "historia animada", "mapas animados", "cronopapel"],
    categoria=27, idioma="es", idioma_audio="es", para_ninos=False,
    miniatura="salida/historia_jalisco_5min_mini_jalisco.jpg", subtitulos="salida/historia_jalisco_5min.srt",
)
json.dump(Y, open("youtube.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(caps)
