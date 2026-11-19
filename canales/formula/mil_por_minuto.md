# Fórmula — Mil por Minuto (`mil_por_minuto`, cómo se fabrican las cosas)

## Alta del 19-nov-2026 (canal nuevo, 0 subs; creado por Claude bajo la cuenta de Google de Edsonxn)
- **Pedido del usuario:** «un canal tipo de cómo se fabrican las cosas… apuntar a un público más general, más grande, no limitarnos
  al público de un juego… las mismas fórmulas aplicadas a ese contenido… bien editado». Claude decide todo (nombre, logo, banner, estilo,
  voz); el usuario solo verifica el canal (SMS) y lo conecta a la API. Referencia que pasó: JPaniagua Docs «ASÍ se FABRICAN las SOPAS
  INSTANTÁNEAS | Dentro de la fábrica de MARUCHAN» (GOXp1qU_yik, 19:09, 2,3 M vistas, ×19,7).
- **Canal:** «Mil por Minuto», **@MilPorMinutoMX**, **UCszgmM9dLbLQBl0kfLIM-Ag**. @MilPorMinuto, @HechoEnSerie, @PlantaAdentro,
  @HechoAEscala y @DetrasDelAnaquel ya estaban ocupados. Nombre = la velocidad de una línea de producción («a mil por hora»).
- **Arte (por código):** `canales/arte/mil_por_minuto/arte.py` → `LOGO_800.jpg` (engrane naranja con «1000 POR MINUTO») y
  `BANNER_2560x1440.jpg` (plano de ingeniería, franjas de peligro, banda con productos idénticos en serie, contador «1 000 / MIN»).
  Logo SUBIDO en Studio el 19-nov (inyectado en el input de archivo; el navegador integrado no abre el selector de archivos ni llega a 127.0.0.1).
  **Banner PENDIENTE:** subirlo por la API (`banner` en el json + `yt` de branding de `nucleo/youtube.py`) cuando el usuario lo conecte.

## Por qué este nicho (NexLev, 19-nov-2026)
- **JPaniagua Docs** (60 mil subs, alta 20-jun-2026, México; canal secundario de un creador grande): outliers ROSS ×24,8 (2,9 M),
  Maruchan ×19,7 (2,3 M), Outlets ×7,5, TEMU ×7,1, Takis ×6,8, Monster ×5,5, Little Caesars ×4,7, Starlink ×4,6, Sabritas ×3,5,
  AutoZone ×2,6, MercadoLibre ×2,5, Costco ×1,8. Fórmula = **MARCA CONOCIDA + cómo se fabrica + el NEGOCIO (cifra en dólares)**, 15-19 min.
- En español hay ~25 canales «cómo se fabrica»: casi todos **metraje reciclado de fábricas + voz** (riesgo de «contenido reutilizado»),
  outlier < 1: Fábricas del Mundo (41 mil, $18 mil/mes), Fábrica Oculta (71 mil), Fábrica Secreta (15 mil, $6,2 mil/mes), Así se Fabrican (33 mil).
  RPM base 6-7 USD. En inglés igual (Beyond Global Factory ×10,9 con 22 videos). **Hueco:** nadie lo hace con animación propia
  (planos, cortes 3D, mapas, MG de cifras) + historia de la marca + negocio. Eso es lo nuestro.

## Lo que hace el video de referencia (transcripción completa leída + 32 cuadros)
1. Gancho 0:00-1:30: el producto en 3 frases («abres el vaso, agua, listo») → la cifra del negocio en pantalla gigante (USD 3.300.000.000)
   → «fabricarlo es lo contrario a instantáneo» → la lista de pasos que vienen → pregunta: «¿cómo se fabrican realmente?».
2. Origen de la empresa (fundador, año, giro raro: empezó con pescado congelado) y sus plantas en el mapa.
3. El PROCESO paso a paso (materia prima → control de calidad → mezcla → laminado → corte → ondas → vapor → fritura → enfriado →
   sazonado → empaque → lote/código → cajas), cada paso con su POR QUÉ («no se busca una masa bonita, se busca una masa predecible»).
4. Pedido de suscripción a ~4:40 («la mayoría no está suscrita»). Trivia a ~9:30 con 3 opciones, respuesta al final (comentarios).
5. Escala: cifras por día/año con la cuenta hecha en voz alta (3.600 millones/año ÷ 365). Personas vs máquinas.
6. Mitos y polémicas desmentidos con datos (¿es plástico?, nutrición) sin hacerla villana ni héroe.
7. Logística y distribución (mapa isométrico de almacenes y tiendas), mercado mundial y economía de escala.
8. Cierre circular: vuelve al vaso del inicio + respuesta de la trivia + suscripción.
- Imagen: video real de planta y anuncios de la marca + stock + imágenes IA (mapa isométrico de distribución) + cifras ENORMES en
  amarillo/verde con contorno, palabras clave en mayúsculas sobre el plano («REVISADAS»); cortes de 1-2 s; voz humana cálida, sin prisa.

