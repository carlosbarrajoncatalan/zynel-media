# Herramientas de producción ZYNEL (se regeneran las piezas con esto)

- `reels/`: motor de reels en HTML (Playwright, 1080x1920, 30 fps) + audio (efectos suaves y música original). `render.py <nombre> <duración>` renderiza; `mk_c.py` genera el audio. Los clips de vídeo del cliente se extraen a fotogramas JPG (`ffmpeg -vf scale=1080:1920`) en `v/f/` y `v/g/`.
- `piezas/`: generadores de page posts (`pieces.py`) y carruseles (`gen.py`) y logos cuadrados (`sq_*.png`).
- Normas: pastilla de color con la Z del color del fondo (Z al 71 % de la pastilla), cierre "HABLEMOS EN ZYNEL" + "RRSS | WEB | MARKETING | IA" en blanco o amarillo, reels < 20 s, sin música estridente.
- Necesita la tipografía Space Grotesk (`brand/fonts`).
