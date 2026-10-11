# -*- coding: utf-8 -*-
"""Cambia el id de la subida de Polybius (se resubió sin el clic de las chinchetas) en ESTADO.md, BITACORA.md y canales/edsonxn.json."""
import io
import json

V, N = 'QMrTGVJXIEg', '6rqPo_fgz58'
p = 'ESTADO.md'
s = io.open(p, encoding='utf-8').read().replace(V, N)
s = s.rstrip('\n') + ('\n- El clic de la chincheta (`pin`) sonaba 67 veces en 5 min y el usuario pidió quitarlo: `tablero.Pieza` ya no lo registra y el papel va a 0,14. '
                      'YouTube no deja cambiar el audio: hubo que resubir (la subida vieja ' + V + ' quedó en privado SIN fecha; la borra el usuario).\n')
io.open(p, 'w', encoding='utf-8', newline='').write(s)

p = r'C:\FabricaAnimaciones\BITACORA.md'
s = io.open(p, encoding='utf-8').read().replace(V, N)
s = s.rstrip('\n') + ('\n- 7-oct-2026 · Edsonxn: Polybius RESUBIDO sin el clic repetido de las chinchetas (' + N + ', misma fecha 14-oct 14:00 CDMX). '
                      'La subida anterior ' + V + ' quedó en privado sin programar: el usuario la borra en Studio.\n')
io.open(p, 'w', encoding='utf-8', newline='').write(s)

p = r'C:\FabricaAnimaciones\canales\edsonxn.json'
d = json.load(open(p, encoding='utf-8'))
for x in d['publicados']:
    if x.get('id') == V:
        x['id'] = N
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

p = r'C:\FabricaAnimaciones\docs\estilo_documental.md'
s = io.open(p, encoding='utf-8').read()
a = '  de luz; el portal se compensa ×1,22 porque `cine` oscurece; el «?» de `Q` necesita aire encima.'
assert a in s
s = s.replace(a, a + '\n- **Sonido del tablero (el usuario, 7-oct-2026):** nada de un efecto por cada pieza. El clic de chincheta (`pin`) se quitó de `tablero.Pieza` '
              'y el papel va muy bajo; con 60-70 piezas el mismo sonido repetido cansa. Reservar los SFX para golpes con sentido (sello, látigo de cámara, corte de hilo).')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