## Nuestra receta (regla de oro de `videos/tes_secretos_40/` aplicada a fábricas)
- **Motor:** SECUENCIA YT (`docs/estilo_secuencia_yt.md`): clip real por beat (videos oficiales de planta y anuncios de la marca, tours de
  fábrica, noticias) con yt-dlp, recortes cortos y transformados; lo que la voz dice SE VE en ese momento; lista de PROMESAS VISUALES.
- **Firma propia (lo que nos separa de los canales de metraje reciclado):**
  1. **El CONTADOR de producción** en una esquina: cuántas piezas salieron de la planta desde que empezó el video (cifra real ÷ segundos).
  2. **PLANO de la línea** (dibujo técnico animado por código, estación por estación, el producto avanza por la banda) = kit nuevo
     `nucleo/mg_planta.py`, PENDIENTE del 1.er video (con fotos reales de las máquinas como referencia; nada de memoria).
  3. **Cifras gigantes** de dinero y volumen (MG), **mapa real con ruta** de plantas → frontera → tiendas (`mg_mapa`, tema `planta` a crear),
     pegatinas de productos y fundadores, recreación Flow marcada «RECREACIÓN» de lo que no tenga video (interior de una máquina).
- **Estructura fija (15-18 min):** gancho con la cifra → origen de la marca → proceso en 8-12 estaciones → suscripción (~4:30) → trivia
  (~9:00) → escala y números → mitos con datos → logística/mapa → el negocio → cierre circular + trivia + suscripción.
- **Títulos** (regla de títulos): «Así se FABRICAN las Maruchan por dentro», «Cómo se hacen los TAKIS y el negocio de 1.100 millones».
- **Voz:** **Brian C** de ElevenLabs (`Czw3Dn181ypdrCOnPfif`, «Clean, professional, warm», Latinoamérica), SIN filtro; finalista del
  casting de Radio Yermo (muestra `videos/_muestras_voz_fallout/04_brian.mp3`), ningún otro canal la usa. Corchetes de actuación, sin
  [whispers]/[excited]/[shouts]; tono de quien recorrió la planta, cálido y sin prisa.
- **Música:** no es canal de juegos → Lyria apegada al guion (`fab.py biblioteca sugerir <v>` primero). **SFX:** máquinas, bandas,
  vapor, prensas (`SFX_ELEVEN`); si la voz nombra un sonido, se oye.
- **Miniaturas:** Flow (Nano Banana escribe el texto): el producto gigante + la máquina + cifra o palabra en MAYÚSCULAS.
- **Comentarios:** canal sin videos → el 1.º va sin agradecimientos ni críticas; suscripción sin cifra.
- **Protegido en `nucleo/filtro_canal.py`** como Tamriel/Radio Yermo (prefijo de videos `mpm_`). Sin promo cruzada hasta que tenga ≥ 2 públicos.
- **Frecuencia y hora (provisional):** ciclo 4 días, 18:37 CDMX (público general, tarde-noche; ningún canal sube a esa hora). Ajustar con datos.

## Primeros temas (los 3 con referencia ×; elegir con `fab.py ideas mil_por_minuto` cuando haya datos)
1. **Takis** (mexicano, Barcel/Bimbo; ref. JPaniagua ×6,8) · 2. **Coca-Cola en México** (FEMSA) · 3. **Bimbo / Gansito** · reserva:
   Sabritas, Maruchan con NUESTRA receta (no copiar su guion), Lego, Crayola, chicles, tortillas industriales (Maseca).

## Alta HECHA (19-nov-2026, 2.ª sesión): pasos 1-4 de abajo listos (descripción, palabras clave, MX, no es para niños en Studio; json, panel, filtro, tema `planta`, C20, bitácora, commit). QUEDA SOLO: el usuario verifica (SMS) y conecta la API → Claude sube banner (`banner_subido` en el json) e idioma es-419.

### (histórico) PENDIENTE del alta (19-nov-2026, sesión cortada por contexto)
1. Studio → Personalización: comprobar que el logo quedó publicado; **descripción** del canal, palabras clave, país MX, no es para niños
   (Configuración → Canal). Ver `canales/radio_yermo.json` y BITACORA del 17-nov como modelo.
2. `canales/mil_por_minuto.json` (copiar estructura de `canales/radio_yermo.json`: canal_id, nombre, handle, estilo, horario, banner,
   publicados: []), color en `nucleo/panel_v2.html` (`mil_por_minuto:"#ff6a1a"`), `PROTEGIDOS`+`PREFIJOS("mpm_")` en `nucleo/filtro_canal.py`,
   tema `planta` en `mg_mapa.py`/`peg_estilos.py` (naranja (255,106,26), acero (15,18,22), amarillo (255,196,0)).
3. Fila **§C20** en `CLAUDE.md` (tabla de estilos) + sección `### C20` en `docs/reglas_globales_completas.md`; línea en `BITACORA.md`;
   memoria `canal-mil-por-minuto.md` + línea en MEMORY.md.
4. `git status` → commit en español de código/config/arte (sin tokens ni métricas) y `git push`.
5. Decir al usuario: verificar por SMS (youtube.com/verify, con el canal Mil por Minuto activo) y conectarlo a la API → luego subir banner e idioma es-419.
