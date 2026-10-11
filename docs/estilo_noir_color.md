# Estilo NOIR COLOR (neo-noir apagado) y su variante FEUDAL

_Creado el 11-oct-2026 a pedido del usuario: «estilo noir, misma esencia, pero con un poco más de color, manteniendo el tono oscuro y
apagado». El mismo día pidió la **variante feudal**: un detective de la época (pesquisidor) que analiza casos, personas y sucesos
antiguos, para contar historias de sagas de fantasía medieval (Game of Thrones, House of the Dragon…) y para canales de historia
antigua/medieval. Pruebas de 30 s: `videos/prueba_noir_color/` y `videos/prueba_noir_feudal/`._

## Qué es (y qué NO cambia respecto al noir B/N)
- La esencia es la de `docs/estilo_noir.md`: tinta y aguada, claroscuro multiplicativo, persianas, lluvia/humo/polvo que solo brillan
  donde hay luz, niebla volumétrica, tramado de plumilla, contraluz, papel, grano, polvo de película, transiciones de mancha de tinta,
  texto a máquina, sello. Todas sus reglas (variedad, nada quieto, texto paralelo al soporte, caminar sin patinar, medios reales) siguen.
- Lo nuevo es el COLOR, y siempre **oscuro y desaturado**. Se consigue con tres capas, sin pintar «a color» a mano:
  1. **Rampas por material** (mapa de degradado: el VALOR elige el color; lo oscuro tira a tinta fría, lo claro a cálido apagado).
     Se sigue pensando en tonos 0..255 como en el noir; `h.pieza(..., rampa="madera")`, `with h.con_rampa("papel"):`, y los fondos
     de `noir_fondos.Lienzo` (gris) se pegan con `NC.pegar(capa, h, prof, rampa="ladrillo")`.
  2. **Luces de color** que multiplican: sodio/antorcha ámbar, luna azul acero, un neón o lámpara de acento. La lluvia, el humo y la
     niebla toman el color de la luz que los atraviesa; las ventanas, faroles, neones y llamas emiten con SU color.
  3. **Etalonaje** (`PALETAS`): curva S sobre la luminancia, saturación global baja (0,55-0,62), negro tintado, sombras frías y luces
     cálidas, papel y grano.
- **Regla de color por plano: dos temperaturas + UN acento.** Frío (luna) contra cálido (sodio/vela) y un solo color fuerte de acento
  (neón rojo, lámpara verde, lacre, estandarte). Lo que el guion quiere señalar puede ser lo único con color: en la prueba, la foto del
  sospechoso se dejó en B/N (`rampa="neutro"`) sobre una mesa a color.

