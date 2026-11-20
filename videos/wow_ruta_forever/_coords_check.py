# -*- coding: utf-8 -*-
"""Coordenadas de «La RUTA del 1 al 60 en WoW Forever» (19-nov-2026; copiado y adaptado de wow_oro_forever/_coords_check.py).
Fuente de TODO: mapa mundial de Wowhead Forever (nether.wowhead.com/forever/data/world-map) vía videos/_investigacion_wow_ruta_forever.md
([WHF]); «WHF-lugar» = rótulo de subzona del mismo mapa (campo places), convertido por mí con el rect de la zona.
Mapas de zona: 1 % de la imagen = 1 de coordenada del juego (mismo rect que usa Wowhead).
    python _coords_check.py        → previews/_coords_check_N.jpg (6 mapas por hoja, MIRARLAS) + previews/_coords_mundo.jpg
    python _coords_check.py md     → imprime la tabla de _coords.md
Tipos: C = centro (pueblo/posada/vuelo) · R = punto de ruta · M = entrada de mazmorra/banda · P = PNJ o referencia."""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
W_ = "WHF"           # investigación (Wowhead Forever, mapa mundial)
WL = "WHF-lugar"     # rótulo de subzona del mapa mundial de Wowhead Forever
GG = "games.gg"
# mapa: [(parada, x, y, rótulo, tipo, fuente, confianza)]
PTS = {
    # ---------------- Parada 1 · 1-10
    "elwynn": [(1, 49.4, 41.3, "Abadía de Villanorte", "R", W_, "ALTA"), (1, 42.4, 66.6, "Villadorada", "C", W_, "ALTA"),
               (1, 43.8, 65.8, "posada (Farley)", "C", W_, "ALTA"), (1, 84.1, 65.3, "Aserradero Vega del Este", "R", W_, "ALTA"),
               (1, 25.0, 92.9, "Hogger (nv 11)", "P", GG, "MEDIA (guía; zona de patrulla)"),
               (1, 30.1, 38.8, "vuelo Ventormenta (Dungar)", "C", W_, "ALTA")],
    "dun_morogh": [(1, 24.1, 74.3, "Valle de Crestanevada", "R", W_, "ALTA"), (1, 46.4, 52.0, "Kharanos", "C", W_, "ALTA"),
                   (1, 47.4, 52.4, "posada (Belm)", "C", W_, "ALTA"),
                   (2, 53.5, 34.8, "Salón de Señores Feudales", "M", W_, "ALTA (bajo Forjaz)"),
                   (2, 64.8, 58.4, "Earthseer Farsen", "P", W_, "ALTA"),
                   (5, 17.7, 39.2, "Gnomeregan", "M", W_, "ALTA")],
    "teldrassil": [(1, 56.9, 32.8, "Cañada Umbría", "R", W_, "ALTA"), (1, 56.3, 60.2, "Dolanaar", "C", W_, "ALTA"),
                   (1, 55.6, 59.8, "posada (Keldamyr)", "C", W_, "ALTA"), (1, 58.4, 94.0, "vuelo Rut'theran", "C", W_, "ALTA")],
    "durotar": [(1, 43.9, 62.2, "Valle de los Retos", "R", W_, "ALTA"), (1, 52.6, 42.4, "Cerrotajo", "C", W_, "ALTA"),
                (1, 51.6, 41.6, "posada (Grosk)", "C", W_, "ALTA")],
    "mulgore": [(1, 44.4, 77.4, "Campamento Narache", "R", W_, "ALTA"), (1, 46.7, 63.2, "Pezuña de Sangre", "C", W_, "ALTA"),
                (1, 45.9, 64.1, "posada (Kauth)", "C", W_, "ALTA"), (1, 39.8, 35.7, "vuelo Cima del Trueno", "C", W_, "ALTA"),
                (1, 34.3, 26.1, "muelle dirigible (cielonatos H)", "C", W_, "ALTA")],
    "tirisfal": [(1, 32.0, 65.0, "Camposanto", "R", W_, "ALTA"), (1, 61.0, 52.7, "Rémol", "C", W_, "ALTA"),
                 (1, 61.6, 52.0, "posada (Renee)", "C", W_, "ALTA"), (1, 21.8, 46.1, "Fuerte de Bandarion", "R", W_, "ALTA"),
                 (1, 16.6, 58.2, "Bosque Susurrante", "R", W_, "ALTA"), (1, 12.2, 63.8, "Vallesombra", "R", W_, "ALTA"),
                 (2, 61.6, 72.6, "Ruinas de Lordaeron", "M", W_, "ALTA (bajo Entrañas)"),
                 (6, 85.1, 31.4, "Monasterio Escarlata", "M", W_, "ALTA")],
    "zephras": [(1, 42.2, 23.5, "Poblado Thendal", "R", W_, "ALTA"), (1, 43.4, 45.1, "Aldea Shen'dar", "C", W_, "ALTA"),
                (1, 43.0, 43.2, "posada (Coriella)", "C", W_, "ALTA"), (1, 63.2, 77.5, "Valanaar", "C", W_, "ALTA"),
                (1, 62.2, 72.6, "posada (Donaal)", "C", W_, "ALTA"), (1, 63.2, 85.6, "Muelles Celestiales", "R", W_, "ALTA"),
                (1, 66.6, 79.8, "Elaadrin (a Dalaran)", "P", W_, "ALTA")],
    # ---------------- Parada 2 · 10-15
    "paramos": [(2, 56.8, 47.3, "Colina del Centinela", "C", W_, "ALTA"), (2, 56.4, 52.6, "vuelo (Thor)", "C", W_, "ALTA"),
                (2, 52.8, 53.6, "posada (Heather)", "C", W_, "ALTA"), (2, 43.0, 69.3, "Arroyo de la Luna", "R", W_, "ALTA"),
                (2, 38.2, 77.5, "Minas de la Muerte", "M", W_, "ALTA"), (3, 52.4, 53.0, "Alba Fairmoon (misión nueva)", "P", W_, "ALTA")],
    "loch_modan": [(2, 35.0, 46.8, "Thelsamar", "C", W_, "ALTA"), (2, 33.8, 50.8, "vuelo (Thorgrum)", "C", W_, "ALTA"),
                   (2, 35.4, 48.4, "posada", "C", W_, "ALTA"), (2, 55.2, 14.3, "Presa de las Tres Cabezas", "R", W_, "ALTA")],
    "costa_oscura": [(2, 38.6, 43.4, "Auberdine", "C", W_, "ALTA"), (2, 36.4, 45.6, "vuelo (Caylais)", "C", W_, "ALTA"),
                     (2, 37.0, 44.0, "posada", "C", W_, "ALTA")],
    "baldios": [(2, 52.1, 30.6, "El Cruce", "C", W_, "ALTA"), (2, 51.4, 30.2, "vuelo (Devrak)", "C", W_, "ALTA"),
                (2, 62.2, 37.9, "Trinquete", "R", W_, "ALTA"), (12, 62.0, 39.4, "posada Wiley (Oso espectral)", "P", W_, "ALTA"),
                (3, 47.7, 35.0, "Cuevas de los Lamentos", "M", W_, "ALTA"), (3, 44.8, 58.7, "Campamento Taurajo", "C", W_, "ALTA"),
                (5, 42.3, 89.9, "Horado Rajacieno", "M", W_, "ALTA"), (7, 50.9, 92.9, "Zahúrda Rajacieno", "M", W_, "ALTA")],
    "argenteos": [(2, 43.6, 41.4, "El Sepulcro", "C", W_, "ALTA"), (2, 45.6, 42.4, "vuelo (Karos)", "C", W_, "ALTA"),
                  (2, 46.8, 73.2, "Aldea Piroleña", "R", W_, "ALTA"), (4, 44.7, 67.8, "Castillo de Colmillo Oscuro", "M", W_, "ALTA")],
    # ---------------- Parada 3 · 15-20
    "crestagrana": [(3, 24.0, 45.1, "Villa del Lago", "C", W_, "ALTA"), (3, 26.8, 44.8, "posada (Brianna)", "C", W_, "ALTA"),
                    (3, 30.6, 59.4, "vuelo (Ariena)", "C", W_, "ALTA"), (3, 46.2, 39.7, "Molino de Alther", "R", W_, "ALTA"),
                    (3, 76.9, 62.7, "Cascadas Petravista", "R", W_, "ALTA"), (3, 93.8, 21.3, "Avanzada del Sur", "R", W_, "ALTA")],
    "sierra_espolon": [(3, 47.8, 60.8, "Refugio Roca del Sol", "C", W_, "ALTA"), (3, 45.2, 59.8, "vuelo (Tharm)", "C", W_, "ALTA"),
                       (3, 47.4, 62.0, "posada (Jayka)", "C", W_, "ALTA")],
    # ---------------- Parada 4 · 20-25
    "bosque_ocaso": [(4, 74.2, 47.1, "Villa Oscura", "C", W_, "ALTA"), (4, 77.4, 44.4, "vuelo (Felicia)", "C", W_, "ALTA"),
                     (4, 79.6, 72.2, "Cementerio Jardín Sereno", "R", W_, "ALTA"), (4, 19.4, 57.5, "Cerro del Cuervo", "R", W_, "ALTA")],
    "humedales": [(4, 10.6, 55.3, "Puerto de Menethil", "C", W_, "ALTA"), (4, 9.4, 59.6, "vuelo (Shellei)", "C", W_, "ALTA"),
                  (4, 34.5, 49.7, "Excavación de Whelgar", "R", W_, "ALTA"), (4, 66.8, 47.2, "Refugio Faucedraco", "R", W_, "ALTA"),
                  (4, 52.2, 79.9, "El Enano Borracho", "R", W_, "ALTA"),
                  (5, 38.5, 60.5, "Sitio de Excavación (mazmorra)", "M", W_, "ALTA")],
    "vallefresno": [(4, 36.1, 50.8, "Astranaar", "C", W_, "ALTA"), (4, 34.4, 48.0, "vuelo (Daelyshia)", "C", W_, "ALTA"),
                    (4, 61.0, 51.8, "Refugio de la Algaba", "R", W_, "ALTA"), (4, 74.0, 62.1, "Puesto del Hachazo", "C", W_, "ALTA"),
                    (4, 12.0, 34.1, "Avanzada de Zoram'gar", "C", WL, "ALTA"),
                    (4, 16.5, 11.0, "Cavernas de Brazanegra", "M", W_, "ALTA")],
    "laderas": [(4, 61.5, 20.0, "Molino Tarren", "C", W_, "ALTA"), (4, 60.2, 18.6, "vuelo (Zarise)", "C", W_, "ALTA"),
                (4, 31.8, 36.7, "Campos de Trabalomas", "R", W_, "ALTA"), (4, 81.8, 39.8, "Castillo de Durnholde", "R", W_, "ALTA"),
                (5, 50.0, 56.4, "Costasur", "C", W_, "ALTA")],
    # ---------------- Parada 5 · 25-30
    "mil_agujas": [(5, 45.7, 50.7, "Poblado Viento Libre", "C", W_, "ALTA"), (5, 45.0, 49.2, "vuelo (Nyse)", "C", W_, "ALTA"),
                   (5, 18.6, 22.2, "Campamento E'thok", "R", W_, "ALTA"), (5, 70.8, 76.7, "El Desierto de Sal", "R", W_, "ALTA"),
                   (14, 17.8, 60.8, "Bancal del Creador (entrada)", "M", W_, "MEDIA (sin comprobar en el cliente)")],
    "feralas": [(5, 89.5, 46.3, "Thalanaar", "C", W_, "ALTA"),
                (10, 31.1, 44.6, "Bastión Plumaluna", "C", W_, "ALTA"), (10, 30.2, 43.2, "vuelo (Fyldren)", "C", W_, "ALTA"),
                (10, 75.2, 43.8, "Campamento Mojache", "C", W_, "ALTA"), (10, 75.4, 44.2, "vuelo (Shyn)", "C", W_, "ALTA"),
                (10, 75.7, 29.9, "Avanzada Gordunni", "R", W_, "ALTA"), (10, 45.0, 22.7, "Los Dos Colosos", "R", W_, "ALTA"),
                (13, 62.0, 33.3, "La Masacre", "M", W_, "ALTA")],
    # ---------------- Parada 6 · 30-35
    "arathi": [(6, 46.1, 46.6, "Refugio de la Zaga", "C", W_, "ALTA"), (6, 45.6, 46.2, "vuelo (Cedrik)", "C", W_, "ALTA"),
               (6, 73.9, 35.8, "Sentencia", "C", W_, "ALTA"), (6, 73.0, 32.6, "vuelo (Urda)", "C", W_, "ALTA"),
               (6, 68.1, 29.9, "Círculo de Vínculo Este", "R", W_, "ALTA"), (6, 69.0, 70.1, "Poblado Secacorteza", "R", W_, "ALTA"),
               (6, 21.8, 64.6, "Castillo de Stromgarde", "R", W_, "ALTA")],
    "alterac": [(6, 16.7, 68.8, "Ciudad de Dalaran (mazmorra)", "M", W_, "ALTA"), (6, 17.8, 66.2, "posaderos Dalaran", "C", W_, "MEDIA (bando sin comprobar)"),
                (1, 12.8, 51.2, "muelle dirigible (cielonatos A)", "C", W_, "ALTA"), (6, 7.7, 58.9, "Imagen de Modera", "P", W_, "ALTA")],
    "desolace": [(6, 65.1, 8.3, "Punta de Nijel", "C", W_, "ALTA"), (6, 55.2, 26.8, "Fortaleza Hacha de Trueno", "R", W_, "ALTA"),
                 (6, 49.3, 60.1, "Cementerio de Kodos", "R", W_, "ALTA"), (6, 25.3, 70.4, "Aldea Cazasombras", "C", W_, "ALTA"),
                 (9, 60.5, 90.2, "Valle de los Huesos (a Shen'dralas)", "R", W_, "ALTA"), (9, 29.1, 62.9, "Maraudon", "M", W_, "ALTA")],
    # ---------------- Parada 7 · 35-40
    "tuercespina": [(7, 38.2, 3.5, "Asentamiento Rebelde", "C", W_, "ALTA"), (7, 36.1, 11.3, "Expedición de Nesingwary", "R", W_, "ALTA"),
                    (7, 45.5, 9.0, "Base de Kurzen", "R", W_, "ALTA"), (7, 31.9, 50.5, "Arena Gurubashi", "R", W_, "ALTA"),
                    (7, 27.2, 75.6, "Bahía del Botín", "C", W_, "ALTA"), (7, 31.9, 28.4, "Campamento Grom'Gol", "C", W_, "ALTA")],
    # Ciudad Anegada: x -15.6 del mapa de la Vega → en tuercespina_oeste (X = (x+30)/130*100). Ver _coords.md
    "tuercespina_oeste": [(7, (-15.6 + 30) / 1.3, 58.3, "La Ciudad Anegada (mar adentro)", "M", W_, "MEDIA (entrada en el agua: comprobar)"),
                          (7, (31.9 + 30) / 1.3, 50.5, "Arena Gurubashi", "R", W_, "ALTA"),
                          (7, (31.9 + 30) / 1.3, 28.4, "Grom'Gol", "C", W_, "ALTA"),
                          (7, (27.2 + 30) / 1.3, 75.6, "Bahía del Botín", "C", W_, "ALTA"),
                          (7, (-8.4 + 30) / 1.3, 50.6, "isla de la Ciudad Anegada (vista en las teselas)", "M", "medido en teselas WHF", "ALTA (isla con ruinas trol)")],
    "ciudad_anegada_isla": [(7, 50.0, 50.0, "isla de la Ciudad Anegada", "M", "medido en teselas WHF", "ALTA"),
                            (7, 18.5, 85.0, "entrada [WHF] -15.6, 58.3 de la Vega", "M", W_, "MEDIA (pin redondo, en el agua)")],
    "marjal": [(7, 65.0, 47.1, "Isla Theramore", "C", W_, "ALTA"), (7, 56.7, 32.9, "Colina de las Brujas", "R", W_, "ALTA"),
               (7, 52.9, 79.5, "Ciénaga de Fuego", "R", W_, "ALTA"), (7, 36.3, 31.4, "Poblado Murohelecho", "C", W_, "ALTA"),
               (11, 77.6, 17.6, "Prisión de Alcaz", "M", W_, "ALTA"), (11, 70.3, 19.1, "Sargento Ulka", "P", W_, "MEDIA: en este mapa cae en el agua; en Forever está en un muelle (ver alcaz_isla)"),
               (14, 52.9, 77.7, "Guarida de Onyxia", "M", W_, "ALTA")],
    # Alcaz con el aspecto de FOREVER (la isla creció; en el mapa del Marjal de Classic Ulka cae en el agua). X = (x-64)/0.22, Y = (y-8)/0.22
    "alcaz_isla": [(11, (77.6 - 64) / 0.22, (17.6 - 8) / 0.22, "Prisión de Alcaz (entrada)", "M", W_, "ALTA"),
                   (11, (70.3 - 64) / 0.22, (19.1 - 8) / 0.22, "Sargento Ulka (muelle)", "P", W_, "ALTA")],
    "inhospitas": [(7, 4.3, 47.4, "Kargath", "C", W_, "ALTA"), (7, 35.2, 10.3, "Uldaman", "M", W_, "ALTA")],
    "pantano": [(7, 46.0, 53.8, "Rocal", "C", W_, "ALTA"), (11, 70.0, 52.9, "Templo de Atal'Hakkar", "M", WL, "ALTA (el templo dibujado en el mapa)"),
                (11, 77.3, 35.9, "pin mazmorra WHF (Atal'Hakkar)", "P", W_, "BAJA: cae en la orilla NE, lejos del templo; NO usar")],
    # ---------------- Parada 8 · 36-45 Claros del Río
    "riverglades": [(8, 28.7, 62.4, "Colinas Espinosas", "R", W_, "ALTA"), (8, 64.4, 83.0, "Fortaleza de Farholde", "C", W_, "ALTA"),
                    (8, 60.6, 81.4, "vuelo (Gretchen)", "C", W_, "ALTA"), (8, 54.8, 75.8, "Cortijo de Wheeler", "R", W_, "ALTA"),
                    (8, 59.6, 64.4, "Avanzada de Terral", "R", W_, "ALTA"), (8, 47.3, 47.9, "Claro Soleado", "R", W_, "ALTA"),
                    (8, 28.7, 42.8, "Sudario Crepuscular", "R", W_, "ALTA"), (8, 65.1, 18.0, "Pedreg'ok", "R", W_, "ALTA"),
                    (8, 48.6, 26.3, "Bastión de Krol'dok", "M", W_, "ALTA"), (8, 59.6, 45.9, "Rog'mar", "C", W_, "ALTA"),
                    (8, 78.9, 55.2, "Puerto Polvomecha", "C", W_, "ALTA"), (8, 80.6, 54.6, "barco a Tanaris", "C", W_, "ALTA")],
    "tanaris": [(8, 68.6, 23.0, "muelle barco a Claros del Río", "C", W_, "ALTA"),
                (10, 51.2, 27.5, "Gadgetzan", "C", W_, "ALTA"), (10, 51.0, 29.2, "vuelo A (Bera)", "C", W_, "ALTA"),
                (10, 60.8, 41.5, "Campo del Manantial", "R", W_, "ALTA"), (10, 40.5, 56.7, "Base Machacaduna", "R", W_, "ALTA"),
                (10, 38.7, 19.9, "Zul'Farrak", "M", W_, "ALTA")],
    # ---------------- Parada 9 · Shen'dralas
    "shendralas": [(9, 24.9, 25.7, "Valle de los Huesos", "R", WL, "ALTA"), (9, 35.8, 12.8, "Orgrul (H)", "P", W_, "ALTA"),
                   (9, 21.0, 22.6, "Nerlokh (H)", "P", W_, "ALTA"), (9, 35.0, 46.4, "Mordent Evenshade", "P", W_, "ALTA"),
                   (9, 32.9, 45.1, "Mirador de Sombrapar", "R", W_, "ALTA"), (9, 36.2, 76.8, "Escondite de Marginado", "R", W_, "ALTA"),
                   (9, 62.2, 54.9, "Frente Magram", "R", W_, "ALTA"), (9, 70.3, 72.0, "Jardines Desolados", "R", W_, "ALTA"),
                   (9, 72.0, 23.2, "Retirada Erizapúas", "R", W_, "ALTA")],
    # ---------------- Parada 10
    "interior": [(10, 14.4, 48.0, "Pico Nidal", "C", W_, "ALTA"), (10, 11.0, 46.0, "vuelo (Guthrum)", "C", W_, "ALTA"),
                 (10, 32.3, 46.1, "Avanzada Quel'Danil", "R", W_, "ALTA"), (10, 34.0, 72.1, "Shadra'Alor", "R", W_, "ALTA"),
                 (10, 62.6, 76.0, "Jintha'Alor", "R", W_, "ALTA"), (10, 78.3, 79.5, "Poblado Sañadiente", "C", W_, "ALTA")],
    # ---------------- Parada 11
    "ungoro": [(11, 43.6, 7.2, "Refugio de Marshal", "C", W_, "ALTA"), (11, 45.2, 5.8, "vuelo (Gryfe)", "C", W_, "ALTA"),
               (11, 51.8, 20.9, "Fosas Lakkari", "R", W_, "ALTA"), (11, 49.1, 49.3, "Cresta Penacho en Llamas", "R", W_, "ALTA"),
               (11, 30.2, 53.4, "Baños de Golakka", "R", W_, "ALTA")],
    "azshara": [(11, 11.7, 77.9, "Punta Talrendis", "C", W_, "ALTA"), (11, 21.8, 50.0, "Valormok", "C", W_, "ALTA"),
                (11, 33.6, 56.9, "Ruinas de Eldarath", "R", W_, "ALTA"), (11, 70.5, 29.3, "Camp. Vanguardia Thalassiano", "R", W_, "ALTA"),
                (11, 67.2, 15.5, "Fortaleza Legashi", "R", W_, "ALTA"),
                (13, 39.6, 32.3, "Bastión Faucenegra", "M", W_, "ALTA"), (13, 41.4, 20.0, "Tradicionalista Nok", "P", W_, "ALTA")],
    # ---------------- Parada 12
    "estepas": [(12, 85.9, 67.6, "Vigilia de Morgan", "C", W_, "ALTA"), (12, 84.4, 68.2, "vuelo (Borgus)", "C", W_, "ALTA"),
                (12, 65.5, 23.0, "Peñasco Llamarada", "C", W_, "ALTA"), (12, 80.2, 38.5, "Roca Machacamiedo", "R", W_, "ALTA"),
                (12, 60.9, 36.8, "Ruinas de Thaurissan", "R", W_, "ALTA"), (12, 33.0, 25.2, "Cumbre de Roca Negra", "R", W_, "ALTA"),
                (12, 22.6, 7.5, "pin Profundidades (portal interior)", "P", W_, "ALTA el dato, pero cae fuera de Las Estepas: NO usar en pantalla"),
                (12, 29.5, 36.0, "Montaña Roca Negra (Profundidades)", "M", "medido en el mapa", "ALTA (icono de la montaña)"),
                (12, 29.0, 29.0, "Franclorn Forjador", "P", W_, "ALTA")],
    "peste_oeste": [(12, 42.7, 85.3, "Campamento del Orvallo", "C", W_, "ALTA"), (12, 26.4, 51.7, "El Baluarte", "C", W_, "ALTA"),
                    (12, 48.1, 80.8, "Colina de las Penas", "R", W_, "ALTA"), (12, 38.8, 52.9, "Campo de Piedramácula", "R", W_, "ALTA")],
    # ---------------- Parada 13
    "cuna_invierno": [(13, 61.2, 38.2, "Vista Eterna", "C", W_, "ALTA"), (13, 51.2, 27.1, "Aldea Estrella Fugaz", "R", W_, "ALTA"),
                      (13, 51.6, 12.3, "Roca Sable de Hielo", "R", W_, "ALTA"), (13, 58.7, 51.8, "Mazthoril", "R", W_, "ALTA"),
                      (13, 58.2, 85.6, "Garganta Negro Rumor (a Hyjal)", "R", W_, "ALTA")],
    "silithus": [(13, 52.2, 39.9, "Fuerte Cenarion", "C", W_, "ALTA"), (13, 50.6, 34.4, "vuelo A", "C", W_, "ALTA"),
                 (13, 48.8, 36.6, "vuelo H", "C", W_, "ALTA")],
    # EPL: el mapa de zamimg (139) tiene el encuadre de Classic y NO cuadra con las coordenadas de Forever (Khaelyn: Classic 81.6, 59.2
    # → Forever 71.8, 49.5). Se usa peste_este_forever.jpg = teselas de Wowhead Forever recortadas con el rect de la zona (_mapa_mundo.py)
    "peste_este_forever": [(13, 71.9, 49.1, "Capilla Esperanza de la Luz", "C", W_, "ALTA"), (13, 53.3, 58.4, "Cruce de Corin", "R", W_, "ALTA"),
                   (13, 73.5, 70.1, "Mano de Tyr", "R", W_, "ALTA"), (13, 24.6, 29.4, "Bosque de la Peste", "R", W_, "ALTA")],
    "frondavil": [(13, 68.5, 6.1, "Bastión Fauces de Madera (túnel)", "R", W_, "ALTA")],
    # ---------------- Parada 14 · Hyjal (mapa de la wiki, mismo encuadre que el del juego)
    "hyjal": [(14, 59.3, 74.3, "Laderas Maculadas", "R", W_, "ALTA"), (14, 55.0, 82.8, "vuelo (Bluebell)", "C", W_, "ALTA"),
              (14, 53.6, 58.5, "Santuario de Aviana", "R", W_, "ALTA"), (14, 13.3, 49.9, "Flora Antigua", "R", W_, "ALTA"),
              (14, 15.6, 54.6, "campamento A (Sefira)", "C", W_, "ALTA"), (14, 14.0, 54.8, "campamento H (Zet'gan)", "C", W_, "ALTA"),
              (14, 58.4, 38.3, "Dae'gun", "R", W_, "ALTA"), (14, 78.5, 36.9, "Cima de la Eternidad", "R", W_, "ALTA"),
              (14, 68.6, 44.2, "vuelo Cima (Fayran)", "C", W_, "ALTA"),
              (14, 58.4, 57.1, "Cavernas del Túmulo + Cumbre Hyjal", "M", W_, "ALTA (bandas del 9-dic)")],
}

