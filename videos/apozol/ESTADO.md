# Apozol: el pueblo de los dos nombres de agua — ESTADO
- canal: bitacora_perdida · **PROGRAMADO lun 19-oct-2026 14:00 CDMX** (`W_Lznwd9o8k`, publishAt 2026-10-19T20:00:00Z; movido el 12-oct desde el panel por el ciclo de 5 días, verificado en YouTube el 13-oct)
- estilo: kurzgesagt ISOMÉTRICO + mapa de relieve real + personajes 2D (`kz_pers2d`) → docs/estilo_kurzgesagt.md §A · ejemplo: videos/juchipila/ (de aquí salen reg/util/paisajes/mapas y los helpers copiados)
- etapa (11-oct-2026 ~22:30): **TERMINADO y verificado** — `salida/apozol_MASTER.mp4` (1080p, 4:06 = 246,1 s, 529 MB, −14,0 LUFS, voz/fondo 14,2 dB, desfase de audio 0). Guion 42 frases (CER 0 en voz sola; 0,3 % medio sobre la mezcla), 7 escenas, música Lyria, 84 SFX. Revisado con 82 cuadros (1 cada 3 s) y corregidos 8 defectos (ver `REVISION_MASTER.md`). Miniatura lista (`salida/apozol_mini_flowA.jpg`) y `youtube.json` con capítulos reales.
- subida (12-oct 04:31 UTC = 11-oct 22:31 CDMX): subido en privado → `W_Lznwd9o8k` (verificado en YouTube: procesado, 4:07, miniatura, .srt `es` y 15 etiquetas). **Programado el 11-oct** para mar 20-oct 14:00 CDMX (luego movido a lun 19-oct 14:00); registrado en `canales/bitacora_perdida.json` y BITACORA.
- siguiente: nada con YouTube (queda programado). Tras la publicación o cuando se apruebe: `python fab.py apozol limpiar`. Siguiente video de la serie: Jalpa (norte, federal 54).

## Acuerdos con el usuario (11-oct-2026)
- Video SOLO de Apozol, historia desde los inicios (como Juchipila), 4 min; los otros pueblos de la carretera 54 van en videos siguientes. El usuario estará ausente: producir hasta dejar el video listo + miniatura. NO subir ni publicar (preguntar antes).
- Orden de la serie sugerido: Juchipila (hecho) → Apozol → siguiente pueblo hacia el norte (Jalpa) por la federal 54.

## Qué hay (archivo · qué se ve)
| escena | archivo | contenido |
|---|---|---|
| gancho | t01 · mundos_1 | mapa relieve + carretera 54 + lupa Juchipila–Apozol–Jalpa; mitades «agua espumosa» / «en el agua caliente»; montaje (caxcanes, frailes, haciendas, guerra); título |
| valle | t02 · mundos_2 | cañón iso (altímetro 1 265 m, sierra de Morones, río), viaje a antes de 1530, aldea caxcana en terrazas al poniente, tributo a Tlatlán, nombre atl+pozolli |
| atotonilco | t03 · mundos_3 | columna de Oñate (≈1530), encomienda (infografía), San Miguel Atotonilco junto a la poza (≈1538), ecuación atl+totonilli+co, ruinas del templo de Santiago, cielo rojo |
| mixton | t04 · mundos_4 (generado por `_gen4.py` desde `_mundos_4_plantilla.py`) | mapa de la rebelión, peñol iso + recuadro, MILES y Tenamaxtli, Alvarado (retrato real), Mendoza y ejército, leyenda de Santiago, caída 1542, borde del vacío |
| paz | t05 · mundos_5 | amanecer de la paz, frailes con la fundación, «Apozol de Santa María Magdalena», cédula 1597 (tierras), archivo 1806 (Pérez Gavilán), papeles vs flechas |
| haciendas | t06 · mundos_6 | valle de haciendas, La Purísima + caña (Porfiriato), casa grande 1775 que se levanta, piloncillo 2D, hotel 1997 |
| hoy | t07 · mundos_7 | decreto 1863, línea de tiempo 1863→1918 a escala, balanza (Estrada Borja), Apozol hoy 2 600/6 000, plaza (laurel, Juárez), fiesta de la Ascensión, tastoanes, agua, mapa «¿qué pueblo sigue?» |

## Falta (en orden)
- [x] Voz, seleccionar, tiempo: hechos (CER 0 en las 42 frases; no hizo falta ALIAS_QA)
- [x] Escenas revisadas con la timeline real; `_humo.py 2` sin excepciones (solo negro intencional en 0 s y en el fundido final)
- [x] Música Lyria / sfx / mezcla HECHOS ( `$env:PYTHONPATH="C:\FabricaAnimaciones\videos\apozol;C:\FabricaAnimaciones\nucleo"; python ..\..\nucleo\lyria_tramos.py todo` (2 tramos en `LYRIA["tramos"]`) → `python fab.py apozol sfx` → `mezcla` (voz/fondo ≥ 11 dB, −14 LUFS)
- [x] (HECHO) Render: pedir cerrar chatterbox_server/app y panel pesado; `python fab.py apozol video` (12 procs) → `final` → `verificar`; revisar MASTER con hoja 2×3 (1 cuadro/3 s) y `docs/estilo_kurzgesagt.md` § «ERRORES A NO REPETIR»; anotar en REVISION_MASTER.md
- [x] Miniatura HECHA (Flow, Nano Banana 2 Lite, 0 puntos; 11-oct): `salida/apozol_mini_flowA.jpg` 1280x720, «APOZOL / DOS NOMBRES DE AGUA» (se lee a 170 px). Prompts A/B en `prompt_miniatura.md`; el proyecto de Flow quedó con 2 variantes (se eligió la 2.ª).
- [x] `youtube.json` con capítulos reales y `.srt` listos · subir en PRIVADO solo si el usuario lo pide

## Lecciones de este video (solo lo no obvio)
- Fuentes de Apozol en conflicto (resueltas en guion.py): nombre «agua espumosa» (otras: «agua de maíz», «camino quebrado donde hay agua»); fundación 1530/1538/1554; la ratificación de los frailes no se fecha; «muchos se arrojaron al vacío» y Santiago a caballo = tradición/leyenda (se dice así). NO afirmar Pueblo Mágico ni cifras de migración.
- Cifras: cabecera 2 608, municipio 6 260 (censo 2020, Wikipedia ES); altitud 1 265 m; «unos dos mil seiscientos / unos seis mil» en la narración.
- No inventar números en pantalla: «MILES» (no «4 000») para los guerreros del peñol.
- Los `T()` buscan por prefijo en las palabras del GUION (con puntuación), no en Whisper: cualquier palabra escrita en la frase sirve de ancla.
- `K2.busto` dibuja en capa 1: fondos de medallón con `capa=1` (en capa 2 lo tapan). `lz.trazo` no tiene `alfa=`: usar color RGBA.
- El kit `kz_pers2d` llama «brazos="arriba"» pero la bandera/objeto va aparte: no flotar telas sobre las cabezas (asta propia).
- Miniatura: el navegador integrado NO tenía sesión de Google; se usó Claude in Chrome (la cuenta PRO de Flow ya estaba abierta). `find` de Chrome gastó cuota y topó con el límite de 5 h de la cuenta.
