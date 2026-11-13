# -*- coding: utf-8 -*-
"""Copia COMPARTIBLE de la Fábrica (22-oct-2026, pedido del usuario: «compartir el proyecto con otra persona sin que vea mis
canales, solo los estilos; que pueda crear sus propios videos y ver el panel con SUS canales»).

    python fab.py compartir                          arma/actualiza la copia limpia (E:\\FabricaCompartida o C:\\FabricaCompartida)
    python fab.py compartir --destino D:\\otra        en otra carpeta
    python fab.py compartir --subir <url .git>       además la sube (commit + push) a ese repo privado de GitHub

Qué lleva: el motor (`nucleo/`, `fab.py`, `API.md`), las plantillas de video, los docs de ESTILO y de producción y el CÓDIGO
(guion/escenas, sin voz, imágenes ni render) de los videos de referencia de cada estilo en `ejemplos/`.
Qué NO lleva: `canales/` (JSON, métricas, tokens, fórmulas, arte), `BITACORA.md`, los demás videos, la biblioteca de música/SFX,
el Estudio comercial, los docs de estrategia (qué funciona, ideas, buenos días, historial…), la memoria de Claude.
Los nombres de tus canales, sus alias e IDs, tu correo y tu dominio se cambian por etiquetas neutras (SUSTITUCIONES) y al final
`revisar_fugas` busca cualquier resto (y claves de API): si encuentra algo, NO sube nada.
La plantilla de lo que es solo de la copia (CLAUDE.md, LEEME.md, requirements.txt, .gitignore, canales/LEEME.md) vive en `compartir/`.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLANTILLA = os.path.join(RAIZ, "compartir")
MARCA = ".fabrica_compartida"          # solo se vacía una carpeta que tenga esta marca (o vacía / nueva)

# Videos cuyo CÓDIGO va como ejemplo de un estilo (columna «Copiar de» de CLAUDE.md). Nunca: anuncios del negocio del usuario
# (duo_promo, duos_promo), privados de reserva (wow_clases_ocultas, wow_pistas_futuro) ni reels de su página.
EJEMPLOS = [
    "independencia_mx", "sol_apagado_8min", "historia_60", "historia_jalisco", "historia_aguascalientes", "historia_egipto", "primer_foton",
    "neandertales", "un_dia_30mil", "voynich", "informante_2027", "secreto_ia", "jalpa", "bichos_invierno", "arana_techo",
    "wow_curiosidades_kalimdor", "er_radagon_atrocidades", "tes_misiones_daedricas", "banjo_tooie", "majora_mask", "freno_enojo",
    "guason_fumado", "sociedad_1200", "got_joffrey", "mods_ia_fusion", "terror_ben_drowned", "gota_bucle", "pelea_meme",
    "gato_cobarde", "wow_tres_noches", "lol_worlds_2026", "ballena_estomago", "euphoria_robots", "cohete_crs30",
    "lol_semana2", "ig_lyon_worlds", "cfo_kc_jugadas", "lol_worlds_tl_al",          # Crónicas de League of Legends (7-nov-2026)
]
NO_EN_EJEMPLO = {"ESTADO.md", "youtube.json"}           # publicación y diario del canal

DOCS = [
    "api_kz.md", "apis.md", "flujo_produccion.md", "musica_biblioteca.md", "panel.md", "publicacion.md", "sesiones.md",
    "voz.md",
] + [f"estilo_{e}.md" for e in (
    "acuarela_pincel", "analisis_tactico", "boceto_gota", "boceto_guache_mapa", "cartoon90", "diseccion", "documental", "grabado_peste", "guache_meme", "kurzgesagt",
    "linea3d",
    "linea_neon", "noir", "noir_color", "pegatina_flow", "rayosx_tecno", "secuencia_flow", "secuencia_fx", "secuencia_yt",
    "terror_crt")]

RAIZ_SUELTOS = ["fab.py", "API.md", ".claude/settings.json", "modelos/bajar_t3.sh"]
NO_NUCLEO = {"nucleo/estadisticas.html.bak", "nucleo/_fx_v3.txt", "nucleo/datos/musica_biblioteca.json",
             "nucleo/datos/sfx_biblioteca.json", "nucleo/compartir.py"}
SKILLS = ["comprimir-video", "analizar-uso-panel", "actualizar-canales", "cronicas-lol"]

# alias de canal -> alias neutro (también en rutas: nucleo/panel_fondos/<alias>.svg)
ALIAS = {
    "bitacora_perdida": "ej_isometrico", "cronopapel": "ej_guache", "sapiens_con_wifi": "ej_doodle", "kuriox": "ej_kuri",
    "edsonxn": "ej_misterio", "pieza_oculta": "ej_plastilina", "wild_next_door": "ej_bichos_en",
    "cronicas_gaming": "ej_gaming", "cronicas_de_warcraft": "ej_wow", "cronicas_warcraft": "ej_wow",
    "runa_caida": "ej_eldenring", "cronicas_tamriel": "ej_skyrim", "cuerpo_en_neon": "ej_neon",
    "cuentas_pendientes": "ej_neon", "historias_mx": "tu_pagina",
}
# (regex, reemplazo) en orden: primero nombres largos
SUSTITUCIONES = [
    (r"Bit[áa]cora Perdida", "Canal isométrico"), (r"BIT[ÁA]CORA PERDIDA", "CANAL ISOMÉTRICO"),
    (r"Bitácora(?=[\s,.;:)»'\"`])", "Canal isométrico"),          # el archivo es BITACORA.md: no se toca
    (r"Cronopapel", "Canal guache"), (r"CRONOPAPEL", "CANAL GUACHE"),
    (r"Sapiens con Wifi", "Canal doodle"),
    (r"Kuriox", "Canal Kuri"),
    (r"Edsonxn", "Canal misterio"), (r"\bEdson\b", "el autor"),
    (r"LogIA", "Canal noir"),
    (r"Plas?titube", "Canal plastilina"),
    (r"Wild Next Door", "Canal bichos (inglés)"), (r"\bWND\b", "bichos-EN"),
    (r"Cr[óo]nicas del [Gg]aming", "Canal gaming retro"),
    (r"(?i)cr[óo]nicas de warcraft", "Canal WoW"), (r"(?i)cr[óo]nicas de tamriel", "Canal Skyrim"),
    (r"Runa Ca[íi]da", "Canal Elden Ring"),
    (r"Cuerpo en Ne[óo]n", "Canal neón"), (r"@cuerpoenneon", "@tucanal"), (r"Cuentas Pendientes", "Canal neón"),
    (r"Historias Perdidas de M[ée]xico", "tu página de Facebook"),
    (r"Qu[ée] [Pp]asa en Juchipila", "tu página de Facebook local"),
    (r"CRONICAS10", "TUCODIGO"), (r"Overgear", "Patrocinador"), (r"overgear", "patrocinador"),
    (r"jairedson5@gmail\.com", "tu-correo@ejemplo.com"), (r"jairedson5?\b", "tu-cuenta"),
    (r"clicknbusiness\.com\.mx", "tu-dominio.com"), (r"mx\.clicknbusiness", "com.tudominio"),
    # restos en minúsculas (listas de señales, descripciones de firmas; 7-nov-2026)
    (r"(?i)clicknbusiness", "tudominio"), (r"(?i)cronicas10", "tucodigo"),
    (r"(?i)runa ca[íi]da", "canal elden ring"), (r"(?i)bit[áa]cora perdida", "canal isométrico"),
    (r"E:\\\\?PaginaFace", r"C:\\TuPagina"),
    (r"\bjaire\b", "usuario"), (r"3 cuentas Pro", "varias cuentas"),
    (r"\bUC[A-Za-z0-9_-]{22}\b", "UCxxxxxxxxxxxxxxxxxxxxxx"),
    # alias con forma de código: `logia` es también palabra española («una logia secreta»), solo pegado a comillas/rutas
    (r"(?<=[\"'`/=\[(])logia(?=[\"'`./\])_,:])", "ej_noir"), (r"(?<=--canal )logia\b", "ej_noir"),
    (r"(?<=\bkuriox )logia\b|(?<=ej_kuri )logia\b", "ej_noir"), (r"\blogia(?=_)", "ej_noir"), (r"(?<=_)logia\b", "ej_noir"),
] + [(rf"(?<![A-Za-z0-9]){re.escape(a)}(?![A-Za-z0-9])", n) for a, n in sorted(ALIAS.items(), key=lambda x: -len(x[0]))]
_SUST = [(re.compile(p), r) for p, r in SUSTITUCIONES]

_EJ = "|".join(sorted(EJEMPLOS, key=len, reverse=True))
_A_EJEMPLOS = re.compile(rf"videos([\\/]+)({_EJ})\b")

TEXTO = {".py", ".md", ".html", ".json", ".txt", ".js", ".css", ".svg", ".ps1", ".sh", ".csv", ".yml", ".yaml", ".toml",
         ".ini", ".cfg"}

# lo que nunca debe quedar (sin distinguir mayúsculas salvo LogIA)
FUGAS = [r"bit[áa]cora perdida", r"cronopapel", r"sapiens con wifi", r"kuriox", r"edsonxn", r"plas?titube",
         r"wild next door", r"cr[óo]nicas del gaming", r"cr[óo]nicas de (warcraft|tamriel)", r"runa ca[íi]da",
         r"cuerpo ?en ?ne[óo]n", r"historias perdidas", r"pasa en juchipila", r"clicknbusiness", r"jairedson",
         r"paginaface", r"overgear", r"cronicas10", r"\buc[a-z0-9_-]{22}\b(?<!ucxxxxxxxxxxxxxxxxxxxxxx)"] + \
        [rf"\b{re.escape(a)}\b" for a in ALIAS if a != "historias_mx"]
FUGAS_EXACTAS = [r"LogIA", r"[\"'`/]logia[\"'`./]",
                 # claves y credenciales
                 r"AIza[0-9A-Za-z_-]{30,}", r"\bsk_[0-9a-f]{30,}", r"\bghp_[0-9A-Za-z]{30,}", r"-----BEGIN [A-Z ]*PRIVATE KEY",
                 r"\"refresh_token\"\s*:", r"\"client_secret\"\s*:\s*\"[^\"]{8,}"]
_FUGAS = [re.compile(p, re.I) for p in FUGAS] + [re.compile(p) for p in FUGAS_EXACTAS]


def _git(*args, cwd=RAIZ, check=True):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode:
        sys.exit(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def archivos_del_proyecto():
    """Lo versionado + lo nuevo sin ignorar (módulos aún sin commit): nunca medios, voz ni secretos (.gitignore)."""
    salida = _git("ls-files", "-z") + _git("ls-files", "-z", "--others", "--exclude-standard")
    return sorted({p.replace("\\", "/") for p in salida.split("\0") if p and os.path.isfile(os.path.join(RAIZ, p))})


def elegir(rutas):
    """(origen relativo, destino relativo) de lo que entra en la copia."""
    sale = []
    for r in rutas:
        if r in RAIZ_SUELTOS:
            sale.append((r, r))
        elif r.startswith("nucleo/") and r not in NO_NUCLEO and "/uso_panel/" not in r:
            sale.append((r, r))
        elif r.startswith("docs/") and (r[5:] in DOCS or r.startswith("docs/ejemplos/")):
            sale.append((r, r))
        elif re.match(r"videos/_plantilla[^/]*/", r):
            sale.append((r, r))
        elif r.startswith(".claude/skills/") and r.split("/")[2] in SKILLS:
            sale.append((r, r))
        else:
            m = re.match(r"videos/([^/]+)/(.+)$", r)
            if m and m.group(1) in EJEMPLOS and os.path.basename(r) not in NO_EN_EJEMPLO:
                sale.append((r, f"ejemplos/{m.group(1)}/{m.group(2)}"))
    # skills: carpetas que git no lista (sin versionar e ignoradas por .claude/)
    for s in SKILLS:
        base = os.path.join(RAIZ, ".claude", "skills", s)
        for dp, _, fs in os.walk(base):
            if "__pycache__" in dp:
                continue
            for f in fs:
                rel = os.path.relpath(os.path.join(dp, f), RAIZ).replace("\\", "/")
                if (rel, rel) not in sale:
                    sale.append((rel, rel))
    return sale


def limpiar_texto(t):
    for rx, rep in _SUST:
        t = rx.sub(rep, t)
    return _A_EJEMPLOS.sub(lambda m: f"ejemplos{m.group(1)}{m.group(2)}", t)


def limpiar_ruta(rel):
    partes = rel.split("/")
    for i, p in enumerate(partes):
        base, ext = os.path.splitext(p)
        partes[i] = dict(ALIAS, logia="ej_noir").get(base, base) + ext
    return "/".join(partes)


def preparar_destino(dest):
    if os.path.isdir(dest) and os.listdir(dest) and not os.path.exists(os.path.join(dest, MARCA)):
        sys.exit(f"{dest} ya existe y no es una copia compartible (falta {MARCA}): elige otra carpeta con --destino")
    os.makedirs(dest, exist_ok=True)
    for n in os.listdir(dest):                       # todo menos .git: la copia se rehace entera cada vez
        if n == ".git":
            continue
        p = os.path.join(dest, n)
        shutil.rmtree(p) if os.path.isdir(p) and not os.path.islink(p) else os.remove(p)


def copiar(pares, dest):
    for orig, rel in pares:
        rel = limpiar_ruta(rel)
        destino = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        src = os.path.join(RAIZ, orig)
        if os.path.splitext(orig)[1].lower() in TEXTO:
            with open(src, encoding="utf-8", errors="surrogateescape", newline="") as f:
                t = f.read()
            with open(destino, "w", encoding="utf-8", errors="surrogateescape", newline="") as f:
                f.write(limpiar_texto(t))
        else:
            shutil.copy2(src, destino)
    # lo que es solo de la copia
    for dp, _, fs in os.walk(PLANTILLA):
        for f in fs:
            src = os.path.join(dp, f)
            rel = os.path.relpath(src, PLANTILLA)
            if f == "gitignore.txt":                 # con punto ignoraría cosas en ESTE repo
                rel = os.path.join(os.path.dirname(rel), ".gitignore")
            destino = os.path.join(dest, rel)
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.copy2(src, destino)
    # bibliotecas vacías: cada quien paga y cataloga su música (no se repite la tuya en canales ajenos)
    for n in ("musica_biblioteca.json", "sfx_biblioteca.json"):
        with open(os.path.join(dest, "nucleo", "datos", n), "w", encoding="utf-8") as f:
            f.write('{\n  "piezas": {},\n  "actualizado": ""\n}\n')
    # galería de estilos: fuera el anuncio de la app/negocio del usuario (su doc y su video no van en la copia)
    gal = os.path.join(dest, "nucleo", "datos", "galeria.json")
    if os.path.exists(gal):
        with open(gal, encoding="utf-8") as f:
            g = json.load(f)
        g["estilos"] = [e for e in g.get("estilos", []) if not str(e.get("video", "")).startswith("duo")]
        with open(gal, "w", encoding="utf-8") as f:
            json.dump(g, f, ensure_ascii=False, indent=1)
    for d in ("canales", "videos"):
        os.makedirs(os.path.join(dest, d), exist_ok=True)
    with open(os.path.join(dest, MARCA), "w", encoding="utf-8") as f:
        f.write("Copia compartible de la Fábrica de Animaciones (nucleo/compartir.py). Se rehace entera en cada exportación.\n")


def revisar_fugas(dest):
    """[(ruta, línea, texto)] de cualquier resto de los canales o credenciales en la copia."""
    malas = []
    for dp, dns, fs in os.walk(dest):
        dns[:] = [d for d in dns if d != ".git"]
        for f in fs:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, dest).replace("\\", "/")
            for rx in _FUGAS:
                if rx.search(rel):
                    malas.append((rel, 0, "(nombre de archivo)"))
            if os.path.splitext(f)[1].lower() not in TEXTO:
                continue
            with open(p, encoding="utf-8", errors="replace") as fh:
                for n, linea in enumerate(fh, 1):
                    if any(rx.search(linea) for rx in _FUGAS):
                        malas.append((rel, n, linea.strip()[:150]))
    return malas


def main():
    ap = argparse.ArgumentParser(description="Copia compartible de la Fábrica (sin tus canales)")
    defecto = r"E:\FabricaCompartida" if os.path.isdir("E:\\") else r"C:\FabricaCompartida"
    ap.add_argument("--destino", default=defecto)
    ap.add_argument("--subir", metavar="URL", help="repo git privado al que hacer push (p. ej. https://github.com/<tu>/fabrica-estilos.git)")
    a = ap.parse_args()
    dest = os.path.abspath(a.destino)
    if os.path.normcase(dest).startswith(os.path.normcase(RAIZ)):
        sys.exit("El destino no puede estar dentro del proyecto")

    pares = elegir(archivos_del_proyecto())
    preparar_destino(dest)
    copiar(pares, dest)
    ej = sorted({r.split("/")[1] for _, r in pares if r.startswith("ejemplos/")})
    falta = sorted(set(EJEMPLOS) - set(ej))
    print(f"Copia en {dest}: {len(pares)} archivos del proyecto + plantilla; {len(ej)} ejemplos de estilo")
    if falta:
        print(f"(aviso) ejemplos sin archivos versionados: {', '.join(falta)}")

    malas = revisar_fugas(dest)
    if malas:
        print(f"\n✗ {len(malas)} restos de tus canales o credenciales; NO se sube nada. Añade la sustitución en nucleo/compartir.py:")
        for rel, n, t in malas[:60]:
            print(f"  {rel}:{n}  {t}")
        sys.exit(1)
    print("✓ Sin restos de tus canales, correo, dominio ni claves")

    if not os.path.isdir(os.path.join(dest, ".git")):
        _git("init", "-b", "main", cwd=dest)
    _git("add", "-A", cwd=dest)
    if _git("status", "--porcelain", cwd=dest).strip():
        _git("commit", "-q", "-m", "Fábrica de Animaciones: actualización del motor y los estilos", cwd=dest)
        print("Commit hecho en la copia")
    else:
        print("Sin cambios desde la última exportación")
    if a.subir:
        remotos = _git("remote", cwd=dest).split()
        _git("remote", "set-url" if "origin" in remotos else "add", "origin", a.subir, cwd=dest)
        r = subprocess.run(["git", "push", "-u", "origin", "main"], cwd=dest)
        if r.returncode:
            sys.exit("No se pudo subir: ¿existe el repo (privado) en GitHub y tienes permiso?")
        print(f"Subido a {a.subir}")


if __name__ == "__main__":
    main()
