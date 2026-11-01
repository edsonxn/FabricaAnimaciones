# Catálogo del kit Kurzgesagt (generado por `python nucleo/api_kz.py`; no editar a mano)

Formato: `def nombre(args)` — primera línea del docstring. Busca con grep; abre el módulo solo para el rango que necesites.


## nucleo/kz_abstracto.py — Conceptos abstractos del estilo Kurzgesagt (referencia: «This Woman Cured Her Cancer…»): ideas que no se pueden filmar se dibujan con formas,

- `def titulo_textura(lz, texto, x, y, px, t, paleta=((108, 40, 150), (255, 150, 44), (255, 204, 70), (236, 70, 140), (90, 210, 190)), k=1.0, alfa=1.0, seed=3, vel=22.0, sombra=(14, 6, 40), ancla=(0.5, 0.5), capa=2, nombre='geo_x')` — Texto grande relleno con un patrón de flores que se desliza lentamente. (x, y) = centro; px = alto de letra.
- `def petalos(lz, t, t0, origen, n=24, dur=2.6, color=((255, 150, 44), (255, 204, 70), (236, 70, 140)), vel=(160, 420), g=-80.0, spread=(-math.pi, 0.0), tam=(10, 22), seed=1, capa=2, alfa=1.0, viento=40.0)` — Ráfaga de pétalos desde `origen` (px). Todo es función de t. spread = rango de ángulos de salida (rad, 0 = derecha, -pi/2 = arriba).
- `def corriente(lz, t, trayecto, n=40, ancho=26.0, vel=0.22, color=((255, 120, 90), (255, 200, 90)), r=(4.0, 8.0), seed=1, capa=1, alfa=1.0, estela=0.0)` — n partículas que avanzan por la curva `trayecto` (puntos en px; se suaviza con Catmull-Rom). Cada una con su desfase y su carril (ancho en px).
- `def halo_punto(lz, x, y, r, t, color=(60, 220, 210), nucleo=(10, 4, 20), latido=0.12, capa=2, alfa=1.0, seed=0)` — Punto oscuro con halo de color que late: el concepto «algo ahí dentro» sin dibujar el objeto.
- `def barrido(lz, t, t0, dur=0.9, color=(255, 255, 255), ang=0.0, alfa=0.9, ancho=0.45, capa=2)` — Ola de color que cruza la pantalla con borde ondulado (sin dejar nada detrás salvo la luz del frente).
- `def grano(img, t, fuerza=0.025)` — Grano fino sobre el cuadro (img float32 HxWx3 en [0,1]).
- `def contador_atras(lz, x, y, valor, px=120, color=(255, 255, 255), k=1.0, alfa=1.0, fuente_='geo_x')` — Cifra grande centrada (entero) con sombra suave; el que llama anima `valor` (p. ej. 2026 -> 1541 con e_inout).
- `def medallon_tiempo(lz, x, y, r, t, hitos, actual=0.0, color_borde=(255, 200, 70), ancho=900, y_linea=None, alfa=1.0)` — Línea de tiempo horizontal con hitos [(etiqueta, ...)] y un medallón circular que se desliza al hito `actual` (fracción 0..n-1).

## nucleo/kz_espacio.py — BAÚL ESPACIAL Kurzgesagt (12-oct-2026, nacido en `videos/dos_lunas/`): lunas con cráteres, asteroides, lunas que se

