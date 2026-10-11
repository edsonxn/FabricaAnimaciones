# Prueba de estilo «Noir a color» — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: — (prueba de estilo, 11-oct-2026; el usuario quiere hacer un video con este estilo)
- estilo: noir_color → doc de estilo: docs/estilo_noir_color.md · kit nucleo/noir_color.py
- etapa: render de prueba hecho (30 s, sin voz) → salida/prueba_noir_color_sodio.mp4
- siguiente: que el usuario elija paleta (sodio · bourbon · medianoche) y tema del video; luego guion con detective narrador

## Hecho
- Kit `nucleo/noir_color.py` (NoirColor: rampas por material, luces y emisión en color, etalonaje apagado; 3 paletas).
- Prueba de 30 s en 3 planos: calle con lluvia (farolas de sodio, neón HOTEL que parpadea, detective llega y enciende),
  oficina (persiana ámbar, neón BAR rojo, calada y humo), escritorio (lámpara verde, expediente que se escribe, sello rojo, relámpago).
- SFX sintetizados (sfx_noir), sin música ni voz. Render 1080p30 en ~10 min con 6 procesos.

## Falta
- [ ] Elegir paleta y tema (con `python fab.py ideas <canal>` si es para un canal)
- [ ] Plano de oficina: poco movimiento entre 13 y 18 s (solo humo, mano y neón); en un video real, más acción

## Cómo retomar (comandos)
```
python videos/prueba_noir_color/prueba.py hoja 2 9 14 26
python videos/prueba_noir_color/prueba.py paletas 9
python videos/prueba_noir_color/prueba.py video --procs 6 --paleta sodio
```

## Archivos clave
- `prueba.py` (planos, montaje, audio, render), `mundos_nc.py` (lienzos pintados)
