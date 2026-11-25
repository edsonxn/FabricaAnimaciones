# mew_pterosaurios_pop — reel de Martin Eastwood megalosaurus en estilo RECETARIO (vertical, completo)

**Encargo (el usuario, 24-nov-2026):** editar https://www.facebook.com/share/v/1DwervMZKf/ («La importancia de los pterosaurios en la cultura pop», página Martin Eastwood megalosaurus, 90,6 s, 1920x1080, selfie en ESPEJO) en el estilo **Recetario** de `videos/hog_pruebas/recetario.py` (el de La Hoguera / fugu), adaptado. El usuario eligió (AskUserQuestion): **Recetario adaptado** y **reel completo vertical** 1080x1920, sin su intro de banda. Mismo creador que `videos/hog_nuevo/` (ahí fue Rojo cómic). No se sube a canales nuestros: se entrega el MP4 al usuario por Rayo.

## Fuente (`fuente/orig.mp4`, id FB 1911926879790107)
- Él a cámara 0-14,0 · **intro de banda 14,0-22,87 (se quita)** · él 22,87-47,0 · **inserto cladograma 47,0-51,5** · él 51,5-64,4 (pegatinas a los lados ~60-63,5) · **inserto dragón de Komodo 64,4-70,53** · él 70,53-90,57 (pegatina de pterosaurio a la izquierda ~86).
- Transcripción: `fuente/frases.txt` / `palabras.json` (faster-whisper large-v3). «pignofibras» = picnofibras.
- Hoja: `previews/fuente_hoja.jpg`, `previews/fuente_cortes.jpg`.

## Plan
1. `recortar.py`: cuadros volteados (hflip) + mate rembg (salta intro e insertos) → `medir.py` (seguimiento).
2. Línea de tiempo de salida: 0-13,5 = fuente 0-13,5 · 13,5-14,1 pase de hoja «Capítulo I» · después fuente 22,87→90,57 · cierre ~2 s. ≈ 83,8 s.
3. `recetario.py` adaptado: «Bestiario / Cuaderno de paleontología», láminas a tinta (grabado) de pterosaurios, dinosaurios, lagartos; cladograma a tinta; postura erguida vs. reptante; picnofibras; durante sus insertos su imagen va pegada como foto sobre la página.
4. Imágenes libres (Commons) con `img/creditos.json`; reusar las de `hog_nuevo/img`.
5. Voz Demucs + música biblioteca + SFX por código → hoja de cuadros finales → render → ffprobe → hoja del MP4 → Rayo.

## En curso
- ◐ 24-nov ~20:40: cuadros (2717) ✓ · mate con **DeepLabV3 en GPU** (`mate_gpu.py`; rembg en CPU iba a ~15 s/cuadro con la PC ocupada por otra sesión) ✓ 2118 cuadros · `medir.py` (tapa sus pegatinas `TAPAS` y el póster de la pared) · `recetario.py` programado (6 páginas, pases de hoja en `T_TURN`) con 2 rondas de hoja · `mezcla.py` ✓ (−14,0 LUFS; música biblioteca `arana_techo__lyria_tramo1` desde 50 s, cliente externo) · imágenes en `img/creditos.json` (Riou 1863 y Buckland PD; fósil Pterodactylus y Jeholopterus CC BY-SA; Crystal Palace y Sordes CC BY 2.0; Pteranodon TotalDino CC BY 4.0) + sus propias imágenes del reel (Retro vs Modern, dinos, Komodo, cladograma).

## ✅ Entregado 24-nov-2026 20:09
**`salida/recetario.mp4` (copia `salida/Pterosaurios_recetario.mp4`) mandado al usuario por Rayo (WiFi).** 1080x1920, 2531 cuadros (ffprobe = N), 84,4 s, −14,0 LUFS, pico −3,1 dBTP. Hoja del MP4: `previews/recetario_mp4_hoja.jpg`.
- Páginas: 0 gancho (Pteranodon en grabado que vuela, Riou 1863, «160 MILLONES DE AÑOS», mancha con «?», ¡COMENZAMOS!) · I recorte de periódico de Cd. Juárez, «pterodáctilo» tachado → «pterosaurio» + su lámina Retro vs Modern · II Crystal Palace 1854 «NO SON DINOSAURIOS», regla del Mesozoico, círculo DINOSAURIA con el pterosaurio FUERA · III cladograma a tinta (Pterosauria marcado) con su cladograma pegado abajo, fósil con lupa, huellas «locomoción» · IV caderas a tinta (bajo la cadera / a los lados) + sus fotos de dinos + su Komodo, zigzag · V Venn, Sordes «picnofibras», Jeholopterus, árbol con «ancestro común», CONTINUARÁ.
- Lecciones: (1) rembg en CPU con otra sesión ocupando la PC = horas; **DeepLabV3 de torchvision en GPU** (`mate_gpu.py`) basta para el recorte con borde crema (0,15-0,3 s/cuadro); toma el póster de personas de la pared como persona → caja en `medir.py`. (2) Lanzar 3 `rembg` a la vez los dejó colgados en el import; escalonar. (3) Commons da 429: `commons.py` reintenta con espera; `PYTHONIOENCODING=utf-8` para imprimir.


## Sesiones
- ✅ 24-nov-2026 (Opus 5.5): de la descarga al MP4 en una sesión; mandado por Rayo.