- `def cuerpo_rocoso(lz, x, y, r, tipo='luna', seed=0, ang_luz=math.pi * 1.25, luz=1.0, rot=0.0, sombra=-0.15, alfa=1.0, tinte=None, fase=None)` — Luna / planeta enano / asteroide grande: disco con mares, cráteres (con borde de luz) que giran con `rot`, y 2 tonos de
- `def roca(lz, x, y, r, seed=0, rot=0.0, tipo='ceniza', ang_luz=math.pi * 1.25, luz=1.0, alargada=1.35)` — Asteroide / luna-patata (Fobos, el visitante que pasa): polígono irregular con sombra y cráteres. Misma luz que `cuerpo_rocoso`.
- `def terminador_gran(x, y, r, ang_luz)` — Media luna de sombra (lado opuesto a la luz) para recortar sobre formas irregulares.
- `def luna_rota(lz, x, y, r, estira, ang, t, seed=0, tipo='luna', rompe=0.0, ang_luz=math.pi * 1.25)` — Luna estirada por la marea hacia el planeta (`ang` = dirección del planeta). estira 0..1: elipse alargada con grietas de
- `def luna_dos_caras(lz, x, y, r, rot=0.0, ang_luz=math.pi * 1.25, alfa=1.0, panqueque=0.0, seed=1, sombra=-0.55)` — La Luna con sus DOS caras: `rot`=0 enseña la visible (lisa, con grandes mares oscuros) y `rot`=pi la oculta (llena de cráteres,
- `def planeta_gas(lz, x, y, r, t=0.0, paleta='jupiter', seed=0, luz=1.0, ang_luz=math.pi * 1.25, tormenta=True, tilt=-0.2)` — Gigante gaseoso genérico con bandas que ondulan. paleta: clave de GIGANTES o lista de 4 colores.
- `def anillo(lz, x, y, r_in, r_out, tilt=-0.25, incl=0.3, mitad=1, col=(226, 204, 150), alfa=1.0, bandas=3)` — Anillo continuo de un planeta. mitad=0: la mitad de ATRÁS (dibújala antes del planeta); mitad=1: la de ADELANTE (después).
- `def anillo_escombros(lz, x, y, r_in, r_out, t, n=120, seed=0, incl=0.3, tilt=-0.25, mitad=1, col=(176, 168, 190), tam=7.0, vel=1.0, brillo=0.0)` — Anillo de pedazos de roca que giran (ω ∝ ρ^-1,5, Kepler). mitad=0 atrás / 1 adelante (como `anillo`). brillo 0..1 añade
- `def lluvia_rocas(lz, t, cx, cy, R, n=26, seed=0, ciclo=1.6, largo=1.0)` — Rocas que caen en línea recta hacia el centro del planeta (cx, cy, radio R) con cola incandescente al entrar.
- `def pos_orbita(cx, cy, rx, ry=None, tilt=0.0, ang=0.0)` — Punto de una órbita elíptica (centro, semiejes, giro) para el ángulo `ang` (rad). ry=None -> círculo.
- `def orbita(lz, cx, cy, rx, ry=None, tilt=0.0, color=(150, 170, 235), ancho=3.0, alfa=0.7, dash=True, frac=1.0, fase=0.0, capa=None)` — Órbita elíptica. dash: línea discontinua que 'corre' con `fase` (px); frac<1 la dibuja solo en parte (se traza).
- `def estela(lz, cx, cy, rx, ry, tilt, ang, color=(190, 205, 255), largo=1.1, ancho=11.0, sentido=1, n=22)` — Cola luminosa que se desvanece detrás de un cuerpo que va por la órbita (en `ang`), hacia atrás `largo` rad.
- `def esfera_hill(lz, x, y, r, t, color=(120, 160, 255), alfa=1.0)` — Esfera de Hill / zona de influencia: disco translúcido con borde discontinuo que respira y destellos en el borde.
- `def punto_lagrange(lz, x, y, nombre, t, s=1.0, color=(255, 214, 90), alfa=1.0, rotulo=True, lado=1)` — Marca de punto de equilibrio (L4/L5...): rombo que pulsa con halo y su nombre.
- `def triangulo_equilibrio(lz, a, b, c, t, color=(255, 214, 90), alfa=1.0, frac=1.0)` — Triángulo equilátero punteado Tierra–Luna–L4/L5 (a, b, c son puntos (x, y)).
- `def abultamiento_marea(lz, x, y, r, lunas, amp=0.22, color=(76, 164, 246), alfa=0.95)` — Capa de agua de la Tierra deformada por una o varias lunas: lunas = [(ang, fuerza)] (ang = dirección a la luna, fuerza 0..1+).
- `def tierra_marea(lz, x, y, r, t, lunas, rot=0.0, luz=1.0, ang_luz=math.pi, amp=0.2)` — La Tierra con su agua deformada hacia/contra cada luna (ver `abultamiento_marea`).
- `def flecha(lz, p0, p1, color=(255, 255, 255), ancho=5.0, frac=1.0, alfa=1.0, cabeza=None, capa=None)` — Flecha de p0 a p1 (se dibuja hasta `frac`). La cabeza mide `cabeza` px (por defecto 3.2×ancho).
- `def flechas_marea(lz, x, y, r, ang, fuerza=1.0, color=(255, 214, 90), t=0.0)` — Par de flechas del tirón de marea (lado cercano más fuerte, lado lejano más débil) hacia la luna en la dirección `ang`.
- `def regla(lz, p0, p1, texto, color=(255, 255, 255), px=34, alfa=1.0, frac=1.0, lado=1, fondo=None)` — Cota de distancia con topes en los extremos y pastilla con el texto a la mitad (ej. «384 400 km»).
- `def etiqueta(lz, x, y, texto, dx=80.0, dy=-70.0, px=34, color=(255, 255, 255), fondo=None, alfa=1.0, frac=1.0)` — Rótulo con línea de llamada desde un cuerpo en (x, y): pastilla en (x+dx, y+dy).
- `def fondo_espacio(t, brillo=1.0, dx=0.0, dy=0.0, tono=0)` — Fondo de espacio (degradado noche->violeta + nebulosa + estrellas titilantes con paralaje dx/dy en px).
- `def nebulosa(lz, x, y, r, color=(160, 90, 220), seed=0, alfa=0.5, capa=0)` — Nube de gas de color propia (varios halos desplazados). Úsala sobre el fondo, antes de los cuerpos.
- `def destello(lz, x, y, r, t, color=(255, 255, 255), alfa=1.0, capa=2)` — Estrella de 4 puntas que centellea (para brillos, descubrimientos, remates).
- `def fantasma(lz, x, y, r, t, alfa=1.0)` — Cuerpo hipotético: disco translúcido con contorno punteado que corre.
- `def marca_x(lz, x, y, s=1.0, k=1.0, color=(255, 90, 110))` — ✗ roja (entra con rebote: k es la escala).
- `def bez2(p0, p1, p2, u)` — Bézier cuadrática (p. ej. aproximación de un asteroide hasta el periapsis antes de pasar a `kepler`).
- `def kepler(a, e, w, M)` — Posición relativa al foco para la anomalía media M (periapsis en el ángulo w; sentido horario en pantalla).
- `def trail(lz, f, t, dur=0.5, n=12, color=(255, 255, 255), ancho=7.0)` — Estela de un objeto cuya posición en pantalla es f(tt), afinándose hacia atrás. f debe valer también para tiempos

## nucleo/kz_gente_iso.py — Personas y animales diminutos del mundo isométrico (estilo Kurzgesagt): carteles en pantalla con 3/4 de frente o de espalda, caminata con balanceo y rebote,

- `def persona(lz, iso, x, y, t=0.0, tipo='campesino', dir=(1.0, 0.0), vel=0.0, seed=0, piel=None, h=34.0, accion=None, z=0.0, tp=0.0, rop=None, sombra=True, alfa=1.0, carga=None, cara=None)` — Persona de h unidades de mundo en (x, y). dir = hacia dónde mira/camina (mundo); vel = ritmo de la caminata (0 = parada). accion: None|'saluda'|'vitorea'|'trabaja'|'reza'|'pelea'|'habla'|'carga'|'cae'.
- `def oveja(lz, iso, x, y, t=0.0, dir=1, seed=0, s=1.0)`
- `def gallina(lz, iso, x, y, t=0.0, dir=1, seed=0, color=(178, 74, 138))`
- `def cerdo(lz, iso, x, y, t=0.0, dir=1, seed=0)`
- `def burro(lz, iso, x, y, t=0.0, dir=1, seed=0, carga=True, s=1.0, color=(150, 140, 134))`
- `def caballo(lz, iso, x, y, t=0.0, dir=1, seed=0, color=(150, 98, 68), vel=0.0, jinete=None, s=1.0)` — Caballo en 3/4 (pequeño). jinete = tipo de persona montada o None.
- `class Multitud` — Agentes que siguen trayectos (o rondan un punto) con fases propias. Todo es función de t (cada cuadro es independiente).
    - `.camina(self, trayecto, tipo='campesino', vel=18.0, fase=0.0, seed=0, h=34.0, bucle=True, accion=None, t0=0.0, t1=None, **kw)` — Agente que recorre una polilínea del suelo a `vel` unidades/s (rebota o repite).
    - `.ronda(self, centro, radio, tipo='campesino', n=1, vel=6.0, seed=0, h=34.0, accion=None, **kw)` — n agentes que deambulan cerca de un punto.
    - `.quieto(self, pos, tipo='campesino', dir=(1.0, 0.0), seed=0, h=34.0, accion=None, **kw)`
    - `.estado(self, a, t)`
    - `.dibujar(self, mundo, t, iso=None)`
- `def iso_k()`

## nucleo/kz_iso.py — Motor isométrico para el estilo Kurzgesagt (dioramas de pueblos, fuertes, ciudades), sobre el Lienzo (polígonos planos, sin contornos).

- `def luz(mul=(1.0, 1.0, 1.0), mix=None, k=0.0)`
- `def tint(c)` — Color de la escena bajo la luz actual.
- `def tonos(c)` — (arriba, izquierda iluminada, derecha en sombra) de un color base.
- `class Iso` — Cámara isométrica. z = px por unidad de mundo.
    - `.P(self, x, y, z=0.0)`
    - `.pts(self, p3)`
    - `.visible(self, x0, y0, x1, y1, h=0.0, margen=140.0)` — ¿Su caja de mundo toca la pantalla?
    - `.inv_suelo(self, sx, sy)` — Punto del suelo (z=0) bajo el píxel (sx, sy).
- `def suelo(lz, iso, pts_xy, color, z=0.0, alfa=1.0)`
- `def suelo_rect(lz, iso, x, y, w, d, color, z=0.0, alfa=1.0)`
- `def suelo_curvo(lz, iso, pts_xy, color, z=0.0, alfa=1.0, n=10)` — Polígono de suelo con bordes suaves (Catmull-Rom cerrado).
- `def camino(lz, iso, pts_xy, ancho, color, borde=None, z=0.0, alfa=1.0, n=10)` — Camino de ancho constante a lo largo de una polilínea (suavizada), con borde más oscuro opcional.
- `def cuadricula(lz, iso, x0, y0, x1, y1, paso, color=(255, 255, 255), alfa=0.08, ancho=1.2, z=0.0)` — Líneas de la rejilla isométrica (baldosas) muy tenues sobre el suelo.
- `def sombra_suelo(lz, iso, x, y, w, d, h, k=0.55, alfa=0.2, dx=1.0, dy=0.28)` — Sombra proyectada sobre el suelo (cae hacia +x, la luz viene de la izquierda).
- `def sombra_elipse(lz, iso, x, y, rx, ry, alfa=0.22)`
- `class Caja` — Prisma rectangular alineado a los ejes: esquina (x, y) mínima, tamaño (w, d, h), base a altura z0.
    - `.punto(self, cara, a, b)` — Punto 3D de la cara 'y' (izquierda, plano y+d, a a lo largo de +x) o 'x' (derecha, plano x+w, a a lo largo de +y), b = altura sobre la base.
    - `.rect(self, cara, a0, a1, b0, b1)`
- `def caja(lz, iso, x, y, w, d, h, color, z0=0.0, t3=None, alfa=1.0)` — Dibuja un prisma con 3 caras. Devuelve la Caja (para colocar ventanas, puertas y techos).
- `def cara_rect(lz, iso, c, cara, a0, a1, b0, b1, color, alfa=1.0, tono=True)` — Rectángulo pegado a una cara de la caja (ventana, puerta, franja). Si tono, se oscurece en la cara derecha.
- `def cara_arco(lz, iso, c, cara, a0, a1, b0, b1, color, alfa=1.0, n=10)` — Vano con arco de medio punto (puerta, ventana, portal) en una cara.
- `def hilera_ventanas(lz, iso, c, cara, n, b0, alto, ancho, margen_a=0.1, color=(86, 58, 96), marco=None, rejas=False, postigo=None)` — n ventanas iguales repartidas a lo largo de la cara.
- `def techo_dos_aguas(lz, iso, c, eje, hr, color, vuelo=4.0, gablete=None, tejas=True, grosor=2.2)` — Techo a dos aguas sobre la caja c. eje = 'x' (cumbrera paralela a x) o 'y'. hr = altura de la cumbrera sobre el borde. gablete = color del hastial.
- `def c_wall(c)`
- `def techo_plano(lz, iso, c, color, borde=3.0, alto=2.5)` — Azotea con pretil: aro bajo en el borde y fondo ligeramente más oscuro.
- `def techo_piramide(lz, iso, c, h, color, vuelo=2.0)` — Techo piramidal (torres, kioscos).
- `def cilindro(lz, iso, x, y, r, h, color, z0=0.0, tapa=True, n=20, t3=None)` — Cilindro vertical de radio r (en unidades de mundo): franjas iluminada / media / sombreada.
- `def cono(lz, iso, x, y, r, h, color, z0=0.0, n=18)`
- `def cupula(lz, iso, x, y, r, color, z0=0.0, n=24, linterna=True)` — Cúpula semiesférica con degradado por franjas.
- `def cruz(lz, iso, x, y, z, s=1.0, color=(250, 244, 230))`
- `class Mundo` — Lista de objetos con su huella en el mundo; se dibujan de atrás hacia delante. `fijos` persisten; `dinamicos` se vacían cada cuadro.
    - `.add(self, x0, y0, x1, y1, h, fn, fijo=True, clave=None)`
    - `.nuevo_cuadro(self)`
    - `.dibujar(self, lz, iso)`
- `def isla(lz, iso, x0, y0, x1, y1, color_top=(120, 188, 96), esp=34.0, c_tierra=(150, 100, 70), c_roca=(122, 104, 148), sombra=True, t=0.0, seed=0)` — Losa de terreno flotante (diorama) con tierra y roca debajo y sombra lejana. Dibujar ANTES de los objetos del suelo y después del fondo.
- `def habitacion(lz, iso, x, y, w, d, h, piso=(176, 120, 86), pared_a=(250, 232, 196), pared_b=None, friso=(150, 100, 80), espesor=4.0)` — Habitación en corte (casa de muñecas): suelo y dos paredes de fondo (planos x e y mínimos) vistas desde dentro. Devuelve la Caja para colocar ventanas y cuadros.

## nucleo/kz_iso_arq.py — Arquitectura colonial mexicana en isométrico (estilo Kurzgesagt): casas, iglesias de dos torres, portales, haciendas, alhóndiga, fuertes, minas, puentes…

- `def casa_colonial(mundo, x, y, w, d, h, muro=CAL, techo=TEJA, eje='x', zocalo=None, ventanas=2, puerta=True, balcon=False, chimenea=False, humo_t=None, toldo=None, seed=0, hr=None, t_fn=None)` — Casa de uno o dos niveles con techo de teja a dos aguas, zócalo de color, ventanas con rejas, puerta con arco y (opcional) balcón y chimenea.
- `def casa_plana(mundo, x, y, w, d, h, muro=CAL, acento=AZUL, seed=0, ventanas=2)` — Casa de azotea plana con pretil (típica de pueblo y ciudad), con barda y puerta con marco de color.
- `def iglesia(mundo, x, y, w=70, largo=120, h_nave=60, muro=CANTERA, techo=TEJA, torres=2, cupula_c=True, luz_ventanas=0.0, campana=None, t_fn=None)` — Iglesia colonial: nave a dos aguas con la fachada en el extremo +y (cara iluminada), portada de cantera con arco, columnas, nicho, ventana del coro y 1-2 torres con campanario.
- `def portal_arcos(mundo, x, y, n, paso=20, d=14, h=40, muro=CAL, eje='x', techo=TEJA)` — Portal con arcos (arcada de un edificio público): n arcos a lo largo de x, con columnas y techo plano.
- `def puesto(mundo, x, y, w=26, d=18, toldo=(236, 90, 96), cosas=(250, 190, 70), seed=0)` — Puesto de mercado: mesa de madera, 4 postes y toldo a rayas.
- `def hacienda(mundo, x, y, w=150, d=110, muro=OCRE, techo=TEJA2, capilla=True)` — Casa grande de hacienda: cuerpo en L con portal, capilla y torre-campanario pequeña.
- `def torre_vigia(mundo, x, y, h=64, w=26, base=PIEDRA, techo=(210, 150, 80))`

## nucleo/kz_iso_arq2.py — Más arquitectura y utilería isométrica para historia de México (estilo Kurzgesagt): alhóndiga, palacio, catedral, fuerte con baluartes, mina y malacate,

- `def alhondiga(mundo, x, y, w=150, d=120, h=84, muro=(226, 196, 176), t_fn=None, puerta_fuego=0.0, bandera_luto=False)` — Alhóndiga de Granaditas (Guanajuato): bloque macizo de piedra rosada de dos niveles con patio, ventanas altas y estrechas, portón de madera y pretil almenado.
- `def palacio(mundo, x, y, w=240, d=60, h=72, muro=TEZONTLE, t_fn=None, campana=True)` — Palacio Nacional / Virreinal: edificio largo y bajo de piedra rojiza (tezontle) con marcos blancos, tres portones, balcón central y torre-campanario.
- `def catedral(mundo, x, y, w=120, largo=150, h=80)` — Catedral Metropolitana (esquema): nave larga, fachada con tres portadas, dos torres altas con campanario y cúpula central.
- `def casa_alta(mundo, x, y, w, d, h, muro=A.CAL, acento=A.AZUL, techo=A.TEJA, seed=0)`
- `def choza(mundo, x, y, r=11, h=14, seed=0, techo=(226, 190, 100))` — Choza de adobe con techo cónico de palma (pueblos y rancherías).
- `def tienda_campana(mundo, x, y, w=30, d=22, color=(246, 240, 226), franja=(206, 70, 70), bandera=None, t_fn=None)` — Tienda de campaña militar (prisma triangular con bandera).
- `def canon(mundo, x, y, dir=1, t_fn=None, disparo=-1.0, escala=1.0)` — Cañón sobre cureña con ruedas (apunta hacia ±x en pantalla). disparo = tiempo desde el disparo (para humo y retroceso).
- `def barco(mundo, x, y, t_fn=None, s=1.0, vela=(250, 244, 230), casco=(120, 80, 60), banderas=(206, 66, 66), dir=1)` — Galeón de vela (3/4): casco con castillo de popa, dos mástiles y velas hinchadas, cabeceo suave sobre el agua.
- `def muelle(mundo, x, y, largo=90, ancho=16, h=6, eje='x')` — Muelle de madera sobre pilotes. eje='x' (largo a lo largo de x) o 'y' (hacia el agua en y).
- `def puente_piedra(mundo, x, y, largo=120, ancho=30, h=26, arcos=4, muro=(214, 196, 178))` — Puente de piedra con arcos a lo largo de x (por ejemplo, el Puente de Calderón); el río pasa por debajo (dibujarlo aparte).
- `def acueducto(mundo, x, y, n=8, paso=26, h=60, muro=(228, 206, 186))` — Acueducto de arcos (como el de Querétaro) a lo largo de x.
- `def mina(mundo, x, y, t_fn=None, s=1.0)` — Bocamina en una colina de roca con marco de madera, vía con vagoneta y malacate (cabrestante).
- `def malacate(mundo, x, y, t_fn=None, mula=True, s=1.0)` — Malacate: tambor de madera con aspas que gira movido por una mula en círculo.
- `def mesa(lz, iso, x, y, w=60, d=30, h=17, color=(150, 100, 70), mantel=None)`
- `def silla(lz, iso, x, y, h=11, color=(130, 86, 64), dir='y')`
- `def estante(lz, iso, x, y, w=50, d=10, h=60, color=(120, 80, 62), libros=True)`
- `def cuadro_pared(lz, iso, c, cara, a, b, w, h, color=(70, 120, 170), marco=(200, 150, 80))`
- `def vela(lz, iso, x, y, z, t=0.0, seed=0)`
- `def candelabro(lz, iso, x, y, z, t=0.0, n=3)`
- `def alfombra(lz, iso, x, y, w, d, color=(190, 70, 70), borde=(240, 200, 120))`

## nucleo/kz_iso_deco.py — Densidad automática para dioramas isométricos (estilo Kurzgesagt): que ningún suelo quede liso.

- `def parches(lz, iso, x0, y0, x1, y1, base, n=14, var=22, seed=0, alfa=0.5, tam=(40, 90))` — Manchas orgánicas más claras u oscuras que el suelo (variación de tono).
- `def campos(lz, iso, x0, y0, x1, y1, nx=3, ny=3, seed=0, t=0.0, colores=None, setos=True, margen=4.0)` — Mosaico de campos (cada celda con otro cultivo: maíz, trigo, hortaliza, barbecho, maguey) separados por setos.
- `def hierba(lz, iso, x0, y0, x1, y1, n=160, seed=0, t=0.0, color=(96, 170, 84), flores=0.12, alto=5.0)` — Briznas de pasto (triangulitos) y flores diminutas que se mecen con el viento. Se dibujan solo las visibles.
- `def esparcir(m, x0, y0, x1, y1, n, fn, seed=0, evitar=(), min_d=0.0, clave_extra=0.0)` — Registra n objetos en posiciones al azar dentro del rectángulo, evitando las cajas `evitar` [(x0,y0,x1,y1), ...] y manteniendo distancia mínima.
- `def bosque(m, x0, y0, x1, y1, n=30, seed=0, evitar=(), t_fn=None, tipos=('arbol',), h=(46, 70), colores=None, min_d=22)` — Arboleda: mezcla de árboles de varios tamaños y colores (+ arbustos al pie).
- `def aves(lz, t, n=7, seed=1, y0=140, y1=420, alfa=0.9, color=(70, 44, 90), vel=1.0, sentido=1)` — Bandada lejana de pájaros (V de dos alas) cruzando la pantalla en bucle.
- `def mariposas(lz, iso, x0, y0, x1, y1, n=5, t=0.0, seed=1)`
- `def polvo_luz(lz, t, n=26, seed=1, color=(255, 240, 200), alfa=0.5, area=(0, 0, 1920, 1080))` — Motas de polvo/pólenes que flotan a distintas profundidades (alfa que titila).
- `def acequia(lz, iso, pts_xy, t, ancho=10.0, c1=(70, 168, 226), c2=(40, 120, 200))` — Canal de agua con corriente (rayitas que avanzan) a lo largo de una polilínea del suelo.
- `def muro_bajo(m, pts_xy, h=10, color=(214, 196, 178))` — Muro bajo de piedra a lo largo de una polilínea (tramos rectos alineados a los ejes).

## nucleo/kz_iso_int.py — Utilería de INTERIORES para habitaciones en corte (kz_iso.habitacion): cortinas, ventanas con vista, escudos heráldicos, araña de cristal, chimenea con fuego, reloj de péndulo,

- `def cortina(lz, iso, c, cara, a0, a1, b0, b1, color=(190, 52, 66), t=0.0, galon=(250, 206, 90))` — Cortina recogida (pliegues alternos claro/oscuro), con cenefa dorada arriba y un cordón; ondula apenas con el aire.
- `def ventana_vista(lz, iso, c, cara, a0, a1, b0, b1, t=0.0, cielo=(140, 196, 248), marco=(250, 244, 230), cortinas=(190, 52, 66), vista='cielo')` — Ventanal con marco, travesaños, cielo con nubes y (opcional) siluetas lejanas; cortinas a los lados.
- `def escudo(lz, iso, c, cara, a, b, s=1.0, tipo='francia')` — Escudo heráldico sobre la pared: 'francia' (águila imperial dorada sobre azul), 'espana' (castillos y leones), 'mexico' (águila y nopal), 'iglesia' (llaves y cruz).
- `def mapa_pared(lz, iso, c, cara, a, b, w=60, h=44, t=0.0)` — Mapa antiguo enmarcado con costas y una ruta punteada que se mueve.
- `def espejo(lz, iso, c, cara, a, b, w=26, h=44)`
- `def araña(lz, iso, x, y, z, t=0.0, velas=6, s=1.0)` — Araña de cristal colgante: aro dorado, velas encendidas con halos y gotas de cristal que brillan.
- `def chimenea(lz, iso, c, cara, a, t=0.0, w=44, h=38, color=(206, 196, 182))` — Chimenea de mármol en la pared con fuego animado, repisa y un reloj encima.
- `def reloj_pie(lz, iso, x, y, t=0.0, s=1.0)` — Reloj de péndulo de caja alta con péndulo que oscila.
- `def maceta(lz, iso, x, y, s=1.0, t=0.0, tipo='helecho')`
- `def sillon(lz, iso, x, y, w=24, d=20, color=(190, 52, 66), orient='y')` — Sillón noble acolchado con respaldo, brazos y patas.
- `def paja(lz, iso, x0, y0, x1, y1, n=70, seed=3, color=(226, 196, 110))` — Paja esparcida en el suelo (celdas).
- `def cadenas(lz, iso, c, cara, a, b, n=5, t=0.0, color=(150, 150, 170))` — Cadena colgando de una argolla en la pared (calabozo).
- `def jarra_pan(lz, iso, x, y, s=1.0)`
- `def baul(lz, iso, x, y, w=22, d=14, h=12, color=(150, 98, 66))`
- `def cuadro_retrato(lz, iso, c, cara, a, b, w=22, h=28, marco=(250, 206, 90), fondo=(70, 90, 130), pelo=(240, 238, 244))` — Cuadro con un retrato esquemático de época (cabeza, peluca y casaca).

## nucleo/kz_iso_obj.py — Objetos del mundo isométrico (estilo Kurzgesagt): vegetación mexicana, roca, cercas, fuego, humo, carretas, barriles, banderas…

- `def arbol(lz, iso, x, y, h=46, color=None, seed=0, t=0.0, sombra=True, tronco=TRONCO)` — Árbol de copa redonda hecha de racimos de círculos en 3 tonos (luz arriba a la izquierda).
- `def arbusto(lz, iso, x, y, r=11, color=None, seed=0, flores=None)`
- `def cipres(lz, iso, x, y, h=52, seed=0)`
- `def palmera(lz, iso, x, y, h=64, seed=0, t=0.0)`
- `def pino(lz, iso, x, y, h=64, seed=0)`
- `def nopal(lz, iso, x, y, s=1.0, seed=0, tunas=True, t=0.0)` — Nopal: palas ovaladas apiladas con espinas y tunas rojas.
- `def maguey(lz, iso, x, y, s=1.0, seed=0, t=0.0)` — Maguey (agave): roseta de pencas azul-verdosas.
- `def organo(lz, iso, x, y, h=44, seed=0)`
- `def milpa(lz, iso, x, y, w, d, t=0.0, seed=0, color=(88, 168, 84))` — Campo de maíz: surcos de tierra con plantas altas que se mecen.
- `def hileras(lz, iso, x, y, w, d, color=(110, 184, 96), t=0.0, tierra=(176, 124, 88), planta='redonda')` — Cultivo en hileras (verduras): montículos de tierra con plantitas.
- `def roca(lz, iso, x, y, s=1.0, seed=0, color=(150, 126, 120))`
- `def barril(lz, iso, x, y, s=1.0, color=(170, 108, 70))`
- `def caja_madera(lz, iso, x, y, s=1.0, color=(190, 140, 90))`
- `def costal(lz, iso, x, y, s=1.0, color=(226, 206, 156))`
- `def cerca(lz, iso, pts_xy, h=14, color=(176, 124, 84), poste_cada=14)` — Cerca de postes y travesaños a lo largo de una polilínea del suelo.
- `def empalizada(lz, iso, pts_xy, h=34, color=(196, 92, 52), grosor=5.2)` — Muro de troncos con punta redondeada (como la empalizada del diorama de referencia, pero original: troncos de mezquite).
- `def muro_piedra(lz, iso, x, y, w, d, h, color=(206, 192, 176))`
- `def fuego(lz, iso, x, y, s=1.0, t=0.0, seed=0, z=0.0, halo=True)`
- `def humo(lz, iso, x, y, z, t, n=6, s=1.0, color=(236, 238, 248), vel=14.0, seed=0, alfa=0.7)` — Bocanadas de humo: círculos que suben, se agrandan y se desvanecen (ciclo continuo).
- `def chispas(lz, iso, x, y, z, t, n=8, seed=0, color=(255, 214, 110))`
- `def antorcha(lz, iso, x, y, t=0.0, h=22, seed=0)`
- `def farol(lz, iso, x, y, h=36, t=0.0, color=(255, 214, 120), encendido=1.0)`
- `def bandera(lz, iso, x, y, h=64, w=34, alto=22, color=(226, 70, 70), t=0.0, seed=0, escudo=None, franjas=None)` — Asta con tela que ondea (ola senoidal). franjas = [(color, fracción), ...] horizontal; escudo: callable(lz, cx, cy, k).
- `def carreta(lz, iso, x, y, t=0.0, mov=0.0, carga=(214, 180, 96), s=1.0, bultos=False)` — Carreta de bueyes: caja de madera, dos ruedas grandes, yugo. `mov` > 0 hace girar las ruedas.
- `def pozo(lz, iso, x, y, s=1.0)`
- `def fuente(lz, iso, x, y, t=0.0, s=1.0)` — Fuente de plaza: pila octogonal, columna y chorros.
- `def agua(lz, iso, pts_xy, t, c1=(58, 150, 220), c2=(40, 112, 200), espuma=(236, 248, 255), z=-1.0, seed=0)` — Masa de agua sobre el suelo: relleno plano, franjas claras que se desplazan y borde de espuma.
- `class Caravana` — n burros con arriero que recorren un trayecto en fila (todo función de t).
    - `.dibujar(self, mundo, t)`
- `def bahia(lz, iso, pts_xy, t, seed=0, c_orilla=(112, 214, 222), c_medio=(58, 156, 220), c_hondo=(36, 104, 196), z=-1.0, espuma=(240, 250, 255), olas=True)` — Bahía/lago orgánico: tres anillos concéntricos (orilla turquesa -> azul -> profundo), crestas de ola que avanzan hacia la orilla y espuma que respira en el borde.

## nucleo/kz_iso_obj2.py — Más utilería para dioramas isométricos de historia de México: lingotes y monedas, pergaminos, carteles, cofres, lluvia, brotes, banderas históricas, estandarte guadalupano,

- `def lingote(lz, iso, x, y, z=0.0, s=1.0, rot=0, brillo=0.0)` — Barra de plata (prisma gris azulado con filo claro).
- `def pila_lingotes(lz, iso, x, y, n=6, s=1.0, z=0.0, t=0.0)`
- `def moneda(lz, iso, x, y, z=0.0, r=4.0, t=0.0, giro=True, color=(250, 200, 60))` — Moneda de oro/plata en pie que gira (ancho oscila con cos) con destello.
- `def cofre(lz, iso, x, y, s=1.0, abierto=0.0, brillo=1.0, oro=True)`
- `def pergamino(lz, iso, x, y, z=0.0, w=12.0, h=16.0, rot=0.0, lineas=True, sello=(206, 60, 60), abre=1.0, billboard=True)` — Pergamino enrollado en los extremos (cartel en pantalla).
- `def cartel(lz, iso, x, y, texto, h=26, w=30, color=(250, 240, 220), tinta=(150, 40, 40), px=9, poste=(130, 90, 66), t=0.0)` — Cartel de madera con texto sobre un poste (SE VENDE, REMATE…).
- `def lluvia(lz, t, dens=1.0, alfa=0.5, ang=0.28, largo=42, seed=1)` — Lluvia en pantalla (capa superior).
- `def nube_tormenta(lz, x, y, s=1.0, t=0.0, relampago=0.0)`
- `def brote(lz, iso, x, y, u=1.0, t=0.0, enojo=True, s=1.0, color=(110, 200, 100))` — Planta que crece (u 0..1) con una carita enojada en la flor: «el descontento sembrado».
- `def tambor(lz, iso, x, y, s=1.0, golpe=0.0)`
- `def estandarte_virgen(lz, iso, x, y, h=64, t=0.0, w=34, alto=46)` — Estandarte de la Virgen de Guadalupe (fondo azul-verde, mandorla dorada, silueta de la Virgen con manto), que ondea. Diseño estilizado propio.
- `def bandera_trigarante(lz, iso, x, y, h=64, t=0.0, w=40, alto=24)` — Bandera del Ejército Trigarante: tres franjas diagonales blanco, verde y rojo con estrellas (diseño de época).
- `def trinchera(lz, iso, x, y, w, d, h=7.0, tierra=(150, 112, 84))` — Trinchera con parapeto de tierra y sacos.
- `def barricada(lz, iso, x, y, w=40, s=1.0)`
- `def escalera(lz, iso, x, y, z0, z1, ancho=6.0)` — Escalera de mano apoyada en un muro (de (x,y,z0) a (x,y+off,z1)).
- `def carruaje(lz, iso, x, y, t=0.0, mov=0.0, color=(206, 60, 70), s=1.0, caballos=2, dir=1)` — Carruaje de gala (cabina con ventanillas, techo con farol, 4 ruedas) tirado por caballos.
- `def faro_bandera(lz, iso, x, y, color=(206, 56, 70), t=0.0, h=60)` — Mástil con la bandera de la Corona (rojo y oro con castillo/león estilizado).
- `def corona(lz, iso, x, y, z=0.0, s=1.0, rot=0.0, brillo=1.0)` — Corona real de oro con joyas (cartel en pantalla, con giro opcional y halo).
- `def barrotes(lz, iso, x, y, w, h, n=7, z=0.0, color=(70, 66, 84))` — Reja de barrotes verticales a lo largo de x (prisión).
- `def grillete(lz, iso, x, y, z, t=0.0)`

## nucleo/kz_mapa.py — Mapa con relieve REAL para el estilo Kurzgesagt (México y alrededores), reutilizable por cualquier video de historia de México.

- `def XY(lon, lat)`
- `class Ventana` — Una ventana rectangular de relieve ETOPO1 (1' de arco) con su pirámide de niveles, humedad y ríos calculados.
    - `.afin_h(self, cam, nivel)` — Matriz 2x3: destino a media resolución (x, y) -> índices (j, i) del nivel de la pirámide (WARP_INVERSE_MAP).
    - `.toca(self, cam)` — ¿La ventana aparece en pantalla para esta cámara?
- `class Mapa` — Singleton perezoso. `base(cam, t)` -> fondo del mapa; `proy(cam, lon, lat)` -> pantalla.
    - `.es_tierra(self, lon, lat)` — True donde hay tierra (según los polígonos de países), vectorizado.
    - `.picos(self)` — Máximos locales (> 2000 m) de todas las ventanas: array [lon, lat, altitud] ordenado de mayor a menor.
    - `.proy(cam, lon, lat)`
    - `.inv(cam, sx, sy)`
    - `.base(self, cam, t=0.0, exag=7.0, mostrar_rios=True, rios_umbral=1.5, sombra=1.0, rio_color=None)` — Fondo del mapa para la cámara cam = (lon, lat, z). float32 H x W x 3 en [0, 1].

## nucleo/kz_mapa_datos.py — Prepara los datos geográficos del mapa con relieve (kz_mapa.py). Se corre UNA vez: `python kz_mapa_datos.py`.

- `def priority_flood(dem, mar)` — Barnes 2014 (Priority-Flood + epsilon). mar: celdas que son salida (mar). Devuelve (relieve llenado, padre, orden de extracción).
- `def acumular(padre, orden)`
- `def rios(alt, lat0=LAT0, lon0=LON0, umbral=260)`
- `def simplificar(p, tol)`
- `def paises()` — Todos los países con alguna parte entre lon -135..50 y lat -58..75 (América, Europa y el norte de África). México y los vecinos cercanos conservan el detalle completo;
- `def lagos()`
- `def ventana(nombre)` — Lee un .nc de NOAA ETOPO1 (altitud en m), calcula los ríos y guarda nucleo/datos/relieve_<nombre>.npz.
- `def main()`

## nucleo/kz_mapa_dib.py — Elementos que se dibujan ENCIMA del mapa con relieve (kz_mapa.py): ciudades como mini-dioramas isométricos, banderas, ondas, rutas con flujo, ejércitos en marcha,

- `def ciudad(lz, cam, lugar, t, t0=0.0, tam=1.0, tipo='pueblo', bando=None, llama=False, nombre=None, px=30, alfa=1.0, color_nombre=U.COL['morado'], semilla=1)` — Mini-diorama isométrico sobre el mapa: baldosa de tierra con iglesia/casas (pueblo), muchas casas (ciudad), muros (fuerte) o casas+muelle (puerto). Aparece con el «pop» del original.
- `def bandera_mapa(lz, x, y, color, t, s=1.0, franjas=None)`
- `def etiqueta(lz, cam, lugar, texto, t, t0=0.0, px=28, color=U.COL['morado'], dy=-34, dx=0.0, lado='abajo', alfa=1.0)`
- `def onda(lz, cam, lugar, t, t0, dur=2.2, r_deg=4.0, color=(255, 236, 170), n=3, ancho=6.0, periodo=0.35, alfa=0.85)` — Anillos que se expanden desde la ciudad a lo ancho del mapa (la campana que se oye en todo el país).
- `def ruta(lz, cam, pts, color=(255, 214, 84), frac=1.0, t=0.0, ancho=7.0, flecha=True, curv=0.0, retorna=False, punta=True)` — Línea discontinua con flujo desde el primer punto hasta `frac` del recorrido, con punta de flecha. pts = [(lon, lat) | nombre, ...]. Devuelve el punto de pantalla de la cabeza.
- `def punto_ruta(cam, pts, u)` — Punto de pantalla a la fracción u de la ruta (misma interpolación que `ruta`).
- `def ejercito(lz, x, y, n, bando='ins', t=0.0, s=1.0, dir=1, marcha=True, bandera=True, semilla=0, polvo=True, estandarte=None)` — Grupo de n soldaditos planos en marcha (con desfase propio), bandera y nube de polvo, de ~26 px de alto a s=1.
- `def montes(lz, cam, min_alt=None, alfa=1.0, t=0.0)` — Montañas y volcanes dibujados como iconos con 3 tonos sobre las cumbres reales del relieve (picos de ETOPO), con nieve en los volcanes.
- `def region(lz, cam, texto, lonlat, px=30, rot=0.0, alfa=0.75, color=(255, 255, 255), espacio=0.18, z_min=0.0, z_max=99.0)` — Nombre de región/mar con letras espaciadas, semitransparente (SIERRA MADRE OCCIDENTAL, GOLFO DE MÉXICO…).
- `def brujula(lz, x, y, s=1.0, alfa=0.9)`
- `def escala(lz, x, y, cam, km=200, alfa=0.9)` — Barra de escala (km) según el zoom: 1° de latitud = 111 km = K*z px.
- `def cuadricula_geo(lz, cam, paso=5, alfa=0.14)` — Meridianos y paralelos tenues con su etiqueta en el borde.
- `def insignia_batalla(lz, cam, lugar, t, t0, año=None, s=1.0, color=(226, 70, 70))` — Espadas cruzadas en un disco rojo (batalla) con el año en una cápsula.
- `def pais(lz, cam, nombre, color, alfa=0.35, borde=None, ancho=4.0, t=0.0, latido=0.0)` — Rellena (y perfila) los polígonos de un país de Natural Earth sobre el mapa.
- `def barco_plano(lz, x, y, s=1.0, t=0.0, dir=1, vela=(250, 244, 230), casco=(120, 80, 60), alfa=1.0)` — Galeón de vela en pantalla (para el mapa): casco, dos mástiles, velas hinchadas, cabeceo.
- `def corona(lz, x, y, s=1.0, alfa=1.0, t=0.0)`
- `def mar_vivo(lz, cam, t, seed=1, densidad=1.0, fauna=True, barcos=True, color=(255, 255, 255))` — Vida sobre el MAR del mapa (solo donde no hay tierra): crestas de ola que respiran, delfines y ballenas que saltan con salpicadura y barcos lejanos que navegan.
- `def medallon(lz, x, y, r, quien, t, emocion='neutro', borde=(250, 206, 90), fondo=(60, 40, 110), alfa=1.0, seed=0, habla=0.0, k=1.0)` — Retrato en círculo con borde dorado (para mapas): se recorta el retrato al disco.
- `def montes_lista(lz, cam, picos, alfa=1.0)` — Montañas en posiciones dadas [(lon, lat, altitud_m), ...] (para zonas sin datos de relieve: Pirineos, Alpes…).
- `def pueblo(lz, cam, lugar, nombre, t, t0=0.0, color=(255, 255, 255), px=24, solo_desde=1.2)` — Punto de población con anillo y nombre pequeño (para dar densidad geográfica sin tapar el mapa). Solo se dibuja con el zoom alto.

## nucleo/kz_pers2d.py — Personajes 2D expresivos del estilo Kurzgesagt (referencia: «This Woman Cured Her Cancer…», primeros planos y multitudes).

- `def variar(tipo, seed)` — Variante de un tipo para multitudes: piel, pelo y ropa distintos con la misma silueta.
- `def busto(lz, x, y, s, spec='mujer', t=0.0, yaw=-0.5, bajar=0.0, roll=0.0, emocion='neutro', ojos=None, mirar=(0.0, 0.0), habla=0.0, mano=None, seed=0, alfa=1.0, flip=1, luz_borde=None, temblor=0.0, brazo=True, torso_inc=0.0)`
- `def v_marcha(s, vel=1.0)` — Velocidad del suelo (px/s) para que los pies no resbalen con `piernas='camina'` a escala s.
- `def cuerpo(lz, x, y, s, spec='hombre', t=0.0, piernas='idle', brazos='balanceo', mirar=1, vista='perfil', ph=None, vel=1.0, cara='auto', obj_d=None, obj_i=None, seed=0, alfa=1.0, sombra=True, lean=0.0, emocion='neutro', objetivo=None, escala_h=1.0)` — Personaje de cuerpo entero. piernas: idle | camina | corre | baila | arrodillado | sentado.

## nucleo/kz_retrato.py — Retratos (bustos grandes y expresivos) del estilo Kurzgesagt: ojos con destello de estrella de 4 puntas, cejas gruesas, rubor, pelo en 2-3 tonos con filo de luz,

- `def retrato(lz, x, y, s, quien, t=0.0, emocion='neutro', habla=0.0, mirar=0.0, alfa=1.0, flip=1, luz_borde=(255, 220, 90), seed=0, mano=None)`

## nucleo/kz_retrato_real.py — Retratos REALES (pinturas, grabados y fotos de dominio público, de Wikimedia Commons) integrados en el estilo Kurzgesagt.

- `def hay(quien)`
- `def retrato(lz, x, y, s, quien, t=0.0, emocion='neutro', habla=0.0, mirar=0.0, alfa=1.0, flip=1, luz_borde=(255, 220, 90), seed=0, mano=None, borde=(250, 206, 90))` — Retrato enmarcado. (x, y, s) con la misma convención que kz_retrato.retrato: s ≈ alto de la cabeza / 2,4; (x, y) = base del cuello. Flota suavemente; si habla, late un poco.
- `def medallon(lz, x, y, r, quien, t, emocion='neutro', borde=(250, 206, 90), fondo=(60, 40, 110), alfa=1.0, seed=0, habla=0.0, k=1.0)` — Retrato real en medallón redondo con anillo dorado (para mapas y escenas). r = radio exterior del anillo en px cuando k = 1.

## nucleo/kz_ui.py — Interfaz y efectos de pantalla del estilo Kurzgesagt: etiquetas en cápsula con muesca (llamadas), globos de diálogo, insignias numeradas, contadores, ondas sonoras,

- `def pop(t, t0, lento=1.0)` — Escala de aparición con la curva medida del original. 0 antes de t0; `lento` estira el tiempo (1.5 = más pausado).
- `def repop(t, t0, amp=0.12, dur=0.32)` — Latido de énfasis: la etiqueta vuelve a «saltar» un poco (1 -> 1+amp -> 1) a partir de t0.
- `def salida(t, t1, dur=0.18)` — 1 hasta t1; baja a 0 en dur (se encoge).
- `def vaciar_diferidos(lz)` — Dibuja las etiquetas sin cola que se dejaron para el final del cuadro, separándolas de la fecha de la esquina y entre sí.
- `def llamada(lz, x, y, texto, color=COL['morado'], px=34, k=1.0, cola='abajo', alfa=1.0, color_texto=(255, 255, 255), capa=2, ancla='centro', sombra=True, clamp=True, _dif=False)` — Etiqueta rectangular de esquinas suaves con una muesca triangular (cola) que apunta al objeto. (x, y) = punta de la cola (o centro si cola=None).
- `def globo(lz, x, y, texto, px=36, k=1.0, color=(255, 255, 255), color_texto=COL['morado'], alfa=1.0, cola='abajo', lado=1)` — Globo de diálogo redondeado (cápsula) con colita curva. (x, y) = punta de la cola.
- `def insignia(lz, x, y, n, color=COL['azul'], r=22, k=1.0, alfa=1.0)`
- `def fecha_lugar(lz, t, t0, t1, lugar, fecha, x=70, y=70, col_lugar=COL['morado'], col_fecha=(255, 255, 255))` — Rótulo de esquina: lugar en cápsula de color y fecha grande debajo (entra con pop, sale encogiéndose).
- `def titulo_grande(lz, t, t0, t1, texto, x=W / 2, y=130, px=96, color=(255, 255, 255), ancla=(0.5, 0.5))`
- `def chispa4(lz, x, y, r, color=(255, 244, 200), alfa=1.0, rot=0.0, capa=2)` — Destello de 4 puntas (estrella «+» afilada).
- `def chispas(lz, t, n=18, area=(0, 0, W, H), seed=1, color=(255, 244, 200), tam=(6, 14), vel=0.7)` — Chispas «+» que titilan (alfa senoidal con frecuencia propia, como las estrellas del original).
- `def bokeh(lz, t, seed=2, n=14, colores=((255, 240, 120), (255, 90, 160), (110, 90, 255), (255, 150, 90)), r=(30, 110), alfa=0.55, area=(0, 0, W, H))` — Discos desenfocados de colores a la deriva (fondo de los primeros planos).
- `def haces_luz(lz, x, y, t, n=7, largo=1500, color=(255, 220, 255), alfa=0.22, ancho=0.1, rot0=0.0, vel=0.12)` — Haces de luz que giran lentamente desde (x, y).
- `def ondas_sonoras(lz, x, y, t, t0, dur=1.6, r1=700, n=4, color=(255, 236, 170), ancho=7.0, periodo=0.32, alfa=0.8, capa=2)` — Anillos que se expanden desde (x, y) a partir de t0 (campanada, explosión, grito).
- `def onda_iso(lz, iso, x, y, t, t0, dur=1.8, r1=160, n=3, color=(255, 236, 170), periodo=0.3, ancho=3.0, z=0.0)` — Anillos en el SUELO isométrico (elipses) desde (x, y) del mundo.
- `def contador(lz, x, y, valor, px=110, color=(255, 255, 255), k=1.0, alfa=1.0, sufijo='', fuente='geo')`
- `def viñeta_color(img, color=(20, 8, 60), fuerza=0.35)`
- `def gradacion(img, luces=(1.02, 1.0, 0.96), sombras=(0.97, 0.98, 1.04), contraste=1.04, saturacion=1.06)` — Correccion de color simple: luces cálidas y sombras frías, algo de contraste y saturación.
- `def pergamino_grande(lz, x, y, w, h, t, t0, lineas=(), titulo=None, sello=True, rot=0.0, alfa=1.0, color=(252, 240, 208), tinta=(110, 70, 50))` — Pergamino enrollado en pantalla que se despliega con «pop»: titulo en negrita, líneas de texto simuladas, sello de lacre rojo con cinta. (x, y) = centro.

## nucleo/plano.py — Kit de vector plano (estilo Kurzgesagt) sobre el Lienzo: esferas con sombra de terminador y borde de luz,

- `def mezcla(c1, c2, u)`
- `def aclarar(c, u)`
- `def oscurecer(c, u)`
- `def terminador(x, y, r, ang, e, n=48)` — Polígono de la zona en sombra de un disco iluminado desde la dirección `ang` (rad, hacia la luz;
- `def borde_luz(x, y, r, ang, grosor=0.08, n=40)` — Media luna fina del lado iluminado (ancho en el ecuador = 2*grosor*r).
- `def esfera(lz, x, y, r, color, ang_luz=math.pi * 1.25, sombra=-0.15, fuerza=0.5, color_sombra=SOMBRA, rim=0.07, color_rim=None, contenido=None, alfa=1.0)` — Disco con 2 tonos de sombra y borde de luz. contenido(): se dibuja recortado dentro del disco.
- `def sol(lz, x, y, r, t, brillo=1.0, apagado=0.0)` — Sol con halo, corona ondulante y núcleo claro. apagado 0..1 lo convierte en un disco oscuro sin brillo.
- `def tierra(lz, x, y, r, t, rot=0.0, ang_luz=math.pi, luz=1.0, hielo=0.0, nubes=1.0, ciudades=0.0, tilt=-0.35, atmosfera=1.0)` — Planeta Tierra. rot: giro (rad); luz 0..1 (0 = sin Sol: todo en noche); hielo 0..1 congela océanos.
- `def luna(lz, x, y, r, ang_luz=math.pi, luz=1.0)`
- `def pajaro(lz, x, y, s=1.0, t=0.0, color=(126, 88, 214), mirar=(0.0, 0.0), aleteo=0.0, tiritar=0.0, feliz=0.0, escarcha=0.0, voltear=False, boca=0.0)` — Pajarito redondo tipo Kurzgesagt (origen en las patas). mirar (-1..1), aleteo 0..1, tiritar 0..1.
- `def kuri(lz, x, y, s=1.0, t=0.0, color=(64, 196, 190), mirar=(0.0, 0.0), aleteo=0.0, tiritar=0.0, feliz=0.0, escarcha=0.0, voltear=False, boca=0.0)` — Kuri, mascota de Kuriox: robot explorador redondo con pantalla de cara y antena (origen en los pies).
- `def microbio(lz, x, y, s, t, color=(120, 230, 150), seed=0, forma=0, mirar=(0.0, 0.0), brillo=0.4)` — Microbio blandito con ojos y cilios. forma 0 = píldora, 1 = redondo, 2 = alargado.
- `def arbol(lz, x, y, s=1.0, t=0.0, hojas=(80, 176, 100), perdida=0.0, seed=0, escarcha=0.0, oscuro=0.0)` — Árbol de copa redonda (origen en la base). perdida 0..1: las hojas se secan y caen. oscuro: noche.
- `def hojas_cayendo(lz, x, y, t, t0, n=10, col=(170, 140, 100), seed=3)` — Hojas que caen desde (x, y) a partir de t0.
- `def termometro(lz, x, y, s, nivel, col=(255, 90, 90), marcas=6)` — Termómetro vertical (origen = centro del bulbo). nivel 0..1.
- `def fumarola(lz, x, y, s, t, calor=1.0, agua=(14, 30, 72))` — Chimenea hidrotermal del fondo del mar (origen en la base) con penacho y brillo.
- `def onda(lz, x, y, r, ancho, color, alfa=1.0, capa=None, frente=0.45, estela=1.8)` — Frente de onda luminoso (anillo) de radio r: borde delantero nítido y estela suave hacia dentro.
- `def discontinua(lz, pts, color, ancho=4.0, largo=22.0, hueco=16.0, fase=0.0, frac=1.0, capa=None)` — Línea discontinua a lo largo de la polilínea pts (coords locales). frac: porción dibujada.
- `def arco_pts(x, y, r, a0, a1, n=240)`
- `def rotulo(lz, x, y, texto, px=46, k=1.0, color=BLANCO, fuente='geo', ancla=(0.5, 0.5), alfa=1.0, sombra=0.45, capa=2, rot=0.0)` — Texto blanco limpio con sombra suave (sin contorno).
- `def pastilla(lz, x, y, texto, px=40, k=1.0, fondo=(255, 255, 255), color=(34, 28, 80), fuente='geo', alfa=1.0, capa=2)` — Etiqueta en cápsula redondeada (fondo claro, texto oscuro).
- `def linea_llamada(lz, p0, p1, frac=1.0, col=(255, 255, 255), ancho=3.0, alfa=0.9)` — Línea fina de llamada (del objeto al rótulo) con punto en el origen.
- `def planeta(lz, x, y, r, tipo, t=0.0, luz=1.0, ang_luz=math.pi, seed=0)` — Planeta del sistema solar (no la Tierra: usa tierra()). luz 0..1 (0 = sin Sol).
- `def sol_corte(lz, x, y, r, t, apertura=1.0, nucleo=1.0, ang=-0.55, brillo=1.0)` — Sol con una cuña recortada que muestra núcleo, zona radiativa y zona convectiva.
- `def galaxia(lz, x, y, R, t=0.0, rot=0.0, inclin=0.5, alfa=1.0, fondo=(12, 12, 34))` — Galaxia espiral (Vía Láctea estilizada) de radio R; alfa mezcla hacia el color de fondo.
- `def estrella_neutrones(lz, x, y, r, col=(170, 210, 255), brillo=1.0)`
- `def humano(lz, x, y, s=1.0, t=0.0, ropa=(92, 142, 232), piel=(250, 202, 164), pelo=(64, 44, 44), paso=0.0, brazo=0.0, voltear=False)` — Persona simple estilo Kurzgesagt (origen en los pies, altura ~170*s).
- `def casa(lz, x, y, s=1.0, calor=0.0, oscuro=0.0)` — Casita (origen en la base). calor 0..1: ventana encendida con luz cálida.
- `def planta(lz, x, y, s=1.0, t=0.0, vida=1.0, col=(96, 196, 110))` — Plantita/flor (origen en la base). vida 0..1: 0 = seca y caída.
- `def conejo(lz, x, y, s=1.0, t=0.0, col=(196, 184, 178), voltear=False, salto=0.0)`
- `def zorro(lz, x, y, s=1.0, t=0.0, voltear=False)`
- `def gusano_tubo(lz, x, y, s=1.0, t=0.0, seed=0, alto=1.0)` — Gusano de tubo gigante (Riftia): tubo blanco y penacho rojo que se mece (origen en la base).
- `def panel_solar(lz, x, y, s=1.0, activo=1.0)`
- `def central_nuclear(lz, x, y, s=1.0, t=0.0, activa=1.0)` — Torre de refrigeración con vapor (origen en la base).
- `def interruptor(lz, x, y, s=1.0, encendido=1.0)`
- `def molecula(lz, x, y, s=1.0, tipo='O2', rot=0.0)` — O2 (dos esferas rojas) o CO2 (carbono gris entre dos oxígenos).

## videos/independencia_mx/util.py — Utilidades comunes de las escenas animadas: tiempos de la voz, claves de animación, cámara, texto, agua, lluvia.

- `def w_(eid, fr, i)` — Tiempo (s) en que empieza la palabra i de la frase fr de la escena eid.
- `def wf(eid, fr, i)` — Tiempo (s) en que TERMINA la palabra i.
- `def INI(eid, i=0)`
- `def FIN(eid, i=-1)`
- `def T0(eid)`
- `def T1(eid)`
- `def K(t, pts, ease=e_inout)` — Interpolación por claves [(t, v), ...] (v escalar o secuencia).
- `def Klog(t, pts, ease=e_inout)` — Como K pero para (x, y, z) con el zoom interpolado en escala logarítmica.
- `def cam(lz, cx, cy, z=1.0)` — Contexto de cámara: el punto (cx, cy) del mundo cae en el centro de la pantalla con zoom z.
- `def vent(t, a, b, fi=0.3, fo=0.3)` — 0..1: sube en [a, a+fi] y baja en [b-fo, b].
- `def etq(lz, t, t0, t1, txt, x, y, px=38, col=None)`
- `def gran(lz, t, t0, t1, txt, x, y, px=96, col=BLANCO)`
- `def cifra(lz, t, t0, txt, x, y, px=120, col=ORO, t1=None)`
- `def bg_grad(top, bot, mid=None, ym=0.55)` — Fondo vertical (H, W, 3) float32 en [0, 1].
- `def bg_plano(c)`
- `def agua(lz, x0, x1, y0, y1, t, c_top=(40, 96, 170), c_bot=(14, 30, 92), amp=6.0, capas=3, seed=0, luna=None, brillo=0.35)` — Masa de agua vista de lado: degradado, crestas onduladas, destellos y (opcional) camino de luna en x = luna.
- `def ondas(lz, x, y, t, t0, dur=1.6, r1=60, col=(255, 255, 255), n=3, alfa=0.7)` — Ondas concéntricas (elipses aplanadas) en la superficie del agua a partir de t0.
- `def chapoteo(lz, x, y, t, t0, s=1.0, col=(230, 246, 255))` — Salpicadura: gotas en parábola + anillo de ondas desde t0.
- `def post_lluvia(img, t, dens=1.0, ang=0.35, largo=46, alfa=0.42, seed=1)`
- `def post_viñeta(img, fuerza=0.35)`
- `def post_fundido_negro(img, t, t0, t1)`
- `def sprite_img(nombre, ancho=420, aspecto=None, foco=(0.5, 0.5), borde=9, radio=16)` — Imagen de imagenes/ como sprite RGBA premultiplicado (uint8) con borde blanco y esquinas redondeadas (ancho*2 px de ancho).
- `def tarjeta(lz, nombre, x, y, ancho=420, aspecto=None, rot=0.0, alfa=1.0, foco=(0.5, 0.5), capa=2, pie=None, px_pie=26)`
- `def T(eid, texto, **kw)` — Instante (s) en que se dice `texto` dentro de la escena `eid` (coincide por prefijo; frase= fija la frase; n= la enésima aparición).
- `def pk(t, t0, d=0.4)` — Escala de entrada con rebote (0 antes de t0).

## videos/independencia_mx/mundos.py — Mundos isométricos del video (cada lugar con su propio decorado): Dolores, Querétaro, Guanajuato, Ciudad de México, Guadalajara, Cuautla…

- `class Dolores` — Dolores (hoy Dolores Hidalgo): parroquia de cantera rosa de dos torres con campana, plaza con ahuehuete, casas de adobe con teja, calles, milpas y magueyes.
    - `.suelo(self, lz, iso, t=0.0, isla=True, bob=True)`
    - `.objetos(self, t, campana=None, gente=1.0)`
- `class RutaPlata` — Isla larga con la mina de plata (arriba a la izquierda), el camino real de las recuas y el puerto con galeones (abajo a la derecha).
    - `.suelo(self, lz, iso, t=0.0, isla=True)`
    - `.objetos(self, t)`

## videos/independencia_mx/mundos_b.py — Mundos isométricos de la escena 2 (Nueva España) con densidad automática: la ruta de la plata, la hacienda y el pueblo arruinado.

- `class RutaPlata` — Isla larga con la mina de plata (arriba a la izquierda), el camino real de las recuas y el puerto con galeones (abajo a la derecha). Densa: campos, bosques, aldea, río.
    - `.suelo(self, lz, iso, t=0.0, isla=True)`
    - `.objetos(self, t)`
- `class Hacienda` — Hacienda de la Nueva España: casa grande con portal, capilla, trojes, corral, huertos y el camino real.
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t)`
- `class PuebloRuina` — Pueblo de calle principal con casas en venta y tapiadas, un éxodo de familias con bultos y carretas cargadas, y el campo de tierra donde brotan las plantas del descontento.
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t)`

## videos/independencia_mx/mundos_c.py — Mundos de la pirámide social (escena 2): tres islas grandes y densas, cada una con su propia vida.

- `class AltoPoder` — Isla de los peninsulares: palacio con balcón, plaza de mármol rosa con fuente, jardines con cipreses, banderas de la Corona, carruaje de gala y nobles de peluca brindando.
    - `.suelo(self, lz, iso, t)`
- `class CiudadCriolla` — Isla de los criollos: calle de casas de dos pisos con balcones de colores, café con toldos, mercado, criollos de levita y sombrero de copa, bolsas de dinero sobre mesas.
    - `.suelo(self, lz, iso, t)`
- `class PuebloTrabajo` — Isla de indígenas, mestizos y esclavos: milpas y surcos, chozas, bocamina con vagonetas, malacate, fogatas, arriería, lavanderas en el río y capilla humilde.
    - `.suelo(self, lz, iso, t)`

## videos/independencia_mx/mundos_d.py — Mundos de la escena 3 (1808): salones en corte (Bayona, trono, ayuntamiento) y la Plaza Mayor de México de día y de noche.

- `def trono(lz, iso, x, y, t=0.0, s=1.0, corona=True, vacio=False)` — Trono dorado de respaldo alto con cojín rojo sobre una tarima de dos escalones (mirando hacia +y).
- `def dibujar_salon(lz, iso, t, firma=0.0, corona_cae=0.0, frances=True, W_=300, D_=260, H_=150, tipo='bayona')` — Salón en corte con ventanal, cortinas, escudos, cuadros, mapa, espejo, chimenea, reloj, plantas y araña de cristal. tipo: 'bayona' (francés: azul/dorado) o 'trono'.
- `def mesa_firma(lz, iso, x, y, t, firma=0.0)`
- `class PlazaMayor` — Plaza Mayor de la Ciudad de México (esquema): Palacio Virreinal al fondo, Catedral a la izquierda, portales con arcos a la derecha, fuente central, multitud, puestos, faroles. Día/noche por luz().
    - `.suelo(self, lz, iso, t, noche=0.0)`
    - `.objetos(self, t, noche=0.0, farolas=0.0)`

## videos/independencia_mx/mundos_e.py — Mundos de la escena 4 (la conspiración): sala criolla de la tertulia, calle de Querétaro con la casa del corregidor, casa de dos pisos en corte (Josefa Ortiz encerrada) y los talleres de Dolores.

- `def libro(lz, iso, x, y, z, abierto=1.0, color=(170, 60, 60), rot=0)` — Libro sobre una mesa: tapa de color y, si está abierto, dos páginas claras con renglones.
- `def sala_criolla(lz, iso, t, W_=300, D_=250, H_=140, noche=True)` — Sala de tertulias criolla (en corte): ventana nocturna con luna, retrato del rey Fernando (la tapadera), estantes con libros, chimenea, cortinas verdes y mesa grande con velas.
- `def mueble_sala(m, t, ocultar_plan=1.0, plan=0.0)` — Mesa grande con mantel verde, libros abiertos (la tapadera), candelabros, el plan oculto (pergamino que asoma) y sillas. Se añade a un Mundo isométrico.
- `class CalleQueretaro` — Calle empedrada de Querétaro con la casa de dos pisos del corregidor (balcón corrido y zaguán), casas vecinas de colores, el acueducto al fondo, faroles y gente.
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t, gente=1.0, farolas=0.0)`
- `def casa_dos_pisos(lz, iso_abajo, iso_arriba, t, H_=120, W_=260, D_=190, candado=1.0)` — Corte de una casa de dos pisos: abajo el zaguán/oficina del alcaide; arriba la recámara donde encierran a Josefa. iso_arriba es la misma cámara subida H_ unidades en pantalla.
- `def cama(lz, iso, x, y, t=0.0, color=(190, 60, 70))`
- `def puerta_cerrada(lz, iso, c, cara, a0, a1, h, candado=1.0, t=0.0)` — Puerta de madera con herrajes y candado (cierra con llave) en una pared de la habitación.
- `class TalleresDolores` — Campo de Dolores con los oficios que Hidalgo enseñaba: alfarería (horno de barro, torno y vasijas), apicultura (colmenas), viñedo, telar de seda y morera. Una choza-escuela al centro.
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t, humo=True)`
- `class PlazaPueblo` — Plaza de pueblo de tierra con iglesia pequeña, casas de adobe, árboles, una tarima de madera con un sillón vacío y mucha gente del pueblo mirándola.
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t)`

## videos/independencia_mx/mundos_f.py — Mundos de la escena 5 (el Grito): la casa del cura (interior), el camino de la marcha insurgente y las tierras del pueblo frente a la hacienda.

- `def casa_cural(lz, iso, t, W_=290, D_=240, H_=140, alba=0.0)` — Cuarto sencillo de la casa del cura de Dolores en la madrugada: cruz de madera, ventana con cielo que va aclarando, cama, mesa con velas y libros, estante y baúl.
- `def amueblar_casa_cural(m, t)`
- `def pos_camino(s)`
- `class CaminoMarcha` — Camino de tierra entre milpas, magueyales y encinos al amanecer, con lomas al fondo: por aquí marcha el ejército insurgente.
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t)`
- `class TierrasPueblo` — Hacienda con su cerca de piedra y la gran parcela que acaparó (barbecho); a la derecha las chozas del pueblo, la mesa del cobrador de tributos y costales de monedas.
    - `.suelo(self, lz, iso, t, verde=0.0, cerca_cae=0.0)`
    - `.objetos(self, t, fence=1.0, tributo=1.0)`

