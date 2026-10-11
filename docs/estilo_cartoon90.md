# Estilo CARTOON 90s («Coraje el perro cobarde»): tinta redibujada a mano, cuadro a cuadro

_Creado el 5-oct-2026 con `videos/gato_cobarde/` («Mostacho y el ruido de la cocina», vertical, 60 s, sin voz). Personajes ORIGINALES: solo se imita el ESTILO._

## Qué es y por qué no son «recortes»
- `ESTILO_VISUAL = "cartoon90"`, `FORMATO = "vertical"`, `SIN_VOZ = True` (compases a 96 BPM; 24 compases = 60 s). Cada clase de escena devuelve el cuadro COMPLETO (float32).
- Motor propio `nucleo/toon.py` (`Toon`): CADA cuadro se redibuja desde cero. Nada se desliza como figura rígida: las formas son curvas elásticas (blob, tubo de goma, cadena) que se estiran/aplastan con volumen.
- **El trazo se ve:** contorno de tinta de grosor variable (más grueso del lado de la sombra, ondas de presión), que se vuelve a trazar a **12 dibujos/s** (`FPS_DIB`; el movimiento va a los 30 cuadros), con 2 arcos «flojos» fuera de línea (`sketch`), relleno desfasado de la línea y sombra de celda de 2 tonos (`sombra_celda`: la parte del relleno que no cubre su copia desplazada hacia la luz).
- Acción superpuesta SIN simular (todo es función pura de `t`, así cualquier tramo se renderiza suelto): `lag`, `muelle`, `Pista` con anticipación/rebote/muelle, orejas/cola/bigotes/cascabel que reaccionan a la velocidad (`AnimGato.pose`).

## Archivos
| Archivo | Qué hace |
|---|---|
| `nucleo/toon.py` | `Toon` (lienzo, `forma`, `trazo`, `anillo`, `relleno`, cámara con capas/paralaje `pegar_capa`/`capa(prof)`, luces `luz_radial`/`luz_cono`, `final` = luz+grano+viñeta+bloom, modo `silueta`), `Pista`, `muelle`, `pulso`, `rebote`, `lag`, `tiembla`, geometría (`blob`, `tubo`, `eje_curvo`, `espinas`, `ondular`) |
| `nucleo/toon_gato.py` | Mostacho: ~45 parámetros (`DEF`), caras prefabricadas (`CARAS`: dormido, susto, terror, grito, tragar, sospecha, feliz…), `AnimGato` (claves + secundario automático), `pasos()` (ciclo de caminar de puntitas sin patinar: v = 4·zancada·s/T), linterna |
| `nucleo/toon_cosa.py` | La Cosa (monstruo gelatinoso, 3 ojos), `AnimCosa`, `anclas()` para colgar objetos de sus manos/boca |
| `nucleo/toon_fondos.py` | `Pintor`: fondos pintados (polígonos de borde rugoso, pinceladas, brillos, luz derramada, alfa acumulado → `rgba_auto()`), `plano_persp` |
| `nucleo/sfx_toon.py` | 40 efectos propios (gritos con formantes, cascabel, crujidos, refri, tripas…); se importan al final de `sfx.py` |
| `videos/gato_cobarde/` | `mundos*.py` (fondos), `props*.py` (murciélagos, puerta del refri, ojo gigante, lámpara…), `esc_<id>.py` (una escena por archivo), `basec.py` (clase `Base`), `_prueba.py` |

## Cómo se escribe una escena
```python
class Sala(Base):                       # basec.Base: dibujar(h, t, u) con u = t - self.t0; post() retoca el cuadro final
    def sonidos(self): self.ev(self.t0 + 2.2, "crujido", 0.7)
    def preparar(self):
        super().preparar(); self.g = Gato(); self.A = AnimGato(x=[(0,650),(2,500,'o')], cara=[(0,'dormido'),(2.5,'alerta','o')], ...)
    def dibujar(self, h, t, u):
        h.camara(zoom, cx, cy, rot); [h.pegar_capa(*c) for c in capas]; self.g.dibujar(h, self.A.pose(u)); h.luz_radial(...)
```
- Tipos de llegada de `Pista`: `l i o io b B a m M h` (ver docstring). `cara=[(t,'nombre','tipo')]` mezcla caras.
- **Coordenadas:** `forma`/`trazo` reciben coordenadas del MUNDO (aplican la cámara); `relleno`/`anillo` reciben PANTALLA (`h.tf(P)`). El rig devuelve coordenadas de mundo: nunca apliques la cámara dos veces (bug de 5-oct: formas desplazadas al hacer zoom).
- Las luces se MULTIPLICAN sobre todo el cuadro (`h.ambiente`): pinta los fondos con valores medios y deja el dramatismo a la luz; el gato lleva `h.tinte` propio.
- Sentado detrás de un mueble: pies recogidos (`pie_*` a la altura de la cadera) y capa «frente» pintada que se dibuja DESPUÉS del personaje.
- Cada escena debe poder renderizarse suelta: nada de estado entre cuadros. Transiciones = efectos locales (flash de color, barrido con desenfoque horizontal, iris), no cortes duros.

## Prueba y revisión
`python videos/<v>/_prueba.py <escena> u1 u2 ...` (tiempos LOCALES; `u0..u1:paso` para cuadros consecutivos; `--cols 6 --solo-hoja`). Revisa a tamaño completo (`previews/p_<escena>_<u>.png`) y tiras de cuadros consecutivos para ver la fluidez.
Medido: ~0,3–0,5 s/cuadro, ~1 GB RSS (2 GB commit) por proceso; los fondos pintados se cachean por proceso (LRU de 2).

## Lecciones
- Comandos > ~8 KB fallan: escribe archivos con Write.
- `pegar_capa` acepta RGB (opaco) o RGBA premultiplicado. Capas con paralaje: prof 0 = infinito, 1 = plano del personaje, >1 = primer plano (se desenfoca).
- Los personajes grandes necesitan escala coherente con el cuarto (el gato mide ~750 px a s=1,35: el techo está a 1 350 px del suelo).
- El monstruo y el gato no se tocan: pelear con la geometría (sombras proyectadas con `h.silueta`, manos con `anclas()`) cuesta más que un gag a distancia.
- Música: `musica` sintetiza un acompañamiento genérico; para algo mejor, Lyria (`LYRIA` en guion.py, `python lyria.py --n 1`).