## Kit (núcleo)
| Archivo | Qué hace |
|---|---|
| `nucleo/noir_color.py` | `NoirColor(Noir)`: la misma interfaz que `Noir` (los personajes, `texto_maquina`, `sello`, `lluvia`, `humo`, `reflejo`, `transicion`, `tinta_cubre` funcionan igual). Añade: `RAMPAS` + `lut/col`, `con_rampa()`, `c(v, rampa)`, `rim_color(col)` (el contraluz toma el color de la luz principal), luces en color (`luz_persiana(..., col=)`, `luz_mascara(..., col=)`, `mapa_rgb`), emisión en color (`emitir(P, v, col=)`, `resplandor(x, y, r, v, col)`, `teñir_emision`), `acabado(..., sat=, col_A=)` en color y `pegar(capa, h, prof, rampa, bruma, col_emis, emis)` para fondos grises. Paletas: **sodio** (calle de noche: ámbar contra azul acero, neón rojo; la de referencia), **bourbon** (interiores: fluorescente verdoso y whisky, vino), **medianoche** (azul y violeta, magenta). Colores con nombre por paleta: `h.pal["sodio"|"luna"|"neon"|"lampara"|"verde"|"relampago"|"sello"|"tinta"|"papel"]`. |
| `nucleo/noir_feudal.py` | **Variante feudal.** Paletas **antorcha** (noche: antorcha/vela contra luna, acento lacre; la de referencia) y **pergamino** (interiores más cálidos). Rampas de época: `muralla`, `entramado`, `teja`, `lana`, `cuero`, `hierro`, `estandarte`, `pergamino`, `cera`, `lacre`, `oro`. Fondos (Lienzo): `sillares`, `muralla` (almenas, adarve, saeteras), `torre` (techo cónico con veleta o almenada), `saetera`, `casa_entramado` (vigas, voladizo, ventanucos emplomados, tejado, chimenea, puerta), `soporte_antorcha`, `adoquines`. Por cuadro: `llama` (fuego vivo emisivo, devuelve su intensidad), `antorcha` (con luz, humo), `vela` (palmatoria, chorretones, llama y luz), `estandarte` (tela que ondea con emblema sol/torre/luna/llave), `lacre` (gota que cae y el anillo que la sella), `vaho` (aliento en el frío). Personajes: **`Pesquisidor(Detective)`** (capucha, capa de lana que ondea, gambesón, barba, FAROL de mano en vez de cigarro; `alzar` levanta el farol; camina igual que el Detective) y **`BustoEncapuchado`** (primer plano de perfil con capucha honda, barba, broche, respiración). Fuentes: `FUENTE_GOTICA` (Old English, titulares) y `FUENTE_PLUMA`/`FUENTE_PLUMA_R` (Bookman: el cuerpo «escrito a pluma» con `texto_maquina`). |
| `nucleo/noir_corte.py` | **Reparto de corte medieval** (11-oct-2026, `videos/got_joffrey/`). `BustoCorte(sem, **rasgos)`: primer plano de perfil con rasgos configurables — `pelo` (corto/melena/largo/trenza/calvo/ninguno, `pelo_rampa`/`pelo_tono`), `barba` (perilla/corta/rala), `corona` (rey = corona de puntas con gemas / diadema), `toca` (velo y griñón de anciana), `edad` (arrugas), `joven`/`fem`, `nariz` (recta/aguileña/pequeña), `ropa`/`capa` = (rampa, tono) (con corona de rey y capa: armiño), `cuello="escote"`, `collar=n` piedras con `falta=i` (engaste vacío; `p["falta"]=False` lo muestra completo; `piedras()` da sus posiciones). Pose: `boca`, `ojo`, `mira`, `adelante`, `ceño`, `sonrisa`, `cab_rot`, **`ahogo`** (tiembla, ojos desorbitados, boca abierta, la cara se amorata con la rampa `purpura`) y `manos_cuello`. `Cortesano(sem, **rasgos)`: cuerpo entero de perfil 3/4 con túnica (acampanada si `fem`), capa, brazos con codo (`mano=(x, y)` local, `mano2`), `alto=0.62` (enano: cuerpo corto, cabeza igual), `baston`, `bufon` (remiendos y calzas a rayas), `rot` (cae girando sobre los pies), `inclina`, `andar`/`paso`, `cab=dict(...)` para la cara; `puntos(p)` da la mano y la cabeza en mundo (para copas, espadas, saetas). `comensales(h, t, x0, x1, y, n, s, reaccion, mira_x)`: fila de invitados sentados tras una mesa, con tocados variados, que charlan, beben y, con `reaccion`, se levantan y miran. Rampas nuevas: `purpura` (el acento del veneno), `azul`, `armino`. Personajes PROPIOS: nunca el aspecto de los actores de una serie. |

## Receta (lo mínimo para un plano)
```python
import noir as N, noir_color as NC, noir_feudal as NF     # NF solo para la época feudal (registra sus paletas y rampas)
h = NC.NoirColor("sodio")            # o "bourbon", "medianoche", "antorcha", "pergamino" — una por proceso
h.nuevo(t); h.camara(z, cx, cy)
h.rim_color(h.pal["sodio"])          # el contraluz de las piezas toma el color de la luz principal
NC.pegar(cielo, h, 0.05, rampa="cielo"); NC.pegar(medio, h, 0.6, rampa="ladrillo", bruma=0.22)
NC.pegar(letrero, h, 1.0, rampa="vino", emis=1.2 * parpadeo, col_emis=h.pal["neon"])   # cada fuente de color en su propia Capa
personaje.dibujar(h, pose)           # Detective / Busto / Pesquisidor: sin rampa usan la del personaje (gabardina caqui, piel cálida)
h.ambiente[:] = np.array(h.pal["luna"]) * 0.8                   # ambiente frío: ~0,8 calle, ~0,3 interior, ~0,25 mesa
h.luz_cono(x, y, ang, abre, largo, h.pal["sodio"], k=1.5)        # luz cálida principal
img = h.acabado(t, niebla=dict(dens=0.26))
```
- Cada fuente emisiva de **otro color** (neón, ventanas, farol) va en su propia `Capa` para darle `col_emis`; con `pegar` las ventanas de
  una capa salen todas del mismo color (por defecto, la lámpara de la paleta).
