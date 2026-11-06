# Cola de escenas.py pendiente (diseñada el 5-nov, no aplicada: el comando falló por largo)
Sustituir en `escenas.py` desde `MOMENTOS = dict(` hasta el final por esto (escribirlo con Write/Edit, nunca por heredoc largo):

- `m_teaser(lz,u,ctx)` = `m_error_vuela(lz, u+0.6, dict(ctx, teaser=True))`; en `m_error_vuela`, con `ctx.get("teaser")`: sin kicker «ERROR REAL» y titular «¿¿NADIE LO TOCÓ??» en vez de «32 > 21».
- `m_presenta` (gancho_2): `pip(lz,"choque",2+u,u,0,cy=640,w=960,h=760)`, titular «SOY TOKEN» y=1170, kicker «LA IA DE ESTE TALLER», muñeco que saluda (`P[MD]=P[PEC]+[14+4sin(9u),-18]`).
- `m_pedido`: tarjeta tipo mensaje (rrect blanco 900x420 en y≈505 con colita) «MI JEFE ESCRIBIÓ:» + el texto real tecleado letra a letra desde `ctx["k"]("pedido_1")`;
  El Jefe = `jefe_canadiense.Jefe("propios/jefe_limpio.png", boca_y=.523/.75, bisagra_x=.33, frente_x=.57, corte=.75)`, `amplitud("voz/final/pedido_1.wav", fps=30)`,
  `j.cuadro(abre, u, alto=880)` (BGRA → RGBA premultiplicado) pegado con `lz.pegar(..., W/2-150, H+40-brinco, ancla=(.5,1))`; Token chico a la derecha. (Copiar propios/jefe_limpio.png de robotaller_n64: aún NO está copiado.)
- `m_problema`: hasta problema_1 → titular «SIEMPRE IGUAL» + 3 tarjetas con la MISMA caída («repetición 1/2/3») + «FALSA» torcido; problema_1 → kicker «GTA IV · 2008», titular «EUPHORIA», dos muñecos (leve, fuerte), pastilla «músculos simulados, no caídas dibujadas»; problema_2 → ventana de navegador (3 puntos, barra «robotaller», sin direcciones) con `D.monitor(clip("caida"), etiqueta="UNA PÁGINA WEB")`, titular «EN UNA WEB».
- `m_agarre` (equilibrio_3): titular «¡AGÁRRATE!», `pip("agarre")`, muñeco «fuerte» con reflejo, pastilla «manos al casco · barandal · lámpara · otro robot».
- `m_mundo`: monitor grande con clip mundo → trampa → enemigo (kickers «MESAS · TUBOS · LÁMPARAS», «TRAMPILLA AL PISO DE ABAJO», «ENEMIGO: PEGATINA CON ALAS»); en mundo_2: «180» gigante + «VECES POR SEGUNDO», «< 1 ms» + «por cuadro (medido: 0,2 ms)».
- `m_error_puente`: kicker «ERROR REAL · 5-NOV», tarjeta `declarada: tramo(x0, x1, y0, y1)` / `llamada: tramo(x0, y0, x1, y1)` (coral); dos pisos dibujados con hueco y una tabla en diagonal (coral) que se endereza (verde) en la palabra «orden»; `pip("puente")` abajo.
- `m_cierre`: cierre_0 → monitor `clip("choque")` con barrido + «CADA CAÍDA» / «ES LA PRIMERA»; cierre_1 → kicker «JUNTA DIRECTIVA», «TÚ» gigante, globo «¿Qué obstáculo les pongo?», Token saludando.
- `TONO_DE = dict(teaser="errores", presenta="pedido", agarre="equilibrio", error_vuela="errores", error_puente="errores")`.
- PLAN con `T(clave, palabra)` desde timeline.json (words: w/s/e): gancho 0 · teaser gancho_1 · presenta gancho_2 · pedido pedido_0 · problema problema_0 · verlet verlet_0 ·
  musculos musculos_0 · equilibrio equilibrio_0 · agarre equilibrio_3 · mundo mundo_0 · error_vuela errores_0 · error_puente errores_2 · cierre cierre_0 (cada uno −0,1 s).
- `pinta(lz, nombre, u, t)` arma `ctx = dict(t=t, k=lambda clave, palabra=None: T(clave, palabra) - t0)`; `Mundo.render` elige el momento y da un destello de 0,12 s en cada cambio.
- m_verlet: anclar fases a `ctx["k"]("verlet_1")` (fórmula, fantasma, flecha, «velocidad = ahora − antes») y a `ctx["k"]("verlet_2","trapo")-0.6` (se desarma), en vez de 2,2 s / 5,0 s fijos.
