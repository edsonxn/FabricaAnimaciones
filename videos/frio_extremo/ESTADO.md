# ¿Cómo sobrevivían los humanos prehistóricos al FRÍO extremo? — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: sapiens_con_wifi · meta: vie 23-oct-2026 14:00 CDMX (hueco del panel de canales, ciclo 5 d tras `sin_medicina` 18-oct)
- estilo: **pegatina_flow** (21-oct-2026, petición del usuario) → docs/estilo_pegatina_flow.md; copiar de `videos/wow_darrowshire/` y `videos/jalpa/`
- etapa: SUBIDO y PROGRAMADO vie 23-oct-2026 14:00 CDMX (psl-j5NFljk, privado con publishAt), MASTER 11:51 revisado
- siguiente: medir a los 7 días (30-oct) contra `sin_medicina`; `fab.py frio_extremo limpiar` cuando el usuario lo apruebe (segmentos/ 3 GB)

## Sesiones (plan de tramos · «continúa el video <alias>» retoma aquí · protocolo docs/sesiones.md)
- alias: frío extremo, frio extremo, sapiens pegatina, sobrevivir al frío
- vista previa: NO; el avance se ve en 🎞 Montaje del panel tras cada escena (`python fab.py frio_extremo montaje`), aviso por voz
- leer al empezar: docs/estilo_pegatina_flow.md (entero), este ESTADO, `videos/wow_darrowshire/escenas.py` (grep) como modelo de tomas
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | (17-oct) datos, guion 15 min, voz | ✅ 17-oct | luego reconvertido |
| 2 | (21-oct, UNA sesión, plan MAX) guion a 11 min, voz, Flow, recorte, animación, Lyria, sfx, mezcla, render, subir | ✅ 21-oct | render 1 h 36 min + 10 tramos rehechos tras el rigor; subido https://youtu.be/psl-j5NFljk |

## Decisiones del episodio
- 17-oct: tema «frío extremo» (ref. Mango Explica SP «iglús a –50 °C» ×13,6), voz Dan (Chatterbox), Lyria, subir en PRIVADO
- 21-oct (el usuario): pasar a **pegatina Flow**, **11 min**, **1 sesión**, avance en el Montaje del panel. Guion recortado quitando
  27 frases enteras (2 557 → 2 097 palabras); la voz vieja se reasignó por texto (`_remap_voz.py`); solo `ropa_5` es nueva.
  Las 4 frases que no pasaban (hielo_1, ropa_5, ropa_21, tu_1 viejas) quedaron fuera o reescritas. Copia: `guion_15min.py.bak`.

## Hecho (21-oct-2026)
- Rigor del MASTER: 237 cuadros (1 cada 3 s) + blackdetect/freezedetect limpios; 10 arreglos rehechos por tramos (Sapi en primer plano en el glaciar, manos azules sin zoom, fantasma reubicado, huecos vacíos en Sudáfrica/refugio/Siberia, cazadora en cuadro, tachón que se va, cúpula más rápida, Sapi lejos de la planta).

## Mapa de piezas (número → pose)
- sapi_hoja 00 calma · 01 habla · 02 señala (der.) · 03 tirita · 04 sorpresa · 05 antorcha
- neandertal_hoja 00 brazos cruzados · 01 golpea pedernal · 02 sopla fuego · 03 fogata con humo · 04 capa · 05 carga carne · 06 tirita
- cazadora_hoja 00 cose · 01 lanza · 02 carga huesos · 03 aviva fuego · 04 raspa piel en bastidor · 05 explica (señala arriba)
- inuit_hoja 00 alza bloque · 01 corta nieve · 02 gatea (izq.) · 03 sentado con lámpara · 04 saluda · 05 arpón
- gente_hoja 00 abuela · 01 niño · 02 madre con bebé · 03 chico con odre · 04 hombre echa hueso al fuego · 05 bosteza
- grupo_dormir 00 familia dormida · 01 tres calentándose · 02 vigía · 03 dos niños bajo la piel
- fauna_hoja 00 rinoceronte · 01 reno · 02 bisonte · 03 (bisonte+caballo, NO usar) · 04 caballo · 05/06 lobos · 07 oso · 08 liebre · 09 foca
- huesos_mamut 00 cráneo frente · 01 cráneo lado · 02 mandíbula · 03/04 colmillos · 05 fémur · 06 omóplato · 07 pelvis · 08 vértebra · 09 costilla · 10 mandíbulas apiladas · 11 piel enrollada
- iglu_utileria 00/01 bloques · 02 iglú · 03 cuchillo de hueso · 04 lámpara de foca · 05 manta · 06 trineo · 07 arpón · 08 botas · 09 capucha · 10 pila de bloques · 11 vaho
- moderno_hoja 00 chamarra · 01 radiador · 02 colchón · 03 termómetro · 04 celular · 05 aguja · 06 bufanda · 07 botas · 08 bolsa de agua · 09 foco · 10 té · 11 gorro
- utileria_fuego 00 fogata chica · 01 fogata grande · 02 pedernal · 03 pirita · 04 lámpara · 05 hueso · 06 tuétano · 07 manojo de pasto · 08 cama de pasto · 09 huesos ardiendo · 10 odre · 11 vaso de hueso · 12 olla con nieve · 13 grasa · 14 carne asada · 15 brasas
- utileria_ropa 00 aguja de hueso · 01 tendón · 02 cuentas · 03 parka oscura · 04 pantalón · 05 botas · 06 gorro con cuentas · 07 piel · 08/09 mitones · 10 raspador · 11 parka de caribú · 12 figurilla · 13 piojo café · 14 piojo gris · 15 pelo · 16 cuero cosido
- ciclos (todos a la derecha): sapi_camina 8, cazadora_camina 8, cazador_corre 8, mamut_camina 6, renos_camina 6, cuervos_aleteo 6

## Falta
- [x] todo lo de producción; [ ] medir el 30-oct; [ ] `limpiar` al aprobar

## Archivos clave
- `guion.py` (narración, hechos, FICHA, LYRIA), `_prompts.py`, `prompts.json`, `escenas.py`, `piezas/`, `imagenes/`, `hojas/`

## Lecciones de este video (solo lo no obvio)
- YouTube rechaza (400 invalidTags) etiquetas que suman > 500 caracteres (las de varias palabras cuentan 2 de comillas).
- Una toma llamada `cv2` tapó `import cv2`: prefijos de 3 letras.
- Recortar un guion ya grabado: quitar frases ENTERAS y reasignar las tomas por texto (`_remap_voz.py`) = 0 voz nueva.
- Fuera de la voz: «ADN» (Whisper oye «Adán»), «Lascaux», «denisovanos», Kostenki/Sungir/Wonderwerk/Yana: se dice el lugar, no el nombre.

## Cierre (regla del 12-oct-2026)
- [x] subido, miniatura, programado y registrado (`canales/sapiens_con_wifi.json`, BITACORA)
- [x] HALLAZGOS y mejoras documentados (docs/estilo_pegatina_flow.md §9, canales/formula/sapiens_con_wifi.md)