- Suelo mojado: refleja también el color de la emisión (copiar `reflejar()` de `videos/prueba_noir_color/prueba.py`).
- Montaje igual que el noir: planos con `transicion(..., "tinta")`; para un video con guion usar `BaseNoir` de `videos/ia_noir/basen.py`
  cambiando `lienzo()` por `NoirColor(...)`.

## Lecciones de la prueba (11-oct-2026)
- **Con color, la luz de ambiente se queda corta:** el noir B/N usaba 0,78 gris; con `luna * 0,55` la calle quedó azul marino plano.
  Calle de noche: `luna * 0,8` + sodio k≈1,5. Interiores: `luna * 0,3` + persiana/neón/lámpara. Mesa: `luna * 0,25-0,3` y DOS fuentes
  cálidas si hay utilería lejos de la principal (si no, la copa o el tintero quedan negros).
- Lo que se pinta oscuro contra un fondo oscuro desaparece (poste de farola, asta): darle un **filo de luz** (línea clara del lado de la
  luna) en el Lienzo, como el contraluz del noir.
- Un Lienzo que no cubre la altura de lo que se pinta lo corta en silencio (la farola sin poste): el `origen`/alto del Lienzo debe
  abarcar todo.
- Edificio de cristal lejano con bruma = «barras flotantes» de luz en el cielo: fuera de los fondos lejanos.
- Sombra de capucha/ala con borde recto sobre los ojos parece un antifaz: contorno curvo (`suave`) y alfa ≈ 0,7.
- La capa aditiva (humo, lluvia) se suma ENCIMA de todo: una antorcha tapada por un personaje deja su humo flotando delante de él.
  Las fuentes con humo, siempre visibles.
- Coste: ~1-2 s por cuadro a 1080p (6 procesos: 30 s de video en ~10 min).

## Lecciones del primer video completo («¿Quién envenenó al rey?», `videos/got_joffrey/`, 11-oct-2026)
- `ESTILO_VISUAL = "noir_feudal"` ya está registrado en `nucleo/estilos.py`; la base de escenas es `videos/got_joffrey/basen.py`
  (BaseNoir con `NoirColor("antorcha")`), con `comun.py` (`banda` en color, `cartela` = pergamino con el nombre en gótica y una
  línea a pluma, `reflejar`, `T_obj`).
- Arreglados en el núcleo: `NoirColor.mapa_rgb` con luz fija (los rótulos con `luz_fija` rompían cv2 al escribir en un canal suelto) y
  `NF.almenas` con semillas negativas (muralla que empieza en x < 0).
- `NC.pegar` lee UNA rampa por capa: un muro con tapices = dos Lienzos (piedra en `muralla`, tapices en `estandarte`).
- Los `comensales` son caros (≈ 8 piezas cada uno): los lejanos van sin tramado; un salón con 36 invitados + 3 candelabros ≈ 10-15 s
  por cuadro con la CPU libre (×10 si hay otro render en marcha).
- Personajes de cuerpo entero: el codo con `flex=1` siempre (si no, el brazo colgando dobla hacia arriba).

## Pruebas
- `python videos/prueba_noir_color/prueba.py hoja 2 9 14 26` · `paletas 9` (sodio/bourbon/medianoche lado a lado) · `video --procs 6 --paleta sodio`
- `python videos/prueba_noir_feudal/prueba.py hoja 2 9 14 26` · `paletas 9` (antorcha/pergamino) · `video --procs 6 --paleta antorcha`
- Salidas en `salida/` de cada carpeta (E:, junction).
