# Amaya: la Independencia de México (guía de estudio) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: NINGUNO — video personal para Amaya (12 años), examen el lun 9-nov-2026. NO se sube a YouTube.
- estilo: ACUARELA PINTADA A MANO POR CÓDIGO (Kuriox, kit de videos/chicle_dentro/) + cara real del usuario (jefe_canadiense) + su voz clonada GUEe… (cuenta 2)
- etapa: guion ✅ · voz ✅ (cuenta 2, 1 045 cr.) · tiempo ✅ (393,9 s, BPM 200) · planos a-j ✅ en hoja · SFX ✅ (sonidos_amaya.py, 161) · música ✅ (biblioteca, 4 tramos) · mezcla ✅ (−14 LUFS) · render ✅ · MASTER ✅ 7-nov 13:29 (6:34) · tele ✅
- siguiente: revisión del usuario; al aprobar `python fab.py amaya_independencia limpiar`

## Sesiones
- alias: amaya_independencia, amaya, el video de Amaya
- vista previa: NO (una sesión directo al MASTER)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion, voz, tiempo, kit, planos a-e | ◐ 7-nov | cortada por contexto (180 mil) tras plano_e |
| 2 | planos f-j, SFX, música, render | ✅ 7-nov | f-j hechos y revisados en hoja (piezas en `piezas_fj.py`); SFX `sonidos_amaya.py` (+ `sonidos_base.py` copiado de chicle); música: chicle_dentro t1, ia_como_ve t1, hormigas_cocina t2, ia_como_ve t4 |

## En curso (checkpoint 7-nov, sesión 1 cortada por contexto)
- HECHO: guion.py (16 escenas; preg1-3 con post 3,2 s de silencio para contestar), voz clonada GUEe… (44/44; CER_MAX_POR_FRASE por fechas en cifras), timeline.json (393,9 s; BPM 200 para no meter huecos).
- Kit: acuarela/comun/personajes/personajes_ia/iconos_ia/utileria/_hoja/sfx_proc copiados de chicle_dentro; fondos_amaya.py = fondos_chicle; `kit_amaya.py` = papá (`papa(im,t,x,yb,alto)`, subclase Papa de Jefe: hueco de la boca recortado por la silueta, sin pico), `cam()` retratos reales (fotos_reales/ + RECORTES, identidad comprobada en previews/retratos_check.jpg), `tarjeta`, `letrero`, `fecha`, `pausa`, `cuenta` (3-2-1), `gente` (personita con cara), `chispas`.
- Planos escritos y revisados con `python _hoja.py <x> t1 t2…` (mirar previews/hoja_<x>.jpg): a gancho, b causas, c grito+preg1+resp1, d truco HMGI, e inicio (últimos arreglos de e SIN volver a mirar: crowd a la izquierda, losa a la espalda, ruta corrida a la izquierda).
- Patrón de cada plano: T_INI = T0(escena); TRAMOS [(t0, funcion)] con desborde 0,6 s; papá chico abajo a la derecha `papa(im, t, 1770, H + 30, alto=330)`; nada importante en x > 1500, y > 750 (lo tapa papá). Palabras con tiempos: previews/palabras.txt.
- FALTA, en orden: plano_f organización (Morelos alumno de Hidalgo, pañuelo/dolor, sitio de Cuautla «+ de 2 meses», Sentimientos de la Nación 1813 con lista LIBRES/SIN ESCLAVITUD/SIN CASTAS, Constitución de Apatzingán 1814, «SIERVO DE LA NACIÓN», 1815, Leona Vicario espía con monedas y carta) · plano_g resistencia (montañas, Guerrero y Guadalupe Victoria aparecen y se esconden, chiste del último día antes de vacaciones, Victoria 1.er presidente) · plano_h consumación (Iturbide REALISTA cambia de bando, Abrazo de Acatempan, Plan de Iguala R-I-U «riu riu» → bandera blanco/verde/rojo, Tratados de Córdoba, 27 SEP 1821 Trigarante entra, pastel de cumpleaños «se regaló un país») · plano_i repaso + preg2/resp2/preg3/resp3 (cuenta regresiva en los silencios, chispas y palomita en respuestas) · plano_j cierre (papá grande, luna/cama «antes de dormir», corazones, «¡TÚ PUEDES, AMAYA!»).
- Luego: SFX sintetizados (sfx_proc.py, anclados a las mismas palabras) · música de la biblioteca (`python fab.py biblioteca sugerir amaya_independencia`, tierna/escolar) · `fab.py amaya_independencia mezcla` · `video --procs 4` · `final` · `verificar` · `python fab.py tele video amaya_independencia master` (segundo plano) · `fab.py avisar`. NO se sube a YouTube (video personal).

- 7-nov 13:29: el render de la sesión 2 se cayó en seg 82 (sin proceso vivo); relanzado con `video --procs 3` → 106/106 en 9 min. MASTER `salida/amaya_independencia_MASTER.mp4`. Whisper no oye «riu riu» en resp3_0 (puede ser falso positivo): revisar al oído.
