# Prueba de estilo «Noir feudal» — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: — (prueba de estilo, 11-oct-2026; para historias de sagas medievales tipo GoT/HotD o canales de historia antigua)
- estilo: noir_feudal → doc de estilo: docs/estilo_noir_color.md § Variante FEUDAL · kit nucleo/noir_feudal.py + noir_color.py
- etapa: render de prueba (30 s, sin voz) → salida/prueba_noir_feudal_antorcha.mp4
- siguiente: que el usuario elija canal/tema; luego guion con el pesquisidor como narrador

## Hecho
- Kit `nucleo/noir_feudal.py`: paletas antorcha/pergamino, rampas de época, muralla/torre/saetera/casa de entramado/adoquines,
  llama/antorcha/vela/estandarte/lacre/vaho, Pesquisidor (capucha, capa, farol) y BustoEncapuchado.
- Prueba de 30 s en 3 planos: villa amurallada bajo la luna (grúa desde el castillo; el pesquisidor llega con su farol y lo alza
  hacia el bando), cámara de la torre (ventana ojival, tapiz, antorcha, busto con vaho), mesa (pergamino que se escribe solo,
  copa volcada, veneno, daga, dos velas, sello de lacre, relámpago y tinta).

## Falta
- [ ] Elegir canal y tema (`python fab.py ideas <canal>`); NO usar logos, escudos ni personajes con el aspecto de la serie de HBO:
      emblemas y personajes propios (el kit ya trae sol/torre/luna/llave)
- [ ] Para un video real: más personajes de época (reyes, caballeros, damas, multitudes) y mapas de reinos (kit de mapas pintados)

## Cómo retomar (comandos)
```
python videos/prueba_noir_feudal/prueba.py hoja 2 9 14 26
python videos/prueba_noir_feudal/prueba.py paletas 9
python videos/prueba_noir_feudal/prueba.py video --procs 6 --paleta antorcha
```

## Archivos clave
- `prueba.py` (planos, montaje, audio, render), `mundos_fe.py` (lienzos pintados)