## videos/independencia_mx/mundos_g.py — Mundos de la escena 6 (Guanajuato): la ciudad minera entre cerros con la Alhóndiga de Granaditas, y los campamentos de los dos bandos.

- `def cerros(lz, cx, cy, t=0.0, tonos=((120, 150, 120), (98, 128, 108), (80, 106, 100)), alturas=(380, 300, 240), casas=True)` — Tres cerros redondeados con casitas de colores trepando por la ladera (como las laderas de Guanajuato), dibujados detrás del diorama con paralaje.
- `class GuanajuatoCiudad` — Guanajuato en 1810: plaza empedrada frente a la Alhóndiga de Granaditas (derecha-fondo), casas de colores, la parroquia, el arroyo con puentecitos, las minas con malacate y recuas de mulas con plata.
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t, gente=1.0)`
- `class Campamentos` — Valle abierto con dos campamentos frente a frente: a la izquierda los insurgentes (tiendas y el estandarte guadalupano), a la derecha los realistas (tiendas con la bandera de la Corona).
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t)`

## videos/independencia_mx/mundos_h.py — Mundos de la escena 7 (la capital a la vista): el monte de las Cruces con sus pinos y el camino, la vista del valle de México desde la cumbre (2D) y el campo de instrucción realista.

- `class MonteCruces` — Paso de montaña boscoso con un camino que sube en zigzag (de abajo-izquierda a arriba-derecha), pinos, rocas, un arroyo y un puesto de vigilancia.
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t)`
- `def vista_capital(lz, t, dx=0.0, horizonte=600.0)` — Valle de México visto desde el monte de las Cruces: volcanes con nieve, lago, ciudad-isla con catedral y calzadas, lomas verdes en primer plano. Todo en pantalla.
- `def multitud_espalda(lz, t, n=140, y0=760.0, y1=1090.0, seed=5, alzar=0.0, banderas=3, escala=1.0)` — Mar de gente vista de espaldas (cabeza, sombrero de palma, camisa blanca, faja roja) con machetes, lanzas y estandartes que se agitan; filas más cercanas = más grandes.
- `class CampoRealista` — Explanada de tierra con cuartel, banderas de la Corona, hileras de cañones y tiendas: aquí se reorganiza el ejército del rey.
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t)`

