# -*- coding: utf-8 -*-
"""PRIMER REEL DIARIO de la página de Facebook «Noticias de Juchipila» (alias noticias_jch, E:\\PaginaFace; receta
E:\\PaginaFace\\reel_diario.md). Vertical 1080x1920, ~60 s, una sesión, directo al MASTER. Sin canal de YouTube.
PÁGINA ANÓNIMA: nada de la voz, música, kits ni arte de los canales de la Fábrica (voz Carlos Corella, kit propio kit_nj.py
con los colores del logo de la página, cama musical nueva de ElevenLabs).
Subtítulos grandes = EXCEPCIÓN a R13 solo para esta página (Edson, 19-nov-2026).

FUENTES (reabiertas el 19-nov-2026):
- González-Elizondo et al. (2011), «Pinus maximartinezii Rzed. (Pinaceae), primer registro para Durango, segunda localidad
  para la especie», Acta Botánica Mexicana 96: https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S0187-71512011000300005
  · descrito por Rzedowski (1964) del Cerro de Piñones, Sierra de Morones, al W de Pueblo Viejo, municipio de Juchipila
  · «por más de cuatro décadas» se creyó restringido a esa localidad; segunda población corroborada en 2010 (La Muralla,
    El Mezquital, Durango, 190 km al NW)
  · «es el piñonero con conos y semillas más grandes en el mundo»
  · Zacatecas: entre 2000-2500 (Donahue y Mar-López 1995, ~400 ha) y 60,548 individuos (otro conteo); Durango > 900
  · Passini (1985): árboles de más de nueve metros en Juchipila ≈ 220 años
  · NOM-059-SEMARNAT-2010: endémica y en peligro de extinción; UICN: En Peligro; follaje «de color azulado» (pino azul)
- Threatened Conifers of the World (RBGE): https://threatenedconifers.rbge.org.uk/conifers/pinus-maximartinezii
  · «main threats are grazing by livestock and fire»; Sierra de Morones ca. 2000-2500 maduros en ~400 ha (Ledig 1999)
- Fotos: Wikimedia Commons, categoría Pinus maximartinezii (créditos en fuente/fotos/creditos.json).
- Mapa: OpenTopoMap (© OpenStreetMap, CC-BY-SA); punto del pino = GPS de las fotos de Commons (21.3567, -103.2226);
  Pueblo Viejo y Juchipila de OpenStreetMap (Nominatim).
"""

TITULO = "El pino azul de la Sierra de Morones"
ARCHIVO = "jchn_261119_pino_azul"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
FORMATO = "vertical"
GAP = 0.22
DURACION = None
BPM = 90

# Carlos Corella (mexicano, grave, con autoridad): elegido por Edson el 19-nov-2026 entre 6 voces sin uso en sus canales.
# Biblioteca compartida, por id; solo la cuenta 4 de ElevenLabs tiene saldo.
VOZ = dict(motor="elevenlabs", voice_id="LnGOA2SxH2fX1e1iNzEp", modelo="eleven_v4_turbo", idioma="es", tomas=1,
           stability=0.5, style=0.3, sin_etiquetas=("whisper", "excit", "shout"))
FONETICA = {}

SECUENCIA = dict(
    video_s=0,          # todo imagen (fotos reales de Commons + mapa por código)
    clip_s=8,
    img_s=3.6,
    rapido_hasta=300,
    img_s_lento=3.6,
    fundido=0.25,
    ambiente=0.0,
    ambiente_por={},
)
TRANSICIONES = [("continua", 0.1)] * 30
MEZCLA = dict(fx=-6.0)
MUSICA = {}

FICHA = dict(estilo="Fotografía real vertical nueve dieciséis", personajes={}, objeto="", epoca="",
             cierre="Sin texto, sin letras, sin logotipos.")

ESCENAS = [
    {"id": "gancho", "pre": 0.3, "frases": [
        "[serious] En la sierra de Juchipila crece un pino que casi no existe en ningún otro lugar del mundo.",
    ]},
    {"id": "contexto", "frases": [
        "Es el pino azul. Vive en el Cerro de Piñones, en la Sierra de Morones.",
        "Un botánico lo describió en mil novecientos sesenta y cuatro, con árboles de ese cerro.",
        "Y por más de cuarenta años se creyó que solo existía aquí.",
    ]},
    {"id": "jugoso", "frases": [
        "Tiene las piñas y los piñones más grandes de todos los pinos piñoneros del mundo.",
        "En la sierra se calculan entre dos mil y dos mil quinientos árboles adultos.",
        "Los más altos rondan los doscientos veinte años.",
        "Hasta dos mil diez apareció otro bosque, en Durango. [short pause] Pero el de aquí sigue siendo el más grande.",
    ]},
    {"id": "cierre", "post": 3.2, "frases": [
        "[serious] Hoy está en peligro de extinción, por el fuego y el ganado suelto.",
        "¿Usted ya lo conocía? Cuéntenos en los comentarios.",
    ]},
]
