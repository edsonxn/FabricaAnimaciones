# Apozol — revisión del MASTER (11-oct-2026)
Hoja 2×3 con un cuadro cada 3 s (82 cuadros, `previews/master_00..13.jpg`) sobre el MASTER 1080p de 4:06.

## Defectos hallados y corregidos (re-render de 27 segmentos de 3 s)
| tiempo | defecto | arreglo |
|---|---|---|
| 7 s | mitad derecha vacía antes de «el otro» | gotas flotando en toda la pantalla |
| 58-64 s | etiquetas «soldados españoles / aliados indígenas» sobre la aldea (señalaban mal) | junto a la columna |
| 94 s | ondas de la rebelión encima de las etiquetas de los pueblos | menos radio y alfa |
| 109 s | retrato de Alvarado con franja estirada en el borde superior | `nucleo/datos/retratos/alvarado.jpg` recortado (original en `alvarado_orig_con_franja.jpg`) |
| 133 s | bajada a negro entre «Mixtón» y «paz» (cuadro negro) | quitado el `post_fundido_negro` de la toma |
| 169 s | ~2 s de pantalla vacía antes de flechas y papeles | aparecen desde el inicio de la toma |
| 175 s | isla de haciendas diminuta con 60 % de pantalla vacía | cámara más cerca |
| 226-231 s | cohetes casi invisibles tras el papel picado | más grandes y más abajo |

## Aceptado (no bloquea)
- Fundidos cruzados de 0,5-0,7 s entre escenas muestran un instante de doble imagen (tiempo viajero, tributo → rápidos).
- Etiquetas que entran/salen encogiéndose (`U.salida`) pasan por tamaño pequeño en ~0,2 s.
- Whisper sobre la MEZCLA marca 3 frases con CER 2-4 % («tierras»→«tiaras», «se hervía»→«servía»); en la voz sola salen bien (CPU large-v3 comprobado): es música/SFX.
- La toma del peñol (iso) es una pirámide escalonada estilizada, no un cerro natural; el fondo de la noche de Santiago es oscuro por diseño.