## videos/independencia_mx/mundos_i.py — Mundos de la escena 8 (Guadalajara y Calderón): la plaza de Guadalajara con catedral y palacio, la imprenta (interior con prensa) y el campo de batalla del puente de Calderón.

- `class Guadalajara` — Plaza de Armas de Guadalajara: catedral al norte, Palacio de Gobierno a un lado, portales con arcos al sur, fuente, jardines con fresnos, casas de cantera y calles.
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t, gente=1.0)`
- `def imprenta(lz, iso, t, W_=300, D_=240, H_=140)` — Taller de imprenta del siglo XIX en corte: ventana con la calle, estantes con cajas de tipos, cuerdas con pliegos colgados, barriles de tinta.
- `def amueblar_imprenta(m, t, k_prensa=0.0)`
- `def prensa(lz, iso, x, y, t, k)` — Prensa de tornillo de madera: bastidor, platina, barra que gira (k=1: en pleno trabajo) y pilas de papel.
- `class CampoCalderon` — Llanura con un río que cruza un puente de piedra (el de Calderón): al oeste el terreno donde se amontona la multitud insurgente, al este las lomas donde se forma el ejército realista; ríos, milpas y encinos.
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t)`

## videos/independencia_mx/mundos_j.py — Mundos de la escena 9 (la captura): el desierto del norte con rocas donde espera la emboscada y el patio de piedra donde ejecutan a los jefes (sin mostrar el momento).

