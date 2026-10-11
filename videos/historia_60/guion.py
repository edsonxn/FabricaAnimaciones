# -*- coding: utf-8 -*-
"""200 000 AÑOS EN 60 SEGUNDOS — historia de la humanidad, vertical, sin voz, estilo Kurzgesagt.
PLANO SECUENCIA: no hay cortes; toda la historia es un mundo continuo (escenas.py -> Mundo) donde cada época se
abre como un portal desde un objeto de la anterior (transiciones procedurales). Las "escenas" de este guion son
solo las 5 secciones musicales (compases enteros a 128 BPM: 32 compases = 60,000 s).

Datos (fechas redondeadas, consenso arqueológico):
  - Homo sapiens: fósiles de Jebel Irhoud (~300 000 a.) y Omo Kibish (~230 000 a.) -> "hace 200 000 años".
  - Salida de África y expansión mundial: hace ~70 000 años (Australia > 50 000 a.).
  - Arte rupestre figurativo más antiguo: Sulawesi, ~45 000 años (Brumm et al. 2021); flautas de hueso ~40 000 a.
  - Agricultura: Creciente Fértil, ~11 000 años.  Rueda: ~3500 a. C. (Mesopotamia/Europa).  Escritura cuneiforme: ~3400 a. C., Sumer.
  - Gran Pirámide de Guiza: ~2560 a. C.  Atenas, democracia: 508 a. C.  Coliseo de Roma: inaugurado en el 80 d. C.
  - Imprenta de tipos móviles de Gutenberg: ~1440.  Colón llega a América: 1492.  Telescopio de Galileo (Júpiter y sus lunas): 1610.
  - Máquina de vapor de Watt (patente): 1769.  Bombilla incandescente práctica de Edison: 1879.
  - Primer vuelo de los Wright: 17 dic 1903 (12 s).  Apolo 11 en la Luna: 1969.  World Wide Web pública: 1991.
  - Primer iPhone / smartphones modernos: 2007.  8 000 millones de personas: noviembre de 2022 (ONU).
"""

TITULO = "200 000 años de historia en 60 segundos"
ARCHIVO = "historia_humanidad_60s"
ESTILO_VISUAL = "kurzgesagt"
FORMATO = "vertical"
SIN_VOZ = True
DURACION = 60.0
BPM = 128
MEZCLA = dict(musica=-21.0, sfx=-25.0)      # con narración: el fondo baja

# Narración (voz Dan) = lee el nombre que aparece en pantalla en cada época (sin tocar la animación). "anclas" = pulso
# (128 BPM) del video en que empieza cada frase (= inicio de la época: sapiens 0, África 8, arte 16, agricultura 24, rueda 30,
# escritura 36, pirámides 42, Atenas 48, Roma 54, imprenta 60, océano 66, telescopio 72, vapor 78, luz 84, vuelo 90, Luna 96,
# web 101, smartphone 106; en "hoy" los rótulos salen en los pulsos 113 y 119,2).
VOZ_ANCLADA = True
SUBTITULOS = False          # los textos ya están en pantalla: sin subtítulos encima (sí se genera el .srt)
ESCENAS = [
    dict(id="origen", compases=6, frases=[
        "Nace Homo sapiens.",
        "Salimos de África.",
        "Nace el arte.",
    ], anclas=[0.0, 8.0, 16.0]),
    dict(id="ciudades", compases=6, frases=[
        "La agricultura.",
        "La rueda.",
        "La escritura.",
        "Las pirámides.",
    ], anclas=[24.0, 30.0, 36.0, 42.0]),
    dict(id="imperios", compases=6, frases=[
        "Atenas: democracia.",
        "Roma: un imperio.",
        "La imprenta.",
        "Cruzar el océano.",
    ], anclas=[48.0, 54.0, 60.0, 66.0]),
    dict(id="maquinas", compases=6, frases=[
        "El telescopio.",
        "La revolución industrial.",
        "La luz eléctrica.",
        "Por fin volamos.",
    ], anclas=[72.0, 78.0, 84.0, 90.0]),
    dict(id="hoy", compases=8, frases=[
        "Un paso en la Luna.",
        "Nace la web.",
        "El mundo en tu bolsillo.",
        "Ocho mil millones de personas.",
        "Doscientos mil años. Y apenas empezamos.",
    ], anclas=[96.0, 101.0, 106.0, 113.0, 119.2]),
]
MUSICA = {
    "origen": dict(sabor="flauta"),
    "ciudades": dict(sabor="epico"),
    "imperios": dict(sabor="brillo"),
    "maquinas": dict(sabor="reloj"),
    "hoy": dict(sabor="final"),
}