# Rect de cada zona en el lienzo del mapa mundial de Wowhead Forever (campo places): para la vista general
RECT = {
    "elwynn": [[35902, 21958], [39234, 24180]], "dun_morogh": [[35646, 18058], [40374, 21210]],
    "teldrassil": [[12722, 5026], [17610, 8284]], "durotar": [[18268, 14648], [23344, 18032]],
    "mulgore": [[14004, 16128], [19912, 20066]], "tirisfal": [[34464, 10652], [38802, 13544]],
    "zephras": [[26146, 8554], [31486, 12114]], "paramos": [[34480, 23360], [37840, 25600]],
    "baldios": [[13866, 14836], [23594, 21322]], "crestagrana": [[38990, 22568], [41074, 23958]],
    "humedales": [[37750, 16398], [41720, 19044]], "mil_agujas": [[16800, 20192], [21024, 23008]],
    "arathi": [[38208, 14464], [41664, 16768]], "alterac": [[36624, 12896], [39312, 14688]],
    "tuercespina": [[35244, 25058], [41370, 29142]], "riverglades": [[39192, 20544], [43848, 23648]],
    "shendralas": [[14440, 18208], [16408, 19520]], "tanaris": [[16594, 22024], [23218, 26440]],
    "azshara": [[19530, 11256], [24398, 14502]], "marjal": [[17320, 18336], [22360, 21696]],
    "estepas": [[37632, 21086], [40444, 22960]], "cuna_invierno": [[16688, 8192], [23504, 12736]],
    "hyjal": [[17270, 10332], [20604, 12554]], "desolace": [[12320, 15950], [16636, 18828]],
}
# Vista general (mundo_forever.jpg): una marca por parada en su lugar principal (zona, x, y del mapa de zona)
MUNDO = [
    (1, "Isla Zephras (inicio cielonato)", "zephras", 43.4, 45.1), (1, "Villadorada", "elwynn", 42.4, 66.6),
    (1, "Kharanos", "dun_morogh", 46.4, 52.0), (1, "Dolanaar", "teldrassil", 56.3, 60.2), (1, "Cerrotajo", "durotar", 52.6, 42.4),
    (1, "Pezuña de Sangre", "mulgore", 46.7, 63.2), (1, "Rémol", "tirisfal", 61.0, 52.7),
    (2, "P2 Colina del Centinela", "paramos", 56.8, 47.3), (2, "P2 El Cruce", "baldios", 52.1, 30.6),
    (3, "P3 Villa del Lago", "crestagrana", 24.0, 45.1), (4, "P4 Puerto de Menethil", "humedales", 10.6, 55.3),
    (5, "P5 Viento Libre", "mil_agujas", 45.7, 50.7), (6, "P6 Arathi", "arathi", 46.1, 46.6), (6, "P6 Dalaran", "alterac", 16.7, 68.8),
    (7, "P7 Bahía del Botín", "tuercespina", 27.2, 75.6), (8, "P8 Claros del Río", "riverglades", 59.6, 45.9),
    (9, "P9 Shen'dralas", "shendralas", 35.0, 46.4), (10, "P10 Gadgetzan", "tanaris", 51.2, 27.5),
    (11, "P11 Azshara", "azshara", 21.8, 50.0), (11, "P11 Alcaz", "marjal", 77.6, 17.6),
    (12, "P12 Las Estepas Ardientes", "estepas", 85.9, 67.6), (13, "P13 Vista Eterna", "cuna_invierno", 61.2, 38.2),
    (14, "P14 Monte Hyjal", "hyjal", 53.6, 58.5),
]
COLOR = {"C": (255, 60, 60), "R": (255, 230, 0), "M": (80, 200, 255), "P": (255, 140, 255)}