- `def pos_camino_d(s)`
- `class Desierto` — Desierto del norte de Coahuila: dunas pálidas, nopales, órganos, magueyes, rocas grandes junto al camino, cerros lejanos y un camino de tierra.
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t)`
- `def patio_ejecucion(lz, iso, t)` — Patio de piedra con un muro alto al fondo y arcos; suelo de lajas (escena sobria).
- `def objetos_patio(t)`

## videos/independencia_mx/mundos_k.py — Mundos de la escena 10 (Morelos): la carpintería del padre de Morelos y Cuautla sitiada (casas de adobe con trincheras y un anillo de campamentos realistas, palmeras y mangos).

- `def carpinteria(lz, iso, t, W_=300, D_=240, H_=140)`
- `def amueblar_carpinteria(m, t)`
- `class Cuautla` — Cuautla de Morelos (tierra caliente): plaza con el convento de Santo Domingo, casas de adobe con trincheras en las bocacalles, palmeras y mangos; fuera, el anillo de campamentos realistas con cañones.
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t, ring=True)`

## videos/independencia_mx/mundos_l.py — Mundos de la escena 11 (el Congreso): el salón del Congreso de Chilpancingo (interior) y utilería 2D para infografías (cadena que se rompe, escalera de castas).

- `def salon_congreso(lz, iso, t, W_=320, D_=260, H_=140)`
- `def amueblar_congreso(m, t)`
- `def cadena(lz, x, y, n=6, t=0.0, rota=0.0, color=(150, 156, 176), ancho=60)` — Cadena horizontal de n eslabones centrada en (x, y); con rota>0 se parte por la mitad y las dos mitades se separan.
- `def escalera_castas(lz, x, y, t, aplana=0.0, k=1.0)` — Cinco barras apiladas de distinto ancho (la jerarquía de castas) que, con aplana 0->1, se igualan en un solo bloque con degradado.

