# Guía del kit — «dos lunas» (1 página; leer ANTES de dibujar escenas)

Estilo: **Kurzgesagt plano secuencia** (una clase `Mundo`, cero cortes) con mascota **Kuri** (`plano.kuri`), nunca el pájaro.
Doc de estilo: `docs/estilo_kurzgesagt.md` (sección «plano secuencia» + «ERRORES A NO REPETIR»). Ejemplo de estructura:
`videos/sol_apagado_8min/` (`escenas.py` = Mundo, `mundo_comun.py` = Cam/camino/Sup/anclas, `anclas.py`).

## Estructura de archivos a crear (sesión 2)
| archivo | para qué |
|---|---|
| `mundo_comun.py` | copiar de `sol_apagado_8min` (T/INI/FIN, `Cam`, `camino`, `mezclar_cam`, `Sup`, `pop`, `ventana`); quitar lo del Sol |
| `anclas.py` | `A = SimpleNamespace(...)` con `T("escena", "palabra", frase=i)` por cada momento clave (tiempo global de la palabra) |
| `mundo_espacio.py` | Tierra, Luna, 2.ª luna, órbitas, Hill, Lagrange, Roche, anillo (todo en coordenadas del mundo, Tierra en el origen) |
| `mundo_tierra.py` | cielo nocturno con dos lunas, costa y marea, corte de la Tierra (volcanes) — planos 2D de cerca |
| `escenas.py` | `render_mundo(lz, t)` + `registrar_sfx` + `class Mundo(Escena)`; `CLASES = {id: Mundo}` |

## El kit (todo con `lz` = Lienzo; firmas exactas: `grep -n "def X" docs/api_kz.md`)
**`nucleo/kz_espacio.py`** (nuevo, 12-oct-2026; probado en `previews/kit_hoja.jpg` con `_hoja_kit.py`):
- Cuerpos: `cuerpo_rocoso(lz,x,y,r,tipo,seed,ang_luz,rot,fase=)` (tipos `luna ceniza rojiza hielo volcanica mercurio oscura`; `fase` 0..1 = fase
  lunar limpia), `roca(...)` (asteroide/Fobos), `luna_rota(lz,x,y,r,estira,ang,t,rompe=)` (se estira, se agrieta y se parte: Roche),
  `planeta_gas(lz,x,y,r,t,paleta)` (`jupiter saturno hielo violeta rojizo`).
- Anillos: `anillo(...,mitad=0|1)` (continuo; mitad 0 ANTES del planeta, 1 DESPUÉS) y `anillo_escombros(...)` (rocas que giran, Kepler),
  `lluvia_rocas(lz,t,cx,cy,R)` (rocas con cola incandescente cayendo al planeta).
- Órbitas: `orbita(lz,cx,cy,rx,ry,tilt,...,fase=,frac=)` (discontinua que corre / se traza), `pos_orbita(cx,cy,rx,ry,tilt,ang)`, `estela(...)`.
- Zonas y puntos: `esfera_hill(lz,x,y,r,t)`, `punto_lagrange(lz,x,y,"L4",t)`, `triangulo_equilibrio(lz,Tierra,Luna,L4,t,frac=)`.
- Mareas: `tierra_marea(lz,x,y,r,t,[(ang,fuerza),...],amp=)` (agua deformada: dos lunas a 90° se anulan, a 0°/180° se suman),
  `flechas_marea(lz,x,y,r,ang,fuerza)`.
- Diagrama: `flecha`, `regla(lz,p0,p1,"384 400 km")`, `etiqueta(lz,x,y,"texto",dx,dy)`, `destello` (estrella de 4 puntas), `nebulosa`, `fondo_espacio(t,dx,dy)`.
**`nucleo/plano.py`** (ya existía): `tierra` (continentes que giran, ciudades), `luna`, `esfera`, `sol`, `planeta` (sistema solar), `kuri`,
`microbio`, `fumarola`, `termometro`, `onda`, `discontinua`, `rotulo`/`pastilla`/`linea_llamada` (texto Poppins), `humano`, `casa`, `conejo`…
`motor`: `prog`, `e_back/e_out/e_inout`, `blob`, `circulo`, `elipse`, `rect_red`, `h01`. Fondos: `F.espacio`, `F.estrellas(img,t,brillo,dx,dy)`.

## Reglas de este video (Kuriox)
- **Ritmo:** frases cortas (GAP 0,35). Algo se mueve SIEMPRE: órbitas corriendo, estelas, rocas, olas, destellos, Kuri reaccionando
  (`mirar`, `feliz`, `aleteo`). Cada concepto nuevo entra con `pop`/`e_back` + su SFX en el pulso. Kuri aparece en cada escena (pequeño, a un lado).
- **Plano secuencia:** el paso de espacio a superficie es una inmersión (la Tierra crece y su borde se aplana: clase `Sup`), nunca un corte.
  Zoom entre escalas con `interp_log` y `camino`. Sin cortes ni fundidos a negro (salvo el final).
- **Cada escena, su propio mundo visual:** distinto fondo/tinte (`F.espacio(tono=0|1)`, `nebulosa` de otro color), otra composición. Nunca
  una toma de «cuerpos quietos sobre fondo». ≥ 3 planos de profundidad: estrellas (paralaje) / nebulosa / cuerpos / etiquetas+Kuri.
- **Escala honesta o declarada:** las distancias del guion (384 400 km, 192 000 km, 1,5 millones km, 9 500–18 400 km) se dibujan con
  `regla` y números; si el dibujo no está a escala, un rótulo «sin escala» discreto.
- **Texto:** solo énfasis (cifras, nombres, L4/L5, «×8»); `rotulo`/`pastilla` ≥ 34 px; nada encima de los cuerpos ni fuera de cuadro.
- **Defectos que bloquean:** escena vacía, cuerpos sin detalle (usa `seed` distinto por cuerpo), texto que choca, algo quieto > 2 s,
  figuras minúsculas (la 2.ª luna debe notarse), cuadros negros. Revisar con la vista, a tamaño completo, un cuadro cada ~3 s.
- Sin subtítulos quemados. Música Lyria (`LYRIA` en guion.py), SFX registrados solo en la instancia `idx == 0`.

## Probar una escena sin esperar el render
`python fab.py dos_lunas escena <id> t1 t2 ...` → `previews/esc_<id>.jpg` (MÍRALA). Para el kit suelto:
`$env:PYTHONPATH="C:\FabricaAnimaciones\nucleo"; python _hoja_kit.py 2.0` (esta carpeta).
