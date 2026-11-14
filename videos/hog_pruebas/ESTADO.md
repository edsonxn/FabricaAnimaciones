# hog_pruebas — 3 pruebas de estilo para La Hoguera Juchipila (encargo externo)

**Cliente:** el dueño de **La Hoguera Juchipila, Zac.** (restaurante, facebook.com/lahoguera.jz, 1,9 mil seguidores). No es canal nuestro: no se sube a YouTube ni a nuestras páginas; se entrega el MASTER al usuario para que se lo mande.
**Encargo (el usuario, 14-nov-2026):** reeditar uno de SUS reels de historia gastronómica, con SU voz y su toma, pero con buena edición, para una «explosión de vistas» (historia, no comercial). **Crear un ESTILO NUEVO de animación que combine con su formato** y presentar **3 pruebas distintas de ~20 s cada una**; el usuario elige una.

## Su formato (visto en sus ~90 reels)
- Él (chef, camisa negra con logo «La Hoguera», jeans) habla a cámara de pie en el salón: **pared ROJA intensa**, ramas secas con luces, sillas de madera, piso de barro. Toma vertical fija, a veces punch-in.
- Rótulo quemado: **UNA palabra blanca en mayúsculas** a ~77 % de la altura, centrada (hay que quitarla o taparla: `nucleo/texto_clips.py` detecta texto quemado). Pegatinas sueltas (pez, molécula) encima.
- Vistas típicas 700-2,5 mil; las más vistas: «manteles» 6,7 mil (892027586931201), Scream 4,1 mil, otras 3,3 mil/3 mil. Historias: Özer «De Juchipila hasta Londres» 2,5 mil, Armin Meiwes 1,2 mil, pulpo asesino (sannakji) 961, miel de la locura 1 mil, Vatel 703, **fugu 1,1 mil (la base elegida)**.

## Base elegida: reel del pez globo (fugu / Bandō Mitsugorō VIII)
- https://www.facebook.com/reel/2202914546923014 → `fuente/fugu.mp4` (1440x2560, 30 fps, 46,7 s, audio original). `fuente/voz.wav` 16 kHz. Hoja: `previews/fuente_hoja.jpg`.
- Transcripción con tiempos por palabra: `fuente/palabras.json` (`transcribir.py`, faster-whisper large-v3).
- **Tramo de las pruebas: 0,00-20,60 s** (las 3 pruebas usan el MISMO tramo para compararlas):
  0,0-3,9 «Comer pez fugu en Japón es como jugar a la ruleta rusa en la mesa.» · 4,0-6,6 «Este pez contiene tetrodotoxina.» · 6,7-9,4 «Es un veneno mil veces más potente que el cianuro,» · 9,5-11,4 «para el cual no existe antídoto.» · 11,6-14,8 «En los años 70, el legendario actor de teatro kabuki,» · 15,0-16,0 «Bandō Mitsugorō,» · 16,2-19,1 «exigió que le sirvieran cuatro hígados de este pez,» · 19,1-20,6 «la parte más venenosa.»
- Ojo con los datos: fue en enero de 1975 en Kioto (Bandō Mitsugorō VIII, Tesoro Nacional Viviente); verificar antes de rotular años o cifras.

## Las 3 direcciones de estilo propuestas (pendiente programarlas)
1. **BRASA** (fuego y carbón, el nombre del lugar): él recortado con borde de luz naranja; detrás, ilustraciones en carbón sobre negro que se encienden por los bordes como papel quemándose; chispas y humo continuos; palabra clave marcada a fuego (hierro candente) en vez de su rótulo blanco; transiciones con llamarada.
2. **ROJO CÓMIC** (la pared roja como firma): todo en blanco y negro con trama de semitono excepto el ROJO (su pared, el veneno, el pez); viñetas de cómic que se abren alrededor de él, onomatopeyas, globos de texto con la cifra («×1000 CIANURO»).
3. **RECETARIO DE ÉPOCA** (para historias): papel viejo/libro de cocina, él dentro de un recuadro tipo grabado, ilustraciones a tinta (ukiyo-e para Japón), sellos, mapa de Japón con Kioto marcado, fichas del platillo.
Comunes: profundidad (nada de paneles planos), SFX sincronizados, música por debajo de su voz (la del original se conserva o se separa con Demucs), cada cosa que nombra se ve (fugu real, molécula, kabuki, Bandō Mitsugorō con foto real con licencia/Commons o Flow como ilustración), vertical 1080x1920.

## Herramientas comprobadas (14-nov)
yt-dlp OK (Facebook sin cookies), faster-whisper + CUDA OK, rembg OK (`isnet-general-use`; para persona en video conviene matting por cuadro o un modelo de video), cv2 4.13. Copiar el patrón de `videos/duos_promo/` (videos reales del cliente + Demucs) y `docs/estilo_secuencia_fx.md`.

## En curso
- [x] Página encontrada y reels revisados · [x] reel base bajado y transcrito
- [ ] Recortar su figura (matting por cuadro) y quitar el rótulo quemado
- [ ] Programar los 3 estilos (`nucleo/hoguera_*.py` o en la carpeta del video) → render 20 s c/u en `salida/prueba_{brasa,comic,recetario}.mp4`
- [ ] Revisar cuadro a cuadro y mandarlas a la tele con `python fab.py tele video hog_pruebas … --pregunta "¿Qué estilo para La Hoguera?" --opciones "Brasa|Rojo cómic|Recetario"`

## Sesiones
- ◐ 14-nov-2026 (Opus 5.5): investigación + base + transcripción; el usuario cambió a Fable 5.2 antes de programar los estilos.
