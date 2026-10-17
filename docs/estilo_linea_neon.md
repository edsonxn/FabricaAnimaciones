# Estilo «LÍNEA BLANCA + NEÓN» (secuencia Flow con efectos; prueba sin canal)

_Creado el 16-oct-2026 con `videos/freno_enojo/` («Lo que pasa dentro de tu cuerpo cuando te callas el coraje»). Origen: reels
que le gustaron al usuario (Polymaths Unite / Deepstash: ratas mirando la luna desde un pozo, granjero con sombrero de neón
junto a un pozo, círculo de neón con gente peleando, rata cazando con una gallina de neón en el granero)._

Motor: SECUENCIA (`nuevo <v> --secuencia`) + capa de efectos (`docs/estilo_secuencia_fx.md`). Las imágenes y clips salen de
Google Flow; el brillo del neón, la cámara, las palabras clave y los SFX van por código.

## El look (lo que define el estilo)
1. **Fondo negro puro** y dibujo de **grabado en línea blanca fina** (como tiza o punta de plata): trazos delgados, sombreado
   con achurado suave, mucho detalle en el escenario (rocas, ladrillos, trigo, tablas) pero todo monocromo.
2. **UN solo elemento protagonista en neón amarillo** con halo dorado (el sombrero, la gallina, el anillo, el nervio, el
   corazón). A veces ojos rojos o amarillos que brillan. Nada más lleva color.
3. Personajes **monigote simpático**: cabeza redonda blanca, ojos de punto, cuerpo de línea; animales en grabado realista.
4. **Palabra gigante blanca al centro** (Poppins Black con sombra). En la referencia es karaoke palabra por palabra; en la
   Fábrica, por la regla «sin subtítulos quemados», **solo palabras clave** (decisión del usuario, 16-oct-2026): ~1 cada 10-15 s.
5. Cámara lenta y el neón **respirando** (FX `neon`): pulso lento + chisporroteo raro del tubo. Viñeta negra suave siempre.

## Prompt de estilo (FICHA["estilo"], en inglés, probado con Nano Banana 2 Lite y Omni 1.1 Flash)
Ver `videos/freno_enojo/guion.py` → `FICHA`. Claves: «white line-art illustration on a pure black background, like a fine
engraving drawn with thin white chalk-like lines», «ONE key element outlined in glowing bright yellow neon light», y en el
cierre «no color other than white lines and yellow neon». Nombrar en cada prompt QUÉ va en neón.

## Efectos por código (efectos.py)
- `dict(tipo="neon", de=0, a=99999, fuerza=.9)`: detecta lo saturado y brillante (sat > 90, val > 110 en HSV) y le suma un
  halo doble (radio 9 y 27 a 1/4 de resolución) que palpita. Parámetros: `fuerza`, `vel`, `radio`, `sat`, `val`.
- `vineta` negra 0,35 en todo el video; `latido` negro (no rojo) en la alarma; `tinte` azul en el frío.
- Rótulos: `dict(texto=..., en="palabras", dur=1.6, tam=140, color="blanco", y=.5)`.

## Voz
ElevenLabs `eleven_v4` con corchetes. Primera voz usada: **Alejandro Durán — Warm, Deep** (`sKgg4MPUDBy69X7iv3fA`, biblioteca
pública, latinoamericano grave con ronquera leve), tono de divulgación calmada.

## Hallazgos de freno_enojo (16-oct-2026)
- **El estilo sale a la primera** con Nano Banana 2 Lite y Omni 1.1 Flash: 50 de 50 imágenes y 6 de 7 clips en estilo, con el
  monigote reconocible. Defectos: 1 niño con pelo en vez del monigote (pedir «bald round white head, no hair») y rótulos
  «V1 V2 V3» en el nervio trigémino aunque el prompt dijera «no labels» (2 veces: se borraron con `cv2.inpaint` NS en cajas
  ajustadas a cada rótulo; con cajas grandes quedaban manchas del halo).
- **Política de Flow (video):** «a glowing yellow neon knot tightens around his throat» se rechazó, y también la versión
  con lágrima + «inside the transparent body… chemical storm». No se cobra. Evitar garganta/cuello apretado, asfixia y
  cuerpos «por dentro» con personas tristes en los CLIPS; en imágenes sí pasaron (nudo de neón en la garganta en scene-012).
  Si un clip falla 2 veces: 2 imágenes del mismo beat + mp4 propio de 10 s (zoom + fundido a la mitad), como `scene-002`.
- **Clips en el navegador integrado (sin extensión):** chip Vídeo · 360p · 10 s · x1 (7 puntos), `__ins(i)` + Return real,
  igual que las imágenes. Para bajarlos: el `<video>` de cada tarjeta solo aparece al pasar el ratón (`hover`), y su `src`
  (`flow-content.google/video/<uuid>?Expires…&Signature…`) se baja con curl sin cookies. Salen a **640x360**: la descarga
  «720p mejorada» es una descarga del navegador (no hay URL). Se reescalaron a 1080 con
  `scale=1920:1080:flags=lanczos,unsharp=5:5:0.8` (originales en `medios/_360p/`): en línea blanca sobre negro + halo de
  neón el reescalado casi no se nota.
- El uuid de la imagen-póster de un clip es el mismo que el del video: sirve para cruzar tarjetas y escenas.
- `browser_batch` admite 25 acciones: 3 por prompt (`__ins` con espera de 3 s dentro, `wait 2`, `Return`) = 8 prompts por lote.
  `__ins` devuelve `pre=` (largo del editor ANTES de borrar): `pre=1` en todos = ningún envío perdido.
- La cuadrícula «Todo» va en 2 columnas de 602 px (con viewport 1500x800): orden de envío = invertir (y, x).
