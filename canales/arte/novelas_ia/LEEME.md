# Página de Facebook «Lágrimas y Venganza» (creada el 23-oct-2026)

Página de Facebook (no es canal de YouTube) para las **novelas con IA**: microdramas verticales 9:16 por capítulos, realistas,
con diálogo y labios sincronizados (formato en `docs/formato_novela_ia.md`). Primera novela: «La muerta en el altar»
(`videos/novela_altar/`). Nombre elegido por Claude: los temas que más multiplican en el formato son humillación → venganza
(suegra villana, amante, herencia, boda).

- Categoría: Programa de TV. Presentación: «Novelas cortas hechas con IA: traiciones, suegras villanas, herencias y venganzas.
  Un capítulo nuevo cada semana.» (dice «con IA» a propósito: Meta pide etiquetar el contenido realista hecho con IA; al subir
  cada capítulo, marcar «Información de IA» / «Hecho con IA»).
- Identidad visual (Flow, Nano Banana 2.1, 0 puntos; proyecto de la novela https://flow.google.com/project/31c0c36e-98b3-485c-a710-ae9e3b2d31a5):
  - `PERFIL_facebook_1024.jpg` = foto de perfil (de `flow/logo_2.jpg`): rosa roja con anillo de bodas y lágrima dorada en marco
    de filigrana sobre terciopelo vino; sin texto.
  - `PORTADA_facebook_1640x624.jpg` = portada (recorte y 0..60..584 de `flow/portada_1.jpg`): suegra contando el dinero del
    sobre, la novia con vestido roto y rosa, la amante de rojo con el anillo abrazando al marido, la niña con su dibujo y la
    ofrenda de muertos al fondo.
  - `flow/` = las 8 variantes; `_hoja_logos.jpg`, `_hoja_portadas.jpg` = hojas de comparación.
- **Dirección:** https://www.facebook.com/profile.php?id=61595668475468 (perfil web); **id de página para la API: 1424757057383312**.
  Asistente de 5 pasos terminado el 23-oct: sin contacto ni WhatsApp, sin invitar amigos, notificaciones de la página ON y
  correos de marketing de Meta OFF.
- **Cómo se subieron las imágenes:** el navegador integrado abre el cuadro «Abrir» de Windows y no se puede manejar (computer-use
  no puede controlar la ventana de Claude). Se hizo en **Chrome (Claude in Chrome)**: gancho a `HTMLInputElement.prototype.click`
  para que el `input[type=file]` no abra el cuadro → «Agregar foto de portada › Subir foto» / «Elegir foto del perfil › Subir foto»
  → `file_upload` sobre el input → Guardar. En Chrome, primero «Cambiar» a la página (si no, no deja editar).
- **Nombre de usuario (@):** pendiente (Facebook no lo deja en páginas recién creadas). Propuesto: `lagrimasyvenganza`.
- **Publicar por API:** `python E:\PaginaFace\pagina.py --pagina novelas_ia …` (carpeta `E:\PaginaFace\paginas\novelas_ia\`).
  **Token guardado el 23-oct-2026** (no caduca; `check` OK). Para renovarlo: Explorador de la API Graph marcando ESTA página
  (`pages_show_list`, `pages_manage_posts`, `pages_read_engagement`), ampliarlo en el depurador y `python pagina.py --pagina novelas_ia setup`.
  Capítulos 9:16 de 3-90 s = tipo `reel`; más largos = tipo `video` con `"titulo"`.
- **Publicaciones:** `publicaciones/NN_<novela>_capN.md` con título y texto. 01 = «La muerta en el altar» cap. 1: PUBLICADO por API el
  23-oct-2026 (tipo video porque dura 99 s > 90 s de reel), https://www.facebook.com/reel/4094617344177384/
  02 = «La heredera del rancho» cap. 1 (126 s, serie larga): PUBLICADO por API el 23-oct-2026,
  https://www.facebook.com/reel/4105030019626908/