## videos/independencia_mx/mundos_m.py — Mundos de la escena 13 (la guerrilla): la sierra del sur (cerros empinados, palmas, rocas, vereda de arrieros) y la selva de Veracruz (vegetación densa, helechos, un fuego pequeño).

- `def pos_vereda(s)`
- `class SierraSur` — Sierra del sur: vereda de arrieros que serpentea entre rocas grandes y palmas, barrancas oscuras, cerros de fondo.
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t)`
- `class Selva` — Selva de Veracruz: árboles altos y densos, palmas, helechos y arbustos con flores, claro con una hoguera y una choza de ramas, arroyo.
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t)`

## videos/independencia_mx/mundos_n.py — Mundos de la escena 15 (Iturbide): la plaza de Iguala con guirnaldas tricolor y el valle de Acatempan para el abrazo.

- `class PlazaIguala` — Plaza de Iguala (tierra caliente): iglesia pequeña de cal, portales, casas de colores vivos, palmeras y guirnaldas de banderines blanco-verde-rojo entre postes.
    - `.suelo(self, lz, iso, t)`
    - `.objetos(self, t, gente=1.0)`
- `def guirnaldas(lz, iso, t, k=1.0, postes=None, z=70)` — Cuerdas con banderines blanco-verde-rojo entre postes alrededor de la plaza (se dibujan sobre el diorama).
