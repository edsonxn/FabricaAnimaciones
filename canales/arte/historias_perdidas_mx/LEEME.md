# Página de Facebook «Historias Perdidas de México» (creada el 22-oct-2026)

Página de Facebook (no es canal de YouTube) para subir videos de historia de México con los estilos de
**Bitácora Perdida** (Kurzgesagt isométrico) y **Cronopapel** (boceto + guache), y más adelante Shorts/reels verticales
con estilos nuevos contando historias de México. Nombre elegido por Claude (hereda la marca «Perdida» y abarca el guache).

- Categoría: Educación. Presentación: «La historia de México que no te contaron, en videos animados. Imperios,
  rebeliones, leyendas y pueblos olvidados, explicados en minutos. Nuevo video cada semana.»
- Identidad visual (Flow, Nano Banana 2.1, 0 puntos; proyecto de Flow del 22-oct 12:38): gouache sobre papel crema,
  pirámide escalonada + sol que forma una rosa de los vientos, grecas mexicas; paleta terracota, jade, ocre y añil.
  Sin águila ni bandera (el escudo nacional tiene uso restringido).
  - `PERFIL_facebook_1024.jpg` = foto de perfil (de `flow/logo_1.jpg`, sin texto: se lee en círculo pequeño).
  - `PORTADA_facebook_1640x624.jpg` = portada (recorte de `flow/portada_8.jpg`: pirámide → Tenochtitlan → iglesia
    colonial → revolucionarios → ciudad).
  - `logo_con_nombre_1024.jpg` = sello con el nombre escrito (marca de agua, cierre de video, miniaturas).
  - `flow/` = las 20 variantes; `_hoja_*.jpg` = hojas de comparación.
- Subir imágenes al navegador integrado: Facebook bloquea `fetch` a otros dominios y el panel no abre pestañas por código,
  así que el selector de archivos lo maneja el usuario.
- **Dirección:** https://www.facebook.com/profile.php?id=61595534920448 (ese número es el del perfil web; el **id de página para la API es 1388991384298203**). Asistente de 5 pasos
  terminado el 22-oct: sin datos de contacto ni WhatsApp (son del usuario), sin invitar amigos (sería enviar mensajes en
  su nombre), botón de acción por defecto («Seguir»), notificaciones de la página ON y correos de marketing de Meta OFF.
- **Nombre de usuario (@):** el elegido es `historiasperdidasmx`. El 22-oct Facebook respondió «En este momento no puedes
  elegir un nombre de usuario» (pasa con las páginas recién creadas). Se pone desde el perfil personal en
  https://accountscenter.facebook.com/profiles/61595534920448/username; volver a intentarlo en unos días.
- **Publicar por API (22-oct):** `E:\PaginaFace\pagina.py --pagina historias_mx …` (carpeta `E:\PaginaFace\paginas\historias_mx\`,
  receta en `E:\PaginaFace\CLAUDE.md` § «Varias páginas»). Falta el token: el usuario lo genera eligiendo esta página y corre
  `setup`. Videos horizontales = tipo `video` con `"titulo"`; Shorts 9:16 = tipo `reel`.
- **Publicaciones:** `publicaciones/NN_<video>.md` con título y texto. 01 = Jalisco: PUBLICADO por API el 22-oct-2026
  14:01 CDMX, https://www.facebook.com/reel/1643180983933186/ (el intento por navegador se atascó en «Publicando» y se
  canceló). Quedan dos videos ocultos de las pruebas: 1640641494259091 (error, 0 s) y 1084611801146352 (prueba de 20 s
  sin publicar). El usuario pidió borrarlos (22-oct); Claude no borra contenido de forma permanente: la prueba de 20 s se
  le dejó abierta en https://www.facebook.com/reel/1084611801146352/ para borrarla él (menú «…» → Eliminar). El de error
  no tiene página en Facebook (sale «no disponible»), no lo ve nadie y no hay botón para borrarlo desde la web.
