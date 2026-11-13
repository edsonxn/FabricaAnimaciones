# Cómo vuela un Falcon 9: la misión CRS-30 — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: SIN CANAL (experimental para un canal nuevo de cohetería y exploración espacial; el usuario decide) · sin fecha
- estilo: KIT NUEVO «LÍNEA 3D» (3D de líneas blancas sobre negro, estilo transmisión de SpaceX) → `nucleo/linea3d.py` + `nucleo/linea3d_cohetes.py` · ejemplo: este video
- etapa: MASTER entregado (espera visto bueno del usuario)
- siguiente: el usuario lo ve y elige canal; al aprobar, `biblioteca sfx catalogar` y `limpiar`

## En curso (13-nov-2026, sesión 2)
- MASTER hecho (`salida/cohete_crs30_MASTER.mp4`, 68,7 s, verificar OK CER 0,3 %), en la tele y avisado. Commit 1c2ae87.
- SIN CANAL: no subir. Al terminar, el usuario decide canal (cohetería nuevo).

## Lecciones (detalle en `docs/estilo_linea3d.md` § Errores)
- Viaje de cámara logarítmico: el foco se mueve al ritmo de la distancia (si no, objeto fuera o cámara bajo tierra).
- `curva_suave` no llega exacto al final: el aterrizaje se cierra con un perfil analítico.
- Lo que cae desde km: la cámara lo acompaña y el suelo sube; mirar desde el mar hacia la costa.
- Rótulos que bajan con el objeto pisan el HUD: `dy` grande hacia arriba o al lado contrario.
- Comentarios: no aplica (sin canal). Música de biblioteca `mods_ia_fusion__lyria_1`; 21 SFX de ElevenLabs (355 créditos, cuenta 2).

## Sesiones
- ✅ 13-nov-2026 (2): MASTER. arreglados regreso (foco al ritmo de la distancia), aterrizaje (cohete flotaba 10 m y fuera de cuadro: perfil final exacto en `p_boo` + cámara que lo acompaña desde el mar), órbita (pila centrada, Estación cerca, bug de foco), cierre (cohete a la izquierda con `Cam(centro=)`, viaje al globo sin cámara bajo tierra). Hoja completa (todo_a-d) y promesas (`promesas.md`, hojas promesas_a/b) revisadas y arregladas (MECO, CABO CAÑAVERAL, aire denso). SFX (21 de ElevenLabs, `SFX_ELEVEN` + `eventos_sfx()` en escenas.py) y música (biblioteca `mods_ia_fusion__lyria_1`) + `mezcla` hechos. Sigue: `video` → `final`.
- ◐ 13-nov-2026 (1): guion, voz, kit linea3d nuevo, 10 planos; revisión hasta el seg 43. Cortada por contexto.
