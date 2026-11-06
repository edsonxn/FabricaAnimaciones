# Plan de cámara para toma.py (robotaller_4apps) — copiar la estructura de videos/robotaller_n64/toma.py

Copiar `videos/robotaller_n64/toma.py`; `FIN_VOZ` = fin de `junta_2`; Jefe = `guion.JEFE` (altima_8, micwifi_5, tele_2) con `m.jefe(...)` y
`propios/jefe_limpio.png` (copiar de robotaller_n64/propios). Token de streamer igual que n64. Nunca dos transiciones iguales seguidas (`m.revisar()`).
Las tomas del Robotaller son casi todo fondo oscuro: acercar al texto (z 1,5-2,1); el mensaje del Jefe ≈ centro-abajo.
Clips = capturas/<n>.mp4 (hojas en previews/cap_<n>.jpg). **Celular:** si llegan videos a `%USERPROFILE%\Downloads\Rayo\`, van en
alt_8-9 (app con datos/alertas), micwifi_2-5 (conectado), rayo_2-4 (recibiendo); vertical con `vertical()` de archivo_canal (cuadro sobre su copia borrosa).

| frase | plano |
|---|---|
| gancho_0 | tok full → en «carro» alt_pide z1.8 · «teléfono» mic_pide · «computadora» rayo_pc · «tele» tele_aviso desde 0 |
| gancho_1 | montaje rápido: alt_funciona → mic_jala → tele_aviso desde 4 (robot) |
| gancho_2 | alt_codigo vel 3 z1→1.4 |
| contraste_0 | tok full; «cuadritos» mic_firewall (se ve lo tapado ▒▒▒) |
| contraste_1 | alt_pide desde 2 z1.4→2.2 sobre el texto del Jefe (sin código, solo palabras) |
| altima_0-2 | alt_pide (mensaje completo, z2) → alt_codigo |
| altima_3 | alt_versiones desde 0 → «no funcionó» alt_falla |
| altima_4 | alt_falla z2.2 |
| altima_5 | alt_registro (el log ELM327, z1.6 y paneo) |
| altima_6 | alt_versiones desde 6 («Línea K», checksum) · tok en «sospechabas» |
| altima_7 | alt_versiones vel 3 (v1.1 → 1.3) |
| altima_8 (Jefe) | alt_funciona z2.4 + m.jefe |
| altima_9 | alt_alertas |
| micwifi_0-2 | mic_pide → mic_codigo |
| micwifi_3 | mic_codigo desde 6 (VB-CABLE) |
| micwifi_4 | mic_firewall (red pública / firewall) |
| micwifi_5 (Jefe) | mic_jala z2.4 + m.jefe |
| micwifi_6 | tok full (aplaude) |
| rayo_0 | rayo_pide (hora 09:49) |
| rayo_1-2 | rayo_codigo → rayo_pc (el haz) z1→1.3 |
| rayo_3 | rayo_pc z2 arriba-izq hacia la lista |
| rayo_4 | auto_rayo («Ya abrí Rayo») → rayo_pc z1.8 en Escaner-2.1.apk |
| puente_0-1 | tv_pide → tele_aviso desde 0 (video → pausa → robot) |
| puente_2 | tv_codigo (espera del código; nada del código ni la IP) |
| puente_3 + post 4,6 s | tele_aviso desde 3.6-(lead): el robot dice el aviso; PISTA sfx/tele_1235.mp3 voz=True en efectos.py al terminar puente_3 |
| tele_0 | tele_aviso desde 8 (vuelve el video) → tok |
| tele_1 | ideas_pide |
| tele_2 (Jefe) | ideas_no z2.4 + m.jefe |
| tele_3 | tok full |
| tele_4 | tele_revision |
| tele_5 | tele_protector · «ese de ahí soy yo» z2 al robot del robotaller |
| cuenta_0 | puente_pc → alt_pide (16:58) / ideas (16:55): rótulo 23 h 57 min |
| cuenta_1 | montaje rápido de las 4 (alt_codigo, mic_codigo, rayo_codigo, tv_codigo) + rótulo 838 |
| cuenta_2-3 | rayo_pc / tele_protector / tok |
| cuenta_4 | tok full |
| junta_0-2 | tele_aviso desde 0 + tok; cierre como n64 |
Rótulos (y=.885): «1 · ESCÁNER DEL CARRO» (sin modelo ni año, 5-nov), «MICWIFI · 18 min», «RAYO · 22 min», «PUENTE TV · 12:35», «23 h 57 min», «838 acciones».
