# Sexto B: Español para el examen (guía de estudio) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: NINGUNO — video para el grupo SEXTO B de la primaria Benito Juárez de Juchipila, Zac. (examen lun 9-nov-2026). NO se sube a YouTube. Al terminar: tele + aviso + Rayo al celular.
- estilo: acuarela por código (kit de `videos/amaya_independencia/`) + presentadora inventada «la profe Tilde» (maestra chibi; `kit_amaya.papa()` ahora la dibuja a ella, boca con `abre(t)`) + voz NEUTRAL Alberto Rodríguez `l1zE9xgNpUTaQCZzpNJa` (eleven_v4_turbo). La cara y la voz del usuario NO salen.
- etapa: TODO ✅ · MASTER v3 (7-nov 15:21, 7:32): presentador cambiado a HOMBRE («el profe Tilde»: pelo corto, bigote, lentes rojos, chaleco verde, corbata) a pedido del usuario porque la voz es de hombre · Rayo, tele y aviso enviados
- siguiente: revisión del usuario. Mejoras posibles: 3 huecos de ~1 s casi vacíos al arrancar escenas (adverbios ~206 s, «dato chido» ~246 s, autobiografía ~287 s). Al aprobar: `python fab.py amaya_estudio2 limpiar`. NO se sube.

## Sesiones
- alias: amaya_estudio2, amaya 2, el video 2 de Amaya
- vista previa: NO (una sesión directo al MASTER)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | todo hasta el MASTER | ✅ 7-nov | el relevo no se pudo abrir (la app no deja desde una tarea de otra sesión): se terminó aquí; a mitad, cambio del usuario → sexto B, voz Alberto, profe Tilde |

## Hallazgos
- Las 13 fotos (`fuente/`, no van a git) son de ESPAÑOL, no de Historia: autobiografía, adverbios, sílabas/tónica, agudas-graves-esdrújulas, reglas de tilde, carta informal, anécdota. El guion cubre eso.
- Error en el cuaderno (WA0026): «Túnel → esdrújula»; es GRAVE. Va como pregunta trampa (preg2/resp2).

## En curso (checkpoint 7-nov, sesión 1 cortada por contexto)
- HECHO: guion.py (18 escenas; preg1-4 con post 3,2 s), voz 44/44 (CER_MAX por «ene/ese/ele»; TAIL_MAX autobio_0 medido), timeline.json (428,1 s).
- Fotos del cuaderno: `propios/cuaderno/*.jpg` (autobio, adverbios, carta, anecdota, tonica, clasif, esdrujulas, graves, reglas, agudas, silabas1-2, tarea) + recortes `tunel.jpg` (con contraste), `juchipila.jpg` («Yo nací en Juchipila»), `adv_ejemplos.jpg` (4 oraciones). Las fotos originales en `fuente/` (no van a git).
- `piezas_es.py`: `hoja`/`polaroid` (foto real con cinta), `ficha` (sílaba; fuerte = encerrada con plumón rosa), `palabra(sils, x, y, px, t, tonica, t_ap(num o lista por ficha), t_ton, etiquetas, t_eti)`, `mano`/`aplauso`, `camion(bip)`, `sopa(letras LSADF, sale)`, `tira` (película), `hotcake`, `sarten`, `carta(partes=[5 u])`, `gis_txt`.
- Planos (revisados con `python _hoja.py <x> t…` → previews/hoja_<x>.jpg): a gancho (corcho + fotos reales + 6 notitas) · b sílabas/clasif/truco esdrújula/camión de reversa · c preg1 música + reglas (AGUDAS vs GRAVES, hermanos peleados, «siempre» + suéter) · d preg2 TRAMPA túnel + renglón real del cuaderno tachado. `opciones()` está en plano_c (lo importa plano_d).
- Patrón: T_INI = T0(escena); TRAMOS [(t0, f)] con `piezas_fj.base`; `papa(im, t, 1770, H + 30, alto=330)`; nada importante en x > 1500, y > 750. Anclas `ww(esc, frase, palabra, n)`; para ver palabras: imprimir timeline.json (escena/frase/words).
- FALTA, en orden: plano_e adverbios (194,4-255,6: definición verbo + cómo/cuándo/dónde/cuánto; foto `adv_ejemplos` con las 4 oraciones; «pregúntale al verbo» ¿dónde?=LUGAR ¿cuándo?=TIEMPO ¿cómo?=MODO ¿cuánto?=CANTIDAD; sí/también AFIRMACIÓN, no/nunca NEGACIÓN, quizá/probablemente DUDA; «-MENTE» con cerebro tachado; papá ronca mucho=CANTIDAD / siempre=TIEMPO, Zzz) + preg3/resp3 (255,6-274,8: «Juan llegó ayer» → AYER, ¿cuándo? = TIEMPO) · plano_f autobio (274,8-298,8: AUTO+BIO+GRAFÍA, «YO», foto `juchipila`, hechos reales/en orden/sueños y metas) + anécdota (298,8-332,4: película `tira` vs un clip; 5 preguntas QUÉ/DÓNDE/CUÁNDO/QUIÉNES/CÓMO ME SENTÍ; hot cake pegado en el techo, familia riendo) · plano_g carta (332,4-367,2: `carta()` se arma por partes; LUGAR Y FECHA, SALUDO «Querida Amaya», ASUNTO, DESPEDIDA, FIRMA; `sopa()` «La Sopa Aguada Da Fuerza») + preg4/resp4 (367,2-384) · plano_h repaso (384-410,4) + cierre (410,4-428,1: papá grande, «HOY ME GUSTA IR» + «LA SOPA AGUADA DA FUERZA», luna/cama de piezas_fj, «¡TÚ PUEDES, AMAYA!», corazones). Añadir plano_e..h a escenas.py ya está (la lista los incluye).
- Luego: `promesas.md` (fotos del cuaderno, túnel tachado, camión ¡BIP! con SFX de reversa, aplausos con SFX de palmada en es/cue/la) · SFX: copiar el patrón de `sonidos_amaya.py`/`sfx_proc.py` del video 1 (anclar a palabras de ESTE guion; añadir aplauso, bip de reversa) · música: `python fab.py biblioteca sugerir amaya_estudio2` (DISTINTA de la del video 1: chicle_dentro t1, ia_como_ve t1/t4, hormigas_cocina t2) → `usar` por tramo (4 tramos en LYRIA) → armar · `mezcla` · `video --procs 3` · `final` · `verificar` · `python fab.py tele video amaya_estudio2 master` (2.º plano) · `python fab.py avisar "..."`. NO se sube.

## Cambios del usuario (7-nov, vía la sesión principal) y humor
- Dedicado a SEXTO B (no a Amaya), sin papá (ni cara ni voz), voz neutral Alberto Rodríguez, pocos chistes y cortos, todas las técnicas de retención.
- Humor investigado (WebSearch 7-nov): los resultados sobre memes infantiles de México 2026 eran páginas de descubrimiento de TikTok (Roblox, «La Fruta de Guadalupe», Mundial 2026), poco fiables y de moda muy corta → regla: nada de memes dudosos. Usé solo vocabulario gamer que no caduca y el Mundial: (1) «Como el lag cuando ya vas a ganar» (esdrújulas: SIEMPRE tilde), (2) «Tienen mente, pero no cerebro» (-mente = modo), (3) «logro desbloqueado» (cierre). Ejemplo de tónica: «¡campeón!» gritado en el estadio (y es palabra de su cuaderno). Quitados: chistes de papá, mamá y suéter, papá ronca, «se pone de ejemplo solita» con risa, todos los [laughs].