def fuente(n):
    for f in ("arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(f, n)
        except OSError:
            pass
    return ImageFont.load_default()


def mundo_px(zona, x, y):
    m = json.load(open(os.path.join(D, "mapas", "mundo_forever.json")))
    (x0, y0), (x1, y1) = RECT[zona]
    cx, cy = x0 + x / 100 * (x1 - x0), y0 + y / 100 * (y1 - y0)
    return cx / m["escala"] - m["recorte"][0], cy / m["escala"] - m["recorte"][1]


def hojas():
    F = fuente(15)
    minis = []
    for m, pts in PTS.items():
        im = Image.open(os.path.join(D, "mapas", m + ".jpg")).convert("RGB")
        im = im.resize((1024, round(1024 * im.height / im.width)))
        W, H = im.size
        d = ImageDraw.Draw(im)
        for p, x, y, r, t, *_ in pts:
            px, py = x / 100 * W, y / 100 * H
            d.ellipse((px - 6, py - 6, px + 6, py + 6), outline=COLOR[t], width=3)
            d.text((px + 8, py - 8), f"{r} [{x:.1f},{y:.1f}]", fill=COLOR[t], font=F, stroke_width=2, stroke_fill=(0, 0, 0))
        d.text((8, H - 24), m, fill=(0, 255, 255), font=fuente(20), stroke_width=2, stroke_fill=(0, 0, 0))
        minis.append(im.resize((960, round(960 * H / W))))
    os.makedirs(os.path.join(D, "previews"), exist_ok=True)
    por = 4
    for k in range(0, len(minis), por):
        lote = minis[k:k + por]
        alto = max(mi.height for mi in lote)
        g = Image.new("RGB", (2 * 960, ((len(lote) + 1) // 2) * alto), (20, 20, 20))
        for i, mi in enumerate(lote):
            g.paste(mi, ((i % 2) * 960, (i // 2) * alto))
        g.save(os.path.join(D, "previews", f"_coords_check_{k // por + 1}.jpg"), quality=85)
    # vista general
    im = Image.open(os.path.join(D, "mapas", "mundo_forever.jpg")).convert("RGB")
    d = ImageDraw.Draw(im)
    F2 = fuente(44)
    for p, r, z, x, y in MUNDO:
        px, py = mundo_px(z, x, y)
        d.ellipse((px - 16, py - 16, px + 16, py + 16), outline=(255, 60, 60), width=6)
        d.text((px + 20, py - 24), r, fill=(255, 240, 120), font=F2, stroke_width=4, stroke_fill=(0, 0, 0))
    im.thumbnail((2400, 2400))
    im.save(os.path.join(D, "previews", "_coords_mundo.jpg"), quality=85)
    print(len(minis), "mapas;", (len(minis) + por - 1) // por, "hojas + _coords_mundo.jpg")


def md():
    filas = []
    for m, pts in PTS.items():
        for p, x, y, r, t, f, c in pts:
            filas.append((p, m, r, t, x, y, f, c))
    filas.sort(key=lambda f: (f[0], f[1]))
    print("| Parada | Mapa | Punto | Tipo | x, y | Fuente | Confianza |\n|---|---|---|---|---|---|---|")
    for p, m, r, t, x, y, f, c in filas:
        print(f"| {p} | `{m}` | {r} | {t} | {x:.1f}, {y:.1f} | {f} | {c} |")
    print("\n| Parada | Lugar | Zona | x, y zona | píxel en mundo_forever.jpg (4080×3187) |\n|---|---|---|---|---|")
    for p, r, z, x, y in MUNDO:
        px, py = mundo_px(z, x, y)
        print(f"| {p} | {r} | `{z}` | {x}, {y} | {px:.0f}, {py:.0f} |")


if __name__ == "__main__":
    md() if sys.argv[1:] == ["md"] else hojas()
