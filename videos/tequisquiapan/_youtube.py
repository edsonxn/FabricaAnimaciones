# -*- coding: utf-8 -*-
"""Escribe youtube.json (título, descripción con Google Maps de cada lugar —regla del 22-oct-2026—, créditos de fotos y fuentes)."""
import json
import os
import urllib.parse

D = os.path.dirname(os.path.abspath(__file__))
CRED = json.load(open(os.path.join(D, "fotos", "creditos.json"), encoding="utf-8"))
USADAS = ["centro_1", "tequis_noche", "codice_chich", "parroquia_1", "calle", "parroquia_2", "carranza", "centro_2", "centro_3",
          "relox", "feria_entrada", "kiosco", "artesano", "opalo", "bernal_1", "plaza", "pendulo", "mercado_1", "bernal_3"]
LUGARES = [
    ("Parroquia de Santa María de la Asunción (y su reloj)", "Parroquia de Santa Maria de la Asuncion Tequisquiapan Queretaro"),
    ("Plaza Miguel Hidalgo y kiosco", "Plaza Miguel Hidalgo Tequisquiapan Queretaro"),
    ("Monumento al Centro Geográfico", "Monumento al Centro Geografico Tequisquiapan Queretaro"),
    ("Parque La Pila", "Parque La Pila Tequisquiapan Queretaro"),
    ("Mercado de Artesanías", "Mercado de Artesanias Tequisquiapan Queretaro"),
    ("Presa Centenario", "Presa Centenario Tequisquiapan Queretaro"),
    ("Hotel El Relox (aguas termales)", "Hotel El Relox Tequisquiapan Queretaro"),
    ("Peña de Bernal", "Pena de Bernal Ezequiel Montes Queretaro"),
]
maps = "\n".join(f"• {n}: https://maps.google.com/?q={urllib.parse.quote_plus(q)}" for n, q in LUGARES)
fotos = " · ".join(CRED[k]["credito_corto"].replace(" / Wikimedia Commons", "") for k in USADAS)
desc = f"""¿Tequisquiapan es el centro de México? Su monumento dice que sí… y no lo es. La historia del pueblo de Querétaro que se llama como una sal, fue capital del estado por unos días y tiene una estación de tren que se llama «Bernal». En 3 minutos, sobre un mapa con relieve real, y con los lugares donde todavía puedes comprobarla.

📍 CÓMO LLEGAR (Google Maps) · confirma horarios antes de ir
{maps}

📚 FUENTES
• Jorge Vega Olvera, Monografía de Tequisquiapan (cronista municipal, 2008): La Pila (1567), el nombre de 1656, el reloj de 1897, el tren de 1902, la Presa Centenario (1910) y la capital del estado (mayo de 1920)
• Fundación oficial: 24 de julio de 1551 («Santa María de la Asunción y de las Aguas Calientes»); lo de la cruz bajo el mezquite es tradición, no documento
• Monumento al Centro Geográfico: placa de 1978; no se conoce el decreto. Centro de masa del país: Homero Adame Martínez, México Desconocido (Zacatecas)
• Peña de Bernal: Aguirre-Díaz et al., Geosphere 9(3), 2013 (domo volcánico de 8,7 millones de años, 433 m)
• Acuífero Valle de Tequisquiapan: Conagua (déficit de 5,15 millones de m³ al año, 2026)
• Relieve: AWS Terrain Tiles y SRTM15+ (NOAA); límites: Natural Earth e INEGI. Los territorios son aproximaciones animadas.

📷 FOTOS (Wikimedia Commons): {fotos}

Narración con voz sintética (ElevenLabs). Ilustraciones creadas con ayuda de IA (Google Flow) a partir de nuestros propios dibujos y animadas sobre el mapa.

¿Qué pueblo del Bajío contamos después? 👇

#Shorts #Tequisquiapan #Queretaro #PueblosMagicos #HistoriaDeMexico"""
assert len(desc.encode("utf-8")) <= 5000 and "<" not in desc and ">" not in desc, len(desc.encode("utf-8"))
yt = dict(
    titulo="La historia de Tequisquiapan en 3 minutos #Shorts",
    titulos_alternativos=["¿Tequisquiapan es el centro de México? #Shorts", "El pueblo que se llama como una sal #Shorts"],
    descripcion=desc,
    etiquetas=["tequisquiapan", "historia de tequisquiapan", "queretaro", "pueblos magicos", "pueblo magico", "peña de bernal",
               "centro geografico de mexico", "el bajio", "feria del queso y el vino", "historia de mexico", "mapas animados",
               "historia animada", "cronopapel", "shorts"],
    categoria=27, idioma="es", idioma_audio="es", para_ninos=False,
    subtitulos="salida/tequisquiapan.srt",
    maps=[dict(lugar=n, consulta=q) for n, q in LUGARES],
)
json.dump(yt, open(os.path.join(D, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(desc), "caracteres,", len(desc.encode("utf-8")), "bytes")
